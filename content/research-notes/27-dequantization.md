---
title: "Dequantization and the Tang algorithms"
date: 2026-04-25
description: "How Ewin Tang's 2018 undergraduate thesis erased an exponential speedup, and what the broader dequantization program tells us about quantum-ML advantage claims."
tags: [research-notes, quantum-computing, machine-learning]
draft: false
---

In 2018, an undergraduate at UT Austin took a well-known quantum machine-learning algorithm that had been advertised with exponential speedup, asked whether a classical algorithm could achieve the same performance given access to the same data access structure, and proved the answer was yes. The result, Ewin Tang's now-famous paper, did not just dequantize one algorithm. It launched a program that dequantized entire classes of "exponentially faster quantum ML" claims. The methodology has since become a discipline.

## The setup

**Kerenidis-Prakash 2017** proposed a quantum algorithm for recommendation systems based on HHL-style linear algebra on a preference matrix $A \in \mathbb{R}^{m \times n}$ stored in QRAM. Given access to $A$ in QRAM and a user index $i$, the algorithm outputs a sample $\tilde x_j$ where $j$ is distributed according to the truncated-SVD reconstruction of $A$, in time $O(\text{poly}(k)\log(mn))$. Compared to classical recommender systems (which are linear in $mn$), this is exponential speedup.

## Tang's classical analog

**Tang 2018** [1] asked: what if we allow the *classical* algorithm the same kind of access structure, $\ell_2$-norm sampling rather than a pointer-access to a random element? Define:

**Definition (sample-access).** A data structure supports $\ell_2$-norm sample-access to $v \in \mathbb{R}^n$ if it can sample an index $j$ with probability $v_j^2 / \|v\|_2^2$ in $O(\log n)$ time, query $v_j$ in $O(\log n)$, and report $\|v\|_2$ in $O(1)$.

This can be implemented by a classical segment tree on $v$. Crucially, this is the classical analog of QRAM's assumed access.

Tang's algorithm: given $\ell_2$-sample-access to rows of $A$, produce a sample from the truncated rank-$k$ approximation in $O(\text{poly}(k) \log(mn))$ time, *matching* Kerenidis-Prakash up to polynomial factors. The claimed exponential quantum speedup, as originally stated, did not exist.

## The general dequantization program

Tang's insight generalized rapidly. **Gilyén, Song, Tang 2022** [2] dequantized linear regression. Dequantizations of PCA [3], supervised clustering [3], support vector machines [4], and semidefinite programming subroutines followed.

The common pattern: a quantum algorithm claims exponential speedup assuming **QRAM access** to input data. Allowing classical $\ell_2$-sampling access, a polynomial-time-preprocessible structure, lets classical algorithms achieve polylog query complexity for the same problem. The quantum speedup was over **naive classical algorithms**, not over classical algorithms on equal footing.

## What survives

Not every quantum ML speedup has dequantized. The ones that survive have structure that classical $\ell_2$-sampling can't replicate:
- **High-dimensional linear algebra with structured operators** (sparse, low-condition-number, geometric), some problems here retain quantum advantage.
- **Sampling from quantum-state-generated distributions**, fundamental sampling problems that classical $\ell_2$-sampling can't reach.
- **Quantum Monte Carlo with quadratic speedup**, Grover-type advantage.

The message is nuanced: **dequantization did not disprove quantum ML**, it refined what "quantum ML advantage" can honestly mean. Claims of polylog-time speedup require specifying classical input access.

## Bigger lesson for claims

Tang's work is a template for how to stress-test complexity claims:
1. Identify the assumed input-access model on the quantum side (QRAM, sparse oracle, etc.).
2. Construct the tightest-possible classical analog.
3. See if the classical analog plus clever algorithms matches the quantum bound.

Applied systematically, this approach is how the quantum ML literature moved from the 2013-2017 "exponential speedup for everything" era to the 2019+ "specific speedups under specific assumptions" era.

For quantum optimization (§17), a partial dequantization has *not* happened, QAOA does not have a known classical analog with the same bound on general Ising instances. But the field has internalized the Tang discipline: every new quantum-advantage claim is now scrutinized for hidden assumptions.

## References

[1] Tang, E. (2018/2019). *A quantum-inspired classical algorithm for recommendation systems*. STOC 2019, 217–228. [arXiv:1807.04271](https://arxiv.org/abs/1807.04271)

[2] Gilyén, A., Song, Z., Tang, E. (2022). *An improved quantum-inspired algorithm for linear regression*. Quantum 6, 754.

[3] Tang, E. (2018). *Quantum-inspired classical algorithms for principal component analysis and supervised clustering*. arXiv:1811.00414.

[4] Ding, C., Bao, T.-Y., Huang, H.-L. (2021). *Quantum-inspired support vector machine*. IEEE Trans. Neural Netw.

[5] Aaronson, S. (2015). *Read the fine print*. Nature Physics 11, 291–293.

