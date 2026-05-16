---
name: mlops-documentation
description: MLOps documentation standards — master experiment log, trade logs, readable-by-someone-who-wasnt-there, no orphan artifacts, consistent formatting, append-only history. Triggers on "MLOps", "experiment summary", "experiment_summary.md", "research journal", "documentation standards".
metadata:
  category: documentation
  source: autoresearch
  related: [dashboard-files-update-mandate, citation-rigor, reasoning-blob-completeness]
---

# MLOps Documentation Standards

## When to use

- Authoring or reviewing `autoresearch_results/experiment_summary.md`.
- Designing the per-experiment markdown template for a new project.
- After every experiment — fill in the row for this experiment.

## The rule

> ### MLOps Documentation Standards (MANDATORY)
> You are a strong MLOps engineer. Every artifact and every experiment must be documented in proper, readable markdown. No exceptions.
>
> **`autoresearch_results/experiment_summary.md`** — the master experiment log. Updated after EVERY experiment. Format:
>
> ```markdown
> ## Experiment Log — [Backbone] Phase
>
> ### Exp[N]: [description]
> - **Config delta from champion:** [what changed]
> - **Rationale:** [diagnosis + literature citation + hypothesis]
> - **Prediction:** [expected composite change]
> - **Result:** Composite [X] | Test Sharpe [Y] | Val Sharpe [Z] | [N]/7 positive folds
> - **Per-fold test Sharpe:** F1=[X] F2=[X] F3=[X] F4=[X] F5=[X] F6=[X] F7=[X]
> - **Classification:** Precision=[X] Recall=[X] F1=[X] F2=[X] MCC=[X]
> - **Status:** KEEP / DISCARD
> - **Learning:** [what was learned, why result matched/differed from prediction]
> - **Win/Loss:** [summary — see per-trade spreadsheet in trade_logs/]
> ```
>
> **`autoresearch_results/trade_logs/`** — per-experiment trade-level detail (see Trade-Level Win/Loss Logging below).
>
> **Key documentation principles:**
> 1. **Readable by a human who wasn't there.** Someone reading the experiment summary 6 months from now must understand WHY each experiment was run and WHAT was learned.
> 2. **No orphan artifacts.** Every file must be referenced from either the checkpoint, experiment summary, or winner README.
> 3. **Consistent formatting.** Same table format, same metric names, same precision (4 decimal places for ratios, 2 for percentages).
> 4. **Append-only experiment log.** Never delete or rewrite experiment entries. If an experiment was wrong (e.g., bug found), add a note — don't erase history.

### Canonical status-snapshot script (`framework/_status.py`)

Every project MUST ship a one-command "how is the run going?" tool. The DSBench canonical artefact is `framework/_status.py`, invoked as:

```powershell
& "C:/Users/evija/anaconda3/python.exe" framework/_status.py
```

Output:

```
BEAT-DSBENCH:   modeling=63/74  analysis=29/38  total=92/112
FORENSIC PASS:  modeling=70/74  analysis=37/38  total=107/112
FORENSIC FAIL:  modeling=4/74
=== modeling FORENSIC FAILS ===
  modeloff_2014_q23_dcf                                 ['agent_I: refit drift 0.012']
  ...
```

The script is the canonical artefact: a fresh Claude Code session can read project health in one command without parsing four JSON files manually. Ship the equivalent in every new project.

### Status-counting asymmetry — KIND vs PROBLEM_TYPE

The two rollup files in `registry/` disagree on the modeling-vs-analysis distinction key. Code that touches both files MUST account for this:

| File | Carries `kind`? | Modeling distinction |
|---|---|---|
| `final_rollup.json` | NO | `r.get('problem_type') != 'qa_excel'` → modeling |
| `forensic_summary.json` | YES | `f.get('kind') == 'modeling'` |

The canonical pattern in `framework/_status.py`:

```python
def is_mod(r):                                  # rollup rows
    return r.get('problem_type') != 'qa_excel'

mod_beat = sum(1 for r in rollup if is_mod(r) and r.get('beats_dsbench'))
mod_pass = sum(1 for f in forensic if f.get('kind') == 'modeling' and f.get('verdict') == 'PASS')
```

Mixing the two keys silently miscounts task health. Add a comment in any new file that touches both rollups, and document the asymmetry in the project's README.

### Research journal twin (markdown form)

> `research_journal.md` mirror — same six fields per experiment:
>
> ```markdown
> ## Exp<N> — <short title>
> **Diagnosis:** ...
> **Citations:** ...
> **Hypothesis:** ...
> **Prediction:** ...
> **Verdict:** ...
> **Learning:** ...
> ```
>
> The journal is the human-readable twin of the JSON; they must stay in sync. If they drift, the JSON is authoritative (runner-written), and the journal gets updated from it.

## Anti-patterns

- **One-line entries** ("Exp24: failed"). Useless to anyone who wasn't there.
- **Editing past entries.** Append-only — if a result was wrong, add a `**Correction:**` line, do not silently overwrite.
- **Orphaned trade-log CSV** with no row in `experiment_summary.md` referring to it. The reader cannot find it.
- **Inconsistent precision.** Mixing `0.27` and `0.2716` in the same column makes scanning fail.
- **Skipping the `Learning:` field** because the result was a DISCARD. Negative results are the most informative entries.

## Implementation checklist

1. After every experiment, write the templated `### Exp[N]` block to `experiment_summary.md`.
2. Author the mirror `## Exp<N> — <title>` block in `research_journal.md`.
3. Cross-link both to `trade_logs/exp<N>_trades.csv`.
4. Use 4-decimal precision for Sharpe/composite/IC; 2-decimal % for hit-rate.
5. Never overwrite a past entry — append a `Correction:` note if needed.

## References

- Source: `autoresearch/CLAUDE.md` section "MLOps Documentation Standards (MANDATORY)"
- Source: `autoresearch/CLAUDE.md` Experiment Log / Exp[N] templates.
- Related: `dashboard-files-update-mandate`, `citation-rigor`, `reasoning-blob-completeness`, `dashboard-reasoning-annotations`.
