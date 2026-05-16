# Experiment Summary — tmdb-box-office-prediction

_(populated by `framework/hill_climb.py`)_

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=-2.2181 val=-2.115232458844642 train=-0.05887587891948178
- **Status:** KEEP
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=-2.5793 val=-2.4567547810908685 train=-0.006623132936376364
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=-1.7276 val=-1.6560195186680973 train=-0.22500438785248122
- **Status:** KEEP
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=-2.1529 val=-2.053699676584379 train=-0.07015433336987288
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=-2.0463 val=-1.9563844872214715 train=-0.15718774731049695
- **Status:** DISCARD
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=-2.2874 val=-2.188956075800112 train=-0.22064964524203198
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=-2.0337 val=-1.9418403247675413 train=-0.10386570178745064
- **Status:** DISCARD
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=-2.2367 val=-2.133190414985998 train=-0.06260186700450515
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=-2.1932 val=-2.091589766934068 train=-0.059984562767348024
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=-2.7364 val=-2.6062801075758353 train=-0.00336480666919503
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=-1.7936 val=-1.7185488496462955 train=-0.217928433535179
- **Status:** DISCARD
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=-2.2181 val=-2.115232458844642 train=-0.05887587891948178
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=-2.2181 val=-2.115232458844642 train=-0.05887587891948178
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=-2.3165 val=-2.2086799877320407 train=-0.05294610715452399
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=-2.3901 val=-2.2775252778611232 train=-0.026381524038439175
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=-2.2403 val=-2.134740496013753 train=-0.022761439030219686
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=-2.2231 val=-2.120218057574225 train=-0.06338838541650522
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=-2.1679 val=-2.067560980196191 train=-0.06115143571494426
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=-2.7852 val=-2.65333046628647 train=-0.015316844646635661
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=-1.5215 val=-1.4644083011632614 train=-0.32346691145294715
- **Status:** KEEP
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=-2.2124 val=-2.107946519712552 train=-0.018463438993107074
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=-2.2181 val=-2.115232458844642 train=-0.05887587891948178
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=-1.8697 val=-1.7854037791454325 train=-0.09999151417371192
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=-2.0795 val=-1.9846638747082337 train=-0.08802704290724139
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=-2.2357 val=-2.1321942338050226 train=-0.06211374742783892
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp26 (lightgbm iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp27 (lightgbm iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-3.9360 val=-3.9150372290570217 train=-3.496232686802921
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp28 (lightgbm iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-4.5422 val=-4.539245480783358 train=-4.4808783030387636
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp29 (lightgbm iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-3.4402 val=-3.40107865434524 train=-2.6181258858485883
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp30 (lightgbm iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-2.1689 val=-2.069803324614275 train=-0.08878079657548377
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp31 (lightgbm iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.1689 val=-2.069803324614275 train=-0.08878079657548377
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp32 (lightgbm iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-4.1643 val=-4.150239279686312 train=-3.8690299202068155
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp33 (lightgbm iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-4.1633 val=-4.149148645725608 train=-3.866261807108715
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp34 (lightgbm iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp35 (lightgbm iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-4.4269 val=-4.420639378840637 train=-4.295119082407205
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp36 (lightgbm iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp37 (lightgbm iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp38 (lightgbm iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-4.3741 val=-4.366063240066945 train=-4.205209806525815
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp39 (lightgbm iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-4.1641 val=-4.150078418641756 train=-3.869652197904065
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp40 (lightgbm iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-4.1683 val=-4.154118799207782 train=-3.870350827920367
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp41 (lightgbm iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp42 (lightgbm iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp43 (lightgbm iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-3.7403 val=-3.712925184651863 train=-3.1660875570929488
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp44 (lightgbm iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-4.6794 val=-4.6683373002680355 train=-4.67888978924377
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp45 (lightgbm iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp46 (lightgbm iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp47 (lightgbm iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-4.1688 val=-4.154585781747538 train=-3.8701281827059772
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp48 (lightgbm iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-4.3210 val=-4.311311677864849 train=-4.117952353134179
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp49 (lightgbm iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-3.9375 val=-3.91640684584198 train=-3.4950026999701604
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp50 (lightgbm iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-4.1636 val=-4.14959550475922 train=-3.8685764907516496
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
- **Result:** composite=-0.5057 val=-0.4984710532587138 train=-0.35310640412713196
- **Status:** KEEP
- **Rationale:** Baseline mlp per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp77 (mlp iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-0.4269 val=-0.4184630136496231 train=-0.2500435820976935
- **Status:** KEEP
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp78 (mlp iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-0.7423 val=-0.7394200176035683 train=-0.6816220649881307
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp79 (mlp iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-0.4002 val=-0.39135848798981426 train=-0.21375178354478455
- **Status:** KEEP
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp80 (mlp iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-0.5565 val=-0.5504451564959307 train=-0.42923351927608056
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp81 (mlp iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-1.9016 val=-1.8919966584916075 train=-1.7000474334157996
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp82 (mlp iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-0.5472 val=-0.5380345924097698 train=-0.35379586256108364
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp83 (mlp iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-0.5045 val=-0.4971167761890043 train=-0.35038957967782997
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp84 (mlp iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-0.4124 val=-0.40343394306721664 train=-0.22468913776718674
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp85 (mlp iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-0.5903 val=-0.5823000856676912 train=-0.42252986026521544
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp86 (mlp iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-0.5475 val=-0.535391567868981 train=-0.29371892886496775
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp87 (mlp iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-0.4553 val=-0.442304659038847 train=-0.18322636999764974
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp88 (mlp iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-0.6756 val=-0.6712690992497414 train=-0.5851458223888223
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp89 (mlp iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-0.5215 val=-0.5128203611916232 train=-0.3399731510269162
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp90 (mlp iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-0.5661 val=-0.5557601389764464 train=-0.34947548332301004
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp91 (mlp iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-0.6342 val=-0.6247160504960071 train=-0.43581582220516185
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp92 (mlp iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-0.3490 val=-0.34001806326875805 train=-0.16020466491404095
- **Status:** KEEP
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp93 (mlp iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-0.4182 val=-0.4098809908062316 train=-0.24404792551637253
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp94 (mlp iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-3.7890 val=-3.7818797194035843 train=-3.788670596275818
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp95 (mlp iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-0.4035 val=-0.39382406628043426 train=-0.2010533159385963
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp96 (mlp iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-0.5057 val=-0.4984710532587138 train=-0.35310640412713196
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp97 (mlp iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-0.5057 val=-0.4984710532587138 train=-0.35310640412713196
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp98 (mlp iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-0.5637 val=-0.5572315492617457 train=-0.4275638292579414
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp99 (mlp iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-0.4487 val=-0.44112883771144185 train=-0.2889610576478294
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp100 (mlp iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-0.5449 val=-0.5359309916198405 train=-0.35633357138591576
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp101 (ft_transformer iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp102 (ft_transformer iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-3.9503 val=-3.9356164528184556 train=-3.641237145060109
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp103 (ft_transformer iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-4.5603 val=-4.557859921745293 train=-4.509447765878108
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp104 (ft_transformer iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-3.4946 val=-3.4640245879649942 train=-2.8529693806499674
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp105 (ft_transformer iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-2.0977 val=-2.0025010453093324 train=-0.09770563243023103
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp106 (ft_transformer iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-2.0977 val=-2.0025010453093324 train=-0.09770563243023103
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp107 (ft_transformer iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp108 (ft_transformer iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp109 (ft_transformer iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp110 (ft_transformer iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-4.4470 val=-4.442046275666809 train=-4.343907558756892
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp111 (ft_transformer iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp112 (ft_transformer iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp113 (ft_transformer iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-4.3870 val=-4.381176806124777 train=-4.2646383446903195
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp114 (ft_transformer iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp115 (ft_transformer iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp116 (ft_transformer iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp117 (ft_transformer iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp118 (ft_transformer iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-3.7690 val=-3.7491689328075735 train=-3.3521760628978368
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp119 (ft_transformer iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-4.6880 val=-4.676485126829606 train=-4.687447033450508
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp120 (ft_transformer iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp121 (ft_transformer iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp122 (ft_transformer iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp123 (ft_transformer iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-4.3307 val=-4.323827280489107 train=-4.1867008295103965
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp124 (ft_transformer iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-3.9508 val=-3.9360361264355612 train=-3.6409677718790268
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp125 (ft_transformer iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-4.1758 val=-4.165989339285481 train=-3.9703471569538054
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp126 (ext xgboost 1/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.0152 val=-1.9469479346658665 train=-0.5828977957073422
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp127 (ext xgboost 2/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-1.8044 val=-1.7254923269962898 train=-0.14828237157303023
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp128 (ext xgboost 3/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.0871 val=-2.00250397337711 train=-0.3112898043186742
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp129 (ext xgboost 4/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.0017 val=-1.9086424400936355 train=-0.04654201061961024
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp130 (ext xgboost 5/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.2631 val=-2.1629124418994037 train=-0.15902684485679167
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp131 (ext xgboost 6/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.2306 val=-2.124897561689636 train=-0.011611966046615133
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp132 (ext xgboost 7/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.4231 val=-2.3114371047922546 train=-0.07885685498296623
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp133 (ext xgboost 8/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.4165 val=-2.301467352801943 train=-0.0017590826522591127
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp134 (ext xgboost 9/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5903 val=-2.4688782477566797 train=-0.040889324140209064
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp135 (ext xgboost 10/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5766 val=-2.4539140537821633 train=-0.0005155908853598599
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp136 (ext xgboost 11/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.7533 val=-2.6231511280648174 train=-0.02025522205250224
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp137 (ext xgboost 12/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.7250 val=-2.595242817567368 train=-0.00047202972590073796
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp138 (ext xgboost 13/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.8033 val=-2.6705915257279687 train=-0.01678611315661114
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp139 (ext xgboost 14/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.7860 val=-2.653336666367065 train=-0.0004364949348859333
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp140 (ext lightgbm 15/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0177 val=-1.9234961602107965 train=-0.03957553797306295
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp141 (ext lightgbm 16/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0653 val=-1.9690470177527306 train=-0.04299364692872338
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp142 (ext lightgbm 17/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0979 val=-2.000728571254405 train=-0.05758460208509975
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp143 (ext lightgbm 18/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.1718 val=-2.0713900587538916 train=-0.06329852522840579
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp144 (ext lightgbm 19/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0979 val=-2.000728571254405 train=-0.05758460208509975
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp145 (ext lightgbm 20/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.1718 val=-2.0713900587538916 train=-0.06329852522840579
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp146 (ext lightgbm 21/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0979 val=-2.000728571254405 train=-0.05758460208509975
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp147 (ext lightgbm 22/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.1718 val=-2.0713900587538916 train=-0.06329852522840579
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
- Result: composite=-0.5935 val=-0.5871489145412643 train=-0.4604493320177734
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp158 (ext mlp 33/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4124 val=-0.40343394306721664 train=-0.22468913776718674
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp159 (ext mlp 34/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.3767 val=-0.36616080386006267 train=-0.1546301381364547
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp160 (ext mlp 35/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4575 val=-0.44896106792894597 train=-0.27800713034531793
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp161 (ext mlp 36/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4004 val=-0.389348615055504 train=-0.16917784900146352
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp162 (ext mlp 37/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.3849 val=-0.3734522708860551 train=-0.14443719870999325
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp163 (ext mlp 38/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3511 val=-0.34315915698571087 train=-0.18430425248331814
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp164 (ext mlp 39/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3450 val=-0.3355667707875215 train=-0.14723376908532362
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp165 (ext mlp 40/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3311 val=-0.3215500371721792 train=-0.1304218679130811
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp166 (ext mlp 41/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4748 val=-0.46356395246389537 train=-0.23787026059786034
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp167 (ext mlp 42/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4197 val=-0.4070012043061118 train=-0.15387122075105966
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp168 (ext mlp 43/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.3874 val=-0.376712524634764 train=-0.16264675304123818
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp169 (ext mlp 44/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4827 val=-0.469784342489504 train=-0.2114624714015845
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp170 (ext mlp 45/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4553 val=-0.442304659038847 train=-0.18322636999764974
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp171 (ext mlp 46/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4180 val=-0.40691072579621856 train=-0.18540804839375147
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp172 (ext ft_transformer 47/200)
- Config: {'iterations': 400, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.1456 val=-2.057185518211496 train=-0.2896208559006878
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp173 (ext ft_transformer 48/200)
- Config: {'iterations': 400, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.1407 val=-2.048540639484704 train=-0.20546576021811483
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp174 (ext ft_transformer 49/200)
- Config: {'iterations': 400, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.1262 val=-2.0337464489921175 train=-0.18481274571491904
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp175 (ext ft_transformer 50/200)
- Config: {'iterations': 800, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.0591 val=-1.9671604163752876 train=-0.1278492227714191
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp176 (ext ft_transformer 51/200)
- Config: {'iterations': 800, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.0874 val=-1.992006174450377 train=-0.08335484777478235
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp177 (ext ft_transformer 52/200)
- Config: {'iterations': 800, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.0860 val=-1.99021690291357 train=-0.0743032355092402
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp178 (ext ft_transformer 53/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.0436 val=-1.9492685449141312 train=-0.06301127253083029
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp179 (ext ft_transformer 54/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.0815 val=-1.9847979466814811 train=-0.05043022675151278
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp180 (ext ft_transformer 55/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.0813 val=-1.9843742850848698 train=-0.04524119441983382
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp181 (ext xgboost 56/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.1, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.9526 val=-1.8644121684641612 train=-0.09971819804817972
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp182 (ext xgboost 57/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.3, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.9526 val=-1.8644121684641612 train=-0.09971819804817972
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp183 (ext xgboost 58/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 1.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.9526 val=-1.8644121684641612 train=-0.09971819804817972
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp184 (ext xgboost 59/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 3.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.9526 val=-1.8644121684641612 train=-0.09971819804817972
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp185 (ext mlp 60/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 128, 64), 'weight_decay': 0.001}
- Result: composite=-0.4531 val=-0.4409210948474192 train=-0.19753651856256646
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp186 (ext mlp 61/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (384, 192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4567 val=-0.4430710615519309 train=-0.170673571195331
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp187 (ext mlp 62/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4685 val=-0.4568481404540852 train=-0.2236746120118869
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp188 (ext mlp 63/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (320, 160), 'weight_decay': 0.001}
- Result: composite=-0.4390 val=-0.4271457576100757 train=-0.189814095869443
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp189 (ext mlp 64/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 256), 'weight_decay': 0.001}
- Result: composite=-0.4310 val=-0.41921193635218307 train=-0.18267413388719478
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp190 (ext ft_transformer 65/200)
- Config: {'iterations': 200, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.8130 val=-2.767285960758462 train=-1.8535443943194343
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp191 (ext ft_transformer 66/200)
- Config: {'iterations': 400, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.3088 val=-2.2470127041110755 train=-1.0119734947839765
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp192 (ext ft_transformer 67/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.0883 val=-2.0198236815785635 train=-0.6507501469442605
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp193 (ext xgboost 68/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 0.1, 'reg_alpha': 0.1}
- Result: composite=-1.8281 val=-1.7555353631630204 train=-0.3049074503922006
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp194 (ext xgboost 69/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 1.0, 'reg_alpha': 0.5}
- Result: composite=-1.7939 val=-1.7240504291133292 train=-0.3270859729858761
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp195 (ext xgboost 70/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 3.0, 'reg_alpha': 1.0}
- Result: composite=-1.8326 val=-1.76269172816031 train=-0.3637201672541235
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp196 (ext xgboost 71/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 0.5}
- Result: composite=-1.8330 val=-1.767531926515567 train=-0.4578873368115728
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp197 (ext xgboost 72/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 3.0}
- Result: composite=-1.8330 val=-1.767531926515567 train=-0.4578873368115728
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp198 (ext patchtsmixer 73/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 128}
- Result: composite=-1.6049 val=-1.6030767214162596 train=-1.5669681749307252
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp199 (ext patchtsmixer 74/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 128}
- Result: composite=-1.5335 val=-1.5260547554921657 train=-1.3767856793689
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp200 (ext patchtsmixer 75/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 256}
- Result: composite=-1.3091 val=-1.2992681001889173 train=-1.1028960252383595
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp201 (ext patchtsmixer 76/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 256}
- Result: composite=-1.1849 val=-1.1684057126410652 train=-0.8382562226526126
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp202 (ext patchtsmixer 77/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 384}
- Result: composite=-1.1245 val=-1.1090359236778287 train=-0.8004683092433678
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp203 (ext patchtsmixer 78/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 384}
- Result: composite=-1.1087 val=-1.0858069142377058 train=-0.6286750984701819
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp204 (ext xgboost 79/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 42}
- Result: composite=-2.1958 val=-2.094477968203426 train=-0.06869314657918431
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp205 (ext xgboost 80/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 0}
- Result: composite=-2.1928 val=-2.091697141974989 train=-0.06928179870426038
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp206 (ext xgboost 81/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7}
- Result: composite=-2.1650 val=-2.0650436437395983 train=-0.06677186815741433
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp207 (ext xgboost 82/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 99}
- Result: composite=-2.1734 val=-2.07315122213447 train=-0.06886480334326166
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp208 (ext xgboost 83/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 2024}
- Result: composite=-2.2005 val=-2.098953272306211 train=-0.0678060652332125
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp209 (ext xgboost 84/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 12345}
- Result: composite=-2.1788 val=-2.078488081570523 train=-0.07202734196005688
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp210 (ext xgboost 85/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7777}
- Result: composite=-2.1798 val=-2.0792376759035336 train=-0.06884809250389023
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp211 (ext xgboost 86/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 31337}
- Result: composite=-2.2115 val=-2.109515376188448 train=-0.06980385850287102
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp212 (ext xgboost 87/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 1729}
- Result: composite=-2.2070 val=-2.1052501897663447 train=-0.06971376526024498
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp213 (ext xgboost 88/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 6174}
- Result: composite=-2.2173 val=-2.1150021694163206 train=-0.0690523176324974
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp214 (ext xgboost 89/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 30, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.7395 val=-1.6974798315364164 train=-0.8567260838719456
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp215 (ext xgboost 90/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 50, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.8081 val=-1.7679468602786237 train=-0.9646322041621048
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp216 (ext xgboost 91/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 100, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.9068 val=-1.8708725322646709 train=-1.1524531425665263
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.
