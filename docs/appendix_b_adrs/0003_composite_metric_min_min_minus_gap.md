# ADR-0003: Composite metric `min(val, train) - 0.05 * |val - train|`

## Status

Accepted (2026-05-15). Lesson 18 in `framework/CLAUDE_template.md`.

## Context

Hill-climbing needs a single scalar to compare experiments. Three obvious candidates:

| Candidate | Problem |
|---|---|
| `val_score` | Doesn't penalise underfit / unstable train. A model that gets train=0.55 val=0.80 wins, but the model is broken — those 0.80 val numbers will collapse on test. |
| `train_score` | Doesn't penalise overfit. Memorisers win. |
| `(val + train) / 2` | A 1.00 train + 0.60 val gives 0.80, same as 0.80 train + 0.80 val — the gap-aware case wins. |

A robust composite needs two properties: (a) both train AND val must be high; (b) the gap is penalised.

## Decision

**Composite metric:**

```
composite = min(val_score, train_score) - 0.05 * abs(val_score - train_score)
```

Higher is better. RMSE / MAE / log-loss are negated inside `framework/runner.py:_score()` so the formula is metric-agnostic — `delta = test_score - dsbench_baseline` works for every metric without sign-flipping (the bug that motivated this convention is documented in [`../appendix_a_postmortems/0001_regression_delta_sign_bug.md`](../appendix_a_postmortems/0001_regression_delta_sign_bug.md)).

Properties:

- The `min` term forces BOTH train and val to be good. A high val with a broken train scores low.
- The `0.05 * gap` term penalises overfit champions. Memorisers with train=1.0 val=0.85 score `0.85 - 0.05 * 0.15 = 0.8425` — strictly worse than a balanced 0.90/0.90 (which scores 0.90).
- The coefficient 0.05 is small enough that a 5-point gap costs 0.25 — a noticeable but not dominant penalty.

`framework/runner.py:run_one` computes the composite. `framework/runner.py:_update_best_if_champion` ratchets `best_config.json` only on strict improvement.

For `qa_excel`, this composite is unsuitable because train sets are 8-30 samples and val sets are 1-5 — the gap term is dominated by sampling noise. We use LOO-CV on `train ∪ val` instead. See [`0008_cross_task_pooling_for_training.md`](0008_cross_task_pooling_for_training.md) and [`0009_qa_train_plus_val_refit.md`](0009_qa_train_plus_val_refit.md).

## Consequences

**Easier:**

- A single number drives every KEEP/DISCARD decision.
- Cross-task aggregation is meaningful — a 0.85 composite on `titanic` and a 0.85 composite on `santander` carry comparable trust.

**Harder:**

- An iter that improves val but hurts train (which is often a regularisation win) may show a flat composite. The reasoning annotation must spell out the mechanism so the reviewer reads through to the train/val pair.

**Riskier:**

- The 0.05 coefficient is a tunable. If a future class of tasks shows huge train/val gaps with genuine signal, the gap penalty may dominate and reject valid champions. Mitigation: the unit tests under `framework/_test_excel.py` and the per-task forensic Agent E catch the most common pathologies.

## Related

- [`../part_3_processes/14_larger_testing.md`](../part_3_processes/14_larger_testing.md)
- Skill `experiment-design`.
- Postmortem [`../appendix_a_postmortems/0001_regression_delta_sign_bug.md`](../appendix_a_postmortems/0001_regression_delta_sign_bug.md).
