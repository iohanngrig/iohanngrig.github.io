---
title: "Multi-agent coordination and emergent behavior"
date: 2026-02-22
draft: false
tags: ["multi-agent", "game-theory", "coordination", "rl"]
---

# Multi-agent coordination and emergent behavior

> A single agent optimizes its reward against a fixed environment. Multiple agents optimize against *each other*, and the environment they present to one another changes as they learn. We cover the classical game-theoretic baseline (Nash equilibrium and its computational complexity), the two ways that coordination can fail (social dilemmas, non-stationarity), and the mechanisms by which cooperative behavior emerges in iterated settings. The contemporary stakes are high: every LLM deployed to interact with other LLMs or with humans is a multi-agent system, and the theory of how such systems reach (or fail to reach) stable equilibria is consequential for alignment, safety, and economics.

## 1. The one-shot baseline

A **game** is a tuple $(N, \{A_i\}, \{u_i\})$: $N$ agents each with an action set $A_i$ and a utility $u_i : A_1 \times \cdots \times A_N \to \mathbb{R}$.

A **Nash equilibrium** is a profile $(a_1, \ldots, a_N)$ such that no agent can improve by unilateral deviation:

$$
u_i(a_i, a_{-i}) \;\ge\; u_i(a'_i, a_{-i}) \quad \text{for all } a'_i \in A_i, \text{ for all } i.
$$

Nash's theorem (1950) guarantees existence in mixed strategies for finite games. Existence does not imply uniqueness or efficiency, two critical failures.

### 1.1 The prisoner's dilemma

The canonical example.

![Prisoner's dilemma payoff matrix](/research-notes/figures/ma-fig1-prisoners.svg)

The unique Nash equilibrium is (Defect, Defect) with payoff $(1, 1)$. The socially optimal outcome is (Cooperate, Cooperate) with payoff $(3, 3)$. Every one-shot rational agent defects. The mechanism-design reading: the game is misspecified for the behavior we want.

### 1.2 Computational complexity

**Daskalakis, Goldberg & Papadimitriou (2009)** proved that computing a Nash equilibrium is **PPAD-complete**, in the same complexity class as Brouwer fixed points, and (if PPAD ≠ P) not solvable in polynomial time. This is a deep negative result: even for moderate-size games, finding an equilibrium is intractable by general-purpose methods.

The practical consequence: **we can't expect learning agents to converge to Nash equilibria in general**. Any convergence guarantees in multi-agent learning must exploit special structure (zero-sum, potential games, convex games).

## 2. When coordination fails

Two distinct failure modes.

### 2.1 Social dilemmas

Any game where the Nash equilibrium is socially suboptimal is a social dilemma. Prisoner's dilemma is the two-agent case; the $n$-agent generalizations include:

- **Tragedy of the commons.** Each agent's optimal use of a shared resource exceeds the socially-optimal per-agent usage.
- **Public goods provision.** Each agent under-contributes to a shared benefit.
- **Arms races.** Each agent over-invests in defensive or offensive capability because others are doing the same.

In the AI context, **Dafoe et al. (2020)** argue that multi-agent AI failures are more likely to come from social-dilemma dynamics than from single-agent alignment failures: each AI system optimizes its local objective, and the collective outcome is a race-to-the-bottom.

### 2.2 Non-stationarity and the moving-target problem

Every agent's "environment" is the other agents' policies. As other agents learn, each agent faces a non-stationary environment, the distribution of states and rewards shifts.

Standard RL convergence guarantees (value iteration, policy gradient) assume stationarity. In multi-agent RL, they break. Agents can **chase each other's past policies**, oscillating without converging. Or they can converge to an equilibrium that is different from the Nash of the underlying game, simply because the *learning dynamics* are not reliable at finding the true fixed point.

**Foerster et al. (2018)**, Learning with Opponent-Learning Awareness (LOLA), explicitly models how one's updates will affect the other agent's learning, sacrificing some greediness in exchange for navigating toward more cooperative outcomes. The idea generalizes: principled multi-agent learning needs to reason about the learning dynamics, not just the one-shot payoff structure.

## 3. How cooperation emerges

Two settings where cooperative behavior reliably arises.

### 3.1 Repeated games and the folk theorem

If a social dilemma is repeated indefinitely, a much wider set of outcomes becomes individually rational via **trigger strategies**, punishing defection with future retaliation. The **folk theorem** formalizes this: in an infinitely repeated game with sufficiently patient agents, any individually-rational payoff profile is sustainable as a Nash equilibrium.

Tit-for-tat (Axelrod 1984) is the famous example in iterated prisoner's dilemma: cooperate on the first round, then copy the opponent's previous action. It wins Axelrod's famous tournament against all comers, despite being embarrassingly simple.

Two lessons:

- **Horizon matters.** Finite-horizon games unravel to one-shot Nash by backward induction. Cooperation requires the shadow of future interaction.
- **Simple strategies dominate.** Complex reasoning about opponent psychology is not the mechanism; reliable, legible, forgiving behavior is.

### 3.2 Self-play in zero-sum games

In zero-sum games (one agent's gain is another's loss), minimax strategies are well-defined and can be computed to convergence.

**AlphaGo / AlphaZero** (Silver et al. 2016, 2017) and the MuZero variant demonstrate that self-play with a learned value function can find near-optimal policies in games of enormous complexity, Go, chess, shogi. The key technical requirements are:

- **Zero-sum structure** (or near-zero-sum, as in chess), so minimax regret has a bounded notion of "better policy."
- **Perfect information** (no hidden state), so value estimates are well-defined.
- **Compute budget** matching the game's search depth.

Self-play in non-zero-sum or imperfect-information games is much harder. **CFR** (Counterfactual Regret Minimization; Zinkevich et al. 2007) handles imperfect information in zero-sum games and has achieved superhuman play in poker (Brown & Sandholm 2017).

## 4. Emergent communication and coordination

A distinct strand of multi-agent work asks whether cooperation can arise *without* explicit coordination mechanisms, can agents invent their own?

**Foerster et al. (2016)** and subsequent work show that agents with differentiable communication channels can learn to emit signals that coordinate joint action. The emergent protocols are task-dependent, often brittle, and usually lack the compositional structure of natural language. But they demonstrate that coordination *signals* are learnable under the right training pressure.

**Lazaridou & Baroni (2020)** review the emergent-communication literature. The honest summary: agents can learn to communicate, but the communication tends to overfit to the training environment and does not generalize the way human language does.

## 5. Cooperative MARL and its open problems

Cooperative multi-agent RL (all agents share a reward) is a more tractable setting than general-sum games. Even here, challenges persist:

**Credit assignment.** When the team succeeds, which agent contributed? Naive approaches (all agents get the team reward) scale poorly; more sophisticated methods (COMA, Foerster et al. 2018; QMIX, Rashid et al. 2018) use learned value decomposition.

**Exploration.** In large teams, uncoordinated exploration is wasteful. Methods like MAVEN and EDTI attempt to coordinate exploration explicitly.

**Partial observability.** Each agent sees only part of the state. Learned communication, centralized critic with decentralized execution (CTDE), and recurrent policies are the standard tools.

## 6. Social dilemmas with learned agents

The sharpest contemporary question: what do *learned* agents do in social dilemmas?

**Leibo et al. (2017)** and subsequent work show that simple deep-RL agents trained in sequential social dilemmas (extensions of iterated prisoner's dilemma to spatial, temporally-extended games) reliably fail to find cooperative equilibria, even though cooperative equilibria exist. They instead settle into low-reward mutual-defection outcomes.

**Jaques et al. (2019)** add an intrinsic motivation for **social influence** (one agent's actions causally affecting the other's) and find that this reliably nudges agents toward cooperation.

The pattern: cooperation does not emerge by accident from standard RL. It requires either explicit mechanism design (as in [note 9](/research-notes/09-mechanism-design)), reputation systems, or intrinsic motivations that reward coordination. This has direct implications for LLM agents deployed at scale: a population of LLMs, each optimizing locally, is at risk of collective failure modes that no individual agent is responsible for.

## 7. Open questions

**Scaling multi-agent methods.** Most theoretical results and empirical benchmarks involve 2–10 agents. Real systems (marketplaces, social media, LLM ecosystems) involve 1000s or more. Scaling MARL methods to this regime, without population-specific tuning, is open.

**Heterogeneous agent populations.** Agents with different architectures, objectives, or capabilities complicate everything. Most methods assume homogeneity; principled treatment of heterogeneous populations is early-stage.

**Transfer from simulation to the world.** Multi-agent methods trained in simulation often fail in deployment, where the other agents are real humans or real LLM services with their own idiosyncrasies. Sim-to-real transfer in multi-agent settings is an open empirical question.

**The population-level alignment problem.** If every LLM is aligned individually, is a population of LLMs aligned? Probably not, social dilemmas can emerge among locally-aligned agents. This is an underappreciated dimension of AI alignment.

## 8. References

- **Nash, J. F.** (1950). *Equilibrium points in N-person games*. Proceedings of the National Academy of Sciences, 36(1), 48–49.
- **Daskalakis, C., Goldberg, P. W., & Papadimitriou, C. H.** (2009). *The complexity of computing a Nash equilibrium*. SIAM Journal on Computing, 39(1), 195–259.
- **Axelrod, R.** (1984). *The evolution of cooperation*. Basic Books.
- **Silver, D., Huang, A., Maddison, C. J., et al.** (2016). *Mastering the game of Go with deep neural networks and tree search*. Nature, 529(7587), 484–489.
- **Silver, D., Schrittwieser, J., Simonyan, K., et al.** (2017). *Mastering the game of Go without human knowledge*. Nature, 550(7676), 354–359.
- **Zinkevich, M., Johanson, M., Bowling, M., & Piccione, C.** (2007). *Regret minimization in games with incomplete information*. NeurIPS.
- **Brown, N., & Sandholm, T.** (2017). *Superhuman AI for heads-up no-limit poker: Libratus beats top professionals*. Science, 359(6374), 418–424.
- **Foerster, J., Assael, Y. M., de Freitas, N., & Whiteson, S.** (2016). *Learning to communicate with deep multi-agent reinforcement learning*. NeurIPS.
- **Foerster, J., Chen, R. Y., Al-Shedivat, M., Whiteson, S., Abbeel, P., & Mordatch, I.** (2018). *Learning with opponent-learning awareness*. AAMAS.
- **Rashid, T., Samvelyan, M., Schroeder, C., Farquhar, G., Foerster, J., & Whiteson, S.** (2018). *QMIX: monotonic value function factorisation for deep multi-agent reinforcement learning*. ICML.
- **Leibo, J. Z., Zambaldi, V., Lanctot, M., Marecki, J., & Graepel, T.** (2017). *Multi-agent reinforcement learning in sequential social dilemmas*. AAMAS.
- **Jaques, N., et al.** (2019). *Social influence as intrinsic motivation for multi-agent deep reinforcement learning*. ICML.
- **Dafoe, A., Hughes, E., Bachrach, Y., et al.** (2020). *Open problems in cooperative AI*. arXiv.
- **Lazaridou, A., & Baroni, M.** (2020). *Emergent multi-agent communication in the deep learning era*. arXiv.
- **Shoham, Y., & Leyton-Brown, K.** (2008). *Multiagent systems: algorithmic, game-theoretic, and logical foundations*. Cambridge University Press.
