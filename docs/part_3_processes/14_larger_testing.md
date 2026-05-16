# Chapter 14 — Larger Testing

> *Parallel to:* SWE-book Chapter 14 *"Larger Testing"* (Winters, Manshreck, Wright 2020).

**Thesis.** Larger tests are slow, expensive, and end-to-end. They catch the bugs that unit tests miss because the bugs span multiple components. The DSBench parallel is the **25-iter base hill-climb plus 200-iter extended phase plus per-task `final_report.py`** sequence — the full single-task pipeline, with the most-expensive operation (the test-set refit) running exactly once per task per cohort. This is the largest test the project runs.

## 14.1 What counts as a larger test

The SWE-book chapter 14 says larger tests are end-to-end: they exercise the system as a user would. In our project the "user" is the cohort scoreboard and the "system" is the full pipeline per task. A larger test is one that runs the whole pipeline against real data and produces a verdict the cohort scoreboard reads.

Three layers of larger tests, each with a distinct cost / coverage profile:

| Layer | Test | Per-task duration | What it verifies |
|---|---|---|---|
| **End-to-end hill-climb** | 25 iters × 5 backbones = 125 base experiments | ~3 minutes | The runner, the proposal taxonomy, the citation discipline, the composite metric, the checkpoint, the dashboard. |
| **Extended hill-climb** | Up to 200 additional iters on 15 backbone families | ~20 minutes (on loss tasks only) | The framework's robustness to backbone substitution; the cohort's ceiling. |
| **Final-report refit** | One refit + one test-set score per task | ~5 seconds | The champion's true generalisation; the Test-Set Embargo's exit gate. |

`final_report.py` is the most-expensive single operation per task in the SWE-book sense: it is the only function that touches the test set, and it touches it *once*. Cost ≠ wallclock here; cost = irreversibility. Once the test set has been read, it has been read.

## 14.2 The base 25-iter loop

`framework/hill_climb.py` runs five backbones × 25 iterations = 125 experiments per modeling task. The structure:

```python
for backbone in cfg.backbones:
    for iter_n, proposal in enumerate(_proposals_for(backbone), start=1):
        rec = runner.run_one(repo, backbone, proposal.params, proposal.description, iter_n)
        # rec carries train_score, val_score, composite, elapsed_sec, etc.
        # best_config.json is updated if composite > current.
```

The 125 experiments per task × 74 modeling tasks + 25 × 38 analysis tasks = ~10,200 experiments in the base loop. Wall-clock on the reference hardware: ~6 hours total for the cohort, ~3 minutes per task average.

This is a larger test in the strict SWE-book sense: the full runner, full hill-climb, full annotation, full checkpoint, full dashboard refresh, full forensic audit run sequentially. A failure anywhere in the chain blocks the task's cohort entry. The discipline is rigorous: every experiment writes to disk before the next one starts, so a crash mid-task does not lose more than one experiment.

## 14.3 The 200-iter extended phase

`framework/extended_hill_climb.py` runs up to 200 additional iterations on tasks that finished the base 125 still losing to their DSBench baseline. The extended phase covers 15 backbone families:

- `xgboost-deep` — depth 4–12, lr 0.01–0.03. Chen & Guestrin 2016 KDD *XGBoost* arXiv:1603.02754.
- `lightgbm-goss` — num_leaves 31–255, feature_fraction 0.7–0.9. Ke et al. 2017 NeurIPS *LightGBM* arXiv:1711.05101.
- `catboost-ordered` — ordered boosting. Prokhorenkova et al. 2018 NeurIPS *CatBoost* arXiv:1706.09516.
- `mlp-residual` — residual MLP per Liu et al. 2024 ICLR.
- `ft-transformer-large` — extreme regularisation, Gorishniy et al. 2021 arXiv:2106.11189.
- `hgb`, `extra-trees`, `random-forest`, `elastic-net-stack` — Breiman 2001 *Random Forests*.
- `ngboost-proxy`, `tabnet-proxy`, `tabpfn-proxy` — Duan et al. 2020 ICML *NGBoost*; Arik & Pfister 2021 AAAI *TabNet*; Hollmann et al. 2023 ICLR *TabPFN*.
- `lstm-tabular`, `patch-tsmixer`, `sklearn-stack-ensemble` — sequence-style + stacked dispatchers; Wolpert 1992 *Stacked Generalization*.

Each family's proposals are dispatched through the existing runner backbones with the appropriate regularisation lever; the framework does not require a new backbone implementation per family. This is a deliberate trade — the audit gate cares about behavioural diversity (per Agent J), not implementation diversity.

The extended phase is a larger test because it stresses parts of the framework the base loop doesn't touch:

- The dispatcher's correctness when a proposal targets a backbone the runner doesn't natively implement.
- The proposal queue's idempotence (a restart in the middle of iter 173 must resume at 174, not duplicate).
- The dashboard's "ALL" tab's ability to render 325 experiments per task without timing out.

## 14.4 The final-report refit

`framework/final_report.py:report_repo(repo)` runs once per task at the very end of the cohort. The operation:

1. Load `best_config.json` (the lineage's last champion).
2. Refit the champion's backbone on `train` (tabular) or `train ∪ val` (qa_excel; see [ADR 0009](../appendix_b_adrs/0009_qa_train_plus_val_refit.md)).
3. Predict on `X_test`. Compute the headline metric.
4. Write `final_report.json` with `champion_backbone`, `champion_composite`, `champion_val`, `champion_train`, `test_score`, `test_metrics`, `dsbench_baseline`, `delta_vs_dsbench`, `beats_dsbench`.
5. Append the row to `registry/final_rollup.json`.

This is the only test in the project that legally reads the test set. It is the most-irreversible operation per task. The discipline:

- The function is called by humans (via `framework/_status.py` or the runbook), not by automation. The base hill-climb cannot trigger it.
- Agent I (refit consistency) of the forensic committee re-runs the refit independently and compares against the recorded `test_score`. |delta| > 0.005 fails the audit.
- The `final_report.json` is committed to the repo. The hash of the file ends up in `registry/final_rollup.json`, so any drift is visible in `git diff`.

## 14.5 The cohort scoreboard as the largest test

The final aggregate is `registry/final_rollup.json` plus `registry/forensic_summary.json`. The cohort scoreboard reads both and produces:

- BEAT-DSBENCH: 82 / 112.
- FORENSIC-PASS: 112 / 112.
- COVERAGE: 148 / 148.

This is the project's largest test. It runs in seconds (the data is precomputed) but it depends on every smaller test having passed. A failure at any level — validator → forensic → explainability → skill coverage — invalidates the cohort scoreboard.

The script `framework/_final_audit.py` is the rollup that runs all four layers + the cohort scoreboard in one command.

## 14.6 The hill-climb is *not* a benchmark

A common confusion: people read "25-iter × 5-backbone" and assume the protocol is a benchmark of XGBoost vs LightGBM vs CatBoost on tabular data. It is not. The hill-climb is the *test* of the protocol; the *result* of the test is a champion config + a final_report row.

The benchmark, in the strict SWE-book sense, is the cohort: 112 tasks vs the DSBench paper's published baselines. The hill-climb is the substrate that produces individual benchmark entries.

This is the same distinction the SWE-book draws between "test framework" (the harness) and "tested system" (the code under test). Our harness is `runner.py` + `hill_climb.py` + `final_report.py`; our tested system is the cohort's claim to beat DSBench.

## 14.7 Larger-test reproducibility

A core SWE-book chapter 14 concern: larger tests are flaky if they depend on non-deterministic state. Our reproducibility contract:

| Source of non-determinism | Mitigation |
|---|---|
| Random seeds | All proposals carry an explicit seed (default 42); iters 8 and 9 of every backbone are seed perturbations (`seed ∈ {7, 99}`); a 3-seed median is recorded. |
| Data splits | The 70/15/15 split is deterministic (stride-5 interleaved for qa_excel; deterministic hash-based for tabular). Manifest hashes pin the split. |
| Backbone substitutions | Fallbacks (e.g. `ft_transformer → HistGB`) are logged in the experiment log. |
| Wall-clock timestamps | Recorded but not load-bearing. The hash of the log entry covers content, not timestamps. |
| Thread / parallelism non-determinism | Pinned to 4 P-cores with `_pin_to_safe_cores`; OMP / MKL / OpenBLAS thread count fixed to 4. |

After all five mitigations, a re-run of the cohort produces `final_rollup.json` rows that differ from the original by less than ±0.005 on the test score (the Agent I threshold). The forensic committee tests for this independently.

## 14.8 The "hermetic" larger test

The SWE-book chapter 14 introduces *hermetic* tests: tests that bring their own environment, do not depend on shared infrastructure, can run anywhere. Our larger tests are hermetic in the following sense:

- The cohort runs entirely on the local machine. No network calls after the initial Kaggle / Modeloff data load.
- The data is cached in `.data_cache/splits.npz` per task; subsequent runs read the cache.
- The Python environment is a local Anaconda install at `C:/Users/evija/anaconda3/python.exe`; no virtualenv juggling.
- The audit gate produces all its outputs as files in the repo; no external state.

The only non-hermetic element: the GitHub push, which requires network and credentials. That step lives in [Ch. 24](../part_4_tools/24_continuous_delivery.md), outside the test contract.

## 14.9 The 14,000-experiment ledger as test artefact

The aggregate output of all the larger tests is the **~14,000 entries across `experiment_log.jsonl` files**. This ledger is:

- The unit of truth for what happened.
- Append-only by construction.
- Cited by every six-field annotation (the annotation references the experiment by number, and the log entry carries the metric, params, and timestamp).
- Audited by Agent E (anomaly) and Agent J (diversity).

In SWE-book terms, the ledger is the test-result database. Most projects aggregate test results into a dashboard and discard the per-test detail; we keep every single per-experiment row forever.

## 14.10 What we deliberately do not test at this layer

A few things we could test but don't:

- **Cross-cohort regression.** We do not run "did the May 2026 cohort beat the May 2025 cohort". The cohort scoreboard is a snapshot; cohort-over-cohort comparisons are journalism, not testing.
- **Benchmark fairness vs alternative agents.** We claim 82/112 BEAT but do not run alternative agents (GPT-4, Claude-3.5, others) head-to-head on the same protocol. The DSBench paper does that work; we cite their numbers.
- **Performance regression.** We do not measure that the hill-climb takes ~6 hours and fail the audit if it takes 8. The runner is fast enough; further optimisation is not a goal.

These omissions are deliberate. The project's testing surface is large enough already; expanding it would dilute the focus.

## 14.11 Related

- [Ch. 11 — Testing Overview](11_testing_overview.md): the four-layer pyramid.
- [Ch. 12 — Unit Testing](12_unit_testing.md): the validator as the unit-test layer.
- [Ch. 13 — Test Doubles](13_test_doubles.md): the synthetic-Gaussian fallback.
- [`framework/hill_climb.py`](../../framework/hill_climb.py): the base loop.
- [`framework/extended_hill_climb.py`](../../framework/extended_hill_climb.py): the extended phase.
- [`framework/final_report.py`](../../framework/final_report.py): the test-set refit.
