---
name: heteroscedastic-loss
description: Heteroscedastic loss rules (Kendall & Gal 2017) — mean + log_variance head, aleatoric range 0.05-0.15, 50% more epochs, LR sweet-spot shifted up, monitor uncertainty per fold. Triggers on "heteroscedastic", "aleatoric", "epistemic", "log_variance", "Kendall & Gal", "uncertainty".
metadata:
  category: engineering
  source: autoresearch
  related: [traditional-ml-metrics, per-sample-decision-logging, explainability-audit-14-section]
---

# Heteroscedastic Loss Rules (Kendall & Gal 2017)

## When to use

- Adding uncertainty heads to a regression model.
- Diagnosing why an "uncertainty-aware" model isn't learning signal.
- Designing the per-fold confidence-stratified evaluation.

## The rule

> ### Heteroscedastic Loss Rules (Kendall & Gal 2017)
> - The model outputs mean + log_variance per prediction. Loss = `exp(-s) * huber(mu, y) + 0.5 * s`.
> - **Variance-branch dominance is the #1 failure mode.** If aleatoric > 0.2, the model is copping out to high variance instead of learning signal. Fix: higher LR, more epochs, or clamp log_var.
> - **Optimal aleatoric range: 0.05-0.15.** Below 0.05 = overconfident. Above 0.20 = lazy variance.
> - **The het-loss needs ~50% more epochs than plain Huber** to converge, because the variance branch adds an optimization axis. Champion with plain Huber: 20 epochs. Champion with het-loss: 30 epochs.
> - **LR sweet spot shifted up:** Plain Huber champion was lr=2e-5. Het-loss champion is lr=3e-5. The exp(-s) weighting reduces effective gradient on mean, so higher base LR compensates.
> - **Monitor uncertainty per fold:** High aleatoric on a fold means the model correctly identifies it as noisy. High epistemic means the model needs more data from that regime. Use confidence < 0.8 as a "don't trade" signal.

### When NOT to use heteroscedastic loss

The LSTM phase finding (autoresearch session learnings): "Heteroscedastic loss helps fold 2 specifically but hurts fold 1 — could be ensemble component". Het-loss isn't a strict win on every task — it's a tool whose value should be measured per-fold.

## Anti-patterns

- **Reporting only mean prediction** — the uncertainty heads are useless without per-fold aleatoric/epistemic logging.
- **`exp(s)` instead of `exp(-s)` in the loss** — the sign matters; `-s` is the precision weighting from Kendall & Gal.
- **Not clamping log_var** — early epochs can blow it to infinity. Use `log_var.clamp(-7, 7)` or similar.
- **Keeping the plain-Huber epoch budget** — het-loss needs ~50% more.
- **Treating low aleatoric as good news.** Below 0.05 the model is overconfident — calibration will be poor.

## Implementation checklist

1. Model head returns `(mu, log_var)`; loss is `exp(-log_var) * huber(mu, y) + 0.5 * log_var`.
2. Clamp `log_var` to a safe range (e.g. `[-7, 7]`).
3. Use ~1.5× the plain-Huber epoch budget; expect early-stop later in training.
4. Bump LR slightly (typical: 1.5×) to compensate for the precision weighting.
5. Log per-fold aleatoric mean, epistemic mean (via MC dropout), and confidence; verify aleatoric ∈ [0.05, 0.15].
6. Build a confidence-stratified evaluation: hit-rate per confidence decile.

## References

- Source: `autoresearch/CLAUDE.md` section "Heteroscedastic Loss Rules (Kendall & Gal 2017)"
- Kendall & Gal (2017) "What Uncertainties Do We Need in Bayesian Deep Learning for Computer Vision?" NeurIPS.
- Lakshminarayanan et al. (2017) "Simple and Scalable Predictive Uncertainty Estimation using Deep Ensembles" — alternative if het-loss underfits.
- Related: `traditional-ml-metrics`, `per-sample-decision-logging`, `explainability-audit-14-section` Section 7 (uncertainty sanity).
