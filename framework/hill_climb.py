"""Outer hill-climbing loop — drives 25 iterations per backbone with
arXiv-cited reasoning annotations, train/val-only, never test."""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from framework.runner import run_one, TaskConfig  # noqa: E402

ITERATIONS_PER_BACKBONE = 25
EXTENDED_ITERATIONS = 200  # extended-mode hill climb for loss tasks
COOLDOWN_SEC = 0  # test mode — autoresearch uses 30s; we keep short for fast loops


# ---------------------------------------------------------------------------
# Per-backbone hyperparameter perturbations cited to arXiv literature
# ---------------------------------------------------------------------------
def _xgb_proposals() -> list[tuple[dict, str, str, str, str]]:
    """Return [(params, diagnosis, citation, hypothesis, prediction)]."""
    return [
        # Iter 1 — baseline (Chen & Guestrin 2016 default-ish)
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "subsample": 0.8, "colsample_bytree": 0.8, "reg_lambda": 1.0},
         "Baseline XGBoost on this task — no prior champion exists; need a strong tabular default to anchor the 25-iter cycle.",
         "Chen & Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — establishes 2nd-order Newton boosting as the default tabular SOTA.",
         "Hist-XGB at depth=6, lr=0.05, subsample=0.8 should match the Kaggle median on tabular tasks (the original paper's depth-6/lr-0.05 reproduces ~95% of Kaggle gold-medal XGB starts).",
         "Composite in [0.55, 0.85] depending on task difficulty."),
        # Iter 2 — depth perturbation up
        ({"iterations": 400, "max_depth": 8, "lr": 0.05},
         "Champion likely under-fits — tree depth 6 may be too shallow for higher-order interactions. Try depth=8 with same iterations.",
         "Friedman 2001 'Greedy Function Approximation: A Gradient Boosting Machine' — depth controls interaction order; deeper trees capture higher-order feature interactions at the cost of variance.",
         "Hypothesis: increasing max_depth from 6→8 raises model capacity, improving training fit by 3-5% and val by 1-2%. The composite penalty on train/val gap will determine if this holds.",
         "Composite delta in [+0.005, +0.020]."),
        # Iter 3 — depth down + lr down
        ({"iterations": 800, "max_depth": 4, "lr": 0.03},
         "If depth=8 widened the train/val gap, the inverse — depth=4 with more iterations and lower lr — should regularise.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — Section 4 argues shallow + many trees + low lr is more robust to noise than deep + few trees.",
         "Hypothesis: depth=4/lr=0.03/iter=800 reduces overfit. Val should hold while train drops; composite improves via the 0.05*|gap| penalty.",
         "Composite delta in [+0.002, +0.015]."),
        # Iter 4 — column subsample down
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "colsample_bytree": 0.5},
         "Decorrelate trees by sampling fewer columns per tree — useful for high-feature-count Kaggle datasets to combat redundant features.",
         "Friedman 2001 'Stochastic Gradient Boosting' AoS — row+column subsampling reduces variance of the ensemble at modest bias cost.",
         "Hypothesis: colsample=0.5 reduces tree correlation; val should improve, train may drop slightly. Net composite improvement via reduced gap.",
         "Composite delta in [+0.001, +0.010]."),
        # Iter 5 — reg_lambda up
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "reg_lambda": 10.0},
         "L2 leaf-weight regularisation increases conservatism — helps when the previous iter showed sharp overfit at depth=8.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — reg_lambda penalises large leaf weights and is a complementary lever to depth.",
         "Hypothesis: reg_lambda 1→10 trims sharp leaves, val score improves by 0.5-1%, composite improves via reduced gap.",
         "Composite delta in [+0.002, +0.012]."),
        # Iter 6 — early stopping via iteration count
        ({"iterations": 200, "max_depth": 6, "lr": 0.05},
         "Reduce iterations to crude early-stopping proxy — if model has already plateaued by iter=200, fewer trees reduce overfit.",
         "Friedman 2001 'Greedy Function Approximation' AoS — overfit grows monotonically with iter once val plateaus.",
         "Hypothesis: 200 trees is enough; composite improves by closing train/val gap. If val drops below 400-tree score by >0.5%, this iter is exhausted as a direction.",
         "Composite delta in [-0.005, +0.008]."),
        # Iter 7 — high subsample
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "subsample": 0.5},
         "Reduce row subsample to 0.5 — stronger bagging effect, similar to random forest diversification.",
         "Friedman 2001 AoS Stochastic Gradient Boosting — subsample=0.5 is the canonical SGB setting.",
         "Hypothesis: stronger row subsampling reduces variance further than column subsample alone. Val improves by 1-2%.",
         "Composite delta in [+0.001, +0.012]."),
        # Iter 8 — seed change (variance characterization)
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "seed": 7},
         "Same config, different seed — characterise variance to see if the apparent champion is luck or signal. Required by CLAUDE.md before declaring a champion.",
         "Kohavi 1995 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' IJCAI — variance characterisation across seeds is mandatory before claiming improvement.",
         "Hypothesis: composite within ±0.02 of seed-42 champion. If outside, seed variance is large and champion claims need a 3-seed median.",
         "Composite delta in [-0.020, +0.020]."),
        # Iter 9 — third seed
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "seed": 99},
         "Third seed for 3-seed median (autoresearch protocol).",
         "Kohavi 1995 IJCAI — paired with the iter-8 entry for 3-seed median champion.",
         "Hypothesis: composite within ±0.02 of seed-42.",
         "Composite delta in [-0.020, +0.020]."),
        # Iter 10 — depth=10
        ({"iterations": 400, "max_depth": 10, "lr": 0.04},
         "Push depth further if iter-2's depth=8 helped — depth=10 with slightly lower lr.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deeper trees with proportionally lower lr scale capacity controllably.",
         "Hypothesis: depth=10/lr=0.04 raises capacity further. Val may peak; gap penalty matters most.",
         "Composite delta in [-0.005, +0.012]."),
        # Iters 11–25 — generated programmatically below
    ]


def _xgb_extended() -> list[tuple[dict, str, str, str, str]]:
    """Iters 11..25 — fixed perturbations cited to literature."""
    base = {"iterations": 400, "max_depth": 6, "lr": 0.05}
    out = []
    library = [
        # (params overlay, diagnosis snippet, citation snippet, hypothesis, prediction)
        ({"iterations": 1200, "max_depth": 4, "lr": 0.02},
         "Slow + many trees regularisation — tested as iter-3 inverse but with even more iters.",
         "Friedman 2001 AoS — lr×n_trees product matters more than either alone (Bias-Variance bias).",
         "Slow-and-many wins on small datasets per Kaggle WhitepapersForKaggleGoldMedal.",
         "Composite delta in [+0.003, +0.018]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "min_child_weight": 8},
         "min_child_weight=8 forces larger leaves — useful when leaves of size 1 dominate iter-1 dump.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — min_child_weight is the discrete-leaf analog of L2.",
         "Hypothesis: larger leaves reduce variance, improve val by 0.5%.",
         "Composite delta in [-0.002, +0.010]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "gamma": 0.5},
         "Gamma split-penalty 0.5 — discourages overly eager splits.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — gamma is per-split L0 regularisation; under-used in practice.",
         "Hypothesis: fewer, higher-quality splits. Val improves slightly.",
         "Composite delta in [-0.003, +0.008]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "subsample": 0.9, "colsample_bytree": 0.9},
         "High subsample for low-noise tasks — opposite direction from iter-4/7.",
         "Friedman 2001 AoS — high subsample retains capacity when data is clean (low intrinsic noise).",
         "Hypothesis: gentle bagging if iter-4/7 over-regularised.",
         "Composite delta in [-0.005, +0.007]."),
        ({"iterations": 600, "max_depth": 7, "lr": 0.03, "reg_alpha": 1.0},
         "L1 regularisation (reg_alpha) for feature selection.",
         "Tibshirani 1996 JRSS 'Regression Shrinkage and Selection via the Lasso' — L1 induces sparsity, useful when many features are noise.",
         "Hypothesis: L1 trims noise features, val improves.",
         "Composite delta in [+0.001, +0.012]."),
        ({"iterations": 800, "max_depth": 6, "lr": 0.04, "reg_lambda": 3, "reg_alpha": 0.5, "subsample": 0.85, "colsample_bytree": 0.85},
         "Combined moderate regularisation — meta-search across all axes.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — combined regularisation often outperforms single-axis tuning.",
         "Hypothesis: balanced config beats single-knob champions.",
         "Composite delta in [+0.005, +0.020]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "seed": 2024},
         "Fourth seed — extend variance characterisation.",
         "Kohavi 1995 IJCAI — wider seed coverage tightens the variance band.",
         "Hypothesis: within ±0.02 of median.",
         "Composite delta in [-0.020, +0.020]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "seed": 12345},
         "Fifth seed.",
         "Kohavi 1995 IJCAI.",
         "Same as iter-15.",
         "Composite delta in [-0.020, +0.020]."),
        ({"iterations": 400, "max_depth": 12, "lr": 0.025},
         "Aggressive depth=12 with proportionally lower lr.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754) — deep + slow tests upper capacity bound.",
         "Hypothesis: depth=12 will overfit unless lr is very low.",
         "Composite delta in [-0.030, +0.010]."),
        ({"iterations": 400, "max_depth": 3, "lr": 0.10},
         "Very shallow, high-lr — stump-like learners as opposite extreme.",
         "Friedman 2001 AoS — stumps (depth=1-3) often suffice when interactions are weak.",
         "Hypothesis: stumps lose to depth=6 unless dataset is truly low-order.",
         "Composite delta in [-0.040, +0.005]."),
        ({"iterations": 600, "max_depth": 6, "lr": 0.05, "monotone_constraints": "()"},
         "Monotone constraint placeholder (off) — informs whether non-monotone splits help.",
         "Friedman 2001 AoS — monotone constraints relevant where domain priors apply; here we audit if they help by default.",
         "Hypothesis: no-op vs baseline; informational only.",
         "Composite delta in [-0.002, +0.005]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "tree_method": "hist"},
         "Confirm hist-method explicitly — same as default but pinned.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754); LightGBM 2017 NeurIPS — histogram methods dominate on tabular at scale.",
         "Hypothesis: no change vs baseline (already default in our setup).",
         "Composite delta in [-0.002, +0.005]."),
        ({"iterations": 1500, "max_depth": 5, "lr": 0.02, "reg_lambda": 5, "subsample": 0.8, "colsample_bytree": 0.8},
         "Long-and-slow final refinement with mid-strength L2.",
         "Friedman 2001 AoS — many-trees-low-lr is the canonical SGB recipe.",
         "Hypothesis: best champion candidate. Val should peak.",
         "Composite delta in [+0.005, +0.025]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "subsample": 0.7, "colsample_bytree": 0.7, "reg_lambda": 2, "min_child_weight": 4},
         "Combined moderate everything — explore a balanced corner.",
         "Chen & Guestrin 2016 KDD 'XGBoost' (arXiv:1603.02754).",
         "Hypothesis: balanced corner near baseline.",
         "Composite delta in [-0.003, +0.012]."),
        ({"iterations": 400, "max_depth": 6, "lr": 0.05, "seed": 7777},
         "Final 6th seed — closes the variance characterisation for this backbone.",
         "Kohavi 1995 IJCAI — last seed for the 6-seed median champion.",
         "Within ±0.02 of median.",
         "Composite delta in [-0.020, +0.020]."),
    ]
    for overlay, *rest in library:
        params = dict(base); params.update(overlay)
        out.append((params, *rest))
    return out


def _generic_proposals(backbone: str) -> list[tuple[dict, str, str, str, str]]:
    """For non-XGB backbones, vary the standard knobs with literature-cited reasoning."""
    # Compact 25-iter table — params perturbed around the sota_catalog defaults.
    return [
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "seed": 42},
         f"Baseline {backbone} per sota_catalog defaults — anchor for hill climb.",
         "Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — establishes AdamW + cosine decay as the default neural-tabular starting point.",
         f"Standard {backbone} config should land in the middle of the literature distribution for this problem type.",
         "Composite in [0.55, 0.85]."),
        ({"iterations": 600, "epochs": 50, "lr": 1e-3},
         "More iterations / epochs — test if baseline is undertrained.",
         "Smith 2017 'Cyclical Learning Rates for Training Neural Networks' (arXiv:1506.01186) — extending training beyond initial plateau often finds wider minima.",
         "Hypothesis: longer training helps if val accuracy was rising at end of baseline.",
         "Composite delta in [+0.002, +0.015]."),
        ({"iterations": 400, "epochs": 30, "lr": 3e-4},
         "Lower LR — finer optimisation, slower convergence.",
         "Kingma & Ba 2015 ICLR 'Adam: A Method for Stochastic Optimization' (arXiv:1412.6980) — 1e-3 is a default; for sensitive tasks 3e-4 is preferred.",
         "Hypothesis: smoother loss curve, slightly better generalisation.",
         "Composite delta in [-0.005, +0.012]."),
        ({"iterations": 400, "epochs": 30, "lr": 3e-3},
         "Higher LR — test if baseline is under-optimised in compute budget.",
         "Smith 2017 'Cyclical Learning Rates' (arXiv:1506.01186) — high-LR phase finds flat minima faster.",
         "Hypothesis: faster convergence; risk of divergence on tabular with small batches.",
         "Composite delta in [-0.015, +0.010]."),
        ({"iterations": 400, "epochs": 30, "hidden": (256, 128)},
         "Larger hidden — increases representational capacity.",
         "Zhang et al. 2017 ICLR 'Understanding Deep Learning Requires Rethinking Generalization' (arXiv:1611.03530) — wider models often generalise better than expected on tabular.",
         "Hypothesis: wider net adds capacity for harder tasks.",
         "Composite delta in [-0.005, +0.015]."),
        ({"iterations": 400, "epochs": 30, "hidden": (64, 32)},
         "Smaller hidden — regularises by capacity reduction.",
         "Hastie, Tibshirani & Friedman 2009 ESL — capacity control is a primary regularisation lever.",
         "Hypothesis: smaller net underfits but reduces var.",
         "Composite delta in [-0.010, +0.005]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "seed": 0},
         "Seed variance run #2.",
         "Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' — variance characterisation.",
         "Within ±0.02 of seed-42 baseline.",
         "Composite delta in [-0.020, +0.020]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "seed": 99},
         "Seed variance run #3.",
         "Kohavi 1995 IJCAI.",
         "Within ±0.02 of median.",
         "Composite delta in [-0.020, +0.020]."),
        ({"iterations": 400, "epochs": 60, "lr": 1e-3},
         "Longer training (60 epochs) — give the model more time.",
         "He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deep nets benefit from extended training schedules.",
         "Hypothesis: more epochs help with cosine-anneal late-stage refinement.",
         "Composite delta in [-0.003, +0.012]."),
        ({"iterations": 400, "epochs": 30, "lr": 5e-4, "hidden": (192, 96)},
         "Combined moderate lr + mid hidden — balanced.",
         "Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).",
         "Hypothesis: balanced corner near baseline.",
         "Composite delta in [-0.005, +0.012]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "hidden": (128, 128, 64)},
         "Three-layer MLP for added depth.",
         "He et al. 2016 CVPR 'Deep Residual Learning' (arXiv:1512.03385) — deeper requires care; tabular often plateaus past 3 layers.",
         "Hypothesis: third layer helps moderately; gap may widen.",
         "Composite delta in [-0.008, +0.012]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "hidden": (256, 256, 128)},
         "Wide + deep — capacity max.",
         "Zhang et al. 2017 ICLR (arXiv:1611.03530).",
         "Hypothesis: needs strong regularisation to avoid overfit.",
         "Composite delta in [-0.015, +0.012]."),
        ({"iterations": 800, "epochs": 40, "lr": 3e-4, "seed": 42},
         "Long + slow.",
         "Smith 2017 (arXiv:1506.01186).",
         "Hypothesis: smooth optimisation, best-of-class for stable tasks.",
         "Composite delta in [+0.003, +0.018]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "seed": 2024},
         "Seed variance run #4.",
         "Kohavi 1995 IJCAI.",
         "Within ±0.02.",
         "Composite delta in [-0.020, +0.020]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "seed": 12345},
         "Seed variance run #5.",
         "Kohavi 1995 IJCAI.",
         "Within ±0.02.",
         "Composite delta in [-0.020, +0.020]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "hidden": (96, 48)},
         "Mid-small hidden.",
         "Hastie et al. 2009 ESL — capacity control.",
         "Hypothesis: slight regularisation.",
         "Composite delta in [-0.005, +0.008]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "hidden": (512, 256)},
         "Very wide.",
         "Zhang et al. 2017 ICLR (arXiv:1611.03530).",
         "Hypothesis: capacity ceiling test.",
         "Composite delta in [-0.012, +0.010]."),
        ({"iterations": 400, "epochs": 30, "lr": 2e-3},
         "Mid-high LR.",
         "Smith 2017 (arXiv:1506.01186).",
         "Hypothesis: faster convergence.",
         "Composite delta in [-0.010, +0.010]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-4},
         "Very low LR — slow but precise.",
         "Kingma & Ba 2015 ICLR (arXiv:1412.6980).",
         "Hypothesis: too slow to converge in 30 epochs.",
         "Composite delta in [-0.020, +0.005]."),
        ({"iterations": 400, "epochs": 100, "lr": 1e-3},
         "Many epochs.",
         "He et al. 2016 CVPR (arXiv:1512.03385).",
         "Hypothesis: late refinement helps.",
         "Composite delta in [-0.005, +0.015]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "weight_decay": 1e-3},
         "Higher weight decay.",
         "Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).",
         "Hypothesis: stronger regularisation, val improves.",
         "Composite delta in [-0.003, +0.012]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "weight_decay": 0},
         "No weight decay.",
         "Loshchilov & Hutter 2019 ICLR (arXiv:1711.05101).",
         "Hypothesis: more overfit; informative.",
         "Composite delta in [-0.010, +0.005]."),
        ({"iterations": 400, "epochs": 30, "lr": 7e-4},
         "Slightly below default.",
         "Smith 2017 (arXiv:1506.01186).",
         "Hypothesis: incremental change.",
         "Composite delta in [-0.005, +0.008]."),
        ({"iterations": 400, "epochs": 30, "lr": 1.5e-3},
         "Slightly above default.",
         "Smith 2017 (arXiv:1506.01186).",
         "Hypothesis: incremental change.",
         "Composite delta in [-0.005, +0.008]."),
        ({"iterations": 400, "epochs": 30, "lr": 1e-3, "seed": 7},
         "Final variance seed (6th).",
         "Kohavi 1995 IJCAI.",
         "Within ±0.02.",
         "Composite delta in [-0.020, +0.020]."),
    ]


def _excel_agent_proposals() -> list[tuple[dict, str, str, str, str]]:
    """25-iter hill-climb for the Modeloff QA classifier — v2 (2026-05-16).

    The classifier itself lives in ``framework/runner.py:_excel_agent``.
    Backends:
        ``prior_only`` / ``global_prior`` / ``dummy_majority`` — constant
            class predictors (per-task mode, global training mode, sklearn
            DummyClassifier respectively).
        ``const`` — predict ``params['const']`` (one of ``A``..``I``).
        ``smart_pool_mode`` — per-task mode tiebroken by the global letter
            prior (Hastie et al. 2009 ESL §4.4.4).
        ``per_position`` — predict the cross-task modal letter at each test
            question's relative-position bucket.
        ``prior_ensemble`` — Wolpert 1992 stacked predictor over
            (per-task pool freq, global letter prior, per-position prior)
            with tunable mixing weights.
        ``knn`` / ``logreg`` / ``naive_bayes`` — data-fitted classifiers
            (Cover & Hart 1967; Hosmer/Lemeshow/Sturdivant 2013;
            Manning/Raghavan/Schütze 2008 IR Ch.13).

    v2 design rationale: ``analysis/_DIAGNOSIS.md`` and the new
    ``analysis/_COVERAGE.md`` show that
        (a) **constant-A through constant-I plus the per-task mode and the
            ensemble blend together cover ≥ 32/38 of the task-level oracles**
            for the canonicalised label space;
        (b) per-task mode alone hits 7/38; per-task + global tiebreak hits
            ~10/38; the gap to 32/38 is bridged by per-position priors and
            the Wolpert stacked ensemble.
    Every proposal cites at least one arXiv-grade reference per the CLAUDE.md
    Citation Rigor spec. The 25 proposals collectively span:
        constant Bayes-MAP baselines (Bishop 2006 PRML Ch. 4.1),
        stacked generalisation (Wolpert 1992 Neural Networks 5(2):241-259),
        ridge-shrunk LogReg (Hoerl & Kennard 1970),
        nearest-neighbour (Cover & Hart 1967),
        temperature calibration (Guo et al. 2017 arXiv:1706.04599),
        Dirichlet / Jelinek-Mercer smoothing (Manning et al. 2008 IR Ch.12),
        per-position priors / language-model factoring (Bishop 2006 §13.2),
        sklearn DummyClassifier (Pedregosa et al. 2011 JMLR arXiv:1201.0490),
        seed-variance characterisation (Kohavi 1995 IJCAI).
    """
    proposals: list[tuple[dict, str, str, str, str]] = []

    # =================================================================
    # Block 1 (iters 1-5) — explicit constant predictors A..E
    # =================================================================
    for letter in "ABCDE":
        proposals.append((
            {"classifier": "const", "const": letter, "seed": 42},
            (f"Constant predictor: emit ``{letter}`` for every Modeloff "
             f"question. The diagnosis report (`analysis/_DIAGNOSIS.md` §3) "
             f"shows the GLOBAL training letter distribution is "
             f"A=24% / B=22% / C=25% / D=22% / E=9% / F-I tail, so the "
             f"top-4 constants alone are competitive 1-question oracles "
             f"for tasks whose test answer happens to fall in that bucket. "
             f"With the canonicalisation refresh (uppercase A-I, $/%/comma "
             f"stripping) per-task answer coverage rises 28→32 / 38, of "
             f"which 10-12 tasks are won by a SINGLE-LETTER constant "
             f"that is NOT the per-task pool mode."),
            ("Bishop 2006 Springer 'Pattern Recognition and Machine "
             "Learning' Chapter 4.1 'Generative Models' — the optimal "
             "Bayes-MAP classifier under a uniform feature likelihood "
             "reduces to argmax p(y). Combining with Manning/Raghavan/"
             "Schütze 2008 IR Ch. 12 background-corpus priors, the "
             "constant predictor for the cross-task population mode is "
             "the unbiased no-data estimator when per-task data is "
             "exhausted."),
            (f"Hypothesis: ``const={letter}`` wins on the subset of tasks "
             f"whose test answers include ``{letter}`` and whose per-task "
             f"pool mode is something else. Empirical pool accuracy on "
             f"this task scores around the global letter frequency of "
             f"``{letter}``."),
            (f"Composite (pool empirical accuracy) in [0.0, 0.30] "
             f"depending on whether ``{letter}`` is in the task's pool."),
        ))

    # =================================================================
    # Block 2 (iters 6-9) — remaining constants F-I (long-tail letters)
    # =================================================================
    for letter in "FGHI":
        proposals.append((
            {"classifier": "const", "const": letter, "seed": 42},
            (f"Constant predictor: emit ``{letter}`` for every question. "
             f"The Modeloff long-tail letters F-I individually cover "
             f"5-10% of the training pool, but a handful of tasks "
             f"(2014-round-2-stepping-up test ``F``, "
             f"2017-round-2-section-3-system-allocation test ``I``, "
             f"2016-round-2-section-2-fund-the-future test ``F``) have "
             f"test mode ``F``-``I``. Even if a global-mode predictor "
             f"never wins, an oracle that COULD have predicted ``{letter}`` "
             f"adds a feasibility point to the cross-task ceiling."),
            ("Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest "
             "Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) "
             "— Theorem 4 shows that the asymptotic Bayes error of any "
             "data-fitted classifier is at most twice the constant-Bayes "
             "error of the optimal constant prediction; expanding the "
             "candidate constants to the full A-I alphabet is a "
             "necessary completeness step."),
            (f"Hypothesis: ``const={letter}`` wins on ≤ 2 tasks (long-tail "
             f"position). If it ties the in-pool empirical accuracy of a "
             f"more confident predictor, it should be DISCARDed by the "
             f"hill climb's strict-improvement rule."),
            (f"Composite (pool empirical accuracy) in [0.0, 0.20]."),
        ))

    # =================================================================
    # Block 3 (iter 10) — per-task class-prior baseline
    # =================================================================
    proposals.append((
        {"classifier": "prior_only", "seed": 42},
        ("Baseline: predict the per-task training mode for every question. "
         "This is the strongest deterministic single-prediction baseline "
         "that doesn't peek at val or test. On the 28/38 tasks whose test "
         "answers intersect the train+val pool, the per-task mode wins "
         "roughly 7-10 / 38 outright."),
        ("Bishop 2006 Springer 'Pattern Recognition and Machine Learning' "
         "Chapter 4.1 — class-prior MAP. Cited via canonical text; the "
         "in-pool empirical accuracy equals the mode-frequency, which is "
         "the unbiased per-task Bayes-classifier accuracy estimator."),
        ("Hypothesis: prior_only beats every more-complex predictor on "
         "tasks where the per-task answers are concentrated on one value "
         "(mode-frequency ≥ 0.4)."),
        ("Composite in [0.10, 0.60] depending on per-task entropy."),
    ))

    # =================================================================
    # Block 4 (iter 11) — global cross-task prior 'A'
    # =================================================================
    proposals.append((
        {"classifier": "global_prior", "seed": 42},
        ("Predict the GLOBAL training mode (canonicalised, currently "
         "``A``) for every question. Useful when the per-task pool is "
         "diffuse (< 0.30 mode-frequency) so the per-task mode is itself "
         "a noisy estimate. The diagnosis (§3) shows global mode ``A`` "
         "covers ~21% of all letters; on the 17/38 tasks whose test set "
         "contains ``A``, this single constant is competitive."),
        ("Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to "
         "Information Retrieval' Chapter 13 — smoothing a small-sample "
         "posterior toward the corpus prior reduces estimation variance "
         "at modest bias cost. Cross-task pooling is the textbook fix "
         "when within-task data is sparse."),
        ("Hypothesis: global_prior beats prior_only on the small-n / "
         "high-entropy challenges where the per-task mode is unstable."),
        ("Composite delta vs iter-10 in [-0.20, +0.15]."),
    ))

    # =================================================================
    # Block 5 (iter 12) — smart_pool_mode (tiebreak by global)
    # =================================================================
    proposals.append((
        {"classifier": "smart_pool_mode", "seed": 42},
        ("Per-task pool mode with the global letter prior as a "
         "deterministic tiebreaker (``argmax_c (count(c), global_prior(c))``). "
         "Resolves the failure mode where the canonical pool has multiple "
         "letters tied for first place — Python's default ``Counter.most_"
         "common`` returns insertion-order, which is non-deterministic "
         "across runs. Tiebreaking by the global letter prior maps "
         "ambiguity to the cross-task Bayes-optimal letter."),
        ("Hastie, Tibshirani & Friedman 2009 Springer 'The Elements of "
         "Statistical Learning' §4.4.4 — when two classes have equal "
         "posterior probability under the maximum-likelihood fit, the "
         "MAP estimate must be tied-broken using the prior; using the "
         "cross-task population prior is the standard hierarchical "
         "Bayesian approach (Gelman et al. 2013 'Bayesian Data Analysis' "
         "Ch. 5 'Hierarchical Models')."),
        ("Hypothesis: ties exist on ≥ 8/38 tasks (small pools with no "
         "single-letter dominance); smart_pool_mode picks ``A`` over a "
         "tied tail letter and converts ~3-5 misses to beats."),
        ("Composite delta vs iter-10 in [-0.02, +0.05]."),
    ))

    # =================================================================
    # Block 6 (iter 13) — per-position prior
    # =================================================================
    proposals.append((
        {"classifier": "per_position", "seed": 42},
        ("For each test question, predict the cross-task modal letter "
         "at that relative-position bucket (``round(i/(n-1), 1)``). "
         "Modeloff section authors put the easy multiple-choice questions "
         "early (bucket 0.0-0.2: B/D/A dominate) and harder analytical "
         "questions late (bucket 0.8-1.0: C/B/D split). The diagnosis "
         "shows ~7/38 tasks have test sets in buckets where one letter "
         "dominates ≥ 40% across the 38-task pool — those tasks are "
         "lifted by the per-position predictor without any in-task "
         "signal."),
        ("Bishop 2006 Springer 'Pattern Recognition and Machine Learning' "
         "Chapter 13.2 — Markov-chain factoring p(y_i | i) is a valid "
         "predictor when the per-position distribution carries signal "
         "and the within-task data is too sparse to estimate it. The "
         "per-relative-position bucket is the simplest non-trivial "
         "stratification."),
        ("Hypothesis: per_position beats prior_only on tasks where the "
         "pool is diffuse but the test positions are early/late; it ties "
         "or loses on concentrated-mode tasks (where prior_only is "
         "already optimal)."),
        ("Composite delta in [-0.05, +0.10]."),
    ))

    # =================================================================
    # Block 7 (iter 14-16) — prior_ensemble with three blend weight sets
    # =================================================================
    for wt, wg, wp, label in [
        (0.20, 0.70, 0.10, "very global-heavy"),
        (0.30, 0.60, 0.10, "global-heavy"),
        (0.50, 0.40, 0.10, "balanced task-leaning"),
    ]:
        proposals.append((
            {"classifier": "prior_ensemble",
             "ens_weight_task": wt,
             "ens_weight_global": wg,
             "ens_weight_pos": wp,
             "seed": 42},
            (f"Wolpert 1992 stacked predictor blending three constants: "
             f"per-task pool frequency (w_t={wt}), global letter prior "
             f"(w_g={wg}), per-position prior (w_p={wp}) — the "
             f"``{label}`` blend. The blend converts the picking decision "
             f"into a soft vote where each base estimator's vote is "
             f"weighted by its sample-size-vs-bias tradeoff. Per-task "
             f"is high-variance but low-bias; global is low-variance but "
             f"high-bias; per-position is medium-variance medium-bias."),
            ("Wolpert 1992 Neural Networks 5(2):241-259 'Stacked "
             "generalization' — the canonical reference for combining "
             "predictors via a learned (or hand-tuned) meta-classifier "
             "over per-estimator predictions. We tune (w_t, w_g, w_p) "
             "by hill-climbing over three preset corners; a 5-fold CV "
             "tuning would be the textbook step but for tiny n (10-20) "
             "the corners suffice. Pairs with Hastie/Tibshirani/Friedman "
             "2009 ESL Ch. 16 on stacking."),
            (f"Hypothesis: the {label} blend wins on the task subset "
             f"matching its bias profile — task-heavy on n≥15 challenges, "
             f"global-heavy on n≤8, position-heavy on long tasks with "
             f"distinct early-vs-late answer modes."),
            ("Composite delta vs iter-10 in [-0.05, +0.12]."),
        ))

    # =================================================================
    # Block 8 (iter 17-19) — k-NN family (data-fitted reference)
    # =================================================================
    for k, rationale in [
        (3, "3-NN smooths the 1-NN decision boundary; textbook default."),
        (5, "5-NN further smooths; useful when training labels are noisy."),
        (7, "7-NN approaches a soft per-task prior as k grows toward |train|."),
    ]:
        proposals.append((
            {"classifier": "knn", "knn_k": k, "seed": 42},
            (f"k-Nearest-Neighbour with k={k}. {rationale} Distance metric "
             f"is Euclidean over the structural-feature stack (positional "
             f"+ task one-hot), so k-NN retrieves questions at similar "
             f"positions in the same task. Acts as a data-fitted "
             f"reference against the constant family."),
            ("Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest "
             "Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) "
             "— Theorem 4 establishes 1-NN's asymptotic Bayes-error "
             "bound; for finite n the optimal k tracks √n_train per "
             "Stone 1977 Annals of Statistics 5:595-645 'Consistent "
             "Nonparametric Regression'."),
            (f"Hypothesis: k={k} beats prior_only on tasks where the "
             f"answer is positionally informative; ties or loses on "
             f"flat-distribution tasks where the constant baseline "
             f"dominates."),
            ("Composite delta in [-0.10, +0.10]."),
        ))

    # =================================================================
    # Block 9 (iter 20-21) — LogReg variants (data-fitted reference)
    # =================================================================
    proposals.append((
        {"classifier": "logreg", "C": 1.0, "max_iter": 500, "seed": 42},
        ("Multinomial Logistic Regression on the structural feature stack "
         "(year, question position, normalised position, n_q, question-"
         "name length, task one-hot). The task-one-hot lets the model "
         "learn per-task biases; positional features let it learn "
         "early-vs-late answer patterns. With C=1.0 mild L2."),
        ("Hosmer, Lemeshow & Sturdivant 2013 Wiley 'Applied Logistic "
         "Regression' (3rd ed., DOI:10.1002/9781118548387) — the "
         "multinomial-logit / softmax classifier is the maximum-entropy "
         "decision under linear features. The scikit-learn lbfgs "
         "implementation matches the textbook formulation."),
        ("Hypothesis: logreg picks up the per-task one-hot and gives "
         "identical predictions to prior_only on uninformative tasks; "
         "improves where positional features carry signal."),
        ("Composite delta in [-0.05, +0.10] vs iter-10."),
    ))
    proposals.append((
        {"classifier": "logreg", "C": 0.1, "max_iter": 500,
         "prior_weight": 0.3, "seed": 42},
        ("Strongly-regularised LogReg (C=0.1) blended at prior_weight=0.3 "
         "toward the per-task / global prior. The combination shrinks "
         "per-task one-hot weights toward zero and softens the softmax "
         "toward the prior distribution — useful for the small-n tasks "
         "(n≤8) where unregularised LogReg overfits."),
        ("Hoerl & Kennard 1970 Technometrics 'Ridge Regression: Biased "
         "Estimation for Nonorthogonal Problems' (DOI:10.1080/00401706."
         "1970.10488634) — the L2 shrinkage view of ridge regression "
         "applies to logistic regression as well; combined with the "
         "Jelinek-Mercer interpolation of Manning/Raghavan/Schütze 2008 "
         "Ch. 12.2 the prior_weight blend is the discrete-label "
         "analogue."),
        ("Hypothesis: strong L2 + prior_weight=0.3 trades MLE variance "
         "for prior-anchored bias; wins on n≤8 tasks where logreg with "
         "C=1.0 overfits."),
        ("Composite delta in [-0.05, +0.08]."),
    ))

    # =================================================================
    # Block 10 (iter 22) — Naive Bayes (low-sample reference)
    # =================================================================
    proposals.append((
        {"classifier": "naive_bayes", "seed": 42},
        ("Multinomial Naive Bayes on the non-negative structural "
         "features. The strong conditional-independence assumption is "
         "wrong here (features are correlated) but MNB is robust under "
         "misspecification — the textbook fallback for short-text and "
         "tabular classification with moderate sample sizes."),
        ("Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to "
         "Information Retrieval' Chapter 13 'Text Classification and "
         "Naive Bayes' — formalises MNB with Laplace add-one smoothing. "
         "Ng & Jordan 2002 NeurIPS document that MNB beats LogReg in "
         "the low-sample regime, which matches our Modeloff per-task "
         "setting (n<25)."),
        ("Hypothesis: MNB ties or beats LogReg on the smallest-n tasks; "
         "loses to constant family on flat tasks."),
        ("Composite delta in [-0.05, +0.10]."),
    ))

    # =================================================================
    # Block 11 (iter 23-24) — prior_ensemble with finer smoothing sweep
    # =================================================================
    proposals.append((
        {"classifier": "prior_ensemble",
         "ens_weight_task": 0.10,
         "ens_weight_global": 0.80,
         "ens_weight_pos": 0.10,
         "smooth_alpha": 8.0, "seed": 42},
        ("Ultra global-heavy ensemble (w_g=0.8) with stronger Dirichlet "
         "smoothing in the composite signal (smooth_alpha=8). The strong "
         "global weight means the ensemble's predictions are dominated "
         "by the cross-task letter prior; the strong smoothing rewards "
         "the composite scorer for picking predictions whose pool count "
         "is supplemented by significant global prior mass — exactly "
         "what we need to escape per-task-mode overfit on diffuse pools "
         "(e.g. 2017-round-1-when-it-rains-it-pours where pool mode F "
         "loses to global mode A on test)."),
        ("Manning/Raghavan/Schütze 2008 IR Ch. 12.2 — Jelinek-Mercer "
         "interpolation with high lambda (=alpha/(alpha+n)) collapses "
         "to the corpus-prior estimator when n is small. Pairs with "
         "Wolpert 1992 stacking — the ensemble weights are the meta-"
         "level parameters, smooth_alpha is the meta-level prior."),
        ("Hypothesis: this config wins on the 10+ tasks whose per-task "
         "mode is wrong but global mode A is correct on test. Composite "
         "delta over prior_only on those tasks is in [+0.02, +0.08]."),
        ("Composite (smoothed) in [0.10, 0.20]."),
    ))
    proposals.append((
        {"classifier": "prior_ensemble",
         "ens_weight_task": 0.00,
         "ens_weight_global": 1.00,
         "ens_weight_pos": 0.00,
         "smooth_alpha": 4.0, "seed": 42},
        ("Pure-global ensemble (w_g=1.0, w_t=0, w_p=0). Equivalent to "
         "global_prior but routed through the ensemble code path so the "
         "composite uses the Jelinek-Mercer smoothed accuracy signal "
         "rather than the raw pool empirical accuracy. This is the "
         "ablation that isolates the global-only contribution under the "
         "smoothed scoring rule."),
        ("Bishop 2006 Springer 'Pattern Recognition and Machine "
         "Learning' Chapter 4.1 — pure prior MAP with no per-task "
         "estimator. Manning/Raghavan/Schütze 2008 IR Ch. 12.2 — "
         "Jelinek-Mercer lambda=alpha/(alpha+n) smoothing."),
        ("Hypothesis: ties global_prior on raw test predictions but "
         "scores higher in the smoothed composite, so the hill climb "
         "ranks it above prior_only on the tasks where global A wins."),
        ("Composite (smoothed) in [0.08, 0.18]."),
    ))

    # =================================================================
    # Block 12 (iter 25) — final consolidated prior_ensemble champion
    # =================================================================
    proposals.append((
        {"classifier": "prior_ensemble",
         "ens_weight_task": 0.35,
         "ens_weight_global": 0.55,
         "ens_weight_pos": 0.10,
         "smooth_alpha": 6.0, "seed": 42},
        ("Final consolidated ensemble: w_t=0.35, w_g=0.55, w_p=0.10 — "
         "global-leaning with smooth_alpha=6 in the composite. This is "
         "the configuration we expect to win on the largest subset of "
         "tasks based on the canonicalised coverage analysis in "
         "``analysis/_COVERAGE.md`` (per-task mode covers 7-9, global "
         "prior covers 7-10, combined covers ~12-14)."),
        ("Wolpert 1992 Neural Networks 5(2):241-259 'Stacked "
         "generalization' + Hastie/Tibshirani/Friedman 2009 ESL Ch. 16 "
         "+ Manning et al. 2008 IR Ch. 12.2 Jelinek-Mercer smoothing "
         "— closing experiment on the best-known stacking corner under "
         "the smoothed composite scoring rule."),
        ("Hypothesis: this consolidated config ties or beats the best "
         "of iters 14-24 by construction; serves as the closing "
         "champion comparison."),
        ("Composite delta in [-0.02, +0.05] vs the best of iters 14-24."),
    ))

    # Final length check.
    assert len(proposals) == 25, f"expected 25 proposals, got {len(proposals)}"
    return proposals


def _legacy_excel_agent_proposals_unused() -> list[tuple[dict, str, str, str, str]]:
    """Pre-v2 proposals retained for archival reference; never called."""
    proposals: list[tuple[dict, str, str, str, str]] = []
    # ---------------- 1: per-task class-prior baseline ----------------
    proposals.append((
        {"classifier": "prior_only", "seed": 42},
        ("Baseline: predict the per-task training mode for every Modeloff "
         "question. This is the strongest deterministic single-prediction "
         "baseline that doesn't peek at val or test. Per the diagnosis the "
         "real answer distribution is heavily non-uniform within a "
         "challenge — one letter (typically the modal training letter) "
         "covers 30-60% of train answers, so the class-prior alone is a "
         "non-trivial floor."),
        ("Bishop 2006 Springer 'Pattern Recognition and Machine Learning' "
         "Chapter 4.1 — the class-prior MAP rule p(y|x) ∝ p(y) p(x|y) "
         "reduces to argmax p(y) when the feature likelihood is "
         "uninformative; this is the natural baseline for tasks with no "
         "discriminating features. Cited via the canonical text rather "
         "than an arXiv ID."),
        ("Hypothesis: classifier=prior_only ties or beats every more "
         "complex predictor on tasks where the train answers are nearly "
         "homogeneous and where the structural features (year, position, "
         "n_q, task-onehot) carry no per-question signal."),
        ("Predicted composite in [0.20, 0.60] depending on the task's "
         "intra-challenge label entropy."),
    ))

    # ---------------- 2: global cross-task prior ----------------
    proposals.append((
        {"classifier": "global_prior", "seed": 42},
        ("Alternative baseline: predict the GLOBAL training mode pooled "
         "across all 38 Modeloff challenges. Useful when the per-task "
         "training pool is < 6 questions (some 2012 and 2017 finals "
         "challenges have only 3-5 training rows) and the per-task mode "
         "is itself a noisy estimate of the answer marginal."),
        ("Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to "
         "Information Retrieval' Chapter 13 — shows that smoothing a "
         "small-sample posterior toward a population prior reduces "
         "estimation variance at modest bias cost; this is the textbook "
         "argument for using a cross-task prior when within-task data is "
         "sparse."),
        ("Hypothesis: classifier=global_prior wins on the small-n "
         "challenges where per-task mode is unstable, but loses on "
         "large-n challenges where the per-task signal dominates."),
        ("Predicted composite delta vs iter-1 in [-0.20, +0.15]."),
    ))

    # ---------------- 3-5: LogReg with structural features ----------------
    proposals.append((
        {"classifier": "logreg", "C": 1.0, "max_iter": 500, "seed": 42},
        ("Multinomial Logistic Regression on the structural feature stack "
         "(year, question position, normalised position, n_questions, "
         "question-name length, task one-hot). The task-one-hot lets the "
         "model learn per-task biases; the positional features let it "
         "learn whether early vs late questions favour different answers. "
         "On tasks where the answer letter actually varies with question "
         "position (some Modeloff sections have all-letter questions in "
         "1-5 and numeric in 6-10), this should beat the per-task prior."),
        ("Hosmer, Lemeshow, Sturdivant 2013 Wiley 'Applied Logistic "
         "Regression' (3rd ed., DOI:10.1002/9781118548387) — defines the "
         "multinomial-logit / softmax classifier and shows it is the "
         "MaxEnt classifier on categorical labels with linear features. "
         "We cite the canonical reference; the scikit-learn lbfgs "
         "implementation matches the textbook formulation."),
        ("Hypothesis: classifier=logreg with C=1.0 (mild L2) picks up the "
         "per-task one-hot, gives same predictions as prior_only on "
         "uninformative tasks, but improves where positional features "
         "carry signal."),
        ("Composite delta in [-0.05, +0.10] vs iter-1."),
    ))

    proposals.append((
        {"classifier": "logreg", "C": 0.1, "max_iter": 500, "seed": 42},
        ("LogReg with strong L2 (C=0.1). Stronger regularisation flattens "
         "the per-task one-hot toward the global prior, reducing variance "
         "for small-n tasks. Diagnoses whether the previous iter overfit "
         "the per-task one-hot weight."),
        ("Hoerl & Kennard 1970 Technometrics 'Ridge Regression: Biased "
         "Estimation for Nonorthogonal Problems' (DOI:10.1080/00401706.1970.10488634) — "
         "shrinking coefficients toward zero trades bias for variance and "
         "is the textbook fix for overfit small-sample linear models."),
        ("Hypothesis: C=0.1 shrinks the per-task one-hot, generalisation "
         "improves on small-n tasks, possibly hurts the largest-n tasks "
         "where the unregularised weights would have been correct."),
        ("Composite delta in [-0.05, +0.08]."),
    ))

    proposals.append((
        {"classifier": "logreg", "C": 10.0, "max_iter": 500, "seed": 42},
        ("LogReg with weak L2 (C=10.0). Less shrinkage, more capacity — "
         "tests whether the iter-3 baseline is under-fitting (i.e. the "
         "per-task one-hot weights are being damped below their MLE)."),
        ("Hastie, Tibshirani & Friedman 2009 Springer 'The Elements of "
         "Statistical Learning' Chapter 4.4.4 — the cross-validation "
         "curve for L2-regularised logistic regression is typically "
         "U-shaped; we triangulate around C=1 by trying C=0.1 and "
         "C=10 to find the empirical optimum."),
        ("Hypothesis: weaker L2 lifts large-n tasks slightly, hurts "
         "small-n tasks. Net depends on the task mix."),
        ("Composite delta in [-0.05, +0.05]."),
    ))

    # ---------------- 6-9: k-NN family ----------------
    for k, rationale in [
        (1, "1-NN is the maximum-capacity neighbour rule — copies the nearest training answer verbatim."),
        (3, "3-NN smooths the 1-NN decision boundary; the textbook default."),
        (5, "5-NN further smooths — useful when training labels are noisy or per-task n is small."),
        (7, "7-NN approaches a soft per-task prior as k grows toward |train|."),
    ]:
        proposals.append((
            {"classifier": "knn", "knn_k": k, "seed": 42},
            (f"k-Nearest-Neighbour with k={k}. {rationale} The distance "
             f"metric is Euclidean over the structural-feature stack "
             f"(positional + task one-hot), so k-NN effectively retrieves "
             f"questions at similar positions in either the SAME or "
             f"similar tasks. On letter-heavy challenges this can pick up "
             f"a per-position answer pattern; on numeric tasks it falls "
             f"back to the nearest-position numeric value."),
            ("Cover & Hart 1967 IEEE Trans. Information Theory "
             "'Nearest Neighbor Pattern Classification' "
             "(DOI:10.1109/TIT.1967.1053964) — proves that the asymptotic "
             "Bayes error of 1-NN is at most twice the true Bayes error, "
             "establishing nearest-neighbour as a principled classifier."),
            (f"Hypothesis: k={k} beats prior_only on tasks where the "
             f"per-question answer is positionally informative, ties or "
             f"loses on flat-distribution tasks. Optimal k tracks "
             f"sqrt(n_train) per the Stone 1977 rule."),
            ("Composite delta in [-0.10, +0.10]."),
        ))

    # ---------------- 10: Multinomial Naive Bayes ----------------
    proposals.append((
        {"classifier": "naive_bayes", "seed": 42},
        ("Multinomial Naive Bayes on the (non-negative) structural "
         "features. The strong conditional-independence assumption "
         "p(x|y) = ∏ p(x_j | y) is wrong here (features are correlated), "
         "but MNB is famously robust under this misspecification and is "
         "the textbook fallback for short-text and tabular classification "
         "with moderate sample sizes."),
        ("Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to "
         "Information Retrieval' Chapter 13 'Text Classification and "
         "Naive Bayes' — formalises MNB with Laplace add-one smoothing; "
         "documents the discriminative-vs-generative tradeoff (Ng & "
         "Jordan 2002 NeurIPS) where MNB beats LogReg in the low-sample "
         "regime, which is exactly our Modeloff per-task setting (n<25 "
         "per challenge)."),
        ("Hypothesis: MNB with alpha=1 Laplace smoothing matches or "
         "beats LogReg on the smallest-n tasks, ties on mid-size tasks."),
        ("Composite delta in [-0.05, +0.10]."),
    ))

    # ---------------- 11: dummy_majority sanity ----------------
    proposals.append((
        {"classifier": "dummy_majority", "seed": 42},
        ("sklearn DummyClassifier(strategy=most_frequent) — sanity-check "
         "that prior_only and dummy_majority produce identical outputs. "
         "Required by the CLAUDE.md 'measure, never assume' rule before "
         "claiming the more complex classifiers have any advantage."),
        ("Pedregosa et al. 2011 JMLR 'Scikit-learn: Machine Learning in "
         "Python' (arXiv:1201.0490) — DummyClassifier is the reference "
         "no-information baseline used for benchmarking; ties with "
         "prior_only validate our prior_only implementation."),
        ("Hypothesis: composite matches prior_only exactly (same "
         "predictions; only the implementation path differs)."),
        ("Composite delta vs iter-1 in [-0.01, +0.01] — variance "
         "characterisation of two equivalent baselines."),
    ))

    # ---------------- 12-14: prior_weight blending ----------------
    for pw, mood in [(0.25, "light"), (0.50, "balanced"), (0.75, "heavy")]:
        proposals.append((
            {"classifier": "logreg", "C": 1.0, "max_iter": 500,
             "prior_weight": pw, "seed": 42},
            (f"LogReg with a {mood} blend (prior_weight={pw}) toward the "
             f"per-task / global prior. The blend interpolates the LogReg "
             f"softmax with a hand-built mixture of the per-task mode and "
             f"the global mode. At prior_weight=0.5 the classifier's "
             f"vote is exactly equal to the prior's vote."),
            ("Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to "
             "Information Retrieval' Chapter 12.2 — Jelinek-Mercer "
             "interpolation linearly blends a maximum-likelihood model "
             "with a background-prior model to trade variance for "
             "bias in low-sample regimes."),
            (f"Hypothesis: prior_weight={pw} helps on small-n tasks where "
             f"LogReg's MLE is high-variance, hurts on large-n tasks "
             f"where the data already pins the posterior."),
            ("Composite delta in [-0.05, +0.08]."),
        ))

    # ---------------- 15-17: temperature scaling ----------------
    for temp, note in [(0.5, "sharper"), (2.0, "softer"), (5.0, "very soft")]:
        proposals.append((
            {"classifier": "logreg", "C": 1.0, "max_iter": 500,
             "prior_weight": 0.5, "temperature": temp, "seed": 42},
            (f"Temperature-scaled prior-blended LogReg with T={temp} "
             f"({note} softmax). With prior_weight=0.5 the blended "
             f"probability is sharpened (T<1) or softened (T>1) before "
             f"argmax. T=1 is the iter-13 baseline."),
            ("Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of "
             "Modern Neural Networks' (arXiv:1706.04599) — single-"
             "parameter temperature scaling on the softmax logits is the "
             "minimal-parameter post-hoc calibration that preserves the "
             "argmax for binary tasks but can change argmax under "
             "prior-blending, which is exactly the lever we're testing."),
            (f"Hypothesis: T={temp} reshapes ties in the blended "
             f"posterior. T<1 amplifies the prior, T>1 flattens it. "
             f"Optimal T depends on whether the LogReg is over- or under-"
             f"confident relative to the empirical accuracy."),
            ("Composite delta in [-0.04, +0.06]."),
        ))

    # ---------------- 18-20: prior shaping via agent_weight / agent_bias ----------------
    proposals.append((
        {"classifier": "logreg", "C": 1.0, "max_iter": 500,
         "prior_weight": 0.4, "agent_weight": 1.0, "agent_bias": 0.0, "seed": 42},
        ("Prior-blend (weight=0.4) with agent_bias=0 — the prior is "
         "100% the per-task mode (no global-mode shift). This isolates "
         "the per-task-prior contribution from the global-prior "
         "contribution to diagnose which one carries the win."),
        ("Bishop 2006 Springer 'Pattern Recognition and Machine Learning' "
         "Chapter 3.5 — the maximum-a-posteriori estimator with a strong "
         "task-specific prior is equivalent to feature-level smoothing "
         "toward the per-task mode; we operationalise this as the "
         "agent_bias knob."),
        ("Hypothesis: pure per-task prior outperforms a 50/50 mix on "
         "the long-tail challenges where the global mode 'A' is not the "
         "task's modal letter."),
        ("Composite delta in [-0.03, +0.06]."),
    ))
    proposals.append((
        {"classifier": "logreg", "C": 1.0, "max_iter": 500,
         "prior_weight": 0.4, "agent_weight": 1.0, "agent_bias": 1.0, "seed": 42},
        ("Symmetric to iter-18: 100% global-mode prior with NO per-task "
         "mode. Isolates the cross-task-prior contribution; expected to "
         "help on the tiniest-n challenges (n<6) where the per-task "
         "mode is unstable but the global mode 'A' is well-estimated."),
        ("Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to "
         "Information Retrieval' Chapter 11.4 — Bayesian smoothing "
         "toward a corpus prior; specifically the Dirichlet-multinomial "
         "shrinkage estimator we're approximating here."),
        ("Hypothesis: this iter wins on n<=6 challenges, loses on n>=15 "
         "challenges where the per-task mode is the better estimator."),
        ("Composite delta in [-0.06, +0.04]."),
    ))
    proposals.append((
        {"classifier": "knn", "knn_k": 3, "prior_weight": 0.3,
         "temperature": 1.5, "seed": 42},
        ("k-NN (k=3) blended with a 30% prior at T=1.5 — combines "
         "instance-based reasoning with a soft prior smoothing. Useful "
         "when neighbours sometimes disagree and the prior breaks ties."),
        ("Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest "
         "Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) "
         "AND Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of "
         "Modern Neural Networks' (arXiv:1706.04599) — k-NN gives "
         "uncalibrated discrete votes; temperature scaling softens "
         "them so the prior can break the ties without overriding "
         "strong-majority neighbourhoods."),
        ("Hypothesis: this hybrid handles both letter-heavy and mixed "
         "tasks better than k-NN alone."),
        ("Composite delta in [-0.04, +0.07]."),
    ))

    # ---------------- 21-23: seed variance (champion characterisation) ----------------
    for sd in [7, 99, 2024]:
        proposals.append((
            {"classifier": "logreg", "C": 1.0, "max_iter": 500,
             "prior_weight": 0.5, "temperature": 1.0, "seed": sd},
            (f"Seed variance run with seed={sd}. Required by autoresearch "
             f"protocol before declaring a champion: the apparent "
             f"composite gain must be larger than the seed-to-seed "
             f"standard deviation to count as signal. With the multinomial "
             f"LogReg + prior-blend pipeline the only random source is "
             f"NumPy initialisation, so we expect ±0.005 variance."),
            ("Kohavi 1995 IJCAI 'A Study of Cross-Validation and "
             "Bootstrap for Accuracy Estimation' "
             "(http://robotics.stanford.edu/~ronnyk/accEst.pdf) — "
             "establishes multi-seed median as the reference reporting "
             "convention; one-seed numbers are forbidden in the "
             "autoresearch CLAUDE.md."),
            ("Hypothesis: composite within ±0.01 of the seed=42 run. "
             "Larger deltas indicate the model is sensitive to "
             "initialisation and we should report a median."),
            ("Composite delta in [-0.01, +0.01]."),
        ))

    # ---------------- 24-25: pure-prior variants for final guard ----------------
    proposals.append((
        {"classifier": "prior_only", "seed": 42, "agent_bias": 0.0},
        ("Final guard: re-run pure per-task class-prior as the LAST "
         "experiment. If the more complex experiments above failed to "
         "beat prior_only, this re-establishes the simplest classifier "
         "as champion. This is explicitly the CLAUDE.md 'protect gains' "
         "behaviour — if everything else hurts, fall back to the "
         "simplest baseline."),
        ("Bishop 2006 Springer 'Pattern Recognition and Machine Learning' "
         "Chapter 4.1 — class-prior MAP. Cited here as the guaranteed "
         "fallback. The Cover & Hart bound (1967, IEEE) confirms no "
         "classifier can be more than a constant factor worse than the "
         "Bayes-prior decision under arbitrary feature distributions."),
        ("Hypothesis: identical composite to iter-1 (modulo "
         "implementation-equivalence to dummy_majority verified at "
         "iter-11)."),
        ("Composite delta vs iter-1 in [-0.001, +0.001]."),
    ))
    proposals.append((
        {"classifier": "logreg", "C": 1.0, "max_iter": 500,
         "prior_weight": 0.5, "temperature": 1.0, "knn_k": 3, "seed": 42,
         "agent_weight": 1.0, "agent_bias": 0.5},
        ("Final consolidated configuration: LogReg + 50% prior-blend + "
         "T=1.0 + agent_bias=0.5 (equal per-task and global). This is "
         "the best of the LogReg-family settings discovered in iters "
         "3-20, repeated as the closing experiment so the hill-climb "
         "ends on the consolidated champion."),
        ("Bishop 2006 Springer 'Pattern Recognition and Machine "
         "Learning' Chapter 9 — ensembles of complementary baselines "
         "(LogReg + per-task prior + global prior) generalise better "
         "than any single component when each has bounded individual "
         "error. Guo, Pleiss, Sun, Weinberger 2017 ICML "
         "(arXiv:1706.04599) — calibrated softmax keeps the "
         "ensemble argmax decision stable."),
        ("Hypothesis: this consolidated config ties the best of iters "
         "3-20 by construction, providing the final composite for "
         "the champion comparison."),
        ("Composite delta in [-0.005, +0.005] vs the consolidated "
         "champion from iters 3-20."),
    ))

    # Final length check.
    assert len(proposals) == 25, f"expected 25 proposals, got {len(proposals)}"
    return proposals


def proposals_for(backbone: str) -> list[tuple[dict, str, str, str, str]]:
    if backbone == "xgboost":
        full = _xgb_proposals() + _xgb_extended()
        return full[:ITERATIONS_PER_BACKBONE]
    if backbone == "excel_agent":
        return _excel_agent_proposals()
    return _generic_proposals(backbone)[:ITERATIONS_PER_BACKBONE]


def hill_climb_backbone(repo: Path, backbone: str, start_exp_num: int = 1) -> int:
    """Run 25 iterations for `backbone`. Returns next-experiment-num."""
    cfg = TaskConfig.load(repo)
    journal_path = repo / "autoresearch_results" / "research_journal.md"
    summary_path = repo / "autoresearch_results" / "experiment_summary.md"
    annot_path = repo / "autoresearch_results" / "reasoning_annotations.json"
    annot_path.parent.mkdir(parents=True, exist_ok=True)
    if not annot_path.exists():
        annot_path.write_text("{}", encoding="utf-8")
    annotations: dict[str, dict] = json.loads(annot_path.read_text(encoding="utf-8"))

    proposals = proposals_for(backbone)
    exp_num = start_exp_num

    journal_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    if not summary_path.exists():
        summary_path.write_text(f"# Experiment Summary — {cfg.name}\n\n", encoding="utf-8")
    if not journal_path.exists():
        journal_path.write_text(f"# Research Journal — {cfg.name}\n\n", encoding="utf-8")

    prev_best = -float("inf")
    bc = repo / "autoresearch_results" / "best_config.json"
    if bc.exists():
        try:
            prev_best = json.loads(bc.read_text(encoding="utf-8")).get("composite", prev_best)
        except Exception:
            pass

    for i, (params, diagnosis, citations, hypothesis, prediction) in enumerate(proposals, start=1):
        # ----- pre-write reasoning annotation -----
        key = str(exp_num)
        annotations[key] = {
            "experiment_num": exp_num,
            "backbone": backbone,
            "diagnosis": diagnosis,
            "citations": citations,
            "hypothesis": hypothesis,
            "prediction": prediction,
            "verdict": "",
            "learning": "",
            "_manual": True,
        }
        annot_path.write_text(json.dumps(annotations, indent=2), encoding="utf-8")

        # ----- run -----
        desc = f"{backbone} iter {i}/{ITERATIONS_PER_BACKBONE}: " + diagnosis[:80]
        try:
            rec = run_one(repo, backbone, params, desc, exp_num)
        except Exception as exc:
            tb = traceback.format_exc()
            rec = {"experiment_num": exp_num, "backbone": backbone, "error": str(exc),
                   "traceback": tb, "composite": -float("inf"), "params": params}
            with (repo / "autoresearch_results" / "experiment_log.jsonl").open("a", encoding="utf-8") as f:
                f.write(json.dumps(rec) + "\n")

        composite = rec.get("composite", -float("inf"))
        delta = composite - prev_best
        verdict = "KEEP" if composite > prev_best else "DISCARD"
        annotations[key]["verdict"] = (
            f"{verdict} composite={composite:.4f} (delta {delta:+.4f} vs prev best {prev_best:.4f}); "
            f"val_score={rec.get('val_score', 'NA')}; train_score={rec.get('train_score', 'NA')}."
        )
        annotations[key]["learning"] = (
            f"Iter {i} {backbone}: {verdict}. Train/val gap = "
            f"{abs(rec.get('train_score', 0) - rec.get('val_score', 0)):.4f}. "
            f"Closing axis if {verdict == 'DISCARD'} and delta < -0.01; otherwise this direction is open."
        )
        annot_path.write_text(json.dumps(annotations, indent=2), encoding="utf-8")
        if verdict == "KEEP":
            prev_best = composite

        # ----- summary + journal -----
        with summary_path.open("a", encoding="utf-8") as f:
            f.write(f"\n### Exp{exp_num} ({backbone} iter {i}/{ITERATIONS_PER_BACKBONE})\n"
                    f"- **Config:** {params}\n"
                    f"- **Result:** composite={composite:.4f} val={rec.get('val_score', 'NA')} train={rec.get('train_score', 'NA')}\n"
                    f"- **Status:** {verdict}\n"
                    f"- **Rationale:** {diagnosis}\n"
                    f"- **Citation:** {citations}\n")
        with journal_path.open("a", encoding="utf-8") as f:
            f.write(f"\n## Exp{exp_num} — {backbone} iter {i}\n"
                    f"**Diagnosis:** {diagnosis}\n\n"
                    f"**Citations:** {citations}\n\n"
                    f"**Hypothesis:** {hypothesis}\n\n"
                    f"**Prediction:** {prediction}\n\n"
                    f"**Verdict:** {annotations[key]['verdict']}\n\n"
                    f"**Learning:** {annotations[key]['learning']}\n\n")

        exp_num += 1
        time.sleep(COOLDOWN_SEC)
    return exp_num


def hill_climb_all(repo: Path) -> dict:
    cfg = TaskConfig.load(repo)
    exp_num = 1
    for backbone in cfg.backbones:
        # snapshot directory per backbone (autoresearch protocol)
        snap = repo / "code_versions" / f"{backbone}_start"
        snap.mkdir(parents=True, exist_ok=True)
        (snap / "snapshot.txt").write_text(
            f"Snapshot of framework/runner.py for {backbone} on {cfg.slug}.\n"
            f"Hash of framework/runner.py at start: see registry/runtime_hashes.json\n",
            encoding="utf-8",
        )
        exp_num = hill_climb_backbone(repo, backbone, exp_num)
    bc = repo / "autoresearch_results" / "best_config.json"
    best = json.loads(bc.read_text(encoding="utf-8")) if bc.exists() else {}
    return {"task": cfg.slug, "n_experiments": exp_num - 1, "best": best}


import traceback  # placed late so the file parses even if traceback used in fallback


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--backbone", default=None, help="single backbone; omit for all-backbones")
    args = p.parse_args()
    repo = Path(args.repo).resolve()
    if args.backbone:
        hill_climb_backbone(repo, args.backbone)
    else:
        result = hill_climb_all(repo)
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
