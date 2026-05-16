---
name: per-backbone-code-snapshot
description: Per-backbone code snapshot mandate — snapshot model/backbone.py + train.py to code_versions/<backbone>_start/ before any backbone's first experiment, and never modify backbone X's code while backbone Y experiments are running. Triggers on "code_versions", "backbone snapshot", "backbone isolation", "snapshot before experiments".
metadata:
  category: protocol
  source: autoresearch
  related: [per-backbone-experiment-mandate, winner-archive-protocol]
---

# Per-Backbone Code Snapshots & Isolation

## When to use

- Before starting experiments on a new backbone (LSTM after MLP, PatchTST after LSTM, etc.).
- Investigating cross-backbone contamination (Did our LSTM tweak break MLP?).
- Reviewing diffs between backbone exploration cycles.

## The rule

> ### Per-Backbone Code Snapshots (MANDATORY)
>
> Before starting experiments on a new backbone, snapshot the CURRENT `model/backbone.py` and `model/train.py` to `code_versions/<backbone>_start/` so you can diff what changed during that backbone's exploration. This prevents mixing MLP-specific changes into LSTM exploration, etc.
>
> ```
> code_versions/
>   v1_original/                 # pre-any-change snapshot
>   v2_residual_mlp/             # after residual skip connection (MLP champion)
>   v3_residual_128h/            # MLP mid-session snapshot
>   lstm_start/                  # snapshot before LSTM experiments begin
>   patchtst_start/              # snapshot before PatchTST experiments begin
>   ...
> ```
>
> Rule: never modify `backbone.py` code specific to backbone X while experiments on backbone Y are in progress. Finish one backbone's 50 experiments, snapshot, then move on.

### Backbone Isolation Rule (append-only)

> Before starting experiments on a new backbone, snapshot `model/backbone.py`, `model/train.py`, `run_autoresearch.py` to `code_versions/<backbone>_start/`. Do NOT modify backbone code specific to backbone X while experiments on backbone Y are in progress. Complete one backbone's 50-experiment cycle, snapshot as `<backbone>_final/`, then move to next backbone.

## Anti-patterns

- **Editing LSTM-specific code paths while running PatchTST experiments.** Future LSTM re-experiments will compare against a different code state — your "+0.94 LSTM gain" might disappear.
- **Skipping the `_start/` snapshot.** Without it you can't diff what the backbone exploration changed.
- **Snapshotting only `backbone.py`.** `train.py` and `run_autoresearch.py` matter too — backbone-specific epoch counts, schedulers, and optimizers live in `train.py`.
- **Editing a shared helper function** during a backbone's run without re-running the prior champion. Either avoid the edit, or re-run all backbones touched by the helper.
- **No `_final/` snapshot** when the backbone's 50-experiment cycle ends — you lose the diff for the next backbone's "start" snapshot.

## Implementation checklist

1. Before experiment 1 of backbone X: `cp model/backbone.py model/train.py run_autoresearch.py code_versions/<X>_start/`.
2. During backbone X exploration: only touch X-specific code paths (or shared code with a re-validation plan).
3. After backbone X's last experiment: `cp ... code_versions/<X>_final/`.
4. Diff `<X>_final/` vs `<X>_start/` and paste the diff into the winner archive if X produced the global champion.
5. The same rule applies to data and feature code — snapshot if changes are backbone-specific.

## References

- Source: `autoresearch/CLAUDE.md` section "Per-Backbone Code Snapshots (MANDATORY)"
- Source: `autoresearch/CLAUDE.md` section "Backbone Isolation Rule"
- Related: `per-backbone-experiment-mandate`, `winner-archive-protocol`, `per-backbone-sota-recipes`.
