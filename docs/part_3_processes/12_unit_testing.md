# Chapter 12 — Unit Testing

> *Parallel to:* SWE-book Chapter 12 *"Unit Testing"* (Winters, Manshreck, Wright 2020).

**Thesis.** Unit tests are cheap, fast, numerous, and the bottom layer of the testing pyramid. The DSBench project's unit-test analogue is `framework/validator.py` plus the audit_pack section-mapping check. Together they run in milliseconds per task, catch the most common bugs (missing protocol section, test-set reference, missing required file), and let the medium- and large-cost layers focus on the harder cases.

## 12.1 What we test as units

The SWE-book chapter 12 defines a unit test as testing a single function in isolation. We test:

| Unit | Test | Cost |
|---|---|---|
| A per-task `CLAUDE.md` | Does it contain all 36 mapped sections? | ~50 ms (substring grep) |
| A per-task `run_autoresearch.py` | Does it never reference `X_test` / `y_test`? | ~5 ms (regex grep) |
| A per-task scaffold | Do all required files exist? | ~20 ms (filesystem checks) |
| A `task_config.json` | Does it parse to a valid `TaskConfig`? | ~5 ms (JSON decode + dataclass instantiation) |
| A `split_manifest.json` | Do the hashes match the on-disk `.npz`? | ~50 ms per file |
| A SKILL.md | Does its YAML frontmatter parse? | ~5 ms |
| A source CLAUDE.md section | Is it matched by ≥ 1 SKILL.md? | ~3 ms |

Each test is a function in `framework/validator.py` or `skills/autoresearch-pack/audit/audit_pack.py`. The tests are deliberately small, deliberately mechanical, and deliberately easy to extend.

## 12.2 `framework/validator.py` — Layer 1 of the audit gate

The validator is a single Python file. It loads `framework/SECTION_MAPPING.md`, walks every task directory under `modeling/` and `analysis/`, and runs four checks per task:

1. **Section coverage.** Every row in `SECTION_MAPPING.md`'s "Task CLAUDE.md location" column must appear as a substring in the task's `CLAUDE.md`. The check is substring-based on purpose — semantic matching would require natural-language understanding, which is out of scope for a unit test.
2. **No-leakage grep.** The files `run_autoresearch.py`, `hill_climb.py`, and any third-party-audit wrapper must not contain the substrings `X_test`, `y_test`, `splits['test']`, `splits["test"]`. Any hit produces a structural error (the most blocking class).
3. **Required-file existence.** A list of mandatory files (`task_config.json`, `seed_reasoning.json`, `paper.md`, `paper_abstract.md`, `README.md`, `autoresearch_results/dashboard.html`, etc.) must all exist. Missing → not_ready.
4. **JSON well-formedness.** `task_config.json`, `split_manifest.json`, `best_config.json`, `final_report.json` must parse. Parse failure → not_ready.

The validator is structurally similar to `lint --strict` for the protocol. It does not check content semantics; the forensic committee does that. The deliberate weakness of the validator is a feature: it can run at every commit without slowing the loop.

## 12.3 The Layer-4 audit_pack as a unit test

`skills/autoresearch-pack/audit/audit_pack.py` is unit-test-shaped: it reads two source CLAUDE.md files (the FX project's `autoresearch/CLAUDE.md` and the SPY adaptation's `autoresearchindexspy/.../CLAUDE.md`) plus our `framework/CLAUDE_template.md`, walks every H2/H3, and asserts each section is matched by at least one SKILL.md's frontmatter or body.

The skill-pack audit's output is `coverage_report.md` with PASS/FAIL per source section. Exit code is 0 iff coverage is 100 % (currently 148 / 148).

The audit is a unit test in the strict SWE-book sense: each section is a unit, the test is `is_covered(section)`, and the assertion is `all(coverage)`. Failure produces a missing-skill list that the human can use to author the missing skill.

## 12.4 Why we do not use pytest

The SWE-book chapter 12 assumes a unit-test framework like JUnit or Google Test. We do not use pytest. Three reasons:

1. **The tests are inherently coupled to the on-disk state.** A pytest fixture for "112 task directories with all required files" would re-create the cohort in a tmpdir; the audit would then test the tmpdir, not the actual cohort. We want to test the actual cohort.
2. **The tests are infrequent.** They run on demand (via `_final_audit.py`) and after every cohort change. Pytest's strength — test discovery, parallel execution, fixtures — is not load-bearing here.
3. **The test output is consumed by the audit gate, not by an IDE.** Pytest's value to a developer's inner loop is irrelevant when the consumer is the cohort scoreboard.

Concretely, the validator and audit_pack write their output as Markdown files (`<task>/audit_report_third_party.md`, `coverage_report.md`) that the dashboard can read. A pytest report does not integrate with the dashboard.

## 12.5 What a "unit failure" looks like

When the validator fails:

```
[validator] modeling/2014-round-1-snakes-and-ladders/CLAUDE.md
  MISSING: ### Sklearn Early-Stopping Val > Train Is Normal (Bishop 2006 §5.5.2)
  STATUS: not_ready
```

The human can read the error and immediately know:

- Which task.
- Which section is missing.
- That the cohort scoreboard cannot include this task until the section is added.

The fix is mechanical: re-run `framework/_regenerate_claude_only.py --task <slug>` to regenerate the `CLAUDE.md` from the template. The validator runs in < 1 second on the single task. The error → fix → re-verify cycle is sub-minute.

## 12.6 The 22,400-check cohort run

Layer 1 of the audit gate runs roughly 22,400 checks per cohort run: 112 tasks × (36 sections + ~5 grep patterns + ~20 file-existence checks) ≈ 22,400. At ~50 ms per task it finishes in ~6 seconds. This is the "fast feedback" the SWE-book calls a unit-test layer's primary virtue.

Comparable to: a pytest run with 22,400 assertions on a fast CI runner — sub-10-second wallclock is expected.

## 12.7 The audit_report_third_party.md per task

Failed validator runs write a per-task report:

```
# Audit Report (Third-Party)

Task: 2014-round-1-snakes-and-ladders
Status: not_ready

## Missing sections
- ### Sklearn Early-Stopping Val > Train Is Normal (Bishop 2006 §5.5.2)

## Forbidden references
(none)

## Missing files
(none)
```

The file is committed to the repo. A reviewer can `git log -p modeling/.../audit_report_third_party.md` to see the history of validator passes and failures. The audit trail is durable.

## 12.8 Coverage by problem-type

The 36 mapped sections in `SECTION_MAPPING.md` are mostly invariant across problem-types. A few are problem-type-specific:

- `### QA-Excel Task Data Loading (real Modeloff answers — NOT synthetic placeholders)` — required on qa_excel tasks only; validator's check is conditional on `task_config.problem_type == "qa_excel"`.
- `### Cross-Task Pooling Discipline (training only — evaluation is per-task)` — required on qa_excel tasks only.
- `### Small-n Stride-5 Interleaved Split (QA tasks only)` — required on qa_excel tasks only.
- `### Sklearn Early-Stopping Val > Train Is Normal (Bishop 2006 §5.5.2)` — required on all tasks (the rule applies generally; just most often surfaces on regression-with-MLP combos).

The conditional logic lives in `framework/validator.py:_required_sections(cfg)`. The conditional dispatch is single-function, ~30 lines, easy to inspect.

## 12.9 What unit tests we deliberately do not write

We do not write:

- **Tests for `framework/runner.py:_fit_predict`.** This is the *behaviour* of the runner; testing it requires a fixture dataset, which is not stable. The forensic committee's Agent I (refit consistency) tests the runner's overall correctness end-to-end without committing to a specific test case.
- **Tests for individual backbone proposals.** A test that says "iter 7 of xgboost is depth=10 lr=0.04" would be a tautology — the test would re-state the proposal. The annotation file *is* the test; the proposal and the rationale are documented together.
- **Tests for the dashboard's HTML output.** The dashboard is regenerated from the rollup files; a wrong rollup produces a wrong dashboard; we test the rollup, not the dashboard.

The pattern: test the *contract* (sections present, no leakage, files exist), not the *implementation* (specific hyperparameters, specific HTML structure).

## 12.10 Anti-patterns in unit testing we deliberately avoid

The SWE-book chapter 12 lists anti-patterns. Our counterparts:

| Anti-pattern | What we do instead |
|---|---|
| Test the implementation, not the behaviour | Validator checks for section *headers*, not for section *content*. |
| Fragile tests that fail on cosmetic changes | Validator uses substring grep, not exact match. A reformatted section still passes. |
| Slow unit tests | All 22,400 checks complete in ~6 seconds. |
| Tests that depend on global state | Validator reads the task directory; no global state. |
| Mocks that hide real interfaces | We do not mock; we use the real on-disk state. Synthetic data ([Ch. 13](13_test_doubles.md)) is a deliberate fallback, not a mock. |
| Tests that don't run in CI | `_final_audit.py` runs all four layers before any commit changing experiment state. |

## 12.11 Related

- [Ch. 11 — Testing Overview](11_testing_overview.md): the four-layer pyramid.
- [Ch. 13 — Test Doubles](13_test_doubles.md): the synthetic-data fallback.
- [Ch. 20 — Static Analysis](../part_4_tools/20_static_analysis.md): the validator's grep-based checks.
- [`framework/validator.py`](../../framework/validator.py): the implementation.
- [`skills/autoresearch-pack/audit/audit_pack.py`](../../skills/autoresearch-pack/audit/audit_pack.py): the Layer-4 audit.
