# Glossary

> Every term defined precisely. Cross-references use absolute paths from `docs/`.

## Project-specific terms

**autoresearch loop.** The Karpathy-adapted research loop: diagnose champion weakness → cite literature → hypothesise → predict → run ONE experiment → analyse → document. The outer loop **is** Claude; the runner is one function call. See [`architecture/04_hill_climb.md`](../part_3_processes/14_larger_testing.md).

**backbone.** A model family the runner can train. Currently 8 native backbones: `xgboost`, `lightgbm`, `catboost`, `mlp`, `ft_transformer` (proxied by `HistGradientBoosting`), `lstm`, `patchtsmixer`, `excel_agent`. See [`reference/api_runner.md`](framework_runner.md).

**champion.** The experiment with the highest `composite` score for a task. Stored in `<repo>/autoresearch_results/best_config.json`. Global, not per-backbone.

**composite.** The KEEP/DISCARD scalar. Tabular: `min(val, train) - 0.05 * |val - train|`. QA-Excel: LOO-CV on `train ∪ val` for fitted classifiers; Dirichlet-smoothed pool accuracy for constant predictors. See [`adr/0003_composite_metric_min_min_minus_gap.md`](../appendix_b_adrs/0003_composite_metric_min_min_minus_gap.md).

**cross-task pooling.** For `qa_excel`, train one classifier on the UNION of all 38 task training subsets, then evaluate per-task on each task's held-out val/test. See [`adr/0008_cross_task_pooling_for_training.md`](../appendix_b_adrs/0008_cross_task_pooling_for_training.md).

**DSBench.** The benchmark we are solving. Jing et al. 2025 ICLR 'DSBench: How Far Are Data Analysis Agents from Becoming Data Analysis Experts' (arXiv:2409.07703). 74 modeling + 38 analysis tasks; reference baseline 34.74% Relative Performance Gap (modeling) / 34.12% success (analysis).

**Extended hill-climb.** A 200-iter recovery cycle for tasks that still lose after the base 125. Covers 15 backbone families. See [`adr/0006_extended_200_iter_phase.md`](../appendix_b_adrs/0006_extended_200_iter_phase.md).

**Forensic committee.** The 10 agents (A–J + Z) that audit a champion. See [`architecture/05_forensic_audit.md`](../part_3_processes/09_code_review.md).

**Four-layer audit gate.** The pre-commit check that must pass before any submission. Validator + forensic + 14-section explainability + skill-pack coverage. See [`adr/0015_four_layer_audit_gate.md`](../appendix_b_adrs/0015_four_layer_audit_gate.md).

**Hill-climb.** The base 25-iter × 5-backbone loop (125 experiments per modeling task; 25 for analysis). See [`architecture/04_hill_climb.md`](../part_3_processes/14_larger_testing.md).

**`kind`.** `"modeling"` or `"analysis"`. The 38 analysis tasks are exactly the `qa_excel` problem-type tasks; the 74 modeling tasks are the rest. Note: `final_rollup.json` rows don't carry `kind`; `forensic_summary.json` rows do. See [`reference/api_status.md`](framework_status.md).

**LOO-CV.** Leave-one-out cross-validation. Used for the `qa_excel` composite where train+val pools are 4-20 samples.

**MD viewer.** `dashboard/md_viewer.html?path=<relative>` — client-side renderer for `.md` artefacts (browsers download `.md` files by default). See [`adr/0011_md_viewer_inline_render.md`](../appendix_b_adrs/0011_md_viewer_inline_render.md).

**Modeloff.** Financial-modelling competition whose 38 multiple-choice challenges form the analysis half of DSBench. Answer keys live in `_analysis_data.json`.

**P-core / E-core.** Performance / Efficient cores in Intel hybrid CPUs. **E-cores are banned** on the reference machine due to WHEA parity errors. See [`architecture/03_runtime.md`](../part_4_tools/25_compute_as_a_service.md).

**`problem_type`.** One of `classification_binary`, `classification_multiclass`, `regression`, `structured`, `qa_excel`. Drives backbone selection and metric.

**`qa_excel`.** The Modeloff QA problem type. Stride-5 split, cross-task pooling, LOO-CV composite, 38-task one-hot features.

**Refit consistency.** Forensic Agent I — champion refits within ±0.005 of recorded test score. See [`adr/0004_10_agent_forensic_committee.md`](../appendix_b_adrs/0004_10_agent_forensic_committee.md).

**Stride-5 split.** Position-bucketed 60/20/20 for small-N QA tasks: indices `i % 5 ∈ {0,1,2}` → train, `i % 5 == 3` → val, `i % 5 == 4` → test. See [`adr/0007_stride5_interleaved_split_for_qa.md`](../appendix_b_adrs/0007_stride5_interleaved_split_for_qa.md).

**Submission archive.** The 14-file per-task bundle under `submissions/dsbench_submission/<kind>/<slug>/`. See [`architecture/09_submission_archive.md`](../part_4_tools/24_continuous_delivery.md).

**Test set.** The 15% held-back split. Touched ONCE per task, by `framework/final_report.py`. Forbidden in any other code path.

## Cited papers (canonical strings)

Use these strings verbatim in reasoning annotations and ADRs.

- **Bishop 2006 'Pattern Recognition and Machine Learning' (PRML)** — Christopher M. Bishop, Springer 2006. Source for §1.3 (i.i.d. / exchangeability), §3.5 (Bayesian priors), §5.5.2 (early-stopping discipline), §11.4 (sequential Monte Carlo / prior shaping).
- **Breiman 2001 MLJ 'Random Forests'** — Leo Breiman, Machine Learning Journal 45(1). Source for permutation feature importance and ensemble theory.
- **Chen, Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754)** — anchors the gradient-boosted-tree hill-climb axis (depth, lr, subsample, colsample, reg_lambda).
- **Cover, Hart 1967 IEEE 'Nearest Neighbor Pattern Classification'** — k-NN convergence guarantees; cited in `qa_excel` iters 6-9.
- **Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine'** — original gradient boosting paper; cited for depth-vs-iter tradeoff and stochastic gradient boosting.
- **Gorishniy et al. 2021 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189)** — FT-Transformer; the runner approximates it with `HistGradientBoosting` for hill-climb speed.
- **Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599)** — temperature scaling; cited in `qa_excel` iters 15-17 and the 14-section audit § 6 (Calibration).
- **Hastie, Tibshirani, Friedman 2009 'The Elements of Statistical Learning' (ESL)** — Springer. §4.4.4 on prior-aware decision rules; cited in `smart_pool_mode` backend.
- **Hoerl, Kennard 1970 Technometrics 'Ridge Regression: Biased Estimation for Nonorthogonal Problems'** — L2 regularisation foundation; cited in `qa_excel` LogReg iters.
- **Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second'** — proxied by FT-Transformer with extreme regularisation in the extended hill-climb.
- **Hosmer, Lemeshow, Sturdivant 2013 'Applied Logistic Regression'** — Wiley. §1.7 on estimator bias under small-sample resampling.
- **Jing et al. 2025 ICLR 'DSBench: How Far Are Data Analysis Agents from Becoming Data Analysis Experts' (arXiv:2409.07703)** — the benchmark we are solving.
- **Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' (arXiv:1711.05101)** — LightGBM with GOSS; leaf-wise GBM SOTA.
- **Kendall, Gal 2017 NeurIPS 'What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?' (arXiv:1703.04977)** — heteroscedastic loss; mean + log_variance regression head.
- **Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation'** — variance characterisation discipline; cited in seed-perturbation iters 8/9/21-23.
- **Loshchilov, Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101)** — AdamW; default for MLP / FT-Transformer.
- **Lundberg, Lee 2017 NeurIPS 'A Unified Approach to Interpreting Model Predictions' (arXiv:1705.07874)** — SHAP; cited in the 14-section audit § 4.
- **Manning, Raghavan, Schütze 2008 'Introduction to Information Retrieval'** — Cambridge UP. Ch. 12.2 Jelinek-Mercer interpolation (Dirichlet smoothing in QA composite); Ch. 13 multinomial Naive Bayes; §2.2 case-folding canonicalisation.
- **Pedregosa et al. 2011 JMLR 'scikit-learn: Machine Learning in Python'** — sklearn `DummyClassifier` baseline.
- **Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: unbiased boosting with categorical features' (arXiv:1706.09516)** — ordered boosting recipe.
- **Wolpert 1992 Neural Networks 'Stacked Generalization'** — meta-learning across base learners; cited in `prior_ensemble` backend.

## Acronyms

- **AUC / ROC-AUC** — Area Under the Receiver Operating Characteristic Curve.
- **ECE** — Expected Calibration Error.
- **GBM** — Gradient-Boosted Machine.
- **GOSS** — Gradient-based One-Side Sampling (LightGBM).
- **HGB** — sklearn `HistGradientBoosting*`.
- **KS** — Kolmogorov-Smirnov (two-sample distribution test).
- **LOO-CV** — Leave-One-Out Cross-Validation.
- **MCC** — Matthews Correlation Coefficient.
- **MI** — Mutual Information.
- **MLP** — Multi-Layer Perceptron.
- **PRML** — Bishop 2006 'Pattern Recognition and Machine Learning' (book title).
- **SHAP** — SHapley Additive exPlanations.
- **WHEA** — Windows Hardware Error Architecture (kernel-mode error logger).

## Related

- [`architecture/01_design_doc.md`](../part_1_thesis/01_what_is_autoresearch_engineering.md)
- [`onboarding/01_what_is_this.md`](../part_1_thesis/01_what_is_autoresearch_engineering.md)
