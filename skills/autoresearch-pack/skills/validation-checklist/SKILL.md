---
name: validation-checklist
description: Validation checklist run before every experiment session — purge/embargo, split shapes, zero overlap, contiguous segments, per-window row counts, cache loaded. Plus the Common Mistakes table. Triggers on "validation checklist", "validate_purge_embargo", "pre-flight checks", "Common Mistakes", "sliding windows across gaps".
metadata:
  category: verification
  source: autoresearch
  related: [data-integrity-rules, train-val-test-invariants, mlfin-researcher-mindset]
---

# Validation Checklist (run before every experiment session)

## When to use

- At the start of every experiment session.
- After any change to `data/`, `splits.py`, or `features.py`.
- When a "too good" Sharpe lands — re-run the checklist.

## The rule

> ### Validation Checklist (Run Before Every Experiment Session)
> 1. `validate_purge_embargo()` passes — 0 violations
> 2. `split_superfold()` returns correct counts — train=3113, val=915, test=1170
> 3. Train-val overlap = 0, train-test overlap = 0, val-test overlap = 0
> 4. `create_contiguous_datasets()` produces expected segment count (7 for training, 7 for val)
> 5. Each test window processed individually has enough rows (>= seq_len + 1)
> 6. Data loaded from `.data_cache/` (not re-downloaded)

### Common Mistakes (Never Repeat)

| Mistake | Consequence | Prevention |
|---------|-------------|------------|
| Sliding windows across date gaps | ~41% garbage windows, meaningless predictions | `create_contiguous_datasets()` for train/val, `_evaluate_per_window()` for test |
| Expanding window without hole-punching | Cross-fold contamination, inflated Sharpe | `split_data()` punches ALL val/test from ALL folds |
| Dead config params (dropout, huber_delta) | Experiments with no effect, wasted GPU | Wire every param end-to-end or remove it |
| Data re-downloading every run | Minutes wasted, flaky network dependency | Default `cache_dir=.data_cache/` in download.py |
| Grid sweep instead of diagnostic | Uninformed, 10x more experiments than needed | One change at a time, diagnose results first |
| Running all 7 folds per experiment | 7x slower, unnecessary | Super-fold: one train, one eval pass |
| Absolute imports in package | `ModuleNotFoundError` when run as `-m` | Always `from .module import ...` |
| Assuming timing/performance | Wrong estimates, wrong priorities | Measure with `time.time()`, log elapsed |
| Monolithic scripts | Can't debug, can't reuse, can't monitor | Runners log. Dashboard reads. Decoupled. |
| `--learning-rate` flag | argparse expects `--lr` only | Use `--lr` in every runner command |
| `huber_delta` > 1.0 | Residuals are ~5e-3, never cross the Huber kink | Any value ≥ 1 is equivalent — treat Huber as MSE at our scale |
| Fine-grained AdamW `wd` < 30% change | AdamW decouples wd from grads; tiny changes are no-ops | Use log-spaced sweeps (1e-4, 5e-4, 1e-3, 5e-3) not 7e-4 vs 8e-4 |
| Smaller batch without seed plan | bs=16 improves mean-case but **doubles** seed std vs bs=32 | When trying bs<32, always multi-seed before declaring champion |
| Blaming model when problem is regime | Folds 1 & 2 are genuinely hard (GFC-onset / post-crash) across all backbones | Don't chase fold-2 perfection; aim for ≥ 0 with acceptable std |

## Anti-patterns

- **Skipping the checklist "because the data hasn't changed".** The data may not have changed, but a refactor of `splits.py` can silently break invariants.
- **Asserting only counts** (e.g. `len(test) == 1170`) but not set overlap. A perfectly-sized leaky split has the right count.
- **Running the checks but not logging the output.** Future audit needs the verbatim output of `validate_purge_embargo()`.
- **Trusting "looks right" instead of MEASURING.** Measure cache hit, segment count, overlap counts.
- **Using the same `seq_len` across all backbones.** Each backbone has its own — verified via `get_seq_len()`.

## Implementation checklist

1. `validate_purge_embargo(df, train_idx, val_idx, test_idx, buffer_days=10) -> int` returns violation count; assert == 0.
2. Assert split counts match expected (project-specific; for autoresearch FX: train=3113, val=915, test=1170).
3. Set arithmetic: `len(set(train) & set(val)) == 0` etc.
4. `create_contiguous_datasets()` returns the expected number of segments.
5. Each test window: `len(test_window) >= seq_len + 1` for every fold.
6. Top-level loader checks `.data_cache/` mtime — refuse to re-download.
7. Paste verbatim output of these checks into the session-start log.

## References

- Source: `autoresearch/CLAUDE.md` section "Validation Checklist (Run Before Every Experiment Session)"
- Source: `autoresearch/CLAUDE.md` section "Common Mistakes (Never Repeat)"
- Related: `data-integrity-rules`, `train-val-test-invariants`, `mlfin-researcher-mindset`.
