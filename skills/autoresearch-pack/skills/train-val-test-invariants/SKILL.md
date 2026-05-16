---
name: train-val-test-invariants
description: Super-fold split invariants — train excludes ALL folds' val/test windows + label buffers; val/test are unions across all folds; zero overlap verified programmatically. Triggers on "super-fold", "split invariants", "train/val/test overlap", "fold 7", "validate_purge_embargo".
metadata:
  category: protocol
  source: autoresearch
  related: [data-integrity-rules, validation-checklist]
---

# Train / Val / Test Invariants (Super-Fold)

## When to use

- Setting up a walk-forward evaluation across multiple market regimes.
- Adapting the FX/SPY 7-fold scheme to a new asset or task type.
- Auditing a suspiciously-high Sharpe — start here, leakage is the usual cause.

## The rule

> ### Super-Fold Invariants
> - Fold 7 training data includes ALL historical data (2005-2023) EXCEPT: all 7 folds' val windows, all 7 folds' test windows, and 10-day label buffers before each.
> - Val set is the UNION of all 7 folds' validation windows (915 rows across 7 regime periods).
> - Test set is the UNION of all 7 folds' test windows (1170 rows across 7 regime periods).
> - **Zero overlap** between train/val/test — verified programmatically before every run.
> - These invariants encode standard ML: train never sees val or test data. Val and test are exhaustive across all regimes.

### Generalization for non-FX tasks

For DSBench / generic tabular tasks the same invariants apply with different numbers; the **shape** of the rule is:

- Train = (full panel) − (∪ all folds' val) − (∪ all folds' test) − (label-horizon buffer around each).
- Val = ∪ folds' val.
- Test = ∪ folds' test.
- Verify zero overlap with set intersection on row indices.

### Test-set exposure rule (dashboard + reporting)

The test set is touched ONCE per task — by `framework/final_report.py`. Every other code path and every dashboard view is train/val only:

- **Per-experiment dashboard rows:** show train AND val metrics. NEVER show a per-experiment test score.
- **Final-report row (champion only):** show train, val, AND test metrics, sourced from `autoresearch_results/final_report.json`. This is the SINGLE place test metrics surface in any UI.
- **No experiment writes to or reads from `splits['X_test']` / `splits['y_test']`.** `framework/validator.py` enforces this by grepping `run_autoresearch.py` and `hill_climb.py` for `X_test` / `y_test` and FAILING the audit if found.

This is the single rule that lets the autoresearch protocol claim an honest test score: every hill-climb / extended-hill-climb / forensic-audit decision used train + val ONLY, and the test pass is one-shot.

## Anti-patterns

- **Single train/val/test split** that doesn't expand across regimes. Even a "long" tail can be regime-homogeneous; multi-fold catches regime-specific failure.
- **Train including the buffer rows that lead into a val window.** The label-horizon buffer must be SUBTRACTED from train.
- **Computing val/test on a per-fold basis but aggregating with simple mean of fold Sharpes.** Aggregate over the UNION of fold rows to get the true holdout Sharpe.
- **Not asserting `len(set(train) & set(val)) == 0` programmatically.** "Looks right" is not a proof.
- **Using fold 7 alone as the "test" — folds 1-6 are no longer holdout** because the model has seen training data from those date ranges via other folds.

## Implementation checklist

1. `split_superfold(df) -> (train_idx, val_idx, test_idx)` returns row-index lists that obey the union property.
2. `validate_purge_embargo(df, train_idx, val_idx, test_idx, buffer_days=10)` asserts zero overlap AND label-horizon buffer.
3. At every experiment start, call `validate_purge_embargo()` and abort if violations > 0.
4. Log expected counts to checkpoint: e.g. `train=3113, val=915, test=1170` — sanity-check on every run.
5. Per-window evaluation: report Sharpe per fold AND aggregate over the union.

## References

- Source: `autoresearch/CLAUDE.md` section "Super-Fold Invariants"
- Source: `autoresearch/CLAUDE.md` section "Validation Checklist (Run Before Every Experiment Session)"
- López de Prado (2018) chapter 7 — Cross-validation in finance, purged k-fold.
- Bailey, López de Prado (2014) "The Deflated Sharpe Ratio" — why multi-regime evaluation matters.
- Related: `data-integrity-rules`, `validation-checklist`.
