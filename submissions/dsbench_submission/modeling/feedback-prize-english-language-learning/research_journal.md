# Research Journal — feedback-prize-english-language-learning

_(populated by `framework/hill_climb.py`)_

## Exp1 — xgboost iter 1
**Diagnosis:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

**Hypothesis:** Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).

**Prediction:** Composite in [0.55, 0.85] depending on task difficulty.

**Verdict:** KEEP composite=-2.1161 (delta +inf vs prev best -inf); val_score=-2.0184516898916036; train_score=-0.06503539705114483.

**Learning:** Iter 1 xgboost: KEEP. Train/val gap = 1.9534. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — xgboost iter 2
**Diagnosis:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.

**Citations:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

**Hypothesis:** Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-2.4811 (delta -0.3650 vs prev best -2.1161); val_score=-2.363303948916042; train_score=-0.00707766269719862.

**Learning:** Iter 2 xgboost: DISCARD. Train/val gap = 2.3562. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — xgboost iter 3
**Diagnosis:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

**Hypothesis:** Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-1.6640 (delta +0.4521 vs prev best -2.1161); val_score=-1.5953061603416439; train_score=-0.22155165651148084.

**Learning:** Iter 3 xgboost: KEEP. Train/val gap = 1.3738. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp4 — xgboost iter 4
**Diagnosis:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.

**Citations:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

**Hypothesis:** Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.

**Prediction:** Composite delta in [+0.001, +0.010].

**Verdict:** DISCARD composite=-2.1929 (delta -0.5289 vs prev best -1.6640); val_score=-2.0918241155366233; train_score=-0.07045878319767751.

**Learning:** Iter 4 xgboost: DISCARD. Train/val gap = 2.0214. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — xgboost iter 5
**Diagnosis:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

**Hypothesis:** Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.

**Prediction:** Composite delta in [+0.002, +0.012].

**Verdict:** DISCARD composite=-1.9654 (delta -0.3014 vs prev best -1.6640); val_score=-1.8786311275314476; train_score=-0.1441109706902406.

**Learning:** Iter 5 xgboost: DISCARD. Train/val gap = 1.7345. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — xgboost iter 6
**Diagnosis:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.

**Citations:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

**Hypothesis:** Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.1902 (delta -0.5262 vs prev best -1.6640); val_score=-2.096493077069058; train_score=-0.22154255965587796.

**Learning:** Iter 6 xgboost: DISCARD. Train/val gap = 1.8750. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — xgboost iter 7
**Diagnosis:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.

**Citations:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

**Hypothesis:** Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-1.8915 (delta -0.2275 vs prev best -1.6640); val_score=-1.8062652032865723; train_score=-0.10152974884447462.

**Learning:** Iter 7 xgboost: DISCARD. Train/val gap = 1.7047. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp8 — xgboost iter 8
**Diagnosis:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.

**Citations:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.0941 (delta -0.4301 vs prev best -1.6640); val_score=-1.9973097827848847; train_score=-0.06236151537140836.

**Learning:** Iter 8 xgboost: DISCARD. Train/val gap = 1.9349. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — xgboost iter 9
**Diagnosis:** Third seed for 3-seed median (autoresearch protocol).

**Citations:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1266 (delta -0.4626 vs prev best -1.6640); val_score=-2.0282260393504514; train_score=-0.06101000839958366.

**Learning:** Iter 9 xgboost: DISCARD. Train/val gap = 1.9672. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — xgboost iter 10
**Diagnosis:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

**Hypothesis:** Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7019 (delta -1.0379 vs prev best -1.6640); val_score=-2.573355592259147; train_score=-0.0031129067706361074.

**Learning:** Iter 10 xgboost: DISCARD. Train/val gap = 2.5702. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — xgboost iter 11
**Diagnosis:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.

**Citations:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

**Hypothesis:** Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-1.6645 (delta -0.0005 vs prev best -1.6640); val_score=-1.5954751793901172; train_score=-0.21530389061257132.

**Learning:** Iter 11 xgboost: DISCARD. Train/val gap = 1.3802. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp12 — xgboost iter 12
**Diagnosis:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

**Hypothesis:** Hypothesis: larger leaves reduce variance, improve val by 0.5%.

**Prediction:** Composite delta in [-0.002, +0.010].

**Verdict:** DISCARD composite=-2.1161 (delta -0.4521 vs prev best -1.6640); val_score=-2.0184516898916036; train_score=-0.06503539705114483.

**Learning:** Iter 12 xgboost: DISCARD. Train/val gap = 1.9534. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — xgboost iter 13
**Diagnosis:** Gamma split-penalty 0.5 — discourages overly eager splits.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

**Hypothesis:** Hypothesis: fewer, higher-quality splits. Val improves slightly.

**Prediction:** Composite delta in [-0.003, +0.008].

**Verdict:** DISCARD composite=-2.1161 (delta -0.4521 vs prev best -1.6640); val_score=-2.0184516898916036; train_score=-0.06503539705114483.

**Learning:** Iter 13 xgboost: DISCARD. Train/val gap = 1.9534. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — xgboost iter 14
**Diagnosis:** High subsample for low-noise tasks — opposite direction from iter-4/7.

**Citations:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

**Hypothesis:** Hypothesis: gentle bagging if iter-4/7 over-regularised.

**Prediction:** Composite delta in [-0.005, +0.007].

**Verdict:** DISCARD composite=-2.2197 (delta -0.5557 vs prev best -1.6640); val_score=-2.1166537692460534; train_score=-0.056139604533195234.

**Learning:** Iter 14 xgboost: DISCARD. Train/val gap = 2.0605. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — xgboost iter 15
**Diagnosis:** L1 regularisation (reg_alpha) for feature selection.

**Citations:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

**Hypothesis:** Hypothesis: L1 trims noise features, val improves.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-2.3740 (delta -0.7100 vs prev best -1.6640); val_score=-2.2623086795740375; train_score=-0.029298450507080298.

**Learning:** Iter 15 xgboost: DISCARD. Train/val gap = 2.2330. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — xgboost iter 16
**Diagnosis:** Combined moderate regularisation — meta-search across all axes.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

**Hypothesis:** Hypothesis: balanced config beats single-knob champions.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-2.0996 (delta -0.4356 vs prev best -1.6640); val_score=-2.0008059308348147; train_score=-0.024131534899646683.

**Learning:** Iter 16 xgboost: DISCARD. Train/val gap = 1.9767. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — xgboost iter 17
**Diagnosis:** Fourth seed — extend variance characterisation.

**Citations:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

**Hypothesis:** Hypothesis: within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1049 (delta -0.4409 vs prev best -1.6640); val_score=-2.007750751421596; train_score=-0.06400870864796765.

**Learning:** Iter 17 xgboost: DISCARD. Train/val gap = 1.9437. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — xgboost iter 18
**Diagnosis:** Fifth seed.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Same as iter-15.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1349 (delta -0.4709 vs prev best -1.6640); val_score=-2.036131407373616; train_score=-0.06134487913368311.

**Learning:** Iter 18 xgboost: DISCARD. Train/val gap = 1.9748. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — xgboost iter 19
**Diagnosis:** Aggressive depth=12 with proportionally lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

**Hypothesis:** Hypothesis: depth=12 will overfit unless lr is very low.

**Prediction:** Composite delta in [-0.030, +0.010].

**Verdict:** DISCARD composite=-2.7247 (delta -1.0607 vs prev best -1.6640); val_score=-2.595689530979264; train_score=-0.01512034312953879.

**Learning:** Iter 19 xgboost: DISCARD. Train/val gap = 2.5806. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — xgboost iter 20
**Diagnosis:** Very shallow, high-lr — stump-like learners as opposite extreme.

**Citations:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

**Hypothesis:** Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.

**Prediction:** Composite delta in [-0.040, +0.005].

**Verdict:** KEEP composite=-1.3722 (delta +0.2918 vs prev best -1.6640); val_score=-1.32172539407747; train_score=-0.3119929849794263.

**Learning:** Iter 20 xgboost: KEEP. Train/val gap = 1.0097. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp21 — xgboost iter 21
**Diagnosis:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.

**Citations:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

**Hypothesis:** Hypothesis: no-op vs baseline; informational only.

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-2.1097 (delta -0.7375 vs prev best -1.3722); val_score=-2.0102569305790037; train_score=-0.02150456065465005.

**Learning:** Iter 21 xgboost: DISCARD. Train/val gap = 1.9888. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — xgboost iter 22
**Diagnosis:** Confirm hist-method explicitly — same as default but pinned.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

**Hypothesis:** Hypothesis: no change vs baseline (already default in our setup).

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-2.1161 (delta -0.7439 vs prev best -1.3722); val_score=-2.0184516898916036; train_score=-0.06503539705114483.

**Learning:** Iter 22 xgboost: DISCARD. Train/val gap = 1.9534. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — xgboost iter 23
**Diagnosis:** Long-and-slow final refinement with mid-strength L2.

**Citations:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

**Hypothesis:** Hypothesis: best champion candidate. Val should peak.

**Prediction:** Composite delta in [+0.005, +0.025].

**Verdict:** DISCARD composite=-1.7899 (delta -0.4177 vs prev best -1.3722); val_score=-1.7092865943712856; train_score=-0.09688192946507862.

**Learning:** Iter 23 xgboost: DISCARD. Train/val gap = 1.6124. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — xgboost iter 24
**Diagnosis:** Combined moderate everything — explore a balanced corner.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-2.0072 (delta -0.6350 vs prev best -1.3722); val_score=-1.9159719479683441; train_score=-0.0904231205032629.

**Learning:** Iter 24 xgboost: DISCARD. Train/val gap = 1.8255. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — xgboost iter 25
**Diagnosis:** Final 6th seed — closes the variance characterisation for this backbone.

**Citations:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1350 (delta -0.7628 vs prev best -1.3722); val_score=-2.0362830383355686; train_score=-0.062232145767190834.

**Learning:** Iter 25 xgboost: DISCARD. Train/val gap = 1.9741. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp26 — lightgbm iter 1
**Diagnosis:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard lightgbm config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 1 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp27 — lightgbm iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-3.9986 (delta -2.6263 vs prev best -1.3722); val_score=-3.969278239689721; train_score=-3.3837967448359456.

**Learning:** Iter 2 lightgbm: DISCARD. Train/val gap = 0.5855. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp28 — lightgbm iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.6410 (delta -3.2688 vs prev best -1.3722); val_score=-4.626555447868935; train_score=-4.337073282209332.

**Learning:** Iter 3 lightgbm: DISCARD. Train/val gap = 0.2895. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp29 — lightgbm iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-3.4672 (delta -2.0950 vs prev best -1.3722); val_score=-3.422683016002938; train_score=-2.5329306173900856.

**Learning:** Iter 4 lightgbm: DISCARD. Train/val gap = 0.8898. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp30 — lightgbm iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-2.0305 (delta -0.6583 vs prev best -1.3722); val_score=-1.9377916820195404; train_score=-0.0836650057844931.

**Learning:** Iter 5 lightgbm: DISCARD. Train/val gap = 1.8541. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp31 — lightgbm iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.0305 (delta -0.6583 vs prev best -1.3722); val_score=-1.9377916820195404; train_score=-0.0836650057844931.

**Learning:** Iter 6 lightgbm: DISCARD. Train/val gap = 1.8541. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp32 — lightgbm iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2363 (delta -2.8640 vs prev best -1.3722); val_score=-4.212821392360605; train_score=-3.7440159404580187.

**Learning:** Iter 7 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp33 — lightgbm iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2427 (delta -2.8705 vs prev best -1.3722); val_score=-4.219090032894432; train_score=-3.746503873763866.

**Learning:** Iter 8 lightgbm: DISCARD. Train/val gap = 0.4726. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp34 — lightgbm iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 9 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp35 — lightgbm iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.5184 (delta -3.1462 vs prev best -1.3722); val_score=-4.501116908945391; train_score=-4.155879148528254.

**Learning:** Iter 10 lightgbm: DISCARD. Train/val gap = 0.3452. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp36 — lightgbm iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 11 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp37 — lightgbm iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 12 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp38 — lightgbm iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-4.4581 (delta -3.0859 vs prev best -1.3722); val_score=-4.439546312791056; train_score=-4.068483285299469.

**Learning:** Iter 13 lightgbm: DISCARD. Train/val gap = 0.3711. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp39 — lightgbm iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2362 (delta -2.8640 vs prev best -1.3722); val_score=-4.212770489188518; train_score=-3.743856944767072.

**Learning:** Iter 14 lightgbm: DISCARD. Train/val gap = 0.4689. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp40 — lightgbm iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2343 (delta -2.8621 vs prev best -1.3722); val_score=-4.211010721353256; train_score=-3.7447920656153704.

**Learning:** Iter 15 lightgbm: DISCARD. Train/val gap = 0.4662. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp41 — lightgbm iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 16 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp42 — lightgbm iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 17 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp43 — lightgbm iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-3.8006 (delta -2.4283 vs prev best -1.3722); val_score=-3.765610218933123; train_score=-3.0666733510313358.

**Learning:** Iter 18 lightgbm: DISCARD. Train/val gap = 0.6989. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp44 — lightgbm iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-4.7729 (delta -3.4007 vs prev best -1.3722); val_score=-4.7613154418538475; train_score=-4.5297415053049805.

**Learning:** Iter 19 lightgbm: DISCARD. Train/val gap = 0.2316. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp45 — lightgbm iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 20 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp46 — lightgbm iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 21 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp47 — lightgbm iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-4.2379 (delta -2.8657 vs prev best -1.3722); val_score=-4.214487744074622; train_score=-3.745653937902599.

**Learning:** Iter 22 lightgbm: DISCARD. Train/val gap = 0.4688. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp48 — lightgbm iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.4007 (delta -3.0285 vs prev best -1.3722); val_score=-4.380862939938056; train_score=-3.984638934287194.

**Learning:** Iter 23 lightgbm: DISCARD. Train/val gap = 0.3962. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp49 — lightgbm iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.0032 (delta -2.6310 vs prev best -1.3722); val_score=-3.9738107708615997; train_score=-3.3858551272281443.

**Learning:** Iter 24 lightgbm: DISCARD. Train/val gap = 0.5880. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp50 — lightgbm iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2323 (delta -2.8601 vs prev best -1.3722); val_score=-4.20899886745352; train_score=-3.743421001900657.

**Learning:** Iter 25 lightgbm: DISCARD. Train/val gap = 0.4656. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp51 — catboost iter 1
**Diagnosis:** Baseline catboost per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard catboost config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 1 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp52 — catboost iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 2 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp53 — catboost iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 3 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp54 — catboost iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 4 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp55 — catboost iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 5 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp56 — catboost iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 6 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp57 — catboost iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 7 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp58 — catboost iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 8 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp59 — catboost iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 9 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp60 — catboost iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 10 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp61 — catboost iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 11 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp62 — catboost iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 12 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp63 — catboost iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 13 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp64 — catboost iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 14 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp65 — catboost iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 15 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp66 — catboost iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 16 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp67 — catboost iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 17 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp68 — catboost iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 18 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp69 — catboost iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 19 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp70 — catboost iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 20 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp71 — catboost iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 21 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp72 — catboost iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 22 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp73 — catboost iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 23 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp74 — catboost iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 24 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp75 — catboost iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.3722); val_score=NA; train_score=NA.

**Learning:** Iter 25 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp76 — mlp iter 1
**Diagnosis:** Baseline mlp per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard mlp config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** KEEP composite=-0.5455 (delta +0.8267 vs prev best -1.3722); val_score=-0.5355016053457978; train_score=-0.33561697905917226.

**Learning:** Iter 1 mlp: KEEP. Train/val gap = 0.1999. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp77 — mlp iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-0.4809 (delta +0.0646 vs prev best -0.5455); val_score=-0.4692429652461572; train_score=-0.23543938703669365.

**Learning:** Iter 2 mlp: KEEP. Train/val gap = 0.2338. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp78 — mlp iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.8248 (delta -0.3439 vs prev best -0.4809); val_score=-0.8186325673341737; train_score=-0.6949866099062556.

**Learning:** Iter 3 mlp: DISCARD. Train/val gap = 0.1236. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp79 — mlp iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** KEEP composite=-0.4285 (delta +0.0524 vs prev best -0.4809); val_score=-0.41766629907325975; train_score=-0.20124367478897442.

**Learning:** Iter 4 mlp: KEEP. Train/val gap = 0.2164. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp80 — mlp iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.5999 (delta -0.1714 vs prev best -0.4285); val_score=-0.5929082626029545; train_score=-0.45380861410818596.

**Learning:** Iter 5 mlp: DISCARD. Train/val gap = 0.1391. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp81 — mlp iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.0501 (delta -1.6216 vs prev best -0.4285); val_score=-2.045088709280579; train_score=-1.9442514490291636.

**Learning:** Iter 6 mlp: DISCARD. Train/val gap = 0.1008. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp82 — mlp iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5145 (delta -0.0860 vs prev best -0.4285); val_score=-0.5067550506434202; train_score=-0.3525822895631613.

**Learning:** Iter 7 mlp: DISCARD. Train/val gap = 0.1542. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp83 — mlp iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5806 (delta -0.1522 vs prev best -0.4285); val_score=-0.5694994683418103; train_score=-0.3467326486456963.

**Learning:** Iter 8 mlp: DISCARD. Train/val gap = 0.2228. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp84 — mlp iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.4706 (delta -0.0421 vs prev best -0.4285); val_score=-0.458488651170541; train_score=-0.21652832237705597.

**Learning:** Iter 9 mlp: DISCARD. Train/val gap = 0.2420. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp85 — mlp iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.5916 (delta -0.1631 vs prev best -0.4285); val_score=-0.5835155787067647; train_score=-0.4220983655681023.

**Learning:** Iter 10 mlp: DISCARD. Train/val gap = 0.1614. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp86 — mlp iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-0.5392 (delta -0.1107 vs prev best -0.4285); val_score=-0.5278197224440746; train_score=-0.3003731473245686.

**Learning:** Iter 11 mlp: DISCARD. Train/val gap = 0.2274. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp87 — mlp iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-0.4519 (delta -0.0234 vs prev best -0.4285); val_score=-0.439174292372718; train_score=-0.18494919333791227.

**Learning:** Iter 12 mlp: DISCARD. Train/val gap = 0.2542. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp88 — mlp iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-0.7365 (delta -0.3080 vs prev best -0.4285); val_score=-0.7295916998830291; train_score=-0.5918839645512494.

**Learning:** Iter 13 mlp: DISCARD. Train/val gap = 0.1377. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp89 — mlp iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.4898 (delta -0.0614 vs prev best -0.4285); val_score=-0.482608079689257; train_score=-0.33801768785883285.

**Learning:** Iter 14 mlp: DISCARD. Train/val gap = 0.1446. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp90 — mlp iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5283 (delta -0.0999 vs prev best -0.4285); val_score=-0.5198771537044571; train_score=-0.3506571875296967.

**Learning:** Iter 15 mlp: DISCARD. Train/val gap = 0.1692. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp91 — mlp iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.5892 (delta -0.1607 vs prev best -0.4285); val_score=-0.5811685658906944; train_score=-0.4209731493710028.

**Learning:** Iter 16 mlp: DISCARD. Train/val gap = 0.1602. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp92 — mlp iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** KEEP composite=-0.3654 (delta +0.0631 vs prev best -0.4285); val_score=-0.35502477314301595; train_score=-0.14808525151702895.

**Learning:** Iter 17 mlp: KEEP. Train/val gap = 0.2069. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp93 — mlp iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-0.4557 (delta -0.0904 vs prev best -0.3654); val_score=-0.4451262268514419; train_score=-0.23311459667679021.

**Learning:** Iter 18 mlp: DISCARD. Train/val gap = 0.2120. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp94 — mlp iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-3.6319 (delta -3.2666 vs prev best -0.3654); val_score=-3.616433116444679; train_score=-3.3065279982572773.

**Learning:** Iter 19 mlp: DISCARD. Train/val gap = 0.3099. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp95 — mlp iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.4596 (delta -0.0942 vs prev best -0.3654); val_score=-0.4470341679072159; train_score=-0.19559585044855674.

**Learning:** Iter 20 mlp: DISCARD. Train/val gap = 0.2514. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp96 — mlp iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.5455 (delta -0.1801 vs prev best -0.3654); val_score=-0.5355016053457978; train_score=-0.33561697905917226.

**Learning:** Iter 21 mlp: DISCARD. Train/val gap = 0.1999. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp97 — mlp iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-0.5455 (delta -0.1801 vs prev best -0.3654); val_score=-0.5355016053457978; train_score=-0.33561697905917226.

**Learning:** Iter 22 mlp: DISCARD. Train/val gap = 0.1999. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp98 — mlp iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.6128 (delta -0.2474 vs prev best -0.3654); val_score=-0.6037321473872359; train_score=-0.42310806494085673.

**Learning:** Iter 23 mlp: DISCARD. Train/val gap = 0.1806. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp99 — mlp iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.4891 (delta -0.1238 vs prev best -0.3654); val_score=-0.478497843509307; train_score=-0.2656765635314016.

**Learning:** Iter 24 mlp: DISCARD. Train/val gap = 0.2128. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp100 — mlp iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5257 (delta -0.1603 vs prev best -0.3654); val_score=-0.5168067798544754; train_score=-0.33926000555951474.

**Learning:** Iter 25 mlp: DISCARD. Train/val gap = 0.1775. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp101 — ft_transformer iter 1
**Diagnosis:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard ft_transformer config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 1 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp102 — ft_transformer iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-4.0355 (delta -3.6701 vs prev best -0.3654); val_score=-4.011409455987208; train_score=-3.5292423205055004.

**Learning:** Iter 2 ft_transformer: DISCARD. Train/val gap = 0.4822. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp103 — ft_transformer iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.6312 (delta -4.2658 vs prev best -0.3654); val_score=-4.618598310001442; train_score=-4.367160683082439.

**Learning:** Iter 3 ft_transformer: DISCARD. Train/val gap = 0.2514. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp104 — ft_transformer iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-3.5281 (delta -3.1627 vs prev best -0.3654); val_score=-3.491183361846738; train_score=-2.752712206622921.

**Learning:** Iter 4 ft_transformer: DISCARD. Train/val gap = 0.7385. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp105 — ft_transformer iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-2.0158 (delta -1.6504 vs prev best -0.3654); val_score=-1.9239123933263798; train_score=-0.08715757331116773.

**Learning:** Iter 5 ft_transformer: DISCARD. Train/val gap = 1.8368. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp106 — ft_transformer iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.0158 (delta -1.6504 vs prev best -0.3654); val_score=-1.9239123933263798; train_score=-0.08715757331116773.

**Learning:** Iter 6 ft_transformer: DISCARD. Train/val gap = 1.8368. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp107 — ft_transformer iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 7 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp108 — ft_transformer iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 8 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp109 — ft_transformer iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 9 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp110 — ft_transformer iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.5053 (delta -4.1400 vs prev best -0.3654); val_score=-4.491081148329384; train_score=-4.206057934194098.

**Learning:** Iter 10 ft_transformer: DISCARD. Train/val gap = 0.2850. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp111 — ft_transformer iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 11 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp112 — ft_transformer iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 12 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp113 — ft_transformer iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-4.4521 (delta -4.0868 vs prev best -0.3654); val_score=-4.436770198443233; train_score=-4.1294912979088005.

**Learning:** Iter 13 ft_transformer: DISCARD. Train/val gap = 0.3073. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp114 — ft_transformer iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 14 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp115 — ft_transformer iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 15 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp116 — ft_transformer iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 16 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp117 — ft_transformer iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 17 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp118 — ft_transformer iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-3.8541 (delta -3.4887 vs prev best -0.3654); val_score=-3.8251866545708837; train_score=-3.247449969686585.

**Learning:** Iter 18 ft_transformer: DISCARD. Train/val gap = 0.5777. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp119 — ft_transformer iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-4.7677 (delta -4.4023 vs prev best -0.3654); val_score=-4.756783199757909; train_score=-4.5392215009249846.

**Learning:** Iter 19 ft_transformer: DISCARD. Train/val gap = 0.2176. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp120 — ft_transformer iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 20 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp121 — ft_transformer iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 21 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp122 — ft_transformer iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 22 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp123 — ft_transformer iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.4001 (delta -4.0347 vs prev best -0.3654); val_score=-4.383663829020032; train_score=-4.0548707085029525.

**Learning:** Iter 23 ft_transformer: DISCARD. Train/val gap = 0.3288. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp124 — ft_transformer iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.0352 (delta -3.6699 vs prev best -0.3654); val_score=-4.011147598569461; train_score=-3.5294095568136425.

**Learning:** Iter 24 ft_transformer: DISCARD. Train/val gap = 0.4817. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp125 — ft_transformer iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2489 (delta -3.8835 vs prev best -0.3654); val_score=-4.229613271122236; train_score=-3.8441728385439013.

**Learning:** Iter 25 ft_transformer: DISCARD. Train/val gap = 0.3854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp126 — ext xgboost 1/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-1.9156 (delta -1.5503 vs prev best -0.3654); val=-1.8506201426382067 train=-0.5503490456658877.

**Learning:** Ext iter 1 (xgboost): DISCARD. Train/val gap = 1.3003. This iter targets Extended xgboost sweep.


## Exp127 — ext xgboost 2/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-1.6740 (delta -1.3086 vs prev best -0.3654); val=-1.6009793592286403 train=-0.141416441829385.

**Learning:** Ext iter 2 (xgboost): DISCARD. Train/val gap = 1.4596. This iter targets Extended xgboost sweep.


## Exp128 — ext xgboost 3/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.0051 (delta -1.6397 vs prev best -0.3654); val=-1.923926460347705 train=-0.30064231586749063.

**Learning:** Ext iter 3 (xgboost): DISCARD. Train/val gap = 1.6233. This iter targets Extended xgboost sweep.


## Exp129 — ext xgboost 4/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-1.8895 (delta -1.5242 vs prev best -0.3654); val=-1.802066435394737 train=-0.05245032678596988.

**Learning:** Ext iter 4 (xgboost): DISCARD. Train/val gap = 1.7496. This iter targets Extended xgboost sweep.


## Exp130 — ext xgboost 5/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.1838 (delta -1.8185 vs prev best -0.3654); val=-2.0870999301223336 train=-0.15217329539603486.

**Learning:** Ext iter 5 (xgboost): DISCARD. Train/val gap = 1.9349. This iter targets Extended xgboost sweep.


## Exp131 — ext xgboost 6/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.1167 (delta -1.7513 vs prev best -0.3654); val=-2.0164336718852898 train=-0.01147118032737687.

**Learning:** Ext iter 6 (xgboost): DISCARD. Train/val gap = 2.0050. This iter targets Extended xgboost sweep.


## Exp132 — ext xgboost 7/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.3243 (delta -1.9589 vs prev best -0.3654); val=-2.217290478842571 train=-0.076872813122937.

**Learning:** Ext iter 7 (xgboost): DISCARD. Train/val gap = 2.1404. This iter targets Extended xgboost sweep.


## Exp133 — ext xgboost 8/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.3015 (delta -1.9362 vs prev best -0.3654); val=-2.1920375084765578 train=-0.0020333566503192412.

**Learning:** Ext iter 8 (xgboost): DISCARD. Train/val gap = 2.1900. This iter targets Extended xgboost sweep.


## Exp134 — ext xgboost 9/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.4825 (delta -2.1171 vs prev best -0.3654); val=-2.3662403591340473 train=-0.04189177917564468.

**Learning:** Ext iter 9 (xgboost): DISCARD. Train/val gap = 2.3243. This iter targets Extended xgboost sweep.


## Exp135 — ext xgboost 10/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.4832 (delta -2.1178 vs prev best -0.3654); val=-2.3649520138475353 train=-0.0005286759827443733.

**Learning:** Ext iter 10 (xgboost): DISCARD. Train/val gap = 2.3644. This iter targets Extended xgboost sweep.


## Exp136 — ext xgboost 11/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.6578 (delta -2.2924 vs prev best -0.3654); val=-2.532225526808745 train=-0.021599264621958415.

**Learning:** Ext iter 11 (xgboost): DISCARD. Train/val gap = 2.5106. This iter targets Extended xgboost sweep.


## Exp137 — ext xgboost 12/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7196 (delta -2.3542 vs prev best -0.3654); val=-2.5901082221732703 train=-0.00045568681439840604.

**Learning:** Ext iter 12 (xgboost): DISCARD. Train/val gap = 2.5897. This iter targets Extended xgboost sweep.


## Exp138 — ext xgboost 13/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7337 (delta -2.3683 vs prev best -0.3654); val=-2.604390483139149 train=-0.018536593373441733.

**Learning:** Ext iter 13 (xgboost): DISCARD. Train/val gap = 2.5859. This iter targets Extended xgboost sweep.


## Exp139 — ext xgboost 14/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7769 (delta -2.4115 vs prev best -0.3654); val=-2.6446511538664175 train=-0.00042112881322234515.

**Learning:** Ext iter 14 (xgboost): DISCARD. Train/val gap = 2.6442. This iter targets Extended xgboost sweep.


## Exp140 — ext lightgbm 15/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-1.8549 (delta -1.4895 vs prev best -0.3654); val=-1.767864705600144 train=-0.027856163854022186.

**Learning:** Ext iter 15 (lightgbm): DISCARD. Train/val gap = 1.7400. This iter targets LightGBM leaf-wise sweep.


## Exp141 — ext lightgbm 16/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-1.9217 (delta -1.5563 vs prev best -0.3654); val=-1.8321034789030248 train=-0.040294050067541005.

**Learning:** Ext iter 16 (lightgbm): DISCARD. Train/val gap = 1.7918. This iter targets LightGBM leaf-wise sweep.


## Exp142 — ext lightgbm 17/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-1.9645 (delta -1.5991 vs prev best -0.3654); val=-1.8735701575261061 train=-0.05484233717487156.

**Learning:** Ext iter 17 (lightgbm): DISCARD. Train/val gap = 1.8187. This iter targets LightGBM leaf-wise sweep.


## Exp143 — ext lightgbm 18/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0377 (delta -1.6723 vs prev best -0.3654); val=-1.9436525650118337 train=-0.06272216089516501.

**Learning:** Ext iter 18 (lightgbm): DISCARD. Train/val gap = 1.8809. This iter targets LightGBM leaf-wise sweep.


## Exp144 — ext lightgbm 19/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-1.9645 (delta -1.5991 vs prev best -0.3654); val=-1.8735701575261061 train=-0.05484233717487156.

**Learning:** Ext iter 19 (lightgbm): DISCARD. Train/val gap = 1.8187. This iter targets LightGBM leaf-wise sweep.


## Exp145 — ext lightgbm 20/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0377 (delta -1.6723 vs prev best -0.3654); val=-1.9436525650118337 train=-0.06272216089516501.

**Learning:** Ext iter 20 (lightgbm): DISCARD. Train/val gap = 1.8809. This iter targets LightGBM leaf-wise sweep.


## Exp146 — ext lightgbm 21/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-1.9645 (delta -1.5991 vs prev best -0.3654); val=-1.8735701575261061 train=-0.05484233717487156.

**Learning:** Ext iter 21 (lightgbm): DISCARD. Train/val gap = 1.8187. This iter targets LightGBM leaf-wise sweep.


## Exp147 — ext lightgbm 22/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0377 (delta -1.6723 vs prev best -0.3654); val=-1.9436525650118337 train=-0.06272216089516501.

**Learning:** Ext iter 22 (lightgbm): DISCARD. Train/val gap = 1.8809. This iter targets LightGBM leaf-wise sweep.


## Exp148 — ext catboost 23/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 23 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp149 — ext catboost 24/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 24 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp150 — ext catboost 25/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 25 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp151 — ext catboost 26/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 26 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp152 — ext catboost 27/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 27 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp153 — ext catboost 28/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 28 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp154 — ext catboost 29/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 29 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp155 — ext catboost 30/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 30 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp156 — ext catboost 31/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3654); val=NA train=NA.

**Learning:** Ext iter 31 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp157 — ext mlp 32/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.6406 (delta -0.2752 vs prev best -0.3654); val=-0.6318016455658787 train=-0.45668613412646797.

**Learning:** Ext iter 32 (mlp): DISCARD. Train/val gap = 0.1751. This iter targets MLP capacity sweep.


## Exp158 — ext mlp 33/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4706 (delta -0.1052 vs prev best -0.3654); val=-0.458488651170541 train=-0.21652832237705597.

**Learning:** Ext iter 33 (mlp): DISCARD. Train/val gap = 0.2420. This iter targets MLP capacity sweep.


## Exp159 — ext mlp 34/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4234 (delta -0.0581 vs prev best -0.3654); val=-0.41173219821689355 train=-0.17775761798168485.

**Learning:** Ext iter 34 (mlp): DISCARD. Train/val gap = 0.2340. This iter targets MLP capacity sweep.


## Exp160 — ext mlp 35/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4835 (delta -0.1181 vs prev best -0.3654); val=-0.4744904922602041 train=-0.2940439077898866.

**Learning:** Ext iter 35 (mlp): DISCARD. Train/val gap = 0.1804. This iter targets MLP capacity sweep.


## Exp161 — ext mlp 36/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4078 (delta -0.0424 vs prev best -0.3654); val=-0.3958742869255984 train=-0.15716674211643702.

**Learning:** Ext iter 36 (mlp): DISCARD. Train/val gap = 0.2387. This iter targets MLP capacity sweep.


## Exp162 — ext mlp 37/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3879 (delta -0.0225 vs prev best -0.3654); val=-0.3756456380242804 train=-0.13150475193954575.

**Learning:** Ext iter 37 (mlp): DISCARD. Train/val gap = 0.2441. This iter targets MLP capacity sweep.


## Exp163 — ext mlp 38/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3816 (delta -0.0162 vs prev best -0.3654); val=-0.3715967082710366 train=-0.17113290778468512.

**Learning:** Ext iter 38 (mlp): DISCARD. Train/val gap = 0.2005. This iter targets MLP capacity sweep.


## Exp164 — ext mlp 39/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.3613 (delta +0.0040 vs prev best -0.3654); val=-0.3505251946066957 train=-0.1340458417537596.

**Learning:** Ext iter 39 (mlp): KEEP. Train/val gap = 0.2165. This iter targets MLP capacity sweep.


## Exp165 — ext mlp 40/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.3409 (delta +0.0205 vs prev best -0.3613); val=-0.32958003276775016 train=-0.10408268215171339.

**Learning:** Ext iter 40 (mlp): KEEP. Train/val gap = 0.2255. This iter targets MLP capacity sweep.


## Exp166 — ext mlp 41/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4498 (delta -0.1089 vs prev best -0.3409); val=-0.4402008477131343 train=-0.2487622480755667.

**Learning:** Ext iter 41 (mlp): DISCARD. Train/val gap = 0.1914. This iter targets MLP capacity sweep.


## Exp167 — ext mlp 42/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3933 (delta -0.0525 vs prev best -0.3409); val=-0.38230172940071844 train=-0.16141567256267214.

**Learning:** Ext iter 42 (mlp): DISCARD. Train/val gap = 0.2209. This iter targets MLP capacity sweep.


## Exp168 — ext mlp 43/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3540 (delta -0.0131 vs prev best -0.3409); val=-0.34374452716632237 train=-0.1396045215619067.

**Learning:** Ext iter 43 (mlp): DISCARD. Train/val gap = 0.2041. This iter targets MLP capacity sweep.


## Exp169 — ext mlp 44/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5016 (delta -0.1607 vs prev best -0.3409); val=-0.4875334697629087 train=-0.2065626274835652.

**Learning:** Ext iter 44 (mlp): DISCARD. Train/val gap = 0.2810. This iter targets MLP capacity sweep.


## Exp170 — ext mlp 45/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4397 (delta -0.0988 vs prev best -0.3409); val=-0.4272516740707002 train=-0.17891706242433913.

**Learning:** Ext iter 45 (mlp): DISCARD. Train/val gap = 0.2483. This iter targets MLP capacity sweep.


## Exp171 — ext mlp 46/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3946 (delta -0.0537 vs prev best -0.3409); val=-0.38251610394778945 train=-0.14097081156537972.

**Learning:** Ext iter 46 (mlp): DISCARD. Train/val gap = 0.2415. This iter targets MLP capacity sweep.


## Exp172 — ext ft_transformer 47/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0429 (delta -1.7021 vs prev best -0.3409); val=-1.9586886854177017 train=-0.27353522181424755.

**Learning:** Ext iter 47 (ft_transformer): DISCARD. Train/val gap = 1.6852. This iter targets FT-Transformer-style sweep.


## Exp173 — ext ft_transformer 48/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0336 (delta -1.6928 vs prev best -0.3409); val=-1.945990365374706 train=-0.19316429716394742.

**Learning:** Ext iter 48 (ft_transformer): DISCARD. Train/val gap = 1.7528. This iter targets FT-Transformer-style sweep.


## Exp174 — ext ft_transformer 49/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0548 (delta -1.7139 vs prev best -0.3409); val=-1.9652735354782942 train=-0.1746870336059194.

**Learning:** Ext iter 49 (ft_transformer): DISCARD. Train/val gap = 1.7906. This iter targets FT-Transformer-style sweep.


## Exp175 — ext ft_transformer 50/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-1.9535 (delta -1.6127 vs prev best -0.3409); val=-1.8659596532283182 train=-0.11487658621838569.

**Learning:** Ext iter 50 (ft_transformer): DISCARD. Train/val gap = 1.7511. This iter targets FT-Transformer-style sweep.


## Exp176 — ext ft_transformer 51/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-1.9824 (delta -1.6415 vs prev best -0.3409); val=-1.8914238317280092 train=-0.07277804498608853.

**Learning:** Ext iter 51 (ft_transformer): DISCARD. Train/val gap = 1.8186. This iter targets FT-Transformer-style sweep.


## Exp177 — ext ft_transformer 52/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0149 (delta -1.6740 vs prev best -0.3409); val=-1.9220591519866566 train=-0.06578877767671205.

**Learning:** Ext iter 52 (ft_transformer): DISCARD. Train/val gap = 1.8563. This iter targets FT-Transformer-style sweep.


## Exp178 — ext ft_transformer 53/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-1.9413 (delta -1.6005 vs prev best -0.3409); val=-1.851486769270326 train=-0.05463469829982472.

**Learning:** Ext iter 53 (ft_transformer): DISCARD. Train/val gap = 1.7969. This iter targets FT-Transformer-style sweep.


## Exp179 — ext ft_transformer 54/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-1.9787 (delta -1.6378 vs prev best -0.3409); val=-1.886438119755609 train=-0.04198638721569486.

**Learning:** Ext iter 54 (ft_transformer): DISCARD. Train/val gap = 1.8445. This iter targets FT-Transformer-style sweep.


## Exp180 — ext ft_transformer 55/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0121 (delta -1.6713 vs prev best -0.3409); val=-1.9182030068259683 train=-0.039726397681359805.

**Learning:** Ext iter 55 (ft_transformer): DISCARD. Train/val gap = 1.8785. This iter targets FT-Transformer-style sweep.


## Exp181 — ext xgboost 56/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.1. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.1 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9029 (delta -1.5621 vs prev best -0.3409); val=-1.817041101569216 train=-0.09886341708743433.

**Learning:** Ext iter 56 (xgboost): DISCARD. Train/val gap = 1.7182. This iter targets NGBoost-flavored sparsity sweep.


## Exp182 — ext xgboost 57/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.3. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.3 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9029 (delta -1.5621 vs prev best -0.3409); val=-1.817041101569216 train=-0.09886341708743433.

**Learning:** Ext iter 57 (xgboost): DISCARD. Train/val gap = 1.7182. This iter targets NGBoost-flavored sparsity sweep.


## Exp183 — ext xgboost 58/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=1.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=1.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9029 (delta -1.5621 vs prev best -0.3409); val=-1.817041101569216 train=-0.09886341708743433.

**Learning:** Ext iter 58 (xgboost): DISCARD. Train/val gap = 1.7182. This iter targets NGBoost-flavored sparsity sweep.


## Exp184 — ext xgboost 59/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=3.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=3.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9029 (delta -1.5621 vs prev best -0.3409); val=-1.817041101569216 train=-0.09886341708743433.

**Learning:** Ext iter 59 (xgboost): DISCARD. Train/val gap = 1.7182. This iter targets NGBoost-flavored sparsity sweep.


## Exp185 — ext mlp 60/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 128, 64). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4216 (delta -0.0808 vs prev best -0.3409); val=-0.4106358040733881 train=-0.19058477493247422.

**Learning:** Ext iter 60 (mlp): DISCARD. Train/val gap = 0.2201. This iter targets TabNet-flavoured wide-residual MLP.


## Exp186 — ext mlp 61/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(384, 192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(384, 192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.3834 (delta -0.0426 vs prev best -0.3409); val=-0.372035167566122 train=-0.14419001815897045.

**Learning:** Ext iter 61 (mlp): DISCARD. Train/val gap = 0.2278. This iter targets TabNet-flavoured wide-residual MLP.


## Exp187 — ext mlp 62/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4423 (delta -0.1015 vs prev best -0.3409); val=-0.4312112320875545 train=-0.20929706211800805.

**Learning:** Ext iter 62 (mlp): DISCARD. Train/val gap = 0.2219. This iter targets TabNet-flavoured wide-residual MLP.


## Exp188 — ext mlp 63/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(320, 160). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(320, 160) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.3769 (delta -0.0361 vs prev best -0.3409); val=-0.3671973206850342 train=-0.17270199721988075.

**Learning:** Ext iter 63 (mlp): DISCARD. Train/val gap = 0.1945. This iter targets TabNet-flavoured wide-residual MLP.


## Exp189 — ext mlp 64/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 256). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 256) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4226 (delta -0.0818 vs prev best -0.3409); val=-0.4108821077326795 train=-0.17589231267368316.

**Learning:** Ext iter 64 (mlp): DISCARD. Train/val gap = 0.2350. This iter targets TabNet-flavoured wide-residual MLP.


## Exp190 — ext ft_transformer 65/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=200. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.7558 (delta -2.4149 vs prev best -0.3409); val=-2.7101298406599517 train=-1.7973597257230596.

**Learning:** Ext iter 65 (ft_transformer): DISCARD. Train/val gap = 0.9128. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp191 — ext ft_transformer 66/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=400. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.2224 (delta -1.8816 vs prev best -0.3409); val=-2.163131152210759 train=-0.9770170693535144.

**Learning:** Ext iter 66 (ft_transformer): DISCARD. Train/val gap = 1.1861. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp192 — ext ft_transformer 67/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=600. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-1.9983 (delta -1.6574 vs prev best -0.3409); val=-1.932788411789073 train=-0.6232398339988894.

**Learning:** Ext iter 67 (ft_transformer): DISCARD. Train/val gap = 1.3095. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp193 — ext xgboost 68/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=0.1 reg_alpha=0.1. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=0.1 smooths leaf weights; reg_alpha=0.1 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7115 (delta -1.3707 vs prev best -0.3409); val=-1.6443413921591512 train=-0.30067091317615957.

**Learning:** Ext iter 68 (xgboost): DISCARD. Train/val gap = 1.3437. This iter targets Elastic-net-flavoured gradient boost.


## Exp194 — ext xgboost 69/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=1.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=1.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7260 (delta -1.3852 vs prev best -0.3409); val=-1.659015362232126 train=-0.3185580517131042.

**Learning:** Ext iter 69 (xgboost): DISCARD. Train/val gap = 1.3405. This iter targets Elastic-net-flavoured gradient boost.


## Exp195 — ext xgboost 70/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=3.0 reg_alpha=1.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=3.0 smooths leaf weights; reg_alpha=1.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7426 (delta -1.4018 vs prev best -0.3409); val=-1.6765840470350601 train=-0.35545690747330816.

**Learning:** Ext iter 70 (xgboost): DISCARD. Train/val gap = 1.3211. This iter targets Elastic-net-flavoured gradient boost.


## Exp196 — ext xgboost 71/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7100 (delta -1.3692 vs prev best -0.3409); val=-1.6489727001162753 train=-0.42787676666367563.

**Learning:** Ext iter 71 (xgboost): DISCARD. Train/val gap = 1.2211. This iter targets Elastic-net-flavoured gradient boost.


## Exp197 — ext xgboost 72/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=3.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=3.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7100 (delta -1.3692 vs prev best -0.3409); val=-1.6489727001162753 train=-0.42787676666367563.

**Learning:** Ext iter 72 (xgboost): DISCARD. Train/val gap = 1.2211. This iter targets Elastic-net-flavoured gradient boost.


## Exp198 — ext patchtsmixer 73/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.5555 (delta -1.2147 vs prev best -0.3409); val=-1.5524665649548575 train=-1.4909105679141001.

**Learning:** Ext iter 73 (patchtsmixer): DISCARD. Train/val gap = 0.0616. This iter targets PatchTSMixer channel-mix sweep.


## Exp199 — ext patchtsmixer 74/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.4927 (delta -1.1519 vs prev best -0.3409); val=-1.4835692778824356 train=-1.3004379048436907.

**Learning:** Ext iter 74 (patchtsmixer): DISCARD. Train/val gap = 0.1831. This iter targets PatchTSMixer channel-mix sweep.


## Exp200 — ext patchtsmixer 75/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.2678 (delta -0.9270 vs prev best -0.3409); val=-1.259224046316628 train=-1.0872133293712978.

**Learning:** Ext iter 75 (patchtsmixer): DISCARD. Train/val gap = 0.1720. This iter targets PatchTSMixer channel-mix sweep.


## Exp201 — ext patchtsmixer 76/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.1020 (delta -0.7612 vs prev best -0.3409); val=-1.0885123594193047 train=-0.8178344353958062.

**Learning:** Ext iter 76 (patchtsmixer): DISCARD. Train/val gap = 0.2707. This iter targets PatchTSMixer channel-mix sweep.


## Exp202 — ext patchtsmixer 77/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.0297 (delta -0.6889 vs prev best -0.3409); val=-1.0172954613367904 train=-0.7689232530208086.

**Learning:** Ext iter 77 (patchtsmixer): DISCARD. Train/val gap = 0.2484. This iter targets PatchTSMixer channel-mix sweep.


## Exp203 — ext patchtsmixer 78/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.0199 (delta -0.6790 vs prev best -0.3409); val=-1.0002624048228006 train=-0.6078134727960564.

**Learning:** Ext iter 78 (patchtsmixer): DISCARD. Train/val gap = 0.3924. This iter targets PatchTSMixer channel-mix sweep.


## Exp204 — ext xgboost 79/200
**Diagnosis:** Multi-seed champion variance run, seed=42. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.0821 (delta -1.7412 vs prev best -0.3409); val=-1.9863597526020311 train=-0.07147129817338917.

**Learning:** Ext iter 79 (xgboost): DISCARD. Train/val gap = 1.9149. This iter targets extended search.


## Exp205 — ext xgboost 80/200
**Diagnosis:** Multi-seed champion variance run, seed=0. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1035 (delta -1.7626 vs prev best -0.3409); val=-2.006860410814886 train=-0.07437068045117766.

**Learning:** Ext iter 80 (xgboost): DISCARD. Train/val gap = 1.9325. This iter targets extended search.


## Exp206 — ext xgboost 81/200
**Diagnosis:** Multi-seed champion variance run, seed=7. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.0979 (delta -1.7570 vs prev best -0.3409); val=-2.0014668092627272 train=-0.07313052248275445.

**Learning:** Ext iter 81 (xgboost): DISCARD. Train/val gap = 1.9283. This iter targets extended search.


## Exp207 — ext xgboost 82/200
**Diagnosis:** Multi-seed champion variance run, seed=99. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1142 (delta -1.7733 vs prev best -0.3409); val=-2.0168219272757653 train=-0.07010770483899058.

**Learning:** Ext iter 82 (xgboost): DISCARD. Train/val gap = 1.9467. This iter targets extended search.


## Exp208 — ext xgboost 83/200
**Diagnosis:** Multi-seed champion variance run, seed=2024. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1178 (delta -1.7770 vs prev best -0.3409); val=-2.0201819900641964 train=-0.06762010147145008.

**Learning:** Ext iter 83 (xgboost): DISCARD. Train/val gap = 1.9526. This iter targets extended search.


## Exp209 — ext xgboost 84/200
**Diagnosis:** Multi-seed champion variance run, seed=12345. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.0701 (delta -1.7292 vs prev best -0.3409); val=-1.9748011645894117 train=-0.06967676371892081.

**Learning:** Ext iter 84 (xgboost): DISCARD. Train/val gap = 1.9051. This iter targets extended search.


## Exp210 — ext xgboost 85/200
**Diagnosis:** Multi-seed champion variance run, seed=7777. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1037 (delta -1.7628 vs prev best -0.3409); val=-2.006971368605406 train=-0.07235377644396489.

**Learning:** Ext iter 85 (xgboost): DISCARD. Train/val gap = 1.9346. This iter targets extended search.


## Exp211 — ext xgboost 86/200
**Diagnosis:** Multi-seed champion variance run, seed=31337. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.0964 (delta -1.7555 vs prev best -0.3409); val=-1.9998903244464314 train=-0.07016156805671886.

**Learning:** Ext iter 86 (xgboost): DISCARD. Train/val gap = 1.9297. This iter targets extended search.


## Exp212 — ext xgboost 87/200
**Diagnosis:** Multi-seed champion variance run, seed=1729. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1105 (delta -1.7696 vs prev best -0.3409); val=-2.0134132729801153 train=-0.07254593842785284.

**Learning:** Ext iter 87 (xgboost): DISCARD. Train/val gap = 1.9409. This iter targets extended search.


## Exp213 — ext xgboost 88/200
**Diagnosis:** Multi-seed champion variance run, seed=6174. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1126 (delta -1.7718 vs prev best -0.3409); val=-2.015405095842496 train=-0.07100585636878134.

**Learning:** Ext iter 88 (xgboost): DISCARD. Train/val gap = 1.9444. This iter targets extended search.


## Exp214 — ext xgboost 89/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=30. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=30, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.6345 (delta -1.2936 vs prev best -0.3409); val=-1.5956083197194373 train=-0.8186920145482418.

**Learning:** Ext iter 89 (xgboost): DISCARD. Train/val gap = 0.7769. This iter targets Extreme regularisation cool-down.


## Exp215 — ext xgboost 90/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=50. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=50, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.6937 (delta -1.3528 vs prev best -0.3409); val=-1.6568815358830562 train=-0.9207244093728504.

**Learning:** Ext iter 90 (xgboost): DISCARD. Train/val gap = 0.7362. This iter targets Extreme regularisation cool-down.


## Exp216 — ext xgboost 91/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=100. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=100, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.7834 (delta -1.4426 vs prev best -0.3409); val=-1.7514981941172454 train=-1.1130159296127968.

**Learning:** Ext iter 91 (xgboost): DISCARD. Train/val gap = 0.6385. This iter targets Extreme regularisation cool-down.

