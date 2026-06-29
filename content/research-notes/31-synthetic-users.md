---
title: "How far synthetic users can take you: validity ceilings and a screening test"
date: 2026-06-28
draft: false
tags: ["llm-agents", "synthetic-users", "evaluation", "experimentation"]
---

# How far synthetic users can take you: validity ceilings and a screening test

> "Silicon samples", LLM agents conditioned to imitate a population, are increasingly proposed to pre-test communications, incentives, and product flows before a live experiment. The literature is split: some report agents reproducing individual human responses at high rates, others document moderate-at-best correlations and minority-opinion collapse. The useful question is not "do they work?" but "for *this* decision, with *this* grounding, how much can I trust the synthetic result, and when should I just run the real test?" Three results turn that into a measured, checkable answer, and the answer is that synthetic users are a calibrated screening instrument, not a substitute for human research.

## 1. A validity ceiling you cannot prompt your way past

Let $\rho_{tt} \in (0,1)$ be the human test-retest reliability of the outcome, the correlation between the same person's answer on two occasions. A predictor correlates with a *noisy* human measurement only through the shared true-score component, so by the attenuation argument its correlation with the observed response is capped:

$$
\rho_{ah} \;\le\; \sqrt{\rho_{tt}} \;<\; 1, \qquad \text{equivalently} \qquad \rho_{ah}^2 \;\le\; \rho_{tt}.
$$

The consequence is uncomfortable and worth internalizing: **no amount of personas, samples, or prompt engineering raises fidelity above this ceiling, which is set by the outcome's own reliability, not by effort.** With a literature-typical $\rho_{tt}\approx 0.7$ the ceiling is $\sqrt{0.7}\approx 0.84$, and grounding imperfection pulls realized fidelity well below it, into the $\approx 0.4$–$0.6$ range reported for typology- and trace-grounded panels. Fidelity is a property of the outcome and the grounding, not of effort.

## 2. Synthetic panels under-state effect sizes, and your sample size is smaller than it looks

Let $\eta = \mathrm{Var}_{\text{agent}}/\mathrm{Var}_{\text{human}} \in (0,1]$ be the variance fidelity. The synthetic panel's minimum detectable effect, expressed in true-human units, is

$$
\Delta_{\text{MDE}}^{\text{real}} \;=\; \frac{(z_{1-\alpha} + z_{1-\beta})\,\sigma_h\sqrt{2/n}}{\sqrt{\eta}}.
$$

Because $\eta < 1$, the real MDE is inflated by $1/\sqrt\eta$: a synthetic effect of size $\Delta_s$ corresponds to a *larger* true effect $\approx \Delta_s/\sqrt\eta$. This assumes $\eta$ acts as a regression-dilution factor, the synthetic panel compresses the response *scale* by $\sqrt\eta$ while its residual dispersion stays at human scale; a pure variance reduction with no scale compression would not carry this penalty. Under that coupling, synthetic panels systematically under-state effects.

The load-bearing practical caveat is the effective sample size. The independent unit is the **persona**, not the stochastic sample. Drawing $M$ samples from each of $K$ personas does not give $KM$ independent observations, because within-persona samples share the same conditioning. So the effective sample size lies between $K$ and $KM$ and collapses toward $K$ as within-persona responses become highly correlated; reporting power as if $n = KM$ can overstate confidence by up to $\sqrt M$. More samples per persona tighten a within-persona estimate; they buy little new information about the population.

## 3. A fidelity floor that says when to trust the panel

The panel is usually used to keep or kill an idea. Model the keep/kill statistic as Gaussian with a mean proportional to $\rho_{ah}\sqrt\eta\,\Delta_h$ and a standard deviation proportional to $\sigma_s/\sqrt K$. To hold a false-keep rate $\le \gamma_0$ and a false-kill rate $\le \gamma_1$ at a true effect $\Delta_h$, a usable threshold exists **iff**

$$
\rho_{ah}\,\sqrt{\tfrac{\eta K}{2}}\;\frac{\Delta_h}{\sigma_h} \;\ge\; z_{1-\gamma_0} + z_{1-\gamma_1}.
$$

Equivalently there is a **fidelity floor** $\rho_{\min} = (z_{1-\gamma_0}+z_{1-\gamma_1})\,\sigma_h \,/\, \big(\Delta_h\sqrt{\eta K/2}\big)$: below it, no threshold meets both error targets and the panel adds nothing over the prior. This is the decision-theoretic heart of the matter. It converts "are synthetic users good enough?" into a checkable inequality in measured quantities, $\rho_{ah}$ (from held-out validation), $\eta$, $K$, and the effect size $\Delta_h/\sigma_h$ the decision actually cares about.

## 4. A protocol that respects the bounds

* **Calibrate** $\rho_{ah}$ and $\eta$ on held-out human traces, per task, and publish the numbers. Fidelity does not transfer across tasks.
* **Report** the variance-corrected MDE with $n_{\text{eff}} = K$, never $KM$.
* **Gate** every decision by the floor: if $\rho_{ah} < \rho_{\min}$, the panel returns "insufficient fidelity, run the live test," not a verdict.
* **Raise fidelity** where possible by grounding on real behavioural traces rather than prompt-only conditioning, and validate the lift against held-out data rather than asserting it.

## 5. Where this is fragile

* **The Gaussian, linear-attenuation model is optimistic.** Heavy-tailed or task-specific biases, social-desirability effects, minority-opinion collapse, all *lower* effective fidelity, so the floor in Section 3 is a best case, not a guarantee.
* **$\rho_{tt}$ is often unknown.** When the outcome's own reliability has not been measured, $\rho_{ah}$ must be bounded by direct held-out validation, not by the decomposition in Section 1.
* **It bounds screening value, not research value.** The framework licenses synthetic panels as a pre-experimental filter; it does not license them as a replacement for qualitative human research, and the floor gate is what enforces that.
* **Scope and ethics.** Persona steering belongs to defensive screening of an organization's own ideas. Modelling or persuading real, identified individuals is out of scope.

## 6. What synthetic users are actually good for

Synthetic users are neither the revolution nor the fraud the two camps describe. They are an instrument with a measurable precision: a ceiling set by human reliability, a scale that compresses effects, and an information content bounded by the number of independent personas. Used as a filter with a published validity score and a floor that defers to a live test when fidelity is too low, they save real experiments. Used as a substitute for them, they launder a prior into a number.

## References

* Park, J. S., Zou, C. Q., Shaw, A., et al. (2024). *Generative agent simulations of 1,000 people.* NeurIPS.
* Argyle, L. P., Busby, E. C., Fulda, N., Gubler, J. R., Rytting, C., & Wingate, D. (2023). *Out of one, many: using language models to simulate human samples.* Political Analysis, 31(3).
* Bisbee, J., Clinton, J., Dorff, C., Kenkel, B., & Larson, J. (2024). *Synthetic replacements for human survey data? The perils of large language models.* Political Analysis.
* Spearman, C. (1904). *The proof and measurement of association between two things.* American Journal of Psychology, 15(1).
* Cohen, J. (1988). *Statistical power analysis for the behavioral sciences.* 2nd ed., Lawrence Erlbaum.

*This is an exposition of public results and a decision framework; it uses public persona/behaviour benchmarks and no proprietary data.*
