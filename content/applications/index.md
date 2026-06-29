---
title: Applications
---

# Applications

*Small, self-contained demos of analytical methods applied to financial and statistical problems. All use public data or synthetic DGPs; code is reproducible; there is no Amazon content here.*

These are deliberately compact, each one targets a single technique, shows a single representative figure, and documents the method at the level of a short applied-stats primer. Several originate from long-running interests predating my time at Amazon: my Citi tenure in MBS analysis, my Insight / Georgetown work on financial time-series forecasting, my Quantopian-era statistical-arbitrage research.

## The applications

### 1. Stock-price forecasting with an LSTM
[Read →](/applications/01-stock-forecasting)

Sequence-to-sequence forecasting of equity prices. The honest story: LSTMs on price series do better than random-walk only under narrow conditions, and their performance on log-returns (the right target) is rarely distinguishable from simpler baselines. Includes a synthetic-but-realistic return series demonstrating the forecasting pipeline and its residual diagnostics.

### 2. Pairs trading and cointegration
[Read →](/applications/02-pairs-trading)

Two assets that share a stochastic trend but diverge around it can be traded when their spread deviates far from its mean. The statistical foundation is cointegration (Engle-Granger 1987; Johansen 1988). Demo shows the two nonstationary series, the stationary spread, and rule-based entry/exit signals.

### 3. Portfolio optimization and the efficient frontier
[Read →](/applications/03-portfolio-optimization)

Markowitz (1952) gave the first analytical framework for choosing portfolio weights given asset return means and covariances. The demo constructs the efficient frontier for a 5-asset universe, identifies the max-Sharpe portfolio, and discusses the practical failures of the approach (parameter estimation error dominates in practice).

### 4. Mortgage prepayment modeling
[Read →](/applications/04-mortgage-prepayment)

The central modeling object in mortgage-backed-securities pricing is the conditional prepayment rate (CPR) as a function of borrower incentive. The demo walks through the S-curve parameterization, the "burnout" effect (cohorts that didn't refinance when it made sense become less responsive to future opportunities), and the implications for MBS cash-flow pricing.

## What these applications are NOT

- Not production trading systems. They are pedagogical demos.
- Not backed by proprietary data. All figures use synthetic or public datasets.
- Not related to my Amazon work. The applications live here because they reflect long-term quantitative interests that predate and are independent of my current role.

## Reproducibility

Figure generation scripts for all four applications are available in the accompanying code. Each script runs in a few seconds with standard scientific Python (numpy, matplotlib, scikit-learn).
