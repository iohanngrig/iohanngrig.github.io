---
title: Research Notes
---

# Research Notes

*A working library on the methodological foundations of causal identification, agent-driven decision systems, the contemporary LLM-and-agent frontier, and the mathematical foundations of intelligence.*

## Editorial stance

These notes exist because the gap between a *method* and its *valid application* is where most applied ML goes wrong. A causal forest fit to panel data can return wrong-sign treatment effects; a difference-in-differences regression with staggered adoption can assign negative weights; an LLM agent that scores 95% on a benchmark can fail catastrophically on a distributionally-similar production task; a self-improving system reasoning about its own correctness runs into Löbian obstacles that are 70 years old. The notes below treat each topic with the care required to know *when the method works, when it fails, and what the current research frontier has to say about the boundary*.

Every note is written at the level of a strong first-year PhD student. Math is present but motivated. Each formal result is accompanied by an intuition, a failure mode, and a reference to the primary source. Visualizations are deliberately simple, a single good figure beats a wall of plots. Every citation has been verified via Semantic Scholar at time of writing, and the notes are updated when a significant new result appears.

## Curatorial logic

Thirty-three notes in five thematic groups.

**A. Causal methodology** (notes 1–4). The classical foundations of causal identification and their recent revolutions.

**B. Agents and reliability** (notes 5–8, 29, 31). What LLM agents actually do, how they fail, how they are evaluated, and what provides principled uncertainty quantification.

**C. Foundations of intelligence as optimization** (notes 9–12, 30, 32, 33). Mechanism design, multi-agent dynamics, scaling laws, and the alignment problem, the four framings of "how do we get desirable behavior out of optimizing systems."

**D. AGI foundations and fundamental limits** (notes 13–16). The mathematical results that bound what any artificial intelligence can do, regardless of architecture or scale.

**E. Quantum computing and complexity** (notes 17–28). What quantum algorithms can provably do, what near-term hardware has demonstrated, and where the hype exceeds the proofs.

## A. Causal methodology

### 1. Double Machine Learning: Neyman orthogonality and the cross-fitting cure
[Read →](/research-notes/01-double-machine-learning)

Plugging a machine-learning predictor into a classical causal estimating equation yields biased estimates and invalid confidence intervals, a failure that does not vanish with more data. Chernozhukov et al. (2018) give a two-part repair: construct a Neyman-orthogonal score, and cross-fit so the score is evaluated on data the nuisance estimator has never seen. Derivation from scratch, 540-replication Monte Carlo, failure modes.

### 2. Causal forests and the honest tree
[Read →](/research-notes/02-causal-forests)

Wager & Athey (2018) proved pointwise consistency and asymptotic normality for a random forest estimating heterogeneous treatment effects, the first nonparametric method with valid pointwise confidence intervals. The key innovation is **honest splitting**: data used to choose tree structure must be disjoint from data used to estimate leaf values.

### 3. The DiD revolution: heterogeneous effects and staggered adoption
[Read →](/research-notes/03-did-revolution)

Between 2018 and 2024, four research groups independently showed that the two-way fixed effects estimator is biased when treatment effects are heterogeneous. Goodman-Bacon decomposition, Callaway-Sant'Anna, de Chaisemartin-D'Haultfœuille, Sun-Abraham, Borusyak-Jaravel-Spiess, the practical replacement toolkit.

### 4. Quantile treatment effects: estimands, identification, and a panel-data pitfall
[Read →](/research-notes/04-qte)

A quantile treatment effect at level $\tau$ is *not* the treatment effect for units at the $\tau$-th percentile. Firpo-Fortin-Lemieux RIF regression separates unconditional from conditional estimands. The pitfall of conflating the two in panel settings with fixed effects.

## B. Agents and reliability

### 5. LLM agents as decision systems: a skeptic's guide
[Read →](/research-notes/05-llm-agents)

ReAct, Reflexion, SWE-agent: the agent literature moved from prototype to production in three years. The gap between benchmark performance and reliable deployment is large and systematic. GAIA, SWE-bench, and a working taxonomy of agent errors.

### 6. Conformal prediction: distribution-free uncertainty that finally works
[Read →](/research-notes/06-conformal)

Conformal wrapping gives any prediction model a finite-sample coverage guarantee under only exchangeability. The marginal vs. conditional coverage caveat, conformalized quantile regression, and adaptive conformal under distribution shift.

### 7. Chain-of-thought reasoning and its limits
[Read →](/research-notes/07-chain-of-thought)

CoT prompting improves reasoning on large models but its *apparent* reasoning often doesn't match its actual computation. Saparov-He, Turpin et al., Lanham et al., the literature of unfaithful chain-of-thought. When CoT works, why, and what it doesn't do.

### 8. Retrieval-augmented generation: the reliability story
[Read →](/research-notes/08-rag)

RAG is the dominant pattern for factual LLM applications. The three failure modes (retrieval miss, index staleness, context pollution), the reliability toolkit (reranking, query rewriting, grounded generation, conformal wrapping), and why "RAG ≠ agent."

### 29. When majority vote works: a probability-gap theory of self-consistency
[Read →](/research-notes/29-self-consistency)

Self-consistency samples several answers and returns the plurality. A per-prompt probability gap, measurable by forced decoding, controls the sample budget ($n \ge 2\log(2/\delta)/\gamma^2$), comes with a matching impossibility when the gap is negative (more samples make it worse), and partitions prompts into three regimes with a decision rule for when to sample, temper, or stop. Companion to a separate technical paper.

### 31. How far synthetic users can take you: validity ceilings and a screening test
[Read →](/research-notes/31-synthetic-users)

Silicon-sample agents as a pre-experimental screen. An attenuation ceiling caps synthetic-to-human fidelity at the outcome's own reliability ($\rho_{ah}\le\rho_{tt}<1$); synthetic panels under-state effects by $1/\sqrt{\eta}$ with effective sample size $n_{\text{eff}}\le K$, not $KM$; and a fidelity floor says exactly when a keep/kill verdict is trustworthy and when to run the live test.

## C. Foundations of intelligence as optimization

### 9. Mechanism design for AI systems: eliciting truth from agents that optimize
[Read →](/research-notes/09-mechanism-design)

Every RLHF system is a mechanism-design problem. Proper scoring rules, the revelation principle, Myerson's optimal auction, and why the classical theory is load-bearing for contemporary alignment work.

### 10. Multi-agent coordination and emergent behavior
[Read →](/research-notes/10-multi-agent)

Nash equilibria, the PPAD-complete complexity of finding them, and the empirical dynamics of multi-agent learning. Prisoner's dilemma, social dilemmas, self-play in zero-sum games, emergent communication, and why cooperation rarely emerges from naive RL.

### 11. The scaling hypothesis: evidence for and against
[Read →](/research-notes/11-scaling-hypothesis)

Kaplan 2020, Hoffmann/Chinchilla 2022, the emergent-abilities debate, and what 2024–2026 has revealed about diminishing returns. Honest accounting of what scaling laws predict and what they do not.

### 12. The alignment problem: formal statements and honest limits
[Read →](/research-notes/12-alignment)

Outer vs. inner alignment, mesa-optimization, scalable oversight, reward hacking. The post-training stack (SFT, RLHF, DPO, CAI, process reward) and what it does and does not fix.

### 30. Paying for the unseen task: multitask contracts and the cost of a missing signal
[Read →](/research-notes/30-multitask-contracts)

Holmström-Milgrom multitask agency, where rewarding one task crowds out a complementary unrewarded one. A partially pooled bonus recovers the missing task; the free-rider attenuation term $\alpha + (1-\alpha)/N$ falls out of the equilibrium effort, and the optimal pooling weight is a noise-versus-incentive trade. Mechanism-design strand of the research agenda.

### 32. Good-enough elasticities: why allocation regret is second-order in estimation error
[Read →](/research-notes/32-allocation-regret)

Allocating a budget across power-law response curves. The optimum is closed-form water-filling, and because the objective is flat to first order there, realized regret is $\Theta(\varepsilon^2)$ in elasticity-estimation error (the envelope theorem in disguise). Past a modest accuracy, sharpening estimates buys almost nothing; concavity and feasibility bind instead.

### 33. The dashboard fell but nothing happened: measurement neutrality and guardrail instability
[Read →](/research-notes/33-guardrail-instability)

Recalibrating a value signal shrinks reported value but, with no platform response, leaves real delivery unchanged, a neutrality and non-identifiability theorem. An automated efficiency-ratio guardrail nonetheless turns that accounting change into a real spend and click cut unless its target is rescaled by the same factor. Goodhart's law instantiated in an autobidding stack.

## D. AGI foundations and fundamental limits

### 13. Gödel, Löb, and the formal limits of self-referential AI
[Read →](/research-notes/13-godel-lob)

Gödel's incompleteness, Löb's theorem, the Löbian obstacle in self-modifying agents. What the classical limitative results do say, what they do not say (the Penrose argument fails), and why they matter for contemporary AI safety.

### 14. AIXI, Solomonoff induction, and the mathematics of universal intelligence
[Read →](/research-notes/14-aixi)

Hutter's AIXI combines universal Solomonoff prediction with Bellman-optimal planning to define provably optimal intelligence in an uncomputable form. Legg-Hutter intelligence measure, Monte Carlo approximations, and what this framework contributes to AGI discussions.

### 15. World-model approaches to AGI
[Read →](/research-notes/15-world-models)

From Ha-Schmidhuber to DreamerV3 to JEPA. The case for learning a compact internal model of the environment that supports planning-by-imagination. Sample-efficiency evidence, the LLM-as-implicit-world-model question, and LeCun's AGI proposal.

### 16. Computational irreducibility and the limits of optimization
[Read →](/research-notes/16-computational-irreducibility)

Three deep negative results: No-Free-Lunch, computational irreducibility, PAC lower bounds. What these do and do not imply for AI, and why "smarter AI" does not bypass them.

## E. Quantum computing and complexity

### 17. Quantum computing for constrained optimization, what's proved, what's hoped
[Read →](/research-notes/17-quantum-optimization)

A careful separation of three questions: what quantum algorithms can provably do faster, what near-term hardware has demonstrated, and what this means for operations-research-style optimization. Shor, Grover, QAOA, adiabatic, NISQ reality, the Sycamore/Jiuzhang supremacy debate, and an honest-limits bibliography. Flagship of the quantum series.

### 18. Adiabatic theorem and gap scaling
[Read →](/research-notes/18-adiabatic-theorem)

Why the adiabatic theorem is quantum computing's favorite sword, and where its blade gets dull. Born-Fock, Jansen-Ruskai-Seiler bounds, Landau-Zener transitions, and why worst-case 3-SAT causes exponential-gap closures (Altshuler-Krovi-Roland 2010).

### 19. Grover's algorithm and amplitude amplification
[Read →](/research-notes/19-grover-amplitude)

The quadratic speedup on unstructured search, why the BBBV 1997 lower bound makes it optimal, and what the Brassard-Høyer-Mosca-Tapp 2002 amplitude-amplification generalization gives you.

### 20. Shor's algorithm and quantum factoring
[Read →](/research-notes/20-shor-factoring)

The one quantum algorithm with a proven exponential speedup over best known classical. Period finding via QFT, the 20-million-qubit estimate for RSA-2048 (Gidney-Ekerå 2021), and NIST's post-quantum cryptography response.

### 21. HHL and quantum linear systems, where the small print matters
[Read →](/research-notes/21-hhl-linear-systems)

The Harrow-Hassidim-Lloyd algorithm and why its advertised exponential speedup collapses under realistic input/output assumptions. Aaronson's fine-print criteria and how Tang-style dequantization has limited the scope.

### 22. Variational quantum eigensolvers (VQE) and their siblings
[Read →](/research-notes/22-vqe-variational)

Why VQE dominates NISQ-era chemistry despite no proven asymptotic advantage. Hardware-efficient vs. chemistry-inspired ansatz, the McClean 2018 barren-plateau result, and comparison with CCSD(T), DFT, DMRG.

### 23. Quantum annealing and the D-Wave saga
[Read →](/research-notes/23-quantum-annealing)

A decade of D-Wave benchmark claims and their classical-community rebuttals. The Rønnow 2014 Science result, embedding overhead, and what quantum annealing does and does not genuinely provide.

### 24. Quantum error correction and the fault-tolerance threshold
[Read →](/research-notes/24-quantum-error-correction)

Why 'just add more qubits' underestimates the engineering problem by three orders of magnitude. Shor/Steane codes, the threshold theorem, surface-code overhead, and the Megaquop roadmap (Preskill 2025).

### 25. Boson sampling and photonic quantum advantage
[Read →](/research-notes/25-boson-sampling)

The Aaronson-Arkhipov 2011 proposal, Jiuzhang 2020 experiment, and why sampling-based supremacy has held up better than circuit-based supremacy. Permanent-of-Gaussians conjecture and the polynomial-hierarchy argument.

### 26. BQP and the complexity-class zoo
[Read →](/research-notes/26-bqp-complexity-classes)

Where BQP sits: above BPP, probably below NP in the worst case, and comfortably inside PSPACE. Bernstein-Vazirani containments, Toda 1991, the Raz-Tal 2019 oracle separation, and implications for quantum advantage claims.

### 27. Dequantization and the Tang algorithms
[Read →](/research-notes/27-dequantization)

How Ewin Tang's 2018 undergraduate work erased an exponential speedup in quantum recommender systems, and what the broader dequantization program tells us about quantum-ML advantage claims. The Aaronson litmus test applied.

### 28. Quantum Monte Carlo and amplitude-estimation speedups
[Read →](/research-notes/28-quantum-monte-carlo)

Where quadratic quantum speedup plausibly applies to finance and risk: Monte Carlo estimation. The Montanaro 2015 framework, amplitude estimation, option-pricing speedups, and realistic deployment timelines.

## How these notes are used

- **Self-contained.** You can read any one without the others.
- **Cross-linked.** Related concepts link to each other via Quartz's graph view.
- **Updated.** I revise notes when a significant new result appears.
- **Honest about limits.** Each note ends with *Open questions*, genuinely unresolved points.
- **Reproducible.** All figures are generated by Python scripts with fixed random seeds, available in the accompanying code.

## What these notes are NOT

- Not a textbook substitute. For that: Hernán & Robins (2020) *Causal Inference: What If*; Sutton & Barto (2018) *Reinforcement Learning: An Introduction*; Hutter (2005) *Universal Artificial Intelligence*; Angelopoulos, Barber & Bates (2024) *Theoretical Foundations of Conformal Prediction*.
- Not promotional summaries of recent papers. The goal is *understanding*, not hype.
- Not a venue for my current research. My applied work has its own publication channel; these notes are pedagogical.
