---
name: dashboard-reasoning-annotations
description: Dashboard reasoning annotations — mandatory 7-field JSON entry per experiment (diagnosis, citations, hypothesis, prediction, verdict, learning, _manual) authored before and after the run. Triggers on "reasoning_annotations.json", "_manual: true", "backfill_reasoning", "dashboard reasoning panel".
metadata:
  category: dashboard
  source: autoresearch
  related: [citation-rigor, reasoning-blob-completeness, dashboard-files-update-mandate, mlops-documentation]
---

# Dashboard Reasoning Annotations (every experiment)

## When to use

- BEFORE running any experiment — pre-author the 4 prediction fields.
- IMMEDIATELY AFTER the experiment completes — author verdict and learning.
- When auditing the dashboard for missing/placeholder annotation entries.

## The rule

> ### Dashboard Reasoning Annotations (MANDATORY — capture EVERYTHING, every experiment)
>
> **Every single experiment MUST have a complete reasoning record in `autoresearch_results/reasoning_annotations.json` keyed by `experiment_num`. No experiment ships without one. Orphan entries or "auto-backfilled" placeholders are a bug.**
>
> The entry is a JSON object with these REQUIRED fields (all non-empty strings):
>
> | Field | Content | Source |
> |-------|---------|--------|
> | `diagnosis` | Why THIS experiment now: which champion weakness it targets, which fold is weakest and why (regime, dates, uncertainty profile), what prior experiments ruled out the alternatives | Authored by Claude BEFORE running |
> | `citations` | Full author/year/venue string for every paper motivating the choice (e.g. "Keskar et al. 2017 ICLR — On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima; He et al. 2016 CVPR (ResNet)"). Multiple papers semicolon-separated. Parenthetical-only tags (e.g. `(Keskar2017)`) are INSUFFICIENT — expand to full reference | Authored before running |
> | `hypothesis` | Concrete mechanism: "parameter X = value Y will change metric Z via mechanism M (what the paper argues)". Not just "try X". | Authored before running |
> | `prediction` | Numeric target: "composite should move from +6.37 to +6.40-6.50; val fold 2 expected to improve from -0.17 to +0.0-0.3". Include ranges, not single numbers | Authored before running |
> | `verdict` | KEEP / DISCARD / NEAR-MISS + composite achieved + delta vs global best + which folds carried it | Written immediately after results |
> | `learning` | What this result updates in the mental model: did the prediction hold? Which axis is now exhausted? Which variant should be tried next? | Written immediately after results |
> | `_manual` | `true` if authored by Claude as part of the 7-step process (which is ALL non-trivial experiments); `false` only for purely mechanical variance-check runs that reuse a prior annotation template | Always set |
>
> **Dashboard `dashboard.html` renders all 7 fields in the detail panel when a row is clicked.** If any field is missing, empty, or placeholder ("(auto-backfilled)", "(no explicit citation)"), that's a regression — fix it before the next experiment.
>
> **Write cadence — two places on every run:**
> 1. **BEFORE the experiment command runs:** Claude adds the entry to `reasoning_annotations.json` with `diagnosis`, `citations`, `hypothesis`, `prediction`, `_manual: true`. The experiment is not launched until this entry exists. This enforces the "never guess, never grid-search" rule.
> 2. **AFTER the experiment completes:** Claude appends `verdict` and `learning` to the same entry by reading the runner's JSONL output. The runner's auto-written entry is only a fallback; Claude's post-analysis is authoritative.
>
> **Enforcement:** At the start of every experiment cycle, Claude MUST check:
> - Does `reasoning_annotations.json` already have a complete entry for the previous experiment? If no `verdict`/`learning`, write them before starting the next.
> - Is the next experiment's pre-entry already authored? If no, write it now.
> - Did the citation field survive any recent `backfill_reasoning.py` run? Check `_manual: true` is preserved.
>
> **Parallel write to `research_journal.md`.** The same diagnosis/citations/hypothesis/prediction/verdict/learning narrative belongs in the research journal in markdown form, keyed by experiment number. Journal format:
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
>
> **`backfill_reasoning.py` rules:**
> - Only runs on DEMAND — not automatically, not after every experiment
> - Never overwrites entries with `_manual: true`
> - Fills in only the fields that are empty AND whose experiment JSONL entry exists
> - Logs every overwrite it makes
> - Is NOT a substitute for authoring the annotation before the run
>
> **Runner's responsibility (`run_autoresearch.py`):**
> - On every invocation, merge the user-visible description's citation tags + the CLI flag delta into the runtime `reasoning_annotations.json` entry — WITHOUT clobbering `_manual: true` fields
> - Populate `verdict` and `learning` from the results automatically as a fallback
> - Never emit placeholder strings like "(auto-backfilled)"; if it can't compute a field, leave it blank and log a warning so Claude knows to author it
>
> **Why this matters:** the dashboard is the shared memory between sessions. A new Claude Code session resuming this project reads the dashboard reasoning panel to understand why a champion was chosen. Missing or shallow annotations mean lost institutional knowledge and wasted experiments that retry dead-end ideas.

## Anti-patterns

- **Placeholder "(auto-backfilled)" or "(no explicit citation)" entries.** They confess no work was done. Fix them or the next session repeats the experiment.
- **Authoring `verdict`/`learning` BEFORE the run** — predictions, yes; verdicts, no. The verdict is written from the result.
- **Skipping the `_manual: true` flag.** `backfill_reasoning.py` will clobber your hand-written citation.
- **Letting the journal drift from the JSON.** When they diverge, the JSON is canonical; update the journal from it.
- **Running `backfill_reasoning.py` instead of authoring** — backfill is for catching missed fields, not as a substitute for the 7-step process.

## Implementation checklist

1. Before launching experiment N+1, verify `reasoning_annotations.json[N]` has all 7 fields and `_manual: true`.
2. Pre-author `reasoning_annotations.json[N+1]` with `diagnosis`/`citations`/`hypothesis`/`prediction` + `_manual: true`.
3. After run, write `verdict` + `learning` from the JSONL output.
4. Mirror to `research_journal.md` under `## Exp<N> — <title>`.
5. Dashboard renders all 7 fields — sanity-check the panel after editing.

## References

- Source: `autoresearch/CLAUDE.md` section "Dashboard Reasoning Annotations (MANDATORY — capture EVERYTHING, every experiment)"
- Related: `citation-rigor`, `reasoning-blob-completeness`, `dashboard-files-update-mandate`, `mlops-documentation`, `seven-step-research-process`.
