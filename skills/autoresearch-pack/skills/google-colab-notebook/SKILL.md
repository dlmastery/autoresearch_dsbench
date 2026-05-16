---
name: google-colab-notebook
description: Google Colab notebook mandate — self-contained notebook for every winner with setup/data/features/training/eval/inference/viz/export cells. Target <5 min on Colab free tier. Triggers on "Colab", "colab_train_and_infer.ipynb", "self-contained notebook", "T4 free tier".
metadata:
  category: documentation
  source: autoresearch
  related: [winner-archive-protocol, explainability-audit-14-section]
---

# Google Colab Notebook (every winner)

## When to use

- A new global champion has just been archived.
- Preparing a model for hand-off to a team without the source repo.
- Producing artifacts for a paper or blog post.

## The rule

> ### Google Colab Notebook (MANDATORY for every winner)
> For every archived winner, generate a self-contained Google Colab notebook at `autoresearch_results/winners/<backbone>_exp<N>_<desc>/colab_train_and_infer.ipynb` that anyone can open in Colab and run end-to-end.
>
> **The Colab notebook must contain:**
> 1. **Setup cell:** `!pip install` all dependencies, clone repo or upload weights
> 2. **Data download cell:** download FX + macro data using `download.py` logic (or bundled CSV)
> 3. **Feature engineering cell:** compute all 104 features with clear explanations
> 4. **Training cell:** full training loop reproducing the winner config exactly — including super-fold split, contiguous datasets, loss function, optimizer, early stopping. Print per-epoch loss + validation metrics.
> 5. **Evaluation cell:** evaluate on all 7 test fold windows, print per-fold Sharpe/IC/win-rate table, compute composite score
> 6. **Inference cell:** load trained model, accept a date range, produce predictions with confidence/aleatoric/epistemic bands. Show a sample prediction table.
> 7. **Visualization cell:** plot equity curves per fold, prediction vs actual scatter, uncertainty calibration, confusion matrix
> 8. **Export cell:** save model weights + config for deployment
>
> **Notebook principles:**
> - Every cell must have a markdown header explaining what it does and WHY
> - Include the champion config as a clearly visible dict at the top
> - Use `torch.manual_seed()` for reproducibility
> - Print all key metrics at the end in a summary table
> - Target runtime: <5 minutes on Colab free tier (T4 GPU or CPU)
> - The notebook must be SELF-CONTAINED — no imports from the autoresearch package (inline all necessary code)

## Anti-patterns

- **`from autoresearch.model import ...`** — the notebook must be self-contained; inline the needed code.
- **`!pip install -e ../`** style relative paths — Colab has no parent repo. Use a public install or bundle the wheel.
- **No markdown headers** between cells — reader can't follow the narrative.
- **Runtime > 5 min on free tier** — Colab free tier sessions disconnect; keep training short via reduced epochs for demonstration (the full config is preserved for offline reproduction).
- **Seed not set** — every run produces different numbers; reviewer can't verify.

## Implementation checklist

1. Notebook lives at `winners/<id>/colab_train_and_infer.ipynb`.
2. Cells in exact order: setup → data → features → train → eval → inference → viz → export.
3. Each cell preceded by a markdown header (what + why).
4. Champion config rendered as a literal dict at top.
5. `torch.manual_seed()`, `numpy.random.seed()`, `random.seed()` set.
6. Final summary table prints all key metrics.
7. Free-tier runtime < 5 minutes — reduce epochs for the in-notebook training, point to full config for offline reproduction.

## References

- Source: `autoresearch/CLAUDE.md` section "Google Colab Notebook (MANDATORY for every winner)"
- Related: `winner-archive-protocol`, `explainability-audit-14-section`.
