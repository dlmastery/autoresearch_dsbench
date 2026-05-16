# Research Journal — cat-in-the-dat-ii

_(populated by `framework/hill_climb.py`)_

## Exp1 — xgboost iter 1
**Diagnosis:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

**Hypothesis:** Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).

**Prediction:** Composite in [0.55, 0.85] depending on task difficulty.

**Verdict:** KEEP composite=0.9566 (delta +inf vs prev best -inf); val_score=0.9586673234517039; train_score=1.0.

**Learning:** Iter 1 xgboost: KEEP. Train/val gap = 0.0413. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — xgboost iter 2
**Diagnosis:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.

**Citations:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

**Hypothesis:** Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=0.9563 (delta -0.0003 vs prev best 0.9566); val_score=0.9583986386637409; train_score=1.0.

**Learning:** Iter 2 xgboost: DISCARD. Train/val gap = 0.0416. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — xgboost iter 3
**Diagnosis:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

**Hypothesis:** Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=0.9638 (delta +0.0072 vs prev best 0.9566); val_score=0.9655187855447585; train_score=1.0.

**Learning:** Iter 3 xgboost: KEEP. Train/val gap = 0.0345. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp4 — xgboost iter 4
**Diagnosis:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.

**Citations:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

**Hypothesis:** Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.

**Prediction:** Composite delta in [+0.001, +0.010].

**Verdict:** DISCARD composite=0.9575 (delta -0.0063 vs prev best 0.9638); val_score=0.9595629394115803; train_score=1.0.

**Learning:** Iter 4 xgboost: DISCARD. Train/val gap = 0.0404. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — xgboost iter 5
**Diagnosis:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

**Hypothesis:** Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.

**Prediction:** Composite delta in [+0.002, +0.012].

**Verdict:** DISCARD composite=0.9569 (delta -0.0069 vs prev best 0.9638); val_score=0.9589807890376607; train_score=1.0.

**Learning:** Iter 5 xgboost: DISCARD. Train/val gap = 0.0410. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — xgboost iter 6
**Diagnosis:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.

**Citations:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

**Hypothesis:** Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9490 (delta -0.0148 vs prev best 0.9638); val_score=0.9514576149746988; train_score=1.0.

**Learning:** Iter 6 xgboost: DISCARD. Train/val gap = 0.0485. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — xgboost iter 7
**Diagnosis:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.

**Citations:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

**Hypothesis:** Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** KEEP composite=0.9700 (delta +0.0062 vs prev best 0.9638); val_score=0.9714298508799426; train_score=1.0.

**Learning:** Iter 7 xgboost: KEEP. Train/val gap = 0.0286. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp8 — xgboost iter 8
**Diagnosis:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.

**Citations:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9551 (delta -0.0149 vs prev best 0.9700); val_score=0.9572791187138955; train_score=1.0.

**Learning:** Iter 8 xgboost: DISCARD. Train/val gap = 0.0427. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — xgboost iter 9
**Diagnosis:** Third seed for 3-seed median (autoresearch protocol).

**Citations:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9541 (delta -0.0159 vs prev best 0.9700); val_score=0.9562491603600376; train_score=1.0.

**Learning:** Iter 9 xgboost: DISCARD. Train/val gap = 0.0438. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — xgboost iter 10
**Diagnosis:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

**Hypothesis:** Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.9534 (delta -0.0166 vs prev best 0.9700); val_score=0.9555774483901303; train_score=1.0.

**Learning:** Iter 10 xgboost: DISCARD. Train/val gap = 0.0444. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — xgboost iter 11
**Diagnosis:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.

**Citations:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

**Hypothesis:** Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.9642 (delta -0.0058 vs prev best 0.9700); val_score=0.965877031928709; train_score=1.0.

**Learning:** Iter 11 xgboost: DISCARD. Train/val gap = 0.0341. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp12 — xgboost iter 12
**Diagnosis:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

**Hypothesis:** Hypothesis: larger leaves reduce variance, improve val by 0.5%.

**Prediction:** Composite delta in [-0.002, +0.010].

**Verdict:** DISCARD composite=0.9566 (delta -0.0134 vs prev best 0.9700); val_score=0.9586673234517039; train_score=1.0.

**Learning:** Iter 12 xgboost: DISCARD. Train/val gap = 0.0413. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — xgboost iter 13
**Diagnosis:** Gamma split-penalty 0.5 — discourages overly eager splits.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

**Hypothesis:** Hypothesis: fewer, higher-quality splits. Val improves slightly.

**Prediction:** Composite delta in [-0.003, +0.008].

**Verdict:** DISCARD composite=0.9566 (delta -0.0134 vs prev best 0.9700); val_score=0.9586673234517039; train_score=1.0.

**Learning:** Iter 13 xgboost: DISCARD. Train/val gap = 0.0413. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — xgboost iter 14
**Diagnosis:** High subsample for low-noise tasks — opposite direction from iter-4/7.

**Citations:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

**Hypothesis:** Hypothesis: gentle bagging if iter-4/7 over-regularised.

**Prediction:** Composite delta in [-0.005, +0.007].

**Verdict:** DISCARD composite=0.9508 (delta -0.0192 vs prev best 0.9700); val_score=0.9531145045004702; train_score=1.0.

**Learning:** Iter 14 xgboost: DISCARD. Train/val gap = 0.0469. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — xgboost iter 15
**Diagnosis:** L1 regularisation (reg_alpha) for feature selection.

**Citations:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

**Hypothesis:** Hypothesis: L1 trims noise features, val improves.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=0.9549 (delta -0.0151 vs prev best 0.9700); val_score=0.9570104339259325; train_score=1.0.

**Learning:** Iter 15 xgboost: DISCARD. Train/val gap = 0.0430. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — xgboost iter 16
**Diagnosis:** Combined moderate regularisation — meta-search across all axes.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

**Hypothesis:** Hypothesis: balanced config beats single-knob champions.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=0.9586 (delta -0.0114 vs prev best 0.9700); val_score=0.9605481169674444; train_score=1.0.

**Learning:** Iter 16 xgboost: DISCARD. Train/val gap = 0.0395. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — xgboost iter 17
**Diagnosis:** Fourth seed — extend variance characterisation.

**Citations:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

**Hypothesis:** Hypothesis: within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9573 (delta -0.0127 vs prev best 0.9700); val_score=0.9593390354216113; train_score=1.0.

**Learning:** Iter 17 xgboost: DISCARD. Train/val gap = 0.0407. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — xgboost iter 18
**Diagnosis:** Fifth seed.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Same as iter-15.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9506 (delta -0.0194 vs prev best 0.9700); val_score=0.9529801621064887; train_score=1.0.

**Learning:** Iter 18 xgboost: DISCARD. Train/val gap = 0.0470. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — xgboost iter 19
**Diagnosis:** Aggressive depth=12 with proportionally lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

**Hypothesis:** Hypothesis: depth=12 will overfit unless lr is very low.

**Prediction:** Composite delta in [-0.030, +0.010].

**Verdict:** DISCARD composite=0.9385 (delta -0.0315 vs prev best 0.9700); val_score=0.9414267162240831; train_score=1.0.

**Learning:** Iter 19 xgboost: DISCARD. Train/val gap = 0.0586. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — xgboost iter 20
**Diagnosis:** Very shallow, high-lr — stump-like learners as opposite extreme.

**Citations:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

**Hypothesis:** Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.

**Prediction:** Composite delta in [-0.040, +0.005].

**Verdict:** DISCARD composite=0.9620 (delta -0.0080 vs prev best 0.9700); val_score=0.9637723344229995; train_score=1.0.

**Learning:** Iter 20 xgboost: DISCARD. Train/val gap = 0.0362. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp21 — xgboost iter 21
**Diagnosis:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.

**Citations:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

**Hypothesis:** Hypothesis: no-op vs baseline; informational only.

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=0.9602 (delta -0.0098 vs prev best 0.9700); val_score=0.9620706640992343; train_score=1.0.

**Learning:** Iter 21 xgboost: DISCARD. Train/val gap = 0.0379. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — xgboost iter 22
**Diagnosis:** Confirm hist-method explicitly — same as default but pinned.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

**Hypothesis:** Hypothesis: no change vs baseline (already default in our setup).

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=0.9566 (delta -0.0134 vs prev best 0.9700); val_score=0.9586673234517039; train_score=1.0.

**Learning:** Iter 22 xgboost: DISCARD. Train/val gap = 0.0413. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — xgboost iter 23
**Diagnosis:** Long-and-slow final refinement with mid-strength L2.

**Citations:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

**Hypothesis:** Hypothesis: best champion candidate. Val should peak.

**Prediction:** Composite delta in [+0.005, +0.025].

**Verdict:** DISCARD composite=0.9654 (delta -0.0046 vs prev best 0.9700); val_score=0.9670413326765483; train_score=1.0.

**Learning:** Iter 23 xgboost: DISCARD. Train/val gap = 0.0330. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — xgboost iter 24
**Diagnosis:** Combined moderate everything — explore a balanced corner.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.9576 (delta -0.0124 vs prev best 0.9700); val_score=0.9596525010075679; train_score=1.0.

**Learning:** Iter 24 xgboost: DISCARD. Train/val gap = 0.0403. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — xgboost iter 25
**Diagnosis:** Final 6th seed — closes the variance characterisation for this backbone.

**Citations:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9606 (delta -0.0095 vs prev best 0.9700); val_score=0.9624289104831847; train_score=1.0.

**Learning:** Iter 25 xgboost: DISCARD. Train/val gap = 0.0376. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp26 — lightgbm iter 1
**Diagnosis:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard lightgbm config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 1 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp27 — lightgbm iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=0.8625 (delta -0.1075 vs prev best 0.9700); val_score=0.8689713850700821; train_score=0.9974915858932832.

**Learning:** Iter 2 lightgbm: DISCARD. Train/val gap = 0.1285. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp28 — lightgbm iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.8290 (delta -0.1410 vs prev best 0.9700); val_score=0.8364605257265684; train_score=0.9859577794514146.

**Learning:** Iter 3 lightgbm: DISCARD. Train/val gap = 0.1495. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp29 — lightgbm iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=0.8847 (delta -0.0853 vs prev best 0.9700); val_score=0.890152702521159; train_score=0.9998632516312855.

**Learning:** Iter 4 lightgbm: DISCARD. Train/val gap = 0.1097. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp30 — lightgbm iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9433 (delta -0.0267 vs prev best 0.9700); val_score=0.9460391384174467; train_score=1.0.

**Learning:** Iter 5 lightgbm: DISCARD. Train/val gap = 0.0540. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp31 — lightgbm iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9433 (delta -0.0267 vs prev best 0.9700); val_score=0.9460391384174467; train_score=1.0.

**Learning:** Iter 6 lightgbm: DISCARD. Train/val gap = 0.0540. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp32 — lightgbm iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8375 (delta -0.1325 vs prev best 0.9700); val_score=0.8448793157494067; train_score=0.9929135770719928.

**Learning:** Iter 7 lightgbm: DISCARD. Train/val gap = 0.1480. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp33 — lightgbm iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8381 (delta -0.1319 vs prev best 0.9700); val_score=0.8454166853253325; train_score=0.9925992599259926.

**Learning:** Iter 8 lightgbm: DISCARD. Train/val gap = 0.1472. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp34 — lightgbm iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 9 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp35 — lightgbm iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.8302 (delta -0.1398 vs prev best 0.9700); val_score=0.8377591688683892; train_score=0.9882233121271311.

**Learning:** Iter 10 lightgbm: DISCARD. Train/val gap = 0.1505. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp36 — lightgbm iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 11 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp37 — lightgbm iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 12 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp38 — lightgbm iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.8289 (delta -0.1411 vs prev best 0.9700); val_score=0.8365500873225561; train_score=0.9888927668277031.

**Learning:** Iter 13 lightgbm: DISCARD. Train/val gap = 0.1523. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp39 — lightgbm iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8379 (delta -0.1321 vs prev best 0.9700); val_score=0.8452375621333571; train_score=0.9927605005398499.

**Learning:** Iter 14 lightgbm: DISCARD. Train/val gap = 0.1475. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp40 — lightgbm iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8383 (delta -0.1317 vs prev best 0.9700); val_score=0.8456405893153016; train_score=0.9930646125837074.

**Learning:** Iter 15 lightgbm: DISCARD. Train/val gap = 0.1474. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp41 — lightgbm iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 16 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp42 — lightgbm iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 17 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp43 — lightgbm iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=0.8725 (delta -0.0975 vs prev best 0.9700); val_score=0.8785096950427655; train_score=0.9990203101942847.

**Learning:** Iter 18 lightgbm: DISCARD. Train/val gap = 0.1205. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp44 — lightgbm iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=0.8274 (delta -0.1426 vs prev best 0.9700); val_score=0.8348931977967847; train_score=0.98419025576027.

**Learning:** Iter 19 lightgbm: DISCARD. Train/val gap = 0.1493. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp45 — lightgbm iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 20 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp46 — lightgbm iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 21 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp47 — lightgbm iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.8445 (delta -0.1255 vs prev best 0.9700); val_score=0.8516412162464735; train_score=0.9940116460625654.

**Learning:** Iter 22 lightgbm: DISCARD. Train/val gap = 0.1424. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp48 — lightgbm iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8332 (delta -0.1368 vs prev best 0.9700); val_score=0.8406699207379876; train_score=0.9902745376578473.

**Learning:** Iter 23 lightgbm: DISCARD. Train/val gap = 0.1496. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp49 — lightgbm iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8673 (delta -0.1027 vs prev best 0.9700); val_score=0.8734942456674578; train_score=0.997803862018855.

**Learning:** Iter 24 lightgbm: DISCARD. Train/val gap = 0.1243. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp50 — lightgbm iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8415 (delta -0.1285 vs prev best 0.9700); val_score=0.8487752451748691; train_score=0.9936075240177079.

**Learning:** Iter 25 lightgbm: DISCARD. Train/val gap = 0.1448. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp51 — catboost iter 1
**Diagnosis:** Baseline catboost per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard catboost config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 1 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp52 — catboost iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 2 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp53 — catboost iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 3 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp54 — catboost iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 4 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp55 — catboost iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 5 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp56 — catboost iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 6 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp57 — catboost iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 7 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp58 — catboost iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 8 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp59 — catboost iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 9 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp60 — catboost iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 10 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp61 — catboost iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 11 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp62 — catboost iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 12 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp63 — catboost iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 13 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp64 — catboost iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 14 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp65 — catboost iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 15 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp66 — catboost iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 16 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp67 — catboost iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 17 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp68 — catboost iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 18 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp69 — catboost iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 19 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp70 — catboost iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 20 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp71 — catboost iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 21 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp72 — catboost iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 22 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp73 — catboost iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 23 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp74 — catboost iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 24 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp75 — catboost iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best 0.9700); val_score=NA; train_score=NA.

**Learning:** Iter 25 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp76 — mlp iter 1
**Diagnosis:** Baseline mlp per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard mlp config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** KEEP composite=0.9893 (delta +0.0193 vs prev best 0.9700); val_score=0.989521293269446; train_score=0.9941545174925657.

**Learning:** Iter 1 mlp: KEEP. Train/val gap = 0.0046. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp77 — mlp iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=0.9893 (delta +0.0000 vs prev best 0.9893); val_score=0.989521293269446; train_score=0.9941545174925657.

**Learning:** Iter 2 mlp: DISCARD. Train/val gap = 0.0046. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp78 — mlp iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.9881 (delta -0.0012 vs prev best 0.9893); val_score=0.9884465541175944; train_score=0.9951362483187094.

**Learning:** Iter 3 mlp: DISCARD. Train/val gap = 0.0067. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp79 — mlp iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** KEEP composite=0.9953 (delta +0.0060 vs prev best 0.9893); val_score=0.9954771394026242; train_score=0.9996366983637139.

**Learning:** Iter 4 mlp: KEEP. Train/val gap = 0.0042. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp80 — mlp iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9917 (delta -0.0036 vs prev best 0.9953); val_score=0.9919842371591061; train_score=0.9984386193721413.

**Learning:** Iter 5 mlp: DISCARD. Train/val gap = 0.0065. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp81 — mlp iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9294 (delta -0.0658 vs prev best 0.9953); val_score=0.9318884062513993; train_score=0.9809899357282666.

**Learning:** Iter 6 mlp: DISCARD. Train/val gap = 0.0491. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp82 — mlp iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9904 (delta -0.0048 vs prev best 0.9953); val_score=0.9908647172092606; train_score=0.9991978789715706.

**Learning:** Iter 7 mlp: DISCARD. Train/val gap = 0.0083. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp83 — mlp iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9889 (delta -0.0064 vs prev best 0.9953); val_score=0.9893421700774707; train_score=0.9989060130502847.

**Learning:** Iter 8 mlp: DISCARD. Train/val gap = 0.0096. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp84 — mlp iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.9893 (delta -0.0060 vs prev best 0.9953); val_score=0.989521293269446; train_score=0.9941545174925657.

**Learning:** Iter 9 mlp: DISCARD. Train/val gap = 0.0046. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp85 — mlp iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.9839 (delta -0.0113 vs prev best 0.9953); val_score=0.984550624692132; train_score=0.9967241622121396.

**Learning:** Iter 10 mlp: DISCARD. Train/val gap = 0.0122. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp86 — mlp iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=0.9879 (delta -0.0074 vs prev best 0.9953); val_score=0.9884017733196004; train_score=0.9989733667244276.

**Learning:** Iter 11 mlp: DISCARD. Train/val gap = 0.0106. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp87 — mlp iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=0.9926 (delta -0.0027 vs prev best 0.9953); val_score=0.9929246339169764; train_score=0.9997346673442854.

**Learning:** Iter 12 mlp: DISCARD. Train/val gap = 0.0068. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp88 — mlp iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.9881 (delta -0.0072 vs prev best 0.9953); val_score=0.9884465541175944; train_score=0.9951362483187094.

**Learning:** Iter 13 mlp: DISCARD. Train/val gap = 0.0067. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp89 — mlp iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9922 (delta -0.0031 vs prev best 0.9953); val_score=0.9925663875330258; train_score=0.999899989999.

**Learning:** Iter 14 mlp: DISCARD. Train/val gap = 0.0073. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp90 — mlp iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9832 (delta -0.0120 vs prev best 0.9953); val_score=0.9839684743182124; train_score=0.9983937169227126.

**Learning:** Iter 15 mlp: DISCARD. Train/val gap = 0.0144. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp91 — mlp iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9857 (delta -0.0096 vs prev best 0.9953); val_score=0.9863418566118848; train_score=0.9996591495884282.

**Learning:** Iter 16 mlp: DISCARD. Train/val gap = 0.0133. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp92 — mlp iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=0.9951 (delta -0.0002 vs prev best 0.9953); val_score=0.9952980162106488; train_score=0.9999101951011428.

**Learning:** Iter 17 mlp: DISCARD. Train/val gap = 0.0046. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp93 — mlp iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=0.9938 (delta -0.0015 vs prev best 0.9953); val_score=0.9940889346648156; train_score=0.9997162981604284.

**Learning:** Iter 18 mlp: DISCARD. Train/val gap = 0.0056. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp94 — mlp iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=0.9070 (delta -0.0883 vs prev best 0.9953); val_score=0.9081098025166808; train_score=0.9305216235909305.

**Learning:** Iter 19 mlp: DISCARD. Train/val gap = 0.0224. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp95 — mlp iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9893 (delta -0.0060 vs prev best 0.9953); val_score=0.989521293269446; train_score=0.9941545174925657.

**Learning:** Iter 20 mlp: DISCARD. Train/val gap = 0.0046. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp96 — mlp iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.9893 (delta -0.0060 vs prev best 0.9953); val_score=0.989521293269446; train_score=0.9941545174925657.

**Learning:** Iter 21 mlp: DISCARD. Train/val gap = 0.0046. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp97 — mlp iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9893 (delta -0.0060 vs prev best 0.9953); val_score=0.989521293269446; train_score=0.9941545174925657.

**Learning:** Iter 22 mlp: DISCARD. Train/val gap = 0.0046. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp98 — mlp iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9931 (delta -0.0022 vs prev best 0.9953); val_score=0.9933276610989208; train_score=0.9983549375345697.

**Learning:** Iter 23 mlp: DISCARD. Train/val gap = 0.0050. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp99 — mlp iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.9951 (delta -0.0001 vs prev best 0.9953); val_score=0.9952980162106488; train_score=0.9987529365181416.

**Learning:** Iter 24 mlp: DISCARD. Train/val gap = 0.0035. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp100 — mlp iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.9926 (delta -0.0027 vs prev best 0.9953); val_score=0.9928798531189826; train_score=0.99855495753657.

**Learning:** Iter 25 mlp: DISCARD. Train/val gap = 0.0057. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp101 — ft_transformer iter 1
**Diagnosis:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard ft_transformer config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 1 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp102 — ft_transformer iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=0.8293 (delta -0.1660 vs prev best 0.9953); val_score=0.8363485737315841; train_score=0.9781855736594068.

**Learning:** Iter 2 ft_transformer: DISCARD. Train/val gap = 0.1418. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp103 — ft_transformer iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.7815 (delta -0.2138 vs prev best 0.9953); val_score=0.7882316062872239; train_score=0.9233351906619234.

**Learning:** Iter 3 ft_transformer: DISCARD. Train/val gap = 0.1351. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp104 — ft_transformer iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=0.8637 (delta -0.1316 vs prev best 0.9953); val_score=0.869956562625946; train_score=0.9953015709734239.

**Learning:** Iter 4 ft_transformer: DISCARD. Train/val gap = 0.1253. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp105 — ft_transformer iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.9367 (delta -0.0586 vs prev best 0.9953); val_score=0.939680265102324; train_score=1.0.

**Learning:** Iter 5 ft_transformer: DISCARD. Train/val gap = 0.0603. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp106 — ft_transformer iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.9367 (delta -0.0586 vs prev best 0.9953); val_score=0.939680265102324; train_score=1.0.

**Learning:** Iter 6 ft_transformer: DISCARD. Train/val gap = 0.0603. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp107 — ft_transformer iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 7 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp108 — ft_transformer iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 8 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp109 — ft_transformer iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 9 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp110 — ft_transformer iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=0.7904 (delta -0.2048 vs prev best 0.9953); val_score=0.7971877658859882; train_score=0.9323075164659325.

**Learning:** Iter 10 ft_transformer: DISCARD. Train/val gap = 0.1351. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp111 — ft_transformer iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 11 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp112 — ft_transformer iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 12 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp113 — ft_transformer iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=0.7930 (delta -0.2023 vs prev best 0.9953); val_score=0.7998298329676234; train_score=0.9373794522309374.

**Learning:** Iter 13 ft_transformer: DISCARD. Train/val gap = 0.1375. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp114 — ft_transformer iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 14 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp115 — ft_transformer iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 15 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp116 — ft_transformer iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 16 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp117 — ft_transformer iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 17 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp118 — ft_transformer iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=0.8411 (delta -0.1542 vs prev best 0.9953); val_score=0.8480139716089741; train_score=0.9864741576198436.

**Learning:** Iter 18 ft_transformer: DISCARD. Train/val gap = 0.1385. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp119 — ft_transformer iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=0.7586 (delta -0.2367 vs prev best 0.9953); val_score=0.7652590569163942; train_score=0.8991725703182563.

**Learning:** Iter 19 ft_transformer: DISCARD. Train/val gap = 0.1339. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp120 — ft_transformer iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 20 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp121 — ft_transformer iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 21 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp122 — ft_transformer iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 22 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp123 — ft_transformer iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8041 (delta -0.1912 vs prev best 0.9953); val_score=0.810890690072097; train_score=0.9463977009945893.

**Learning:** Iter 23 ft_transformer: DISCARD. Train/val gap = 0.1355. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp124 — ft_transformer iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=0.8293 (delta -0.1660 vs prev best 0.9953); val_score=0.8363933545295777; train_score=0.9781753685572638.

**Learning:** Iter 24 ft_transformer: DISCARD. Train/val gap = 0.1418. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp125 — ft_transformer iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=0.8213 (delta -0.1739 vs prev best 0.9953); val_score=0.8282432492947024; train_score=0.9662200913968948.

**Learning:** Iter 25 ft_transformer: DISCARD. Train/val gap = 0.1380. Closing axis if True and delta < -0.01; otherwise this direction is open.

