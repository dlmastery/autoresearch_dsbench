---
name: qa-task-feature-engineering
description: QA-Excel real-data feature engineering — load real Modeloff answers, build 9-D structural feature stack + 38-task one-hot, support 5 backends (LogReg / KNN / NaiveBayes / class_prior / dummy_majority) with prior_weight / knn_k / temperature knobs. NOT a synthetic-feature placeholder. Triggers on "qa_excel", "excel agent", "Modeloff", "task one-hot", "prior weight", "class prior backend", "QA features".
metadata:
  category: engineering
  source: dsbench
  related: [cross-task-pooling-discipline, small-n-stride-split, problem-type-aware-audit-thresholds]
---

# QA-Task Feature Engineering (real Modeloff answers)

## When to use

- Setting up a new `qa_excel` / multiple-choice / short-answer benchmark.
- Reviewing the `_excel_agent` backbone in `framework/runner.py`.
- Designing the data-loader for a cross-task-pooled training regime.
- Tuning the agent's predictor: which of LogReg / KNN / NaiveBayes / class_prior / dummy_majority is right for THIS task.

## The rule

`framework/runner.py::load_or_make_data()` for `problem_type == "qa_excel"` loads REAL Modeloff multiple-choice answers — NOT synthetic feature noise.

### Data source

- `_analysis_data.json` — per-question rows: `{task, q_id, question_text, options[A..E], correct_answer}`.
- `registry/analysis_tasks.json` — task registry (38 entries) carrying task-level metadata (source URL, problem subtype, baseline).

### Feature stack (per question)

1. **9-D structural features** computed from the question text + options:
   - `len_question` — character count of question text.
   - `n_numeric_tokens` — count of numeric tokens (regex `\b\d+(?:\.\d+)?\b`).
   - `n_alpha_tokens` — count of alphabetic tokens.
   - `has_decimal` — 0/1 flag for `\d+\.\d+` in question.
   - `has_percent` — 0/1 flag for `%` in question.
   - `has_currency` — 0/1 flag for `$`, `€`, `£`, etc.
   - `n_options` — option count (usually 4 or 5).
   - `question_tier` — task-level difficulty band (1=easy, 2=medium, 3=hard).
   - `source_document_tier` — task-level source-doc complexity band.
2. **38-task one-hot indicator** — one binary column per registered Modeloff task. Each question's row has exactly one `task_onehot_<slug> = 1`, all others = 0.

The feature matrix shape is `(N_total_questions, 9 + 38) = (N, 47)`.

### Backbones (`backend` param)

| backend | Description | Knobs that apply |
|---|---|---|
| `logistic_regression` | Sklearn `LogisticRegression(C=…, solver='lbfgs')` on the 47-D feature stack. | `temperature` (softmax) |
| `knn` | Sklearn `KNeighborsClassifier(n_neighbors=knn_k)` with Euclidean distance on z-scored features. | `knn_k`, `temperature` |
| `naive_bayes` | Sklearn `GaussianNB` on numeric features, `BernoulliNB` on the 38-onehot block. | `prior_weight` |
| `class_prior` | Predict argmax of the per-task label prior (computed across training subset of THAT task). | `prior_weight` |
| `dummy_majority` | Predict the global majority class. Baseline floor. | (none) |

### Knobs (cross-cutting)

- `prior_weight ∈ [0, 1]` — convex blend of the **per-task class-prior** with the model's predicted logits: `final_logits = (1 - w) * model_logits + w * prior_logits`. At `w=1` the agent IS the prior; at `w=0` it's the model alone. Used by `logistic_regression` / `knn` / `naive_bayes` / `class_prior`.
- `knn_k ∈ {1, 3, 5, 7, ...}` — KNN neighbour count; only meaningful when `backend=knn`.
- `temperature ∈ (0, 5]` — softmax temperature applied to the model logits before argmax. `T < 1` sharpens, `T > 1` softens.

### Cross-task pooling note

Training is POOLED across all 38 tasks (only training subsets) — see `cross-task-pooling-discipline`. The task-onehot column is what lets the pooled model learn per-task priors without collapsing to the global mode. This is also why agent B (target leakage) in the forensic audit must use `qa_excel`-calibrated thresholds — see `problem-type-aware-audit-thresholds`.

## Anti-patterns

- **Using a synthetic-feature placeholder instead of the real Modeloff stack.** The agent will appear to "work" on synthetic but produce zero signal on the real test set. We had this bug; the fix was the real-data loader.
- **Skipping the task-onehot column.** Pooled training collapses to "predict the global mode" without it.
- **Per-task training without pooling.** Per-task n=5..20 is too small to train any non-trivial classifier; pooling is mandatory.
- **`prior_weight=0` for a sklearn LogReg backend.** The default `solver='lbfgs'` will overfit on n=200ish; even a small prior blend (w=0.2) stabilises the predictions.
- **Hand-engineering a 100-D feature stack.** The 9 structural + 38 onehot stack is intentionally minimal — the question is whether structural metadata is informative, NOT whether a transformer can solve the answer. Add features only after the baseline-on-baseline comparison rules them out as informative.

## Implementation checklist

1. `framework/runner.py::load_or_make_data(repo, cfg)` branches on `cfg.problem_type == "qa_excel"` and loads `_analysis_data.json` + `registry/analysis_tasks.json`.
2. `_build_qa_feature_stack(rows, task_registry)` returns `(X, y)` with shape `(N, 9 + n_tasks)`.
3. `_excel_agent(params, X_train, y_train, X_eval)` dispatches on `params["backend"]` to one of the 5 implementations.
4. `prior_weight` / `knn_k` / `temperature` are wired end-to-end through the CLI and recorded in `best_config.json`.
5. The interleaved stride-5 split (see `small-n-stride-split`) is applied PER TASK before pooling — train union pools the per-task train splits.
6. Unit test: synthesise 38 tasks with known per-task priors; assert `class_prior` backend achieves the per-task prior baseline ±1%.

## References

- Source: `framework/CLAUDE_template.md` section "QA-Excel Task Data Loading".
- Source: `framework/runner.py::load_or_make_data()` (DSBench codebase, 2026-05).
- DSBench (Jing et al. 2025 ICLR) — Modeloff data-analysis benchmark.
- Related: `cross-task-pooling-discipline`, `small-n-stride-split`, `problem-type-aware-audit-thresholds`, `regression-early-stopping-discipline`.
