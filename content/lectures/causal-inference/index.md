---
title: "Lectures on causal inference"
description: "Twelve-chapter graduate-level textbook: from Neyman-Rubin potential outcomes to modern ML-augmented causal inference."
---

# Lectures on causal inference

A twelve-chapter graduate textbook, written from scratch. The series builds sequentially from the Neyman-Rubin potential-outcomes framework to modern machine-learning-augmented causal inference. Each chapter contains: intended learning outcomes, a suggested 3-lecture plan, formal theorems with proofs, numbered equations, Python code with `numpy / scikit-learn / statsmodels / econml / dowhy / pgmpy`, synthetic worked examples, and graded exercises.

*Target reader: strong first-year PhD student in statistics, economics, or machine learning.*

---

## Part I, Foundations

- **[Chapter 1 · Potential outcomes and causal estimands](/lectures/causal-inference/01-potential-outcomes).** Neyman-Rubin framework, ATE/ATT/CATE, the fundamental problem, Neyman's 1923 variance formula, Fisher's randomization test, SUTVA.
- **[Chapter 2 · Identification](/lectures/causal-inference/02-identification).** Strong ignorability, g-formula proof, the Rosenbaum-Rubin propensity-score theorem, identification vs. estimation, sensitivity analysis with $\Gamma$-bounds and E-values.
- **[Chapter 3 · DAGs and the do-calculus](/lectures/causal-inference/03-dags-docalculus).** d-separation, backdoor and frontdoor criteria, Pearl's three rules, Shpitser-Pearl identification algorithm.

## Part II, Classical estimation

- **[Chapter 4 · Randomized experiments](/lectures/causal-inference/04-randomized-experiments).** Design choices, Neyman allocation, CUPED variance reduction with identity proof, cluster-randomized inference.
- **[Chapter 5 · Regression adjustment and weighting](/lectures/causal-inference/05-regression-weighting).** Outcome regression, IPW, AIPW with double-robustness proof, matching.
- **[Chapter 6 · Instrumental variables](/lectures/causal-inference/06-instrumental-variables).** 2SLS, the Imbens-Angrist LATE theorem with full proof, weak-instrument diagnostics, control functions.

## Part III, Panel data and staggered designs

- **[Chapter 7 · Difference-in-differences](/lectures/causal-inference/07-did).** Parallel trends, Goodman-Bacon decomposition, Callaway-Sant'Anna, the heterogeneous-effects revolution.
- **[Chapter 8 · Regression discontinuity](/lectures/causal-inference/08-regression-discontinuity).** Sharp and fuzzy RD, local linear regression, CCT bias correction, McCrary density test.
- **[Chapter 9 · Synthetic control](/lectures/causal-inference/09-synthetic-control).** Abadie-Diamond-Hainmueller, placebo inference, generalized SCM, synthetic DiD (Arkhangelsky et al. 2021).

## Part IV, Modern ML-augmented causal inference

- **[Chapter 10 · Double machine learning](/lectures/causal-inference/double-machine-learning).** Neyman orthogonality, cross-fitting, rate conditions. The bridge between classical identification and modern ML estimation.
- **[Chapter 11 · Causal forests](/lectures/causal-inference/11-causal-forests).** Honest-split trees, Wager-Athey consistency theorem, generalized random forests, policy learning.
- **[Chapter 12 · Bayesian causal inference](/lectures/causal-inference/12-bayesian-causal).** Rubin's Bayesian potential outcomes, BART (Hill 2011), Bayesian Causal Forests (Hahn-Murray-Carvalho 2020), Bayesian sensitivity analysis.

---

Return to the [Lectures hub](/lectures/) for quantum computing and AGI foundations series.
