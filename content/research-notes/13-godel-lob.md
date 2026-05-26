---
title: "Gödel, Löb, and the formal limits of self-referential AI"
date: 2026-03-07
draft: false
tags: ["logic", "incompleteness", "ai-foundations"]
---

# Gödel, Löb, and the formal limits of self-referential AI

> Gödel's incompleteness theorems (1931) and Löb's theorem (1955) are usually introduced as results in mathematical logic. They are also the most-cited, and most-misunderstood, formal arguments about the limits of AI. This note derives the two results accurately, clarifies what they do and do not imply about machines that reason, and surveys the recent AI-safety literature on self-referential agents where these results are technically load-bearing rather than rhetorical.

## 1. Gödel's first incompleteness theorem

Let $T$ be a formal theory: a recursively enumerable set of axioms, a set of inference rules, and a language strong enough to express arithmetic. We say $T$ is:

- **Consistent** if $T$ does not prove both $\phi$ and $\lnot\phi$ for any $\phi$.
- **Complete** if for every sentence $\phi$, either $T \vdash \phi$ or $T \vdash \lnot\phi$.

**Theorem (Gödel 1931).** Any consistent, recursively enumerable theory $T$ that includes Peano arithmetic is incomplete: there exists a sentence $G_T$ in the language of $T$ such that neither $T \vdash G_T$ nor $T \vdash \lnot G_T$.

### 1.1 The proof idea, honestly

The proof constructs $G_T$ via *diagonalization*. In $T$'s language, encode formal proofs as natural numbers (Gödel numbering). Define the predicate $\text{Prov}_T(x) :\equiv$ "$x$ is the Gödel number of a sentence provable in $T$". This predicate exists and is expressible because $T$ is recursively enumerable.

Now construct a sentence $G_T$ that "says" $\lnot \text{Prov}_T(\lceil G_T \rceil)$, informally, "this sentence is not provable in $T$". The construction is via the **diagonal lemma**, which states that for any formula $\phi(x)$ there exists a sentence $\psi$ such that $T \vdash \psi \leftrightarrow \phi(\lceil \psi \rceil)$.

![Gödel's first incompleteness theorem by diagonalization](/research-notes/figures/godel-fig1-diagonalization.svg)

The argument:

- If $T \vdash G_T$, then $G_T$ is provable, so $\text{Prov}_T(\lceil G_T \rceil)$ is true. But $G_T$ asserts $\lnot \text{Prov}_T(\lceil G_T \rceil)$. By consistency, $T \nvdash \lnot G_T$. So $T$ proves both $G_T$ and something equivalent to $\lnot G_T$. Contradiction.
- If $T \vdash \lnot G_T$, then (by the same reasoning applied to $\lnot G_T$) we get a similar contradiction *provided $T$ is $\omega$-consistent* (a slightly stronger assumption than consistency; Rosser 1936 showed consistency alone suffices with a trickier construction).

So $T$ proves neither $G_T$ nor $\lnot G_T$. Incompleteness.

### 1.2 What this does and does NOT say

**Says:** any sufficiently strong, consistent, recursively axiomatized formal theory has true sentences it cannot prove.

**Does not say:** humans can do things no machine can do. The sentence $G_T$ that $T$ cannot prove is provable in any stronger theory $T' \supsetneq T$, including by a human working in a more expressive system. There is no privileged cognitive power here; there is just a specific theory-relative result.

**Does not say:** AI is impossible or that AI cannot reason about mathematics. Automated theorem provers are not one-true-theory machines; they can operate in multiple theories and, crucially, can recognize when a particular theory is too weak for a given statement.

The famous **Penrose argument** (*The Emperor's New Mind* 1989) claims Gödel's theorem proves human consciousness cannot be computational. The argument has been widely rebutted (see Davis 1993, Chalmers 1995, Feferman 1996): it requires the assumption that a human can *know with certainty* that their own reasoning is consistent, which Gödel's second theorem (below) shows is exactly what no formal system can do for itself.

## 2. Gödel's second incompleteness theorem

**Theorem (Gödel 1931, second).** A consistent, recursively axiomatized theory $T$ extending Peano arithmetic cannot prove its own consistency:

$$
T \nvdash \text{Con}(T),
$$

where $\text{Con}(T) :\equiv \lnot \text{Prov}_T(\lceil 0 = 1 \rceil)$ (equivalently, "there is no proof of a contradiction in $T$").

This sharpens the first theorem. It is not just that $T$ fails to prove some true sentences, it specifically fails to prove the statement of its own consistency, which (if $T$ is in fact consistent) is true.

The AI-relevant implication: *an automated theorem prover that implements $T$ cannot certify its own correctness using the reasoning principles it embodies*. Certification requires a stronger system, which in turn cannot self-certify. This is an infinite regress: no axiomatizable system of any strength can produce a fully internal guarantee of its own soundness.

## 3. Löb's theorem and self-referential agents

Löb's theorem (1955) extends the Gödel framework in a direction that is particularly relevant to self-modifying AI.

**Theorem (Löb 1955).** For a theory $T$ extending Peano arithmetic, and any sentence $\phi$:

$$
T \vdash \text{Prov}_T(\lceil \phi \rceil) \to \phi \quad \text{implies} \quad T \vdash \phi.
$$

In words: if $T$ can prove "if $\phi$ is provable then $\phi$," then $T$ can prove $\phi$ outright.

**Contrapositive.** $T$ cannot prove $\phi$ unless it can prove $\phi$ without going through "$T$ proves $\phi$". $T$'s own claim that its proofs are sound is never available internally.

### 3.1 The Löbian obstacle

In the AI-alignment context, Löb's theorem has been studied as an obstacle to principled self-trust in self-modifying agents. An agent that reasons about its own future actions wants to assert things like "if my future self proves $\phi$, then $\phi$ is true." Under Löb's theorem, the agent cannot prove such conditional trust unconditionally, the conditional trust only exists when the antecedent collapses, which defeats the point.

**Yudkowsky & Herreshoff (2013)** formalized this as the **Löbian obstacle**. A self-improving AI that wants to verify the improvements it makes cannot do so via internal proof; it needs a stronger theory for verification, which itself has a Löbian obstacle, ad infinitum.

**Fallenstein, Soares, Taylor, Yudkowsky** and colleagues at MIRI subsequently proposed *modal combat agents* and *logical induction* (Garrabrant et al. 2016) as partial technical responses. These are active research areas with no fully satisfactory solution as of 2026.

## 4. The halting problem and its AI connections

Related but distinct: the **halting problem** (Turing 1936) is the undecidable question "does this program halt on this input?"

For AI: no algorithm can decide, for an arbitrary program, whether that program's execution terminates. Practical consequences:

- **No general-purpose safety analyzer.** You cannot build a verifier that decides whether a given AI program will ever enter some unsafe state.
- **Bounded verification.** Practical safety analysis must restrict to decidable fragments (bounded-step behavior, restricted program classes) or accept incompleteness (sound but incomplete verifiers).
- **Rice's theorem** (1953) generalizes this: any non-trivial semantic property of programs is undecidable. "Will this program output a harmful response?" is undecidable in the general case.

These are not arguments against AI safety, they are arguments *for* principled, restricted safety analysis rather than blanket guarantees.

## 5. What the incompleteness results mean for contemporary AI

A few honest claims:

- **For theorem provers and formal verification tools**, Gödel and Löb constrain what can be verified internally. Practical verification uses stronger meta-systems, accepts incompleteness, or uses bounded checks.
- **For learned systems (LLMs, RL agents)**, the incompleteness results apply only insofar as the system is operating as a theorem prover, which is rarely the right frame. An LLM is not a first-order theory; its "consistency" is not formally well-defined; Gödel doesn't directly apply.
- **For self-improving AI or goal-preserving modification**, the Löbian obstacle is a real technical constraint on proof-theoretic approaches, which is one (among many) reasons contemporary alignment research does not rely on proof-based self-verification.
- **For the "can AI be conscious / have understanding" debate**, Gödel's theorems are almost always misapplied.

## 6. Open questions

**Probabilistic self-reference.** Christiano et al. (2013) propose probabilistic reflection as a way around Löbian obstacles: agents assign probabilities to their own future statements rather than provability. The approach partially avoids the obstacle but has its own technical problems.

**Logical induction** (Garrabrant et al. 2016) constructs probability distributions on sentences of a formal language that converge to correct values over time, with self-referential properties that avoid the sharp Löbian traps. The framework is elegant but computationally impractical at scale.

**Verification of neural networks.** Formal verification of neural networks is an active subfield but faces the halting-problem wall for general networks. Progress is limited to restricted classes (piecewise-linear activations, bounded depth) and specific properties (local robustness).

## 7. References (verified April 2026, core papers via standard logic references)

- **Gödel, K.** (1931). *Über formal unentscheidbare Sätze der Principia Mathematica und verwandter Systeme I*. Monatshefte für Mathematik und Physik, 38, 173–198. English translation in *From Frege to Gödel* (Heijenoort 1967).
- **Löb, M. H.** (1955). *Solution of a problem of Leon Henkin*. Journal of Symbolic Logic, 20(2), 115–118.
- **Turing, A. M.** (1936). *On computable numbers, with an application to the Entscheidungsproblem*. Proceedings of the London Mathematical Society, s2-42(1), 230–265.
- **Rosser, J. B.** (1936). *Extensions of some theorems of Gödel and Church*. Journal of Symbolic Logic, 1(3), 87–91.
- **Rice, H. G.** (1953). *Classes of recursively enumerable sets and their decision problems*. Trans. AMS, 74(2), 358–366.
- **Davis, M.** (1993). *How subtle is Gödel's theorem? More on Roger Penrose*. Behavioral and Brain Sciences, 16(3), 611–612.
- **Chalmers, D.** (1995). *Minds, machines, and mathematics: a review of Shadows of the Mind by Roger Penrose*. PSYCHE, 2(9).
- **Feferman, S.** (1996). *Penrose's Gödelian argument*. PSYCHE, 2(7).
- **Yudkowsky, E., & Herreshoff, M.** (2013). *Tiling agents for self-modifying AI, and the Löbian obstacle*. MIRI technical report.
- **Fallenstein, B., & Soares, N.** (2015). *Vingean reflection: reliable reasoning for self-improving agents*. MIRI technical report.
- **Garrabrant, S., et al.** (2016). *Logical induction*. arXiv.
- **Christiano, P., Yudkowsky, E., Herreshoff, M., & Barasz, M.** (2013). *Probabilistic self-reference*. MIRI technical report.
- **Penrose, R.** (1989). *The emperor's new mind*. Oxford University Press. [For context; the arguments are rebutted by the references above.]
- **Boolos, G.** (1979). *The unprovability of consistency*. Cambridge University Press.
- **Smullyan, R. M.** (1992). *Gödel's incompleteness theorems*. Oxford University Press.
