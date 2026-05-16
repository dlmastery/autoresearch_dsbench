# ADR-0007: Stride-5 interleaved split for small-N QA tasks

## Status

Accepted (2026-05-15). Lesson 7 in `framework/CLAUDE_template.md`.

## Context

The 38 Modeloff analysis challenges have **5 to 20 questions each**. The canonical 70/15/15 random split for `n = 10` gives ~7 train / ~1 val / ~2 test — already noisy. The harder problem: Modeloff challenges are **difficulty-ordered**. Early questions are warm-up; late questions are finals-level. A contiguous-block 70/15/15 puts all easy questions in train and all hard questions in test, violating the train/test exchangeability assumption (Bishop 2006 'Pattern Recognition and Machine Learning' PRML §1.3 — i.i.d. assumption).

A random split mitigates ordering but is itself high-variance at `n = 5..20`: a single re-seed can produce splits with 0 hard questions in train.

## Decision

For `qa_excel` tasks, use a **stride-5 interleaved split**:

```
position i mod 5 = 0, 1, 2  → TRAIN
position i mod 5 = 3        → VAL
position i mod 5 = 4        → TEST
```

So `indices = [0, 1, 2, 5, 6, 7, 10, 11, 12, ...]` go to train, `[3, 8, 13, ...]` to val, `[4, 9, 14, ...]` to test. Every position-bucket is **equally represented** in train, val, and test — the difficulty-ordering correlation is broken at every scale.

Edge cases (`framework/runner.py:strided_split`):

| n | train | val | test |
|---|---|---|---|
| 1 | [0] | [] | [] |
| 2 | [0] | [] | [1] |
| 3 | [0] | [1] | [2] |
| 4 | [0, 1, 2] | [] | [3] |
| ≥5 | per stride-5 rule | per rule | per rule |

The forensic Agent D (distribution shift) has a `qa_excel`-calibrated threshold because the stride-5 split deterministically varies the position feature between train and test — KS > 0.2 is mechanical, not pathological. See [`0010_sklearn_early_stopping_whitelist.md`](0010_sklearn_early_stopping_whitelist.md).

Tabular tasks with `n ≥ 100` keep the standard 70/15/15 random split — exchangeability holds at that sample size.

## Consequences

**Easier:**

- A `qa_excel` task with `n = 20` always has 12 train / 4 val / 4 test, deterministically. The split is reproducible from `cfg.slug` alone.
- The forensic audit can pre-compute the expected position-distribution shift and pass it as a baseline, removing false positives on Agent D.

**Harder:**

- The position feature is now a mechanical predictor of the split. Forensic Agent B (target leakage) needs the `qa_excel` MI threshold of 0.50 nats (vs 0.05 for tabular). See [`0010_sklearn_early_stopping_whitelist.md`](0010_sklearn_early_stopping_whitelist.md).
- Tasks with `n = 1` or `n = 2` cannot have a balanced split. Per-task test sets of 1-4 questions are the structural ceiling discussed in [`../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md`](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md).

**Riskier:**

- If Modeloff ever publishes a challenge where consecutive questions are co-dependent (e.g., q5 references q4's answer), the stride-5 split could leak q4's answer into the test split. Mitigation: the canonical answer key is the only signal we use, and answer keys are independent per the Modeloff dataset structure.

## Related

- [`../part_3_processes/14_larger_testing.md`](../part_3_processes/14_larger_testing.md) § 3
- Skill `small-n-stride-split`.
- `framework/runner.py:strided_split`.
- Postmortem [`../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md`](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md).
