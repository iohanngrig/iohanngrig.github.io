---
title: "Quantum error correction and the fault-tolerance threshold"
date: 2026-04-12
description: "Why quantum computers need error correction, how the surface code and threshold theorem work, and why 'just add more qubits' is an underestimate by three orders of magnitude."
tags: [research-notes, quantum-computing, error-correction]
draft: false
---

The arithmetic is stark: current superconducting qubits have physical error rates around $10^{-3}$ per gate. Shor-on-RSA-2048 needs about $10^{10}$ operations. Multiply those and every candidate output is vaporized by noise before the algorithm finishes. Quantum error correction is not a polish step, it is a roughly thousand-to-one qubit multiplier that every useful quantum computation is eventually going to need.

## Why QEC is harder than classical ECC

Classical error correction repeats bits: send $000$, decode majority. This works because bits are discrete. Quantum states are continuous, a qubit lives on the Bloch sphere and can decohere in infinitely many ways.

Worse, the no-cloning theorem forbids $|\psi\rangle \to |\psi\rangle |\psi\rangle$. You cannot make backup copies.

**Shor 1995** [1] and **Steane 1996** [2] showed that QEC is nevertheless possible by encoding one logical qubit into many physical qubits and measuring *syndrome operators*, commuting observables that detect errors without collapsing the encoded state.

## The threshold theorem

**Aharonov-Ben-Or, Kitaev, Knill-Laflamme-Zurek 1996–1997** [3]: if physical-gate error $p$ is below a threshold $p_{th}$, arbitrary-length quantum computations can be performed at logical error rate $p_L = (p/p_{th})^{d/2}$ using a distance-$d$ code, with polynomial overhead.

For the surface code, $p_{th} \approx 10^{-2}$ in theoretical analyses [4], $\approx 10^{-3}$ in realistic circuit-level noise models. Current superconducting qubits (Google Willow 2024) achieve per-gate error $\sim 10^{-3}$, right at the threshold, which is why "distance-3, distance-5, distance-7 surface codes" are the topic of current experiments.

## Surface code overhead

For a logical qubit to sustain computation of depth $T$ operations at failure probability $\le \varepsilon$, we need a surface-code distance $d$ such that

$$
p_L T \le \varepsilon \implies d \ge 2 \frac{\log(T/\varepsilon)}{\log(p_{th}/p)}.
\qquad (1)
$$

Each logical qubit requires $\sim d^2 \cdot k$ physical qubits (where $k$ is a small constant). For $T = 10^6$ (megaquop), $p = 10^{-3}$, $p_{th} = 10^{-2}$, $\varepsilon = 10^{-2}$:

$$
d \gtrsim 2 \frac{\log(10^8)}{\log(10)} = 16 \implies \text{physical qubits per logical} \approx 500-1000.
$$

For Shor on RSA-2048, **Gidney-Ekerå 2021** [5] arrived at $\sim 20$ million physical qubits. This is three to four orders of magnitude more than 2026-era hardware.

## The Megaquop roadmap

**Preskill 2025** [6] named the next milestone: a machine executing $\ge 10^6$ logical operations reliably. Recent results:
- **Google Willow 2024** demonstrated below-threshold error correction at distance-5 and distance-7, with logical error rate decreasing as distance increases, the first *scalable* QEC demonstration.
- **Quantinuum H2 2024** demonstrated 56-qubit trapped-ion devices with 99.99% two-qubit gate fidelity, far exceeding the threshold.
- **IBM Heron 2024** (133 qubits) targets error-rate reduction to enable early QEC.

The Megaquop milestone is credibly 5-10 years away, conditional on continued progress. The CRQC milestone (Shor-capable) is likely 10-20 years.

## What this means for algorithms

1. **NISQ algorithms (VQE, QAOA, basic quantum simulation) will need to produce useful results in the "early FT" window** when only dozens of logical qubits are available. Most published NISQ demonstrations will not survive the transition.
2. **Shor, HHL, quantum simulation of large molecules need full FT**, and timelines for those are longer.
3. **Error correction research itself is the bottleneck.** Improvements in code efficiency (e.g., LDPC codes with better rate) and decoder algorithms (neural decoders, real-time classical processing) have high marginal value.

## Good-to-know bounds

- **Knill-Laflamme conditions**, a code corrects a set of errors $\{E_a\}$ iff $\langle i_L | E_a^\dagger E_b | j_L \rangle = c_{ab} \delta_{ij}$ for some Hermitian $c$. The foundation of all QEC design.
- **Eastin-Knill theorem 2009**, no QEC code can have a universal transversal gate set. Implication: non-Clifford gates (e.g., $T$ gate) require "magic state distillation," a large fraction of surface-code overhead.
- **Quantum LDPC codes.** The hypergraph-product construction (Tillich-Zémor) achieves $k d^2 \le O(n^2)$ (for example $k=\Theta(n)$, $d=\Theta(\sqrt n)$). This is *not* a fundamental limit: asymptotically good qLDPC codes with constant rate $k=\Theta(n)$ **and** linear distance $d=\Theta(n)$ were constructed in 2022 (Panteleev-Kalachev lifted-product codes; quantum Tanner codes), resolving the qLDPC conjecture and enabling far lower fault-tolerance overhead than the surface code.

## References

[1] Shor, P. W. (1995). *Scheme for reducing decoherence in quantum computer memory*. Phys. Rev. A 52, R2493.

[2] Steane, A. M. (1996). *Error Correcting Codes in Quantum Theory*. Phys. Rev. Lett. 77, 793.

[3] Aharonov, D., Ben-Or, M. (1997). *Fault-Tolerant Quantum Computation With Constant Error Rate*. SIAM J. Comput. 38(4), 1207. Kitaev, A. Y. (1997). *Quantum computations: algorithms and error correction*. Russ. Math. Surv. 52, 1191.

[4] Fowler, A. G., Mariantoni, M., Martinis, J. M., Cleland, A. N. (2012). *Surface codes: Towards practical large-scale quantum computation*. Phys. Rev. A 86, 032324.

[5] Gidney, C., Ekerå, M. (2021). *How to factor 2048-bit RSA integers in 8 hours using 20 million noisy qubits*. Quantum 5, 433.

[6] Preskill, J. (2025). *Beyond NISQ: The Megaquop Machine*. ACM Trans. Quantum Comput. 6(3).

