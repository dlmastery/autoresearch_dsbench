---
name: metric-sign-convention
description: Metric sign convention — _score() returns higher-is-better for every metric (RMSE/MAE/log-loss are negated inside). All downstream delta / beats-baseline / leaderboard computations use the same arithmetic for every metric — no special-case sign flip for loss-style metrics. Triggers on "regression delta", "metric sign", "beats DSBench", "RMSE negation", "delta vs baseline", "final_report.py".
metadata:
  category: protocol
  source: dsbench
  related: [experiment-design, traditional-ml-metrics]
---

# Metric Sign Convention (higher-is-better, ALWAYS)

## When to use

- Writing `final_report.py` or any cross-metric leaderboard / rollup.
- Computing the delta between a champion test score and a baseline.
- Reviewing a PR that touches `_score()`, `_composite()`, or any "did we beat X?" computation.
- Debugging a leaderboard that ranks regression tasks backwards.

## The rule

`framework/runner.py::_score(metric, y_true, y_pred, y_proba)` returns a single **higher-is-better** scalar for EVERY supported metric. Loss-style metrics (RMSE, MAE, log-loss, NLL) are **negated inside `_score()`** before being returned. The downstream rule is therefore the same for every metric:

```python
# CORRECT — works for accuracy, F1, ROC-AUC, RMSE, MAE, exact-match, …
delta            = test_score - baseline_score
beats_baseline   = delta > 0
composite        = min(val_score, train_score) - 0.05 * abs(val_score - train_score)
champion_better  = new_composite > old_composite
```

```python
# WRONG — re-flips the sign for RMSE/MAE that was already flipped inside _score()
if metric in {"rmse", "mae"}:
    delta = -(test_score - baseline_score)   # ← BUG
```

The bug that motivated this skill: `framework/final_report.py` had a `metric in {"rmse",...}` branch that re-negated the delta for regression tasks. The result was that regression tasks reported `beats_dsbench=True` when they were actually worse than baseline. Fix: delete the special case; `delta = test_score - dsb_baseline` for every metric.

## Anti-patterns

- **Maintaining a list of "loss metrics" outside `_score()`.** The list will drift; the negation will be applied twice in some paths and zero times in others.
- **Treating `composite > 0` as "good".** Composite is on the metric's native scale post-negation; for a negated RMSE in [-3, 0], a composite of `-0.7` may be excellent.
- **Reporting raw RMSE in user-facing tables when the rest of the pipeline uses negated RMSE.** Pick one convention; the rest of the pack chose higher-is-better. Display layer can re-negate for the user (`display_rmse = -metric_value`), but every comparison stays in higher-is-better space.
- **Sorting a leaderboard ascending for regression and descending for classification.** With the negation convention, every leaderboard sorts descending by `score`.
- **Forgetting the sign on `dsbench_baseline`.** If `_score()` returns `-rmse`, the baseline must also be `-baseline_rmse` (loaded that way in `task_config.json`).

## Implementation checklist

1. `_score()` is the SOLE producer of metric scalars; every other consumer takes its output verbatim.
2. Unit-test `_score("rmse", y, y, None) == 0.0` and `_score("rmse", y, y + 1, None) < 0`.
3. `task_config.json:dsbench_baseline` is stored in the same higher-is-better space as `_score()` output.
4. `delta = test_score - dsb_baseline` — no `if metric in {...}: delta = -delta` branches anywhere in the codebase.
5. Display-layer code may re-negate for user-friendly output (`abs(score)` for RMSE / MAE), but ALWAYS compare in the higher-is-better space.
6. CI / validator: grep for `metric in {"rmse"` and `metric == "rmse"` outside `_score()`; any hit is a bug.

## References

- Source: `framework/CLAUDE_template.md` section "Experiment Design" → "Metric sign convention".
- Source: bug fix `framework/final_report.py` 2026-05 — removed the regression-specific sign flip.
- Related: `experiment-design`, `traditional-ml-metrics`, `winner-archive-protocol`.
