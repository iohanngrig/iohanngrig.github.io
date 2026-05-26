---
title: "What I would build in the first 90 days as a Research Director"
date: 2026-04-12
description: "A concrete plan for the first 90 days of a hypothetical Research Director role: team onboarding, research-program selection, deliverable milestones, and external engagement."
tags: [writing, leadership]
draft: false
---

A common interview question for research leadership roles: "what would you do in the first 90 days?" I have been asked versions of this question and have asked it myself of candidates I was evaluating. The quality of the answer tells you substantially more about a candidate's readiness for leadership than any technical interview.

The worst answers are generic. "I would meet with stakeholders, understand the team's priorities, and build trust." The best are specific about the particular research context, realistic about what 90 days can and cannot accomplish, and anchored in concrete deliverables that someone can evaluate. Here is my answer, calibrated for a Research Director role leading a small-to-medium applied-research group (six to twelve scientists) at a company like Amazon, Microsoft, or Google.

## The situation I am writing for

I am assuming a specific scenario. I am hired as Research Director of an applied-research group of eight scientists working on causal-ML-backed decision systems. The group has an existing research portfolio, a relationship with a product organization that uses the research, and a history, some of it good, some less so. I am not hired into a greenfield. I am inheriting a going concern.

This is the most common Research Director scenario, and it is the one for which my plan is calibrated. A greenfield situation would require different emphasis: more hiring, more team formation, less existing-relationship management. A research-lab-in-crisis scenario would require different tactics: more triage, more conflict resolution, less pure-research direction-setting.

## Week 1 to 2. Listen and diagnose

The single worst thing a new Research Director can do is arrive with a strategic plan and announce it. No matter how good the plan is, announcing it before listening signals that the leader does not actually care about what the team has been doing. That signal poisons the relationship with the existing researchers. They are the people whose work is going to determine whether the next year goes well.

The first two weeks are dedicated to listening.

**One-on-ones with every team member.** Thirty minutes each. The agenda: what are you working on, what do you care about, what is going well, what is frustrating, what would you change if you were in my seat. I take notes and do not offer opinions. The goal is to build a concrete, detailed model of what the team is actually doing, which is often different from what the organization claims the team is doing.

**Two-on-ones with adjacent leaders.** The partner engineering director, the adjacent science director, the product leader who consumes the research output. Thirty to forty-five minutes each. The agenda is similar. What is going well, what is frustrating, what are the unstated expectations of my group. Particular attention to where the team's delivery has previously fallen short of expectations. Those gaps are where the first performance tests will come.

**Deep reads of recent work.** Every paper the group has published in the last eighteen months. Every internal doc circulated in the last six months. The code review history for the top three projects. This reading produces a specific technical understanding of what the group has done, where the research is strong, and where the engineering or methodology has gaps.

**Stakeholder mapping.** A concrete org-level map of which other groups consume the research, which groups produce data the research needs, which leaders are patrons or critics. This map becomes the infrastructure for everything that follows. I spend real time on it.

By end of week 2, I have a detailed mental model of the team's current work, its relationships with adjacent teams, and its reputation. No commitments made, no plans announced.

## Week 3 to 4. Convert listening into a two-page thesis

By week 3 I have enough information to form specific views about three things. Where the research portfolio is strong and should be protected. Where it is weak and should be fixed. Where there are empty spaces that a Research Director should fill. I write these views as a two-page document that I share with my director and with the team.

The document is titled something like "First-quarter research priorities for [group]." It is concrete. It names specific research programs that are strong and explains why they should continue. It names specific programs that need repair and explains what repair looks like. It identifies one or two new research directions the group should enter and explains the intellectual rationale.

The two-page document is the artifact that, if I did this job well, my director and team will judge me on for the first year. I do not mind publicly committing to it. If it turns out to be wrong, I will revise and be transparent about why. Publishing the thesis at week 3 is a signal that I am running the group seriously and not hedging against accountability.

A common mistake is to treat the two-page thesis as an internal consensus-building document that edits out anything controversial. The edits produce a bland document that signals nothing. The controversial items are exactly what a leader should be committing to publicly, because the existence of the commitment raises the cost of later retreating from it.

## Month 2. Hire, staff, and ship

With the thesis set, the next month is executing the concrete moves that follow from it.

**Immediate hiring or reallocation.** If the thesis identified a staffing gap (for example, "we need one person dedicated to agent reliability research"), I start the hiring or reallocation process that day. If a gap is filled by reallocating an existing researcher, I have the one-on-one conversation with them the same week, explaining the move, the intellectual rationale, and what success looks like in the new role.

**Project scoping for existing work.** Each of the existing research programs gets a six-month roadmap. I write the first draft after talking to the lead researcher. We iterate for a week. The document is frozen by the end of month 2. The roadmap has concrete deliverables with dates, dependency on other teams, explicit risk factors, and success criteria that would be visible from outside the group.

**Product-partnership contracts.** If the thesis identified a gap in product-research alignment ("the product team is asking for X which our research does not deliver"), I have the direct conversation with the product leader and formalize the request. Either we commit to do X with a timeline, or we explicitly decline X with the reason. The un-explicit state is the one to avoid.

**External engagement plan.** Every research group needs external visibility through publications, invited talks, and open-source releases. I draft a 12-month external-engagement calendar and review it with the team. This is where researchers get accountability-neutral places to build their own research reputations, which is a recruiting and retention tool.

By end of month 2, I have a hiring decision for any open gaps, a six-month roadmap for each research program, one or two concrete product-partnership deliverables, and an external engagement calendar. The team has seen me execute at pace on specific commitments.

## Month 3. Protect the research time

Once the plan is set and the roadmap is aligned, the highest-leverage work of a Research Director is protecting the team's time. This sounds soft. It is the hardest and most consequential job.

Research time is under constant attack from three directions. Product escalations: something broke, can the research team help triage. Management overhead: quarterly planning, review cycles, promotion discussions. Opportunistic asks: a new VP has a new idea, please investigate. A Research Director who does not actively protect the research calendar will find that three months in, the team has been entirely pulled into firefighting and the original roadmap has been discarded.

Concrete tactics.

**Default escalation responder.** All escalations route to me first. I triage. If it is genuinely urgent and research-shaped, I assign it. If it is urgent but not research-shaped, I route it elsewhere. If it is research-shaped but not urgent, it goes on a list and gets addressed in the next sprint. The team does not see the noise. They see the work I have filtered and prioritized.

**Calendar defense.** I actively push back on meeting requests that do not have a clear decision. If someone wants my scientists to attend a status review where no decisions will be made, I attend alone and summarize back. The multiplier is large. Saving each scientist one hour per week compounds into four to eight hours of recovered research time per week per scientist.

**Cross-team liaison.** When the partner engineering team needs information from the research team, I am the primary point of contact for most of it. I translate engineering-urgent asks into research-shaped work, and I translate research progress into engineering-actionable summaries. The translation is a sustained cost. It buys the researchers more time on research and less on negotiation.

**Saying no.** The hardest and most underrated part of the job. Saying no to asks that are reasonable but not aligned with the research thesis. Saying no to the patron executive who wants the group to pivot to their current priority. Saying no to the product team who wants a scientist assigned to full-time support. The no-saying is where the reputation for clarity is built, and where the team learns that their time is protected.

By end of month 3, the team should have more research time than they did when I started. If they do not, I am failing.

## The 30/60/90 deliverables

Here are the specific deliverables I commit to for the first 90 days.

### Day 30

- Two-page research priorities thesis, published internally and reviewed with director.
- Complete one-on-ones with every team member and adjacent leader.
- Stakeholder map drafted and validated.
- Reading review of all team output from the last 18 months.

### Day 60

- Six-month roadmaps in place for each research program.
- Any staffing gaps from the thesis either filled or in active recruiting.
- First product-partnership contract executed (either commitment with timeline, or explicit decline with rationale).
- External engagement calendar published.
- First external presentation planned (an invited talk at a conference, workshop, or university seminar).

### Day 90

- Research roadmaps delivering against their first milestone, or a written diagnosis of why they are not, with a revised plan.
- At least one paper submitted to a target venue.
- At least one open-source release made.
- Team time-utilization moved substantially toward research hours.
- First cross-team research collaboration agreed, or actively in negotiation.

These deliverables are specific enough that at day 90 anyone can evaluate whether I did the job. They are aggressive but not unrealistic. I have seen all of them hit within 90 days on comparable leadership transitions.

## What I would not do

Two things I deliberately avoid in the first 90 days.

**Big reorganizations.** Research Directors new to a group who immediately reorganize the team structure tend to signal that they do not trust the people who were there before them. The signal is a recruiting and retention liability. If a reorganization is needed, I wait until month 4 or 5, after I have earned the credibility to make the case. Nothing substantive is lost by the wait.

**Public critique of prior leadership.** Even when the prior leader made decisions I would not have made, the public version is about building the future, not relitigating the past. The team will be watching closely for whether I treat my predecessor's decisions charitably. If I pass this test, they trust me with future decisions. If I fail it, they become cautious about sharing information that might be used against them. Being charitable about predecessors is a 90-day investment that pays dividends for years.

## The leadership test at 90 days

At day 90, the hiring manager or my director will evaluate me on three things. Did I execute on the commitments I made in month 1? Did I protect and strengthen the team? Did I set the direction for the next six months in a way that the team and adjacent organizations can align behind? Each of these is testable from outside the group.

The interview version of the 90-day question tests whether I have the judgment to know which of those three tests matters, and the realism to understand what 90 days can and cannot accomplish. A candidate who promises a three-paper research breakthrough in 90 days is not credible. A candidate who commits to the specific deliverables above, explains the tradeoffs, and acknowledges the risks is operating at the right level.

## Why I would be ready for this role

The 90-day plan above is not hypothetical for me. I have seen this playbook executed well and badly by research leaders I have worked with. I know which parts are rare and therefore worth highlighting. I have done pieces of this work at smaller scope: running technical partnerships, leading cross-functional research coordination, making the judgment calls about which research is worth pursuing and which is not. What I have not yet done, at Research Director scope, is put all of it together and own the outcome.

The right hiring manager for this role will look at my technical track record (substantial), my existing delivery experience (shipped production systems, cross-org research circulation, internal reading groups), my writing and communication quality (these essays, my paper drafts, my internal docs), and will make a judgment about whether I have the readiness. I believe the answer is yes. The 90-day plan is concrete evidence of how I would execute, presented in advance so that the hiring manager can evaluate my judgment rather than take it on faith.

---

*If you are a hiring manager for a Research Director role and want to discuss any of the above in more detail, I am at iohanngrig@gmail.com.*
