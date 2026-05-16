# Chapter 2 — Working Well With Agents

> *Parallel to:* SWE-book Chapter 2 *"How to Work Well on Teams"* (Winters, Manshreck, Wright 2020).

**Thesis.** A team in the SWE-book is a group of humans whose individual fallibility is mitigated by shared culture and review. A team in the DSBench project is a human plus an LLM collaborator (Claude Code) plus 10 forensic-audit agents plus a validator plus a build system. The collaborator's individual fallibility is real and well-documented; the team mitigates it the same way the SWE-book recommends: through Humility, Respect, and Trust (HRT) made concrete in artefacts.

## 2.1 The team composition

The SWE-book's chapter 2 opens with the observation that software engineers are not lone geniuses — they work in teams, and the team's culture matters more than any individual member's IQ. In our project the team has the following composition:

| Member | Strengths | Failure modes | Mitigation |
|---|---|---|---|
| **Human operator (Evi)** | Long-horizon judgement, holds the project thesis, decides what counts as "done", commits checkpoints. | Cannot run 14,000 experiments by hand. Subject to fatigue, attention drift. | Delegates execution to Claude; reviews every commit; spot-checks per-task `forensic_audit.md`. |
| **Claude Code (LLM)** | Drives the experiment loop, writes annotations, refactors framework code, generates per-task scaffolds. | No persistent memory between sessions. Capable of fabricating numbers (the "synthetic-data placeholder" failure mode — see [postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md)). | Six-Field Annotation Rule; crash-recovery checkpoint after every experiment; static-code grep for `X_test`. |
| **Forensic committee (10 agents)** | Independent concerns, no shared state, parallel verdicts. | Calibration drift on new problem types (false positives on `qa_excel` early; see [postmortem 0003](../appendix_a_postmortems/0003_forensic_false_positive_val_gt_train.md)). | Problem-type-aware thresholds; Agent J's "record-only" verdict; Agent Z committee aggregator. |
| **Validator** | Cheap, fast, machine-readable PASS/FAIL on every commit. | Substring matching is blind to semantics. | Forensic committee catches what the validator misses; the two layers are complementary. |
| **Build system** | Idempotent, reproducible, single-command refresh. | Silent failure if intermediate state is stale. | Layer-4 audit (`audit_pack.py`) and `_final_audit.py` re-detect coverage. |

The point of the table is to make explicit that the team is *heterogeneous*. Different members have different fallibility profiles. The forensic agents do not catch what the validator catches (and vice versa); the human does not catch what either catches. The four-layer gate is what makes the heterogeneity productive.

## 2.2 Humility, Respect, Trust — applied to an LLM collaborator

The SWE-book lists Humility, Respect, and Trust as the foundational team values. They translate directly to LLM-collaborator work:

### 2.2.1 Humility

**The human is not the smartest member of the team.** Claude often spots optimisation directions the human missed (e.g. the per-position letter prior for `qa_excel` — Bishop 2006 *Pattern Recognition and Machine Learning* §3.5 — was Claude's idea, captured in `experiment_log.jsonl` exp 14 of `2012-round-2-find-that-error`). The reverse is also true: when Claude proposes "I'll just check the test score quickly", the human says no, every time. Neither member of the team gets to skip the audit gate on grounds of seniority.

### 2.2.2 Respect

Respect is reified in the protocol. Claude does not get told "just do it"; Claude gets told "here's the protocol — read CLAUDE.md, then proceed." When Claude makes a mistake, the human files a Lessons-Learned row, not a complaint. The 26 rows in the Lessons-Learned table across the per-task `CLAUDE.md` files are the entire history of corrections; each entry is dated, sourced, and tied to a specific commit. The protocol respects the collaborator enough to assume the next session will read the corrections.

### 2.2.3 Trust

Trust is bidirectional and earned. The human trusts Claude to checkpoint after every experiment, to write six-field annotations, to never grep `X_test` outside `final_report.py`. Claude trusts the human to commit the work, to push to GitHub, to run the `_final_audit.py` aggregator before declaring a session done. The Four-Layer Gate Rule ([Ch. 11](../part_3_processes/11_testing_overview.md)) is the contract that makes trust verifiable.

## 2.3 The session-start ritual

The SWE-book chapter 2 talks about onboarding new team members. Every Claude session is a new team member. The session-start ritual, codified in every per-task `CLAUDE.md` and the framework template (`framework/CLAUDE_template.md` § "On Session Start"):

1. **Read the checkpoint** (`memory/project_autoresearch_checkpoint.md`) — the most recent state of the team's joint memory.
2. **Read the last 3 rows of `experiment_log.jsonl`** + `best_config.json` — verify state.
3. **Read `seed_reasoning.json`** — the first-experiment plan, frozen at scaffold generation.
4. **Resume the loop** — diagnose → cite → hypothesise → predict → run ONE → analyse → checkpoint. Don't ask "what do I do"; the checkpoint says.
5. **Start the dashboard** once per session, in the background.
6. **Issue experiments** via `run_autoresearch.py --backbone <b> --description "..."`.

A session that skips step 1 is a session that is not part of the team. The validator does not enforce the ritual (substring grep can't); the human enforces it by reading the next commit and rejecting work that doesn't reference the checkpoint.

## 2.4 The Lessons-Learned table — the team's append-only memory

Across the 112 per-task `CLAUDE.md` files there is a "Lessons Learned" table that is *append-only*. Twenty-six rows as of commit `1be5130`. The schema:

| Row | Date | Trigger | Lesson | Codified in |
|---|---|---|---|---|
| ... | 2026-05-15 | Human correction during code review | Statement of the rule | Pointer to the file that enforces it (validator pattern, forensic agent, skill SKILL.md, etc.) |

Two example rows from `framework/CLAUDE_template.md`:

> Row 18 (2026-05-15) — *Composite metric sign convention.* RMSE / MAE must be negated inside `_score` so the composite formula `min(val, train) - 0.05 * |val - train|` is metric-agnostic. Codified in `framework/runner.py:_score` and `skills/autoresearch-pack/skills/metric-sign-convention/SKILL.md`.

> Row 26 (2026-05-15) — *Status-counting asymmetry.* `final_rollup.json` does not carry `kind` (modeling vs analysis); `forensic_summary.json` does. Aggregation scripts must therefore join on slug, not assume both rows have the same shape. Codified in `framework/_status.py` and `framework/_final_audit.py`.

The table is append-only by convention. If a row is wrong, you add a corrective row; you do not delete the original. The SWE-book's chapter 2 makes the same recommendation for team retrospectives.

## 2.5 The blame-free postmortem

The SWE-book — and SRE practice generally — emphasises blameless postmortems. Our five postmortems in [Appendix A](../appendix_a_postmortems/) follow the Five-Whys + Action-Items format. Each one names the *mechanism* of the failure, not the *culprit*. The phrase "Claude did X" does not appear; the phrase "the validator did not enforce X" does. This is intentional. The mitigation is always a tooling or process change, never a "Claude should be more careful" instruction.

This matters because the team is going to keep working with a stateless LLM collaborator. "Claude should be more careful next time" is not a mitigation; the next session is a clean instance and remembers nothing. "The validator now greps for X" is a mitigation that survives the collaborator forgetting.

## 2.6 Asynchronous collaboration

SWE-book chapter 2 emphasises that good teams work asynchronously — code review, design docs, and CL comments let team members contribute without all being online at once. The DSBench team's asynchrony is even more extreme: the human and Claude are *almost never* online at the same time. The handoff happens through the repository.

The artefacts that carry handoffs:

| Artefact | Direction | Frequency | Lifetime |
|---|---|---|---|
| `memory/project_autoresearch_checkpoint.md` | Claude → next-Claude | After every experiment | Until next experiment |
| `experiment_log.jsonl` | Claude → reviewer | Append-only | Forever |
| `reasoning_annotations.json` | Claude → reviewer | Append-only | Forever |
| `forensic_audit.md` | Forensic → human | Per audit run | Until next audit |
| Lessons-Learned row | Human → Claude | On every correction | Forever |
| `framework/CLAUDE_template.md` | Human → all future tasks | On framework change | Forever |
| Git commit message | Human → posterity | Per commit | Forever |

The lifetime column matters. The checkpoint is ephemeral; the experiment log is not. Confusing the two is the failure mode behind [postmortem 0001](../appendix_a_postmortems/0001_regression_delta_sign_bug.md) (regression-delta sign bug — the diagnosis was right in the checkpoint but the bug had been baked into `experiment_log.jsonl` for 87 experiments and could not be retroactively fixed).

## 2.7 What "good team behaviour" looks like in practice

The SWE-book gives a checklist for team behaviour. Our parallel:

- **Do leave the campsite cleaner than you found it.** If you touch a per-task `CLAUDE.md`, regenerate the section coverage. If you touch a framework function, regenerate the SOTA catalogue digest. If you touch a skill, re-run `audit_pack.py`.
- **Don't be a "lone gun" agent.** No commit without the four-layer audit gate green. Even when you (the human) are certain the change is trivial, the gate still runs — that's the rule's point. See [Ch. 11](../part_3_processes/11_testing_overview.md).
- **Do write the rationale.** Every commit message names the failure mode it mitigates, the new lesson it codifies, and the SKILL/ADR/postmortem it touches.
- **Don't optimise the protocol away.** The protocol is the team's contract. The Per-Backbone 25-Experiment Mandate exists *because* the collaborator forgets which axes are exhausted. Skipping iters 23–25 because they "look exhausted at iter 22" is the failure mode the rule was built to prevent.

## 2.8 Related

- [Ch. 3 — Knowledge Sharing](03_knowledge_sharing.md): how the 44-skill industry-shareable pack codifies the team's working knowledge.
- [Ch. 5 — How to Lead an Agent Team](05_how_to_lead_an_agent_team.md): orchestrating parallel agents.
- [Ch. 10 — Documentation](../part_3_processes/10_documentation.md): the Six-Field Annotation Rule.
- [Appendix A](../appendix_a_postmortems/) — concrete examples of the failure modes named above.
