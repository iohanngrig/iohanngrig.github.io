---
title: "LLM agents as decision systems: a skeptic's guide"
date: 2026-02-07
draft: false
tags: ["llm-agents", "reliability", "evaluation"]
---

# LLM agents as decision systems: a skeptic's guide

> Since 2022 the LLM-agent literature has moved from prototype (tool-calling + chain-of-thought) to benchmark domination (ReAct, Reflexion, SWE-agent, Voyager) to production deployment. The gap between *benchmark performance* and *reliable production behavior* is large, systematic, and under-measured. This note takes the skeptic's view: which agent capabilities have survived replication, what agent evaluations actually measure, and what fails in deployment that benchmarks do not catch. Throughout, I argue that agent reliability engineering is a real sub-discipline, distinct from improving base model quality, and that the deployment posture of *augmentation rather than replacement* is the one the evidence supports.

## 1. The agent pattern that actually works

Three design ingredients appear in essentially every agent framework that has survived replication since 2022.

**Chain-of-thought prompting** (Wei et al. 2022). The model is prompted to produce intermediate reasoning steps before its final answer. Empirically this improves performance on arithmetic, commonsense, and symbolic reasoning tasks in the GPT-3-and-larger regime. It does not help small models and does not help tasks that don't admit verbal decomposition.

**Tool use** (Toolformer: Schick et al. 2023). The model can invoke external APIs, search, calculator, code interpreter, database, web browser, and incorporate the results into its context. This externalizes the knowledge the model would otherwise hallucinate. The mechanism is supervised: the training data contains examples of tool calls, and the model learns to emit them in the right format at the right time.

**Observation–action interleaving** (ReAct: Yao et al. 2022). Rather than producing a full plan before acting, the agent alternates reasoning traces with tool calls, incorporating each tool's output before the next reasoning step.

```
Thought: I need to find the director of the 1974 film "Chinatown."
Action: search("Chinatown 1974 film director")
Observation: Directed by Roman Polanski.
Thought: Confirmed. Answer: Roman Polanski.
```

The empirical consequence of this interleaving, documented in the ReAct paper: on question-answering benchmarks that require external knowledge (HotpotQA, FEVER), ReAct overcomes hallucination-propagation by checking external APIs mid-reasoning, rather than reasoning to a conclusion and then looking up facts. On interactive decision-making benchmarks (ALFWorld, WebShop), ReAct outperforms imitation and RL baselines by 10–34 absolute percentage points.

## 2. Reflexion and self-critique

Reflexion (Shinn et al. 2023) adds a **verbal self-critique loop**: after a failed trajectory, the agent generates an explicit explanation of what went wrong ("I tried X, it failed because Y, next time I should do Z"), stores it in episodic memory, and re-attempts the task with the critique as additional context.

This works when:
- The task admits a binary success/failure signal.
- Repeated attempts are cheap.
- The failure mode is verbal-rationalizable (the agent's world model is approximately correct; the mistake is tactical).

The important caveat: the self-critique is **produced by the same LLM** whose world model was wrong. Systematic errors, the kind that caused the failure in the first place, propagate into the critique. Reflexion is not an oracle. It is a structured way of letting the model re-sample with additional prompting, and its gains disappear as the failure becomes less about tactical missteps and more about missing knowledge.

## 3. Agent evaluations, and why they mislead

Three benchmarks, three lessons about what agent evals measure and miss.

### 3.1 WebShop and ALFWorld, the simulated environments

These are text-interface simulators (a web shop, an embodied household) where the agent navigates by typing actions. ReAct scores high on both. The lesson is cautionary: these environments are close to the pretraining distribution of text-interface documentation. Performance there does not transfer to unfamiliar web UIs, real operating systems, or physical action spaces. An agent that scores 80% on WebShop may fail on a novel e-commerce site it has not seen described on the internet.

### 3.2 GAIA, the honest benchmark

GAIA (Mialon et al. 2023) is a **general AI assistant benchmark** with 466 questions requiring reasoning, multimodality, web browsing, tool use, and multi-step planning. Questions range from "look up a particular chess game and determine the winner's rating" to "find the average temperature of a specific city on a specific date from a specific source."

The published results at the time of the paper, and the trend through 2025, show a striking gap. The specific percentages shown below are *illustrative of the range* reported on the GAIA leaderboard and in the original paper, exact numbers move as models improve, so treat them as order-of-magnitude indicators rather than authoritative scores.

![GAIA benchmark: best LLM agents vs. human baseline, by difficulty level](/research-notes/figures/agents-fig1-benchmark-gap.svg)

Humans achieve ~90%+ accuracy across all three difficulty levels. The best LLM agents as of late 2025 hover in the 30–50% range on Level 1 and drop substantially on Levels 2 and 3. **GAIA is the first benchmark where leading LLM agents are not close to humans** on a task that is itself close to real-world assistant work.

The takeaway is not that agents are useless. The takeaway is that for many tasks the user cares about, the honest human baseline is out of current agent reach.

### 3.3 SWE-bench, the dramatic story with a caveat

SWE-bench (Jimenez et al. 2024) scores agents on their ability to resolve real GitHub issues: given the issue text and the repository, produce a patch that makes the hidden test suite pass. SWE-bench Verified is a curated subset with cleaned-up tests.

![SWE-bench Verified: published agent scores over time](/research-notes/figures/agents-fig2-swebench-trend.svg)

The trend from ~2% (early 2024) to ~60%+ (late 2025) is real and one of the fastest improvement curves in the history of program synthesis. It is also:

- **Gameable.** The "hidden" test suite is visible in the repository; agents that access the test file directly perform artificially well. Mitigating this requires curation that is itself adversarial.
- **Not the same as deployed close rate.** Teams deploying SWE-bench-topping agents (Cognition, Sourcegraph, Aider) report real-world issue-close rates substantially lower than benchmark scores, because real issues are less well-specified, span more files, and have more complex branch state than the benchmark cases.
- **Insensitive to solution quality.** A fix that passes the test suite but introduces a regression elsewhere scores the same as a clean fix.

The benchmark-to-deployment gap is a first-class fact about agent reliability, not a minor artifact.

## 4. A taxonomy of agent errors

A production deployment of an agent will encounter all three error categories. Correcting for them requires different tools.

![Agent-error taxonomy: three categories with examples and detectability](/research-notes/figures/agents-fig3-error-taxonomy.svg)

**Specification errors.** The user's request is ambiguous; the agent commits to the wrong interpretation silently and proceeds with confidence. The fix is to require the agent to produce an *interpretation* and *clarification questions* before acting. Recent work (SpeakRL, Acikgoz et al. 2025) trains agents to proactively clarify rather than silently commit; this improves task-completion rates by ~20 percentage points without increasing turn counts.

**Tool-call errors.** The argument to a tool is malformed, type-mismatched, or semantically wrong. Strict schema validation on tool outputs catches the first two; the third, correct type, wrong value, is harder. Retry with error feedback helps. Constrained decoding on tool arguments helps more. Even with schema validation, 5–15% of tool calls in production deployments contain semantic errors, the right kind of thing, wrong specific thing.

**Reasoning errors.** The agent's chain of reasoning is invalid; conclusions do not follow from premises. The remedy is externalization: structured outputs, verification against tool results, critic models that independently check the chain. The humility note: reasoning errors are the hardest to detect automatically because the agent sounds confident. Automated detection requires a separate critic that the agent cannot influence.

## 5. RLHF, DPO, and the alignment layer

Alignment is the engineering step between a pretrained LLM and an agent that follows instructions without blatant harms. Two eras.

**RLHF** (Christiano et al. 2017; Ouyang et al. 2022). Fit a reward model $r_\phi(x, y)$ to human preference data, then optimize the policy $\pi_\theta$ via PPO to maximize expected reward while staying close to the pretrained policy in KL divergence:

$$
\max_\theta \;\mathbb{E}_{x \sim D, y \sim \pi_\theta(\cdot \mid x)} \bigl[ r_\phi(x, y) \bigr] \;-\; \beta \, \mathrm{KL}\bigl(\pi_\theta(\cdot \mid x) \,\|\, \pi_{\text{ref}}(\cdot \mid x)\bigr).
$$

Effective but complex and unstable: reward-model overfit, PPO hyperparameter sensitivity, and reward hacking are all well-documented pathologies.

**Direct Preference Optimization** (Rafailov et al. 2023). Analytical manipulation of the RLHF objective yields

$$
\mathcal{L}_{\mathrm{DPO}}(\theta) \;=\; -\mathbb{E}_{(x, y_w, y_l) \sim D} \biggl[ \log \sigma\biggl( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_{\text{ref}}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_{\text{ref}}(y_l \mid x)} \biggr) \biggr]
$$

where $(y_w, y_l)$ is a preferred/dispreferred response pair and $\sigma$ is the sigmoid. The key algebraic fact is that *the optimal policy under the RLHF objective has a closed form in terms of the reward*, so you can skip reward modeling and PPO entirely. DPO is substantially simpler, more stable, and has become the default alignment step since 2024.

The alignment layer reduces *visible* bad behavior (harmfulness, verbosity, refusal appropriateness). It does not directly improve task **reliability**. A well-aligned agent is not a reliable agent: it fails gracefully where a misaligned agent might fail harmfully, but the failure rate on the intended task can be identical.

## 6. What I have come to believe

**Agent reliability engineering is a real sub-discipline.** It consists of: strict tool schemas, atomic tool calls, explicit failure handling, conservative fallbacks, and observability. Most production reliability gains come from these, not from a bigger base model.

**The deployment posture that survives contact with reality is augmentation, not replacement.** An agent that asks a human to approve a decision before taking it can be useful at 70% base accuracy. An agent deployed autonomously at 95% accuracy can be catastrophic: the 5% of failures are frequently correlated (similar prompts trigger similar errors) and adversarial (once a failure mode is known, it can be exploited).

**The "scaling will solve reliability" claim is unfalsifiable on present evidence** and almost certainly wrong for the specification-error category. Scaling improves fluency, knowledge breadth, and apparent confidence. Specification errors persist because they are about the *user's* mental model, which no amount of model scaling addresses.

## 7. Three real-life applications

**Research-assistant agents on public domains.** Perplexity, Deep Research (OpenAI), and domain-specific research tools operating on Wikipedia, arXiv, and curated databases are the highest current reliability. The task space is narrow, the error cost is low (user can verify), and tool use is well-specified.

**Code-assistance agents on open-source repositories.** Aider, SWE-agent, and similar tools have moderate reliability and high value when used interactively. Autonomous operation on production codebases remains in early stages. Deployment reports document substantial benefit when the agent is a collaborator; substantial risk when it operates without review.

**Shopping, planning, and scheduling assistants.** Low reliability, high leverage on multi-step tasks. A 70% reliable shopping assistant is arguably useful if it defers cleanly on the 30% it is unsure about. It is dangerous if it silently makes irreversible choices (purchases, bookings, deletions). Financial actions should be human-approved; this is not a theoretical constraint.

## 8. Open questions

**Objective functions for agents.** Task success is too coarse; verbal-feedback rewards overfit to stylistic preferences; alignment targets are proxies for what we actually want. The field lacks a clean objective that distinguishes "reliable" from "plausible-sounding."

**Long-horizon planning.** Beyond ~5–10 steps, error accumulation dominates agent performance. This is a structural problem, not a scale problem. Current research on hierarchical planning, tree-of-thought search, and learned critics offers partial answers but no general solution.

**Out-of-distribution evaluation.** Evaluating agents on tasks that were not in the pretraining distribution is methodologically fraught. GAIA is the current best answer; holdout-based benchmarks for dynamic knowledge are still primitive.

**Reliability–alignment tradeoff.** Strongly aligned (refusal-prone) agents also refuse legitimate but unusual requests, reducing usefulness. The alignment tax is real and poorly quantified. Research on selective refusal (refuse in danger, accept in legitimate edge cases) is early.

## 9. References (verified April 2026)

- **Yao, S., Zhao, J., Yu, D., Du, N., Shafran, I., Narasimhan, K., & Cao, Y.** (2022). *ReAct: Synergizing Reasoning and Acting in Language Models*. ICLR 2023. [S.S. `99832586`]
- **Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichter, B., Xia, F., Chi, E., Le, Q., & Zhou, D.** (2022). *Chain-of-thought prompting elicits reasoning in large language models*. NeurIPS.
- **Schick, T., Dwivedi-Yu, J., Dessì, R., Raileanu, R., Lomeli, M., Zettlemoyer, L., Cancedda, N., & Scialom, T.** (2023). *Toolformer: language models can teach themselves to use tools*. NeurIPS.
- **Shinn, N., Cassano, F., Berman, E., Gopinath, A., Narasimhan, K., & Yao, S.** (2023). *Reflexion: language agents with verbal reinforcement learning*. NeurIPS.
- **Mialon, G., Fourrier, C., Swift, C., Wolf, T., LeCun, Y., & Scialom, T.** (2023). *GAIA: a benchmark for general AI assistants*. arXiv.
- **Jimenez, C. E., Yang, J., Wettig, A., Yao, S., Pei, K., Press, O., & Narasimhan, K. R.** (2024). *SWE-bench: can language models resolve real-world GitHub issues?* ICLR.
- **Ouyang, L., et al.** (2022). *Training language models to follow instructions with human feedback*. NeurIPS.
- **Rafailov, R., Sharma, A., Mitchell, E., Ermon, S., Manning, C. D., & Finn, C.** (2023). *Direct preference optimization: your language model is secretly a reward model*. NeurIPS. [S.S. `0d1c76d4`]
- **Christiano, P., Leike, J., Brown, T. B., Martic, M., Legg, S., & Amodei, D.** (2017). *Deep reinforcement learning from human preferences*. NeurIPS.
- **Acikgoz, E. C., et al.** (2025). *SpeakRL: synergizing reasoning, speaking, and acting in language models with reinforcement learning*. arXiv.
- **Sutton, R. S., & Barto, A. G.** (2018). *Reinforcement learning: an introduction*. 2nd ed., MIT Press. Freely available online.

---

*Figure numerical values in §3 are approximate and illustrative of widely-reported public leaderboard ranges (GAIA, SWE-bench Verified). For authoritative numbers, consult the original papers and the current state of the respective leaderboards.*
