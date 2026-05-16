# demand-forecasting-kernels-only · DSBench autoresearch

**Kind:** modeling · **Problem:** regression · **Task type:** time_series

DSBench source: https://www.kaggle.com/competitions/demand-forecasting-kernels-only

## Quick start

```powershell
# Run a single hill-climb backbone (25 iters)
& "C:/Users/evija/anaconda3/python.exe" -m framework.hill_climb --repo "C:\Users\evija\dsbench\modeling\demand-forecasting-kernels-only" --backbone xgboost

# Run the full multi-backbone loop
& "C:/Users/evija/anaconda3/python.exe" -m framework.hill_climb --repo "C:\Users\evija\dsbench\modeling\demand-forecasting-kernels-only"

# Audit this repo against autoresearch SECTION_MAPPING
& "C:/Users/evija/anaconda3/python.exe" -m framework.validator --repo "C:\Users\evija\dsbench\modeling\demand-forecasting-kernels-only"
```

## DSBench comparison target

The DSBench paper reports the best agent achieving 34.12% on data-analysis tasks and 34.74% Relative Performance Gap on data-modeling. The final score for this task is written to `autoresearch_results/final_report.json` after one test-set pass.

## Architecture

Generated from `framework/CLAUDE_template.md` (parameterised clone of `autoresearch/CLAUDE.md`). See `CLAUDE.md` for the full 36-section protocol applied to this task.
