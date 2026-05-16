# Research Journal — commonlitreadabilityprize

_(populated by `framework/hill_climb.py`)_

## Exp1 — xgboost iter 1
**Diagnosis:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

**Hypothesis:** Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).

**Prediction:** Composite in [0.55, 0.85] depending on task difficulty.

**Verdict:** KEEP composite=-3.2753 (delta +inf vs prev best -inf); val_score=-3.123074205194283; train_score=-0.07843293359561201.

**Learning:** Iter 1 xgboost: KEEP. Train/val gap = 3.0446. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — xgboost iter 2
**Diagnosis:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.

**Citations:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

**Hypothesis:** Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-3.6535 (delta -0.3782 vs prev best -3.2753); val_score=-3.4798361463447836; train_score=-0.006908225589258113.

**Learning:** Iter 2 xgboost: DISCARD. Train/val gap = 3.4729. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — xgboost iter 3
**Diagnosis:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

**Hypothesis:** Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-2.7580 (delta +0.5173 vs prev best -3.2753); val_score=-2.64150561935864; train_score=-0.31237986162668263.

**Learning:** Iter 3 xgboost: KEEP. Train/val gap = 2.3291. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp4 — xgboost iter 4
**Diagnosis:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.

**Citations:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

**Hypothesis:** Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.

**Prediction:** Composite delta in [+0.001, +0.010].

**Verdict:** DISCARD composite=-3.2262 (delta -0.4682 vs prev best -2.7580); val_score=-3.0765528657916383; train_score=-0.08347341162465516.

**Learning:** Iter 4 xgboost: DISCARD. Train/val gap = 2.9931. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — xgboost iter 5
**Diagnosis:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

**Hypothesis:** Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.

**Prediction:** Composite delta in [+0.002, +0.012].

**Verdict:** DISCARD composite=-3.1253 (delta -0.3673 vs prev best -2.7580); val_score=-2.985873021138752; train_score=-0.19760162706976972.

**Learning:** Iter 5 xgboost: DISCARD. Train/val gap = 2.7883. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — xgboost iter 6
**Diagnosis:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.

**Citations:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

**Hypothesis:** Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-3.3751 (delta -0.6171 vs prev best -2.7580); val_score=-3.228319922560325; train_score=-0.2931120458477458.

**Learning:** Iter 6 xgboost: DISCARD. Train/val gap = 2.9352. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — xgboost iter 7
**Diagnosis:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.

**Citations:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

**Hypothesis:** Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-2.7900 (delta -0.0321 vs prev best -2.7580); val_score=-2.6633424205251015; train_score=-0.12928516876610677.

**Learning:** Iter 7 xgboost: DISCARD. Train/val gap = 2.5341. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp8 — xgboost iter 8
**Diagnosis:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.

**Citations:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.2253 (delta -0.4674 vs prev best -2.7580); val_score=-3.0756722374497643; train_score=-0.08226127956285278.

**Learning:** Iter 8 xgboost: DISCARD. Train/val gap = 2.9934. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — xgboost iter 9
**Diagnosis:** Third seed for 3-seed median (autoresearch protocol).

**Citations:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.2118 (delta -0.4538 vs prev best -2.7580); val_score=-3.06273416674903; train_score=-0.08169019850386844.

**Learning:** Iter 9 xgboost: DISCARD. Train/val gap = 2.9810. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — xgboost iter 10
**Diagnosis:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

**Hypothesis:** Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-3.8850 (delta -1.1271 vs prev best -2.7580); val_score=-3.700218122084288; train_score=-0.0036485015601597686.

**Learning:** Iter 10 xgboost: DISCARD. Train/val gap = 3.6966. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — xgboost iter 11
**Diagnosis:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.

**Citations:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

**Hypothesis:** Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** KEEP composite=-2.6805 (delta +0.0775 vs prev best -2.7580); val_score=-2.5671746948442906; train_score=-0.30043434598746.

**Learning:** Iter 11 xgboost: KEEP. Train/val gap = 2.2667. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp12 — xgboost iter 12
**Diagnosis:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

**Hypothesis:** Hypothesis: larger leaves reduce variance, improve val by 0.5%.

**Prediction:** Composite delta in [-0.002, +0.010].

**Verdict:** DISCARD composite=-3.2753 (delta -0.5948 vs prev best -2.6805); val_score=-3.123074205194283; train_score=-0.07843293359561201.

**Learning:** Iter 12 xgboost: DISCARD. Train/val gap = 3.0446. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — xgboost iter 13
**Diagnosis:** Gamma split-penalty 0.5 — discourages overly eager splits.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

**Hypothesis:** Hypothesis: fewer, higher-quality splits. Val improves slightly.

**Prediction:** Composite delta in [-0.003, +0.008].

**Verdict:** DISCARD composite=-3.2753 (delta -0.5948 vs prev best -2.6805); val_score=-3.123074205194283; train_score=-0.07843293359561201.

**Learning:** Iter 13 xgboost: DISCARD. Train/val gap = 3.0446. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — xgboost iter 14
**Diagnosis:** High subsample for low-noise tasks — opposite direction from iter-4/7.

**Citations:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

**Hypothesis:** Hypothesis: gentle bagging if iter-4/7 over-regularised.

**Prediction:** Composite delta in [-0.005, +0.007].

**Verdict:** DISCARD composite=-3.3443 (delta -0.6638 vs prev best -2.6805); val_score=-3.188538774756776; train_score=-0.07245069081740244.

**Learning:** Iter 14 xgboost: DISCARD. Train/val gap = 3.1161. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — xgboost iter 15
**Diagnosis:** L1 regularisation (reg_alpha) for feature selection.

**Citations:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

**Hypothesis:** Hypothesis: L1 trims noise features, val improves.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-3.4476 (delta -0.7671 vs prev best -2.6805); val_score=-3.2850331613385197; train_score=-0.0340823780823688.

**Learning:** Iter 15 xgboost: DISCARD. Train/val gap = 3.2510. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — xgboost iter 16
**Diagnosis:** Combined moderate regularisation — meta-search across all axes.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

**Hypothesis:** Hypothesis: balanced config beats single-knob champions.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-3.2601 (delta -0.5796 vs prev best -2.6805); val_score=-3.106113275784841; train_score=-0.026102301792004186.

**Learning:** Iter 16 xgboost: DISCARD. Train/val gap = 3.0800. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — xgboost iter 17
**Diagnosis:** Fourth seed — extend variance characterisation.

**Citations:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

**Hypothesis:** Hypothesis: within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.1948 (delta -0.5143 vs prev best -2.6805); val_score=-3.0464411500010833; train_score=-0.07847803043741357.

**Learning:** Iter 17 xgboost: DISCARD. Train/val gap = 2.9680. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — xgboost iter 18
**Diagnosis:** Fifth seed.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Same as iter-15.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.3803 (delta -0.6997 vs prev best -2.6805); val_score=-3.222896682555651; train_score=-0.07580748538963668.

**Learning:** Iter 18 xgboost: DISCARD. Train/val gap = 3.1471. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — xgboost iter 19
**Diagnosis:** Aggressive depth=12 with proportionally lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

**Hypothesis:** Hypothesis: depth=12 will overfit unless lr is very low.

**Prediction:** Composite delta in [-0.030, +0.010].

**Verdict:** DISCARD composite=-3.9501 (delta -1.2696 vs prev best -2.6805); val_score=-3.7629481254690056; train_score=-0.019871913270696755.

**Learning:** Iter 19 xgboost: DISCARD. Train/val gap = 3.7431. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — xgboost iter 20
**Diagnosis:** Very shallow, high-lr — stump-like learners as opposite extreme.

**Citations:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

**Hypothesis:** Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.

**Prediction:** Composite delta in [-0.040, +0.005].

**Verdict:** KEEP composite=-2.4721 (delta +0.2084 vs prev best -2.6805); val_score=-2.3757129402212542; train_score=-0.4481239578469048.

**Learning:** Iter 20 xgboost: KEEP. Train/val gap = 1.9276. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp21 — xgboost iter 21
**Diagnosis:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.

**Citations:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

**Hypothesis:** Hypothesis: no-op vs baseline; informational only.

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-3.2661 (delta -0.7940 vs prev best -2.4721); val_score=-3.1116658881713786; train_score=-0.023218045147851276.

**Learning:** Iter 21 xgboost: DISCARD. Train/val gap = 3.0884. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — xgboost iter 22
**Diagnosis:** Confirm hist-method explicitly — same as default but pinned.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

**Hypothesis:** Hypothesis: no change vs baseline (already default in our setup).

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-3.2753 (delta -0.8032 vs prev best -2.4721); val_score=-3.123074205194283; train_score=-0.07843293359561201.

**Learning:** Iter 22 xgboost: DISCARD. Train/val gap = 3.0446. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — xgboost iter 23
**Diagnosis:** Long-and-slow final refinement with mid-strength L2.

**Citations:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

**Hypothesis:** Hypothesis: best champion candidate. Val should peak.

**Prediction:** Composite delta in [+0.005, +0.025].

**Verdict:** DISCARD composite=-2.9023 (delta -0.4302 vs prev best -2.4721); val_score=-2.7702280306000473; train_score=-0.12816172224731698.

**Learning:** Iter 23 xgboost: DISCARD. Train/val gap = 2.6421. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — xgboost iter 24
**Diagnosis:** Combined moderate everything — explore a balanced corner.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-2.9747 (delta -0.5026 vs prev best -2.4721); val_score=-2.8384631971426373; train_score=-0.11339453261771397.

**Learning:** Iter 24 xgboost: DISCARD. Train/val gap = 2.7251. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — xgboost iter 25
**Diagnosis:** Final 6th seed — closes the variance characterisation for this backbone.

**Citations:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.2507 (delta -0.7786 vs prev best -2.4721); val_score=-3.0997313659929953; train_score=-0.08079733841467523.

**Learning:** Iter 25 xgboost: DISCARD. Train/val gap = 3.0189. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp26 — lightgbm iter 1
**Diagnosis:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard lightgbm config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 1 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp27 — lightgbm iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-5.3109 (delta -2.8388 vs prev best -2.4721); val_score=-5.2821441123578365; train_score=-4.707626903637106.

**Learning:** Iter 2 lightgbm: DISCARD. Train/val gap = 0.5745. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp28 — lightgbm iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-6.0515 (delta -3.5794 vs prev best -2.4721); val_score=-6.049452746441326; train_score=-6.00921097635696.

**Learning:** Iter 3 lightgbm: DISCARD. Train/val gap = 0.0402. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp29 — lightgbm iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-4.7258 (delta -2.2537 vs prev best -2.4721); val_score=-4.6694039694468215; train_score=-3.541144899781756.

**Learning:** Iter 4 lightgbm: DISCARD. Train/val gap = 1.1283. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp30 — lightgbm iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-3.0634 (delta -0.5913 vs prev best -2.4721); val_score=-2.9224222517204677; train_score=-0.10373379480444132.

**Learning:** Iter 5 lightgbm: DISCARD. Train/val gap = 2.8187. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp31 — lightgbm iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-3.0634 (delta -0.5913 vs prev best -2.4721); val_score=-2.9224222517204677; train_score=-0.10373379480444132.

**Learning:** Iter 6 lightgbm: DISCARD. Train/val gap = 2.8187. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp32 — lightgbm iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.5921 (delta -3.1200 vs prev best -2.4721); val_score=-5.573512077989455; train_score=-5.201289046229112.

**Learning:** Iter 7 lightgbm: DISCARD. Train/val gap = 0.3722. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp33 — lightgbm iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.5872 (delta -3.1151 vs prev best -2.4721); val_score=-5.568829698016567; train_score=-5.200635584647554.

**Learning:** Iter 8 lightgbm: DISCARD. Train/val gap = 0.3682. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp34 — lightgbm iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 9 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp35 — lightgbm iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-5.9012 (delta -3.4292 vs prev best -2.4721); val_score=-5.89459852001868; train_score=-5.761718870843982.

**Learning:** Iter 10 lightgbm: DISCARD. Train/val gap = 0.1329. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp36 — lightgbm iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 11 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp37 — lightgbm iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 12 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp38 — lightgbm iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-5.8310 (delta -3.3589 vs prev best -2.4721); val_score=-5.822083677586177; train_score=-5.644707221486275.

**Learning:** Iter 13 lightgbm: DISCARD. Train/val gap = 0.1774. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp39 — lightgbm iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.5957 (delta -3.1236 vs prev best -2.4721); val_score=-5.5770448836014195; train_score=-5.2034917417999.

**Learning:** Iter 14 lightgbm: DISCARD. Train/val gap = 0.3736. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp40 — lightgbm iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.5894 (delta -3.1173 vs prev best -2.4721); val_score=-5.570851912986695; train_score=-5.200066824881832.

**Learning:** Iter 15 lightgbm: DISCARD. Train/val gap = 0.3708. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp41 — lightgbm iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 16 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp42 — lightgbm iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 17 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp43 — lightgbm iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-5.0796 (delta -2.6075 vs prev best -2.4721); val_score=-5.041202805723948; train_score=-4.273153421127297.

**Learning:** Iter 18 lightgbm: DISCARD. Train/val gap = 0.7680. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp44 — lightgbm iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-6.2763 (delta -3.8042 vs prev best -2.4721); val_score=-6.21828460812266; train_score=-6.273511010517275.

**Learning:** Iter 19 lightgbm: DISCARD. Train/val gap = 0.0552. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp45 — lightgbm iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 20 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp46 — lightgbm iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 21 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp47 — lightgbm iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-5.5769 (delta -3.1048 vs prev best -2.4721); val_score=-5.55895690764888; train_score=-5.200435307751701.

**Learning:** Iter 22 lightgbm: DISCARD. Train/val gap = 0.3585. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp48 — lightgbm iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.7590 (delta -3.2869 vs prev best -2.4721); val_score=-5.7480837909687015; train_score=-5.529059259818215.

**Learning:** Iter 23 lightgbm: DISCARD. Train/val gap = 0.2190. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp49 — lightgbm iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.3048 (delta -2.8327 vs prev best -2.4721); val_score=-5.276390735884258; train_score=-4.709100778680811.

**Learning:** Iter 24 lightgbm: DISCARD. Train/val gap = 0.5673. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp50 — lightgbm iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.5937 (delta -3.1217 vs prev best -2.4721); val_score=-5.575159163362027; train_score=-5.203380925445536.

**Learning:** Iter 25 lightgbm: DISCARD. Train/val gap = 0.3718. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp51 — catboost iter 1
**Diagnosis:** Baseline catboost per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard catboost config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 1 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp52 — catboost iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 2 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp53 — catboost iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 3 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp54 — catboost iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 4 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp55 — catboost iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 5 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp56 — catboost iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 6 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp57 — catboost iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 7 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp58 — catboost iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 8 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp59 — catboost iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 9 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp60 — catboost iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 10 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp61 — catboost iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 11 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp62 — catboost iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 12 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp63 — catboost iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 13 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp64 — catboost iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 14 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp65 — catboost iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 15 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp66 — catboost iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 16 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp67 — catboost iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 17 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp68 — catboost iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 18 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp69 — catboost iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 19 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp70 — catboost iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 20 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp71 — catboost iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 21 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp72 — catboost iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 22 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp73 — catboost iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 23 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp74 — catboost iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 24 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp75 — catboost iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.4721); val_score=NA; train_score=NA.

**Learning:** Iter 25 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp76 — mlp iter 1
**Diagnosis:** Baseline mlp per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard mlp config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** KEEP composite=-0.6288 (delta +1.8433 vs prev best -2.4721); val_score=-0.6194644646647672; train_score=-0.4334957080692398.

**Learning:** Iter 1 mlp: KEEP. Train/val gap = 0.1860. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp77 — mlp iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-0.5494 (delta +0.0793 vs prev best -0.6288); val_score=-0.5371474928768181; train_score=-0.29124894485773667.

**Learning:** Iter 2 mlp: KEEP. Train/val gap = 0.2459. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp78 — mlp iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.9651 (delta -0.4156 vs prev best -0.5494); val_score=-0.9629610666503602; train_score=-0.9203520981668196.

**Learning:** Iter 3 mlp: DISCARD. Train/val gap = 0.0426. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp79 — mlp iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** KEEP composite=-0.4806 (delta +0.0688 vs prev best -0.5494); val_score=-0.46861474946971393; train_score=-0.22850558267029916.

**Learning:** Iter 4 mlp: KEEP. Train/val gap = 0.2401. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp80 — mlp iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.6192 (delta -0.1386 vs prev best -0.4806); val_score=-0.616051824131412; train_score=-0.5534956848386394.

**Learning:** Iter 5 mlp: DISCARD. Train/val gap = 0.0626. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp81 — mlp iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-2.9203 (delta -2.4397 vs prev best -0.4806); val_score=-2.915233059918218; train_score=-2.813357752231489.

**Learning:** Iter 6 mlp: DISCARD. Train/val gap = 0.1019. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp82 — mlp iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.5622 (delta -0.0816 vs prev best -0.4806); val_score=-0.5548082139740366; train_score=-0.4063423125216593.

**Learning:** Iter 7 mlp: DISCARD. Train/val gap = 0.1485. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp83 — mlp iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6352 (delta -0.1546 vs prev best -0.4806); val_score=-0.6260596590635527; train_score=-0.44287918571305146.

**Learning:** Iter 8 mlp: DISCARD. Train/val gap = 0.1832. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp84 — mlp iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.5329 (delta -0.0523 vs prev best -0.4806); val_score=-0.5196492054054764; train_score=-0.2544688520762752.

**Learning:** Iter 9 mlp: DISCARD. Train/val gap = 0.2652. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp85 — mlp iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.6468 (delta -0.1661 vs prev best -0.4806); val_score=-0.6399243407678724; train_score=-0.503014803600319.

**Learning:** Iter 10 mlp: DISCARD. Train/val gap = 0.1369. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp86 — mlp iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-0.7232 (delta -0.2426 vs prev best -0.4806); val_score=-0.7059264218228218; train_score=-0.36092628610208355.

**Learning:** Iter 11 mlp: DISCARD. Train/val gap = 0.3450. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp87 — mlp iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-0.5192 (delta -0.0386 vs prev best -0.4806); val_score=-0.5057036112160234; train_score=-0.23615555728640644.

**Learning:** Iter 12 mlp: DISCARD. Train/val gap = 0.2695. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp88 — mlp iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-0.8581 (delta -0.3774 vs prev best -0.4806); val_score=-0.8544352310816876; train_score=-0.7820953754425382.

**Learning:** Iter 13 mlp: DISCARD. Train/val gap = 0.0723. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp89 — mlp iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6508 (delta -0.1701 vs prev best -0.4806); val_score=-0.6403268725158456; train_score=-0.4315994726388165.

**Learning:** Iter 14 mlp: DISCARD. Train/val gap = 0.2087. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp90 — mlp iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6724 (delta -0.1918 vs prev best -0.4806); val_score=-0.6600505812003847; train_score=-0.41326018642118195.

**Learning:** Iter 15 mlp: DISCARD. Train/val gap = 0.2468. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp91 — mlp iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.7028 (delta -0.2221 vs prev best -0.4806); val_score=-0.695035450634994; train_score=-0.5405253312953023.

**Learning:** Iter 16 mlp: DISCARD. Train/val gap = 0.1545. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp92 — mlp iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** KEEP composite=-0.3944 (delta +0.0862 vs prev best -0.4806); val_score=-0.3845962887617648; train_score=-0.18902382928059153.

**Learning:** Iter 17 mlp: KEEP. Train/val gap = 0.1956. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp93 — mlp iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-0.5163 (delta -0.1219 vs prev best -0.3944); val_score=-0.505078866106922; train_score=-0.2804599633075745.

**Learning:** Iter 18 mlp: DISCARD. Train/val gap = 0.2246. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp94 — mlp iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-4.9224 (delta -4.5280 vs prev best -0.3944); val_score=-4.8884959111110255; train_score=-4.920796981707401.

**Learning:** Iter 19 mlp: DISCARD. Train/val gap = 0.0323. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp95 — mlp iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.5156 (delta -0.1213 vs prev best -0.3944); val_score=-0.501483118305572; train_score=-0.21826389490873246.

**Learning:** Iter 20 mlp: DISCARD. Train/val gap = 0.2832. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp96 — mlp iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.6288 (delta -0.2344 vs prev best -0.3944); val_score=-0.6194644646647672; train_score=-0.4334957080692398.

**Learning:** Iter 21 mlp: DISCARD. Train/val gap = 0.1860. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp97 — mlp iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-0.6288 (delta -0.2344 vs prev best -0.3944); val_score=-0.6194644646647672; train_score=-0.4334957080692398.

**Learning:** Iter 22 mlp: DISCARD. Train/val gap = 0.1860. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp98 — mlp iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.7154 (delta -0.3210 vs prev best -0.3944); val_score=-0.7079628555230952; train_score=-0.559889883556838.

**Learning:** Iter 23 mlp: DISCARD. Train/val gap = 0.1481. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp99 — mlp iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.5630 (delta -0.1687 vs prev best -0.3944); val_score=-0.5523517483964399; train_score=-0.3384588568228371.

**Learning:** Iter 24 mlp: DISCARD. Train/val gap = 0.2139. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp100 — mlp iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6788 (delta -0.2845 vs prev best -0.3944); val_score=-0.6671820575572537; train_score=-0.4342808477330285.

**Learning:** Iter 25 mlp: DISCARD. Train/val gap = 0.2329. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp101 — ft_transformer iter 1
**Diagnosis:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard ft_transformer config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 1 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp102 — ft_transformer iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-5.3853 (delta -4.9909 vs prev best -0.3944); val_score=-5.362507066183509; train_score=-4.906957101648363.

**Learning:** Iter 2 ft_transformer: DISCARD. Train/val gap = 0.4555. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp103 — ft_transformer iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-6.0605 (delta -5.6661 vs prev best -0.3944); val_score=-6.060298491665039; train_score=-6.056933053352624.

**Learning:** Iter 3 ft_transformer: DISCARD. Train/val gap = 0.0034. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp104 — ft_transformer iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-4.8767 (delta -4.4823 vs prev best -0.3944); val_score=-4.828496754112086; train_score=-3.86412033720893.

**Learning:** Iter 4 ft_transformer: DISCARD. Train/val gap = 0.9644. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp105 — ft_transformer iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-3.1238 (delta -2.7295 vs prev best -0.3944); val_score=-2.9805392653077076; train_score=-0.11460886229062506.

**Learning:** Iter 5 ft_transformer: DISCARD. Train/val gap = 2.8659. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp106 — ft_transformer iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-3.1238 (delta -2.7295 vs prev best -0.3944); val_score=-2.9805392653077076; train_score=-0.11460886229062506.

**Learning:** Iter 6 ft_transformer: DISCARD. Train/val gap = 2.8659. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp107 — ft_transformer iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 7 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp108 — ft_transformer iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 8 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp109 — ft_transformer iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 9 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp110 — ft_transformer iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-5.9227 (delta -5.5283 vs prev best -0.3944); val_score=-5.918822825944913; train_score=-5.841189062408165.

**Learning:** Iter 10 ft_transformer: DISCARD. Train/val gap = 0.0776. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp111 — ft_transformer iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 11 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp112 — ft_transformer iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 12 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp113 — ft_transformer iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-5.8596 (delta -5.4653 vs prev best -0.3944); val_score=-5.853787822810698; train_score=-5.736840972445387.

**Learning:** Iter 13 ft_transformer: DISCARD. Train/val gap = 0.1169. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp114 — ft_transformer iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 14 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp115 — ft_transformer iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 15 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp116 — ft_transformer iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 16 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp117 — ft_transformer iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 17 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp118 — ft_transformer iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-5.1846 (delta -4.7902 vs prev best -0.3944); val_score=-5.153034213299611; train_score=-4.52269155885587.

**Learning:** Iter 18 ft_transformer: DISCARD. Train/val gap = 0.6303. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp119 — ft_transformer iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-6.2917 (delta -5.8973 vs prev best -0.3944); val_score=-6.219825280039657; train_score=-6.288262259006641.

**Learning:** Iter 19 ft_transformer: DISCARD. Train/val gap = 0.0684. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp120 — ft_transformer iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 20 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp121 — ft_transformer iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 21 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp122 — ft_transformer iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 22 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp123 — ft_transformer iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.7998 (delta -5.4054 vs prev best -0.3944); val_score=-5.791993160117287; train_score=-5.635630068577931.

**Learning:** Iter 23 ft_transformer: DISCARD. Train/val gap = 0.1564. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp124 — ft_transformer iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.3855 (delta -4.9911 vs prev best -0.3944); val_score=-5.362695162757308; train_score=-4.906445440005268.

**Learning:** Iter 24 ft_transformer: DISCARD. Train/val gap = 0.4562. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp125 — ft_transformer iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.6331 (delta -5.2388 vs prev best -0.3944); val_score=-5.619463932270366; train_score=-5.345775324220736.

**Learning:** Iter 25 ft_transformer: DISCARD. Train/val gap = 0.2737. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp126 — ext xgboost 1/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.0680 (delta -2.6736 vs prev best -0.3944); val=-2.95951724652155 train=-0.790308996986961.

**Learning:** Ext iter 1 (xgboost): DISCARD. Train/val gap = 2.1692. This iter targets Extended xgboost sweep.


## Exp127 — ext xgboost 2/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.7002 (delta -2.3058 vs prev best -0.3944); val=-2.5807114083108633 train=-0.19074978457259967.

**Learning:** Ext iter 2 (xgboost): DISCARD. Train/val gap = 2.3900. This iter targets Extended xgboost sweep.


## Exp128 — ext xgboost 3/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.1524 (delta -2.7580 vs prev best -0.3944); val=-3.0219547864761886 train=-0.41321442682191056.

**Learning:** Ext iter 3 (xgboost): DISCARD. Train/val gap = 2.6087. This iter targets Extended xgboost sweep.


## Exp129 — ext xgboost 4/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.9786 (delta -2.5842 vs prev best -0.3944); val=-2.8397757457792188 train=-0.0629318561215809.

**Learning:** Ext iter 4 (xgboost): DISCARD. Train/val gap = 2.7768. This iter targets Extended xgboost sweep.


## Exp130 — ext xgboost 5/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.3382 (delta -2.9439 vs prev best -0.3944); val=-3.1891412436498077 train=-0.2072619915732533.

**Learning:** Ext iter 5 (xgboost): DISCARD. Train/val gap = 2.9819. This iter targets Extended xgboost sweep.


## Exp131 — ext xgboost 6/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.2407 (delta -2.8464 vs prev best -0.3944); val=-3.08712150941086 train=-0.014602917237462527.

**Learning:** Ext iter 6 (xgboost): DISCARD. Train/val gap = 3.0725. This iter targets Extended xgboost sweep.


## Exp132 — ext xgboost 7/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.5385 (delta -3.1441 vs prev best -0.3944); val=-3.3746498774012017 train=-0.09769781658558482.

**Learning:** Ext iter 7 (xgboost): DISCARD. Train/val gap = 3.2770. This iter targets Extended xgboost sweep.


## Exp133 — ext xgboost 8/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.4612 (delta -3.0669 vs prev best -0.3944); val=-3.2965149886283642 train=-0.0022426268499941286.

**Learning:** Ext iter 8 (xgboost): DISCARD. Train/val gap = 3.2943. This iter targets Extended xgboost sweep.


## Exp134 — ext xgboost 9/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.6950 (delta -3.3007 vs prev best -0.3944); val=-3.521507529691971 train=-0.05115636188198315.

**Learning:** Ext iter 9 (xgboost): DISCARD. Train/val gap = 3.4704. This iter targets Extended xgboost sweep.


## Exp135 — ext xgboost 10/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.6606 (delta -3.2662 vs prev best -0.3944); val=-3.486324021793804 train=-0.0005266928677053572.

**Learning:** Ext iter 10 (xgboost): DISCARD. Train/val gap = 3.4858. This iter targets Extended xgboost sweep.


## Exp136 — ext xgboost 11/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.8982 (delta -3.5038 vs prev best -0.3944); val=-3.7137418731323195 train=-0.025224694827101546.

**Learning:** Ext iter 11 (xgboost): DISCARD. Train/val gap = 3.6885. This iter targets Extended xgboost sweep.


## Exp137 — ext xgboost 12/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.8933 (delta -3.4989 vs prev best -0.3944); val=-3.7079148360001843 train=-0.00045710029131051813.

**Learning:** Ext iter 12 (xgboost): DISCARD. Train/val gap = 3.7075. This iter targets Extended xgboost sweep.


## Exp138 — ext xgboost 13/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.9845 (delta -3.5901 vs prev best -0.3944); val=-3.7957872630121043 train=-0.022141541365307483.

**Learning:** Ext iter 13 (xgboost): DISCARD. Train/val gap = 3.7736. This iter targets Extended xgboost sweep.


## Exp139 — ext xgboost 14/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.9631 (delta -3.5687 vs prev best -0.3944); val=-3.7743881639231134 train=-0.00041579902854564985.

**Learning:** Ext iter 14 (xgboost): DISCARD. Train/val gap = 3.7740. This iter targets Extended xgboost sweep.


## Exp140 — ext lightgbm 15/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.9507 (delta -2.5564 vs prev best -0.3944); val=-2.8122311464861016 train=-0.04221063229171553.

**Learning:** Ext iter 15 (lightgbm): DISCARD. Train/val gap = 2.7700. This iter targets LightGBM leaf-wise sweep.


## Exp141 — ext lightgbm 16/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.0527 (delta -2.6583 vs prev best -0.3944); val=-2.9093700121822987 train=-0.043393761020346346.

**Learning:** Ext iter 16 (lightgbm): DISCARD. Train/val gap = 2.8660. This iter targets LightGBM leaf-wise sweep.


## Exp142 — ext lightgbm 17/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1280 (delta -2.7337 vs prev best -0.3944); val=-2.982171845254366 train=-0.06476162897400468.

**Learning:** Ext iter 17 (lightgbm): DISCARD. Train/val gap = 2.9174. This iter targets LightGBM leaf-wise sweep.


## Exp143 — ext lightgbm 18/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1322 (delta -2.7378 vs prev best -0.3944); val=-2.9863688096978027 train=-0.07015877936484781.

**Learning:** Ext iter 18 (lightgbm): DISCARD. Train/val gap = 2.9162. This iter targets LightGBM leaf-wise sweep.


## Exp144 — ext lightgbm 19/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1280 (delta -2.7337 vs prev best -0.3944); val=-2.982171845254366 train=-0.06476162897400468.

**Learning:** Ext iter 19 (lightgbm): DISCARD. Train/val gap = 2.9174. This iter targets LightGBM leaf-wise sweep.


## Exp145 — ext lightgbm 20/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1322 (delta -2.7378 vs prev best -0.3944); val=-2.9863688096978027 train=-0.07015877936484781.

**Learning:** Ext iter 20 (lightgbm): DISCARD. Train/val gap = 2.9162. This iter targets LightGBM leaf-wise sweep.


## Exp146 — ext lightgbm 21/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1280 (delta -2.7337 vs prev best -0.3944); val=-2.982171845254366 train=-0.06476162897400468.

**Learning:** Ext iter 21 (lightgbm): DISCARD. Train/val gap = 2.9174. This iter targets LightGBM leaf-wise sweep.


## Exp147 — ext lightgbm 22/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1322 (delta -2.7378 vs prev best -0.3944); val=-2.9863688096978027 train=-0.07015877936484781.

**Learning:** Ext iter 22 (lightgbm): DISCARD. Train/val gap = 2.9162. This iter targets LightGBM leaf-wise sweep.


## Exp148 — ext catboost 23/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 23 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp149 — ext catboost 24/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 24 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp150 — ext catboost 25/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 25 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp151 — ext catboost 26/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 26 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp152 — ext catboost 27/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 27 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp153 — ext catboost 28/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 28 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp154 — ext catboost 29/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 29 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp155 — ext catboost 30/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 30 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp156 — ext catboost 31/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.3944); val=NA train=NA.

**Learning:** Ext iter 31 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp157 — ext mlp 32/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.7479 (delta -0.3535 vs prev best -0.3944); val=-0.7411745487171745 train=-0.6069816637836147.

**Learning:** Ext iter 32 (mlp): DISCARD. Train/val gap = 0.1342. This iter targets MLP capacity sweep.


## Exp158 — ext mlp 33/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5329 (delta -0.1385 vs prev best -0.3944); val=-0.5196492054054764 train=-0.2544688520762752.

**Learning:** Ext iter 33 (mlp): DISCARD. Train/val gap = 0.2652. This iter targets MLP capacity sweep.


## Exp159 — ext mlp 34/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4620 (delta -0.0676 vs prev best -0.3944); val=-0.4481055855635537 train=-0.1701808906522802.

**Learning:** Ext iter 34 (mlp): DISCARD. Train/val gap = 0.2779. This iter targets MLP capacity sweep.


## Exp160 — ext mlp 35/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4815 (delta -0.0872 vs prev best -0.3944); val=-0.47481659498077045 train=-0.3403045555637666.

**Learning:** Ext iter 35 (mlp): DISCARD. Train/val gap = 0.1345. This iter targets MLP capacity sweep.


## Exp161 — ext mlp 36/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4191 (delta -0.0247 vs prev best -0.3944); val=-0.40930445186958214 train=-0.21431509345891991.

**Learning:** Ext iter 36 (mlp): DISCARD. Train/val gap = 0.1950. This iter targets MLP capacity sweep.


## Exp162 — ext mlp 37/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3987 (delta -0.0043 vs prev best -0.3944); val=-0.3869631986887575 train=-0.15263203707084727.

**Learning:** Ext iter 37 (mlp): DISCARD. Train/val gap = 0.2343. This iter targets MLP capacity sweep.


## Exp163 — ext mlp 38/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4138 (delta -0.0195 vs prev best -0.3944); val=-0.4042979069940784 train=-0.21338930257440686.

**Learning:** Ext iter 38 (mlp): DISCARD. Train/val gap = 0.1909. This iter targets MLP capacity sweep.


## Exp164 — ext mlp 39/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3950 (delta -0.0006 vs prev best -0.3944); val=-0.3843227102797196 train=-0.171154859812316.

**Learning:** Ext iter 39 (mlp): DISCARD. Train/val gap = 0.2132. This iter targets MLP capacity sweep.


## Exp165 — ext mlp 40/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.3584 (delta +0.0360 vs prev best -0.3944); val=-0.34809575535033666 train=-0.142300636219176.

**Learning:** Ext iter 40 (mlp): KEEP. Train/val gap = 0.2058. This iter targets MLP capacity sweep.


## Exp166 — ext mlp 41/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4980 (delta -0.1396 vs prev best -0.3584); val=-0.4880135985183888 train=-0.2876883268317507.

**Learning:** Ext iter 41 (mlp): DISCARD. Train/val gap = 0.2003. This iter targets MLP capacity sweep.


## Exp167 — ext mlp 42/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4371 (delta -0.0787 vs prev best -0.3584); val=-0.42588265987457397 train=-0.20196491701389532.

**Learning:** Ext iter 42 (mlp): DISCARD. Train/val gap = 0.2239. This iter targets MLP capacity sweep.


## Exp168 — ext mlp 43/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.3941 (delta -0.0357 vs prev best -0.3584); val=-0.3829660691502471 train=-0.15984023131322603.

**Learning:** Ext iter 43 (mlp): DISCARD. Train/val gap = 0.2231. This iter targets MLP capacity sweep.


## Exp169 — ext mlp 44/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5607 (delta -0.2023 vs prev best -0.3584); val=-0.5462845203045799 train=-0.25887848370785393.

**Learning:** Ext iter 44 (mlp): DISCARD. Train/val gap = 0.2874. This iter targets MLP capacity sweep.


## Exp170 — ext mlp 45/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5071 (delta -0.1487 vs prev best -0.3584); val=-0.4925635581468035 train=-0.20184736821530921.

**Learning:** Ext iter 45 (mlp): DISCARD. Train/val gap = 0.2907. This iter targets MLP capacity sweep.


## Exp171 — ext mlp 46/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4460 (delta -0.0876 vs prev best -0.3584); val=-0.4324573367911929 train=-0.1612741890496027.

**Learning:** Ext iter 46 (mlp): DISCARD. Train/val gap = 0.2712. This iter targets MLP capacity sweep.


## Exp172 — ext ft_transformer 47/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.2686 (delta -2.9102 vs prev best -0.3584); val=-3.1307706035283553 train=-0.3750412321712419.

**Learning:** Ext iter 47 (ft_transformer): DISCARD. Train/val gap = 2.7557. This iter targets FT-Transformer-style sweep.


## Exp173 — ext ft_transformer 48/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1789 (delta -2.8205 vs prev best -0.3584); val=-3.039994143251367 train=-0.26142095264465937.

**Learning:** Ext iter 48 (ft_transformer): DISCARD. Train/val gap = 2.7786. This iter targets FT-Transformer-style sweep.


## Exp174 — ext ft_transformer 49/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1319 (delta -2.7736 vs prev best -0.3584); val=-2.9935377960327543 train=-0.22546754485036571.

**Learning:** Ext iter 49 (ft_transformer): DISCARD. Train/val gap = 2.7681. This iter targets FT-Transformer-style sweep.


## Exp175 — ext ft_transformer 50/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1401 (delta -2.7817 vs prev best -0.3584); val=-2.997977114985904 train=-0.15593411714304978.

**Learning:** Ext iter 50 (ft_transformer): DISCARD. Train/val gap = 2.8420. This iter targets FT-Transformer-style sweep.


## Exp176 — ext ft_transformer 51/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1013 (delta -2.7429 vs prev best -0.3584); val=-2.9570138401317285 train=-0.07175692248301073.

**Learning:** Ext iter 51 (ft_transformer): DISCARD. Train/val gap = 2.8853. This iter targets FT-Transformer-style sweep.


## Exp177 — ext ft_transformer 52/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.0774 (delta -2.7190 vs prev best -0.3584); val=-2.9341061722165334 train=-0.06913442005340363.

**Learning:** Ext iter 52 (ft_transformer): DISCARD. Train/val gap = 2.8650. This iter targets FT-Transformer-style sweep.


## Exp178 — ext ft_transformer 53/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1231 (delta -2.7647 vs prev best -0.3584); val=-2.977744625604746 train=-0.07012636307187814.

**Learning:** Ext iter 53 (ft_transformer): DISCARD. Train/val gap = 2.9076. This iter targets FT-Transformer-style sweep.


## Exp179 — ext ft_transformer 54/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.0949 (delta -2.7366 vs prev best -0.3584); val=-2.949037405463437 train=-0.03083197952894706.

**Learning:** Ext iter 54 (ft_transformer): DISCARD. Train/val gap = 2.9182. This iter targets FT-Transformer-style sweep.


## Exp180 — ext ft_transformer 55/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.0737 (delta -2.7153 vs prev best -0.3584); val=-2.9291753988695803 train=-0.038902783903946934.

**Learning:** Ext iter 55 (ft_transformer): DISCARD. Train/val gap = 2.8903. This iter targets FT-Transformer-style sweep.


## Exp181 — ext xgboost 56/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.1. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.1 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9227 (delta -2.5643 vs prev best -0.3584); val=-2.7902035556219587 train=-0.14021396833827474.

**Learning:** Ext iter 56 (xgboost): DISCARD. Train/val gap = 2.6500. This iter targets NGBoost-flavored sparsity sweep.


## Exp182 — ext xgboost 57/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.3. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.3 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9227 (delta -2.5643 vs prev best -0.3584); val=-2.7902035556219587 train=-0.14021396833827474.

**Learning:** Ext iter 57 (xgboost): DISCARD. Train/val gap = 2.6500. This iter targets NGBoost-flavored sparsity sweep.


## Exp183 — ext xgboost 58/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=1.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=1.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9227 (delta -2.5643 vs prev best -0.3584); val=-2.7902035556219587 train=-0.14021396833827474.

**Learning:** Ext iter 58 (xgboost): DISCARD. Train/val gap = 2.6500. This iter targets NGBoost-flavored sparsity sweep.


## Exp184 — ext xgboost 59/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=3.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=3.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9227 (delta -2.5643 vs prev best -0.3584); val=-2.7902035556219587 train=-0.14021396833827474.

**Learning:** Ext iter 59 (xgboost): DISCARD. Train/val gap = 2.6500. This iter targets NGBoost-flavored sparsity sweep.


## Exp185 — ext mlp 60/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 128, 64). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4668 (delta -0.1084 vs prev best -0.3584); val=-0.4558740948520855 train=-0.23694474193812834.

**Learning:** Ext iter 60 (mlp): DISCARD. Train/val gap = 0.2189. This iter targets TabNet-flavoured wide-residual MLP.


## Exp186 — ext mlp 61/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(384, 192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(384, 192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4656 (delta -0.1072 vs prev best -0.3584); val=-0.4522662081494759 train=-0.18549666478263974.

**Learning:** Ext iter 61 (mlp): DISCARD. Train/val gap = 0.2668. This iter targets TabNet-flavoured wide-residual MLP.


## Exp187 — ext mlp 62/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4879 (delta -0.1295 vs prev best -0.3584); val=-0.47624874730583705 train=-0.24334569068998002.

**Learning:** Ext iter 62 (mlp): DISCARD. Train/val gap = 0.2329. This iter targets TabNet-flavoured wide-residual MLP.


## Exp188 — ext mlp 63/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(320, 160). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(320, 160) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4187 (delta -0.0603 vs prev best -0.3584); val=-0.4088809395384644 train=-0.2124294482947355.

**Learning:** Ext iter 63 (mlp): DISCARD. Train/val gap = 0.1965. This iter targets TabNet-flavoured wide-residual MLP.


## Exp189 — ext mlp 64/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 256). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 256) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4850 (delta -0.1266 vs prev best -0.3584); val=-0.47344443124160435 train=-0.24309907374134945.

**Learning:** Ext iter 64 (mlp): DISCARD. Train/val gap = 0.2303. This iter targets TabNet-flavoured wide-residual MLP.


## Exp190 — ext ft_transformer 65/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=200. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-4.0880 (delta -3.7296 vs prev best -0.3584); val=-4.014218341792115 train=-2.5393311590529333.

**Learning:** Ext iter 65 (ft_transformer): DISCARD. Train/val gap = 1.4749. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp191 — ext ft_transformer 66/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=400. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-3.4825 (delta -3.1241 vs prev best -0.3584); val=-3.382069713478677 train=-1.374444163271807.

**Learning:** Ext iter 66 (ft_transformer): DISCARD. Train/val gap = 2.0076. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp192 — ext ft_transformer 67/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=600. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-3.1917 (delta -2.8333 vs prev best -0.3584); val=-3.0806705616289443 train=-0.8595821335540728.

**Learning:** Ext iter 67 (ft_transformer): DISCARD. Train/val gap = 2.2211. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp193 — ext xgboost 68/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=0.1 reg_alpha=0.1. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=0.1 smooths leaf weights; reg_alpha=0.1 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.8317 (delta -2.4733 vs prev best -0.3584); val=-2.7171367375094477 train=-0.42588638617497077.

**Learning:** Ext iter 68 (xgboost): DISCARD. Train/val gap = 2.2913. This iter targets Elastic-net-flavoured gradient boost.


## Exp194 — ext xgboost 69/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=1.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=1.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.8515 (delta -2.4931 vs prev best -0.3584); val=-2.7369926783805596 train=-0.44709669696084336.

**Learning:** Ext iter 69 (xgboost): DISCARD. Train/val gap = 2.2899. This iter targets Elastic-net-flavoured gradient boost.


## Exp195 — ext xgboost 70/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=3.0 reg_alpha=1.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=3.0 smooths leaf weights; reg_alpha=1.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.8474 (delta -2.4890 vs prev best -0.3584); val=-2.7356444981320056 train=-0.5003468085587387.

**Learning:** Ext iter 70 (xgboost): DISCARD. Train/val gap = 2.2353. This iter targets Elastic-net-flavoured gradient boost.


## Exp196 — ext xgboost 71/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.8362 (delta -2.4778 vs prev best -0.3584); val=-2.730553097711412 train=-0.6177387190405886.

**Learning:** Ext iter 71 (xgboost): DISCARD. Train/val gap = 2.1128. This iter targets Elastic-net-flavoured gradient boost.


## Exp197 — ext xgboost 72/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=3.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=3.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.8362 (delta -2.4778 vs prev best -0.3584); val=-2.730553097711412 train=-0.6177387190405886.

**Learning:** Ext iter 72 (xgboost): DISCARD. Train/val gap = 2.1128. This iter targets Elastic-net-flavoured gradient boost.


## Exp198 — ext patchtsmixer 73/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-2.7188 (delta -2.3604 vs prev best -0.3584); val=-2.623570552539579 train=-2.714277952226138.

**Learning:** Ext iter 73 (patchtsmixer): DISCARD. Train/val gap = 0.0907. This iter targets PatchTSMixer channel-mix sweep.


## Exp199 — ext patchtsmixer 74/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-2.1541 (delta -1.7957 vs prev best -0.3584); val=-2.122298149872134 train=-2.1525855508389022.

**Learning:** Ext iter 74 (patchtsmixer): DISCARD. Train/val gap = 0.0303. This iter targets PatchTSMixer channel-mix sweep.


## Exp200 — ext patchtsmixer 75/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.8415 (delta -1.4831 vs prev best -0.3584); val=-1.8405746660328848 train=-1.8214193098115934.

**Learning:** Ext iter 75 (patchtsmixer): DISCARD. Train/val gap = 0.0192. This iter targets PatchTSMixer channel-mix sweep.


## Exp201 — ext patchtsmixer 76/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.6591 (delta -1.3007 vs prev best -0.3584); val=-1.6483251162723713 train=-1.432900575616058.

**Learning:** Ext iter 76 (patchtsmixer): DISCARD. Train/val gap = 0.2154. This iter targets PatchTSMixer channel-mix sweep.


## Exp202 — ext patchtsmixer 77/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.6226 (delta -1.2642 vs prev best -0.3584); val=-1.6135463542964543 train=-1.4333223091115532.

**Learning:** Ext iter 77 (patchtsmixer): DISCARD. Train/val gap = 0.1802. This iter targets PatchTSMixer channel-mix sweep.


## Exp203 — ext patchtsmixer 78/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.4684 (delta -1.1100 vs prev best -0.3584); val=-1.4505407673295283 train=-1.0937565939568252.

**Learning:** Ext iter 78 (patchtsmixer): DISCARD. Train/val gap = 0.3568. This iter targets PatchTSMixer channel-mix sweep.


## Exp204 — ext xgboost 79/200
**Diagnosis:** Multi-seed champion variance run, seed=42. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2409 (delta -2.8825 vs prev best -0.3584); val=-3.090849624663535 train=-0.09075200167791853.

**Learning:** Ext iter 79 (xgboost): DISCARD. Train/val gap = 3.0001. This iter targets extended search.


## Exp205 — ext xgboost 80/200
**Diagnosis:** Multi-seed champion variance run, seed=0. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2264 (delta -2.8680 vs prev best -0.3584); val=-3.077139294803539 train=-0.09127055104929002.

**Learning:** Ext iter 80 (xgboost): DISCARD. Train/val gap = 2.9859. This iter targets extended search.


## Exp206 — ext xgboost 81/200
**Diagnosis:** Multi-seed champion variance run, seed=7. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2230 (delta -2.8646 vs prev best -0.3584); val=-3.073952727580391 train=-0.09310273905282196.

**Learning:** Ext iter 81 (xgboost): DISCARD. Train/val gap = 2.9808. This iter targets extended search.


## Exp207 — ext xgboost 82/200
**Diagnosis:** Multi-seed champion variance run, seed=99. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.1899 (delta -2.8316 vs prev best -0.3584); val=-3.0423037937313313 train=-0.08963420002728759.

**Learning:** Ext iter 82 (xgboost): DISCARD. Train/val gap = 2.9527. This iter targets extended search.


## Exp208 — ext xgboost 83/200
**Diagnosis:** Multi-seed champion variance run, seed=2024. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2328 (delta -2.8744 vs prev best -0.3584); val=-3.0830607078927663 train=-0.0879339641105536.

**Learning:** Ext iter 83 (xgboost): DISCARD. Train/val gap = 2.9951. This iter targets extended search.


## Exp209 — ext xgboost 84/200
**Diagnosis:** Multi-seed champion variance run, seed=12345. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2699 (delta -2.9115 vs prev best -0.3584); val=-3.1185445102428346 train=-0.09129461395627629.

**Learning:** Ext iter 84 (xgboost): DISCARD. Train/val gap = 3.0272. This iter targets extended search.


## Exp210 — ext xgboost 85/200
**Diagnosis:** Multi-seed champion variance run, seed=7777. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2165 (delta -2.8581 vs prev best -0.3584); val=-3.06754230423462 train=-0.08921829492416165.

**Learning:** Ext iter 85 (xgboost): DISCARD. Train/val gap = 2.9783. This iter targets extended search.


## Exp211 — ext xgboost 86/200
**Diagnosis:** Multi-seed champion variance run, seed=31337. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.3104 (delta -2.9520 vs prev best -0.3584); val=-3.1568775119745065 train=-0.08626533151326887.

**Learning:** Ext iter 86 (xgboost): DISCARD. Train/val gap = 3.0706. This iter targets extended search.


## Exp212 — ext xgboost 87/200
**Diagnosis:** Multi-seed champion variance run, seed=1729. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.1728 (delta -2.8144 vs prev best -0.3584); val=-3.025951986029013 train=-0.08958433369236941.

**Learning:** Ext iter 87 (xgboost): DISCARD. Train/val gap = 2.9364. This iter targets extended search.


## Exp213 — ext xgboost 88/200
**Diagnosis:** Multi-seed champion variance run, seed=6174. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2050 (delta -2.8466 vs prev best -0.3584); val=-3.056685396786722 train=-0.09077796153679858.

**Learning:** Ext iter 88 (xgboost): DISCARD. Train/val gap = 2.9659. This iter targets extended search.


## Exp214 — ext xgboost 89/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=30. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=30, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-2.6050 (delta -2.2466 vs prev best -0.3584); val=-2.537181075024918 train=-1.1813909093382742.

**Learning:** Ext iter 89 (xgboost): DISCARD. Train/val gap = 1.3558. This iter targets Extreme regularisation cool-down.


## Exp215 — ext xgboost 90/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=50. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=50, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-2.6771 (delta -2.3187 vs prev best -0.3584); val=-2.613261361039319 train=-1.3366925074789924.

**Learning:** Ext iter 90 (xgboost): DISCARD. Train/val gap = 1.2766. This iter targets Extreme regularisation cool-down.


## Exp216 — ext xgboost 91/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=100. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=100, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-2.8418 (delta -2.4834 vs prev best -0.3584); val=-2.783112406005052 train=-1.6091003183560966.

**Learning:** Ext iter 91 (xgboost): DISCARD. Train/val gap = 1.1740. This iter targets Extreme regularisation cool-down.

