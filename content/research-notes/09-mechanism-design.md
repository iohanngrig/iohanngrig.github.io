---
title: "Mechanism design for AI systems: eliciting truth from agents that optimize"
date: 2026-02-21
draft: false
tags: ["mechanism-design", "game-theory", "ai-safety"]
---

# Mechanism design for AI systems: eliciting truth from agents that optimize

> Mechanism design is the sub-field of economics and game theory that asks: given a population of agents with private preferences, can we design a game whose equilibria produce a socially desirable outcome? The foundational results, Myerson's optimal auction, the revelation principle, proper scoring rules, predate AI by decades but are increasingly central to how we build systems where AI agents make or report decisions. This note covers the classical framework, connects it to contemporary problems in reward modeling and AI alignment, and argues that the design of incentive-compatible reporting schemes is a load-bearing part of any system that elicits predictions, preferences, or evaluations from learned agents.

## 1. The problem

An agent, human, institution, or AI, has private information $\theta$ about some quantity we care about. The agent reports $\hat\theta$. We score the report somehow and compensate the agent accordingly. The design question: *what scoring rule makes truthful reporting $\hat\theta = \theta$ optimal for the agent?*

The naive approach, "pay more for correct answers", fails catastrophically. If we only know the truth after the fact, we can pay based on the agent's report versus the realized outcome. But unless the scoring rule is carefully designed, the agent has incentive to report the answer that maximizes expected payoff given *their private beliefs*, which is generally different from their actual beliefs.

**This is not a theoretical curiosity.** Every RLHF system, every reward model, every evaluation benchmark, every human preference dataset, and every LLM-judge pipeline is a mechanism-design problem. We are extracting signal from agents and hoping, often without checking, that the agents have no incentive to misreport.

## 2. Proper scoring rules

A **scoring rule** $S(\hat p, y)$ maps a probabilistic report $\hat p$ and a realized outcome $y$ to a number representing the agent's loss (lower is better). The rule is **proper** if, for any true belief $p$, the expected loss is minimized by reporting $\hat p = p$:

$$
\mathbb{E}_{y \sim p}\bigl[S(p, y)\bigr] \;\le\; \mathbb{E}_{y \sim p}\bigl[S(\hat p, y)\bigr] \quad \text{for all } \hat p.
$$

It is **strictly proper** if the inequality is strict unless $\hat p = p$.

The two canonical examples, both strictly proper on probability distributions over a finite outcome set:

**Brier score** (squared-error):
$$
S_{\text{Brier}}(\hat p, y) \;=\; \sum_k \bigl(\hat p_k - \mathbb{1}[y = k]\bigr)^2.
$$

**Logarithmic score**:
$$
S_{\log}(\hat p, y) \;=\; -\log \hat p_y.
$$

![Expected Brier score is minimized at truthful report](/research-notes/figures/md-fig1-proper-scoring.svg)

The figure shows the expected Brier score as a function of the reported probability $\hat p$, when the true probability is $p = 0.7$. The minimum is exactly at $\hat p = 0.7$. Any deviation, toward 0.5 (under-confident) or toward 1.0 (over-confident), raises the expected score.

**Gneiting & Raftery (2007)** give the comprehensive characterization: a scoring rule is proper iff it is induced by a convex "scoring function" on the simplex of probability distributions, with truthfulness corresponding to the function's minimum along the ray from the simplex center. Brier corresponds to Euclidean distance; log-score corresponds to Kullback-Leibler divergence.

## 3. The revelation principle

Myerson's **revelation principle** (Myerson 1979, 1981) is the foundational reduction of mechanism design.

**Principle.** Any social choice function that can be implemented by *some* mechanism where agents play strategically can be implemented by a *direct* mechanism where agents are asked to truthfully report their types.

The practical consequence: in searching for the best mechanism, we can restrict attention to direct mechanisms in which truthful reporting is a dominant strategy. This collapses an infinite-dimensional search (over all possible games) to a finite-dimensional one (over reporting protocols).

The revelation principle does *not* say truthful mechanisms always exist, just that if any mechanism achieves a given outcome, a truthful one does. Finding the actual truthful mechanism is still hard, and for many objectives it is **impossible** (Gibbard-Satterthwaite: no dictatorship-free truthful mechanism can aggregate preferences over more than two alternatives).

## 4. Myerson's optimal auction

For the canonical mechanism-design problem, selling a single item to bidders with private values, Myerson (1981) characterized the revenue-optimal auction.

**Theorem (Myerson 1981, informal).** For bidders with independent private values drawn from a regular distribution, the revenue-optimal auction is a second-price auction with a reserve price $r^\ast$ that depends on the value distribution, not on the number of bidders. The expected revenue equals the expected value of the *virtual surplus*, a transformation of bidder values that internalizes the information rent.

The technical machinery (virtual valuations, regular distributions, ironing for irregular distributions) is non-trivial but the economic content is clean: optimal revenue is about eliciting truthful valuations, and the price paid by the winner should not depend on their own bid (only on others' bids), so as to give them no incentive to shade.

## 5. Why mechanism design matters for AI

Three contemporary applications make the classical theory urgent.

### 5.1 Reward modeling and RLHF

In reinforcement learning from human feedback (Christiano et al. 2017; Ouyang et al. 2022), a reward model is trained on pairwise human preference labels $(x, y_w, y_l)$ where $y_w$ is preferred to $y_l$. The resulting reward model is used to fine-tune the LLM.

Mechanism-design question: *do human labelers have incentive to report their true preferences?* If labelers are paid per label, they have incentive to produce labels quickly, which biases toward short responses regardless of quality. If labelers are paid per "correct" label (as judged by consensus), they have incentive to report the *consensus* preference rather than their own, collapsing the information the reward model would otherwise extract.

**Bai et al. (2022)** Constitutional AI side-steps some of this by using LLM-generated critique rather than human preferences for training. But the labeler-incentive problem recurs: the critic LLM is itself a learned agent that may have systematic biases.

### 5.2 LLM-as-judge

A widespread evaluation pattern uses one LLM to judge the outputs of another. Zheng et al. (2023) document well-known biases: position bias (the first answer presented is more often picked), verbosity bias (longer answers preferred), self-enhancement bias (models prefer outputs from themselves or from the same family).

These biases are mechanism-design failures: the judge's "reporting scheme", the way its judgment is elicited, is not incentive-compatible with truthful ranking. Remedies include:
- **Swap evaluation** (judge the same pair in both orders and look for consistency).
- **Calibration against human judges** on a held-out set.
- **Cross-family judging** (never use the same model family as judge and judged).

### 5.3 Peer prediction for AI outputs

When ground-truth is unavailable, **peer prediction** methods (Miller et al. 2005; Witkowski & Parkes 2012) elicit truthful reports by rewarding agreement with peers in a way that makes truthful reporting the equilibrium. Recent applications (Schoenebeck & Yu 2023) explore peer-prediction for LLM-generated labels where no gold standard exists.

## 6. The alignment connection

Mechanism design is one of the cleanest formal frameworks for the *outer alignment* problem: how do you specify what you want from an agent in a way that makes truthful optimization align with what you actually want?

Consider a toy example. You want a language model that is helpful, honest, and harmless. You train it by fine-tuning on human preference data. The reward model that emerges defines the *elicited preferences* of the humans in the training loop, with all the biases those humans have, all the incentives the pipeline imposes, and all the coarseness of pairwise comparisons. Calling the resulting system "aligned" is an abuse of language: it is aligned with the *mechanism* you used to elicit preferences, not with any normatively grounded target.

**Gabriel (2020)** and **Leike et al. (2018)** on scalable oversight develop this theme: alignment is fundamentally a mechanism-design problem of specifying, eliciting, and aggregating preferences at scale. The classical literature on proper scoring rules and truthful mechanisms is the right starting point, but the contemporary problem has elements the classical theory never considered, most importantly, that the *agents themselves are learned systems* whose biases we are still discovering.

## 7. Open questions

**Mechanism design for non-probabilistic reports.** Proper scoring rules are elegant for probability forecasts but less developed for complex outputs (full text, code, policy decisions). Distributional scoring rules for LLM outputs are an active research area.

**Robust mechanisms under learning agents.** Classical mechanism design assumes agents are Bayesian-rational. Learned agents have systematic non-Bayesian biases. Bergemann & Morris's "robust mechanism design" line is the closest bridge but has not been fully connected to ML.

**Incentive-compatible RLHF.** The standard RLHF pipeline is not known to be incentive-compatible for labelers. What does a robust version look like? This is an underexplored connection between mechanism design and alignment.

## 8. References (verified April 2026)

- **Myerson, R. B.** (1979). *Incentive compatibility and the bargaining problem*. Econometrica, 47(1), 61–73.
- **Myerson, R. B.** (1981). *Optimal auction design*. Mathematics of Operations Research, 6(1), 58–73.
- **Gneiting, T., & Raftery, A. E.** (2007). *Strictly proper scoring rules, prediction, and estimation*. JASA, 102(477), 359–378.
- **Gibbard, A.** (1973). *Manipulation of voting schemes: a general result*. Econometrica, 41(4), 587–601.
- **Satterthwaite, M. A.** (1975). *Strategy-proofness and Arrow's conditions*. Journal of Economic Theory, 10(2), 187–217.
- **Christiano, P., Leike, J., Brown, T. B., Martic, M., Legg, S., & Amodei, D.** (2017). *Deep reinforcement learning from human preferences*. NeurIPS.
- **Ouyang, L., et al.** (2022). *Training language models to follow instructions with human feedback*. NeurIPS.
- **Bai, Y., et al.** (2022). *Constitutional AI: harmlessness from AI feedback*. arXiv.
- **Zheng, L., et al.** (2023). *Judging LLM-as-a-judge with MT-Bench and Chatbot Arena*. NeurIPS.
- **Miller, N., Resnick, P., & Zeckhauser, R.** (2005). *Eliciting informative feedback: the peer-prediction method*. Management Science, 51(9), 1359–1373.
- **Gabriel, I.** (2020). *Artificial intelligence, values, and alignment*. Minds and Machines, 30, 411–437.
- **Leike, J., et al.** (2018). *Scalable agent alignment via reward modeling: a research direction*. arXiv.
- **Roughgarden, T.** (2016). *Twenty lectures on algorithmic game theory*. Cambridge University Press.
