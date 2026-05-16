---
name: committee-resumption-pointers
description: Committee summary / resumption pointers — the top-of-CLAUDE.md block that captures session-complete state for a fresh laptop pickup. Includes champion composite, stacked KEEPs, critical caveats, resumption commands, and "what's left for a future session". Triggers on "session-complete state", "resumption pointers", "committee summary", "top-of-CLAUDE.md", "deployable champion", "fresh laptop", "what's left".
metadata:
  category: documentation
  source: autoresearchindexspy
  related: [crash-recovery-checkpoint, session-startup, mlops-documentation]
---

# Committee / Resumption Pointers (top-of-CLAUDE.md block)

## When to use

- End of a major session — capture the entire state at the top of CLAUDE.md.
- Hand-off to a new contributor or new laptop.
- After a multi-week project arc, before a long break.

## The rule

The pattern below is taken verbatim from `autoresearchindexspy/autoresearchspy/CLAUDE.md`. It's the FIRST block in the file (before `## On Session Start`) so any reader — human, fresh Claude session, external auditor — can fully resume in 60 seconds.

> **🏆 SESSION-COMPLETE STATE (2026-05-04, after 28 commits, 59 distinct runs)**
>
> **Deployable champion**: 12-component val-weighted ensemble + regime gate (rvol60d > 15%) — composite **+0.368** on 1410-day held-out test (2008-2025).
>
> **Three stacked validated KEEPs**:
> 1. Asian/EU pre-market block (+0.330 composite over daily-only) — `data/asian_premarket.py`
> 2. Val-weighted 12-component ensemble (+0.277) — `_ensemble_val_weighted.py`
> 3. Regime gate `rvol60d > 15%` (+0.134) — `_ensemble_regime_gated.py`
>
> **Cumulative gain**: -0.373 (daily-only) → **+0.368** (champion) = +0.741 stacked.
>
> **Critical caveat**: model is a CRISIS-TRADE SPECIALIST. Sub-period sharpe 2008-2012 = +1.10, 2021-2025 = -0.67. Regime gate prevents trading in low-vol bull regimes (only ~30% of days in 2024-2025) but doesn't generate alpha there. See `autoresearchspy/autoresearch_results/champion_verification/robustness_audit.txt`.
>
> **Resumption pointers (for a fresh laptop)**:
> - Read `autoresearchspy/DEPLOYMENT.md` — production deployment recipe
> - Read `autoresearchspy/autoresearch_results/research_journal.md` — full session arc
> - Read `autoresearchspy/memory/project_autoresearch_checkpoint.md` — exact next-experiment commands
> - Run `python -m autoresearchspy._ensemble_regime_gated` — reproduces +0.368 verification
> - Run `python -m autoresearchspy._ensemble_robustness` — reproduces regime-dependence audit
>
> **What's left for a future session** (all out of scope for the 2026-05 session):
> - Forward OOS validation on 2026+ data when available
> - Paid Barchart Premier hourly history (yfinance 730d cap blocks intraday training)
> - Stacking via meta-learner (requires runner change to log val predictions)
> - Regime-conditional model architecture (better than single-rule gating)

### Template (copy-paste for any autoresearch project)

```markdown
**🏆 SESSION-COMPLETE STATE (<date>, after <N> commits, <M> distinct runs)**

**Deployable champion**: <short name> — composite **<X>** on <Y>-day held-out test (<date range>).

**Stacked validated KEEPs**:
1. <KEEP 1 description> (+<gain> composite over <prior baseline>) — `<file>`
2. <KEEP 2 description> (+<gain>) — `<file>`
3. ...

**Cumulative gain**: <baseline> → **<champion>** = +<delta> stacked.

**Critical caveats**: <list of regime-dependence, data-source caveats, deployment risks>. See <link to audit>.

**Resumption pointers (for a fresh laptop)**:
- Read `<deployment doc>`
- Read `<research journal>`
- Read `<checkpoint>`
- Run `<reproduction command 1>`
- Run `<reproduction command 2>`

**What's left for a future session**:
- <Item 1>
- <Item 2>
- ...
```

## Anti-patterns

- **Resumption pointers buried in section 7 of the CLAUDE.md.** Put them FIRST — readers don't read past the first screen.
- **No "what's left" list** — the next session re-discovers ideas you already considered.
- **Critical caveats missing.** A clean champion summary with no caveats reads like a sales pitch.
- **Reproduction commands not provided.** "Run the ensemble" forces the next session to search; specify `python -m autoresearchspy._ensemble_regime_gated`.
- **Stale block.** Update the block at session end; out-of-date summaries are worse than no summary.

## Implementation checklist

1. At the top of project CLAUDE.md (before `## On Session Start`), add the block following the template.
2. Update at end of every major session — date, commit count, run count, champion delta.
3. Stacked KEEPs listed with their concrete + composite gain numbers.
4. Critical caveats explicit (regime dependence, data caps, deployment risks).
5. Resumption pointers list 3-5 files to read + 2-3 commands to run.
6. "What's left" enumerates known-but-deferred work.

## References

- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` top-of-file SESSION-COMPLETE STATE block.
- Source: `autoresearch/CLAUDE.md` section "Key protocol additions" (session-end packaging cadence).
- Related: `crash-recovery-checkpoint`, `session-startup`, `mlops-documentation`.
