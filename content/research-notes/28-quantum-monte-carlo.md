---
title: "Quantum Monte Carlo and amplitude-estimation speedups"
date: 2026-04-26
description: "Where quadratic quantum speedup applies to finance and risk: Monte Carlo estimation. The Montanaro 2015 framework, amplitude estimation as the core, and realistic NISQ prospects."
tags: [research-notes, quantum-computing, finance, monte-carlo]
draft: false
---

If you had to bet on one quantum computing application reaching Wall Street first, the smart money would be on Monte Carlo. Not chemistry, not optimization, not cryptography, Monte Carlo. The reason is unglamorous: Monte Carlo is everywhere in finance and the quantum speedup is modest (quadratic) but unusually clean. No QRAM, no barren plateaus, no dequantization, no exotic input assumptions. Montanaro proved the quadratic bound in 2015. The only thing standing between this and production is fault-tolerant hardware.

## The core tool: amplitude estimation

**Brassard-Høyer-Mosca-Tapp 2002** [2] showed how to estimate the probability $p$ of measuring $|1\rangle$ on an indicator qubit prepared by a quantum procedure $\mathcal{A}$. Classical Monte Carlo needs $O(1/\varepsilon^2)$ calls to $\mathcal{A}$. Quantum amplitude estimation needs $O(1/\varepsilon)$.

The mechanism: apply Grover-like iteration $G = \mathcal{A}(2|0\rangle\langle 0| - I)\mathcal{A}^\dagger(I - 2P)$ where $P$ is the projector onto the "good" outcome. Eigenvalue phase-estimation of $G$ yields $p$.

## Applications in finance

**Financial derivatives pricing** (options, structured products) requires averaging payoffs over thousands of Monte Carlo paths. For a derivative with payoff $f$ on underlying $X$, price is $\mathbb{E}[e^{-rT} f(X_T)]$. Classical: $O(1/\varepsilon^2)$ Monte Carlo paths. Quantum (Stamatopoulos et al. 2020 [3]): $O(1/\varepsilon)$ amplitude-estimation calls.

**Value-at-Risk, credit risk**, same structure. Expected loss estimation for portfolio VaR requires averaging indicator-of-loss over scenarios. Amplitude estimation is the natural tool.

## The noise-budget reality

Amplitude estimation uses Grover-type iteration. Its coherence time scales with $1/\varepsilon$. For a 1-basis-point accuracy ($\varepsilon = 10^{-4}$), the circuit has depth $\sim 10^4$. At NISQ per-gate error $10^{-3}$, fidelity drops below $e^{-10}$. The advertised quadratic speedup is a **fault-tolerance speedup**, not a NISQ one.

This is the same pattern as Grover (§19). NISQ demonstrations of amplitude estimation exist but for small $\varepsilon$ only; at the $\varepsilon = 10^{-3}$ scale that matters in finance, fault-tolerant hardware is needed.

## Alternatives for NISQ

**Iterative Amplitude Estimation** (Grinko et al. 2021) reduces the coherence-depth demand by trading phase-estimation for classical post-processing, enabling shorter circuits. Current experiments on NISQ hardware reach $\varepsilon \sim 10^{-2}$, useful for prototyping but not production.

## Comparison to classical variance-reduction

Classical Monte Carlo has well-developed variance-reduction techniques (control variates, importance sampling, quasi-Monte Carlo). These can reduce effective sample count by factors of 10-1000 on structured problems. A quantum quadratic speedup of 100× (say) is competitive only when classical variance reduction fails, e.g., rare-event simulation, deep-in-the-money options. The operational question: **does the financial institution care enough about the last factor of 2 to pay for a quantum computer?**

Current consensus among quant finance researchers: possibly, for specific risk-management applications (tail-event estimation, complex structured products) once error-corrected hardware arrives. For vanilla option pricing, classical methods will likely dominate for another decade.

## Honest summary

Quantum Monte Carlo is the most credible "quantum advantage for quant finance" claim. It does not require QRAM. It does not evaporate under dequantization. Its speedup is quadratic, not exponential. And it requires fault-tolerance to be practically competitive. Realistic deployment: 2030s, contingent on Megaquop-class hardware.

## References

[1] Montanaro, A. (2015). *Quantum speedup of Monte Carlo methods*. Proc. R. Soc. A 471, 20150301.

[2] Brassard, G., Høyer, P., Mosca, M., Tapp, A. (2002). *Quantum Amplitude Amplification and Estimation*. Contemp. Math. 305, 53–74.

[3] Stamatopoulos, N., Egger, D. J., Sun, Y., Zoufal, C., Iten, R., Shen, N., Woerner, S. (2020). *Option Pricing using Quantum Computers*. Quantum 4, 291.

[4] Grinko, D., Gacon, J., Zoufal, C., Woerner, S. (2021). *Iterative Quantum Amplitude Estimation*. npj Quantum Information 7, 52.

[5] Rebentrost, P., Gupt, B., Bromley, T. R. (2018). *Quantum computational finance: Monte Carlo pricing of financial derivatives*. Phys. Rev. A 98, 022321.

