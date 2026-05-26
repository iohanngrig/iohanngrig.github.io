---
title: "Quantum computing for constrained optimization, what's proved, what's hoped"
date: 2026-03-21
description: "A pedagogical tour through Shor, Grover, the adiabatic theorem, QAOA, and NISQ hardware, with an honest accounting of what has been mathematically proved about quantum advantage for constrained optimization and what remains heuristic."
tags:
  - research-notes
  - quantum-computing
  - optimization
  - complexity
draft: false
---

> The purpose of these notes is to separate three questions that are easy to confuse: *(a)* what quantum algorithms can provably do faster than any classical algorithm; *(b)* what near-term quantum hardware has actually demonstrated; *(c)* whether either of those tells us that constrained optimization, the workhorse of operations research, machine learning, finance, logistics, will get quantum-easier in practice. The short answers are: very few things provably; sampling tasks, not optimization; and *probably not in the regime anyone cares about*, with important caveats. The long answers follow.

## 1. Preliminaries, what counts as a speedup

A **constrained optimization** problem has the form

$$
\min_{x \in \mathcal{X}} f(x) \qquad \text{subject to } g_j(x) \le 0,\ j = 1,\dots,m,
\qquad (1)
$$

with $\mathcal{X} \subseteq \mathbb{R}^n$ or $\{0,1\}^n$. When the variables are binary and the objective is a quadratic form, the problem becomes a **Quadratic Unconstrained Binary Optimization** (QUBO) after penalizing violations:

$$
\min_{x \in \{0,1\}^n}\ x^\top Q x + \lambda \sum_j \max(0, g_j(x))^2.
\qquad (2)
$$

Substituting $x_i = (1 - s_i)/2$ with $s_i \in \{-1,+1\}$, QUBO becomes the **Ising** problem

$$
\min_{s \in \{-1,+1\}^n}\ \sum_{i<j} J_{ij}\, s_i s_j + \sum_i h_i s_i,
\qquad (3)
$$

which is the canonical target of quantum-heuristic optimization algorithms. Max-Cut, graph coloring, portfolio selection, traffic routing, and many scheduling problems reduce to (3). Solving Ising exactly is **NP-hard** (Barahona 1982).

A **quantum speedup** is a claim that some quantum algorithm solves a problem in asymptotically fewer operations than the best possible classical algorithm. Three flavors matter:

| Type | Example | Status |
|---|---|---|
| **Exact, provable vs. best classical known** | Shor's factoring | Exponential speedup, broadly believed but unproved-vs-best-possible |
| **Exact, provable vs. black-box lower bound** | Grover's search | Quadratic speedup, proven optimal in query model |
| **Heuristic (no proof vs. best classical)** | QAOA, VQE, quantum annealing | No asymptotic advantage established for general instances |

Readers who leave these pages remembering only one distinction should remember this one.

## 2. Two algorithms with actual proofs

### 2.1 Shor, factoring in polynomial time

**Shor's algorithm** (Shor 1995 [1]) factors an $N$-bit integer in $O((\log N)^3)$ time on a quantum computer, exponentially faster than the best known classical algorithm (general number field sieve, $\exp(O((\log N)^{1/3} (\log \log N)^{2/3}))$). The speedup comes from the **Quantum Fourier Transform** (QFT) computing the period of the function $f(x) = a^x \bmod N$ in polylog time.

Factoring is not known to be NP-hard. This matters: Shor's algorithm does *not* break NP, and in fact most complexity theorists conjecture $\text{NP} \not\subseteq \text{BQP}$. Shor is an existence proof that quantum computers can do *something* classical computers probably cannot, not that they solve the problems optimization researchers care about.

### 2.2 Grover, quadratic speedup for search

**Grover's algorithm** (Grover 1996 [2]) finds a marked element in an unsorted database of $N$ items using $O(\sqrt{N})$ quantum queries, versus $\Theta(N)$ classically. It is provably optimal in the **query model** (Bennett-Bernstein-Brassard-Vazirani 1997).

For NP-hard constrained optimization, Grover gives a *quadratic* speedup on brute-force enumeration: from $2^n$ to $2^{n/2}$. This is useful but not transformational. It does **not** beat structured classical heuristics (branch and bound, local search, cutting planes, SDP relaxations) on real instances, because those heuristics already run much faster than $2^n$.

![Grover vs. brute-force enumeration on n bits; Shor vs. general number field sieve](/research-notes/figures/qo-fig1-speedups.svg)

The quadratic-vs-exponential distinction is why "quantum computing will solve optimization" claims deserve scrutiny: Grover bounds most general-purpose quantum optimization heuristics, and Grover alone does not clear the bar.

## 3. The adiabatic theorem and QAOA, the optimization-specific toolkit

### 3.1 Adiabatic quantum computation

**Farhi-Goldstone-Gutmann-Sipser 2000** [3] proposed encoding optimization as ground-state preparation. Define

$$
H(t) = \left(1 - \frac{t}{T}\right) H_B + \frac{t}{T} H_C,
\qquad (4)
$$

where $H_B = -\sum_i X_i$ is a trivial "mixing" Hamiltonian with known ground state $|+\rangle^{\otimes n}$, and $H_C$ is a problem Hamiltonian whose ground state encodes the optimum of (3). For Ising, $H_C = \sum_{i<j} J_{ij} Z_i Z_j + \sum_i h_i Z_i$.

The **adiabatic theorem** (Born-Fock 1928; see Jansen-Ruskai-Seiler 2007 for modern bounds) states: if the system starts in the ground state of $H(0) = H_B$ and $H(t)$ changes slowly enough, it stays in the instantaneous ground state. Specifically, the evolution time $T$ must satisfy

$$
T \gg \frac{\max_t \|\dot{H}(t)\|}{\min_t \Delta(t)^2},
\qquad (5)
$$

where $\Delta(t)$ is the spectral gap between the ground state and first excited state of $H(t)$.

The good news: at $t = T$, the state is the ground state of $H_C$, i.e., the optimizer. The bad news: **$\Delta(t)$ is exponentially small at first-order quantum phase transitions**. For worst-case hard instances of 3-SAT, the gap closes as $\Delta_{\min} \sim 2^{-\alpha n}$ for some $\alpha > 0$, and required runtime becomes exponential (Altshuler-Krovi-Roland 2010; Farhi et al. 2001 [4]). The adiabatic algorithm is **provably equivalent in power to universal quantum computation** (Aharonov et al. 2007) but it is *not* provably better than classical algorithms on NP-hard optimization.

### 3.2 QAOA, discretizing the adiabatic path

For gate-model quantum computers, the adiabatic path is approximated by a Trotter decomposition. **Farhi-Goldstone-Gutmann 2014** [5] formalized this as the **Quantum Approximate Optimization Algorithm** (QAOA). With classical parameters $\boldsymbol{\gamma} = (\gamma_1,\ldots,\gamma_p)$ and $\boldsymbol{\beta} = (\beta_1,\ldots,\beta_p)$, the QAOA ansatz is

$$
|\psi_p(\boldsymbol{\gamma}, \boldsymbol{\beta})\rangle = e^{-i \beta_p H_B} e^{-i \gamma_p H_C} \cdots e^{-i \beta_1 H_B} e^{-i \gamma_1 H_C} |+\rangle^{\otimes n}.
\qquad (6)
$$

One measures the expected cost $\langle \psi_p | H_C | \psi_p \rangle$ and uses a classical outer loop to minimize over $(\boldsymbol{\gamma}, \boldsymbol{\beta}) \in \mathbb{R}^{2p}$. As $p \to \infty$ with optimal parameters, QAOA recovers the adiabatic limit.

**At $p=1$ on 3-regular Max-Cut**, Farhi-Goldstone-Gutmann [5] proved an approximation ratio

$$
\mathbb{E}[f(x_{\text{QAOA}})] \ge 0.6924 \cdot f(x^*),
$$

where $x^*$ is the optimum. Compare to the classical Goemans-Williamson 1995 SDP bound of $0.8786$. **QAOA at $p=1$ does not beat Goemans-Williamson.** At higher $p$, QAOA numerical studies (Farhi-Goldstone-Gutmann-Zhou 2019 [6]) show QAOA at $p=11$ on the Sherrington-Kirkpatrick model **outperforming** standard semidefinite programming, but still trailing the conjecturally-optimal Montanari 2019 algorithm, and only in the infinite-size limit ($n \to \infty$), not on finite hardware.

### 3.3 VQE, the chemistry-flavored sibling

**Peruzzo-McClean et al. 2013** [7] extended the same variational recipe to eigenvalue problems relevant to quantum chemistry. The Variational Quantum Eigensolver (VQE) uses a parameterized state $|\psi(\boldsymbol{\theta})\rangle$ and minimizes $\langle \psi(\boldsymbol{\theta}) | H | \psi(\boldsymbol{\theta}) \rangle$ classically. For optimization, VQE and QAOA are essentially the same architecture; QAOA just restricts the ansatz to alternating-operator form.

## 4. Where the claim of "supremacy" actually comes from

Claims of quantum *computational supremacy* (Preskill 2012) do **not** come from optimization. They come from three sampling tasks:

### 4.1 Random Circuit Sampling (Google Sycamore 2019)

A random circuit of $n$ qubits and depth $d$ produces a distribution $p(x)$ over $n$-bit strings that is provably hard to sample from classically, assuming the polynomial hierarchy does not collapse (Boixo et al. 2018; Bouland et al. 2019). Google's Sycamore experiment (**Arute et al. 2019, Nature 574**) sampled 53-qubit circuits in 200 seconds and estimated 10,000 years for Summit.

**What happened next** is instructive. Within 14 months, two classical simulation results tightened the gap:
- **Huang et al. 2020**, tensor-network contraction brought the Summit estimate from 10,000 years to **20 days** [8].
- **Liu et al. 2021** (Sunway supercomputer), further reduced it to **1 week**, with the authors writing that their result "collapses the quantum supremacy claim of Sycamore" [9].

The lesson is *not* that quantum computers lost. The lesson is that **supremacy claims have been a moving target** as classical algorithms and hardware improve in lockstep. Both Preskill 2018 [10] and Preskill 2025 [11] stress this: "quantum advantage is a dynamic competition between quantum devices and classical simulation."

### 4.2 Gaussian Boson Sampling (USTC Jiuzhang 2020)

**Zhong et al. 2020 Science 370** [12] used a 100-mode photonic processor to produce sampling events at a rate $\sim 10^{14}$ faster than reported classical simulators at the time. Unlike Sycamore, the speedup survived follow-up classical simulation attempts through 2024, strengthening the claim. Subsequent Jiuzhang 4.0 (Liu et al. 2025) pushed to 3050 photon clicks with larger margins.

### 4.3 The framing problem

Notice what these results are *not*: they are not optimizing portfolio weights, not solving vehicle routing, not training neural networks. They are sampling from particular probability distributions that happen to be classically hard. Boson sampling is a one-output machine. RCS is not even a programmable algorithm, it's a benchmark.

This has two practical implications:
1. The hardware that demonstrated supremacy **cannot run Shor**. It can run sampling circuits because those tolerate noise in a particular way (Aaronson-Gunn 2019).
2. No supremacy experiment has demonstrated quantum advantage on an **optimization** problem. The closest attempt, QAOA on Sycamore, came out against the quantum processor. See §5.

## 5. What happens when you try QAOA on real hardware

**Harrigan, Arute, et al. 2020, Nature Physics 17** [13] (593 citations) ran QAOA on Google's Sycamore processor on two classes of problems:

1. **Hardware-native graph problems** (defined on Sycamore's planar connectivity graph). Here QAOA gave approximation ratios independent of problem size, improving with circuit depth.
2. **Non-native problems** (Sherrington-Kirkpatrick, general Max-Cut). Performance *decreased* with problem size. Circuits involving several thousand gates still beat random guessing but **not efficient classical algorithms**.

The reason is brutal arithmetic. Compiling a non-native interaction graph onto a hardware topology takes depth $O(n)$ for SWAP chains. Noise per gate is $\sim 10^{-3}$; compose that over $10^3$ gates and state fidelity drops to $\sim e^{-1}$. Classical benchmarks (Goemans-Williamson, greedy, tabu) have no such fidelity penalty.

The authors concluded: *"it will be challenging to scale near-term implementations of the QAOA for problems on non-native graphs. As these graphs are closer to real-world instances, we suggest more emphasis should be placed on such problems when using the QAOA to benchmark quantum processors."*

This is, frankly, the most important paper in the "quantum optimization advantage" literature. It was co-authored by essentially every Google Quantum AI researcher including Farhi himself.

![QAOA on Sycamore, native vs. non-native graphs, stylized after Harrigan et al. 2020](/research-notes/figures/qo-fig2-qaoa-hardware.svg)

## 6. The NISQ bottleneck and what comes after

### 6.1 NISQ

Preskill 2018 [10] coined **Noisy Intermediate-Scale Quantum** (NISQ) for 50-1000 qubit devices without error correction. The paper's central honest assessment:

> *NISQ devices will be useful tools for exploring many-body quantum physics, and may have other useful applications, but the 100-qubit quantum computer will not change the world right away.*

Seven years later, this has aged well. Sycamore is 53 qubits. IBM Heron is 133. Quantinuum is ~56 ion-trap qubits. None has beaten a well-tuned classical solver on any problem an operations-research engineer would pay to solve.

### 6.2 Error correction and Megaquop

**Preskill 2025** [11] names the next target: the **Megaquop machine**, an error-corrected device performing $\ge 10^6$ logical operations. Getting there requires surface-code-style encoding at physical error rates $\sim 10^{-3}$ below the fault-tolerance threshold. Current IBM and Google demos achieve this at small scale; scaling to tens of thousands of physical qubits per logical qubit is the engineering problem of the decade.

If the Megaquop machine arrives, Shor on RSA-2048 becomes feasible ($\sim 20$ million physical qubits; Gidney-Ekerå 2021). Optimization is more uncertain: even error-free QAOA has no asymptotic speedup proof against classical algorithms on general Ising.

### 6.3 Dequantization

**Tang 2018** [14] dequantized an influential quantum ML algorithm (Kerenidis-Prakash quantum recommender system), showing that under the same access assumptions, a classical algorithm achieves the same polylogarithmic scaling. A cascade of similar results followed, for principal component analysis, supervised clustering, semidefinite programming, and various linear-algebra subroutines.

The Tang lesson: **many claimed quantum speedups assume unrealistic data access** (QRAM). If classical algorithms are allowed $\ell_2$-norm sampling on the same input, those speedups evaporate. Honest quantum advantage requires specifying *classical input access* on the same footing.

## 7. When is quantum optimization plausibly useful?

Synthesizing the above into an operational guide, quantum optimization plausibly helps when:

1. **The problem has a natural local Hamiltonian structure** on qubits (spin-glass physics, quantum chemistry, lattice-model simulation). Here the hardware native graph matches the problem graph. See Harrigan et al.'s "hardware-native" setting [13].
2. **Classical heuristics are weak.** If Goemans-Williamson already gives 0.87, a 0.7 QAOA bound is not interesting. QAOA's value proposition is on *specific* problem structures where classical bounds are known to be tight against $P \ne NP$ barriers.
3. **You have a fault-tolerant device.** Without error correction, the circuit-depth budget is too small for meaningful QAOA depth.
4. **You don't need exponential speedup.** Grover-style quadratic speedups on enumeration may become practical on error-corrected machines; exponential speedup for general optimization likely requires a complexity-theoretic breakthrough (probably false).

None of those conditions holds in 2026 for logistics, portfolio optimization, supply chain, scheduling, or most operations-research applications. Published quantum-advantage claims on those problems have, to the best of this author's knowledge, been classically matched or outperformed shortly after.

## 8. Honest limits and open problems

**What is provably true:**
- Shor gives exponential advantage for factoring and discrete log [1].
- Grover gives quadratic advantage for unstructured search [2].
- Adiabatic QC and gate-model QC are polynomially equivalent (Aharonov et al. 2007).

**What is *not* provably true despite frequent claims otherwise:**
- Quantum computers have an asymptotic speedup for NP-hard optimization. No such proof exists. Most complexity theorists conjecture $\text{NP} \not\subseteq \text{BQP}$.
- QAOA outperforms the best classical algorithms on any natural problem. The paper most often cited as evidence [6] only shows QAOA matching SDP at $p=11$ in infinite-size limit.
- Quantum annealing (D-Wave) gives speedup. Rønnow et al. 2014 Science showed D-Wave 2X gives at most constant-factor speedup over simulated annealing.
- The Sycamore 2019 experiment demonstrated unconditional supremacy. Huang et al. [8] and Liu et al. [9] brought the classical simulation cost within reach.

**Genuinely open questions:**
- Does $\text{BQP} \neq \text{BPP}$? This is not proven, Shor's speedup is relative to our best known classical factoring algorithms.
- Is there a natural NP-hard problem with provable quantum speedup? None known.
- Can fault-tolerant quantum computation achieve better approximation ratios than SDP on Max-Cut? Conjectured yes for specific instance distributions; unproven.
- When does dequantization succeed? Partially understood (low-rank, QRAM-free settings); general criteria open.

The next 18 months will likely see Google/IBM demonstrate early error-corrected logical operations. Whether these scale to the Megaquop regime is the dominant open engineering question. Whether that matters for *optimization* specifically, as opposed to chemistry or cryptanalysis, is an open scientific question that this research note cannot answer.

---

## Bibliography

[1] Shor, P. W. (1995). *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer*. SIAM Review 41(2), 303–332 (1999 journal; 1995 conference). [arXiv:quant-ph/9508027](https://arxiv.org/abs/quant-ph/9508027)

[2] Grover, L. K. (1996). *A fast quantum mechanical algorithm for database search*. STOC 1996, 212–219. [arXiv:quant-ph/9605043](https://arxiv.org/abs/quant-ph/9605043)

[3] Farhi, E., Goldstone, J., Gutmann, S., Sipser, M. (2000). *Quantum Computation by Adiabatic Evolution*. [arXiv:quant-ph/0001106](https://arxiv.org/abs/quant-ph/0001106)

[4] Farhi, E., Goldstone, J., Gutmann, S., Lapan, J., Lundgren, A., Preda, D. (2001). *A Quantum Adiabatic Evolution Algorithm Applied to Random Instances of an NP-Complete Problem*. Science 292(5516), 472–475.

[5] Farhi, E., Goldstone, J., Gutmann, S. (2014). *A Quantum Approximate Optimization Algorithm*. [arXiv:1411.4028](https://arxiv.org/abs/1411.4028). Companion: *A Quantum Approximate Optimization Algorithm Applied to a Bounded Occurrence Constraint Problem*, [arXiv:1412.6062](https://arxiv.org/abs/1412.6062).

[6] Farhi, E., Goldstone, J., Gutmann, S., Zhou, L. (2019). *The Quantum Approximate Optimization Algorithm and the Sherrington-Kirkpatrick Model at Infinite Size*. Quantum 6, 759 (2022). [arXiv:1910.08187](https://arxiv.org/abs/1910.08187)

[7] Peruzzo, A., McClean, J., Shadbolt, P., et al. (2013). *A variational eigenvalue solver on a photonic quantum processor*. Nature Communications 5, 4213.

[8] Huang, C., Zhang, F., Newman, M., et al. (2020). *Classical Simulation of Quantum Supremacy Circuits*. [arXiv:2005.06787](https://arxiv.org/abs/2005.06787)

[9] Liu, X., Guo, C., Liu, Y., et al. (2021). *Redefining the Quantum Supremacy Baseline With a New Generation Sunway Supercomputer*. [arXiv:2111.01066](https://arxiv.org/abs/2111.01066)

[10] Preskill, J. (2018). *Quantum Computing in the NISQ era and beyond*. Quantum 2, 79.

[11] Preskill, J. (2025). *Beyond NISQ: The Megaquop Machine*. ACM Transactions on Quantum Computing 6(3).

[12] Zhong, H.-S., Wang, H., Deng, Y.-H., et al. (2020). *Quantum computational advantage using photons*. Science 370(6523), 1460–1463.

[13] Harrigan, M. P., Arute, F., et al. (2021). *Quantum approximate optimization of non-planar graph problems on a planar superconducting processor*. Nature Physics 17, 332–336. [Primary source for honest-limits of QAOA on hardware.]

[14] Tang, E. (2018/2019). *A quantum-inspired classical algorithm for recommendation systems*. STOC 2019, 217–228. [arXiv:1807.04271](https://arxiv.org/abs/1807.04271)

**Additional canonical references:**

- Aharonov, D., van Dam, W., Kempe, J., Landau, Z., Lloyd, S., Regev, O. (2007). *Adiabatic Quantum Computation Is Equivalent to Standard Quantum Computation*. SIAM Journal on Computing 37(1), 166–194.
- Barahona, F. (1982). *On the computational complexity of Ising spin glass models*. Journal of Physics A 15(10), 3241.
- Boixo, S., Isakov, S. V., Smelyanskiy, V. N., et al. (2018). *Characterizing quantum supremacy in near-term devices*. Nature Physics 14(6), 595–600.
- Goemans, M. X., Williamson, D. P. (1995). *Improved Approximation Algorithms for Maximum Cut and Satisfiability Problems Using Semidefinite Programming*. JACM 42(6), 1115–1145.
- Harrow, A. W., Hassidim, A., Lloyd, S. (2009). *Quantum Algorithm for Linear Systems of Equations*. Physical Review Letters 103, 150502.
- Rønnow, T. F., Wang, Z., Job, J., et al. (2014). *Defining and detecting quantum speedup*. Science 345(6195), 420–424.

---

*Figures in this note reproduce analytical formulas from Farhi-Goldstone-Gutmann 2014 [5] (QAOA approximation bound, §3.2) and Farhi-Goldstone-Gutmann-Zhou 2019 [6] (SK model results). Classical-simulation time comparisons in §4.1 follow the numbers reported by Arute et al. 2019, Huang et al. 2020 [8], and Liu et al. 2021 [9]. No Sycamore or Jiuzhang data is reproduced, only the published headline metrics.*

---

**Related research notes in this series:**

- [13. Gödel, Löb, and the formal limits of self-referential AI](13-godel-lob.md), computability context for BQP vs. recursion-theoretic undecidability
- [16. Wolfram's computational irreducibility](16-computational-irreducibility.md), a different view of "what cannot be shortcut"
- Notes 18–27 (quantum series), *forthcoming*, see the research-notes index
