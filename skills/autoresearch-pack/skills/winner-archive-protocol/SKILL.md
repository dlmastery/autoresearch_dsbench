---
name: winner-archive-protocol
description: Winner archiving protocol — full portable archive for every new global champion (README, config, weights, code snapshot, inference script, reproduction). Includes Winner Definition clarification (global, not per-backbone) and the trading-strategy README section. Triggers on "winner archive", "champion", "best_config.json", "winners/", "model_checkpoint.pt", "reproduction".
metadata:
  category: documentation
  source: autoresearch
  related: [explainability-audit-14-section, google-colab-notebook, per-backbone-code-snapshot]
---

# Winner Archiving Protocol

## When to use

- A new experiment has `status=KEEP` and `composite > previous global best`.
- Preparing a model for hand-off or deployment.
- Auditing whether past champions are reproducible.

## The rule

> ### Winner Definition (CLARIFICATION)
>
> **"Winner" means the GLOBAL champion across ALL backbones and ALL experiments.** Not per-backbone. The one single best model (by composite score) at any point in time.
>
> Per-backbone best is tracked separately in the checkpoint but does NOT get archived to `winners/` unless it is also the global best.
>
> When a new experiment beats the global composite:
> 1. Save artifacts to `autoresearch_results/winners/<backbone>_exp<N>_<desc>/`
> 2. Include: README.md, config.json, model_checkpoint.pt, code/ (frozen snapshot), inference/, reproduction/, audit_report.md (14 sections per audit rules)
> 3. Update `best_config.json` at repo root

> ### Winner Archiving Protocol (MANDATORY for every NEW BEST)
> Every time a new champion is found (status=KEEP and composite > previous best), archive ALL artifacts to a self-contained subdirectory. The archive must be fully portable — someone can copy the directory to another machine and reproduce + run inference without any external dependencies beyond the conda environment.
>
> **Directory structure:** `autoresearch_results/winners/<backbone>_exp<N>_<short_description>/`
>
> ```
> winners/
>   mlp_exp32_residual_seed0/
>     README.md                    # Full description (see template below)
>     config.json                  # Exact config that produced this winner
>     model_checkpoint.pt          # Saved model weights (copy of best_model.pt)
>     experiment_log_entry.json    # The JSONL entry for this experiment
>     per_fold_results.json        # Full per-fold val + test breakdown
>     code/                        # Frozen snapshot of ALL source code at time of win
>       backbone.py
>       train.py
>       features.py
>       splits.py
>       metrics.py
>       run_autoresearch.py
>     inference/
>       predict.py                 # Standalone inference script with sample usage
>       README_inference.md        # How to load model and run predictions
>     reproduction/
>       reproduce_log.txt          # Output from reproduction run
>       seed_variance.json         # Cross-seed results if available
> ```
>
> **README.md template for each winner:**
> - Model name + experiment number
> - Champion composite score, test Sharpe, val Sharpe
> - Per-fold test Sharpe table (all 7 folds)
> - Per-fold val Sharpe table
> - Full hyperparameter config
> - Architecture description (layers, activation, skip connections, etc.)
> - Key insight: WHY this config won (what change from previous champion)
> - Training details: epochs run, early stopping epoch, training time
> - Uncertainty metrics: aleatoric, epistemic, confidence per fold
> - Traditional ML metrics: precision, recall, F1, F2 (direction classification)
> - Reproduction status: seeds tested, variance observed
> - Sample inference code snippet
>
> **After archiving:** Rerun the winner to verify reproduction. The reproduction log goes into `reproduction/reproduce_log.txt`. If the reproduction fails (composite differs by >0.5), flag it and investigate before proceeding.
>
> **Model checkpoint (`model_checkpoint.pt`) MUST be portable and self-contained:**
> Include in the torch.save dict:
> - `model_state_dict` — all trainable weights
> - `config` — hyperparameters dict (matches the `--seed` run command)
> - `scaler_mean`, `scaler_scale` — StandardScaler parameters (np.ndarray[n_features])
> - `feature_columns` — list of feature names in order (for schema validation at inference)
> - `target_columns` — list of target names (e.g. `['ret_1d', 'ret_5d']`)
> - `n_features` — int, feature count
> - `composite`, `description`, `backbone`, `experiment_num` — provenance
>
> The checkpoint must be loadable and reusable WITHOUT the source repo. Someone can rebuild the model, apply the scaler, and make predictions from the checkpoint alone + the architecture definition.
>
> **The `predict.py` inference script must:**
> 1. Load the model checkpoint
> 2. Accept raw feature input (or date range to download)
> 3. Output: prediction (mean), confidence, aleatoric uncertainty, epistemic uncertainty
> 4. Include a `__main__` block with a working example
> 5. Print results in a clear table format
>
> **Trading Strategy section (MANDATORY in every winner README.md):**
> Must include the following for any user to deploy the model:
> 1. **Signal Generation** — inputs, outputs, MC Dropout usage
> 2. **Entry rules** — pseudocode with thresholds (magnitude + confidence)
> 3. **Position sizing** — Kelly fraction, per-trade cap
> 4. **Exit rules** — horizon matching, stop-loss policy
> 5. **Rebalancing cadence** — daily/intraday/weekly
> 6. **Per-regime performance table** — accuracy/MCC/Sharpe per fold
> 7. **Risk controls** — daily loss cap, drawdown pause, regime shift detection
> 8. **Expected performance** — Sharpe, return, drawdown estimates (pre/post cost)
> 9. **Caveats and warnings** — seed variance, pair specificity, feature dependencies, transaction costs
> 10. **Reference to inference code** — link to `inference/predict.py`

## Anti-patterns

- **Archiving without the frozen code snapshot.** Tomorrow's code change to `backbone.py` will silently break yesterday's `model_checkpoint.pt` deployment.
- **Skipping the `scaler_mean`/`scaler_scale` save.** Inference will silently use a different scaling and produce subtly wrong outputs.
- **Not running reproduction.** Without `reproduction/reproduce_log.txt`, you don't know if your champion is luck or signal.
- **Archiving a per-backbone best that isn't the global best.** The `winners/` directory is reserved for global champions; per-backbone bests live in the checkpoint.
- **A `predict.py` that imports from the project package.** The archive must be self-contained — inline all needed code.

## Champion refit rule (final_report.py)

The one-and-only test-set pass is `framework/final_report.py`. The refit regime DIFFERS by problem type:

- **`qa_excel`:** refit on **train + val** before scoring test. Reason: per-task train is only ~6-10 questions, so adding val (~2-3 more) is the difference between a usable estimator and a degenerate one. Val gating is already finished before `final_report.py` runs, so val cannot leak into the test decision.
- **All other (`problem_type != "qa_excel"`):** refit on **train only**, exactly as during hill climbing. Preserves the held-out-val invariant that the explainability and forensic audits depend on.

```python
if cfg.problem_type == "qa_excel":
    X_fit = np.concatenate([X_train, X_val])
    y_fit = np.concatenate([y_train, y_val])
else:
    X_fit, y_fit = X_train, y_train
```

The forensic-audit refit-consistency check (agent I) MUST use the same regime; otherwise the ±0.005 reproduction tolerance is meaningless.

## Implementation checklist

1. On `composite > prev_best`, runner triggers archive creation atomically.
2. `model_checkpoint.pt` includes all 8 keys listed above; unit-test it loads & predicts on a held-out row.
3. `code/` is a tar/copy of source files at HEAD — no symlinks.
4. `inference/predict.py` runs from the archive directory only (no `sys.path` hacks).
5. Reproduction rerun: same config, same seed, same data → composite within 0.5 of original.
6. `audit_report.md` produced per `explainability-audit-14-section` skill.
7. README's Trading Strategy section follows the 10-item template.

## References

- Source: `autoresearch/CLAUDE.md` section "Winner Definition (CLARIFICATION)"
- Source: `autoresearch/CLAUDE.md` section "Winner Archiving Protocol (MANDATORY for every NEW BEST)"
- Related: `explainability-audit-14-section`, `google-colab-notebook`, `per-backbone-code-snapshot`, `dashboard-files-update-mandate`.
