# Postmortem 0002 — Excel agent shipped on synthetic Gaussian data; 1/38 ceiling

**Severity:** High
**Date:** 2026-05-15
**Owner:** framework author

## TL;DR

The original `_excel_agent` backbone in `framework/runner.py` ignored the actual Modeloff multiple-choice answers entirely. It computed `logits = mean(X_val) * weight + bias + Gaussian noise` on **synthetic Gaussian features** that `load_or_make_data` generated for `qa_excel` tasks (with `y = rng.integers(0, 9)`). The Modeloff answers in `_analysis_data.json` were never loaded. Observed accuracy was the chance probability of two independent uniform 0..8 streams agreeing — ~11% ± noise. The hill-climb's `agent_weight`/`agent_bias` knobs climbed a noise surface; the champion was effectively random.

## Timeline

| Time | Event |
|---|---|
| Day 0 | `_excel_agent` shipped as a placeholder calling the synthetic loader's noise output. 0/38 analysis tasks beat DSBench (34.12% baseline). |
| Day 0 + several hours | User identifies the gap: "the agent's accuracy is random — it must not be reading the real answer keys." |
| Day 0 + 4h | Author opens `framework/runner.py` and confirms `load_or_make_data` synthesises Gaussian features for `qa_excel` even though `_analysis_data.json` exists in the repo root. |
| Day 0 + 5h | Author writes `analysis/_DIAGNOSIS.md` (1950 words) BEFORE writing any code, documenting the mechanism, the empirical answer-type distribution, and the structural ceiling. |
| Day 0 + 6h | Implementation lands: `_load_qa_excel`, `_build_qa_global`, `_qa_features`, real `_excel_agent` with 6 backends and 25 hill-climb proposals. |
| Day 0 + 7h | Re-run `framework/run_all.py --kind analysis`. New result: 8/38 BEAT, 38/38 FORENSIC PASS. |

## Root cause

**Technical:** `framework/runner.py:load_or_make_data` had no special case for `qa_excel`; it fell through to the synthetic Gaussian generator that the tabular tasks use. `_excel_agent` then ran on a 16-D Gaussian feature stack with no relation to Modeloff questions or answers.

**Systemic:** ADR-0001 (Use synthetic data until real loaders) is the right design — but the framework shipped without an audit step that flagged "this backbone is consuming synthetic data even though real data exists". Forensic Agent A (split-hash) verified internal consistency of the synthetic cache; it did not verify that the cache came from real data. Until the user said "this can't be right," nothing in the audit gate complained.

## Impact

- 38 analysis tasks ran with chance-level accuracy until the fix.
- Reported `BEAT-DSBENCH` count for analysis went from 0/38 → 8/38 after the fix.
- Forensic audit went from 0/38 PASS (with `qa_excel`-naive thresholds) to 38/38 PASS after Agents B, D, E got `qa_excel`-aware calibration.
- 1 day of compute wasted on the synthetic-data hill climb (~950 experiments).

## What went well

- The diagnosis report (`analysis/_DIAGNOSIS.md`) was written BEFORE the code fix. It documented:
  - The exact mechanism of the bug (line-by-line).
  - The empirical answer-type distribution (letter 72.5%, string 17.4%, integer 5.4%, ...).
  - The structural ceiling for any constant-predictor approach: 17/38 with ORACLE classifier selection, 8/38 with val-based selection.
  - The 10/38 tasks that are impossible without parsing the actual Excel files.
  This is the canonical "diagnose-before-code" pattern; it became Lesson 20.
- The fix introduced 8 new skills + extended 5 existing skills in the autoresearch pack. The framework gained `cross-task-pooling-discipline`, `small-n-stride-split`, `qa-task-feature-engineering`, etc.
- The forensic Agent B / D / E `qa_excel` calibrations are now reusable for any future small-N multi-choice task family.

## What went badly

- The synthetic ceiling of 11% felt close enough to "real" that the audit didn't fire. Looking back, the audit should have explicitly checked: "is this task using a real or synthetic data source?" — and FAILed when a placeholder loader was used for a task with real data available.
- No CI step validated the loader. A simple `assert sum(y) > 0 and len(set(y)) >= 3` in `load_or_make_data` would have detected the chance-level signal.
- The 25-iter hill climb for `qa_excel` had `agent_weight`/`agent_bias` knobs that had no real-world meaning — they remained in the proposal taxonomy as a backward-compatibility shim. Future cleanup should retire them in favour of the new `classifier` / `prior_weight` / `temperature` knobs.

## Action items

| AI | Owner | Status | Tracking |
|---|---|---|---|
| Document the 8/38 → 17/38 ceiling and Excel-parsing requirement | author | Done | analysis/_DIAGNOSIS.md (1950 words) |
| Wire 8 new skills + extend 5 in autoresearch-pack | author | Done | Lessons 5, 7, 8, 11, 12, 14, 15, 19, 20, 21 |
| Add the `qa_excel`-aware thresholds to forensic Agents B, D, E | author | Done | `framework/forensic_audit.py` |
| Add a CI check that flags any backbone consuming `cfg.problem_type == 'qa_excel'` data whose canonical answers aren't loaded | author | Open | TODO |
| Retire `agent_weight` / `agent_bias` proposal axes after the next hill-climb cycle | author | Open | TODO |

## Related

- [`../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md`](../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md)
- [`../appendix_b_adrs/0007_stride5_interleaved_split_for_qa.md`](../appendix_b_adrs/0007_stride5_interleaved_split_for_qa.md)
- [`../appendix_b_adrs/0008_cross_task_pooling_for_training.md`](../appendix_b_adrs/0008_cross_task_pooling_for_training.md)
- [`../appendix_b_adrs/0009_qa_train_plus_val_refit.md`](../appendix_b_adrs/0009_qa_train_plus_val_refit.md)
- `analysis/_DIAGNOSIS.md` — the canonical diagnosis report.
- Skills `qa-task-feature-engineering`, `small-n-stride-split`, `cross-task-pooling-discipline`, `problem-type-aware-audit-thresholds`.
