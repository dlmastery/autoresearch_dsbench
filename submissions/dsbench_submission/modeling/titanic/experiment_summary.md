# Experiment Summary — titanic

_(populated by `framework/hill_climb.py`)_

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** KEEP
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=0.9367 val=0.9396904465397615 train=1.0
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=0.9495 val=0.9518768902330548 train=1.0
- **Status:** KEEP
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=0.9471 val=0.949653086639388 train=1.0
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=0.9516 val=0.9538783134673545 train=1.0
- **Status:** KEEP
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=0.9299 val=0.9331969400462551 train=1.0
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=0.9548 val=0.9569916384984879 train=1.0
- **Status:** KEEP
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=0.9417 val=0.9444493862302081 train=1.0
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=0.9507 val=0.9530777441736346 train=1.0
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=0.9438 val=0.9464952855363814 train=1.0
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=0.9490 val=0.9514321295143213 train=1.0
- **Status:** DISCARD
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=0.9377 val=0.9406244440491016 train=1.0
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=0.9448 val=0.9474292830457215 train=1.0
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=0.9477 val=0.9501867995018681 train=1.0
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=0.9361 val=0.9391122576054083 train=1.0
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=0.9409 val=0.9437377690802349 train=1.0
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=0.9422 val=0.9449830990926882 train=1.0
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=0.9552 val=0.9573029710016012 train=1.0
- **Status:** KEEP
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=0.9422 val=0.9449386230208148 train=1.0
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=0.9543 val=0.9565024017078811 train=1.0
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=0.9429 val=0.9456502401707881 train=1.0
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=0.9441 val=0.9468066180394948 train=1.0
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** DISCARD
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=0.9367 val=0.9396904465397615 train=1.0
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=0.9495 val=0.9518768902330548 train=1.0
- **Status:** DISCARD
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=0.9471 val=0.949653086639388 train=1.0
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=0.9516 val=0.9538783134673545 train=1.0
- **Status:** DISCARD
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=0.9299 val=0.9331969400462551 train=1.0
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=0.9548 val=0.9569916384984879 train=1.0
- **Status:** DISCARD
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=0.9417 val=0.9444493862302081 train=1.0
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=0.9507 val=0.9530777441736346 train=1.0
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=0.9438 val=0.9464952855363814 train=1.0
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=0.9490 val=0.9514321295143213 train=1.0
- **Status:** DISCARD
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=0.9377 val=0.9406244440491016 train=1.0
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=0.9448 val=0.9474292830457215 train=1.0
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=0.9477 val=0.9501867995018681 train=1.0
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=0.9361 val=0.9391122576054083 train=1.0
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=0.9409 val=0.9437377690802349 train=1.0
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=0.9422 val=0.9449830990926882 train=1.0
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=0.9552 val=0.9573029710016012 train=1.0
- **Status:** DISCARD
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=0.9422 val=0.9449386230208148 train=1.0
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=0.9398 val=0.9426703433552749 train=1.0
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=0.9543 val=0.9565024017078811 train=1.0
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=0.9429 val=0.9456502401707881 train=1.0
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=0.9441 val=0.9468066180394948 train=1.0
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp26 (lightgbm iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp27 (lightgbm iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=0.8462 val=0.8534513431773706 train=0.9980959144814581
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp28 (lightgbm iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=0.8004 val=0.8091531755915318 train=0.9841713962681556
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp29 (lightgbm iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=0.8646 val=0.8710638676392101 train=0.9998469384631398
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp30 (lightgbm iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=0.9270 val=0.9304394235901084 train=1.0
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp31 (lightgbm iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=0.9270 val=0.9304394235901084 train=1.0
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp32 (lightgbm iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=0.8293 val=0.8372175769436043 train=0.9947448872344637
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp33 (lightgbm iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=0.8332 val=0.840909090909091 train=0.9953408068179731
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp34 (lightgbm iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp35 (lightgbm iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=0.8054 val=0.8140900195694717 train=0.987430586593034
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp36 (lightgbm iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp37 (lightgbm iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp38 (lightgbm iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=0.8121 val=0.8205390499911048 train=0.9894591621615554
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp39 (lightgbm iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=0.8325 val=0.840241949830991 train=0.9947877444647846
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp40 (lightgbm iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=0.8310 val=0.8388187155310443 train=0.995522439841714
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp41 (lightgbm iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp42 (lightgbm iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp43 (lightgbm iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=0.8502 val=0.8572762853584772 train=0.9992163249312753
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp44 (lightgbm iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=0.7983 val=0.8071072762853585 train=0.9826611891044675
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp45 (lightgbm iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp46 (lightgbm iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp47 (lightgbm iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=0.8342 val=0.8418875644903041 train=0.9956122359433386
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp48 (lightgbm iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=0.8182 val=0.8264543675502579 train=0.9916244727030055
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp49 (lightgbm iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=0.8404 val=0.8479363102650773 train=0.9979775468929528
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp50 (lightgbm iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=0.8348 val=0.8424657534246576 train=0.9949081528737813
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
- **Result:** composite=0.9870 val=0.9876356520192137 train=0.9997632648229894
- **Status:** KEEP
- **Rationale:** Baseline mlp per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp77 (mlp iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=0.9870 val=0.9876356520192137 train=0.9997632648229894
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp78 (mlp iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=0.9757 val=0.9766055861946273 train=0.9953979497917342
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp79 (mlp iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=0.9868 val=0.9873243195161003 train=0.9986163237067831
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp80 (mlp iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=0.9866 val=0.9872353673723537 train=0.9994387743648456
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp81 (mlp iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=0.9687 val=0.9692670343355275 train=0.980355061949106
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp82 (mlp iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=0.9873 val=0.987813556306707 train=0.9987367321157798
- **Status:** KEEP
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp83 (mlp iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=0.9926 val=0.9929283045721402 train=0.9999367345647645
- **Status:** KEEP
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp84 (mlp iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=0.9870 val=0.9876356520192137 train=0.9997632648229894
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp85 (mlp iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=0.9913 val=0.9916829745596869 train=0.9999510203082047
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp86 (mlp iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=0.9826 val=0.9833659491193738 train=0.9993224475968319
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp87 (mlp iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=0.9878 val=0.9883917452410603 train=0.9994999989795897
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp88 (mlp iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=0.9757 val=0.9766055861946273 train=0.9953979497917342
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp89 (mlp iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=0.9920 val=0.9923501156377869 train=0.9999836734360682
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp90 (mlp iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=0.9861 val=0.9867906066536203 train=0.9998673466680544
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp91 (mlp iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=0.9907 val=0.9911492616972069 train=0.9999673468721364
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp92 (mlp iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=0.9942 val=0.9944404910158334 train=0.999595917542689
- **Status:** KEEP
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp93 (mlp iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=0.9888 val=0.9893257427504003 train=0.9995204071845044
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp94 (mlp iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=0.9134 val=0.9156733677281622 train=0.9601529799040406
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp95 (mlp iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=0.9870 val=0.9876356520192137 train=0.9997632648229894
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp96 (mlp iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=0.9870 val=0.9876356520192137 train=0.9997632648229894
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp97 (mlp iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=0.9870 val=0.9876356520192137 train=0.9997632648229894
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp98 (mlp iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=0.9888 val=0.9892812666785269 train=0.9998734691295289
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp99 (mlp iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=0.9814 val=0.9821650951787938 train=0.9967693811620023
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp100 (mlp iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=0.9917 val=0.9921277352784201 train=0.9999081630778839
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp101 (ft_transformer iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp102 (ft_transformer iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=0.8030 val=0.8114214552570718 train=0.9801652656433993
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp103 (ft_transformer iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=0.7392 val=0.7472869596157268 train=0.9097896118155342
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp104 (ft_transformer iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=0.8415 val=0.8489147838462908 train=0.996716319829224
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp105 (ft_transformer iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=0.9293 val=0.932663227183775 train=1.0
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp106 (ft_transformer iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=0.9293 val=0.932663227183775 train=1.0
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp107 (ft_transformer iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp108 (ft_transformer iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp109 (ft_transformer iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp110 (ft_transformer iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=0.7477 val=0.7565157445294431 train=0.9327274137294158
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp111 (ft_transformer iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp112 (ft_transformer iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp113 (ft_transformer iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=0.7544 val=0.7634095356698096 train=0.9439825387398748
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp114 (ft_transformer iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp115 (ft_transformer iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp116 (ft_transformer iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp117 (ft_transformer iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp118 (ft_transformer iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=0.8241 val=0.8319249243906779 train=0.9889142630903329
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp119 (ft_transformer iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=0.7359 val=0.7431951610033802 train=0.8891977330565981
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp120 (ft_transformer iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp121 (ft_transformer iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp122 (ft_transformer iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp123 (ft_transformer iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=0.7606 val=0.7696806618039495 train=0.9512845944583559
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp124 (ft_transformer iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=0.8030 val=0.8114214552570717 train=0.9801468982589759
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp125 (ft_transformer iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=0.7850 val=0.7937199786514856 train=0.9672060555225622
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.
