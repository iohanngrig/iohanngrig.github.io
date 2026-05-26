---
title: "Adiabatic theorem and gap scaling"
date: 2026-03-22
description: "Why the adiabatic theorem is quantum computing's favorite sword, and where its blade gets dull. Gap scaling, Landau-Zener transitions, first-order phase transitions, and why worst-case 3-SAT defeats it."
tags: [research-notes, quantum-computing, adiabatic]
draft: false
---

Quantum systems are reluctant to leave their ground state. That single physical fact, proved by Born and Fock in 1928 and sharpened across the following century, is what makes *adiabatic quantum computation* possible and what places its limits.

## The theorem

If a Hamiltonian $H(s)$, $s \in [0,1]$, has spectral gap $\Delta(s)$ between its ground state and first excited state, then evolution that interpolates from $H(0)$ to $H(1)$ over time $T$ keeps the state close to the instantaneous ground state provided

$$
T \gg \max_s \frac{\|\dot H(s)\|}{\Delta(s)^2}.
\qquad (1)
$$

A more rigorous form, due to Jansen-Ruskai-Seiler [3], involves second-derivative terms and gives the error as $\varepsilon = O(1/T\Delta^2)$ under a gap condition. The essential message is unchanged: **runtime scales inversely with the square of the minimum gap**.

## Where the gap closes

For an interpolation $H(s) = (1-s) H_B + s H_C$, the ground-state gap $\Delta(s)$ generically reaches a minimum at some intermediate $s^*$. Three regimes:

1. **Polynomially small minimum gap**, $\Delta_{\min} = \Omega(1/\text{poly}(n))$. Runtime is polynomial. This is the *good case*.
2. **Exponentially small minimum gap at a second-order phase transition**, $\Delta_{\min} \sim 2^{-\alpha \sqrt{n}}$ or similar. Runtime is exponential.
3. **First-order quantum phase transitions**, gap closes as $\Delta_{\min} \sim 2^{-\alpha n}$ (exponentially small in system size). Runtime is exponential and the problem is effectively unsolvable by adiabatic evolution.

**Altshuler-Krovi-Roland 2010** [4] showed that random instances of 3-SAT generically exhibit first-order transitions with $\Delta_{\min} \sim 2^{-\alpha n}$ in the worst case. The adiabatic algorithm is therefore not a silver bullet for NP-hard problems.

## Landau-Zener, the two-level prototype

To build intuition, consider a two-level system with Hamiltonian

$$
H(t) = \begin{pmatrix} vt & \Delta/2 \\ \Delta/2 & -vt \end{pmatrix}.
$$

At $t \to -\infty$, the ground state is $(0,1)$; at $t \to +\infty$, it is $(1,0)$. The **Landau-Zener** formula [5] gives the probability of diabatic transition (staying in the original state rather than the ground state):

$$
P_{\text{diabatic}} = \exp\left(-\frac{\pi \Delta^2}{2 \hbar v}\right).
$$

For adiabatic evolution ($P_{\text{diabatic}} \to 0$), we need $v \ll \Delta^2$, i.e., the sweep rate must be small compared to the gap squared. This is the microscopic version of (1).

## Equivalence to gate-model quantum computation

**Aharonov, van Dam, Kempe, Landau, Lloyd, Regev 2007** [6] proved adiabatic quantum computation is polynomially equivalent to the standard gate model. Consequently, any circuit can be simulated adiabatically with polynomial overhead; and any adiabatic computation can be compiled into a gate-model circuit. The two models are computationally interchangeable, so upper and lower bounds translate freely between them.

## Why adiabatic is *not* obviously better than classical

Even with an arbitrarily slow evolution, the adiabatic algorithm returns the ground state, which is the optimum. So if the gap is polynomial, we have a polynomial-time quantum algorithm for an NP-hard problem. Why doesn't this prove $\text{NP} \subseteq \text{BQP}$?

Because on worst-case hard instances, the gap is *not* polynomial. Farhi et al. 2002 and subsequent work showed that on carefully-constructed hard instances (crafted to have first-order transitions), the adiabatic algorithm fails. Classical heuristics (simulated annealing, branch and bound) may have similar worst-case blowups, but the adiabatic algorithm has no proven advantage over classical on the worst case.

For structured problems with polynomial gaps, physics problems, quantum chemistry, some engineered optimization instances, the adiabatic algorithm can be efficient. But it does not provide a general NP-hard solver.

## References

[1] Born, M., Fock, V. (1928). *Beweis des Adiabatensatzes*. Zeitschrift für Physik 51, 165–180.

[2] Farhi, E., Goldstone, J., Gutmann, S., Sipser, M. (2000). *Quantum Computation by Adiabatic Evolution*. [arXiv:quant-ph/0001106](https://arxiv.org/abs/quant-ph/0001106)

[3] Jansen, S., Ruskai, M.-B., Seiler, R. (2007). *Bounds for the adiabatic approximation with applications to quantum computation*. J. Math. Phys. 48, 102111.

[4] Altshuler, B., Krovi, H., Roland, J. (2010). *Anderson localization makes adiabatic quantum optimization fail*. PNAS 107(28), 12446–12450.

[5] Zener, C. (1932). *Non-Adiabatic Crossing of Energy Levels*. Proc. Royal Soc. London A 137(833), 696–702.

[6] Aharonov, D., van Dam, W., Kempe, J., Landau, Z., Lloyd, S., Regev, O. (2007). *Adiabatic Quantum Computation Is Equivalent to Standard Quantum Computation*. SIAM J. Comput. 37(1), 166–194.

