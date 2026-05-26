---
title: "Pairs trading and cointegration"
date: 2026-04-19
tags: ["statistical-arbitrage", "time-series", "cointegration"]
---

# Pairs trading and cointegration

> A pair of nonstationary asset-price processes can have a *stationary* linear combination. This is **cointegration** (Engle-Granger 1987; Johansen 1988), and it is the theoretical foundation for pairs trading: enter when the stationary spread deviates far from its mean, exit when it mean-reverts. The demo constructs two synthetic cointegrated series, shows the spread with entry bands, and discusses why real-world pairs trading has become much harder since the 2000s.

## 1. Cointegration, formally

A collection of series $(X_t, Y_t)$ is **cointegrated** of order $(1, 1)$ if:

1. Each series is individually $I(1)$, integrated of order 1, i.e., nonstationary but first-differences are stationary.
2. There exists a linear combination $X_t - \beta Y_t$ that is $I(0)$, stationary.

The cointegrating coefficient $\beta$ is the key: if estimable, it defines a mean-reverting spread $Z_t = X_t - \beta Y_t$ that can be traded.

## 2. The demo

We simulate two assets sharing a common nonstationary trend:

$$
X_t = \text{trend}_t + \epsilon^X_t, \qquad Y_t = 1.05 \cdot \text{trend}_t + \epsilon^Y_t,
$$

where $\text{trend}_t$ is a random walk and $\epsilon^X_t, \epsilon^Y_t$ are stationary idiosyncratic noise. The cointegrating coefficient is $\beta = 1.05$ by construction. The spread $Z_t = X_t - 1.05 Y_t$ is stationary with a well-defined mean and variance.

![Two cointegrated assets and their stationary spread with trading signals](/applications/figures/app-pairs-trading.svg)

The upper panel shows the two nonstationary series; neither is stationary on its own, but they move together. The lower panel shows the spread with $\pm 2\sigma$ entry bands. Long signals (below the lower band): buy the spread (long $X$, short $\beta Y$). Short signals (above the upper band): sell the spread.

## 3. The trading strategy

Classic pairs trading rules:

- **Enter** when $|Z_t| > k\sigma$ (typically $k = 2$).
- **Exit** when $Z_t$ returns to $|Z_t| < 0.5\sigma$ or crosses the mean.
- **Stop loss** when $|Z_t| > 3\sigma$ or when cointegration appears to break (rolling-window cointegration test fails).

The Sharpe ratio of the strategy depends on (a) the speed of mean reversion of the spread, (b) the bid-ask and market-impact cost of the two legs, and (c) the frequency of cointegration break-ups.

## 4. Johansen vs. Engle-Granger

Two standard estimation frameworks.

**Engle-Granger two-step.** (1) Estimate $\beta$ by OLS: regress $X_t$ on $Y_t$. (2) Test the residual $\hat Z_t$ for stationarity via augmented Dickey-Fuller (ADF). If the ADF test rejects a unit root, the pair is cointegrated. Simple but sensitive to variable ordering.

**Johansen test.** Eigenvalue-based estimator that handles multivariate cointegration and does not require choosing a dependent variable. Preferred in practice for more than two series, and a better option even for pairs when the direction of causation is unclear.

## 5. Why pairs trading is harder than it looks

The empirical record since the 2000s is sobering.

**Gatev, Goetzmann & Rouwenhorst (2006)**, the canonical empirical pairs-trading paper, find that the strategy produced annualized returns of ~11% in the 1962–2002 period. **Do & Faff (2010)** show the returns decayed substantially after the early 2000s. By the 2010s, simple cointegration-based pairs trading was competitive with basic risk-parity on a risk-adjusted basis.

Reasons for decay:

- **Increased competition.** Quantitative hedge funds arbitraged away the easiest pairs.
- **Higher transaction costs on "exotic" legs.** Many formerly-profitable pairs had low-liquidity components whose execution costs erased the statistical edge.
- **Cointegration breakups.** The statistical relationship between two securities is less stable than the method assumes. Rolling cointegration tests often reject today what was tested positive a year ago.

Modern statistical-arbitrage work has moved to higher-dimensional baskets (50–500 stocks) with factor-adjusted residuals, machine-learned signals on top of classical cointegration, and high-frequency intraday versions of the same logic.

## 6. References

- **Engle, R. F., & Granger, C. W. J.** (1987). *Co-integration and error correction: representation, estimation, and testing*. Econometrica, 55(2), 251–276.
- **Johansen, S.** (1988). *Statistical analysis of cointegration vectors*. Journal of Economic Dynamics and Control, 12(2-3), 231–254.
- **Gatev, E., Goetzmann, W. N., & Rouwenhorst, K. G.** (2006). *Pairs trading: performance of a relative-value arbitrage rule*. Review of Financial Studies, 19(3), 797–827.
- **Do, B., & Faff, R.** (2010). *Does simple pairs trading still work?* Financial Analysts Journal, 66(4), 83–95.
- **Hamilton, J. D.** (1994). *Time series analysis*. Princeton University Press.
