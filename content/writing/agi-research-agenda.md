---
title: "The AGI foundations research agenda: what's real, what's speculation, what I would invest in"
date: 2026-04-25
description: "An opinionated map of the contemporary AGI research landscape, separating genuine progress from benchmark inflation and sketching a five-year investment thesis."
tags: [writing, agi, research-agenda]
draft: false
---

The AGI discourse of the last three years has been simultaneously the most substantive and the least serious public conversation I have seen in applied AI. Billions of dollars are moving on narrative rather than evidence. Research careers are being built on hype trajectories that will not sustain their current pace for another three years. At the same time, genuinely important work is happening in quiet corners of the field that receive very little public attention. This essay is my attempt to sort signal from noise and to lay out the research programs I would fund if I were leading an AGI foundations lab over the next five years.

I will be direct about what I think is real, what is speculation, and what is actively overrated. These are opinions, not consensus. Where I disagree with widely held positions, I will say so and give my reasons. The point of an essay like this is to make calls. Hedging everything to avoid disagreement makes the essay useless.

## Category 1. Real and underfunded

Three research programs fit this category. Each has a clear empirical foundation, a specific research roadmap, and a shortage of serious researchers doing the work relative to its importance. If I were hiring into an AGI foundations lab, I would be disproportionately interested in candidates working in these areas.

### World models and planning-by-imagination

The Ha-Schmidhuber 2018 world-models paper laid out a simple proposition. Learn a compact latent representation of the environment, then plan by imagining rollouts in the latent space rather than interacting with the real environment. DreamerV3 (Hafner et al. 2023) scaled this to 150 domains with a single hyperparameter configuration, achieving sample efficiency an order of magnitude better than model-free reinforcement learning. LeCun's JEPA (Joint Embedding Predictive Architecture) is an alternative that predicts abstract embeddings rather than reconstructing observations.

Why this matters. Sample efficiency is the fundamental bottleneck for RL in the real world. Robotics, healthcare, education, autonomous driving: all require systems that learn from hundreds or thousands of real interactions, not billions. World models are the most empirically validated path to the necessary sample efficiency. DreamerV3 solving Minecraft diamond collection without human demonstrations is the sort of milestone that the public AI discourse should have spent more time on than it did.

Why I call it underfunded. The frontier labs (OpenAI, Anthropic, DeepMind's LLM-focused work) have emphasized language modeling and RLHF. World models are being developed at DeepMind's RL group, Schmidhuber's group, Meta's LeCun lab, and a handful of academic groups. Relative to the capital flowing into LLM pretraining, world-models work is dramatically under-resourced.

What I would fund. Scaling DreamerV3-style architectures to long-horizon planning with millions-of-steps time scales. Combining world models with mechanism design for multi-agent environments, a natural fit that has not been seriously explored. JEPA-style embedding-based world models, where the abstraction is semantic rather than visual. World-model architectures for language, analogous to predicting the latent dynamics of a document rather than the next token.

### Mechanism design for scaled agent systems

Almost no one is doing this, and the stakes are substantial. Production systems are increasingly populated by multiple LLM-based agents that interact, negotiate, recommend, and trade. These are mechanism-design problems by any classical definition. Yet almost all published work on LLM agents treats them as isolated decision-makers.

The mechanism-design-for-agents question: how do you design the incentive structure, the information flows, and the protocol rules so that a population of agents with different objectives converges to desirable collective behavior? This is the kind of work Myerson, Roughgarden, Parkes, and others have developed over forty years. The classical literature has not been adapted to the setting where the agents are LLM-driven, operate in natural language, and whose preferences must be inferred rather than reported.

I believe this is the single most intellectually interesting and commercially consequential research direction in AGI foundations. Every firm running a marketplace, every firm with scaled customer-service agents, every firm with scaled agent-assisted decision support will need this research within five years. The number of serious researchers doing it today is probably fewer than twenty worldwide.

What I would fund. Incentive compatibility in LLM-agent interactions, formally defined. Empirical mechanism design on simulated multi-agent benchmarks, with adversarial training to stress-test the mechanism. Distributed mechanism-design protocols where agents can collectively compute mechanism outcomes without a central authority. Causal identification of treatment effects within a mechanism, so the mechanism can adapt based on what it has learned.

### Causal identification for self-supervised agents

The third program is less developed as a research area and more developed as a research need. Modern LLMs are trained self-supervised on text that is itself produced by agents with their own objectives. Over time, this creates a feedback loop. LLMs are trained on content influenced by earlier LLMs, and the distributional shift is an active phenomenon rather than a hypothetical concern.

Causal inference has a natural application here. The question "what is the causal effect of training on LLM-generated text on the model's subsequent behavior" is identifiable under appropriate randomization. The tools of difference-in-differences, synthetic control, and instrumental-variables estimation can in principle be applied. Almost nobody is doing this kind of work rigorously. It combines research communities that do not typically interact: causal econometrics and large-model training.

What I would fund. Randomized training runs with varying LLM-generated fractions, to estimate the causal effect on downstream behavior. Synthetic-control estimators for "what would the model look like if it had been trained on fully organic text." Instrumental-variable approaches exploiting random variation in training pipelines. Long-run extrapolation of the feedback-loop trajectory under different training-policy regimes.

## Category 2. Real but saturated

These are research programs that have produced genuine progress but are now at the point where the marginal dollar is better spent elsewhere. The frontier has moved beyond what the current generation of researchers is actively studying. Incremental research output will lag the saturation of labor and capital.

### LLM scaling

Pretraining scale is still a useful research program. The ratio of new insight to dollars spent has fallen dramatically since 2022. Kaplan scaling laws are well understood. Chinchilla showed the compute-optimal data-to-parameter ratio. The architecture has converged on variations of the transformer. Training efficiency improvements continue but at diminishing returns.

A research lab entering LLM scaling today is competing against OpenAI, Anthropic, Google DeepMind, xAI, and Meta's FAIR. The frontier requires billions of dollars of compute. The marginal intellectual contribution for a $100 million investment is small relative to what was possible in 2019-2021. Unless your lab has a specific architectural innovation or a specific data-source advantage, LLM scaling is not where to invest.

### Chain-of-thought reasoning benchmarks

The CoT literature has been productive. It is now producing mostly benchmark-engineering results rather than insights about reasoning. Turpin et al., Lanham et al., and Saparov-He have documented that chains of thought are frequently unfaithful to the model's actual computation. The explanations are post-hoc rationalizations rather than faithful traces. Subsequent research has mostly improved benchmark numbers without seriously engaging with the unfaithfulness finding.

What is missing is serious empirical work on whether reasoning traces produced by LLMs can be made verifiable, not just plausible looking but provably faithful to the computation. This would require architectural changes (attention tracing, gradient-based attribution, mechanistic interpretability) beyond what current research programs are willing to invest in. Until such work is done, the CoT benchmark race is mostly a treadmill.

### RLHF variants

RLHF, DPO, Constitutional AI, process reward models, and the family of methods improving alignment via preference learning: this is a mature research area. The big labs have deployed these methods at scale. Published work is largely refinement rather than breakthrough. The RLHF-as-training-paradigm question ("is there a better way to align models than rewarding preferences") is a serious open question. Most research is parameter-tweaking within the existing paradigm.

What would make this area less saturated is a serious alternative to preference learning. Constitutional AI gestures at this but remains inside the preference-learning framing. Direct mathematical specification of desired behaviors (via formal verification, say) is a stronger alternative but technically very hard. Research investment should go into the alternatives to preference learning, not the fifteenth variant of preference learning.

## Category 3. Speculative but worth hedging

These are research programs whose long-term payoff is unclear, whose empirical base is thin, and whose philosophical assumptions are contested. If they pay off, the payoff is large enough that a diversified research portfolio should include some investment. I would allocate perhaps 10-20 percent of a lab's research capacity to this category.

### AIXI approximations and universal intelligence

Hutter's AIXI gives a mathematically rigorous definition of universal intelligence. Combine Solomonoff prediction with Bellman-optimal planning. The construction is uncomputable. Monte Carlo AIXI (Veness et al. 2011) and AIXI-tl provide computable approximations.

The serious concern: AIXI does not reflect the inductive biases that make biological intelligence work. It ranges uniformly over all programs weighted by length. Real intelligence exploits compositional structure, causal regularities, and physical priors that the Solomonoff universal distribution does not encode.

Why hedge anyway. If the AGI conversation continues to emphasize generality, a mathematical framework for universal intelligence may become newly relevant. The technical questions (how to accelerate AIXI approximations, how to combine them with modern deep learning, how to compute intelligence measures on arbitrary agents) are genuinely interesting. I would fund this area at small scale for diversification and long-term optionality.

### Gödel-robust self-improvement

The Löbian obstacle is a real theoretical limit on self-modifying agents (Yudkowsky-Herreshoff 2013, Fallenstein-Soares 2015). The question is whether it matters in practice. Will AI systems encounter it as a concrete failure mode, or is its domain of relevance too remote from practical systems to matter?

I lean toward "it will matter eventually but not soon." Systems that self-modify at the level of model weights (not prompt tuning or tool augmentation) are still rare and small-scale. If the trajectory toward stronger self-improvement continues, the Löbian obstacle may become concretely relevant in a five-to-ten year horizon. Research investment in logical inductors, probabilistic self-trust, and related mathematical machinery is a hedge worth maintaining.

### Compute-optimal theoretical scaling

The empirical scaling laws (Kaplan, Chinchilla, Hoffmann) describe observed regularities. A theoretical derivation of why the scaling laws hold, what their asymptotic form is, and whether they generalize to new architectures would be a major scientific advance. Work by Bahri et al. (2024), Maloney et al., and others on the "neural scaling" theoretical program has produced partial results.

This is speculative in that the payoff is unclear. A proven theoretical scaling law would be intellectually thrilling but may not change practical decisions. If the field produces its Maxwell equations for scaling, a derivation that unifies the empirical regularities and extends them, the result will be important. I would want a small team working on it.

## The actively overrated

Not everything in contemporary AGI discourse is real. Some research programs are generating publications and attention out of proportion to their actual contribution.

**Agent benchmarks as a measure of AGI progress.** SWE-bench completion rates are not a measure of general intelligence. They are a measure of specific, narrow-task performance that happens to be measurable. Treating benchmark progress as AGI progress has distorted research investment toward benchmark engineering rather than general capability.

**"Emergent abilities" discourse.** The emergent-abilities framing (Wei et al. 2022) has been substantially complicated by Schaeffer-Miranda-Koyejo 2023 ("Are Emergent Abilities a Mirage?"). The original claim, that new capabilities appear discontinuously at specific scales, is now contested, with much of the evidence explainable by metric-choice artifacts. Research that treats emergent abilities as settled science is working from outdated premises.

**Pure-RLHF alignment.** Alignment via preference learning is necessary but not sufficient. The claim that sufficiently careful RLHF will produce safely-aligned superintelligent systems is not supported by evidence. Research investment that assumes RLHF-is-enough is hedging on a bet that is less certain than the funding level suggests.

**Short-term AGI timeline claims.** Public statements from frontier labs about AGI arriving in 2-5 years are not calibrated to what I see in the research community. The gap between current systems and a system that can autonomously execute a novel research project at a postdoctoral level is large. Most research trajectories do not close it on that timeline. This does not mean AGI is far away. It means timeline claims are not reliable signals for research investment.

## What I would build

If I were leading an AGI foundations lab with six to twelve scientists over five years, here is how I would allocate research capacity.

| Category | Allocation | Research focus |
|---|---|---|
| World models and planning-by-imagination | 25% | Scaling, JEPA-style abstraction, language world models |
| Mechanism design for scaled agents | 25% | Incentive-compatible LLM interactions, multi-agent benchmarks |
| Causal identification for self-supervised training | 15% | Randomized training experiments, feedback-loop quantification |
| AIXI approximations and hedges | 5% | Long-term optionality |
| Agent reliability and calibration | 15% | Applied research, bridges to production deployments |
| Theoretical scaling laws | 5% | Long-term intellectual investment |
| Unbudgeted / emerging | 10% | Space for what surprises us |

The headline commitment is the first three: sixty-five percent of capacity on world models, mechanism design for agent systems, and causal identification for self-supervised training. These are the three areas where the intellectual opportunity-to-talent ratio is highest. They also compose into a coherent vision of an AGI foundations lab whose center of intellectual gravity is distinct from the LLM-scaling path.

## Conclusion

The AGI discourse is going to be louder, not quieter, over the next five years. My advice to anyone building a research lab in this space. Ignore the noise. Look at the specific research directions that combine intellectual depth, empirical tractability, and relative lack of serious competition. Invest disproportionately in those. The three I have named (world models, mechanism design for agents, causal identification for self-supervised systems) are my answer for 2026. Yours may reasonably differ. The discipline is in making the call rather than hedging across everything.

If I am leading this kind of work, I will be deliberate about what I build and what I do not. I have a clear view of the intellectual territory I think is most important. I do not expect universal agreement. I expect to be wrong about some of the allocation. The exercise of making the call, writing it down publicly, and staking a research program on it is the exercise that distinguishes a research director from a research producer.

---

*This is an essay of research taste. It is not a consensus view, and it is not a comprehensive review. Comments welcome at iohanngrig@gmail.com.*
