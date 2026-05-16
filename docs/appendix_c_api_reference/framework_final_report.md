# API Reference — `framework.final_report`

> The one-shot test-set scorer. The **only** code path that legally touches `X_test` / `y_test`.

## Module: `framework.final_report`

`C:/Users/evija/dsbench/framework/final_report.py`

## Public functions

### `report_repo(repo) -> dict`

Refit the champion (from `<repo>/autoresearch_results/best_config.json`) and score on the test set ONCE. Per [`../appendix_b_adrs/0009_qa_train_plus_val_refit.md`](../appendix_b_adrs/0009_qa_train_plus_val_refit.md):

- `problem_type == "qa_excel"` → refit on `X_train ∪ X_val`.
- Otherwise → refit on `X_train` only.

Returns:

```python
{
    "task": "titanic",
    "name": "titanic",
    "problem_type": "classification_binary",
    "metric": "roc_auc",
    "champion_backbone": "xgboost",
    "champion_composite": 0.9555,
    "champion_val": 0.9573,
    "champion_train": 0.9931,
    "test_score": 0.9624,
    "test_metrics": {...},   # all traditional metrics
    "dsbench_baseline": 0.50,
    "delta_vs_dsbench": 0.4624,
    "beats_dsbench": True,
    "timestamp": "...",
}
```

**Side effect:** writes `<repo>/autoresearch_results/final_report.json` with the same content.

**Critical:** `delta_vs_dsbench = test_score - dsbench_baseline` is computed without any metric-specific sign flip because `runner._score()` already negates loss-style metrics. See [`../appendix_a_postmortems/0001_regression_delta_sign_bug.md`](../appendix_a_postmortems/0001_regression_delta_sign_bug.md).

## CLI

```powershell
# All tasks; writes registry/final_rollup.json
& "C:/Users/evija/anaconda3/python.exe" framework/final_report.py

# One task
& "C:/Users/evija/anaconda3/python.exe" framework/final_report.py --repo modeling/titanic
```

After a full run, `registry/final_rollup.json` is a list of `report_repo` dicts, one per task. This is the master file the cross-task dashboard, `_status.py`, `_summary.py`, and `_losses.py` read.

## Invariant

`final_report.py` is the ONLY code path that calls `_fit_predict(..., splits["X_test"], ...)`. The validator (`framework/validator.py`) greps the per-task `run_autoresearch.py` and `hill_climb.py` for `X_test`/`y_test` references and FAILs on any. Agent F of the forensic audit re-greps after every run. See [`../appendix_b_adrs/0002_train_val_only_for_hill_climb.md`](../appendix_b_adrs/0002_train_val_only_for_hill_climb.md).

## Related

- [`framework_runner.md`](framework_runner.md)
- [`framework_forensic_audit.md`](framework_forensic_audit.md)
- [`../appendix_b_adrs/0002_train_val_only_for_hill_climb.md`](../appendix_b_adrs/0002_train_val_only_for_hill_climb.md)
- [`../appendix_b_adrs/0009_qa_train_plus_val_refit.md`](../appendix_b_adrs/0009_qa_train_plus_val_refit.md)
