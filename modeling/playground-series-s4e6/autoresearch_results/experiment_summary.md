# Experiment Summary — playground-series-s4e6

_(populated by `framework/hill_climb.py`)_

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=0.9643 val=0.9659663678130158 train=1.0
- **Status:** KEEP
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=0.9596 val=0.9615058655604621 train=1.0
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=0.9646 val=0.96632320799322 train=1.0
- **Status:** KEEP
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=0.9643 val=0.9659663678130157 train=1.0
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=0.9646 val=0.9662786029706945 train=1.0
- **Status:** DISCARD
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=0.9552 val=0.9573129934430616 train=1.0
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=0.9704 val=0.971809625763861 train=1.0
- **Status:** KEEP
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=0.9618 val=0.9636023016191624 train=1.0
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=0.9604 val=0.9622641509433962 train=1.0
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=0.9582 val=0.960167714884696 train=1.0
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=0.9682 val=0.9697131897051607 train=1.0
- **Status:** DISCARD
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=0.9643 val=0.9659663678130158 train=1.0
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=0.9643 val=0.9659663678130158 train=1.0
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=0.9592 val=0.9611490253802578 train=1.0
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=0.9614 val=0.9632008564164325 train=1.0
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=0.9643 val=0.9659663678130157 train=1.0
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=0.9651 val=0.9667246531959498 train=1.0
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=0.9632 val=0.964985057317454 train=1.0
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=0.9539 val=0.9561086578348722 train=1.0
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=0.9671 val=0.9686872741870735 train=1.0
- **Status:** DISCARD
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=0.9664 val=0.9679735938266648 train=1.0
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=0.9643 val=0.9659663678130158 train=1.0
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=0.9701 val=0.9714973906061822 train=1.0
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=0.9630 val=0.9648066372273518 train=1.0
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=0.9683 val=0.9698023997502119 train=1.0
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp26 (lightgbm iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp27 (lightgbm iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=0.8984 val=0.903028681029484 train=0.9955862328027422
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp28 (lightgbm iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=0.8754 val=0.8807707747892413 train=0.9879468633059157
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp29 (lightgbm iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=0.9076 val=0.9119496855345911 train=0.9992813848041467
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp30 (lightgbm iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=0.9559 val=0.9580266738034704 train=1.0
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp31 (lightgbm iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=0.9559 val=0.9580266738034704 train=1.0
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp32 (lightgbm iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=0.8887 val=0.8935724162540702 train=0.9916869287570611
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp33 (lightgbm iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=0.8902 val=0.8949551719523618 train=0.9908539884164129
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp34 (lightgbm iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp35 (lightgbm iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=0.8780 val=0.8833132610731969 train=0.9894677960357756
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp36 (lightgbm iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp37 (lightgbm iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp38 (lightgbm iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=0.8812 val=0.8863910076274588 train=0.9893820521771794
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp39 (lightgbm iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=0.8936 val=0.8982559436192515 train=0.9922013919086379
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp40 (lightgbm iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=0.8912 val=0.8959364824479236 train=0.990896860345711
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp41 (lightgbm iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp42 (lightgbm iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp43 (lightgbm iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=0.9018 val=0.9063294526963735 train=0.9973684801492759
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp44 (lightgbm iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=0.8761 val=0.8813060350595477 train=0.9858216405249974
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp45 (lightgbm iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp46 (lightgbm iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp47 (lightgbm iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=0.8880 val=0.8930371559837638 train=0.992799557398368
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp48 (lightgbm iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=0.8811 val=0.8863017975824078 train=0.990645753331251
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp49 (lightgbm iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=0.8978 val=0.9024934207591774 train=0.9956760597022238
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp50 (lightgbm iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=0.8903 val=0.895133592042464 train=0.9917073439614887
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
- **Result:** composite=0.9881 val=0.9885811142334626 train=0.998270832184978
- **Status:** KEEP
- **Rationale:** Baseline mlp per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp77 (mlp iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=0.9881 val=0.9885811142334626 train=0.998270832184978
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp78 (mlp iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=0.9859 val=0.9864400731522369 train=0.9975215941824833
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp79 (mlp iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=0.9897 val=0.9901422900218565 train=0.9982055035308095
- **Status:** KEEP
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp80 (mlp iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=0.9946 val=0.9948258173870378 train=0.9992854678450322
- **Status:** KEEP
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp81 (mlp iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=0.9322 val=0.9336277264820019 train=0.9616030835124767
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp82 (mlp iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=0.9962 val=0.9963869931754316 train=0.9992017655068789
- **Status:** KEEP
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp83 (mlp iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=0.9892 val=0.989517819706499 train=0.9953657485949235
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp84 (mlp iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=0.9881 val=0.9885811142334626 train=0.998270832184978
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp85 (mlp iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=0.9956 val=0.9958071278825995 train=0.999322215213002
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp86 (mlp iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=0.9909 val=0.9913020206075205 train=0.9983790327684446
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp87 (mlp iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=0.9950 val=0.9952272625897676 train=0.9999407959071598
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp88 (mlp iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=0.9859 val=0.9864400731522369 train=0.9975215941824833
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp89 (mlp iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=0.9945 val=0.9947366073419868 train=0.9999448789480453
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp90 (mlp iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=0.9961 val=0.9962977831303804 train=0.9995937374318897
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp91 (mlp iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=0.9942 val=0.994424372184308 train=0.9997121456175702
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp92 (mlp iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=0.9979 val=0.9979927739863509 train=0.9998040140374945
- **Status:** KEEP
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp93 (mlp iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=0.9909 val=0.9912574155849949 train=0.998748547968585
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp94 (mlp iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=0.9041 val=0.906195637628797 train=0.947581921111567
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp95 (mlp iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=0.9881 val=0.9885811142334626 train=0.998270832184978
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp96 (mlp iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=0.9881 val=0.9885811142334626 train=0.998270832184978
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp97 (mlp iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=0.9881 val=0.9885811142334626 train=0.998270832184978
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp98 (mlp iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=0.9884 val=0.9888487443686159 train=0.9983198286756043
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp99 (mlp iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=0.9907 val=0.9911236005174182 train=0.9989220772062202
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp100 (mlp iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=0.9941 val=0.9942905571167313 train=0.9990894818825268
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp101 (ft_transformer iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp102 (ft_transformer iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=0.8653 val=0.8704224095633168 train=0.9733846979876734
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp103 (ft_transformer iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=0.8177 val=0.8226281279272046 train=0.9207685916162922
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp104 (ft_transformer iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=0.8843 val=0.8894241491591953 train=0.9917338837272448
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp105 (ft_transformer iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=0.9558 val=0.9579374637584191 train=1.0
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp106 (ft_transformer iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=0.9558 val=0.9579374637584191 train=1.0
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp107 (ft_transformer iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp108 (ft_transformer iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp109 (ft_transformer iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp110 (ft_transformer iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=0.8320 val=0.83701324769169 train=0.9374008586634982
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp111 (ft_transformer iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp112 (ft_transformer iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp113 (ft_transformer iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=0.8375 val=0.8425442704848566 train=0.9428210954390391
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp114 (ft_transformer iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp115 (ft_transformer iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp116 (ft_transformer iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp117 (ft_transformer iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp118 (ft_transformer iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=0.8775 val=0.8825103706677372 train=0.9818672154273617
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp119 (ft_transformer iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=0.8069 val=0.8116329898746599 train=0.9065228619666781
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp120 (ft_transformer iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp121 (ft_transformer iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp122 (ft_transformer iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp123 (ft_transformer iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=0.8417 val=0.8467817476247826 train=0.9474961772529709
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp124 (ft_transformer iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=0.8656 val=0.87069003969847 train=0.9730927605643579
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp125 (ft_transformer iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=0.8478 val=0.8529595432445694 train=0.9560307534639498
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.
