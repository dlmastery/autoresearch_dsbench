---
name: per-backbone-experiment-mandate
description: Per-backbone N-experiment mandate (default 50) — full literature-aware exploration with arch variants, cross-variants, feature changes, multi-seed, novel regularizers. Each experiment cites its paper. Negative results documented. Triggers on "50-experiment mandate", "per-backbone exploration", "SOTA exploration", "axis exhausted".
metadata:
  category: protocol
  source: autoresearch
  related: [per-backbone-sota-recipes, karpathy-agent-protocol, per-backbone-code-snapshot]
---

# Per-Backbone N-Experiment Mandate

## When to use

- Planning the experiment budget for a new backbone.
- Asked "is this backbone done yet?" — answer with the mandate count.
- Deciding whether to move to the next backbone or keep exploring.

## The rule

> ### Per-Backbone 50-Experiment Mandate (MANDATORY, not optional)
>
> **Every backbone gets a full 50-experiment exploration.** Do not stop early because "axes look exhausted." The mandate:
>
> 1. **50 experiments per backbone** — no fewer. If standard HP sweeps plateau, explore:
>    - Architectural variants from arXiv literature through 2026 (see per-backbone table below)
>    - Cross-variant combinations (e.g., attention-LSTM × dropout tuning)
>    - Feature engineering changes (input projections, feature selection)
>    - Multi-seed studies on the champion to characterize variance
>    - Regularization beyond weight decay (label smoothing, mixup, stochastic depth)
>
> 2. **Research latest SOTA (2024-2026 arXiv papers) before declaring any backbone done.** For each backbone category, the literature evolves yearly:
>    - **LSTM/RNN**: xLSTM (Beck et al. 2024), Mamba (Gu & Dao 2024), Retentive Networks (Sun et al. 2023), DA-RNN with attention (Qin 2017), LayerNorm-LSTM (Ba 2016), AWD-LSTM (Merity 2018), GRU comparison (Cho 2014), stacked multi-layer (Graves 2013)
>    - **Transformer TS**: PatchTST (Nie 2023), iTransformer (Liu 2024), TimesNet (Wu 2023), Informer (Zhou 2021), FEDformer (Zhou 2022), Crossformer (Zhang 2023), Autoformer (Wu 2021)
>    - **MLP TS**: TSMixer (Chen 2023), N-HiTS (Challu 2023), N-BEATS (Oreshkin 2020), DLinear (Zeng 2023) — "Are Transformers Effective for TS?"
>    - **Foundation**: TimesFM (Das 2024), Chronos (Ansari 2024), Moment (Goswami 2024), LFM2 (Liquid 2024)
>    - **GBM**: XGBoost, LightGBM, CatBoost — tune n_estimators, max_depth, learning_rate, regularization
>
> 3. **Each experiment must cite its paper/source** — no "let me try X". Per CLAUDE.md rule 4.
>
> 4. **Document all 50 in research_journal.md** — even DISCARDs. Negative results are informative.
>
> 5. **Only after 50 experiments** may a backbone be declared "done" and progression to the next backbone resume.

### Budget exceptions (Tier-3 GBM example)

The mandate is per architectural family. Where 3 closely-related backbones share a budget — e.g. XGBoost/LightGBM/CatBoost share 50 split 20/15/15 — record the split in the project's CLAUDE.md and treat each as its own backbone for archiving/snapshot purposes.

### Tunable for project scale

For smaller projects (e.g. dsbench tasks under tight wall-clock) the mandate may be tuned down (25-experiment variant). Whatever the chosen N, it is the **minimum** — early-stopping a backbone is the mandate violation, not the exact number.

## Anti-patterns

- **"Axes look exhausted after 12 experiments — moving on."** That's a local-optimum signal — go deeper (code change, novel regularizer, multi-seed study). The mandate exists exactly to defeat this temptation.
- **Counting variance-check reruns as separate experiments.** Multi-seed is part of the mandate, but a 3-seed variance check is 3 experiments — log all 3.
- **Skipping the SOTA literature review.** Without 2024-2026 papers, the exploration repeats 2022-era ideas.
- **Treating a DISCARD as a wasted experiment.** Negative results define the exhausted axes — document them or the next session re-tries.
- **Not citing the paper that motivated experiment N.** Citation rigor applies to every entry, even DISCARDs.

## Implementation checklist

1. Maintain a per-backbone experiment counter in the checkpoint.
2. Pre-plan the 50 experiments across HP axes + architectural variants + multi-seed (5 axes × 8-10 each + 5-seed studies typically fills 50).
3. Each experiment's reasoning annotation cites a specific paper.
4. DISCARDs land in `research_journal.md` with the same six-field structure as KEEPs.
5. At experiment 50, write a "backbone retrospective" entry summarising what was learned about that backbone family.

## References

- Source: `autoresearch/CLAUDE.md` section "Per-Backbone 50-Experiment Mandate (MANDATORY, not optional)"
- Source: `autoresearch/CLAUDE.md` Tier-3 GBM budget allocation table.
- Related: `per-backbone-sota-recipes`, `karpathy-agent-protocol`, `per-backbone-code-snapshot`.
