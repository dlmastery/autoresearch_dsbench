# ADR-0004: A 10-agent forensic committee polices every champion

## Status

Accepted (2026-05-15). Lessons 16, 17, 22 in `framework/CLAUDE_template.md`.

## Context

A single test-leakage check (e.g., "Is `X_test` referenced anywhere?") catches the most blatant violations but misses subtler ones: a data-pipeline bug that puts a future timestamp in a training row, a champion config that doesn't reproduce when refit, a mechanically high feature-to-label MI introduced by a one-hot encoding step. No single check covers all of these. We need an **ensemble of independent checks**.

The predecessor SPY project (`autoresearchspy/CLAUDE.md`) shipped an 8-agent committee. DSBench's specific failure modes — refit drift on multi-step training, single-backbone-only champions, qa_excel mechanically high-MI task one-hots — motivated two additions.

## Decision

`framework/forensic_audit.py` runs **10 agents** per task, then Agent Z aggregates into a PASS/FAIL:

| Agent | Concern | Class |
|---|---|---|
| A | split-hash integrity | FAIL |
| B | target / label leakage | FAIL |
| C | row overlap | FAIL |
| D | distribution shift | FAIL |
| E | anomaly (val > train, perfect 1.0, jumps > 0.3) | FAIL (with whitelist) |
| F | static-code grep for `X_test` / `y_test` | FAIL |
| G | temporal order | FAIL (N/A on synthetic data) |
| H | seed stability | RECORD-ONLY |
| **I — refit consistency** | champion refits within ±0.005 of recorded test score | **FAIL (new)** |
| **J — backbone diversity** | ≥ 3 distinct backbones tried | **WARN (new)** |
| Z | committee verdict aggregator | — |

Two structural rules:

1. **Independent agents.** No agent reads another's output during its check; they all read raw artefacts (`split_manifest.json`, `experiment_log.jsonl`, `best_config.json`, `.data_cache/splits.npz`). This means a bug in one agent can never silently corrupt another.
2. **Problem-type-aware thresholds.** Agents B, D, E have calibrated thresholds for `qa_excel` because the task one-hot, stride-5 split, and constant-class classifiers legitimately trigger the tabular thresholds. See [`0010_sklearn_early_stopping_whitelist.md`](0010_sklearn_early_stopping_whitelist.md) and `framework/CLAUDE_template.md` § "Forensic Audit — Problem-Type-Aware Thresholds".

## Consequences

**Easier:**

- A new agent is added by writing one function in `framework/forensic_audit.py`; Agent Z picks it up automatically.
- Per-task `forensic_audit.md` is a self-contained narrative — a reviewer reads one file to understand the champion's integrity.
- `registry/forensic_summary.json` is a one-row-per-task table for diffing across commits.

**Harder:**

- 10 agents × 112 tasks = 1120 checks per audit. Total runtime ~10 minutes on the reference machine. Live debugging requires `--repo modeling/<slug>` to limit scope.
- Threshold drift across qa_excel vs tabular agents is a footgun; adding new task families requires recalibration.

**Riskier:**

- A genuine champion can fail Agent I (refit consistency) due to non-deterministic training (e.g., un-seeded data shuffling). Mitigation: every backbone in `runner.py:_fit_predict` accepts a `seed` param and exposes `random_state`.

## Related

- [`../part_3_processes/09_code_review.md`](../part_3_processes/09_code_review.md)
- [`../appendix_d_diagrams/ten_agent_forensic_committee.mmd`](../appendix_d_diagrams/ten_agent_forensic_committee.mmd)
- Skill `forensic-audit-pipeline`.
- Postmortem [`../appendix_a_postmortems/0003_forensic_false_positive_val_gt_train.md`](../appendix_a_postmortems/0003_forensic_false_positive_val_gt_train.md).
