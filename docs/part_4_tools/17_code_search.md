# Chapter 17 — Code Search

> *Parallel to:* SWE-book Chapter 17 *"Code Search"* (Winters, Manshreck, Wright 2020).

**Thesis.** The SWE-book chapter 17 describes Google's internal Code Search as a first-class developer tool. The DSBench project has no Code Search service; we use `ripgrep` / `Grep` over `framework/` + `skills/` + `modeling/` + `analysis/`. The discipline is that *every audit rule has a grep pattern that enforces it* and *every grep pattern is documented in the SKILL.md or the validator source*.

## 17.1 What we search

The project has three corpora to search:

| Corpus | Size | Typical search |
|---|---|---|
| `framework/*.py` | ~3,000 lines across 22 files | "where is `_pin_to_safe_cores` called?", "every reference to `X_test`" |
| `skills/autoresearch-pack/skills/*/SKILL.md` | 44 files, ~80,000 words total | "which skill mentions early-stopping?", "which skill enforces citation format?" |
| `modeling/*/CLAUDE.md` and `analysis/*/CLAUDE.md` | 112 files, ~150 sections each | "every task with the new `Sklearn Early-Stopping Val > Train Is Normal` section", "every task missing the Lessons-Learned table" |

Each corpus has a different concern. The framework Python search is for refactoring; the SKILL.md search is for protocol guidance; the per-task `CLAUDE.md` search is for audit coverage.

## 17.2 The SECTION_MAPPING audit as code search

`framework/validator.py` is, in essence, a code-search engine specialised for the protocol. It reads `framework/SECTION_MAPPING.md`, extracts the "Task CLAUDE.md location" column, and greps every per-task `CLAUDE.md` for each substring. The search produces a per-task `audit_report_third_party.md` that the dashboard renders.

This is the SWE-book chapter 17 pattern: search becomes a first-class audit tool when the search results are persisted as artefacts. A reviewer reading `audit_report_third_party.md` for a task knows immediately which sections are missing without having to grep themselves.

## 17.3 The `X_test` grep

The most-load-bearing grep in the project: the validator (Layer 1) and Agent F of the forensic committee (Layer 2) both search every runner / hill-climb file for the patterns `X_test`, `y_test`, `splits['test']`, `splits["test"]`. Any hit fails the audit.

The grep is deliberately *over-broad*. A legitimate use of `X_test` inside `framework/final_report.py` is allowed (that file is exempt; it is the only legal reader). Anywhere else, even in a comment, even in a string literal, the grep fires. This is intentional: a hit in a comment is still a smell ("why is the protocol's most important variable being mentioned in a runner file?") and worth investigating.

The grep's *pattern* is documented in:

- `framework/validator.py:_FORBIDDEN_TEST_REFS` (the regex).
- `skills/autoresearch-pack/skills/train-val-test-invariants/SKILL.md` (the rule).
- [Ch. 11 — Testing Overview](../part_3_processes/11_testing_overview.md) (the explanation).

Three-way redundancy. A change to one without the others would surface as a coverage gap in the next `audit_pack.py` run.

## 17.4 The forbidden-path audit

A specific grep added in May 2026: `_backup_pre_*` paths under `modeling/` or `analysis/` are forbidden in the cohort scoreboard. Lessons-Learned row 25 codifies the rule. The implementation in `framework/_final_audit.py`:

```python
forbidden = list((ROOT / "modeling").glob("*/**/_backup_pre_*")) + \
            list((ROOT / "analysis").glob("*/**/_backup_pre_*"))
if forbidden:
    print(f"[FORBIDDEN] {len(forbidden)} _backup_pre_* paths under modeling/ or analysis/")
    for p in forbidden:
        print(f"  - {p.relative_to(ROOT)}")
    sys.exit(1)
```

The rationale: `_backup_pre_*` is a deliberate convention for the human's spot-check ([Ch. 15](../part_3_processes/15_deprecation.md)), but the cohort scoreboard should not include a task that has a `_backup_pre_*` lying around — that means the previous state wasn't cleaned up after a deprecation.

## 17.5 The audit-pack section walker

`skills/autoresearch-pack/audit/audit_pack.py` walks every H2/H3 header in `autoresearch/CLAUDE.md`, `autoresearchindexspy/.../CLAUDE.md`, and `framework/CLAUDE_template.md`. The walker treats the H2/H3 as the search key; the search target is every SKILL.md's frontmatter `triggers` field and its body text.

The script is two passes:

1. **Build the section index.** Parse the three source CLAUDE.md files; emit `(file, level, header)` tuples.
2. **Build the skill index.** Parse every SKILL.md; collect the `triggers` field and the H1 header.
3. **Match.** For each section, find skills whose triggers / body contain the section header substring. Emit `coverage_report.md` with PASS / FAIL per section.

The walker is the project's own code-search engine. It runs in ~5 seconds. Its output is the contract that the protocol's documentation surface is complete.

## 17.6 The dashboard reasoning-annotation search

Per-task `autoresearch_results/dashboard.html` carries a "Reasoning" tab that lets the reviewer search the per-experiment annotations by keyword. Implementation: the dashboard HTML embeds the `reasoning_annotations.json` content; a small JavaScript filter narrows by substring. The dashboard's search is read-only and lightweight; it does not have the audit's enforcement role.

Cross-task search across the 112 per-task dashboards is not implemented. A reviewer who wants to find "every task that cited Bishop 2006 §5.5.2" would have to grep the underlying `reasoning_annotations.json` files. This is a missing tool — see "follow-up" below.

## 17.7 The skill-pack as a discoverability index

The 44 SKILL.md files in `skills/autoresearch-pack/skills/` each have YAML frontmatter that includes `triggers` (a list of phrases that, when seen in context, suggest the skill is relevant). The skill loader (Claude Code) uses these triggers to auto-load skills.

Sample frontmatter:

```yaml
---
name: citation-rigor
description: Enforces the canonical citation format for autoresearch annotations
triggers:
  - "citation"
  - "arXiv"
  - "(arXiv:"
  - "paper relevance"
  - "negative result"
---
```

This is structurally a search index: the trigger phrases are the keys, the SKILL.md is the value. The Skill tool's invocation is a search operation against this index.

## 17.8 What we cannot search

Three categories of code are hard to search with our current tooling:

1. **Cross-task experiment metadata.** Finding "every task where iter 12 of xgboost was the eventual champion" requires walking 112 `experiment_log.jsonl` files. There is no SQL-equivalent. A simple Python script can do it but it's not productised.
2. **Cross-task forensic risks.** Finding "every task with an Agent J warning (low backbone diversity)" requires walking 112 `forensic_audit.json` files. `framework/_summary.py` does this for a few cases but not generally.
3. **Cross-task citation usage.** Finding "every task that cited Bishop 2006" requires walking 112 `reasoning_annotations.json` files. No tool exists.

In each case the dataset is small enough (112 × small file) that a one-off Python script is the right answer; building a search service is not justified at our scale.

## 17.9 What we don't need

The SWE-book chapter 17 lists features of Google's Code Search: cross-repo indexing, language-aware navigation, build-graph integration. We don't need any of these at our scale:

- **Cross-repo indexing.** One repo.
- **Language-aware navigation.** Python only, modest scale, IDE / editor's built-in features suffice.
- **Build-graph integration.** No build system in the SWE-book sense; `framework/run_all.py` is the entry point.

The minimum viable search is `ripgrep` plus the validator. That is what we have.

## 17.10 Related

- [Ch. 12 — Unit Testing](../part_3_processes/12_unit_testing.md): the validator as the grep-based audit.
- [Ch. 20 — Static Analysis](20_static_analysis.md): the grep patterns that enforce the protocol.
- [`framework/validator.py`](../../framework/validator.py): the section-mapping audit.
- [`skills/autoresearch-pack/audit/audit_pack.py`](../../skills/autoresearch-pack/audit/audit_pack.py): the skill-pack walker.

## Follow-up

A cross-task SQL-like view over `experiment_log.jsonl` + `forensic_audit.json` + `reasoning_annotations.json` would be valuable. Likely shape: a single `pandas` DataFrame keyed by `(task_slug, experiment_num)` with one column per metric and per agent. A future ADR could pin this.
