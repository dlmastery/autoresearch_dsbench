# Chapter 7 — Measuring Engineering Productivity

> *Parallel to:* SWE-book Chapter 7 *"Measuring Engineering Productivity"* (Winters, Manshreck, Wright 2020).

**Thesis.** Engineering productivity is measurable only if you can name a unit of work that's not gameable. Lines of code are gameable. Commits are gameable. Experiments completed is gameable. The DSBench project's productivity metric is the **BEAT-DSBENCH × FORENSIC-PASS × COVERAGE** triple: a task counts as "done" only if it beats the published DSBench baseline *and* passes the 10-agent forensic committee *and* keeps the skill-pack at 100 % coverage. Any one of the three at zero invalidates the row.

## 7.1 Why the triple

The SWE-book's chapter 7 lists the failure modes of single-number productivity metrics. The DSBench parallel is direct:

| If we measured only ... | We would game it by ... | What we'd lose |
|---|---|---|
| BEAT-DSBENCH count | Setting `dsbench_baseline` artificially low. | The whole point of the project: actually beating a real published baseline. |
| FORENSIC-PASS count | Silently lowering forensic thresholds. | The audit's reason to exist. |
| Skill-pack coverage | Adding empty SKILL.md files. | The protocol's transferability. |
| Experiments per day | Running shallow grid searches. | The Karpathy citation discipline. |
| Lines of code | Padding `framework/runner.py` with noise. | The runner's readability. |

The triple BEAT × FORENSIC × COVERAGE is gameable only if you game all three at once, which would require coordinated effort and would still leave a paper trail in `experiment_log.jsonl`. The triple is the productivity metric.

## 7.2 The four headline numbers

Four numbers, each tied to a script that produces them:

### 7.2.1 BEAT-DSBENCH: 82 / 112

`framework/_status.py` reads `registry/final_rollup.json` and counts tasks where `beats_dsbench: true`. A task beats DSBench when `final_report.test_score > dsbench_baseline`. The headline at commit `1be5130` is **82 / 112 BEAT (73 %)**.

The number is meaningful because:

- It uses the published DSBench paper's baselines (`registry/modeling_tasks.json` and `registry/analysis_tasks.json` carry the upstream numbers).
- The test score is computed by `framework/final_report.py`, which is the only function in the codebase that legally touches the test set (Test-Set Embargo Rule).
- The number is checked by Agent I (refit consistency) of the forensic committee — refitting the champion config and re-scoring must match within ±0.005.

### 7.2.2 FORENSIC-PASS: 112 / 112

`framework/_status.py` reads `registry/forensic_summary.json` and counts tasks where `verdict: PASS`. The headline is **112 / 112 PASS**.

What "PASS" requires:

- Agent A (split-hash): manifest hashes match the actual `.npz`.
- Agent B (target leakage): max MI ≤ 0.9 on tabular; calibrated for qa_excel.
- Agent C (row overlap): zero shared rows across train / val / test of the same task.
- Agent D (distribution shift): ≤ 10 % flagged features.
- Agent E (anomaly): no val > train + 0.05 (unless whitelisted), no perfect 1.0s, no jumps > 0.3.
- Agent F (static-code): no `X_test` references in runner code.
- Agent G (temporal): no future timestamps in train rows (N/A on synthetic).
- Agent H (seed stability): multi-seed reproduction logged.
- Agent I (refit consistency): |delta| ≤ 0.005.
- Agent J (backbone diversity): ≥ 3 distinct backbones (WARN not FAIL).
- Agent Z (committee verdict): aggregator.

A PASS at 112 / 112 means every task's audit log is green. A WARN does not block PASS; a FAIL on any of A–I blocks PASS.

### 7.2.3 COVERAGE: 148 / 148

`skills/autoresearch-pack/audit/audit_pack.py` parses every H2/H3 across the three source CLAUDE.md files and matches each section to ≥ 1 SKILL.md. The headline is **148 / 148 sections covered (100 %)**.

This is Layer 4 of the audit gate. A new section added to `framework/CLAUDE_template.md` that doesn't have a matching SKILL.md drops the coverage and fails the audit. The CI hook is `audit_pack.py`'s exit code.

### 7.2.4 LESSONS-LEARNED: 26 rows

`framework/CLAUDE_template.md` has an append-only Lessons-Learned table. Rows are added when a correction is codified. The headline is **26 rows** as of commit `1be5130`.

Unlike the previous three numbers, this one is not a target — it's a process indicator. A high row count means the team is learning; a stagnant count means corrections are being lost or no corrections are happening (both bad).

## 7.3 The composite-of-composites

For internal use the project occasionally computes a "BEAT-DSBENCH × FORENSIC-PASS × COVERAGE" triple by row, then takes the count of rows where all three are green. The May 2026 state is **82 / 112** by this strict combined metric (every BEAT has its FORENSIC PASS and every BEAT contributes to COVERAGE). The remaining 30 are FORENSIC PASS + COVERAGE but did not beat DSBench. We do not call those "incomplete"; we call them *bounded* — the protocol ran cleanly, the audit is clean, the baseline was harder than our ceiling. Some of those tasks have a structural ceiling (the qa_excel pure-numeric tasks; see [`analysis/_DIAGNOSIS.md`](../../analysis/_DIAGNOSIS.md)).

## 7.4 The VALIDATOR-OK and AUDIT-PACK metrics

Two more metrics surface in the `_final_audit.py` summary:

### 7.4.1 VALIDATOR-OK: 112 / 112

`framework/validator.py` reads `framework/SECTION_MAPPING.md` and verifies every required section header is present in each per-task `CLAUDE.md`. Also greps `run_autoresearch.py` and `hill_climb.py` per task for `X_test` references and fails on any hit. **Target: 112 / 112.** Currently 112 / 112.

### 7.4.2 AUDIT-PACK: PASS

`skills/autoresearch-pack/audit/audit_pack.py` runs and exits 0. Currently PASS.

These two are Layers 1 and 4 of the four-layer gate. Layer 2 is FORENSIC-PASS. Layer 3 is the per-task 14-section explainability audit — checked by the presence of `audit_report.md` in each submission archive with 14 H2 sections.

## 7.5 What the metrics deliberately do *not* measure

The SWE-book chapter 7 emphasises that what you measure changes what people do. Things we explicitly do not measure:

- **Experiments per hour.** This would reward shallow experiments. Karpathy-style autoresearch is the antithesis of grid search.
- **Lines of code per commit.** This would reward verbose code in `framework/`. We do not measure framework LOC.
- **Time-to-first-experiment for a new task.** This would reward skipping scaffold generation. Scaffold generation is *the contract*; skipping it breaks the validator.
- **Average composite score across tasks.** This would silently weight 74 modeling tasks against 38 analysis tasks. See [Ch. 4](04_engineering_for_equity.md) for the equity argument.

The metric we *would* measure but don't yet: **cohort completion velocity** — number of tasks per day that go from `not_ready` → 4-layer-green. The reason we don't measure it is that the May 2026 cohort was a single-day-equivalent push; the metric makes sense only across multiple cohorts.

## 7.6 The "useful" diagnostic numbers

Not productivity metrics, but useful diagnostics:

- **Median composite gap (train − val):** indicates overfit pressure. Currently ~0.03 across the cohort.
- **Median citation-uniqueness:** number of distinct arXiv IDs cited per task across its 25 base + 200 extended iters. Higher = more genuine literature coverage. Currently ~12 per task.
- **Forensic warning count (Agent J):** tasks with < 3 distinct backbones. Currently 38 (all qa_excel; structurally unavoidable).
- **Per-task experiment count:** distribution mode is 125 (base loop completed); long tail is 325 (base + extended). No task should have < 125 unless it errored.

These live in `framework/_summary.py` for spot-checking.

## 7.7 The "honest about the bounds" metric

A productivity metric should be honest about its bounds. Two ways our metric is bounded and we say so:

1. **The qa_excel structural ceiling.** Three Modeloff challenges (`2012-finals-excel-knowledge-test`, `2017-finals-word-play`, `2017-finals-funding-fun`) have answers that require actual Excel parsing (Excel function names, dict outputs). Our `excel_agent` cannot solve these without a real Excel parser. The structural ceiling is ~17 / 38; we treat tasks above that as bonus.
2. **The DSBench baseline quality.** Some DSBench baselines are conservative (`dsbench_baseline: 0.50` for binary classification on tasks where any half-decent model gets 0.8+). Beating those is meaningful but easy; we report the delta `test - baseline` to make this visible.

The SWE-book chapter 7 calls this the "denominator question": always make the denominator inspectable. Our denominator is `registry/modeling_tasks.json` + `registry/analysis_tasks.json`, both committed and visible.

## 7.8 Related

- [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md): the four-layer audit gate that produces the FORENSIC and VALIDATOR numbers.
- [Ch. 23 — Continuous Integration](../part_4_tools/23_continuous_integration.md): how the metrics get computed on every cohort run.
- [Appendix C — `framework_status.md`](../appendix_c_api_reference/framework_status.md): the API reference for `_status.py`.
- [Appendix C — `framework_final_audit.md`](../appendix_c_api_reference/framework_final_audit.md): the rollup script.
