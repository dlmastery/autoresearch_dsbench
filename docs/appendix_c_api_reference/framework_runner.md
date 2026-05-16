# API Reference — `framework.runner`

> The single-experiment runner. Logs only — does not orchestrate the hill-climb.

## Module: `framework.runner`

`C:/Users/evija/dsbench/framework/runner.py`

## Public functions

### `run_one(repo, backbone, params, description, experiment_num) -> dict`

Run exactly one experiment for the task at `repo`.

| Parameter | Type | Notes |
|---|---|---|
| `repo` | `pathlib.Path` | Absolute path to the task directory containing `task_config.json`. |
| `backbone` | `str` | One of `xgboost / lightgbm / catboost / mlp / ft_transformer / lstm / patchtsmixer / excel_agent`. |
| `params` | `dict` | Backbone-specific hyperparameters. See `_fit_predict` for what each backbone consumes. |
| `description` | `str` | Free-text description for the experiment log. Forms the human label in the dashboard. |
| `experiment_num` | `int` | 1-based experiment index. Used to key `trade_logs/exp<N>_*.csv` and `reasoning_annotations.json`. |

**Returns:** A `dict` with keys `experiment_num, backbone, description, params, metric, train_score, val_score, composite, train_metrics, val_metrics, elapsed_sec, timestamp, task_slug, uses_test_set`. The same dict is appended to `<repo>/autoresearch_results/experiment_log.jsonl`.

**Side effects:**
- Appends one JSON line to `<repo>/autoresearch_results/experiment_log.jsonl`.
- Writes `<repo>/autoresearch_results/trade_logs/exp<N>_decisions.csv`.
- Writes `<repo>/autoresearch_results/trade_logs/exp<N>_decision_summary.json`.
- Overwrites `<repo>/autoresearch_results/best_config.json` if `composite > current best`.

**Example:**
```python
from pathlib import Path
from framework.runner import run_one
rec = run_one(
    repo=Path("C:/Users/evija/dsbench/modeling/titanic"),
    backbone="xgboost",
    params={"iterations": 400, "max_depth": 10, "lr": 0.04},
    description="depth=10 lr=0.04 — push capacity",
    experiment_num=7,
)
print(rec["composite"])
```

### `TaskConfig.load(repo) -> TaskConfig`

Load `<repo>/task_config.json` into a dataclass. See [`../part_3_processes/10_documentation.md`](../part_3_processes/10_documentation.md) for the schema.

### `load_or_make_data(repo, cfg, seed=42) -> dict`

Return a dict with keys `X_train, y_train, X_val, y_val, X_test, y_test` (cached in `<repo>/.data_cache/splits.npz`). For `qa_excel` tasks, loads real Modeloff answers via `_load_qa_excel`. For other types, generates synthetic Gaussian data — see [`../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md`](../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md).

## CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/runner.py `
    --repo C:/Users/evija/dsbench/modeling/titanic `
    --backbone xgboost `
    --params '{"iterations": 400, "max_depth": 10, "lr": 0.04}' `
    --description "depth=10 lr=0.04" `
    --experiment-num 7
```

Prints the result dict to stdout (excluding `params` for brevity).

## Hardware-pinning

`_pin_to_safe_cores()` is called at module import. It pins to P-cores 0,2,4,6 and sets `OMP / MKL / OPENBLAS_NUM_THREADS=4`. Override via env `AUTORESEARCH_USE_ALL_CORES=1` (not recommended). See [`../part_4_tools/25_compute_as_a_service.md`](../part_4_tools/25_compute_as_a_service.md) § 1.

## Related

- [`framework_hill_climb.md`](framework_hill_climb.md)
- [`framework_final_report.md`](framework_final_report.md)
- [`../part_4_tools/25_compute_as_a_service.md`](../part_4_tools/25_compute_as_a_service.md)
