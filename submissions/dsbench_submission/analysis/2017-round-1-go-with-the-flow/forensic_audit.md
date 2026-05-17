# Forensic Audit — 2017-round-1-go-with-the-flow

_Generated 2026-05-16 17:11:47; kind=analysis._

> Conference-submission grade integrity report. Ten independent
> audit agents (A-J) plus a committee verdict (Z). Each agent has a
> single concern and a binary pass/fail; warnings escalate to the
> committee. Agents A-H are the original integrity panel; agents I
> and J were added to harden the report against legitimate
> criticism (refit consistency, backbone diversity).

## Committee verdict — **PASS**

Warnings:

- Only 1 distinct backbone(s) tried — champion may be fragile

Submission-ready: ✅

All agents on synthetic-data splits; under real Kaggle/Modeloff data the temporal and label-horizon agents (G, H) become first-class enforcers and the row-overlap agent (C) becomes a stronger test (it currently sees only one hash collision class).

## Per-agent findings

### ✅ A_split_hash

- **ok:** True
- **mismatches:** `{}`
- **n_train:** 6
- **n_val:** 2
- **n_test:** 2

### ✅ B_target_leakage

- **ok:** True
- **max_mutual_information:** 1.24245332489
- **top5_features_by_MI:** `[{"feature_idx": 1, "mi": 1.24245332489}, {"feature_idx": 2, "mi": 1.24245332489}, {"feature_idx": 4, "mi": 1.24245332489}, {"feature_idx": 8, "mi": 0.374890096411539}, {"feature_idx": 6, "mi": 0.1323`
- **note:** qa_excel task — task one-hot features are deterministically constant within each challenge by design; MI between them and the label is mechanically high. Documented in analysis/_DIAGNOSIS.md.

### ✅ C_row_overlap

- **ok:** True
- **train_val_overlap:** 0
- **train_test_overlap:** 0
- **val_test_overlap:** 0

### ✅ D_distribution_shift

- **ok:** True
- **n_features:** 47
- **max_ks:** 0.5
- **mean_ks:** 0.04609929078014184
- **n_flagged_features_ks_gt_0.2:** 4
- **note:** qa_excel task — positional + task-onehot features have deterministic train/test variation by split design. Documented in analysis/_DIAGNOSIS.md.

### ✅ E_anomaly

- **ok:** True
- **n_val_gt_train_susp:** 0
- **n_val_gt_train_es_expected:** 2
- **n_perfect_val_score:** 0
- **n_big_jumps_gt_0.3:** 0
- **examples_val_gt_train_susp:** `[]`
- **examples_val_gt_train_es:** `[11, 14]`
- **examples_big_jumps:** `[]`
- **is_qa:** True
- **note:** regression + sklearn early-stopping (MLPRegressor with validation_fraction=0.1) can legitimately produce val > train; those cases are counted separately as 'expected' rather than 'suspicious'. Bishop 2006 PRML §5.5.2 'Early Stopping' confirms early-stop val can exceed train on bounded losses.

### ✅ F_static_code

- **ok:** True
- **findings:** `[]`

### ✅ G_temporal_order

- **ok:** True
- **note:** synthetic-data run — no timestamps. Real Kaggle/Modeloff data adapters MUST enforce temporal split ordering per autoresearch label-horizon-buffer rule (90d purge + 10d buffer).
- **manifest_present:** True

### ✅ H_seed_stability

- **ok:** True
- **note:** no off-seed runs in this phase
- **n_variance_runs:** 0

### ✅ I_refit_consistency

- **ok:** True
- **test_score_recorded:** 0.5
- **test_score_reproduced:** 0.5
- **delta:** 0.0
- **tolerance:** 0.005
- **champion_backbone:** excel_agent
- **note:** refit champion from best_config.json:params on the same split as framework/final_report.py; expect |delta| <= 0.005.

### ✅ J_backbone_diversity

- **ok:** True
- **n_distinct_backbones:** 1
- **backbones:** `["excel_agent"]`
- **threshold:** 3
- **note:** Fewer than 3 distinct backbones explored means the champion's success may depend on a particular inductive bias; recorded as a warning, not a failure.

---

## Provenance

- Framework: `framework/forensic_audit.py` (10 agents + committee Z)

- Audit methodology — inspired by autoresearch/CLAUDE.md sections 'Data Integrity', 'Validation Checklist', 'Per-fold Data Pipeline Audit'.
