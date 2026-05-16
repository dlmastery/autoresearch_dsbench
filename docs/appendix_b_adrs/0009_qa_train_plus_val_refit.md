# ADR-0009: QA-Excel final refit on `train ∪ val`; tabular stays train-only

## Status

Accepted (2026-05-15). Lesson 6 in `framework/CLAUDE_template.md`.

## Context

The canonical autoresearch rule is "the final refit uses TRAIN only" — `final_report.py` retrains the champion on the training split, scores on the held-out test, and reports the delta. For tabular tasks with `n_train > 100`, this is the right move: val is a held-out signal used during hill-climbing, and re-using val for the final refit risks adding a second-order test-leakage path.

For `qa_excel` tasks the math is different. Per-task train sets are 3-15 questions. A LogReg / k-NN / Naive Bayes fit on 3 samples is essentially undefined. Adding the val rows (1-5 more samples) is the difference between a usable estimator and a degenerate one — without it, the champion that was selected by LOO-CV on `train ∪ val` cannot be re-fit at the same data size for the test score.

There is a key timing property that makes this safe: **val gating is finished by the time `final_report.py` runs**. Hill-climbing is over; the champion has been selected; val cannot influence the test decision because the test decision is "refit and score", not "compare and select".

## Decision

In `framework/final_report.py:report_repo`:

```python
if cfg.problem_type == "qa_excel":
    X_fit = np.concatenate([splits["X_train"], splits["X_val"]], axis=0)
    y_fit = np.concatenate([splits["y_train"], splits["y_val"]], axis=0)
else:
    X_fit, y_fit = splits["X_train"], splits["y_train"]
```

The champion is then refit on `(X_fit, y_fit)` and scored on `X_test` ONCE.

Forensic Agent I (refit consistency) reproduces this protocol exactly when verifying the |delta| ≤ 0.005 invariant — including the `train ∪ val` concatenation for `qa_excel`. Without this calibration, every `qa_excel` task would fail Agent I.

## Consequences

**Easier:**

- The hill-climb LOO-CV composite is consistent with the final-report fit recipe — what we selected is what we deploy.
- A reviewer reads `final_report.json` and sees `champion_val` plus `test_score`; the train+val refit explains the absence of a separate "refit train score".

**Harder:**

- A reviewer reading the rule in `framework/CLAUDE_template.md` § "Champion refit rule" must understand the two-rule design (train for tabular; train+val for `qa_excel`) — there is no longer one universal rule.
- The forensic Agent I implementation has a branch: it concatenates train+val for `qa_excel` and only-train for tabular. Easy to get wrong; covered by the `framework/_test_excel.py` test.

**Riskier:**

- A future task family (say, multi-modal QA) might fall into a third category not anticipated. The branch logic needs revisiting when adding new families.

## Related

- [`0008_cross_task_pooling_for_training.md`](0008_cross_task_pooling_for_training.md)
- Skill `winner-archive-protocol` (extended).
- `framework/final_report.py:report_repo`.
- `framework/forensic_audit.py` Agent I.
