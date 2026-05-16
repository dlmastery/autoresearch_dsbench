---
name: traditional-ml-metrics
description: Traditional ML metrics mandate — precision, recall, F1, F2, accuracy, MCC, confusion matrix per fold AND aggregate, computed in addition to financial metrics. Triggers on "precision recall", "F1 F2", "MCC", "Matthews correlation", "confusion matrix", "direction classification".
metadata:
  category: verification
  source: autoresearch
  related: [explainability-audit-14-section, per-sample-decision-logging, experiment-design]
---

# Traditional ML Metrics (every experiment)

## When to use

- Every experiment — compute these metrics alongside any task-specific metrics (e.g. Sharpe, IC).
- Building the dashboard's per-window metrics table.
- Investigating why a model has high Sharpe but unreliable directional accuracy.

## The rule

> ### Traditional ML Metrics (MANDATORY for every experiment)
> In addition to financial metrics (Sharpe, Sortino, IC, etc.), compute and log direction-classification metrics for every experiment. The trading strategy uses `sign(prediction)` as the directional bet, so treat direction prediction as binary classification:
> - **Positive class:** model predicts UP (pred > 0) and actual move is UP (actual > 0)
> - **Negative class:** model predicts DOWN (pred < 0) and actual move is DOWN (actual < 0)
>
> Metrics to compute per fold AND aggregate:
> - **Precision:** TP / (TP + FP) — of all UP predictions, how many were correct
> - **Recall:** TP / (TP + FN) — of all actual UP moves, how many did we catch
> - **F1 Score:** harmonic mean of precision and recall
> - **F2 Score:** weighted harmonic mean favoring recall (beta=2), useful for FX where missing a move costs more than a false signal
> - **Accuracy:** (TP + TN) / total — same as hit rate / win rate but explicit
> - **Matthews Correlation Coefficient (MCC):** balanced measure even with class imbalance
> - **Confusion matrix counts:** TP, FP, TN, FN per fold
>
> These must appear in:
> 1. `trading_report()` output in `metrics.py`
> 2. Per-window results in JSONL log entries
> 3. Dashboard per-window tables
> 4. Winner archive `per_fold_results.json`
> 5. Experiment summary markdown

### Generalisation for non-trading tasks

For classification DSBench tasks: treat the task labels directly, compute the same metrics. For multi-class, use macro-averaged precision/recall/F1 + per-class confusion matrix. MCC generalises to multi-class via the multi-class formulation.

For regression DSBench tasks where there's no natural direction: report RMSE / MAE / R² / Spearman correlation alongside; the direction-classification metrics may be skipped if `sign(prediction)` isn't a meaningful action.

## Anti-patterns

- **Reporting only accuracy** on imbalanced data. MCC is required; accuracy can be 95% on a 95/5 class split with zero predictive value.
- **Aggregating across folds with simple mean** — aggregate over the union of fold rows, report a single confusion matrix.
- **Skipping F2 because "F1 is enough"** — in many tasks recall dominates cost (missed signal > false signal); F2 makes this explicit.
- **Inconsistent positive-class definition** between folds. Lock down the convention.
- **Not surfacing in JSONL.** If the dashboard can't read it, it's invisible.

## Implementation checklist

1. `metrics.py:trading_report()` (or `classification_report()` for generic tasks) returns a dict with all 7 metrics + 4 confusion counts.
2. JSONL log entry includes `per_window_metrics[i] = {...}` for each fold AND `aggregate_metrics = {...}`.
3. Dashboard per-window table renders Precision, Recall, F1, F2, MCC columns.
4. Winner archive `per_fold_results.json` includes the full breakdown.
5. `experiment_summary.md` "Classification" row reports `Precision=X Recall=Y F1=Z F2=W MCC=V`.

## References

- Source: `autoresearch/CLAUDE.md` section "Traditional ML Metrics (MANDATORY for every experiment)"
- Matthews (1975) "Comparison of the predicted and observed secondary structure of T4 phage lysozyme" — original MCC.
- van Rijsbergen (1979) "Information Retrieval" — F-beta family.
- Related: `explainability-audit-14-section`, `per-sample-decision-logging`, `experiment-design`.
