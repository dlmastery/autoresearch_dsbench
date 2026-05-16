# Chapter 19 — Critique: Our Code-Review Tool

> *Parallel to:* SWE-book Chapter 19 *"Critique: Google's Code Review Tool"* (Winters, Manshreck, Wright 2020).

**Thesis.** Google built Critique because manual code review at Google's scale required tooling. The DSBench project does code review through a 10-agent forensic committee that writes a persistent verdict per task to `forensic_audit.md`. That file is our Critique: it carries the verdict, the per-agent rationale, and the timestamped audit trail. A reviewer reads it the way a Google engineer reads a Critique CL.

## 19.1 What `forensic_audit.md` is

For each of the 112 tasks, `<task>/forensic_audit.md` is the persistent code-review record. The file is regenerated every time `framework/forensic_audit.py` runs. Its schema:

```markdown
# Forensic Audit — <task slug>

**Verdict:** PASS / FAIL / PASS_WITH_WARN
**Run at:** 2026-05-16 14:23:08
**Last log hash:** <16-char SHA-1>
**Kind:** modeling / analysis
**Problem type:** classification_binary / regression / qa_excel / ...

## Agent A — split-hash integrity
<verdict + numerical evidence>

## Agent B — target / label leakage
<verdict + per-feature MI top-5>

## Agent C — row overlap
<verdict + counts>

## Agent D — distribution shift (KS)
<verdict + flagged features>

## Agent E — anomaly detector
<verdict + flagged experiments>

## Agent F — static-code audit
<verdict + grep output>

## Agent G — temporal order
<verdict + N/A on synthetic>

## Agent H — seed stability
<seed-perturbation evidence>

## Agent I — refit consistency
<refit delta vs recorded test_score>

## Agent J — backbone diversity
<distinct backbones; WARN if < 3>

## Committee verdict (Agent Z)
<aggregate + risks list>
```

A reviewer reading the file can see exactly which agent flagged what, what the threshold was, and what the agent's reasoning was. The file is committed to the repo, so it appears in `git diff` when the audit changes.

## 19.2 Why the file is the review record

The SWE-book chapter 19 emphasises that Critique's persistence is the key feature: a code review at Google leaves an audit trail that survives the developer's session. Our equivalent:

- The forensic-audit file is *persistent* — committed to the repo, surviving any session.
- The forensic-audit file is *per-task* — granular enough to debug one task without reading the whole cohort.
- The forensic-audit file is *deterministic* — re-running the audit on a clean repo produces the same file content (modulo timestamps in the header).
- The forensic-audit file is *integrated* — the dashboard renders it inline (Lessons-Learned row 24); the cohort scoreboard reads its verdict.

The four properties give the same affordance as a Critique CL: a durable record of the review, accessible to any reviewer, integrated with the build's status.

## 19.3 The committee verdict (Agent Z)

The aggregator that produces the "LGTM equivalent":

```python
def _committee_verdict(per_agent: dict) -> dict:
    fails = [k for k, v in per_agent.items() if v.get("verdict") == "FAIL"]
    warns = [k for k, v in per_agent.items() if v.get("verdict") == "WARN"]
    if fails:
        return {"verdict": "FAIL", "fails": fails, "warns": warns, "risks": _gather_risks(per_agent)}
    if warns:
        return {"verdict": "PASS_WITH_WARN", "warns": warns}
    return {"verdict": "PASS"}
```

Three verdicts:

- **PASS** — every Agent A–I returned PASS; no Agent J warning.
- **PASS_WITH_WARN** — every Agent A–I returned PASS; ≥ 1 Agent J warning (low backbone diversity is the usual cause).
- **FAIL** — at least one Agent A–I returned FAIL.

The cohort scoreboard counts PASS and PASS_WITH_WARN as "forensic PASS" (since Agent J is record-only). A FAIL blocks the task from contributing to BEAT-DSBENCH.

## 19.4 The "discussion threads" analogue

Critique has discussion threads on each line of the CL. We do not have per-line discussion; the committee's per-agent section is the unit of discussion. A reviewer who disagrees with Agent E's verdict can:

1. Open an issue or a Lessons-Learned row explaining the disagreement.
2. Propose a calibration change (e.g. "whitelist sklearn early-stopping val > train") in a new ADR.
3. Update `framework/forensic_audit.py:_agent_e` with the new calibration.
4. Re-run the audit. The new `forensic_audit.md` reflects the change.

This is the structural equivalent of "argue with the reviewer until LGTM". The reviewer here is a script; the argument is in the ADR; the LGTM is the new `forensic_audit.md`.

[ADR 0010](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md) is the canonical example: it documents the disagreement with the pre-ADR Agent E threshold, the rationale (Bishop 2006 *Pattern Recognition and Machine Learning* §5.5.2), the calibration change, and the new threshold.

## 19.5 The "presubmit" analogue

Critique's presubmit checks are mandatory tests that must pass before a CL can be submitted. Our presubmit is `framework/_final_audit.py`: a single script that runs all four layers and exits non-zero if any layer is red. The convention is to run it before every commit that changes experiment state; pushing a red-gate state to `main` is forbidden by convention.

The script is the project's CI binding. [Ch. 23](23_continuous_integration.md) covers the full CI story.

## 19.6 The "snapshot" analogue

Critique lets a reviewer see successive snapshots of a CL (the original, after each round of feedback). Our equivalent: every cohort run produces a new `forensic_audit.md`; `git log -p <task>/forensic_audit.md` shows the file's evolution across cohort runs. A reviewer can see when an Agent's verdict changed for a task and which commit caused it.

This is weaker than Critique (we don't store per-author drafts), but it serves the same purpose: the audit trail is durable and inspectable.

## 19.7 What the file deliberately is not

A few things `forensic_audit.md` is not:

- **It is not editable.** A human who edits the file by hand is overwriting the audit. The next `forensic_audit.py` run will regenerate the file deterministically; the manual edit is lost. The audit is the source of truth, not the human.
- **It is not the final word.** A FAIL verdict can be a false positive (e.g. Agent E on regression early-stopping). The human can disable the failing check with documented ADR + recalibration + new audit run.
- **It is not multi-task.** Each task has its own file. The cross-task summary is `registry/forensic_summary.json`. A cross-task narrative does not exist; the per-task files are the unit.

## 19.8 The dashboard's inline rendering

A specific UX choice: the per-task dashboard (`autoresearch_results/dashboard.html`) renders `forensic_audit.md` inline. The reviewer does not have to switch to a Markdown viewer; the dashboard's MD viewer parses the file and renders it in a tab. This is Lessons-Learned row 24: "MD viewer inline rendering".

The implementation: a tiny vanilla-JS Markdown renderer in the dashboard template. Pre-fix, the dashboard provided only a "Download forensic_audit.md" link; the reviewer would download, open in a Markdown editor, switch back. Post-fix, the file renders in the dashboard's "Forensic Audit" tab.

## 19.9 The "integration with build status" analogue

In Critique, the build status of the CL is shown next to the CL. Our equivalent: the cohort dashboard at `dashboard/index.html` carries per-task columns for `forensic_verdict` (PASS / WARN / FAIL) and `beats_dsbench` (yes / no). A reviewer can sort the table by verdict and immediately see which tasks need attention.

The cohort dashboard is regenerated by `_refresh_dashboards.py`. It is the single page a reviewer would land on to triage the cohort.

## 19.10 Related

- [Ch. 9 — Code Review](../part_3_processes/09_code_review.md): the conceptual framework for the forensic committee as code review.
- [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md): the four-layer audit gate.
- [Ch. 20 — Static Analysis](20_static_analysis.md): Agent F (static-code).
- [`framework/forensic_audit.py`](../../framework/forensic_audit.py): the implementation.
- [ADR 0004 — 10-agent forensic committee](../appendix_b_adrs/0004_10_agent_forensic_committee.md): why ten agents.
