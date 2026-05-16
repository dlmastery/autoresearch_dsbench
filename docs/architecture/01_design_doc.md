# DSBench AutoResearch — Master Design Document

> Audience: a new engineer or reviewer who needs to understand **what we built and why** in 30 minutes.
> Status: shipped (commit `1be5130`, branch `main`).
> Last reviewed: 2026-05-16.

## 1. Elevator pitch (5 seconds)

We turn the 112 tasks of [DSBench (Jing et al. 2025 ICLR 'DSBench: How Far Are Data Analysis Agents from Becoming Data Analysis Experts' (arXiv:2409.07703))](https://arxiv.org/abs/2409.07703) into 112 self-contained autoresearch repos, then run a Karpathy-style hill-climb on each one, with a 4-layer audit gate that refuses to declare any task "done" until the protocol is provably honoured.

## 2. One-minute glance

| Question | Answer |
|---|---|
| **What** | Autonomous Kaggle-style solver for the 74 modeling + 38 analysis tasks of DSBench. |
| **Why** | DSBench's strongest baseline is GPT-4 + Code-Interpreter at 34.12% data-analysis success / 34.74% Relative Performance Gap. We want a transparent, citable, reproducible alternative that beats those numbers on as many tasks as possible. |
| **How** | A shared `framework/` runs hill-climbing on each task's `train + val` split; `framework/final_report.py` touches `test` exactly once; a 10-agent forensic committee polices every champion. |
| **Where** | `C:/Users/evija/dsbench/` locally; <https://github.com/dlmastery/autoresearch_dsbench> remotely. |
| **Who** | Single-operator project. Claude Code runs the loop; the human commits checkpoints. |
| **When** | First commit 2026-05-15; current run 82/112 BEAT, 112/112 forensic PASS, 156/156 skill-pack coverage. |

## 3. Five-minute overview

DSBench is structured as 112 independent benchmarks. Treating it as one monolithic search would be a mistake — the tasks span tabular binary / multiclass / regression, NLP regression (CommonLit), structured prediction (Conway's Reverse Game of Life), and 38 small-N Modeloff financial QA challenges. We therefore mirror the structure of `dlmastery/autoresearch` (the predecessor FX-research project) **per task**. Every task gets its own:

- `CLAUDE.md` — task-parameterised clone of the master autoresearch protocol (52 sections, validated by `framework/validator.py`).
- `task_config.json` + `seed_reasoning.json` — frozen task identity + first-experiment plan.
- `data/{splits.py, .data_cache/, split_manifest.json}` — frozen 70/15/15 split with hash-pinned `X_train, y_train, X_val, y_val, X_test, y_test` npz cache.
- `autoresearch_results/{experiment_log.jsonl, best_config.json, reasoning_annotations.json, trade_logs/, winners/, dashboard.html, ...}` — append-only experiment ledger.
- `memory/project_autoresearch_checkpoint.md` — crash-recovery checkpoint.
- `run_autoresearch.py`, `hill_climb.py`, `third_party_audit.py` — thin wrappers calling shared framework functions.

The shared framework lives in `C:/Users/evija/dsbench/framework/`. It provides one runner (`runner.py`), one hill-climbing loop (`hill_climb.py` for the 25-iter base + `extended_hill_climb.py` for the 200-iter recovery), one final-report function (`final_report.py`), one validator (`validator.py`), one forensic auditor (`forensic_audit.py`), one submission builder (`build_submission.py`), and a constellation of `_status.py` / `_summary.py` / `_losses.py` rollup scripts.

Pipeline (per task, end-to-end):

1. `generate_scaffolds.py` reads the registry, writes the per-task repo, validates section coverage.
2. `hill_climb.py` runs **25 iters × 5 backbones = 125 experiments** on `train + val` only; each iter has a pre-written 4-field reasoning annotation (`diagnosis / citations / hypothesis / prediction`) and a post-result 2-field one (`verdict / learning`).
3. If the task is still losing to its DSBench baseline, `extended_hill_climb.py` runs **200 additional iters** covering 15 backbone families with arXiv citations.
4. `final_report.py` refits the champion (on `train` for tabular, on `train ∪ val` for `qa_excel`), scores on `test` ONCE, writes `final_report.json`.
5. `forensic_audit.py` runs 10 agents (A–J + Z verdict) per task, writes `forensic_audit.{md,json}`.
6. `build_submission.py` packages every task's bundle to `submissions/dsbench_submission/<kind>/<slug>/` (14 files per task).
7. `_status.py` and `_final_audit.py` aggregate the cross-task scoreboard.

## 4. Thirty-minute deep dive

### 4.1 Why one-repo-per-task

The autoresearch protocol assumes **one** champion lineage. Sharing a single `experiment_log.jsonl` across 112 tasks would conflate signal: a CatBoost depth-10 win on `titanic` says nothing about whether the same recipe wins on `santander-customer-transaction`. The per-task repo also lets reviewers spot-check one task at a time without reproducing the full 112-task state.

### 4.2 The 4-layer audit gate

Every commit that changes experiment state runs all 4 layers (see [`architecture/05_forensic_audit.md`](05_forensic_audit.md) for the agent-by-agent contract):

| Layer | Tool | What it polices |
|---|---|---|
| 1 — Section coverage | `framework/validator.py` | Every per-task `CLAUDE.md` contains the 36+ required sections. Greps for `X_test` / `y_test` in runner code — fail on any reference. |
| 2 — Forensic committee | `framework/forensic_audit.py` | 10 independent agents (A–J) inspect split integrity, leakage, distribution shift, refit consistency, backbone diversity. Agent Z aggregates. |
| 3 — Explainability | `framework/build_submission.py` | 14-section audit report per winner: importance, SHAP, calibration, uncertainty, drift, risk, deployment checklist. |
| 4 — Skill coverage | `skills/autoresearch-pack/audit/audit_pack.py` | Every H2/H3 across all three source CLAUDE.md files maps to ≥ 1 SKILL.md. Target 100%. |

Aggregator: `framework/_final_audit.py` rolls all 4 + the dashboard / md-viewer / Lessons-Learned checks into one report.

### 4.3 Held-back test set as a *first-class invariant*

The single hardest discipline to maintain in 112 parallel hill-climbs is "**test set is OFF-LIMITS until `final_report.py`**." Three mechanisms enforce it:

1. **Codegen invariant.** `framework/generate_scaffolds.py` writes runner wrappers that never reference `X_test` / `y_test`. The validator greps and fails on any deviation.
2. **Runtime invariant.** `framework/runner.py:run_one` predicts on `X_train` and `X_val` only. The composite is `min(val, train) - 0.05 * |val - train|` on tabular tasks (LOO-CV on `train ∪ val` for `qa_excel`).
3. **Forensic invariant.** Agent F (static-code) re-greps after the run; Agent A (split-hash) confirms the test-set hash matches the manifest pre/post run.

See [`adr/0002_train_val_only_for_hill_climb.md`](../adr/0002_train_val_only_for_hill_climb.md).

### 4.4 The composite metric

`composite = min(val_score, train_score) - 0.05 * abs(val_score - train_score)` (Higher is better. RMSE / MAE are negated inside `runner._score` so the formula is metric-agnostic.) The `min` term forces both train AND val to be good; the gap penalty rejects overfit champions. See [`adr/0003_composite_metric_min_min_minus_gap.md`](../adr/0003_composite_metric_min_min_minus_gap.md).

### 4.5 The hill-climb taxonomy

- **Base 25-iter × 5-backbone loop** (`hill_climb.py`): xgboost / lightgbm / catboost / mlp / ft-transformer, with the per-backbone proposals pulled from `framework/sota_catalog.yaml`. Each iter cites its motivating paper.
- **Extended 200-iter loss-only loop** (`extended_hill_climb.py`): probes 15 backbone families on tasks that didn't beat DSBench in the base 125 — dispatching every proposal through the existing runner backbones with the regularisation lever for the targeted family.
- **`qa_excel` 25-iter excel-agent loop**: 25 proposals across class-priors, LogReg, k-NN, Naive Bayes, dummy-majority, prior blending, temperature scaling, per-position prior, prior-ensemble (Wolpert 1992).

### 4.6 Citations

The protocol is rigorous about citations. Every reasoning annotation includes at least one paper with author / year / venue / title / arXiv-ID and a one-sentence relevance note. Examples used across the codebase:

- Chen, Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — anchors the gradient-boosted-tree axis.
- Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' (arXiv:1711.05101) — leaf-wise GOSS sampling.
- Loshchilov, Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW anchor for the MLP / FT-Transformer backbones.
- Bishop 2006 'Pattern Recognition and Machine Learning' PRML §1.3, §5.5.2 — exchangeability + early-stopping discipline.
- Manning, Raghavan, Schütze 2008 'Introduction to Information Retrieval' Ch. 12.2 — Jelinek-Mercer smoothing used in the `qa_excel` Dirichlet composite.
- Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599) — temperature scaling for the excel-agent softmax.
- Wolpert 1992 Neural Networks 'Stacked Generalization' — motivates the `prior_ensemble` backend.

See [`reference/glossary.md`](../reference/glossary.md) for the full citation list.

## 5. Non-goals

- We do **not** parse the underlying Modeloff Excel sheets. Analysis tasks have a documented structural ceiling of ~17/38 (see [`postmortems/0002_excel_agent_synthetic_placeholder.md`](../postmortems/0002_excel_agent_synthetic_placeholder.md)).
- We do **not** maintain a multi-tenant deployment. Single-operator local runs only.
- We do **not** target real-time inference. The hill-climb is offline batch.

## 6. Pointers

- Data model: [`02_data_model.md`](02_data_model.md)
- Runtime: [`03_runtime.md`](03_runtime.md)
- Hill-climb loop: [`04_hill_climb.md`](04_hill_climb.md)
- Forensic audit: [`05_forensic_audit.md`](05_forensic_audit.md)
- 14-section explainability audit: [`06_explainability_audit.md`](06_explainability_audit.md)
- Skill pack: [`07_skill_pack.md`](07_skill_pack.md)
- Dashboards: [`08_dashboards.md`](08_dashboards.md)
- Submission archive: [`09_submission_archive.md`](09_submission_archive.md)
- ADR index: [`../adr/README.md`](../adr/README.md)
- Runbooks: [`../runbooks/README.md`](../runbooks/README.md)
- Postmortems: [`../postmortems/README.md`](../postmortems/README.md)
- SLOs: [`../slos/README.md`](../slos/README.md)
