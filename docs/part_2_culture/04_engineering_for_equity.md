# Chapter 4 — Engineering for Equity

> *Parallel to:* SWE-book Chapter 4 *"Engineering for Equity"* (Winters, Manshreck, Wright 2020).

**Thesis.** SWE-book chapter 4 argues that engineering decisions encode value judgements, and a system that treats users uniformly often produces unequal outcomes. The DSBench parallel is benchmark fairness: a benchmark that *appears* to give every task the same evaluation can in fact systematically advantage one task family over another. Engineering for equity in our project means **giving every task family — tabular, NLP, time-series, structured, qa_excel — a fair evaluation, with the same audit, the same documentation, and the same Test-Set Embargo**.

## 4.1 The fairness target in ML benchmarks

In SWE-book chapter 4 the equity target is human user groups; in our project the target is *task families*. The 112 DSBench tasks split into:

| Family | Count | Problem type | Natural evaluation |
|---|---|---|---|
| Tabular binary | 56 | classification_binary | ROC-AUC |
| Tabular regression | 16 | regression | RMSE / MAE |
| Tabular multiclass | 1 | classification_multiclass | macro-F1 / accuracy |
| Structured | 1 | structured (Conway's reverse Game-of-Life) | exact-match accuracy |
| NLP regression | 8 (subset of modeling) | regression on text | RMSE |
| Time-series | 8 (subset of modeling) | regression / forecast | RMSE |
| qa_excel | 38 (all analysis) | discrete-choice on Excel-derived features | accuracy |

These families have wildly different natural difficulties. A binary tabular task with 60k rows can be solved by XGBoost defaults to 95 %+ ROC-AUC. A qa_excel task with 4 questions in its test set has a 50 % standard error on accuracy. *The same audit rule applied uniformly to both produces inequity.*

This is the same problem the SWE-book describes in chapter 4: a uniform process applied to non-uniform inputs amplifies pre-existing disadvantage.

## 4.2 The forensic-audit calibration

Three forensic-audit calibrations exist explicitly to make the evaluation fair across families:

### 4.2.1 Problem-type-aware thresholds

Agent B (target / label leakage) flags features whose mutual information with the label exceeds 0.9 on tabular tasks. For `qa_excel` the threshold is different: the 38-task one-hot encoding is *intentionally* highly informative — it tells the model which Modeloff task this question is from, and the per-task prior is the main signal. A naive threshold would fail every qa_excel task. The `problem-type-aware-audit-thresholds` skill codifies the calibration; `framework/forensic_audit.py:_agent_b` reads the problem type and applies the appropriate threshold.

The same pattern repeats for Agent D (distribution shift, KS test): tabular tasks use a 10 % flagged-feature threshold; qa_excel uses a stride-5 split that is, by design, slightly imbalanced, so the threshold is relaxed.

### 4.2.2 Agent E's sklearn early-stopping whitelist

Agent E catches anomalies: val > train, perfect 1.0 scores, jumps > 0.3 in composite. But sklearn's `MLPClassifier(early_stopping=True)` legitimately produces val > train on regression tasks (the model fits on 90 % of the training set after sklearn's internal 10 % holdout for stopping; the recorded "train" score is on the full training set including data the model never saw). Bishop 2006 *Pattern Recognition and Machine Learning* §5.5.2 explains the mechanism. Failing the audit for this would be inequitable: we'd be punishing the family of estimators that uses early stopping correctly. The whitelist is documented in [ADR 0010](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md).

### 4.2.3 Agent J's "record-only" verdict on backbone diversity

Agent J counts distinct backbones in `experiment_log.jsonl`. Fewer than 3 triggers a *warning*, never a failure. For qa_excel tasks, only one backbone (`excel_agent`) exists — failing for low diversity would be inequitable, since the family literally has only one backbone. The record-only verdict respects the family's structural constraint while still surfacing the data for human review.

## 4.3 The 70 / 15 / 15 split — fairness as a structural choice

Every task gets a 70 / 15 / 15 train / val / test split, hash-pinned in `data/split_manifest.json`. The 15 % test slice is the Test-Set Embargo target ([Ch. 11](../part_3_processes/11_testing_overview.md)). The choice of 15 % (not 20 %, not 10 %) is a fairness choice: it has to be big enough for small-n tasks (qa_excel tasks have 8–10 questions per test set; 15 % of 60 = 9) and small enough not to starve the train set on large tasks.

For qa_excel specifically, the split is a **stride-5 interleaved split**: every 5th question goes to val, every 5th-plus-1 to test, the rest to train. The interleaving (vs random sampling) is what gives small-n tasks a representative test set instead of "all the easy questions in train and all the hard ones in test". See [ADR 0007](../appendix_b_adrs/0007_stride5_interleaved_split_for_qa.md).

This is the same pattern the SWE-book recommends for fairness in product engineering: *expose the structural choice and justify it*, don't bury it in a config file.

## 4.4 Cross-task pooling — fairness for small-n families

The 38 qa_excel tasks have ~10 questions each on average — far too few to train a per-task classifier reliably. The fairness move is **cross-task pooling for training, per-task evaluation**: every task's classifier trains on all 38 tasks' train splits pooled (with the 38-task one-hot encoded as a feature), then scores on its own val and its own test. This gives small-n tasks the statistical power of a 466-row training set while preserving the per-task evaluation contract.

The discipline is codified in:

- The `cross-task-pooling-discipline` skill.
- [ADR 0008](../appendix_b_adrs/0008_cross_task_pooling_for_training.md).
- `framework/runner.py:_pool_train_for_qa` (the implementation).
- Agent C's row-overlap detector (which must distinguish "same row appears in two tasks' train splits — legal" from "same row appears in train and test of the same task — illegal").

Without this, the qa_excel evaluation would be a coin-flip; with it, the qa_excel ceiling is ~17 / 38 (the structural limit set by the 3 pure-numeric / pure-string challenges that need actual Excel parsing — see [`analysis/_DIAGNOSIS.md`](../../analysis/_DIAGNOSIS.md)).

## 4.5 What inequity looks like in practice

Three failure modes the project has actually encountered and fixed:

### 4.5.1 The val > train false positive on regression tasks

Before [ADR 0010](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md), Agent E would flag every regression task that used `MLPRegressor(early_stopping=True)` as anomalous. The val > train pattern is *legitimate* for that estimator family (sklearn holds back an internal 10 % for stopping; the reported train score is over the full training set including the held-back fraction). The fix: whitelist `MLPRegressor early_stopping=True` in Agent E, document the mechanism, cite Bishop 2006 §5.5.2. See [postmortem 0003](../appendix_a_postmortems/0003_forensic_false_positive_val_gt_train.md).

### 4.5.2 The Conway problem-type misroute

The Conway's-Reverse-Game-of-Life task is `problem_type: structured`. An early version of `framework/runner.py:_score` routed it through the regression branch (`metric: rmse`), which silently negated the exact-match accuracy and produced unintelligible composites. The fix: a `structured` branch in `_score` that preserves the higher-is-better convention. See [postmortem 0004](../appendix_a_postmortems/0004_conways_problem_type_misroute.md).

### 4.5.3 The qa_excel synthetic-data placeholder

The original `_excel_agent` ignored the actual Modeloff questions and trained on synthetic Gaussian features (`y = rng.integers(0, 9)`). Every qa_excel task scored 0–22 % on test — chance probability. This was *systematic inequity*: an entire family of 38 tasks was being silently failed because the framework was treating them as a synthetic regression problem. The fix: load real Modeloff answers from `_analysis_data.json`, derive the 9-D structural feature stack, add the 38-task one-hot, ship the `excel_agent` backbone. See [postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md).

The takeaway: equity is not "treat every task identically"; equity is "give every task a fair evaluation according to its structural reality, and audit your audit rules for false positives on the families they were not designed for".

## 4.6 The dashboard equity check

The cross-task dashboard at `dashboard/index.html` has equal column treatment for modeling and analysis tasks. Two tabs (one per kind) with the same sortable columns: composite, val_score, train_score, test_score, dsbench_baseline, delta_vs_dsbench, beats_dsbench, forensic_verdict. The dashboard refuses to display "average performance across tasks" — that aggregation would silently weight 74 large-ish modeling tasks against 38 small-n analysis tasks. Per-task numbers only; the cohort scoreboard is "82/112 BEAT", not "73.2 % average composite".

This is the same pattern the SWE-book recommends for fairness in product metrics: *report the distribution, not just the mean*.

## 4.7 Related

- [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md): the four-layer audit gate.
- [Ch. 14 — Larger Testing](../part_3_processes/14_larger_testing.md): the extended-hill-climb phase as the equity escape hatch for stuck tasks.
- [Appendix A — Postmortems](../appendix_a_postmortems/): five concrete failure modes the audit calibration was built to mitigate.
- [`framework/forensic_audit.py`](../../framework/forensic_audit.py): the implementation of problem-type-aware thresholds.
