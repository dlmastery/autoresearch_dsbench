# Appendix A — Postmortems

> Five engineering postmortems in Five-Whys + Action-Items format. Each one explains a real bug or near-bug, what it cost us, and the tooling change that prevents recurrence.

These are **engineering** postmortems, not production-incident postmortems. The project is single-operator, batch, offline — there are no SLOs, no on-call rotations. The failure mode of an engineering postmortem is: a bug landed, we discovered it, here is what we now do differently.

| ID | Title | Class | Key tooling change |
|---|---|---|---|
| [0001](0001_regression_delta_sign_bug.md) | Regression delta-sign bug flipped 16 wins to losses | Correctness | Metric-sign convention (Lessons-Learned row 18); skill `metric-sign-convention`. |
| [0002](0002_excel_agent_synthetic_placeholder.md) | Excel agent shipped on synthetic data; 1/38 ceiling | Correctness | Real Modeloff data loader; `qa-task-feature-engineering` skill; [ADR 0001](../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md). |
| [0003](0003_forensic_false_positive_val_gt_train.md) | Forensic Agent E flagged sklearn early-stop as leakage | False positive in audit | Agent E whitelist; `regression-early-stopping-discipline` skill; [ADR 0010](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md). |
| [0004](0004_conways_problem_type_misroute.md) | Conway's Reverse Game of Life misrouted as binary classification | Routing | `structured` branch in `runner._score`; problem-type-aware dispatch. |
| [0005](0005_git_push_ssl_cert_failure.md) | `git push` blocked by SSL certificate error on Windows | Tooling | schannel → openssl SSL backend swap; one-time global git config. |

## Format

Each postmortem follows a uniform structure:

1. **TL;DR** — one-paragraph summary.
2. **Timeline** — observable events in order, with timestamps.
3. **Root cause** — technical + systemic.
4. **Impact** — what broke and what didn't.
5. **What went well** — the parts of the system that surfaced the bug.
6. **What went badly** — the parts that should have surfaced it earlier.
7. **Action items** — owner, status, tracking pointer.
8. **Related** — ADRs, skills, code paths.

## Reading order

Start with [postmortem 0002](0002_excel_agent_synthetic_placeholder.md) — it is the most consequential of the five and the one that most-directly motivated the four-layer audit gate. Then [postmortem 0003](0003_forensic_false_positive_val_gt_train.md) for the calibration story; then [postmortem 0001](0001_regression_delta_sign_bug.md) for the metric-sign story. Postmortem 0004 (problem-type routing) and 0005 (SSL) are tooling-only.
