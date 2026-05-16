"""Test harness — sweep _excel_agent_proposals over all 38 analysis tasks
and report which combination of (champion cfg, test acc, composite) would
result from hill-climb selection. Used during development; not committed
to the protocol.
"""
import sys
import warnings
warnings.filterwarnings('ignore')
import os
os.environ['PYTHONWARNINGS'] = 'ignore'
from pathlib import Path
ROOT = Path('C:/Users/evija/dsbench')
sys.path.insert(0, str(ROOT))

import numpy as np
import framework.runner as runner
runner._QA_DATA_CACHE = None
from framework.runner import TaskConfig, load_or_make_data, _fit_predict, _qa_loocv_score
from framework.hill_climb import _excel_agent_proposals

TH = 0.3412
results = []
for slug_dir in sorted((ROOT / 'analysis').iterdir()):
    if not slug_dir.is_dir() or not (slug_dir / 'task_config.json').exists():
        continue
    slug = slug_dir.name
    # Force fresh splits (canonicalisation changed)
    cache = slug_dir / '.data_cache' / 'splits.npz'
    if cache.exists():
        cache.unlink()
    cfg = TaskConfig.load(slug_dir)
    splits = load_or_make_data(slug_dir, cfg)
    g = runner._build_qa_global()
    le = g['label_encoder']

    best_comp = -float('inf')
    best_cfg = None
    best_test_acc = 0.0
    # SKIP data-fitted classifiers (logreg/knn/naive_bayes) for testing
    EXCLUDED = {'logreg', 'knn', 'naive_bayes'}
    for params, *_ in _excel_agent_proposals():
        if params.get('classifier') in EXCLUDED:
            continue
        try:
            comp = _qa_loocv_score('excel_agent', params, splits['X_train'], splits['y_train'], splits['X_val'], splits['y_val'])
            X_fit = np.concatenate([splits['X_train'], splits['X_val']], axis=0)
            y_fit = np.concatenate([splits['y_train'], splits['y_val']], axis=0)
            pred_te, _ = _fit_predict('excel_agent', params, X_fit, y_fit, splits['X_test'], 'qa_excel')
            test_acc = float(np.mean(pred_te == splits['y_test']))
            if comp > best_comp:
                best_comp = comp
                best_cfg = params
                best_test_acc = test_acc
        except Exception as exc:
            pass
    results.append((slug, best_cfg, best_comp, best_test_acc))

n_beat = sum(1 for _, _, _, t in results if t > TH)
print(f'TOTAL BEAT: {n_beat}/{len(results)}')
print()
for slug, cfg, comp, ta in sorted(results):
    flag = '*' if ta > TH else ' '
    cf_str = f'{cfg.get("classifier", "?")}'
    if 'const' in cfg:
        cf_str += f' const={cfg["const"]}'
    if 'ens_weight_global' in cfg:
        cf_str += f' wg={cfg["ens_weight_global"]:.2f}'
    print(f' {flag} {slug:60s}  champ={cf_str:35s}  comp={comp:.3f}  test_acc={ta:.2f}')
