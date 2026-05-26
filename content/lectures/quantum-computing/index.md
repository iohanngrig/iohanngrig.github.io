---
title: Lectures on quantum computing
description: "A three-chapter series on quantum algorithms, optimization, machine-learning applications, and the limits of quantum advantage."
---

# Lectures on quantum computing

Three chapters at graduate level. The thread throughout: separating provable quantum speedup from heuristic promise, and separating hardware demonstrations from useful computation.

*Target reader: graduate student or research scientist with basic quantum mechanics (Hilbert space, unitary evolution, measurement) and some linear algebra. The mathematical prerequisites are lighter than the causal-inference series; the complexity-theoretic discussion is the hardest part.*

---

## [Chapter 1 · Quantum optimization and supremacy claims](/lectures/quantum-computing/quantum-optimization-and-supremacy)

QUBO and Ising formulations. Adiabatic quantum computation and the gap bottleneck. QAOA and its $p=1$ bound on 3-regular Max-Cut. NISQ hardware reality: the Harrigan/Arute 2020 result showing QAOA loses to efficient classical algorithms on non-native graphs. Supremacy claims from Google Sycamore and USTC Jiuzhang, and their classical counterattacks.

## [Chapter 2 · Quantum algorithms with provable speedup](/lectures/quantum-computing/quantum-algorithms)

Shor's exponential factoring. Grover's quadratic search and the BBBV optimality lower bound. HHL linear systems and Aaronson's fine-print criteria. A summary table of provable speedups by problem class.

## [Chapter 3 · Quantum machine learning, limits and honest prospects](/lectures/quantum-computing/quantum-ml-limits)

VQE and the barren-plateau result (McClean et al. 2018). Quantum Monte Carlo and amplitude estimation. BQP and the complexity landscape. Tang's dequantization program. The error-correction horizon and what the 2030s realistically look like.

---

Related shorter notes on quantum topics are in the [research notes library](/research-notes/), including companion discussions of boson sampling, quantum annealing (D-Wave), quantum error correction, and Bayesian perspectives on quantum state preparation.
