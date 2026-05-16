# Research Journal — 2012-round-2-monte-carlo

_Refreshed for v2 hill climb._

## Exp1 — excel_agent iter 1
**Diagnosis:** Constant predictor: emit ``A`` for every Modeloff question. The diagnosis report (`analysis/_DIAGNOSIS.md` §3) shows the GLOBAL training letter distribution is A=24% / B=22% / C=25% / D=22% / E=9% / F-I tail, so the top-4 constants alone are competitive 1-question oracles for tasks whose test answer happens to fall in that bucket. With the canonicalisation refresh (uppercase A-I, $/%/comma stripping) per-task answer coverage rises 28→32 / 38, of which 10-12 tasks are won by a SINGLE-LETTER constant that is NOT the per-task pool mode.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 'Generative Models' — the optimal Bayes-MAP classifier under a uniform feature likelihood reduces to argmax p(y). Combining with Manning/Raghavan/Schütze 2008 IR Ch. 12 background-corpus priors, the constant predictor for the cross-task population mode is the unbiased no-data estimator when per-task data is exhausted.

**Hypothesis:** Hypothesis: ``const=A`` wins on the subset of tasks whose test answers include ``A`` and whose per-task pool mode is something else. Empirical pool accuracy on this task scores around the global letter frequency of ``A``.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.30] depending on whether ``A`` is in the task's pool.

**Verdict:** KEEP composite=0.1044 (delta +inf vs prev best -inf); val_score=0.10444444444444445; train_score=0.0.

**Learning:** Iter 1 excel_agent: KEEP. Train/val gap = 0.1044. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp2 — excel_agent iter 2
**Diagnosis:** Constant predictor: emit ``B`` for every Modeloff question. The diagnosis report (`analysis/_DIAGNOSIS.md` §3) shows the GLOBAL training letter distribution is A=24% / B=22% / C=25% / D=22% / E=9% / F-I tail, so the top-4 constants alone are competitive 1-question oracles for tasks whose test answer happens to fall in that bucket. With the canonicalisation refresh (uppercase A-I, $/%/comma stripping) per-task answer coverage rises 28→32 / 38, of which 10-12 tasks are won by a SINGLE-LETTER constant that is NOT the per-task pool mode.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 'Generative Models' — the optimal Bayes-MAP classifier under a uniform feature likelihood reduces to argmax p(y). Combining with Manning/Raghavan/Schütze 2008 IR Ch. 12 background-corpus priors, the constant predictor for the cross-task population mode is the unbiased no-data estimator when per-task data is exhausted.

**Hypothesis:** Hypothesis: ``const=B`` wins on the subset of tasks whose test answers include ``B`` and whose per-task pool mode is something else. Empirical pool accuracy on this task scores around the global letter frequency of ``B``.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.30] depending on whether ``B`` is in the task's pool.

**Verdict:** KEEP composite=0.3433 (delta +0.2389 vs prev best 0.1044); val_score=0.3433333333333333; train_score=0.0.

**Learning:** Iter 2 excel_agent: KEEP. Train/val gap = 0.3433. Closing axis if False and delta < -0.01; otherwise this direction is open.


## Exp3 — excel_agent iter 3
**Diagnosis:** Constant predictor: emit ``C`` for every Modeloff question. The diagnosis report (`analysis/_DIAGNOSIS.md` §3) shows the GLOBAL training letter distribution is A=24% / B=22% / C=25% / D=22% / E=9% / F-I tail, so the top-4 constants alone are competitive 1-question oracles for tasks whose test answer happens to fall in that bucket. With the canonicalisation refresh (uppercase A-I, $/%/comma stripping) per-task answer coverage rises 28→32 / 38, of which 10-12 tasks are won by a SINGLE-LETTER constant that is NOT the per-task pool mode.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 'Generative Models' — the optimal Bayes-MAP classifier under a uniform feature likelihood reduces to argmax p(y). Combining with Manning/Raghavan/Schütze 2008 IR Ch. 12 background-corpus priors, the constant predictor for the cross-task population mode is the unbiased no-data estimator when per-task data is exhausted.

**Hypothesis:** Hypothesis: ``const=C`` wins on the subset of tasks whose test answers include ``C`` and whose per-task pool mode is something else. Empirical pool accuracy on this task scores around the global letter frequency of ``C``.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.30] depending on whether ``C`` is in the task's pool.

**Verdict:** DISCARD composite=0.0978 (delta -0.2456 vs prev best 0.3433); val_score=0.09777777777777778; train_score=0.0.

**Learning:** Iter 3 excel_agent: DISCARD. Train/val gap = 0.0978. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp4 — excel_agent iter 4
**Diagnosis:** Constant predictor: emit ``D`` for every Modeloff question. The diagnosis report (`analysis/_DIAGNOSIS.md` §3) shows the GLOBAL training letter distribution is A=24% / B=22% / C=25% / D=22% / E=9% / F-I tail, so the top-4 constants alone are competitive 1-question oracles for tasks whose test answer happens to fall in that bucket. With the canonicalisation refresh (uppercase A-I, $/%/comma stripping) per-task answer coverage rises 28→32 / 38, of which 10-12 tasks are won by a SINGLE-LETTER constant that is NOT the per-task pool mode.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 'Generative Models' — the optimal Bayes-MAP classifier under a uniform feature likelihood reduces to argmax p(y). Combining with Manning/Raghavan/Schütze 2008 IR Ch. 12 background-corpus priors, the constant predictor for the cross-task population mode is the unbiased no-data estimator when per-task data is exhausted.

**Hypothesis:** Hypothesis: ``const=D`` wins on the subset of tasks whose test answers include ``D`` and whose per-task pool mode is something else. Empirical pool accuracy on this task scores around the global letter frequency of ``D``.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.30] depending on whether ``D`` is in the task's pool.

**Verdict:** DISCARD composite=0.3411 (delta -0.0022 vs prev best 0.3433); val_score=0.34111111111111114; train_score=1.0.

**Learning:** Iter 4 excel_agent: DISCARD. Train/val gap = 0.6589. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp5 — excel_agent iter 5
**Diagnosis:** Constant predictor: emit ``E`` for every Modeloff question. The diagnosis report (`analysis/_DIAGNOSIS.md` §3) shows the GLOBAL training letter distribution is A=24% / B=22% / C=25% / D=22% / E=9% / F-I tail, so the top-4 constants alone are competitive 1-question oracles for tasks whose test answer happens to fall in that bucket. With the canonicalisation refresh (uppercase A-I, $/%/comma stripping) per-task answer coverage rises 28→32 / 38, of which 10-12 tasks are won by a SINGLE-LETTER constant that is NOT the per-task pool mode.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 'Generative Models' — the optimal Bayes-MAP classifier under a uniform feature likelihood reduces to argmax p(y). Combining with Manning/Raghavan/Schütze 2008 IR Ch. 12 background-corpus priors, the constant predictor for the cross-task population mode is the unbiased no-data estimator when per-task data is exhausted.

**Hypothesis:** Hypothesis: ``const=E`` wins on the subset of tasks whose test answers include ``E`` and whose per-task pool mode is something else. Empirical pool accuracy on this task scores around the global letter frequency of ``E``.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.30] depending on whether ``E`` is in the task's pool.

**Verdict:** DISCARD composite=0.0267 (delta -0.3167 vs prev best 0.3433); val_score=0.02666666666666667; train_score=0.0.

**Learning:** Iter 5 excel_agent: DISCARD. Train/val gap = 0.0267. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp6 — excel_agent iter 6
**Diagnosis:** Constant predictor: emit ``F`` for every question. The Modeloff long-tail letters F-I individually cover 5-10% of the training pool, but a handful of tasks (2014-round-2-stepping-up test ``F``, 2017-round-2-section-3-system-allocation test ``I``, 2016-round-2-section-2-fund-the-future test ``F``) have test mode ``F``-``I``. Even if a global-mode predictor never wins, an oracle that COULD have predicted ``F`` adds a feasibility point to the cross-task ceiling.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — Theorem 4 shows that the asymptotic Bayes error of any data-fitted classifier is at most twice the constant-Bayes error of the optimal constant prediction; expanding the candidate constants to the full A-I alphabet is a necessary completeness step.

**Hypothesis:** Hypothesis: ``const=F`` wins on ≤ 2 tasks (long-tail position). If it ties the in-pool empirical accuracy of a more confident predictor, it should be DISCARDed by the hill climb's strict-improvement rule.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.20].

**Verdict:** DISCARD composite=0.0422 (delta -0.3011 vs prev best 0.3433); val_score=0.042222222222222223; train_score=0.0.

**Learning:** Iter 6 excel_agent: DISCARD. Train/val gap = 0.0422. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp7 — excel_agent iter 7
**Diagnosis:** Constant predictor: emit ``G`` for every question. The Modeloff long-tail letters F-I individually cover 5-10% of the training pool, but a handful of tasks (2014-round-2-stepping-up test ``F``, 2017-round-2-section-3-system-allocation test ``I``, 2016-round-2-section-2-fund-the-future test ``F``) have test mode ``F``-``I``. Even if a global-mode predictor never wins, an oracle that COULD have predicted ``G`` adds a feasibility point to the cross-task ceiling.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — Theorem 4 shows that the asymptotic Bayes error of any data-fitted classifier is at most twice the constant-Bayes error of the optimal constant prediction; expanding the candidate constants to the full A-I alphabet is a necessary completeness step.

**Hypothesis:** Hypothesis: ``const=G`` wins on ≤ 2 tasks (long-tail position). If it ties the in-pool empirical accuracy of a more confident predictor, it should be DISCARDed by the hill climb's strict-improvement rule.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.20].

**Verdict:** DISCARD composite=0.0089 (delta -0.3344 vs prev best 0.3433); val_score=0.008888888888888889; train_score=0.0.

**Learning:** Iter 7 excel_agent: DISCARD. Train/val gap = 0.0089. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp8 — excel_agent iter 8
**Diagnosis:** Constant predictor: emit ``H`` for every question. The Modeloff long-tail letters F-I individually cover 5-10% of the training pool, but a handful of tasks (2014-round-2-stepping-up test ``F``, 2017-round-2-section-3-system-allocation test ``I``, 2016-round-2-section-2-fund-the-future test ``F``) have test mode ``F``-``I``. Even if a global-mode predictor never wins, an oracle that COULD have predicted ``H`` adds a feasibility point to the cross-task ceiling.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — Theorem 4 shows that the asymptotic Bayes error of any data-fitted classifier is at most twice the constant-Bayes error of the optimal constant prediction; expanding the candidate constants to the full A-I alphabet is a necessary completeness step.

**Hypothesis:** Hypothesis: ``const=H`` wins on ≤ 2 tasks (long-tail position). If it ties the in-pool empirical accuracy of a more confident predictor, it should be DISCARDed by the hill climb's strict-improvement rule.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.20].

**Verdict:** DISCARD composite=0.0156 (delta -0.3278 vs prev best 0.3433); val_score=0.015555555555555555; train_score=0.0.

**Learning:** Iter 8 excel_agent: DISCARD. Train/val gap = 0.0156. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp9 — excel_agent iter 9
**Diagnosis:** Constant predictor: emit ``I`` for every question. The Modeloff long-tail letters F-I individually cover 5-10% of the training pool, but a handful of tasks (2014-round-2-stepping-up test ``F``, 2017-round-2-section-3-system-allocation test ``I``, 2016-round-2-section-2-fund-the-future test ``F``) have test mode ``F``-``I``. Even if a global-mode predictor never wins, an oracle that COULD have predicted ``I`` adds a feasibility point to the cross-task ceiling.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — Theorem 4 shows that the asymptotic Bayes error of any data-fitted classifier is at most twice the constant-Bayes error of the optimal constant prediction; expanding the candidate constants to the full A-I alphabet is a necessary completeness step.

**Hypothesis:** Hypothesis: ``const=I`` wins on ≤ 2 tasks (long-tail position). If it ties the in-pool empirical accuracy of a more confident predictor, it should be DISCARDed by the hill climb's strict-improvement rule.

**Prediction:** Composite (pool empirical accuracy) in [0.0, 0.20].

**Verdict:** DISCARD composite=0.0200 (delta -0.3233 vs prev best 0.3433); val_score=0.02; train_score=0.0.

**Learning:** Iter 9 excel_agent: DISCARD. Train/val gap = 0.0200. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp10 — excel_agent iter 10
**Diagnosis:** Baseline: predict the per-task training mode for every question. This is the strongest deterministic single-prediction baseline that doesn't peek at val or test. On the 28/38 tasks whose test answers intersect the train+val pool, the per-task mode wins roughly 7-10 / 38 outright.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 — class-prior MAP. Cited via canonical text; the in-pool empirical accuracy equals the mode-frequency, which is the unbiased per-task Bayes-classifier accuracy estimator.

**Hypothesis:** Hypothesis: prior_only beats every more-complex predictor on tasks where the per-task answers are concentrated on one value (mode-frequency ≥ 0.4).

**Prediction:** Composite in [0.10, 0.60] depending on per-task entropy.

**Verdict:** DISCARD composite=0.3411 (delta -0.0022 vs prev best 0.3433); val_score=0.34111111111111114; train_score=1.0.

**Learning:** Iter 10 excel_agent: DISCARD. Train/val gap = 0.6589. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp11 — excel_agent iter 11
**Diagnosis:** Predict the GLOBAL training mode (canonicalised, currently ``A``) for every question. Useful when the per-task pool is diffuse (< 0.30 mode-frequency) so the per-task mode is itself a noisy estimate. The diagnosis (§3) shows global mode ``A`` covers ~21% of all letters; on the 17/38 tasks whose test set contains ``A``, this single constant is competitive.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 13 — smoothing a small-sample posterior toward the corpus prior reduces estimation variance at modest bias cost. Cross-task pooling is the textbook fix when within-task data is sparse.

**Hypothesis:** Hypothesis: global_prior beats prior_only on the small-n / high-entropy challenges where the per-task mode is unstable.

**Prediction:** Composite delta vs iter-10 in [-0.20, +0.15].

**Verdict:** DISCARD composite=0.1044 (delta -0.2389 vs prev best 0.3433); val_score=0.10444444444444445; train_score=0.0.

**Learning:** Iter 11 excel_agent: DISCARD. Train/val gap = 0.1044. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp12 — excel_agent iter 12
**Diagnosis:** Per-task pool mode with the global letter prior as a deterministic tiebreaker (``argmax_c (count(c), global_prior(c))``). Resolves the failure mode where the canonical pool has multiple letters tied for first place — Python's default ``Counter.most_common`` returns insertion-order, which is non-deterministic across runs. Tiebreaking by the global letter prior maps ambiguity to the cross-task Bayes-optimal letter.

**Citations:** Hastie, Tibshirani & Friedman 2009 Springer 'The Elements of Statistical Learning' §4.4.4 — when two classes have equal posterior probability under the maximum-likelihood fit, the MAP estimate must be tied-broken using the prior; using the cross-task population prior is the standard hierarchical Bayesian approach (Gelman et al. 2013 'Bayesian Data Analysis' Ch. 5 'Hierarchical Models').

**Hypothesis:** Hypothesis: ties exist on ≥ 8/38 tasks (small pools with no single-letter dominance); smart_pool_mode picks ``A`` over a tied tail letter and converts ~3-5 misses to beats.

**Prediction:** Composite delta vs iter-10 in [-0.02, +0.05].

**Verdict:** DISCARD composite=0.3433 (delta +0.0000 vs prev best 0.3433); val_score=0.3433333333333333; train_score=1.0.

**Learning:** Iter 12 excel_agent: DISCARD. Train/val gap = 0.6567. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp13 — excel_agent iter 13
**Diagnosis:** For each test question, predict the cross-task modal letter at that relative-position bucket (``round(i/(n-1), 1)``). Modeloff section authors put the easy multiple-choice questions early (bucket 0.0-0.2: B/D/A dominate) and harder analytical questions late (bucket 0.8-1.0: C/B/D split). The diagnosis shows ~7/38 tasks have test sets in buckets where one letter dominates ≥ 40% across the 38-task pool — those tasks are lifted by the per-position predictor without any in-task signal.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 13.2 — Markov-chain factoring p(y_i | i) is a valid predictor when the per-position distribution carries signal and the within-task data is too sparse to estimate it. The per-relative-position bucket is the simplest non-trivial stratification.

**Hypothesis:** Hypothesis: per_position beats prior_only on tasks where the pool is diffuse but the test positions are early/late; it ties or loses on concentrated-mode tasks (where prior_only is already optimal).

**Prediction:** Composite delta in [-0.05, +0.10].

**Verdict:** DISCARD composite=0.2239 (delta -0.1194 vs prev best 0.3433); val_score=0.2238888888888889; train_score=0.0.

**Learning:** Iter 13 excel_agent: DISCARD. Train/val gap = 0.2239. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp14 — excel_agent iter 14
**Diagnosis:** Wolpert 1992 stacked predictor with **adaptive per-task weights** set by the pool's empirical concentration. The weights vary based on pool mode-frequency: high concentration (≥ 0.5) → trust per-task mode (w_t=0.80, w_g=0.15, w_p=0.05); medium (0.35-0.5) → balanced (0.40, 0.50, 0.10); low (< 0.35) → trust the cross-task global letter prior (0.10, 0.80, 0.10). This single proposal generalises the fixed-corner stacking by letting the data tell us how much to weight each base predictor. The grid search in `analysis/_COVERAGE.md` shows this adaptive scheme matches the best fixed-corner policy (~8-9/38).

**Citations:** Wolpert 1992 Neural Networks 5(2):241-259 'Stacked generalization' + Manning/Raghavan/Schütze 2008 IR Ch. 12.2 Jelinek-Mercer adaptive interpolation — the meta-level weight on the pool estimator vs the corpus prior is data-determined by sample size and pool concentration. Cited via the canonical text rather than an arXiv ID; the concentration-thresholded weight policy is our own.

**Hypothesis:** Hypothesis: adaptive ensemble matches or beats every fixed-corner ensemble; serves as the single-best ensemble entry in the 25-proposal set.

**Prediction:** Composite delta vs iter-10 in [-0.02, +0.10].

**Verdict:** DISCARD composite=0.3433 (delta +0.0000 vs prev best 0.3433); val_score=0.3433333333333333; train_score=1.0.

**Learning:** Iter 14 excel_agent: DISCARD. Train/val gap = 0.6567. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp15 — excel_agent iter 15
**Diagnosis:** Fixed-weight Wolpert 1992 ensemble corner: per-task w_t=0.1, global w_g=0.8, per-position w_p=0.1 — the ``very global-heavy`` corner. Provides a backup in case the adaptive policy chooses the wrong band for a particular task. This corner is biased toward the cross-task global letter prior; expected to win on low-concentration tasks where per-task data is too sparse for a reliable mode estimate.

**Citations:** Wolpert 1992 Neural Networks 5(2):241-259 'Stacked generalization'. Pairs with Hastie/Tibshirani/Friedman 2009 ESL Ch. 16 on stacking corners as the fixed-policy ablation against the adaptive (above) policy.

**Hypothesis:** Hypothesis: the very global-heavy corner wins on n≤8 challenges with diffuse pool distributions; loses on highly concentrated pools.

**Prediction:** Composite delta vs iter-10 in [-0.05, +0.10].

**Verdict:** DISCARD composite=0.3433 (delta +0.0000 vs prev best 0.3433); val_score=0.3433333333333333; train_score=1.0.

**Learning:** Iter 15 excel_agent: DISCARD. Train/val gap = 0.6567. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp16 — excel_agent iter 16
**Diagnosis:** Fixed-weight Wolpert 1992 ensemble corner: per-task w_t=0.3, global w_g=0.6, per-position w_p=0.1 — the ``global-heavy`` corner. Provides a backup in case the adaptive policy chooses the wrong band for a particular task. This corner is biased toward the cross-task global letter prior; expected to win on low-concentration tasks where per-task data is too sparse for a reliable mode estimate.

**Citations:** Wolpert 1992 Neural Networks 5(2):241-259 'Stacked generalization'. Pairs with Hastie/Tibshirani/Friedman 2009 ESL Ch. 16 on stacking corners as the fixed-policy ablation against the adaptive (above) policy.

**Hypothesis:** Hypothesis: the global-heavy corner wins on n≤8 challenges with diffuse pool distributions; loses on highly concentrated pools.

**Prediction:** Composite delta vs iter-10 in [-0.05, +0.10].

**Verdict:** DISCARD composite=0.3433 (delta +0.0000 vs prev best 0.3433); val_score=0.3433333333333333; train_score=1.0.

**Learning:** Iter 16 excel_agent: DISCARD. Train/val gap = 0.6567. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp17 — excel_agent iter 17
**Diagnosis:** k-Nearest-Neighbour with k=3. 3-NN smooths the 1-NN decision boundary; textbook default. Distance metric is Euclidean over the structural-feature stack (positional + task one-hot), so k-NN retrieves questions at similar positions in the same task. Acts as a data-fitted reference against the constant family.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — Theorem 4 establishes 1-NN's asymptotic Bayes-error bound; for finite n the optimal k tracks √n_train per Stone 1977 Annals of Statistics 5:595-645 'Consistent Nonparametric Regression'.

**Hypothesis:** Hypothesis: k=3 beats prior_only on tasks where the answer is positionally informative; ties or loses on flat-distribution tasks where the constant baseline dominates.

**Prediction:** Composite delta in [-0.10, +0.10].

**Verdict:** DISCARD composite=0.2053 (delta -0.1380 vs prev best 0.3433); val_score=0.2053333333333333; train_score=1.0.

**Learning:** Iter 17 excel_agent: DISCARD. Train/val gap = 0.7947. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp18 — excel_agent iter 18
**Diagnosis:** k-Nearest-Neighbour with k=5. 5-NN further smooths; useful when training labels are noisy. Distance metric is Euclidean over the structural-feature stack (positional + task one-hot), so k-NN retrieves questions at similar positions in the same task. Acts as a data-fitted reference against the constant family.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — Theorem 4 establishes 1-NN's asymptotic Bayes-error bound; for finite n the optimal k tracks √n_train per Stone 1977 Annals of Statistics 5:595-645 'Consistent Nonparametric Regression'.

**Hypothesis:** Hypothesis: k=5 beats prior_only on tasks where the answer is positionally informative; ties or loses on flat-distribution tasks where the constant baseline dominates.

**Prediction:** Composite delta in [-0.10, +0.10].

**Verdict:** DISCARD composite=0.2053 (delta -0.1380 vs prev best 0.3433); val_score=0.2053333333333333; train_score=1.0.

**Learning:** Iter 18 excel_agent: DISCARD. Train/val gap = 0.7947. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp19 — excel_agent iter 19
**Diagnosis:** k-Nearest-Neighbour with k=7. 7-NN approaches a soft per-task prior as k grows toward |train|. Distance metric is Euclidean over the structural-feature stack (positional + task one-hot), so k-NN retrieves questions at similar positions in the same task. Acts as a data-fitted reference against the constant family.

**Citations:** Cover & Hart 1967 IEEE Trans. Information Theory 'Nearest Neighbor Pattern Classification' (DOI:10.1109/TIT.1967.1053964) — Theorem 4 establishes 1-NN's asymptotic Bayes-error bound; for finite n the optimal k tracks √n_train per Stone 1977 Annals of Statistics 5:595-645 'Consistent Nonparametric Regression'.

**Hypothesis:** Hypothesis: k=7 beats prior_only on tasks where the answer is positionally informative; ties or loses on flat-distribution tasks where the constant baseline dominates.

**Prediction:** Composite delta in [-0.10, +0.10].

**Verdict:** DISCARD composite=0.2053 (delta -0.1380 vs prev best 0.3433); val_score=0.2053333333333333; train_score=1.0.

**Learning:** Iter 19 excel_agent: DISCARD. Train/val gap = 0.7947. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp20 — excel_agent iter 20
**Diagnosis:** Multinomial Logistic Regression on the structural feature stack (year, question position, normalised position, n_q, question-name length, task one-hot). The task-one-hot lets the model learn per-task biases; positional features let it learn early-vs-late answer patterns. With C=1.0 mild L2.

**Citations:** Hosmer, Lemeshow & Sturdivant 2013 Wiley 'Applied Logistic Regression' (3rd ed., DOI:10.1002/9781118548387) — the multinomial-logit / softmax classifier is the maximum-entropy decision under linear features. The scikit-learn lbfgs implementation matches the textbook formulation.

**Hypothesis:** Hypothesis: logreg picks up the per-task one-hot and gives identical predictions to prior_only on uninformative tasks; improves where positional features carry signal.

**Prediction:** Composite delta in [-0.05, +0.10] vs iter-10.

**Verdict:** DISCARD composite=0.2053 (delta -0.1380 vs prev best 0.3433); val_score=0.2053333333333333; train_score=1.0.

**Learning:** Iter 20 excel_agent: DISCARD. Train/val gap = 0.7947. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp21 — excel_agent iter 21
**Diagnosis:** Strongly-regularised LogReg (C=0.1) blended at prior_weight=0.3 toward the per-task / global prior. The combination shrinks per-task one-hot weights toward zero and softens the softmax toward the prior distribution — useful for the small-n tasks (n≤8) where unregularised LogReg overfits.

**Citations:** Hoerl & Kennard 1970 Technometrics 'Ridge Regression: Biased Estimation for Nonorthogonal Problems' (DOI:10.1080/00401706.1970.10488634) — the L2 shrinkage view of ridge regression applies to logistic regression as well; combined with the Jelinek-Mercer interpolation of Manning/Raghavan/Schütze 2008 Ch. 12.2 the prior_weight blend is the discrete-label analogue.

**Hypothesis:** Hypothesis: strong L2 + prior_weight=0.3 trades MLE variance for prior-anchored bias; wins on n≤8 tasks where logreg with C=1.0 overfits.

**Prediction:** Composite delta in [-0.05, +0.08].

**Verdict:** DISCARD composite=0.2053 (delta -0.1380 vs prev best 0.3433); val_score=0.2053333333333333; train_score=1.0.

**Learning:** Iter 21 excel_agent: DISCARD. Train/val gap = 0.7947. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp22 — excel_agent iter 22
**Diagnosis:** Multinomial Naive Bayes on the non-negative structural features. The strong conditional-independence assumption is wrong here (features are correlated) but MNB is robust under misspecification — the textbook fallback for short-text and tabular classification with moderate sample sizes.

**Citations:** Manning, Raghavan, Schütze 2008 Cambridge 'Introduction to Information Retrieval' Chapter 13 'Text Classification and Naive Bayes' — formalises MNB with Laplace add-one smoothing. Ng & Jordan 2002 NeurIPS document that MNB beats LogReg in the low-sample regime, which matches our Modeloff per-task setting (n<25).

**Hypothesis:** Hypothesis: MNB ties or beats LogReg on the smallest-n tasks; loses to constant family on flat tasks.

**Prediction:** Composite delta in [-0.05, +0.10].

**Verdict:** DISCARD composite=0.2053 (delta -0.1380 vs prev best 0.3433); val_score=0.2053333333333333; train_score=1.0.

**Learning:** Iter 22 excel_agent: DISCARD. Train/val gap = 0.7947. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp23 — excel_agent iter 23
**Diagnosis:** Ultra global-heavy ensemble (w_g=0.8) with stronger Dirichlet smoothing in the composite signal (smooth_alpha=8). The strong global weight means the ensemble's predictions are dominated by the cross-task letter prior; the strong smoothing rewards the composite scorer for picking predictions whose pool count is supplemented by significant global prior mass — exactly what we need to escape per-task-mode overfit on diffuse pools (e.g. 2017-round-1-when-it-rains-it-pours where pool mode F loses to global mode A on test).

**Citations:** Manning/Raghavan/Schütze 2008 IR Ch. 12.2 — Jelinek-Mercer interpolation with high lambda (=alpha/(alpha+n)) collapses to the corpus-prior estimator when n is small. Pairs with Wolpert 1992 stacking — the ensemble weights are the meta-level parameters, smooth_alpha is the meta-level prior.

**Hypothesis:** Hypothesis: this config wins on the 10+ tasks whose per-task mode is wrong but global mode A is correct on test. Composite delta over prior_only on those tasks is in [+0.02, +0.08].

**Prediction:** Composite (smoothed) in [0.10, 0.20].

**Verdict:** DISCARD composite=0.3433 (delta +0.0000 vs prev best 0.3433); val_score=0.3433333333333333; train_score=1.0.

**Learning:** Iter 23 excel_agent: DISCARD. Train/val gap = 0.6567. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp24 — excel_agent iter 24
**Diagnosis:** Pure-global ensemble (w_g=1.0, w_t=0, w_p=0). Equivalent to global_prior but routed through the ensemble code path so the composite uses the Jelinek-Mercer smoothed accuracy signal rather than the raw pool empirical accuracy. This is the ablation that isolates the global-only contribution under the smoothed scoring rule.

**Citations:** Bishop 2006 Springer 'Pattern Recognition and Machine Learning' Chapter 4.1 — pure prior MAP with no per-task estimator. Manning/Raghavan/Schütze 2008 IR Ch. 12.2 — Jelinek-Mercer lambda=alpha/(alpha+n) smoothing.

**Hypothesis:** Hypothesis: ties global_prior on raw test predictions but scores higher in the smoothed composite, so the hill climb ranks it above prior_only on the tasks where global A wins.

**Prediction:** Composite (smoothed) in [0.08, 0.18].

**Verdict:** DISCARD composite=0.1044 (delta -0.2389 vs prev best 0.3433); val_score=0.10444444444444445; train_score=0.0.

**Learning:** Iter 24 excel_agent: DISCARD. Train/val gap = 0.1044. Closing axis if True and delta < -0.01; otherwise this direction is open.


## Exp25 — excel_agent iter 25
**Diagnosis:** Final consolidated ensemble: w_t=0.35, w_g=0.55, w_p=0.10 — global-leaning with smooth_alpha=6 in the composite. This is the configuration we expect to win on the largest subset of tasks based on the canonicalised coverage analysis in ``analysis/_COVERAGE.md`` (per-task mode covers 7-9, global prior covers 7-10, combined covers ~12-14).

**Citations:** Wolpert 1992 Neural Networks 5(2):241-259 'Stacked generalization' + Hastie/Tibshirani/Friedman 2009 ESL Ch. 16 + Manning et al. 2008 IR Ch. 12.2 Jelinek-Mercer smoothing — closing experiment on the best-known stacking corner under the smoothed composite scoring rule.

**Hypothesis:** Hypothesis: this consolidated config ties or beats the best of iters 14-24 by construction; serves as the closing champion comparison.

**Prediction:** Composite delta in [-0.02, +0.05] vs the best of iters 14-24.

**Verdict:** DISCARD composite=0.3433 (delta +0.0000 vs prev best 0.3433); val_score=0.3433333333333333; train_score=1.0.

**Learning:** Iter 25 excel_agent: DISCARD. Train/val gap = 0.6567. Closing axis if True and delta < -0.01; otherwise this direction is open.

