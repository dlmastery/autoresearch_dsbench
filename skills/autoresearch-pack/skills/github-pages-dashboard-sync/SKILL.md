---
name: github-pages-dashboard-sync
description: GitHub Pages dashboard sync mandate — copy dashboard.html + data files to docs/dashboard/ on every commit that changes experiment state, treat the Pages mirror as a public freshness contract. Triggers on "GitHub Pages", "docs/dashboard", "_sync_dashboard_to_docs", "dashboard sync".
metadata:
  category: dashboard
  source: autoresearch
  related: [dashboard-files-update-mandate, mlops-documentation]
---

# GitHub Pages Dashboard Sync

## When to use

- After every experiment that writes to `experiment_log.jsonl`.
- After any edit to `reasoning_annotations.json`.
- After every winner archive.
- Before every `git push` — staleness is a regression.

## The rule

> ### GitHub Pages Dashboard Sync (MANDATORY — every push, zero exceptions)
>
> **The live dashboard MUST be published to GitHub Pages on every commit that changes experiment state.** Hosted at:
>
> > https://dlmastery.github.io/autoresearch/dashboard/
>
> **Source of truth:** `autoresearch/autoresearch_results/dashboard.html` (+ its data files: `experiment_log.jsonl`, `best_config.json`, `reasoning_annotations.json`, and the `.md` report/journal/summary files the dashboard links to).
>
> **Pages mirror:** `docs/dashboard/` — GitHub Pages serves the `docs/` folder; the dashboard's `dashboard.html` is copied to `docs/dashboard/index.html` so the URL `/dashboard/` routes directly to it.
>
> **The sync step runs BEFORE every `git commit` that touches experiment state:**
>
> ```bash
> python -m autoresearch._sync_dashboard_to_docs
> # or equivalently
> python autoresearch/_sync_dashboard_to_docs.py
> ```
>
> The script copies:
> - `autoresearch_results/dashboard.html` → `docs/dashboard/index.html`
> - `autoresearch_results/experiment_log.jsonl` → `docs/dashboard/experiment_log.jsonl`
> - `autoresearch_results/best_config.json` → `docs/dashboard/best_config.json`
> - `autoresearch_results/reasoning_annotations.json` → `docs/dashboard/reasoning_annotations.json`
> - Optional: `experiment_summary.md`, `autoresearch_report.md`, `research_journal.md`, `medium_article.md` if present
>
> The sync script is idempotent; run it freely. It fails loudly if any required file is missing.
>
> **When must you sync?**
>
> - After every experiment that writes to the JSONL (effectively: every `run_autoresearch` call)
> - After every reasoning-annotation edit
> - After every winner archive
> - Before every `git push` — the commit without the synced `docs/dashboard/` is a bug
>
> **Enforcement:** a commit that changes `autoresearch/autoresearch_results/experiment_log.jsonl` but does NOT update `docs/dashboard/experiment_log.jsonl` is a regression. In practice this means the commit ritual is:
>
> ```bash
> # 1. run experiments (runner auto-writes JSONL + trade logs + annotations)
> # 2. edit reasoning annotations to full-rigor post-run verdict/learning
> # 3. sync dashboard to docs/
> python autoresearch/_sync_dashboard_to_docs.py
> # 4. stage + commit
> git add autoresearch/autoresearch_results docs/dashboard autoresearch/memory
> git commit -F .commit_msg.txt
> # 5. push (Pages rebuilds within ~30-60s)
> git push origin master
> ```
>
> **Verification:** after push, `curl https://dlmastery.github.io/autoresearch/dashboard/best_config.json` should show the latest champion within 2 minutes. If stale, check `git log -1 docs/dashboard/` — the commit that updated the pages folder must match the commit that updated the source.
>
> **Why this matters:** the paper and Medium article both cite the live dashboard as the project's institutional memory. A stale dashboard makes the citation a lie. Treat the Pages mirror as a public artefact with the same freshness guarantees as the JSONL.

## Anti-patterns

- **Forgetting to run `_sync_dashboard_to_docs.py` before commit.** The push lands stale Pages.
- **Editing `docs/dashboard/` directly.** It's a mirror — edit the source.
- **Lazy "I'll sync at end of session"** — every state-changing commit must sync.
- **Trusting "git status looks clean".** Pages mirror staleness is silent — verify with `curl` after push.
- **Sync without staging the docs folder.** `git add autoresearch_results` alone won't include `docs/dashboard/`.

## Implementation checklist

1. `_sync_dashboard_to_docs.py` is idempotent and fails loudly on missing files.
2. Pre-commit hook (or convention) runs the sync before every commit that touches `autoresearch_results/`.
3. `git status` after sync shows `docs/dashboard/` as modified — stage it.
4. After `git push`, run `curl <pages-url>/best_config.json` to verify freshness.
5. Document the URL prominently in the project README so external readers can find the live dashboard.

## References

- Source: `autoresearch/CLAUDE.md` section "GitHub Pages Dashboard Sync (MANDATORY — every push, zero exceptions)"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` same section.
- GitHub Pages docs (`docs/` folder publishing model).
- Related: `dashboard-files-update-mandate`, `mlops-documentation`.
