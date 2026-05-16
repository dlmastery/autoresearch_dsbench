# Style Guide

> Style is a tool for clarity, not aesthetics. The rules below maximise scan-ability for the next reader.

## Python

### Required

- **Python 3.10+ type hints.** `from __future__ import annotations` at the top of every module.
- **f-strings**, never `%` or `.format()`.
- **`pathlib.Path`** for every file path. Absolute paths everywhere.
- **Pure functions** for the analytic core (`runner._score`, `runner._fit_predict`, every agent in `forensic_audit.py`). Side effects in dedicated I/O functions named `_append_log`, `_write_trade_log`, `_write_manifest`.
- **Docstrings** with the citation when relevant.

### Avoid

- Mutable global state. The `_QA_DATA_CACHE` in `runner.py` is justified; add new caches only with the same justification.
- Wildcard imports.
- Bare `except:` — always `except Exception:` or narrower; re-raise or log.
- `time.sleep` inside the runner. Cooldowns are the hill-climb's responsibility.

## Markdown

### File structure

- **H1 once per file.** The title.
- **One blockquote near the top** identifying the audience.
- **Tables, not prose**, for structured data (parameters, agents, files in an archive).
- **Code blocks** with language fences: ` ```python ` / ` ```powershell ` / ` ```json ` / ` ```mermaid `.

### Cross-references

- Use relative paths from the current file.
- Never use absolute GitHub URLs for internal links.
- Use the in-browser markdown viewer for `.md` artefact links from dashboards: `dashboard/md_viewer.html?path=...`.

### Tone

- Active voice. "The runner writes the log" not "The log is written by the runner."
- Present tense.
- Imperative for runbook steps.
- Short sentences.

### What to skip

- Filler ("It is important to note that ...").
- Marketing language ("powerful", "robust", "comprehensive").
- Emoji.

## Citation style

Mandatory format:

```
Author1, Author2, Author3 YEAR VENUE 'Paper Title' (arXiv:XXXX.XXXXX) — one-sentence relevance.
```

Examples:

- Chen, Guestrin 2016 KDD 'XGBoost: A Scalable Tree Boosting System' (arXiv:1603.02754) — anchors the gradient-boosted-tree axis.
- Bishop 2006 'Pattern Recognition and Machine Learning' (PRML) §5.5.2 — early-stopping discipline.

Rules:

1. **All authors' surnames** — for ≤ 5 list all; for > 5 use "Author1 et al."
2. **Year** — publication year.
3. **Venue** — conference / journal / book.
4. **Title in single quotes** — exact title.
5. **arXiv ID in parens** — `(arXiv:XXXX.XXXXX)`. Omit only for pre-arXiv papers.
6. **Em-dash + one-sentence relevance.**

Parenthetical-only tags (`(Bishop 2006)`) are insufficient. The skill `citation-rigor` polices this.

## File naming

- Snake-case for Python: `forensic_audit.py`.
- Kebab-case for skill directories: `crash-recovery-checkpoint`.
- Numeric-prefix for ordered doc series: `01_design_doc.md`, `0001_use_synthetic_data_until_real_loaders.md`.
- Lower-case for everything in `docs/`.

## Word counts

Targets per file type, enforced by judgment:

| File type | Target |
|---|---|
| Architecture doc | 600-1500 words |
| ADR | 300-600 words |
| Runbook | 200-500 words |
| Postmortem | 500-1200 words |
| Reference page | 200-500 words |
| SLO page | 200-400 words |
| Onboarding page | 300-600 words |
| Contributing page | 300-800 words |

Going long is forgiven if every paragraph earns its space. Padding is not.

## Related

- [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Skill `citation-rigor`.
- Skill `mlops-documentation`.
