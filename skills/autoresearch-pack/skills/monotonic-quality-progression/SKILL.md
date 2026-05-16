---
name: monotonic-quality-progression
description: Monotonic quality progression — every experiment justified, champion lineage tracked, plateaus trigger structural change, quality ratchet protects gains. Triggers on "monotonic improvement", "quality ratchet", "champion lineage", "plateau", "structural change".
metadata:
  category: protocol
  source: autoresearch
  related: [karpathy-agent-protocol, seven-step-research-process, winner-archive-protocol]
---

# Monotonic Quality Progression

## When to use

- When deciding whether to KEEP or DISCARD an experiment that moved one metric up and another down.
- After 3 consecutive DISCARDs — apply the "go deeper" rule.
- When evaluating a bold experiment whose composite dropped >2.0 — diagnose before continuing.

## The rule

> ### Monotonic Quality Progression (NEVER regress)
> The experiment loop must work towards monotonic increase in quality. This means:
> - **Never run an experiment you can't justify.** Every experiment must have a written rationale citing literature or prior empirical evidence from this project.
> - **Track the champion lineage.** Document the chain: Exp1 (baseline) → Exp5 (residual skip, +3x) → Exp10 (LR bump, +1.2x) → etc. Each link must explain WHY the improvement happened.
> - **When you hit a plateau, go deeper.** If 3+ consecutive experiments are DISCARD, you're in a local optimum. The answer is NOT more hyperparameter tweaks — it's a structural change: different architecture, different loss, different features, different training procedure.
> - **Protect gains.** When trying bold changes, if the result is far worse (composite drops >2.0), investigate WHY before trying the next thing. Understanding failures is as valuable as finding improvements.
> - **Quality ratchet:** once a metric improves, treat the new level as the floor. If a change improves test Sharpe but regresses val Sharpe below the previous champion, it's a DISCARD — both must improve or at least hold.

## Anti-patterns

- **"It's a DISCARD but let me try the same idea with a slightly different value"** — that's grid-searching a known dead axis. Go deeper instead.
- **Cherry-picking the metric that improved.** Quality ratchet: BOTH val and test must hold or improve.
- **Skipping the lineage document.** A 6-month-old champion that nobody can explain is a deployment liability.
- **Treating every catastrophic result as noise** — composite drops >2.0 are signal, often the most informative signal you'll get.
- **Treating each DISCARD in isolation.** 3 in a row is a structural signal — stop tweaking, change architecture/loss/features.

## Implementation checklist

1. Maintain `champion_lineage.md` (or equivalent in the checkpoint) — a directed chain of champions with the WHY of each transition.
2. The KEEP/DISCARD logic checks BOTH `min(test_sharpe, val_sharpe) > previous_champion` AND `n_negative_folds <= previous_champion`.
3. After 3 consecutive DISCARDs, the next checkpoint MUST include a "structural change" entry — what architecture/loss/feature/procedure change is being attempted.
4. After a >2.0 composite drop, write a "post-mortem" entry: which fold collapsed, what the prediction distribution looks like, what feature drift looks like.
5. The `seven-step-research-process` Step 3 (`prediction`) is the contract — Step 5 (`learning`) closes it.

## References

- Source: `autoresearch/CLAUDE.md` section "Monotonic Quality Progression (NEVER regress)"
- Karpathy (2019) "A Recipe for Training Neural Networks" — the "don't be afraid of a long debugging session" principle.
- Related: `karpathy-agent-protocol`, `seven-step-research-process`, `winner-archive-protocol`.
