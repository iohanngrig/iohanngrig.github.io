---
title: "From theoretical physics to applied AI: what transferred, what didn't"
date: 2026-04-04
description: "An intellectual genealogy of the transition from theoretical high-energy physics to applied machine learning and agent development."
tags: [writing, career]
draft: false
---

I spent eleven years in theoretical physics, five as a doctoral student and six as a postdoctoral researcher at Argonne National Laboratory, Ohio State, and New York University. By 2014 I had produced a respectable body of work in quantum field theory applied to gauge theories, lattice formulations, and related topics. Then I left the academic track. Two years as a fixed-income quantitative researcher at Citi, then the shift into applied machine learning, and today I am a Senior Applied Scientist at Amazon, shipping production Bedrock agents and causal-ML pipelines. The transition worked. I have noticed that many physicists who make this move tell a story about how their physics background became useless. That is not my experience.

I want to lay out what actually transferred, what did not, and what I wish someone had told me in 2013 about the translation. The intended readers are two. First, physicists considering the same jump. Second, hiring managers trying to evaluate a physicist who has already jumped. I hope to clarify what the relevant signal is and what it is not.

## What transferred well

### The renormalization group as a theory of inductive bias

The renormalization group, invented by Kadanoff and Wilson in the 1960s and 1970s, is a machine for extracting the relevant degrees of freedom from a complicated system. Given a microscopic theory with many parameters, you ask what the low-energy, long-wavelength effective theory looks like. The answer comes from iteratively integrating out the fine-grained modes and tracking how the couplings flow.

The lesson of the RG is that the world is organized by scales. At some scales, the appropriate description is one thing. At others, it is something else entirely. The map between the two is computable: you can derive the coarse-grained theory from the microscopic one by systematically averaging over irrelevant details.

This generalizes directly to inductive bias in machine learning. A neural network's architecture encodes an implicit commitment about the relevant scales of the problem. Convolutions assume translation-equivariance at pixel scale; attention assumes soft context-dependence without a built-in range. The right architecture for a task is the one whose implicit RG flow matches the data. When you see deep-learning papers arguing about "inductive bias," they are making RG-flavored arguments without the vocabulary.

For an applied ML practitioner, carrying this intuition into the work matters. When a model with an inductive bias mismatch fails at scale, the RG frame tells you *why*: you were sitting at the wrong fixed point. When Chinchilla suggested we had been training at the wrong compute-data ratio, the argument was an RG-style one about optimal scaling.

### Quantum field theory as a theory of causal structure

QFT is organized around propagators, which are objects that encode how a disturbance at spacetime point $x$ affects a measurement at point $y$. The structure of the propagator determines what is causally connected to what. In a Lorentz-invariant theory, the propagator vanishes outside the light cone. That is the theorem that says information does not travel faster than light.

This has a direct analog in causal inference. Pearl's do-calculus and the potential-outcomes framework both formalize the question "what connects to what, causally" in a way that propagator calculus foreshadows. A confounder in an observational study is a variable that creates a spurious propagator between treatment and outcome, a correlation without the underlying causal connection. A valid instrument is a variable whose propagator to the outcome passes through the treatment only, analogous to a current that couples only through one vertex in a Feynman diagram.

Coming to causal inference from QFT, I found the subject strangely familiar. The careful tracking of which variables are on which side of which conditioning bar is exactly the sort of accounting that a field theorist does when computing a scattering amplitude. The honest causal forest's proof of consistency, which invokes U-statistics and Hoeffding decomposition, reminded me of perturbative expansions in which a cancellation at one order requires particular symmetries to hold. The mathematical depth of the causal-inference literature is substantial, and physicists typically find they can read it in its original form after a short adjustment period.

### Large-scale numerical simulation

Physicists running lattice QCD on supercomputers develop a particular kind of operational competence. You learn to run long-running, memory-intensive computations on distributed hardware; to diagnose when they are converging and when they are diverging; to checkpoint and restart; to tune parameters until the statistics are adequate. None of this is ML-specific. All of it transfers to training large neural networks.

I spent part of my postdoctoral time on lattice gauge-theory simulations and part on distributed Markov chain Monte Carlo. When I later sat with deep-learning colleagues discussing loss-landscape dynamics, learning-rate schedules, and the engineering of distributed training, the conversation was immediate and productive. The specific tools are different. My conjugate-gradient solvers became Adam, my Wilson-line observables became loss curves. The operational posture underneath is identical.

### Mathematical comfort under high uncertainty

Physics training cultivates a particular epistemic stance. You work on problems where the answer might be wrong. You hold ideas provisionally. You express results with careful error bars, because if you miss by three sigma you are wrong. You learn to separate "I know this because I proved it" from "I believe this because the evidence is accumulating" from "I suspect this because it fits." This is an ordinary property of senior researchers in any discipline, but physics cultivates it especially hard because the gap between theoretical speculation and experimental verification can be decades.

The same stance is useful in applied ML. A model that works well on the training distribution might fail on the distribution shift. A benchmark result might be inflated by data contamination. A scaling prediction might hold for one architecture and not another. Being comfortable with provisional belief, with error bars, with the gap between what we know and what we think, is the foundational cognitive skill that lets you lead research rather than just do it.

## What did not transfer

### Specific physics content

The specific quantum field theory I knew did not help me at Citi or Amazon. I did not compute any Feynman diagrams at work. I did not use my expertise on lattice gauge theory to analyze mortgage-backed securities. The domain knowledge of theoretical physics is, as a hiring manager might suspect, essentially useless in applied industrial contexts outside of a few specialized research labs.

This is fine. Nobody hires a physicist for their domain knowledge; they hire them for their mathematical maturity. If you are a physicist looking to transition, stop advertising your expertise in renormalization-group flows and start advertising your ability to absorb a new mathematical subject in three months and be productive in six.

### Academic publication rhythm

Academia rewards slow, careful, correct work. Industry rewards shipped, revenue-generating, good-enough work on a rolling calendar. The physics training teaches you to spend a year on one problem until you have a publishable result. The industry training teaches you to make ten incremental improvements in a year, each shipped and measured, none of them individually publishable.

This is a cultural adjustment that catches many physicists off guard. For the first year after my transition I kept searching for the equivalent of a paper in my quarterly deliverables, and I kept feeling like the work was not substantive enough. The correct reframe took a while to internalize. The deliverable is the deployed system, which is the analog of a paper, but its citation count is measured in dollars of business impact rather than academic citations. Once the substitution clicked, my productivity rose sharply.

### The theoretical-physics style of explanation

Theoretical physicists communicate a result as a mathematical derivation. Start from a Lagrangian, apply the symmetries, derive the consequences. The audience is expected to follow and check. This style is excellent for establishing correctness, and terrible for communicating to non-specialists.

Industry communication has to land in five bullet points or a two-paragraph summary. The derivation lives in an appendix, if anywhere. The headline is a statement of business impact in dollars and an assertion of statistical significance. This style took me about eighteen months to learn, and another eighteen to master. If you are transitioning, the single highest-leverage thing you can practice is condensing a three-page derivation into a three-sentence executive summary.

### The ex-academic hierarchy

Academia has a status hierarchy tied to specific journals, conferences, advisors, and institutions. An ex-physicist arriving in industry may try to reproduce this hierarchy. "I published in PRL, I trained at MIT, my advisor was so-and-so." Nobody outside a narrow academic-adjacent slice cares. The industrial hierarchy is different. It is based on what you have shipped, the business impact, and what your team of engineers thinks of your code reviews. Arriving with the academic hierarchy pre-loaded makes you legible to other ex-academics and invisible to everyone else.

My advice: in the first year, do not mention your academic record. Establish yourself on the ground. After a year, the people who matter will know you through your work. At that point the academic record becomes useful context, but it is never the primary credential.

## What a hiring committee should look for in an ex-physicist

If you are a hiring manager evaluating a physicist-turned-applied-ML candidate, these are the signals that separate a successful transition from a nominal one.

**A shipped production system.** Papers and academic projects are not enough. A shipped system, one that is used by real people to make real decisions, tells you the candidate has cleared the culture-shift hurdle. If a physicist candidate has been in industry five years and has never shipped a system, they are still in an academic mindset.

**Facility with a broad ML toolkit.** The candidate should be comfortable switching between a causal model, a deep learning architecture, and a traditional statistical method, choosing the right tool for the problem rather than defaulting to one. If they only use neural networks, they have not yet absorbed the breadth of applied ML.

**Comfort with ambiguous problem framing.** Physics trains you to work on well-posed problems. Industry rarely hands you well-posed problems. The test is whether the candidate can take an ambiguous business question and convert it into a mathematically tractable formulation. This is the single hardest skill for ex-physicists to acquire.

**Evidence of partnerships.** Has the candidate worked closely with product, engineering, and business stakeholders? Or have they been sequestered with other researchers? The former tells you they are ready for leadership. The latter tells you they have not yet earned their industrial stripes.

**Acknowledgment of what they do not know.** The worst ex-physicists come into industry certain that their mathematical sophistication makes them superior to the engineers. The best come in knowing that shipping systems requires skills they do not yet have and are eager to learn. Ask the candidate what they were wrong about in their first year of industry. If they cannot answer, they may not have reflected honestly.

## Why I made the transition, and why I do not regret it

I loved theoretical physics, and I still enjoy reading the new papers in my old subfield. But the economic and social structure of academic physics in 2014 was unforgiving. Many more trained postdocs than tenure-track positions. A hiring process that prized a handful of high-impact publications over sustained productivity. A career timeline that did not align with the life I wanted to build.

Industry is different in ways that suit me. The problems are immediate and real. The work has consequences that touch millions of people. The compensation is such that I can live in New York comfortably and support a family. The intellectual content is, in the specific research area I work on, equal to or greater than what I would have done in physics. I have not regretted the transition once.

The one thing I would tell my 2013 self is this. The transition is harder than you think but more complete than you think. You will feel like an outsider for two years and then stop feeling like one. The mathematical maturity you built will transfer completely. The culture and communication style will not, and you will need to rebuild them deliberately. The end state, where you are using your full intellectual power on problems that matter in the world, is worth the investment.

Ten years in, this is the career I would have chosen if I had known what I know now. To physicists considering the jump: the water is fine. To those already in industry and looking for leadership roles: the bridge between your physics past and your applied-AI future is not to hide the physics. It is to use it as the foundation of a research agenda that others cannot construct.

*If you are a physicist considering the transition, I am happy to correspond. Reach me at iohanngrig@gmail.com.*
