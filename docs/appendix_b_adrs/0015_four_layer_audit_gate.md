# ADR-0015: Every commit that changes experiment state passes all 4 audit layers

## Status

Accepted (2026-05-15). Lesson 22 in `framework/CLAUDE_template.md`.

## Context

The autoresearch protocol has many guard rails: a section-coverage validator, a 10-agent forensic committee, a 14-section explainability report per winner, a skill-pack coverage audit. Each is a useful local check, but a single one in isolation is insufficient.

- The **validator** verifies the protocol is documented; it does not verify the protocol was followed.
- The **forensic auditor** verifies a champion has no leakage; it does not verify the explainability report exists.
- The **explainability report** documents WHY a champion behaves the way it does; it does not verify the skill pack is current.
- The **skill-pack audit** verifies the protocol is shareable; it does not verify the champion is real.

A submission is only credible if ALL FOUR pass. We need a single gate that runs all four and reports green / red.

## Decision

**Four-layer audit gate, all must pass:**

| Layer | Tool | Pass condition |
|---|---|---|
| 1 — Section coverage | `framework/validator.py` | 112/112 OK; every required section in every per-task `CLAUDE.md`; no `X_test`/`y_test` in runner code |
| 2 — Forensic committee | `framework/forensic_audit.py` | 112/112 PASS verdict; no FAIL-class agent failures |
| 3 — Explainability | `framework/build_submission.py` | 14 sections present in every winner's `audit_report.md` |
| 4 — Skill-pack coverage | `skills/autoresearch-pack/audit/audit_pack.py` | Every H2/H3 in the three source CLAUDE.md files maps to ≥ 1 skill |

**Aggregator: `framework/_final_audit.py`.** Combines all 4 + 7 additional cross-checks (Lessons-Learned in every CLAUDE.md, About-dropdown in every dashboard, md_viewer in both `dashboard/` and `submissions/`, md_viewer routes counted in `task_detail.html` + `dashboard_template.html`, new forensic agents I+J in submission archives, etc.). The script writes a one-page report.

**Run before every commit that changes experiment state.** The full 9-step ritual is documented at the end of `framework/CLAUDE_template.md`:

```powershell
# 1. apply code changes
# 2. regenerate per-task CLAUDE.md
python framework/_regenerate_claude_only.py
# 3. re-run affected experiments
python framework/run_all.py --kind analysis
# 4. four audit layers
python framework/final_report.py
python framework/forensic_audit.py
python framework/validator.py
python skills/autoresearch-pack/audit/audit_pack.py
# 5. submission archive
python framework/build_submission.py
# 6. per-task dashboards
python framework/_refresh_dashboards.py
# 7. status snapshot
python framework/_status.py
# 8. final cross-check
python framework/_final_audit.py
# 9. commit + push
git add -A && git commit -F .commit_msg.txt && git push origin main
```

## Consequences

**Easier:**

- A single command (`python framework/_final_audit.py`) tells a reviewer whether the repo is in a submittable state.
- A new contributor can run the 9-step ritual without needing to understand each tool individually.
- Regression catching: a code change that breaks one of the four layers fails fast.

**Harder:**

- The 9-step ritual takes ~15 minutes end-to-end. Long-running iter loops do not run all four after every single experiment — the ritual is per-batch, not per-experiment.
- The aggregator (`_final_audit.py`) is a script, not a CI pipeline. Self-discipline is required to actually run it. Mitigation: the runbooks ([`../part_4_tools/23_continuous_integration.md`](../part_4_tools/23_continuous_integration.md)) require it.

**Riskier:**

- A new audit layer added in the future (e.g., a 5th forensic dimension) must be plumbed into both `_final_audit.py` AND the 9-step ritual. Easy to forget. The skill `mlops-documentation` (extended) documents the canonical pattern.

## Related

- [`../part_3_processes/09_code_review.md`](../part_3_processes/09_code_review.md)
- [`../part_3_processes/10_documentation.md`](../part_3_processes/10_documentation.md)
- [`../appendix_d_diagrams/four_layer_audit_gate.mmd`](../appendix_d_diagrams/four_layer_audit_gate.mmd)
- [`../part_4_tools/23_continuous_integration.md`](../part_4_tools/23_continuous_integration.md)
- [`../part_2_culture/07_measuring_engineering_productivity.md`](../part_2_culture/07_measuring_engineering_productivity.md)
