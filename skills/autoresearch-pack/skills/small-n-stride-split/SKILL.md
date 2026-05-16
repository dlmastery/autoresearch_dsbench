---
name: small-n-stride-split
description: Stride-5 interleaved train/val/test split for tiny multiple-choice tasks (n=5..20). Block 70/15/15 fails exchangeability (Bishop 2006 PRML §1.3) on tiny n — interleave gives every position-bucket equal split representation. Triggers on "stride split", "interleaved split", "small n", "tiny tasks", "stride-5", "qa_excel split", "exchangeability".
metadata:
  category: protocol
  source: dsbench
  related: [train-val-test-invariants, qa-task-feature-engineering, data-integrity-rules]
---

# Small-n Stride-5 Interleaved Split (QA tasks only)

## When to use

- Splitting a per-task multiple-choice / short-answer dataset with n ≤ 20.
- Auditing why a 70/15/15 block split produces a train set that's "all easy questions" and a test set that's "all hard questions".
- Designing the loader for a new tiny-n benchmark (Modeloff, ARC, ScienceQA mini-eval, …).

## The rule

For tiny multiple-choice tasks (n = 5..20 questions per challenge), a contiguous-block 70/15/15 split violates **exchangeability** (Bishop 2006 PRML §1.3): the question order in a Modeloff challenge is roughly **difficulty-ordered** — early questions are warm-up, late questions test the harder mechanics. A block split therefore places "easy" questions in train and "hard" questions in test, producing a biased generalisation estimate.

The DSBench QA loader instead uses a **stride-5 interleaved split**:

```
positions 0, 1, 2, 5, 6, 7, 10, 11, 12, ...   → train      (60% of indices)
positions 3, 8, 13, 18, 23, ...               → val        (20%)
positions 4, 9, 14, 19, 24, ...               → test       (20%)
```

The pattern: for `i in range(n): bucket = i % 5; train if bucket ∈ {0,1,2}, val if bucket == 3, test if bucket == 4`. Every fifth question goes to val; every fifth question goes to test. The difficulty-ordering correlation is broken because each split sees a uniform sample of the position distribution.

### When NOT to use stride-5

- **n ≥ 100 random-order samples.** Standard 70/15/15 random split (with `seed=42`) is unbiased; stride-5 adds no value.
- **Time-series / walk-forward.** Use the `train-val-test-invariants` super-fold scheme; stride-5 would leak temporal info.
- **Cross-task pooled training.** Apply stride-5 PER TASK before pooling (see `cross-task-pooling-discipline`); the pooled train is the union of per-task strides.

## Anti-patterns

- **Random shuffle then block 70/15/15 on tiny n.** With n=10 and a random shuffle, the test split is 1-2 rows — every seed gives a different "champion". Stride-5 is deterministic and balanced.
- **Stratified split on the answer label.** With 4-5 options and n=10, you can't get a meaningful stratification — most strata are empty. Stride-5 gives positional balance, which is what matters at small n.
- **Reusing the same split index across tasks of different sizes.** Each task computes its own stride-5 indices from its own n.
- **Not asserting the union covers all n rows.** Defensive: `assert sorted(train ∪ val ∪ test) == list(range(n))`.
- **Mixing stride-5 (QA) and random 70/15/15 (tabular) without documenting which is which.** The loader logs the split strategy in `split_manifest.json` per task.

## Implementation checklist

1. `framework/runner.py::_stride5_split(n)` returns `(train_idx, val_idx, test_idx)` with the bucket-mod-5 logic.
2. The split is computed PER TASK before pooling; pooled train is `np.concatenate([train_i for i in tasks])`.
3. The manifest record per task: `{"task": slug, "n": n, "split_strategy": "stride_5", "train": len(t), "val": len(v), "test": len(te)}`.
4. The forensic-audit agent D (distribution shift) uses `qa_excel`-calibrated thresholds (see `problem-type-aware-audit-thresholds`) because stride-5 is mechanically KS-different at small n.
5. Unit test: for n in {5, 10, 17, 20}, assert `set(train) ∪ set(val) ∪ set(test) == set(range(n))` and `set(train) ∩ set(val) == set()` and `train ≥ val ≥ test` in size.

## References

- Source: `framework/CLAUDE_template.md` section "Small-n Stride-5 Interleaved Split".
- Source: `framework/runner.py::_stride5_split()` (DSBench codebase).
- Bishop (2006) PRML §1.3 — exchangeability / i.i.d. assumption on the train/test partition.
- Related: `train-val-test-invariants`, `qa-task-feature-engineering`, `cross-task-pooling-discipline`, `data-integrity-rules`.
