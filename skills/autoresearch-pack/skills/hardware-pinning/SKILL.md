---
name: hardware-pinning
description: P-core pinning, E-core bans, and BSOD-prevention rules for ML workloads on Intel hybrid CPUs. Triggers on "hardware constraints", "BSOD", "P-core", "E-core", "cpu_affinity", "WHEA-Logger", "set_num_threads".
metadata:
  category: protocol
  source: autoresearch
  related: [session-startup, crash-recovery-checkpoint]
---

# Hardware Pinning (P-cores only, BSOD prevention)

## When to use

- Authoring a new training/runner script that will run sustained compute on an Intel 14th-gen HX (or similar hybrid P/E-core) system.
- Inheriting a script that uses default `torch.set_num_threads()` — it almost certainly schedules onto E-cores and will BSOD.
- Investigating a `WHEA-Logger` parity-error or unexplained Windows kernel crash.

## The rule

> **E-cores are BANNED.** On Intel 14th-gen HX system (32 logical CPUs), WHEA-Logger reported Internal parity errors on CPU APIC IDs 16, 17, 24, 25 (all E-cores). System BSODed 4 times today under sustained compute.
>
> - **Use ONLY P-cores**: logical IDs 0-15. Even IDs (0,2,4,...,14) are primary threads, odd IDs (1,3,...,15) are HT siblings.
> - **Default**: 4 P-core threads via `torch.set_num_threads(4)` + `cpu_affinity([0,2,4,6])`.
> - **GPU does heavy compute**; CPU is coordination only. 4 cores is enough.
> - `run_autoresearch.py:_pin_to_safe_cores()` handles this automatically.
> - Override with env var `AUTORESEARCH_USE_ALL_CORES=1` (not recommended).
> - Override thread count with `AUTORESEARCH_N_THREADS=N`.
>
> **NEVER run a training loop without the pinning.** If you write a new runner script, call `_pin_to_safe_cores()` first thing or the laptop will BSOD.

## Anti-patterns

- **`torch.set_num_threads(os.cpu_count())`** — schedules onto the parity-error-prone E-cores; sustained load → BSOD within minutes.
- **Setting affinity AFTER instantiating DataLoader.** Workers inherit the parent affinity at fork-time; pin before constructing any pool.
- **Trusting Windows scheduler hints.** The scheduler will silently migrate threads to E-cores during heavy compute. Pin explicitly.
- **Pinning to a single core (`[0]`).** Single-core pin throttles GPU feeders and stalls training. Use 4 P-cores minimum.
- **Skipping pinning "just for a quick experiment".** Quick experiments are the most common BSOD trigger because they're run without ceremony.

## Implementation checklist

1. Top of every runner script:
   ```python
   import os, psutil, torch
   def _pin_to_safe_cores():
       if os.environ.get("AUTORESEARCH_USE_ALL_CORES") == "1":
           return
       n = int(os.environ.get("AUTORESEARCH_N_THREADS", 4))
       cores = [0, 2, 4, 6][:n]  # P-core primary threads only
       psutil.Process().cpu_affinity(cores)
       torch.set_num_threads(n)
   _pin_to_safe_cores()
   ```
2. Document the BSOD history in `memory/project_hardware_crash_log.md` — APIC IDs that produced WHEA parity errors, date, workload.
3. Verify pin took effect: `psutil.Process().cpu_affinity()` should return `[0, 2, 4, 6]`.
4. If on a non-hybrid CPU, still set explicit `cpu_affinity` to ≤ 50% of physical cores — leaves headroom for OS + GPU feeder threads.

## References

- Source: `autoresearch/CLAUDE.md` section "Hardware Constraints (MANDATORY)"
- Source: `autoresearchindexspy/autoresearchspy/CLAUDE.md` section "Hardware Constraints (MANDATORY)"
- WHEA-Logger Event ID 18 (Internal Parity Error) — Microsoft KB.
- Intel 14th-gen P/E-core scheduling guidance — Intel Thread Director technical brief.
