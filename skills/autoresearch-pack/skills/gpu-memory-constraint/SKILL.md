---
name: gpu-memory-constraint
description: GPU memory constraint — 16 GB VRAM hard cap, pre-flight check for every backbone, parameter ceilings by training mode, BF16/gradient-checkpointing/LoRA escape hatches. Triggers on "VRAM", "GPU memory", "OOM", "16 GB", "BF16", "gradient checkpointing", "LoRA", "PEFT".
metadata:
  category: engineering
  source: autoresearch
  related: [per-backbone-sota-recipes, per-backbone-experiment-mandate]
---

# GPU Memory Constraint (16 GB VRAM hard cap)

## When to use

- Before launching Experiment 1 on any new backbone.
- After OOM on a previously-fitting model — your bs/seq/precision changed.
- When considering a foundation model > 100M params — apply the size-class rule.

## The rule

> ### GPU Memory Constraint (MANDATORY — 16 GB VRAM hard cap)
>
> **This laptop has 16 GB of GPU VRAM. Every backbone selection, every experiment, every fine-tuning run MUST fit within this budget with headroom. A model that OOMs mid-training is not a valid experiment — it's a wasted GPU cycle and a crash risk.**
>
> **Memory budget breakdown (16 GB total):**
>
> | Component | Budget | Notes |
> |-----------|--------|-------|
> | Model parameters | ≤ 3 GB | FP32 weights; BF16/FP16 halves this |
> | Optimizer state (AdamW) | ≤ 6 GB | Adam stores 2 moments at FP32 even with BF16 weights → ≈ 2× param size |
> | Gradients | ≤ 3 GB | Same size as params; freed after step |
> | Activations | ≤ 3 GB | batch × seq × hidden, scales with bs and depth |
> | Reserved / fragmentation | ≥ 1 GB | PyTorch caching allocator overhead |
>
> **Practical parameter ceilings by training mode:**
>
> | Training mode | Max params @ FP32 | Max params @ BF16/FP16 | Max params w/ grad-ckpt + BF16 |
> |---------------|-------------------|------------------------|-------------------------------|
> | From-scratch train (Adam full states) | ~500 M | ~1.0 B | ~2.0 B |
> | Full fine-tune | ~500 M | ~1.0 B | ~2.0 B |
> | Parameter-efficient FT (LoRA r=8, adapter-only) | ~1.0 B | ~3.0 B | ~5.0 B |
> | Frozen-backbone head-only FT | ~1.5 B | ~4.0 B | ~7.0 B |
> | Inference only (no grads) | ~4.0 B | ~8.0 B | ~8.0 B |
>
> **Rules by backbone size class:**
>
> 1. **< 100 M params** — safe for anything. Use FP32 defaults.
> 2. **100 M – 500 M params** — FROM-SCRATCH TRAIN OK in FP32 at bs=32. Measure GPU use on Experiment 1; if > 12 GB, drop batch to 16 and/or switch to BF16.
> 3. **500 M – 2 B params** — FROM-SCRATCH not viable. Use: (a) parameter-efficient fine-tuning (LoRA/adapters), OR (b) frozen backbone + trainable head, OR (c) zero-shot inference then distil into a smaller student.
> 4. **> 2 B params** — INFERENCE ONLY. Use zero-shot forecasting, cache predictions, never train.
>
> **Mandatory pre-flight check for any new backbone:**
>
> Before launching Experiment 1 on ANY new backbone, run this check (in reasoning annotation):
>
> ```
> Measured/estimated size: N million params
> Training mode selected: [from-scratch | LoRA fine-tune | head-only FT | zero-shot]
> Expected peak VRAM: <X> GB at bs=<Y>, seq=<Z>, precision=<FP32|BF16>
> Headroom vs 16 GB: <16 - X> GB
> Fallback plan if OOM: [reduce bs to 16 | switch to BF16 | gradient checkpointing | adapter-only]
> ```
>
> Without this entry, Experiment 1 does not launch. The same check applies any time we change batch size or sequence length during a backbone's 50-experiment cycle.

### Size-class annotations for Tier-2 backbones

| Backbone | Approx size | Training mode fit in 16 GB |
|----------|------------|-----------------------------|
| timesfm-200m (small) | 200 M | from-scratch fine-tune OK at BF16 |
| timesfm-2.5 (500 M) | 500 M | PEFT or head-only FT; full fine-tune risky |
| chronos-bolt-small | 9 M | trivially fits |
| chronos-bolt-base | 48 M | trivially fits |
| chronos-bolt-large | 205 M | fine-tune fits in FP32 |
| chronos-t5-large | 700 M | PEFT only |
| moirai-small/base | 14 M / 91 M | fits, from-scratch OK |
| moirai-large / moirai 2.0 | 311 M / ~500 M | fine-tune at BF16 |
| moment-small / base / large | 40 M / 125 M / 385 M | all fit; large at BF16 |
| tirex | ~300 M (est.) | fine-tune at BF16 |
| sundial | 500 M – 1 B (est.) | PEFT only |
| time-moe-base / large | 113 M / 453 M | fits; large at BF16 |
| timemixer / timesnet / mambats | < 50 M each | trivially fits |

### Default protocol when adopting a new foundation model

1. Start with the SMALLEST published checkpoint of that family (e.g. Chronos-Bolt-small, Moirai-small, MOMENT-small).
2. Run zero-shot first — measure composite without any training. Pay only inference cost.
3. If zero-shot is promising, fine-tune (full or PEFT depending on size).
4. Scale up to larger checkpoint ONLY if smaller shows signal AND the memory math works.

### BF16 + gradient-checkpointing notes

- **BF16:** safer mixed-precision choice vs FP16 on RTX-class GPUs — keeps dynamic range without loss-scaling. Use `torch.autocast(dtype=torch.bfloat16)` + `GradScaler` unset. Measure before/after; some ops (LayerNorm, GroupNorm) should stay FP32.
- **Gradient checkpointing:** Use `torch.utils.checkpoint.checkpoint_sequential` for any model > 200 M params being fine-tuned. Costs ~30% more FLOPs but cuts activation memory by 70-80%, unlocking bs=32 at 500 M-1 B params.

## Anti-patterns

- **Skipping the pre-flight VRAM math.** OOM mid-training wastes the wall-clock cost and destabilises the GPU driver.
- **Switching to FP16 instead of BF16 on RTX.** FP16 needs loss-scaling and risks overflow; BF16 is the safer pick.
- **Full fine-tune of a 700M-param model with AdamW.** Optimizer state alone exceeds 11 GB — go LoRA or head-only.
- **Estimating VRAM without measuring.** First-experiment VRAM is data; future budget decisions rely on it.
- **Increasing bs without rerunning the VRAM check.** A bs=16→32 doubles activation memory.

## Implementation checklist

1. Pre-flight block in reasoning annotation for Experiment 1 of each new backbone (5 lines: size, mode, expected VRAM, headroom, fallback).
2. Measure peak VRAM via `torch.cuda.max_memory_allocated()` at end of Exp 1; log to JSONL.
3. If headroom < 2 GB, drop bs or switch precision BEFORE Exp 2.
4. Gradient checkpointing on by default for any FT of > 200M params.
5. Foundation-model adoption follows the "smallest first → zero-shot → fine-tune → scale" sequence.

## References

- Source: `autoresearch/CLAUDE.md` section "GPU Memory Constraint (MANDATORY — 16 GB VRAM hard cap)"
- Kaplan et al. (2020) "Scaling Laws for Neural Language Models" — parameter scaling heuristics.
- Hu et al. (2022) "LoRA: Low-Rank Adaptation of Large Language Models" — adapter-only FT.
- PyTorch docs: `torch.utils.checkpoint`, `torch.autocast(dtype=torch.bfloat16)`.
- Related: `per-backbone-sota-recipes`, `per-backbone-experiment-mandate`.
