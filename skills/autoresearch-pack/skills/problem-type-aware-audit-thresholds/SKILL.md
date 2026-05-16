---
name: problem-type-aware-audit-thresholds
description: Problem-type-aware forensic-audit thresholds — qa_excel tasks need calibrated thresholds because task-onehot features have mechanical MI with label, stride-5 split has mechanical KS shift, and prior-only classifiers legitimately have val > train. Triggers on "audit thresholds", "qa_excel forensic", "false-positive leakage", "task onehot MI", "val > train prior", "stride-5 KS".
metadata:
  category: verification
  source: dsbench
  related: [forensic-audit-pipeline, qa-task-feature-engineering, small-n-stride-split, regression-early-stopping-discipline]
---

# Problem-Type-Aware Forensic-Audit Thresholds

## When to use

- Designing or reviewing `framework/forensic_audit.py` for a multi-problem-type project.
- Hitting "data leakage" / "distribution shift" / "anomaly" warnings on `qa_excel` tasks that aren't actually leakage.
- Calibrating audit thresholds for any cross-task-pooled training regime (`cross-task-pooling-discipline`).
- Reviewing a champion whose val > train and wondering if it's a bug.

## The rule

The base 8-agent forensic audit (`forensic-audit-pipeline` skill) was calibrated for tabular tasks with n ≥ 100 rows per split, random 70/15/15 splits, and per-task training. `qa_excel` violates ALL THREE of those assumptions: cross-task training (38 tasks pooled), stride-5 interleaved split, and tiny per-task n (5..20). The audit MUST therefore use different thresholds for `qa_excel`:

### Agent B — Target Leakage Auditor

- **Tabular threshold:** mutual information MI(feature, label) > 0.05 nats → flag as potential leakage.
- **qa_excel threshold:** MI > 0.50 nats AND feature is NOT a task-onehot indicator. Reason: each Modeloff task has a different per-task label prior (e.g. task 17's answers are 60% "B"; task 23's are 70% "D"). A binary task-onehot feature is therefore mechanically MI-correlated with the label by construction — that's the cross-task pooling design, not leakage.
- Implementation: `if cfg.problem_type == "qa_excel" and feature_name.startswith("task_onehot_"): continue`.

### Agent D — Distribution Shift Auditor

- **Tabular threshold:** Kolmogorov-Smirnov KS-test p < 0.01 between train and val feature distributions → flag.
- **qa_excel threshold:** REPLACE the KS-test with a chi-square on the **label distribution** only; warn when chi-square p < 0.001. Reason: stride-5 interleaved split places consecutive question-buckets in different splits, so structural-feature distributions are mechanically KS-different at small-n. The label distribution, however, should still be ≈uniform across splits — that's the question worth asking.

### Agent E — Anomaly (val > train) Auditor

- **Tabular threshold:** val_score > train_score + 0.05 → flag as suspicious (suggests leakage or overfitting to val).
- **qa_excel exemption:** suppress the warning when ANY of:
  - `backend ∈ {class_prior, dummy_majority}` — a prior-only classifier whose per-task val happens to lie closer to the global prior than per-task train does is NOT a bug; it's the prior baseline working as designed.
  - `model_type == sklearn.MLPRegressor and early_stopping == True` AND gap ≤ 0.05 — see `regression-early-stopping-discipline` skill (Bishop 2006 PRML §5.5.2).

## Anti-patterns

- **One global threshold across all problem types.** Will produce 50%+ false-positive leakage warnings on QA tasks; the user stops trusting the audit and starts ignoring all warnings.
- **Removing task-onehot features to silence the MI warning.** Defeats the whole cross-task pooling design — every task collapses to "predict the global mode".
- **Tightening the chi-square p-threshold on label distribution.** With n=5..20 per split, the test is already low-power; p<0.001 catches only catastrophic stratification failures, which is what we want.
- **Suppressing the val > train warning unconditionally for qa_excel.** Only suppress for prior-only backends AND sklearn early-stopping; a logistic-regression QA model with val > train + 0.10 IS suspicious.
- **Not logging the suppression.** Every threshold-relaxation case writes a one-line audit note: `"agent_E: SUPPRESSED — backend=class_prior, prior-only val > train is design-correct"`. Silent suppressions are indistinguishable from bugs.

## Implementation checklist

1. `framework/forensic_audit.py` reads `cfg.problem_type` and branches on `qa_excel` vs tabular for agents B / D / E.
2. Suppression cases are LOGGED to the audit report, not silently skipped.
3. Per-task `forensic_summary.json` row carries `thresholds_used: {agent_B: 0.50, agent_D: chisq_p_0.001, agent_E: suppressed_prior}` for transparency.
4. Unit test: synthesise a `qa_excel` task with a task-onehot feature whose label correlation is 0.7; assert agent B does NOT flag it.
5. Unit test: synthesise a tabular task with the same correlation; assert agent B DOES flag it.

## References

- Source: `framework/CLAUDE_template.md` section "Forensic Audit — Problem-Type-Aware Thresholds & Agents I/J".
- Source: `framework/forensic_audit.py` (DSBench codebase).
- Bishop (2006) PRML §1.3 — exchangeability and stratification.
- Bishop (2006) PRML §5.5.2 — early-stopping val/train asymmetry.
- Related: `forensic-audit-pipeline`, `qa-task-feature-engineering`, `small-n-stride-split`, `regression-early-stopping-discipline`, `cross-task-pooling-discipline`.
