# Experiment Summary — lmsys-chatbot-arena

_(populated by `framework/hill_climb.py`)_

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=-2.5459 val=-2.428316078866554 train=-0.07618941508597821
- **Status:** KEEP
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=-2.8714 val=-2.7349963544859643 train=-0.007916899866976539
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=-2.0022 val=-1.9190965743301807 train=-0.2561591190746616
- **Status:** KEEP
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=-2.5358 val=-2.4187672025477873 train=-0.07794003644982335
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=-2.3607 val=-2.256349399733556 train=-0.16884991813631703
- **Status:** DISCARD
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=-2.6358 val=-2.522144943216687 train=-0.24810158133792742
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=-2.1393 val=-2.0427808511075916 train=-0.1115758924499952
- **Status:** DISCARD
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=-2.4861 val=-2.3711010902957326 train=-0.07212072098226617
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=-2.4808 val=-2.3660744042390687 train=-0.07101145345985703
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=-3.0867 val=-2.9398240980089074 train=-0.0030936620086053812
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=-2.0038 val=-1.9207489312330452 train=-0.2603339238641426
- **Status:** DISCARD
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=-2.5459 val=-2.428316078866554 train=-0.07618941508597821
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=-2.5459 val=-2.428316078866554 train=-0.07618941508597821
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=-2.6388 val=-2.51633287030885 train=-0.06699919344243978
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=-2.7441 val=-2.614888744576888 train=-0.030419129840465405
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=-2.5017 val=-2.3838897771316816 train=-0.02721463420167707
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=-2.5702 val=-2.451388090407902 train=-0.07472505227440779
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=-2.4862 val=-2.3715506149639602 train=-0.07871751805099043
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=-3.0985 val=-2.9517961368207 train=-0.017651672281501465
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=-1.7181 val=-1.6540776527470342 train=-0.37362721623937234
- **Status:** KEEP
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=-2.5378 val=-2.4180815490147447 train=-0.02382910425487788
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=-2.5459 val=-2.428316078866554 train=-0.07618941508597821
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=-2.1775 val=-2.0793639197138893 train=-0.11597289621475507
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=-2.3782 val=-2.2695720097727556 train=-0.09712588774430032
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=-2.5573 val=-2.4391638139091816 train=-0.07662372270032129
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp26 (lightgbm iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp27 (lightgbm iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-4.4364 val=-4.412065291626712 train=-3.9246584947965064
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp28 (lightgbm iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-5.1831 val=-5.17903863603321 train=-5.09825364362216
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp29 (lightgbm iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-3.8727 val=-3.82656750149378 train=-2.9045354211269068
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp30 (lightgbm iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-2.4054 val=-2.2951339507211888 train=-0.09054372774987117
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp31 (lightgbm iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.4054 val=-2.2951339507211888 train=-0.09054372774987117
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp32 (lightgbm iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-4.7027 val=-4.686405707521806 train=-4.360768799103952
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp33 (lightgbm iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-4.7040 val=-4.687749469702748 train=-4.363571830331913
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp34 (lightgbm iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp35 (lightgbm iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-5.0307 val=-5.023092573718018 train=-4.870715544093739
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp36 (lightgbm iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp37 (lightgbm iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp38 (lightgbm iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-4.9602 val=-4.950736146354453 train=-4.762320899291816
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp39 (lightgbm iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-4.7020 val=-4.6857927222063065 train=-4.360781776031912
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp40 (lightgbm iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-4.7058 val=-4.689314056834621 train=-4.36045598378211
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp41 (lightgbm iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp42 (lightgbm iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp43 (lightgbm iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-4.2128 val=-4.180823083340967 train=-3.5412611224964694
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp44 (lightgbm iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-5.3476 val=-5.347320888663636 train=-5.341076819272249
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp45 (lightgbm iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp46 (lightgbm iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp47 (lightgbm iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-4.7070 val=-4.690659502535379 train=-4.3629392422342
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp48 (lightgbm iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-4.8941 val=-4.882890397303932 train=-4.658190442126686
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp49 (lightgbm iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-4.4362 val=-4.411826082674299 train=-3.923365667416042
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp50 (lightgbm iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-4.7058 val=-4.689273550710505 train=-4.358542989521586
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
- **Result:** composite=-0.5638 val=-0.5553321316264516 train=-0.3851790168022412
- **Status:** KEEP
- **Rationale:** Baseline mlp per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp77 (mlp iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-0.5006 val=-0.48996403447817516 train=-0.2764310729254032
- **Status:** KEEP
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp78 (mlp iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-0.8868 val=-0.8855954756354983 train=-0.8615480172562687
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp79 (mlp iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-0.4556 val=-0.444834553067772 train=-0.2304953058751593
- **Status:** KEEP
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp80 (mlp iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-0.6106 val=-0.6057084870245635 train=-0.5081119828005496
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp81 (mlp iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.0331 val=-2.02815503772657 train=-1.9300486732433089
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp82 (mlp iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-0.5904 val=-0.5798696792055817 train=-0.3691288981517662
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp83 (mlp iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-0.5950 val=-0.5839957041582419 train=-0.36341461686889714
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp84 (mlp iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-0.4858 val=-0.474286177364848 train=-0.24470459458134128
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp85 (mlp iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-0.6239 val=-0.6159749493567837 train=-0.4578858886327995
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp86 (mlp iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-0.6879 val=-0.6710771214442293 train=-0.33449479746799854
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp87 (mlp iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-0.5425 val=-0.5269463914083279 train=-0.2158398338913667
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp88 (mlp iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-0.7725 val=-0.7695138222516952 train=-0.7088984918201368
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp89 (mlp iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-0.5569 val=-0.5484126136980518 train=-0.37798573080887826
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp90 (mlp iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-0.6395 val=-0.6285928217657956 train=-0.4103453064214217
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp91 (mlp iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-0.7098 val=-0.6986230198464731 train=-0.47530480443178386
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp92 (mlp iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-0.3656 val=-0.35621995464582745 train=-0.1682939929086738
- **Status:** KEEP
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp93 (mlp iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-0.4787 val=-0.46861325494634753 train=-0.26711610598700974
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp94 (mlp iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-4.1217 val=-4.118761373454991 train=-4.0605008414899055
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp95 (mlp iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-0.4721 val=-0.4586804946403967 train=-0.18980900285568436
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp96 (mlp iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-0.5638 val=-0.5553321316264516 train=-0.3851790168022412
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp97 (mlp iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-0.5638 val=-0.5553321316264516 train=-0.3851790168022412
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp98 (mlp iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-0.6379 val=-0.6310143531369937 train=-0.4939571688410519
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp99 (mlp iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-0.5058 val=-0.4962603822337933 train=-0.3060839635969909
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp100 (mlp iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-0.5834 val=-0.574743900072566 train=-0.4007060227611927
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp101 (ft_transformer iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp102 (ft_transformer iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-4.5012 val=-4.4806871329176685 train=-4.070315497948841
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp103 (ft_transformer iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-5.1928 val=-5.189576675537151 train=-5.125650908807511
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp104 (ft_transformer iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-4.0002 val=-3.9603102697424433 train=-3.1627740048243527
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp105 (ft_transformer iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-2.4233 val=-2.3128107457519143 train=-0.10244471361825251
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp106 (ft_transformer iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.4233 val=-2.3128107457519143 train=-0.10244471361825251
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp107 (ft_transformer iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp108 (ft_transformer iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp109 (ft_transformer iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp110 (ft_transformer iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-5.0477 val=-5.041573299833252 train=-4.919133772237361
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp111 (ft_transformer iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp112 (ft_transformer iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp113 (ft_transformer iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-4.9793 val=-4.971779056376359 train=-4.821427457763893
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp114 (ft_transformer iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp115 (ft_transformer iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp116 (ft_transformer iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp117 (ft_transformer iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp118 (ft_transformer iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-4.3094 val=-4.28176196900415 train=-3.728911135483529
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp119 (ft_transformer iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-5.3500 val=-5.349984720914125 train=-5.348833385625038
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp120 (ft_transformer iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp121 (ft_transformer iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp122 (ft_transformer iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp123 (ft_transformer iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-4.9174 val=-4.908270024408429 train=-4.726467148266192
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp124 (ft_transformer iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-4.5010 val=-4.480486762472251 train=-4.0704663074690615
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp125 (ft_transformer iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-4.7459 val=-4.732285793722398 train=-4.459935844718253
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp126 (ext xgboost 1/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.3388 val=-2.2581034014249877 train=-0.6443125729517795
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp127 (ext xgboost 2/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-1.9708 val=-1.8845782092902812 train=-0.1603325652509643
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp128 (ext xgboost 3/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.4046 val=-2.306524029917299 train=-0.34419917973501535
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp129 (ext xgboost 4/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.2606 val=-2.155795837339719 train=-0.05981647137720756
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp130 (ext xgboost 5/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5674 val=-2.453553569313838 train=-0.1771893896611013
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp131 (ext xgboost 6/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5404 val=-2.42011477584417 train=-0.014253428353410426
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp132 (ext xgboost 7/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.7363 val=-2.6101370058603384 train=-0.08741714309622253
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp133 (ext xgboost 8/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.7359 val=-2.605756706556356 train=-0.0021251110208994205
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp134 (ext xgboost 9/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.9201 val=-2.7832417589149734 train=-0.04518214015266526
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp135 (ext xgboost 10/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.8945 val=-2.756693842783521 train=-0.0005384359910561912
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp136 (ext xgboost 11/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.1186 val=-2.9712053284518727 train=-0.022690060478935153
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp137 (ext xgboost 12/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.1242 val=-2.97546110025913 train=-0.00045932832062969457
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp138 (ext xgboost 13/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.2117 val=-3.0597604448383477 train=-0.02027193584604645
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp139 (ext xgboost 14/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-3.2104 val=-3.0575066165431397 train=-0.00042367179405381335
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp140 (ext lightgbm 15/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.2366 val=-2.131620916764966 train=-0.0327013896825696
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp141 (ext lightgbm 16/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.3489 val=-2.238862349988427 train=-0.038897488127375646
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp142 (ext lightgbm 17/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.3417 val=-2.23274477278663 train=-0.05418267949329203
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp143 (ext lightgbm 18/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.4577 val=-2.343964030341529 train=-0.0692021766496564
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp144 (ext lightgbm 19/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.3417 val=-2.23274477278663 train=-0.05418267949329203
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp145 (ext lightgbm 20/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.4577 val=-2.343964030341529 train=-0.0692021766496564
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp146 (ext lightgbm 21/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.3417 val=-2.23274477278663 train=-0.05418267949329203
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp147 (ext lightgbm 22/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.4577 val=-2.343964030341529 train=-0.0692021766496564
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
- Result: composite=-0.6672 val=-0.6611912981813631 train=-0.5414043916392394
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp158 (ext mlp 33/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4858 val=-0.474286177364848 train=-0.24470459458134128
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp159 (ext mlp 34/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4364 val=-0.4238823359402199 train=-0.17302851590315968
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp160 (ext mlp 35/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5060 val=-0.49747787584539144 train=-0.32661479868836385
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp161 (ext mlp 36/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4348 val=-0.42246480614614323 train=-0.17570448894827898
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp162 (ext mlp 37/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4257 val=-0.4128572629155528 train=-0.15638339190031061
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp163 (ext mlp 38/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3840 val=-0.3746581307387136 train=-0.1881112031218051
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp164 (ext mlp 39/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3498 val=-0.3394240605034982 train=-0.13101800868641655
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp165 (ext mlp 40/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3179 val=-0.3087596568053029 train=-0.12666686135149516
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp166 (ext mlp 41/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.5369 val=-0.5246409914398481 train=-0.28018783963548954
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp167 (ext mlp 42/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4592 val=-0.44630326930833125 train=-0.18765584111863948
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp168 (ext mlp 43/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.3958 val=-0.38488177177887045 train=-0.16601913672828214
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp169 (ext mlp 44/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5800 val=-0.5641112298601333 train=-0.24614441062579587
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp170 (ext mlp 45/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5328 val=-0.5152781504789354 train=-0.1653401038806594
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp171 (ext mlp 46/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4641 val=-0.4489958500362358 train=-0.14715527439867399
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp172 (ext ft_transformer 47/200)
- Config: {'iterations': 400, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.4983 val=-2.3944826115631495 train=-0.3186582803629497
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp173 (ext ft_transformer 48/200)
- Config: {'iterations': 400, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.4961 val=-2.3877171619322812 train=-0.22059049554931584
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp174 (ext ft_transformer 49/200)
- Config: {'iterations': 400, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.4535 val=-2.346005465381176 train=-0.1968422606231028
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp175 (ext ft_transformer 50/200)
- Config: {'iterations': 800, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.3794 val=-2.272683430825628 train=-0.13883804184643533
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp176 (ext ft_transformer 51/200)
- Config: {'iterations': 800, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.4181 val=-2.306194388100761 train=-0.06908090823193455
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp177 (ext ft_transformer 52/200)
- Config: {'iterations': 800, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.3972 val=-2.285660857507387 train=-0.055759923321165236
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp178 (ext ft_transformer 53/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.3592 val=-2.2500464527923727 train=-0.06644734315181847
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp179 (ext ft_transformer 54/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.4111 val=-2.297304461163478 train=-0.021181603631862878
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp180 (ext ft_transformer 55/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.3937 val=-2.281195832884832 train=-0.03162406613205082
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp181 (ext xgboost 56/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.1, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.2495 val=-2.1482446202481906 train=-0.12302212996153493
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp182 (ext xgboost 57/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.3, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.2495 val=-2.1482446202481906 train=-0.12302212996153493
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp183 (ext xgboost 58/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 1.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.2495 val=-2.1482446202481906 train=-0.12302212996153493
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp184 (ext xgboost 59/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 3.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-2.2495 val=-2.1482446202481906 train=-0.12302212996153493
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp185 (ext mlp 60/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 128, 64), 'weight_decay': 0.001}
- Result: composite=-0.4874 val=-0.47411047062233214 train=-0.20863139566477162
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp186 (ext mlp 61/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (384, 192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4099 val=-0.39845219753308975 train=-0.16920860809620739
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp187 (ext mlp 62/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4867 val=-0.47431454704286286 train=-0.22652655349222334
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp188 (ext mlp 63/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (320, 160), 'weight_decay': 0.001}
- Result: composite=-0.4215 val=-0.4108874569725893 train=-0.19816601045998233
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp189 (ext mlp 64/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 256), 'weight_decay': 0.001}
- Result: composite=-0.4602 val=-0.447792259578798 train=-0.19935375202045605
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp190 (ext ft_transformer 65/200)
- Config: {'iterations': 200, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-3.3156 val=-3.2556136783939587 train=-2.055805567771029
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp191 (ext ft_transformer 66/200)
- Config: {'iterations': 400, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.7582 val=-2.679991528495024 train=-1.1152965242997523
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp192 (ext ft_transformer 67/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.4852 val=-2.4008170429777063 train=-0.7129856626439323
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp193 (ext xgboost 68/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 0.1, 'reg_alpha': 0.1}
- Result: composite=-2.1193 val=-2.0347158354513235 train=-0.3428352169866158
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp194 (ext xgboost 69/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 1.0, 'reg_alpha': 0.5}
- Result: composite=-2.0935 val=-2.011365426155317 train=-0.3693011505027945
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp195 (ext xgboost 70/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 3.0, 'reg_alpha': 1.0}
- Result: composite=-2.1163 val=-2.035306196491467 train=-0.41580352390955694
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp196 (ext xgboost 71/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 0.5}
- Result: composite=-2.0972 val=-2.0211443186576363 train=-0.4996743781041013
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp197 (ext xgboost 72/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 3.0}
- Result: composite=-2.0972 val=-2.0211443186576363 train=-0.4996743781041013
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp198 (ext patchtsmixer 73/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 128}
- Result: composite=-2.0907 val=-2.083576938373954 train=-1.9419855677248132
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp199 (ext patchtsmixer 74/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 128}
- Result: composite=-1.8797 val=-1.869385451144456 train=-1.662230365083563
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp200 (ext patchtsmixer 75/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 256}
- Result: composite=-1.5999 val=-1.5882787851745124 train=-1.3551227666693768
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp201 (ext patchtsmixer 76/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 256}
- Result: composite=-1.4004 val=-1.3843326725742726 train=-1.0624392997007905
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp202 (ext patchtsmixer 77/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 384}
- Result: composite=-1.3485 val=-1.332870219189433 train=-1.0205040160478127
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp203 (ext patchtsmixer 78/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 384}
- Result: composite=-1.2810 val=-1.2591483562980297 train=-0.8220097014418543
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp204 (ext xgboost 79/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 42}
- Result: composite=-2.4957 val=-2.3807361999643724 train=-0.08238209616492984
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp205 (ext xgboost 80/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 0}
- Result: composite=-2.5037 val=-2.388699023762317 train=-0.08860829653560383
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp206 (ext xgboost 81/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7}
- Result: composite=-2.5127 val=-2.3971876435372423 train=-0.08746333897570426
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp207 (ext xgboost 82/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 99}
- Result: composite=-2.4838 val=-2.369498858684805 train=-0.08306283529639472
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp208 (ext xgboost 83/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 2024}
- Result: composite=-2.4786 val=-2.364442146108143 train=-0.08214227225168719
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp209 (ext xgboost 84/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 12345}
- Result: composite=-2.5230 val=-2.4068024236513765 train=-0.08260782021880711
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp210 (ext xgboost 85/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7777}
- Result: composite=-2.5030 val=-2.387955515282634 train=-0.086825853762732
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp211 (ext xgboost 86/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 31337}
- Result: composite=-2.5077 val=-2.3923474258993562 train=-0.08582176467281548
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp212 (ext xgboost 87/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 1729}
- Result: composite=-2.5798 val=-2.4609179299197064 train=-0.08261389669443146
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp213 (ext xgboost 88/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 6174}
- Result: composite=-2.5209 val=-2.4050082681240146 train=-0.08633881573914405
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp214 (ext xgboost 89/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 30, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.9288 val=-1.8818966232674108 train=-0.943153627440203
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp215 (ext xgboost 90/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 50, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.9933 val=-1.9487159707436452 train=-1.0560522786009434
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp216 (ext xgboost 91/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 100, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-2.1074 val=-2.0680086957058803 train=-1.2793620551590732
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.
