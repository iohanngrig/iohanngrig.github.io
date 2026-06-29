---
title: "Good-enough elasticities: why allocation regret is second-order in estimation error"
date: 2026-06-28
draft: false
tags: ["optimization", "causal-inference", "incentives", "allocation"]
---

# Good-enough elasticities: why allocation regret is second-order in estimation error

> Allocating a fixed budget across units whose response is estimated, ad spend across campaigns, incentive budget across participants, treatment across sites, has a comforting property that is easy to miss: at the optimum the objective is flat to first order, so the error in your estimated response curves costs you only quadratically. The practical consequence is that, past a modest accuracy, more effort spent sharpening elasticity estimates buys almost nothing, and the binding constraints become concavity and feasibility, not estimation precision. We prove the claim and say exactly where it stops being true.

## 1. The allocation problem

Unit $c \in \{1,\dots,M\}$ receives spend $s_c \ge 0$ and produces performance under a power law with diminishing returns,

$$
f_c(s_c) \;=\; b_c\,(s_c/s_0)^{\beta_c}, \qquad b_c > 0,\ \beta_c \in (0,1),
$$

so $f_c$ is strictly concave on $s_c > 0$. Given budget $B$ and caps $u_c$, the allocator solves $\max_{s\in\mathcal F}\sum_c f_c(s_c)$ over the polytope $\mathcal F = \{s : \sum_c s_c \le B,\ 0\le s_c\le u_c\}$. The objective is concave and $\mathcal F$ is compact convex, so an optimum $s^\star$ exists.

## 2. The optimum is water-filling, not a metaheuristic

Because the program is concave over a polytope, KKT is necessary and sufficient. Interior units are all funded to the same marginal return $\lambda$:

$$
s_c^\star \;=\; \mathrm{clip}_{[0,u_c]}\!\Big[\big(b_c\beta_c\,s_0^{-\beta_c}/\lambda\big)^{1/(1-\beta_c)}\Big],
$$

with $\lambda$ set so the budget binds. This is a one-dimensional root-find in the price $\lambda$, equalize marginal returns, clip at the caps. A population metaheuristic (differential evolution and friends) converges to the same point at far higher cost; it earns its keep only when the caps are replaced by non-convex constraints (minimum-spend thresholds, integer counts) that break concavity.

## 3. The main result: regret is $O(\varepsilon^2)$

Suppose the allocator holds estimated parameters and solves the estimated program, obtaining $\hat s$, while performance is realized under the true $F$. Define regret $R = F(s^\star) - F(\hat s) \ge 0$. Let $\varepsilon$ bound the parameter error, let $F$ be $m$-strongly concave on the funded coordinates, and let the gradient be $C'$-Lipschitz in the parameters.

$$
R \;=\; F(s^\star) - F(\hat s) \;\le\; \frac{(C'\varepsilon)^2}{2m} \;=\; O(\varepsilon^2).
$$

The proof is short. $\hat s$ maximizes the estimated objective, so it satisfies the variational inequality $\langle \nabla \hat F(\hat s),\, s^\star - \hat s\rangle \le 0$. Strong concavity of $F$ gives $F(s^\star) \le F(\hat s) + \langle \nabla F(\hat s),\, s^\star-\hat s\rangle - \tfrac m2\|s^\star-\hat s\|^2$. Add and subtract $\nabla\hat F(\hat s)$, use the variational inequality, then Cauchy-Schwarz and the Lipschitz bound, and maximize the resulting $C'\varepsilon\,t - \tfrac m2 t^2$ over $t = \|s^\star-\hat s\|$. The maximizer is $t = C'\varepsilon/m$, giving $R \le (C'\varepsilon)^2/(2m)$.

The mechanism is the envelope theorem in disguise. At the optimum the first-order conditions hold, so a parameter perturbation moves the *gradient* by $O(\varepsilon)$ but the *objective* by only $O(\varepsilon^2)$. Halving estimation error cuts realized loss four-fold; once $\varepsilon$ is small, further accuracy is nearly free of benefit. A matching $\Omega(\varepsilon^2)$ instance (a two-unit perturbation aligned with the active marginal-return difference) makes the rate tight: regret is $\Theta(\varepsilon^2)$, not merely $O(\varepsilon^2)$.

## 4. What this changes about where effort goes

The standard pipeline pours effort into elasticity estimation under the fear that error propagates linearly into lost performance. It does not. Past a modest accuracy the realized loss is quadratically small, and the real risks move elsewhere: to whether the response is actually concave (increasing returns break Section 2 and the bound), and to whether the feasible set is modelled correctly. Where estimation accuracy *does* still matter, the cleanest lever is not a better observational fit but a small randomized perturbation, an experimental slice fused with the observational panel identifies the local slope without selection bias and shrinks $\varepsilon$ at its source, which by the theorem shrinks regret quadratically.

## 5. Where the bound fails

* **Concavity is assumed.** With increasing returns ($\beta_c \ge 1$) the water-filling characterization and the bound both break, and the problem likely needs integer/threshold handling.
* **The bound is local.** It governs small $\varepsilon$. Under gross mis-specification, regret can be first-order, and the quadratic comfort disappears.
* **Strong concavity must be real.** If $m$ is tiny (a nearly flat objective near the optimum) the constant $1/(2m)$ is large; "second-order" is reassuring only when the curvature is bounded away from zero on the funded set.

## 6. The takeaway

Stop over-investing in elasticity precision and start guaranteeing concavity and feasibility. The optimum's own flatness means a good-enough response curve produces a near-optimal budget, and the cheapest way to improve a stubborn estimate is a randomized slice, not a fancier regressor.

## References

* Bertsekas, D. P. (2016). *Nonlinear programming.* 3rd ed., Athena Scientific (water-filling, KKT).
* Boyd, S., & Vandenberghe, L. (2004). *Convex optimization.* Cambridge University Press (strong convexity, envelope arguments).
* Athey, S., & Wager, S. (2021). *Policy learning with observational data.* Econometrica, 89(1) (heterogeneous effects, the experimental-fusion angle).
* Storn, R., & Price, K. (1997). *Differential evolution.* Journal of Global Optimization, 11(4).

*All quantities in this note are from a synthetic generator with known ground-truth parameters; no proprietary data is used.*
