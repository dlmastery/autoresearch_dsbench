---
name: per-backbone-sota-recipes
description: Per-backbone SOTA training recipes — every backbone re-derives epochs/patience/LR/warmup/scheduler/batch/WD/opt/loss from its own 2024-2026 paper. Includes the full Tier 1/2/3 recipe table and the epoch-budget scaling heuristics. Triggers on "SOTA recipe", "training recipe", "per-backbone hyperparameters", "epoch budget", "PatchTST seq_len", "GBM hyperparameters".
metadata:
  category: engineering
  source: autoresearch
  related: [per-backbone-experiment-mandate, gpu-memory-constraint, experiment-design]
---

# Per-Backbone SOTA Training Recipes

## When to use

- Before Experiment 1 of any new backbone — you MUST re-derive the recipe.
- When a paper-derived default doesn't match your data scale — apply the scaling heuristics.
- When a backbone underperforms — first check the recipe is paper-accurate.

## The rule

> ### Per-Backbone SOTA Training Recipes (MANDATORY — re-derive per backbone)
>
> **Every backbone picks its OWN epochs, patience, learning rate, batch size, scheduler, and optimizer from the latest SOTA literature for THAT architecture. Never copy another backbone's config.** Defaults in `train.py` (ep=20, pat=5, lr=3e-4, bs=32, wd=1e-5) are starting points for MLP only — inherited values are bugs.
>
> **Before the first experiment on any new backbone, Claude MUST:**
>
> 1. **Pull the latest 2024-2026 arXiv / NeurIPS / ICML / ICLR paper for the backbone family.** For each backbone, read the paper's experimental section and note:
>    - Recommended epochs (and how they terminate — fixed vs early-stop)
>    - Patience threshold (absolute vs relative to epochs — e.g. "10% of total")
>    - Learning rate (and whether warmup is required — many 2024+ transformers need 5-10% warmup)
>    - Scheduler (cosine annealing, linear decay, plateau, ReduceLROnPlateau — varies widely)
>    - Optimizer (Adam vs AdamW vs Lion vs Adafactor vs SOAP — Lion/SOAP in 2024+ for large models)
>    - Batch size (and whether it's effective-batch via grad accumulation)
>    - Weight decay (AdamW uses decoupled; varies from 0 to 0.1 by architecture)
>    - Gradient clipping (transformers usually clip to 1.0; RNNs to 0.25-1.0; GBMs N/A)
>    - Loss function (MSE vs Huber vs Quantile vs Log-Cosh)
>
> 2. **Record the chosen recipe with a paper citation in the reasoning annotation** for Experiment 1 of that backbone. Other experiments in the backbone's 50-run cycle start from this config, not from MLP's or LSTM's.
>
> 3. **Justify the DELTA from the paper.** If our chosen epochs deviate from the paper's recommendation, the reasoning entry MUST explain why (e.g. "Nie 2023 used ep=100 on ETTh1 n=8640; we scale to ep=80 for our n=2738 — 3.15× less data, scale training proportionally per Smith 2017 rule").
>
> 4. **Never assume "ep=50 works for everything."** Historical proof:
>    - MLP Exp32 champion converged at ep=50, pat=10 (Gu/Kelly/Xiu 2020)
>    - LSTM Exp3 (ep=100, pat=15) beat LSTM Exp1 (ep=50, pat=10) by **+0.94 composite** (Fischer & Krauss 2018) — wrong epoch count costs 20% of peak performance
>    - PatchTST Exp1 at our MLP defaults (seq=10, ep=20) gave composite **−1.72** because Nie 2023's minimum seq=60 and ep=100 were ignored
>    - LFM2 head-only fine-tuning needs ep=20, pat=5 — LSTM's ep=100 would catastrophically overfit the adapter head

### Backbone-Specific Training Recipes (Tier 1 — neural backbones)

| Backbone | Epochs | Patience | LR | Warmup | Scheduler | Batch | WD | Opt. | Loss | Paper (full citation) |
|----------|--------|----------|-----|--------|-----------|-------|-----|------|------|-----------------------|
| mlp | 50 | 10 | 3e-4 | 0 | cosine | 32 | 1e-5 | AdamW | Huber δ=1 | Gu, Kelly & Xiu 2020 RFS "Empirical Asset Pricing via Machine Learning" |
| lstm | 100 | 15 | 1e-3 | 0 | cosine | 16-32 | 7e-4 | AdamW | Huber δ=1 | Fischer & Krauss 2018 EJOR "Deep learning with LSTMs for financial market predictions" |
| patchtst | 100 | 20 | 1e-4 | 10 | cosine | 32 | 1e-4 | AdamW | MSE | Nie, Nguyen, Sinthong, Kalagnanam 2023 ICLR "A Time Series is Worth 64 Words" (arXiv:2211.14730) — requires seq_len ≥ 60 |
| patchtsmixer | 100 | 15 | 1e-3 | 5 | cosine | 32 | 1e-5 | AdamW | MSE | Ekambaram et al. 2023 KDD "TSMixer" (arXiv:2306.09364) |
| itransformer | 150 | 20 | 5e-5 | 10 | cosine | 32 | 0 | AdamW | MSE | Liu et al. 2024 ICLR "iTransformer" (arXiv:2310.06625) |
| xlstm | 80 | 15 | 5e-4 | 5 | cosine | 16 | 1e-3 | AdamW | Huber δ=1 | Beck et al. 2024 NeurIPS "xLSTM" (arXiv:2405.04517) |
| mamba | 100 | 20 | 5e-4 | 10 | cosine | 32 | 0.1 | AdamW | MSE | Gu & Dao 2024 COLM "Mamba" (arXiv:2312.00752) |

### Tier 2 — 10 new 2024-2026 SOTA foundation models

| # | Backbone | Family | Epochs | Patience | LR | Warmup | Scheduler | Batch | WD | Opt. | Loss | Paper |
|---|----------|--------|--------|----------|-----|--------|-----------|-------|-----|------|------|-------|
| 1 | timesfm | Foundation (decoder-only) | 20 | 5 | 1e-4 | 2 | cosine | 32 | 1e-5 | AdamW | Quantile | Das et al. 2024 ICML (arXiv:2310.10688); TimesFM 2.5 (2025) |
| 2 | chronos-bolt | Foundation (T5 enc-dec) | 15 | 5 | 5e-5 | 2 | cosine | 32 | 1e-5 | AdamW | CrossEnt | Ansari et al. 2024 TMLR (arXiv:2403.07815); Chronos-2 (arXiv:2510.15821) |
| 3 | moirai | Foundation (probabilistic + MoE) | 20 | 5 | 1e-4 | 2 | cosine | 32 | 0 | AdamW | NLL student-T | Woo et al. 2024 ICML (arXiv:2402.02592); Moirai-MoE (arXiv:2410.10469); Moirai 2.0 (arXiv:2511.11698) |
| 4 | moment | Foundation (T5 enc, masked) | 30 | 10 | 5e-5 | 3 | cosine | 32 | 1e-5 | AdamW | MSE | Goswami et al. 2024 ICML (arXiv:2402.03885) |
| 5 | tirex | Foundation (xLSTM decoder) | 25 | 8 | 1e-4 | 3 | cosine | 16 | 1e-4 | AdamW | Quantile | Auer et al. 2025 NXAI/JKU |
| 6 | sundial | Foundation (TimeFlow loss) | 30 | 10 | 1e-4 | 3 | cosine | 32 | 1e-5 | AdamW | TimeFlow | Liu et al. 2025 (arXiv:2502.00816) |
| 7 | time-moe | Foundation (sparse MoE) | 20 | 5 | 1e-4 | 2 | cosine | 32 | 1e-5 | AdamW | MSE+LB | Shi et al. 2024 ICLR'25 (arXiv:2409.16040) |
| 8 | timemixer | MLP-multiscale | 100 | 15 | 1e-3 | 5 | cosine | 32 | 1e-5 | AdamW | MSE | Wang et al. 2024 ICLR (arXiv:2405.14616) |
| 9 | timesnet | 2D-variation (CNN-inception) | 100 | 20 | 1e-4 | 5 | cosine | 32 | 1e-4 | AdamW | MSE | Wu et al. 2023 ICLR (arXiv:2210.02186) |
| 10 | mambats | SSM (Mamba-based) | 100 | 20 | 1e-3 | 5 | cosine | 32 | 1e-4 | AdamW | MSE | Cai et al. 2024 NeurIPS (arXiv:2405.16440); DMamba (arXiv:2602.09081) |

**Bonus Tier 2.5:** DLinear/NLinear (Zeng 2023), N-HiTS (Challu 2023), TFT (Lim 2021), Crossformer (Zhang 2023), Autoformer (Wu 2021), N-BEATS (Oreshkin 2020), EMTSF (arXiv:2510.23396 2025).

### Tier 3 — GBM trio (50-experiment budget split 20/15/15)

| Backbone | Key HP starting points | Special feature | Paper |
|----------|------------------------|------------------|-------|
| xgboost | n_estimators=1500, max_depth=6, lr=0.03, subsample=0.8, colsample_bytree=0.8, early_stop=50, reg_lambda=1.0, min_child_weight=1, gamma=0 | 2nd-order Newton boosting, monotonic constraints, histogram method | Chen & Guestrin 2016 KDD (arXiv:1603.02754) |
| lightgbm | n_estimators=2000, num_leaves=63, lr=0.03, feature_fraction=0.8, bagging_fraction=0.8, early_stop=50, min_data_in_leaf=20 | Leaf-wise growth, GOSS sampling, EFB, native categorical | Ke et al. 2017 NeurIPS |
| catboost | iterations=2000, depth=6, lr=0.03, random_strength=1.0, early_stop=100, l2_leaf_reg=3, bagging_temperature=1.0 | Symmetric oblivious trees, ordered boosting, native categorical via ordered target-stat | Prokhorenkova et al. 2018 NeurIPS (arXiv:1706.09516) |

**Why GBMs are 3 separate backbones (not one bundled "GBM backbone"):**

- **XGBoost** uses 2nd-order gradient info (Hessian) — effective on imbalanced targets, fast on GPU.
- **LightGBM** uses leaf-wise growth + GOSS — fastest wall-clock, handles large n well.
- **CatBoost** uses ordered boosting to fight prediction shift — slowest but often best out-of-box accuracy on tabular.

Each has different failure modes (LightGBM: leaf-wise overfit on small data; CatBoost: depth ceiling at 6 symmetric trees). Do not skip any.

### Epoch-budget rule of thumb (when in doubt)

If the paper's recipe is unclear, use this scaling heuristic:

- **Data scaling (Smith 2017):** `epochs ≈ paper_epochs × (paper_n / our_n)^0.5`. Our n=2738; if paper used n=8000, scale paper_epochs × 0.59.
- **Parameter scaling (Kaplan 2020):** holding data fixed, larger models need more epochs. `epochs ≈ base × (our_params / paper_params)^0.2`.
- **Patience as 15% of epochs** is a safe default when papers don't specify.
- **Warmup = 5-10% of total epochs** for transformer families (required by layer-norm stability).

These are starting heuristics; always iterate and checkpoint the actual convergence profile per backbone.

### Empirical evidence (LSTM phase confirmations)

- LSTM Exp3 (ep=100 pat=15) beat Exp1 (ep=50 pat=10) by +0.94 composite — confirmed Fischer & Krauss 2018.
- PatchTST at seq=10 gave -1.72 — confirmed Nie 2023's seq≥60 minimum.
- MLP converged at ep=50 — Gu/Kelly/Xiu 2020 recipe validated.
- Per-backbone convergence epochs (observed early-stop point): MLP ~25, LSTM ~29, PatchTST pending ~40-60 est.

### Re-derive per variant

When a backbone family has multiple SOTA variants (e.g. LSTM family → xLSTM/sLSTM/mLSTM/Mamba; Transformer TS → PatchTST/iTransformer/Crossformer/Autoformer/FEDformer; Mamba family → MambaTS/DMamba/S-Mamba/CMMamba), each variant re-derives its recipe from its OWN paper. Don't assume xLSTM uses vanilla LSTM's ep=100, pat=15, or that MambaTS uses vanilla Mamba's ep=100.

## Anti-patterns

- **Copying MLP's `train.py` defaults into LSTM.** ep=20, lr=3e-4, wd=1e-5 underfits LSTM — needs ep=100, lr=1e-3, wd=7e-4 (Fischer & Krauss 2018).
- **PatchTST at seq_len=10.** Nie 2023 requires seq_len ≥ 60 — at 10, attention has too few patches to be useful (-1.72 composite confirmed).
- **Skipping warmup on transformers.** Layer-norm stability requires 5-10% warmup; without it, fold-2-style hard regimes diverge.
- **Same epoch count across all backbones.** MLP wants 50, LSTM 100, foundation-FT 20 — copying breaks at least one.
- **GBM bundled as "the gradient-boost backbone".** They are 3 distinct architectures with different splits/regularizers/categorical handling.

## Implementation checklist

1. For each backbone, paste the paper-derived recipe into Experiment 1's reasoning annotation (with citation).
2. Justify any delta from the paper using the data/parameter scaling heuristics.
3. Log effective patience as ~15% of epochs.
4. Use the table above as the canonical starting point — iterate via the 7-step process.
5. Add a "convergence-profile" entry to the checkpoint after Exp 1 of each backbone: when did early-stop fire?

## References

- Source: `autoresearch/CLAUDE.md` sections "Per-Backbone SOTA Training Recipes (MANDATORY — re-derive per backbone)", "Backbone-Specific Training Recipes (updated 2026-04-19 from SOTA literature)", "Epoch-budget rule of thumb", "Empirical evidence (LSTM phase confirmations)", "Session Learnings (LSTM Phase)".
- All papers cited inline above (full author lists in source CLAUDE.md).
- Related: `per-backbone-experiment-mandate`, `gpu-memory-constraint`, `experiment-design`.
