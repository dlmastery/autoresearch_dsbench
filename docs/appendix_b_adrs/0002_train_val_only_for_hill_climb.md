# ADR-0002: Hill-climb on train + val only; touch test once via `final_report.py`

## Status

Accepted (2026-05-15). Lesson 13 in `framework/CLAUDE_template.md`.

## Context

The fundamental DSBench-comparison claim — "we beat the DSBench baseline on task X" — is only credible if the test set never influenced any hill-climbing decision. Test leakage in 112 parallel autoresearch loops has many failure modes:

- A runner that reads `X_test` to "monitor convergence".
- A hill-climb proposal that conditions on test-set distribution.
- An audit step that uses test labels to verify the model output.

All three are invisible to a reviewer reading the final number. The only defence is structural: make it physically impossible for the test set to enter the loop, then audit that the invariant holds.

## Decision

**Three enforcement mechanisms**, layered:

1. **Code-gen invariant.** `framework/generate_scaffolds.py` writes per-task `run_autoresearch.py` and `hill_climb.py` wrappers that never reference `X_test` or `y_test`.
2. **Runtime invariant.** `framework/runner.py:run_one` predicts on `X_train` and `X_val` only. Composite = `min(val, train) - 0.05 * |val - train|` for tabular; LOO-CV on `train ∪ val` for `qa_excel`.
3. **Forensic invariant.** Forensic Agent F greps the per-task `run_autoresearch.py` / `hill_climb.py` for `X_test` / `y_test`; ANY reference is a FAIL. Forensic Agent A re-hashes the test split pre/post run to confirm no read happened.

`framework/final_report.py` is the **single** code path that touches the test set, per task. It runs ONCE per task, refits the champion (train-only for tabular; `train ∪ val` for `qa_excel` per ADR-0009), scores on test, writes `final_report.json`.

## Consequences

**Easier:**

- A reviewer can ground the BEAT-DSBENCH claim on a single grep + a single hash comparison.
- The hill-climb loop is composable — `run_one` is a pure function of `(train, val, params)`.
- Adding a new audit agent requires no change to the runner.

**Harder:**

- Validating a single experiment in isolation requires loading the full split and computing the test score by hand (the runner won't do it for you).
- The dashboard physically has no test-metric column for non-champion rows — extending it requires a deliberate design decision, not a one-line code change.

**Riskier:**

- A bug in `final_report.py` (e.g., the regression-delta-sign bug — see [`../appendix_a_postmortems/0001_regression_delta_sign_bug.md`](../appendix_a_postmortems/0001_regression_delta_sign_bug.md)) reaches every task's reported test score simultaneously. The mitigation is full unit-test coverage on the metric and delta math.

## Related

- [`../appendix_b_adrs/0015_four_layer_audit_gate.md`](0015_four_layer_audit_gate.md)
- [`../appendix_d_diagrams/per_task_split.mmd`](../appendix_d_diagrams/per_task_split.mmd)
- Skills `data-integrity-rules`, `train-val-test-invariants`.
- `framework/CLAUDE_template.md` § "Data Integrity" and "Validation Checklist".
