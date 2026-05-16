# Chapter 5 — How to Lead an Agent Team

> *Parallel to:* SWE-book Chapter 5 *"How to Lead a Team"* (Winters, Manshreck, Wright 2020).

**Thesis.** Leading a software team is mostly about making decisions, removing blockers, and protecting the team's culture. Leading an agent team is the same plus one twist: the agent collaborator has no memory across sessions, so every leadership decision must be encoded in artefacts the next session will read. The leader's primary deliverable is the artefact, not the conversation.

## 5.1 The two managerial anti-patterns from the SWE-book

The SWE-book chapter 5 names two anti-patterns: the *unwilling-to-decide* manager and the *micromanager*. Both translate directly to LLM-collaborator work.

### 5.1.1 Unwilling to decide

The "unwilling-to-decide" failure mode: the human keeps asking Claude "what do you think?" without ever stating the constraint. Claude proposes three options, the human picks one, the next session starts cold and re-proposes three different options, the human picks differently, and the protocol drifts.

The mitigation is the **Architectural Decision Record (ADR)**. When a real decision happens, it gets written into [Appendix B](../appendix_b_adrs/) in Michael Nygard format (context, decision, consequences). The 15 ADRs in this repository are the project's decision history. An ADR that exists cannot be re-opened by the next session unless the human explicitly supersedes it.

Examples of decisions that lived as drift before they were ADRed:

- **Train/val for hill-climb, train+val for qa_excel refit.** Drifted between "train only" and "train+val" in the early qa_excel work until [ADR 0009](../appendix_b_adrs/0009_qa_train_plus_val_refit.md) pinned it.
- **Composite metric formula.** Drifted between three formulations before [ADR 0003](../appendix_b_adrs/0003_composite_metric_min_min_minus_gap.md) pinned `min(val, train) - 0.05 * |val - train|`.
- **25 iters per backbone.** Drifted between 10, 25, 50 before [ADR 0005](../appendix_b_adrs/0005_25_iters_per_backbone.md) pinned 25.

### 5.1.2 Micromanagement

The "micromanagement" failure mode: the human writes the next experiment's hyperparameters into the checkpoint themselves, leaving Claude with no decision space. Claude's contribution drops to executing the human's prompt verbatim, and the autoresearch hypothesis (Claude can drive the loop) dies.

The mitigation is the **Karpathy Agent Protocol**: Claude proposes the next experiment from the current best config + the citation library + the previous result; the human reviews; if the proposal is sound, it runs. The human's leadership role is to *review the proposal*, not to author it. The `karpathy-agent-protocol` skill codifies the workflow.

## 5.2 The leader's daily artefacts

A typical day in this project produces five artefacts, in roughly this order:

| Artefact | Author | Purpose | Frequency |
|---|---|---|---|
| Per-experiment six-field annotation | Claude | The thought process behind one experiment | Per experiment (typically 5–25 per day) |
| Checkpoint update | Claude | The state the next session will resume from | After every experiment |
| Lessons-Learned row | Human | Codify a correction so the next session doesn't repeat the mistake | Per session, sometimes none |
| Commit message | Human | The narrative of the day's work | Once or twice per day |
| ADR | Human | A new structural decision | Per session, often zero |

The leader (human) writes commits, Lessons-Learned rows, and ADRs. The leader does *not* write annotations or checkpoints — those are Claude's deliverables. A leader who writes Claude's annotations is micromanaging; a leader who lets Claude write Lessons-Learned rows is delegating decisions Claude shouldn't be making (Claude's session memory dies; the leader's doesn't, so the leader owns the long-horizon learning).

## 5.3 The protocol-first leadership stance

The SWE-book chapter 5 emphasises that good leaders make *systems-level* decisions, not *case-by-case* ones. The DSBench parallel: the leader works on the *protocol*, not on the *task*. When `2014-round-1-precise-debt-modeling` is stuck, the leader does not hand-craft the next experiment for that task. The leader asks "why is the protocol not solving this?" and changes the protocol.

Concretely, every time a task is stuck the leader has three legal moves:

1. **Add a new backbone family** to `framework/extended_hill_climb.py` and cite the paper that motivates it. This affects every stuck task, not just the current one. See [ADR 0006](../appendix_b_adrs/0006_extended_200_iter_phase.md).
2. **Loosen an audit threshold** that was producing false positives, citing the empirical evidence and adding a skill that documents the calibration. See [ADR 0010](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md).
3. **Add a Lessons-Learned row** if the diagnosis surfaced a class of mistake the protocol hadn't named. The row goes into `framework/CLAUDE_template.md` and propagates to every task on the next scaffold regeneration.

A leader who hand-crafts the next experiment for a specific task is treating the symptom, not the disease.

## 5.4 The orchestration ladder

Multi-agent orchestration scales the team. Three rungs of the ladder, each used in this project:

### 5.4.1 Single agent, sequential

The default. One Claude session, one task at a time, 25 iters per backbone. Most reliable. Used for any task with non-trivial debugging.

### 5.4.2 Single agent, fan-out across tasks

`framework/run_all.py` invokes the single-task runner for each of the 112 tasks in sequence. Identical protocol per task; only the task slug changes. This is parallelism at the *task* level (the 112 invocations are independent) but sequential at the *experiment* level inside any one task.

### 5.4.3 Multiple agents, parallel

`framework/run_all.py --kind modeling` and `--kind analysis` can run as two background processes simultaneously (one for the 74 modeling tasks, one for the 38 analysis tasks). They write to disjoint directories (`registry/run_all_stdout.log` vs `registry/run_all_analysis_stdout.log`) so they cannot collide. This is `parallel-agent-orchestration` skill territory.

The orchestration choice is a leadership call. Parallel agents go ~1.8× faster than sequential but produce two parallel commit streams that the leader must merge, and a crash in one agent can leave the other in an inconsistent state. For the May 2026 final run we used sequential; for the May 2025 mid-run rebuild we used parallel. [Ch. 6](06_leading_at_scale.md) covers the scale tradeoff in more detail.

## 5.5 What the leader actually owns

Across the 112 tasks there are roughly three job functions:

| Function | Who | Examples |
|---|---|---|
| Per-task execution | Claude | Run iter 7 of xgboost on titanic; write the annotation; checkpoint. |
| Cross-task orchestration | `framework/run_all.py` + Claude | Loop over all 74 modeling tasks; aggregate `final_rollup.json`. |
| Project leadership | Human | Decide the next ADR; merge stuck-task escalations; commit; push; tell the user "we beat 82/112". |

The leader's job is the third row. The first two rows can in principle be delegated entirely to automation; the third row cannot, because the third row makes the decisions that bind the first two.

## 5.6 The escalation pathway

A task that fails the four-layer audit gate is *escalated*. The escalation pathway:

1. Claude detects the failure and writes the failure mode into `forensic_audit.md` and the checkpoint.
2. Claude does *not* attempt to fix it silently. The whole point of the audit gate is that silent fixes are forbidden.
3. The next human session reads the `forensic_audit.md` and decides: is this a calibration issue (false positive)? a real bug? a class-of-bugs issue?
4. The fix lands as an ADR (if structural), a postmortem entry (if a real bug), a Lessons-Learned row (if a one-off correction), or a code change to `framework/` (if the framework is wrong).
5. Re-run the audit gate. Until it's green, no commit.

This is the SWE-book's pattern for incident management adapted to a single-operator project. The leader owns the escalation. Claude does not.

## 5.7 The Beyoncé Rule, applied

> "If you liked it, you should have put a CI test on it." — SWE-book Chapter 1.

Every leadership decision in this project ends with the question: *what runs in CI to enforce this?* If the answer is "nothing", the decision is informal and will drift. ADRs are the formal version of the question. The 15 ADRs in Appendix B each list, in their Consequences section, the CI hook that enforces them. For example:

- ADR 0003 (composite metric) → `framework/runner.py:_composite` plus the validator's grep that the formula appears in the file.
- ADR 0005 (25 iters per backbone) → `framework/hill_climb.py` constant `ITERS_PER_BACKBONE = 25` plus the validator's substring check on per-task `CLAUDE.md`.
- ADR 0007 (stride-5 interleaved split) → `framework/runner.py:_qa_split` plus Agent A's hash check on the manifest.

A decision without a CI hook is a wish, not a decision.

## 5.8 Related

- [Ch. 6 — Leading at Scale](06_leading_at_scale.md): what changes when the cohort goes from 1 → 112 → 540 → arbitrary.
- [Ch. 9 — Code Review](../part_3_processes/09_code_review.md): the forensic committee as code review.
- [Ch. 23 — Continuous Integration](../part_4_tools/23_continuous_integration.md): the four-layer audit gate as CI.
- [Appendix B](../appendix_b_adrs/): the 15 ADRs.
