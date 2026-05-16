# Experiment Summary — covid19-global-forecasting-week-3

_(populated by `framework/hill_climb.py`)_

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=-2.7198 val=-2.5934554702645496 train=-0.06646864077864417
- **Status:** KEEP
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=-3.0764 val=-2.9302624761301015 train=-0.0072900539021650765
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=-2.1364 val=-2.046410777324426 train=-0.2458360094326182
- **Status:** KEEP
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=-2.6552 val=-2.5323011311571664 train=-0.07519985470119697
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=-2.6148 val=-2.4980513607697703 train=-0.16406997595511355
- **Status:** DISCARD
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=-2.8097 val=-2.687898739354986 train=-0.2510583202620954
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=-2.3207 val=-2.2155719616222047 train=-0.11263427056353573
- **Status:** DISCARD
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=-2.6505 val=-2.527443460799921 train=-0.06686235614708719
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=-2.6690 val=-2.5450881587499725 train=-0.06741774731484804
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=-3.3247 val=-3.1665065791840106 train=-0.0031225071007842577
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=-2.1263 val=-2.036406325304634 train=-0.2389514830501764
- **Status:** KEEP
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=-2.7198 val=-2.5934554702645496 train=-0.06646864077864417
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=-2.7198 val=-2.5934554702645496 train=-0.06646864077864417
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=-2.8016 val=-2.671282786273884 train=-0.06469185644605496
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=-2.9145 val=-2.7771836461357777 train=-0.030839591573381175
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=-2.7278 val=-2.599033719016167 train=-0.024474693352078258
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=-2.6156 val=-2.4942616408704352 train=-0.06738116428183852
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=-2.6771 val=-2.5526890768922312 train=-0.0637903819090795
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=-3.3462 val=-3.1876098015516647 train=-0.015738774302609136
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=-1.8277 val=-1.7569271994822084 train=-0.34224116196377397
- **Status:** KEEP
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=-2.7128 val=-2.584651754153078 train=-0.021888744211975137
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=-2.7198 val=-2.5934554702645496 train=-0.06646864077864417
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=-2.2945 val=-2.190385604598486 train=-0.10857383610616288
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=-2.5360 val=-2.4193814145956343 train=-0.08793652713362203
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=-2.6647 val=-2.541062538599403 train=-0.06926758513268404
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp26 (lightgbm iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp27 (lightgbm iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-4.7799 val=-4.739812215030453 train=-3.938002902910664
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp28 (lightgbm iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-5.5626 val=-5.539037756445358 train=-5.068346287397298
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp29 (lightgbm iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-4.1655 val=-4.107458881786641 train=-2.9459131890810966
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp30 (lightgbm iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-2.5765 val=-2.4579315445155108 train=-0.08625539548067859
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp31 (lightgbm iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.5765 val=-2.4579315445155108 train=-0.08625539548067859
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp32 (lightgbm iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-5.0618 val=-5.02851441690181 train=-4.362719407422213
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp33 (lightgbm iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-5.0621 val=-5.028879189077089 train=-4.364282831308425
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp34 (lightgbm iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp35 (lightgbm iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-5.4044 val=-5.378019853416923 train=-4.850655344400744
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp36 (lightgbm iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp37 (lightgbm iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp38 (lightgbm iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-5.3294 val=-5.301728889066858 train=-4.747351286283635
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp39 (lightgbm iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-5.0600 val=-5.026762425987201 train=-4.362225568246185
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp40 (lightgbm iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-5.0551 val=-5.022092458926782 train=-4.3627310733779865
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp41 (lightgbm iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp42 (lightgbm iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp43 (lightgbm iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-4.5441 val=-4.497358640120741 train=-3.56204727579879
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp44 (lightgbm iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-5.7354 val=-5.714636187367149 train=-5.299761743498172
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp45 (lightgbm iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp46 (lightgbm iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp47 (lightgbm iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-5.0644 val=-5.031076838642848 train=-4.36376863542587
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp48 (lightgbm iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-5.2588 val=-5.229646915474447 train=-4.647164124470526
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp49 (lightgbm iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-4.7879 val=-4.7474224471882485 train=-3.9374718555703043
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp50 (lightgbm iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-5.0617 val=-5.028491452688146 train=-4.363725818254666
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
- **Result:** composite=-0.6380 val=-0.6269031397778163 train=-0.4054743624906975
- **Status:** KEEP
- **Rationale:** Baseline mlp per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp77 (mlp iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-0.5449 val=-0.532494377858745 train=-0.28499947771643586
- **Status:** KEEP
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp78 (mlp iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-0.9596 val=-0.9525733351823636 train=-0.8130188165835567
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp79 (mlp iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-0.4806 val=-0.46864587898986193 train=-0.22903013587510995
- **Status:** KEEP
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp80 (mlp iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-0.6302 val=-0.6248352548909379 train=-0.5179100843437355
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp81 (mlp iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.7398 val=-2.7227101040170174 train=-2.380846957642967
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp82 (mlp iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-0.6534 val=-0.6405758024723929 train=-0.3836614187808575
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp83 (mlp iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-0.5898 val=-0.5805478233398446 train=-0.39578920879712576
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp84 (mlp iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-0.5278 val=-0.5152946916953426 train=-0.2643269912831613
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp85 (mlp iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-0.6249 val=-0.6166350149288282 train=-0.4503913833069187
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp86 (mlp iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-0.6521 val=-0.6378317857786167 train=-0.35205913010008183
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp87 (mlp iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-0.5349 val=-0.5196908691260338 train=-0.21565435251225656
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp88 (mlp iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-0.8565 val=-0.8489802695094613 train=-0.6995441808947539
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp89 (mlp iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-0.5732 val=-0.5637864131967001 train=-0.37605162032348527
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp90 (mlp iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-0.5781 val=-0.5693108895028084 train=-0.3940786466081184
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp91 (mlp iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-0.7102 val=-0.699439988751654 train=-0.48466293944178857
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp92 (mlp iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-0.3927 val=-0.3821111794387993 train=-0.17052441676721966
- **Status:** KEEP
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp93 (mlp iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-0.5236 val=-0.5115647120535719 train=-0.27094853989175516
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp94 (mlp iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-4.4608 val=-4.438457761751986 train=-3.9924866924410467
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp95 (mlp iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-0.4999 val=-0.48643834040996947 train=-0.21692600356829678
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp96 (mlp iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-0.6380 val=-0.6269031397778163 train=-0.4054743624906975
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp97 (mlp iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-0.6380 val=-0.6269031397778163 train=-0.4054743624906975
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp98 (mlp iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-0.7214 val=-0.7113305985786378 train=-0.5097183556399943
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp99 (mlp iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-0.5625 val=-0.550705410761425 train=-0.31552249027487544
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp100 (mlp iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-0.5826 val=-0.5730147422305447 train=-0.38042771746756665
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp101 (ft_transformer iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp102 (ft_transformer iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-4.8667 val=-4.830109094642149 train=-4.097366861369269
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp103 (ft_transformer iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-5.5664 val=-5.544127953139907 train=-5.098652267181552
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp104 (ft_transformer iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-4.2673 val=-4.21683861527742 train=-3.2073343693817784
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp105 (ft_transformer iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-2.4731 val=-2.3602546016133363 train=-0.10325677041403583
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp106 (ft_transformer iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.4731 val=-2.3602546016133363 train=-0.10325677041403583
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp107 (ft_transformer iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp108 (ft_transformer iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp109 (ft_transformer iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp110 (ft_transformer iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-5.4208 val=-5.396317577286011 train=-4.906097788658472
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp111 (ft_transformer iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp112 (ft_transformer iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp113 (ft_transformer iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-5.3537 val=-5.328084869504514 train=-4.815580912848739
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp114 (ft_transformer iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp115 (ft_transformer iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp116 (ft_transformer iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp117 (ft_transformer iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp118 (ft_transformer iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-4.6404 val=-4.598765672440939 train=-3.7669753732011686
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp119 (ft_transformer iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-5.7322 val=-5.711994351933193 train=-5.30854823454381
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp120 (ft_transformer iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp121 (ft_transformer iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp122 (ft_transformer iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp123 (ft_transformer iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-5.2879 val=-5.261093813592681 train=-4.725904932950001
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp124 (ft_transformer iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-4.8672 val=-4.830516258618095 train=-4.096874124771858
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp125 (ft_transformer iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-5.1086 val=-5.078293673979548 train=-4.472830398110283
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp126 (ext xgboost 1/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.4330 val=-2.347779332646023 train=-0.6435871029274635
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp127 (ext xgboost 2/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.1024 val=-2.009569282690899 train=-0.15306582256175183
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp128 (ext xgboost 3/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5015 val=-2.398499130799162 train=-0.33854661228773447
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp129 (ext xgboost 4/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.3804 val=-2.269782730325372 train=-0.05749248490513876
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp130 (ext xgboost 5/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.7482 val=-2.6254470081288397 train=-0.17073475219553633
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp131 (ext xgboost 6/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.6632 val=-2.537011171808782 train=-0.013731403268155987
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp132 (ext xgboost 7/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.9737 val=-2.836167843714424 train=-0.08482639852327827
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp133 (ext xgboost 8/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.9325 val=-2.7929592745960337 train=-0.002158407386486192
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp134 (ext xgboost 9/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.1367 val=-2.9894560854388845 train=-0.044243255550305505
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp135 (ext xgboost 10/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.0611 val=-2.9153519710093607 train=-0.0005264441493810927
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp136 (ext xgboost 11/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.3455 val=-3.187179549321666 train=-0.020704837916022296
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp137 (ext xgboost 12/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.3540 val=-3.194346237515876 train=-0.0004632331263857214
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp138 (ext xgboost 13/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.4266 val=-3.2641962019443005 train=-0.017057615784697274
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp139 (ext xgboost 14/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.4285 val=-3.265249422369324 train=-0.00041963249753884435
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp140 (ext lightgbm 15/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.4151 val=-2.3013686309156234 train=-0.027162915606944067
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp141 (ext lightgbm 16/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.4447 val=-2.3295560839356426 train=-0.026965161742983572
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp142 (ext lightgbm 17/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.5568 val=-2.4376491171877492 train=-0.05462689777175568
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp143 (ext lightgbm 18/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.5281 val=-2.410623607932089 train=-0.06143531089885831
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp144 (ext lightgbm 19/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.5568 val=-2.4376491171877492 train=-0.05462689777175568
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp145 (ext lightgbm 20/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.5281 val=-2.410623607932089 train=-0.06143531089885831
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp146 (ext lightgbm 21/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.5568 val=-2.4376491171877492 train=-0.05462689777175568
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp147 (ext lightgbm 22/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.5281 val=-2.410623607932089 train=-0.06143531089885831
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
- Result: composite=-0.7502 val=-0.7406439541350992 train=-0.5503708142085235
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp158 (ext mlp 33/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.5278 val=-0.5152946916953426 train=-0.2643269912831613
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp159 (ext mlp 34/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4645 val=-0.4512769898667288 train=-0.1866168242744159
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp160 (ext mlp 35/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5029 val=-0.49446078999280535 train=-0.3261088464566421
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp161 (ext mlp 36/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4165 val=-0.4049399785023217 train=-0.17359653325600802
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp162 (ext mlp 37/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4070 val=-0.39569735282762514 train=-0.169266571700418
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp163 (ext mlp 38/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.4087 val=-0.3982569715628428 train=-0.18934078425206308
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp164 (ext mlp 39/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3873 val=-0.37576753825274384 train=-0.1461181449412092
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp165 (ext mlp 40/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3642 val=-0.3528784705757225 train=-0.12740058537471122
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp166 (ext mlp 41/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.5633 val=-0.5495324553432267 train=-0.27318497304853867
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp167 (ext mlp 42/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4904 val=-0.47655913867703065 train=-0.20011474104515284
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp168 (ext mlp 43/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4543 val=-0.44020057690646314 train=-0.15820115877036356
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp169 (ext mlp 44/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5931 val=-0.5765791407305584 train=-0.24657221859584724
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp170 (ext mlp 45/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5350 val=-0.5177265458258313 train=-0.17253016640872687
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp171 (ext mlp 46/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4634 val=-0.4481772082733329 train=-0.14382743227127237
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp172 (ext ft_transformer 47/200)
- Config: {'iterations': 400, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.5278 val=-2.4221699539237265 train=-0.31006885301907255
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp173 (ext ft_transformer 48/200)
- Config: {'iterations': 400, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.5142 val=-2.404467787216974 train=-0.21044578311245307
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp174 (ext ft_transformer 49/200)
- Config: {'iterations': 400, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.5173 val=-2.4063849629998484 train=-0.18816052843374415
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp175 (ext ft_transformer 50/200)
- Config: {'iterations': 800, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.4070 val=-2.298123222298418 train=-0.12050173974884885
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp176 (ext ft_transformer 51/200)
- Config: {'iterations': 800, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.4513 val=-2.337510982146876 train=-0.061143432861559995
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp177 (ext ft_transformer 52/200)
- Config: {'iterations': 800, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.4698 val=-2.3548266304168095 train=-0.055536300324498515
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp178 (ext ft_transformer 53/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.3916 val=-2.2803785805036507 train=-0.05572598046133157
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp179 (ext ft_transformer 54/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.4466 val=-2.33109246601529 train=-0.021856826374517503
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp180 (ext ft_transformer 55/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.4685 val=-2.3523621628404108 train=-0.02966352499048963
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp181 (ext xgboost 56/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.1, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.4264 val=-2.3161451118547607 train=-0.111711294418929
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp182 (ext xgboost 57/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.3, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.4264 val=-2.3161451118547607 train=-0.111711294418929
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp183 (ext xgboost 58/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 1.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.4264 val=-2.3161451118547607 train=-0.111711294418929
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp184 (ext xgboost 59/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 3.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.4264 val=-2.3161451118547607 train=-0.111711294418929
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp185 (ext mlp 60/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 128, 64), 'weight_decay': 0.001}
- Result: composite=-0.5277 val=-0.5123450254265632 train=-0.2051817314378185
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp186 (ext mlp 61/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (384, 192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4670 val=-0.45412126723985874 train=-0.1955850035331038
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp187 (ext mlp 62/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4828 val=-0.47050609659568515 train=-0.22528762414195755
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp188 (ext mlp 63/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (320, 160), 'weight_decay': 0.001}
- Result: composite=-0.4540 val=-0.4419816579335697 train=-0.20129562016351912
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp189 (ext mlp 64/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 256), 'weight_decay': 0.001}
- Result: composite=-0.5039 val=-0.4914159328070747 train=-0.24150727482169052
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp190 (ext ft_transformer 65/200)
- Config: {'iterations': 200, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-3.3419 val=-3.283935517489578 train=-2.124964950404296
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp191 (ext ft_transformer 66/200)
- Config: {'iterations': 400, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.7402 val=-2.663924270626485 train=-1.1382301285807583
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp192 (ext ft_transformer 67/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.4726 val=-2.3888233458180608 train=-0.7129501854305597
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp193 (ext xgboost 68/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 0.1, 'reg_alpha': 0.1}
- Result: composite=-2.2041 val=-2.1148088331831376 train=-0.3287256850653312
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp194 (ext xgboost 69/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 1.0, 'reg_alpha': 0.5}
- Result: composite=-2.2180 val=-2.129551892850527 train=-0.36102554436441786
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp195 (ext xgboost 70/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 3.0, 'reg_alpha': 1.0}
- Result: composite=-2.2040 val=-2.1182766185804693 train=-0.4041837635389613
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp196 (ext xgboost 71/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 0.5}
- Result: composite=-2.1755 val=-2.096004922970239 train=-0.505162676160618
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp197 (ext xgboost 72/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 3.0}
- Result: composite=-2.1755 val=-2.096004922970239 train=-0.505162676160618
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp198 (ext patchtsmixer 73/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 128}
- Result: composite=-2.2494 val=-2.2369953076480087 train=-1.989286517093924
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp199 (ext patchtsmixer 74/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 128}
- Result: composite=-2.0373 val=-2.021954084733445 train=-1.7145778997373022
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp200 (ext patchtsmixer 75/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 256}
- Result: composite=-1.7480 val=-1.7327028066108128 train=-1.4260333112755654
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp201 (ext patchtsmixer 76/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 256}
- Result: composite=-1.4681 val=-1.450669952708501 train=-1.1030112405102201
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp202 (ext patchtsmixer 77/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 384}
- Result: composite=-1.4598 val=-1.4422825576352782 train=-1.0926477600317686
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp203 (ext patchtsmixer 78/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 384}
- Result: composite=-1.3362 val=-1.314572786549832 train=-0.8828018322865563
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp204 (ext xgboost 79/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 42}
- Result: composite=-2.6774 val=-2.5537035619217106 train=-0.0796909012489367
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp205 (ext xgboost 80/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 0}
- Result: composite=-2.6716 val=-2.5477687461087752 train=-0.07133119788032172
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp206 (ext xgboost 81/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7}
- Result: composite=-2.6628 val=-2.539611099838247 train=-0.0754517017531639
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp207 (ext xgboost 82/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 99}
- Result: composite=-2.7068 val=-2.5814536136742805 train=-0.07411131486479143
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp208 (ext xgboost 83/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 2024}
- Result: composite=-2.6637 val=-2.540480091800027 train=-0.07632258373633201
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp209 (ext xgboost 84/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 12345}
- Result: composite=-2.6261 val=-2.5046770215782064 train=-0.07555380120821102
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp210 (ext xgboost 85/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7777}
- Result: composite=-2.6503 val=-2.5277916159152065 train=-0.07819439369090238
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp211 (ext xgboost 86/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 31337}
- Result: composite=-2.6382 val=-2.516006440807886 train=-0.07256789718992043
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp212 (ext xgboost 87/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 1729}
- Result: composite=-2.6669 val=-2.543598149896469 train=-0.07712540705285936
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp213 (ext xgboost 88/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 6174}
- Result: composite=-2.6301 val=-2.5082184174871567 train=-0.06993706128031396
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp214 (ext xgboost 89/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 30, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-2.0443 val=-1.9926110509273278 train=-0.9588802615207714
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp215 (ext xgboost 90/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 50, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-2.0986 val=-2.0503232608019157 train=-1.0847150110148054
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp216 (ext xgboost 91/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 100, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-2.2477 val=-2.203194042233215 train=-1.3125195274716894
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.
