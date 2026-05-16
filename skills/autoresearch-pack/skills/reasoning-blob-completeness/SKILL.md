---
name: reasoning-blob-completeness
description: Reasoning blob completeness — per-field minimum content, word-count floor, must-include keywords for diagnosis/citations/hypothesis/prediction/verdict/learning/_manual. Batch-updates forbidden. Triggers on "reasoning blob", "word count floor", "minimum content", "acceptance criteria", "batch updates forbidden".
metadata:
  category: documentation
  source: autoresearch
  related: [dashboard-reasoning-annotations, citation-rigor, mlops-documentation]
---

# Reasoning Blob Completeness

## When to use

- Authoring or reviewing any `reasoning_annotations.json` entry.
- Building a linter / pre-commit check on annotation completeness.
- Spotting entries that look "done" but are actually too thin.

## The rule

> ### Reasoning Blob Completeness (what "full reasoning" means)
>
> Each of the 7 fields in `reasoning_annotations.json` has a minimum content spec. Entries that fall below this spec must be rewritten. Use these as acceptance criteria before an experiment is considered "documented":
>
> | Field | Minimum content | Word count floor | Must include |
> |-------|-----------------|------------------|--------------|
> | `diagnosis` | Why THIS experiment NOW; which champion weakness; which fold is worst and why (regime name, date range, uncertainty signature); what prior experiments ruled out | ≥ 60 words | Reference to at least one prior experiment by number OR a per-fold metric from the current champion |
> | `citations` | Per the Citation Rigor spec above | ≥ 40 words for single paper, ≥ 80 for multi-paper | Author list + year + venue + title + arXiv ID + relevance note for each paper |
> | `hypothesis` | The config change stated mechanistically — what parameter(s) move, what they do in the model, what the cited paper predicts will happen | ≥ 50 words | The word "mechanism" or "because" or "per [paper]"; the specific parameter and value |
> | `prediction` | Concrete numeric range on composite AND at least one fold-level or uncertainty-level sub-prediction | ≥ 25 words | A numeric range (e.g. "+6.30 to +6.50"); a direction for at least one sub-metric |
> | `verdict` | KEEP/DISCARD/NEAR-MISS + exact composite + delta vs global best + per-fold narrative (which folds carried or killed it) | ≥ 30 words | Status label; composite to 4 decimals; mention of at least one per-fold result |
> | `learning` | What this updates in the mental model; which axis is now closed/open; what to try next | ≥ 40 words | "Axis closed" / "axis open" language OR a concrete "next try: ..." |
> | `_manual` | Boolean | — | `true` if Claude-authored (expected for non-variance experiments); `false` only for mechanical reruns |
>
> **When running a batch of variance checks** (same config, varying seed), the `_manual: true` entries can share templated `diagnosis` and `citations` across runs, but `verdict`/`learning` must always be per-run-specific (different seed → different fold outcomes).
>
> **Batch updates are forbidden.** Don't do 5 experiments then update the journal/summary/checkpoint in one go — each experiment's state gets stale and crash-recovery breaks. Update everything, then move on.

## Anti-patterns

- **`diagnosis: "Need to improve fold 2"`** — 6 words, no prior-experiment reference, no per-fold metric. Rewrite.
- **`hypothesis: "Try lr=5e-4"`** — no mechanism, no paper, no parameter justification. Rewrite.
- **`prediction: "should improve"`** — no numeric range. Rewrite.
- **`verdict: "OK"`** — missing label, composite, delta, per-fold. Rewrite.
- **`learning: "good result"`** — missing axis-closed/axis-open language, missing next-try. Rewrite.
- **Batch-writing 5 verdicts at once.** State drifts between experiments; the 3rd verdict will lean on the wrong champion.

## Implementation checklist

1. Pre-commit / lint: each annotation entry has ≥ floor words per field and contains the must-include keyword(s).
2. Variance-check entries reuse `diagnosis`/`citations` template but author per-run `verdict` + `learning`.
3. Refuse to launch Exp N+1 if Exp N entries fail the spec.
4. Save the entry IMMEDIATELY after the run — don't wait until 5 runs later.
5. The dashboard renders the entry — if any field looks thin, fix it before moving on.

## References

- Source: `autoresearch/CLAUDE.md` section "Reasoning Blob Completeness (what \"full reasoning\" means)"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` same section.
- Related: `dashboard-reasoning-annotations`, `citation-rigor`, `mlops-documentation`, `seven-step-research-process`.
