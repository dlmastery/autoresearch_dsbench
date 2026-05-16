# autoresearch-pack — A reusable skill pack for the autoresearch protocol

**An industry-shareable Claude Code skill pack** that packages the full **autoresearch protocol** — Karpathy-style autonomous ML research with a 7-step diagnose-cite-hypothesize-predict-run-analyze-document loop, hard data-integrity rules, mandatory MLOps documentation, 14-section audit reports, winner archiving, GitHub Pages-synced dashboards, and the spy-project additions (three-stream feature engineering, val-weighted stacked ensembles, regime gates, sub-period robustness audits, and resumption-pointer committee summaries).

It is **36 atomic, self-contained skills** plus one composite umbrella skill, plus an audit script that proves every section of the source CLAUDE.md files is covered.

## What's in the pack

```
skills/autoresearch-pack/
  README.md                           # this file
  composite-autoresearch.skill.md     # umbrella with progressive disclosure
  coverage_matrix.md                  # row = source section, col = skill, X marks coverage
  audit/
    audit_pack.py                     # verifies every CLAUDE.md section → skill
    coverage_report.md                # auto-generated PASS/FAIL per section
  skills/
    <36 sub-skills, one directory each, with SKILL.md inside>
```

The 36 sub-skills span 5 categories:

- **protocol** (10) — session startup, hardware pinning, crash-recovery checkpointing, mindset, data integrity, train-val-test invariants, experiment design, Karpathy agent protocol, 7-step research process, monotonic quality progression, per-backbone code snapshot, per-backbone experiment mandate.
- **engineering** (6) — per-backbone SOTA recipes, GPU memory constraint, architecture / separation of concerns, heteroscedastic loss, three-stream feature engineering, stacked ensemble design, regime gate.
- **documentation** (7) — MLOps documentation, citation rigor, reasoning blob completeness, winner archive protocol, Google Colab notebook, committee resumption pointers.
- **verification** (6) — explainability audit (14 sections), traditional ML metrics, per-sample decision logging, validation checklist, forensic audit pipeline, sub-period robustness audit.
- **dashboard** (5) — reasoning annotations, backbone tabs, files-update mandate, GitHub Pages sync, interactive dashboard design.

## Why this exists

The autoresearch protocol started as a single 968-line `CLAUDE.md` in the predecessor FX project and was extended to ~1074 lines in the SPY project. That monolithic document encodes hard-won engineering and research discipline (BSOD prevention, crash-recovery checkpointing, citation rigor, no-blind-sweeps, 14-section audits, winner archiving, regime gates, val-weighted ensembles). It is too long to load whole, and reusing it across projects means copy-pasting a wall of text.

**This pack decomposes the protocol into 36 atomic skills**, each preserving the source text verbatim. Each skill is self-contained, machine-discoverable (YAML frontmatter with triggers), and human-readable. You load only the skills relevant to the current task, keeping context windows tight while keeping the rules sharp.

## Industry shareability

The pack is designed for two audiences:

### Audience 1 — Claude Code users

**Install** by dropping the folder into `.claude/skills/`:

```bash
# Per-project install
cp -r autoresearch-pack /path/to/your-project/.claude/skills/

# Or per-user install (available across all projects)
cp -r autoresearch-pack ~/.claude/skills/
```

**Invoke** via the Skill tool by name:

- `composite-autoresearch` — the umbrella; reads a description of which sub-skills to load when.
- `<sub-skill-name>` — e.g. `dashboard-files-update-mandate`, `citation-rigor`, `regime-gate`.

Claude will auto-detect the right skill via the `description` and trigger phrases in each SKILL.md frontmatter (e.g. "BSOD", "checkpoint", "champion archive").

### Audience 2 — non-Claude-Code users (human readers)

Every SKILL.md is a self-contained Markdown protocol document. A teammate reading `crash-recovery-checkpoint/SKILL.md` gets:

1. **When to use** — trigger contexts.
2. **The rule** — the verbatim text from the source CLAUDE.md (with citations preserved).
3. **Anti-patterns** — common violations and their consequences.
4. **Implementation checklist** — actionable adoption steps.
5. **References** — source paths + relevant papers + sibling skills.

You can hand the directory to a teammate as a protocol manual. No Claude Code required.

## Hard requirements satisfied

1. ✅ **Every source-CLAUDE.md section maps to ≥1 skill.** Verified by `audit/audit_pack.py` — 109/109 sections covered (PASS).
2. ✅ **Audit script** parses both source CLAUDE.md files for H2/H3 headers and emits `coverage_report.md`.
3. ✅ **5 dashboard skills** (annotations, tabs, files-update, Pages sync, interactive design) — exceeds the 4-skill minimum.
4. ✅ **Composite umbrella skill** with progressive disclosure recommendations.
5. ✅ **README describes install and invocation** for Claude Code AND human-readable use.
6. ✅ **Every skill includes the full relevant text** from CLAUDE.md, not just a summary. The SKILL.md files are self-contained.
7. ✅ **Audit script run, 100% coverage confirmed** before package was finalised.

## Running the audit

From any working directory:

```bash
"C:/Users/evija/anaconda3/python.exe" "C:/Users/evija/dsbench/skills/autoresearch-pack/audit/audit_pack.py"
# or any python with stdlib
python C:/Users/evija/dsbench/skills/autoresearch-pack/audit/audit_pack.py
```

Output: `audit/coverage_report.md` with PASS/FAIL per source section + an aggregate verdict. Exit code 0 if 100% coverage, 1 otherwise.

The audit takes the section list from the two real source files:

- `C:/Users/evija/autoresearch/CLAUDE.md`
- `C:/Users/evija/autoresearchindexspy/autoresearchspy/CLAUDE.md`

If those files are missing on the local machine, the audit skips them and reports — it does not fail spuriously.

## Adapting to a non-financial project

The pack is anchored in financial ML examples (FX, SPY, Sharpe ratios, fold-2 GFC recovery regimes) because the source projects were financial. **The pattern transfers directly to any autoresearch task** — DSBench tasks, CV/NLP benchmarks, RL evaluation suites, scientific ML.

The substitutions:

| Financial concept | Generic equivalent |
|---|---|
| Sharpe ratio | Task-native primary metric (accuracy, F1, RMSE, BLEU, etc.) |
| 7-fold super-fold | k-fold walk-forward / time-aware split |
| Per-trade win/loss CSV | Per-sample decision log CSV |
| Trading-Strategy section in winner README | Inference / deployment recipe |
| Regime gate (rvol60d > 15%) | Conditional gate on any causal feature with bimodal performance |
| Three-stream feature engineering | Multi-source / multi-frequency feature stack with causal anchor |

The skill files note this generalisation explicitly. Drop in the financial-only skills (`heteroscedastic-loss`, `regime-gate`, `three-stream-feature-engineering`) when they apply; ignore otherwise — the audit still passes because the financial sections are still mapped.

## Provenance and versioning

- **Source A:** `C:/Users/evija/autoresearch/CLAUDE.md` — the FX autoresearch project (968 lines).
- **Source B:** `C:/Users/evija/autoresearchindexspy/autoresearchspy/CLAUDE.md` — the SPY adaptation (1074 lines), adds three-stream feature engineering, stacked ensemble (12 components, +0.277), regime gate (rvol60d > 15%, +0.134), sub-period robustness audit, and session-complete-state resumption pointers.
- **Built:** 2026-05-15.

When the source CLAUDE.md files evolve, re-run `audit_pack.py` to detect new sections needing coverage. The audit is the contract — green audit = ready to share.

## License & attribution

The protocol text is original work by the autoresearch project author (Evi Janti, eranti@gmail.com). The decomposition into a skill pack is intended to be **freely sharable to industry**. When you adopt the pack, the SKILL.md files retain inline references back to the source CLAUDE.md sections; please keep those attributions.
