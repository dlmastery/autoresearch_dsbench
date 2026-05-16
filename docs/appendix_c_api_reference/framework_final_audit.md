# API Reference — `framework._final_audit`

> The four-layer audit-gate aggregator. The single command that decides whether the cohort is submittable.

## Module: `framework._final_audit`

`C:/Users/evija/dsbench/framework/_final_audit.py`

## Purpose

Runs all four layers of the audit gate ([Ch. 11](../part_3_processes/11_testing_overview.md)) in order, plus the cross-cutting checks (forbidden paths, Lessons-Learned section presence, dashboard "About this task" disclosure). Prints a cohort summary and exits 0 iff every layer is green.

## Layers run

1. **Layer 1 — Section coverage.** `framework/validator.py` against all 112 per-task `CLAUDE.md`.
2. **Layer 2 — Forensic committee.** `framework/forensic_audit.py` over all 112 tasks.
3. **Layer 3 — 14-section explainability.** Confirms every winner's `audit_report.md` has all 14 H2 sections.
4. **Layer 4 — Skill-pack coverage.** `skills/autoresearch-pack/audit/audit_pack.py`.

Plus:

- **Forbidden paths.** No `_backup_pre_*` under `modeling/` or `analysis/` (Lessons-Learned row 25).
- **Lessons-Learned presence.** Every per-task `CLAUDE.md` contains the Lessons-Learned section header.
- **Dashboard disclosure.** Every per-task dashboard has an "About this task" disclosure with task description and split summary.
- **MD viewer routing.** All `.md` links in dashboards route through `dashboard/md_viewer.html`.

## Public functions

### `run() -> int`

Run the full audit-gate sequence. Returns 0 if green, 1 otherwise.

## CLI

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_final_audit.py
```

Exit code 0 = submittable. Non-zero = some layer failed; the offending layer is named in the printed summary.

## Output

Sample green run:

```
[Layer 1 validator] 112/112 OK
[Layer 2 forensic ] 112/112 PASS (4 WARN — Agent J on qa_excel; structural, ignorable)
[Layer 3 14-section] 30/30 winners have full audit_report.md
[Layer 4 skill coverage] 148/148 source sections covered (100%)
[Forbidden paths   ] 0 _backup_pre_* under modeling/ or analysis/
[Lessons-Learned  ] 112/112 with section present
[Dashboard disclosure] 112/112 with About-this-task disclosure
[MD viewer routing ] All dashboard .md links route through md_viewer.html
[Cohort scoreboard]
  BEAT-DSBENCH     82 / 112 (73%)
  FORENSIC-PASS   112 / 112 (100%)
  COVERAGE        148 / 148 (100%)
[VERDICT] GREEN — submittable
```

## Wall-clock

~25 minutes for the full audit on a fresh-state cohort (Layer 2 dominates). On a previously-audited cohort with no state changes, ~30 seconds (Layer 2 reuses cached `forensic_audit.json` per task; only re-runs on stale log entries).

## Related

- [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md): the four-layer gate.
- [Ch. 23 — Continuous Integration](../part_4_tools/23_continuous_integration.md): the gate as CI.
- [Ch. 24 — Continuous Delivery](../part_4_tools/24_continuous_delivery.md): post-audit delivery.
- [`framework/validator.py`](../../framework/validator.py): Layer 1.
- [`framework/forensic_audit.py`](../../framework/forensic_audit.py): Layer 2.
- [`framework/build_submission.py`](../../framework/build_submission.py): Layer 3.
- [`skills/autoresearch-pack/audit/audit_pack.py`](../../skills/autoresearch-pack/audit/audit_pack.py): Layer 4.
