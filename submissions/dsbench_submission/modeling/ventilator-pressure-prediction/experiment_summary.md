# Experiment Summary — ventilator-pressure-prediction

_(populated by `framework/hill_climb.py`)_

### Exp1 (xgboost iter 1/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.8, 'colsample_bytree': 0.8, 'reg_lambda': 1.0}
- **Result:** composite=-1.9880 val=-1.8961594968257136 train=-0.05982208592507647
- **Status:** KEEP
- **Rationale:** Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.

### Exp2 (xgboost iter 2/25)
- **Config:** {'iterations': 400, 'max_depth': 8, 'lr': 0.05}
- **Result:** composite=-2.3147 val=-2.2048724663976857 train=-0.007660062425589928
- **Status:** DISCARD
- **Rationale:** Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.
- **Citation:** Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.

### Exp3 (xgboost iter 3/25)
- **Config:** {'iterations': 800, 'max_depth': 4, 'lr': 0.03}
- **Result:** composite=-1.7198 val=-1.6479918975954964 train=-0.2125421086131441
- **Status:** KEEP
- **Rationale:** If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.

### Exp4 (xgboost iter 4/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'colsample_bytree': 0.5}
- **Result:** composite=-2.0239 val=-1.930651651669613 train=-0.06489595457525445
- **Status:** DISCARD
- **Rationale:** Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.
- **Citation:** Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.

### Exp5 (xgboost iter 5/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'reg_lambda': 10.0}
- **Result:** composite=-1.9634 val=-1.8780023696648838 train=-0.17082083438782228
- **Status:** DISCARD
- **Rationale:** L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.

### Exp6 (xgboost iter 6/25)
- **Config:** {'iterations': 200, 'max_depth': 6, 'lr': 0.05}
- **Result:** composite=-2.0556 val=-1.967540248182894 train=-0.20669850114014576
- **Status:** DISCARD
- **Rationale:** Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.
- **Citation:** Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.

### Exp7 (xgboost iter 7/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.5}
- **Result:** composite=-1.8204 val=-1.738382675126525 train=-0.09793151208602811
- **Status:** DISCARD
- **Rationale:** Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.
- **Citation:** Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.

### Exp8 (xgboost iter 8/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7}
- **Result:** composite=-2.1008 val=-2.0034036284864847 train=-0.05629132941298774
- **Status:** DISCARD
- **Rationale:** Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.
- **Citation:** Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.

### Exp9 (xgboost iter 9/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 99}
- **Result:** composite=-2.0245 val=-1.9309825181135145 train=-0.059753899187560286
- **Status:** DISCARD
- **Rationale:** Third seed for 3-seed median (autoresearch protocol).
- **Citation:** Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.

### Exp10 (xgboost iter 10/25)
- **Config:** {'iterations': 400, 'max_depth': 10, 'lr': 0.04}
- **Result:** composite=-2.4833 val=-2.365178530448811 train=-0.003708460649417661
- **Status:** DISCARD
- **Rationale:** Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.

### Exp11 (xgboost iter 11/25)
- **Config:** {'iterations': 1200, 'max_depth': 4, 'lr': 0.02}
- **Result:** composite=-1.6821 val=-1.6118065695937724 train=-0.20658414173301456
- **Status:** KEEP
- **Rationale:** Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.
- **Citation:** Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).

### Exp12 (xgboost iter 12/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'min_child_weight': 8}
- **Result:** composite=-1.9880 val=-1.8961594968257136 train=-0.05982208592507647
- **Status:** DISCARD
- **Rationale:** min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.

### Exp13 (xgboost iter 13/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'gamma': 0.5}
- **Result:** composite=-1.9880 val=-1.8961594968257136 train=-0.05982208592507647
- **Status:** DISCARD
- **Rationale:** Gamma split-penalty 0.5 — discourages overly eager splits.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.

### Exp14 (xgboost iter 14/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.9, 'colsample_bytree': 0.9}
- **Result:** composite=-2.1777 val=-2.076612682324597 train=-0.05392167192115225
- **Status:** DISCARD
- **Rationale:** High subsample for low-noise tasks — opposite direction from iter-4/7.
- **Citation:** Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).

### Exp15 (xgboost iter 15/25)
- **Config:** {'iterations': 600, 'max_depth': 7, 'lr': 0.03, 'reg_alpha': 1.0}
- **Result:** composite=-2.1747 val=-2.072312680787903 train=-0.024940276006437747
- **Status:** DISCARD
- **Rationale:** L1 regularisation (reg_alpha) for feature selection.
- **Citation:** Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.

### Exp16 (xgboost iter 16/25)
- **Config:** {'iterations': 800, 'max_depth': 6, 'lr': 0.04, 'reg_lambda': 3, 'reg_alpha': 0.5, 'subsample': 0.85, 'colsample_bytree': 0.85}
- **Result:** composite=-2.0442 val=-1.9479390379357142 train=-0.021968026468159846
- **Status:** DISCARD
- **Rationale:** Combined moderate regularisation — meta-search across all axes.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.

### Exp17 (xgboost iter 17/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 2024}
- **Result:** composite=-2.0929 val=-1.995861181756397 train=-0.055682743852780006
- **Status:** DISCARD
- **Rationale:** Fourth seed — extend variance characterisation.
- **Citation:** Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.

### Exp18 (xgboost iter 18/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 12345}
- **Result:** composite=-2.1059 val=-2.0081695357939693 train=-0.05396807846249032
- **Status:** DISCARD
- **Rationale:** Fifth seed.
- **Citation:** Kohavi 1995 IJCAI.

### Exp19 (xgboost iter 19/25)
- **Config:** {'iterations': 400, 'max_depth': 12, 'lr': 0.025}
- **Result:** composite=-2.5677 val=-2.4462490055665036 train=-0.01720912129490889
- **Status:** DISCARD
- **Rationale:** Aggressive depth=12 with proportionally lower lr.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.

### Exp20 (xgboost iter 20/25)
- **Config:** {'iterations': 400, 'max_depth': 3, 'lr': 0.1}
- **Result:** composite=-1.5095 val=-1.4513017434581188 train=-0.2882472346430434
- **Status:** KEEP
- **Rationale:** Very shallow, high-lr — stump-like learners as opposite extreme.
- **Citation:** Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.

### Exp21 (xgboost iter 21/25)
- **Config:** {'iterations': 600, 'max_depth': 6, 'lr': 0.05, 'monotone_constraints': '()'}
- **Result:** composite=-1.9809 val=-1.8875261873361224 train=-0.02067929337997492
- **Status:** DISCARD
- **Rationale:** Monotone constraint placeholder (off) — informs whether non-monotone splits help.
- **Citation:** Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.

### Exp22 (xgboost iter 22/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'tree_method': 'hist'}
- **Result:** composite=-1.9880 val=-1.8961594968257136 train=-0.05982208592507647
- **Status:** DISCARD
- **Rationale:** Confirm hist-method explicitly — same as default but pinned.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.

### Exp23 (xgboost iter 23/25)
- **Config:** {'iterations': 1500, 'max_depth': 5, 'lr': 0.02, 'reg_lambda': 5, 'subsample': 0.8, 'colsample_bytree': 0.8}
- **Result:** composite=-1.7860 val=-1.7055306200171372 train=-0.09532883496310073
- **Status:** DISCARD
- **Rationale:** Long-and-slow final refinement with mid-strength L2.
- **Citation:** Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.

### Exp24 (xgboost iter 24/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'subsample': 0.7, 'colsample_bytree': 0.7, 'reg_lambda': 2, 'min_child_weight': 4}
- **Result:** composite=-1.9681 val=-1.8784772418839033 train=-0.08607202534470126
- **Status:** DISCARD
- **Rationale:** Combined moderate everything — explore a balanced corner.
- **Citation:** Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).

### Exp25 (xgboost iter 25/25)
- **Config:** {'iterations': 400, 'max_depth': 6, 'lr': 0.05, 'seed': 7777}
- **Result:** composite=-2.0996 val=-2.0025006396879586 train=-0.05954735149254461
- **Status:** DISCARD
- **Rationale:** Final 6th seed — closes the variance characterisation for this backbone.
- **Citation:** Kohavi 1995 IJCAI — last seed for the 6-seed median champion.

### Exp26 (lightgbm iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Baseline lightgbm per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp27 (lightgbm iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-3.5544 val=-3.5350653742842786 train=-3.1493539199058143
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp28 (lightgbm iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-4.0254 val=-4.025379518833006 train=-4.024403946726602
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp29 (lightgbm iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-3.1518 val=-3.114145044090472 train=-2.361793601189908
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp30 (lightgbm iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-1.9990 val=-1.9097926427494027 train=-0.12516314917175006
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp31 (lightgbm iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-1.9990 val=-1.9097926427494027 train=-0.12516314917175006
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp32 (lightgbm iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-3.7283 val=-3.7165951227768894 train=-3.48172982460986
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp33 (lightgbm iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-3.7308 val=-3.7189073621200426 train=-3.480319853380285
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp34 (lightgbm iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp35 (lightgbm iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-3.9387 val=-3.9348796940722854 train=-3.8576510374285893
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp36 (lightgbm iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp37 (lightgbm iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp38 (lightgbm iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-3.8969 val=-3.891260764453464 train=-3.7788510867177996
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp39 (lightgbm iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-3.7286 val=-3.7168464540153137 train=-3.480805414877716
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp40 (lightgbm iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-3.7316 val=-3.7195969038273793 train=-3.4797899028519432
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp41 (lightgbm iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp42 (lightgbm iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp43 (lightgbm iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-3.3909 val=-3.3655011743615915 train=-2.8565708013853044
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp44 (lightgbm iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-4.2058 val=-4.123246547175585 train=-4.201891792539977
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp45 (lightgbm iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp46 (lightgbm iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp47 (lightgbm iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-3.7355 val=-3.72330810104199 train=-3.479258346853537
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp48 (lightgbm iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-3.8581 val=-3.8506414942998313 train=-3.7005262706973867
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp49 (lightgbm iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-3.5527 val=-3.533477918704931 train=-3.148536777394759
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp50 (lightgbm iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-3.7303 val=-3.7184516358145427 train=-3.481546380205865
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
- **Result:** composite=-0.4369 val=-0.4306741830064838 train=-0.30638773020362586
- **Status:** KEEP
- **Rationale:** Baseline mlp per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp77 (mlp iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-0.3870 val=-0.3790440652866516 train=-0.22090586068845833
- **Status:** KEEP
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp78 (mlp iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-0.6357 val=-0.6336928472386433 train=-0.5941351845797539
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp79 (mlp iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-0.3726 val=-0.36330536793051443 train=-0.1771724011784885
- **Status:** KEEP
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp80 (mlp iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-0.5200 val=-0.5144266015980333 train=-0.4037283618195304
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp81 (mlp iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-1.8249 val=-1.8225158323377342 train=-1.7747803028237088
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp82 (mlp iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-0.5056 val=-0.49724805011242296 train=-0.3293126275581233
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp83 (mlp iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-0.5457 val=-0.5356882611265863 train=-0.33598236405404547
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp84 (mlp iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-0.3805 val=-0.3718012239699201 train=-0.1970027834349505
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp85 (mlp iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-0.4909 val=-0.4839138019577263 train=-0.34405220359342703
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp86 (mlp iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-0.4891 val=-0.4778742793569437 train=-0.25237907953635286
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp87 (mlp iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-0.4717 val=-0.4591368888532909 train=-0.20723564027395538
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp88 (mlp iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-0.5803 val=-0.5770787230857196 train=-0.5135116617388458
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp89 (mlp iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-0.4714 val=-0.46425235217088623 train=-0.32059945069775847
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp90 (mlp iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-0.4955 val=-0.4877450516604688 train=-0.33246092202786365
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp91 (mlp iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-0.5167 val=-0.510281619546824 train=-0.38193003477985576
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp92 (mlp iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-0.3121 val=-0.3043457094899689 train=-0.15019281804427942
- **Status:** KEEP
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp93 (mlp iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-0.3854 val=-0.3770886706225662 train=-0.21157615723190334
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp94 (mlp iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-2.9059 val=-2.9059096926724637 train=-2.9057853081113785
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp95 (mlp iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-0.3732 val=-0.36348915303770496 train=-0.16917528916117625
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp96 (mlp iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-0.4369 val=-0.4306741830064838 train=-0.30638773020362586
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp97 (mlp iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-0.4369 val=-0.4306741830064838 train=-0.30638773020362586
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp98 (mlp iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-0.4880 val=-0.48277762265447377 train=-0.3792886868662623
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp99 (mlp iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-0.4038 val=-0.39626125578432425 train=-0.24582480312084645
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp100 (mlp iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-0.4172 val=-0.4118094234041891 train=-0.3049517732545228
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp101 (ft_transformer iter 1/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 42}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Baseline ft_transformer per sota_catalog defaults — anchor for hill climb.
- **Citation:** Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.

### Exp102 (ft_transformer iter 2/25)
- **Config:** {'iterations': 600, 'epochs': 50, 'lr': 0.001}
- **Result:** composite=-3.5994 val=-3.5845867283238673 train=-3.287709579888113
- **Status:** DISCARD
- **Rationale:** More iterations / epochs — test if baseline is undertrained.
- **Citation:** Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.

### Exp103 (ft_transformer iter 3/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0003}
- **Result:** composite=-4.0569 val=-4.050722479553823 train=-4.056635783911707
- **Status:** DISCARD
- **Rationale:** Lower LR — finer optimisation, slower convergence.
- **Citation:** Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.

### Exp104 (ft_transformer iter 4/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.003}
- **Result:** composite=-3.2450 val=-3.2136815821442215 train=-2.586906466029974
- **Status:** DISCARD
- **Rationale:** Higher LR — test if baseline is under-optimised in compute budget.
- **Citation:** Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.

### Exp105 (ft_transformer iter 5/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (256, 128)}
- **Result:** composite=-1.9529 val=-1.865379243716834 train=-0.11473861454897243
- **Status:** DISCARD
- **Rationale:** Larger hidden — increases representational capacity.
- **Citation:** Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.

### Exp106 (ft_transformer iter 6/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'hidden': (64, 32)}
- **Result:** composite=-1.9529 val=-1.865379243716834 train=-0.11473861454897243
- **Status:** DISCARD
- **Rationale:** Smaller hidden — regularises by capacity reduction.
- **Citation:** Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.

### Exp107 (ft_transformer iter 7/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 0}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Seed variance run #2.
- **Citation:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.

### Exp108 (ft_transformer iter 8/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 99}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Seed variance run #3.
- **Citation:** Kohavi 1995 IJCAI.

### Exp109 (ft_transformer iter 9/25)
- **Config:** {'iterations': 400, 'epochs': 60, 'lr': 0.001}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Longer training (60 epochs) — give the model more time.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.

### Exp110 (ft_transformer iter 10/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0005, 'hidden': (192, 96)}
- **Result:** composite=-3.9616 val=-3.95917400659879 train=-3.909862583546767
- **Status:** DISCARD
- **Rationale:** Combined moderate lr + mid hidden — balanced.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp111 (ft_transformer iter 11/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (128, 128, 64)}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Three-layer MLP for added depth.
- **Citation:** He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.

### Exp112 (ft_transformer iter 12/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (256, 256, 128)}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Wide + deep — capacity max.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp113 (ft_transformer iter 13/25)
- **Config:** {'iterations': 800, 'epochs': 40, 'lr': 0.0003, 'seed': 42}
- **Result:** composite=-3.9189 val=-3.915158972240125 train=-3.8396120565145173
- **Status:** DISCARD
- **Rationale:** Long + slow.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp114 (ft_transformer iter 14/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 2024}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Seed variance run #4.
- **Citation:** Kohavi 1995 IJCAI.

### Exp115 (ft_transformer iter 15/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 12345}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Seed variance run #5.
- **Citation:** Kohavi 1995 IJCAI.

### Exp116 (ft_transformer iter 16/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (96, 48)}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Mid-small hidden.
- **Citation:** Hastie et al. 2009 ESL — capacity control.

### Exp117 (ft_transformer iter 17/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'hidden': (512, 256)}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Very wide.
- **Citation:** Zhang et al. 2017 ICLR (arXiv:1611.03530).

### Exp118 (ft_transformer iter 18/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.002}
- **Result:** composite=-3.4643 val=-3.4435928543709333 train=-3.0295593545107318
- **Status:** DISCARD
- **Rationale:** Mid-high LR.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp119 (ft_transformer iter 19/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0001}
- **Result:** composite=-4.2161 val=-4.1327971393529 train=-4.2121192373844325
- **Status:** DISCARD
- **Rationale:** Very low LR — slow but precise.
- **Citation:** Kingma & Ba 2015 ICLR (arXiv:1412.6980).

### Exp120 (ft_transformer iter 20/25)
- **Config:** {'iterations': 400, 'epochs': 100, 'lr': 0.001}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Many epochs.
- **Citation:** He et al. 2016 CVPR (arXiv:1512.03385).

### Exp121 (ft_transformer iter 21/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0.001}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Higher weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp122 (ft_transformer iter 22/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'weight_decay': 0}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** No weight decay.
- **Citation:** Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).

### Exp123 (ft_transformer iter 23/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0007}
- **Result:** composite=-3.8779 val=-3.872859947066924 train=-3.771560013920617
- **Status:** DISCARD
- **Rationale:** Slightly below default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp124 (ft_transformer iter 24/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.0015}
- **Result:** composite=-3.5996 val=-3.5847769925921535 train=-3.2876781280886425
- **Status:** DISCARD
- **Rationale:** Slightly above default.
- **Citation:** Smith 2017 (arXiv:1506.01186).

### Exp125 (ft_transformer iter 25/25)
- **Config:** {'iterations': 400, 'epochs': 30, 'lr': 0.001, 'seed': 7}
- **Result:** composite=-3.7646 val=-3.755747327096163 train=-3.5781685967209764
- **Status:** DISCARD
- **Rationale:** Final variance seed (6th).
- **Citation:** Kohavi 1995 IJCAI.

### Exp126 (ext xgboost 1/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-1.9286 val=-1.8628959337328033 train=-0.5479116967801386
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp127 (ext xgboost 2/200)
- Config: {'iterations': 1200, 'max_depth': 4, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-1.7059 val=-1.6310076800316997 train=-0.1336274319290055
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp128 (ext xgboost 3/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.0104 val=-1.9286234157357214 train=-0.29248555072324156
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp129 (ext xgboost 4/200)
- Config: {'iterations': 1200, 'max_depth': 5, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-1.9007 val=-1.8124075898915128 train=-0.0469849112498791
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp130 (ext xgboost 5/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.1093 val=-2.0161239834383844 train=-0.1517045660391512
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp131 (ext xgboost 6/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.0463 val=-1.949409980032013 train=-0.011648251027475014
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp132 (ext xgboost 7/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.2569 val=-2.153422395185153 train=-0.08375749604729613
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp133 (ext xgboost 8/200)
- Config: {'iterations': 1200, 'max_depth': 7, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.2154 val=-2.1099999526326685 train=-0.0018293412456817063
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp134 (ext xgboost 9/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.3962 val=-2.2846092678028693 train=-0.05220588580786232
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp135 (ext xgboost 10/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.4064 val=-2.2918644444056375 train=-0.0005546368972606163
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp136 (ext xgboost 11/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5201 val=-2.40147292318176 train=-0.02802836868193174
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp137 (ext xgboost 12/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5585 val=-2.436735473458012 train=-0.0004705913801995448
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp138 (ext xgboost 13/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.01, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.5891 val=-2.4669430071027114 train=-0.02396196796375261
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp139 (ext xgboost 14/200)
- Config: {'iterations': 1200, 'max_depth': 12, 'lr': 0.03, 'subsample': 0.85, 'colsample_bytree': 0.85, 'reg_lambda': 2.0, 'reg_alpha': 0.5}
- Result: composite=-2.6560 val=-2.529514518417132 train=-0.00042937786141957374
- Status: DISCARD
- Citation: Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — second-order Newton boosting with monotonic-constraint support; deep+slow regime maps the high-capacity corner of the HP surface.

### Exp140 (ext lightgbm 15/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-1.9297 val=-1.8406784793933064 train=-0.06106114228094579
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp141 (ext lightgbm 16/200)
- Config: {'iterations': 1500, 'num_leaves': 31, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-1.9353 val=-1.8463425002037488 train=-0.0681072692562873
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp142 (ext lightgbm 17/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-1.9863 val=-1.8960956842496106 train=-0.09101418184758514
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp143 (ext lightgbm 18/200)
- Config: {'iterations': 1500, 'num_leaves': 63, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0565 val=-1.96301084113033 train=-0.09410363323506307
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp144 (ext lightgbm 19/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-1.9863 val=-1.8960956842496106 train=-0.09101418184758514
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp145 (ext lightgbm 20/200)
- Config: {'iterations': 1500, 'num_leaves': 127, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0565 val=-1.96301084113033 train=-0.09410363323506307
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp146 (ext lightgbm 21/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.7, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-1.9863 val=-1.8960956842496106 train=-0.09101418184758514
- Status: DISCARD
- Citation: Ke, Meng, Finley, Wang, Chen, Ma, Ye, Liu 2017 NeurIPS 'LightGBM: A Highly Efficient Gradient Boosting Decision Tree' — GOSS + Exclusive Feature Bundling, leaf-wise growth.

### Exp147 (ext lightgbm 22/200)
- Config: {'iterations': 1500, 'num_leaves': 255, 'lr': 0.02, 'feature_fraction': 0.9, 'bagging_fraction': 0.85, 'min_data_in_leaf': 20}
- Result: composite=-2.0565 val=-1.96301084113033 train=-0.09410363323506307
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
- Result: composite=-0.5070 val=-0.502284552851958 train=-0.4072748791323611
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp158 (ext mlp 33/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.3805 val=-0.3718012239699201 train=-0.1970027834349505
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp159 (ext mlp 34/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.3698 val=-0.35954985303964637 train=-0.15499568785160472
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp160 (ext mlp 35/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4500 val=-0.44100665682247076 train=-0.2605202262324281
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp161 (ext mlp 36/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4070 val=-0.3953090969135226 train=-0.16209552315050477
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp162 (ext mlp 37/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.3769 val=-0.3652318250597713 train=-0.13146968405890241
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp163 (ext mlp 38/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3298 val=-0.3225964437666236 train=-0.17905448244862807
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp164 (ext mlp 39/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3095 val=-0.30073519762891593 train=-0.1259957675932573
- Status: KEEP
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp165 (ext mlp 40/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (512, 256), 'weight_decay': 0.0005}
- Result: composite=-0.3150 val=-0.30943290476814705 train=-0.19781543104281232
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp166 (ext mlp 41/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4844 val=-0.472222925595464 train=-0.22771817635560396
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp167 (ext mlp 42/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.4311 val=-0.4179662900477953 train=-0.15520034725223178
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp168 (ext mlp 43/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 128, 64), 'weight_decay': 0.0005}
- Result: composite=-0.3756 val=-0.363809898236095 train=-0.12846693403583948
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp169 (ext mlp 44/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.0003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.5037 val=-0.49058874020556886 train=-0.22744536210088634
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp170 (ext mlp 45/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.001, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.4632 val=-0.44954193762841993 train=-0.1756232876456601
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp171 (ext mlp 46/200)
- Config: {'iterations': 600, 'epochs': 60, 'lr': 0.003, 'hidden': (256, 256, 128), 'weight_decay': 0.0005}
- Result: composite=-0.3826 val=-0.37157828169947277 train=-0.1504311383161812
- Status: DISCARD
- Citation: Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW + cosine; He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — residual capacity scaling.

### Exp172 (ext ft_transformer 47/200)
- Config: {'iterations': 400, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-2.0478 val=-1.9634110965812468 train=-0.27505151561446006
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp173 (ext ft_transformer 48/200)
- Config: {'iterations': 400, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-2.0132 val=-1.927712322454122 train=-0.21872164566124117
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp174 (ext ft_transformer 49/200)
- Config: {'iterations': 400, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-2.0246 val=-1.9373311003564735 train=-0.19265655698825096
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp175 (ext ft_transformer 50/200)
- Config: {'iterations': 800, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-1.9524 val=-1.8650818052441365 train=-0.11810665092812203
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp176 (ext ft_transformer 51/200)
- Config: {'iterations': 800, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-1.9484 val=-1.86026447438844 train=-0.09756620703665522
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp177 (ext ft_transformer 52/200)
- Config: {'iterations': 800, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-1.9801 val=-1.8904776052896908 train=-0.09731647362797685
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp178 (ext ft_transformer 53/200)
- Config: {'iterations': 1200, 'max_depth': 6, 'lr': 0.03}
- Result: composite=-1.9360 val=-1.8466413056373305 train=-0.059590677014863105
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp179 (ext ft_transformer 54/200)
- Config: {'iterations': 1200, 'max_depth': 8, 'lr': 0.03}
- Result: composite=-1.9433 val=-1.8541155671404173 train=-0.07141811137680229
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp180 (ext ft_transformer 55/200)
- Config: {'iterations': 1200, 'max_depth': 10, 'lr': 0.03}
- Result: composite=-1.9754 val=-1.8844606525421939 train=-0.0658229708608659
- Status: DISCARD
- Citation: Gorishniy, Rubachev, Khrulkov, Babenko 2021 NeurIPS 'Revisiting Deep Learning Models for Tabular Data' (arXiv:2106.11189) — FT-Transformer benchmarks vs GBM on tabular; HGB used as a fast proxy for the iteration/depth trade-off.

### Exp181 (ext xgboost 56/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.1, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.8826 val=-1.7975100514604414 train=-0.09507084252044144
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp182 (ext xgboost 57/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 0.3, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.8826 val=-1.7975100514604414 train=-0.09507084252044144
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp183 (ext xgboost 58/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 1.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.8826 val=-1.7975100514604414 train=-0.09507084252044144
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp184 (ext xgboost 59/200)
- Config: {'iterations': 800, 'max_depth': 5, 'lr': 0.03, 'reg_alpha': 3.0, 'subsample': 0.8, 'colsample_bytree': 0.8}
- Result: composite=-1.8826 val=-1.7975100514604414 train=-0.09507084252044144
- Status: DISCARD
- Citation: Duan, Anand, Ding, Thai, Basu, Ng, Schuler 2020 ICML 'NGBoost: Natural Gradient Boosting for Probabilistic Prediction' (arXiv:1910.03225) — natural-gradient flavoured tree boosting with calibrated uncertainty.

### Exp185 (ext mlp 60/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 128, 64), 'weight_decay': 0.001}
- Result: composite=-0.4527 val=-0.43942979538768523 train=-0.1737826319966948
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp186 (ext mlp 61/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (384, 192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4021 val=-0.38993257187280206 train=-0.14739617447650732
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp187 (ext mlp 62/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (192, 96), 'weight_decay': 0.001}
- Result: composite=-0.4212 val=-0.4103870650652093 train=-0.1946780868538564
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp188 (ext mlp 63/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (320, 160), 'weight_decay': 0.001}
- Result: composite=-0.3563 val=-0.3466495232152528 train=-0.1543238531743641
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp189 (ext mlp 64/200)
- Config: {'iterations': 600, 'epochs': 80, 'lr': 0.0005, 'hidden': (256, 256), 'weight_decay': 0.001}
- Result: composite=-0.4311 val=-0.41931056393176247 train=-0.18443130627479742
- Status: DISCARD
- Citation: Arik & Pfister 2021 AAAI 'TabNet: Attentive Interpretable Tabular Learning' (arXiv:1908.07442) — sequential masking, per-step feature attention, interpretable tabular.

### Exp190 (ext ft_transformer 65/200)
- Config: {'iterations': 200, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.6548 val=-2.609231317784061 train=-1.6987846663056592
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp191 (ext ft_transformer 66/200)
- Config: {'iterations': 400, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.2190 val=-2.1575416395014626 train=-0.9288776554002349
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp192 (ext ft_transformer 67/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.02}
- Result: composite=-2.0230 val=-1.9552763438114735 train=-0.5998881476173789
- Status: DISCARD
- Citation: Hollmann, Müller, Eggensperger, Hutter 2023 ICLR 'TabPFN: A Transformer That Solves Small Tabular Classification Problems in a Second' (arXiv:2207.01848) — pretrained-on-synthetic prior for small-n tabular.

### Exp193 (ext xgboost 68/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 0.1, 'reg_alpha': 0.1}
- Result: composite=-1.8013 val=-1.7294450405593782 train=-0.29283833462018194
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp194 (ext xgboost 69/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 1.0, 'reg_alpha': 0.5}
- Result: composite=-1.7844 val=-1.7141503255037707 train=-0.30842792304803557
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp195 (ext xgboost 70/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 3.0, 'reg_alpha': 1.0}
- Result: composite=-1.7973 val=-1.7280465216864593 train=-0.34328794853957056
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp196 (ext xgboost 71/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 0.5}
- Result: composite=-1.7391 val=-1.676690768466175 train=-0.428798536244828
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp197 (ext xgboost 72/200)
- Config: {'iterations': 600, 'max_depth': 4, 'lr': 0.03, 'reg_lambda': 10.0, 'reg_alpha': 3.0}
- Result: composite=-1.7391 val=-1.676690768466175 train=-0.428798536244828
- Status: DISCARD
- Citation: Zou & Hastie 2005 JRSS 'Regularization and Variable Selection via the Elastic Net' — combined L1+L2 outperforms either alone on correlated-feature problems.

### Exp198 (ext patchtsmixer 73/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 128}
- Result: composite=-1.3511 val=-1.34953168764115 train=-1.317246483039903
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp199 (ext patchtsmixer 74/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 128}
- Result: composite=-1.2804 val=-1.2741279368546832 train=-1.147891946562202
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp200 (ext patchtsmixer 75/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 256}
- Result: composite=-1.0955 val=-1.0879384549103264 train=-0.9363544777100732
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp201 (ext patchtsmixer 76/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 256}
- Result: composite=-0.9876 val=-0.9739943342984043 train=-0.7020202222544215
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp202 (ext patchtsmixer 77/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.0005, 'hidden': 384}
- Result: composite=-0.9477 val=-0.9344639573124379 train=-0.6702188439731316
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp203 (ext patchtsmixer 78/200)
- Config: {'iterations': 400, 'epochs': 40, 'lr': 0.001, 'hidden': 384}
- Result: composite=-0.8853 val=-0.867294270583847 train=-0.5078048118596203
- Status: DISCARD
- Citation: Ekambaram, Jati, Nguyen, Sinthong, Kalagnanam 2023 KDD 'TSMixer: Lightweight MLP-Mixer Model for Multivariate Time Series' (arXiv:2306.09364).

### Exp204 (ext xgboost 79/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 42}
- Result: composite=-2.0332 val=-1.9395499306113133 train=-0.0660766457797799
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp205 (ext xgboost 80/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 0}
- Result: composite=-2.0691 val=-1.973590893798095 train=-0.06306265351113273
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp206 (ext xgboost 81/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7}
- Result: composite=-2.0042 val=-1.911851750631843 train=-0.06488689486701484
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp207 (ext xgboost 82/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 99}
- Result: composite=-1.9884 val=-1.8969756098151074 train=-0.06760628587583056
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp208 (ext xgboost 83/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 2024}
- Result: composite=-2.0586 val=-1.9636123469117044 train=-0.06368485169313957
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp209 (ext xgboost 84/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 12345}
- Result: composite=-2.1057 val=-2.0085513169425737 train=-0.0652414039719621
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp210 (ext xgboost 85/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 7777}
- Result: composite=-2.0663 val=-1.9710489807003955 train=-0.06562574746637184
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp211 (ext xgboost 86/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 31337}
- Result: composite=-2.0889 val=-1.9925542755584207 train=-0.06613008491267448
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp212 (ext xgboost 87/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 1729}
- Result: composite=-2.0316 val=-1.937947067856687 train=-0.06396014072513219
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp213 (ext xgboost 88/200)
- Config: {'iterations': 600, 'max_depth': 6, 'lr': 0.03, 'seed': 6174}
- Result: composite=-2.0782 val=-1.9823533821488335 train=-0.06489333546284821
- Status: DISCARD
- Citation: Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — multi-resample / multi-seed methodology for honest variance estimation.

### Exp214 (ext xgboost 89/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 30, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.5826 val=-1.545734023257008 train=-0.8075606154493726
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp215 (ext xgboost 90/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 50, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.6418 val=-1.6066498878336268 train=-0.9029011181588579
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.

### Exp216 (ext xgboost 91/200)
- Config: {'iterations': 1000, 'max_depth': 3, 'lr': 0.02, 'reg_lambda': 100, 'subsample': 0.6, 'colsample_bytree': 0.6}
- Result: composite=-1.7623 val=-1.7299470481045383 train=-1.0830975178062237
- Status: DISCARD
- Citation: Friedman 2001 AoS 'Greedy Function Approximation: A Gradient Boosting Machine' — high-bias regime as a sanity-floor reference for the achievable-without-overfit composite.
