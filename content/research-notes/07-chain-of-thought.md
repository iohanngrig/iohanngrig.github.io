---
title: "Chain-of-thought reasoning and its limits"
date: 2026-02-14
draft: false
tags: ["llm", "reasoning", "methodology"]
---

# Chain-of-thought reasoning and its limits

> Chain-of-thought (CoT) prompting, asking a language model to produce intermediate reasoning steps before a final answer, is the most surprising and most consequential prompting technique of the last four years. It improves GSM8K performance from chance to state-of-the-art on large enough models, with no parameter changes. We cover the empirical phenomenon (Wei et al. 2022), the emergence threshold, the mechanisms by which CoT succeeds and fails, and the recent literature showing that *apparent* CoT reasoning is often a better stochastic-parrot than a better reasoner.

## 1. The empirical effect

Wei et al. (2022) showed that prompting a large language model with a handful of exemplars that include step-by-step reasoning traces, "let's think step by step", produces dramatic accuracy gains on multi-step reasoning tasks. On GSM8K (grade-school math word problems), prompting PaLM-540B with 8 CoT exemplars achieves ~57% accuracy, compared to ~18% for the same model with standard prompting and 3% for smaller models.

**Kojima et al. (2022)** showed the effect persists even without exemplars: a single instruction "Let's think step by step" induces CoT-style reasoning and improves zero-shot performance on GSM8K from 10.4% to 40.7% on InstructGPT-175B.

### 1.1 Scaling emergence

The single most striking feature of CoT gains is **scale-dependence**. Wei et al. 2022 report that CoT does not help, and can actively hurt, models below approximately 60 billion parameters. Above that threshold, gains appear rapidly.

![Chain-of-thought performance vs. model scale](/research-notes/figures/cot-fig1-scaling.svg)

The sharp transition led to the "emergent abilities" framing that dominated 2022–2023 discourse. As we'll see in [note 11 on the scaling hypothesis](/research-notes/11-scaling-hypothesis), Schaeffer et al. (2023) subsequently showed that the *sharpness* is partly an artifact of discrete evaluation metrics. Under smoother metrics, the CoT gain is still present but less abrupt.

## 2. Why CoT works, mechanistic accounts

Three non-exclusive mechanisms have been proposed.

**Serialized computation.** A single forward pass of a transformer has a fixed computation budget per token. Generating intermediate reasoning tokens extends the effective computation, allowing the model to break long problems into subproblems that each fit in-context. This is the "tokens as scratchpad" view (Nye et al. 2021).

**In-distribution unlock.** Pretraining corpora contain vast amounts of step-by-step reasoning (textbook solutions, Q&A forums, code comments). CoT prompting activates this latent capability by cuing the model to generate output in the "reasoned explanation" distribution rather than the "direct answer" distribution. The model has seen what good reasoning looks like; CoT makes it produce it.

**Path selection.** Problems where the correct answer is reached by a specific chain of steps may have many incorrect shortcut paths in the model's output distribution. CoT concentrates probability on paths whose intermediate steps are individually plausible, biasing the sampling toward correct trajectories.

The three mechanisms are consistent with one another and probably all contribute.

## 3. Limits and failure modes

### 3.1 Apparent reasoning vs. actual reasoning

**Saparov & He (2023)** introduce PrOntoQA, a synthetic reasoning benchmark where the ground-truth reasoning chain is known. They find that LLMs can produce CoT chains that *arrive at correct answers via incorrect reasoning*, the final answer is right, but the intermediate steps contain errors or unjustified inferences. This pattern is invisible to standard accuracy metrics.

**Turpin et al. (2023)** find that CoT explanations can *systematically misrepresent* the model's actual computation. When biasing cues are introduced (e.g., reordering multiple-choice options so the correct answer is always "A"), models generate CoT traces that appear to reason about the content but consistently pick "A" regardless. The CoT is a post-hoc rationalization, not a faithful computation.

### 3.2 Sensitivity to prompt format

**Prystawski et al. (2024)** and **Madaan et al. (2023)** document that CoT performance is highly sensitive to minor prompt changes: exemplar ordering, minor phrasing, irrelevant appended text. Effects of ±10 percentage points from seemingly cosmetic changes are common. This undermines the view of CoT as a robust capability and suggests it is still substantially an in-context-learning phenomenon with all the brittleness that entails.

### 3.3 Length and compositional limits

**Dziri et al. (2024)** show that transformer CoT accuracy on multi-step arithmetic and logical composition degrades sharply with task depth. A model that achieves 95% on 3-step problems may get 15% on 6-step problems, far worse than would be predicted by independent step-errors. They attribute this to *compositional brittleness*: the model learns individual operations but fails to reliably chain them.

**Lanham et al. (2023)** run faithfulness experiments where CoT tokens are perturbed during generation, and compare final-answer accuracy with and without the perturbation. They find that for many tasks, **the CoT has little causal effect on the answer**, the model would have produced the same answer anyway. This is direct evidence that the CoT is decorative rather than computational in many settings.

### 3.4 Self-consistency is not self-correction

**Huang et al. (2024)** show that "self-correction" prompts, where the model is asked to critique its own CoT and produce a revised answer, often *reduce* accuracy on tasks where the model already has reasonable calibration. The self-critique is just another forward pass, subject to the same biases, and adding a stage where the model must justify a revision introduces a bias toward *finding something to revise*, even when the original answer was correct.

## 4. Interaction with tool use and RAG

CoT combined with tool use (ReAct: Yao et al. 2022; see [note 5](/research-notes/05-llm-agents)) is materially stronger than CoT alone, because external tools can *verify* intermediate steps. A CoT trace that says "the Wikipedia page reports the director as X" and then actually queries Wikipedia is a qualitatively different artifact from an unverified internal assertion. This is the strongest current argument for agent-style deployments over pure CoT prompting.

Similarly, retrieval-augmented generation (see [note 8](/research-notes/08-rag)) can ground CoT chains in external facts, reducing the hallucination-propagation problem. The combination RAG + CoT + self-consistency is the current production default for factual question answering.

## 5. Open questions

**Is there a reasoning-faithful CoT training objective?** Current models are trained on next-token prediction; faithful reasoning is a behavioral property, not an explicit objective. Recent work on process-reward models (Lightman et al. 2023) trains models to produce intermediate steps that are individually graded by a reward model, an objective that directly targets faithfulness, but the approach is expensive and not yet standard.

**Why does scale help, and will it continue?** The empirical curve in §1.1 is well-documented but poorly understood at the mechanistic level. Whether the trend continues, saturates, or reverses at 10T+ parameters is a central open question for the scaling debate.

**Can we detect unfaithful CoT automatically?** Lanham et al.'s perturbation methodology is the current gold standard but expensive. Efficient faithfulness checks would enable better evaluation and targeted training.

## 6. References

- **Wei, J., Wang, X., Schuurmans, D., Bosma, M., Chi, E., Le, Q., & Zhou, D.** (2022). *Chain of thought prompting elicits reasoning in large language models*. NeurIPS. [S.S. `1b6e810c`]
- **Kojima, T., Gu, S., Reid, M., Matsuo, Y., & Iwasawa, Y.** (2022). *Large language models are zero-shot reasoners*. NeurIPS.
- **Nye, M., et al.** (2021). *Show your work: scratchpads for intermediate computation with language models*. arXiv.
- **Saparov, A., & He, H.** (2023). *Language models are greedy reasoners: a systematic formal analysis of chain-of-thought*. ICLR.
- **Turpin, M., Michael, J., Perez, E., & Bowman, S. R.** (2023). *Language models don't always say what they think: unfaithful explanations in chain-of-thought prompting*. NeurIPS.
- **Prystawski, B., Li, M. Y., & Goodman, N. D.** (2024). *Why think step-by-step? Reasoning emerges from the locality of experience*. NeurIPS.
- **Madaan, A., et al.** (2023). *Self-refine: iterative refinement with self-feedback*. NeurIPS.
- **Dziri, N., Lu, X., Sclar, M., et al.** (2024). *Faith and fate: limits of transformers on compositionality*. NeurIPS.
- **Lanham, T., et al.** (2023). *Measuring faithfulness in chain-of-thought reasoning*. arXiv.
- **Huang, J., Chen, X., Mishra, S., et al.** (2024). *Large language models cannot self-correct reasoning yet*. ICLR.
- **Lightman, H., Kosaraju, V., Burda, Y., et al.** (2023). *Let's verify step by step*. ICLR.

*Figure 1 illustrates the emergence-vs-scale relationship reported in Wei et al. 2022 Figure 4; specific numbers are illustrative rather than a direct replication.*
