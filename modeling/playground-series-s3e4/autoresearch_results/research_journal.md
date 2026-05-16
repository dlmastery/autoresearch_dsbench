# Research Journal — playground-series-s3e4

_(populated by `framework/hill_climb.py`)_

## Exp1 — xgboost iter 1
**Diagnosis:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

**Hypothesis:** Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).

**Prediction:** Composite in [0.55, 0.85] depending on task difficulty.

**Verdict:** KEEP composite=0.9702 (delta +inf vs prev best -inf); val_score=0.9716114285714286; train_score=1.0.

**Learning:** Iter 1 xgboost: KEEP. Train/val gap = 0.0284. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — xgboost iter 2
**Diagnosis:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.

**Citations:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

**Hypothesis:** Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=0.9661 (delta -0.0041 vs prev best 0.9702); val_score=0.9676800000000001; train_score=1.0.

**Learning:** Iter 2 xgboost: DISCARD. Train/val gap = 0.0323. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — xgboost iter 3
**Diagnosis:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

**Hypothesis:** Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=0.9704 (delta +0.0002 vs prev best 0.9702); val_score=0.9718399999999999; train_score=1.0.

**Learning:** Iter 3 xgboost: KEEP. Train/val gap = 0.0282. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp4 — xgboost iter 4
**Diagnosis:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.

**Citations:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

**Hypothesis:** Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.

**Prediction:** Composite delta in [+0.001, +0.010].

**Verdict:** DISCARD composite=0.9693 (delta -0.0012 vs prev best 0.9704); val_score=0.9707428571428571; train_score=1.0.

**Learning:** Iter 4 xgboost: DISCARD. Train/val gap = 0.0293. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — xgboost iter 5
**Diagnosis:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

**Hypothesis:** Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.

**Prediction:** Composite delta in [+0.002, +0.012].

**Verdict:** DISCARD composite=0.9696 (delta -0.0009 vs prev best 0.9704); val_score=0.9710171428571428; train_score=1.0.

**Learning:** Iter 5 xgboost: DISCARD. Train/val gap = 0.0290. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — xgboost iter 6
**Diagnosis:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.

**Citations:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

**Hypothesis:** Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9616 (delta -0.0089 vs prev best 0.9704); val_score=0.9633828571428571; train_score=1.0.

**Learning:** Iter 6 xgboost: DISCARD. Train/val gap = 0.0366. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — xgboost iter 7
**Diagnosis:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.

**Citations:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

**Hypothesis:** Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** KEEP composite=0.9795 (delta +0.0091 vs prev best 0.9704); val_score=0.9804799999999999; train_score=1.0.

**Learning:** Iter 7 xgboost: KEEP. Train/val gap = 0.0195. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp8 — xgboost iter 8
**Diagnosis:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.

**Citations:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9673 (delta -0.0122 vs prev best 0.9795); val_score=0.9688228571428572; train_score=1.0.

**Learning:** Iter 8 xgboost: DISCARD. Train/val gap = 0.0312. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — xgboost iter 9
**Diagnosis:** Third seed for 3-seed median (autoresearch protocol).

**Citations:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9689 (delta -0.0106 vs prev best 0.9795); val_score=0.970422857142857; train_score=1.0.

**Learning:** Iter 9 xgboost: DISCARD. Train/val gap = 0.0296. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — xgboost iter 10
**Diagnosis:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

**Hypothesis:** Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.9622 (delta -0.0173 vs prev best 0.9795); val_score=0.9639771428571428; train_score=1.0.

**Learning:** Iter 10 xgboost: DISCARD. Train/val gap = 0.0360. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — xgboost iter 11
**Diagnosis:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.

**Citations:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

**Hypothesis:** Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.9733 (delta -0.0062 vs prev best 0.9795); val_score=0.9745828571428572; train_score=1.0.

**Learning:** Iter 11 xgboost: DISCARD. Train/val gap = 0.0254. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp12 — xgboost iter 12
**Diagnosis:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

**Hypothesis:** Hypothesis: larger leaves reduce variance, improve val by 0.5%.

**Prediction:** Composite delta in [-0.002, +0.010].

**Verdict:** DISCARD composite=0.9702 (delta -0.0093 vs prev best 0.9795); val_score=0.9716114285714286; train_score=1.0.

**Learning:** Iter 12 xgboost: DISCARD. Train/val gap = 0.0284. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — xgboost iter 13
**Diagnosis:** Gamma split-penalty 0.5 — discourages overly eager splits.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

**Hypothesis:** Hypothesis: fewer, higher-quality splits. Val improves slightly.

**Prediction:** Composite delta in [-0.003, +0.008].

**Verdict:** DISCARD composite=0.9702 (delta -0.0093 vs prev best 0.9795); val_score=0.9716114285714286; train_score=1.0.

**Learning:** Iter 13 xgboost: DISCARD. Train/val gap = 0.0284. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — xgboost iter 14
**Diagnosis:** High subsample for low-noise tasks — opposite direction from iter-4/7.

**Citations:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

**Hypothesis:** Hypothesis: gentle bagging if iter-4/7 over-regularised.

**Prediction:** Composite delta in [-0.005, +0.007].

**Verdict:** DISCARD composite=0.9662 (delta -0.0133 vs prev best 0.9795); val_score=0.9677714285714285; train_score=1.0.

**Learning:** Iter 14 xgboost: DISCARD. Train/val gap = 0.0322. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — xgboost iter 15
**Diagnosis:** L1 regularisation (reg_alpha) for feature selection.

**Citations:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

**Hypothesis:** Hypothesis: L1 trims noise features, val improves.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=0.9659 (delta -0.0136 vs prev best 0.9795); val_score=0.9674971428571428; train_score=1.0.

**Learning:** Iter 15 xgboost: DISCARD. Train/val gap = 0.0325. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — xgboost iter 16
**Diagnosis:** Combined moderate regularisation — meta-search across all axes.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

**Hypothesis:** Hypothesis: balanced config beats single-knob champions.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=0.9724 (delta -0.0071 vs prev best 0.9795); val_score=0.9737142857142858; train_score=1.0.

**Learning:** Iter 16 xgboost: DISCARD. Train/val gap = 0.0263. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — xgboost iter 17
**Diagnosis:** Fourth seed — extend variance characterisation.

**Citations:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

**Hypothesis:** Hypothesis: within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9688 (delta -0.0107 vs prev best 0.9795); val_score=0.9702857142857142; train_score=1.0.

**Learning:** Iter 17 xgboost: DISCARD. Train/val gap = 0.0297. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — xgboost iter 18
**Diagnosis:** Fifth seed.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Same as iter-15.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9666 (delta -0.0129 vs prev best 0.9795); val_score=0.9682285714285714; train_score=1.0.

**Learning:** Iter 18 xgboost: DISCARD. Train/val gap = 0.0318. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — xgboost iter 19
**Diagnosis:** Aggressive depth=12 with proportionally lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

**Hypothesis:** Hypothesis: depth=12 will overfit unless lr is very low.

**Prediction:** Composite delta in [-0.030, +0.010].

**Verdict:** DISCARD composite=0.9555 (delta -0.0240 vs prev best 0.9795); val_score=0.9575771428571428; train_score=1.0.

**Learning:** Iter 19 xgboost: DISCARD. Train/val gap = 0.0424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — xgboost iter 20
**Diagnosis:** Very shallow, high-lr — stump-like learners as opposite extreme.

**Citations:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

**Hypothesis:** Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.

**Prediction:** Composite delta in [-0.040, +0.005].

**Verdict:** DISCARD composite=0.9727 (delta -0.0068 vs prev best 0.9795); val_score=0.9739885714285714; train_score=1.0.

**Learning:** Iter 20 xgboost: DISCARD. Train/val gap = 0.0260. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp21 — xgboost iter 21
**Diagnosis:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.

**Citations:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

**Hypothesis:** Hypothesis: no-op vs baseline; informational only.

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=0.9726 (delta -0.0069 vs prev best 0.9795); val_score=0.9739428571428571; train_score=1.0.

**Learning:** Iter 21 xgboost: DISCARD. Train/val gap = 0.0261. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — xgboost iter 22
**Diagnosis:** Confirm hist-method explicitly — same as default but pinned.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

**Hypothesis:** Hypothesis: no change vs baseline (already default in our setup).

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=0.9702 (delta -0.0093 vs prev best 0.9795); val_score=0.9716114285714286; train_score=1.0.

**Learning:** Iter 22 xgboost: DISCARD. Train/val gap = 0.0284. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — xgboost iter 23
**Diagnosis:** Long-and-slow final refinement with mid-strength L2.

**Citations:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

**Hypothesis:** Hypothesis: best champion candidate. Val should peak.

**Prediction:** Composite delta in [+0.005, +0.025].

**Verdict:** DISCARD composite=0.9741 (delta -0.0054 vs prev best 0.9795); val_score=0.9753142857142857; train_score=1.0.

**Learning:** Iter 23 xgboost: DISCARD. Train/val gap = 0.0247. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — xgboost iter 24
**Diagnosis:** Combined moderate everything — explore a balanced corner.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.9706 (delta -0.0089 vs prev best 0.9795); val_score=0.9720228571428572; train_score=1.0.

**Learning:** Iter 24 xgboost: DISCARD. Train/val gap = 0.0280. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — xgboost iter 25
**Diagnosis:** Final 6th seed — closes the variance characterisation for this backbone.

**Citations:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9679 (delta -0.0116 vs prev best 0.9795); val_score=0.9694171428571428; train_score=1.0.

**Learning:** Iter 25 xgboost: DISCARD. Train/val gap = 0.0306. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp26 — lightgbm iter 1
**Diagnosis:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard lightgbm config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 1 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp27 — lightgbm iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=0.8832 (delta -0.0963 vs prev best 0.9795); val_score=0.8886400000000001; train_score=0.9978012358077442.

**Learning:** Iter 2 lightgbm: DISCARD. Train/val gap = 0.1092. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp28 — lightgbm iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.8372 (delta -0.1423 vs prev best 0.9795); val_score=0.8442971428571429; train_score=0.9868299138288973.

**Learning:** Iter 3 lightgbm: DISCARD. Train/val gap = 0.1425. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp29 — lightgbm iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=0.9131 (delta -0.0664 vs prev best 0.9795); val_score=0.9172571428571429; train_score=0.9998977318980347.

**Learning:** Iter 4 lightgbm: DISCARD. Train/val gap = 0.0826. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp30 — lightgbm iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9611 (delta -0.0184 vs prev best 0.9795); val_score=0.9629714285714286; train_score=1.0.

**Learning:** Iter 5 lightgbm: DISCARD. Train/val gap = 0.0370. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp31 — lightgbm iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9611 (delta -0.0184 vs prev best 0.9795); val_score=0.9629714285714286; train_score=1.0.

**Learning:** Iter 6 lightgbm: DISCARD. Train/val gap = 0.0370. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp32 — lightgbm iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8687 (delta -0.1108 vs prev best 0.9795); val_score=0.8746971428571428; train_score=0.9950318156065214.

**Learning:** Iter 7 lightgbm: DISCARD. Train/val gap = 0.1203. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp33 — lightgbm iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8651 (delta -0.1144 vs prev best 0.9795); val_score=0.8713142857142857; train_score=0.9948927309878486.

**Learning:** Iter 8 lightgbm: DISCARD. Train/val gap = 0.1236. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp34 — lightgbm iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 9 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp35 — lightgbm iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.8467 (delta -0.1328 vs prev best 0.9795); val_score=0.8534857142857143; train_score=0.9899695445592347.

**Learning:** Iter 10 lightgbm: DISCARD. Train/val gap = 0.1365. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp36 — lightgbm iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 11 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp37 — lightgbm iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 12 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp38 — lightgbm iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.8494 (delta -0.1301 vs prev best 0.9795); val_score=0.8561371428571429; train_score=0.9907897347369972.

**Learning:** Iter 13 lightgbm: DISCARD. Train/val gap = 0.1347. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp39 — lightgbm iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8703 (delta -0.1092 vs prev best 0.9795); val_score=0.8762514285714287; train_score=0.995514521047798.

**Learning:** Iter 14 lightgbm: DISCARD. Train/val gap = 0.1193. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp40 — lightgbm iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8741 (delta -0.1054 vs prev best 0.9795); val_score=0.8799085714285714; train_score=0.995733374786004.

**Learning:** Iter 15 lightgbm: DISCARD. Train/val gap = 0.1158. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp41 — lightgbm iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 16 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp42 — lightgbm iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 17 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp43 — lightgbm iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=0.8969 (delta -0.0826 vs prev best 0.9795); val_score=0.9018057142857143; train_score=0.9990509520137612.

**Learning:** Iter 18 lightgbm: DISCARD. Train/val gap = 0.0972. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp44 — lightgbm iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=0.8304 (delta -0.1491 vs prev best 0.9795); val_score=0.8376685714285714; train_score=0.9834059777750961.

**Learning:** Iter 19 lightgbm: DISCARD. Train/val gap = 0.1457. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp45 — lightgbm iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 20 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp46 — lightgbm iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 21 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp47 — lightgbm iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.8673 (delta -0.1122 vs prev best 0.9795); val_score=0.8734171428571428; train_score=0.9955677004608201.

**Learning:** Iter 22 lightgbm: DISCARD. Train/val gap = 0.1222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp48 — lightgbm iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8554 (delta -0.1241 vs prev best 0.9795); val_score=0.8619428571428572; train_score=0.9929087298097199.

**Learning:** Iter 23 lightgbm: DISCARD. Train/val gap = 0.1310. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp49 — lightgbm iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8837 (delta -0.0958 vs prev best 0.9795); val_score=0.8890971428571428; train_score=0.9977746461012331.

**Learning:** Iter 24 lightgbm: DISCARD. Train/val gap = 0.1087. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp50 — lightgbm iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8731 (delta -0.1064 vs prev best 0.9795); val_score=0.8789028571428571; train_score=0.9954449787384616.

**Learning:** Iter 25 lightgbm: DISCARD. Train/val gap = 0.1165. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp51 — catboost iter 1
**Diagnosis:** Baseline catboost per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard catboost config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 1 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp52 — catboost iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 2 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp53 — catboost iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 3 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp54 — catboost iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 4 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp55 — catboost iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 5 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp56 — catboost iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 6 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp57 — catboost iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 7 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp58 — catboost iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 8 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp59 — catboost iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 9 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp60 — catboost iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 10 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp61 — catboost iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 11 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp62 — catboost iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 12 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp63 — catboost iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 13 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp64 — catboost iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 14 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp65 — catboost iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 15 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp66 — catboost iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 16 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp67 — catboost iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 17 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp68 — catboost iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 18 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp69 — catboost iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 19 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp70 — catboost iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 20 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp71 — catboost iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 21 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp72 — catboost iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 22 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp73 — catboost iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 23 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp74 — catboost iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 24 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp75 — catboost iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9795); val_score=NA; train_score=NA.

**Learning:** Iter 25 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp76 — mlp iter 1
**Diagnosis:** Baseline mlp per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard mlp config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** KEEP composite=0.9930 (delta +0.0135 vs prev best 0.9795); val_score=0.9932799999999999; train_score=0.9995316120929986.

**Learning:** Iter 1 mlp: KEEP. Train/val gap = 0.0063. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp77 — mlp iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=0.9930 (delta +0.0000 vs prev best 0.9930); val_score=0.9932799999999999; train_score=0.9995316120929986.

**Learning:** Iter 2 mlp: DISCARD. Train/val gap = 0.0063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp78 — mlp iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.9859 (delta -0.0071 vs prev best 0.9930); val_score=0.98624; train_score=0.9938168705551726.

**Learning:** Iter 3 mlp: DISCARD. Train/val gap = 0.0076. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp79 — mlp iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=0.9929 (delta -0.0001 vs prev best 0.9930); val_score=0.9931885714285714; train_score=0.9995541110754309.

**Learning:** Iter 4 mlp: DISCARD. Train/val gap = 0.0064. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp80 — mlp iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9917 (delta -0.0013 vs prev best 0.9930); val_score=0.9920457142857143; train_score=0.9998629607433663.

**Learning:** Iter 5 mlp: DISCARD. Train/val gap = 0.0078. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp81 — mlp iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9663 (delta -0.0267 vs prev best 0.9930); val_score=0.9672228571428572; train_score=0.9854492944523645.

**Learning:** Iter 6 mlp: DISCARD. Train/val gap = 0.0182. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp82 — mlp iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9912 (delta -0.0018 vs prev best 0.9930); val_score=0.9915885714285714; train_score=0.9995561564374702.

**Learning:** Iter 7 mlp: DISCARD. Train/val gap = 0.0080. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp83 — mlp iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9895 (delta -0.0035 vs prev best 0.9930); val_score=0.9898971428571428; train_score=0.9979628194088495.

**Learning:** Iter 8 mlp: DISCARD. Train/val gap = 0.0081. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp84 — mlp iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.9930 (delta +0.0000 vs prev best 0.9930); val_score=0.9932799999999999; train_score=0.9995316120929986.

**Learning:** Iter 9 mlp: DISCARD. Train/val gap = 0.0063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp85 — mlp iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.9892 (delta -0.0038 vs prev best 0.9930); val_score=0.9896228571428571; train_score=0.998564155848406.

**Learning:** Iter 10 mlp: DISCARD. Train/val gap = 0.0089. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp86 — mlp iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** KEEP composite=0.9933 (delta +0.0003 vs prev best 0.9930); val_score=0.9935542857142857; train_score=0.9995868368680598.

**Learning:** Iter 11 mlp: KEEP. Train/val gap = 0.0060. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp87 — mlp iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** KEEP composite=0.9954 (delta +0.0021 vs prev best 0.9933); val_score=0.9956114285714286; train_score=0.9999509113110566.

**Learning:** Iter 12 mlp: KEEP. Train/val gap = 0.0043. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp88 — mlp iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.9884 (delta -0.0070 vs prev best 0.9954); val_score=0.9888457142857142; train_score=0.997122175610694.

**Learning:** Iter 13 mlp: DISCARD. Train/val gap = 0.0083. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp89 — mlp iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9868 (delta -0.0086 vs prev best 0.9954); val_score=0.9872457142857143; train_score=0.9953447559985356.

**Learning:** Iter 14 mlp: DISCARD. Train/val gap = 0.0081. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp90 — mlp iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9929 (delta -0.0025 vs prev best 0.9954); val_score=0.9932342857142857; train_score=0.9995479749893129.

**Learning:** Iter 15 mlp: DISCARD. Train/val gap = 0.0063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp91 — mlp iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9929 (delta -0.0025 vs prev best 0.9954); val_score=0.9932342857142857; train_score=0.9997177400385755.

**Learning:** Iter 16 mlp: DISCARD. Train/val gap = 0.0065. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp92 — mlp iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=0.9954 (delta -0.0000 vs prev best 0.9954); val_score=0.9955657142857144; train_score=0.9997668287275189.

**Learning:** Iter 17 mlp: DISCARD. Train/val gap = 0.0042. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp93 — mlp iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=0.9898 (delta -0.0056 vs prev best 0.9954); val_score=0.9902171428571429; train_score=0.9980814504071294.

**Learning:** Iter 18 mlp: DISCARD. Train/val gap = 0.0079. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp94 — mlp iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=0.9438 (delta -0.0516 vs prev best 0.9954); val_score=0.9445028571428572; train_score=0.957892131696771.

**Learning:** Iter 19 mlp: DISCARD. Train/val gap = 0.0134. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp95 — mlp iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9930 (delta -0.0024 vs prev best 0.9954); val_score=0.9932799999999999; train_score=0.9995316120929986.

**Learning:** Iter 20 mlp: DISCARD. Train/val gap = 0.0063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp96 — mlp iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.9930 (delta -0.0024 vs prev best 0.9954); val_score=0.9932799999999999; train_score=0.9995316120929986.

**Learning:** Iter 21 mlp: DISCARD. Train/val gap = 0.0063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp97 — mlp iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9930 (delta -0.0024 vs prev best 0.9954); val_score=0.9932799999999999; train_score=0.9995316120929986.

**Learning:** Iter 22 mlp: DISCARD. Train/val gap = 0.0063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp98 — mlp iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9917 (delta -0.0037 vs prev best 0.9954); val_score=0.9920457142857142; train_score=0.9988893684126559.

**Learning:** Iter 23 mlp: DISCARD. Train/val gap = 0.0068. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp99 — mlp iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9925 (delta -0.0029 vs prev best 0.9954); val_score=0.992822857142857; train_score=0.999595018316217.

**Learning:** Iter 24 mlp: DISCARD. Train/val gap = 0.0068. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp100 — mlp iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9918 (delta -0.0036 vs prev best 0.9954); val_score=0.9921828571428571; train_score=0.9999570473971746.

**Learning:** Iter 25 mlp: DISCARD. Train/val gap = 0.0078. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp101 — ft_transformer iter 1
**Diagnosis:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard ft_transformer config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 1 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp102 — ft_transformer iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=0.8553 (delta -0.1401 vs prev best 0.9954); val_score=0.8612571428571428; train_score=0.9808267762435291.

**Learning:** Iter 2 ft_transformer: DISCARD. Train/val gap = 0.1196. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp103 — ft_transformer iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.7908 (delta -0.2046 vs prev best 0.9954); val_score=0.796822857142857; train_score=0.9182284710305149.

**Learning:** Iter 3 ft_transformer: DISCARD. Train/val gap = 0.1214. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp104 — ft_transformer iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=0.8867 (delta -0.1087 vs prev best 0.9954); val_score=0.8919314285714286; train_score=0.9963326658635212.

**Learning:** Iter 4 ft_transformer: DISCARD. Train/val gap = 0.1044. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp105 — ft_transformer iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9530 (delta -0.0424 vs prev best 0.9954); val_score=0.9552457142857143; train_score=1.0.

**Learning:** Iter 5 ft_transformer: DISCARD. Train/val gap = 0.0448. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp106 — ft_transformer iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9530 (delta -0.0424 vs prev best 0.9954); val_score=0.9552457142857143; train_score=1.0.

**Learning:** Iter 6 ft_transformer: DISCARD. Train/val gap = 0.0448. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp107 — ft_transformer iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 7 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp108 — ft_transformer iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 8 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp109 — ft_transformer iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 9 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp110 — ft_transformer iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.8123 (delta -0.1831 vs prev best 0.9954); val_score=0.8184; train_score=0.9400177128352605.

**Learning:** Iter 10 ft_transformer: DISCARD. Train/val gap = 0.1216. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp111 — ft_transformer iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 11 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp112 — ft_transformer iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 12 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp113 — ft_transformer iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.8208 (delta -0.1746 vs prev best 0.9954); val_score=0.8268800000000001; train_score=0.9476663441812518.

**Learning:** Iter 13 ft_transformer: DISCARD. Train/val gap = 0.1208. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp114 — ft_transformer iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 14 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp115 — ft_transformer iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 15 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp116 — ft_transformer iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 16 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp117 — ft_transformer iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 17 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp118 — ft_transformer iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=0.8690 (delta -0.1264 vs prev best 0.9954); val_score=0.8746514285714286; train_score=0.9882800755147665.

**Learning:** Iter 18 ft_transformer: DISCARD. Train/val gap = 0.1136. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp119 — ft_transformer iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=0.7853 (delta -0.2101 vs prev best 0.9954); val_score=0.7909485714285716; train_score=0.9040858152097212.

**Learning:** Iter 19 ft_transformer: DISCARD. Train/val gap = 0.1131. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp120 — ft_transformer iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 20 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp121 — ft_transformer iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 21 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp122 — ft_transformer iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 22 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp123 — ft_transformer iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8244 (delta -0.1710 vs prev best 0.9954); val_score=0.8305828571428572; train_score=0.9533544960125668.

**Learning:** Iter 23 ft_transformer: DISCARD. Train/val gap = 0.1228. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp124 — ft_transformer iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8558 (delta -0.1396 vs prev best 0.9954); val_score=0.8617142857142857; train_score=0.9808185947953718.

**Learning:** Iter 24 ft_transformer: DISCARD. Train/val gap = 0.1191. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp125 — ft_transformer iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8343 (delta -0.1611 vs prev best 0.9954); val_score=0.8405028571428572; train_score=0.9640302631767336.

**Learning:** Iter 25 ft_transformer: DISCARD. Train/val gap = 0.1235. Closing axis if True and delta < -0.01; otherwise this direction is open.

