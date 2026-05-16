# Chapter 11 — Testing Overview

> *Parallel to:* SWE-book Chapter 11 *"Testing Overview"* (Winters, Manshreck, Wright 2020).

**Thesis.** The SWE-book describes a testing pyramid: many small unit tests, fewer medium integration tests, very few large end-to-end tests. The DSBench parallel is the **four-layer audit gate**: many cheap section-coverage checks, a medium-cost 10-agent forensic committee per task, an expensive 14-section per-champion explainability audit, and a project-wide skill-pack coverage script. The pyramid is the right metaphor; the layers are the implementation.

## 11.1 The testing pyramid, mapped

The SWE-book chapter 11 draws the pyramid and warns against the inverted-pyramid anti-pattern. We claim our four-layer audit gate sits on the correct side of the pyramid:

```
                    Layer 4 (project-wide)        — skill-pack coverage script   ~5 sec
                  Layer 3 (per-champion, expensive) — 14-section explainability  ~30 sec
                Layer 2 (per-task, medium)          — 10-agent forensic audit    ~3 sec
              Layer 1 (per-task, cheap, fast, many) — section validator + grep    ~50 ms
```

Each layer's *cost* and *coverage* are calibrated so the cheap layer catches the common cases (missing section header, `X_test` reference) and the expensive layers catch the rare ones (refit-consistency violation, missing audit subsection).

| Layer | Tool | Per-task or cohort | Latency | What it polices |
|---|---|---|---|---|
| **1** | `framework/validator.py` | Per-task | ~50 ms | 36 section headers present; no `X_test` grep hits; required files exist. |
| **2** | `framework/forensic_audit.py` | Per-task | ~3 s | Split integrity, leakage, distribution shift, refit, backbone diversity. |
| **3** | `framework/build_submission.py` | Per-champion | ~30 s | 14 audit-report sections (importance, SHAP, calibration, uncertainty, drift, risk, deployment). |
| **4** | `skills/autoresearch-pack/audit/audit_pack.py` | Project-wide | ~5 s | Every H2/H3 in source CLAUDE.md maps to ≥ 1 SKILL.md. |

`framework/_final_audit.py` is the rollup that runs all four and reports the cohort state in one command.

## 11.2 The Test-Set Embargo Rule

This chapter is the home of the project's most important named principle.

> **The Test-Set Embargo Rule.** If the test set is read once, it leaks once. The only legal reader of `splits['X_test']` / `splits['y_test']` is `framework/final_report.py`, exactly once per task at the very end of the cohort run.

The rule has three independent enforcement mechanisms — *defence in depth*. Any one mechanism failing should not blow the embargo:

### 11.2.1 Codegen invariant

`framework/generate_scaffolds.py` writes per-task runner wrappers (`run_autoresearch.py`, `hill_climb.py`, `third_party_audit.py`). These wrappers never reference `X_test` or `y_test`. The generator's own code does not produce a token that touches the test set.

### 11.2.2 Runtime invariant

`framework/runner.py:run_one` calls `_fit_predict` and `_score` on `X_train` and `X_val` only. The composite is `min(val, train) - 0.05 * |val - train|` (or LOO-CV on train ∪ val for qa_excel). The runner is the *only* path through which experiments reach data, and the runner is structurally incapable of reading `X_test`.

### 11.2.3 Forensic invariant

Agent F (static-code) of the forensic committee greps every file under the task's repo for `X_test` / `y_test` / `splits['test']` references. Any hit fails the audit. Agent A (split-hash) confirms the test-set hash matches the manifest pre-run and post-run. Agent I (refit-consistency) refits the champion from `best_config.json`, scores on test inside `final_report.py`, and compares against the recorded `test_score` — within ±0.005 is the threshold.

Three mechanisms, three independent failure modes. The rule has not been violated since the initial commit. The May 2026 work added Agent I (refit) and the static-code grep (Agent F) to harden the rule; both were paid for by drafts of postmortem 0001 that ran on slightly-different versions of `final_report.py` and would have shifted by 0.04 in the score had the refit check not caught it.

## 11.3 The Four-Layer Gate Rule

> **The Four-Layer Gate Rule.** No commit that changes experiment state lands until all four audit layers are green. Validator + forensic committee + 14-section explainability (for new champions) + skill-pack coverage.

"Changes experiment state" means: writes to `experiment_log.jsonl`, `best_config.json`, `reasoning_annotations.json`, `final_report.json`, or `forensic_audit.{md,json}` in any task's `autoresearch_results/`. Commits that only touch this docs/ or `framework/` source code without rerunning experiments do not require the gate.

The gate is enforced informally (single operator). The mechanism is the `_final_audit.py` rollup, which exits non-zero if any layer is red. The convention is: run `_final_audit.py`, commit only if green, push.

## 11.4 The cost / coverage trade-off

The SWE-book chapter 11 warns: too many expensive tests slow the development loop; too few cheap tests miss bugs. Our calibration:

- **Layer 1 (validator) runs on every cohort change**, takes 50 ms × 112 = ~6 seconds total. Cost is negligible. Catches the most common bugs (missing section, `X_test` reference). This is the unit test layer.
- **Layer 2 (forensic) runs after every cohort batch**, takes ~3 sec × 112 = ~5 minutes. Cost is meaningful but tolerable. Catches subtle leakage, anomalies, refit inconsistencies. This is the integration test layer.
- **Layer 3 (explainability) runs only when a champion changes**, takes ~30 sec per champion × ~30 champion-changes per cohort = ~15 minutes. Cost is heavy but rare. Catches missing audit subsections. This is the per-feature integration test layer.
- **Layer 4 (skill coverage) runs on every CLAUDE.md change**, takes ~5 sec project-wide. Cost is negligible. Catches drift in the protocol contract. This is the project-wide architectural test layer.

Total cost for a clean cohort run: ~25 minutes for all four layers. The hill-climb itself takes ~6 hours for 14,000 experiments. The audit gate is < 10 % of the cohort's wall-clock budget — within the SWE-book's recommended budget for test infrastructure.

## 11.5 What each layer does *not* catch

Each layer has a deliberate gap that the next layer covers:

- **Layer 1 (validator)** does not check content semantics. A section header that exists with empty content passes.
- **Layer 2 (forensic)** does not check style or documentation. An audit-pass with an empty annotation file passes the forensic committee but would fail Layer 3.
- **Layer 3 (explainability)** does not check cross-task consistency. A champion's audit report can be locally green while the cohort scoreboard is mis-counting.
- **Layer 4 (skill coverage)** does not check whether the SKILL.md content is accurate — only that there is *a* SKILL.md per H2/H3.

The four-layer composition catches the union of failure modes. The gaps are intentional; closing all gaps in one layer would make that layer untestable.

## 11.6 The "test-set as a first-class invariant" pattern

A specific pattern worth naming: the test set is treated as *data* with an *invariant*, not as a function call. The invariant is encoded in `data/split_manifest.json` (the hash of the test set is committed to the repo). Any time the audit runs, it can re-hash the on-disk test set and compare; if the hash drifts, the test set has been touched by something it shouldn't have been.

The pattern works because:

1. The hash is small (16 hex chars) and easy to compare.
2. The hash is committed to the repo, so a `git diff` on `data/split_manifest.json` instantly shows test-set drift.
3. The hash is checked by Agent A on every cohort audit.

The contrast: a code-level invariant ("don't call `X_test`") is harder to audit because the LLM collaborator might write a new code path that references `X_test` legitimately for an unrelated reason. A *data-level* invariant ("the test set's bytes have not changed") is unambiguous.

## 11.7 The pyramid in numbers

| Layer | Tests | Failures observed in May 2026 cohort | Failure rate |
|---|---|---|---|
| 1 — validator | 112 (one per task) × 36 sections × ~5 grep patterns ≈ 22,400 checks | 0 (after final pre-commit gate) | 0.000 % |
| 2 — forensic | 112 × 10 agents = 1,120 agent verdicts | 0 (after problem-type-aware calibration) | 0.000 % |
| 3 — explainability | 112 × 14 sections = 1,568 section checks | 0 | 0.000 % |
| 4 — skill coverage | 148 source sections × 44 skills = 6,512 match cells (sparse) | 0 (148 / 148 covered) | 0.000 % |

The May 2026 numbers say zero failures. The *path* to zero, however, is paved with the five postmortems in [Appendix A](../appendix_a_postmortems/) — each one names a class of failure that the audit gate now catches because of a specific bug it didn't catch the first time.

## 11.8 The pyramid is not a hierarchy

A subtle point the SWE-book chapter 11 makes: the pyramid is about *cost*, not about *importance*. Layer 1 is the most numerous tests, but Layer 2 catches the bugs that would have caused the most damage. Layer 4 runs least frequently but catches the bugs that would have eroded the project's integrity over time.

In particular: Layer 1 cannot detect that the test set was leaked through an unusual code path; Layer 2's Agent F catches it. Layer 2 cannot detect that the audit-report has missing sections; Layer 3 catches it. Layer 3 cannot detect that the protocol has drifted; Layer 4 catches it. The layers are *complementary*, not hierarchical.

## 11.9 The `_final_audit.py` rollup

The single command that runs all four layers + the dashboard / md-viewer / Lessons-Learned checks:

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_final_audit.py
```

Output: a summary line per layer plus an aggregate verdict. The script exits 0 only if all layers are green. The convention is: run this before any commit that touches experiment state; do not push if it's red.

The rollup is the closest thing the project has to a single CI command. [Ch. 23](../part_4_tools/23_continuous_integration.md) describes how the same command runs in batch mode after every cohort refresh.

## 11.10 Related

- [Ch. 12 — Unit Testing](12_unit_testing.md): Layer 1 (the validator) in depth.
- [Ch. 13 — Test Doubles](13_test_doubles.md): the synthetic-data fallback as a test double.
- [Ch. 14 — Larger Testing](14_larger_testing.md): Layers 2–4 in depth.
- [Ch. 23 — Continuous Integration](../part_4_tools/23_continuous_integration.md): the gate as CI.
- [Appendix A](../appendix_a_postmortems/): the five postmortems that each paid for a layer or a calibration.
