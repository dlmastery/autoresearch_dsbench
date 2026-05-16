# ADR-0005: 25 iterations per backbone, every backbone, no early stop

## Status

Accepted (2026-05-15).

## Context

The autoresearch source CLAUDE.md (FX project) ran 50 iterations per backbone. Halving to 25 is a deliberate compute-budget decision for DSBench's 112-task fan-out: 50 iters × 5 backbones × 112 tasks = 28,000 experiments; 25 iters keeps the budget at 14,000 — still rich enough to explore each backbone's axis surface, half the wall-clock cost.

The harder question is **whether to allow early stop**. A backbone can look exhausted after 8 iterations — all axes either flat or regressed. Naive engineering says "stop and move to the next backbone". The autoresearch protocol says no, for two reasons:

1. **Negative results inform downstream backbones.** Knowing that `colsample=0.5` failed on XGBoost shapes the LightGBM `feature_fraction` proposal.
2. **Seed variance.** Iters 8 and 9 are seed perturbations (`seed ∈ {7, 99}` paired with the default `42`); stopping early skips the variance characterisation.

## Decision

**Every backbone runs 25 iterations.** No early stop. The proposals 11-25 are generated programmatically from a library of cited perturbations when the hand-curated 1-10 don't pre-fill them.

Two structural rules:

1. **Iter 1 is the published paper default.** Chen & Guestrin 2016 KDD for XGBoost; Ke et al. 2017 NeurIPS for LightGBM; Prokhorenkova et al. 2018 NeurIPS for CatBoost; etc.
2. **Iters 8 and 9 are seed perturbations.** Pair `seed = 7` and `seed = 99` with the default `seed = 42` to compute a 3-seed median champion. Without this, claimed champions can be variance flukes.

Loosely-coupled discipline: a backbone may be declared "done" only after all 25 iters land in `experiment_log.jsonl`. The dashboard's "experiments per backbone" counter exposes this.

## Consequences

**Easier:**

- Cross-task comparisons are well-defined: every task has 125 base experiments + (optionally) 200 extension experiments.
- A reviewer can trust a champion claim because variance characterisation is baked in.
- The reasoning-annotation requirement means every iter must cite a paper — the discipline rules out blind sweeping.

**Harder:**

- For tasks where one backbone dominates, the other 4 × 25 = 100 experiments feel wasteful. Mitigated by the extended 200-iter recovery for losers — those backbone iters still inform the extension.

**Riskier:**

- The seed-variance characterisation at iters 8 and 9 doesn't fully isolate `seed` from other axes. A future fix would be 3-seed × 1-config holdouts at the end of each 25-block.

## Related

- [`../part_3_processes/14_larger_testing.md`](../part_3_processes/14_larger_testing.md)
- [`0006_extended_200_iter_phase.md`](0006_extended_200_iter_phase.md)
- Skill `per-backbone-experiment-mandate`.
- `framework/sota_catalog.yaml` — per-backbone SOTA recipes.
