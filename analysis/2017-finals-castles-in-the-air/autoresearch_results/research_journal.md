# Research Journal — 2017-finals-castles-in-the-air


## Exp1 — excel_agent iter 1
**Diagnosis:** Baseline: predict the per-task training mode for every Modeloff question. This is the strongest deterministic single-prediction baseline that doesn't peek at val or test. Per the diagnosis the real answer distribution is heavily non-uniform within a challenge — one letter (typically the modal training letter) covers 30-60% of train answers, so the class-prior alone is a non-trivial floor.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 — the class-prior MAP rule p(y|x) ∝ p(y) p(x|y) reduces to argmax p(y) when the feature likelihood is uninformative; this is the natural baseline for tasks with no discriminating features. Cited via the canonical text rather than an arXiv ID.

**Hypothesis:** Hypothesis: classifier=prior_only ties or beats every more complex predictor on tasks where the train answers are nearly homogeneous and where the structural features (year, position, n_q, task-onehot) carry no per-question signal.

**Prediction:** Predicted composite in [0.20, 0.60] depending on the task's intra-challenge label entropy.

**Verdict:** KEEP composite=0.4000 (delta +inf vs prev best -inf); val_score=0.4; train_score=0.5.

**Learning:** Iter 1 excel_agent: KEEP. Train/val gap = 0.1000. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — excel_agent iter 2
**Diagnosis:** Alternative baseline: predict the GLOBAL training mode pooled across all 38 Modeloff challenges. Useful when the per-task training pool is < 6 questions (some 2012 and 2017 finals challenges have only 3-5 training rows) and the per-task mode is itself a noisy estimate of the answer marginal.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 13 — shows that smoothing a small-sample posterior toward a population prior reduces estimation variance at modest bias cost; this is the textbook argument for using a cross-task prior when within-task data is sparse.

**Hypothesis:** Hypothesis: classifier=global_prior wins on the small-n challenges where per-task mode is unstable, but loses on large-n challenges where the per-task signal dominates.

**Prediction:** Predicted composite delta vs iter-1 in [-0.20, +0.15].

**Verdict:** DISCARD composite=0.1000 (delta -0.3000 vs prev best 0.4000); val_score=0.1; train_score=0.0.

**Learning:** Iter 2 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp3 — excel_agent iter 3
**Diagnosis:** Multinomial Logistic Regression on the structural feature stack (year, question position, normalised position, n_questions, question-name length, task one-hot). The task-one-hot lets the model learn per-task biases; the positional features let it learn whether early vs late questions favour different answers. On tasks where the answer letter actually varies with question position (some Modeloff sections have all-letter questions in 1-5 and numeric in 6-10), this should beat the per-task prior.

**Citations:** Hosmer, Lemeshow, Sturdivant 2013 Wiley 'Applied Logistic Regression' (3rd ed., DOI:10.1002/9781118548387) — defines the multinomial-logit / softmax classifier and shows it is the MaxEnt classifier on categorical labels with linear features. We cite the canonical reference; the scikit-learn lbfgs implementation matches the textbook formulation.

**Hypothesis:** Hypothesis: classifier=logreg with C=1.0 (mild L2) picks up the per-task one-hot, gives same predictions as prior_only on uninformative tasks, but improves where positional features carry signal.

**Prediction:** Composite delta in [-0.05, +0.10] vs iter-1.

**Verdict:** DISCARD composite=0.3000 (delta -0.1000 vs prev best 0.4000); val_score=0.3; train_score=0.5.

**Learning:** Iter 3 excel_agent: DISCARD. Train/val gap = 0.2000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp4 — excel_agent iter 4
**Diagnosis:** LogReg with strong L2 (C=0.1). Stronger regularisation flattens the per-task one-hot toward the global prior, reducing variance for small-n tasks. Diagnoses whether the previous iter overfit the per-task one-hot weight.

**Citations:** Hoerl & Kennard 1970 Technometrics 'Ridge Regression: Biased Estimation for Nonorthogonal Problems' (DOI:10.1080/00401706.1970.10488634) — shrinking coefficients toward zero trades bias for variance and is the textbook fix for overfit small-sample linear models.

**Hypothesis:** Hypothesis: C=0.1 shrinks the per-task one-hot, generalisation improves on small-n tasks, possibly hurts the largest-n tasks where the unregularised weights would have been correct.

**Prediction:** Composite delta in [-0.05, +0.08].

**Verdict:** DISCARD composite=0.3000 (delta -0.1000 vs prev best 0.4000); val_score=0.3; train_score=0.5.

**Learning:** Iter 4 excel_agent: DISCARD. Train/val gap = 0.2000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — excel_agent iter 5
**Diagnosis:** LogReg with weak L2 (C=10.0). Less shrinkage, more capacity — tests whether the iter-3 baseline is under-fitting (i.e. the per-task one-hot weights are being damped below their MLE).

**Citations:** Hastie, Tibshirani & Friedman 2009 Springer 'The Elements of Statistical Learning' Chapter 4.4.4 — the cross-validation curve for L2-regularised logistic regression is typically U-shaped; we triangulate around C=1 by trying C=0.1 and C=10 to find the empirical optimum.

**Hypothesis:** Hypothesis: weaker L2 lifts large-n tasks slightly, hurts small-n tasks. Net depends on the task mix.

**Prediction:** Composite delta in [-0.05, +0.05].

**Verdict:** DISCARD composite=0.2000 (delta -0.2000 vs prev best 0.4000); val_score=0.2; train_score=0.625.

**Learning:** Iter 5 excel_agent: DISCARD. Train/val gap = 0.4250. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — excel_agent iter 6
**Diagnosis:** k-Nearest-Neighbour with k=1. 1-NN is the maximum-capacity neighbour rule — copies the nearest training answer verbatim. The distance metric is Euclidean over the structural-feature stack (positional + task one-hot), so k-NN effectively retrieves questions at similar positions in either the SAME or similar tasks. On letter-heavy challenges this can pick up a per-position answer pattern; on numeric tasks it falls back to the nearest-position numeric value.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — proves that the asymptotic Bayes error of 1-NN is at most twice the true Bayes error, establishing nearest-neighbour as a principled classifier.

**Hypothesis:** Hypothesis: k=1 beats prior_only on tasks where the per-question answer is positionally informative, ties or loses on flat-distribution tasks. Optimal k tracks sqrt(n_train) per the Stone 1977 rule.

**Prediction:** Composite delta in [-0.10, +0.10].

**Verdict:** DISCARD composite=0.2000 (delta -0.2000 vs prev best 0.4000); val_score=0.2; train_score=1.0.

**Learning:** Iter 6 excel_agent: DISCARD. Train/val gap = 0.8000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — excel_agent iter 7
**Diagnosis:** k-Nearest-Neighbour with k=3. 3-NN smooths the 1-NN decision boundary; the textbook default. The distance metric is Euclidean over the structural-feature stack (positional + task one-hot), so k-NN effectively retrieves questions at similar positions in either the SAME or similar tasks. On letter-heavy challenges this can pick up a per-position answer pattern; on numeric tasks it falls back to the nearest-position numeric value.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — proves that the asymptotic Bayes error of 1-NN is at most twice the true Bayes error, establishing nearest-neighbour as a principled classifier.

**Hypothesis:** Hypothesis: k=3 beats prior_only on tasks where the per-question answer is positionally informative, ties or loses on flat-distribution tasks. Optimal k tracks sqrt(n_train) per the Stone 1977 rule.

**Prediction:** Composite delta in [-0.10, +0.10].

**Verdict:** DISCARD composite=0.2000 (delta -0.2000 vs prev best 0.4000); val_score=0.2; train_score=1.0.

**Learning:** Iter 7 excel_agent: DISCARD. Train/val gap = 0.8000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp8 — excel_agent iter 8
**Diagnosis:** k-Nearest-Neighbour with k=5. 5-NN further smooths — useful when training labels are noisy or per-task n is small. The distance metric is Euclidean over the structural-feature stack (positional + task one-hot), so k-NN effectively retrieves questions at similar positions in either the SAME or similar tasks. On letter-heavy challenges this can pick up a per-position answer pattern; on numeric tasks it falls back to the nearest-position numeric value.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — proves that the asymptotic Bayes error of 1-NN is at most twice the true Bayes error, establishing nearest-neighbour as a principled classifier.

**Hypothesis:** Hypothesis: k=5 beats prior_only on tasks where the per-question answer is positionally informative, ties or loses on flat-distribution tasks. Optimal k tracks sqrt(n_train) per the Stone 1977 rule.

**Prediction:** Composite delta in [-0.10, +0.10].

**Verdict:** DISCARD composite=0.2000 (delta -0.2000 vs prev best 0.4000); val_score=0.2; train_score=1.0.

**Learning:** Iter 8 excel_agent: DISCARD. Train/val gap = 0.8000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — excel_agent iter 9
**Diagnosis:** k-Nearest-Neighbour with k=7. 7-NN approaches a soft per-task prior as k grows toward |train|. The distance metric is Euclidean over the structural-feature stack (positional + task one-hot), so k-NN effectively retrieves questions at similar positions in either the SAME or similar tasks. On letter-heavy challenges this can pick up a per-position answer pattern; on numeric tasks it falls back to the nearest-position numeric value.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — proves that the asymptotic Bayes error of 1-NN is at most twice the true Bayes error, establishing nearest-neighbour as a principled classifier.

**Hypothesis:** Hypothesis: k=7 beats prior_only on tasks where the per-question answer is positionally informative, ties or loses on flat-distribution tasks. Optimal k tracks sqrt(n_train) per the Stone 1977 rule.

**Prediction:** Composite delta in [-0.10, +0.10].

**Verdict:** DISCARD composite=0.2000 (delta -0.2000 vs prev best 0.4000); val_score=0.2; train_score=1.0.

**Learning:** Iter 9 excel_agent: DISCARD. Train/val gap = 0.8000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — excel_agent iter 10
**Diagnosis:** Multinomial Naive Bayes on the (non-negative) structural features. The strong conditional-independence assumption p(x|y) = ∏ p(x_j | y) is wrong here (features are correlated), but MNB is famously robust under this misspecification and is the textbook fallback for short-text and tabular classification with moderate sample sizes.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 13 'Text Classification and Naive Bayes' — formalises MNB with Laplace add-one smoothing; documents the discriminative-vs-generative tradeoff (Ng & Jordan 2002 NeurIPS) where MNB beats LogReg in the low-sample regime, which is exactly our Modeloff per-task setting (n<25 per challenge).

**Hypothesis:** Hypothesis: MNB with alpha=1 Laplace smoothing matches or beats LogReg on the smallest-n tasks, ties on mid-size tasks.

**Prediction:** Composite delta in [-0.05, +0.10].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 10 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — excel_agent iter 11
**Diagnosis:** sklearn DummyClassifier(strategy=most_frequent) — sanity-check that prior_only and dummy_majority produce identical outputs. Required by the CLAUDE.md 'measure, never assume' rule before claiming the more complex classifiers have any advantage.

**Citations:** Pedregosa et al. 2011 JMLR 'Scikit-learn: Machine Learning in Python' (arXiv:1201.0490) — DummyClassifier is the reference no-information baseline used for benchmarking; ties with prior_only validate our prior_only implementation.

**Hypothesis:** Hypothesis: composite matches prior_only exactly (same predictions; only the implementation path differs).

**Prediction:** Composite delta vs iter-1 in [-0.01, +0.01] — variance characterisation of two equivalent baselines.

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 11 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp12 — excel_agent iter 12
**Diagnosis:** LogReg with a light blend (prior_weight=0.25) toward the per-task / global prior. The blend interpolates the LogReg softmax with a hand-built mixture of the per-task mode and the global mode. At prior_weight=0.5 the classifier's vote is exactly equal to the prior's vote.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 12.2 — Jelinek-Mercer interpolation linearly blends a maximum-likelihood model with a background-prior model to trade variance for bias in low-sample regimes.

**Hypothesis:** Hypothesis: prior_weight=0.25 helps on small-n tasks where LogReg's MLE is high-variance, hurts on large-n tasks where the data already pins the posterior.

**Prediction:** Composite delta in [-0.05, +0.08].

**Verdict:** DISCARD composite=0.3000 (delta -0.1000 vs prev best 0.4000); val_score=0.3; train_score=0.625.

**Learning:** Iter 12 excel_agent: DISCARD. Train/val gap = 0.3250. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — excel_agent iter 13
**Diagnosis:** LogReg with a balanced blend (prior_weight=0.5) toward the per-task / global prior. The blend interpolates the LogReg softmax with a hand-built mixture of the per-task mode and the global mode. At prior_weight=0.5 the classifier's vote is exactly equal to the prior's vote.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 12.2 — Jelinek-Mercer interpolation linearly blends a maximum-likelihood model with a background-prior model to trade variance for bias in low-sample regimes.

**Hypothesis:** Hypothesis: prior_weight=0.5 helps on small-n tasks where LogReg's MLE is high-variance, hurts on large-n tasks where the data already pins the posterior.

**Prediction:** Composite delta in [-0.05, +0.08].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 13 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — excel_agent iter 14
**Diagnosis:** LogReg with a heavy blend (prior_weight=0.75) toward the per-task / global prior. The blend interpolates the LogReg softmax with a hand-built mixture of the per-task mode and the global mode. At prior_weight=0.5 the classifier's vote is exactly equal to the prior's vote.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 12.2 — Jelinek-Mercer interpolation linearly blends a maximum-likelihood model with a background-prior model to trade variance for bias in low-sample regimes.

**Hypothesis:** Hypothesis: prior_weight=0.75 helps on small-n tasks where LogReg's MLE is high-variance, hurts on large-n tasks where the data already pins the posterior.

**Prediction:** Composite delta in [-0.05, +0.08].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 14 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — excel_agent iter 15
**Diagnosis:** Temperature-scaled prior-blended LogReg with T=0.5 (sharper softmax). With prior_weight=0.5 the blended probability is sharpened (T<1) or softened (T>1) before argmax. T=1 is the iter-13 baseline.

**Citations:** Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599) — single-parameter temperature scaling on the softmax logits is the minimal-parameter post-hoc calibration that preserves the argmax for binary tasks but can change argmax under prior-blending, which is exactly the lever we're testing.

**Hypothesis:** Hypothesis: T=0.5 reshapes ties in the blended posterior. T<1 amplifies the prior, T>1 flattens it. Optimal T depends on whether the LogReg is over- or under-confident relative to the empirical accuracy.

**Prediction:** Composite delta in [-0.04, +0.06].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 15 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — excel_agent iter 16
**Diagnosis:** Temperature-scaled prior-blended LogReg with T=2.0 (softer softmax). With prior_weight=0.5 the blended probability is sharpened (T<1) or softened (T>1) before argmax. T=1 is the iter-13 baseline.

**Citations:** Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599) — single-parameter temperature scaling on the softmax logits is the minimal-parameter post-hoc calibration that preserves the argmax for binary tasks but can change argmax under prior-blending, which is exactly the lever we're testing.

**Hypothesis:** Hypothesis: T=2.0 reshapes ties in the blended posterior. T<1 amplifies the prior, T>1 flattens it. Optimal T depends on whether the LogReg is over- or under-confident relative to the empirical accuracy.

**Prediction:** Composite delta in [-0.04, +0.06].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 16 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — excel_agent iter 17
**Diagnosis:** Temperature-scaled prior-blended LogReg with T=5.0 (very soft softmax). With prior_weight=0.5 the blended probability is sharpened (T<1) or softened (T>1) before argmax. T=1 is the iter-13 baseline.

**Citations:** Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599) — single-parameter temperature scaling on the softmax logits is the minimal-parameter post-hoc calibration that preserves the argmax for binary tasks but can change argmax under prior-blending, which is exactly the lever we're testing.

**Hypothesis:** Hypothesis: T=5.0 reshapes ties in the blended posterior. T<1 amplifies the prior, T>1 flattens it. Optimal T depends on whether the LogReg is over- or under-confident relative to the empirical accuracy.

**Prediction:** Composite delta in [-0.04, +0.06].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 17 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — excel_agent iter 18
**Diagnosis:** Prior-blend (weight=0.4) with agent_bias=0 — the prior is 100% the per-task mode (no global-mode shift). This isolates the per-task-prior contribution from the global-prior contribution to diagnose which one carries the win.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 3.5 — the maximum-a-posteriori estimator with a strong task-specific prior is equivalent to feature-level smoothing toward the per-task mode; we operationalise this as the agent_bias knob.

**Hypothesis:** Hypothesis: pure per-task prior outperforms a 50/50 mix on the long-tail challenges where the global mode 'A' is not the task's modal letter.

**Prediction:** Composite delta in [-0.03, +0.06].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 18 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — excel_agent iter 19
**Diagnosis:** Symmetric to iter-18: 100% global-mode prior with NO per-task mode. Isolates the cross-task-prior contribution; expected to help on the tiniest-n challenges (n<6) where the per-task mode is unstable but the global mode 'A' is well-estimated.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 11.4 — Bayesian smoothing toward a corpus prior; specifically the Dirichlet-multinomial shrinkage estimator we're approximating here.

**Hypothesis:** Hypothesis: this iter wins on n<=6 challenges, loses on n>=15 challenges where the per-task mode is the better estimator.

**Prediction:** Composite delta in [-0.06, +0.04].

**Verdict:** DISCARD composite=0.1000 (delta -0.3000 vs prev best 0.4000); val_score=0.1; train_score=0.5.

**Learning:** Iter 19 excel_agent: DISCARD. Train/val gap = 0.4000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — excel_agent iter 20
**Diagnosis:** k-NN (k=3) blended with a 30% prior at T=1.5 — combines instance-based reasoning with a soft prior smoothing. Useful when neighbours sometimes disagree and the prior breaks ties.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) AND Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599) — k-NN gives uncalibrated discrete votes; temperature scaling softens them so the prior can break the ties without overriding strong-majority neighbourhoods.

**Hypothesis:** Hypothesis: this hybrid handles both letter-heavy and mixed tasks better than k-NN alone.

**Prediction:** Composite delta in [-0.04, +0.07].

**Verdict:** DISCARD composite=0.2000 (delta -0.2000 vs prev best 0.4000); val_score=0.2; train_score=1.0.

**Learning:** Iter 20 excel_agent: DISCARD. Train/val gap = 0.8000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp21 — excel_agent iter 21
**Diagnosis:** Seed variance run with seed=7. Required by autoresearch protocol before declaring a champion: the apparent composite gain must be larger than the seed-to-seed standard deviation to count as signal. With the multinomial LogReg + prior-blend pipeline the only random source is NumPy initialisation, so we expect ±0.005 variance.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' (http://robotics.stanford.edu/~ronnyk/accEst.pdf) — establishes multi-seed median as the reference reporting convention; one-seed numbers are forbidden in the autoresearch CLAUDE.md.

**Hypothesis:** Hypothesis: composite within ±0.01 of the seed=42 run. Larger deltas indicate the model is sensitive to initialisation and we should report a median.

**Prediction:** Composite delta in [-0.01, +0.01].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 21 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — excel_agent iter 22
**Diagnosis:** Seed variance run with seed=99. Required by autoresearch protocol before declaring a champion: the apparent composite gain must be larger than the seed-to-seed standard deviation to count as signal. With the multinomial LogReg + prior-blend pipeline the only random source is NumPy initialisation, so we expect ±0.005 variance.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' (http://robotics.stanford.edu/~ronnyk/accEst.pdf) — establishes multi-seed median as the reference reporting convention; one-seed numbers are forbidden in the autoresearch CLAUDE.md.

**Hypothesis:** Hypothesis: composite within ±0.01 of the seed=42 run. Larger deltas indicate the model is sensitive to initialisation and we should report a median.

**Prediction:** Composite delta in [-0.01, +0.01].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 22 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — excel_agent iter 23
**Diagnosis:** Seed variance run with seed=2024. Required by autoresearch protocol before declaring a champion: the apparent composite gain must be larger than the seed-to-seed standard deviation to count as signal. With the multinomial LogReg + prior-blend pipeline the only random source is NumPy initialisation, so we expect ±0.005 variance.

**Citations:** Kohavi 1995 IJCAI 'A Study of Cross-Validation and Bootstrap for Accuracy Estimation' (http://robotics.stanford.edu/~ronnyk/accEst.pdf) — establishes multi-seed median as the reference reporting convention; one-seed numbers are forbidden in the autoresearch CLAUDE.md.

**Hypothesis:** Hypothesis: composite within ±0.01 of the seed=42 run. Larger deltas indicate the model is sensitive to initialisation and we should report a median.

**Prediction:** Composite delta in [-0.01, +0.01].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 23 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — excel_agent iter 24
**Diagnosis:** Final guard: re-run pure per-task class-prior as the LAST experiment. If the more complex experiments above failed to beat prior_only, this re-establishes the simplest classifier as champion. This is explicitly the CLAUDE.md 'protect gains' behaviour — if everything else hurts, fall back to the simplest baseline.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 — class-prior MAP. Cited here as the guaranteed fallback. The Cover & Hart bound (1967, IEEE) confirms no classifier can be more than a constant factor worse than the Bayes-prior decision under arbitrary feature distributions.

**Hypothesis:** Hypothesis: identical composite to iter-1 (modulo implementation-equivalence to dummy_majority verified at iter-11).

**Prediction:** Composite delta vs iter-1 in [-0.001, +0.001].

**Verdict:** DISCARD composite=0.4000 (delta +0.0000 vs prev best 0.4000); val_score=0.4; train_score=0.5.

**Learning:** Iter 24 excel_agent: DISCARD. Train/val gap = 0.1000. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — excel_agent iter 25
**Diagnosis:** Final consolidated configuration: LogReg + 50% prior-blend + T=1.0 + agent_bias=0.5 (equal per-task and global). This is the best of the LogReg-family settings discovered in iters 3-20, repeated as the closing experiment so the hill-climb ends on the consolidated champion.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 9 — ensembles of complementary baselines (LogReg + per-task prior + global prior) generalise better than any single component when each has bounded individual error. Guo, Pleiss, Sun, Weinberger 2017 ICML (arXiv:1706.04599) — calibrated softmax keeps the ensemble argmax decision stable.

**Hypothesis:** Hypothesis: this consolidated config ties the best of iters 3-20 by construction, providing the final composite for the champion comparison.

**Prediction:** Composite delta in [-0.005, +0.005] vs the consolidated champion from iters 3-20.

**Verdict:** DISCARD composite=0.3000 (delta -0.1000 vs prev best 0.4000); val_score=0.3; train_score=0.625.

**Learning:** Iter 25 excel_agent: DISCARD. Train/val gap = 0.3250. Closing axis if True and delta < -0.01; otherwise this direction is open.

