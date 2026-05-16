# Chapter 6 — Leading at Scale

> *Parallel to:* SWE-book Chapter 6 *"Leading at Scale"* (Winters, Manshreck, Wright 2020).

**Thesis.** Leading one task is leading at the experiment level. Leading 112 tasks is leading at the cohort level. Leading a benchmark family is leading at the protocol level. As the scale axis stretches, the leader's job shifts from doing the work to making *the protocol that does the work* increasingly robust to scale-induced failure modes.

## 6.1 The three scale regimes

The DSBench project has lived in three scale regimes since the May 2026 initial commit. Each regime exposed a different class of failure that single-task work does not.

| Regime | Scale | Defining artefact | Defining failure mode |
|---|---|---|---|
| **Single-task** | 1 task | `experiment_log.jsonl` | Per-experiment bugs (sign convention, label leakage). |
| **Cohort** | 112 tasks | `registry/final_rollup.json`, `registry/forensic_summary.json` | Cross-task aggregation bugs; one slow task blocks the cohort. |
| **Protocol** | Arbitrary benchmark | `framework/CLAUDE_template.md`, the `autoresearch-pack` skill bundle | Protocol clauses that worked for FX but not for tabular ML. |

The SWE-book describes the same three levels at Google: the team leader, the senior engineering manager, and the staff-engineer / director. The job titles differ; the rotational change is the same. The leader who used to write code now writes the system that writes the code.

## 6.2 The cohort-level fan-out

The single-task pipeline (`runner.py:run_one` → `hill_climb.py` → `final_report.py` → `forensic_audit.py` → `build_submission.py`) fan-outs to 112 tasks via `framework/run_all.py`. The fan-out has three rules:

1. **No shared mutable state across tasks.** Each task has its own `autoresearch_results/`, its own `data/.data_cache/`, its own `forensic_audit.json`. The only shared state is `registry/final_rollup.json` and `registry/forensic_summary.json`, which are *written once at the end* by aggregator scripts that read every task's own file.
2. **Per-task isolation of failure.** A crash in task `2014-round-1-snakes-and-ladders` does not abort the cohort. The runner logs the failure and continues. The aggregator script counts the failure as `forensic_verdict: error` and the cohort proceeds.
3. **Idempotent re-runs.** Running `run_all.py` twice does not double-count experiments. The runner reads the current `experiment_log.jsonl` and resumes from `len(log) + 1`. The `_status.py` snapshot is computed from the on-disk state, not from any in-memory counter.

These rules are not negotiable at the cohort level. A single-task pipeline that violates them works fine; a 112-task pipeline that violates them is unmaintainable.

## 6.3 The aggregation asymmetry

A subtle scale failure surfaced during the May 2026 work and is now Lessons-Learned row 26: **`final_rollup.json` rows do not carry `kind` (modeling vs analysis); `forensic_summary.json` rows do**. The reason: the final rollup's row is the test-set score and is the same shape for every task; the forensic summary's row needs to know `kind` because the problem-type-aware thresholds depend on it.

The asymmetry caused a subtle bug in `_status.py`: an early version of the script joined the two rollups by index and assumed both carried `kind`, producing wrong cohort counts when a task was in one rollup but not the other. The fix: join by slug, treat missing entries explicitly, and document the asymmetry in the row.

This is the kind of scale-induced bug that does not exist at single-task scale. It exists *only* because there are two parallel rollups that have to agree.

## 6.4 What stays the same as scale grows

The Per-Backbone 25-Experiment Mandate stays the same. The Test-Set Embargo Rule stays the same. The Six-Field Annotation Rule stays the same. The Citation-Rigor Rule stays the same. The Four-Layer Gate Rule stays the same. These five rules are *invariant* across scale.

This is the SWE-book's chapter-6 thesis: the *culture* survives scale, the *implementation* mutates. The validator at 1 task is a function call; at 112 tasks it's a script that loops over `modeling/*/CLAUDE.md`; at 540 tasks it's the same script with sharding and parallel I/O; at arbitrary scale it's a CI pipeline with a per-task worker pool. The rule "every `CLAUDE.md` has the 36 sections" is the same in all four cases.

## 6.5 What changes as scale grows

| Scale | Validator | Forensic | Dashboard | Submission archive |
|---|---|---|---|---|
| 1 task | one function call | one script call | one HTML file | one folder |
| 10 tasks | a for-loop | a for-loop | a cross-task index page | a folder of folders |
| 112 (current) | a for-loop with progress bar | a for-loop with `--limit` flag | a two-tab page with `<details>` and a paginated table | 112 folders, archived per kind/slug |
| 540 (hypothetical) | parallel I/O with shard manifests | a job pool with per-task workers | server-side pagination; client-side filtering only | per-kind tarballs |
| Arbitrary | CI pipeline + worker pool | CI pipeline + worker pool | static site generator + search index | object storage with manifest digest |

The point of the table is that each *cell* shows a different engineering artefact. The protocol doesn't change; the artefact does. The leader's job at scale is to choose the right artefact for the current scale and to *retire* the previous artefact cleanly (see [Ch. 15 — Deprecation](../part_3_processes/15_deprecation.md)).

## 6.6 The protocol-level leadership decisions

At the protocol level, the leader's decisions are not "what's the next experiment" but "what's the next *rule*". Three protocol-level decisions made during the DSBench work:

### 6.6.1 The 200-iter extended phase

The base 25-iter × 5-backbone loop produces 125 experiments per task. After the first cohort run, ~30 tasks still hadn't beaten their DSBench baseline. The leader's options:

- Give those tasks more iterations on the same backbones (low ROI; the axes were exhausted).
- Add new backbones (higher ROI; the loss tasks were structurally different from the wins).
- Declare the cohort done and ship at 82/112.

The decision: a **200-iter extended phase** ([ADR 0006](../appendix_b_adrs/0006_extended_200_iter_phase.md)) that adds 15 backbone families with per-family citations. This is a protocol-level decision because it changes the rule for every loss task, not the prescription for any one task. The implementation: `framework/extended_hill_climb.py`. Cohort result: lifted from 82/112 BEAT (pre-extension) to ... no improvement actually, but the audit story is more complete because every loss task now has a documented 325-iter trail. The decision was right even though the cohort number didn't move; without the extension, the loss tasks would have an unexplored ceiling and the audit would be incomplete.

### 6.6.2 The cross-task pooling discipline

When the original `_excel_agent` was discovered to be training on synthetic data ([postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md)), the protocol-level decision was: *pool training data across all 38 qa_excel tasks, evaluate per-task*. This is one rule, applied across 38 tasks. The leader's job was to write the rule into [ADR 0008](../appendix_b_adrs/0008_cross_task_pooling_for_training.md) and the `cross-task-pooling-discipline` skill, then let the framework apply it.

### 6.6.3 The four-layer audit gate consolidation

Pre-May 2026, the validator ran as a standalone check. The forensic audit ran separately. The 14-section explainability report was written manually. The skill-pack audit was nascent. The leader's protocol-level decision was to *name* the four layers, write the contract, and consolidate the rollup into `framework/_final_audit.py` so a single command reports the cohort's gate state. This is [ADR 0015](../appendix_b_adrs/0015_four_layer_audit_gate.md).

## 6.7 The 112 → 540 → arbitrary growth path

If the cohort grew to 540 (a 5× expansion), what would have to change?

1. **Per-task CLAUDE.md generation must remain fast.** Currently `framework/generate_scaffolds.py` runs in ~30 seconds for 112 tasks; at 540 it would be ~3 minutes. Still fine.
2. **The forensic audit needs sharding.** Currently `framework/forensic_audit.py` runs 10 agents × 112 tasks sequentially in ~5 minutes; at 540 it would be ~25 minutes. Sharding by `--shard 0/5` ... `--shard 4/5` and running in parallel would cut this to ~5 min again.
3. **The dashboard needs server-side pagination.** Currently the page loads all 112 rows; at 540 the DOM gets slow. Switch to server-side pagination with client-side filtering.
4. **The submission archive needs object storage.** Currently 112 folders × 14 files = 1568 files. At 540 it's 7560 files. Filesystem performance degrades; switch to per-kind tarballs or object storage.

What does *not* change: the protocol rules (Test-Set Embargo, Six-Field Annotation, Citation Rigor, Four-Layer Gate, Per-Backbone 25). The leader's job at 540-scale is to make sure those rules still hold.

## 6.8 The "build vs buy" decision at scale

The SWE-book chapter 6 talks about when to build vs when to buy. Our analogue: when to write protocol vs when to adopt protocol from the source autoresearch project. The skill pack's coverage matrix in `skills/autoresearch-pack/coverage_matrix.md` tracks every section in the source CLAUDE.md (`autoresearch/CLAUDE.md` and `autoresearchspy/CLAUDE.md`) and maps it to a sub-skill. New rules we add (the 8 DSBench-specific corrections in the corrections category) are written from scratch; existing rules we inherit verbatim. This is build-when-novel, buy-when-shared.

## 6.9 Related

- [Ch. 5 — How to Lead an Agent Team](05_how_to_lead_an_agent_team.md): the per-task version of leadership.
- [Ch. 7 — Measuring Engineering Productivity](07_measuring_engineering_productivity.md): the metrics that prove the leadership decisions worked.
- [Ch. 22 — Large-Scale Changes](../part_4_tools/22_large_scale_changes.md): the tooling for scaling up.
- [Appendix B](../appendix_b_adrs/): the 15 ADRs, each one a protocol-level leadership decision.
