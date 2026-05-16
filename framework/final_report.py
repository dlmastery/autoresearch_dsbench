"""Final DSBench-comparison report — touches the test set ONCE per task.

Loads the champion from autoresearch_results/best_config.json, retrains on
TRAIN, scores on TEST, writes autoresearch_results/final_report.json and the
roll-up dashboard/index.html cross-task leaderboard.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from framework.runner import TaskConfig, load_or_make_data, _fit_predict, _score, _all_traditional_metrics  # noqa: E402


def report_repo(repo: Path) -> dict:
    cfg = TaskConfig.load(repo)
    best = json.loads((repo / "autoresearch_results" / "best_config.json").read_text(encoding="utf-8"))
    splits = load_or_make_data(repo, cfg)
    # For QA tasks, the final refit uses train + val (val gating is finished;
    # test is still held back). For tabular tasks we preserve the original
    # train-only refit so the audit invariants (held-out val) are unchanged.
    if cfg.problem_type == "qa_excel":
        import numpy as _np
        X_fit = _np.concatenate([splits["X_train"], splits["X_val"]], axis=0)
        y_fit = _np.concatenate([splits["y_train"], splits["y_val"]], axis=0)
    else:
        X_fit, y_fit = splits["X_train"], splits["y_train"]
    # Refit on train(+val), predict on TEST (one-shot, frozen).
    pred_te, proba_te = _fit_predict(
        best["backbone"], best.get("params", {}),
        X_fit, y_fit,
        splits["X_test"], cfg.problem_type,
    )
    test_score = _score(cfg.metric, splits["y_test"], pred_te, proba_te)
    metrics = _all_traditional_metrics(cfg.problem_type, splits["y_test"], pred_te, proba_te)
    dsb_baseline = cfg.dsbench_baseline or 0.5
    # _score() always returns higher-is-better (RMSE/MAE are already negated)
    # so the delta calculation is the same for every metric.
    delta = test_score - dsb_baseline
    report = {
        "task": cfg.slug,
        "name": cfg.name,
        "problem_type": cfg.problem_type,
        "metric": cfg.metric,
        "champion_backbone": best["backbone"],
        "champion_composite": best["composite"],
        "champion_val": best["val_score"],
        "champion_train": best["train_score"],
        "test_score": float(test_score),
        "test_metrics": metrics,
        "dsbench_baseline": dsb_baseline,
        "delta_vs_dsbench": float(delta),
        "beats_dsbench": bool(delta > 0),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
    }
    (repo / "autoresearch_results" / "final_report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--repo", default=None)
    args = p.parse_args()
    if args.repo:
        rep = report_repo(Path(args.repo).resolve())
        print(json.dumps(rep, indent=2))
        return
    rollup: list[dict] = []
    for root in (ROOT / "modeling", ROOT / "analysis"):
        for child in sorted(root.iterdir()):
            if (child / "autoresearch_results" / "best_config.json").exists():
                try:
                    rollup.append(report_repo(child))
                except Exception as exc:
                    rollup.append({"task": child.name, "error": str(exc)})
    (ROOT / "registry" / "final_rollup.json").write_text(json.dumps(rollup, indent=2), encoding="utf-8")
    n_beat = sum(1 for r in rollup if r.get("beats_dsbench"))
    print(f"[final-report] {len(rollup)} tasks scored, {n_beat} beat DSBench baseline")


if __name__ == "__main__":
    main()
