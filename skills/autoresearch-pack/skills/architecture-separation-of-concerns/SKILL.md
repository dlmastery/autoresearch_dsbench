---
name: architecture-separation-of-concerns
description: Architecture and separation of concerns — autoresearch loop = Claude agent, runner LOGS ONLY, dashboard READS ONLY, relative imports, project structure, key constants. Triggers on "separation of concerns", "runner", "dashboard decoupled", "relative imports", "key constants", "project structure".
metadata:
  category: engineering
  source: autoresearch
  related: [mlfin-researcher-mindset, validation-checklist, dashboard-files-update-mandate]
---

# Architecture & Separation of Concerns

## When to use

- Designing the package layout for a new autoresearch project.
- Reviewing a PR that bundles runner + dashboard or runner + evaluator.
- Auditing for "monolithic script" smells.

## The rule

> ### Architecture
> - **Autoresearch loop = Claude agent.** Claude reads results, decides what to try, calls the runner, reads output. The intelligence is in the agent, NOT in Python code. No pre-baked experiment lists.
> - Runner (`run_autoresearch.py`) executes ONE experiment per call. Logs JSONL. That's it.
> - Dashboard (`dashboard.html`) reads logs. DECOUPLED from runner.
> - Save checkpoint after every experiment (JSONL append + best_config.json overwrite).
> - Use relative imports (`from .model.backbone import ...`).

### Project Structure (autoresearch reference)

```
autoresearch/                    # package root
  baseline.py                    # single-backbone walk-forward evaluation
  run_ablation.py                # multi-backbone comparison
  run_autoresearch.py            # Karpathy-style autonomous experiment loop (LOGS ONLY)
  data/
    download.py                  # FX + macro data (cached to .data_cache/)
    features.py                  # 104 backward-looking features
    splits.py                    # folds, purge/embargo, hole-punching, split_superfold()
  model/
    backbone.py                  # 8 backbones, per-backbone seq_len via get_seq_len()
    train.py                     # training loop, create_contiguous_datasets()
  evaluation/
    metrics.py                   # Sharpe, PSR, DSR, IC, trading_report + precision/recall/F1/F2/MCC
  autoresearch_results/
    experiment_log.jsonl          # structured experiment log (append-only)
    best_config.json             # current best configuration
    dashboard.html               # live HTML dashboard (reads logs, decoupled)
    experiment_summary.md        # master human-readable experiment log (updated every experiment)
    trade_logs/                  # per-trade win/loss CSVs for every experiment
      exp<N>_trades.csv          # one row per trade on test data
      exp<N>_trade_summary.json  # per-fold trade statistics
    winners/                     # archived champions (one subdir per winner, fully self-contained)
      <backbone>_exp<N>_<desc>/  # e.g. mlp_exp32_residual_seed0/
        README.md                # full description, metrics, reproduction status
        config.json              # exact config
        model_checkpoint.pt      # saved weights
        code/                    # frozen source snapshot
        inference/               # predict.py + inference README
        reproduction/            # reproduction logs + seed variance
```

### Key Constants (autoresearch reference)

| Constant | Value | Location |
|----------|-------|----------|
| SEQ_LEN (LFM2) | 60 | backbone.py `BACKBONE_SEQ_LEN` |
| SEQ_LEN (others) | 10 | backbone.py `_DEFAULT_SEQ_LEN` |
| PURGE_DAYS | 90 | splits.py |
| EMBARGO_DAYS | 21 | splits.py |
| LABEL_HORIZON_BUFFER | 10 | splits.py |
| LEARNING_RATE | 3e-4 | train.py |
| BATCH_SIZE | 32 | train.py |
| EPOCHS | 20 | train.py |
| PATIENCE | 5 | train.py |
| WEIGHT_DECAY | 1e-5 | train.py |

## Anti-patterns

- **Runner writes to the dashboard's data files via DOM templating.** Runner emits JSONL only; dashboard reads JSONL only.
- **Pre-baked experiment list** (`experiments_to_run.py`). Intelligence belongs in the agent, not in code.
- **Absolute imports** in the package (`from autoresearch.model import ...`). When run as `python -m autoresearch`, you'll get `ModuleNotFoundError`. Always `from .model.backbone import ...`.
- **Magic constants scattered through the codebase.** Lift them into `train.py` / `splits.py` constants block — one source of truth.
- **Runner that also does evaluation analytics.** Runners log. Evaluators evaluate. Dashboards display. Never tangle.

## Implementation checklist

1. `run_autoresearch.py` does NOT import the dashboard; the dashboard does NOT import the runner.
2. Runner returns metrics + appends JSONL — no analytic side-effects (no plots, no summaries).
3. Dashboard `dashboard.html` is static HTML/JS that fetches JSONL — no server-side rendering.
4. All imports inside the package are relative.
5. Constants block at the top of `train.py` / `splits.py` matches the Key Constants table.
6. Per-backbone seq_len comes from `backbone.py:get_seq_len()` — not hard-coded in the dataset.

## References

- Source: `autoresearch/CLAUDE.md` section "Architecture"
- Source: `autoresearch/CLAUDE.md` section "Project Structure"
- Source: `autoresearch/CLAUDE.md` section "Key Constants"
- Related: `mlfin-researcher-mindset`, `validation-checklist`, `dashboard-files-update-mandate`.
