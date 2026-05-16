# Skill Pack — The 44-Skill Industry-Shareable Bundle

> Audience: a Claude Code user or a teammate who wants to adopt the autoresearch protocol without copy-pasting a 968-line CLAUDE.md.

## 1. What's in the pack

`skills/autoresearch-pack/` decomposes three source CLAUDE.md files into **44 atomic, self-contained skills** plus one composite umbrella skill. Each skill is a Markdown document with YAML frontmatter, a trigger description, the verbatim rule from the source CLAUDE.md, anti-patterns, an implementation checklist, and references.

```
skills/autoresearch-pack/
├── README.md
├── composite-autoresearch.skill.md         # umbrella with progressive disclosure
├── coverage_matrix.md
├── audit/
│   ├── audit_pack.py                       # verifies every source-CLAUDE.md section → skill
│   └── coverage_report.md                  # PASS/FAIL per section, auto-generated
└── skills/
    └── <44 sub-skills, one directory each, with SKILL.md inside>
```

## 2. Why 44

The skill count grew with the protocol:

| Wave | Skills | Source |
|---|---|---|
| Foundation (FX project) | 31 | `C:/Users/evija/autoresearch/CLAUDE.md` (968 lines) |
| SPY additions | 5 | `C:/Users/evija/autoresearchindexspy/autoresearchspy/CLAUDE.md` (1074 lines) |
| DSBench corrections (2026-05) | 8 NEW + 5 EXTENDED | `framework/CLAUDE_template.md` (see Lessons 1-26) |
| **Total** | **44** | — |

The 8 DSBench-only new skills are:

1. `metric-sign-convention` — `delta = test - baseline` works for all metrics because `_score()` is higher-is-better.
2. `extended-hill-climb-phase` — 200-iter recovery cycle for tasks losing to baseline.
3. `problem-type-aware-audit-thresholds` — calibrated thresholds for `qa_excel` agents B / D / E.
4. `regression-early-stopping-discipline` — sklearn early-stop val > train is normal per Bishop 2006 PRML §5.5.2.
5. `qa-task-feature-engineering` — 9-D structural stack + 38-task one-hot for Modeloff.
6. `small-n-stride-split` — stride-5 interleave for `n ∈ [5, 20]`.
7. `cross-task-pooling-discipline` — pool train across 38 tasks, score per-task.
8. `task-description-disclosure` — `<details>` "About this task" block on every per-task dashboard.

The 5 extended skills are `forensic-audit-pipeline`, `winner-archive-protocol`, `interactive-dashboard-design`, `train-val-test-invariants`, `mlops-documentation`. See `skills/autoresearch-pack/coverage_matrix.md` for the full row-by-column matrix.

## 3. Five categories

| Category | Count | Examples |
|---|---|---|
| protocol | 12 | session-startup, hardware-pinning, crash-recovery-checkpoint, karpathy-agent-protocol |
| engineering | 8 | per-backbone-sota-recipes, gpu-memory-constraint, heteroscedastic-loss, three-stream-feature-engineering, regime-gate |
| documentation | 9 | mlops-documentation, citation-rigor, reasoning-blob-completeness, winner-archive-protocol, committee-resumption-pointers |
| verification | 8 | explainability-audit-14-section, traditional-ml-metrics, per-sample-decision-logging, forensic-audit-pipeline, sub-period-robustness-audit |
| dashboard | 7 | dashboard-reasoning-annotations, dashboard-backbone-tabs, github-pages-dashboard-sync, interactive-dashboard-design, task-description-disclosure |

## 4. Skill anatomy

Each `SKILL.md` has 5 mandatory sections:

```markdown
---
name: skill-name
description: When to invoke this skill (≤ 200 chars trigger phrase)
---

# Skill Name

## When to use
Trigger contexts in plain English.

## The rule
Verbatim text from the source CLAUDE.md, citations preserved.

## Anti-patterns
Common violations + their consequences.

## Implementation checklist
Actionable adoption steps.

## References
Source paths + relevant arXiv papers + sibling skills.
```

A teammate reading one SKILL.md gets the full rule without loading the rest of the pack.

## 5. The umbrella skill

`composite-autoresearch.skill.md` is the progressive-disclosure entry point. It maps user intents ("I'm starting a new autoresearch project", "I just hit a champion", "My audit is failing on Agent E") to the right subset of sub-skills to load.

## 6. The audit script

```powershell
& "C:/Users/evija/anaconda3/python.exe" skills/autoresearch-pack/audit/audit_pack.py
```

The auditor:
1. Parses all H2/H3 headers from the three source CLAUDE.md files.
2. For each header, checks the row exists in `coverage_matrix.md`.
3. For each row, checks at least one `X` mark exists.
4. For each skill mentioned in the matrix, verifies the corresponding `SKILL.md` exists.
5. Writes `audit/coverage_report.md` with PASS/FAIL per section.

Current state: **156/156 sections covered, PASS**.

## 7. Industry shareability

The pack is designed to be **installed by drop-in copy**:

```powershell
# Per-project
Copy-Item -Recurse skills\autoresearch-pack <your-project>\.claude\skills\

# Per-user
Copy-Item -Recurse skills\autoresearch-pack $env:USERPROFILE\.claude\skills\
```

Adopters who don't use Claude Code still benefit — the SKILL.md files are self-contained markdown protocol documents that read as a manual. The financial-only skills (`heteroscedastic-loss`, `regime-gate`, `three-stream-feature-engineering`) generalise as documented in `skills/autoresearch-pack/README.md` § "Adapting to a non-financial project".

## 8. Related

- [`../adr/0013_44_skill_industry_pack.md`](../adr/0013_44_skill_industry_pack.md)
- [`../slos/05_documentation_freshness.md`](../slos/05_documentation_freshness.md)
- The pack itself: `C:/Users/evija/dsbench/skills/autoresearch-pack/`
