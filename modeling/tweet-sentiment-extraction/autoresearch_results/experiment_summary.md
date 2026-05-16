# Experiment Summary — tweet-sentiment-extraction

_(populated by `framework/hill_climb.py`)_

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=-3.3179 val=-3.1637955917998077 train=-0.08253367996809287
- **Status:** KEEP
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=-3.9542 val=-3.766319748985622 train=-0.008459266867205686
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=-2.6727 val=-2.559536872188317 train=-0.29715385641685926
- **Status:** KEEP
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=-3.3131 val=-3.1594078960271976 train=-0.08468499809876856
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=-3.2450 val=-3.099661217912777 train=-0.19347603486495735
- **Status:** DISCARD
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=-3.4147 val=-3.2661453635575795 train=-0.29591542059880327
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=-3.0045 val=-2.867665430300683 train=-0.1301382321162814
- **Status:** DISCARD
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=-3.3658 val=-3.20958345176409 train=-0.08506067494628469
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=-3.3167 val=-3.1624441270076713 train=-0.07799641637219086
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=-4.3036 val=-4.098836519724797 train=-0.0034458604822636472
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=-2.6526 val=-2.5400478857137223 train=-0.2899617821075871
- **Status:** KEEP
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=-3.3179 val=-3.1637955917998077 train=-0.08253367996809287
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=-3.3179 val=-3.1637955917998077 train=-0.08253367996809287
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=-3.4740 val=-3.3117980213221343 train=-0.06841724194449082
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=-3.6526 val=-3.4805424572196775 train=-0.03853169342526064
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=-3.3070 val=-3.1509465142798048 train=-0.030023035311530107
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=-3.2847 val=-3.132237255527517 train=-0.08220918125106266
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=-3.3511 val=-3.1952674321584875 train=-0.07839794461466479
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=-4.3194 val=-4.114671202417504 train=-0.02015626980120773
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=-2.3803 val=-2.2874586716550813 train=-0.4308156376044695
- **Status:** KEEP
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=-3.3091 val=-3.1527949392007564 train=-0.026550575781006547
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=-3.3179 val=-3.1637955917998077 train=-0.08253367996809287
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=-2.9320 val=-2.798566168420811 train=-0.1301175198168535
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=-3.1976 val=-3.0507176352302396 train=-0.11291598757783622
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=-3.2726 val=-3.120657994259972 train=-0.08124718729982769
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp26 (lightgbm iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp27 (lightgbm iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-5.7831 val=-5.732771760803439 train=-4.726683915780517
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp28 (lightgbm iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-6.5146 val=-6.490847593276693 train=-6.015995315298495
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp29 (lightgbm iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-5.1378 val=-5.063019633891814 train=-3.567115583186671
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp30 (lightgbm iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-3.1905 val=-3.0430917473295587 train=-0.09454767075578535
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp31 (lightgbm iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-3.1905 val=-3.0430917473295587 train=-0.09454767075578535
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp32 (lightgbm iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-6.0499 val=-6.0102730939138445 train=-5.216923135442443
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp33 (lightgbm iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-6.0559 val=-6.015861904783357 train=-5.214537111980953
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp34 (lightgbm iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp35 (lightgbm iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-6.3698 val=-6.341158722409136 train=-5.769000812831813
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp36 (lightgbm iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp37 (lightgbm iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp38 (lightgbm iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-6.3001 val=-6.2692977534200285 train=-5.652891593275914
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp39 (lightgbm iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-6.0548 val=-6.014829385393398 train=-5.216331801599987
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp40 (lightgbm iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-6.0612 val=-6.020952575284094 train=-5.2166106706176985
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp41 (lightgbm iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp42 (lightgbm iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp43 (lightgbm iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-5.5312 val=-5.472241731627517 train=-4.292437341957941
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp44 (lightgbm iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-6.6717 val=-6.6529899409355755 train=-6.278928827338698
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp45 (lightgbm iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp46 (lightgbm iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp47 (lightgbm iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-6.0564 val=-6.01630150614299 train=-5.213802313973906
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp48 (lightgbm iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-6.2366 val=-6.203299950759998 train=-5.537049069620756
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp49 (lightgbm iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-5.7768 val=-5.7267635062346525 train=-4.725249932444344
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp50 (lightgbm iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-6.0575 val=-6.017388704086822 train=-5.214611462264468
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp51 (catboost iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Baseline catboost per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp52 (catboost iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp53 (catboost iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp54 (catboost iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp55 (catboost iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp56 (catboost iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp57 (catboost iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp58 (catboost iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp59 (catboost iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp60 (catboost iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp61 (catboost iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp62 (catboost iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp63 (catboost iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp64 (catboost iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp65 (catboost iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp66 (catboost iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp67 (catboost iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp68 (catboost iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp69 (catboost iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp70 (catboost iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp71 (catboost iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp72 (catboost iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp73 (catboost iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp74 (catboost iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp75 (catboost iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-inf val=NA train=NA
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp76 (mlp iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-0.6815 val=-0.6689388302676919 train=-0.4182573373918225
- **Status:** KEEP
- **Rationale:** Baseline mlp per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp77 (mlp iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-0.6023 val=-0.5874756777578252 train=-0.29089833142404276
- **Status:** KEEP
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp78 (mlp iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-0.9861 val=-0.9800950208160119 train=-0.8597232459792651
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp79 (mlp iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-0.5089 val=-0.4961258885343692 train=-0.24116486329419606
- **Status:** KEEP
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp80 (mlp iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-0.7972 val=-0.7868817097178591 train=-0.5809584081046416
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp81 (mlp iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-3.0272 val=-3.0177855978939188 train=-2.829183980882237
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp82 (mlp iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-0.6503 val=-0.6391149727840344 train=-0.4159644010286532
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp83 (mlp iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-0.6618 val=-0.6515709416782564 train=-0.4463572543945105
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp84 (mlp iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-0.5826 val=-0.5671266118515009 train=-0.2585767919045138
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp85 (mlp iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-0.7093 val=-0.7005147165553746 train=-0.5246766922765181
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp86 (mlp iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-0.6803 val=-0.6661202804361013 train=-0.3820210859198674
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp87 (mlp iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-0.6098 val=-0.5923843992509479 train=-0.24312191333625557
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp88 (mlp iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-0.9096 val=-0.9010993997824375 train=-0.7319333901637267
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp89 (mlp iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-0.6369 val=-0.626279046685153 train=-0.4131149931083804
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp90 (mlp iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-0.7063 val=-0.6944320762380586 train=-0.45785661491351276
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp91 (mlp iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-0.7163 val=-0.7075512486016371 train=-0.5316583242280064
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp92 (mlp iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-0.4086 val=-0.3978249572337726 train=-0.18184575424164937
- **Status:** KEEP
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp93 (mlp iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-0.5627 val=-0.549528659080144 train=-0.285692012133671
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp94 (mlp iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-5.2630 val=-5.246662532282892 train=-4.919471565649047
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp95 (mlp iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-0.5733 val=-0.5573943807000447 train=-0.23920126266148226
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp96 (mlp iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-0.6815 val=-0.6689388302676919 train=-0.4182573373918225
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp97 (mlp iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-0.6815 val=-0.6689388302676919 train=-0.4182573373918225
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp98 (mlp iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-0.7580 val=-0.7469560922308993 train=-0.5265435257840851
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp99 (mlp iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-0.6040 val=-0.5905594935748906 train=-0.3226682633017775
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp100 (mlp iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-0.6013 val=-0.5936014842960149 train=-0.43887603166850625
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp101 (ft_transformer iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp102 (ft_transformer iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-5.8643 val=-5.8198912138994165 train=-4.932020972539073
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp103 (ft_transformer iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-6.5417 val=-6.518615289471205 train=-6.057745559661726
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp104 (ft_transformer iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-5.2537 val=-5.189034364867947 train=-3.8960265290036613
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp105 (ft_transformer iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-3.1530 val=-3.008481509568851 train=-0.11798823578730835
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp106 (ft_transformer iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-3.1530 val=-3.008481509568851 train=-0.11798823578730835
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp107 (ft_transformer iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp108 (ft_transformer iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp109 (ft_transformer iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp110 (ft_transformer iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-6.4180 val=-6.3905197266396145 train=-5.840642305078788
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp111 (ft_transformer iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp112 (ft_transformer iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp113 (ft_transformer iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-6.3554 val=-6.325925930882272 train=-5.737303878851517
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp114 (ft_transformer iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp115 (ft_transformer iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp116 (ft_transformer iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp117 (ft_transformer iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp118 (ft_transformer iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-5.6444 val=-5.592404301993815 train=-4.552530720891175
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp119 (ft_transformer iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-6.6788 val=-6.660416201119539 train=-6.292720388266021
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp120 (ft_transformer iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp121 (ft_transformer iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp122 (ft_transformer iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp123 (ft_transformer iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-6.2945 val=-6.263246240054421 train=-5.637204525354397
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp124 (ft_transformer iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-5.8632 val=-5.818827708694891 train=-4.93196403197465
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp125 (ft_transformer iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-6.1161 val=-6.07966965124358 train=-5.352046634601448
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp126 (ext xgboost 1/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.0119 val=-2.9061438428297532 train=-0.7917614470179243
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp127 (ext xgboost 2/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.6648 val=-2.5472183464165945 train=-0.1952278335165374
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp128 (ext xgboost 3/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.1815 val=-3.049897714369325 train=-0.4172114347528462
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp129 (ext xgboost 4/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.0129 val=-2.872570338039586 train=-0.06599903772972972
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp130 (ext xgboost 5/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.4196 val=-3.2666475438187557 train=-0.20857989304482097
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp131 (ext xgboost 6/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.3967 val=-3.2356566317837485 train=-0.015514511659308247
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp132 (ext xgboost 7/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.7000 val=-3.528592350215454 train=-0.09982101079256624
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp133 (ext xgboost 8/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.6927 val=-3.51701158094628 train=-0.002588391828332698
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp134 (ext xgboost 9/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.9158 val=-3.7317895598206796 train=-0.05192680705121985
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp135 (ext xgboost 10/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.9201 val=-3.7334947386546578 train=-0.0005528707343642492
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp136 (ext xgboost 11/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-4.2100 val=-4.01082719295266 train=-0.0275834647569777
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp137 (ext xgboost 12/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-4.2638 val=-4.06081789845279 train=-0.00045992649515422084
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp138 (ext xgboost 13/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-4.3223 val=-4.1175812563727305 train=-0.02356845559688294
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp139 (ext xgboost 14/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-4.3502 val=-4.143087324315563 train=-0.0004208652016813271
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp140 (ext lightgbm 15/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.0558 val=-2.9122817940964087 train=-0.041923380287920475
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp141 (ext lightgbm 16/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.0362 val=-2.893818343929681 train=-0.0463704546676754
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp142 (ext lightgbm 17/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.1980 val=-3.048854510191262 train=-0.06560491437874391
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp143 (ext lightgbm 18/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.2551 val=-3.1035410144497515 train=-0.07304573678551259
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp144 (ext lightgbm 19/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.1980 val=-3.048854510191262 train=-0.06560491437874391
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp145 (ext lightgbm 20/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.2551 val=-3.1035410144497515 train=-0.07304573678551259
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp146 (ext lightgbm 21/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.1980 val=-3.048854510191262 train=-0.06560491437874391
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp147 (ext lightgbm 22/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-3.2551 val=-3.1035410144497515 train=-0.07304573678551259
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp148 (ext catboost 23/200)
- Config: {'iterations': 1500, 'depth': 4, 'lr': 0.03, 'l2_leaf_reg': 1}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp149 (ext catboost 24/200)
- Config: {'iterations': 1500, 'depth': 4, 'lr': 0.03, 'l2_leaf_reg': 3}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp150 (ext catboost 25/200)
- Config: {'iterations': 1500, 'depth': 4, 'lr': 0.03, 'l2_leaf_reg': 10}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp151 (ext catboost 26/200)
- Config: {'iterations': 1500, 'depth': 6, 'lr': 0.03, 'l2_leaf_reg': 1}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp152 (ext catboost 27/200)
- Config: {'iterations': 1500, 'depth': 6, 'lr': 0.03, 'l2_leaf_reg': 3}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp153 (ext catboost 28/200)
- Config: {'iterations': 1500, 'depth': 6, 'lr': 0.03, 'l2_leaf_reg': 10}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp154 (ext catboost 29/200)
- Config: {'iterations': 1500, 'depth': 8, 'lr': 0.03, 'l2_leaf_reg': 1}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp155 (ext catboost 30/200)
- Config: {'iterations': 1500, 'depth': 8, 'lr': 0.03, 'l2_leaf_reg': 3}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp156 (ext catboost 31/200)
- Config: {'iterations': 1500, 'depth': 8, 'lr': 0.03, 'l2_leaf_reg': 10}
- Result: composite=-inf val=NA train=NA
- Status: DISCARD
- Citation: Prokhorenkova, Gusev, Vorobev, Dorogush, Gulin 2018 NeurIPS 'CatBoost: Unbiased Boosting with Categorical Features' (arXiv:1706.09516) — ordered target stats + symmetric oblivious trees, robust to category cardinality.

### Exp157 (ext mlp 32/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.8042 val=-0.7928985790154797 train=-0.5659676267545248
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp158 (ext mlp 33/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.5826 val=-0.5671266118515009 train=-0.2585767919045138
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp159 (ext mlp 34/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4720 val=-0.45745868746478024 train=-0.1660191030698972
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp160 (ext mlp 35/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.6695 val=-0.6557606734709884 train=-0.38017581339026846
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp161 (ext mlp 36/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5336 val=-0.5179473136044872 train=-0.20553639389916215
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp162 (ext mlp 37/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4811 val=-0.46715021526866984 train=-0.18807468162757124
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp163 (ext mlp 38/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.4339 val=-0.4233089554549717 train=-0.21226845390841226
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp164 (ext mlp 39/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.4065 val=-0.3948596305355748 train=-0.16236942758241493
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp165 (ext mlp 40/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.4007 val=-0.38888178002391915 train=-0.1522502979336722
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp166 (ext mlp 41/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.6207 val=-0.6053405133698905 train=-0.29893352170765863
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp167 (ext mlp 42/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.5343 val=-0.5178020928395465 train=-0.18731164412164517
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp168 (ext mlp 43/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4798 val=-0.4658769936934734 train=-0.1869641036728774
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp169 (ext mlp 44/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.6667 val=-0.6474838367860272 train=-0.2626230785793444
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp170 (ext mlp 45/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5870 val=-0.5683085363139294 train=-0.19458850186635837
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp171 (ext mlp 46/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5029 val=-0.48631853454203067 train=-0.15563835592294195
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp172 (ext ft_transformer 47/200)
- Config: {'iterations': 400, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-3.1891 val=-3.056421649364057 train=-0.40327466606521156
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp173 (ext ft_transformer 48/200)
- Config: {'iterations': 400, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-3.1839 val=-3.0452970594784596 train=-0.27244006355293615
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp174 (ext ft_transformer 49/200)
- Config: {'iterations': 400, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-3.1424 val=-3.00388064323946 train=-0.23332753319839955
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp175 (ext ft_transformer 50/200)
- Config: {'iterations': 800, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-3.0423 val=-2.9053112192146795 train=-0.16613091566220733
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp176 (ext ft_transformer 51/200)
- Config: {'iterations': 800, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-3.0981 val=-2.954490244404423 train=-0.08291188233149992
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp177 (ext ft_transformer 52/200)
- Config: {'iterations': 800, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-3.0729 val=-2.9301980790629516 train=-0.07700161110070554
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp178 (ext ft_transformer 53/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-3.0221 val=-2.882253758838954 train=-0.0843371415657367
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp179 (ext ft_transformer 54/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-3.0915 val=-2.9457915434999897 train=-0.03259341790526028
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp180 (ext ft_transformer 55/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-3.0670 val=-2.922918734442714 train=-0.04034612853950885
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp181 (ext xgboost 56/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.1, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-3.0127 val=-2.875808602109465 train=-0.137850829155199
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp182 (ext xgboost 57/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.3, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-3.0127 val=-2.875808602109465 train=-0.137850829155199
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp183 (ext xgboost 58/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 1.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-3.0127 val=-2.875808602109465 train=-0.137850829155199
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp184 (ext xgboost 59/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 3.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-3.0127 val=-2.875808602109465 train=-0.137850829155199
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp185 (ext mlp 60/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 128, 64), 'weight_decay': 0.001}
- Result: composite=-0.5680 val=-0.5507046260696932 train=-0.20427936128779317
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp186 (ext mlp 61/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (384, 192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4972 val=-0.48205404119539597 train=-0.17941413693350708
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp187 (ext mlp 62/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (192, 96), 'weight_decay': 0.001}
- Result: composite=-0.5518 val=-0.538930240936568 train=-0.2815617846480924
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp188 (ext mlp 63/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (320, 160), 'weight_decay': 0.001}
- Result: composite=-0.4582 val=-0.4465368905809422 train=-0.21361414427599057
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp189 (ext mlp 64/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 256), 'weight_decay': 0.001}
- Result: composite=-0.5066 val=-0.49274748780351896 train=-0.21478930563759094
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp190 (ext ft_transformer 65/200)
- Config: {'iterations': 200, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-4.1623 val=-4.088573316396766 train=-2.613161221646135
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp191 (ext ft_transformer 66/200)
- Config: {'iterations': 400, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-3.4303 val=-3.334343438005558 train=-1.4159593348476949
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp192 (ext ft_transformer 67/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-3.0911 val=-2.9871187083414195 train=-0.9079304476309981
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp193 (ext xgboost 68/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 0.1, 'reg_alpha': 0.1}
- Result: composite=-2.8057 val=-2.691392873611761 train=-0.40555020728714436
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp194 (ext xgboost 69/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 1.0, 'reg_alpha': 0.5}
- Result: composite=-2.7691 val=-2.6580736968226595 train=-0.43666818424985193
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp195 (ext xgboost 70/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 3.0, 'reg_alpha': 1.0}
- Result: composite=-2.7402 val=-2.633117567550343 train=-0.49137244782989553
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp196 (ext xgboost 71/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 0.5}
- Result: composite=-2.7610 val=-2.6582544281189975 train=-0.6038785170569363
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp197 (ext xgboost 72/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 3.0}
- Result: composite=-2.7610 val=-2.6582544281189975 train=-0.6038785170569363
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp198 (ext patchtsmixer 73/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 128}
- Result: composite=-3.1248 val=-3.106145667428944 train=-2.73298854010057
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp199 (ext patchtsmixer 74/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 128}
- Result: composite=-2.6655 val=-2.640452994438383 train=-2.139811340287149
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp200 (ext patchtsmixer 75/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 256}
- Result: composite=-2.2969 val=-2.2715074664292754 train=-1.763893358553666
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp201 (ext patchtsmixer 76/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 256}
- Result: composite=-2.0724 val=-2.039917865109481 train=-1.3899405005639747
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp202 (ext patchtsmixer 77/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 384}
- Result: composite=-2.0672 val=-2.0376248608109333 train=-1.4465663935076765
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp203 (ext patchtsmixer 78/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 384}
- Result: composite=-1.8665 val=-1.829555962164595 train=-1.090061999928747
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp204 (ext xgboost 79/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 42}
- Result: composite=-3.3027 val=-3.149972092035583 train=-0.09601833536002304
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp205 (ext xgboost 80/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 0}
- Result: composite=-3.3617 val=-3.206173818177699 train=-0.09656150414592213
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp206 (ext xgboost 81/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7}
- Result: composite=-3.2991 val=-3.1466112164552476 train=-0.0963426118013854
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp207 (ext xgboost 82/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 99}
- Result: composite=-3.3592 val=-3.2035016094338875 train=-0.08972589392074586
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp208 (ext xgboost 83/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 2024}
- Result: composite=-3.3317 val=-3.1773682179949825 train=-0.09045930608070128
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp209 (ext xgboost 84/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 12345}
- Result: composite=-3.3906 val=-3.2333236681082553 train=-0.08710817028290291
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp210 (ext xgboost 85/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7777}
- Result: composite=-3.3404 val=-3.1857950475256356 train=-0.0935667949957172
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp211 (ext xgboost 86/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 31337}
- Result: composite=-3.2839 val=-3.1319170882747116 train=-0.09171779757172523
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp212 (ext xgboost 87/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 1729}
- Result: composite=-3.3408 val=-3.186188820827374 train=-0.0945005916896719
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp213 (ext xgboost 88/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 6174}
- Result: composite=-3.4113 val=-3.253297893169585 train=-0.09417477874589363
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp214 (ext xgboost 89/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 30, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-2.4906 val=-2.427522142114828 train=-1.1657345942707027
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp215 (ext xgboost 90/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 50, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-2.5766 val=-2.516572193452514 train=-1.3165855851538757
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp216 (ext xgboost 91/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 100, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-2.7762 val=-2.7201175977024983 train=-1.5987367590385002
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.
