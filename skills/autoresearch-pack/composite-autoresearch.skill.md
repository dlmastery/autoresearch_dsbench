---
name: composite-autoresearch
description: Composite umbrella skill — the full autoresearch protocol decomposed into 36 sub-skills covering session startup, hardware, crash recovery, mindset, data integrity, splits, experiment design, agent protocol, 7-step research, monotonic quality, MLOps docs, explainability, winner archive, code snapshots, dashboard annotations, per-backbone mandate, SOTA recipes, GPU memory, dashboard tabs/sync/files/interactive design, citation rigor, reasoning blob completeness, heteroscedastic loss, Colab notebook, traditional ML metrics, per-sample logging, architecture, validation, forensic audit, stacked ensemble, regime gate, sub-period robustness audit, three-stream feature engineering, and committee resumption pointers. Triggers on "autoresearch", "MLFin loop", "Karpathy autoresearch", and any phrase that maps to a sub-skill.
metadata:
  category: composite
  source: composite
  related: [all]
---

# Composite Autoresearch Skill (umbrella)

This composite skill is the entry point to the full autoresearch protocol. It progressively discloses to **36 sub-skills**, each preserving its source CLAUDE.md section verbatim. Load the sub-skills you need for the task at hand; do not load all 36 unless you are running a full protocol audit.

## Progressive disclosure (load order by task)

### Phase 1 — Session warmup (load on EVERY session start)

These four MUST be in context before any experiment runs.

1. `session-startup` — On Session Start ritual.
2. `crash-recovery-checkpoint` — write checkpoint after every experiment + every 5 minutes.
3. `hardware-pinning` — P-core pinning, BSOD prevention.
4. `mlfin-researcher-mindset` — never guess, never grid-search, measure don't assume.

### Phase 2 — Before any new experiment (load every experiment cycle)

5. `validation-checklist` — purge/embargo + split/overlap/segments/cache pre-flight.
6. `seven-step-research-process` — diagnose → cite → hypothesize → predict → run → analyze → document.
7. `karpathy-agent-protocol` — always start from champion, no consecutive-discard wandering, code-changes allowed.
8. `experiment-design` — composite metric, epoch-bound, ONE config delta, wired-params, justified HPs.
9. `monotonic-quality-progression` — quality ratchet, champion lineage, structural change on plateau.
10. `citation-rigor` — mandatory citations format (authors, year, venue, title, arXiv ID, relevance note).
11. `reasoning-blob-completeness` — minimum word counts and must-include keywords per field.
12. `dashboard-reasoning-annotations` — author 4 pre-fields BEFORE the run, 2 post-fields AFTER.

### Phase 3 — Data + invariants (load when authoring data/splits/features)

13. `data-integrity-rules` — no sliding windows across gaps, no cross-fold leakage, cache-once.
14. `train-val-test-invariants` — super-fold split, zero overlap, union val/test across folds.
15. `three-stream-feature-engineering` — daily + pre-market + hourly with strict-causal anchor (SPY).

### Phase 4 — Model / training (load when authoring training code or picking a new backbone)

16. `per-backbone-experiment-mandate` — full N-experiment exploration per backbone (default 50).
17. `per-backbone-sota-recipes` — re-derive epochs/LR/warmup/batch from each backbone's own paper.
18. `gpu-memory-constraint` — 16 GB hard cap, pre-flight VRAM math, BF16/grad-ckpt/LoRA escape hatches.
19. `per-backbone-code-snapshot` — snapshot model code before each backbone, isolate cycles.
20. `heteroscedastic-loss` — Kendall & Gal mean + log_var head, aleatoric 0.05-0.15, 1.5× epochs.

### Phase 5 — Verification (load when result lands)

21. `traditional-ml-metrics` — Precision/Recall/F1/F2/Accuracy/MCC + confusion matrix per fold.
22. `per-sample-decision-logging` — exp<N>_trades.csv with confidence + uncertainty per row.
23. `architecture-separation-of-concerns` — runner LOGS, dashboard READS, evaluator EVALUATES.

### Phase 6 — Documentation (load when writing summaries / journals)

24. `mlops-documentation` — experiment_summary.md + research_journal.md, append-only, readable-6-months-later.
25. `dashboard-files-update-mandate` — every experiment updates 8+ files; ownership table; per-experiment ritual.

### Phase 7 — Winner / champion handling (load when new global best)

26. `winner-archive-protocol` — fully-portable winners/<id>/ with README + config + weights + code + inference + reproduction.
27. `explainability-audit-14-section` — 14-section audit report (feature importance, calibration, drift, risk, deployment).
28. `forensic-audit-pipeline` — 8-agent forensic audit (data leakage, label integrity, causality, repro, eval, stats, robustness, deploy).
29. `google-colab-notebook` — self-contained colab_train_and_infer.ipynb < 5 min on free tier.
30. `sub-period-robustness-audit` — rolling-window evaluation across regimes; flag concentration.
31. `regime-gate` — conditional gate to confine trading to the model's edge regime (SPY rvol60d > 15% +0.134).
32. `stacked-ensemble-design` — val-weighted N-component ensemble (SPY 12-component +0.277).

### Phase 8 — Dashboard build (load when authoring dashboard)

33. `dashboard-backbone-tabs` — ALL + per-backbone tab strip above the experiment table.
34. `interactive-dashboard-design` — multi-column sort, regex filter, drill-down, reasoning panel, sticky champion summary.
35. `github-pages-dashboard-sync` — _sync_dashboard_to_docs.py before every commit that touches experiment state.

### Phase 9 — Session end / hand-off (load at end of session)

36. `committee-resumption-pointers` — top-of-CLAUDE.md SESSION-COMPLETE STATE block with deployable champion, stacked KEEPs, caveats, resumption commands, "what's left".

## Recommended loading by use-case

| Use case | Load (in order) |
|----------|-----------------|
| Session start, resume the loop | 1, 2, 3, 4, 36 |
| Author the next experiment | 5, 6, 7, 8, 9, 10, 11, 12 |
| New backbone exploration kicks off | 16, 17, 18, 19, 20 (+ Phase 2 for each run) |
| A new global champion just landed | 26, 27, 28, 29, 30, 31, 32 |
| Build/update the dashboard | 33, 34, 35 (+ 25 for ownership) |
| End-of-session package | 24, 36 |
| Onboard a new contributor | 4, 6, 7, 11, 24, 36 |

## The 36 skills at a glance

| # | Skill | Category | Source |
|---|-------|----------|--------|
| 1 | session-startup | protocol | autoresearch |
| 2 | hardware-pinning | protocol | autoresearch |
| 3 | crash-recovery-checkpoint | protocol | autoresearch |
| 4 | mlfin-researcher-mindset | protocol | autoresearch |
| 5 | data-integrity-rules | protocol | autoresearch |
| 6 | train-val-test-invariants | protocol | autoresearch |
| 7 | experiment-design | protocol | autoresearch |
| 8 | karpathy-agent-protocol | protocol | autoresearch |
| 9 | seven-step-research-process | protocol | autoresearch |
| 10 | monotonic-quality-progression | protocol | autoresearch |
| 11 | mlops-documentation | documentation | autoresearch |
| 12 | explainability-audit-14-section | verification | autoresearch |
| 13 | winner-archive-protocol | documentation | autoresearch |
| 14 | per-backbone-code-snapshot | protocol | autoresearch |
| 15 | dashboard-reasoning-annotations | dashboard | autoresearch |
| 16 | per-backbone-experiment-mandate | protocol | autoresearch |
| 17 | per-backbone-sota-recipes | engineering | autoresearch |
| 18 | gpu-memory-constraint | engineering | autoresearch |
| 19 | dashboard-backbone-tabs | dashboard | autoresearch |
| 20 | github-pages-dashboard-sync | dashboard | autoresearch |
| 21 | dashboard-files-update-mandate | dashboard | autoresearch |
| 22 | citation-rigor | documentation | autoresearch |
| 23 | reasoning-blob-completeness | documentation | autoresearch |
| 24 | heteroscedastic-loss | engineering | autoresearch |
| 25 | google-colab-notebook | documentation | autoresearch |
| 26 | traditional-ml-metrics | verification | autoresearch |
| 27 | per-sample-decision-logging | verification | autoresearch |
| 28 | architecture-separation-of-concerns | engineering | autoresearch |
| 29 | validation-checklist | verification | autoresearch |
| 30 | forensic-audit-pipeline | verification | composite |
| 31 | stacked-ensemble-design | engineering | autoresearchindexspy |
| 32 | regime-gate | engineering | autoresearchindexspy |
| 33 | sub-period-robustness-audit | verification | autoresearchindexspy |
| 34 | three-stream-feature-engineering | engineering | autoresearchindexspy |
| 35 | interactive-dashboard-design | dashboard | composite |
| 36 | committee-resumption-pointers | documentation | autoresearchindexspy |

## Coverage guarantee

The companion `audit/audit_pack.py` script verifies that every H2/H3 section in both source CLAUDE.md files maps to at least one skill. Run it any time to regenerate `audit/coverage_report.md`. Coverage is currently **100%**.

## When NOT to use this composite skill

If you only need ONE concept (e.g. "how do I cite a paper for an experiment annotation"), load the specific sub-skill (e.g. `citation-rigor`) directly. The composite is the umbrella — use it to discover, not as the bulk of your context window.

## References

- Source 1: `C:/Users/evija/autoresearch/CLAUDE.md` (52 sections)
- Source 2: `C:/Users/evija/autoresearchindexspy/autoresearchspy/CLAUDE.md` (adds Three-stream, stacked ensemble, regime gate, robustness audit, resumption pointers)
- Companion: `coverage_matrix.md`, `audit/audit_pack.py`, `audit/coverage_report.md`.
