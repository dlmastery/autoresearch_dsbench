# Chapter 20 — Static Analysis

> *Parallel to:* SWE-book Chapter 20 *"Static Analysis"* (Winters, Manshreck, Wright 2020).

**Thesis.** Static analysis is "everything you can learn about the code without running it". The SWE-book chapter 20 talks about Tricorder, the Error Prone framework, and a small army of analyzers. We don't have those. What we do have is **`framework/validator.py`** (Layer 1) and **`framework/forensic_audit.py:_agent_f`** (Agent F, static-code) and **`audit_pack.py`** (Layer 4) — all three are grep-based static analyzers tailored to the protocol.

## 20.1 What we analyze without running

Three classes of static check the project performs:

### 20.1.1 Section-mapping coverage

`framework/validator.py` reads `framework/SECTION_MAPPING.md` (44 rows) and verifies the substring of each row's "Task CLAUDE.md location" column is present in every per-task `CLAUDE.md`. The check does not execute any code in the task; it reads the Markdown file as text.

This is the project's most-frequent static analysis. It runs on every cohort change. Cost: ~6 seconds for 112 tasks × ~5 ms each. Catches: missing protocol section, garbled section header, file truncation.

### 20.1.2 Forbidden-pattern grep (the X_test grep)

`framework/validator.py:_FORBIDDEN_TEST_REFS` and Agent F of the forensic committee both grep every `run_autoresearch.py`, `hill_climb.py`, and `third_party_audit.py` per task for the patterns:

- `X_test`
- `y_test`
- `splits['test']`
- `splits["test"]`

The grep does not execute the runner; it reads the source file. The check is *over-broad on purpose*: a reference to `X_test` in a comment is treated as a smell ("why is the protocol's most-restricted variable named in a runner file?") and worth blocking.

The grep exempts `framework/final_report.py` because that file is the only legal reader of the test set. The exemption is hard-coded in the validator; changing it requires a code change to the validator itself.

### 20.1.3 Skill-pack coverage

`skills/autoresearch-pack/audit/audit_pack.py` parses every H2/H3 in the three source CLAUDE.md files (`autoresearch/CLAUDE.md`, `autoresearchindexspy/.../CLAUDE.md`, `framework/CLAUDE_template.md`) and verifies each section is matched by ≥ 1 SKILL.md (by trigger phrase or body substring). The check is static: parse the Markdown, build the section index, build the skill index, compute the bipartite match.

This is the project's slowest static analysis at ~5 seconds, but it's also the most architectural: it verifies the entire protocol surface has a corresponding skill.

## 20.2 What static analysis cannot do

The SWE-book chapter 20 is candid: static analysis can't replace dynamic testing. Our static analysis cannot:

- **Verify that a backbone's hyperparameters are sensible.** The validator checks that the iter has six annotation fields and a citation; it does not check that the citation actually motivates the change.
- **Verify that `runner._score` normalises metrics correctly.** That requires running the code (which the integration test does via Agent I's refit consistency).
- **Verify that the dashboard renders correctly.** That requires rendering the HTML.
- **Verify that the forensic audit's thresholds are calibrated.** That requires running the audit and inspecting the false-positive rate.

These checks live in the dynamic layers (Layer 2 — forensic; Layer 3 — explainability). Static and dynamic compose; neither suffices alone.

## 20.3 The audit_pack section parser

`audit_pack.py` is the project's most-interesting static analyzer because it walks markdown structure, not just content. The parser:

1. Reads a CLAUDE.md file line by line.
2. Identifies lines starting with `## ` (H2) or `### ` (H3) as section boundaries.
3. Captures the header text, the file path, and the line number into a `(file, level, header)` tuple.
4. For each tuple, searches every `skills/.../SKILL.md` for the header text in the `triggers` field or the body.

The walker treats Markdown as a structured document, not as opaque text. A subtle correctness point: H2 and H3 headers can repeat across files (`## On Session Start` appears in multiple sources), so the walker keys by `(file, header)`, not by header alone.

The output `coverage_report.md`:

```markdown
# Coverage Report

**Total sections:** 148
**Covered:** 148 (100.0%)
**Verdict:** PASS

## By file

### autoresearch/CLAUDE.md (45 sections, 45 covered)
...

### autoresearchindexspy/autoresearchspy/CLAUDE.md (54 sections, 54 covered)
...

### dsbench/framework/CLAUDE_template.md (49 sections, 49 covered)
...
```

Exit code 0 iff coverage is 100 %.

## 20.4 The Agent F static-code grep

A specific implementation note for Agent F: the grep is not a simple substring match. It excludes:

- Comments that explicitly state the rule (e.g. "# Test set: NEVER read here").
- The `final_report.py` file (the exemption).
- The `forensic_audit.py` file (which legitimately needs to grep for these references in others).

The exclusion logic is in `framework/forensic_audit.py:_agent_f` and is documented inline. Changing the exclusion list is a hard change; it requires an ADR and an audit re-run.

The grep result is reported in the per-task `forensic_audit.md` under "Agent F — static-code audit". A hit fails the audit; the hit's filename and line number are reported so the reviewer can investigate.

## 20.5 The `_required_sections(cfg)` problem-type-aware check

The validator's section check is problem-type-aware. The function:

```python
def _required_sections(cfg: TaskConfig) -> list[str]:
    base = _BASE_SECTIONS  # 36 sections, all tasks
    if cfg.problem_type == "qa_excel":
        base = base + _QA_EXCEL_EXTRA_SECTIONS  # +4 sections
    if cfg.problem_type == "regression":
        base = base + _REGRESSION_EXTRA_SECTIONS  # +1 section (Sklearn Early-Stopping)
    return base
```

This is a small static-dispatch table that codifies which sections are required for which problem types. The dispatch is itself audited (every problem type must have a known section list).

## 20.6 Anti-patterns in static analysis we avoid

The SWE-book chapter 20 lists static-analysis anti-patterns. Our equivalents:

| Anti-pattern | Mitigation |
|---|---|
| Too many false positives | The X_test grep is over-broad but the failure rate is 0 in practice — runner authors don't reference `X_test` in any legitimate way. |
| Linter that everyone disables | The audit gate cannot be disabled; the convention is to fix the failure or recalibrate via ADR. |
| Slow analysis | All three static layers complete in < 20 sec total. |
| Vague error messages | Every audit message names the section / pattern / file / line. |
| Reports that nobody reads | `audit_report_third_party.md` per task is committed; the dashboard renders it inline; `_status.py` reports the totals. |

## 20.7 The static / dynamic boundary

A simple rule of thumb: **the static layer checks what should be true regardless of data; the dynamic layer checks what is true for this data**.

| Question | Layer |
|---|---|
| Does `CLAUDE.md` have all 36 sections? | Static (validator). |
| Does the runner reference `X_test`? | Static (validator + Agent F). |
| Does every protocol section have a skill? | Static (audit_pack). |
| Does the test set's hash match the manifest? | Dynamic (Agent A). |
| Does the train/test KS test exceed 10 % flagged features? | Dynamic (Agent D). |
| Does the refit reproduce the recorded test score? | Dynamic (Agent I). |
| Does the experiment log have ≥ 3 distinct backbones? | Dynamic (Agent J). |

The static / dynamic split is a deliberate testing-pyramid choice ([Ch. 11](../part_3_processes/11_testing_overview.md)): static is cheap and runs always; dynamic is more expensive and runs after the static is green.

## 20.8 What we'd add if we scaled

A few static analyses we'd add at higher scale:

- **AST-based check that `_pin_to_safe_cores` is the first call in every runner file.** Currently grep-based.
- **AST-based check that no top-level code mutates the registry.** Currently convention-only.
- **Markdown link-check across `docs/`.** Currently manual. A simple Python script with `markdown_it_py` would do.
- **Citation-format check on `reasoning_annotations.json`.** Currently the `citation-rigor` skill carries the rule but no automated enforcement. A regex check for the canonical format would catch ~80 % of malformed citations.

Each of these would be a single Python file in `framework/`, < 200 lines. They have not been written because the failure rate at 112-task scale is low; at 540-scale they become worth the engineering investment.

## 20.9 Related

- [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md): the four-layer pyramid.
- [Ch. 12 — Unit Testing](../part_3_processes/12_unit_testing.md): the validator as the unit-test layer.
- [Ch. 17 — Code Search](17_code_search.md): the grep patterns that the validator uses.
- [`framework/validator.py`](../../framework/validator.py): Layer 1.
- [`framework/forensic_audit.py`](../../framework/forensic_audit.py): Layer 2, Agent F.
- [`skills/autoresearch-pack/audit/audit_pack.py`](../../skills/autoresearch-pack/audit/audit_pack.py): Layer 4.
