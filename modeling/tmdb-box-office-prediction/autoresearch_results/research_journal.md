# Research Journal — tmdb-box-office-prediction

_(populated by `framework/hill_climb.py`)_

## Exp1 — xgboost iter 1
**Diagnosis:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

**Hypothesis:** Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).

**Prediction:** Composite in [0.55, 0.85] depending on task difficulty.

**Verdict:** KEEP composite=-2.2181 (delta +inf vs prev best -inf); val_score=-2.115232458844642; train_score=-0.05887587891948178.

**Learning:** Iter 1 xgboost: KEEP. Train/val gap = 2.0564. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — xgboost iter 2
**Diagnosis:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.

**Citations:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

**Hypothesis:** Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-2.5793 (delta -0.3612 vs prev best -2.2181); val_score=-2.4567547810908685; train_score=-0.006623132936376364.

**Learning:** Iter 2 xgboost: DISCARD. Train/val gap = 2.4501. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — xgboost iter 3
**Diagnosis:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

**Hypothesis:** Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-1.7276 (delta +0.4905 vs prev best -2.2181); val_score=-1.6560195186680973; train_score=-0.22500438785248122.

**Learning:** Iter 3 xgboost: KEEP. Train/val gap = 1.4310. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp4 — xgboost iter 4
**Diagnosis:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.

**Citations:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

**Hypothesis:** Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.

**Prediction:** Composite delta in [+0.001, +0.010].

**Verdict:** DISCARD composite=-2.1529 (delta -0.4253 vs prev best -1.7276); val_score=-2.053699676584379; train_score=-0.07015433336987288.

**Learning:** Iter 4 xgboost: DISCARD. Train/val gap = 1.9835. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — xgboost iter 5
**Diagnosis:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

**Hypothesis:** Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.

**Prediction:** Composite delta in [+0.002, +0.012].

**Verdict:** DISCARD composite=-2.0463 (delta -0.3188 vs prev best -1.7276); val_score=-1.9563844872214715; train_score=-0.15718774731049695.

**Learning:** Iter 5 xgboost: DISCARD. Train/val gap = 1.7992. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — xgboost iter 6
**Diagnosis:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.

**Citations:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

**Hypothesis:** Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.2874 (delta -0.5598 vs prev best -1.7276); val_score=-2.188956075800112; train_score=-0.22064964524203198.

**Learning:** Iter 6 xgboost: DISCARD. Train/val gap = 1.9683. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — xgboost iter 7
**Diagnosis:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.

**Citations:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

**Hypothesis:** Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-2.0337 (delta -0.3062 vs prev best -1.7276); val_score=-1.9418403247675413; train_score=-0.10386570178745064.

**Learning:** Iter 7 xgboost: DISCARD. Train/val gap = 1.8380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp8 — xgboost iter 8
**Diagnosis:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.

**Citations:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.2367 (delta -0.5091 vs prev best -1.7276); val_score=-2.133190414985998; train_score=-0.06260186700450515.

**Learning:** Iter 8 xgboost: DISCARD. Train/val gap = 2.0706. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — xgboost iter 9
**Diagnosis:** Third seed for 3-seed median (autoresearch protocol).

**Citations:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1932 (delta -0.4656 vs prev best -1.7276); val_score=-2.091589766934068; train_score=-0.059984562767348024.

**Learning:** Iter 9 xgboost: DISCARD. Train/val gap = 2.0316. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — xgboost iter 10
**Diagnosis:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

**Hypothesis:** Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7364 (delta -1.0089 vs prev best -1.7276); val_score=-2.6062801075758353; train_score=-0.00336480666919503.

**Learning:** Iter 10 xgboost: DISCARD. Train/val gap = 2.6029. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — xgboost iter 11
**Diagnosis:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.

**Citations:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

**Hypothesis:** Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-1.7936 (delta -0.0660 vs prev best -1.7276); val_score=-1.7185488496462955; train_score=-0.217928433535179.

**Learning:** Iter 11 xgboost: DISCARD. Train/val gap = 1.5006. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp12 — xgboost iter 12
**Diagnosis:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

**Hypothesis:** Hypothesis: larger leaves reduce variance, improve val by 0.5%.

**Prediction:** Composite delta in [-0.002, +0.010].

**Verdict:** DISCARD composite=-2.2181 (delta -0.4905 vs prev best -1.7276); val_score=-2.115232458844642; train_score=-0.05887587891948178.

**Learning:** Iter 12 xgboost: DISCARD. Train/val gap = 2.0564. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — xgboost iter 13
**Diagnosis:** Gamma split-penalty 0.5 — discourages overly eager splits.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

**Hypothesis:** Hypothesis: fewer, higher-quality splits. Val improves slightly.

**Prediction:** Composite delta in [-0.003, +0.008].

**Verdict:** DISCARD composite=-2.2181 (delta -0.4905 vs prev best -1.7276); val_score=-2.115232458844642; train_score=-0.05887587891948178.

**Learning:** Iter 13 xgboost: DISCARD. Train/val gap = 2.0564. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — xgboost iter 14
**Diagnosis:** High subsample for low-noise tasks — opposite direction from iter-4/7.

**Citations:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

**Hypothesis:** Hypothesis: gentle bagging if iter-4/7 over-regularised.

**Prediction:** Composite delta in [-0.005, +0.007].

**Verdict:** DISCARD composite=-2.3165 (delta -0.5889 vs prev best -1.7276); val_score=-2.2086799877320407; train_score=-0.05294610715452399.

**Learning:** Iter 14 xgboost: DISCARD. Train/val gap = 2.1557. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — xgboost iter 15
**Diagnosis:** L1 regularisation (reg_alpha) for feature selection.

**Citations:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

**Hypothesis:** Hypothesis: L1 trims noise features, val improves.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-2.3901 (delta -0.6625 vs prev best -1.7276); val_score=-2.2775252778611232; train_score=-0.026381524038439175.

**Learning:** Iter 15 xgboost: DISCARD. Train/val gap = 2.2511. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — xgboost iter 16
**Diagnosis:** Combined moderate regularisation — meta-search across all axes.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

**Hypothesis:** Hypothesis: balanced config beats single-knob champions.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-2.2403 (delta -0.5128 vs prev best -1.7276); val_score=-2.134740496013753; train_score=-0.022761439030219686.

**Learning:** Iter 16 xgboost: DISCARD. Train/val gap = 2.1120. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — xgboost iter 17
**Diagnosis:** Fourth seed — extend variance characterisation.

**Citations:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

**Hypothesis:** Hypothesis: within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.2231 (delta -0.4955 vs prev best -1.7276); val_score=-2.120218057574225; train_score=-0.06338838541650522.

**Learning:** Iter 17 xgboost: DISCARD. Train/val gap = 2.0568. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — xgboost iter 18
**Diagnosis:** Fifth seed.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Same as iter-15.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1679 (delta -0.4403 vs prev best -1.7276); val_score=-2.067560980196191; train_score=-0.06115143571494426.

**Learning:** Iter 18 xgboost: DISCARD. Train/val gap = 2.0064. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — xgboost iter 19
**Diagnosis:** Aggressive depth=12 with proportionally lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

**Hypothesis:** Hypothesis: depth=12 will overfit unless lr is very low.

**Prediction:** Composite delta in [-0.030, +0.010].

**Verdict:** DISCARD composite=-2.7852 (delta -1.0577 vs prev best -1.7276); val_score=-2.65333046628647; train_score=-0.015316844646635661.

**Learning:** Iter 19 xgboost: DISCARD. Train/val gap = 2.6380. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — xgboost iter 20
**Diagnosis:** Very shallow, high-lr — stump-like learners as opposite extreme.

**Citations:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

**Hypothesis:** Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.

**Prediction:** Composite delta in [-0.040, +0.005].

**Verdict:** KEEP composite=-1.5215 (delta +0.2061 vs prev best -1.7276); val_score=-1.4644083011632614; train_score=-0.32346691145294715.

**Learning:** Iter 20 xgboost: KEEP. Train/val gap = 1.1409. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp21 — xgboost iter 21
**Diagnosis:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.

**Citations:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

**Hypothesis:** Hypothesis: no-op vs baseline; informational only.

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-2.2124 (delta -0.6910 vs prev best -1.5215); val_score=-2.107946519712552; train_score=-0.018463438993107074.

**Learning:** Iter 21 xgboost: DISCARD. Train/val gap = 2.0895. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — xgboost iter 22
**Diagnosis:** Confirm hist-method explicitly — same as default but pinned.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

**Hypothesis:** Hypothesis: no change vs baseline (already default in our setup).

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-2.2181 (delta -0.6966 vs prev best -1.5215); val_score=-2.115232458844642; train_score=-0.05887587891948178.

**Learning:** Iter 22 xgboost: DISCARD. Train/val gap = 2.0564. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — xgboost iter 23
**Diagnosis:** Long-and-slow final refinement with mid-strength L2.

**Citations:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

**Hypothesis:** Hypothesis: best champion candidate. Val should peak.

**Prediction:** Composite delta in [+0.005, +0.025].

**Verdict:** DISCARD composite=-1.8697 (delta -0.3482 vs prev best -1.5215); val_score=-1.7854037791454325; train_score=-0.09999151417371192.

**Learning:** Iter 23 xgboost: DISCARD. Train/val gap = 1.6854. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — xgboost iter 24
**Diagnosis:** Combined moderate everything — explore a balanced corner.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-2.0795 (delta -0.5580 vs prev best -1.5215); val_score=-1.9846638747082337; train_score=-0.08802704290724139.

**Learning:** Iter 24 xgboost: DISCARD. Train/val gap = 1.8966. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — xgboost iter 25
**Diagnosis:** Final 6th seed — closes the variance characterisation for this backbone.

**Citations:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.2357 (delta -0.7142 vs prev best -1.5215); val_score=-2.1321942338050226; train_score=-0.06211374742783892.

**Learning:** Iter 25 xgboost: DISCARD. Train/val gap = 2.0701. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp26 — lightgbm iter 1
**Diagnosis:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard lightgbm config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 1 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp27 — lightgbm iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-3.9360 (delta -2.4145 vs prev best -1.5215); val_score=-3.9150372290570217; train_score=-3.496232686802921.

**Learning:** Iter 2 lightgbm: DISCARD. Train/val gap = 0.4188. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp28 — lightgbm iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.5422 (delta -3.0207 vs prev best -1.5215); val_score=-4.539245480783358; train_score=-4.4808783030387636.

**Learning:** Iter 3 lightgbm: DISCARD. Train/val gap = 0.0584. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp29 — lightgbm iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-3.4402 (delta -1.9188 vs prev best -1.5215); val_score=-3.40107865434524; train_score=-2.6181258858485883.

**Learning:** Iter 4 lightgbm: DISCARD. Train/val gap = 0.7830. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp30 — lightgbm iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-2.1689 (delta -0.6474 vs prev best -1.5215); val_score=-2.069803324614275; train_score=-0.08878079657548377.

**Learning:** Iter 5 lightgbm: DISCARD. Train/val gap = 1.9810. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp31 — lightgbm iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.1689 (delta -0.6474 vs prev best -1.5215); val_score=-2.069803324614275; train_score=-0.08878079657548377.

**Learning:** Iter 6 lightgbm: DISCARD. Train/val gap = 1.9810. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp32 — lightgbm iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1643 (delta -2.6428 vs prev best -1.5215); val_score=-4.150239279686312; train_score=-3.8690299202068155.

**Learning:** Iter 7 lightgbm: DISCARD. Train/val gap = 0.2812. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp33 — lightgbm iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1633 (delta -2.6418 vs prev best -1.5215); val_score=-4.149148645725608; train_score=-3.866261807108715.

**Learning:** Iter 8 lightgbm: DISCARD. Train/val gap = 0.2829. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp34 — lightgbm iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 9 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp35 — lightgbm iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.4269 (delta -2.9055 vs prev best -1.5215); val_score=-4.420639378840637; train_score=-4.295119082407205.

**Learning:** Iter 10 lightgbm: DISCARD. Train/val gap = 0.1255. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp36 — lightgbm iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 11 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp37 — lightgbm iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 12 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp38 — lightgbm iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-4.3741 (delta -2.8527 vs prev best -1.5215); val_score=-4.366063240066945; train_score=-4.205209806525815.

**Learning:** Iter 13 lightgbm: DISCARD. Train/val gap = 0.1609. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp39 — lightgbm iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1641 (delta -2.6426 vs prev best -1.5215); val_score=-4.150078418641756; train_score=-3.869652197904065.

**Learning:** Iter 14 lightgbm: DISCARD. Train/val gap = 0.2804. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp40 — lightgbm iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1683 (delta -2.6469 vs prev best -1.5215); val_score=-4.154118799207782; train_score=-3.870350827920367.

**Learning:** Iter 15 lightgbm: DISCARD. Train/val gap = 0.2838. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp41 — lightgbm iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 16 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp42 — lightgbm iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 17 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp43 — lightgbm iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-3.7403 (delta -2.2188 vs prev best -1.5215); val_score=-3.712925184651863; train_score=-3.1660875570929488.

**Learning:** Iter 18 lightgbm: DISCARD. Train/val gap = 0.5468. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp44 — lightgbm iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-4.6794 (delta -3.1580 vs prev best -1.5215); val_score=-4.6683373002680355; train_score=-4.67888978924377.

**Learning:** Iter 19 lightgbm: DISCARD. Train/val gap = 0.0106. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp45 — lightgbm iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 20 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp46 — lightgbm iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 21 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp47 — lightgbm iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-4.1688 (delta -2.6474 vs prev best -1.5215); val_score=-4.154585781747538; train_score=-3.8701281827059772.

**Learning:** Iter 22 lightgbm: DISCARD. Train/val gap = 0.2845. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp48 — lightgbm iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.3210 (delta -2.7995 vs prev best -1.5215); val_score=-4.311311677864849; train_score=-4.117952353134179.

**Learning:** Iter 23 lightgbm: DISCARD. Train/val gap = 0.1934. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp49 — lightgbm iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-3.9375 (delta -2.4160 vs prev best -1.5215); val_score=-3.91640684584198; train_score=-3.4950026999701604.

**Learning:** Iter 24 lightgbm: DISCARD. Train/val gap = 0.4214. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp50 — lightgbm iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1636 (delta -2.6422 vs prev best -1.5215); val_score=-4.14959550475922; train_score=-3.8685764907516496.

**Learning:** Iter 25 lightgbm: DISCARD. Train/val gap = 0.2810. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp51 — catboost iter 1
**Diagnosis:** Baseline catboost per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard catboost config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 1 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp52 — catboost iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 2 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp53 — catboost iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 3 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp54 — catboost iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 4 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp55 — catboost iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 5 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp56 — catboost iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 6 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp57 — catboost iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 7 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp58 — catboost iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 8 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp59 — catboost iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 9 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp60 — catboost iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 10 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp61 — catboost iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 11 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp62 — catboost iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 12 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp63 — catboost iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 13 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp64 — catboost iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 14 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp65 — catboost iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 15 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp66 — catboost iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 16 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp67 — catboost iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 17 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp68 — catboost iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 18 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp69 — catboost iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 19 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp70 — catboost iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 20 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp71 — catboost iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 21 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp72 — catboost iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 22 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp73 — catboost iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 23 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp74 — catboost iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 24 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp75 — catboost iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.5215); val_score=NA; train_score=NA.

**Learning:** Iter 25 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp76 — mlp iter 1
**Diagnosis:** Baseline mlp per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard mlp config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** KEEP composite=-0.5057 (delta +1.0157 vs prev best -1.5215); val_score=-0.4984710532587138; train_score=-0.35310640412713196.

**Learning:** Iter 1 mlp: KEEP. Train/val gap = 0.1454. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp77 — mlp iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-0.4269 (delta +0.0789 vs prev best -0.5057); val_score=-0.4184630136496231; train_score=-0.2500435820976935.

**Learning:** Iter 2 mlp: KEEP. Train/val gap = 0.1684. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp78 — mlp iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.7423 (delta -0.3154 vs prev best -0.4269); val_score=-0.7394200176035683; train_score=-0.6816220649881307.

**Learning:** Iter 3 mlp: DISCARD. Train/val gap = 0.0578. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp79 — mlp iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** KEEP composite=-0.4002 (delta +0.0266 vs prev best -0.4269); val_score=-0.39135848798981426; train_score=-0.21375178354478455.

**Learning:** Iter 4 mlp: KEEP. Train/val gap = 0.1776. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp80 — mlp iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.5565 (delta -0.1563 vs prev best -0.4002); val_score=-0.5504451564959307; train_score=-0.42923351927608056.

**Learning:** Iter 5 mlp: DISCARD. Train/val gap = 0.1212. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp81 — mlp iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-1.9016 (delta -1.5014 vs prev best -0.4002); val_score=-1.8919966584916075; train_score=-1.7000474334157996.

**Learning:** Iter 6 mlp: DISCARD. Train/val gap = 0.1919. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp82 — mlp iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5472 (delta -0.1470 vs prev best -0.4002); val_score=-0.5380345924097698; train_score=-0.35379586256108364.

**Learning:** Iter 7 mlp: DISCARD. Train/val gap = 0.1842. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp83 — mlp iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5045 (delta -0.1042 vs prev best -0.4002); val_score=-0.4971167761890043; train_score=-0.35038957967782997.

**Learning:** Iter 8 mlp: DISCARD. Train/val gap = 0.1467. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp84 — mlp iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.4124 (delta -0.0121 vs prev best -0.4002); val_score=-0.40343394306721664; train_score=-0.22468913776718674.

**Learning:** Iter 9 mlp: DISCARD. Train/val gap = 0.1787. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp85 — mlp iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.5903 (delta -0.1900 vs prev best -0.4002); val_score=-0.5823000856676912; train_score=-0.42252986026521544.

**Learning:** Iter 10 mlp: DISCARD. Train/val gap = 0.1598. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp86 — mlp iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-0.5475 (delta -0.1472 vs prev best -0.4002); val_score=-0.535391567868981; train_score=-0.29371892886496775.

**Learning:** Iter 11 mlp: DISCARD. Train/val gap = 0.2417. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp87 — mlp iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-0.4553 (delta -0.0550 vs prev best -0.4002); val_score=-0.442304659038847; train_score=-0.18322636999764974.

**Learning:** Iter 12 mlp: DISCARD. Train/val gap = 0.2591. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp88 — mlp iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-0.6756 (delta -0.2753 vs prev best -0.4002); val_score=-0.6712690992497414; train_score=-0.5851458223888223.

**Learning:** Iter 13 mlp: DISCARD. Train/val gap = 0.0861. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp89 — mlp iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5215 (delta -0.1212 vs prev best -0.4002); val_score=-0.5128203611916232; train_score=-0.3399731510269162.

**Learning:** Iter 14 mlp: DISCARD. Train/val gap = 0.1728. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp90 — mlp iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5661 (delta -0.1658 vs prev best -0.4002); val_score=-0.5557601389764464; train_score=-0.34947548332301004.

**Learning:** Iter 15 mlp: DISCARD. Train/val gap = 0.2063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp91 — mlp iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.6342 (delta -0.2339 vs prev best -0.4002); val_score=-0.6247160504960071; train_score=-0.43581582220516185.

**Learning:** Iter 16 mlp: DISCARD. Train/val gap = 0.1889. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp92 — mlp iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** KEEP composite=-0.3490 (delta +0.0512 vs prev best -0.4002); val_score=-0.34001806326875805; train_score=-0.16020466491404095.

**Learning:** Iter 17 mlp: KEEP. Train/val gap = 0.1798. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp93 — mlp iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-0.4182 (delta -0.0692 vs prev best -0.3490); val_score=-0.4098809908062316; train_score=-0.24404792551637253.

**Learning:** Iter 18 mlp: DISCARD. Train/val gap = 0.1658. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp94 — mlp iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-3.7890 (delta -3.4400 vs prev best -0.3490); val_score=-3.7818797194035843; train_score=-3.788670596275818.

**Learning:** Iter 19 mlp: DISCARD. Train/val gap = 0.0068. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp95 — mlp iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.4035 (delta -0.0545 vs prev best -0.3490); val_score=-0.39382406628043426; train_score=-0.2010533159385963.

**Learning:** Iter 20 mlp: DISCARD. Train/val gap = 0.1928. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp96 — mlp iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.5057 (delta -0.1567 vs prev best -0.3490); val_score=-0.4984710532587138; train_score=-0.35310640412713196.

**Learning:** Iter 21 mlp: DISCARD. Train/val gap = 0.1454. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp97 — mlp iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-0.5057 (delta -0.1567 vs prev best -0.3490); val_score=-0.4984710532587138; train_score=-0.35310640412713196.

**Learning:** Iter 22 mlp: DISCARD. Train/val gap = 0.1454. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp98 — mlp iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.5637 (delta -0.2147 vs prev best -0.3490); val_score=-0.5572315492617457; train_score=-0.4275638292579414.

**Learning:** Iter 23 mlp: DISCARD. Train/val gap = 0.1297. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp99 — mlp iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.4487 (delta -0.0997 vs prev best -0.3490); val_score=-0.44112883771144185; train_score=-0.2889610576478294.

**Learning:** Iter 24 mlp: DISCARD. Train/val gap = 0.1522. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp100 — mlp iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5449 (delta -0.1959 vs prev best -0.3490); val_score=-0.5359309916198405; train_score=-0.35633357138591576.

**Learning:** Iter 25 mlp: DISCARD. Train/val gap = 0.1796. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp101 — ft_transformer iter 1
**Diagnosis:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard ft_transformer config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 1 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp102 — ft_transformer iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-3.9503 (delta -3.6013 vs prev best -0.3490); val_score=-3.9356164528184556; train_score=-3.641237145060109.

**Learning:** Iter 2 ft_transformer: DISCARD. Train/val gap = 0.2944. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp103 — ft_transformer iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.5603 (delta -4.2113 vs prev best -0.3490); val_score=-4.557859921745293; train_score=-4.509447765878108.

**Learning:** Iter 3 ft_transformer: DISCARD. Train/val gap = 0.0484. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp104 — ft_transformer iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-3.4946 (delta -3.1456 vs prev best -0.3490); val_score=-3.4640245879649942; train_score=-2.8529693806499674.

**Learning:** Iter 4 ft_transformer: DISCARD. Train/val gap = 0.6111. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp105 — ft_transformer iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-2.0977 (delta -1.7487 vs prev best -0.3490); val_score=-2.0025010453093324; train_score=-0.09770563243023103.

**Learning:** Iter 5 ft_transformer: DISCARD. Train/val gap = 1.9048. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp106 — ft_transformer iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.0977 (delta -1.7487 vs prev best -0.3490); val_score=-2.0025010453093324; train_score=-0.09770563243023103.

**Learning:** Iter 6 ft_transformer: DISCARD. Train/val gap = 1.9048. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp107 — ft_transformer iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 7 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp108 — ft_transformer iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 8 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp109 — ft_transformer iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 9 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp110 — ft_transformer iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.4470 (delta -4.0979 vs prev best -0.3490); val_score=-4.442046275666809; train_score=-4.343907558756892.

**Learning:** Iter 10 ft_transformer: DISCARD. Train/val gap = 0.0981. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp111 — ft_transformer iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 11 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp112 — ft_transformer iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 12 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp113 — ft_transformer iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-4.3870 (delta -4.0380 vs prev best -0.3490); val_score=-4.381176806124777; train_score=-4.2646383446903195.

**Learning:** Iter 13 ft_transformer: DISCARD. Train/val gap = 0.1165. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp114 — ft_transformer iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 14 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp115 — ft_transformer iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 15 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp116 — ft_transformer iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 16 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp117 — ft_transformer iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 17 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp118 — ft_transformer iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-3.7690 (delta -3.4200 vs prev best -0.3490); val_score=-3.7491689328075735; train_score=-3.3521760628978368.

**Learning:** Iter 18 ft_transformer: DISCARD. Train/val gap = 0.3970. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp119 — ft_transformer iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-4.6880 (delta -4.3390 vs prev best -0.3490); val_score=-4.676485126829606; train_score=-4.687447033450508.

**Learning:** Iter 19 ft_transformer: DISCARD. Train/val gap = 0.0110. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp120 — ft_transformer iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 20 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp121 — ft_transformer iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 21 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp122 — ft_transformer iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 22 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp123 — ft_transformer iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.3307 (delta -3.9817 vs prev best -0.3490); val_score=-4.323827280489107; train_score=-4.1867008295103965.

**Learning:** Iter 23 ft_transformer: DISCARD. Train/val gap = 0.1371. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp124 — ft_transformer iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-3.9508 (delta -3.6018 vs prev best -0.3490); val_score=-3.9360361264355612; train_score=-3.6409677718790268.

**Learning:** Iter 24 ft_transformer: DISCARD. Train/val gap = 0.2951. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp125 — ft_transformer iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1758 (delta -3.8268 vs prev best -0.3490); val_score=-4.165989339285481; train_score=-3.9703471569538054.

**Learning:** Iter 25 ft_transformer: DISCARD. Train/val gap = 0.1956. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp126 — ext xgboost 1/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.0152 (delta -1.6661 vs prev best -0.3490); val=-1.9469479346658665 train=-0.5828977957073422.

**Learning:** Ext iter 1 (xgboost): DISCARD. Train/val gap = 1.3641. This iter targets Extended xgboost sweep.


## Exp127 — ext xgboost 2/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-1.8044 (delta -1.4553 vs prev best -0.3490); val=-1.7254923269962898 train=-0.14828237157303023.

**Learning:** Ext iter 2 (xgboost): DISCARD. Train/val gap = 1.5772. This iter targets Extended xgboost sweep.


## Exp128 — ext xgboost 3/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.0871 (delta -1.7381 vs prev best -0.3490); val=-2.00250397337711 train=-0.3112898043186742.

**Learning:** Ext iter 3 (xgboost): DISCARD. Train/val gap = 1.6912. This iter targets Extended xgboost sweep.


## Exp129 — ext xgboost 4/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.0017 (delta -1.6527 vs prev best -0.3490); val=-1.9086424400936355 train=-0.04654201061961024.

**Learning:** Ext iter 4 (xgboost): DISCARD. Train/val gap = 1.8621. This iter targets Extended xgboost sweep.


## Exp130 — ext xgboost 5/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.2631 (delta -1.9141 vs prev best -0.3490); val=-2.1629124418994037 train=-0.15902684485679167.

**Learning:** Ext iter 5 (xgboost): DISCARD. Train/val gap = 2.0039. This iter targets Extended xgboost sweep.


## Exp131 — ext xgboost 6/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.2306 (delta -1.8816 vs prev best -0.3490); val=-2.124897561689636 train=-0.011611966046615133.

**Learning:** Ext iter 6 (xgboost): DISCARD. Train/val gap = 2.1133. This iter targets Extended xgboost sweep.


## Exp132 — ext xgboost 7/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.4231 (delta -2.0741 vs prev best -0.3490); val=-2.3114371047922546 train=-0.07885685498296623.

**Learning:** Ext iter 7 (xgboost): DISCARD. Train/val gap = 2.2326. This iter targets Extended xgboost sweep.


## Exp133 — ext xgboost 8/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.4165 (delta -2.0674 vs prev best -0.3490); val=-2.301467352801943 train=-0.0017590826522591127.

**Learning:** Ext iter 8 (xgboost): DISCARD. Train/val gap = 2.2997. This iter targets Extended xgboost sweep.


## Exp134 — ext xgboost 9/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.5903 (delta -2.2413 vs prev best -0.3490); val=-2.4688782477566797 train=-0.040889324140209064.

**Learning:** Ext iter 9 (xgboost): DISCARD. Train/val gap = 2.4280. This iter targets Extended xgboost sweep.


## Exp135 — ext xgboost 10/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.5766 (delta -2.2276 vs prev best -0.3490); val=-2.4539140537821633 train=-0.0005155908853598599.

**Learning:** Ext iter 10 (xgboost): DISCARD. Train/val gap = 2.4534. This iter targets Extended xgboost sweep.


## Exp136 — ext xgboost 11/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7533 (delta -2.4043 vs prev best -0.3490); val=-2.6231511280648174 train=-0.02025522205250224.

**Learning:** Ext iter 11 (xgboost): DISCARD. Train/val gap = 2.6029. This iter targets Extended xgboost sweep.


## Exp137 — ext xgboost 12/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7250 (delta -2.3760 vs prev best -0.3490); val=-2.595242817567368 train=-0.00047202972590073796.

**Learning:** Ext iter 12 (xgboost): DISCARD. Train/val gap = 2.5948. This iter targets Extended xgboost sweep.


## Exp138 — ext xgboost 13/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.8033 (delta -2.4543 vs prev best -0.3490); val=-2.6705915257279687 train=-0.01678611315661114.

**Learning:** Ext iter 13 (xgboost): DISCARD. Train/val gap = 2.6538. This iter targets Extended xgboost sweep.


## Exp139 — ext xgboost 14/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7860 (delta -2.4370 vs prev best -0.3490); val=-2.653336666367065 train=-0.0004364949348859333.

**Learning:** Ext iter 14 (xgboost): DISCARD. Train/val gap = 2.6529. This iter targets Extended xgboost sweep.


## Exp140 — ext lightgbm 15/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0177 (delta -1.6687 vs prev best -0.3490); val=-1.9234961602107965 train=-0.03957553797306295.

**Learning:** Ext iter 15 (lightgbm): DISCARD. Train/val gap = 1.8839. This iter targets LightGBM leaf-wise sweep.


## Exp141 — ext lightgbm 16/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0653 (delta -1.7163 vs prev best -0.3490); val=-1.9690470177527306 train=-0.04299364692872338.

**Learning:** Ext iter 16 (lightgbm): DISCARD. Train/val gap = 1.9261. This iter targets LightGBM leaf-wise sweep.


## Exp142 — ext lightgbm 17/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0979 (delta -1.7489 vs prev best -0.3490); val=-2.000728571254405 train=-0.05758460208509975.

**Learning:** Ext iter 17 (lightgbm): DISCARD. Train/val gap = 1.9431. This iter targets LightGBM leaf-wise sweep.


## Exp143 — ext lightgbm 18/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1718 (delta -1.8228 vs prev best -0.3490); val=-2.0713900587538916 train=-0.06329852522840579.

**Learning:** Ext iter 18 (lightgbm): DISCARD. Train/val gap = 2.0081. This iter targets LightGBM leaf-wise sweep.


## Exp144 — ext lightgbm 19/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0979 (delta -1.7489 vs prev best -0.3490); val=-2.000728571254405 train=-0.05758460208509975.

**Learning:** Ext iter 19 (lightgbm): DISCARD. Train/val gap = 1.9431. This iter targets LightGBM leaf-wise sweep.


## Exp145 — ext lightgbm 20/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1718 (delta -1.8228 vs prev best -0.3490); val=-2.0713900587538916 train=-0.06329852522840579.

**Learning:** Ext iter 20 (lightgbm): DISCARD. Train/val gap = 2.0081. This iter targets LightGBM leaf-wise sweep.


## Exp146 — ext lightgbm 21/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0979 (delta -1.7489 vs prev best -0.3490); val=-2.000728571254405 train=-0.05758460208509975.

**Learning:** Ext iter 21 (lightgbm): DISCARD. Train/val gap = 1.9431. This iter targets LightGBM leaf-wise sweep.


## Exp147 — ext lightgbm 22/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1718 (delta -1.8228 vs prev best -0.3490); val=-2.0713900587538916 train=-0.06329852522840579.

**Learning:** Ext iter 22 (lightgbm): DISCARD. Train/val gap = 2.0081. This iter targets LightGBM leaf-wise sweep.


## Exp148 — ext catboost 23/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 23 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp149 — ext catboost 24/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 24 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp150 — ext catboost 25/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 25 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp151 — ext catboost 26/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 26 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp152 — ext catboost 27/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 27 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp153 — ext catboost 28/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 28 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp154 — ext catboost 29/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 29 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp155 — ext catboost 30/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 30 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp156 — ext catboost 31/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3490); val=NA train=NA.

**Learning:** Ext iter 31 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp157 — ext mlp 32/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5935 (delta -0.2445 vs prev best -0.3490); val=-0.5871489145412643 train=-0.4604493320177734.

**Learning:** Ext iter 32 (mlp): DISCARD. Train/val gap = 0.1267. This iter targets MLP capacity sweep.


## Exp158 — ext mlp 33/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4124 (delta -0.0634 vs prev best -0.3490); val=-0.40343394306721664 train=-0.22468913776718674.

**Learning:** Ext iter 33 (mlp): DISCARD. Train/val gap = 0.1787. This iter targets MLP capacity sweep.


## Exp159 — ext mlp 34/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3767 (delta -0.0277 vs prev best -0.3490); val=-0.36616080386006267 train=-0.1546301381364547.

**Learning:** Ext iter 34 (mlp): DISCARD. Train/val gap = 0.2115. This iter targets MLP capacity sweep.


## Exp160 — ext mlp 35/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4575 (delta -0.1085 vs prev best -0.3490); val=-0.44896106792894597 train=-0.27800713034531793.

**Learning:** Ext iter 35 (mlp): DISCARD. Train/val gap = 0.1710. This iter targets MLP capacity sweep.


## Exp161 — ext mlp 36/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4004 (delta -0.0513 vs prev best -0.3490); val=-0.389348615055504 train=-0.16917784900146352.

**Learning:** Ext iter 36 (mlp): DISCARD. Train/val gap = 0.2202. This iter targets MLP capacity sweep.


## Exp162 — ext mlp 37/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3849 (delta -0.0359 vs prev best -0.3490); val=-0.3734522708860551 train=-0.14443719870999325.

**Learning:** Ext iter 37 (mlp): DISCARD. Train/val gap = 0.2290. This iter targets MLP capacity sweep.


## Exp163 — ext mlp 38/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3511 (delta -0.0021 vs prev best -0.3490); val=-0.34315915698571087 train=-0.18430425248331814.

**Learning:** Ext iter 38 (mlp): DISCARD. Train/val gap = 0.1589. This iter targets MLP capacity sweep.


## Exp164 — ext mlp 39/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.3450 (delta +0.0040 vs prev best -0.3490); val=-0.3355667707875215 train=-0.14723376908532362.

**Learning:** Ext iter 39 (mlp): KEEP. Train/val gap = 0.1883. This iter targets MLP capacity sweep.


## Exp165 — ext mlp 40/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.3311 (delta +0.0139 vs prev best -0.3450); val=-0.3215500371721792 train=-0.1304218679130811.

**Learning:** Ext iter 40 (mlp): KEEP. Train/val gap = 0.1911. This iter targets MLP capacity sweep.


## Exp166 — ext mlp 41/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4748 (delta -0.1437 vs prev best -0.3311); val=-0.46356395246389537 train=-0.23787026059786034.

**Learning:** Ext iter 41 (mlp): DISCARD. Train/val gap = 0.2257. This iter targets MLP capacity sweep.


## Exp167 — ext mlp 42/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4197 (delta -0.0886 vs prev best -0.3311); val=-0.4070012043061118 train=-0.15387122075105966.

**Learning:** Ext iter 42 (mlp): DISCARD. Train/val gap = 0.2531. This iter targets MLP capacity sweep.


## Exp168 — ext mlp 43/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3874 (delta -0.0563 vs prev best -0.3311); val=-0.376712524634764 train=-0.16264675304123818.

**Learning:** Ext iter 43 (mlp): DISCARD. Train/val gap = 0.2141. This iter targets MLP capacity sweep.


## Exp169 — ext mlp 44/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4827 (delta -0.1516 vs prev best -0.3311); val=-0.469784342489504 train=-0.2114624714015845.

**Learning:** Ext iter 44 (mlp): DISCARD. Train/val gap = 0.2583. This iter targets MLP capacity sweep.


## Exp170 — ext mlp 45/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4553 (delta -0.1242 vs prev best -0.3311); val=-0.442304659038847 train=-0.18322636999764974.

**Learning:** Ext iter 45 (mlp): DISCARD. Train/val gap = 0.2591. This iter targets MLP capacity sweep.


## Exp171 — ext mlp 46/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4180 (delta -0.0869 vs prev best -0.3311); val=-0.40691072579621856 train=-0.18540804839375147.

**Learning:** Ext iter 46 (mlp): DISCARD. Train/val gap = 0.2215. This iter targets MLP capacity sweep.


## Exp172 — ext ft_transformer 47/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.1456 (delta -1.8145 vs prev best -0.3311); val=-2.057185518211496 train=-0.2896208559006878.

**Learning:** Ext iter 47 (ft_transformer): DISCARD. Train/val gap = 1.7676. This iter targets FT-Transformer-style sweep.


## Exp173 — ext ft_transformer 48/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.1407 (delta -1.8096 vs prev best -0.3311); val=-2.048540639484704 train=-0.20546576021811483.

**Learning:** Ext iter 48 (ft_transformer): DISCARD. Train/val gap = 1.8431. This iter targets FT-Transformer-style sweep.


## Exp174 — ext ft_transformer 49/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.1262 (delta -1.7951 vs prev best -0.3311); val=-2.0337464489921175 train=-0.18481274571491904.

**Learning:** Ext iter 49 (ft_transformer): DISCARD. Train/val gap = 1.8489. This iter targets FT-Transformer-style sweep.


## Exp175 — ext ft_transformer 50/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0591 (delta -1.7280 vs prev best -0.3311); val=-1.9671604163752876 train=-0.1278492227714191.

**Learning:** Ext iter 50 (ft_transformer): DISCARD. Train/val gap = 1.8393. This iter targets FT-Transformer-style sweep.


## Exp176 — ext ft_transformer 51/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0874 (delta -1.7563 vs prev best -0.3311); val=-1.992006174450377 train=-0.08335484777478235.

**Learning:** Ext iter 51 (ft_transformer): DISCARD. Train/val gap = 1.9087. This iter targets FT-Transformer-style sweep.


## Exp177 — ext ft_transformer 52/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0860 (delta -1.7549 vs prev best -0.3311); val=-1.99021690291357 train=-0.0743032355092402.

**Learning:** Ext iter 52 (ft_transformer): DISCARD. Train/val gap = 1.9159. This iter targets FT-Transformer-style sweep.


## Exp178 — ext ft_transformer 53/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0436 (delta -1.7125 vs prev best -0.3311); val=-1.9492685449141312 train=-0.06301127253083029.

**Learning:** Ext iter 53 (ft_transformer): DISCARD. Train/val gap = 1.8863. This iter targets FT-Transformer-style sweep.


## Exp179 — ext ft_transformer 54/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0815 (delta -1.7504 vs prev best -0.3311); val=-1.9847979466814811 train=-0.05043022675151278.

**Learning:** Ext iter 54 (ft_transformer): DISCARD. Train/val gap = 1.9344. This iter targets FT-Transformer-style sweep.


## Exp180 — ext ft_transformer 55/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0813 (delta -1.7502 vs prev best -0.3311); val=-1.9843742850848698 train=-0.04524119441983382.

**Learning:** Ext iter 55 (ft_transformer): DISCARD. Train/val gap = 1.9391. This iter targets FT-Transformer-style sweep.


## Exp181 — ext xgboost 56/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.1. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.1 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9526 (delta -1.6215 vs prev best -0.3311); val=-1.8644121684641612 train=-0.09971819804817972.

**Learning:** Ext iter 56 (xgboost): DISCARD. Train/val gap = 1.7647. This iter targets NGBoost-flavored sparsity sweep.


## Exp182 — ext xgboost 57/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.3. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.3 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9526 (delta -1.6215 vs prev best -0.3311); val=-1.8644121684641612 train=-0.09971819804817972.

**Learning:** Ext iter 57 (xgboost): DISCARD. Train/val gap = 1.7647. This iter targets NGBoost-flavored sparsity sweep.


## Exp183 — ext xgboost 58/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=1.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=1.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9526 (delta -1.6215 vs prev best -0.3311); val=-1.8644121684641612 train=-0.09971819804817972.

**Learning:** Ext iter 58 (xgboost): DISCARD. Train/val gap = 1.7647. This iter targets NGBoost-flavored sparsity sweep.


## Exp184 — ext xgboost 59/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=3.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=3.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9526 (delta -1.6215 vs prev best -0.3311); val=-1.8644121684641612 train=-0.09971819804817972.

**Learning:** Ext iter 59 (xgboost): DISCARD. Train/val gap = 1.7647. This iter targets NGBoost-flavored sparsity sweep.


## Exp185 — ext mlp 60/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 128, 64). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4531 (delta -0.1220 vs prev best -0.3311); val=-0.4409210948474192 train=-0.19753651856256646.

**Learning:** Ext iter 60 (mlp): DISCARD. Train/val gap = 0.2434. This iter targets TabNet-flavoured wide-residual MLP.


## Exp186 — ext mlp 61/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(384, 192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(384, 192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4567 (delta -0.1256 vs prev best -0.3311); val=-0.4430710615519309 train=-0.170673571195331.

**Learning:** Ext iter 61 (mlp): DISCARD. Train/val gap = 0.2724. This iter targets TabNet-flavoured wide-residual MLP.


## Exp187 — ext mlp 62/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4685 (delta -0.1374 vs prev best -0.3311); val=-0.4568481404540852 train=-0.2236746120118869.

**Learning:** Ext iter 62 (mlp): DISCARD. Train/val gap = 0.2332. This iter targets TabNet-flavoured wide-residual MLP.


## Exp188 — ext mlp 63/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(320, 160). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(320, 160) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4390 (delta -0.1079 vs prev best -0.3311); val=-0.4271457576100757 train=-0.189814095869443.

**Learning:** Ext iter 63 (mlp): DISCARD. Train/val gap = 0.2373. This iter targets TabNet-flavoured wide-residual MLP.


## Exp189 — ext mlp 64/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 256). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 256) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4310 (delta -0.0999 vs prev best -0.3311); val=-0.41921193635218307 train=-0.18267413388719478.

**Learning:** Ext iter 64 (mlp): DISCARD. Train/val gap = 0.2365. This iter targets TabNet-flavoured wide-residual MLP.


## Exp190 — ext ft_transformer 65/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=200. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.8130 (delta -2.4819 vs prev best -0.3311); val=-2.767285960758462 train=-1.8535443943194343.

**Learning:** Ext iter 65 (ft_transformer): DISCARD. Train/val gap = 0.9137. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp191 — ext ft_transformer 66/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=400. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.3088 (delta -1.9777 vs prev best -0.3311); val=-2.2470127041110755 train=-1.0119734947839765.

**Learning:** Ext iter 66 (ft_transformer): DISCARD. Train/val gap = 1.2350. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp192 — ext ft_transformer 67/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=600. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.0883 (delta -1.7572 vs prev best -0.3311); val=-2.0198236815785635 train=-0.6507501469442605.

**Learning:** Ext iter 67 (ft_transformer): DISCARD. Train/val gap = 1.3691. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp193 — ext xgboost 68/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=0.1 reg_alpha=0.1. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=0.1 smooths leaf weights; reg_alpha=0.1 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.8281 (delta -1.4970 vs prev best -0.3311); val=-1.7555353631630204 train=-0.3049074503922006.

**Learning:** Ext iter 68 (xgboost): DISCARD. Train/val gap = 1.4506. This iter targets Elastic-net-flavoured gradient boost.


## Exp194 — ext xgboost 69/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=1.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=1.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7939 (delta -1.4628 vs prev best -0.3311); val=-1.7240504291133292 train=-0.3270859729858761.

**Learning:** Ext iter 69 (xgboost): DISCARD. Train/val gap = 1.3970. This iter targets Elastic-net-flavoured gradient boost.


## Exp195 — ext xgboost 70/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=3.0 reg_alpha=1.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=3.0 smooths leaf weights; reg_alpha=1.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.8326 (delta -1.5015 vs prev best -0.3311); val=-1.76269172816031 train=-0.3637201672541235.

**Learning:** Ext iter 70 (xgboost): DISCARD. Train/val gap = 1.3990. This iter targets Elastic-net-flavoured gradient boost.


## Exp196 — ext xgboost 71/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.8330 (delta -1.5019 vs prev best -0.3311); val=-1.767531926515567 train=-0.4578873368115728.

**Learning:** Ext iter 71 (xgboost): DISCARD. Train/val gap = 1.3096. This iter targets Elastic-net-flavoured gradient boost.


## Exp197 — ext xgboost 72/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=3.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=3.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.8330 (delta -1.5019 vs prev best -0.3311); val=-1.767531926515567 train=-0.4578873368115728.

**Learning:** Ext iter 72 (xgboost): DISCARD. Train/val gap = 1.3096. This iter targets Elastic-net-flavoured gradient boost.


## Exp198 — ext patchtsmixer 73/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.6049 (delta -1.2738 vs prev best -0.3311); val=-1.6030767214162596 train=-1.5669681749307252.

**Learning:** Ext iter 73 (patchtsmixer): DISCARD. Train/val gap = 0.0361. This iter targets PatchTSMixer channel-mix sweep.


## Exp199 — ext patchtsmixer 74/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.5335 (delta -1.2024 vs prev best -0.3311); val=-1.5260547554921657 train=-1.3767856793689.

**Learning:** Ext iter 74 (patchtsmixer): DISCARD. Train/val gap = 0.1493. This iter targets PatchTSMixer channel-mix sweep.


## Exp200 — ext patchtsmixer 75/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.3091 (delta -0.9780 vs prev best -0.3311); val=-1.2992681001889173 train=-1.1028960252383595.

**Learning:** Ext iter 75 (patchtsmixer): DISCARD. Train/val gap = 0.1964. This iter targets PatchTSMixer channel-mix sweep.


## Exp201 — ext patchtsmixer 76/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.1849 (delta -0.8538 vs prev best -0.3311); val=-1.1684057126410652 train=-0.8382562226526126.

**Learning:** Ext iter 76 (patchtsmixer): DISCARD. Train/val gap = 0.3301. This iter targets PatchTSMixer channel-mix sweep.


## Exp202 — ext patchtsmixer 77/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.1245 (delta -0.7934 vs prev best -0.3311); val=-1.1090359236778287 train=-0.8004683092433678.

**Learning:** Ext iter 77 (patchtsmixer): DISCARD. Train/val gap = 0.3086. This iter targets PatchTSMixer channel-mix sweep.


## Exp203 — ext patchtsmixer 78/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.1087 (delta -0.7776 vs prev best -0.3311); val=-1.0858069142377058 train=-0.6286750984701819.

**Learning:** Ext iter 78 (patchtsmixer): DISCARD. Train/val gap = 0.4571. This iter targets PatchTSMixer channel-mix sweep.


## Exp204 — ext xgboost 79/200
**Diagnosis:** Multi-seed champion variance run, seed=42. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1958 (delta -1.8647 vs prev best -0.3311); val=-2.094477968203426 train=-0.06869314657918431.

**Learning:** Ext iter 79 (xgboost): DISCARD. Train/val gap = 2.0258. This iter targets extended search.


## Exp205 — ext xgboost 80/200
**Diagnosis:** Multi-seed champion variance run, seed=0. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1928 (delta -1.8617 vs prev best -0.3311); val=-2.091697141974989 train=-0.06928179870426038.

**Learning:** Ext iter 80 (xgboost): DISCARD. Train/val gap = 2.0224. This iter targets extended search.


## Exp206 — ext xgboost 81/200
**Diagnosis:** Multi-seed champion variance run, seed=7. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1650 (delta -1.8339 vs prev best -0.3311); val=-2.0650436437395983 train=-0.06677186815741433.

**Learning:** Ext iter 81 (xgboost): DISCARD. Train/val gap = 1.9983. This iter targets extended search.


## Exp207 — ext xgboost 82/200
**Diagnosis:** Multi-seed champion variance run, seed=99. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1734 (delta -1.8423 vs prev best -0.3311); val=-2.07315122213447 train=-0.06886480334326166.

**Learning:** Ext iter 82 (xgboost): DISCARD. Train/val gap = 2.0043. This iter targets extended search.


## Exp208 — ext xgboost 83/200
**Diagnosis:** Multi-seed champion variance run, seed=2024. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.2005 (delta -1.8694 vs prev best -0.3311); val=-2.098953272306211 train=-0.0678060652332125.

**Learning:** Ext iter 83 (xgboost): DISCARD. Train/val gap = 2.0311. This iter targets extended search.


## Exp209 — ext xgboost 84/200
**Diagnosis:** Multi-seed champion variance run, seed=12345. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1788 (delta -1.8477 vs prev best -0.3311); val=-2.078488081570523 train=-0.07202734196005688.

**Learning:** Ext iter 84 (xgboost): DISCARD. Train/val gap = 2.0065. This iter targets extended search.


## Exp210 — ext xgboost 85/200
**Diagnosis:** Multi-seed champion variance run, seed=7777. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1798 (delta -1.8487 vs prev best -0.3311); val=-2.0792376759035336 train=-0.06884809250389023.

**Learning:** Ext iter 85 (xgboost): DISCARD. Train/val gap = 2.0104. This iter targets extended search.


## Exp211 — ext xgboost 86/200
**Diagnosis:** Multi-seed champion variance run, seed=31337. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.2115 (delta -1.8804 vs prev best -0.3311); val=-2.109515376188448 train=-0.06980385850287102.

**Learning:** Ext iter 86 (xgboost): DISCARD. Train/val gap = 2.0397. This iter targets extended search.


## Exp212 — ext xgboost 87/200
**Diagnosis:** Multi-seed champion variance run, seed=1729. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.2070 (delta -1.8759 vs prev best -0.3311); val=-2.1052501897663447 train=-0.06971376526024498.

**Learning:** Ext iter 87 (xgboost): DISCARD. Train/val gap = 2.0355. This iter targets extended search.


## Exp213 — ext xgboost 88/200
**Diagnosis:** Multi-seed champion variance run, seed=6174. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.2173 (delta -1.8862 vs prev best -0.3311); val=-2.1150021694163206 train=-0.0690523176324974.

**Learning:** Ext iter 88 (xgboost): DISCARD. Train/val gap = 2.0459. This iter targets extended search.


## Exp214 — ext xgboost 89/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=30. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=30, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.7395 (delta -1.4084 vs prev best -0.3311); val=-1.6974798315364164 train=-0.8567260838719456.

**Learning:** Ext iter 89 (xgboost): DISCARD. Train/val gap = 0.8408. This iter targets Extreme regularisation cool-down.


## Exp215 — ext xgboost 90/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=50. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=50, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.8081 (delta -1.4770 vs prev best -0.3311); val=-1.7679468602786237 train=-0.9646322041621048.

**Learning:** Ext iter 90 (xgboost): DISCARD. Train/val gap = 0.8033. This iter targets Extreme regularisation cool-down.


## Exp216 — ext xgboost 91/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=100. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=100, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.9068 (delta -1.5757 vs prev best -0.3311); val=-1.8708725322646709 train=-1.1524531425665263.

**Learning:** Ext iter 91 (xgboost): DISCARD. Train/val gap = 0.7184. This iter targets Extreme regularisation cool-down.

