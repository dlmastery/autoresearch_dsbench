---
name: karpathy-agent-protocol
description: Karpathy-adapted autoresearch agent protocol — always start from champion, stop on consecutive discards, explore + radical, cite reasoning, never stop, checkpoint, deep per-fold analysis, code changes allowed. Triggers on "agent protocol", "Karpathy", "current best config", "consecutive discards".
metadata:
  category: protocol
  source: autoresearch
  related: [seven-step-research-process, monotonic-quality-progression, crash-recovery-checkpoint]
---

# Karpathy-Adapted Autoresearch Agent Protocol

## When to use

- Every decision about what to try next.
- After a run of consecutive DISCARDs — apply the "stop and rethink" rule.
- When tempted to "wander off from the champion" — apply the "start from current best" rule.
- When considering a code change vs another HP tweak.

## The rule

> ### Autoresearch Agent Protocol (Karpathy-adapted)
> 1. **Always start from the current best config.** Every experiment modifies ONE thing from the best. If it improves, it becomes the new best. If it doesn't, revert and try a different direction. Never wander off from the best baseline.
> 2. **If you see consecutive discards, stop and rethink.** Multiple failures mean your hypothesis about what to change is wrong. Re-read the per-window results. Look at which folds are weak and WHY. Don't keep guessing.
> 3. **Explore around the best AND try radical changes.** Most experiments should be small tweaks around the champion. But occasionally try something bold (different architecture, very different seq_len) to escape local optima.
> 4. **Cite your reasoning for every experiment.** "I'm trying X because fold Y has negative Sharpe due to Z, and paper W suggests this fix." Not "let me try X and see."
> 5. **The agent never stops.** If out of ideas, research deeper: read the LFM2 technical report, adapter papers, FX microstructure literature. Think harder. Try combining near-misses.
> 6. **Checkpoint reasoning to memory every few minutes.** The laptop crashes often. After every experiment (or every ~3 minutes of reasoning), save the current state to `memory/project_autoresearch_checkpoint.md`: what the current champion is, what was just tried, what the leading hypothesis is for the next experiment, and which folds are weak and why. On session start, read this checkpoint to recover full context without re-reading logs.
> 7. **Deep per-fold failure analysis every iteration.** For each fold with negative test Sharpe, explain WHY: what regime it is, what dates, what market conditions, what the uncertainty outputs reveal (high aleatoric = noisy data, high epistemic = model doesn't know, low confidence = skip signal). Use this to guide the next experiment.
> 8. **Code changes are allowed.** The agent may modify the Python codebase (model architecture, loss function, training loop, features, evaluation) if it has a principled reason. Save modified versions to `autoresearch/code_versions/` with a version number. Code changes are the most powerful lever — hyperparams only go so far.

## Anti-patterns

- **Drifting away from the champion.** After a DISCARD, set the next experiment's baseline back to the champion — not to the previous DISCARD config.
- **Wandering instead of rethinking.** 3+ consecutive DISCARDs and you're guessing — STOP. Reanalyze. Possibly checkpoint a "diagnosis-only" entry.
- **Hyperparam-only thinking.** When the HP surface is exhausted, the answer is a code change (architecture, loss, features), not a finer HP grid.
- **"Let me try X and see"** — every experiment needs the diagnosis-citation-hypothesis-prediction chain.
- **Random restart from a non-champion config** — pollutes the lineage and breaks the monotonic-quality-progression invariant.

## Implementation checklist

1. Every experiment command derives from `best_config.json` + ONE delta.
2. After 3 DISCARDs in a row, write a "diagnosis entry" in the checkpoint summarising why the hypothesis is failing — read it before authoring experiment N+1.
3. Maintain an `code_versions/` directory; major code changes get a version number and a snapshot.
4. The reasoning_annotation entry must encode steps 1, 4, 7 explicitly (which fold is weak, paper cited, predicted target).
5. The agent never asks "what should I do?" — it always has a next experiment ready (or a `diagnosis-rethink` entry explaining why it doesn't).

## References

- Source: `autoresearch/CLAUDE.md` section "Autoresearch Agent Protocol (Karpathy-adapted)"
- Karpathy (2019) "A Recipe for Training Neural Networks" (karpathy.github.io)
- Related: `seven-step-research-process`, `monotonic-quality-progression`, `crash-recovery-checkpoint`, `per-backbone-code-snapshot`.
