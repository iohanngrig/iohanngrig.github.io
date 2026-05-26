---
title: "The scaling hypothesis: evidence for and against"
date: 2026-02-28
draft: false
tags: ["scaling", "llm", "agi"]
---

# The scaling hypothesis: evidence for and against

> The **scaling hypothesis** is the claim that capability improvements in large language models and related systems follow predictable power-law relationships with compute, data, and parameters, and that continued scaling will continue to produce capability gains. Between 2020 and 2024, the evidence was remarkably strong. Since 2024 the picture has become more complicated. This note covers the empirical foundations (Kaplan 2020, Hoffmann 2022), the critique (Schaeffer 2023, emergent-abilities revisionism), the separate question of whether scaling produces AGI, and what we can honestly say about the next 10× of compute.

## 1. The empirical law

**Kaplan et al. (2020)** empirically established the scaling law for transformer language models. They found that validation loss follows a power law in model parameters $N$, training tokens $D$, and compute budget $C$, over *seven orders of magnitude*:

$$
L(N, D) \;\approx\; \left(\frac{N_c}{N}\right)^{\alpha_N} + \left(\frac{D_c}{D}\right)^{\alpha_D} + L_\infty,
$$

with $\alpha_N \approx 0.076$ and $\alpha_D \approx 0.095$ in their experiments. The law holds across dataset sizes, model widths, and architectural details, which itself was a striking finding.

![Scaling laws: Kaplan vs. Hoffmann vs. hypothetical saturation](/research-notes/figures/scaling-fig1-laws.svg)

**Hoffmann et al. (2022)**, the Chinchilla paper, revised the allocation question. They trained 400+ models at varying $N$ and $D$, found that Kaplan's original law had under-weighted data, and proposed that for compute-optimal training, $N$ and $D$ should be scaled *proportionally*: doubling compute means doubling both model size and training tokens. The Chinchilla finding implied that most contemporary models (GPT-3, Gopher) were substantially *undertrained* for their parameter count, they had been sized per Kaplan, not per Hoffmann.

This was a cheap-feeling empirical result with large practical implications. A 70B-parameter Chinchilla model trained on 1.4T tokens substantially outperformed 530B Megatron-Turing NLG trained on 270B tokens, despite having ~13% of the parameters. The compute allocation matters as much as the total compute.

## 2. What scaling laws actually predict

The scaling laws predict *loss*, specifically, validation cross-entropy on a held-out distribution similar to training. They do *not* directly predict:

- **Downstream task accuracy.** Loss translates to accuracy via task-specific transformations that may be nonlinear.
- **Emergence of qualitatively new capabilities.** A smooth loss curve can hide discrete capability jumps.
- **Generalization out of distribution.** Scaling laws are fit on in-distribution validation; deployment is OOD.
- **Robustness and reliability.** Scaling a model does not necessarily make it more robust; in some cases the opposite.

Forgetting these caveats produces the overreaching version of the scaling hypothesis: *"just scale more and all problems will solve themselves."* This reading is not supported by the empirical literature even when the empirical literature is most supportive.

## 3. The emergent-abilities controversy

**Wei et al. (2022)**, also lead authors of the chain-of-thought paper, introduced **emergent abilities**: capabilities that are absent in smaller models, present in larger models, and *not predictable by extrapolating the smaller models' performance curves*. Examples: arithmetic, chain-of-thought, multi-step reasoning.

![Illustration of the Wei et al. framing vs. Schaeffer et al. rebuttal](/research-notes/figures/cot-fig1-scaling.svg)

The finding was influential and contributed to the expectation that "one more order of magnitude" of compute would unlock new capabilities.

**Schaeffer, Miranda & Koyejo (2023)**, *Are Emergent Abilities of Large Language Models a Mirage?*, argued that many reported emergent abilities are artifacts of the evaluation metric. Specifically:

1. For tasks scored by exact-match accuracy (binary: right or wrong), the measured capability curve looks sharp even if the underlying log-probability of the correct answer is improving smoothly.
2. Under smoother metrics, e.g., token-level log-likelihood, or partial-credit accuracy, the apparent emergence flattens into a smooth power-law improvement.
3. Their three empirical tests confirm this across InstructGPT/GPT-3 on BIG-Bench and across vision tasks.

This does *not* invalidate the claim that large models have capabilities small models lack. It reframes the claim: the capabilities improve smoothly with scale; they cross task-specific thresholds at particular scales; and some metrics are sensitive to those thresholds while others are not.

**Implication for scaling hypothesis:** "unpredictable emergence" is partially a measurement artifact. The smooth power-law view is *more* consistent with the scaling hypothesis, not less, but also less exciting as a forecasting tool, because predicting *when* a model will cross a task-threshold is different from predicting that it will.

## 4. What 2024–2026 has revealed

Several threads of evidence complicate the simple "keep scaling" narrative.

### 4.1 Diminishing empirical returns

Multiple reports from industry labs indicate that flagship models in 2024–2026 show smaller per-dollar capability gains than the 2020–2023 generation. The data underlying these reports is often not public, but the consistency of the signal across labs is notable.

Several explanations are plausible:

- **Data scarcity.** High-quality text data is finite; the frontier of useful training data has largely been exhausted. Synthetic data partially substitutes but has its own failure modes.
- **Architectural limits.** Standard transformers may be approaching a regime where additional parameters add less per-parameter capability. Mixture-of-experts, state-space models, and other architectural innovations are being tested.
- **Task-threshold saturation.** Tasks with clear thresholds (arithmetic, code completion) have already crossed; the remaining headroom is in tasks where scaling alone helps less.

### 4.2 The compute-efficient Pareto frontier

Chinchilla-scaling already said: allocate compute between parameters and data. The 2024-2026 picture is that this allocation interacts with training techniques:

- **RLHF / DPO.** Post-training alignment is cheap relative to pretraining and produces large usability gains. This shifts the effective frontier.
- **Chain-of-thought and process supervision.** Models trained with explicit reasoning objectives are more reasoning-capable than same-size models trained without, at negligible cost. Again, frontier shift.
- **Inference-time compute** (o1-style reasoning). Spending compute at inference rather than training moves the frontier further, and inference-time scaling has its own laws that are still being characterized.

The scaling hypothesis needs to be updated: *capability* scales with *effectively-used compute*, not raw compute. The transformation between the two is the thing that moved the most between 2022 and 2026.

## 5. Does scaling imply AGI?

This is the contested question. Three positions, each held by serious people:

**Strong scaling hypothesis (Sutskever, Amodei, various).** Continued scaling, with appropriate post-training, will produce systems that are effectively AGI. The constraints are compute, data, and engineering, not a missing algorithmic insight. Evidence: the remarkable empirical success of 2018–2023 scaling, the absence of clear diminishing-returns ceilings in the public record.

**Weak scaling hypothesis (most practitioners).** Scaling will continue to produce capability improvements but AGI requires architectural or objective-level changes. Current transformers trained with next-token prediction are not on a direct path to AGI; they are on a path to very capable but bounded systems.

**Anti-scaling position (Marcus, LeCun, Mitchell, various).** Language models trained with next-token prediction cannot, in principle, achieve AGI because they lack world models, grounded perception, or other faculties that human intelligence requires. Scaling is pushing a capable but fundamentally limited system.

Which position the evidence supports depends on what *AGI* means. For "matching human performance on a broad battery of benchmarks," the strong position is at least not yet falsified. For "producing systems with the flexible, sample-efficient, world-model-using intelligence of a 5-year-old human," the evidence substantially favors the weak or anti-scaling positions.

## 6. What to believe, honestly

- The scaling laws are real and have been replicated.
- The original Kaplan allocation was wrong; Chinchilla's proportional-scaling is the better guide.
- Emergent-abilities claims are partially metric artifacts; the underlying capability improvements are smoother than the headline curves.
- Post-training (RLHF, DPO, CoT, process supervision) has been more valuable than most expected in 2020.
- Whether scaling continues to produce capability improvements at 10× more compute is an empirical question that will be answered in the next 3–5 years.
- Whether scaling produces AGI is contested and likely requires a different kind of evidence than scaling laws can provide.

The honest posture: strong expectations that scaling will continue to produce useful capability improvements; skeptical of both "AGI is imminent" and "scaling has stopped" claims, because neither has good evidence; focused on the engineering frontier of effectively-used compute.

## 7. References (verified April 2026)

- **Kaplan, J., McCandlish, S., Henighan, T., et al.** (2020). *Scaling laws for neural language models*. arXiv. [S.S. `e6c561d0`]
- **Hoffmann, J., Borgeaud, S., Mensch, A., et al.** (2022). *Training compute-optimal large language models*. NeurIPS. [S.S. `8342b592`]
- **Wei, J., Tay, Y., Bommasani, R., et al.** (2022). *Emergent abilities of large language models*. TMLR.
- **Schaeffer, R., Miranda, B., & Koyejo, S.** (2023). *Are emergent abilities of large language models a mirage?* NeurIPS. [S.S. `29c7f009`]
- **Brown, T. B., Mann, B., Ryder, N., et al.** (2020). *Language models are few-shot learners*. NeurIPS.
- **Henighan, T., et al.** (2020). *Scaling laws for autoregressive generative modeling*. arXiv.
- **Tamay Besiroglu et al.** (2023). *Epoch AI scaling trend datasheets*. Epoch.
- **Marcus, G., & Davis, E.** (2019). *Rebooting AI*. Pantheon.
- **LeCun, Y.** (2022). *A path towards autonomous machine intelligence*. Position paper.
