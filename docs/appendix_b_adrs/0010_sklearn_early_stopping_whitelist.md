# ADR-0010: Whitelist sklearn early-stop regression in Agent E

## Status

Accepted (2026-05-15). Lessons 4 and 23 in `framework/CLAUDE_template.md`.

## Context

Forensic Agent E flags `val_score > train_score + 0.05` as a leakage suspect. This is the right default for most regimes — if val systematically beats train, the model has seen something it shouldn't have.

But three legitimate regimes break this rule:

1. **sklearn `MLPRegressor(early_stopping=True)`.** Per Bishop 2006 'Pattern Recognition and Machine Learning' PRML §5.5.2, sklearn's early-stopping reserves an internal validation slice (default 10% of training data) and selects the stopping epoch to minimise loss on that slice. The post-fit `train_score` is computed on the *remaining* 90% of training data — while the model was selected on the slice. The slice is effectively a second training signal, and the reported train score underestimates the true train performance. `val > train + 0.05` is then **normal**, not leakage.
2. **LightGBM with `early_stopping_rounds`.** Same mechanism — gradient-boosted trees with held-out early stop.
3. **`qa_excel` constant predictors.** A `prior_only` / `class_prior` / `dummy_majority` classifier predicts the per-task training mode for every question. If the per-task val happens to be closer to the global prior than the per-task train, `val > train` is mechanical.

A naive Agent E flags all three. False positives drown out real leakage signals.

## Decision

Whitelist three combinations from Agent E's anomaly check:

1. **sklearn `MLPRegressor(early_stopping=True)` × `problem_type == regression`.** Suppress the warning when `gap ≤ 0.05`. Citation: Bishop 2006 PRML §5.5.2.
2. **LightGBM with `early_stopping_rounds > 0` × `problem_type == regression`.** Same suppression rule.
3. **`qa_excel` backbones in `{class_prior, dummy_majority, prior_only}`.** Always suppress; val > train is structural for constant predictors. Citation: Manning, Raghavan, Schütze 2008 'Introduction to Information Retrieval' Ch. 12 on prior-based classifiers.

The whitelist is **backbone-AND-problem-type aware** (Lesson 23). Classification + early-stop is NOT whitelisted — different failure modes.

Implementation lives in `framework/forensic_audit.py:agent_e_anomaly`; the whitelist is a small lookup table keyed on `(backbone, problem_type, params.get("early_stopping"))`.

## Consequences

**Easier:**

- Agent E focuses on real leakage signals; false positives drop to near zero.
- Adding a new backbone with internal early stopping is a one-line whitelist addition + a unit test.

**Harder:**

- The whitelist is a small piece of knowledge that lives in the auditor — not in the runner. Someone reading the runner without the auditor can miss the rule's existence. Mitigated by the docstring in `agent_e_anomaly` and the cross-reference to `framework/CLAUDE_template.md` § "Sklearn Early-Stopping Val > Train Is Normal".

**Riskier:**

- A future class of legitimate `val > train` regimes (say, semi-supervised pretraining) would need its own whitelist entry. The pattern is extensible but easy to forget. The forensic audit's "WARN-only" version of Agent E logs the suppression in the per-task `forensic_audit.md` so reviewers can sanity-check.

## Related

- [`0004_10_agent_forensic_committee.md`](0004_10_agent_forensic_committee.md)
- Skills `regression-early-stopping-discipline`, `problem-type-aware-audit-thresholds`.
- Postmortem [`../appendix_a_postmortems/0003_forensic_false_positive_val_gt_train.md`](../appendix_a_postmortems/0003_forensic_false_positive_val_gt_train.md).
