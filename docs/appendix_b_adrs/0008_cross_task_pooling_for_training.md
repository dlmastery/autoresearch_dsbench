# ADR-0008: Pool training across 38 QA tasks; score per-task

## Status

Accepted (2026-05-15). Lesson 8 in `framework/CLAUDE_template.md`.

## Context

Each of the 38 Modeloff challenges has 5-20 questions, so the per-task train pool is 3-15 samples. Fitting a `LogisticRegression` to 3-15 samples is hopeless — the model has 9 + 38 = 47 features (9 structural + 38-dim task one-hot) and 134 possible classes (the canonical answer encoder). The per-task fitter degenerates to the per-task mode in 8 of 38 cases.

But across all 38 tasks, the **combined** training pool is ~281 samples. A single LogReg fit on the union can learn:

- The cross-task **answer-letter prior** (Modeloff favours A/B/C/D; E-I are rare).
- The cross-task **positional prior** (early questions skew toward A; late questions diffuse).
- The **task-conditional prior** via the 38-dim task one-hot — each task gets its own learnable bias.

This is mathematically equivalent to training a multi-task model with hard parameter sharing.

## Decision

For `qa_excel` training, **pool the training subsets across all 38 tasks** into one combined `(X_train_pool, y_train_pool)`. A single classifier (LogReg / k-NN / Naive Bayes / etc.) is fit once on the pool.

**Evaluation remains per-task.** Each task is scored on its own held-out val and test splits. The composite is per-task (LOO-CV on per-task `train ∪ val`); the cross-task rollup is the standard mean across 38 per-task numbers.

`framework/runner.py:_build_qa_global` builds the pool. The 38-task one-hot is the feature that lets a single shared classifier serve all 38 tasks while preserving per-task identity.

Why this is **not** test leakage:

- The pool only contains TRAINING rows from each task.
- The val and test rows of every task are excluded from the pool.
- Per-task evaluation uses the per-task val (during hill-climbing) or per-task test (during `final_report.py`).

This is a documented decision per the autoresearch CLAUDE.md "test is the only held-back split" rule.

## Consequences

**Easier:**

- A single LogReg model trained on 281 samples generalises across all 38 challenges — replaces 38 hopelessly under-fit per-task models.
- The 38-task one-hot is a learnable degree of freedom that captures per-task priors automatically.
- Hill-climbing efficiency: one fit + 38 evaluations per iter, not 38 fits.

**Harder:**

- The 38-task one-hot has **mechanical mutual information** with the label (each one-hot column is constant within its task, and each task has a different per-task prior). Forensic Agent B's MI threshold must be raised to 0.50 nats for `qa_excel` (vs 0.05 for tabular). See [`0010_sklearn_early_stopping_whitelist.md`](0010_sklearn_early_stopping_whitelist.md).

**Riskier:**

- A bug in the pool-construction code (e.g., accidentally including val rows in `train_pool`) would corrupt every task's training data simultaneously. Mitigated by Agent A (split-hash) — the cached `splits.npz` is hashed per-task; cross-task pooling happens at fit time only, not at cache time.

## Related

- [`../part_3_processes/14_larger_testing.md`](../part_3_processes/14_larger_testing.md) § 3
- [`0009_qa_train_plus_val_refit.md`](0009_qa_train_plus_val_refit.md)
- Skill `cross-task-pooling-discipline`.
- `framework/runner.py:_build_qa_global` and `_excel_agent`.
- Postmortem [`../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md`](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md).
