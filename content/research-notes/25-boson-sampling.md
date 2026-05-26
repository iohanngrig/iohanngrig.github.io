---
title: "Boson sampling and photonic quantum advantage"
date: 2026-04-18
description: "The Aaronson-Arkhipov 2011 proposal, Jiuzhang 2020 experiment, and why sampling-based supremacy has held up better than circuit-based supremacy."
tags: [research-notes, quantum-computing, photonics, supremacy]
draft: false
---

The most defensible quantum advantage experiment yet performed does not run an algorithm. Boson sampling generates random outputs from an optical interferometer; the task is to produce samples from a particular probability distribution. Aaronson and Arkhipov proved in 2011 that if classical computers could efficiently simulate this sampling, the polynomial hierarchy would collapse to the third level, a consequence few complexity theorists would accept. USTC's Jiuzhang platform has demonstrated this in hardware, and unlike the Sycamore circuits, no classical attack has come close to collapsing the claim.

## The task

A linear optical setup with $n$ identical indistinguishable photons sent through an $m$-mode interferometer (with $m = \Omega(n^2)$) produces a distribution over $\binom{m}{n}$ output configurations. The probability of a given output $S$ is

$$
P(S) = \frac{|\text{Perm}(U_S)|^2}{s_1! \cdots s_m!}
\qquad (1)
$$

where $U_S$ is an $n \times n$ submatrix of the scattering unitary $U$ and $\text{Perm}$ is the matrix permanent.

The classical-hardness argument: **computing the permanent is $\#\text{P}$-hard** (Valiant 1979). Exact sampling from (1) would let you approximate permanents of arbitrary complex matrices. Under reasonable conjectures about the average-case complexity of permanents, this implies classical computers cannot simulate boson sampling even approximately.

## The Aaronson-Arkhipov conjectures

Their proof relies on two conjectures:
- **Permanent-of-Gaussians conjecture**: Approximating the permanent of a matrix of Gaussian entries is $\#\text{P}$-hard on average.
- **Anti-concentration conjecture**: The distribution of $|\text{Perm}(X)|^2$ for Gaussian $X$ is not too concentrated near the mean.

Both remain open problems in complexity theory, but widely believed.

## Hardware demonstrations

**Zhong et al. 2020, Science 370** [2], Jiuzhang. 100-mode interferometer, 50 single-mode squeezed input states, up to 76 photon clicks. Measured sampling rate 10^{14} times faster than state-of-the-art classical simulation. This was published alongside supporting classical complexity analysis, and has held up to subsequent classical simulation attempts better than Sycamore RCS.

**Liu et al. 2025**, Jiuzhang 4.0. 8176 modes, 3050 photon detection events. Classical simulation (matrix product state method on El Capitan supercomputer) estimated at $>10^{42}$ years. A quantum sample takes 25.6 μs.

The critical difference from RCS: photon loss in boson sampling is an **asymmetric** error, it reduces output signal but doesn't produce wrong answers. Sycamore circuits accumulate all forms of noise (bit-flips, phase errors, leakage) which mimic "anti-concentration" and can mimic the structure of an honest quantum sample, making classical spoofing more feasible.

## What boson sampling does not do

Boson sampling is not programmable. Each Jiuzhang run samples from a distribution determined by the interferometer's optical-element settings; there is no general-purpose algorithm. It is a **one-shot complexity demonstration**, not a quantum computer.

Recent efforts (Gaussian Boson Sampling with programmable phase shifters) are introducing some programmability, but the task remains specialized to problems that map to permanent computation. Graph-theoretic problems (e.g., dense-subgraph search) have been shown to reduce to GBS, providing a narrow application domain.

## Educational value

Boson sampling taught the quantum computing community a crucial lesson: **proving hardness from complexity assumptions is a viable strategy, not just an asymptotic curiosity**. The Jiuzhang results have survived classical counterattacks in a way Sycamore results have not, because the complexity assumptions underlying boson sampling are tighter than those underlying RCS. This has influenced subsequent supremacy experiments (e.g., IQP sampling, DQC1 sampling).

## References

[1] Aaronson, S., Arkhipov, A. (2011). *The Computational Complexity of Linear Optics*. STOC 2011, 333–342. Expanded: *Theory of Computing* 9(4), 143–252 (2013).

[2] Zhong, H.-S., Wang, H., Deng, Y.-H., et al. (2020). *Quantum computational advantage using photons*. Science 370(6523), 1460–1463.

[3] Liu, H.-L., Su, H.-R., Gong, S.-Q., et al. (2025). *Robust quantum computational advantage with programmable 3050-photon Gaussian boson sampling*. [preprint]

[4] Clifford, P., Clifford, R. (2017). *The Classical Complexity of Boson Sampling*. SODA 2018, 146–155.

