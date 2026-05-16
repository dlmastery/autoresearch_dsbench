# Chapter 21 — Dependency Management

> *Parallel to:* SWE-book Chapter 21 *"Dependency Management"* (Winters, Manshreck, Wright 2020).

**Thesis.** The SWE-book chapter 21 says dependency management is the slow killer of software projects. Library version drift, transitive dependency conflicts, and the diamond dependency problem all become first-order issues at scale. The DSBench project's dependency graph is intentionally shallow (numpy, sklearn, xgboost, lightgbm, catboost, torch — top-level only), but it has a *protocol-level* dependency graph that needs the same care: **`framework/sota_catalog.yaml` is the protocol's dependency manifest, naming per-backbone training recipes and their citations**.

## 21.1 The two dependency graphs

| Graph | Nodes | Edges | Pinned by |
|---|---|---|---|
| **Python libraries** | numpy, sklearn, xgboost, lightgbm, catboost, torch, psutil, pyyaml | `requirements.txt` (not yet committed; convention only) | Conda environment + hand-versioning |
| **Protocol recipes** | 19 backbones (MLP, LSTM, PatchTST, PatchTSMixer, iTransformer, xLSTM, Mamba, FT-Transformer, TimesFM, Chronos-Bolt, Moirai, MOMENT, TiRex, Sundial, Time-MoE, TimeMixer, TimesNet, MambaTS, XGBoost, LightGBM, CatBoost) | per-backbone (epochs, lr, opt, paper citation) | `framework/sota_catalog.yaml` |

The Python-library graph is shallow and stable. The protocol-recipe graph is where the action is.

## 21.2 `framework/sota_catalog.yaml` as the dependency manifest

The catalog file is a YAML document keyed by backbone name with per-task-type recipes and citations:

```yaml
xgboost:
  classification_binary:
    recipe:
      n_estimators: 800
      max_depth: 6
      learning_rate: 0.05
      subsample: 0.9
      colsample_bytree: 0.8
    citation:
      authors: "Chen, Guestrin"
      year: 2016
      venue: "KDD"
      title: "XGBoost: A Scalable Tree Boosting System"
      arxiv: "1603.02754"
      relevance: "anchors the gradient-boosted-tree axis; section 4 covers depth-vs-iter tradeoff"
  regression:
    recipe: ...
    citation: ...
  qa_excel: null  # XGBoost not used for qa_excel; excel_agent is the backbone
```

Every recipe carries a citation in the canonical format. Every recipe is the *starting point* for a backbone's 25-iter exploration; the proposals in `framework/hill_climb.py` perturb from this default.

The catalog is a frozen contract. Changes to a recipe go through code review + an ADR + a re-run of the affected cohort.

## 21.3 The protocol's diamond dependency

A specific case of the SWE-book chapter 21's diamond dependency problem:

```
                  hill_climb.py
                 /             \
       _xgb_proposals      _lgbm_proposals
                 \             /
                 runner.run_one
                       │
                  load_or_make_data
                       │
              data/.data_cache/splits.npz
```

`runner.run_one` is the single point through which all proposals reach data. The diamond is: `_xgb_proposals` and `_lgbm_proposals` both go through `runner.run_one` because the runner is the audit-gate-respecting code path. Adding a new backbone that bypassed the runner would create a divergent leaf in the diamond — a violation of the Test-Set Embargo because the new backbone might not honour the discipline.

The mitigation: every backbone in `framework/runner.py:_fit_predict` is a function called by name. There are no parallel code paths. The diamond is structurally enforced.

## 21.4 The Python-library version pin

We do not currently commit a `requirements.txt`. The project's Python dependencies are described informally:

- Python 3.11.
- numpy ≥ 1.24.
- scikit-learn ≥ 1.3.
- xgboost ≥ 1.7.
- lightgbm ≥ 4.0.
- catboost ≥ 1.2.
- torch ≥ 2.0 (CPU build is fine; GPU build for FT-Transformer).
- psutil ≥ 5.9 (for `_pin_to_safe_cores`).
- pyyaml ≥ 6.0.

The local Anaconda install at `C:/Users/evija/anaconda3/` has these. The reproducibility contract is "install Python 3.11 + the above libraries". A future `requirements.txt` would pin exact versions; this has not been done because the project is single-operator and the environment is stable.

## 21.5 The transitive dependency problem

The SWE-book chapter 21 emphasises transitive dependencies: library X depends on library Y at version `>= 2.0`; library Z depends on Y at version `< 2.0`; conflict. Our equivalent:

- **xgboost and lightgbm both depend on numpy.** Conflict-free in practice.
- **torch and sklearn both depend on numpy.** Conflict-free in practice.
- **The FT-Transformer reference library** (when used) brings deep transitive dependencies. We avoid these by routing FT-Transformer through `_sklearn_fallback` (Histogram Gradient Boosting) on the hill-climb path; the real FT-Transformer is invoked only in the extended phase for `ft-transformer-large` family runs, and even then through a contained subprocess.

The project survives transitive dependency hell by keeping the top-level surface small and routing the "deep" backbones through the framework's substitution layer.

## 21.6 What we depend on outside the language environment

Two non-Python dependencies:

1. **Git** (Windows-native, with `schannel → openssl` SSL backend swap; see [postmortem 0005](../appendix_a_postmortems/0005_git_push_ssl_cert_failure.md)).
2. **GitHub** (the remote at <https://github.com/dlmastery/autoresearch_dsbench>; private credentials via PAT).

That is the full external surface. No CI service, no artefact repository, no package registry.

## 21.7 The sota_catalog as documentation

A subtle point: `sota_catalog.yaml` doubles as documentation. A reviewer who wants to know "what's the published-paper default for LightGBM on regression?" reads the catalog. The citation is a primary reference; the recipe is the starting point. The catalog is roughly 19 backbones × 4 task types × (recipe + citation) ≈ 150 YAML entries.

The catalog is committed to the repo. Changes are reviewed like code. The catalog's content is part of the protocol contract.

## 21.8 Adding a new backbone

The five-step process to add a new backbone (analogous to the SWE-book chapter 21's "add a new dependency" workflow):

1. **Add the recipe and citation to `framework/sota_catalog.yaml`.** Cite the paper in canonical format.
2. **Add the dispatch case to `framework/runner.py:_fit_predict`.** The case calls the backbone library (or `_sklearn_fallback` if no library).
3. **Add the proposal family to `framework/hill_climb.py` or `framework/extended_hill_climb.py`.** Document the iter taxonomy (iter 1 is published-paper default, iters 2-N are perturbations).
4. **Add the SKILL.md if the backbone has a discipline-level concern.** Most backbones do not; they share the protocol's general training rules.
5. **Re-run `audit_pack.py`** to confirm coverage is still 100 %.

The five steps are reviewable as a single commit. The Lessons-Learned table records the addition.

## 21.9 The "vendoring" decision

The SWE-book chapter 21 talks about when to vendor vs when to depend. Our decision:

- **We vendor nothing.** Every backbone library is a top-level pip / conda install.
- **We do not bundle the autoresearch protocol's source CLAUDE.md** (the FX project's `autoresearch/CLAUDE.md` and the SPY adaptation). The skill pack treats those as upstream documents and runs the audit against them at the local path. If they're missing on a target machine, the audit reports "skipped" rather than failing.

This is the right choice at our scale. Vendoring would mean shipping ~30 MB of upstream protocol text in our repo for very little gain.

## 21.10 The protocol-level diamond — qa_excel cross-task pooling

A protocol-level diamond worth naming explicitly: the qa_excel cross-task pooling discipline (cross-task training; per-task evaluation) means every task's `_excel_agent` depends on every other task's training data. This is a directed acyclic graph with 38 leaves all reaching back to a shared training pool.

The mitigation: the pool is constructed deterministically (`framework/runner.py:_pool_train_for_qa` reads the 38 train splits in slug-sorted order) and the manifest hashes are checked by Agent A per task. A change to the pool's construction is a cohort-wide change that requires re-running all 38 tasks; this is exactly the kind of large-scale change [Ch. 22](22_large_scale_changes.md) is built for.

## 21.11 Related

- [Ch. 8 — Style Guides and Rules](../part_3_processes/08_style_guides_and_rules.md): the protocol's style guide.
- [Ch. 22 — Large-Scale Changes](22_large_scale_changes.md): how to do cohort-wide refactors.
- [`framework/sota_catalog.yaml`](../../framework/sota_catalog.yaml): the per-backbone recipe + citation catalog.
- [`framework/runner.py`](../../framework/runner.py): the dispatch table.
- [ADR 0008](../appendix_b_adrs/0008_cross_task_pooling_for_training.md): the cross-task pooling discipline.
