---
title: "Causal identification and mechanism design for agent-driven decision systems"
date: 2026-04-26
description: "A research agenda at the intersection of causal inference, production LLM agents, and mechanism design under uncertainty."
tags: [writing, research-agenda]
draft: false
---

Three research programs are converging, and I believe the next decade of applied AI and economics will be decided at their intersection. They are rarely studied together, which is the opportunity.

The first program is causal inference for panel data: how to identify treatment effects when the data is longitudinal, heterogeneous, and staggered. The second is LLM agents for decision support: how to build language-model-driven systems that recommend policies, prices, and contracts in production. The third is mechanism design under uncertainty: how to design incentive schemes robust to estimation error and elasticity misspecification. Each has its own community, its own textbooks, its own conferences. The researchers I most respect in each area rarely cite the other two.

My research sits in the intersection. I lay out the three strands below, explain why they connect at this specific moment, and sketch the work I plan to lead over the next five years.

## Strand one: causal methodology for the panels we actually have

Industrial data is almost always panel data. Firms observe the same customers, products, merchants, or markets repeatedly over time. A unit's outcome today depends on its history, its treatment history, and the treatment histories of units around it. The standard causal estimators, including two-way fixed effects, simple difference-in-differences, and cross-sectional propensity weighting, assume away most of this structure. They pay for the convenience with biased estimates, invalid confidence intervals, and occasionally wrong-signed treatment effects.

The field has known this for at least a decade, and the response has been productive. Goodman-Bacon's 2021 decomposition made the TWFE bias concrete. Callaway and Sant'Anna's group-time estimator gave us a principled alternative. De Chaisemartin and D'Haultfœuille mapped the full weighting structure. Chernozhukov and co-authors' Double Machine Learning framework handled the high-dimensional-nuisance problem. Causal forests with honest splitting gave us pointwise confidence intervals on heterogeneous treatment effects.

What the field has not done, and what I intend to contribute, is to stitch these pieces into a methodology that works on the panels actual companies analyze. In industry, the panel is always unbalanced. Treatment is staggered across multiple cohorts. The effects are genuinely heterogeneous across units and over time. The outcomes are affected by unit-level fixed effects that would absorb half the variation in a proper specification. Running DML on this kind of panel without careful attention to fixed-effect residualization can give wrong-signed CATE estimates. I have watched this happen in production repeatedly. Recent work formalizes DML for static panels with fixed effects (Clarke & Polselli 2025), but the production failure mode and a practitioner-ready fix remain under-applied.

My first line of work, already drafted to about 60 percent, documents this failure mode and proposes an estimator that residualizes panel fixed effects before the DML machinery runs. The primary question is not "can we fit a more expressive model." It is "does the model respect the identification assumptions the panel structure enforces." Empirically the fix recovers the sign and magnitude of the true CATE on carefully constructed simulations. I aim to show that it preserves the $\sqrt n$-consistency and semiparametric efficiency that make DML valuable in the first place.

This is the cleanest methodology contribution in my agenda. It establishes that standard tools fail on the settings most commonly used in industry, and it provides a repair. I expect it to be widely adopted because the failure mode is both common and invisible to practitioners running standard library calls.

## Strand two: production LLM agents for mechanism design

The second strand grew from unexpected ground. Since August 2024 I have shipped multiple production Bedrock agents that recommend incentive structures and compensation decisions. The agents ingest observational data, call causal-ML tools to estimate treatment effects, and generate structured recommendations that flow into downstream decision processes. They work. Watching them work reveals something the agent-research literature has largely missed.

The public literature on LLM agents (ReAct, Reflexion, Voyager, SWE-agent, GAIA benchmarks) treats agent reliability as a property to be measured on held-out benchmarks. Success is a number: $x$ percent of tasks completed. This misses the thing that determines whether an agent is actually useful in production. Usefulness is not the benchmark score. It is the agent's behavior in the ambiguous middle ground between a clear task with a clear completion criterion and a task the user and the agent disagree about the nature of.

In production, an agent's job is not to complete a task. It is to be a trustworthy counterparty to a human decision-maker who will use its output for a decision with real consequences. The human has to know when to trust the agent and when to override it. The agent has to produce calibrated uncertainty about its own recommendations. It has to escalate when it is uncertain. It has to refuse gracefully when the request is outside its competence. None of these properties are measured by SWE-bench.

The bridge to causal inference and mechanism design is this. An agent that recommends an incentive scheme is making a mechanism-design decision with downstream effects on principal-agent interaction. If the agent recommends a payment structure that changes merchant behavior, the treatment-effect estimate that informed the recommendation is now contaminated. The agent is operating inside the causal system it was supposed to analyze. The standard assumption of exogenous treatment assignment fails. The standard identification formula fails with it.

The research question: how do you design agents that recommend causal-inference-backed decisions while respecting the fact that those decisions change the identifying assumptions of future inference? This is largely unstudied. My second research line is a framework for causal evaluation of agent-driven mechanism implementation. The framework treats the agent's recommendation as a policy intervention and the downstream mechanism-equilibrium as the post-treatment state.

I expect this line to produce an Economics & Computation (EC) submission in 2026 and a longer-horizon paper for the ICML or NeurIPS agents track. The work also defines the intellectual territory that differentiates me from the hundreds of people who can either build LLM agents or do causal inference, but rarely both.

## Strand three: mechanism design under estimation uncertainty

The third strand is mechanism design theory. Here I am on less fully developed ground. Classical mechanism design assumes the designer knows the agents' utilities, or at least their priors over utilities. The revelation principle gives us optimal auction theory, the Myerson allocation, and the broad kit of principal-agent contracts. In settings where the utility function must be estimated from data, essentially every real-world mechanism design problem, the classical framework assumes an empirical quantity that does not exist.

Personalized pricing is the cleanest example. If a firm wants to set price-discriminating offers to maximize expected revenue, the Myerson optimal mechanism requires knowledge of the demand elasticity at each customer. In practice the elasticity is estimated from a causal model, and that estimate has a standard error. The mechanism that is optimal under the point estimate of elasticity is not the mechanism that is optimal under the uncertainty distribution over elasticities.

The technical question is how to design mechanisms that are robust to elasticity estimation error. This connects to the robust mechanism design literature (Bergemann-Morris 2005, Carroll 2015) and to the distributionally robust optimization literature (Delage-Ye 2010). But the specific problem of an ML-estimated elasticity, with an ML-quantified uncertainty distribution, feeding into a practical production mechanism, is not well covered by either literature. The gap is substantial. The business stakes are large. Any company doing personalized pricing, personalized advertising auctions, or personalized compensation is implicitly running a mechanism that assumes a zero-uncertainty elasticity.

My third research line is elasticity-aware robust mechanism design. I intend it to be my signature research contribution. The goal is a framework that takes a causal-ML estimator of elasticities, propagates uncertainty through the mechanism design optimization, and produces a mechanism that is optimal against an adversarial realization of the elasticity. The approach borrows from distributionally robust optimization, from conformal prediction for the uncertainty calibration, and from mechanism design for the incentive-compatibility constraints.

This will be a multi-year research program. I expect the first substantial paper out of it in late 2026, submitted to EC or the AAAI mechanism-design track.

## Why these three converge now

These three strands have been nominally studyable for twenty years. Causal inference has been a mature field since the 1990s, and mechanism design theory is older. Why does their convergence now, specifically at the intersection with LLM agents, matter?

The answer is that a production-LLM-agent-driven decision system is the first setting in economic history where the mechanism designer, the agent who interacts with the principals, and the empirical causal inference supporting the decisions are all the same computational object. In classical mechanism design, the designer is a person. The empirical inference is in a separate paper. The agent (the implementation) is a regulation. The three were decoupled.

In a production LLM agent that calls causal-ML tools, recommends a mechanism, and whose outputs update the data on which the next iteration will be trained, the decoupling vanishes. The designer is the agent. The empirical inference is the agent's tool call. The mechanism is the agent's recommendation. The next iteration's training data is determined by the current mechanism's deployment.

This tight coupling is the thing that economics has not yet reckoned with, that agent research has not yet reckoned with, and that causal inference has not yet reckoned with. It is nevertheless the operational reality of an increasing fraction of applied decision-making. It is what I see in production. It is the intellectual territory I believe is most important to map over the next five years.

## The 18-month research roadmap

Concretely, here is what I intend to produce over the next eighteen months.

**Paper 1 (by month 4).** The panel-aware causal forest methodology paper, already drafted to 60 percent. Target venue: NeurIPS Causal ML workshop or *Journal of Causal Inference*. Primary readership: methodology researchers at MSR, Google Research, and academic econometrics.

**Paper 2 (by month 6).** Agent reliability patterns for causal decision systems. Generalizes observations from five production agents into a reliability framework. Target venue: ICML or NeurIPS agents-track workshop. Primary readership: applied-ML research groups that deploy agents.

**Paper 3 (by month 10).** Causal evaluation of LLM-driven mechanism implementation. This is the signature piece. Target venue: EC 2026 or AAAI mechanism-design track. Primary readership: MSR Economics, Google Research Economics, and academic mechanism design.

**Paper 4 (by month 12).** Elasticity-aware robust mechanism design, combining DRO, conformal prediction, and Myerson. Target venue: KDD ADS track or *Marketing Science*. Primary readership: applied economics and industrial applications of mechanism design.

Alongside the papers, I will open-source three tools: a fixed-effects-aware causal forest (already in progress), a framework for causal evaluation of agent decisions, and a reference implementation of elasticity-aware mechanism optimization. Open-source artifacts are a credential for the applied-research community in a way that papers alone are not.

## What this looks like five years out

If the eighteen-month plan lands, the five-year horizon is this. I lead a research group that owns the intersection of LLM agents, causal inference for panel data, and mechanism design under uncertainty. The group ships methods papers at the top venues (NeurIPS, ICML, EC, AEA). It ships open-source tools that become standard in the applied community. It consults on real production mechanism-design problems at large firms. It produces researchers who themselves go on to lead research programs at industry or academia.

The group is small, six to twelve scientists. It is not a product-feature group. It is not a trading-strategies team. It is an applied-research group that produces both methodology and shipped systems, because the research questions are only correctly posed when you can see how real deployments work.

The work is intrinsically interdisciplinary, which means it will be hard to staff and harder to explain to management. That is fine. The scientists I want to recruit are people who are equally comfortable with Myerson's 1981 theorem, Pearl's do-calculus, and debugging a Bedrock agent in production. That set is small but extraordinary. A lab that identifies and concentrates them creates a durable intellectual advantage that cannot be replicated by throwing more generic ML researchers at the problem.

The intellectual dividend of such a lab is a coherent body of work that the rest of the applied-ML community looks to when they want to understand how to ship causal-ML-backed agent systems responsibly. The business dividend is that the lab's methods flow into products and services whose aggregate revenue is substantial, because every firm doing personalized pricing, personalized incentives, marketplace mechanism design, or agent-assisted decision support will eventually need the research we produce.

I am not building a research group in the abstract. I am already building it in practice, at smaller scale, through the production systems I ship and the research I write. The question I would pose to anyone considering hiring me for a leadership role is whether they see the same convergence I see. If they do, they have to decide whether they want their organization to be the one where this research intersection is defined.

*This is a research agenda, not a hiring pitch. I intend to execute it at whichever institution gives me the time, the collaborators, and the industrial access to do the work seriously. If that is the lab you lead, I would welcome a conversation.*
