---
name: seven-step-research-process
description: The 6/7-step research-driven experiment selection process — diagnose, cite, hypothesize, predict, run ONE, analyze, document. No blind sweeps. Triggers on "7-step", "research process", "diagnose-cite-hypothesize", "predict-then-run", "no grid search".
metadata:
  category: protocol
  source: autoresearch
  related: [karpathy-agent-protocol, citation-rigor, reasoning-blob-completeness]
---

# 7-Step Research-Driven Experiment Selection

## When to use

- BEFORE every single experiment. No exceptions.
- When the runner is idle and you're deciding what to try next.
- When the temptation arises to launch a hyperparameter sweep — apply this process instead.

## The rule

> ### Research-Driven Experiment Selection (STRICT — no blind sweeps)
> The experiment loop is NOT a grid search. It is a research process. Every single experiment must follow this exact sequence:
>
> **Step 1 — Diagnose the champion's weakness.** Look at the per-fold test results. Which folds are weakest? What regime are they? What do the uncertainty metrics say? What does the win/loss spread look like for those folds? Identify the SPECIFIC failure mode (e.g., "fold 2 post-crash recovery has low IC=0.08, high epistemic uncertainty — model hasn't seen enough crisis-recovery data").
>
> **Step 2 — Search the literature.** Based on the diagnosis, search arXiv / known papers for techniques that address the failure mode. Examples:
> - Weak on volatile regimes → regime-aware training, volatility scaling (Kiraly et al. 2020)
> - High epistemic in specific folds → data augmentation, ensemble methods (Lakshminarayanan et al. 2017)
> - Overfitting to majority regime → focal loss (Lin et al. 2017), re-weighting
> - Architecture ceiling hit → residual connections (He et al. 2016), attention mechanisms (Vaswani et al. 2017)
> - LR too high/low → cyclical LR (Smith 2017), warmup (Goyal et al. 2017)
>
> **Step 3 — Form a hypothesis and predict the outcome.** Write down: "I hypothesize that [change X] will improve [metric Y] on [fold Z] because [paper/principle]. I predict composite will move from [current] to approximately [target]." If you can't write this sentence, you don't understand what you're doing. Stop and think more.
>
> **Step 4 — Run ONE experiment.** Execute the change. ONE change only.
>
> **Step 5 — Analyze against prediction.** Did the result match your prediction? If yes, why? If no, what does that tell you about your mental model? Update your understanding.
>
> **Step 6 — Document everything.** Write the full cycle (diagnosis → literature → hypothesis → prediction → result → learning) into the experiment log and checkpoint. This creates a research trail that prevents repeating failed ideas.
>
> **The goal is monotonic improvement.** Every experiment should have a principled reason to believe it will improve composite score. Random guessing wastes GPU and time. If you're out of ideas for hyperparameters, the answer is almost always a CODE CHANGE — modify the architecture, loss function, or feature engineering.

## Anti-patterns

- **Skipping Step 3 — running without a numeric prediction.** Without a predicted target, Step 5 (analyse) is meaningless; you can't tell if the result matched expectations.
- **Citing "arxiv paper on batch size"** instead of the full reference. See `citation-rigor` skill — partial citations break institutional memory.
- **Multi-parameter delta** (Step 4). One change only. If you really need to bundle two, that's two experiments.
- **Discarding the Step 5 analysis as soon as a new result lands** — you lose the learning that prevents repeating the failure.
- **Treating "the literature search was inconclusive" as permission to guess.** If literature is inconclusive, run a deliberately structured ablation — but the ablation itself is the hypothesis.

## Implementation checklist

1. Write the `diagnosis` field of `reasoning_annotations.json` BEFORE running the experiment.
2. Write the `citations`, `hypothesis`, `prediction` fields BEFORE running.
3. The runner refuses to launch if any of those four fields are empty.
4. After the run, write `verdict` and `learning` IMMEDIATELY — do not start the next experiment first.
5. Mirror the same six fields in `research_journal.md` as a markdown narrative.

## References

- Source: `autoresearch/CLAUDE.md` section "Research-Driven Experiment Selection (STRICT — no blind sweeps)"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` section "Research-Driven Experiment Selection (STRICT — no blind sweeps)"
- Karpathy (2019) "A Recipe for Training Neural Networks".
- Related: `karpathy-agent-protocol`, `citation-rigor`, `reasoning-blob-completeness`, `dashboard-reasoning-annotations`.
