---
title: "When majority vote works: a probability-gap theory of self-consistency"
date: 2026-06-28
draft: false
tags: ["llm", "test-time-scaling", "self-consistency", "reliability"]
---

# When majority vote works: a probability-gap theory of self-consistency

> Self-consistency samples several answers from a language model and returns the plurality. It reliably improves reasoning accuracy, and a large literature now spends inference compute adaptively by estimating how *hard* each prompt is. The premise of this note is that the difficulty proxy is unnecessary: for a model with accessible token probabilities and a prompt with a canonical answer, difficulty is a one-line measurement on the model's own conditional distribution, and that measurement determines whether sampling helps at all, how many samples it needs, and which intervention to reach for when it does not.

## 1. The setup

Fix a model $p_\theta(\cdot \mid x, T)$ over answer strings for prompt $x$ at temperature $T$, truncated to a finite answer set $\mathcal A(x)$ so that $p_\theta$ is a genuine probability measure. Let $y^\star(x)$ be the canonical answer. Define the **probability gap**

$$
\gamma(x, T) \;=\; p_\theta\!\bigl(y^\star \mid x, T\bigr) \;-\; \max_{y \neq y^\star}\, p_\theta\!\bigl(y \mid x, T\bigr).
$$

The gap is positive exactly when the correct answer is the *mode* of the answer distribution. It is measurable directly by forced decoding: teacher-force each candidate string and read off its sequence log-probability, one forward pass per candidate, no sampling. Self-consistency draws $Y_1, \dots, Y_n$ i.i.d. and returns the plurality $\widehat y_n$.

The point of writing the gap down is that everything below is a statement about this one measured quantity, not about a latent "difficulty" accessed through a learned probe.

## 2. The gap controls the sample budget

> **Sample-complexity bound.** If $\gamma := \gamma(x, T) > 0$, then for any $\delta \in (0,1)$, drawing
> $$ n \;\ge\; \frac{2\log(2/\delta)}{\gamma^2} $$
> samples makes plurality voting return $y^\star$ with probability at least $1 - \delta$.

The argument is one application of Hoeffding's inequality to the pairwise vote margin against the strongest competitor. Let $y^\dagger$ be that competitor with mass $p_2$, and write $Z_i = \mathbb 1[Y_i = y^\star] - \mathbb 1[Y_i = y^\dagger] \in \{-1,0,1\}$ with $\mathbb E[Z_i] = p_1 - p_2 = \gamma$. The plurality loses to $y^\dagger$ only if $\frac1n\sum_i Z_i \le 0$, which Hoeffding bounds by $\exp(-n\gamma^2/2)$. With a single dominant competitor (the two-outcome case), bounding the total failure probability by $2e^{-n\gamma^2/2}$ and setting it $\le \delta$ gives the stated $n$; the general $K$-competitor bound $n \ge (2/\gamma^2)\log(K/\delta)$ is recorded in Section 6, and the displayed bound is its $K=2$ case.

Two things make this useful rather than ornamental. It is **per-prompt**: the budget depends only on *this* prompt's measured $\gamma$, not on a dataset average. And it is **checkable**: at $n^\star = \lceil 2\log(2/\delta)/\gamma^2\rceil$ the empirical error should not exceed $\delta$, so the bound is falsifiable on the model in front of you. Dataset-averaged scaling laws for self-consistency give a structurally similar $\gamma^{-2}$ rate but cannot tell you what to do with a single prompt.

## 3. The negative-gap impossibility

The non-obvious half is what happens when the gap is negative.

> **Impossibility.** If $\gamma(x, T) < 0$, then $\Pr[\widehat y_n = y^\star] \to 0$ as $n \to \infty$.

A negative gap means some wrong answer $y^\dagger$ has more mass than $y^\star$. By the law of large numbers the empirical vote shares converge almost surely to the true probabilities, so the plurality converges to $y^\dagger \neq y^\star$. **More samples make self-consistency worse, not better**: the method concentrates, with increasing confidence, on a confident wrong answer. No sampling budget rescues a prompt the model is confidently wrong about. Only a change to the conditional distribution, through temperature, a prompt transformation, or external information, can move the gap.

This single sign flip is why "spend more compute" is not a universal recipe. It is a recipe for the positive-gap regime and a trap in the negative-gap regime, and the two are distinguishable by a measurement you can take before spending anything.

## 4. Three regimes and a decision rule

The sign of the gap, across an accessible set of temperatures $\mathcal T$, partitions prompts into three operationally distinct classes.

* **Solvable.** $\gamma(x, 1) > 0$. Self-consistency converges at the rate of Section 2; greedy decoding is often already correct.
* **Recoverable.** $\gamma(x, 1) \le 0$ but $\gamma(x, T') > 0$ for some $T' \in \mathcal T$. Plain voting at $T = 1$ fails, but tempering or a transformation restores a positive gap.
* **Unrecoverable.** $\gamma(x, T) \le 0$ for all $T \in \mathcal T$. No temperature makes $y^\star$ modal; sampling provably cannot succeed, and only new information will help.

The decision rule writes itself, and it is the practical payoff: solvable prompts get greedy or small-$n$ voting; recoverable prompts get tempered or transformed, then voting; unrecoverable prompts should not receive a sampling budget at all, they need retrieval, tools, or a different prompt. This gives a concrete reason for the recurring finding that no test-time strategy dominates across a benchmark: the optimal strategy is regime-dependent, and the regime is measurable.

## 5. What a transformation buys

Let $\mathcal S(x, T) = p_\theta(y^\star \mid x, T)$ be the truth mass. For a transformation $\tau$ (a chain-of-thought cue, a few-shot block, retrieved context) the **specialization gain** is

$$
\Delta_{\mathcal S}(\tau; x, T) \;=\; \mathcal S(\tau(x), T) - \mathcal S(x, T),
$$

two forced-decoding passes. The framework predicts a regime-dependent ranking, consistent with experiments on open-weight models: recoverable prompts gain most from a reasoning cue (it unlocks a latent positive gap), unrecoverable prompts gain only from retrieval (only new information flips a uniformly negative gap), and solvable prompts have $\Delta_{\mathcal S} \approx 0$ because they are already at ceiling. A transformation can move a prompt from recoverable to solvable; it cannot move one from unrecoverable to solvable unless it injects information. This is the precise sense in which chain-of-thought helps reasoning but not missing facts.

## 6. A refinement: measure the empirical margin, not the population gap

The forced-decoded gap of Section 1 is the clean object for theory, but on short-answer tasks it is not the best *estimator* of reliability. The **empirical sample margin**, the normalized vote-count difference between the top correct and top incorrect answers in the sample you already drew, empirically ranks prompts by majority-vote error better than the forced-decoded population gap. There are two reasons. The margin is the statistic the plurality rule actually thresholds at zero, so it is the natural scalar for ranking prompts by how decisively the vote will resolve. And it is robust to surface-form fragmentation, where one semantic answer is split across several string variants that forced decoding scores as separate competitors; counting over merged samples repairs this, whereas a forced-decoded gap between raw strings does not. The population-gap theorem is the two-outcome special case of the $K$-outcome bound $n \ge (2/\gamma^2)\log(K/\delta)$, and the regime partition is unchanged. The two measurements are complementary, not competing: the forced-decoded gap is the cheap pre-sampling screen that sets the regime and the budget, and the sample margin is the post-sampling refinement that ranks residual reliability once the samples are in hand. The empirical claim that the margin ranks prompts better is established in the companion paper, not here.

## 7. Where the theory stops

* **Tokenizer dependence.** The gap is defined on the model's own answer tokenization; a paraphrase or a different canonical-form normalization changes it. Robustness checks against paraphrases and a validated answer-equivalence relation are not optional.
* **Canonical-answer assumption.** Everything here needs a well-defined $y^\star$ and a finite competitor set. Open-ended generation requires a semantic equivalence judge, which is itself an error source to be validated on a labeled subset.
* **It is a claim about the model's distribution, not the world.** The bound governs whether voting recovers the *model's* modal answer. If the mode is wrong (the unrecoverable regime) the theory tells you to stop sampling, not how to be right.
* **Cost crossover.** Direct gap measurement beats sampling only once the voting budget exceeds a handful of candidates; for tiny budgets, just sample.

## 8. Why this framing is the right one

The dominant practice estimates per-prompt difficulty through a proxy, an activation probe, a reasoning-path feature, a sub-question uncertainty score, and then allocates compute. The argument here is that the target quantity is not latent. It is a measurement on the conditional distribution, it provably controls the sampling budget with a matching impossibility on the other side of zero, and it induces a decision rule that says when to sample, when to temper, and when to stop. Proxies should be calibrated *against* it, not used in its place. In test-time scaling, measure the gap; do not estimate a proxy for it.

## References

* Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., & Zhou, D. (2023). *Self-consistency improves chain-of-thought reasoning in language models.* ICLR.
* Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D. (2022). *Chain-of-thought prompting elicits reasoning in large language models.* NeurIPS.
* Kojima, T., Gu, S., Reid, M., Matsuo, Y., & Iwasawa, Y. (2022). *Large language models are zero-shot reasoners.* NeurIPS.
* Hoeffding, W. (1963). *Probability inequalities for sums of bounded random variables.* JASA, 58(301), 13–30.
* Massart, P. (2007). *Concentration inequalities and model selection.* Springer (for the multinomial mode-identification rate).

*The probability-gap framing and the three-regime decision rule in this note are the subject of a separate technical paper; this is the plain-language companion. All experiments referenced use open-weight models and public reasoning benchmarks.*
