# Chapter 13 — Test Doubles

> *Parallel to:* SWE-book Chapter 13 *"Test Doubles"* (Winters, Manshreck, Wright 2020).

**Thesis.** A test double is something that stands in for a real dependency so the test can run. The SWE-book chapter 13 names four kinds: dummy, fake, stub, mock. The DSBench parallel is the **synthetic-data fallback** in `framework/runner.py:load_or_make_data` — when a real Kaggle dataset is not available, the runner generates a deterministic Gaussian-feature dataset with the right shape. The fallback is a deliberate test double, *not* an experimental shortcut, and the project explicitly forbids champions trained on it.

## 13.1 What the synthetic-data fallback does

The function `load_or_make_data(repo, cfg, seed=42)` in `framework/runner.py`:

1. Checks `.data_cache/splits.npz` — if it exists, returns it.
2. If the task is `qa_excel`, loads real Modeloff answers from `_analysis_data.json` and `registry/analysis_tasks.json` and derives features (the 9-D structural stack plus 38-task one-hot).
3. Otherwise, generates **synthetic Gaussian features** with a deterministic seed derived from `cfg.slug`. Shape: 2000 rows × 32 features for tabular tasks. Label generation depends on `problem_type` (binary uses a sigmoidal mixture; multiclass uses a softmax over linear combinations; regression uses a noisy linear function).

The synthetic data is committed via the `.data_cache/splits.npz` file, so once generated it is *reproducible*. The hash is recorded in `data/split_manifest.json`, so the audit can verify the synthetic data hasn't drifted.

## 13.2 Why a fallback exists

The 74 Kaggle modeling tasks in DSBench require downloading the actual competition CSVs from Kaggle. For an arbitrary developer on an arbitrary machine, that download:

- Requires Kaggle API credentials.
- Costs gigabytes.
- May be unavailable if the competition is closed or behind a license wall.

The synthetic-data fallback lets the framework be exercised — the runner runs, the hill-climb produces a champion, the forensic audit runs, the dashboard renders — without requiring real data. **This is exactly the test-double's role in the SWE-book sense:** the dependency (real Kaggle data) is unavailable, the test double (synthetic Gaussian features) lets the test proceed.

## 13.3 What the fallback is *not*

The fallback is **not** a permission to ship champions trained on synthetic data. The protocol is explicit:

> A champion's `final_report.json` must derive from a real task's data. The synthetic fallback exists for framework development and CI-equivalent runs only; champions in the cohort scoreboard must come from real-data runs.

The mechanism that enforces this: the May 2026 cohort runs on real Kaggle data (downloaded and cached locally; not redistributed) and on real Modeloff data (loaded from `_analysis_data.json`). The 82/112 BEAT-DSBENCH number is computed against real-data champions. A synthetic-data champion would be visible in the manifest hash (Gaussian features have a distinct distribution from real-task features) and would not match the upstream task's natural feature schema, so Agent A and Agent D of the forensic committee would flag the mismatch.

A specific failure mode the project hit — [postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md) — was the synthetic fallback being used *unintentionally* for qa_excel tasks because the original `_excel_agent` didn't load real Modeloff data. The fix surfaced the principle: synthetic data is a deliberate fallback for the framework, not for any task. We now load real Modeloff answers from `_analysis_data.json` for qa_excel, and the synthetic Gaussian path is gated to non-qa_excel tasks only.

## 13.4 The four SWE-book double types, mapped

| SWE-book type | Definition | DSBench analogue |
|---|---|---|
| **Dummy** | An object passed but never used. | The `_unused_kwargs` pattern in `runner.py` for backbone-specific params that don't apply (e.g. `early_stopping=True` passed to xgboost, silently ignored). |
| **Fake** | A simplified working implementation. | The synthetic-Gaussian fallback in `load_or_make_data`. Has the right shape and the right interface but is a simplified working implementation. |
| **Stub** | Returns hard-coded values. | The `_sklearn_fallback` path that substitutes `HistGradientBoostingClassifier` for `FTTransformer` when the FT-Transformer library is unavailable. The substitution is logged so the audit can flag it. |
| **Mock** | Records calls for verification. | We do not use mocks. The forensic committee's Agent F greps for forbidden test-set references — *closest* to a mock in that it verifies the *absence* of certain calls. |

The strongest of these is the **Fake**. The synthetic-Gaussian implementation is a fake in the strict SWE-book sense: it has the same interface as the real data loader, it returns the same dictionary keys (`X_train, y_train, X_val, y_val, X_test, y_test`), and it produces correct-shape arrays. A test that runs against the fake passes if and only if the runner's logic is correct; the fake itself is not lying.

## 13.5 The `_sklearn_fallback` stub

A second test-double in `framework/runner.py:_fit_predict`:

```python
if backbone == "ft_transformer":
    try:
        return _ft_transformer_fit_predict(...)
    except ImportError:
        return _sklearn_fallback(...)
```

The fallback substitutes `HistGradientBoostingClassifier` (sklearn) for the FT-Transformer family. The reasoning: FT-Transformer (Gorishniy et al. 2021 *Revisiting Deep Learning Models for Tabular Data* arXiv:2106.11189) is in the canonical tabular-deep-learning family but the reference implementation is heavy. HistGB is the closest sklearn equivalent that runs at hill-climb speed.

The substitution is *logged* in the experiment log as `backbone: ft_transformer (sklearn_fallback)`. Agent J of the forensic committee counts the fallback as a distinct backbone for diversity (since it has different inductive bias than vanilla xgboost). The substitution is visible to the reviewer, not hidden.

This is the SWE-book's pattern: a stub is allowed, but the stub must announce itself. Silent stubs are mocks-in-disguise.

## 13.6 The Modeloff-real / synthetic dichotomy

The qa_excel task family runs on real Modeloff data exclusively. The decision was made after [postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md) revealed that the original `_excel_agent` was scoring near chance on test (~11 % ± noise) because it was training on synthetic Gaussian features that had no relationship to the actual Modeloff answers.

The fix:

1. `framework/runner.py:_load_qa_excel` reads real Modeloff answers from `_analysis_data.json`.
2. Features are the 9-D structural stack (length, # numeric tokens, # alphabetic tokens, has-decimal flag, has-percent flag, has-currency flag, n-options, question-tier, source-document-tier) plus the 38-task one-hot.
3. The split is a deterministic stride-5 interleaved split ([ADR 0007](../appendix_b_adrs/0007_stride5_interleaved_split_for_qa.md)).
4. The split manifest is hashed and committed.
5. Agent B's threshold is calibrated for the high-MI one-hot encoding.

After the fix, the qa_excel ceiling is ~17 / 38 (the structural limit; see [`analysis/_DIAGNOSIS.md`](../../analysis/_DIAGNOSIS.md)). Pre-fix, the ceiling was ~7 / 38 (chance with noise). The double — synthetic Gaussian — was *the bug*.

## 13.7 The audit-pack as a meta-test

A subtle test-double pattern: `audit_pack.py` is a test for the *skill pack*, which is itself a test surface for the protocol. The audit pack treats SKILL.md files as units, source CLAUDE.md sections as test cases, and the coverage matrix as the assertion. This is testing-of-tests, but it works because the units and assertions are unambiguous.

## 13.8 What tests we did not write

The SWE-book chapter 13 warns against over-mocking: a test that mocks every dependency is a test of the test, not of the code. We deliberately did not:

- **Mock the file system.** The validator and forensic committee read real files. A mocked filesystem would let the validator pass on a cohort that doesn't exist.
- **Mock `numpy` or `sklearn`.** The synthetic-Gaussian data is real numpy arrays; the runner uses real sklearn estimators. The hill-climb's behaviour is the behaviour of those libraries.
- **Mock `pathlib.Path`.** Paths are real paths in the real repository. A mocked `Path` would make the audit live in a parallel universe.

The pattern: use real implementations everywhere we can; use fakes only when the real dependency is unavailable; refuse mocks unless absolutely necessary. The audit gate is structurally hostile to mocks.

## 13.9 The deterministic-seed contract

Every test double in the project is *deterministic*. Two consequences:

1. **The synthetic-Gaussian data is the same every time.** The seed is derived from `cfg.slug` via `seed + hash(cfg.slug) % 10000`, so `titanic` always produces the same Gaussian features. The hash in `split_manifest.json` is stable.
2. **The audit is reproducible.** Re-running `framework/forensic_audit.py` on a clean repo produces the same `forensic_audit.md` byte-for-byte (modulo timestamps in the header). The reviewer can `git diff` to see real changes.

Non-deterministic test doubles are forbidden. If a random component is needed (e.g. seed-stability check in Agent H), it draws from a small fixed seed list (`{7, 42, 99}`) so the test is reproducible.

## 13.10 Related

- [Ch. 11 — Testing Overview](11_testing_overview.md): the four-layer audit gate.
- [Ch. 12 — Unit Testing](12_unit_testing.md): the validator as the unit-test layer.
- [Ch. 14 — Larger Testing](14_larger_testing.md): the forensic committee as the integration layer.
- [Postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md): the synthetic-data-as-bug failure mode.
- [ADR 0001](../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md): the decision to keep the synthetic fallback.
