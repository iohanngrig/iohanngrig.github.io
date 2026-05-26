---
title: "Shor's algorithm and quantum factoring"
date: 2026-03-29
description: "The one quantum algorithm everyone's heard of, and the one most likely to actually matter. Period finding, quantum Fourier transform, and RSA's expiration date."
tags: [research-notes, quantum-computing, cryptography]
draft: false
---

Integer factoring is the problem that broke the "classical computers are universal" intuition. Given an $N$-bit integer, the best classical method, the general number field sieve, runs in sub-exponential but super-polynomial time. Shor's algorithm factors in $O((\log N)^3)$ quantum operations. That single gap, exponential versus sub-exponential, is also the entire reason post-quantum cryptography exists as a field: RSA and elliptic-curve key exchange would be dead the day a large fault-tolerant quantum computer gets switched on.

## Reduction to period finding

For $a$ coprime to $N$, the function $f(x) = a^x \bmod N$ is periodic: $f(x) = f(x + r)$ where $r$ is the multiplicative order of $a$ modulo $N$. If $r$ is even and $a^{r/2} \not\equiv \pm 1 \pmod N$, then $\gcd(a^{r/2} - 1, N)$ is a non-trivial factor of $N$.

Shor's insight: **period finding is classically exponential but quantum polynomial** using the Quantum Fourier Transform.

## Quantum Fourier Transform

The QFT on $n$ qubits is

$$
|x\rangle \mapsto \frac{1}{\sqrt{2^n}} \sum_{y=0}^{2^n-1} e^{2\pi i x y / 2^n} |y\rangle.
\qquad (1)
$$

It can be implemented with $O(n^2)$ gates using a nested structure of Hadamard and controlled-phase gates. In contrast, the classical Fast Fourier Transform takes $O(n 2^n)$ operations on a Hilbert space of dimension $2^n$.

## The algorithm

1. Prepare $\frac{1}{\sqrt{Q}} \sum_{x=0}^{Q-1} |x\rangle |0\rangle$ with $Q \approx N^2$.
2. Compute $|x\rangle |a^x \bmod N\rangle$.
3. Measure the second register. The first register collapses to a superposition over $x$'s with the same $a^x \bmod N$, i.e., arithmetic progressions with period $r$.
4. Apply QFT to the first register. The output is concentrated near multiples of $Q/r$.
5. Measure; classically post-process to extract $r$ via continued fractions.
6. Use $r$ to recover a factor of $N$ as above.

The entire quantum part runs in $O((\log N)^3)$ gates (dominated by modular exponentiation).

## Why Shor exponential speedup is credible

Unlike QAOA or adiabatic optimization, Shor's speedup rests on the QFT's inherent quantum-parallelism advantage: QFT computes a linear transformation over $2^n$-dimensional vector space in polynomial depth, exploiting the tensor structure of qubit states. Classical FFT cannot do this in polylogarithmic time because the classical vector must be written out explicitly.

Shor's algorithm is therefore the cleanest example of quantum speedup we have. The speedup is exponential assuming the best classical factoring algorithm really is exponential, which has not been proven, but is widely believed.

## RSA-2048 and the Megaquop gap

**Gidney-Ekerå 2021** [2] carefully estimated the resource cost of running Shor on RSA-2048 with surface-code error correction: approximately **20 million physical qubits** for 8 hours, assuming physical error rate $10^{-3}$. Currently, the largest quantum hardware has $\sim 10^3$ physical qubits. The gap is four orders of magnitude in qubits and significant in error rates.

Nevertheless, governments and security agencies are planning for "harvest now, decrypt later" threats: adversaries recording encrypted traffic today to decrypt when a cryptographically-relevant quantum computer (CRQC) arrives. NIST's Post-Quantum Cryptography standardization (lattice-based schemes; CRYSTALS-Kyber, CRYSTALS-Dilithium in FIPS 203-204) is the policy response [3].

## What Shor does *not* do

Shor solves a specific structured problem, factoring and discrete log. It does not solve:
- NP-hard optimization (not the same complexity class)
- Machine learning training (no analog of QFT for general loss landscapes)
- General linear systems beyond very restricted cases (HHL has practical limitations)

Overstating Shor's reach is a common media mistake. Cryptographers care; operations researchers usually should not.

## References

[1] Shor, P. W. (1995/1999). *Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer*. SIAM J. Comput. 26(5), 1484–1509. [arXiv:quant-ph/9508027](https://arxiv.org/abs/quant-ph/9508027)

[2] Gidney, C., Ekerå, M. (2021). *How to factor 2048-bit RSA integers in 8 hours using 20 million noisy qubits*. Quantum 5, 433.

[3] NIST (2024). *Federal Information Processing Standards 203 (ML-KEM) and 204 (ML-DSA)*. Post-Quantum Cryptography standardization.

