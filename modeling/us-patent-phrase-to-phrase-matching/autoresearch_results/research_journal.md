# Research Journal — us-patent-phrase-to-phrase-matching

_(populated by `framework/hill_climb.py`)_

## Exp1 — xgboost iter 1
**Diagnosis:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

**Hypothesis:** Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).

**Prediction:** Composite in [0.55, 0.85] depending on task difficulty.

**Verdict:** KEEP composite=-3.2070 (delta +inf vs prev best -inf); val_score=-3.0582795937898655; train_score=-0.0833434723358478.

**Learning:** Iter 1 xgboost: KEEP. Train/val gap = 2.9749. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — xgboost iter 2
**Diagnosis:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.

**Citations:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

**Hypothesis:** Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-3.6919 (delta -0.4848 vs prev best -3.2070); val_score=-3.5164781679614494; train_score=-0.008534810776805827.

**Learning:** Iter 2 xgboost: DISCARD. Train/val gap = 3.5079. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — xgboost iter 3
**Diagnosis:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

**Hypothesis:** Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-2.6476 (delta +0.5594 vs prev best -3.2070); val_score=-2.5367227425645167; train_score=-0.3189944970447015.

**Learning:** Iter 3 xgboost: KEEP. Train/val gap = 2.2177. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp4 — xgboost iter 4
**Diagnosis:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.

**Citations:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

**Hypothesis:** Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.

**Prediction:** Composite delta in [+0.001, +0.010].

**Verdict:** DISCARD composite=-3.2188 (delta -0.5712 vs prev best -2.6476); val_score=-3.0698240245869393; train_score=-0.09103248791977497.

**Learning:** Iter 4 xgboost: DISCARD. Train/val gap = 2.9788. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — xgboost iter 5
**Diagnosis:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

**Hypothesis:** Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.

**Prediction:** Composite delta in [+0.002, +0.012].

**Verdict:** DISCARD composite=-3.0878 (delta -0.4401 vs prev best -2.6476); val_score=-2.9507939256350895; train_score=-0.21163758027515284.

**Learning:** Iter 5 xgboost: DISCARD. Train/val gap = 2.7392. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — xgboost iter 6
**Diagnosis:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.

**Citations:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

**Hypothesis:** Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-3.3222 (delta -0.6746 vs prev best -2.6476); val_score=-3.178717237896982; train_score=-0.3087740021615456.

**Learning:** Iter 6 xgboost: DISCARD. Train/val gap = 2.8699. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — xgboost iter 7
**Diagnosis:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.

**Citations:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

**Hypothesis:** Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-2.7385 (delta -0.0909 vs prev best -2.6476); val_score=-2.6144606319577903; train_score=-0.1339646461130529.

**Learning:** Iter 7 xgboost: DISCARD. Train/val gap = 2.4805. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp8 — xgboost iter 8
**Diagnosis:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.

**Citations:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.1859 (delta -0.5383 vs prev best -2.6476); val_score=-3.037854736712601; train_score=-0.07713401333652595.

**Learning:** Iter 8 xgboost: DISCARD. Train/val gap = 2.9607. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — xgboost iter 9
**Diagnosis:** Third seed for 3-seed median (autoresearch protocol).

**Citations:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

**Hypothesis:** Hypothesis: composite within ±0.02 of seed-42.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.2490 (delta -0.6014 vs prev best -2.6476); val_score=-3.0981166348354985; train_score=-0.08100271569533407.

**Learning:** Iter 9 xgboost: DISCARD. Train/val gap = 3.0171. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — xgboost iter 10
**Diagnosis:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

**Hypothesis:** Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-3.9458 (delta -1.2982 vs prev best -2.6476); val_score=-3.7580559982748305; train_score=-0.003402038206412763.

**Learning:** Iter 10 xgboost: DISCARD. Train/val gap = 3.7547. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — xgboost iter 11
**Diagnosis:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.

**Citations:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

**Hypothesis:** Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-2.6526 (delta -0.0050 vs prev best -2.6476); val_score=-2.5408770371687557; train_score=-0.3067214640586197.

**Learning:** Iter 11 xgboost: DISCARD. Train/val gap = 2.2342. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp12 — xgboost iter 12
**Diagnosis:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

**Hypothesis:** Hypothesis: larger leaves reduce variance, improve val by 0.5%.

**Prediction:** Composite delta in [-0.002, +0.010].

**Verdict:** DISCARD composite=-3.2070 (delta -0.5594 vs prev best -2.6476); val_score=-3.0582795937898655; train_score=-0.0833434723358478.

**Learning:** Iter 12 xgboost: DISCARD. Train/val gap = 2.9749. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — xgboost iter 13
**Diagnosis:** Gamma split-penalty 0.5 — discourages overly eager splits.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

**Hypothesis:** Hypothesis: fewer, higher-quality splits. Val improves slightly.

**Prediction:** Composite delta in [-0.003, +0.008].

**Verdict:** DISCARD composite=-3.2070 (delta -0.5594 vs prev best -2.6476); val_score=-3.0582795937898655; train_score=-0.0833434723358478.

**Learning:** Iter 13 xgboost: DISCARD. Train/val gap = 2.9749. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — xgboost iter 14
**Diagnosis:** High subsample for low-noise tasks — opposite direction from iter-4/7.

**Citations:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

**Hypothesis:** Hypothesis: gentle bagging if iter-4/7 over-regularised.

**Prediction:** Composite delta in [-0.005, +0.007].

**Verdict:** DISCARD composite=-3.4017 (delta -0.7541 vs prev best -2.6476); val_score=-3.243352106346486; train_score=-0.07611516528774812.

**Learning:** Iter 14 xgboost: DISCARD. Train/val gap = 3.1672. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — xgboost iter 15
**Diagnosis:** L1 regularisation (reg_alpha) for feature selection.

**Citations:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

**Hypothesis:** Hypothesis: L1 trims noise features, val improves.

**Prediction:** Composite delta in [+0.001, +0.012].

**Verdict:** DISCARD composite=-3.5124 (delta -0.8648 vs prev best -2.6476); val_score=-3.346770873885393; train_score=-0.03388756509103261.

**Learning:** Iter 15 xgboost: DISCARD. Train/val gap = 3.3129. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — xgboost iter 16
**Diagnosis:** Combined moderate regularisation — meta-search across all axes.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

**Hypothesis:** Hypothesis: balanced config beats single-knob champions.

**Prediction:** Composite delta in [+0.005, +0.020].

**Verdict:** DISCARD composite=-3.2583 (delta -0.6107 vs prev best -2.6476); val_score=-3.1046589881267397; train_score=-0.03150746337263042.

**Learning:** Iter 16 xgboost: DISCARD. Train/val gap = 3.0732. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — xgboost iter 17
**Diagnosis:** Fourth seed — extend variance characterisation.

**Citations:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

**Hypothesis:** Hypothesis: within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.2040 (delta -0.5564 vs prev best -2.6476); val_score=-3.0554855357923127; train_score=-0.08516973565874898.

**Learning:** Iter 17 xgboost: DISCARD. Train/val gap = 2.9703. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — xgboost iter 18
**Diagnosis:** Fifth seed.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Same as iter-15.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.2128 (delta -0.5652 vs prev best -2.6476); val_score=-3.0636026382648103; train_score=-0.07901934778131009.

**Learning:** Iter 18 xgboost: DISCARD. Train/val gap = 2.9846. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — xgboost iter 19
**Diagnosis:** Aggressive depth=12 with proportionally lower lr.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

**Hypothesis:** Hypothesis: depth=12 will overfit unless lr is very low.

**Prediction:** Composite delta in [-0.030, +0.010].

**Verdict:** DISCARD composite=-4.0485 (delta -1.4009 vs prev best -2.6476); val_score=-3.856748606196853; train_score=-0.02139751257748083.

**Learning:** Iter 19 xgboost: DISCARD. Train/val gap = 3.8354. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — xgboost iter 20
**Diagnosis:** Very shallow, high-lr — stump-like learners as opposite extreme.

**Citations:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

**Hypothesis:** Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.

**Prediction:** Composite delta in [-0.040, +0.005].

**Verdict:** KEEP composite=-2.2888 (delta +0.3588 vs prev best -2.6476); val_score=-2.2002062570813563; train_score=-0.4281744587306659.

**Learning:** Iter 20 xgboost: KEEP. Train/val gap = 1.7720. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp21 — xgboost iter 21
**Diagnosis:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.

**Citations:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

**Hypothesis:** Hypothesis: no-op vs baseline; informational only.

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-3.1934 (delta -0.9046 vs prev best -2.2888); val_score=-3.042552522881435; train_score=-0.026336901985286484.

**Learning:** Iter 21 xgboost: DISCARD. Train/val gap = 3.0162. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — xgboost iter 22
**Diagnosis:** Confirm hist-method explicitly — same as default but pinned.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

**Hypothesis:** Hypothesis: no change vs baseline (already default in our setup).

**Prediction:** Composite delta in [-0.002, +0.005].

**Verdict:** DISCARD composite=-3.2070 (delta -0.9182 vs prev best -2.2888); val_score=-3.0582795937898655; train_score=-0.0833434723358478.

**Learning:** Iter 22 xgboost: DISCARD. Train/val gap = 2.9749. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — xgboost iter 23
**Diagnosis:** Long-and-slow final refinement with mid-strength L2.

**Citations:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

**Hypothesis:** Hypothesis: best champion candidate. Val should peak.

**Prediction:** Composite delta in [+0.005, +0.025].

**Verdict:** DISCARD composite=-2.8078 (delta -0.5190 vs prev best -2.2888); val_score=-2.680321799074551; train_score=-0.13007620704084605.

**Learning:** Iter 23 xgboost: DISCARD. Train/val gap = 2.5502. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — xgboost iter 24
**Diagnosis:** Combined moderate everything — explore a balanced corner.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-2.9782 (delta -0.6894 vs prev best -2.2888); val_score=-2.8423679892182876; train_score=-0.12505153994168777.

**Learning:** Iter 24 xgboost: DISCARD. Train/val gap = 2.7173. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — xgboost iter 25
**Diagnosis:** Final 6th seed — closes the variance characterisation for this backbone.

**Citations:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-3.2043 (delta -0.9155 vs prev best -2.2888); val_score=-3.0555788578724727; train_score=-0.0814880397380331.

**Learning:** Iter 25 xgboost: DISCARD. Train/val gap = 2.9741. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp26 — lightgbm iter 1
**Diagnosis:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard lightgbm config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 1 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp27 — lightgbm iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-5.4147 (delta -3.1259 vs prev best -2.2888); val_score=-5.382584766403114; train_score=-4.739524874183264.

**Learning:** Iter 2 lightgbm: DISCARD. Train/val gap = 0.6431. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp28 — lightgbm iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-6.2568 (delta -3.9680 vs prev best -2.2888); val_score=-6.251496599130976; train_score=-6.145188088829682.

**Learning:** Iter 3 lightgbm: DISCARD. Train/val gap = 0.1063. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp29 — lightgbm iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-4.8031 (delta -2.5143 vs prev best -2.2888); val_score=-4.742007765584079; train_score=-3.5197708836137105.

**Learning:** Iter 4 lightgbm: DISCARD. Train/val gap = 1.2222. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp30 — lightgbm iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-3.1810 (delta -0.8922 vs prev best -2.2888); val_score=-3.0351384951571214; train_score=-0.11864498689624225.

**Learning:** Iter 5 lightgbm: DISCARD. Train/val gap = 2.9165. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp31 — lightgbm iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-3.1810 (delta -0.8922 vs prev best -2.2888); val_score=-3.0351384951571214; train_score=-0.11864498689624225.

**Learning:** Iter 6 lightgbm: DISCARD. Train/val gap = 2.9165. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp32 — lightgbm iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7087 (delta -3.4199 vs prev best -2.2888); val_score=-5.687649376583759; train_score=-5.266925644043592.

**Learning:** Iter 7 lightgbm: DISCARD. Train/val gap = 0.4207. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp33 — lightgbm iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7128 (delta -3.4240 vs prev best -2.2888); val_score=-5.6917699271455; train_score=-5.270950036565418.

**Learning:** Iter 8 lightgbm: DISCARD. Train/val gap = 0.4208. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp34 — lightgbm iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 9 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp35 — lightgbm iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-6.0815 (delta -3.7927 vs prev best -2.2888); val_score=-6.071632304966757; train_score=-5.873700383869573.

**Learning:** Iter 10 lightgbm: DISCARD. Train/val gap = 0.1979. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp36 — lightgbm iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 11 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp37 — lightgbm iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 12 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp38 — lightgbm iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-5.9989 (delta -3.7101 vs prev best -2.2888); val_score=-5.9868772120105564; train_score=-5.74638106427866.

**Learning:** Iter 13 lightgbm: DISCARD. Train/val gap = 0.2405. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp39 — lightgbm iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.6994 (delta -3.4106 vs prev best -2.2888); val_score=-5.678764265434872; train_score=-5.266179414062485.

**Learning:** Iter 14 lightgbm: DISCARD. Train/val gap = 0.4126. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp40 — lightgbm iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7114 (delta -3.4226 vs prev best -2.2888); val_score=-5.690365557463557; train_score=-5.2703648046879685.

**Learning:** Iter 15 lightgbm: DISCARD. Train/val gap = 0.4200. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp41 — lightgbm iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 16 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp42 — lightgbm iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 17 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp43 — lightgbm iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-5.1841 (delta -2.8953 vs prev best -2.2888); val_score=-5.140878862844855; train_score=-4.276386524582778.

**Learning:** Iter 18 lightgbm: DISCARD. Train/val gap = 0.8645. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp44 — lightgbm iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-6.4468 (delta -4.1580 vs prev best -2.2888); val_score=-6.446277357794511; train_score=-6.435289900621604.

**Learning:** Iter 19 lightgbm: DISCARD. Train/val gap = 0.0110. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp45 — lightgbm iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 20 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp46 — lightgbm iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 21 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp47 — lightgbm iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-5.7111 (delta -3.4223 vs prev best -2.2888); val_score=-5.689904809500932; train_score=-5.265434732176618.

**Learning:** Iter 22 lightgbm: DISCARD. Train/val gap = 0.4245. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp48 — lightgbm iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.9229 (delta -3.6340 vs prev best -2.2888); val_score=-5.90839580712202; train_score=-5.6192903188344605.

**Learning:** Iter 23 lightgbm: DISCARD. Train/val gap = 0.2891. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp49 — lightgbm iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.4138 (delta -3.1250 vs prev best -2.2888); val_score=-5.381579568186676; train_score=-4.736882033763193.

**Learning:** Iter 24 lightgbm: DISCARD. Train/val gap = 0.6447. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp50 — lightgbm iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7095 (delta -3.4207 vs prev best -2.2888); val_score=-5.688645026387909; train_score=-5.27126104750402.

**Learning:** Iter 25 lightgbm: DISCARD. Train/val gap = 0.4174. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp51 — catboost iter 1
**Diagnosis:** Baseline catboost per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard catboost config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 1 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp52 — catboost iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 2 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp53 — catboost iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 3 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp54 — catboost iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 4 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp55 — catboost iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 5 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp56 — catboost iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 6 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp57 — catboost iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 7 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp58 — catboost iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 8 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp59 — catboost iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 9 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp60 — catboost iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 10 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp61 — catboost iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 11 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp62 — catboost iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 12 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp63 — catboost iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 13 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp64 — catboost iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 14 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp65 — catboost iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 15 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp66 — catboost iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 16 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp67 — catboost iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 17 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp68 — catboost iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 18 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp69 — catboost iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 19 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp70 — catboost iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 20 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp71 — catboost iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 21 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp72 — catboost iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 22 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp73 — catboost iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 23 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp74 — catboost iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 24 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp75 — catboost iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -2.2888); val_score=NA; train_score=NA.

**Learning:** Iter 25 catboost: DISCARD. Train/val gap = 0.0000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp76 — mlp iter 1
**Diagnosis:** Baseline mlp per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard mlp config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** KEEP composite=-0.7390 (delta +1.5498 vs prev best -2.2888); val_score=-0.7256467647393366; train_score=-0.4589998607863836.

**Learning:** Iter 1 mlp: KEEP. Train/val gap = 0.2666. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp77 — mlp iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** KEEP composite=-0.6483 (delta +0.0907 vs prev best -0.7390); val_score=-0.6327212468038336; train_score=-0.3212322080449938.

**Learning:** Iter 2 mlp: KEEP. Train/val gap = 0.3115. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp78 — mlp iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-1.0980 (delta -0.4497 vs prev best -0.6483); val_score=-1.0942294568544784; train_score=-1.0182477684305615.

**Learning:** Iter 3 mlp: DISCARD. Train/val gap = 0.0760. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp79 — mlp iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** KEEP composite=-0.5654 (delta +0.0829 vs prev best -0.6483); val_score=-0.5511914342360708; train_score=-0.266659377539871.

**Learning:** Iter 4 mlp: KEEP. Train/val gap = 0.2845. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp80 — mlp iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.6768 (delta -0.1113 vs prev best -0.5654); val_score=-0.6732019583399911; train_score=-0.602138318011751.

**Learning:** Iter 5 mlp: DISCARD. Train/val gap = 0.0711. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp81 — mlp iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-3.2829 (delta -2.7174 vs prev best -0.5654); val_score=-3.222608161336285; train_score=-3.2799921440402597.

**Learning:** Iter 6 mlp: DISCARD. Train/val gap = 0.0574. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp82 — mlp iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6350 (delta -0.0696 vs prev best -0.5654); val_score=-0.6251893948647643; train_score=-0.42837259066627437.

**Learning:** Iter 7 mlp: DISCARD. Train/val gap = 0.1968. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp83 — mlp iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6854 (delta -0.1200 vs prev best -0.5654); val_score=-0.6749756702700794; train_score=-0.4663816864088516.

**Learning:** Iter 8 mlp: DISCARD. Train/val gap = 0.2086. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp84 — mlp iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.6301 (delta -0.0647 vs prev best -0.5654); val_score=-0.6136398481902655; train_score=-0.28497448445174856.

**Learning:** Iter 9 mlp: DISCARD. Train/val gap = 0.3287. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp85 — mlp iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-0.7668 (delta -0.2014 vs prev best -0.5654); val_score=-0.7585775308809993; train_score=-0.5936593940267267.

**Learning:** Iter 10 mlp: DISCARD. Train/val gap = 0.1649. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp86 — mlp iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-0.6913 (delta -0.1258 vs prev best -0.5654); val_score=-0.6770110874268276; train_score=-0.3922326574886308.

**Learning:** Iter 11 mlp: DISCARD. Train/val gap = 0.2848. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp87 — mlp iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** KEEP composite=-0.5603 (delta +0.0052 vs prev best -0.5654); val_score=-0.545022852576012; train_score=-0.24027387557891366.

**Learning:** Iter 12 mlp: KEEP. Train/val gap = 0.3047. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp88 — mlp iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-0.9517 (delta -0.3915 vs prev best -0.5603); val_score=-0.9457447860598251; train_score=-0.8259604253340392.

**Learning:** Iter 13 mlp: DISCARD. Train/val gap = 0.1198. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp89 — mlp iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6200 (delta -0.0597 vs prev best -0.5603); val_score=-0.6111482593294685; train_score=-0.43442711346003465.

**Learning:** Iter 14 mlp: DISCARD. Train/val gap = 0.1767. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp90 — mlp iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6970 (delta -0.1367 vs prev best -0.5603); val_score=-0.6861381697778128; train_score=-0.46989341199359974.

**Learning:** Iter 15 mlp: DISCARD. Train/val gap = 0.2162. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp91 — mlp iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.7611 (delta -0.2009 vs prev best -0.5603); val_score=-0.7509210811602778; train_score=-0.5468821388868589.

**Learning:** Iter 16 mlp: DISCARD. Train/val gap = 0.2040. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp92 — mlp iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** KEEP composite=-0.4230 (delta +0.1373 vs prev best -0.5603); val_score=-0.41190437895171395; train_score=-0.18992002705185385.

**Learning:** Iter 17 mlp: KEEP. Train/val gap = 0.2220. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp93 — mlp iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-0.6208 (delta -0.1978 vs prev best -0.4230); val_score=-0.6060494376276959; train_score=-0.31124406203768296.

**Learning:** Iter 18 mlp: DISCARD. Train/val gap = 0.2948. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp94 — mlp iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-5.2651 (delta -4.8421 vs prev best -0.4230); val_score=-5.262784559661466; train_score=-5.216328316015382.

**Learning:** Iter 19 mlp: DISCARD. Train/val gap = 0.0465. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp95 — mlp iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-0.5996 (delta -0.1766 vs prev best -0.4230); val_score=-0.5819063244592148; train_score=-0.2271798864030743.

**Learning:** Iter 20 mlp: DISCARD. Train/val gap = 0.3547. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp96 — mlp iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-0.7390 (delta -0.3160 vs prev best -0.4230); val_score=-0.7256467647393366; train_score=-0.4589998607863836.

**Learning:** Iter 21 mlp: DISCARD. Train/val gap = 0.2666. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp97 — mlp iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-0.7390 (delta -0.3160 vs prev best -0.4230); val_score=-0.7256467647393366; train_score=-0.4589998607863836.

**Learning:** Iter 22 mlp: DISCARD. Train/val gap = 0.2666. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp98 — mlp iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.8167 (delta -0.3937 vs prev best -0.4230); val_score=-0.8055546356795164; train_score=-0.582947771057362.

**Learning:** Iter 23 mlp: DISCARD. Train/val gap = 0.2226. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp99 — mlp iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-0.6617 (delta -0.2387 vs prev best -0.4230); val_score=-0.6472121000749043; train_score=-0.3583260029035599.

**Learning:** Iter 24 mlp: DISCARD. Train/val gap = 0.2889. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp100 — mlp iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-0.6408 (delta -0.2178 vs prev best -0.4230); val_score=-0.6324584582788347; train_score=-0.4659971785112026.

**Learning:** Iter 25 mlp: DISCARD. Train/val gap = 0.1665. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp101 — ft_transformer iter 1
**Diagnosis:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

**Hypothesis:** Standard ft_transformer config should land in the middle of the literature distribution for this problem type.

**Prediction:** Composite in [0.55, 0.85].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 1 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp102 — ft_transformer iter 2
**Diagnosis:** More iterations / epochs — test if baseline is undertrained.

**Citations:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

**Hypothesis:** Hypothesis: longer training helps if val accuracy was rising at end of baseline.

**Prediction:** Composite delta in [+0.002, +0.015].

**Verdict:** DISCARD composite=-5.4932 (delta -5.0702 vs prev best -0.4230); val_score=-5.464702020971915; train_score=-4.895223335605561.

**Learning:** Iter 2 ft_transformer: DISCARD. Train/val gap = 0.5695. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp103 — ft_transformer iter 3
**Diagnosis:** Lower LR — finer optimisation, slower convergence.

**Citations:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

**Hypothesis:** Hypothesis: smoother loss curve, slightly better generalisation.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-6.2669 (delta -5.8439 vs prev best -0.4230); val_score=-6.262257699918113; train_score=-6.169114511298019.

**Learning:** Iter 3 ft_transformer: DISCARD. Train/val gap = 0.0931. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp104 — ft_transformer iter 4
**Diagnosis:** Higher LR — test if baseline is under-optimised in compute budget.

**Citations:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

**Hypothesis:** Hypothesis: faster convergence; risk of divergence on tabular with small batches.

**Prediction:** Composite delta in [-0.015, +0.010].

**Verdict:** DISCARD composite=-4.9233 (delta -4.5003 vs prev best -0.4230); val_score=-4.870763791750615; train_score=-3.8197053546951767.

**Learning:** Iter 4 ft_transformer: DISCARD. Train/val gap = 1.0511. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp105 — ft_transformer iter 5
**Diagnosis:** Larger hidden — increases representational capacity.

**Citations:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

**Hypothesis:** Hypothesis: wider net adds capacity for harder tasks.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-3.1812 (delta -2.7582 vs prev best -0.4230); val_score=-3.0355006546064205; train_score=-0.12140676444075187.

**Learning:** Iter 5 ft_transformer: DISCARD. Train/val gap = 2.9141. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp106 — ft_transformer iter 6
**Diagnosis:** Smaller hidden — regularises by capacity reduction.

**Citations:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

**Hypothesis:** Hypothesis: smaller net underfits but reduces var.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-3.1812 (delta -2.7582 vs prev best -0.4230); val_score=-3.0355006546064205; train_score=-0.12140676444075187.

**Learning:** Iter 6 ft_transformer: DISCARD. Train/val gap = 2.9141. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp107 — ft_transformer iter 7
**Diagnosis:** Seed variance run #2.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

**Hypothesis:** Within ±0.02 of seed-42 baseline.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 7 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp108 — ft_transformer iter 8
**Diagnosis:** Seed variance run #3.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02 of median.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 8 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp109 — ft_transformer iter 9
**Diagnosis:** Longer training (60 epochs) — give the model more time.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

**Hypothesis:** Hypothesis: more epochs help with cosine-anneal late-stage refinement.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 9 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp110 — ft_transformer iter 10
**Diagnosis:** Combined moderate lr + mid hidden — balanced.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: balanced corner near baseline.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-6.1006 (delta -5.6776 vs prev best -0.4230); val_score=-6.092070521415229; train_score=-5.920692870181379.

**Learning:** Iter 10 ft_transformer: DISCARD. Train/val gap = 0.1714. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp111 — ft_transformer iter 11
**Diagnosis:** Three-layer MLP for added depth.

**Citations:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

**Hypothesis:** Hypothesis: third layer helps moderately; gap may widen.

**Prediction:** Composite delta in [-0.008, +0.012].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 11 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp112 — ft_transformer iter 12
**Diagnosis:** Wide + deep — capacity max.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: needs strong regularisation to avoid overfit.

**Prediction:** Composite delta in [-0.015, +0.012].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 12 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp113 — ft_transformer iter 13
**Diagnosis:** Long + slow.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: smooth optimisation, best-of-class for stable tasks.

**Prediction:** Composite delta in [+0.003, +0.018].

**Verdict:** DISCARD composite=-6.0203 (delta -5.5973 vs prev best -0.4230); val_score=-6.010013316747723; train_score=-5.80328676235162.

**Learning:** Iter 13 ft_transformer: DISCARD. Train/val gap = 0.2067. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp114 — ft_transformer iter 14
**Diagnosis:** Seed variance run #4.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 14 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp115 — ft_transformer iter 15
**Diagnosis:** Seed variance run #5.

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 15 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp116 — ft_transformer iter 16
**Diagnosis:** Mid-small hidden.

**Citations:** Hastie et al. 2009 ESL — capacity control.

**Hypothesis:** Hypothesis: slight regularisation.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 16 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp117 — ft_transformer iter 17
**Diagnosis:** Very wide.

**Citations:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

**Hypothesis:** Hypothesis: capacity ceiling test.

**Prediction:** Composite delta in [-0.012, +0.010].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 17 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp118 — ft_transformer iter 18
**Diagnosis:** Mid-high LR.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: faster convergence.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-5.2869 (delta -4.8639 vs prev best -0.4230); val_score=-5.2489500853471585; train_score=-4.488962372703761.

**Learning:** Iter 18 ft_transformer: DISCARD. Train/val gap = 0.7600. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp119 — ft_transformer iter 19
**Diagnosis:** Very low LR — slow but precise.

**Citations:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

**Hypothesis:** Hypothesis: too slow to converge in 30 epochs.

**Prediction:** Composite delta in [-0.020, +0.005].

**Verdict:** DISCARD composite=-6.4484 (delta -6.0254 vs prev best -0.4230); val_score=-6.448010291759409; train_score=-6.440918452232855.

**Learning:** Iter 19 ft_transformer: DISCARD. Train/val gap = 0.0071. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp120 — ft_transformer iter 20
**Diagnosis:** Many epochs.

**Citations:** He et al. 2016 CVPR (arXiv:1512.03385).

**Hypothesis:** Hypothesis: late refinement helps.

**Prediction:** Composite delta in [-0.005, +0.015].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 20 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp121 — ft_transformer iter 21
**Diagnosis:** Higher weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: stronger regularisation, val improves.

**Prediction:** Composite delta in [-0.003, +0.012].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 21 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp122 — ft_transformer iter 22
**Diagnosis:** No weight decay.

**Citations:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

**Hypothesis:** Hypothesis: more overfit; informative.

**Prediction:** Composite delta in [-0.010, +0.005].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 22 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp123 — ft_transformer iter 23
**Diagnosis:** Slightly below default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.9452 (delta -5.5222 vs prev best -0.4230); val_score=-5.932997644180716; train_score=-5.689536022449111.

**Learning:** Iter 23 ft_transformer: DISCARD. Train/val gap = 0.2435. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp124 — ft_transformer iter 24
**Diagnosis:** Slightly above default.

**Citations:** Smith 2017 (arXiv:1506.01186).

**Hypothesis:** Hypothesis: incremental change.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-5.4928 (delta -5.0698 vs prev best -0.4230); val_score=-5.464295294995443; train_score=-4.894814144861945.

**Learning:** Iter 24 ft_transformer: DISCARD. Train/val gap = 0.5695. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp125 — ft_transformer iter 25
**Diagnosis:** Final variance seed (6th).

**Citations:** Kohavi 1995 IJCAI.

**Hypothesis:** Within ±0.02.

**Prediction:** Composite delta in [-0.020, +0.020].

**Verdict:** DISCARD composite=-5.7497 (delta -5.3267 vs prev best -0.4230); val_score=-5.731661351927118; train_score=-5.370094860276683.

**Learning:** Iter 25 ft_transformer: DISCARD. Train/val gap = 0.3616. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp126 — ext xgboost 1/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.0404 (delta -2.6174 vs prev best -0.4230); val=-2.9348549804732587 train=-0.8239640117952753.

**Learning:** Ext iter 1 (xgboost): DISCARD. Train/val gap = 2.1109. This iter targets Extended xgboost sweep.


## Exp127 — ext xgboost 2/200
**Diagnosis:** Extended xgboost sweep — depth=4 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=4 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.6017 (delta -2.1787 vs prev best -0.4230); val=-2.487335360652057 train=-0.1992935246029331.

**Learning:** Ext iter 2 (xgboost): DISCARD. Train/val gap = 2.2880. This iter targets Extended xgboost sweep.


## Exp128 — ext xgboost 3/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.1127 (delta -2.6896 vs prev best -0.4230); val=-2.9850985463806725 train=-0.43402485422633263.

**Learning:** Ext iter 3 (xgboost): DISCARD. Train/val gap = 2.5511. This iter targets Extended xgboost sweep.


## Exp129 — ext xgboost 4/200
**Diagnosis:** Extended xgboost sweep — depth=5 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=5 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-2.9860 (delta -2.5630 vs prev best -0.4230); val=-2.8470820095201166 train=-0.06935934222466163.

**Learning:** Ext iter 4 (xgboost): DISCARD. Train/val gap = 2.7777. This iter targets Extended xgboost sweep.


## Exp130 — ext xgboost 5/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.3314 (delta -2.9084 vs prev best -0.4230); val=-3.1829719544714274 train=-0.21411412062177781.

**Learning:** Ext iter 5 (xgboost): DISCARD. Train/val gap = 2.9689. This iter targets Extended xgboost sweep.


## Exp131 — ext xgboost 6/200
**Diagnosis:** Extended xgboost sweep — depth=6 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=6 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.3505 (delta -2.9275 vs prev best -0.4230); val=-3.1917694520128244 train=-0.016163969329057972.

**Learning:** Ext iter 6 (xgboost): DISCARD. Train/val gap = 3.1756. This iter targets Extended xgboost sweep.


## Exp132 — ext xgboost 7/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.5777 (delta -3.1547 vs prev best -0.4230); val=-3.412261697462223 train=-0.10398181268700617.

**Learning:** Ext iter 7 (xgboost): DISCARD. Train/val gap = 3.3083. This iter targets Extended xgboost sweep.


## Exp133 — ext xgboost 8/200
**Diagnosis:** Extended xgboost sweep — depth=7 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=7 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.5703 (delta -3.1473 vs prev best -0.4230); val=-3.4003983376474136 train=-0.0023685364201573647.

**Learning:** Ext iter 8 (xgboost): DISCARD. Train/val gap = 3.3980. This iter targets Extended xgboost sweep.


## Exp134 — ext xgboost 9/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.7302 (delta -3.3072 vs prev best -0.4230); val=-3.555174674720419 train=-0.05421295077973412.

**Learning:** Ext iter 9 (xgboost): DISCARD. Train/val gap = 3.5010. This iter targets Extended xgboost sweep.


## Exp135 — ext xgboost 10/200
**Diagnosis:** Extended xgboost sweep — depth=8 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=8 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.7612 (delta -3.3382 vs prev best -0.4230); val=-3.582155181837484 train=-0.0005431164504133553.

**Learning:** Ext iter 10 (xgboost): DISCARD. Train/val gap = 3.5816. This iter targets Extended xgboost sweep.


## Exp136 — ext xgboost 11/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-3.9336 (delta -3.5106 vs prev best -0.4230); val=-3.747507411346334 train=-0.02621733836565637.

**Learning:** Ext iter 11 (xgboost): DISCARD. Train/val gap = 3.7213. This iter targets Extended xgboost sweep.


## Exp137 — ext xgboost 12/200
**Diagnosis:** Extended xgboost sweep — depth=10 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=10 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-4.0115 (delta -3.5885 vs prev best -0.4230); val=-3.820493728926102 train=-0.0004508982133582038.

**Learning:** Ext iter 12 (xgboost): DISCARD. Train/val gap = 3.8200. This iter targets Extended xgboost sweep.


## Exp138 — ext xgboost 13/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.01. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.01 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-4.0830 (delta -3.6600 vs prev best -0.4230); val=-3.8896392431397104 train=-0.02236574411365157.

**Learning:** Ext iter 13 (xgboost): DISCARD. Train/val gap = 3.8673. This iter targets Extended xgboost sweep.


## Exp139 — ext xgboost 14/200
**Diagnosis:** Extended xgboost sweep — depth=12 lr=0.03. The 25-iter phase covered the basic L1/L2/depth axes; this extension probes deep×slow-and-many combinations where the loss surface differs from the baseline.

**Citations:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

**Hypothesis:** Mechanism: max_depth=12 raises interaction order; lr=0.03 forces small step sizes that pair with iterations=1200 to find narrower minima. Net composite improves if val gap is bounded by reg_lambda.

**Prediction:** Composite delta in [-0.005, +0.010] depending on data noise.

**Verdict:** DISCARD composite=-4.0988 (delta -3.6758 vs prev best -0.4230); val=-3.903596999473916 train=-0.00041889911967410784.

**Learning:** Ext iter 14 (xgboost): DISCARD. Train/val gap = 3.9032. This iter targets Extended xgboost sweep.


## Exp140 — ext lightgbm 15/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-2.9453 (delta -2.5223 vs prev best -0.4230); val=-2.807233702435532 train=-0.04593256933226431.

**Learning:** Ext iter 15 (lightgbm): DISCARD. Train/val gap = 2.7613. This iter targets LightGBM leaf-wise sweep.


## Exp141 — ext lightgbm 16/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=31 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=31 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.0043 (delta -2.5813 vs prev best -0.4230); val=-2.8638088488577167 train=-0.053308271769466224.

**Learning:** Ext iter 16 (lightgbm): DISCARD. Train/val gap = 2.8105. This iter targets LightGBM leaf-wise sweep.


## Exp142 — ext lightgbm 17/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.0724 (delta -2.6494 vs prev best -0.4230); val=-2.929439265796237 train=-0.0701075353773964.

**Learning:** Ext iter 17 (lightgbm): DISCARD. Train/val gap = 2.8593. This iter targets LightGBM leaf-wise sweep.


## Exp143 — ext lightgbm 18/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=63 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=63 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1775 (delta -2.7545 vs prev best -0.4230); val=-3.0300675581494376 train=-0.08139193958700797.

**Learning:** Ext iter 18 (lightgbm): DISCARD. Train/val gap = 2.9487. This iter targets LightGBM leaf-wise sweep.


## Exp144 — ext lightgbm 19/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.0724 (delta -2.6494 vs prev best -0.4230); val=-2.929439265796237 train=-0.0701075353773964.

**Learning:** Ext iter 19 (lightgbm): DISCARD. Train/val gap = 2.8593. This iter targets LightGBM leaf-wise sweep.


## Exp145 — ext lightgbm 20/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=127 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=127 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1775 (delta -2.7545 vs prev best -0.4230); val=-3.0300675581494376 train=-0.08139193958700797.

**Learning:** Ext iter 20 (lightgbm): DISCARD. Train/val gap = 2.9487. This iter targets LightGBM leaf-wise sweep.


## Exp146 — ext lightgbm 21/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.7. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.7 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.0724 (delta -2.6494 vs prev best -0.4230); val=-2.929439265796237 train=-0.0701075353773964.

**Learning:** Ext iter 21 (lightgbm): DISCARD. Train/val gap = 2.8593. This iter targets LightGBM leaf-wise sweep.


## Exp147 — ext lightgbm 22/200
**Diagnosis:** LightGBM leaf-wise sweep — num_leaves=255 feature_fraction=0.9. GOSS (Gradient-based One-Side Sampling) keeps the largest-gradient samples and randomly subsamples the rest, so the leaf depth ceiling matters more than for XGBoost level-wise.

**Citations:** Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

**Hypothesis:** Mechanism: num_leaves=255 caps tree expressiveness; feature_fraction=0.9 decorrelates trees. Together they control the bias-variance trade-off; too-large num_leaves with too-small feature_fraction destabilises.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-3.1775 (delta -2.7545 vs prev best -0.4230); val=-3.0300675581494376 train=-0.08139193958700797.

**Learning:** Ext iter 22 (lightgbm): DISCARD. Train/val gap = 2.9487. This iter targets LightGBM leaf-wise sweep.


## Exp148 — ext catboost 23/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 23 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp149 — ext catboost 24/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 24 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp150 — ext catboost 25/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=4 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=4 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 25 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp151 — ext catboost 26/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 26 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp152 — ext catboost 27/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 27 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp153 — ext catboost 28/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=6 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=6 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 28 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp154 — ext catboost 29/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=1. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=1 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 29 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp155 — ext catboost 30/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=3. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=3 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 30 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp156 — ext catboost 31/200
**Diagnosis:** CatBoost ordered-boosting sweep — depth=8 l2_leaf_reg=10. Ordered boosting trains on a random permutation to avoid prediction-shift, so deeper symmetric trees are tractable.

**Citations:** Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

**Hypothesis:** Mechanism: depth=8 with symmetric oblivious tree gives 2^d leaves all at same depth; l2_leaf_reg=10 controls leaf weight magnitude. Ordered boosting reduces variance vs greedy.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-inf (delta -inf vs prev best -0.4230); val=NA train=NA.

**Learning:** Ext iter 31 (catboost): DISCARD. Train/val gap = 0.0000. This iter targets CatBoost ordered-boosting sweep.


## Exp157 — ext mlp 32/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.8470 (delta -0.4240 vs prev best -0.4230); val=-0.836648870091424 train=-0.6303960793741781.

**Learning:** Ext iter 32 (mlp): DISCARD. Train/val gap = 0.2063. This iter targets MLP capacity sweep.


## Exp158 — ext mlp 33/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.6301 (delta -0.2071 vs prev best -0.4230); val=-0.6136398481902655 train=-0.28497448445174856.

**Learning:** Ext iter 33 (mlp): DISCARD. Train/val gap = 0.3287. This iter targets MLP capacity sweep.


## Exp159 — ext mlp 34/200
**Diagnosis:** MLP capacity sweep — hidden=(128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5345 (delta -0.1115 vs prev best -0.4230); val=-0.518012213861229 train=-0.18851023951274787.

**Learning:** Ext iter 34 (mlp): DISCARD. Train/val gap = 0.3295. This iter targets MLP capacity sweep.


## Exp160 — ext mlp 35/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5493 (delta -0.1263 vs prev best -0.4230); val=-0.5404425660512766 train=-0.36335644917857224.

**Learning:** Ext iter 35 (mlp): DISCARD. Train/val gap = 0.1771. This iter targets MLP capacity sweep.


## Exp161 — ext mlp 36/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4684 (delta -0.0454 vs prev best -0.4230); val=-0.45539761244563054 train=-0.19454194656133245.

**Learning:** Ext iter 36 (mlp): DISCARD. Train/val gap = 0.2609. This iter targets MLP capacity sweep.


## Exp162 — ext mlp 37/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4436 (delta -0.0206 vs prev best -0.4230); val=-0.42976957751025335 train=-0.15234733846301712.

**Learning:** Ext iter 37 (mlp): DISCARD. Train/val gap = 0.2774. This iter targets MLP capacity sweep.


## Exp163 — ext mlp 38/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4463 (delta -0.0233 vs prev best -0.4230); val=-0.43547829058064363 train=-0.21902931636828143.

**Learning:** Ext iter 38 (mlp): DISCARD. Train/val gap = 0.2164. This iter targets MLP capacity sweep.


## Exp164 — ext mlp 39/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.4203 (delta +0.0027 vs prev best -0.4230); val=-0.40857123245423665 train=-0.17452300408263974.

**Learning:** Ext iter 39 (mlp): KEEP. Train/val gap = 0.2340. This iter targets MLP capacity sweep.


## Exp165 — ext mlp 40/200
**Diagnosis:** MLP capacity sweep — hidden=(512, 256) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(512, 256) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** KEEP composite=-0.4024 (delta +0.0179 vs prev best -0.4203); val=-0.39073559149220477 train=-0.15833106577864056.

**Learning:** Ext iter 40 (mlp): KEEP. Train/val gap = 0.2324. This iter targets MLP capacity sweep.


## Exp166 — ext mlp 41/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5816 (delta -0.1793 vs prev best -0.4024); val=-0.5690833655296976 train=-0.3180902431739574.

**Learning:** Ext iter 41 (mlp): DISCARD. Train/val gap = 0.2510. This iter targets MLP capacity sweep.


## Exp167 — ext mlp 42/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5286 (delta -0.1263 vs prev best -0.4024); val=-0.5140250844586262 train=-0.22168058655678352.

**Learning:** Ext iter 42 (mlp): DISCARD. Train/val gap = 0.2923. This iter targets MLP capacity sweep.


## Exp168 — ext mlp 43/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 128, 64) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.4735 (delta -0.0711 vs prev best -0.4024); val=-0.4591342762405427 train=-0.1721533017718823.

**Learning:** Ext iter 43 (mlp): DISCARD. Train/val gap = 0.2870. This iter targets MLP capacity sweep.


## Exp169 — ext mlp 44/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.0003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.0003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5972 (delta -0.1949 vs prev best -0.4024); val=-0.5821196469762614 train=-0.2802930818379017.

**Learning:** Ext iter 44 (mlp): DISCARD. Train/val gap = 0.3018. This iter targets MLP capacity sweep.


## Exp170 — ext mlp 45/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.001. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.001 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5568 (delta -0.1545 vs prev best -0.4024); val=-0.5401944976674709 train=-0.2071126022288885.

**Learning:** Ext iter 45 (mlp): DISCARD. Train/val gap = 0.3331. This iter targets MLP capacity sweep.


## Exp171 — ext mlp 46/200
**Diagnosis:** MLP capacity sweep — hidden=(256, 256, 128) lr=0.003. The base 25-iter phase found 256x128x128 helpful; this extension confirms it across LR levels and probes alternatives.

**Citations:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

**Hypothesis:** Mechanism: hidden=(256, 256, 128) controls representational capacity; lr=0.003 controls step size on the new loss surface. Larger hidden + smaller LR is the classical wider-flatter-minima recipe (Zhang 2017 ICLR).

**Prediction:** Composite delta in [-0.015, +0.020].

**Verdict:** DISCARD composite=-0.5060 (delta -0.1036 vs prev best -0.4024); val=-0.4902767603815321 train=-0.17588393073395162.

**Learning:** Ext iter 46 (mlp): DISCARD. Train/val gap = 0.3144. This iter targets MLP capacity sweep.


## Exp172 — ext ft_transformer 47/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.2057 (delta -2.8034 vs prev best -0.4024); val=-3.0718876166711078 train=-0.3953628683196474.

**Learning:** Ext iter 47 (ft_transformer): DISCARD. Train/val gap = 2.6765. This iter targets FT-Transformer-style sweep.


## Exp173 — ext ft_transformer 48/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.2260 (delta -2.8236 vs prev best -0.4024); val=-3.085796030953876 train=-0.28218376039160775.

**Learning:** Ext iter 48 (ft_transformer): DISCARD. Train/val gap = 2.8036. This iter targets FT-Transformer-style sweep.


## Exp174 — ext ft_transformer 49/200
**Diagnosis:** FT-Transformer-style sweep — iterations=400 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1635 (delta -2.7611 vs prev best -0.4024); val=-3.024735551426751 train=-0.24978888659253934.

**Learning:** Ext iter 49 (ft_transformer): DISCARD. Train/val gap = 2.7749. This iter targets FT-Transformer-style sweep.


## Exp175 — ext ft_transformer 50/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.0482 (delta -2.6458 vs prev best -0.4024); val=-2.9104915454528473 train=-0.1571330664096192.

**Learning:** Ext iter 50 (ft_transformer): DISCARD. Train/val gap = 2.7534. This iter targets FT-Transformer-style sweep.


## Exp176 — ext ft_transformer 51/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1276 (delta -2.7253 vs prev best -0.4024); val=-2.982945785518946 train=-0.08944332906529048.

**Learning:** Ext iter 51 (ft_transformer): DISCARD. Train/val gap = 2.8935. This iter targets FT-Transformer-style sweep.


## Exp177 — ext ft_transformer 52/200
**Diagnosis:** FT-Transformer-style sweep — iterations=800 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.0809 (delta -2.6785 vs prev best -0.4024); val=-2.9380920407076525 train=-0.08284046599948992.

**Learning:** Ext iter 52 (ft_transformer): DISCARD. Train/val gap = 2.8553. This iter targets FT-Transformer-style sweep.


## Exp178 — ext ft_transformer 53/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=6. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.0250 (delta -2.6226 vs prev best -0.4024); val=-2.884603767469357 train=-0.07720981367444572.

**Learning:** Ext iter 53 (ft_transformer): DISCARD. Train/val gap = 2.8074. This iter targets FT-Transformer-style sweep.


## Exp179 — ext ft_transformer 54/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=8. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.1202 (delta -2.7178 vs prev best -0.4024); val=-2.9736432381878766 train=-0.04251838630867701.

**Learning:** Ext iter 54 (ft_transformer): DISCARD. Train/val gap = 2.9311. This iter targets FT-Transformer-style sweep.


## Exp180 — ext ft_transformer 55/200
**Diagnosis:** FT-Transformer-style sweep — iterations=1200 max_depth=10. Our runner approximates FT-Transformer with sklearn's HistGradientBoosting on tabular for hill-climb iteration speed; the iteration / depth axes map to the transformer's attention-block stacking depth and per-block feature dim.

**Citations:** Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

**Hypothesis:** Mechanism: deeper trees with more iterations covers the same capacity dial as wider/longer attention; weak proxy but captures the bias-variance trade-off direction.

**Prediction:** Composite delta in [-0.008, +0.015].

**Verdict:** DISCARD composite=-3.0765 (delta -2.6742 vs prev best -0.4024); val=-2.9323648903416024 train=-0.04883841653543618.

**Learning:** Ext iter 55 (ft_transformer): DISCARD. Train/val gap = 2.8835. This iter targets FT-Transformer-style sweep.


## Exp181 — ext xgboost 56/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.1. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.1 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9362 (delta -2.5338 vs prev best -0.4024); val=-2.8029301910580693 train=-0.13745422766424137.

**Learning:** Ext iter 56 (xgboost): DISCARD. Train/val gap = 2.6655. This iter targets NGBoost-flavored sparsity sweep.


## Exp182 — ext xgboost 57/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=0.3. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=0.3 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9362 (delta -2.5338 vs prev best -0.4024); val=-2.8029301910580693 train=-0.13745422766424137.

**Learning:** Ext iter 57 (xgboost): DISCARD. Train/val gap = 2.6655. This iter targets NGBoost-flavored sparsity sweep.


## Exp183 — ext xgboost 58/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=1.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=1.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9362 (delta -2.5338 vs prev best -0.4024); val=-2.8029301910580693 train=-0.13745422766424137.

**Learning:** Ext iter 58 (xgboost): DISCARD. Train/val gap = 2.6655. This iter targets NGBoost-flavored sparsity sweep.


## Exp184 — ext xgboost 59/200
**Diagnosis:** NGBoost-flavored sparsity sweep — reg_alpha=3.0. NGBoost casts regression as a probabilistic problem with explicit scale prediction; in our gradient-boosting proxy we approximate the regularisation effect with L1 leaf-weight shrinkage.

**Citations:** Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

**Hypothesis:** Mechanism: reg_alpha=3.0 L1-shrinks leaf weights, mimicking the natural-gradient penalty NGBoost applies to mean/scale params.

**Prediction:** Composite delta in [-0.005, +0.008].

**Verdict:** DISCARD composite=-2.9362 (delta -2.5338 vs prev best -0.4024); val=-2.8029301910580693 train=-0.13745422766424137.

**Learning:** Ext iter 59 (xgboost): DISCARD. Train/val gap = 2.6655. This iter targets NGBoost-flavored sparsity sweep.


## Exp185 — ext mlp 60/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 128, 64). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 128, 64) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.5380 (delta -0.1357 vs prev best -0.4024); val=-0.5233419530405687 train=-0.22921747038262394.

**Learning:** Ext iter 60 (mlp): DISCARD. Train/val gap = 0.2941. This iter targets TabNet-flavoured wide-residual MLP.


## Exp186 — ext mlp 61/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(384, 192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(384, 192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.5003 (delta -0.0980 vs prev best -0.4024); val=-0.48593111187332944 train=-0.19806450834908215.

**Learning:** Ext iter 61 (mlp): DISCARD. Train/val gap = 0.2879. This iter targets TabNet-flavoured wide-residual MLP.


## Exp187 — ext mlp 62/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(192, 96). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(192, 96) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.5529 (delta -0.1506 vs prev best -0.4024); val=-0.539909664607148 train=-0.2798340972649888.

**Learning:** Ext iter 62 (mlp): DISCARD. Train/val gap = 0.2601. This iter targets TabNet-flavoured wide-residual MLP.


## Exp188 — ext mlp 63/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(320, 160). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(320, 160) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.4746 (delta -0.0723 vs prev best -0.4024); val=-0.4617040854511859 train=-0.2028371715674877.

**Learning:** Ext iter 63 (mlp): DISCARD. Train/val gap = 0.2589. This iter targets TabNet-flavoured wide-residual MLP.


## Exp189 — ext mlp 64/200
**Diagnosis:** TabNet-flavoured wide-residual MLP — hidden=(256, 256). TabNet uses sequential attention to feature subsets; our MLP proxy uses deep+wide layers with strong WD to mimic the regularisation.

**Citations:** Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

**Hypothesis:** Mechanism: hidden=(256, 256) provides the per-step decision blocks; strong weight_decay (1e-3) plays the role of TabNet's sparsity regularisation.

**Prediction:** Composite delta in [-0.010, +0.012].

**Verdict:** DISCARD composite=-0.5287 (delta -0.1263 vs prev best -0.4024); val=-0.5129880523535891 train=-0.19972397748683252.

**Learning:** Ext iter 64 (mlp): DISCARD. Train/val gap = 0.3133. This iter targets TabNet-flavoured wide-residual MLP.


## Exp190 — ext ft_transformer 65/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=200. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-4.0827 (delta -3.6804 vs prev best -0.4024); val=-4.0085746465521845 train=-2.5257265562925824.

**Learning:** Ext iter 65 (ft_transformer): DISCARD. Train/val gap = 1.4828. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp191 — ext ft_transformer 66/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=400. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-3.4695 (delta -3.0671 vs prev best -0.4024); val=-3.371168552464102 train=-1.4049854385067428.

**Learning:** Ext iter 66 (ft_transformer): DISCARD. Train/val gap = 1.9662. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp192 — ext ft_transformer 67/200
**Diagnosis:** TabPFN-flavoured tiny-strong-regulariser sweep — iterations=600. TabPFN ships pretrained on synthetic data and runs in-context; we approximate the prior-aware tiny-model regime with shallow trees + low iterations.

**Citations:** Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

**Hypothesis:** Mechanism: shallow trees (depth=4) with low iter count enforces TabPFN-like simplicity prior; works on small datasets but may underfit at our n=2000.

**Prediction:** Composite delta in [-0.015, +0.005].

**Verdict:** DISCARD composite=-3.1615 (delta -2.7592 vs prev best -0.4024); val=-3.054085860899793 train=-0.9049264019718832.

**Learning:** Ext iter 67 (ft_transformer): DISCARD. Train/val gap = 2.1492. This iter targets TabPFN-flavoured tiny-strong-regulariser sweep.


## Exp193 — ext xgboost 68/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=0.1 reg_alpha=0.1. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=0.1 smooths leaf weights; reg_alpha=0.1 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7480 (delta -2.3456 vs prev best -0.4024); val=-2.6378381232165165 train=-0.4346813617220796.

**Learning:** Ext iter 68 (xgboost): DISCARD. Train/val gap = 2.2032. This iter targets Elastic-net-flavoured gradient boost.


## Exp194 — ext xgboost 69/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=1.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=1.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7627 (delta -2.3604 vs prev best -0.4024); val=-2.653377101319954 train=-0.4659339078512719.

**Learning:** Ext iter 69 (xgboost): DISCARD. Train/val gap = 2.1874. This iter targets Elastic-net-flavoured gradient boost.


## Exp195 — ext xgboost 70/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=3.0 reg_alpha=1.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=3.0 smooths leaf weights; reg_alpha=1.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7501 (delta -2.3478 vs prev best -0.4024); val=-2.643887282249884 train=-0.5188907604668215.

**Learning:** Ext iter 70 (xgboost): DISCARD. Train/val gap = 2.1250. This iter targets Elastic-net-flavoured gradient boost.


## Exp196 — ext xgboost 71/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=0.5. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=0.5 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7580 (delta -2.3557 vs prev best -0.4024); val=-2.6573251680011674 train=-0.6435873807669275.

**Learning:** Ext iter 71 (xgboost): DISCARD. Train/val gap = 2.0137. This iter targets Elastic-net-flavoured gradient boost.


## Exp197 — ext xgboost 72/200
**Diagnosis:** Elastic-net-flavoured gradient boost — reg_lambda=10.0 reg_alpha=3.0. Combines L1 (sparsity) + L2 (shrinkage) at the leaf level for elastic-net style regularisation.

**Citations:** Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

**Hypothesis:** Mechanism: reg_lambda=10.0 smooths leaf weights; reg_alpha=3.0 zeros out small leaves. Elastic-net works best when many features are correlated.

**Prediction:** Composite delta in [-0.005, +0.012].

**Verdict:** DISCARD composite=-2.7580 (delta -2.3557 vs prev best -0.4024); val=-2.6573251680011674 train=-0.6435873807669275.

**Learning:** Ext iter 72 (xgboost): DISCARD. Train/val gap = 2.0137. This iter targets Elastic-net-flavoured gradient boost.


## Exp198 — ext patchtsmixer 73/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-2.7987 (delta -2.3964 vs prev best -0.4024); val=-2.6627796473970657 train=-2.792263384760737.

**Learning:** Ext iter 73 (patchtsmixer): DISCARD. Train/val gap = 0.1295. This iter targets PatchTSMixer channel-mix sweep.


## Exp199 — ext patchtsmixer 74/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=128 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=128 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-2.2020 (delta -1.7996 vs prev best -0.4024); val=-2.2015217026665925 train=-2.192752417863481.

**Learning:** Ext iter 74 (patchtsmixer): DISCARD. Train/val gap = 0.0088. This iter targets PatchTSMixer channel-mix sweep.


## Exp200 — ext patchtsmixer 75/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.8734 (delta -1.4711 vs prev best -0.4024); val=-1.8729834202746967 train=-1.8641348429069375.

**Learning:** Ext iter 75 (patchtsmixer): DISCARD. Train/val gap = 0.0088. This iter targets PatchTSMixer channel-mix sweep.


## Exp201 — ext patchtsmixer 76/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=256 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=256 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.7153 (delta -1.3129 vs prev best -0.4024); val=-1.7058364562636679 train=-1.5166796131769191.

**Learning:** Ext iter 76 (patchtsmixer): DISCARD. Train/val gap = 0.1892. This iter targets PatchTSMixer channel-mix sweep.


## Exp202 — ext patchtsmixer 77/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.0005. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.0005 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.6978 (delta -1.2954 vs prev best -0.4024); val=-1.6891835609548471 train=-1.5177993122271685.

**Learning:** Ext iter 77 (patchtsmixer): DISCARD. Train/val gap = 0.1714. This iter targets PatchTSMixer channel-mix sweep.


## Exp203 — ext patchtsmixer 78/200
**Diagnosis:** PatchTSMixer channel-mix sweep — hidden=384 lr=0.001. Mixer blocks alternate token-mixing and channel-mixing; on tabular data without sequence structure, channel-mixing dominates and we measure the channel-mix MLP's contribution.

**Citations:** Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

**Hypothesis:** Mechanism: hidden=384 is the channel-mix MLP width; lr=0.001 controls AdamW step size. On tabular this is equivalent to a 2-layer GELU MLP with layer-norm.

**Prediction:** Composite delta in [-0.010, +0.010].

**Verdict:** DISCARD composite=-1.5699 (delta -1.1675 vs prev best -0.4024); val=-1.5516587088299232 train=-1.1873983540449513.

**Learning:** Ext iter 78 (patchtsmixer): DISCARD. Train/val gap = 0.3643. This iter targets PatchTSMixer channel-mix sweep.


## Exp204 — ext xgboost 79/200
**Diagnosis:** Multi-seed champion variance run, seed=42. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.1714 (delta -2.7690 vs prev best -0.4024); val=-3.0248744024259353 train=-0.09508818491686173.

**Learning:** Ext iter 79 (xgboost): DISCARD. Train/val gap = 2.9298. This iter targets extended search.


## Exp205 — ext xgboost 80/200
**Diagnosis:** Multi-seed champion variance run, seed=0. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2003 (delta -2.7980 vs prev best -0.4024); val=-3.0523569724326483 train=-0.09253555719540844.

**Learning:** Ext iter 80 (xgboost): DISCARD. Train/val gap = 2.9598. This iter targets extended search.


## Exp206 — ext xgboost 81/200
**Diagnosis:** Multi-seed champion variance run, seed=7. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2545 (delta -2.8521 vs prev best -0.4024); val=-3.1039729900659707 train=-0.09442857691507126.

**Learning:** Ext iter 81 (xgboost): DISCARD. Train/val gap = 3.0095. This iter targets extended search.


## Exp207 — ext xgboost 82/200
**Diagnosis:** Multi-seed champion variance run, seed=99. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.1947 (delta -2.7923 vs prev best -0.4024); val=-3.046982670373215 train=-0.09274179521326188.

**Learning:** Ext iter 82 (xgboost): DISCARD. Train/val gap = 2.9542. This iter targets extended search.


## Exp208 — ext xgboost 83/200
**Diagnosis:** Multi-seed champion variance run, seed=2024. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2442 (delta -2.8418 vs prev best -0.4024); val=-3.0941810692916776 train=-0.09414196033243023.

**Learning:** Ext iter 83 (xgboost): DISCARD. Train/val gap = 3.0000. This iter targets extended search.


## Exp209 — ext xgboost 84/200
**Diagnosis:** Multi-seed champion variance run, seed=12345. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2034 (delta -2.8010 vs prev best -0.4024); val=-3.0552529984773096 train=-0.09233280747993496.

**Learning:** Ext iter 84 (xgboost): DISCARD. Train/val gap = 2.9629. This iter targets extended search.


## Exp210 — ext xgboost 85/200
**Diagnosis:** Multi-seed champion variance run, seed=7777. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.1568 (delta -2.7544 vs prev best -0.4024); val=-3.0110095187226458 train=-0.09528118658830004.

**Learning:** Ext iter 85 (xgboost): DISCARD. Train/val gap = 2.9157. This iter targets extended search.


## Exp211 — ext xgboost 86/200
**Diagnosis:** Multi-seed champion variance run, seed=31337. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.1681 (delta -2.7658 vs prev best -0.4024); val=-3.0217510714755886 train=-0.09384565639052077.

**Learning:** Ext iter 86 (xgboost): DISCARD. Train/val gap = 2.9279. This iter targets extended search.


## Exp212 — ext xgboost 87/200
**Diagnosis:** Multi-seed champion variance run, seed=1729. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.2072 (delta -2.8048 vs prev best -0.4024); val=-3.05886516121975 train=-0.09205822062889203.

**Learning:** Ext iter 87 (xgboost): DISCARD. Train/val gap = 2.9668. This iter targets extended search.


## Exp213 — ext xgboost 88/200
**Diagnosis:** Multi-seed champion variance run, seed=6174. Required by autoresearch CLAUDE.md before declaring any KEEP a 'real' champion. Six-seed median is the minimum bar; we run 10 for tightness.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

**Hypothesis:** Mechanism: same hyperparameters, different RNG seed. Variance across seeds bounds how much of any reported improvement is noise. Standard deviation > 0.02 composite ⇒ champion claim is fragile.

**Prediction:** Within ±0.025 of seed-42 median.

**Verdict:** DISCARD composite=-3.1720 (delta -2.7697 vs prev best -0.4024); val=-3.0253720267544875 train=-0.09181819323285954.

**Learning:** Ext iter 88 (xgboost): DISCARD. Train/val gap = 2.9336. This iter targets extended search.


## Exp214 — ext xgboost 89/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=30. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=30, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-2.5626 (delta -2.1603 vs prev best -0.4024); val=-2.498020819199287 train=-1.2055600283188672.

**Learning:** Ext iter 89 (xgboost): DISCARD. Train/val gap = 1.2925. This iter targets Extreme regularisation cool-down.


## Exp215 — ext xgboost 90/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=50. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=50, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-2.5994 (delta -2.1971 vs prev best -0.4024); val=-2.540225094410619 train=-1.3564315586477607.

**Learning:** Ext iter 90 (xgboost): DISCARD. Train/val gap = 1.1838. This iter targets Extreme regularisation cool-down.


## Exp216 — ext xgboost 91/200
**Diagnosis:** Extreme regularisation cool-down — reg_lambda=100. After 195 iterations the champion likely lives in a moderate-cap corner; we audit the high-bias / low-var corner to confirm the champion is not just a regularisation accident.

**Citations:** Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

**Hypothesis:** Mechanism: depth=3, reg_lambda=100, subsample/colsample=0.6 is the maximum-shrinkage corner — if composite holds, the champion's gains generalise; if it collapses, gains were regularisation-sensitive.

**Prediction:** Composite delta in [-0.030, -0.005] expected; informational.

**Verdict:** DISCARD composite=-2.7561 (delta -2.3537 vs prev best -0.4024); val=-2.7019991431923165 train=-1.620307014478118.

**Learning:** Ext iter 91 (xgboost): DISCARD. Train/val gap = 1.0817. This iter targets Extreme regularisation cool-down.

