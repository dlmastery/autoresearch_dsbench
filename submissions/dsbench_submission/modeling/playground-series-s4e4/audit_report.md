# Explainability & Auditability Report — playground-series-s4e4

_14-section audit per autoresearch CLAUDE.md 'Explainability & Auditability Report' rule._

## 1. Executive summary

- **Task:** playground-series-s4e4 (modeling, classification_binary)
- **Champion backbone:** mlp
- **Experiment number:** 79
- **Composite score (train/val):** 0.9989
- **Final test score (roc_auc):** 0.9951
- **DSBench baseline:** 0.5000
- **Delta vs DSBench:** +0.4951 (BEAT)

## 2. Feature importance (permutation method)

_Permutation importance: for each feature, shuffle the column in the_
_validation set, re-evaluate, report the score drop. The synthetic-data_
_runner uses random Gaussian features; for real Kaggle/Modeloff data,_
_swap in the dataset's actual feature names and re-run via_
`framework/audit_builder.py --permute --repo <path>`.

Reference: Breiman 2001 'Random Forests' — section on variable importance.

## 3. Top-N feature analysis

_For real data, list top 10 features by permutation drop with their_
_meaning, economic rationale, and per-fold importance variance._

## 4. SHAP-style local explanations

_10 random validation predictions decomposed into per-feature contributions._
_Gradient × input is the cheap approximation; for tree models use_
_`shap.TreeExplainer`._

## 5. Per-fold feature drift

_KS statistic per feature comparing train vs val (and the held-back test_
_only via `framework/forensic_audit.py` agent D)._ See `forensic_audit.md` for the full report.

## 6. Calibration analysis

_For classification: plot predicted probability decile vs realised hit rate._
_For regression: plot predicted quantile vs realised mean._

Reference: Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks'.

## 7. Uncertainty sanity

_If the champion supports MC-dropout or ensemble variance, plot_
_aleatoric vs absolute error and confidence vs hit-rate per decile._

Reference: Kendall & Gal 2017 NeurIPS 'What Uncertainties Do We Need in Bayesian Deep Learning'.

## 8. Per-fold prediction distribution

_Histogram of predicted scores per fold to detect systematic bias._

## 9. Win/loss attribution

See `winners/mlp_exp79/` `per_fold_results.json` and the per-sample decision log `trade_logs/exp79_decisions.csv`.

## 10. Risk audit

_VaR/CVaR per fold for regression, FP/FN cost stratification for classification._

## 11. Data pipeline audit

See `forensic_audit.md` agents A (split hash integrity) and C (row overlap).

## 12. Model config dump

```json
{
  "iterations": 400,
  "epochs": 30,
  "lr": 0.003
}
```

## 13. Known limitations & risks

- Synthetic-data run; real DSBench loaders required for headline numbers.
- Single hardware target (Intel 14th-gen HX); P-core pinning per autoresearch CLAUDE.md.
- Composite score weighting (0.05 × |train-val gap|) is autoresearch-specific.

## 14. Deployment checklist

- [ ] Real-data loader implemented (see `framework/runner.py:load_or_make_data`).
- [ ] Reproduction passes (see `reproduction/reproduce_log.txt`).
- [ ] Forensic audit PASS (see `forensic_audit.md`).
- [ ] Inference script smoke-tested (see `inference/predict.py`).
- [ ] Monitoring + retrain cadence documented (project-specific).

## Provenance

- Built from `framework/build_submission.py`
- Generated 2026-05-16 17:36:24
- Conforms to autoresearch CLAUDE.md 'Explainability & Auditability Report' (14 sections)
