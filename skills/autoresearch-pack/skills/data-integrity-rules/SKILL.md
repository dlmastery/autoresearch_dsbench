---
name: data-integrity-rules
description: Hard data-integrity rules — no sliding windows across gaps, no cross-fold leakage, label-horizon buffer, cache-once, load-once. Triggers on "data integrity", "leakage", "contiguous datasets", "purge", "embargo", "cache_dir".
metadata:
  category: protocol
  source: autoresearch
  related: [train-val-test-invariants, validation-checklist, three-stream-feature-engineering]
---

# Data Integrity Rules (Hard, NEVER violate)

## When to use

- Authoring a new dataset/feature pipeline.
- Reviewing any change to `splits.py`, `download.py`, `features.py`, or the dataset class.
- Investigating "too good to be true" Sharpe ratios — they're almost always leakage.
- Adding a new data stream (e.g., the spy project's Asian pre-market or Barchart hourly).

## The rule

> ### Data Integrity
> - NEVER create sliding windows (FXDataset / SPYDataset / equivalent) across non-contiguous date ranges. Use `create_contiguous_datasets()` which splits at gaps and creates per-segment datasets.
> - NEVER include any fold's val or test dates in any fold's training data. Verify with `split_superfold()` — 0 overlap verified.
> - ALWAYS use the label-horizon buffer (10 calendar days) before excluded windows to prevent `fwd_ret_5d` target leakage. The purge gap + buffer together prevent any forward-looking information from leaking into training.
> - ALWAYS cache downloaded data. `download_all_pairs()` and `download_macro_signals()` default to `.data_cache/`. NEVER re-download mid-run.
> - Load data ONCE at startup. Compute features/targets ONCE. Split ONCE. Reuse across all experiments in a loop.

### Common-mistakes addendum (from "Common Mistakes" table)

> | Mistake | Consequence | Prevention |
> |---------|-------------|------------|
> | Sliding windows across date gaps | ~41% garbage windows, meaningless predictions | `create_contiguous_datasets()` for train/val, `_evaluate_per_window()` for test |
> | Expanding window without hole-punching | Cross-fold contamination, inflated Sharpe | `split_data()` punches ALL val/test from ALL folds |
> | Data re-downloading every run | Minutes wasted, flaky network dependency | Default `cache_dir=.data_cache/` in download.py |

## Anti-patterns

- **Naive `df.rolling(window=10)` across a multi-year date range** — silently creates windows that span weekends, holidays, and most importantly the fold boundaries.
- **`train_test_split(shuffle=True)`** on time-series — random shuffle obliterates causality.
- **Re-downloading data inside the experiment loop** — adds network flakiness and re-runs the data pipeline you already paid for.
- **Computing features inside `__getitem__`** — features recomputed N_epochs × N_steps times, masking pipeline bugs and burning GPU.
- **Forgetting the label-horizon buffer.** If your target is `fwd_ret_5d`, the last 5 training days leak the val target. Use a 10-day buffer to be safe across weekends.

## Implementation checklist

1. `download_*()` functions accept and default `cache_dir`; check cache before fetching.
2. `create_contiguous_datasets(df, splits)` returns one Dataset per gap-free segment.
3. `split_superfold()` (or your project's equivalent) returns train/val/test row indices with **zero** overlap; assert this with set arithmetic before training.
4. `LABEL_HORIZON_BUFFER` constant (typically 10 days) is applied in `splits.py` and re-asserted in `validate_purge_embargo()`.
5. Top-level runner loads data ONCE before the experiment loop — feature DataFrame is reused across all experiments.

## References

- Source: `autoresearch/CLAUDE.md` section "Hard Rules → Data Integrity"
- Source: `autoresearch/CLAUDE.md` section "Common Mistakes (Never Repeat)" (rows on sliding windows, hole-punching, cache).
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` section "Data Integrity" (with spy's two cache dirs `.data_cache_spy/` and `.data_cache_spy_hourly/`).
- López de Prado (2018) "Advances in Financial Machine Learning" — chapter on purged k-fold and embargo.
- Related: `train-val-test-invariants`, `validation-checklist`, `three-stream-feature-engineering`.
