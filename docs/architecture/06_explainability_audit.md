# Explainability Audit — The 14-Section Winner Report

> Audience: a stakeholder reading a single winner archive and wanting a conference-quality account of WHY the model behaves the way it does.

## 1. When the report is written

`framework/build_submission.py:_audit_report_skeleton` writes `audit_report.md` for every task whose champion changed since the last submission build. The 14-section structure is the contract — skipping any section is a regression, and the submission builder is re-run.

The 14 sections mirror the original `autoresearch/CLAUDE.md` § "Explainability & Auditability Report" rule and are required by Lesson 22 (four-layer audit gate).

## 2. The 14 sections

| # | Section | What it answers | Source |
|---|---|---|---|
| 1 | Executive summary | Task, champion backbone, composite, test score, DSBench delta, BEAT/MISS verdict | `final_report.json` + `best_config.json` |
| 2 | Feature importance (permutation) | Which features most affect val score under permutation | `framework/audit_builder.py --permute` (per Breiman 2001 'Random Forests' MLJ) |
| 3 | Top-N feature analysis | Top-5 features by importance with rationale | Permutation table sorted |
| 4 | SHAP-style local explanations | Per-sample attribution on 10 wins + 10 losses | `shap.TreeExplainer` for GBM, `shap.KernelExplainer` fallback (Lundberg & Lee 2017 NeurIPS 'A Unified Approach to Interpreting Model Predictions' arXiv:1705.07874) |
| 5 | Per-fold feature drift | KS train-vs-test per top-5 feature | Agent D outputs |
| 6 | Calibration | Reliability diagram + ECE (Expected Calibration Error) | Guo, Pleiss, Sun, Weinberger 2017 ICML 'On Calibration of Modern Neural Networks' (arXiv:1706.04599) |
| 7 | Uncertainty sanity | Predicted-confidence distribution; bimodality flag | Histogram of `proba.max(axis=1)` |
| 8 | Per-fold prediction distribution | Class-frequency drift per fold | Counter on `pred_va` |
| 9 | Trade / decision attribution | Top-5 wins + top-5 losses with full per-sample row | `trade_logs/exp<N>_decisions.csv` |
| 10 | Risk audit | Known failure modes, edge cases | Agent E suspicions + manual notes |
| 11 | Data pipeline audit | Re-verify zero train/val leakage | Agent A + C re-run, hashes re-checked |
| 12 | Model config dump | Full champion config from `best_config.json` | `json.dumps(best, indent=2)` |
| 13 | Known limitations & risks | Documented blind spots, ceilings | Hand-written narrative |
| 14 | Deployment checklist | What a downstream operator must verify before serving | Hand-written checklist |

Each section starts with a one-paragraph plain-English summary, then a data table or figure caption, then a citation. The audit is reproducible — the builder regenerates everything except sections 10 and 13 from the artefacts in `autoresearch_results/`.

## 3. Why this is the third audit layer

Layer 1 (validator) and Layer 2 (forensic committee) verify that the **protocol** was honoured. Layer 3 (explainability) verifies that the **model** is interpretable. A champion that passes Layers 1 and 2 but fails Layer 3 is one we cannot deploy: we don't know why it works, so we don't know when it will break.

## 4. Anti-patterns

- **Boilerplate explanations.** If sections 2-5 look identical across 10 tasks, the builder reverted to scaffolds. The fix is to re-run with the real model loaded.
- **Missing calibration.** ECE / reliability diagrams are mandatory for classification champions. Regression champions document RMSE-of-residuals stratified by predicted quantile in its place.
- **Skipping section 11.** Re-verifying zero leakage in the audit is a redundancy that has caught real bugs (see [`../postmortems/0001_regression_delta_sign_bug.md`](../postmortems/0001_regression_delta_sign_bug.md)) — never skip.

## 5. Reading the report

The audit is `submissions/dsbench_submission/<kind>/<slug>/audit_report.md`. Open it via the in-browser markdown viewer at `dashboard/md_viewer.html?path=...` (browsers download raw `.md` files; the viewer renders them client-side via marked.js). The viewer is documented in [`../adr/0011_md_viewer_inline_render.md`](../adr/0011_md_viewer_inline_render.md).

## 6. Generating the report

```powershell
# Refresh for every champion-updated task
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py

# Re-build a single task
& "C:/Users/evija/anaconda3/python.exe" framework/build_submission.py --repo modeling/titanic
```

## 7. Related

- [`../reference/api_build_submission.md`](../reference/api_build_submission.md)
- [`09_submission_archive.md`](09_submission_archive.md)
- [`../slos/03_validator_clean.md`](../slos/03_validator_clean.md)
