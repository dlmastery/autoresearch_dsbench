---
name: cross-task-pooling-discipline
description: Cross-task pooling rule — QA training pools answers across ALL tasks (train subsets only); each task is scored per-task on its held-out test. Pooling allowed for TRAINING; per-task split mandatory for EVALUATION. Triggers on "cross-task pooling", "pooled training", "per-task evaluation", "qa training regime", "Modeloff pooling".
metadata:
  category: protocol
  source: dsbench
  related: [qa-task-feature-engineering, small-n-stride-split, data-integrity-rules, problem-type-aware-audit-thresholds]
---

# Cross-Task Pooling Discipline (training only, NOT evaluation)

## When to use

- Designing the training regime for a multi-task benchmark where each task has very few rows (n ≤ 20).
- Reviewing a QA / multiple-choice / short-answer pipeline that uses a single model across N tasks.
- Setting up the per-task evaluation loop after a pooled train pass.
- Auditing whether a "single model on all tasks" champion is actually evaluated fairly.

## The rule

For `qa_excel`-style benchmarks (Modeloff, ARC, ScienceQA mini), the discipline splits cleanly into two regimes:

### Training: POOL across all tasks

- Compute the train / val / test split PER TASK first (using `small-n-stride-split` for tiny n).
- Pool the per-task train splits: `X_pooled_train = np.concatenate([X_train_task_i for i in tasks])`.
- Fit ONE model on the pooled training set.
- The task-onehot column (see `qa-task-feature-engineering`) is what lets the pooled model learn per-task priors without collapsing to the global mode.

### Evaluation: SPLIT per task

- For each task individually, score the model on THAT task's held-out val (during hill climb) or test (in `final_report.py`).
- Report per-task metrics; aggregate to the macro-average for the leaderboard, but the per-task rows are the authoritative diagnostic.
- DO NOT pool val/test rows across tasks for scoring — the per-task rollup is the contract with the DSBench leaderboard.

### Cross-task pooling chart

```
  Task 1 ──▶ stride-5 ──▶ tr1  v1  te1 ────────┐
  Task 2 ──▶ stride-5 ──▶ tr2  v2  te2 ────────┤
  Task 3 ──▶ stride-5 ──▶ tr3  v3  te3 ────────┤  TRAINING regime: pool tr1+tr2+tr3+...
  ...                                          │   → one model, all tasks
  Task 38 ──▶ stride-5 ──▶ tr38 v38 te38 ──────┘

  EVALUATION regime: per-task
    score model on v1; score on v2; ... score on v38
    score model on te1; score on te2; ... score on te38  (only via final_report.py)
    leaderboard = macro_average(per_task_scores)
```

## Anti-patterns

- **Pooling val OR test for scoring.** Defeats per-task diagnostics; a model that gets all 5 questions right on the easy task and all 5 wrong on the hard task looks like 50% global accuracy and hides the per-task failure.
- **Training per-task instead of pooling.** With n=5..20 per task, per-task training fits noise; no usable classifier emerges. Pooling is mandatory.
- **Pooling without the task-onehot column.** Pooled training collapses to "predict the global mode" because tasks have different per-task priors. Task-onehot lets the model condition.
- **Treating cross-task MI(task_onehot, label) as leakage.** It's a design feature, not a bug — see `problem-type-aware-audit-thresholds` agent B threshold.
- **Reporting only the macro-average and hiding the per-task rows.** The per-task table is the artefact the user needs to spot tasks that the model regresses on.

## Implementation checklist

1. `framework/runner.py::load_or_make_data()` builds per-task stride-5 indices first, then pools the train subsets.
2. The pooled training tensor carries the task-onehot block (one column per task).
3. `framework/runner.py::run_one()` scores the model PER TASK on val (during hill climb).
4. `framework/final_report.py::report_repo()` scores the champion PER TASK on test.
5. The cross-task rollup (`registry/final_rollup.json`) carries one row per task, NOT one aggregated row.
6. Dashboard renders per-task rows + a macro-average summary at the top.
7. Forensic audit thresholds for `qa_excel` account for cross-task-pooled training (see `problem-type-aware-audit-thresholds`).

## References

- Source: `framework/CLAUDE_template.md` section "Cross-Task Pooling Discipline".
- Source: `framework/runner.py::load_or_make_data()` for the pooled-train + per-task-eval implementation.
- Caruana (1997) Machine Learning 'Multitask Learning' — the foundational case for cross-task pooling with shared representations.
- Related: `qa-task-feature-engineering`, `small-n-stride-split`, `data-integrity-rules`, `problem-type-aware-audit-thresholds`.
