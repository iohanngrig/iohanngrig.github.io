---
title: "Production LLM agents: what the reliability engineering literature missed"
date: 2026-04-18
description: "Lessons from shipping agent systems to production, and a framework for agent reliability that extends beyond benchmark completion rates."
tags: [writing, llm-agents, reliability]
draft: false
---

The public research on LLM agents has been productive, and in important ways it has been misleading. A literature has accumulated around benchmark scores. SWE-bench for coding agents, GAIA for general-purpose agents, HumanEval for code generation, MT-Bench for conversational evaluators. Every six months a new agent architecture posts a higher completion rate and claims progress. Meanwhile, in production, agent systems routinely fail in ways the benchmarks do not measure. The literature offers little guidance on how to repair them.

I have shipped multiple production LLM agents over the past eighteen months at Amazon. They handle decision-support tasks for business users. Some recommend compensation structures. Some summarize research for internal stakeholders. Some execute multi-step analytical workflows that previously took analysts hours. They work. Getting them to work required solving problems the public research literature has not seriously engaged with. Those are the problems I take up.

## The benchmark fallacy

The premise of agent benchmarks is that the task is well-defined. SWE-bench gives you a GitHub issue, a reference resolution commit, and a set of tests the resolution must pass. The agent either produces a patch that passes the tests, or it does not. The score is the fraction of issues resolved.

In production, the task is never this clean. A business user asks: "look at last month's underperforming markets and recommend what to change." This is four distinct underspecified sub-tasks. What does "underperforming" mean in this context? Which metrics are the right ones to examine? What counts as "last month" given timezone and holiday considerations? What level of intervention is the user empowered to make? A benchmark would score an agent for completing this task. In reality the agent's job begins with interrogating the ambiguity: asking clarifying questions, surfacing the implicit assumptions, offering the user a choice among three framings before any analysis runs.

An agent that blindly completes the stated task on its first reading is not exhibiting good behavior. It is exhibiting a pathology that benchmarks reward, namely eager completion at the cost of correctness. A production-grade agent's first response to most requests is a short interrogation, not a solution. Benchmarks do not measure this.

The second way benchmarks mislead: they measure task *completion*, not task *utility*. A SWE-bench-style agent that produces a patch passing the tests scores 1.0. If the patch is a 400-line change that fixes the narrow tested failure while introducing three design-level inconsistencies the reviewer will reject, the patch is useless and the score is misleading. Production agents have to produce *minimal, reviewable, rejectable* recommendations. A human reviewer needs to be able to quickly accept or push back on the artifact. An agent that produces maximalist outputs that score well on tests but are operationally unusable is not a good agent. It is a benchmark-inflating system that happens to be deployed.

## What reliability actually looks like

Classical reliability engineering has a distinction the agent literature has not imported. Reliability for an agent is not one number. It is a vector of properties.

**Calibration.** When the agent says it is confident, it should be right in proportion to its expressed confidence. When it says it is uncertain, the decision maker should treat its output as a draft, not a conclusion. Calibration is the property most agent benchmarks fail to measure and most production deployments end up needing. An agent that is 98 percent accurate but produces its incorrect 2 percent with maximum confidence is dangerous. An agent that is 85 percent accurate but knows when it is uncertain is much better.

**Graceful refusal.** A production agent will occasionally face requests outside its competence. Requests requiring data it cannot access. Policy decisions above its authorization. Technical questions in a domain it has no tool for. The failure mode is not "get it wrong." The failure mode is "try to answer anyway and fabricate something plausible." A well-engineered agent says, verbatim: "I can't help with this. Here is what I would need to help, and here is a human who can." Graceful refusal is an engineered property, not a natural one.

**Escalation.** When the agent is processing a task and encounters a signal that the work product will have unusually large downstream consequences (a compensation recommendation affecting a large account, an analytical conclusion that contradicts last week's conclusion), it should escalate. Flag the work for human review before submission rather than completing it silently. Escalation requires the agent to recognize when it is operating outside its usual regime. Benchmarks do not train for this.

**Tool-call discipline.** Modern agents call external tools: databases, APIs, analytical engines. A small fraction of these calls will fail. The API times out. The database returns zero rows. The analytical engine returns a numerically implausible result. A poorly engineered agent will pass the failed-call result through to the user as if it were valid. A well-engineered agent has explicit validation logic for each tool's return type, detects when the return is malformed, and either retries or falls back to a different tool. This is ordinary defensive programming. The agent research literature has strangely ignored it.

**Session memory discipline.** Multi-turn conversations require the agent to remember context. The memory should forget irrelevant details and retain only what is actively load-bearing. An agent that remembers every previous turn verbatim quickly bloats its context window with noise that degrades downstream generation quality. An agent that forgets too aggressively loses thread and asks the user to re-specify things already said. The memory-management problem is analogous to operating-system paging. The appropriate data structures (hierarchical summarization, explicit slot filling for key entities) are well known from cognitive architectures and have not been imported to LLM-agent research.

These five properties are the reliability vector for an LLM agent. None of them is measured by SWE-bench or GAIA. All of them are necessary for production deployment. An agent that scores 70 percent on benchmarks with a good reliability vector deploys successfully. An agent that scores 90 percent on benchmarks with a poor reliability vector gets pulled from production within weeks.

## Five reliability patterns from production

Here are five concrete patterns I have observed shipping agents, generalized to be applicable beyond any single company.

**Pattern 1. Strict structured output with explicit ambiguity flags.** Every agent response is a structured artifact with a schema. A typical schema: `interpretation` (what the agent believes the user asked, restated), `confidence` (numeric), `result` (the actual answer), `uncertainty` (where the agent is uncertain), `assumptions` (what the agent assumed to produce the result), `next_steps` (what the user might want to follow up on). The schema is strict. The agent refuses to produce an output that fails validation. This makes the agent's reasoning legible to the user and to downstream systems.

**Pattern 2. Calibration-oriented prompting.** In the system prompt, the agent is given explicit guidance about when to express confidence and when to express uncertainty. The exact language matters. "Only express high confidence when you have verified the claim against at least two independent sources" produces measurably better calibration than "be confident when you are right." Prompt engineering as calibration engineering is a real and underdeveloped practice.

**Pattern 3. Constrained tool-call patterns.** Each tool the agent can call has a constrained input schema that the agent must satisfy. The constraints are checked before the call is issued, not after. If the agent tries to call a tool with malformed inputs, the call is rejected and the agent receives a specific error message that it can act on. This prevents the failure mode where the agent produces a nominally well-formed tool call that the tool interprets incorrectly.

**Pattern 4. Deterministic retry and fallback.** Every tool call has an explicit retry policy and a fallback chain. If the primary tool fails, the agent tries a secondary tool with different characteristics (a cached version of the primary tool's data, a lower-resolution approximation). The fallback is deterministic, not LLM-mediated. You do not want the LLM to freestyle a fallback during a production incident.

**Pattern 5. Continuous evaluation against a production-shadow suite.** A representative sample of real user queries is replayed through the agent nightly. The agent's outputs are compared against reference outputs. Drift in the agent's behavior, even when benchmark scores are stable, triggers investigation. This is the continuous-integration analog for agent systems. The public literature has almost no discussion of how to do it.

## Why the literature has missed this

A plausible explanation is that the LLM-agent research community is dominated by researchers at frontier labs whose objective is pushing the benchmark score. Shipping an agent to a production user base with business-critical consequences is a different activity. The labs that publish papers do not typically run the production agents. The companies that run production agents do not typically publish papers about their engineering.

This gap has academic and commercial consequences. Academically, the published benchmarks do not capture the dimensions of performance that matter. Incremental research progress on benchmarks may not translate to better production systems. Commercially, firms rebuilding the reliability patterns in isolation waste substantial effort on a set of problems that are fundamentally the same across firms.

I believe this will change in the next two years. As more companies ship production agent systems, the reliability patterns will get documented, generalized, and eventually published. I intend to be one of the people doing the documentation. The forthcoming paper from my research track, provisionally titled "Production LLM Agent Reliability: Patterns from Financial-Stakes Deployment," is a first attempt.

## The broader point about applied-research taste

Underneath the specific technical content, this essay is making a broader point about research judgment. The ability to look at an active research literature, identify the systematic gap between what is published and what is needed, and then do the research that closes the gap: that is what distinguishes senior applied researchers from junior ones.

The literature on LLM agents has been publishing for five years. The research community is large, well funded, and producing steady benchmark progress. Yet the benchmark-score trajectory has not translated to a matching trajectory in production reliability. That gap is the signal that the community has been looking at the wrong problem.

A senior researcher's job is to notice this kind of gap before it has been articulated by anyone else, while the rest of the community is still debating the best attention mechanism. My work on the panel-aware causal forest is another example. The DML literature has been mature for five years. Almost nobody has written up the panel-data failure mode, even though it is common and consequential.

Hiring for senior and principal applied research is, in large part, hiring for this kind of gap-detection judgment. The candidate who can explain why the literature is missing something important, and describe how they would fix it, is operationally more valuable than the candidate who can implement the latest paper faster. Both skills matter. The first one is rarer and more valuable.

## What I would build if leading an agent-reliability research program

If I were leading a research program on LLM-agent reliability, here is what the first year's work would look like.

**Month 1 to 3.** Establish a continuous-evaluation framework on a shared benchmark of production-realistic agent tasks, including tasks that require the reliability-vector properties (graceful refusal, escalation, tool-call discipline). Open-source the framework.

**Month 4 to 6.** Evaluate existing agent architectures (ReAct, Reflexion, SWE-agent, Voyager, our own production systems) on this benchmark. Report the gap between their benchmark-score rank order and their reliability-vector rank order. That headline result, that the rank orders disagree and the magnitude of the disagreement, is the central contribution.

**Month 7 to 9.** Develop architectural mitigations for the reliability-vector failures most visible in the evaluation. I would focus first on calibration, because it is the most measurable, and then on graceful refusal, because it is the most under-studied.

**Month 10 to 12.** Ship a public reference implementation demonstrating the mitigations, plus a paper reporting the architectural improvements. Submit to the ICML or NeurIPS agents-track workshop.

This is the research program I intend to lead at whatever institution gives me the scope to do it seriously. The work is not glamorous. Nobody gets famous for publishing calibration improvements. It is genuinely useful, and it occupies a gap in the research landscape that the current trajectory is unlikely to fill on its own.

*The essay is a preview of the forthcoming research agenda paper. Comments and critique welcome.*
