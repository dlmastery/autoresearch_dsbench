# Chapter 22 — Large-Scale Changes

> *Parallel to:* SWE-book Chapter 22 *"Large-Scale Changes"* (Winters, Manshreck, Wright 2020).

**Thesis.** A "large-scale change" (LSC) at Google touches thousands of files across hundreds of projects with a single coordinated change. The DSBench LSC analogue: a change that touches all 112 per-task `CLAUDE.md` files, all 112 per-task `forensic_audit.md` files, or all per-task wrappers. The tooling for safe LSCs in this project is the **single-command end-to-end refresh** pattern: `framework/_regenerate_claude_only.py`, `framework/_refresh_dashboards.py`, `framework/_final_audit.py`, run in order, leave the cohort in a coherent state.

## 22.1 What constitutes a large-scale change here

Three categories of LSC, in increasing order of risk:

| LSC type | Scope | Risk | Tooling |
|---|---|---|---|
| **Template change** | 112 per-task `CLAUDE.md` regenerated from `framework/CLAUDE_template.md` | Low — section content drift; caught by validator | `framework/_regenerate_claude_only.py` |
| **Framework change** | `framework/runner.py` or `framework/hill_climb.py` | Medium — affects every experiment from now on; old log entries stay valid but new ones interpret the protocol differently | Re-run hill-climb on a representative subset; commit; document Lessons-Learned row |
| **Audit recalibration** | `framework/forensic_audit.py` threshold change | High — old PASS verdicts may become FAIL or vice versa; cohort scoreboard moves | ADR + recalibration + re-run audit on all 112 + verify the new failure list is intentional |

Each category has its own cookbook below.

## 22.2 Template change cookbook

A template change is the most-common LSC: a new section appears in the upstream protocol (e.g. the May 2026 addition of `### QA-Excel Task Data Loading (real Modeloff answers — NOT synthetic placeholders)`) and must propagate to every per-task `CLAUDE.md`.

The five-step playbook:

1. **Edit `framework/CLAUDE_template.md`.** Add the new section with the canonical header.
2. **Add a row to `framework/SECTION_MAPPING.md`.** New section header in the "Task CLAUDE.md location" column.
3. **Add a SKILL.md to `skills/autoresearch-pack/skills/`.** Verbatim text + frontmatter + triggers.
4. **Run `framework/_regenerate_claude_only.py`.** This walks every task directory and regenerates `CLAUDE.md` from the template with the task-specific parameters substituted.
5. **Run `framework/validator.py`** — confirm 112 / 112 ok. Run `skills/autoresearch-pack/audit/audit_pack.py` — confirm coverage is still 100 %.

Total wall-clock for the cohort: ~30 seconds (regeneration) + ~6 seconds (validator) + ~5 seconds (audit pack) ≈ 45 seconds. Fast enough to do as part of the normal commit cycle.

The May 2026 work executed this playbook nine times (one per new Lessons-Learned row 18–26).

## 22.3 Framework change cookbook

A framework change touches `framework/*.py` directly. Examples:

- Changing the composite formula (`framework/runner.py:_composite`).
- Adding a new backbone to `runner._fit_predict`.
- Recalibrating Agent E's whitelist (`framework/forensic_audit.py:_agent_e`).

The seven-step playbook:

1. **Decide.** Author an ADR in [Appendix B](../appendix_b_adrs/) naming the decision, context, and consequences.
2. **Implement.** Make the framework change. Add a SKILL.md if the change implies a discipline.
3. **Run the framework change on one task.** Pick a representative task (e.g. `titanic`). Confirm the new behaviour matches the ADR's expectation.
4. **Run the framework change on a representative subset (~10 tasks).** Confirm the cohort numbers move in the expected direction.
5. **Run the framework change on the full cohort.** This may take hours for hill-climb changes; minutes for audit-only changes.
6. **Re-run `framework/_final_audit.py`** — confirm all four layers green.
7. **Commit + push.**

For audit-only changes (e.g. relaxing an Agent E threshold), steps 3–5 collapse to a single re-run of `framework/forensic_audit.py` over all 112 tasks (~5 minutes). For hill-climb changes, the cohort re-run is the most expensive operation in the project (~6 hours wall-clock).

## 22.4 Audit recalibration cookbook

The most-careful LSC: changing a forensic-audit threshold. Three calibrations done in the May 2026 work:

| Calibration | Pre-ADR | Post-ADR | ADR |
|---|---|---|---|
| Agent E whitelist | val > train + 0.05 = FAIL on every backbone | val > train + 0.05 = FAIL except sklearn early-stop regression (Bishop 2006 PRML §5.5.2) | [ADR 0010](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md) |
| Agent B qa_excel threshold | MI > 0.05 = FAIL | MI > 0.50 = FAIL on qa_excel (calibrated for 38-task one-hot) | (covered by [ADR 0008](../appendix_b_adrs/0008_cross_task_pooling_for_training.md)) |
| Agent D qa_excel test | KS test > 10 % flagged = FAIL | chi-square on label, p ≥ 0.001 = PASS (calibrated for stride-5 split) | (covered by [ADR 0007](../appendix_b_adrs/0007_stride5_interleaved_split_for_qa.md)) |

The playbook:

1. **Diagnose the false positive.** Read the existing `forensic_audit.md` for a representative failing task. Identify which agent fired and what the threshold was.
2. **Cite the literature.** Find the paper that justifies the new threshold. Bishop 2006 PRML §5.5.2 for early-stopping; appropriate IR / boosting paper for any other family.
3. **Write the ADR.** Context (the false positive), Decision (new threshold), Consequences (cohort movement).
4. **Implement the calibration.** Touch `framework/forensic_audit.py:_agent_<X>` with a new branch or threshold.
5. **Re-run forensic_audit on the cohort.** Verify the previously-failing tasks now PASS and no new failures appeared.
6. **Add a SKILL.md.** `problem-type-aware-audit-thresholds` or `regression-early-stopping-discipline`.
7. **Commit + push.**

The risk: the recalibration could *hide* a real bug. Mitigation: the ADR must name the paper that justifies the threshold. A recalibration without a citation is a smell.

## 22.5 The "single command refresh" pattern

The umbrella LSC tool: `framework/_refresh_dashboards.py` reads every per-task state and regenerates every dashboard + the cross-task `index.html` + the rollup files. Run after any LSC that touches per-task state.

```powershell
# After any large-scale change:
& "C:/Users/evija/anaconda3/python.exe" framework/_regenerate_claude_only.py  # if template changed
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py            # if audit changed
& "C:/Users/evija/anaconda3/python.exe" framework/_refresh_dashboards.py       # always
& "C:/Users/evija/anaconda3/python.exe" framework/_final_audit.py              # always
```

Four commands, ~10 minutes wall-clock for the full sequence. The project's LSC tooling is this small.

## 22.6 What LSCs we deliberately do not run

Three classes of LSC we avoid:

1. **Schema migrations of `experiment_log.jsonl`.** The ledger is append-only; never edit historical rows. New fields are added to new rows; old rows lack the new fields; readers tolerate missing fields gracefully. This is the SWE-book chapter 22 pattern for ledger-style state.
2. **Hand-edits across all 112 `CLAUDE.md` files.** The template is the source of truth; never hand-edit a generated file. The audit's substring check would still pass on a hand-edit, but the next regeneration would clobber it.
3. **Mass-rename of slugs in the registry.** A slug is the filesystem key; renaming would invalidate every per-task path. We have never done this; if we did, it would require a full cohort re-run.

## 22.7 The Lessons-Learned row as the LSC log

Every LSC produces a Lessons-Learned row that names the change. The 26 rows in `framework/CLAUDE_template.md` are the chronological LSC log. A reviewer reading the rows in order sees:

- Row 1–11: original protocol from `autoresearch/CLAUDE.md` adapted to DSBench.
- Row 12–17: the SPY adaptation's additions (regime gate, three-stream features, stacked ensemble, sub-period robustness audit).
- Row 18–26: the May 2026 DSBench corrections (sign convention, coverage gate, X_test grep, single-command refresh, parallel-agent orchestration, two-tab navigation, MD viewer rendering, forbidden-path audit, status-counting asymmetry).

Each row points to the SKILL.md, the ADR, the postmortem (if any), and the code path that codifies the rule.

## 22.8 The "no surprises" principle

A specific LSC discipline: every change must move the cohort scoreboard in a *predicted* direction. A change that's predicted to move BEAT-DSBENCH from 70 to 80 and instead moves it to 65 is a bug, not a feature.

The mechanism: the ADR's Consequences section names the expected movement. Re-running the cohort after the LSC must produce a scoreboard that matches the prediction (modulo within-threshold noise). A mismatch triggers a postmortem.

This is the SWE-book chapter 22 pattern: LSCs are validated against pre-stated predictions, not against post-hoc rationalisations.

## 22.9 The bisection contract

When an LSC moves the scoreboard unexpectedly, the bisection contract is:

1. **Identify the previous green cohort run.** Tag in git, e.g. `v2026-05-15-cohort`.
2. **`git checkout v2026-05-15-cohort`** — confirm the scoreboard matches the tag's recorded numbers.
3. **`git checkout main`** — confirm the new scoreboard differs.
4. **Bisect commits between the tag and HEAD.** For each bisect step, re-run `framework/_final_audit.py` and inspect the cohort scoreboard.
5. **The offending commit is the LSC that moved the scoreboard unexpectedly.**

The bisection is more expensive than `git bisect` for code (each step is ~25 minutes for the audit + refresh), but the granularity is acceptable for the project's commit frequency (a few commits per day at most).

## 22.10 Related

- [Ch. 8 — Style Guides and Rules](../part_3_processes/08_style_guides_and_rules.md): the template that gets propagated by LSCs.
- [Ch. 15 — Deprecation](../part_3_processes/15_deprecation.md): the deprecation LSC.
- [Ch. 18 — Build Systems](18_build_systems.md): the build pipeline that runs after every LSC.
- [Ch. 23 — Continuous Integration](23_continuous_integration.md): the four-layer audit gate as the LSC's safety net.
- [Appendix B — ADRs](../appendix_b_adrs/): every LSC of consequence has an ADR.
