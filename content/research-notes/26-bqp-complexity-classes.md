---
title: "BQP and the complexity-class zoo"
date: 2026-04-19
description: "Where BQP sits: above BPP, probably below NP in the worst case, and comfortably inside PSPACE. A tour for people who want the actual containments."
tags: [research-notes, quantum-computing, complexity]
draft: false
---

Complexity classes classify problems by the resources needed to solve them. Quantum computing introduces a new resource, coherent superposition, and with it a new class, BQP. Whether BQP is strictly larger than the classical randomized class BPP is one of the central open problems of computer science. We have Shor as strong evidence and very little else.

- **P**, solvable in polynomial time deterministically.
- **BPP**, bounded-error probabilistic polynomial time. The "tractable" class for classical computing with randomness.
- **BQP**, bounded-error quantum polynomial time. The quantum analog.
- **NP**, problems where a "yes" answer has a short classical certificate.
- **PSPACE**, problems solvable using polynomial memory.
- **#P**, counting problems (counting satisfying assignments of formulas). Polynomial hierarchy $\text{PH} \subseteq \text{P}^{\#\text{P}}$ (Toda 1991).

## Established containments

The following are proven:

$$
\text{P} \subseteq \text{BPP} \subseteq \text{BQP} \subseteq \text{PSPACE}.
\qquad (1)
$$

Proofs:
- $\text{P} \subseteq \text{BPP}$: trivially, ignore the randomness.
- $\text{BPP} \subseteq \text{BQP}$: quantum computers can simulate classical randomness.
- $\text{BQP} \subseteq \text{PSPACE}$: Bernstein-Vazirani 1997 simulated a quantum computation using polynomial space (trading time for space via path-sum formulas).

## Unproven but widely believed

- $\text{P} \neq \text{NP}$: the million-dollar problem.
- $\text{BPP} \neq \text{BQP}$: we believe quantum computers are strictly more powerful than classical randomized ones. Shor's algorithm is evidence (exponential speedup for factoring vs. best classical known) but not proof (because factoring may be classically easy by some yet-undiscovered algorithm).
- $\text{NP} \not\subseteq \text{BQP}$: we believe quantum computers do *not* efficiently solve NP-hard problems. Grover's quadratic speedup is the limit for black-box NP-search (BBBV 1997).

## The Aaronson picture

**Scott Aaronson** has produced the most widely-used visualization of the complexity zoo. For quantum computing, the relevant picture:

```
           PSPACE
              |
              BQP
            /  |  \
         P^#P BPP  QMA
          |    |
         PH  (unknown if in BQP)
          |
         NP
          |
         BPP
          |
          P
```

BQP's relationship to NP is the interesting open question. Relative to an oracle, there is a problem in BQP outside PH (Raz-Tal 2019). Without oracles, the question is open. Most evidence suggests BQP does *not* contain all of NP.

## Implications for optimization

NP-hard combinatorial optimization (Max-Cut, TSP, SAT) is in NP. If $\text{NP} \not\subseteq \text{BQP}$, which is the consensus conjecture, then there is no polynomial-time quantum algorithm for exact NP-hard optimization. Heuristic quantum approaches (QAOA, annealing) may provide better approximation ratios on average instances, but will not provide general NP-hard solvability.

## Sampling classes

A separate parallel hierarchy exists for sampling problems:

- **SampP**, **SampBPP**, **SampBQP**, decision problems replaced by "sample from distribution within $\varepsilon$ total variation".

**Aaronson-Arkhipov 2011** showed that $\text{SampBQP} \not\subseteq \text{SampBPP}$ assuming the polynomial hierarchy is infinite. This is the theoretical foundation of boson-sampling supremacy claims. The RCS supremacy claims rely on a similar structure via **IQP** sampling hardness.

## The Eastin-Knill and related obstructions

Universal quantum computation requires non-Clifford gates. Within Clifford-only circuits, the **Gottesman-Knill theorem** says classical simulation is polynomial. Hence the quantum advantage must come from the non-Clifford (e.g., $T$-gate) portion of circuits. This is one reason **magic state distillation** dominates the resource cost of fault-tolerant quantum computation.

## What to conclude

For a practical scientist, the relevant takeaways:
- Quantum advantage on optimization does not follow automatically from BQP $\neq$ BPP. The advantage has to come from specific problem structure.
- Supremacy claims on sampling tasks (RCS, boson sampling) rest on complexity assumptions that would collapse PH if violated.
- Shor's speedup does not extend to NP-hard optimization.

These are important scales for the "what can quantum computing do for me" conversation.

## References

[1] Bernstein, E., Vazirani, U. (1993/1997). *Quantum Complexity Theory*. SIAM J. Comput. 26(5), 1411–1473.

[2] Aaronson, S., Arkhipov, A. (2011). *The Computational Complexity of Linear Optics*. STOC 2011, 333–342.

[3] Toda, S. (1991). *PP is as hard as the polynomial-time hierarchy*. SIAM J. Comput. 20(5), 865–877.

[4] Raz, R., Tal, A. (2019). *Oracle Separation of BQP and PH*. STOC 2019, 13–23.

[5] Bennett, C. H., Bernstein, E., Brassard, G., Vazirani, U. (1997). *Strengths and Weaknesses of Quantum Computing*. SIAM J. Comput. 26(5), 1510–1523.

