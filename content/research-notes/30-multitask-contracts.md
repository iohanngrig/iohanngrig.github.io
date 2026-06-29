---
title: "Paying for the unseen task: multitask contracts and the cost of a missing signal"
date: 2026-06-28
draft: false
tags: ["mechanism-design", "contract-theory", "incentives"]
---

# Paying for the unseen task: multitask contracts and the cost of a missing signal

> Most performance pay rewards one measured outcome. But effort usually moves several outcomes at once, and when the contract pays on only some of them, the agent rationally starves the rest. This is the multitask principal-agent problem of Holmström and Milgrom (1991), and it is the cleanest lens I know for a recurring failure in incentive design: a metric looks fine, the paid task improves, and an unpaid task that the same effort would have improved quietly decays. We work through the model, the linear-contract result that makes it tractable, and a small extension, a partially pooled bonus, that recovers the missing task without paying the full cost of team-based pay.

## 1. The problem, stated plainly

An agent exerts effort that raises two outcomes: one the principal can measure and pay on, and one the principal also values but does not reward. Classical single-task intuition says "pay a share of the measured outcome and effort follows." Multitask theory says something sharper and less comfortable: when one task is rewarded and a second, complementary task is not, strengthening the incentive on the first can *reduce* effort on the second, because the agent reallocates a fixed effort budget toward where the money is. The unrewarded task is not merely under-supplied in absolute terms; it is actively crowded out.

The practical signature is familiar. A platform pays partners on directly attributed outcomes and separately captures value from a second channel that the same quality effort drives. The second channel's value never enters the partner's pay, so quality effort is supplied only up to the point the first channel justifies. The shortfall is invisible on the paid metric and shows up only where no one is looking.

## 2. Why the contract is linear

Under constant-absolute-risk-aversion preferences and Gaussian noise, Holmström and Milgrom (1987) prove the optimal contract is **linear in aggregate output**. This rules out option-like or step contracts as the optimum and is what makes the problem analytically clean: the design space collapses to a few slopes. Holmström and Milgrom (1991) then show that with multiple efforts and signals, the optimal slopes must spread incentives across tasks, and any task without a signal to pay on is supplied below first-best. Holmström (1982) supplies the third ingredient, that shared-output (team) pay induces free-riding which, under risk aversion, cannot reach first-best.

These three results bound the design. A useful contract should be linear (1987), it should attach a slope to the previously unrewarded task (1991), and if it pools across agents to reduce risk it should pool only partially, because full pooling pays the team free-rider cost (1982).

## 3. A partially pooled bonus

Keep the existing pay on the measured outcome and add a slope on a signal for the second task, with a small pooled component. For agent $c$ in a cohort of size $N$, with $O_c$ the measured outcome, $\pi_c$ the second-task signal, and $\bar\pi$ the cohort mean of that signal:

$$
w_c \;=\; \underbrace{r\,O_c}_{\text{existing pay}} \;+\; \underbrace{\beta\bigl[\alpha\,\pi_c + (1-\alpha)\,\bar\pi\bigr]}_{\text{new partially pooled bonus}},
$$

with share $\beta \in [0,1]$ and individual-vs-pooled weight $\alpha \in [0,1]$. This nests the familiar cases: $\beta = 0$ is the status quo, $\alpha = 1$ is a pure individual bonus, $\alpha = 0$ is a pure pool. The interior point is the object of interest, and the contract *adds* to existing pay rather than replacing it, which preserves the legal and accounting classification of the base.

## 4. The free-rider term falls out of the first-order condition

Let the measured outcome and the second signal have effort-increasing means $\mathbb E[O_c]=\mu_O\big(1+a_O(e_c-\tfrac12)\big)$ and $\mathbb E[\pi_c]=\mu_M\big(1+a_M(e_c-\tfrac12)\big)$ with additive noise, and let the effort cost $\tfrac\kappa2 e_c^2$ be quadratic. The symmetric Nash effort is

$$
e^\star \;=\; \frac{r\,a_O\,\mu_O \;+\; \beta\,a_M\,\mu_M\bigl(\alpha + \tfrac{1-\alpha}{N}\bigr)}{\kappa}.
$$

Only the agent's own $\tfrac1N$ share of the cohort mean responds to the agent's own effort, so the pooled part of the bonus enters attenuated by $\alpha + \tfrac{1-\alpha}{N}$. At $\alpha = 1$ the second-task incentive is at full strength; at $\alpha = 0$ it scales as $1/N$ and vanishes for large cohorts. That bracket is the Holmström (1982) team effect made explicit, and it is why a pure pool cannot motivate effort and why the pooled component must stay small.

## 5. The weight is a noise-versus-incentive trade

Total welfare nets the principal's surplus against the agent's risk premium. Effort, and therefore the surplus terms, is maximized at $\alpha = 1$. Pay variance moves the other way, but only conditionally: pooling diversifies away idiosyncratic second-task noise, and the variance reduction it buys scales with $(1-\rho)$, where $\rho$ is the cross-agent correlation of that noise, so the benefit of pooling vanishes as $\rho \to 1$. The interior optimum $\alpha^\star$ therefore rises with the productivity-to-noise ratio of the second signal, rises with the cohort correlation $\rho$, and falls with risk aversion. The reading is intuitive: pool more (lower $\alpha$) when the individual signal is noisy and agents' shocks are independent; pool less when the signal is clean or the shocks move together. When the cohort is tightly correlated, pooling buys almost no variance reduction and the contract collapses toward a pure individual bonus ($\alpha \to 1$).

## 6. Where this holds and where it breaks

* **Attribution is the load-bearing assumption.** The whole construction requires a per-agent signal $\pi_c$ for the second task. If that signal cannot be attributed with reasonable accuracy, the incentive degrades in proportion, and this is a measurement problem outside the theory.
* **The calibration is illustrative, not estimated.** Effort cost and risk aversion are not directly observable; the *structural* result, that a partially pooled bonus dominates the status quo, a flat payment, a pure individual bonus, and a pure pool, is robust across plausible ranges, but the exact optimal weights are not pinned down without a natural experiment or structural estimation.
* **One period.** Real relationships are dynamic, with effort learning, depreciation, and payment lags; a dynamic treatment would likely raise both the share and the individual weight.
* **Linear pay invites gaming.** A linear bonus on the second signal rewards inflating that signal; a floor that withholds the bonus on loss-making outcomes converts the clean linear contract into a linear-plus-floor structure not modeled here.

## 7. The general lesson

The result that travels beyond this specific contract is the diagnosis, not the formula. When you strengthen an incentive and a complementary outcome you also care about gets worse, suspect a multitask problem before you suspect the agents. The fix is rarely a bigger lever on the measured task; it is a slope, however small, on a signal for the task you were not paying for, with just enough pooling to cut variance and not so much that free-riding eats the incentive. Pay for the unseen task, and pool only as far as the noise requires.

## References

* Holmström, B. (1979). *Moral hazard and observability.* Bell Journal of Economics, 10(1), 74–91.
* Holmström, B. (1982). *Moral hazard in teams.* Bell Journal of Economics, 13(2), 324–340.
* Holmström, B., & Milgrom, P. (1987). *Aggregation and linearity in the provision of intertemporal incentives.* Econometrica, 55(2), 303–328.
* Holmström, B., & Milgrom, P. (1991). *Multitask principal-agent analyses: incentive contracts, asset ownership, and job design.* Journal of Law, Economics, & Organization, 7, 24–52.
* Innes, R. (1990). *Limited liability and incentive contracting with ex-ante action choices.* Journal of Economic Theory, 52(1), 45–67.
* Cachon, G., & Lariviere, M. (2005). *Supply chain coordination with revenue-sharing contracts.* Management Science, 51(1), 30–44.

*The model in this note is developed on a fully synthetic two-sided-platform abstraction; the parameter values used to illustrate the optimal weights are chosen for exposition, not estimated from any dataset.*
