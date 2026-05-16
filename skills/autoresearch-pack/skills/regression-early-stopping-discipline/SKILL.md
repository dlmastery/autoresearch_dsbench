---
name: regression-early-stopping-discipline
description: Sklearn early-stopping val > train is NORMAL (not leakage). MLPRegressor(early_stopping=True) reserves an internal validation slice — post-fit train_score underestimates true train. Bishop 2006 PRML §5.5.2. Triggers on "early stopping", "val > train", "MLPRegressor", "leakage false positive", "sklearn neural", "validation_fraction".
metadata:
  category: verification
  source: dsbench
  related: [forensic-audit-pipeline, problem-type-aware-audit-thresholds, experiment-design]
---

# Regression Early-Stopping Discipline (val > train is normal)

## When to use

- Reviewing a forensic-audit "anomaly: val > train" warning on a regression task.
- Building a regression baseline with `sklearn.neural_network.MLPRegressor`.
- Comparing two backbones where one uses early-stopping and the other doesn't, and the train scores disagree by 5+ points.
- Choosing whether to enable `early_stopping=True` for an MLP / Logistic / GBM that supports it.

## The rule

`sklearn.neural_network.MLPRegressor(early_stopping=True)` (and the analogous `MLPClassifier`, `SGDRegressor`, etc.) by default:

1. Reserves `validation_fraction=0.10` of the training data as an INTERNAL validation slice.
2. Selects the stopping epoch by minimising loss on that slice.
3. **After training, `model.score(X_train, y_train)` is computed on the FULL X_train passed in (including the reserved slice).** But the slice was effectively part of the training-time signal — the model was selected to fit it well. So the post-fit train score is biased toward optimistic.
4. Meanwhile, `model.score(X_val, y_val)` is computed on the held-out outer val set — never seen during training. That score is unbiased.

The result: when the inner-slice fit happens to be a hard subset of the training distribution, the post-fit `model.score(X_train)` UNDERESTIMATES the true train performance, and the outer `model.score(X_val)` is therefore **higher than the reported train score**. This is NORMAL, NOT LEAKAGE — see Bishop 2006 PRML §5.5.2.

The forensic-audit rule (suppress the "anomaly: val > train" warning) requires ALL of:

- `model_type == sklearn.MLPRegressor` (or MLPClassifier, SGDRegressor with `early_stopping=True`).
- `early_stopping == True` in the saved config.
- gap = `val_score - train_score` ≤ 0.05.

Beyond 0.05 (e.g. val > train + 0.10), even sklearn early-stopping shouldn't produce that big a gap — the warning re-enables.

## Anti-patterns

- **Disabling early-stopping to "fix" the val > train warning.** Worse: the model now overfits without the slice-based stop, producing a real (rather than apparent) generalisation gap.
- **Reporting `model.score(X_train, y_train)` without noting `early_stopping=True`.** The reader can't distinguish "model is genuinely better on val" from "post-fit train is biased low".
- **Comparing an early-stopping model to a non-early-stopping model using raw train_score.** Apples-to-oranges; report both with and without internal-slice exclusion, OR report only val for the comparison.
- **Suppressing the warning for ALL sklearn models.** It's specific to early-stopping-enabled estimators with an internal slice; a plain `RandomForestRegressor` with val > train IS suspicious.
- **Suppressing the warning for ALL gaps.** A 0.20 gap is still suspect even with early-stopping; the 0.05 threshold catches the design-correct asymmetry and re-enables the warning for genuine leakage.

## Implementation checklist

1. `framework/forensic_audit.py` reads the saved config and checks `model_type` + `early_stopping`.
2. Suppression case is LOGGED: `agent_E: SUPPRESSED — sklearn MLPRegressor early_stopping=True, gap=0.034`.
3. Champion README (per `winner-archive-protocol`) documents the early-stopping setup and the expected post-fit train-bias direction.
4. Unit test: fit `MLPRegressor(early_stopping=True)` on a noisy synthetic regression; assert `val_score ≥ train_score - 0.05` in 9 out of 10 random seeds (the bias should occur typically).
5. Unit test: refit the same task with `early_stopping=False`; assert `train_score ≥ val_score - 0.05` (no internal slice → no bias).

## References

- Source: `framework/CLAUDE_template.md` section "Sklearn Early-Stopping Val > Train Is Normal".
- Source: `framework/forensic_audit.py` agent E suppression case.
- Bishop (2006) "Pattern Recognition and Machine Learning" §5.5.2 — early-stopping as implicit regularisation; train/val asymmetry under internal-slice selection.
- Scikit-learn user guide §1.17.2 — `MLPRegressor.early_stopping` and `validation_fraction` parameters.
- Related: `forensic-audit-pipeline`, `problem-type-aware-audit-thresholds`, `experiment-design`, `traditional-ml-metrics`.
