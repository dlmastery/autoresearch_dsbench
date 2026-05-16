# Chapter 9 — Code Review

> *Parallel to:* SWE-book Chapter 9 *"Code Review"* (Winters, Manshreck, Wright 2020).

**Thesis.** Code review is the most important cultural practice the SWE-book describes. Critique — Google's internal review tool — receives more attention in chapter 9 than any single piece of infrastructure. In the DSBench project, code review takes a different form: every commit that changes experiment state is reviewed by a **10-agent forensic committee** that runs unsupervised, produces a written verdict per task, and refuses to mark the cohort done until every task's verdict is PASS. The committee is the code reviewer; the verdict file is the LGTM.

## 9.1 What "code" means here

A traditional code review reviews source code. A DSBench review reviews:

1. **Source code** in `framework/*.py` — when the framework changes.
2. **Per-task `CLAUDE.md`** changes — when the protocol is amended.
3. **Reasoning annotations** in `autoresearch_results/reasoning_annotations.json` per task — when an experiment lands.
4. **The experiment log** `experiment_log.jsonl` per task — append-only, but the contents are reviewed.
5. **The 14-section explainability audit** `submissions/.../audit_report.md` per champion — reviewed when a new global champion lands.

Item 1 is reviewed by the human reading the diff. Items 2–5 are reviewed by the **10-agent forensic committee** because no human can read 14,000 experiments and 112 audit reports. The committee is automated *necessity*, not convenience.

## 9.2 The 10-agent forensic committee

`framework/forensic_audit.py` runs per task. Ten agents, each with a single concern, write independent verdicts to `<task>/forensic_audit.json`. An aggregator (Agent Z) writes the committee verdict to `forensic_audit.md` and `registry/forensic_summary.json`. The agents:

| Agent | Concern | Pass threshold |
|---|---|---|
| **A — split-hash** | Manifest hashes in `data/split_manifest.json` match the actual `.data_cache/splits.npz`. | Mismatches ≥ 1 → FAIL. |
| **B — target / label leakage** | Per-feature mutual information with the label. | Max MI > 0.9 → FAIL on tabular; calibrated for qa_excel one-hot. |
| **C — row overlap** | Train / val / test row-hash intersections. | Any overlap > 0 → FAIL. |
| **D — distribution shift** | Per-feature two-sample Kolmogorov-Smirnov train vs test. | > 10 % flagged features → FAIL on tabular; calibrated for qa_excel stride split. |
| **E — anomaly** | `val > train + 0.05`; perfect 1.0 scores; jumps > 0.3 in composite. | Suspicious count > 0 → FAIL; sklearn early-stop on regression is whitelisted (Bishop 2006 *Pattern Recognition and Machine Learning* §5.5.2). |
| **F — static-code** | `grep` for `X_test` / `y_test` in runner / hill-climb code. | Any reference → FAIL. |
| **G — temporal order** | No future timestamps in train rows. | N/A on synthetic data; N/A on Modeloff. |
| **H — seed stability** | Multi-seed champion reproduction variance. | Record-only. |
| **I — refit consistency** | Refit champion from `best_config.json`, score on test, compare to recorded. | \|delta\| > 0.005 → FAIL. |
| **J — backbone diversity** | Distinct backbones in `experiment_log.jsonl`. | < 3 → WARN (not FAIL). |
| **Z — committee verdict** | Aggregates A–J → PASS / FAIL with risks list. | PASS iff none of A–I FAILed. |

Per-agent rationale is in `forensic_audit.md`. The script is parameterised by `--task-slug` for spot-checking a single task. Full cohort run takes ~5 minutes for 112 tasks on the reference hardware.

The committee is the reviewer that scales. A human cannot read 112 audit reports per cohort change; the committee does it in 5 minutes per run.

## 9.3 Why ten agents, not one

The SWE-book chapter 9 makes a specific point: a good code review has a single reviewer because consensus-by-committee is slow. The DSBench parallel might seem to argue for one agent, not ten. The reason for ten:

1. **Concerns must be independent.** Mixing "is the test set leaked" with "are the backbones diverse" produces a verdict that's hard to debug. Ten single-concern agents produce ten independently-debuggable verdicts.
2. **Calibration must be per-concern.** Agent B's MI threshold is 0.9 on tabular and different on qa_excel. Agent D's KS-test threshold is per problem-type. A single-agent reviewer can't carry that much problem-type-aware state without becoming unreadable.
3. **False positives must be quarantinable.** When Agent E flagged regression tasks for val > train, we whitelisted *Agent E's specific check*, not the whole audit. The quarantining only works if the agents are separate.
4. **The verdict file is the LGTM.** A committee verdict that aggregates ten passes is the strongest possible LGTM; a single-agent green is one program's opinion. The cohort scoreboard reads the committee verdict.

This is the SWE-book's pattern for incident-response committees, applied to code review. The agents do the reading; Agent Z writes the LGTM.

## 9.4 The `_manual: true` annotation

The committee reviews mechanical things. The human reviews semantic things. The marker that distinguishes the two: every reasoning annotation carries `_manual: true` when authored or reviewed by a human. The audit emits a warning when `_manual: false` annotations appear in a champion's lineage.

Concretely, the lineage of a champion is the chain of experiments that landed in `best_config.json`. The human must have signed off (`_manual: true`) on every step of that chain. Auto-generated annotations are allowed for non-champion iterations (the negative-result iters that the protocol requires for completeness) but cannot ride the lineage of a champion. This is the closest the project gets to "two reviewers required" for high-stakes changes.

## 9.5 Pre-submit vs post-submit

The SWE-book chapter 9 distinguishes pre-submit ("review happens before the code lands") from post-submit review. We are pre-submit:

1. Claude proposes an experiment + writes the six-field annotation (pre-write fields).
2. The experiment runs.
3. Claude writes the post-write fields (`verdict`, `learning`).
4. The human reads the annotation and the log entry.
5. The human commits *or* asks for changes.

The committee runs *after* the commit but *before* the cohort scoreboard updates. A failing committee verdict blocks the scoreboard from claiming the task is done. Effectively the commit lands but the cohort number does not move until the verdict is PASS. This is a compromise between speed (we want to commit experiments as they happen) and safety (we do not want the cohort scoreboard to claim a task is done without committee approval).

## 9.6 The escalation pathway

When the committee fails a task, the escalation pathway is:

1. **Read `forensic_audit.md` for the task.** The committee verdict names which agent failed and what the threshold was.
2. **Diagnose.** Is this a real bug (e.g. test-set leakage)? a calibration false positive (e.g. Agent E on regression)? a structural ceiling (e.g. Agent J on qa_excel with only one backbone)?
3. **Choose the fix.** A real bug → fix the framework + add a Lessons-Learned row + add an ADR if structural. A calibration false positive → whitelist with citation + add a SKILL.md. A structural ceiling → demote the verdict from FAIL to WARN with a documented reason.
4. **Re-run the committee.** Until PASS, the task does not enter the BEAT-DSBENCH count even if `final_report.test_score > dsbench_baseline`.

The five postmortems in [Appendix A](../appendix_a_postmortems/) each name an instance of this pathway. The pathway is the project's substitute for "argue with your reviewer until they LGTM" — the agents do not argue, but the human can disable the failing check with a documented and audited override.

## 9.7 The "size of a CL" rule

The SWE-book chapter 9 cites research that review effectiveness drops sharply on CLs above 200 lines. Our parallel:

- **One commit per logical change.** A framework change goes in one commit; a per-task scaffold regeneration goes in another; a Lessons-Learned row + ADR goes in a third.
- **Atomic cohort updates.** The "single-command end-to-end refresh" pattern (`framework/_refresh_dashboards.py`) regenerates every dashboard from the current rollup files in one commit. Dashboards are *not* hand-edited.
- **No "WIP" commits to `main`.** The branch protection rule is informal (single operator), but in practice every commit to `main` passes the four-layer audit gate. WIP work lives in checkpoint files (`memory/project_autoresearch_checkpoint.md`) that are committed but are not "experiment state" in the audit-gate sense.

## 9.8 What the committee does *not* review

The committee is mechanical. Three classes of error it does not catch:

1. **A wrong baseline in `registry/modeling_tasks.json`.** If `dsbench_baseline` was transcribed incorrectly from the upstream paper, the committee will happily PASS a task that beats a too-low baseline. Human review is the only line of defence.
2. **A wrong metric in `task_config.json`.** If a regression task is mis-labelled as classification_binary, the runner will silently route through the wrong branch. The validator's substring check does not catch this.
3. **Conceptual errors in the citation.** If the annotation cites a paper that doesn't actually motivate the experiment, the committee can't tell. Human review of the annotation file is the only check.

These three classes are exactly the cases where the human's reading matters most. The committee buys the human time to focus on them.

## 9.9 The forensic-audit.md file as the review record

For each task, `<task>/forensic_audit.md` is the persistent review record. The file has the schema:

```
# Forensic Audit — <task slug>

**Verdict:** PASS / FAIL / PASS_WITH_WARN
**Run at:** 2026-05-16 14:23:08
**Hash of last log entry:** ...

## Agent A — split-hash integrity
<verdict + numerical evidence>

## Agent B — target / label leakage
<verdict + per-feature MI top-5>

... (one section per agent) ...

## Committee summary
<Z's aggregate + risks list>
```

The file is committed to the repo, never edited by hand. Re-running the audit overwrites it deterministically (the same inputs produce the same file). A reviewer who wants to spot-check a task reads this file; a reviewer who wants to audit the auditor reads `framework/forensic_audit.py`.

## 9.10 Related

- [Ch. 8 — Style Guides and Rules](08_style_guides_and_rules.md): the rules the committee is enforcing.
- [Ch. 11 — Testing Overview](11_testing_overview.md): the committee as Layer 2 of the four-layer gate.
- [Ch. 19 — Critique-Equivalent Tool](../part_4_tools/19_critique_code_review_tool.md): the `forensic_audit.md` file as our Critique.
- [Appendix A](../appendix_a_postmortems/): five concrete cases where the committee was the only thing standing between a bug and a green cohort.
- [`framework/forensic_audit.py`](../../framework/forensic_audit.py): the implementation.
