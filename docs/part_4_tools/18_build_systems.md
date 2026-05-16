# Chapter 18 — Build Systems and Build Philosophy

> *Parallel to:* SWE-book Chapter 18 *"Build Systems and Build Philosophy"* (Winters, Manshreck, Wright 2020).

**Thesis.** The SWE-book chapter 18 argues a build system is "the right tool to convert source into running software, reliably and reproducibly". The DSBench project has no Bazel or Make. The build system is a small set of Python entry-point scripts (`framework/run_all.py`, `framework/build_submission.py`, `framework/_refresh_dashboards.py`) plus the audit-gate aggregator (`framework/_final_audit.py`). The combination produces every artefact the cohort scoreboard reads, and is the project's idempotent build.

## 18.1 The build target

What does "the build" produce? Five categories of artefact:

| Build target | Producer | Inputs | Outputs |
|---|---|---|---|
| **Per-task scaffold** | `framework/generate_scaffolds.py` | `registry/modeling_tasks.json`, `registry/analysis_tasks.json`, `framework/CLAUDE_template.md`, `framework/sota_catalog.yaml` | 112 task directories with their `CLAUDE.md`, `task_config.json`, `data/splits.py`, `run_autoresearch.py`, etc. |
| **Per-task cohort experiments** | `framework/run_all.py` | scaffolds + cached data | 112 `experiment_log.jsonl`, 112 `best_config.json`, 112 `reasoning_annotations.json`, ~14,000 experiment rows |
| **Per-task final report** | `framework/final_report.py` | `best_config.json` + test set (read once) | 112 `final_report.json` |
| **Per-task forensic audit** | `framework/forensic_audit.py` | full task state | 112 `forensic_audit.{md,json}` + `registry/forensic_summary.json` |
| **Per-task submission archive** | `framework/build_submission.py` | full task state | `submissions/dsbench_submission/<kind>/<slug>/` × 112 (14 files per task) |
| **Cross-task rollup + dashboards** | `framework/_refresh_dashboards.py` + `framework/_status.py` | rollup files | `registry/final_rollup.json`, `registry/forensic_summary.json`, `dashboard/index.html`, per-task `dashboard.html` |

The build is idempotent: running it twice produces the same outputs (modulo timestamps). Re-running on a partial cohort resumes; re-running on a complete cohort is a no-op for most steps.

## 18.2 The entry-point scripts

`framework/run_all.py` is the cohort entry point. Invocation:

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/run_all.py [--kind modeling|analysis] [--all] [--limit N]
```

What it does:

1. Reads the registry to determine the task list.
2. For each task, invokes `framework/hill_climb.py --repo <task>` for the base 125 experiments.
3. After the base loop, invokes `framework/extended_hill_climb.py --repo <task>` if the task hasn't beaten its baseline.
4. After the hill-climb, invokes `framework/final_report.py --repo <task>` (test-set refit, once).
5. Background stdout goes to `registry/run_all_stdout.log` and `registry/run_all_analysis_stdout.log` so `framework/_status.py` can give a live snapshot.

The script is *resumable*. If interrupted, re-running picks up at the next task (because each task's `final_report.json` either exists or doesn't, and the script checks). No locking required because each task writes to its own directory.

## 18.3 The build graph

The dependency graph between artefacts:

```
registry/modeling_tasks.json ──┐
registry/analysis_tasks.json ──┤
framework/CLAUDE_template.md ──┼──► framework/generate_scaffolds.py ──► modeling/<slug>/ scaffolds
framework/sota_catalog.yaml ───┘                                       analysis/<slug>/ scaffolds
                                                                              │
                                                                              ▼
                                                                  framework/run_all.py
                                                                              │
                                                                  hill_climb.py per task
                                                                              │
                                                                  experiment_log.jsonl
                                                                  best_config.json
                                                                  reasoning_annotations.json
                                                                              │
                                                                              ▼
                                                                  framework/final_report.py
                                                                              │
                                                                  final_report.json
                                                                              │
                                                                              ▼
                                                                  framework/forensic_audit.py
                                                                              │
                                                                  forensic_audit.{md,json}
                                                                              │
                                                                              ▼
                                                                  framework/build_submission.py
                                                                              │
                                                                  submissions/.../*.* × 14
                                                                              │
                                                                              ▼
                                                                  framework/_refresh_dashboards.py
                                                                              │
                                                                  dashboard/index.html
                                                                  per-task dashboard.html
                                                                  registry/final_rollup.json
                                                                  registry/forensic_summary.json
```

The graph is hand-maintained; there is no `make` or `ninja` that knows the graph. The discipline is: each script reads its inputs from known paths and writes its outputs to known paths. A script that bypasses the known paths is a smell.

## 18.4 Reproducibility

The SWE-book chapter 18 argues "the build system must be reproducible". Three sources of irreproducibility we mitigate:

1. **Wall-clock timestamps.** Recorded in every artefact (experiment log row, audit report) but not load-bearing — the content's hash is independent of the timestamp.
2. **Random seeds.** Every experiment carries `seed: 42` (or 7, or 99 for the seed-variance check). The numpy / sklearn / torch backends use these seeds. The synthetic-Gaussian fallback also seeds from `cfg.slug`.
3. **Thread non-determinism.** `_pin_to_safe_cores` fixes the thread count to 4. OMP / MKL / OpenBLAS environment variables fixed at 4.

After these three mitigations, a cohort re-run on the same machine produces `final_rollup.json` rows whose test scores differ from the original by < ±0.005 (within Agent I's threshold). The forensic committee verifies this.

The remaining non-determinism is hardware-dependent (different CPU SIMD instructions across machines may give slightly different floating-point results). We do not promise cross-machine bit-identical reproducibility; we promise cross-machine within-threshold reproducibility.

## 18.5 The `_refresh_dashboards.py` script

`framework/_refresh_dashboards.py` is the build target for the presentation layer:

1. Walk every task; load its `final_report.json`, `experiment_log.jsonl`, `reasoning_annotations.json`, `forensic_audit.json`.
2. Re-render the per-task `autoresearch_results/dashboard.html` from the dashboard template.
3. Aggregate the per-task results into `registry/final_rollup.json` and `registry/forensic_summary.json`.
4. Re-render `dashboard/index.html` (the cross-task scoreboard).
5. Verify every internal link in the dashboards resolves.

The script is the canonical "single-command end-to-end refresh" — Lessons-Learned row 21. After any change to per-task state, running this script brings every dashboard up to date in one operation. No partial refresh is allowed; the dashboards either reflect the current state or they don't.

## 18.6 The `_final_audit.py` aggregator

`framework/_final_audit.py` is the build target for the audit-gate state:

1. Run Layer 1 (validator) on all 112 tasks.
2. Run Layer 2 (forensic) on all 112 tasks.
3. Run Layer 3 (explainability) on every task with a recent champion change.
4. Run Layer 4 (skill-pack coverage).
5. Check that every dashboard has an "About this task" disclosure (Lessons-Learned row 23).
6. Check that the MD viewer renders inline (Lessons-Learned row 24).
7. Check Lessons-Learned section presence in every per-task `CLAUDE.md`.

Output: a four-line summary of the gate state plus a list of any forbidden paths. Exit code 0 iff the gate is fully green.

This is the project's single CI command. [Ch. 23](23_continuous_integration.md) describes how it gets invoked.

## 18.7 Anti-patterns we avoid

The SWE-book chapter 18 lists build-system anti-patterns. Our equivalents:

| Anti-pattern | What we do |
|---|---|
| Implicit dependencies | Every script names its inputs explicitly via path; no global state. |
| Slow rebuilds | The hill-climb takes hours but is structurally unavoidable; `_refresh_dashboards.py` is < 30 sec; `_final_audit.py` is < 5 min. |
| Cached but stale outputs | Each script either reads fresh from disk or honours the cache contract (`.data_cache/splits.npz` is content-hashed in the manifest). |
| Side effects in build steps | The framework scripts write files; they do not modify any shared registry except via the documented files. |
| Mixed source and generated artefacts | Per-task `CLAUDE.md` is generated; `framework/CLAUDE_template.md` is source. The two are not mixed in the same directory. |

## 18.8 What we cannot build incrementally

A few things require full rebuilds:

- **The cross-task `final_rollup.json`** depends on every task's `final_report.json`. If one task's report is stale, the rollup is stale. The mitigation: `_refresh_dashboards.py` always reads all 112 fresh.
- **The `forensic_summary.json`** depends on every task's `forensic_audit.json`. Same pattern.
- **The skill-pack coverage** depends on every source CLAUDE.md and every SKILL.md. `audit_pack.py` always re-reads.

None of these is slow enough to need incremental builds. The full rebuild fits in 30 seconds.

## 18.9 The "single command" cohort refresh

The end-to-end cohort refresh:

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/run_all.py --all
& "C:/Users/evija/anaconda3/python.exe" framework/forensic_audit.py
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py
& "C:/Users/evija/anaconda3/python.exe" framework/_refresh_dashboards.py
& "C:/Users/evija/anaconda3/python.exe" framework/_final_audit.py
```

Five commands, ~6 hours of wall-clock for the hill-climb plus ~30 minutes for the audits and refresh. The cohort scoreboard at the end is `82 / 112 BEAT, 112 / 112 PASS, 148 / 148 COVERAGE`.

There is a wrapper that runs all five sequentially (`framework/run_all.py --all --then-audit --then-submit --then-dashboards --then-final`). The wrapper is preferred for clean cohort runs; the individual commands are preferred for debugging.

## 18.10 Related

- [Ch. 22 — Large-Scale Changes](22_large_scale_changes.md): the cookbook for cohort-level changes.
- [Ch. 23 — Continuous Integration](23_continuous_integration.md): the audit gate as CI.
- [Ch. 24 — Continuous Delivery](24_continuous_delivery.md): the submission archive + GitHub push.
- [`framework/run_all.py`](../../framework/run_all.py): the cohort entry point.
- [`framework/_final_audit.py`](../../framework/_final_audit.py): the audit-gate aggregator.
