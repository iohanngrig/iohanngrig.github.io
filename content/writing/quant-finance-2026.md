---
title: "Quant finance in 2026: where ML actually helps, where it doesn't"
date: 2026-04-05
description: "An honest assessment of where machine learning has improved quantitative finance and where classical methods remain dominant, with specific examples and deployment time horizons."
tags: [writing, quantitative-finance, machine-learning]
draft: false
---

Quantitative finance and machine learning are a famously awkward pair. Finance has two hundred years of well-developed statistics, a profound respect for out-of-sample evidence, and a culture of methodological rigor that most applied-ML communities lack. ML has more flexible models, more computational power, and more enthusiasm than finance traditionally tolerates. The combination is uneasy. Twelve years after the ML boom began to reshape adjacent industries, the question of how much ML has actually improved quantitative finance remains contested.

My perspective comes from more than one angle. I spent 2014-2015 as a quantitative researcher in mortgage-backed securities at Citi Global Markets, working on classical stochastic-calculus-based prepayment models. I won the Quantopian trading contest across four months in 2019 using a mix of traditional statistical and ML-adjacent techniques. I have followed the quantitative-finance literature closely through my professional network, and I continue to read the papers that appear at the AEA, SoFiE, and American Finance Association meetings. Since 2024, I have shipped production ML systems at Amazon. The Amazon work is not financial ML, but the engineering principles carry over.

This essay is my honest assessment of where ML has added real value to quantitative finance by 2026, where it has been overapplied or mismeasured, and where the next decade's gains are likely to come from. I will be specific about methods, applications, and time horizons.

## Where ML genuinely helps

### Forecasting at specific time horizons

ML-based forecasting has materially improved short-horizon predictions in certain markets. Deep learning models on macro-economic time series (Makridakis M5 competition winners, the LSTM-based household-demand forecasting systems at Amazon, DoorDash, Uber) consistently beat classical ARIMA and Prophet baselines on week-to-month horizons in high-signal domains.

Where this does not carry over, and where the claims get inflated:

**Return prediction at mid-frequency.** Equity returns over one-day to one-month horizons have approximately zero predictable component in efficient markets. A decade of papers claiming ML "beats" classical forecasting at these horizons are typically either cherry-picked (reporting only the best of many runs) or leaking information (using future data at prediction time). After careful out-of-sample evaluation, the edge is small or zero. Once transaction costs and leverage constraints are included, the out-of-sample Sharpe is typically below 0.5. Not zero, but not a production strategy either.

**Macroeconomic time series at quarterly horizons.** The literature on forecasting GDP, inflation, and unemployment with ML has produced many papers showing improvements over classical forecasts. The improvements are usually modest (10-20 percent RMSE reduction). The gains often come from the ML model's use of non-standard data rather than the ML architecture. The forecast accuracy at business-relevant horizons remains poor enough that monetary-policy makers cannot act on the improvements with confidence. The Federal Reserve uses ML-augmented forecasts internally but with substantial human review layered on top.

Where ML helps concretely: short-horizon volatility forecasting using deep neural networks with micro-structure features (Xiong et al. 2015 and subsequent work), short-horizon order-book prediction using recurrent architectures on limit-order-book features, and cross-sectional return prediction where the signal-to-noise ratio is substantial due to known mispricings (small-cap stocks, specific commodity futures).

### Execution algorithms

This is the area where ML has most cleanly displaced classical methods. Optimal-execution problems (how to buy or sell a large order over time while minimizing price impact) have been reformulated as reinforcement-learning problems and demonstrated to outperform classical VWAP/TWAP baselines. The RL approach can adapt to specific market regimes and learn from execution history in ways the classical benchmarks cannot.

Execution is a good fit for ML for specific reasons. The feedback loop is tight (fills in seconds, cost metrics in minutes). The action space is well-defined. The stationarity assumption, while imperfect, is better than in return forecasting. Execution specialists have concrete business incentives to deploy the best methods, so the literature has been tested under real trading conditions.

Where ML helps: optimal execution under market impact constraints, adaptive limit-order-book strategies, market-making in continuous markets, and some forms of arbitrage detection.

Where classical methods still dominate: statistical-arbitrage-style execution where the alpha signal is the driver, and execution under regulatory constraints where the constraint specification is classical.

### Risk modeling

ML has added value to risk modeling, though less dramatically than enthusiasts predicted a decade ago. Credit scoring using gradient-boosted decision trees on features engineered by credit analysts has clearly outperformed classical logistic regression across many banks and fintechs. The improvement is real, measured in better default prediction and lower false-positive rates. XGBoost plus careful feature engineering is the operational state of the art for consumer credit as of 2026.

Fraud detection has similarly benefited from ML. Ensembled gradient-boosted trees plus neural-network-based anomaly detection are routinely deployed at card networks and payment processors. The improvements are large in some settings (a factor of 2-5 reduction in fraud losses at fixed false-positive rate) and sustain over time because the adversarial fraud environment reliably produces new signals for the models to exploit.

Where ML has not dramatically helped: market-risk measurement (VaR, CVaR) at the portfolio level. Classical parametric and historical-simulation methods remain competitive. The regulatory environment rewards simplicity of interpretation over marginal improvements in accuracy. Credit risk at the portfolio level (CDO tranche valuation, for example) has been resistant to ML for similar reasons. The regulator wants auditable model logic. The financial consequences of model failure are severe enough that the industry has been conservative.

### Derivatives pricing

For vanilla options with well-understood underlyings, classical Black-Scholes-and-extensions are still the standard. ML has added value in two specific niches.

**Exotic options where closed-form pricing is unavailable.** Deep neural networks trained to approximate the pricing function (Horvath et al. 2019, Beck et al. 2020) can price path-dependent exotics faster than Monte Carlo simulation while maintaining comparable accuracy. This is a genuine ML contribution. Not because neural networks understand finance, but because they are efficient function approximators for smooth high-dimensional mappings.

**Calibration of stochastic-volatility models.** Fitting parameters of SABR, Heston, and rough-volatility models to observed market data is a high-dimensional optimization problem that neural-network-based calibrators have improved substantially (Horvath et al.). This is deployment-grade ML in one of the most conservative parts of the industry.

Where ML does not help: pricing of vanilla options and standard futures. The classical models are correct and fast. The ML models add complexity without improving accuracy.

## Where ML has been overapplied

I want to be direct about this section because the hype vastly exceeds the evidence. Being specific about overapplication is a service to the industry.

**Deep learning for alpha in mid-frequency equity return prediction.** Despite the enormous interest and the enormous number of papers, I cannot identify a single systematic fund that has robustly built a strategy based on deep learning for mid-frequency equity alpha and sustained its performance over a multi-year period net of fees. The ones that have worked (Renaissance, Two Sigma, DE Shaw) are using ML substantially but not as the primary edge. The edge is the data infrastructure, the execution sophistication, and the systematic discipline. The ML is a refinement, not the driver.

**LLMs for investment research automation.** There is a flood of vendors claiming to automate investment research using LLMs. The actual output is mostly regurgitated summarization with modest value-add over a human analyst. The core issue is that LLMs are trained on text produced before 2023 (or 2024 for the more recent ones), they do not have real-time access to proprietary data, they cannot perform causal reasoning about specific companies, and they hallucinate in ways that are costly for financial research. A human analyst with an LLM as a research assistant is better than a human analyst alone. An LLM as a replacement for an analyst is not yet there, and may not be for another five years.

**Reinforcement learning for portfolio optimization.** RL-based portfolio optimization (training a policy that takes market state and outputs allocation weights) has been a rich research literature and a poor deployment record. Several reasons. The training regime is not stationary (markets change). The sample efficiency is poor. The reward function is ambiguous (Sharpe ratio, drawdown, terminal value). The policies frequently do not generalize out of sample. Classical Markowitz mean-variance with careful covariance estimation and realistic constraints remains competitive and has better interpretability properties.

**Reinforcement learning for trade execution at the strategy level.** Here RL has been useful (see above) but the inflated claims are about automating the full strategy design, which has not been achieved. The pieces (execution, some market-making) are real. The whole is not.

## Where the next decade's gains will come from

My forecast for where meaningful ML-driven gains in quantitative finance will come from over the next decade.

**Regime identification and conditional strategies.** Classical strategies often have specific regimes where they work and regimes where they fail. ML techniques that can dynamically identify the regime and switch strategies accordingly have produced real value, though modestly so. The room to improve is substantial. Transfer-learning across regimes and meta-learning approaches are underexplored.

**Alternative data extraction at scale.** Satellite imagery, shipping data, patent filings, social-media signals, web-scraped consumer data. ML is essential for extracting signal from these data sources at scale. The edge of a fund in 2026 is increasingly its ability to process alternative data efficiently. This is as much an engineering problem as a modeling one.

**Transaction cost modeling.** Modeling the expected transaction cost of a proposed trade (how much the market will move against me given order size, timing, and venue) is a bread-and-butter ML problem that is still imperfectly solved. Gradient-boosted trees on order-book features combined with neural-network-based market-impact models are operationally competitive with classical models and will probably overtake them in the next five years.

**Quantum Monte Carlo for risk estimation.** This is a longer-horizon bet, 10-plus years until production deployment. The quadratic speedup of amplitude estimation (Montanaro 2015) over classical Monte Carlo is real and proven. For exotic derivatives pricing and tail-risk estimation, quantum Monte Carlo on error-corrected hardware could change the cost structure of risk management. I discuss the realistic timeline in a companion essay on quantum computing's business case.

**Multi-agent market simulation.** Agent-based models of markets have been a research backwater for twenty years. The combination of better ML for agent training plus better computational power may make them genuinely useful by 2030. Training many autonomous RL agents to simulate market participants. Evaluating new strategies against their interaction. Testing regulatory changes before rollout. This work is at the frontier and may not deliver. The payoff would be substantial.

## For a firm hiring me to lead quant research

If a firm like Two Sigma's Research Platform or DE Shaw's Research group were hiring me to lead a quant-research team, the thesis I would bring is this.

The ML-in-quant-finance boom is past its easy-gain stage. The remaining gains are harder to find and require a specific combination of skills. Rigorous methodology to distinguish genuine signal from data-mining artifacts. Finance-specific domain knowledge to know which problems are tractable and which are not. Industrial applied-ML fluency to actually ship the tooling. My research leadership would emphasize the first two heavily, the third instrumentally, and would actively pass on research directions where the expected signal-to-noise ratio looks poor regardless of the technical sophistication.

Concretely, my research portfolio at such a firm would allocate capacity as follows.

- 30 percent on execution and transaction cost modeling, where the ML payoff is clearest.
- 25 percent on alternative data extraction and associated infrastructure.
- 20 percent on regime identification and conditional strategy selection.
- 15 percent on derivatives calibration, risk modeling, and specialized applications.
- 10 percent on frontier research (quantum Monte Carlo, multi-agent simulation) as long-term hedge.

The 10 percent long-term hedge is important. Most firms overweight short-horizon research because the compensation structure rewards near-term P&L attribution. A research director's job is to maintain the long-term pipeline that produces the breakthroughs of five years from now. I would be disciplined about preserving this 10 percent even in years when the short-term research is producing strongly.

## Conclusion

Machine learning has genuinely improved quantitative finance in specific areas: execution, credit scoring, exotic-option pricing, fraud detection, volatility forecasting at short horizons. It has been overapplied in mid-frequency alpha generation, automated investment research, and RL-based portfolio optimization. The next decade of gains is likely to come from regime identification, alternative data at scale, transaction-cost modeling, and, on a longer horizon, quantum Monte Carlo for risk.

For a firm hiring quant research leadership in 2026, the question is not whether we want ML. The question is whether we have the research discipline to distinguish the genuine ML gains from the ones that are either noise or artifacts. That discipline is what I would bring to the role, and it is the thing I would screen candidates for more than any specific technical skill.

---

*This essay represents my view of the quant-finance-meets-ML landscape as of 2026. Perspectives may reasonably differ. Comments welcome.*
