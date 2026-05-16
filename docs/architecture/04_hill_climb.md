# Hill-Climb — 25-Iter Base + 200-Iter Extension + Citation Discipline

> Audience: an engineer extending the proposal taxonomy or debugging a stuck task.

## 1. Philosophy

The hill-climb is a **diagnose → cite → hypothesise → predict → run ONE experiment → analyse → document** loop. It is the antithesis of grid search. Every experiment changes ONE config parameter, cites at least one arXiv-grade paper, and predicts the expected composite delta. The goal is **monotonic** improvement: once a metric improves, the new level is the floor. See [`../adr/0005_25_iters_per_backbone.md`](../adr/0005_25_iters_per_backbone.md) and `framework/CLAUDE_template.md` § "Research-Driven Experiment Selection".

The protocol is Karpathy-adapted: every experiment starts from the **current best** config and modifies exactly one knob. If it improves, it's the new best. If not, revert.

## 2. The base 25-iter loop (`framework/hill_climb.py`)

Five backbones × 25 iters = **125 experiments per task** for modeling tasks (`xgboost`, `lightgbm`, `catboost`, `mlp`, `ft_transformer`). Each iter is a tuple `(params, diagnosis, citation, hypothesis, prediction)`. The proposals live in `_xgb_proposals()`, `_lgbm_proposals()`, `_catboost_proposals()`, `_mlp_proposals()`, `_ft_proposals()` and similar helpers.

Iter 1 for every backbone is the **published-paper default** (Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) for XGBoost; Ke et al. 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' (arXiv:1711.05101) for LightGBM; etc.). Iters 2-10 are documented perturbations along one axis. Iters 11-25 are generated programmatically from a library of cited perturbations (subsample, colsample, reg_lambda, num_leaves, depth, GOSS sampling, etc.).

Three structural rules (`framework/CLAUDE_template.md` § "Per-Backbone 25-Experiment Mandate"):

1. **Every backbone gets a full 25-iter exploration**, even if axes "look exhausted" earlier.
2. **Each iter must cite a paper.** Negative results are informative and stay in the log.
3. **Variance characterisation is mandatory before declaring a champion**: iter 8 and iter 9 of every backbone are seed perturbations (`seed ∈ {7, 99}` alongside the default `42`) to compute a 3-seed median.

## 3. The `qa_excel` 25-iter loop

For the 38 Modeloff analysis tasks, the single backbone is `excel_agent` with 25 proposals across:

| Iter range | Backend / lever | Citation anchor |
|---|---|---|
| 1, 2, 24 | `class_prior` / per-task `prior_only` | Bishop 2006 PRML; Manning, Raghavan, Schütze 2008 IR |
| 3, 4, 5 | Logistic regression (C, max_iter, regularisation) | Hosmer, Lemeshow, Sturdivant 2013 'Applied Logistic Regression'; Hoerl & Kennard 1970 |
| 6-9 | k-NN (k, weights) | Cover & Hart 1967 IEEE |
| 10 | Multinomial Naive Bayes | Manning, Raghavan, Schütze 2008 IR Ch. 13 |
| 11 | `dummy_majority` (sklearn baseline) | Pedregosa et al. 2011 JMLR 'scikit-learn' |
| 12-14 | Prior blending (Jelinek-Mercer interpolation) | Manning, Raghavan, Schütze 2008 IR §12.2 |
| 15-17 | Temperature scaling | Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599) |
| 18-20 | Prior shaping (`agent_weight`, `agent_bias`) | Bishop 2006 PRML §3.5 |
| 21-23 | Seed-variance characterisation | Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap' |
| 24-25 | Final consolidated configurations | — |

Plus three newer backends added during the May 2026 diagnostic: `per_position` (per-relative-position letter prior), `prior_ensemble` (Wolpert 1992 'Stacked Generalization' Neural Networks) and `smart_pool_mode` (Hastie, Tibshirani, Friedman 2009 ESL §4.4.4).

The `qa_excel` composite is **leave-one-out CV on `train ∪ val`** for fitted classifiers, and a **Dirichlet-smoothed pool accuracy** for constant predictors — see [`postmortems/0002_excel_agent_synthetic_placeholder.md`](../postmortems/0002_excel_agent_synthetic_placeholder.md) and [`../adr/0009_qa_train_plus_val_refit.md`](../adr/0009_qa_train_plus_val_refit.md).

## 4. The 200-iter extension (`framework/extended_hill_climb.py`)

Triggered by `framework/run_extended.py` for any task that finishes the base 125 STILL losing to its DSBench baseline. Appends iters 126..325 to the same `experiment_log.jsonl` (no separate log; the dashboard / annotations / winner-archive machinery is reused unchanged).

The extension covers **15 backbone families**, each cited:

- `xgboost-deep` (16 iters) — depth ∈ {4..12}, lr ∈ {0.01, 0.03}; Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).
- `lightgbm-goss` (10 iters) — num_leaves ∈ {31, 63, 127, 255}, feature_fraction ∈ {0.7, 0.9}; Ke et al. 2017 NeurIPS 'LightGBM' (arXiv:1711.05101).
- `catboost-ordered` — ordered boosting recipe; Prokhorenkova et al. 2018 NeurIPS 'CatBoost: unbiased boosting with categorical features' (arXiv:1706.09516).
- `mlp-residual` — residual MLP per Liu et al. 2024 ICLR 'ResMLP for Tabular' family.
- `ft-transformer-large` — extreme regularisation, Gorishniy et al. 2021 'Revisiting DL for Tabular' (arXiv:2106.11189).
- `hgb`, `extra-trees`, `random-forest`, `elastic-net-stack` — sklearn ensembles; Breiman 2001 'Random Forests' MLJ.
- `ngboost-proxy`, `tabnet-proxy`, `tabpfn-proxy` — proxy dispatchers through XGBoost / FT-Transformer with the family's regularisation lever (NGBoost: Duan et al. 2020 ICML; TabNet: Arik & Pfister 2021 AAAI 'TabNet'; TabPFN: Hollmann et al. 2023 ICLR 'TabPFN').
- `lstm-tabular`, `patch-tsmixer`, `sklearn-stack-ensemble` — sequence-style + stacked dispatchers.

Proposals targeting backbones the runner doesn't natively implement (NGBoost, TabNet, TabPFN, PatchTSMixer) hit the closest implementation with the appropriate regularisation lever. The extension preserves the **one-config-change-per-experiment** rule from the base loop.

## 5. Composite metric

For modeling (and `structured`):
```
composite = min(val_score, train_score) - 0.05 * abs(val_score - train_score)
```
Higher is better. RMSE/MAE are negated inside `_score()` so the formula is metric-agnostic.

For `qa_excel`:
```
composite = leave_one_out_accuracy(train ∪ val)              # fitted classifiers
composite = dirichlet_smoothed_pool_accuracy(predicted, pool, alpha=8)  # constant predictors
```

The shift to LOO-CV for `qa_excel` is documented in [`../adr/0008_cross_task_pooling_for_training.md`](../adr/0008_cross_task_pooling_for_training.md) and the diagnostic [`../postmortems/0002_excel_agent_synthetic_placeholder.md`](../postmortems/0002_excel_agent_synthetic_placeholder.md).

## 6. Citation discipline

Every reasoning annotation includes at least one citation in the canonical format:

```
Author1, Author2, ... YEAR VENUE 'Paper Title' (arXiv:XXXX.XXXXX) — one-sentence relevance.
```

Parenthetical-only tags (`(Keskar2017)`) are insufficient — the audit warns on them. See [`../adr/0013_44_skill_industry_pack.md`](../adr/0013_44_skill_industry_pack.md) for the `citation-rigor` skill that polices this.

## 7. Stopping condition

The base loop runs all 125 iters unconditionally — early stopping is forbidden by the per-backbone mandate. The extension runs until 200 additional iters complete OR the task beats its DSBench baseline by >0.02 on the composite, whichever comes first. The full ledger lives in `experiment_log.jsonl`; the dashboard's "ALL" tab shows every iter.

## 8. Related

- [`../adr/0005_25_iters_per_backbone.md`](../adr/0005_25_iters_per_backbone.md) — why 25.
- [`../adr/0006_extended_200_iter_phase.md`](../adr/0006_extended_200_iter_phase.md) — why 200 extension.
- [`../reference/api_hill_climb.md`](../reference/api_hill_climb.md) — invocation contract.
- [`../runbooks/02_run_full_hill_climb.md`](../runbooks/02_run_full_hill_climb.md) — how to run.
