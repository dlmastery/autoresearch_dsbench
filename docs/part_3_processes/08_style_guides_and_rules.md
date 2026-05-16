# Chapter 8 — Style Guides and Rules

> *Parallel to:* SWE-book Chapter 8 *"Style Guides and Rules"* (Winters, Manshreck, Wright 2020).

**Thesis.** A style guide is a project's shared judgement, written down. It exists so that decisions stop being relitigated every commit. In the DSBench project the style guide is `framework/CLAUDE_template.md` and the 112 per-task `CLAUDE.md` files it generates. Those files are the *protocol* in the sense that they are the contract every Claude session reads on startup. They are checked mechanically by `framework/validator.py`. A change to the style guide that does not also change the validator is a wish, not a rule.

## 8.1 Three kinds of rules

The SWE-book chapter 8 distinguishes rules ("things you must do, enforced by the linter"), guidelines ("things you should do, reviewed in code review"), and recommendations ("things experienced engineers do"). The DSBench parallel:

| Tier | Example | Enforced by |
|---|---|---|
| **Rule** | Every experiment changes exactly one config knob. | The Six-Field Annotation Rule + Citation-Rigor Rule + manual code review of the annotation. |
| **Rule** | The runner never references `X_test`. | `framework/validator.py` greps and fails on any hit. |
| **Rule** | Every per-task `CLAUDE.md` contains the 36 mapped sections. | `framework/validator.py` substring check against `SECTION_MAPPING.md`. |
| **Rule** | Every commit changing experiment state has the four-layer gate green. | `framework/_final_audit.py` exit code. |
| **Guideline** | Iter 1 of every backbone is the published-paper default. | Code review of the proposals in `framework/hill_climb.py`. |
| **Guideline** | Annotations name at least one paper per experiment. | The Citation-Rigor Rule + reviewer judgement. |
| **Recommendation** | Diagnose the per-fold variance before declaring a new champion. | Experienced practice; not policed. |

The line between rule and guideline matters. A rule has a CI hook; a guideline does not. A rule that loses its CI hook silently demotes itself to a guideline and then drifts. The validator is the rule's defence.

## 8.2 `CLAUDE.md` as the project style guide

Every per-task `CLAUDE.md` is a parameterised clone of `framework/CLAUDE_template.md`. The template has 36+ required sections enumerated in `framework/SECTION_MAPPING.md`. The sections fall into five groups:

1. **Operational** — session start, hardware constraints, crash-recovery checkpointing, mindset.
2. **Hard rules** — data integrity (Test-Set Embargo), split invariants, experiment design.
3. **Loop protocol** — autoresearch agent protocol (Karpathy-adapted), research-driven experiment selection, monotonic quality progression.
4. **Documentation** — MLOps documentation standards, explainability & auditability report, winner definition, per-backbone code snapshots, dashboard reasoning annotations.
5. **Verification** — per-backbone 25-experiment mandate, GPU memory constraint, dashboard backbone tabs, GitHub Pages dashboard sync, dashboard files update mandate, citation rigor, reasoning blob completeness, etc.

The full table is in [`framework/SECTION_MAPPING.md`](../../framework/SECTION_MAPPING.md). The validator's substring check is a deliberately weak contract: it asserts the *header* is there, not that the content under the header is correct. The stronger checks happen in code review (the human reading the commit) and in the skill-pack audit (which verifies each header has a SKILL.md companion).

## 8.3 The Per-Backbone 25-Experiment Mandate

The canonical example of a rule the project enforces: **every backbone gets a full 25-iteration exploration, even if axes "look exhausted" earlier**. The rule:

> Each backbone (`xgboost`, `lightgbm`, `catboost`, `mlp`, `ft_transformer` for tabular tasks; `excel_agent` for qa_excel) runs 25 numbered iterations. Iter 1 is the published-paper default. Iters 2–10 are documented perturbations along one axis with a paper citation each. Iters 11–25 are generated from a library of cited perturbations (subsample, colsample, reg_lambda, num_leaves, depth, GOSS sampling). Iters 8 and 9 of every backbone are seed perturbations (`seed ∈ {7, 99}` alongside the default `42`) for a 3-seed median.

The reason for the rule: the LLM collaborator's working memory dies between sessions. Without the mandate, iter 23 of `xgboost` (after a poor iter 22) gets skipped because "the axis looks exhausted", and the next session has no record of *which* axes were actually exhausted. The mandate forces the log to be the memory.

The CI hook for the rule is two-pronged:

1. `framework/validator.py` checks every per-task `CLAUDE.md` for the substring `Per-Backbone 25-Experiment Mandate`. Missing → not_ready.
2. `framework/_status.py` reports the per-task experiment count distribution. A task with `< 125` experiments and no `extended_hill_climb` activity is flagged for human review.

See [ADR 0005](../appendix_b_adrs/0005_25_iters_per_backbone.md) for the structural reasoning.

## 8.4 The One-Knob Rule

> Every hill-climb experiment changes exactly one config knob from the current best config and cites at least one paper that motivates the change.

The SWE-book chapter 8 calls this an "anti-grid-search guardrail"; the autoresearch literature calls it Karpathy-style autoresearch. The point is the same: a grid search produces a champion that the team doesn't understand; a one-knob-at-a-time hill-climb produces a champion the team has a written argument for.

The mechanism: the six-field annotation. The `hypothesis` field is required to name the knob being changed and the predicted direction of the composite delta. The `prediction` field is required to commit to a numerical range *before* running. The `verdict` field is required to compare prediction to outcome. If the prediction was way off, the `learning` field is required to name why.

Annotations with `_manual: true` are the gold standard — human-authored or human-reviewed. Annotations without `_manual: true` exist but are flagged in code review as "auto-only, please review".

## 8.5 The Citation-Rigor Rule

> Every reasoning annotation includes ≥ 1 citation in the canonical format `Author1, Author2, ... YEAR VENUE 'Paper Title' (arXiv:XXXX.XXXXX) — one-sentence relevance note`.

Worked example from `2014-round-1-precise-debt-modeling` iter 11 of xgboost:

> citations: "Friedman 2001 *Greedy Function Approximation: A Gradient Boosting Machine* — section 4 argues that stochastic subsampling (rows + columns) reduces variance more than depth restriction at fixed boosting rounds. Chen & Guestrin 2016 KDD *XGBoost* arXiv:1603.02754 — extends Friedman's argument with `subsample` + `colsample_bytree` as the canonical lever."

A non-example (would fail the rule):

> citations: "(Friedman 2001) subsample helps."

The non-example fails because (a) no venue, (b) no title, (c) no arXiv / DOI, (d) no relevance sentence. The `citation-rigor` skill carries the full enforcement text and links to the audit. The Citation-Rigor Rule is enforced in code review of the annotations file.

## 8.6 What is *not* style

A few decisions that are intentionally *not* style — they live in code and config, not in the style guide:

- **Python formatting.** Not policed. The project uses idiomatic NumPy / sklearn / torch conventions; we do not run `black` or `isort`. Saving the rule for later if the team scales beyond one human.
- **Commit-message format.** Loose. We use the SWE-book's recommendation (subject line ≤ 70 chars, body explains why), but there's no commitlint hook. The 26 Lessons-Learned rows demonstrate the discipline holds without enforcement.
- **Test framework.** We do not use pytest. The audit gate *is* the test suite. See [Ch. 12](12_unit_testing.md) for the framing.
- **Directory layout outside `modeling/` / `analysis/`.** Free. Only the per-task scaffolds are mechanically enforced.

The boundary is: anything the validator or the forensic committee can check mechanically is in the style guide; anything else is convention.

## 8.7 The "no future sections" rule

A specific failure mode the SWE-book flags: style guides that promise things the implementation doesn't deliver. The DSBench parallel: documentation that describes state that hasn't been measured. We forbid this explicitly. From the README:

> Placeholder fields are LITERAL — they are deliberately not auto-substituted in this template so the file never lies about state it hasn't measured.

The "Champion summary" block at the top of `framework/CLAUDE_template.md` carries literal placeholders (`<count>/<total>`, `<task_slug>`). A future pre-commit hook (`framework/_substitute_champion_summary.py`) will substitute these from `registry/final_rollup.json` + `registry/forensic_summary.json` *at scaffold-generation time*. Until that hook ships, the placeholders stay literal. We do not write the numbers manually because the manual number would lie within a day of being written.

This is the strongest possible form of the SWE-book's "documentation should not drift": refuse to write down the number until a script can write it for you.

## 8.8 How the style guide changes

The style guide changes when:

1. A new section appears in the upstream `autoresearch/CLAUDE.md` (the FX project — `4/20/2026` snapshot) or `autoresearchindexspy/.../CLAUDE.md` (the SPY adaptation). We mirror it into `framework/CLAUDE_template.md`, add a `SECTION_MAPPING.md` row, add a SKILL.md, regenerate the 112 scaffolds, re-run the four-layer audit.
2. A Lessons-Learned row crystallises into a structural rule. The row promotes itself into a new section in `CLAUDE_template.md` + a new SKILL.md + a `SECTION_MAPPING.md` row.
3. A postmortem in [Appendix A](../appendix_a_postmortems/) names a missing rule. The postmortem's Action Items section lists the new rule, the new SKILL.md, and the new SECTION_MAPPING row.

In all three cases the *style guide change is followed by a coverage check* — `audit_pack.py` must come back at 100 %. A style-guide change without a coverage check is a regression.

## 8.9 The 26 Lessons-Learned rows

The current Lessons-Learned table in `framework/CLAUDE_template.md` has 26 rows. Rows are dated and tied to a specific commit. The most recent batch (rows 18–26) was added at commit `1be5130` and covers:

- Row 18: Composite-metric sign convention (RMSE / MAE must be negated inside `_score`).
- Row 19: Skill-pack coverage gate must be re-run after every CLAUDE.md change.
- Row 20: Held-back surface discipline (`X_test` references in any runner = audit fail).
- Row 21: Single-command end-to-end refresh (`framework/_refresh_dashboards.py` must produce all dashboards in one run).
- Row 22: Parallel-agent-orchestration tradeoff (two background processes go 1.8× faster but require disjoint output paths).
- Row 23: Two-tab navigation rule (dashboard kind toggle without losing scroll position).
- Row 24: MD viewer inline rendering (forensic_audit.md must render in the dashboard, not require download).
- Row 25: Forbidden-path audit (any `_backup_pre_*` folder is a hard error in the cohort scoreboard).
- Row 26: Status-counting asymmetry (final_rollup.json doesn't carry `kind`; forensic_summary.json does).

Each row points to a SKILL.md in the autoresearch-pack and, where applicable, to a specific ADR or postmortem.

## 8.10 Related

- [Ch. 9 — Code Review](09_code_review.md): how the style guide gets enforced commit-by-commit.
- [Ch. 11 — Testing Overview](11_testing_overview.md): the four-layer audit gate that backs the rules.
- [Ch. 15 — Deprecation](15_deprecation.md): how rules get retired when they stop earning their keep.
- [Ch. 20 — Static Analysis](../part_4_tools/20_static_analysis.md): the validator's grep-based checks.
- [`framework/SECTION_MAPPING.md`](../../framework/SECTION_MAPPING.md): the canonical section list.
- [`framework/CLAUDE_template.md`](../../framework/CLAUDE_template.md): the style guide itself.
