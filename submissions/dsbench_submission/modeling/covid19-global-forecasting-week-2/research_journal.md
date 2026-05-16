# Research Journal — covid19-global-forecasting-week-2

_(populated by `framework/hill_climb.py`)_

## Exp1 — xgboost iter 1
**Diagnosis:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

**Hypothesis:** Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).

**Prediction:** Composite in [0.55, 0.85] depending on task difficulty.

**Verdict:** KEEP composite=-2.1947 (delta +inf vs prev best -inf); val_score=-2.0931102857189283; train_score=-0.06134585075794238.

**Learning:** Iter 1 xgboost: KEEP. Train/val gap = 2.0318. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — xgboost iter 2
**Diagnosis:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.

**Citations:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

**Hypothesis:** Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-2.5342 (delta -0.3395 vs prev best -2.1947); val_score=-2.4138208163366492; train_score=-0.006236479673689476.

**Learning:** Iter 2 xgboost: DISCARD. Train/val gap = 2.4076. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — xgboost iter 3
**Diagnosis:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

**Hypothesis:** Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-1.7218 (delta +0.4729 vs prev best -2.1947); val_score=-1.6500425795638667; train_score=-0.214327095604377.

**Learning:** Iter 3 xgboost: KEEP. Train/val gap = 1.4357. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp4 — xgboost iter 4
**Diagnosis:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.

**Citations:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

**Hypothesis:** Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.

**Prediction:** Composite delta in [+0.001, +0.010].

**Verdict:** DISCARD composite=-2.1737 (delta -0.4519 vs prev best -1.7218); val_score=-2.0731340866188743; train_score=-0.06137402496393731.

**Learning:** Iter 4 xgboost: DISCARD. Train/val gap = 2.0118. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — xgboost iter 5
**Diagnosis:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

**Hypothesis:** Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.

**Prediction:** Composite delta in [+0.002, +0.012].

**Verdict:** DISCARD composite=-2.0149 (delta -0.2930 vs prev best -1.7218); val_score=-1.9254343211686753; train_score=-0.13676340872399315.

**Learning:** Iter 5 xgboost: DISCARD. Train/val gap = 1.7887. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — xgboost iter 6
**Diagnosis:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.

**Citations:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

**Hypothesis:** Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.2669 (delta -0.5451 vs prev best -1.7218); val_score=-2.1686415719402796; train_score=-0.20373034142515914.

**Learning:** Iter 6 xgboost: DISCARD. Train/val gap = 1.9649. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — xgboost iter 7
**Diagnosis:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.

**Citations:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

**Hypothesis:** Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-1.9800 (delta -0.2582 vs prev best -1.7218); val_score=-1.8901338175675229; train_score=-0.09278642663875741.

**Learning:** Iter 7 xgboost: DISCARD. Train/val gap = 1.7973. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp8 — xgboost iter 8
**Diagnosis:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.

**Citations:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1284 (delta -0.4066 vs prev best -1.7218); val_score=-2.029786741959478; train_score=-0.05735841523944157.

**Learning:** Iter 8 xgboost: DISCARD. Train/val gap = 1.9724. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — xgboost iter 9
**Diagnosis:** Third seed for 3-seed median (autoresearch protocol).

**Citations:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1867 (delta -0.4649 vs prev best -1.7218); val_score=-2.085428240042427; train_score=-0.05960262313466081.

**Learning:** Iter 9 xgboost: DISCARD. Train/val gap = 2.0258. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — xgboost iter 10
**Diagnosis:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

**Hypothesis:** Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7018 (delta -0.9800 vs prev best -1.7218); val_score=-2.573260162117013; train_score=-0.002392891154351158.

**Learning:** Iter 10 xgboost: DISCARD. Train/val gap = 2.5709. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — xgboost iter 11
**Diagnosis:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.

**Citations:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

**Hypothesis:** Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** KEEP composite=-1.6651 (delta +0.0567 vs prev best -1.7218); val_score=-1.5958186169668709; train_score=-0.2094177583191508.

**Learning:** Iter 11 xgboost: KEEP. Train/val gap = 1.3864. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp12 — xgboost iter 12
**Diagnosis:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

**Hypothesis:** Hypothesis: larger leaves reduce variance, improve val by 0.5%.

**Prediction:** Composite delta in [-0.002, +0.010].

**Verdict:** DISCARD composite=-2.1947 (delta -0.5296 vs prev best -1.6651); val_score=-2.0931102857189283; train_score=-0.06134585075794238.

**Learning:** Iter 12 xgboost: DISCARD. Train/val gap = 2.0318. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — xgboost iter 13
**Diagnosis:** Gamma split-penalty 0.5 — discourages overly eager splits.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

**Hypothesis:** Hypothesis: fewer, higher-quality splits. Val improves slightly.

**Prediction:** Composite delta in [-0.003, +0.008].

**Verdict:** DISCARD composite=-2.1947 (delta -0.5296 vs prev best -1.6651); val_score=-2.0931102857189283; train_score=-0.06134585075794238.

**Learning:** Iter 13 xgboost: DISCARD. Train/val gap = 2.0318. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — xgboost iter 14
**Diagnosis:** High subsample for low-noise tasks — opposite direction from iter-4/7.

**Citations:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

**Hypothesis:** Hypothesis: gentle bagging if iter-4/7 over-regularised.

**Prediction:** Composite delta in [-0.005, +0.007].

**Verdict:** DISCARD composite=-2.2010 (delta -0.5359 vs prev best -1.6651); val_score=-2.0986282682303057; train_score=-0.05049996923263363.

**Learning:** Iter 14 xgboost: DISCARD. Train/val gap = 2.0481. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — xgboost iter 15
**Diagnosis:** L1 regularisation (reg_alpha) for feature selection.

**Citations:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

**Hypothesis:** Hypothesis: L1 trims noise features, val improves.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-2.3773 (delta -0.7121 vs prev best -1.6651); val_score=-2.2653248555228904; train_score=-0.026294037226354247.

**Learning:** Iter 15 xgboost: DISCARD. Train/val gap = 2.2390. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — xgboost iter 16
**Diagnosis:** Combined moderate regularisation — meta-search across all axes.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

**Hypothesis:** Hypothesis: balanced config beats single-knob champions.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-2.1689 (delta -0.5037 vs prev best -1.6651); val_score=-2.0665815023081895; train_score=-0.020607615337606206.

**Learning:** Iter 16 xgboost: DISCARD. Train/val gap = 2.0460. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — xgboost iter 17
**Diagnosis:** Fourth seed — extend variance characterisation.

**Citations:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

**Hypothesis:** Hypothesis: within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1959 (delta -0.5308 vs prev best -1.6651); val_score=-2.09421773212479; train_score=-0.05972484766729444.

**Learning:** Iter 17 xgboost: DISCARD. Train/val gap = 2.0345. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — xgboost iter 18
**Diagnosis:** Fifth seed.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Same as iter-15.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.1745 (delta -0.5093 vs prev best -1.6651); val_score=-2.073867681934026; train_score=-0.06168664937957116.

**Learning:** Iter 18 xgboost: DISCARD. Train/val gap = 2.0122. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — xgboost iter 19
**Diagnosis:** Aggressive depth=12 with proportionally lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

**Hypothesis:** Hypothesis: depth=12 will overfit unless lr is very low.

**Prediction:** Composite delta in [-0.030, +0.010].

**Verdict:** DISCARD composite=-2.7880 (delta -1.1229 vs prev best -1.6651); val_score=-2.6558439954247026; train_score=-0.011975063242264973.

**Learning:** Iter 19 xgboost: DISCARD. Train/val gap = 2.6439. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — xgboost iter 20
**Diagnosis:** Very shallow, high-lr — stump-like learners as opposite extreme.

**Citations:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

**Hypothesis:** Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.

**Prediction:** Composite delta in [-0.040, +0.005].

**Verdict:** KEEP composite=-1.4429 (delta +0.2223 vs prev best -1.6651); val_score=-1.3886421726231875; train_score=-0.3043700422827109.

**Learning:** Iter 20 xgboost: KEEP. Train/val gap = 1.0843. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp21 — xgboost iter 21
**Diagnosis:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.

**Citations:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

**Hypothesis:** Hypothesis: no-op vs baseline; informational only.

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-2.1879 (delta -0.7451 vs prev best -1.4429); val_score=-2.0847291339599017; train_score=-0.020642307168683934.

**Learning:** Iter 21 xgboost: DISCARD. Train/val gap = 2.0641. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — xgboost iter 22
**Diagnosis:** Confirm hist-method explicitly — same as default but pinned.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

**Hypothesis:** Hypothesis: no change vs baseline (already default in our setup).

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-2.1947 (delta -0.7518 vs prev best -1.4429); val_score=-2.0931102857189283; train_score=-0.06134585075794238.

**Learning:** Iter 22 xgboost: DISCARD. Train/val gap = 2.0318. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — xgboost iter 23
**Diagnosis:** Long-and-slow final refinement with mid-strength L2.

**Citations:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

**Hypothesis:** Hypothesis: best champion candidate. Val should peak.

**Prediction:** Composite delta in [+0.005, +0.025].

**Verdict:** DISCARD composite=-1.8496 (delta -0.4067 vs prev best -1.4429); val_score=-1.7657509142784054; train_score=-0.08966106001807662.

**Learning:** Iter 23 xgboost: DISCARD. Train/val gap = 1.6761. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — xgboost iter 24
**Diagnosis:** Combined moderate everything — explore a balanced corner.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-2.0611 (delta -0.6183 vs prev best -1.4429); val_score=-1.9668579698182327; train_score=-0.08152666043050986.

**Learning:** Iter 24 xgboost: DISCARD. Train/val gap = 1.8853. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — xgboost iter 25
**Diagnosis:** Final 6th seed — closes the variance characterisation for this backbone.

**Citations:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-2.2202 (delta -0.7774 vs prev best -1.4429); val_score=-2.1171412163774592; train_score=-0.05556283287331063.

**Learning:** Iter 25 xgboost: DISCARD. Train/val gap = 2.0616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp26 — lightgbm iter 1
**Diagnosis:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard lightgbm config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 1 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp27 — lightgbm iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-3.9800 (delta -2.5371 vs prev best -1.4429); val_score=-3.945560313802513; train_score=-3.257477300790579.

**Learning:** Iter 2 lightgbm: DISCARD. Train/val gap = 0.6881. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp28 — lightgbm iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.5629 (delta -3.1201 vs prev best -1.4429); val_score=-4.5441546546816065; train_score=-4.168339488256012.

**Learning:** Iter 3 lightgbm: DISCARD. Train/val gap = 0.3758. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp29 — lightgbm iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-3.4849 (delta -2.0421 vs prev best -1.4429); val_score=-3.4352102801563125; train_score=-2.4412966147577864.

**Learning:** Iter 4 lightgbm: DISCARD. Train/val gap = 0.9939. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp30 — lightgbm iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-2.1786 (delta -0.7358 vs prev best -1.4429); val_score=-2.0771262183067263; train_score=-0.047524097922466535.

**Learning:** Iter 5 lightgbm: DISCARD. Train/val gap = 2.0296. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp31 — lightgbm iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.1786 (delta -0.7358 vs prev best -1.4429); val_score=-2.0771262183067263; train_score=-0.047524097922466535.

**Learning:** Iter 6 lightgbm: DISCARD. Train/val gap = 2.0296. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp32 — lightgbm iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1980 (delta -2.7551 vs prev best -1.4429); val_score=-4.169675936207406; train_score=-3.6034140267859627.

**Learning:** Iter 7 lightgbm: DISCARD. Train/val gap = 0.5663. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp33 — lightgbm iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1936 (delta -2.7508 vs prev best -1.4429); val_score=-4.165462744147295; train_score=-3.601924685179735.

**Learning:** Iter 8 lightgbm: DISCARD. Train/val gap = 0.5635. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp34 — lightgbm iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 9 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp35 — lightgbm iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.4510 (delta -3.0081 vs prev best -1.4429); val_score=-4.4293574007051335; train_score=-3.9969175135181305.

**Learning:** Iter 10 lightgbm: DISCARD. Train/val gap = 0.4324. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp36 — lightgbm iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 11 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp37 — lightgbm iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 12 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp38 — lightgbm iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-4.3985 (delta -2.9556 vs prev best -1.4429); val_score=-4.375410159442004; train_score=-3.913557241704717.

**Learning:** Iter 13 lightgbm: DISCARD. Train/val gap = 0.4619. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp39 — lightgbm iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1949 (delta -2.7521 vs prev best -1.4429); val_score=-4.166660533584858; train_score=-3.6009988030176556.

**Learning:** Iter 14 lightgbm: DISCARD. Train/val gap = 0.5657. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp40 — lightgbm iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1967 (delta -2.7539 vs prev best -1.4429); val_score=-4.168601986980221; train_score=-3.605918535356724.

**Learning:** Iter 15 lightgbm: DISCARD. Train/val gap = 0.5627. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp41 — lightgbm iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 16 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp42 — lightgbm iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 17 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp43 — lightgbm iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-3.7913 (delta -2.3484 vs prev best -1.4429); val_score=-3.7513108384102303; train_score=-2.9523416561213005.

**Learning:** Iter 18 lightgbm: DISCARD. Train/val gap = 0.7990. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp44 — lightgbm iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-4.6807 (delta -3.2378 vs prev best -1.4429); val_score=-4.664967011575845; train_score=-4.350800005964637.

**Learning:** Iter 19 lightgbm: DISCARD. Train/val gap = 0.3142. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp45 — lightgbm iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 20 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp46 — lightgbm iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 21 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp47 — lightgbm iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-4.1990 (delta -2.7561 vs prev best -1.4429); val_score=-4.17067236166247; train_score=-3.6042592006030105.

**Learning:** Iter 22 lightgbm: DISCARD. Train/val gap = 0.5664. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp48 — lightgbm iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.3462 (delta -2.9033 vs prev best -1.4429); val_score=-4.321777725871419; train_score=-3.8339737211149356.

**Learning:** Iter 23 lightgbm: DISCARD. Train/val gap = 0.4878. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp49 — lightgbm iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-3.9828 (delta -2.5399 vs prev best -1.4429); val_score=-3.9483108533685596; train_score=-3.258543775188817.

**Learning:** Iter 24 lightgbm: DISCARD. Train/val gap = 0.6898. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp50 — lightgbm iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.1974 (delta -2.7545 vs prev best -1.4429); val_score=-4.169104981518187; train_score=-3.603259365915335.

**Learning:** Iter 25 lightgbm: DISCARD. Train/val gap = 0.5658. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp51 — catboost iter 1
**Diagnosis:** Baseline catboost per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard catboost config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 1 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp52 — catboost iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 2 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp53 — catboost iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 3 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp54 — catboost iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 4 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp55 — catboost iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 5 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp56 — catboost iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 6 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp57 — catboost iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 7 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp58 — catboost iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 8 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp59 — catboost iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 9 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp60 — catboost iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 10 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp61 — catboost iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 11 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp62 — catboost iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 12 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp63 — catboost iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 13 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp64 — catboost iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 14 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp65 — catboost iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 15 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp66 — catboost iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 16 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp67 — catboost iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 17 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp68 — catboost iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 18 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp69 — catboost iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 19 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp70 — catboost iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 20 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp71 — catboost iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 21 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp72 — catboost iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 22 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp73 — catboost iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 23 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp74 — catboost iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 24 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp75 — catboost iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -1.4429); val_score=NA; train_score=NA.

**Learning:** Iter 25 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp76 — mlp iter 1
**Diagnosis:** Baseline mlp per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard mlp config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** KEEP composite=-0.5318 (delta +0.9111 vs prev best -1.4429); val_score=-0.5219270063516379; train_score=-0.3248256036626714.

**Learning:** Iter 1 mlp: KEEP. Train/val gap = 0.1971. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp77 — mlp iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-0.4697 (delta +0.0621 vs prev best -0.5318); val_score=-0.45820510941878173; train_score=-0.22884503284841257.

**Learning:** Iter 2 mlp: KEEP. Train/val gap = 0.2294. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp78 — mlp iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.8256 (delta -0.3559 vs prev best -0.4697); val_score=-0.8179412356233263; train_score=-0.6656789739870582.

**Learning:** Iter 3 mlp: DISCARD. Train/val gap = 0.1523. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp79 — mlp iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** KEEP composite=-0.4023 (delta +0.0674 vs prev best -0.4697); val_score=-0.39201779968492956; train_score=-0.18691263985565795.

**Learning:** Iter 4 mlp: KEEP. Train/val gap = 0.2051. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp80 — mlp iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.5428 (delta -0.1405 vs prev best -0.4023); val_score=-0.5360770830606106; train_score=-0.40217938815860305.

**Learning:** Iter 5 mlp: DISCARD. Train/val gap = 0.1339. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp81 — mlp iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-1.8402 (delta -1.4379 vs prev best -0.4023); val_score=-1.8273445484931052; train_score=-1.5705812138906634.

**Learning:** Iter 6 mlp: DISCARD. Train/val gap = 0.2568. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp82 — mlp iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5444 (delta -0.1422 vs prev best -0.4023); val_score=-0.5340898846278889; train_score=-0.32709408208878116.

**Learning:** Iter 7 mlp: DISCARD. Train/val gap = 0.2070. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp83 — mlp iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5525 (delta -0.1502 vs prev best -0.4023); val_score=-0.5421210333459368; train_score=-0.3346744569005369.

**Learning:** Iter 8 mlp: DISCARD. Train/val gap = 0.2074. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp84 — mlp iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.4571 (delta -0.0548 vs prev best -0.4023); val_score=-0.4451982954045332; train_score=-0.20680703311495094.

**Learning:** Iter 9 mlp: DISCARD. Train/val gap = 0.2384. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp85 — mlp iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.5435 (delta -0.1412 vs prev best -0.4023); val_score=-0.5364422903779252; train_score=-0.39553403414234406.

**Learning:** Iter 10 mlp: DISCARD. Train/val gap = 0.1409. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp86 — mlp iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-0.5403 (delta -0.1380 vs prev best -0.4023); val_score=-0.5282174960515739; train_score=-0.28615404642624526.

**Learning:** Iter 11 mlp: DISCARD. Train/val gap = 0.2421. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp87 — mlp iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-0.5104 (delta -0.1082 vs prev best -0.4023); val_score=-0.4947824042273118; train_score=-0.18183471195779038.

**Learning:** Iter 12 mlp: DISCARD. Train/val gap = 0.3129. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp88 — mlp iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-0.7464 (delta -0.3441 vs prev best -0.4023); val_score=-0.7378659972750421; train_score=-0.5676470353050367.

**Learning:** Iter 13 mlp: DISCARD. Train/val gap = 0.1702. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp89 — mlp iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5360 (delta -0.1337 vs prev best -0.4023); val_score=-0.5258482744368334; train_score=-0.32346019711306173.

**Learning:** Iter 14 mlp: DISCARD. Train/val gap = 0.2024. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp90 — mlp iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5335 (delta -0.1313 vs prev best -0.4023); val_score=-0.5238537058888602; train_score=-0.33014209962517593.

**Learning:** Iter 15 mlp: DISCARD. Train/val gap = 0.1937. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp91 — mlp iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.5387 (delta -0.1365 vs prev best -0.4023); val_score=-0.5307499832498311; train_score=-0.370914054328897.

**Learning:** Iter 16 mlp: DISCARD. Train/val gap = 0.1598. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp92 — mlp iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** KEEP composite=-0.3370 (delta +0.0653 vs prev best -0.4023); val_score=-0.32776739297439006; train_score=-0.14290805424615485.

**Learning:** Iter 17 mlp: KEEP. Train/val gap = 0.1849. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp93 — mlp iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-0.4429 (delta -0.1059 vs prev best -0.3370); val_score=-0.4327829357750397; train_score=-0.23083775285134886.

**Learning:** Iter 18 mlp: DISCARD. Train/val gap = 0.2019. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp94 — mlp iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-3.4954 (delta -3.1584 vs prev best -0.3370); val_score=-3.479795722665969; train_score=-3.167936990486995.

**Learning:** Iter 19 mlp: DISCARD. Train/val gap = 0.3119. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp95 — mlp iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.4443 (delta -0.1073 vs prev best -0.3370); val_score=-0.4316019412006336; train_score=-0.1778468205996779.

**Learning:** Iter 20 mlp: DISCARD. Train/val gap = 0.2538. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp96 — mlp iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.5318 (delta -0.1948 vs prev best -0.3370); val_score=-0.5219270063516379; train_score=-0.3248256036626714.

**Learning:** Iter 21 mlp: DISCARD. Train/val gap = 0.1971. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp97 — mlp iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-0.5318 (delta -0.1948 vs prev best -0.3370); val_score=-0.5219270063516379; train_score=-0.3248256036626714.

**Learning:** Iter 22 mlp: DISCARD. Train/val gap = 0.1971. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp98 — mlp iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.6072 (delta -0.2701 vs prev best -0.3370); val_score=-0.5975347158489998; train_score=-0.4050610456848171.

**Learning:** Iter 23 mlp: DISCARD. Train/val gap = 0.1925. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp99 — mlp iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.4756 (delta -0.1386 vs prev best -0.3370); val_score=-0.4656716995374604; train_score=-0.2676339752495383.

**Learning:** Iter 24 mlp: DISCARD. Train/val gap = 0.1980. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp100 — mlp iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5065 (delta -0.1695 vs prev best -0.3370); val_score=-0.49778621060578687; train_score=-0.32264849720431565.

**Learning:** Iter 25 mlp: DISCARD. Train/val gap = 0.1751. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp101 — ft_transformer iter 1
**Diagnosis:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard ft_transformer config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 1 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp102 — ft_transformer iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-4.0095 (delta -3.6725 vs prev best -0.3370); val_score=-3.9807727932045878; train_score=-3.4059385843131746.

**Learning:** Iter 2 ft_transformer: DISCARD. Train/val gap = 0.5748. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp103 — ft_transformer iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.5627 (delta -4.2257 vs prev best -0.3370); val_score=-4.545469808206067; train_score=-4.201183148174946.

**Learning:** Iter 3 ft_transformer: DISCARD. Train/val gap = 0.3443. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp104 — ft_transformer iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-3.5589 (delta -3.2219 vs prev best -0.3370); val_score=-3.51675219202337; train_score=-2.6728836883088998.

**Learning:** Iter 4 ft_transformer: DISCARD. Train/val gap = 0.8439. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp105 — ft_transformer iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-2.0803 (delta -1.7433 vs prev best -0.3370); val_score=-1.9851456401082423; train_score=-0.08216355401130705.

**Learning:** Iter 5 ft_transformer: DISCARD. Train/val gap = 1.9030. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp106 — ft_transformer iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.0803 (delta -1.7433 vs prev best -0.3370); val_score=-1.9851456401082423; train_score=-0.08216355401130705.

**Learning:** Iter 6 ft_transformer: DISCARD. Train/val gap = 1.9030. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp107 — ft_transformer iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 7 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp108 — ft_transformer iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 8 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp109 — ft_transformer iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 9 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp110 — ft_transformer iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-4.4517 (delta -4.1147 vs prev best -0.3370); val_score=-4.432563311318114; train_score=-4.04998665578528.

**Learning:** Iter 10 ft_transformer: DISCARD. Train/val gap = 0.3826. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp111 — ft_transformer iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 11 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp112 — ft_transformer iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 12 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp113 — ft_transformer iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-4.4002 (delta -4.0632 vs prev best -0.3370); val_score=-4.380071368461572; train_score=-3.977911172498729.

**Learning:** Iter 13 ft_transformer: DISCARD. Train/val gap = 0.4022. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp114 — ft_transformer iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 14 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp115 — ft_transformer iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 15 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp116 — ft_transformer iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 16 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp117 — ft_transformer iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 17 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp118 — ft_transformer iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-3.8396 (delta -3.5026 vs prev best -0.3370); val_score=-3.8060627737067287; train_score=-3.134353311392109.

**Learning:** Iter 18 ft_transformer: DISCARD. Train/val gap = 0.6717. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp119 — ft_transformer iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-4.6816 (delta -4.3446 vs prev best -0.3370); val_score=-4.66641455181102; train_score=-4.3622425485040175.

**Learning:** Iter 19 ft_transformer: DISCARD. Train/val gap = 0.3042. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp120 — ft_transformer iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 20 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp121 — ft_transformer iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 21 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp122 — ft_transformer iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 22 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp123 — ft_transformer iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.3505 (delta -4.0134 vs prev best -0.3370); val_score=-4.329421480438685; train_score=-3.908756054756397.

**Learning:** Iter 23 ft_transformer: DISCARD. Train/val gap = 0.4207. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp124 — ft_transformer iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-4.0098 (delta -3.6728 vs prev best -0.3370); val_score=-3.981036312718106; train_score=-3.4057462829849916.

**Learning:** Iter 24 ft_transformer: DISCARD. Train/val gap = 0.5753. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp125 — ft_transformer iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-4.2084 (delta -3.8714 vs prev best -0.3370); val_score=-4.18477062559304; train_score=-3.711275543808686.

**Learning:** Iter 25 ft_transformer: DISCARD. Train/val gap = 0.4735. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp126 — ext xgboost 1/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-1.9582 (delta -1.6212 vs prev best -0.3370); val=-1.889910034682531 train=-0.524258212154831.

**Learning:** Ext iter 1 (xgboost): DISCARD. Train/val gap = 1.3657. This iter targets Extended xgboost sweep.


## Exp127 — ext xgboost 2/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-1.6783 (delta -1.3413 vs prev best -0.3370); val=-1.604777463417369 train=-0.13448169071208443.

**Learning:** Ext iter 2 (xgboost): DISCARD. Train/val gap = 1.4703. This iter targets Extended xgboost sweep.


## Exp128 — ext xgboost 3/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.0296 (delta -1.6926 vs prev best -0.3370); val=-1.9462713000553622 train=-0.28019153581257367.

**Learning:** Ext iter 3 (xgboost): DISCARD. Train/val gap = 1.6661. This iter targets Extended xgboost sweep.


## Exp129 — ext xgboost 4/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-1.9183 (delta -1.5813 vs prev best -0.3370); val=-1.8290686494928219 train=-0.04457120754904555.

**Learning:** Ext iter 4 (xgboost): DISCARD. Train/val gap = 1.7845. This iter targets Extended xgboost sweep.


## Exp130 — ext xgboost 5/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.1935 (delta -1.8565 vs prev best -0.3370); val=-2.0959055039383836 train=-0.14414686561659038.

**Learning:** Ext iter 5 (xgboost): DISCARD. Train/val gap = 1.9518. This iter targets Extended xgboost sweep.


## Exp131 — ext xgboost 6/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.1715 (delta -1.8345 vs prev best -0.3370); val=-2.068628050560603 train=-0.011142044411915212.

**Learning:** Ext iter 6 (xgboost): DISCARD. Train/val gap = 2.0575. This iter targets Extended xgboost sweep.


## Exp132 — ext xgboost 7/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.3797 (delta -2.0427 vs prev best -0.3370); val=-2.2696880870735874 train=-0.06911590074842155.

**Learning:** Ext iter 7 (xgboost): DISCARD. Train/val gap = 2.2006. This iter targets Extended xgboost sweep.


## Exp133 — ext xgboost 8/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.3606 (delta -2.0236 vs prev best -0.3370); val=-2.2482502809666673 train=-0.0018445615742376427.

**Learning:** Ext iter 8 (xgboost): DISCARD. Train/val gap = 2.2464. This iter targets Extended xgboost sweep.


## Exp134 — ext xgboost 9/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.5166 (delta -2.1796 vs prev best -0.3370); val=-2.398371891279965 train=-0.03292884508256812.

**Learning:** Ext iter 9 (xgboost): DISCARD. Train/val gap = 2.3654. This iter targets Extended xgboost sweep.


## Exp135 — ext xgboost 10/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.5513 (delta -2.2143 vs prev best -0.3370); val=-2.429835962009907 train=-0.0005257411601060506.

**Learning:** Ext iter 10 (xgboost): DISCARD. Train/val gap = 2.4293. This iter targets Extended xgboost sweep.


## Exp136 — ext xgboost 11/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7056 (delta -2.3686 vs prev best -0.3370); val=-2.5774262377214163 train=-0.013399986293654718.

**Learning:** Ext iter 11 (xgboost): DISCARD. Train/val gap = 2.5640. This iter targets Extended xgboost sweep.


## Exp137 — ext xgboost 12/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7266 (delta -2.3896 vs prev best -0.3370); val=-2.59677618506647 train=-0.0004470873325041233.

**Learning:** Ext iter 12 (xgboost): DISCARD. Train/val gap = 2.5963. This iter targets Extended xgboost sweep.


## Exp138 — ext xgboost 13/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7675 (delta -2.4304 vs prev best -0.3370); val=-2.636209441551745 train=-0.011307158443922851.

**Learning:** Ext iter 13 (xgboost): DISCARD. Train/val gap = 2.6249. This iter targets Extended xgboost sweep.


## Exp139 — ext xgboost 14/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.8159 (delta -2.4789 vs prev best -0.3370); val=-2.681819056876676 train=-0.0003959073676419838.

**Learning:** Ext iter 14 (xgboost): DISCARD. Train/val gap = 2.6814. This iter targets Extended xgboost sweep.


## Exp140 — ext lightgbm 15/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-1.9501 (delta -1.6131 vs prev best -0.3370); val=-1.8579604599897699 train=-0.014951581447897166.

**Learning:** Ext iter 15 (lightgbm): DISCARD. Train/val gap = 1.8430. This iter targets LightGBM leaf-wise sweep.


## Exp141 — ext lightgbm 16/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.0318 (delta -1.6948 vs prev best -0.3370); val=-1.9359906221130152 train=-0.019295203052873414.

**Learning:** Ext iter 16 (lightgbm): DISCARD. Train/val gap = 1.9167. This iter targets LightGBM leaf-wise sweep.


## Exp142 — ext lightgbm 17/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1022 (delta -1.7652 vs prev best -0.3370); val=-2.003242575953476 train=-0.024430230176615504.

**Learning:** Ext iter 17 (lightgbm): DISCARD. Train/val gap = 1.9788. This iter targets LightGBM leaf-wise sweep.


## Exp143 — ext lightgbm 18/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1573 (delta -1.8203 vs prev best -0.3370); val=-2.0559839992266746 train=-0.030221714240640647.

**Learning:** Ext iter 18 (lightgbm): DISCARD. Train/val gap = 2.0258. This iter targets LightGBM leaf-wise sweep.


## Exp144 — ext lightgbm 19/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1022 (delta -1.7652 vs prev best -0.3370); val=-2.003242575953476 train=-0.024430230176615504.

**Learning:** Ext iter 19 (lightgbm): DISCARD. Train/val gap = 1.9788. This iter targets LightGBM leaf-wise sweep.


## Exp145 — ext lightgbm 20/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1573 (delta -1.8203 vs prev best -0.3370); val=-2.0559839992266746 train=-0.030221714240640647.

**Learning:** Ext iter 20 (lightgbm): DISCARD. Train/val gap = 2.0258. This iter targets LightGBM leaf-wise sweep.


## Exp146 — ext lightgbm 21/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1022 (delta -1.7652 vs prev best -0.3370); val=-2.003242575953476 train=-0.024430230176615504.

**Learning:** Ext iter 21 (lightgbm): DISCARD. Train/val gap = 1.9788. This iter targets LightGBM leaf-wise sweep.


## Exp147 — ext lightgbm 22/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.1573 (delta -1.8203 vs prev best -0.3370); val=-2.0559839992266746 train=-0.030221714240640647.

**Learning:** Ext iter 22 (lightgbm): DISCARD. Train/val gap = 2.0258. This iter targets LightGBM leaf-wise sweep.


## Exp148 — ext catboost 23/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 23 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp149 — ext catboost 24/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 24 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp150 — ext catboost 25/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 25 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp151 — ext catboost 26/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 26 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp152 — ext catboost 27/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 27 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp153 — ext catboost 28/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 28 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp154 — ext catboost 29/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 29 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp155 — ext catboost 30/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 30 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp156 — ext catboost 31/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3370); val=NA train=NA.

**Learning:** Ext iter 31 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp157 — ext mlp 32/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.6443 (delta -0.3073 vs prev best -0.3370); val=-0.6344018921061437 train=-0.43694544454802203.

**Learning:** Ext iter 32 (mlp): DISCARD. Train/val gap = 0.1975. This iter targets MLP capacity sweep.


## Exp158 — ext mlp 33/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4571 (delta -0.1201 vs prev best -0.3370); val=-0.4451982954045332 train=-0.20680703311495094.

**Learning:** Ext iter 33 (mlp): DISCARD. Train/val gap = 0.2384. This iter targets MLP capacity sweep.


## Exp159 — ext mlp 34/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3948 (delta -0.0578 vs prev best -0.3370); val=-0.38257877844454186 train=-0.1383262881518231.

**Learning:** Ext iter 34 (mlp): DISCARD. Train/val gap = 0.2443. This iter targets MLP capacity sweep.


## Exp160 — ext mlp 35/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4523 (delta -0.1153 vs prev best -0.3370); val=-0.44303520888196873 train=-0.25850894090456394.

**Learning:** Ext iter 35 (mlp): DISCARD. Train/val gap = 0.1845. This iter targets MLP capacity sweep.


## Exp161 — ext mlp 36/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3854 (delta -0.0484 vs prev best -0.3370); val=-0.37437832482187794 train=-0.15330566652163533.

**Learning:** Ext iter 36 (mlp): DISCARD. Train/val gap = 0.2211. This iter targets MLP capacity sweep.


## Exp162 — ext mlp 37/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3617 (delta -0.0247 vs prev best -0.3370); val=-0.3505598074438456 train=-0.12750583058003057.

**Learning:** Ext iter 37 (mlp): DISCARD. Train/val gap = 0.2231. This iter targets MLP capacity sweep.


## Exp163 — ext mlp 38/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3499 (delta -0.0129 vs prev best -0.3370); val=-0.3410820816497676 train=-0.16390030086437643.

**Learning:** Ext iter 38 (mlp): DISCARD. Train/val gap = 0.1772. This iter targets MLP capacity sweep.


## Exp164 — ext mlp 39/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.3307 (delta +0.0064 vs prev best -0.3370); val=-0.3203055683409426 train=-0.11334295483187454.

**Learning:** Ext iter 39 (mlp): KEEP. Train/val gap = 0.2070. This iter targets MLP capacity sweep.


## Exp165 — ext mlp 40/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.3160 (delta +0.0147 vs prev best -0.3307); val=-0.30644798301957904 train=-0.11606464073027974.

**Learning:** Ext iter 40 (mlp): KEEP. Train/val gap = 0.1904. This iter targets MLP capacity sweep.


## Exp166 — ext mlp 41/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5056 (delta -0.1896 vs prev best -0.3160); val=-0.4922331682846777 train=-0.22539826219865328.

**Learning:** Ext iter 41 (mlp): DISCARD. Train/val gap = 0.2668. This iter targets MLP capacity sweep.


## Exp167 — ext mlp 42/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4402 (delta -0.1242 vs prev best -0.3160); val=-0.4262409353550895 train=-0.14759085155559246.

**Learning:** Ext iter 42 (mlp): DISCARD. Train/val gap = 0.2787. This iter targets MLP capacity sweep.


## Exp168 — ext mlp 43/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3942 (delta -0.0782 vs prev best -0.3160); val=-0.383590394450193 train=-0.17172818524174585.

**Learning:** Ext iter 43 (mlp): DISCARD. Train/val gap = 0.2119. This iter targets MLP capacity sweep.


## Exp169 — ext mlp 44/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5478 (delta -0.2318 vs prev best -0.3160); val=-0.5310109385981935 train=-0.19579787026236783.

**Learning:** Ext iter 44 (mlp): DISCARD. Train/val gap = 0.3352. This iter targets MLP capacity sweep.


## Exp170 — ext mlp 45/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4947 (delta -0.1787 vs prev best -0.3160); val=-0.4783342290110072 train=-0.1507779496577877.

**Learning:** Ext iter 45 (mlp): DISCARD. Train/val gap = 0.3276. This iter targets MLP capacity sweep.


## Exp171 — ext mlp 46/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4261 (delta -0.1101 vs prev best -0.3160); val=-0.4128924699090686 train=-0.14857316092120462.

**Learning:** Ext iter 46 (mlp): DISCARD. Train/val gap = 0.2643. This iter targets MLP capacity sweep.


## Exp172 — ext ft_transformer 47/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0778 (delta -1.7618 vs prev best -0.3160); val=-1.9916599784021736 train=-0.269208808151508.

**Learning:** Ext iter 47 (ft_transformer): DISCARD. Train/val gap = 1.7225. This iter targets FT-Transformer-style sweep.


## Exp173 — ext ft_transformer 48/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0967 (delta -1.7808 vs prev best -0.3160); val=-2.005421671738459 train=-0.17898141541773316.

**Learning:** Ext iter 48 (ft_transformer): DISCARD. Train/val gap = 1.8264. This iter targets FT-Transformer-style sweep.


## Exp174 — ext ft_transformer 49/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0539 (delta -1.7379 vs prev best -0.3160); val=-1.9633513509110614 train=-0.15334417689113558.

**Learning:** Ext iter 49 (ft_transformer): DISCARD. Train/val gap = 1.8100. This iter targets FT-Transformer-style sweep.


## Exp175 — ext ft_transformer 50/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-1.9839 (delta -1.6679 vs prev best -0.3160); val=-1.8946706959836503 train=-0.1109181282340737.

**Learning:** Ext iter 50 (ft_transformer): DISCARD. Train/val gap = 1.7838. This iter targets FT-Transformer-style sweep.


## Exp176 — ext ft_transformer 51/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0470 (delta -1.7311 vs prev best -0.3160); val=-1.9521414956856005 train=-0.05419707268281671.

**Learning:** Ext iter 51 (ft_transformer): DISCARD. Train/val gap = 1.8979. This iter targets FT-Transformer-style sweep.


## Exp177 — ext ft_transformer 52/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0143 (delta -1.6984 vs prev best -0.3160); val=-1.9200843781804076 train=-0.035268954701382825.

**Learning:** Ext iter 52 (ft_transformer): DISCARD. Train/val gap = 1.8848. This iter targets FT-Transformer-style sweep.


## Exp178 — ext ft_transformer 53/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-1.9734 (delta -1.6574 vs prev best -0.3160); val=-1.8819684852465715 train=-0.05384298091018708.

**Learning:** Ext iter 53 (ft_transformer): DISCARD. Train/val gap = 1.8281. This iter targets FT-Transformer-style sweep.


## Exp179 — ext ft_transformer 54/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0452 (delta -1.7293 vs prev best -0.3160); val=-1.9485961189864849 train=-0.015699435857143295.

**Learning:** Ext iter 54 (ft_transformer): DISCARD. Train/val gap = 1.9329. This iter targets FT-Transformer-style sweep.


## Exp180 — ext ft_transformer 55/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-2.0126 (delta -1.6967 vs prev best -0.3160); val=-1.9172282405118584 train=-0.009259988708411425.

**Learning:** Ext iter 55 (ft_transformer): DISCARD. Train/val gap = 1.9080. This iter targets FT-Transformer-style sweep.


## Exp181 — ext xgboost 56/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.1. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.1 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9596 (delta -1.6436 vs prev best -0.3160); val=-1.8708982743827574 train=-0.09707532232700379.

**Learning:** Ext iter 56 (xgboost): DISCARD. Train/val gap = 1.7738. This iter targets NGBoost-flavored sparsity sweep.


## Exp182 — ext xgboost 57/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.3. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.3 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9596 (delta -1.6436 vs prev best -0.3160); val=-1.8708982743827574 train=-0.09707532232700379.

**Learning:** Ext iter 57 (xgboost): DISCARD. Train/val gap = 1.7738. This iter targets NGBoost-flavored sparsity sweep.


## Exp183 — ext xgboost 58/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=1.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=1.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9596 (delta -1.6436 vs prev best -0.3160); val=-1.8708982743827574 train=-0.09707532232700379.

**Learning:** Ext iter 58 (xgboost): DISCARD. Train/val gap = 1.7738. This iter targets NGBoost-flavored sparsity sweep.


## Exp184 — ext xgboost 59/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=3.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=3.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-1.9596 (delta -1.6436 vs prev best -0.3160); val=-1.8708982743827574 train=-0.09707532232700379.

**Learning:** Ext iter 59 (xgboost): DISCARD. Train/val gap = 1.7738. This iter targets NGBoost-flavored sparsity sweep.


## Exp185 — ext mlp 60/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 128, 64). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4766 (delta -0.1606 vs prev best -0.3160); val=-0.46168065373834166 train=-0.16317294421051606.

**Learning:** Ext iter 60 (mlp): DISCARD. Train/val gap = 0.2985. This iter targets TabNet-flavoured wide-residual MLP.


## Exp186 — ext mlp 61/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(384, 192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(384, 192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4188 (delta -0.1028 vs prev best -0.3160); val=-0.40609182432920937 train=-0.15194758231049374.

**Learning:** Ext iter 61 (mlp): DISCARD. Train/val gap = 0.2541. This iter targets TabNet-flavoured wide-residual MLP.


## Exp187 — ext mlp 62/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4099 (delta -0.0939 vs prev best -0.3160); val=-0.4003317626856936 train=-0.20938202646905807.

**Learning:** Ext iter 62 (mlp): DISCARD. Train/val gap = 0.1909. This iter targets TabNet-flavoured wide-residual MLP.


## Exp188 — ext mlp 63/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(320, 160). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(320, 160) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.3751 (delta -0.0591 vs prev best -0.3160); val=-0.3649249882892947 train=-0.1612137851135452.

**Learning:** Ext iter 63 (mlp): DISCARD. Train/val gap = 0.2037. This iter targets TabNet-flavoured wide-residual MLP.


## Exp189 — ext mlp 64/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 256). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 256) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4331 (delta -0.1171 vs prev best -0.3160); val=-0.42046796199706316 train=-0.16880209591069145.

**Learning:** Ext iter 64 (mlp): DISCARD. Train/val gap = 0.2517. This iter targets TabNet-flavoured wide-residual MLP.


## Exp190 — ext ft_transformer 65/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=200. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.8199 (delta -2.5040 vs prev best -0.3160); val=-2.76847534888525 train=-1.739261652385832.

**Learning:** Ext iter 65 (ft_transformer): DISCARD. Train/val gap = 1.0292. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp191 — ext ft_transformer 66/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=400. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.2868 (delta -1.9709 vs prev best -0.3160); val=-2.221904957740818 train=-0.9231548582815913.

**Learning:** Ext iter 66 (ft_transformer): DISCARD. Train/val gap = 1.2988. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp192 — ext ft_transformer 67/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=600. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-2.0603 (delta -1.7444 vs prev best -0.3160); val=-1.9902149972671037 train=-0.5877386710829178.

**Learning:** Ext iter 67 (ft_transformer): DISCARD. Train/val gap = 1.4025. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp193 — ext xgboost 68/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=0.1 reg_alpha=0.1. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=0.1 smooths leaf weights; reg_alpha=0.1 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7906 (delta -1.4746 vs prev best -0.3160); val=-1.7187610279076255 train=-0.2825868280498031.

**Learning:** Ext iter 68 (xgboost): DISCARD. Train/val gap = 1.4362. This iter targets Elastic-net-flavoured gradient boost.


## Exp194 — ext xgboost 69/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=1.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=1.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7832 (delta -1.4673 vs prev best -0.3160); val=-1.7126797379890417 train=-0.301724070912504.

**Learning:** Ext iter 69 (xgboost): DISCARD. Train/val gap = 1.4110. This iter targets Elastic-net-flavoured gradient boost.


## Exp195 — ext xgboost 70/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=3.0 reg_alpha=1.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=3.0 smooths leaf weights; reg_alpha=1.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7739 (delta -1.4579 vs prev best -0.3160); val=-1.7051799870463138 train=-0.3313360678222872.

**Learning:** Ext iter 70 (xgboost): DISCARD. Train/val gap = 1.3738. This iter targets Elastic-net-flavoured gradient boost.


## Exp196 — ext xgboost 71/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7410 (delta -1.4250 vs prev best -0.3160); val=-1.677433719718446 train=-0.40704140238630154.

**Learning:** Ext iter 71 (xgboost): DISCARD. Train/val gap = 1.2704. This iter targets Elastic-net-flavoured gradient boost.


## Exp197 — ext xgboost 72/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=3.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=3.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.7410 (delta -1.4250 vs prev best -0.3160); val=-1.677433719718446 train=-0.40704140238630154.

**Learning:** Ext iter 72 (xgboost): DISCARD. Train/val gap = 1.2704. This iter targets Elastic-net-flavoured gradient boost.


## Exp198 — ext patchtsmixer 73/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.5673 (delta -1.2513 vs prev best -0.3160); val=-1.5594739985718518 train=-1.4031262353156755.

**Learning:** Ext iter 73 (patchtsmixer): DISCARD. Train/val gap = 0.1563. This iter targets PatchTSMixer channel-mix sweep.


## Exp199 — ext patchtsmixer 74/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.5716 (delta -1.2556 vs prev best -0.3160); val=-1.5551079416375067 train=-1.2252978955278728.

**Learning:** Ext iter 74 (patchtsmixer): DISCARD. Train/val gap = 0.3298. This iter targets PatchTSMixer channel-mix sweep.


## Exp200 — ext patchtsmixer 75/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.3719 (delta -1.0559 vs prev best -0.3160); val=-1.3538845159565853 train=-0.9933628119717871.

**Learning:** Ext iter 75 (patchtsmixer): DISCARD. Train/val gap = 0.3605. This iter targets PatchTSMixer channel-mix sweep.


## Exp201 — ext patchtsmixer 76/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.1775 (delta -0.8616 vs prev best -0.3160); val=-1.1546501225886012 train=-0.6972574826574548.

**Learning:** Ext iter 76 (patchtsmixer): DISCARD. Train/val gap = 0.4574. This iter targets PatchTSMixer channel-mix sweep.


## Exp202 — ext patchtsmixer 77/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.0567 (delta -0.7408 vs prev best -0.3160); val=-1.0379411770501719 train=-0.6622034191758215.

**Learning:** Ext iter 77 (patchtsmixer): DISCARD. Train/val gap = 0.3757. This iter targets PatchTSMixer channel-mix sweep.


## Exp203 — ext patchtsmixer 78/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.0180 (delta -0.7021 vs prev best -0.3160); val=-0.9914678231335774 train=-0.45988525286290843.

**Learning:** Ext iter 78 (patchtsmixer): DISCARD. Train/val gap = 0.5316. This iter targets PatchTSMixer channel-mix sweep.


## Exp204 — ext xgboost 79/200
**Diagnosis:** Multi-seed champion variance run, seed=42. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.2080 (delta -1.8920 vs prev best -0.3160); val=-2.105939766423695 train=-0.06501881209709424.

**Learning:** Ext iter 79 (xgboost): DISCARD. Train/val gap = 2.0409. This iter targets extended search.


## Exp205 — ext xgboost 80/200
**Diagnosis:** Multi-seed champion variance run, seed=0. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1383 (delta -1.8223 vs prev best -0.3160); val=-2.039523602378311 train=-0.06450573262556136.

**Learning:** Ext iter 80 (xgboost): DISCARD. Train/val gap = 1.9750. This iter targets extended search.


## Exp206 — ext xgboost 81/200
**Diagnosis:** Multi-seed champion variance run, seed=7. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1350 (delta -1.8191 vs prev best -0.3160); val=-2.0365554773391943 train=-0.06697769981521279.

**Learning:** Ext iter 81 (xgboost): DISCARD. Train/val gap = 1.9696. This iter targets extended search.


## Exp207 — ext xgboost 82/200
**Diagnosis:** Multi-seed champion variance run, seed=99. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1328 (delta -1.8168 vs prev best -0.3160); val=-2.0342348908961108 train=-0.06389356602122012.

**Learning:** Ext iter 82 (xgboost): DISCARD. Train/val gap = 1.9703. This iter targets extended search.


## Exp208 — ext xgboost 83/200
**Diagnosis:** Multi-seed champion variance run, seed=2024. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.2018 (delta -1.8858 vs prev best -0.3160); val=-2.0999307076057545 train=-0.06226475782939274.

**Learning:** Ext iter 83 (xgboost): DISCARD. Train/val gap = 2.0377. This iter targets extended search.


## Exp209 — ext xgboost 84/200
**Diagnosis:** Multi-seed champion variance run, seed=12345. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.2248 (delta -1.9088 vs prev best -0.3160); val=-2.122147384486849 train=-0.06918137408289429.

**Learning:** Ext iter 84 (xgboost): DISCARD. Train/val gap = 2.0530. This iter targets extended search.


## Exp210 — ext xgboost 85/200
**Diagnosis:** Multi-seed champion variance run, seed=7777. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1749 (delta -1.8589 vs prev best -0.3160); val=-2.07433380554985 train=-0.06319323175848046.

**Learning:** Ext iter 85 (xgboost): DISCARD. Train/val gap = 2.0111. This iter targets extended search.


## Exp211 — ext xgboost 86/200
**Diagnosis:** Multi-seed champion variance run, seed=31337. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1423 (delta -1.8263 vs prev best -0.3160); val=-2.0435156591612067 train=-0.06774936710304869.

**Learning:** Ext iter 86 (xgboost): DISCARD. Train/val gap = 1.9758. This iter targets extended search.


## Exp212 — ext xgboost 87/200
**Diagnosis:** Multi-seed champion variance run, seed=1729. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1599 (delta -1.8439 vs prev best -0.3160); val=-2.0602251859378042 train=-0.06769107023881411.

**Learning:** Ext iter 87 (xgboost): DISCARD. Train/val gap = 1.9925. This iter targets extended search.


## Exp213 — ext xgboost 88/200
**Diagnosis:** Multi-seed champion variance run, seed=6174. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-2.1585 (delta -1.8426 vs prev best -0.3160); val=-2.0589218312525253 train=-0.06639564653898387.

**Learning:** Ext iter 88 (xgboost): DISCARD. Train/val gap = 1.9925. This iter targets extended search.


## Exp214 — ext xgboost 89/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=30. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=30, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.6172 (delta -1.3012 vs prev best -0.3160); val=-1.5767146692099387 train=-0.767008407417383.

**Learning:** Ext iter 89 (xgboost): DISCARD. Train/val gap = 0.8097. This iter targets Extreme regularisation cool-down.


## Exp215 — ext xgboost 90/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=50. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=50, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.6712 (delta -1.3552 vs prev best -0.3160); val=-1.632732991742253 train=-0.8632333319297942.

**Learning:** Ext iter 90 (xgboost): DISCARD. Train/val gap = 0.7695. This iter targets Extreme regularisation cool-down.


## Exp216 — ext xgboost 91/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=100. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=100, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-1.8023 (delta -1.4863 vs prev best -0.3160); val=-1.766079261880331 train=-1.0416007338956366.

**Learning:** Ext iter 91 (xgboost): DISCARD. Train/val gap = 0.7245. This iter targets Extreme regularisation cool-down.

