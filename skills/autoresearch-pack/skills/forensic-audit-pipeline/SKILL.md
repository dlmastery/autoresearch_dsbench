---
name: forensic-audit-pipeline
description: Forensic audit pipeline pattern — a 10-agent forensic audit that rigorously verifies a champion. Agents A-H cover data leakage, label integrity, feature causality, training reproducibility, evaluation correctness, statistical significance, robustness, deployment readiness; agents I-J add refit-consistency (±0.005 on test) and backbone-diversity (≥3 distinct). Problem-type-aware thresholds for qa_excel. Triggers on "forensic audit", "8-agent audit", "10-agent audit", "champion verification", "audit pipeline", "refit consistency", "backbone diversity audit".
metadata:
  category: verification
  source: composite
  related: [explainability-audit-14-section, sub-period-robustness-audit, validation-checklist, problem-type-aware-audit-thresholds, regression-early-stopping-discipline]
---

# Forensic Audit Pipeline (8-agent pattern)

## When to use

- A new global champion exceeds the previous best by a large margin (>2.0 composite).
- Preparing a model for external review or deployment.
- Suspicion of data leakage, look-ahead bias, or evaluation bugs.

## The rule

A forensic audit pipeline runs 8 independent agents (or 8 sequential steps) over the champion to cross-check the result from multiple angles. No single agent can produce a clean bill of health — they each look at a different failure mode. The pipeline composes the audit findings into a single PASS/FAIL verdict.

### The 8 agents

1. **Data Leakage Auditor** — re-runs `validate_purge_embargo()`, set-arithmetic overlap checks, label-horizon buffer assertions, and any project-specific contamination tests (e.g. spy's `_enforce_no_2026()`). Verbatim output captured.
2. **Label Integrity Auditor** — confirms the target column was computed from forward-looking data only AFTER the feature row's anchor cutoff; checks for accidental same-bar features (close-of-day features predicting same-day return).
3. **Feature Causality Auditor** — for every feature in the top-10 importance ranking, traces its computation: what data goes in, when is it observable, is it strictly causal w.r.t. the prediction timestamp. Flags any feature whose component is observed AFTER the anchor.
4. **Training Reproducibility Auditor** — re-runs training from the saved seed and config; compares per-epoch loss curves and final metrics. Composite difference > 0.5 = FAIL.
5. **Evaluation Correctness Auditor** — recomputes per-fold Sharpe/IC/MCC from the per-sample trade log (independent of the runner's computation). Discrepancies > 1% = FAIL.
6. **Statistical Significance Auditor** — applies Deflated Sharpe Ratio (Bailey & López de Prado 2014), block-bootstrap CI on test composite, PSR. Flags champions whose DSR < 0.5.
7. **Robustness Auditor** — re-evaluates on rolling sub-periods (see `sub-period-robustness-audit` skill); flags champions whose performance is concentrated in a single regime.
8. **Deployment Readiness Auditor** — verifies the winner archive is fully portable (checkpoint loads, scaler bundled, inference script runs standalone, audit report present, Colab notebook present).
9. **(Agent I) Refit-Consistency Auditor** — refits the champion from `best_config.json:params` on the same train (or train+val for `qa_excel` — see `winner-archive-protocol`), scores on the SAME test set, and asserts `|new_test_score - original_test_score| ≤ 0.005`. Drift > 0.005 indicates non-deterministic training, an unwired config-param, or a stale model checkpoint. FAIL blocks deployment.
10. **(Agent J) Backbone-Diversity Auditor** — counts distinct values of `experiment_log.jsonl:backbone` for the task. ≥ 3 distinct = PASS; < 3 = WARN with documented mitigation (e.g. "task too small to fit ft_transformer; documented in winner README"). Prevents declaring a champion before the SOTA backbone surface has been meaningfully explored.

### Problem-type-aware thresholds (qa_excel)

Agents B, D, and E use `qa_excel`-calibrated thresholds when `cfg.problem_type == "qa_excel"`. See the dedicated skill `problem-type-aware-audit-thresholds` for the full schema. Key cases:

- Agent B (target leakage): MI threshold raised to 0.50 nats; task-onehot features exempt.
- Agent D (distribution shift): KS-test replaced by chi-square on label distribution (p < 0.001 = warn).
- Agent E (val > train anomaly): suppressed for `backend ∈ {class_prior, dummy_majority}` and for `sklearn.MLPRegressor(early_stopping=True)` with gap ≤ 0.05 (see `regression-early-stopping-discipline`, Bishop 2006 PRML §5.5.2).

Every suppression is LOGGED to the audit report so it's distinguishable from a silent skip.

### Composition

- Each agent emits a structured `{status: PASS|FAIL|WARN, findings: [...], evidence_paths: [...]}` blob.
- The pipeline writes `forensic_audit.md` to the winner archive containing all 8 agents' outputs verbatim.
- A champion is "deployable" only after all 8 agents emit PASS (WARN allowed with documented mitigation; FAIL blocks deployment).

## Anti-patterns

- **Single auditor signing off on the whole model** — different failure modes require different lenses; one auditor's PASS doesn't cover the others.
- **Reusing the runner's metric computation in the evaluation auditor** — the point of the audit is independence.
- **Skipping the robustness auditor for "small projects".** A single-period win is often a regime fluke.
- **Treating WARN as PASS** — WARNs need documented mitigation in the deployment checklist.
- **No verbatim evidence paths.** Future reviewers can't reproduce the audit.

## Implementation checklist

1. `framework/forensic_audit.py` orchestrates the 10 agents — one function per agent.
2. Each agent reads the winner archive + raw data + JSONL; produces a structured blob.
3. Composition: write `forensic_audit.md` to `winners/<id>/` with all 10 outputs.
4. Pipeline status block at top: `Overall: PASS (7 PASS, 3 WARN, 0 FAIL)`.
5. WARNs require a follow-up entry in the winner README's "Known Limitations & Risks" section (per `explainability-audit-14-section` Section 13).
6. Per-task `forensic_summary.json` row carries `thresholds_used: {...}` and `suppressions: [...]` for transparency.
7. Agent I (refit-consistency) MUST use the same refit regime as `framework/final_report.py` — train-only for tabular, train+val for `qa_excel`.

## References

- Source: `autoresearch/CLAUDE.md` section "Explainability & Auditability Report" (14-section audit underpins agents 1-2-3-5-6-10-11-12).
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` champion verification block at top (regime-gated ensemble + robustness audit motivates agents 7-8).
- Bailey & López de Prado (2014) "The Deflated Sharpe Ratio" — Statistical Significance Auditor reference.
- Related: `explainability-audit-14-section`, `sub-period-robustness-audit`, `validation-checklist`, `winner-archive-protocol`.
