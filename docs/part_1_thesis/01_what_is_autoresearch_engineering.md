# Chapter 1 — What Is AutoResearch Engineering?

> *Parallel to:* SWE-book Chapter 1 *"What Is Software Engineering?"* (Winters, Manshreck, Wright 2020).

**Thesis.** AutoResearch is software engineering for ML experiment loops integrated over collaborator turns. Software engineering is programming integrated over time and people; autoresearch engineering is programming integrated over time, people, and a non-deterministic LLM collaborator that drives the experiment loop. The collaborator's working memory dies between sessions, so every artefact must survive without it.

## 1.1 The three dimensions

The SWE-book draws a clean distinction between *programming* (writing code that works today), *software engineering* (writing code that keeps working across time and engineers and dependency churn), and *computer science* (the underlying theory). It then argues that scale changes everything: as a project moves along the time, people, and dependency axes, the practices that work at small scale fail.

AutoResearch projects sit on a fourth axis that the SWE-book doesn't address directly: **collaborator turns**. The LLM collaborator (Claude Code in our case) has no persistent memory; every session starts cold. The repository *is* the memory. This implies:

| Axis | SWE-book treatment | DSBench autoresearch implication |
|---|---|---|
| Time | "Programming integrated over time." Practices must survive code drift, dependency churn, and Hyrum's Law. | The experiment ledger must be append-only. `experiment_log.jsonl` never rewrites; champions ratchet monotonically. |
| People | "Code is read more often than written." Code review, style guides, documentation. | The collaborator reads the repository every session. The repo is a person-equivalent. CLAUDE.md is the project style guide. |
| Dependencies | Dependency drift is the silent killer. | `framework/sota_catalog.yaml` pins per-backbone proposals to specific arXiv papers; library substitutions are recorded in the log. |
| Collaborator turns | (not in SWE-book) | Crash-recovery checkpoint is mandatory after every experiment, every 5 min of reasoning, before / after every code change. |

The collaborator-turns axis is what makes autoresearch a different discipline. A traditional ML project has a human researcher whose memory persists between sessions; if a tuning knob feels exhausted, the human remembers and doesn't re-try it. Our collaborator forgets. The Per-Backbone 25-Experiment Mandate ([Ch. 8](../part_3_processes/08_style_guides_and_rules.md)) is the rule that converts "the human remembers" into "the log remembers and the next session reads the log".

## 1.2 What we build

DSBench (Jing et al. 2025 ICLR *DSBench: How Far Are Data Analysis Agents from Becoming Data Analysis Experts* arXiv:2409.07703) packages 74 Kaggle modeling tasks and 38 Modeloff data-analysis challenges into a 112-task benchmark. The reference numbers in the paper:

- Best agent on data-analysis: **34.12 %** success.
- Best agent on data-modeling: **34.74 %** Relative Performance Gap.

We treat the benchmark as 112 independent autoresearch problems. Every task gets its own `CLAUDE.md`, its own `task_config.json`, its own 70/15/15 split with a hash-pinned manifest, its own append-only ledger, its own dashboard, and its own forensic-audit report. A shared `framework/` library provides the runner, the hill-climb loop, the validator, the forensic auditor, the final-report (test-set) function, the submission builder, and a constellation of rollup scripts. Per-task code is a thin wrapper around the framework.

At the end of a run we have, per task, a fourteen-file submission archive ([Ch. 24](../part_4_tools/24_continuous_delivery.md)) that lets a reviewer spot-check one task without reproducing the full 112-task state. The aggregate state lives in `registry/final_rollup.json` (one row per task) and `registry/forensic_summary.json` (one row per task). Two rollups, one Definition of Done.

Current state (commit `1be5130` on `main`):

- **82 / 112 BEAT** the DSBench baseline.
- **112 / 112 FORENSIC PASS** by the 10-agent committee.
- **148 / 148 SKILL COVERAGE** by the audit script.
- **26 Lessons-Learned rows** appended across the 112 per-task `CLAUDE.md` files.
- **~14,000 experiments** logged across the base 25-iter loop + the 200-iter extended phase.

## 1.3 The four discipline pillars

Treat the project as four discipline pillars stacked vertically. Lower pillars carry higher pillars; if the foundation cracks, everything above collapses.

```
                  4. Continuous Delivery (submission archive, GitHub push)
                  3. Continuous Integration (4-layer audit gate)
                  2. Process (style guide, code review, testing pyramid)
                  1. Substrate (hardware contract, splits, citations)
```

1. **Substrate.** P-core pinning, the 70/15/15 split with hash manifest, the citation format, the six-field reasoning annotation. Everything else assumes this layer is correct. [Ch. 25](../part_4_tools/25_compute_as_a_service.md), [Ch. 12](../part_3_processes/12_unit_testing.md).
2. **Process.** The style guide (CLAUDE.md), code review (10-agent forensic committee), documentation (six-field annotation + research journal), testing (validator + forensic + 14-section + skill-pack). [Ch. 8](../part_3_processes/08_style_guides_and_rules.md) — [Ch. 14](../part_3_processes/14_larger_testing.md).
3. **Continuous integration.** The four-layer audit gate that no commit changing experiment state may skip. [Ch. 23](../part_4_tools/23_continuous_integration.md).
4. **Continuous delivery.** The per-task submission archive plus the cross-task `dashboard/index.html` plus the GitHub push pipeline. [Ch. 24](../part_4_tools/24_continuous_delivery.md).

Each pillar's chapter explains both *what* the rule is and *why* it survives time, people, dependencies, and collaborator turns. SWE-book voice: lead with the thesis, formalise the principle, then mine the postmortem to show what happens when the principle is missing.

## 1.4 Named principles introduced in this docs/

The SWE-book formalises Hyrum's Law ("with a sufficient number of users of an API, it does not matter what you promise in the contract — all observable behaviours of your system will be depended on by somebody"), the Beyoncé Rule ("if you liked it, you should have put a CI test on it"), and the Three Laws of Optimization. We canonise eight principles in this documentation, all listed in the [main README](../README.md). The two that carry the most weight in everyday work are:

- **The Test-Set Embargo Rule** ([Ch. 11](../part_3_processes/11_testing_overview.md)): *if the test set is read once, it leaks once*. There is no "just a peek" allowance. The only legal reader is `framework/final_report.py`, exactly once per task. Mechanisms (Codegen: the scaffold generator never references `X_test`; runtime: the runner predicts on `X_train` and `X_val` only; forensic: Agent F greps and Agent A checks the hash) implement the rule three ways so a single mechanism failure does not blow the embargo.
- **The Four-Layer Gate Rule** ([Ch. 11](../part_3_processes/11_testing_overview.md)): *no commit that changes experiment state lands until all four audit layers are green*. The layers are the validator (cheap section grep), the forensic committee (medium-cost 10-agent committee), the 14-section explainability report (per-task winner audit), and the skill-pack coverage script (every H2/H3 across all source CLAUDE.md files maps to ≥ 1 SKILL.md). [Ch. 23](../part_4_tools/23_continuous_integration.md) covers how the gate runs in practice.

## 1.5 Why one repo per task

A common reflex in benchmark engineering is to fan out across a shared logging substrate: one big `experiments.csv`, one big `wandb` project, one big `mlruns/` tree. We do not. Every task gets its own repository inside `modeling/<slug>/` or `analysis/<slug>/` with its own `CLAUDE.md`, its own `autoresearch_results/`, its own `data/.data_cache/splits.npz`. Three reasons:

1. **No cross-task signal contamination.** A CatBoost depth-10 win on `titanic` says nothing about whether the same recipe wins on `santander-customer-transaction`. Sharing the log conflates signal and tempts the collaborator to copy a hyperparameter that doesn't generalise.
2. **Spot-check-able for reviewers.** A reviewer who wants to audit one task does not have to reproduce the full 112-task state. The per-task repo + its submission archive is self-contained.
3. **The collaborator's working set fits in context.** Loading `CLAUDE.md` + `memory/project_autoresearch_checkpoint.md` + the last three rows of `experiment_log.jsonl` is ~6 K tokens; loading the global state would be ~600 K and unworkable.

The shared framework lives at `C:/Users/evija/dsbench/framework/`. Per-task code is a thin wrapper. The contract between the two is `task_config.json` (frozen at scaffold generation) plus the validator's section-mapping check.

## 1.6 Scale considerations

The SWE-book repeats throughout that practices change with scale. Our scale axis is *task count*:

| Scale | What stays the same | What has to change |
|---|---|---|
| 1 task | Hill-climb loop, citation discipline, six-field annotation, four-layer gate. | Nothing — this is the baseline. |
| 10 tasks | All of the above. | Rollup script becomes necessary (`framework/_status.py`). Cross-task dashboard helpful. |
| 112 tasks (current) | All of the above. | Submission archive becomes necessary. Validator must be parallel-safe. Forensic-audit script must run idempotently per-task so one task's failure doesn't block the cohort. |
| 540 tasks (hypothetical 5× expansion) | All of the above. | Per-task `CLAUDE.md` generation has to be templated (already is). Forensic audit needs sharding. Dashboard pagination required. |
| Arbitrary benchmark | All of the above. | The registry (`registry/modeling_tasks.json`, `registry/analysis_tasks.json`) becomes the dependency-graph root. Build system needs to detect which tasks were affected by a framework change. |

The Per-Backbone 25-Experiment Mandate is invariant across all scales. The Test-Set Embargo Rule is invariant across all scales. These are the "rules" in the style-guide sense — they do not bend.

## 1.7 What this chapter does not promise

This chapter is the project's elevator pitch. It does not:

- Explain how to run an experiment — see [Ch. 18](../part_4_tools/18_build_systems.md) and [Appendix C](../appendix_c_api_reference/cli_reference.md).
- Explain a specific bug or its postmortem — see [Appendix A](../appendix_a_postmortems/).
- Justify any specific architectural choice — see [Appendix B](../appendix_b_adrs/).
- Explain the deep-learning theory — see [`appendix_c_api_reference/glossary.md`](../appendix_c_api_reference/glossary.md) for the citation list (Bishop 2006 *Pattern Recognition and Machine Learning*; Goodfellow, Bengio, Courville 2016 *Deep Learning*; Hastie, Tibshirani, Friedman 2009 *Elements of Statistical Learning*; Chen & Guestrin 2016 KDD *XGBoost* arXiv:1603.02754; Loshchilov & Hutter 2019 ICLR *Decoupled Weight Decay Regularization* arXiv:1711.05101; Wolpert 1992 *Stacked Generalization*; Friedman 2001 *Stochastic Gradient Boosting*; Kohavi 1995 IJCAI *A Study of Cross-Validation and Bootstrap*).

It does promise the reader that, by the end of [Part III](../part_3_processes/), they will be able to write or review any commit to this repository, and by the end of [Part IV](../part_4_tools/), they will be able to add a new task, a new backbone, or a new audit layer without breaking the contract.

## 1.8 Companion pointers

- The current project state: [`STATUS.md`](../../STATUS.md) at the repo root.
- The protocol's source: [`framework/CLAUDE_template.md`](../../framework/CLAUDE_template.md).
- The section-mapping audit contract: [`framework/SECTION_MAPPING.md`](../../framework/SECTION_MAPPING.md).
- The skill pack: [`skills/autoresearch-pack/README.md`](../../skills/autoresearch-pack/README.md).
- The diagnosis that justified the May 2026 excel-agent rewrite: [`analysis/_DIAGNOSIS.md`](../../analysis/_DIAGNOSIS.md).
