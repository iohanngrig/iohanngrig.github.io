---
title: "Computational irreducibility and the limits of optimization"
date: 2026-03-15
draft: false
tags: ["computational-complexity", "ai-foundations", "no-free-lunch"]
---

# Computational irreducibility and the limits of optimization

> Three deep negative results constrain what any AI system can do, regardless of architecture, data, or scale. The **No-Free-Lunch theorems** (Wolpert & Macready 1997) say that averaged over all problems, no optimization algorithm outperforms any other. **Computational irreducibility** (Wolfram 1985, 2002) says that for many systems, the only way to predict a future state is to simulate to it, no shortcut exists. **PAC-learning lower bounds** (Vapnik-Chervonenkis dimension, Kearns & Vazirani 1994) say that sample complexity has hard information-theoretic limits. This note derives the three results cleanly, explains what they do and do not imply for contemporary AI, and clarifies why "smarter AI" doesn't always escape these constraints.

## 1. No-Free-Lunch theorems

### 1.1 The statement

**Theorem (Wolpert & Macready 1997, simplified).** Let $\mathcal{F}$ be the space of all functions $f: \mathcal{X} \to \mathcal{Y}$ for finite $\mathcal{X}, \mathcal{Y}$. For any two black-box optimization algorithms $A, B$,

$$
\sum_{f \in \mathcal{F}} P\bigl(\text{performance}(A, f, m)\bigr) \;=\; \sum_{f \in \mathcal{F}} P\bigl(\text{performance}(B, f, m)\bigr),
$$

where $m$ is the number of queries allowed. Averaged over all functions, any two algorithms have the same expected performance.

![No-free-lunch illustration: per-problem vs. averaged](/research-notes/figures/nfl-fig1-tradeoff.svg)

The theorem is uncontroversial as a mathematical statement. Its philosophical implications are often overstated.

### 1.2 What NFL actually says

**What NFL says:**
1. No algorithm is universally better than another, *averaged over all possible objective functions*.
2. Any algorithm that does well on one set of problems must do poorly on another set, by a conservation argument.
3. Specialization is mathematically necessary: algorithms that exploit problem structure outperform generic ones *on the problems they exploit*, at the cost of performing worse on problems they don't.

**What NFL does NOT say:**
1. "All algorithms are equally good in practice." The set of practical problems is not the set of all possible problems. The practical distribution is highly non-uniform; most real-world problems share structure (locality, smoothness, compositional dependencies).
2. "Machine learning doesn't work." ML exploits assumptions about problem structure (iid data, smoothness, sparse features) that hold in the practical distribution, so it works there despite NFL's existence over the full function space.
3. "There is no best algorithm for a given problem." NFL averages over a uniform prior on functions; with any informative prior (e.g., "most real problems are smooth"), the averaging argument fails, and one algorithm can dominate.

The practical takeaway: the search for "general-purpose AGI" faces a version of the NFL problem. An agent trained on Earth-distribution data will necessarily perform worse on adversarially-constructed problems that violate Earth-distribution assumptions. "General" is relative to a distribution, not absolute.

## 2. Computational irreducibility

**Wolfram (1985, 2002)** introduced the concept of **computational irreducibility**: a system is computationally irreducible if the only way to determine its state at step $n$ is to simulate $n$ steps. No closed-form shortcut exists.

### 2.1 Examples

- **Cellular automata.** Many simple rules (Rule 30, Rule 110) produce patterns whose detailed future requires step-by-step simulation. No known shortcut predicts Rule 30's state at step $10^6$ short of running $10^6$ updates.
- **Turing-complete systems in general.** By undecidability of the halting problem, any Turing-complete system has inputs for which predicting future states is Turing-complete itself, hence not reducible by any faster algorithm.
- **Protein folding, chaotic systems, emergent behaviors.** Many real-world systems exhibit what is plausibly computational irreducibility, though rigorously proving irreducibility is typically hard.

### 2.2 Implications for AI

If a system is computationally irreducible, **no amount of intelligence can bypass the irreducibility**. An AI trying to predict the system must either (a) simulate it, incurring the full computational cost, or (b) accept imperfect predictions.

This bounds what AI can do in specific domains:

- **Weather forecasting.** Beyond ~14 days, forecasting is limited by the chaos of the atmosphere. No amount of better data or smarter AI extends this horizon significantly, the limit is physical, not algorithmic.
- **Long-horizon planning in rich environments.** An AI planning over long time horizons in a rich environment faces exponentially growing uncertainty. Planning longer than the environment's "predictability horizon" gives diminishing returns regardless of the planner's sophistication.
- **AGI forecasting.** The evolution of AI systems themselves, including the development trajectory to AGI, is plausibly computationally irreducible, the only way to know what AGI research produces is to do it.

The AI-safety community has occasionally overinvoked computational irreducibility to argue that AI systems are fundamentally unpredictable. This is only true in the specific technical sense; in practice, AI systems have substantial predictability at the level that matters for safety analysis.

## 3. PAC learning bounds

The **Probably Approximately Correct** (PAC) framework (Valiant 1984) gives information-theoretic lower bounds on learning.

### 3.1 The sample-complexity bound

**Theorem (VC).** For a hypothesis class $\mathcal{H}$ with VC-dimension $d$, any algorithm that outputs a hypothesis with error at most $\varepsilon$ with probability at least $1 - \delta$ requires at least

$$
m(\varepsilon, \delta) \;=\; \Omega\!\left(\frac{d + \log(1/\delta)}{\varepsilon}\right)
$$

training samples.

This is a *lower* bound: no algorithm, regardless of cleverness, can learn with fewer samples. It is a pure information-theoretic constraint.

### 3.2 What this means for contemporary AI

- **Neural networks have very high VC-dimension.** A fully-connected ReLU network with $W$ weights has VC-dimension of order $W$ (Bartlett et al. 2019). A modern LLM has $W \sim 10^{10}$ to $10^{12}$, VC-dimension that would suggest astronomical sample requirements for uniform-convergence-based generalization.
- **The observed generalization gap is much smaller than VC bounds predict.** Zhang et al. (2016), *Understanding Deep Learning Requires Rethinking Generalization*, showed that neural networks can memorize random labels (evidence of high capacity) yet generalize well on structured data. This is a puzzle for classical learning theory.
- **Modern theory** (e.g., Neal's Bayesian neural networks, NTK / infinite-width limits, margin-based bounds) gives refined generalization estimates that are substantially tighter than VC bounds but still do not fully explain the empirical success of deep learning.

PAC bounds are still the right reference for lower-bound reasoning: if you need to solve a problem with error $\varepsilon$ and the problem has VC-dimension $d$, no amount of architectural cleverness reduces the $d/\varepsilon$ lower bound below it. Sample-efficiency improvements come from restricting the effective hypothesis class, not from violating the bound.

## 4. Kolmogorov complexity and the impossibility of universal compression

Related to NFL and to Solomonoff induction (see [note 14](/research-notes/14-aixi)) is **Kolmogorov complexity**: $K(x)$ is the length of the shortest program that outputs $x$.

**Theorem.** $K(x)$ is uncomputable. For any computable upper-bound function $f$, there exists $x$ with $K(x) > f(|x|)$.

This has two AI-relevant corollaries.

**No universal compression.** No algorithm can compress every string. For any compression algorithm, there exist strings that cannot be compressed by it.

**The learning-compression connection.** Solomonoff induction essentially says: the best prediction is the one consistent with the shortest description. But since $K(x)$ is uncomputable, so is the optimal Solomonoff predictor. Practical approximations (MDL, neural compression) do well empirically but cannot in principle reach the uncomputable optimum.

## 5. Why these results matter for AGI

A thought experiment. Suppose someone built an "AGI" that claimed to solve any computational problem optimally. The three limits above would immediately refute the claim:

- **NFL:** Averaged over all problem distributions, the AGI's performance must equal any other algorithm's. If it dominates on every distribution, then a simple parity argument shows something is wrong.
- **Computational irreducibility:** There are problems whose solution requires fundamental simulation cost that cannot be shortcut. The AGI can only match this cost, not beat it.
- **PAC lower bounds:** For any learned behavior, the AGI's sample-complexity for achieving $(\varepsilon, \delta)$ guarantees is bounded below.

The AGI thought-experiment would either be false, or true only in the restricted sense of "very-capable-on-practically-important-distributions", which is what we'd call a highly-capable but bounded AI.

## 6. The more honest formulation

Rather than asking "will AI solve all problems?", the right question is: *for the practically-important distribution of problems, what capability levels are achievable and at what cost?*

This reframes the AGI debate from a binary (AGI yes/no) to a continuous one (what fraction of economically or scientifically valuable problems can current AI solve, and how fast is this fraction growing?). The continuous framing is more respectful of the fundamental limits surveyed here and also more informative about practical impact.

## 7. Open questions

**Effective sample complexity of deep learning.** Why do over-parameterized neural networks generalize? Why is their effective sample complexity much smaller than VC theory predicts? Partial answers exist (margin bounds, implicit regularization, infinite-width limits), but a satisfying theory is not settled.

**Meta-learning and its limits.** Learning-to-learn algorithms can reduce sample complexity on a target task by leveraging related tasks. How much reduction is possible, and against what structural assumptions about the task distribution, is a rich open area.

**Quantum advantage.** Quantum computers may provide polynomial (but not super-polynomial) speedups over classical for many problems; they do not bypass NFL, irreducibility, or PAC bounds at the level of this note.

**Approximations of uncomputable objects.** Solomonoff induction and AIXI are uncomputable. Practical approximations exist (context-tree weighting, MDL estimators, MuZero-style learned models). How good can these approximations get in principle, and what information is unavoidably lost?

## 8. References (verified April 2026)

- **Wolpert, D. H., & Macready, W. G.** (1997). *No free lunch theorems for optimization*. IEEE Transactions on Evolutionary Computation, 1(1), 67–82.
- **Wolfram, S.** (1985). *Undecidability and intractability in theoretical physics*. Physical Review Letters, 54(8), 735.
- **Wolfram, S.** (2002). *A new kind of science*. Wolfram Media.
- **Valiant, L. G.** (1984). *A theory of the learnable*. Communications of the ACM, 27(11), 1134–1142.
- **Vapnik, V. N., & Chervonenkis, A. Y.** (1971). *On the uniform convergence of relative frequencies of events to their probabilities*. Theory of Probability and Its Applications, 16(2), 264–280.
- **Kearns, M. J., & Vazirani, U. V.** (1994). *An introduction to computational learning theory*. MIT Press.
- **Bartlett, P. L., Harvey, N., Liaw, C., & Mehrabian, A.** (2019). *Nearly-tight VC-dimension and pseudodimension bounds for piecewise linear neural networks*. JMLR.
- **Zhang, C., Bengio, S., Hardt, M., Recht, B., & Vinyals, O.** (2016). *Understanding deep learning requires rethinking generalization*. ICLR 2017.
- **Kolmogorov, A. N.** (1965). *Three approaches to the quantitative definition of information*. Problems of Information Transmission, 1(1), 1–7.
- **Li, M., & Vitányi, P. M. B.** (2008). *An introduction to Kolmogorov complexity and its applications*. 3rd ed., Springer.
- **Turing, A. M.** (1936). *On computable numbers, with an application to the Entscheidungsproblem*. Proc. London Math. Soc., s2-42(1), 230–265.
