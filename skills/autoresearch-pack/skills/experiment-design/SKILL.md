---
name: experiment-design
description: Experiment design rules — composite keep/revert metric, epoch-bound training, cooldown, ONE change per experiment, per-fold breakdown, wired-or-removed params, justified hyperparameter choices. Triggers on "experiment design", "composite metric", "keep/discard", "one config change", "epoch-bound".
metadata:
  category: protocol
  source: autoresearch
  related: [karpathy-agent-protocol, seven-step-research-process, monotonic-quality-progression]
---

# Experiment Design

## When to use

- Defining the keep/revert decision rule for a new project.
- Designing the next experiment after a result lands.
- Reviewing a PR that adds a config parameter or changes the runner.

## The rule

> ### Experiment Design
> - **Composite metric for keep/revert:** `min(test_sharpe, val_sharpe) - 0.1 * n_negative_folds`. The model must do well on BOTH val and test across ALL fold windows. Fold 7 is the most important regime but the model must NOT have large drawdowns in other regimes.
> - Training is EPOCH-BOUND (minimum 20 epochs with early stopping). NOT time-bound.
> - **60-second cooldown after each experiment** to let the GPU/CPU cool. Use `sleep 60` between runs.
> - ONE config change per experiment. Diagnose WHY before choosing what to change next.
> - Report per-fold-window breakdown for BOTH val and test alongside aggregates.
> - Dashboard shows train/val/test tabs for per-window breakdown. Test is the default view.
> - Every config parameter must be wired end-to-end. Dead params are bugs — remove them.
> - Every hyperparameter choice must be justified by published papers, model developer guidelines, or prior empirical results from this project. Never choose arbitrary values.

### Practical addendum (from Common Mistakes table)

- `--learning-rate` flag does not exist — use `--lr` in every runner command.
- `huber_delta` > 1.0 is a no-op at this residual scale — treat Huber as MSE.
- Fine-grained AdamW `wd` < 30% change is a no-op; use log-spaced sweeps (1e-4, 5e-4, 1e-3, 5e-3).
- Smaller batch without seed plan: `bs=16` improves mean-case but **doubles** seed std vs `bs=32`.

## Anti-patterns

- **Changing two configs in one experiment.** You will not know which one mattered.
- **Time-bound training** ("run for 10 minutes"). Different backbones converge at different speeds; use epoch budget + patience.
- **Composite that's a simple mean of fold Sharpes.** Hides large negative folds. Use the `min(...) - 0.1*n_neg` rule (or a project-specific equivalent that penalises regime-specific failure).
- **A config param that's parsed but not wired into the model.** It silently no-ops; future "experiments" on that param will look like seed noise.
- **Skipping per-fold breakdown** and reporting only aggregate — the model that's great-on-average and catastrophic on fold-2 is undeployable.

## Implementation checklist

1. Implement the composite metric exactly as defined; unit-test on toy inputs.
2. Every CLI flag in the runner maps to a code path that observably changes behaviour — add a "wiring" smoke-test.
3. Per-experiment JSONL entry includes: config, composite, per-fold val Sharpe (array), per-fold test Sharpe (array), n_negative_folds.
4. ONE config delta per experiment — encode as the runner argument list diff vs the previous champion.
5. Justify the chosen value with a paper, developer-guideline, or prior result. If none, do not run.

## References

- Source: `autoresearch/CLAUDE.md` section "Hard Rules → Experiment Design"
- Source: `autoresearch/CLAUDE.md` section "Common Mistakes (Never Repeat)"
- Bailey & López de Prado (2014) "The Deflated Sharpe Ratio" — motivates the regime-aware composite.
- Related: `karpathy-agent-protocol`, `seven-step-research-process`, `monotonic-quality-progression`.
