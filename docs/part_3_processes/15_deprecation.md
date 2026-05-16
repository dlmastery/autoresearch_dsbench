# Chapter 15 — Deprecation

> *Parallel to:* SWE-book Chapter 15 *"Deprecation"* (Winters, Manshreck, Wright 2020).

**Thesis.** Code that earns its keep stays; code that doesn't gets removed. The SWE-book chapter 15 argues that deprecation is a *process*, not an event: code is announced as deprecated, callers migrate, the code is removed, the archive is retained. The DSBench parallel is the **failed-backbone retirement** path plus the `_backup_pre_*` convention for hill-climb retries. Both follow the same rhythm: announce, migrate, archive, remove.

## 15.1 What we deprecate

Three categories of code and config get deprecated in this project:

1. **Failed backbones.** A backbone whose 25-iter exploration produces no winning experiments on any task family family is a candidate for retirement.
2. **Failed proposal recipes.** A specific iter (e.g. `xgboost depth=12 lr=0.01`) that has produced no wins in the cohort can be retired from `framework/hill_climb.py:_xgb_proposals`.
3. **Failed audit calibrations.** An Agent E threshold that produces too many false positives gets recalibrated with a new threshold + a Lessons-Learned row; the old threshold's "default" status is deprecated.

Each category follows the same five-step process below.

## 15.2 The five-step deprecation process

The SWE-book chapter 15 names a five-step process. We follow the same shape:

### 15.2.1 Step 1 — Decide

The decision happens in an ADR. Example: [ADR 0010](../appendix_b_adrs/0010_sklearn_early_stopping_whitelist.md) decides that the val > train pattern on sklearn-early-stopped regression is *not* an anomaly. The pre-ADR threshold (any val > train + 0.05 = anomaly) is now deprecated; the post-ADR threshold (val > train + 0.05 = anomaly *unless* `early_stopping=True` is in the params and the backbone is a sklearn regressor) is the rule.

### 15.2.2 Step 2 — Announce

The Lessons-Learned table in `framework/CLAUDE_template.md` gets a new row that names the deprecation and the replacement. The corresponding SKILL.md in `skills/autoresearch-pack/skills/` is updated. The audit pack's coverage matrix grows by one row.

### 15.2.3 Step 3 — Migrate callers

Every per-task `CLAUDE.md` is regenerated via `framework/_regenerate_claude_only.py`. The new section appears in every task; the old behaviour is no longer the default. The validator's substring check verifies every task has the new section header.

### 15.2.4 Step 4 — Archive

The old code path is not deleted; it is *renamed* with a `_backup_pre_*` suffix. For example, if `framework/runner.py:_score_v1` is being deprecated, it gets renamed `_score_v1_backup_pre_<commit_short_sha>` and the new function takes the name `_score_v1`. This is the "archive" step.

The `_backup_pre_*` convention is **forbidden in the cohort scoreboard**: Lessons-Learned row 25 says any `_backup_pre_*` folder or file under `modeling/` or `analysis/` is a hard error. The convention exists in `framework/` only.

### 15.2.5 Step 5 — Remove

After two cohort runs that confirm the new behaviour is correct, the `_backup_pre_*` reference is deleted from `framework/`. Git history preserves it for reviewers. The deprecation is complete.

## 15.3 Worked example: the `_excel_agent` rewrite

The pre-May 2026 `_excel_agent` was scored on synthetic Gaussian features ([postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md)). The five-step deprecation:

1. **Decide.** [ADR 0001](../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md) names the synthetic-data path as a fallback only. The `_excel_agent` is rewritten to load real Modeloff data.
2. **Announce.** Lessons-Learned rows 13 and 19 announce the rewrite. SKILL.md for `qa-task-feature-engineering` is authored.
3. **Migrate callers.** `framework/_regenerate_claude_only.py` runs against all 38 analysis tasks. The new section `### QA-Excel Task Data Loading (real Modeloff answers — NOT synthetic placeholders)` appears in every task's `CLAUDE.md`.
4. **Archive.** The old `_excel_agent` implementation is renamed `_excel_agent_synthetic_backup_pre_<sha>` for one cohort run, then deleted.
5. **Remove.** The May 2026 cohort runs on the real-data implementation. Git history preserves the synthetic version.

The cohort scoreboard moved from "qa_excel ceiling ~7 / 38" to "qa_excel ceiling ~17 / 38" — paid for by the deprecation.

## 15.4 The "easy to deprecate" property

The SWE-book chapter 15 argues that code should be designed to be deprecatable. Our equivalent: every backbone is dispatched by name from `runner._fit_predict`, which means a deprecation is a one-line change to the dispatch table plus a SKILL.md update. We deliberately do not allow backbones to live as global state or as module-level singletons; every backbone is a function called by name.

This is a structural choice that pays off whenever a backbone is retired. Compare: a project where each backbone has its own subdirectory, its own `__init__.py`, its own configuration class. Retiring such a backbone is a 50-file change; retiring ours is a 5-line change.

## 15.5 Soft deprecation vs hard deprecation

The SWE-book distinguishes *soft* deprecation (callers are warned but not blocked) from *hard* deprecation (callers are broken). Our process is closer to soft:

- The Lessons-Learned row + SKILL.md announce the change.
- The new behaviour is the default; the old behaviour is logged with a `deprecated_*` flag in the experiment log (e.g. `backbone: ft_transformer (deprecated_synthetic_v1)`).
- After the next cohort run validates the new behaviour, the old code is removed.

A hard deprecation in this project would look like: rename the function, do not provide a forwarding alias, fail every per-task scaffold that references the old name. We have done this twice (once for `_excel_agent`, once for the pre-`_pin_to_safe_cores` runner). Both times the migration was forced by a *correctness* concern, not a *naming* concern.

## 15.6 The `_backup_pre_*` convention

When a hill-climb run needs to retry a phase, we sometimes archive the current state under a `_backup_pre_*` directory:

```
modeling/titanic/autoresearch_results/_backup_pre_2026-05-15T14-23/
  experiment_log.jsonl
  best_config.json
  reasoning_annotations.json
  ...
```

The convention has rules:

1. The `_backup_pre_*` directory is **scoped to a single task** and **lives under `autoresearch_results/`** of that task.
2. The directory is **never** read by the runner, hill-climb, or audit. It exists only for the human's spot-check.
3. The directory is **forbidden in the cohort scoreboard** — Lessons-Learned row 25 says the cohort scoreboard's audit will flag any `_backup_pre_*` directory under `modeling/` or `analysis/` as a hard error.
4. The directory is **deleted after the next successful cohort run** that validates the new state.

The convention pays off when a hill-climb run gets stuck in a bad local optimum and the human wants to restart from iter 1 of a backbone. The archive lets the new run start cleanly while the old state is preserved for inspection.

## 15.7 What we do *not* deprecate

A few categories of code we keep even when they look superfluous:

- **The synthetic-Gaussian fallback.** Even after the `_excel_agent` rewrite made the synthetic path irrelevant for qa_excel, the path stays for tabular tasks because it lets the framework be exercised without Kaggle credentials. See [Ch. 13](13_test_doubles.md).
- **The `sklearn` early-stopping path.** Even though we whitelisted the val > train pattern, the underlying sklearn path stays because the behaviour is the *correct* behaviour for sklearn estimators. The deprecation is on the *audit*, not the code.
- **Old citation entries.** The glossary keeps every paper ever cited, even if no current experiment cites it. Citation history is testimony; we do not garbage-collect.

The pattern: deprecate when the code is *wrong* (synthetic features for qa_excel was wrong); keep when the code is merely *unused* (synthetic features for tabular is unused but correct).

## 15.8 The audit-pack as a deprecation gate

The skill-pack audit catches deprecation drift: if a section is removed from `framework/CLAUDE_template.md` without removing the corresponding SKILL.md, the coverage matrix still claims the section is covered when it isn't. The audit catches this by parsing the source files fresh on each run.

Conversely, if a SKILL.md is deleted without removing the corresponding section from `CLAUDE_template.md`, the section becomes uncovered and the audit fails.

The audit-pack therefore enforces a *bidirectional* coupling: SKILL.md ↔ source section. Deprecation has to update both sides or the audit fails.

## 15.9 The 26 Lessons-Learned rows as a deprecation history

Every Lessons-Learned row records either a correction or a deprecation. Reading the 26 rows in order is reading the project's deprecation history. The most consequential deprecations:

- Row 13 (Date 2026-05-15): The synthetic-features `_excel_agent` is deprecated; real Modeloff loading is the rule.
- Row 18 (Date 2026-05-15): The pre-negation RMSE convention is deprecated; the post-negation convention is the rule.
- Row 20 (Date 2026-05-15): `X_test` references in any runner code are now hard errors; the previous lenient grep is deprecated.
- Row 24 (Date 2026-05-15): Manual MD viewing is deprecated; inline rendering via the MD viewer is the rule.
- Row 26 (Date 2026-05-15): Cross-rollup joining by index is deprecated; joining by slug is the rule.

Each row points to the ADR, SKILL.md, and code path that codifies the rule. None of the rows are retroactive — every row applies from its commit forward.

## 15.10 Related

- [Ch. 8 — Style Guides and Rules](08_style_guides_and_rules.md): the Lessons-Learned table as the deprecation log.
- [Ch. 22 — Large-Scale Changes](../part_4_tools/22_large_scale_changes.md): how to deprecate across 112 tasks.
- [Postmortem 0002](../appendix_a_postmortems/0002_excel_agent_synthetic_placeholder.md): the canonical worked example.
- [ADR 0001](../appendix_b_adrs/0001_use_synthetic_data_until_real_loaders.md): the synthetic-data ADR.
