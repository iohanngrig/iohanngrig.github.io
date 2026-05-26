---
title: "Variational quantum eigensolvers (VQE) and their siblings"
date: 2026-04-05
description: "Why VQE dominates NISQ-era chemistry despite having no proven asymptotic advantage. The hybrid classical-quantum loop, ansatz design, and the barren plateau problem."
tags: [research-notes, quantum-computing, chemistry, variational]
draft: false
---

Variational quantum eigensolvers took over NISQ-era quantum chemistry in about 2015 and have held the position ever since. The irony is that VQE has no proven asymptotic advantage over classical methods on any problem. What it *does* have is a practical architecture that works within the depth budget of noisy hardware, and a natural coupling to established classical optimization. Peruzzo, McClean, and collaborators proposed it in 2013 as a workaround; a decade later, it is the dominant paradigm.

## The variational principle

For any Hermitian $H$ with ground-state energy $E_0$,

$$
E_0 \le \langle \psi | H | \psi \rangle \quad \forall |\psi\rangle.
\qquad (1)
$$

The right-hand side is an upper bound, tight at the ground state. VQE parameterizes $|\psi(\boldsymbol{\theta})\rangle$ via a shallow quantum circuit $U(\boldsymbol{\theta})$ acting on a reference state $|\psi_0\rangle$, then classically optimizes $\boldsymbol{\theta}$ to minimize $\langle \psi(\boldsymbol{\theta}) | H | \psi(\boldsymbol{\theta}) \rangle$.

On quantum hardware, one prepares $|\psi(\boldsymbol{\theta})\rangle$ for a given $\boldsymbol{\theta}$, measures $\langle H \rangle$ (typically by decomposing $H$ into Pauli strings and averaging), and passes the result to a classical optimizer. The classical optimizer proposes a new $\boldsymbol{\theta}$; the loop repeats.

## Ansatz design

Two dominant ansatz families:

**Hardware-efficient ansatz**, layers of single-qubit rotations and CNOT gates in a pattern matching the physical qubit connectivity. Advantage: shallow depth, low gate count. Disadvantage: no physical meaning; the optimization landscape is treacherous.

**Chemistry-inspired ansatz** (UCC, UCCSD), derived from coupled-cluster theory:

$$
|\psi(\boldsymbol{\theta})\rangle = e^{T(\boldsymbol{\theta}) - T^\dagger(\boldsymbol{\theta})} |\text{Hartree-Fock}\rangle
\qquad (2)
$$

where $T$ is a fermionic excitation operator. Advantage: has classical theoretical foundation, systematically improvable. Disadvantage: depth scales poorly with system size.

## QAOA as a sibling

When $H = H_C$ is an Ising Hamiltonian and the ansatz is restricted to alternating $e^{-i\gamma H_C} e^{-i\beta H_B}$ layers with $H_B = -\sum X_i$, VQE reduces to QAOA. VQE is the general framework; QAOA is a specific ansatz choice motivated by the adiabatic theorem.

## The barren plateau problem

**McClean et al. 2018** [2] proved a surprising and bad result: for random parameterized circuits of depth $\ge O(\log n)$ on $n$ qubits, the gradient of the VQE cost function is exponentially concentrated near zero. Specifically, $\mathbb{E}[\partial E/\partial\theta] = 0$ and $\text{Var}[\partial E/\partial\theta] = O(2^{-2n})$. In expectation, gradient descent sees zero signal, a **barren plateau**.

This result has practical consequences:
- Random initialization of deep parameterized circuits is essentially useless.
- Structured initialization (near-Hartree-Fock for chemistry, near-adiabatic path for optimization) is essential.
- Shallow circuits, or circuits with problem-specific locality, often avoid the plateau.

The barren plateau problem is one reason QAOA initialization using adiabatic paths (e.g., linear ramp) works much better than random initialization.

## Classical competition

For quantum chemistry, VQE competes with:
- **Configuration interaction** (CI, CCSD, CCSD(T)), classical gold standard for small molecules.
- **Density functional theory** (DFT), cheap but approximate.
- **Classical tensor network methods** (DMRG, PEPS), excellent for 1D and 2D lattice problems.

On modest molecules (H$_2$, LiH, BeH$_2$, up to maybe 12 qubits), VQE matches classical. On larger molecules (10+ atoms, 50+ qubits), noise accumulation degrades VQE faster than increasing system size degrades classical methods. **No molecule has been demonstrated where VQE on current hardware beats a well-tuned classical method.** This is a central open challenge of NISQ-era quantum chemistry.

## Honest summary

VQE is a *framework*, not an algorithm-with-speedup. It is likely to be the first quantum-computing application that provides practical value, but the value will come from hybrid algorithms where the quantum subroutine handles strongly correlated regions of the wavefunction that classical methods can't efficiently represent. The *timeline* for this is tied to fault-tolerant quantum hardware, not to NISQ.

## References

[1] Peruzzo, A., McClean, J., Shadbolt, P., Yung, M.-H., Zhou, X.-Q., Love, P. J., Aspuru-Guzik, A., O'Brien, J. L. (2013). *A variational eigenvalue solver on a photonic quantum processor*. Nature Communications 5, 4213.

[2] McClean, J. R., Boixo, S., Smelyanskiy, V. N., Babbush, R., Neven, H. (2018). *Barren plateaus in quantum neural network training landscapes*. Nature Communications 9, 4812.

[3] Cerezo, M., Arrasmith, A., Babbush, R., Benjamin, S. C., Endo, S., Fujii, K., McClean, J. R., Mitarai, K., Yuan, X., Cincio, L., Coles, P. J. (2021). *Variational Quantum Algorithms*. Nature Reviews Physics 3, 625–644.

