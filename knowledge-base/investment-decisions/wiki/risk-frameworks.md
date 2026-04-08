# Risk Frameworks for AI-Assisted Trading

How to think about risk when AI is generating the signals, and why most AI systems are dangerously bad at it.

---

## Position Sizing Methods

Position sizing answers the question "how much of my capital should I put into this trade?" Get it right and a mediocre strategy can be profitable. Get it wrong and a brilliant strategy can blow up your account.

### Kelly Criterion

Developed by John Kelly Jr. at Bell Labs in 1956, the Kelly criterion calculates the mathematically optimal bet size to maximize long-term growth rate of capital. The formula is:

```
f* = (bp - q) / b
```

Where f* = fraction of capital to bet, b = net odds received, p = probability of winning, q = probability of losing (1-p).

**In practice:** Full Kelly is too aggressive for real trading. It produces enormous volatility and drawdowns that would make any reasonable person (or risk committee) panic. Most practitioners use fractional Kelly - typically 25% to 50% of the full Kelly recommendation.

Recent research (2025) combining Kelly sizing with volatility metrics like VIX found a sweet spot that yields annualized returns in the 20-25% range with controlled tail risk. The key insight: Kelly works best when you have an accurate estimate of your edge. If your edge estimate is wrong (and it usually is), full Kelly amplifies the error.

**The danger for AI:** AI models tend to be overconfident in their probability estimates. If a model says it has a 70% edge but the real edge is 55%, Kelly sizing based on the model's confidence will massively overbet. This is one of the most direct ways AI overconfidence translates to financial loss.

### Fixed Fractional

The simplest approach: risk a fixed percentage of your portfolio on each trade, typically 1-2% for conservative strategies or up to 5% for aggressive ones.

**Pros:** Simple, prevents any single trade from causing catastrophic loss, automatically scales position size with portfolio value (bet less when losing, more when winning).

**Cons:** Doesn't account for edge quality. A 90% probability trade and a 55% probability trade get the same allocation. This leaves money on the table when you have high-confidence setups.

### Risk Parity

Instead of allocating by dollar amount, risk parity allocates so that each position contributes equally to the portfolio's overall risk. If bonds are less volatile than stocks, you hold more bonds.

**Why it matters for AI:** An AI model generating signals across multiple asset classes (stocks, crypto, prediction markets) needs a way to normalize risk across very different volatility profiles. A 5% position in Bitcoin is radically different from a 5% position in Treasury bonds. Risk parity forces the model to think about risk contribution, not just expected return.

### Practical Recommendations

For AI-assisted trading, a layered approach works best:

1. **Maximum position limit** - Never more than X% of capital in a single name (hard ceiling, regardless of model confidence)
2. **Kelly-informed sizing** - Use fractional Kelly (quarter to half) for position sizing within the ceiling
3. **Risk parity across asset classes** - Normalize exposure across different markets
4. **Volatility scaling** - Reduce position sizes when realized volatility is elevated


## Measuring Portfolio Risk

### Value at Risk (VaR)

VaR answers: "What is the maximum I could lose over a given time period with X% confidence?" A 95% daily VaR of $100K means: on 95 out of 100 days, you'll lose less than $100K.

**The problem:** VaR tells you nothing about what happens in the worst 5% of cases. It's a threshold, not a description of tail risk. A portfolio could have $100K VaR but potentially lose $10M in the worst case. The 2008 financial crisis blew up many VaR-based risk models because they assumed normal distributions where reality had fat tails.

### Conditional Value at Risk (CVaR / Expected Shortfall)

CVaR fixes VaR's biggest weakness. It asks: "Given that we're in the worst X% of outcomes, what is the average loss?" This is the average of losses on the very worst days.

CVaR is mathematically subadditive, meaning diversification actually reduces CVaR (unlike VaR, which can paradoxically increase when you combine portfolios). This makes it a better tool for portfolio construction. Most modern quant funds use CVaR instead of or alongside VaR.

### Maximum Drawdown

The largest peak-to-trough decline in portfolio value. If your portfolio went from $1M to $650K before recovering, your max drawdown is 35%.

Max drawdown is arguably the single most important risk metric for actual human investors because:
- It measures the worst pain you'd actually experience
- It determines whether you'd panic and abandon the strategy at the worst possible time
- Institutional allocators use max drawdown as a primary filter for fund selection
- Recovery time from large drawdowns is nonlinear (a 50% loss requires a 100% gain to break even)

### Sharpe Ratio

Risk-adjusted return: (Portfolio return - Risk-free rate) / Standard deviation of returns.

Benchmarks: Below 1.0 is mediocre. 1.0-2.0 is good. Above 2.0 is excellent. Above 3.0 is either exceptional or a sign of overfitting.

**Limitation:** Sharpe penalizes upside volatility and downside volatility equally. If your strategy occasionally has huge up days, Sharpe treats that as "risky." That's mathematically consistent but practically silly.

### Sortino Ratio

Like Sharpe, but only penalizes downside volatility. Uses semi-variance (only returns below target) instead of total variance.

**How to read it:** A manager with Sharpe 1.5 and Sortino 3.0 is managing downside risk effectively (most volatility is to the upside). A manager with Sharpe 1.5 and Sortino 1.8 has symmetric volatility - both up and down moves are happening.

For AI trading strategies that aim for asymmetric returns (small frequent losses, occasional large gains), Sortino is the better measure.


## Why AI Models Are Bad at Risk

### Overconfidence

This is the number one problem. LLMs rarely say "I don't have enough information to form a view." They generate confident-sounding analysis even when the situation is genuinely uncertain. A 2024 study found that LLMs hallucinate in up to 41% of finance-related queries while presenting those hallucinations with high fluency and syntactic confidence.

In trading, false confidence is not just unhelpful - it's actively destructive. A model that says "this trade has a 75% probability of success" when the real probability is 50% will cause the position sizing system to bet too much, and the losses compound.

### No Tail Risk Awareness

Models are trained on data where most days are normal. Extreme events (market crashes, flash crashes, liquidity crises) are rare in training data and don't get enough weight. A model might assign a 0.1% probability to a 20% market drop, when the historical base rate is closer to 1-2% in any given year.

This matters because tail events are where the most money is lost. A strategy that works 99% of the time but blows up catastrophically in the 1% case has negative expected value if the blowup is large enough.

### No Transaction Cost Modeling

Models have no concept of slippage, commissions, bid-ask spreads, or market impact. A model might recommend trading a small-cap stock with a 5-cent spread and $50K of daily volume without realizing that executing a meaningful position would move the price 3% against you before you're even filled.

Transaction costs are the graveyard of backtested alpha. A strategy that shows 15% annual returns in a backtest might show -2% after realistic transaction cost assumptions.

### Data Staleness

Financial data has a shelf life measured in minutes or hours. LLM training data has a shelf life measured in months or years. This mismatch means models will confidently cite stock prices, P/E ratios, and earnings figures that are wrong - sometimes dramatically wrong. A model trained before a stock split will report prices that are 2x, 5x, or 10x off.

The fix is tool use (real-time data APIs at inference time), but most evaluation scenarios test the model without tools, which creates a misleading picture of how dangerous this problem is in practice.

### Model Drift

Unlike traditional algorithms with fixed rules, ML models can drift as they're retrained on new data. Several quant funds have discovered "silent strategy migration" - where models gradually shift their behavior without triggering review processes. One multi-strategy hedge fund found in 2023 that its equity market-neutral strategy had drifted over 18 months from statistical arbitrage into concentrated sector bets, violating its risk mandates and investor disclosures.


## Risks Specific to AI-Generated Trading Signals

### Hallucinated Data

Models confidently fabricate specific financial figures - stock prices, earnings numbers, ratios - that look authoritative but are wrong. This is particularly dangerous because the format looks professional and the numbers are plausible (they're drawn from the distribution of real financial data in training).

Example: "Apple's current P/E ratio is 28.3x" when the actual number is 31.7x. The model generates a number that's in the right ballpark but wrong, and it does so with complete confidence.

### Stale Information Treated as Current

A model that was trained 6 months ago doesn't know about the last two quarters of earnings, any recent acquisitions, management changes, or macro shifts. But it will still generate analysis as if it has current information, just filling in plausible-sounding details that are actually historical.

### Survivorship Bias in Training Data

The internet disproportionately documents successes. Failed companies, failed trades, and failed strategies are underrepresented in training data. This means models have an implicit optimistic bias - they've seen more examples of "I bought Tesla at $20 and now it's $200" than "I bought Theranos at $10 and now it's zero."

### Correlated Failures

If many market participants use similar AI models trained on similar data, they'll generate similar signals, enter similar positions, and try to exit simultaneously when things go wrong. This creates systemic risk that no individual model accounts for. The "quant winter of 2025" highlighted this vulnerability - when many quantitative strategies based on similar signals unwound simultaneously.

### Lack of Regime Awareness

Models pattern-match against historical data. When market regimes shift (low-rate to high-rate, low-volatility to high-volatility, risk-on to risk-off), historical patterns may not apply. Models don't know when to throw out their priors. This is different from being wrong - it's being confidently wrong about the entire framework.


## How Professional Quant Funds Handle AI Risk

### Ensemble Models

No serious fund relies on a single model. They run ensembles of models with different architectures, training data, and assumptions. Signals only become trades when multiple independent models agree. This reduces the impact of any single model's blind spots or biases.

### Human Oversight Layers

Firms like Bridgewater explicitly blend AI models with human oversight to reduce blind spots. The industry consensus emerging in 2025 is that pure AI autonomy in trading is reckless. Hybrid approaches - where AI generates signals and humans validate and execute - consistently outperform pure AI or pure human approaches.

### Circuit Breakers

Hard limits that shut down trading automatically when certain thresholds are breached:
- Maximum daily loss limit (stop trading for the day after losing X%)
- Maximum position concentration (no more than Y% in any single name)
- Maximum drawdown trigger (reduce all positions by Z% if drawdown exceeds threshold)
- Volatility scaling (automatically reduce position sizes when market volatility spikes)

These exist because the model doesn't know when it's broken. A model that's malfunctioning will generate signals with the same confidence as a model that's working correctly.

### Stress Testing

Running the portfolio through historical crisis scenarios (2008, COVID crash, Flash Crash) and hypothetical scenarios (20% overnight gap, complete liquidity withdrawal, correlated selloff across all positions). If the portfolio can't survive these scenarios, it doesn't trade.

### Risk Budget Allocation

Funds allocate a "risk budget" to each strategy, model, and trader. If a model is using more than its allocated risk budget (measured by VaR, position size, or drawdown), it gets scaled back automatically regardless of how confident its signals are. This prevents any single source of alpha from becoming a single point of failure.


## Backtesting Pitfalls

Backtesting is how you evaluate whether a strategy would have worked historically. It's necessary but deeply dangerous because the ways it can mislead you are subtle.

### Look-Ahead Bias

Using information in the backtest that wasn't available at the time the decision would have been made. This is the most common backtesting error. Examples:
- Using the day's closing price to make a decision that would have been made at the open
- Using revised economic data (GDP is revised multiple times) instead of the initially reported figure
- Using the current composition of an index to backtest a strategy that would have used the historical composition

The effect is excessively optimistic results. Every look-ahead bias tilts in your favor because you're using better information than you would have actually had.

### Survivorship Bias

Only testing against companies that still exist today. If you backtest a stock-picking strategy on the current S&P 500, you're missing all the companies that were in the index but went bankrupt or were delisted. Research shows survivorship bias can inflate annual returns by 1-4%, with a compounding effect over time.

The fix is to use point-in-time databases that include all companies that ever existed, not just current survivors.

### Overfitting

The most dangerous backtesting sin. Modern computing allows testing billions of parameter combinations, virtually guaranteeing you'll find patterns that worked historically but fail going forward. If you test 1,000 strategies, 50 of them will look good at the 95% confidence level just by chance.

Warning signs of overfitting:
- Sharpe ratios above 3.0 in backtests (extremely rare in live trading)
- Strategies that require very specific parameter values to work
- Performance that degrades dramatically with small parameter changes
- Dramatically different performance in-sample vs out-of-sample

### Data Snooping

A subtler form of overfitting. Even if you don't directly optimize parameters on historical data, the iterative process of designing a strategy while looking at historical results introduces bias. You unconsciously reject ideas that would have failed and keep ideas that look good historically.

### Transaction Cost Assumptions

Many backtests assume zero transaction costs, or use unrealistically low estimates. In reality:
- Bid-ask spreads can eat 0.1-0.5% per round trip on liquid stocks, much more on illiquid names
- Market impact means large orders move the price against you
- Short selling involves borrowing costs that can be very high for hard-to-borrow stocks
- Commission structures change over time (what costs $0 today cost $7.95/trade in 2015)

A strategy that shows 15% annual returns with zero transaction costs might show 2% or even negative returns with realistic costs.


## Real Examples of AI/Algorithmic Trading Failures

### Knight Capital (August 1, 2012)

A deployment error left old code on one of eight servers. When the new trading system went live, that server began executing an old "Power Peg" algorithm that had been deprecated. The bug caused the system to buy high and sell low across 154 stocks, executing 4 million trades in 45 minutes.

Loss: $440 million. The company had to accept a $400 million rescue financing package and merged with Getco LLC in July 2013 to form KCG Holdings (Getco deal valued at $1.4 billion). KCG was later acquired by Virtu Financial in 2017, also for approximately $1.4 billion.

Key lesson: The existing circuit breakers didn't trigger because they were designed for price swings, not trading volume. The algorithm was buying and selling rapidly without pushing any single stock past the 10% price change threshold. This shows how risk controls designed for one failure mode miss completely different failure modes.

### The Flash Crash (May 6, 2010)

Waddell & Reed executed a large algorithmic sell order for 75,000 E-Mini S&P 500 contracts worth $4.1 billion. Their algorithm sold at 9% of the prior minute's trading volume regardless of price or timing. This triggered a cascade as high-frequency traders passed contracts back and forth (a "hot potato" effect), creating a feedback loop that crashed the Dow Jones 1,000 points in minutes before recovering.

Key lesson: Algorithms interacting with other algorithms create emergent behaviors that no individual model predicted or intended. The system-level risk is invisible at the component level.

### The Quant Winter of 2025

Multiple quantitative strategies based on similar AI-driven signals unwound simultaneously when market conditions shifted. The Treasury Department's December 2024 report acknowledged that AI defects could pose systemic risks to financial stability. The 2025 experience demonstrated that when many funds use similar models, they create correlated risk that amplifies drawdowns.

The industry learned (again) that AI's most convincing financial applications in 2025 were not in generating alpha but in risk monitoring - forecasting market stress, liquidity deterioration, and systemic fragility. These tools don't promise excess returns, but they promise earlier warnings, better hedging, and fewer catastrophic mistakes.

### Multi-Agent Simulation Failures

Multi-agent trading simulations in 2024-2025 exposed uncomfortable truths: agents learn shortcuts, exploit artifacts in the simulation environment, and synchronize in unstable ways. None of this shows up in static backtests, but all of it shows up in production. One industry retrospective noted that "autonomy expands the action space faster than it expands understanding" - each added degree of freedom becomes another way to overfit or create hidden policy risks.


## Implications for Eval Design

Testing an AI model's risk awareness matters more than testing its alpha generation claims. A good financial eval should check whether the model:

1. **Acknowledges uncertainty** - Does it say "I'm not sure" when it genuinely shouldn't be sure?
2. **Considers transaction costs** - Does it mention slippage, spread, and market impact when recommending trades?
3. **Sizes positions sanely** - Does it recommend betting the entire portfolio on a single high-conviction idea?
4. **Identifies tail risks** - Does it consider what happens if it's wrong, not just what happens if it's right?
5. **Knows its data limitations** - Does it flag when its training data might be stale or when it's uncertain about a specific number?
6. **Avoids hallucinating specifics** - When asked for a current stock price, does it acknowledge it doesn't have real-time data or does it make up a number?

Risk-aware behavior is harder to test than financial knowledge, but it's what separates a useful financial AI from a dangerous one.

---



## References

1. Kelly, J.L. Jr. (1956). "A New Interpretation of Information Rate." Bell System Technical Journal, 35(4), pp. 917-926. Developed at Bell Labs.
2. Knight Capital incident (August 1, 2012). $440 million loss in ~45 minutes. 4 million executions in 154 stocks. Accepted $400 million rescue financing; later merged with Getco in December 2012 (deal valued at $1.4 billion). Subsequently, the combined entity KCG Holdings was acquired by Virtu Financial in 2017 for approximately $1.4 billion. https://en.wikipedia.org/wiki/Knight_Capital_Group
3. Flash Crash (May 6, 2010). Waddell & Reed sold 75,000 E-Mini S&P 500 contracts (~$4.1 billion) using an algorithm targeting 9% of prior minute's volume. https://en.wikipedia.org/wiki/2010_flash_crash
4. LLM hallucination in finance. FailSafeQA benchmark (2024-2025) found hallucination rates up to 41% in finance-related queries. https://arxiv.org/abs/2311.15548
5. U.S. Treasury Department (December 2024). "Artificial Intelligence in Financial Services - Report on the Uses, Opportunities, and Risks." https://home.treasury.gov/news/press-releases/jy2760
6. Quant Winter of 2025. Multiple quant funds (including Qube Research & Technologies, Point72's Cubist) experienced drawdowns from correlated AI-driven strategy unwinding. https://www.ainvest.com/news/quant-winter-2025-market-structure-shifts-ai-limitations-expose-hidden-vulnerabilities-2507/
7. Survivorship bias inflating returns by 1-4%. This is a commonly cited range in academic backtesting literature. See Elton, E.J. et al. (1996). "Survivorship Bias and Mutual Fund Performance."
