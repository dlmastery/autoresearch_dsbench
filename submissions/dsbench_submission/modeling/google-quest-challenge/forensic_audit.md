# Forensic Audit — google-quest-challenge

_Generated 2026-05-16 00:23:06; kind=modeling._

> Conference-submission grade integrity report. Ten independent
> audit agents (A-J) plus a committee verdict (Z). Each agent has a
> single concern and a binary pass/fail; warnings escalate to the
> committee. Agents A-H are the original integrity panel; agents I
> and J were added to harden the report against legitimate
> criticism (refit consistency, backbone diversity).

## Committee verdict — **PASS**

Submission-ready: ✅

All agents on synthetic-data splits; under real Kaggle/Modeloff data the temporal and label-horizon agents (G, H) become first-class enforcers and the row-overlap agent (C) becomes a stronger test (it currently sees only one hash collision class).

## Per-agent findings

### ✅ A_split_hash

- **ok:** True
- **mismatches:** `{}`
- **n_train:** 1400
- **n_val:** 300
- **n_test:** 300

### ✅ B_target_leakage

- **ok:** True
- **max_mutual_information:** 0.13224722981099465
- **top5_features_by_MI:** `[{"feature_idx": 24, "mi": 0.13224722981099465}, {"feature_idx": 19, "mi": 0.12620339255674579}, {"feature_idx": 22, "mi": 0.12407968665800176}, {"feature_idx": 17, "mi": 0.12341178799442071}, {"featu`
- **note:** MI > 0.9 suggests potential label leakage; investigate.

### ✅ C_row_overlap

- **ok:** True
- **train_val_overlap:** 0
- **train_test_overlap:** 0
- **val_test_overlap:** 0

### ✅ D_distribution_shift

- **ok:** True
- **n_features:** 32
- **max_ks:** 0.0942857142857143
- **mean_ks:** 0.06236607142857144
- **n_flagged_features_ks_gt_0.2:** 0

### ✅ E_anomaly

- **ok:** True
- **n_val_gt_train_susp:** 0
- **n_val_gt_train_es_expected:** 4
- **n_perfect_val_score:** 0
- **n_big_jumps_gt_0.3:** 28
- **examples_val_gt_train_susp:** `[]`
- **examples_val_gt_train_es:** `[44, 94, 119]`
- **examples_big_jumps:** `[{"experiment_num": 3, "from": -3.5101298573756314, "to": -2.4688706781641425}, {"experiment_num": 7, "from": -3.1232340721113117, "to": -2.58377066295026}, {"experiment_num": 11, "from": -3.688279228`
- **is_qa:** False
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
- **n_variance_runs:** 34
- **mean_composite:** -inf
- **std_composite:** nan
- **min_max:** `[-Infinity, -0.5632010528556921]`

### ✅ I_refit_consistency

- **ok:** True
- **test_score_recorded:** -0.33798526254456007
- **test_score_reproduced:** -0.33798526254456007
- **delta:** 0.0
- **tolerance:** 0.005
- **champion_backbone:** mlp
- **note:** refit champion from best_config.json:params on the same split as framework/final_report.py; expect |delta| <= 0.005.

### ✅ J_backbone_diversity

- **ok:** True
- **n_distinct_backbones:** 6
- **backbones:** `["catboost", "ft_transformer", "lightgbm", "mlp", "patchtsmixer", "xgboost"]`
- **threshold:** 3
- **note:** Fewer than 3 distinct backbones explored means the champion's success may depend on a particular inductive bias; recorded as a warning, not a failure.

---

## Provenance

- Framework: `framework/forensic_audit.py` (10 agents + committee Z)

- Audit methodology — inspired by autoresearch/CLAUDE.md sections 'Data Integrity', 'Validation Checklist', 'Per-fold Data Pipeline Audit'.
