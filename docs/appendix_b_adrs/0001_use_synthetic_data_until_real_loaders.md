# ADR-0001: Use synthetic Gaussian data until real loaders are wired

## Status

Accepted (2026-05-15).

## Context

The DSBench benchmark spans 74 Kaggle competitions (modeling) and 38 Modeloff challenges (analysis). Pulling each Kaggle dataset requires per-competition credentials, accepting per-competition rules, and ~10-50 GB of disk. Pulling the Modeloff datasets requires opening Excel sheets and answering financial-modelling questions by hand. Wiring 112 real loaders before the framework is even validated is risk-stacking: a bug in `runner.py` would mean re-downloading 100 GB to retry.

The autoresearch protocol is **agnostic** to data semantics — it cares about splits, hashes, and the composite metric. We can therefore stand up the entire pipeline on **synthetic** data, validate the 4-layer audit, the hill-climb, the dashboards, and the submission archive, then wire real loaders one task family at a time.

`framework/runner.py:load_or_make_data` builds:

- For `classification_binary`: `X ~ N(0, I)` of shape `(2000, 32)`, `y = sigmoid(Xw) > 0`.
- For `classification_multiclass`: same `X`, `y = argmax(XW)` with 4-column `W`.
- For `regression`: `y = Xw + 0.2 * noise`.
- For `structured`: same as binary classification with explicit framing.

The split is the canonical 70/15/15 random permutation seeded at 42, and is hash-cached to `.data_cache/splits.npz`.

## Decision

Ship the framework with synthetic data and the 4-layer audit gate. **Real loaders are wired per-task on demand**, replacing the synthetic loader only when the human commits to running that specific task against its DSBench baseline. The `qa_excel` loader was wired first (it has documented real-data answer keys); other task families follow when needed.

## Consequences

**Easier:**

- Framework can be reviewed end-to-end with `pytest`-like determinism.
- A new contributor can run all 112 hill-climbs locally in a day on synthetic data — exercising every audit path.
- The Titanic real-data champion at val ROC-AUC 0.9573 / test 0.9624 proves the pipeline works on real data, while the synthetic baseline confirms the audit triggers correctly on every task.

**Harder:**

- Comparing test scores against the DSBench paper is **only meaningful** on tasks with real data wired. The synthetic ceilings are bounded by the noise distribution we chose.
- A reviewer reading a per-task `final_report.json` for a synthetic-loader task must understand the score is calibrated against synthetic, not real.

**Riskier:**

- A real-loader bug at integration time may surface a forensic-audit failure that the synthetic loader hid. Mitigated by Agent A (split-hash) and Agent F (static-code) which still pass on real data.

## Related

- Postmortem [`../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md`](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md) — the bug that motivated wiring the real `qa_excel` loader before any other family.
- Skill `data-integrity-rules` in the autoresearch pack.
- `framework/runner.py:load_or_make_data` and `framework/runner.py:_load_qa_excel`.
