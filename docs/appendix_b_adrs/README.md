# Appendix B — Architectural Decision Records

> Fifteen ADRs in Michael Nygard format (Status, Context, Decision, Consequences). Each ADR records a structural decision that binds the protocol from its date forward.

| # | Title | Status |
|---|---|---|
| [0001](0001_use_synthetic_data_until_real_loaders.md) | Use synthetic Gaussian data until real loaders are wired | Accepted |
| [0002](0002_train_val_only_for_hill_climb.md) | Hill-climb on train + val only; touch test once via `final_report.py` | Accepted |
| [0003](0003_composite_metric_min_min_minus_gap.md) | Composite metric `min(val, train) - 0.05 * |val - train|` | Accepted |
| [0004](0004_10_agent_forensic_committee.md) | A 10-agent forensic committee polices every champion | Accepted |
| [0005](0005_25_iters_per_backbone.md) | 25 iterations per backbone, every backbone | Accepted |
| [0006](0006_extended_200_iter_phase.md) | 200-iter extended recovery cycle | Accepted |
| [0007](0007_stride5_interleaved_split_for_qa.md) | Stride-5 interleaved split for small-N QA tasks | Accepted |
| [0008](0008_cross_task_pooling_for_training.md) | Pool training across 38 QA tasks; score per-task | Accepted |
| [0009](0009_qa_train_plus_val_refit.md) | QA-Excel final refit on `train ∪ val` | Accepted |
| [0010](0010_sklearn_early_stopping_whitelist.md) | Whitelist sklearn early-stop regression in Agent E | Accepted |
| [0011](0011_md_viewer_inline_render.md) | All `.md` links route through `dashboard/md_viewer.html` | Accepted |
| [0012](0012_two_tab_navigation.md) | Cross-task = new tab; per-task = inline drawer | Accepted |
| [0013](0013_44_skill_industry_pack.md) | Decompose protocol into 44 industry-shareable skills | Accepted |
| [0014](0014_github_checkpoint_protocol.md) | GitHub checkpoint cadence + Windows SSL workaround | Accepted |
| [0015](0015_four_layer_audit_gate.md) | Every commit passes all 4 audit layers | Accepted |

## Format

Michael Nygard's ADR template:

1. **Status** — Accepted / Superseded by ADR-N / Deprecated.
2. **Context** — what problem the decision addresses, what alternatives were on the table.
3. **Decision** — what was decided.
4. **Consequences** — easier / harder / riskier outcomes of the decision.
5. **Related** — pointers to the chapter, skill, postmortem, or other ADRs.

## Reading order

The ADRs are roughly chronological. Read [0002](0002_train_val_only_for_hill_climb.md) (Test-Set Embargo) and [0003](0003_composite_metric_min_min_minus_gap.md) (composite metric) first — they are the structural decisions every other ADR builds on. Then [0004](0004_10_agent_forensic_committee.md) and [0015](0015_four_layer_audit_gate.md) for the audit-gate story. The qa_excel cluster ([0007](0007_stride5_interleaved_split_for_qa.md), [0008](0008_cross_task_pooling_for_training.md), [0009](0009_qa_train_plus_val_refit.md)) is the analysis-task complement.

## How to add a new ADR

1. Pick the next available number (0016).
2. Copy the format from an existing ADR (e.g. [0003](0003_composite_metric_min_min_minus_gap.md)).
3. Author with Status = Proposed; convert to Accepted when the decision is committed.
4. Update this README's table.
5. Run `framework/_final_audit.py` to confirm the rest of the audit gate is unaffected.
