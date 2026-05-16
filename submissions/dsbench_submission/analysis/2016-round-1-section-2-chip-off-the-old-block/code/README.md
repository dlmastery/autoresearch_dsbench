# 2016-round-1-section-2-chip-off-the-old-block · DSBench autoresearch

**Kind:** analysis · **Problem:** qa_excel · **Task type:** financial_modeling_excel

DSBench source: https://www.eloquens.com/tool/vYDF7b/finance/modeloff-sample-past-questions/2016-round-1-section-2-chip-off-the-old-block

## Quick start

```powershell
# Run a single hill-climb backbone (25 iters)
& "C:/Users/evija/anaconda3/python.exe" -m framework.hill_climb --repo "C:\Users\evija\dsbench\analysis\2016-round-1-section-2-chip-off-the-old-block" --backbone xgboost

# Run the full multi-backbone loop
& "C:/Users/evija/anaconda3/python.exe" -m framework.hill_climb --repo "C:\Users\evija\dsbench\analysis\2016-round-1-section-2-chip-off-the-old-block"

# Audit this repo against autoresearch SECTION_MAPPING
& "C:/Users/evija/anaconda3/python.exe" -m framework.validator --repo "C:\Users\evija\dsbench\analysis\2016-round-1-section-2-chip-off-the-old-block"
```

## DSBench comparison target

The DSBench paper reports the best agent achieving 34.12% on data-analysis tasks and 34.74% Relative Performance Gap on data-modeling. The final score for this task is written to `autoresearch_results/final_report.json` after one test-set pass.

## Architecture

Generated from `framework/CLAUDE_template.md` (parameterised clone of `autoresearch/CLAUDE.md`). See `CLAUDE.md` for the full 36-section protocol applied to this task.
