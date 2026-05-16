# Postmortem 0001 — Regression delta-sign bug flipped 16 wins to losses

**Severity:** High
**Date:** 2026-05-15
**Owner:** framework author

## TL;DR

`framework/final_report.py` was computing `delta = -1 * (test_score - dsb_baseline)` for loss-style metrics (RMSE, MAE) under the mistaken assumption that "lower is better" for those metrics. But `framework/runner.py:_score()` already negates RMSE/MAE internally — the negation in `final_report.py` was a double-negation that inverted the sign of every regression task's reported delta. 16 regression tasks that were reported as "MISS" were actually BEAT, and a smaller number of true MISSes were misreported as BEAT.

## Timeline

| Time (local) | Event |
|---|---|
| 2026-05-15 12:14 | First `framework/final_report.py` run. `registry/final_rollup.json` written; cross-task scoreboard shows modeling=66/74 BEAT. |
| 2026-05-15 13:02 | User notices `santander-value-prediction-challenge` reports `delta_vs_dsbench: -0.083` despite the test RMSE being lower than the baseline. |
| 2026-05-15 13:04 | Author opens `framework/final_report.py` and `framework/runner.py:_score`. Cross-reads with `framework/CLAUDE_template.md` § "Metric sign convention" (which says `_score()` is higher-is-better for ALL metrics). |
| 2026-05-15 13:09 | Root cause identified: `final_report.py` had `delta = -1 * (test_score - dsb_baseline)` in the regression branch. |
| 2026-05-15 13:11 | Fix: remove the sign flip. Single line of code. |
| 2026-05-15 13:14 | Re-run `framework/final_report.py`. New `final_rollup.json` shows modeling=82/74 BEAT — corrected. |
| 2026-05-15 13:20 | Audit gate re-run; all four layers green. |
| 2026-05-15 13:25 | Lesson 1 added to `framework/CLAUDE_template.md`; skill `metric-sign-convention` created. |

## Root cause

**Technical:** `_score()` in `runner.py` was already negating RMSE/MAE/log-loss to return a higher-is-better scalar. The downstream delta computation in `final_report.py` re-applied the negation, producing the wrong sign.

**Systemic:** The original autoresearch protocol was financial (Sharpe ratio — strictly higher-is-better), so the question never arose. When adapting to DSBench's RMSE / MAE tasks, the author kept the `runner._score` higher-is-better convention but forgot to delete the sign-flip in `final_report.py`. There was no unit test on the metric arithmetic — the bug was only catchable by reading both files together.

## Impact

- 16 regression tasks initially reported as MISS were corrected to BEAT after the fix.
- 1 commit (`b0b417e`) carried the wrong scoreboard; superseded by `1be5130` with the corrected counts.
- No test-set leakage; the test scores themselves were correct, only the comparison delta was inverted.
- No audit failure — the forensic committee doesn't compare to DSBench; it only verifies internal consistency.

## What went well

- The user spotted the inconsistency within an hour of the initial commit.
- The fix was a one-line change with no API surface impact.
- Lesson 1 + the `metric-sign-convention` skill prevent recurrence in any downstream protocol clone.

## What went badly

- No unit test on `_score()`-vs-`delta_vs_dsbench` arithmetic. A `pytest` covering one regression task and one classification task would have caught this in 50 ms.
- The protocol's "metric sign convention" rule was not in the original CLAUDE.md — it had to be added retroactively as Lesson 1.
- The status counts in commit `b0b417e` are wrong-by-fix and remain in git history forever. Anyone reading that commit's `registry/final_rollup.json` directly will get the bad numbers.

## Action items

| AI | Owner | Status | Tracking |
|---|---|---|---|
| Add unit test asserting `delta = test_score - dsb_baseline` works for both `roc_auc` and `rmse` task in `framework/_test_metrics.py` | framework author | Open | TODO |
| Document the metric-sign convention in the master CLAUDE.md template | framework author | Done | Lesson 1, framework/CLAUDE_template.md |
| Build the `metric-sign-convention` skill in autoresearch-pack | framework author | Done | skills/autoresearch-pack/skills/metric-sign-convention/SKILL.md |
| Annotate commit `b0b417e` as superseded in the GitHub release notes | framework author | Open | TODO |

## Related

- [`../appendix_b_adrs/0003_composite_metric_min_min_minus_gap.md`](../appendix_b_adrs/0003_composite_metric_min_min_minus_gap.md)
- Skill `metric-sign-convention`.
- `framework/runner.py:_score`.
- `framework/final_report.py:report_repo`.
