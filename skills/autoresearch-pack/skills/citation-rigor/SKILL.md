---
name: citation-rigor
description: Citation rigor — mandatory format for the citations field (all authors, year, venue, title in quotes, arXiv ID, relevance note). Examples of good and BAD citations. Triggers on "citation", "arXiv", "venue", "(Keskar2017)", "bad citation", "citations field".
metadata:
  category: documentation
  source: autoresearch
  related: [dashboard-reasoning-annotations, reasoning-blob-completeness, seven-step-research-process]
---

# Citation Rigor (mandatory format)

## When to use

- Authoring the `citations` field of any `reasoning_annotations.json` entry.
- Reviewing a citation that looks short or vague — apply the spec.
- Onboarding a new contributor — point them at this skill.

## The rule

> ### Citation Rigor (MANDATORY format for `citations` field)
>
> **Every citation string MUST contain, for every paper referenced:**
>
> 1. **All authors' surnames** (not just first-author et al. unless > 6 authors)
> 2. **Year** of publication
> 3. **Venue** — journal name, conference abbreviation (NeurIPS, ICML, ICLR, AAAI, CVPR, KDD, etc.), or `arXiv` if preprint-only
> 4. **Full paper title** in single quotes
> 5. **arXiv ID** in the form `(arXiv:XXXX.YYYYY)` if available — mandatory for any paper posted to arXiv
> 6. **One-sentence relevance note** — why this paper motivates THIS experiment specifically
>
> **Format template:**
>
> ```
> Author1, Author2, Author3 YEAR VENUE 'Paper Title'
> (arXiv:XXXX.XXXXX) — one-sentence note on why we cite it here.
> ```
>
> **Multiple papers separated by semicolons + linebreak.** Minimum one primary citation per experiment; secondary citations encouraged when the experiment combines ideas from multiple papers.
>
> **Examples of GOOD citations (copy this style):**
>
> > Keskar, Mudigere, Nocedal, Smelyanskiy, Tang 2017 ICLR 'On Large-Batch Training for Deep Learning: Generalization Gap and Sharp Minima' (arXiv:1609.04836) — motivates bs=16 as a flat-minima probe.
>
> > Loshchilov & Hutter 2019 ICLR 'Decoupled Weight Decay Regularization' (arXiv:1711.05101) — AdamW wd acts as decoupled weight shrinkage, so perturbations must be log-scale.
>
> > Nie, Nguyen, Sinthong, Kalagnanam 2023 ICLR 'A Time Series is Worth 64 Words: Long-term Forecasting with Transformers' (arXiv:2211.14730) — requires seq_len ≥ 60 for attention heads to have enough patches.
>
> **Examples of BAD citations (REJECTED — rewrite required):**
>
> - `"Keskar 2017 flat minima"` — missing coauthors, venue, title, arXiv, relevance note
> - `"(Keskar2017)"` — parenthetical tag only, useless
> - `"Keskar et al."` — no year, no venue
> - `"arxiv paper on batch size"` — no attribution
> - `"(no citation tag)"` — confesses the author didn't do the work
> - `"see research_journal.md"` — redirects instead of citing
>
> **The goal:** anyone (including a future Claude Code session with zero project context) must be able to open the dashboard, click a row, read the `citations` field, and immediately know which paper to read and why. Citations are institutional memory.
>
> **Arxiv ID lookup discipline.** If you know the paper but not its arXiv ID, fetch it via WebSearch or WebFetch (arxiv.org/abs search) before writing the entry. Authoring a citation without the arXiv ID is a partial job.

## Anti-patterns

(See "Examples of BAD citations" above — every one is a regression in past projects.)

- **First-author-et-al when authors ≤ 6.** List them all.
- **Bracketed tag with no body** (`(Smith2020)`) — useless for retrieval.
- **Title in normal text** instead of single quotes — breaks the parser/dashboard rendering.
- **No relevance note.** A citation without a relevance note doesn't justify the experiment.
- **Citing the project's own journal** instead of the paper — the journal IS the citation context, not the source.

## Implementation checklist

1. Open the paper's arXiv page; copy the full author list, year, venue, title, arXiv ID.
2. Add the one-sentence relevance note connecting the paper to THIS experiment.
3. Multi-paper citations: separate with `; \n`.
4. Spot-check by reading the citation aloud — if you can't tell which paper from the text, rewrite.
5. If you don't know the arXiv ID, fetch it before saving the annotation.

## References

- Source: `autoresearch/CLAUDE.md` section "Citation Rigor (MANDATORY format for `citations` field)"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` same section.
- Related: `dashboard-reasoning-annotations`, `reasoning-blob-completeness`, `seven-step-research-process`.
