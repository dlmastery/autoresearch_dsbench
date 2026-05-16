---
name: single-command-refresh
description: Single-command end-to-end refresh — the 9-step cookbook a user runs after adding a correction to propagate it through all 112 task repos. Regenerate task CLAUDE.md, re-run affected experiment loops, refresh the 4 audit layers, rebuild submissions, refresh dashboards, snapshot status, run final audit, commit + push. Triggers on "single-command refresh", "9-step ritual", "propagate correction", "end-to-end refresh", "regenerate-and-audit", "_regenerate_claude_only".
metadata:
  category: protocol
  source: dsbench
  related: [mlops-documentation, forensic-audit-pipeline, dashboard-files-update-mandate, winner-archive-protocol, validation-checklist]
---

# Single-Command End-to-End Refresh (the 9-step ritual)

## When to use

- The user added a correction (a new row in the Lessons Learned table).
- A code change in `framework/runner.py` / `framework/forensic_audit.py` / `framework/build_submission.py` requires every task repo to re-render.
- A new skill landed in `skills/autoresearch-pack/skills/` and the coverage audit needs to ratchet up.
- Before any commit that changes experiment state, the four audit layers must be re-verified.

## The rule

> Whenever the user adds a correction, run the 9 steps in order. Skipping any step risks the per-task `CLAUDE.md` files drifting from the template, the audit layers reporting stale numbers, or a submission archive missing the new audit section.

### The 9-step recipe (copy-paste)

```powershell
# 1. apply the code change(s) implied by the correction
# 2. regenerate all 112 task CLAUDE.md from the updated template
& "C:/Users/evija/anaconda3/python.exe" framework/_regenerate_claude_only.py
# 3. re-run every experiment loop that's affected (use --kind to scope)
& "C:/Users/evija/anaconda3/python.exe" framework/run_all.py --kind analysis
# 4. refresh the four audit layers
& "C:/Users/evija/anaconda3/python.exe" framework/final_report.py
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py
& "C:/Users/evija/anaconda3/python.exe" framework/validator.py
& "C:/Users/evija/anaconda3/python.exe" skills/autoresearch-pack/audit/audit_pack.py
# 5. rebuild the submission archive
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py
# 6. refresh the per-task dashboards
& "C:/Users/evija/anaconda3/python.exe" framework/_refresh_dashboards.py
# 7. status snapshot
& "C:/Users/evija/anaconda3/python.exe" framework/_status.py
# 8. final cross-check audit
& "C:/Users/evija/anaconda3/python.exe" framework/_final_audit.py
# 9. commit + push
git add -A
git commit -m "<correction summary>"
git push origin main
```

### What each step does

| Step | Script | Purpose |
|---|---|---|
| 1 | _user-authored_ | The code change implied by the correction (e.g. patched runner, added skill). |
| 2 | `framework/_regenerate_claude_only.py` | Re-substitute the template into all 112 task `CLAUDE.md` so the new rule reaches every repo. |
| 3 | `framework/run_all.py --kind <k>` | Re-run affected experiment loops. `--kind` scopes (`modeling`, `analysis`, `all`). Skip if the correction is doc-only. |
| 4a | `framework/final_report.py` | Re-score every task on the held-back test surface, refresh `final_rollup.json`. |
| 4b | `framework/forensic_audit.py` | Re-run the 10-agent committee; refresh `forensic_summary.json`. |
| 4c | `framework/validator.py` | Section-coverage validator: 112/112 ok. |
| 4d | `skills/autoresearch-pack/audit/audit_pack.py` | Skill-pack coverage audit: 100% PASS. |
| 5 | `framework/build_submission.py` | Re-pack every winner archive (14-file contract) so the audit section reflects the new rule. |
| 6 | `framework/_refresh_dashboards.py` | Regenerate per-task + cross-task dashboards. |
| 7 | `framework/_status.py` | One-line BEAT-DSBENCH / FORENSIC-PASS / FORENSIC-FAIL snapshot. |
| 8 | `framework/_final_audit.py` | End-to-end aggregator: combines all 4 layers + dashboard checks + Lessons-Learned presence. |
| 9 | `git add -A && git commit && git push` | Commit with correction summary; push to `dlmastery/autoresearch_dsbench`. |

### Doc-only corrections shortcut

If the correction is documentation-only (no code change, no metric impact):

- **Skip step 3** (no experiment re-run needed).
- **Skip step 4a** (no scores changed).
- **Run 2, 4b, 4c, 4d, 5, 6, 7, 8, 9.**

### When a step legitimately fails

| Step | Failure | Action |
|---|---|---|
| 2 | Template / substitution mismatch | Fix `framework/_regenerate_claude_only.py` placeholder map; re-run. |
| 3 | Runner crash / hardware BSOD | Resume from `memory/project_autoresearch_checkpoint.md` per the `crash-recovery-checkpoint` skill. |
| 4a-d | Audit FAIL | Diagnose the failing task / section first; do not proceed to commit until all 4 layers PASS. |
| 5 | Submission build error | Likely a winner archive missing a file from the 14-file contract; see `winner-archive-protocol`. |
| 6 | Dashboard render error | The template + JS code in `framework/dashboard_template.html` drifted from the data schema; fix and re-run. |
| 7 | Status numbers regressed | Investigate before commit — quality ratchet says we never regress. |
| 8 | Final audit FAIL | Usually means a per-task `CLAUDE.md` lost a Lessons Learned section (template drift). Re-run step 2. |
| 9 | Push fails (Windows schannel) | `git config --global http.sslBackend schannel` (see `mlops-documentation` lesson 24). |

## Anti-patterns

- **Skipping step 2 after a template change** — the per-task `CLAUDE.md` files drift; tasks see the old rules.
- **Skipping step 4d** — the skill-pack coverage audit; a new rule lands in the template but no skill covers it.
- **Skipping step 8** — final audit catches drift the other steps miss (e.g. dashboards lose the "About this task" disclosure).
- **Manual commit before step 7-8** — committing on unaudited numbers risks pushing a regression.
- **Running steps out of order** — e.g. step 5 before step 4 means the submission archive contains stale forensic verdicts.
- **`run_all.py` without `--kind`** scope on a doc-only correction — wastes hours re-running experiments that didn't change.

## Implementation checklist

1. The 9-step ritual is documented verbatim in `framework/CLAUDE_template.md` (section "Single-command end-to-end refresh").
2. Each script exists and is callable from PowerShell.
3. The validator + forensic + audit pack + final audit all exit non-zero on FAIL (so a CI hook can block bad commits).
4. The status script (`_status.py`) prints to stdout in a parsable format so a shell loop can verify "BEAT count didn't regress".
5. Lessons Learned row 21 (background-agent + git-checkpoint cadence) and row 24 (GitHub schannel) are co-required for step 9 to succeed on Windows.

## References

- Source: `C:/Users/evija/dsbench/framework/CLAUDE_template.md` section "Single-command end-to-end refresh".
- Lessons Learned rows 14-26 inform individual steps.
- Related: `mlops-documentation`, `forensic-audit-pipeline`, `dashboard-files-update-mandate`, `winner-archive-protocol`, `validation-checklist`, `crash-recovery-checkpoint`, `committee-resumption-pointers`.
