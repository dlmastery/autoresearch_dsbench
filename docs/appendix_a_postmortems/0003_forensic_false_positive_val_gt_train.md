# Postmortem 0003 — Forensic Agent E flagged sklearn early-stop regression as leakage

**Severity:** Medium
**Date:** 2026-05-15
**Owner:** framework author

## TL;DR

Forensic Agent E's "val > train + 0.05" check fired on every regression task using sklearn `MLPRegressor(early_stopping=True)`. The val-greater-than-train signal is **structural** for sklearn's early-stop scheme (it reserves an internal validation slice and the post-fit `train_score` is computed on the *remaining* 90% of training data) — not a leakage signal. The agent's blanket threshold flagged ~20 modeling tasks as FAIL until the whitelist was added.

## Timeline

| Time | Event |
|---|---|
| Day 0 | First `framework/forensic_audit.py` run on the 74 modeling tasks. ~20 tasks marked FAIL with Agent E suspicion `val_score (0.X) > train_score (0.Y) + 0.05`. |
| Day 0 + 30m | Author opens one of the failed tasks (`commonlitreadabilityprize` regression). Champion is `mlp` with `params: {epochs: 50, early_stopping: true}`. |
| Day 0 + 35m | Author reads sklearn `MLPRegressor` source: when `early_stopping=True`, sklearn splits training data into 90% inner-train / 10% inner-val, picks the stopping epoch by inner-val loss, then reports `score()` on the 90% inner-train. The reported train score systematically underestimates true train performance. |
| Day 0 + 40m | Author cross-references Bishop 2006 PRML §5.5.2 — the early-stopping discipline. Confirms the val > train artefact is normal. |
| Day 0 + 45m | Whitelist added to Agent E: suppress when `(backbone, problem_type, early_stopping) ∈ {(mlp/ft_transformer/lstm/patchtsmixer/lightgbm, regression, true)}` AND `gap ≤ 0.05`. |
| Day 0 + 50m | Re-run forensic auditor. Affected tasks now PASS with the suppression note recorded. |
| Day 0 + 55m | Lessons 4 + 23 added to `framework/CLAUDE_template.md`; skill `regression-early-stopping-discipline` created. |

## Root cause

**Technical:** Agent E used a single tabular threshold (`val > train + 0.05 → FAIL`) for all (backbone, problem_type) pairs. The threshold is correct for "fitted-then-evaluated" classifiers but wrong for sklearn's "fitted-with-internal-val-split-then-evaluated-on-remainder" early-stopping scheme.

**Systemic:** The original autoresearch protocol came from financial time-series tasks (Sharpe-ratio-based composite, no sklearn early-stop). When adapting to DSBench's tabular regression tasks, the author kept Agent E's threshold un-calibrated. The forensic auditor didn't have a backbone-AND-problem-type-aware threshold table — it had per-problem-type thresholds only.

## Impact

- ~20 modeling tasks reported as FORENSIC FAIL until the whitelist landed.
- 0 actual leakage; the suspicion was a false positive in every case.
- `registry/forensic_summary.json` showed 92/112 PASS during the false-positive window; corrected to 112/112 PASS after the whitelist.

## What went well

- The fix is small (~15 lines including the whitelist table) and the citation (Bishop 2006 PRML §5.5.2) is rigorous.
- The forensic auditor's "narrative + structured JSON" output made the suspicion explicit: the agent printed "val (0.823) > train (0.794) + 0.05 → suspicious" — the author could read the suspicion and immediately know the regime.
- The whitelist was implemented as data (a table), not code — extending it to a new backbone is a one-line addition.

## What went badly

- The threshold was un-calibrated when the protocol crossed domains. The skill `forensic-audit-pipeline` did not document the threshold table at the time; it only described the agents abstractly.
- The whitelist is currently encoded only in `framework/forensic_audit.py:agent_e_anomaly`. A future fork of the auditor would re-introduce the false positive unless the author also copies the whitelist.
- No unit test exists that asserts "Agent E suppresses on a sklearn early-stop regression task." A 5-line test would prevent regression.

## Action items

| AI | Owner | Status | Tracking |
|---|---|---|---|
| Whitelist (mlp, ft_transformer, lstm, patchtsmixer, lightgbm) × regression in Agent E | author | Done | `framework/forensic_audit.py` |
| Document the whitelist in `framework/CLAUDE_template.md` and `regression-early-stopping-discipline` skill | author | Done | Lessons 4 and 23 |
| Extend Agent E to handle classification + early-stop separately (not whitelisted; different failure modes) | author | Done | distinction is in the skill |
| Add unit test in `framework/_test_*.py` asserting suppression behaviour | author | Open | TODO |

## Related

- [`../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md`](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md)
- [`../part_3_processes/09_code_review.md`](../part_3_processes/09_code_review.md)
- Skill `regression-early-stopping-discipline`.
- Bishop 2006 'Pattern Recognition and Machine Learning' PRML §5.5.2.
