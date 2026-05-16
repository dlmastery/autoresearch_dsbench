# Chapter 25 — Compute as a Service

> *Parallel to:* SWE-book Chapter 25 *"Compute as a Service"* (Winters, Manshreck, Wright 2020).

**Thesis.** The SWE-book chapter 25 describes Borg / Kubernetes / cloud compute as the substrate Google's services run on. The DSBench parallel is the reference 14th-gen HX laptop with its hybrid P-core / E-core CPU and 16 GB Ada-class GPU. The "compute service" here is a single machine with a strict hardware contract: **P-cores 0, 2, 4, 6 for sustained compute; ≤ 16 GB VRAM; E-cores BANNED**. The contract is encoded in `framework/runner.py:_pin_to_safe_cores()` and is the substrate every experiment runs on.

## 25.1 The hardware contract

| Resource | Budget | Enforced by |
|---|---|---|
| CPU | P-cores only (logical IDs 0, 2, 4, 6). 4 threads default. | `framework.runner._pin_to_safe_cores()` |
| GPU VRAM | ≤ 16 GB (3 GB params FP32, 6 GB optimiser state, 3 GB grads, 3 GB activations, 1 GB reserved). | Pre-flight check in Experiment 1 reasoning annotation per backbone. |
| RAM | 64 GB; not a binding constraint. | — |
| Disk | `.data_cache/splits.npz` per task (≤ 5 MB each). | `_write_manifest` |

The reference machine is an Intel 14th-gen HX laptop with hybrid P-cores and E-cores. WHEA-Logger reports internal parity errors on CPU APIC IDs 16, 17, 24, 25 — all E-cores. Sustained compute on E-cores BSODs the machine within ~3 minutes. The runtime contract is therefore:

> **E-cores are BANNED.** Use ONLY P-cores. Default 4 P-core threads via `torch.set_num_threads(4)` + `cpu_affinity([0, 2, 4, 6])`.

The runner enforces this on first import:

```python
def _pin_to_safe_cores() -> None:
    if os.environ.get("AUTORESEARCH_USE_ALL_CORES") == "1":
        return
    n_threads = int(os.environ.get("AUTORESEARCH_N_THREADS", "4"))
    try:
        import torch
        torch.set_num_threads(n_threads)
    except Exception:
        pass
    try:
        import psutil
        psutil.Process().cpu_affinity([0, 2, 4, 6][:n_threads])
    except Exception:
        pass
    os.environ.setdefault("OMP_NUM_THREADS", str(n_threads))
    os.environ.setdefault("MKL_NUM_THREADS", str(n_threads))
    os.environ.setdefault("OPENBLAS_NUM_THREADS", str(n_threads))

_pin_to_safe_cores()
```

The function is the literal first call in `runner.py`. Skipping it crashes the laptop within minutes. The escape hatch `AUTORESEARCH_USE_ALL_CORES=1` exists for non-sustained debugging only; do not commit any setting that enables it.

## 25.2 The "compute service" contract

Even though there's no cloud, the project treats the reference hardware as a *service*. Three properties of the contract:

1. **Reservation.** The 4 P-cores 0, 2, 4, 6 are reserved for the runner during a cohort run. Foreground GUI work is fine (Windows still has 12 logical CPUs available for the desktop); background batch work on those P-cores would slow the cohort but not break it.
2. **Quotas.** The GPU VRAM budget is split into 5 buckets (params / optimiser / grads / activations / reserved). A new backbone's first experiment must check the budget in its reasoning annotation; exceeding it would OOM and crash the run.
3. **Isolation.** Each `runner.run_one` call is a fresh process state. The runner does not spawn threads that survive the call. A crash in one experiment does not leave residue for the next.

The contract is checked by:

- `_pin_to_safe_cores` at every runner import.
- The pre-flight VRAM check in the per-backbone first-experiment annotation.
- The cooldown between experiments (`COOLDOWN_SEC`, default 30 sec) to let thermals stabilise.

## 25.3 The cooldown

A specific operational note: the base hill-climb has a 30-second cooldown per experiment (override via `COOLDOWN_SEC`). The purpose is to let CPU and GPU thermals stabilise between experiments. On the reference machine, sustained back-to-back compute pushes the CPU package to 95–100 °C; the cooldown drops it to 75–80 °C before the next experiment starts.

The cooldown is convention, not enforcement. A test-mode default of `COOLDOWN_SEC=0` is used for fast iteration during framework development; production runs (cohort-wide) honour the 30-second budget.

## 25.4 The "what if we had Kubernetes" thought experiment

The SWE-book chapter 25 argues for elastic compute. If we had Kubernetes, what would change?

| What would change | Effect on the project |
|---|---|
| 112 tasks could run in parallel | Wall-clock for a cohort drops from ~6 hours to ~5 minutes. |
| Per-task isolation in containers | The forensic committee's static-code audit (Agent F) becomes lower-stakes; per-container the runner can't accidentally read another task's data. |
| Reproducible Docker image | The Python environment becomes hermetic; the schannel SSL issue would not exist on Linux containers. |
| Cost | A non-zero monthly bill instead of zero. |
| Determinism | Worse — different container hosts produce slightly different floating-point results; cross-host reproducibility within Agent I's ±0.005 threshold is plausible but not guaranteed. |

The thought experiment ends: the wall-clock benefit is real, but the project's scale (single operator, 112 tasks, ~6-hour cohort) doesn't justify the operational complexity. If the cohort grew to 540 tasks ([Ch. 6](../part_2_culture/06_leading_at_scale.md) scale section), parallel compute would become worth the investment.

## 25.5 The 16 GB VRAM budget — detail

The 16 GB GPU is the project's binding scarce resource for the deep backbones. The budget breakdown:

| Bucket | Size | Purpose |
|---|---|---|
| Params (FP32) | 3 GB | Model weights. |
| Optimiser state | 6 GB | Adam-style 2× weights (m, v); some optimisers more. |
| Gradients | 3 GB | One copy per weight. |
| Activations | 3 GB | Forward-pass intermediate tensors; depends on batch size and depth. |
| Reserved | 1 GB | CUDA workspace + safety margin. |
| **Total** | **16 GB** | |

The MLP backbones (`mlp`, `ft_transformer`) fit comfortably. The transformer-style backbones (`patch_tsmixer`, `lstm-tabular` with sequence length > 100) need batch-size tuning to fit. The extended-phase families that target very large models (FT-Transformer-large, TabNet, TabPFN) route through `_sklearn_fallback` (HistGB) when the budget would be exceeded — the substitution is logged.

The budget is encoded in `framework/CLAUDE_template.md` § "GPU Memory Constraint (MANDATORY — 16 GB VRAM hard cap)" and verified by the human reading the per-backbone first-experiment annotation. There is no automated VRAM monitor; it's a contract enforced by review.

## 25.6 The data substrate

Compute is one half of "compute as a service"; data is the other half. The project's data substrate:

- **Tabular Kaggle data** lives in `<task>/data/.data_cache/splits.npz`. Generated on first run; hash-pinned in `data/split_manifest.json`. Each cache is ≤ 5 MB.
- **Modeloff qa_excel data** lives in `_analysis_data.json` at the repo root (parsed and committed). The synthetic-Gaussian fallback ([Ch. 13](../part_3_processes/13_test_doubles.md)) is the substitute when real data is unavailable.
- **Registry** lives in `registry/modeling_tasks.json` and `registry/analysis_tasks.json`. These are committed and serve as the per-task contract (slug, problem_type, metric, baseline).

Total committed data: ~5 MB across the 112 tasks. The repo is small.

## 25.7 The "where it crashes" failure modes

Three classes of compute failure the project has observed:

1. **E-core BSOD.** Mitigated by `_pin_to_safe_cores`. Has not occurred since pinning was added.
2. **GPU OOM.** Mitigated by the 16 GB budget convention and `_sklearn_fallback`. Occurs occasionally when a new backbone is added without the pre-flight check; caught by the first-experiment failure and a Lessons-Learned row.
3. **Windows Update reboot.** Mitigated by the Checkpoint-After-Every-Experiment Rule ([Ch. 16](16_version_control_and_branches.md)). A reboot loses at most one experiment.

Each failure mode has a corresponding mitigation in the runtime contract. The discipline is to *expect* the failure and pre-build the recovery, not to *prevent* the failure.

## 25.8 What the project depends on outside the laptop

The project has three external compute dependencies:

1. **GitHub** — for git push and public hosting. Used at most a few times per day.
2. **Kaggle** — for the original tabular CSVs. Used once at scaffold generation; the data is cached locally.
3. **The DSBench paper's reference numbers** — for the baselines in `registry/modeling_tasks.json`. Used once at registry build; the numbers are pinned.

There are no continuous external dependencies. The cohort runs offline once the data is cached.

## 25.9 The single-machine ceiling

The reference hardware sets the project's ceiling. What we can't do:

- **Cannot run 112 tasks in parallel.** The single GPU has 16 GB; one task's MLP training uses ~8 GB; two simultaneous deep tasks would OOM.
- **Cannot run the full 14,000-experiment cohort in under 4 hours.** The wall-clock is bounded by the 30-sec cooldown × 14,000 ≈ 117 hours theoretical, ~6 hours practical with cooldown skipped during base-loop testing.
- **Cannot run continuous re-cohort.** A cohort run takes a fraction of a day; running it daily would consume the machine. Cadence is event-driven, per [Ch. 24](24_continuous_delivery.md).

These constraints are real. Lifting them requires either parallel compute ([§ 25.4](#254-the-what-if-we-had-kubernetes-thought-experiment)) or smaller per-experiment work (which would violate the One-Knob Rule).

## 25.10 Related

- [Ch. 14 — Larger Testing](../part_3_processes/14_larger_testing.md): the hill-climb that consumes the compute.
- [Ch. 16 — Version Control and Branches](16_version_control_and_branches.md): the Checkpoint-After-Every-Experiment Rule.
- [Postmortem 0005 — git push SSL](../appendix_a_postmortems/0005_git_push_ssl_cert_failure.md): the only external-dependency failure mode observed.
- [`framework/runner.py:_pin_to_safe_cores`](../../framework/runner.py): the hardware-contract enforcement.
- [Appendix D — diagrams](../appendix_d_diagrams/per_experiment_lifecycle.mmd): the per-experiment lifecycle on the reference hardware.
