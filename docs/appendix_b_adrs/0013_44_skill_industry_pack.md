# ADR-0013: Decompose protocol into 44 industry-shareable skills

## Status

Accepted (2026-05-15).

## Context

The autoresearch protocol is encoded in three source `CLAUDE.md` files:

- `C:/Users/evija/autoresearch/CLAUDE.md` (FX project, 968 lines).
- `C:/Users/evija/autoresearchindexspy/autoresearchspy/CLAUDE.md` (SPY project, 1074 lines).
- `C:/Users/evija/dsbench/framework/CLAUDE_template.md` (DSBench, ~660 lines).

Sharing the protocol with another team or porting it to a non-financial project means copy-pasting one of these walls of text. Reusing only the parts that apply means manual surgery — error-prone and unreviewable.

Claude Code's Skill mechanism solves this: each Markdown document is an atomic, self-contained protocol unit with YAML frontmatter for machine discovery. We can decompose the wall of text into N atomic skills, each with a trigger description, the verbatim rule, anti-patterns, an adoption checklist, and references.

## Decision

Build `skills/autoresearch-pack/` with **44 atomic skills + 1 composite umbrella + 1 audit script**.

Structure:

```
skills/autoresearch-pack/
├── README.md                           # install + invocation guide
├── composite-autoresearch.skill.md     # progressive-disclosure umbrella
├── coverage_matrix.md                  # row = source-CLAUDE section, col = skill
├── audit/
│   ├── audit_pack.py                   # asserts every section maps to ≥ 1 skill
│   └── coverage_report.md              # PASS/FAIL, auto-generated
└── skills/<44 sub-skills>/SKILL.md
```

Five categories (count subject to the split-skill churn):
- **protocol** (~12) — session-startup, hardware-pinning, crash-recovery, mindset, data-integrity.
- **engineering** (~8) — SOTA recipes, GPU memory, separation of concerns, heteroscedastic loss.
- **documentation** (~9) — MLOps docs, citation rigor, reasoning blob completeness, winner archive.
- **verification** (~8) — explainability audit, traditional metrics, per-sample decisions, forensic audit.
- **dashboard** (~7) — reasoning annotations, backbone tabs, files-update, Pages sync, interactive design.

Three audit invariants enforced by `audit_pack.py`:

1. Every H2/H3 in the three source CLAUDE.md files maps to ≥ 1 skill.
2. Every skill listed in `coverage_matrix.md` exists as a directory.
3. Every skill directory contains a `SKILL.md` with the 5 mandatory sections.

Current state: **156/156 source sections covered, PASS**.

## Consequences

**Easier:**

- A team adopting the protocol drops the folder into `.claude/skills/` and gets only the skills relevant to their context (Claude auto-discovers by trigger phrase).
- Non-Claude-Code users read the SKILL.md files as a protocol manual.
- New DSBench corrections (e.g., Lesson 22 — the four-layer audit gate) extend or add skills; the audit script forces the corresponding `coverage_matrix.md` row to be updated.

**Harder:**

- 44 small files vs 1 big one: navigation requires the `coverage_matrix.md` or the umbrella skill. Mitigated by the table-of-contents in the umbrella and the README install guide.
- A protocol change requires updating BOTH the source CLAUDE.md AND the relevant skill(s) — a discipline overhead. The audit catches mismatches.

**Riskier:**

- A skill that drifts from its source-CLAUDE section is hard to detect manually. The audit only checks that the section *maps* to a skill, not that the content matches. Mitigated by the 2026-05 batch update process: every correction lands in CLAUDE.md AND the skill in the same commit.

## Related

- [`../part_2_culture/03_knowledge_sharing.md`](../part_2_culture/03_knowledge_sharing.md)
- [`../part_2_culture/07_measuring_engineering_productivity.md`](../part_2_culture/07_measuring_engineering_productivity.md)
- `skills/autoresearch-pack/README.md`.
