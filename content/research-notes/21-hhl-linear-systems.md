---
title: "HHL and quantum linear systems, where the small print matters"
date: 2026-04-04
description: "The Harrow-Hassidim-Lloyd algorithm and why its advertised exponential speedup collapses under realistic input/output assumptions."
tags: [research-notes, quantum-computing, linear-algebra]
draft: false
---

Few quantum algorithms have an asterisk next to every line of their performance sheet quite like HHL. The headline is striking: solve $A\vec x = \vec b$ for sparse, well-conditioned $A$ in time polylogarithmic in the problem dimension. The fine print is more striking: you need the input as a quantum state, you cannot read the output as a classical vector, and the condition number can shred the speedup. What's left, once you read the fine print, determines whether HHL is a billion-dollar industrial algorithm or a mathematical curiosity.

## The algorithm, briefly

The HHL procedure uses quantum phase estimation to diagonalize $A$ in the eigenbasis, rotates by $1/\lambda$ for each eigenvalue, and inverse-phase-estimates. The output is the state $|x\rangle = A^{-1}|b\rangle / \|A^{-1}|b\rangle\|$ within precision $\varepsilon$.

The running time depends on:
- $\kappa$ = condition number of $A$
- $N$ = dimension (exponential in qubit count)
- $s$ = sparsity (rows with $O(s)$ non-zeros)
- $\varepsilon$ = precision

The final state is quantum, a vector in Hilbert space. Measuring it gives one classical sample per run, and the amplitudes themselves are not efficiently read out.

## The three small-print clauses

**Clause 1: State preparation.** HHL requires $|b\rangle$ already prepared as a quantum state. If $b$ is a classical vector with $N = 2^n$ entries, preparing $|b\rangle$ in general takes $\Omega(N)$ time, erasing the claimed exponential speedup. Only if $b$ can be quantum-prepared from an efficient quantum circuit (e.g., it arises from a physics simulation, or is stored in QRAM) does the input cost not dominate.

**Clause 2: Output extraction.** We get the state $|x\rangle$, not its classical entries. Extracting a single entry $x_j$ would require amplitude estimation with precision $\varepsilon$, taking $\Omega(1/\varepsilon)$ measurements. Computing all $N$ entries takes $\Omega(N)$, again erasing exponential speedup.

**Clause 3: Condition number.** If $\kappa = \Omega(N)$, the algorithm is no faster than classical. Real-world matrices often have poor conditioning; preconditioners help classically but not always quantumly.

## The Aaronson litmus test

**Aaronson 2015** [2] articulated the four conditions for HHL to provide genuine speedup:
1. $|b\rangle$ must be efficiently quantum-preparable.
2. $A$ must be efficiently quantum-accessible (e.g., sparse and row-accessible, or stored in QRAM).
3. Only global properties of $|x\rangle$ are wanted (not individual entries).
4. The condition number $\kappa$ must be polylogarithmic or polynomial in interesting parameters.

When all four hold, HHL is efficient and classical conjugate gradient is not. Such settings exist (differential equations with structured sources, machine learning inner loops with implicit matrices) but are rare in practice.

## Dequantization via Tang

**Tang 2018** [3] introduced classical $\ell_2$-norm sampling access as a classical analog of QRAM. Under this access model, many "exponentially faster" quantum linear-algebra subroutines (recommender systems, SVMs, PCA) become classically efficient with polynomial overhead. HHL itself has partial dequantization under related assumptions [4].

The Tang result was not a "quantum computing doesn't work" finding. It was: *the claimed exponential speedups assumed a quantum-favored input format*. If classical and quantum are put on even input footing, some speedups evaporate.

## Hardware prospects

HHL on current NISQ hardware has been demonstrated for $2 \times 2$ systems [5]. Scaling to $N \sim 10^6$ (the regime where HHL would be useful) requires error correction. **Preskill 2025** [6] lists HHL among the applications of interest for the coming Megaquop machine era, alongside chemistry, materials science, and selected ML routines.

## References

[1] Harrow, A. W., Hassidim, A., Lloyd, S. (2009). *Quantum Algorithm for Linear Systems of Equations*. Phys. Rev. Lett. 103, 150502.

[2] Aaronson, S. (2015). *Read the fine print*. Nature Physics 11, 291–293.

[3] Tang, E. (2018/2019). *A quantum-inspired classical algorithm for recommendation systems*. STOC 2019, 217–228.

[4] Gilyén, A., Song, Z., Tang, E. (2022). *An improved quantum-inspired algorithm for linear regression*. Quantum 6, 754.

[5] Zaman, A., Wong, H. (2022). *Study of Error Propagation in HHL*. IEEE LAEDC 2022.

[6] Preskill, J. (2025). *Beyond NISQ: The Megaquop Machine*. ACM Trans. Quantum Comput.

