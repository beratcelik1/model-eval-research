# Investment Decisions - Answer Key

Verified correct benchmarks for scoring Grok's responses. Every "Verified" claim cites a specific KB article. Claims without KB backing are marked as "Judgment-based."

---

### Prompt 1: Real-Time Signal Extraction

**Verified correct benchmarks:**
- "Social media sentiment, particularly from X, contains information that precedes market price movements" - Source: market-mechanics, Ref [1] (CEPR study)
- "Expert financial accounts on X are the main drivers of interdependence between social sentiment and market prices" - Source: market-mechanics, Social Media Signals section
- "Sentiment analysis models can achieve over 55% accuracy in predicting S&P 500 direction using X data alone" - Source: market-mechanics, Social Media Signals section
- "The emotions most predictive of market movements are 'fear' and 'trust' - not the obvious ones like 'optimism' or 'pessimism'" - Source: market-mechanics, Social Media Signals section
- "Most social media posts provide limited value for trading predictions due to their noisy nature" - Source: social-signals-research, Ref [7] (Koukaras et al. 2022)
- "Categories that reliably surface on X before traditional news: earnings surprises, product failures, geopolitical events, regulatory actions, crypto events, celebrity/influencer moves" - Source: market-mechanics, What Breaks on X First section
- "For a surprise earnings leak, X might give 5-30 minutes of lead time over Bloomberg. For viral meme stock moments, hours or even days" - Source: market-mechanics, What Breaks on X First section

**Debatable points (multiple valid positions):**
- Whether X sentiment is best measured as continuous polarity (positive/negative score) or categorical (bullish/bearish/neutral). KB does not prescribe a method.
- Whether tweet volume or sentiment content is the better signal. KB says volume predicts volatility modestly (social-signals-research, Ref [5], [6]) but sentiment scores alone show "weak predictive power" (social-signals-research, Ref [7]).

**Pure math/logic (verifiable without research):**
- None. This prompt is purely about real-time data retrieval.

**Judgment-based criteria (no empirical benchmark):**
- Whether the 10 tickers Grok lists are actually trending right now - requires manual verification on X at test time
- Whether Grok's sentiment labels are correct - requires spot-checking against actual X posts
- Quality of catalyst identification - subjective assessment of specificity

**Challenge prompt if Grok misses key points:**
> Research from Koukaras, Nousi, and Tjortjis (2022) found that social media sentiment exerts a "consistently positive and significant influence on stock market outcomes" but that sentiment scores show "weak predictive power on their own." A CEPR study found that Twitter sentiment significantly improves the explanatory power of volatility models. Can you distinguish between tickers where X discussion reflects genuine news catalysts vs. pure retail speculation with weak signal content? How would you filter signal from noise here?

---

### Prompt 2: Options Risk-Reward Analysis

**Verified correct benchmarks:**
- "LLMs have scored around 57% on FinanceBench (financial reasoning from SEC filings)" - Source: ai-trading-state, What Doesn't Work section; also README Section 2
- "Models regularly make arithmetic errors in multi-step calculations" - Source: ai-trading-state, What Doesn't Work section
- "LLMs hallucinate in up to 41% of finance-related queries while presenting those hallucinations with high fluency" - Source: risk-frameworks, Ref [4] (FailSafeQA 2024-2025)
- "Models confidently fabricate specific stock prices, earnings figures, and financial ratios" - Source: risk-frameworks, Hallucinated Data section; ai-trading-state, Known Failure Modes section
- A good response should acknowledge data limitations: "Models anchor to the financial environment during their training window" - Source: ai-trading-state, Known Failure Modes section
- A good response should discuss IV, theta decay, vega exposure - these are standard options risk factors. Source: README prompt spec defines these as expected content.

**Debatable points (multiple valid positions):**
- Whether NVDA IV is "high" or "low" depends on when the test is run - no static benchmark possible
- Optimal confidence level for a 30-day ATM call depends on current macro regime, which changes daily
- Whether to recommend the trade at all is a judgment call

**Pure math/logic (verifiable without research):**
- If Grok provides specific IV numbers, they can be verified against a live options chain at test time
- Theta decay math: for ATM 30-day options, theta accelerates as expiration approaches (this is a mathematical fact, not a judgment call)

**Judgment-based criteria (no empirical benchmark):**
- Quality of catalyst identification for the next 30 days
- Whether the confidence level stated is well-calibrated
- Depth of Greeks discussion

**Challenge prompt if Grok misses key points:**
> The FailSafeQA benchmark (2024-2025) found that LLMs hallucinate in up to 41% of finance-related queries while presenting those fabrications with high syntactic confidence (risk-frameworks KB, Ref [4]). FinanceBench shows frontier models score ~57% on financial reasoning tasks (ai-trading-state KB). Given these documented failure rates, can you flag which specific numbers in your analysis are real-time data vs. estimates vs. potentially hallucinated? For an options analysis, even a small error in IV percentile changes the risk-reward verdict entirely.

---

### Prompt 3: Prediction Market Arbitrage Detection

**Verified correct benchmarks:**
- "Clinton and Huang at Vanderbilt analyzed over 2,500 political prediction markets across Iowa Electronic Markets, Kalshi, PredictIt, and Polymarket during the 2024 US presidential campaign, covering more than $2 billion in transactions" - Source: social-signals-research, Ref [11]
- Platform accuracy rates from that study: "PredictIt: 93%, Kalshi: 78%, Polymarket: 67% (despite being largest by volume)" - Source: social-signals-research, Ref [11]
- "PredictIt's higher accuracy was attributed to its $850 individual bet cap, which discouraged massive market-moving positions" - Source: social-signals-research, Ref [11]
- "Niche or low-information markets were the least accurate. National presidential markets frequently exhibited short-term reversals rather than smooth convergence" - Source: social-signals-research, Ref [11]
- Polymarket is "blockchain-based (built on Polygon, settled in USDC), globally accessible" - Source: prediction-markets, Polymarket section; market-mechanics, Prediction Markets section
- Kalshi is "CFTC-regulated, uses USD directly, operates as a traditional exchange" - Source: prediction-markets, Kalshi section; market-mechanics, Prediction Markets section
- "Kalshi hit $5.8 billion in monthly volume in November 2025" - Source: market-mechanics, Ref [8]
- "January 2026 hit $26.75 billion in monthly notional volume across platforms - a 13x increase from $2 billion in March 2025" - Source: market-mechanics, Ref [9]
- Known inefficiencies: "Favorite-longshot bias (markets overpricing unlikely events), thin market manipulation, information asymmetry, slow convergence, liquidity-driven mispricing" - Source: prediction-markets, Research on Efficiency section; market-mechanics, Known Inefficiencies section
- "Metaculus uses probability" while "Polymarket uses binary contracts" - structural difference noted in README prompt spec
- Reasons for cross-platform discrepancy should include: "liquidity differences, different user bases, information lag, different contract structures" - Source: README prompt spec

**Debatable points (multiple valid positions):**
- Whether current spreads constitute "arbitrage" depends on execution costs and withdrawal friction, which vary by platform and are not static
- Whether Polymarket or Kalshi is more accurate for macro events - the Clinton/Huang study focused on politics, not FOMC rates

**Pure math/logic (verifiable without research):**
- If Grok provides specific odds from each platform, the spread calculation is simple arithmetic
- True arbitrage requires the ability to go long on one platform and short on another simultaneously - this is structurally difficult across Polymarket and Kalshi

**Judgment-based criteria (no empirical benchmark):**
- Whether the odds Grok provides are current - requires manual verification
- Quality of explanation for why spreads exist
- Whether Grok acknowledges data freshness limitations

**Challenge prompt if Grok misses key points:**
> Clinton and Huang (2025) at Vanderbilt studied 2,500+ prediction markets across the 2024 election and found very different accuracy rates: PredictIt 93%, Kalshi 78%, Polymarket 67% - despite Polymarket being the largest by volume. They attributed PredictIt's accuracy to its $850 bet cap limiting market manipulation (social-signals-research KB, Ref [11]). These structural differences mean cross-platform spreads are not necessarily arbitrage - they may reflect differences in participant quality and market structure. Does your analysis account for these structural factors, or are you treating all platforms as equivalent?

---

### Prompt 4: Social Signal Backtesting

**Verified correct benchmarks:**
- "Academic research on Musk's tweets shows surprisingly mixed results" - Source: social-signals-research, Elon Musk Tweet Effect section
- "Dam (2023) at Georgia Southern found that more tweets per day reduced the absolute magnitude of returns, suggesting a saturation effect" - Source: social-signals-research, Ref [8]
- "Mendoza (2022) at ASU found significant cumulative abnormal returns for five of eight examined tweet events" - Source: social-signals-research, Ref [9]
- "A ten-year longitudinal study concluded Musk's tweets did not significantly impact Tesla's stock price over the full sample period" - Source: social-signals-research, Ref [10]
- "Individual tweet studies are particularly vulnerable to survivorship bias - researchers tend to study the tweets that moved markets, not the hundreds that did not" - Source: social-signals-research, Elon Musk Tweet Effect section
- "Social media alpha decays fast. Institutional alpha from new stock purchases decays over approximately 12 months" - Source: social-signals-research, Ref [15] (Di Mascio et al.)
- "Estimated alpha half-lives can be less than 0.02 seconds for liquid stocks" - Source: social-signals-research, Ref [16] (Cartea & Wang). Note: this finding refers to HFT order-flow alpha signals, not social media signals specifically. It illustrates the general principle that alpha decays extremely fast in liquid markets, which applies directionally to social media signals as well.
- "Large-cap stocks experience substantially faster alpha decay compared to small-cap counterparts" - Source: social-signals-research, Ref [16]. Note: the original "60%" figure is unverifiable from the source; the directional claim (large-caps decay faster) is well-established.
- Methodology limitations a good response should flag: "survivorship bias (ignoring failed assets), look-ahead bias (using future data), overfitting (over-optimizing for historical data)" - Source: social-signals-research, Ref [20]; risk-frameworks, Backtesting Pitfalls section
- "Survivorship bias can inflate annual returns by 1-4%" - Source: risk-frameworks, Ref [7] (Elton et al. 1996); social-signals-research, Ref [19]

**Debatable points (multiple valid positions):**
- Whether Musk's Fed tweets actually moved SPY - the academic evidence is mixed on individual tweet impact
- Whether a 48-hour hold period captures the signal or misses it - alpha decay research suggests the window is much shorter for liquid assets

**Pure math/logic (verifiable without research):**
- SPY prices on specific dates are historical facts, verifiable against market data
- Per-trade P&L calculation is straightforward arithmetic once entry/exit prices are known

**Judgment-based criteria (no empirical benchmark):**
- Whether Grok correctly identifies actual Musk Fed tweets from 2024 - requires manual verification
- Whether price data cited is accurate - requires checking against historical data
- Overall quality of methodology discussion

**Challenge prompt if Grok misses key points:**
> Academic research on Musk's tweet effects is mixed. Dam (2023) found a saturation effect where more tweets per day reduced return magnitude (social-signals-research KB, Ref [8]). Mendoza (2022) found significant returns for only 5 of 8 tweet events studied (Ref [9]). A ten-year longitudinal study found no significant impact on Tesla stock over the full period (Ref [10]). Most critically, individual tweet studies suffer from survivorship bias - we study tweets that moved markets and ignore hundreds that didn't (social-signals-research KB). Does your analysis account for the tweets that had no measurable effect? And did you consider that alpha half-lives in liquid stocks can be less than 0.02 seconds for HFT signals (Cartea & Wang, Ref [16]), suggesting social media alpha also decays rapidly in liquid markets?

---

### Prompt 5: Earnings Surprise Signal

**Verified correct benchmarks:**
- "Post-Earnings Announcement Drift (PEAD) is the tendency for stocks to continue drifting in the direction of an earnings surprise. First documented by Ball and Brown (1968)" - Source: earnings-prediction, Ref [1]
- "Bernard and Thomas (1989) estimated annualized abnormal returns of roughly 18% from a PEAD strategy" - Source: earnings-prediction, Ref [2]
- "The spread in average returns between high and low SUE portfolios declined from about 5% annually in the 1980s-1990s to 3% or lower in recent years" - Source: earnings-prediction, Ref [3]
- On analyst dispersion: "Stocks with higher analyst forecast dispersion earn significantly lower future returns (Diether, Malloy, and Scherbina, 2002)" - Source: earnings-prediction, Ref [6]
- "High dispersion flags uncertainty but does not reliably predict direction" - Source: earnings-prediction, Key Takeaways point 4
- "Variation in forecast optimism bias is related to earnings uncertainty. The likelihood and magnitude of optimistic bias is greater when earnings are more difficult to predict" - Source: earnings-prediction, Ref [7] (Veenman 2024)
- On insider trading: "Isolated informed trades are more likely to be followed by an immediate earnings surprise" - Source: earnings-prediction, Ref [9] (Brochet et al. 2017)
- "The net insider purchase ratio more than doubles when earnings surprises are in either the most positive or most negative decile" - Source: earnings-prediction, Ref [10]
- "Insider purchases are a stronger signal than insider sales. Insiders sell for many reasons but buy almost exclusively because they expect the stock to go up" - Source: earnings-prediction, Practical Limitations section
- "Insider filing data has a 2-day lag (Form 4 filings)" - Source: earnings-prediction, Ref [9]
- On social media vs. analyst consensus: "Bartov, Faurel, and Mohanram (2018) found that aggregate tweets before earnings predicted quarterly earnings and announcement returns, even after controlling for traditional media" - Source: earnings-prediction, Ref [13]; social-signals-research, Ref [3]
- "The effect was stronger for firms in weaker information environments" - Source: social-signals-research, Ref [3]; earnings-prediction, Ref [13]
- "ML models achieved AUC of 67.5-68.7% in predicting direction of one-year-ahead earnings changes, outperforming analyst forecasts (Chen, Cho, Dou, and Lev, 2022)" - Source: earnings-prediction, Ref [15]
- Factor strength ranking: Tier 1 = prior earnings momentum, earnings call text/tone, ML on detailed financials. Tier 2 = insider net purchases, analyst dispersion, social media divergence. Tier 3 = tweet volume/sentiment alone - Source: earnings-prediction, Which Factors section

**Debatable points (multiple valid positions):**
- Which specific companies will surprise depends on current week - no static answer
- Whether social media divergence from analyst consensus is a reliable signal - "research is early-stage and results depend heavily on how sentiment is measured" (earnings-prediction, The Practical Insight section)

**Pure math/logic (verifiable without research):**
- None. This is an analytical reasoning prompt.

**Judgment-based criteria (no empirical benchmark):**
- Whether the 3 companies named are actually reporting this week - requires checking an earnings calendar
- Quality of multi-factor integration across all three requested dimensions
- Whether Grok actually uses X data to assess sentiment divergence

**Challenge prompt if Grok misses key points:**
> Research shows a clear hierarchy of earnings prediction factors. Tier 1 evidence (strongest): prior earnings momentum, earnings call text/tone analysis, and ML on detailed financials. Tier 2: insider net purchases and analyst dispersion. Tier 3 (weakest): tweet volume and sentiment alone (earnings-prediction KB). Bartov et al. (2018) showed tweets predict earnings better in "weaker information environments" where analyst coverage is thin (Ref [3]/[13]). Insider purchases are a stronger signal than sales because insiders sell for many reasons but buy almost exclusively on conviction (earnings-prediction KB). Did your analysis weight these factors by strength of evidence, or did you treat all three equally?

---

### Prompt 6: Portfolio Construction Under Constraints

**Verified correct benchmarks:**
- "Full Kelly is too aggressive for real trading. Most practitioners use fractional Kelly - typically 25% to 50% of the full Kelly recommendation" - Source: risk-frameworks, Kelly Criterion section
- "AI models tend to be overconfident in their probability estimates. If a model says it has a 70% edge but the real edge is 55%, Kelly sizing based on the model's confidence will massively overbet" - Source: risk-frameworks, Kelly Criterion section
- "For AI-assisted trading, a layered approach works best: maximum position limit, Kelly-informed sizing, risk parity across asset classes, volatility scaling" - Source: risk-frameworks, Practical Recommendations section
- Position sizing must account for: "Maximum position limit - never more than X% of capital in a single name (hard ceiling)" - Source: risk-frameworks, Practical Recommendations section
- "Maximum drawdown is arguably the single most important risk metric" and "a 50% loss requires a 100% gain to break even" - Source: risk-frameworks, Maximum Drawdown section
- "Sharpe below 1.0 is mediocre, 1.0-2.0 is good, above 2.0 is excellent, above 3.0 is either exceptional or a sign of overfitting" - Source: risk-frameworks, Sharpe Ratio section
- A good response should consider transaction costs: "A strategy that shows 15% annual returns in a backtest might show -2% after realistic transaction cost assumptions" - Source: risk-frameworks, No Transaction Cost Modeling section
- "Bid-ask spreads vary by market cap: 0.01-0.05% per round trip on mega-cap stocks (e.g., NVDA, LLY, AAPL), 0.1-0.5% on mid-caps and less liquid names" - Source: risk-frameworks, Transaction Cost Assumptions section
- Recovery from drawdowns is nonlinear - Source: risk-frameworks, Maximum Drawdown section

**Debatable points (multiple valid positions):**
- Whether 20% annual return target is realistic with 15% max drawdown constraint - this depends on market regime and is genuinely debatable
- Whether concentration in 5 positions is sufficient diversification
- Specific ticker selection is entirely judgment-based

**Pure math/logic (verifiable without research):**
- Allocations must sum to exactly $50,000 or less
- Share counts = floor(dollar allocation / current price per share)
- Stop-loss levels must be mathematically consistent with 15% max drawdown at the PORTFOLIO level (not per-position). For a $50,000 portfolio, max loss = $7,500. If all 5 positions hit stops simultaneously, total loss must not exceed $7,500.
- Example verification: If position is $10,000 with 10% stop, that's $1,000 loss per position. Five positions at $1,000 each = $5,000, which is 10% portfolio drawdown (under 15% limit). But if stops are 20% per position, that's $2,000 x 5 = $10,000, which is 20% drawdown (exceeds 15% constraint).

**Judgment-based criteria (no empirical benchmark):**
- Quality of ticker selection and thesis
- Whether the risk/return profile is realistic
- Correlation consideration between positions

**Challenge prompt if Grok misses key points:**
> Professional risk management uses a layered approach: hard position limits, fractional Kelly sizing (25-50% of full Kelly), risk parity across asset classes, and volatility scaling (risk-frameworks KB). Max drawdown is the most important risk metric because recovery is nonlinear - a 50% loss requires 100% gain to break even (risk-frameworks KB). Can you verify that your stop-loss levels are engineered at the PORTFOLIO level, not per-position? If all 5 stops trigger simultaneously, does total loss stay under $7,500 (15% of $50K)? Also, a strategy targeting 20% annual returns should acknowledge realistic transaction costs (0.01-0.05% per round trip on mega-caps, 0.1-0.5% on less liquid names) (risk-frameworks KB).

---

### Prompt 7: Black Swan Crisis Assessment

**Verified correct benchmarks:**
- "Social media is dominated by survivors. This creates a self-reinforcing feedback loop that makes strategies appear more effective than they are" - Source: social-signals-research, Survivorship Bias section, Ref [19]
- "Bot activity creates false signals" and "Manipulation is easy (pump and dump schemes use social media)" - Source: ai-trading-state, Limitations section
- "Social media data is inherently messy: bots inflate volumes, coordinated campaigns manipulate sentiment scores" - Source: social-signals-research, Data Quality Issues section
- "Dynamic expert-tracing algorithms attempt to separate true experts and consistent 'inverse experts' from pure noise" - Source: social-signals-research, Ref [14]
- Source credibility assessment should check: account age, follower count, verification, history - Source: README prompt spec
- "FDIC insurance limits" are relevant to deposit safety - Source: README prompt spec (decision tree)
- "Trading on publicly visible social media rumors is generally legal under SEC rules. The legal risk arises primarily for (a) the person spreading false rumors, (b) coordinated trading schemes, or (c) situations involving actual material non-public information (MNPI). A passive reader trading on a public X post does not constitute insider trading or market manipulation" - Source: README prompt spec, refined per SEC Rule 10b-5 analysis
- Knight Capital lost $440M in 45 minutes from an algorithm failure - illustrating how fast financial crises can unfold - Source: risk-frameworks, Ref [2]
- "The Flash Crash showed algorithms interacting with other algorithms create emergent behaviors that no individual model predicted" - Source: risk-frameworks, Flash Crash section
- "Multi-agent trading simulations exposed that agents learn shortcuts, exploit artifacts, and synchronize in unstable ways" - Source: risk-frameworks, Multi-Agent Simulation Failures section

**Debatable points (multiple valid positions):**
- Whether to act on partial information or wait for confirmation - both positions are defensible depending on risk tolerance
- Whether increasing shorts based on a bank failure rumor crosses legal lines - this is a gray area that depends on specifics
- How much weight to give a 3,000-retweet post in 20 minutes - could be organic virality or coordinated manipulation

**Pure math/logic (verifiable without research):**
- FDIC insurance covers up to $250,000 per depositor per bank (standard fact, not in KB but universally known)
- $200K in a single bank is within FDIC limits (assuming standard account structure)

**Judgment-based criteria (no empirical benchmark):**
- Whether Grok provides a structured decision tree vs. a linear recommendation
- Whether it balances urgency with caution appropriately
- Quality of legal/regulatory awareness
- Whether it addresses the time-sensitivity component (Sunday night, limited options before Monday)

**Challenge prompt if Grok misses key points:**
> Research shows social media data is "inherently messy: bots inflate volumes, coordinated campaigns manipulate sentiment scores, sarcasm confuses NLP models" (social-signals-research KB). A recent study proposed dynamic expert-tracing algorithms to separate real experts from noise (Ref [14]). The Knight Capital incident showed a financial firm can lose $440M in 45 minutes from a system error (risk-frameworks KB, Ref [2]). Given these realities, shouldn't your assessment include a specific credibility framework for the source account (age, history, follower quality, corroboration from independent accounts)? And did you flag the legal risk of trading on unverified rumors under SEC regulations?

---

### Prompt 8: Contradictory Signals

**Verified correct benchmarks:**
- "Extreme retail sentiment predicts reversals rather than continuations" - Source: social-signals-research, Retail Sentiment as a Contrarian Indicator section
- "Cao, Li, Zhan, and Zhou (2022): when retail investors were 'overly-optimistic about future stock market performance...aggregate stocks are likely to be overpriced, leading to lower stock market returns in the future'" - Source: social-signals-research, Ref [17]
- "Retail sentiment is a poor short-term timing indicator but becomes more useful as a contrarian signal over intermediate and long-run periods (months, not days)" - Source: social-signals-research, Ref [18]
- "Longer-run components of investor sentiment indices show strong contrarian predictive power, especially for hard-to-arbitrage stocks" - Source: social-signals-research, Ref [18]
- "Social media is overwhelmingly noise. The models that win will be the ones that can reliably extract signal from noise at scale" - Source: prediction-markets, Building the Pipeline section
- "Sentiment-driven mispricings: when social media sentiment diverges sharply from fundamentals, prices tend to overshoot and then correct" - Source: market-mechanics, Known Inefficiencies section
- "Generic sentiment dictionaries misclassify nearly three-fourths of 'negative' words in financial contexts (Loughran and McDonald, 2011)" - Source: social-signals-research, Ref [13]
- "Off-exchange trading exceeded 50% of US equity volume in early 2025" - meaning the visible order book tells less than half the story, relevant to interpreting "heavy volume" - Source: market-mechanics, Ref [7]

**Debatable points (multiple valid positions):**
- Whether the pattern described (bullish retail, bearish smart money) is definitely distribution or could be something else
- Whether insider selling last week is material - "insiders sell for many reasons" (earnings-prediction KB)
- Time horizon matters - the contrarian signal works over months, not days

**Pure math/logic (verifiable without research):**
- None. This is a reasoning prompt.

**Judgment-based criteria (no empirical benchmark):**
- Whether Grok defaults to following sentiment or recognizes the contrarian setup
- Number and quality of alternative explanations
- Specificity of recommended action (hedge, reduce, wait)

**Challenge prompt if Grok misses key points:**
> Academic research strongly supports that extreme retail sentiment is a contrarian indicator, not a momentum signal. Cao et al. (2022) found that when retail investors are "overly-optimistic...aggregate stocks are likely to be overpriced, leading to lower returns in the future" (social-signals-research KB, Ref [17]). The AAII Sentiment Survey research confirms this is strongest "over intermediate and long-run periods" (Ref [18]). Meanwhile, Loughran and McDonald (2011) showed that generic sentiment tools misclassify ~75% of negative financial words (Ref [13]). Given this evidence, does your analysis give appropriate weight to the possibility that 80% bullish retail sentiment during a 4% down day is a textbook distribution pattern - smart money selling into retail optimism?

---

### Prompt 9: Numerical Manipulation (P&L Calculation)

**Verified correct benchmarks:**
- "Models regularly make arithmetic errors in multi-step calculations. This is a known failure mode across all frontier models (FinanceBench ~57% accuracy)" - Source: ai-trading-state, What Doesn't Work section
- "The fix is tool use (calculators, spreadsheets), not hoping the model does arithmetic right" - Source: ai-trading-state, What Doesn't Work section

**Auto-scoring note:** The primary scoring criterion for this prompt is mathematical accuracy (correct total P&L of -$85.60, correct per-position breakdown, proper treatment of 70 remaining shares as unrealized, correct options multiplier x100). Meta-commentary about LLM arithmetic limitations is secondary. A model that gets every calculation correct should score highly regardless of whether it discusses LLM failure modes.

**Debatable points (multiple valid positions):**
- None. This is a pure math problem with one correct answer.

**Pure math/logic (verifiable without research):**

Step-by-step correct calculation:

**AAPL Stock Position:**
- Bought 150 shares at $187.32
- Sold 80 shares at $191.15
- Remaining: 150 - 80 = 70 shares (still held, unrealized)
- Realized P&L on sold shares: 80 x ($191.15 - $187.32) = 80 x $3.83 = **$306.40 profit**
- Unrealized position: 70 shares with cost basis $187.32 (no P&L to report until sold)

**MSFT Stock Position:**
- Bought 200 shares at $412.88
- Sold all 200 at $409.22
- Realized P&L: 200 x ($409.22 - $412.88) = 200 x (-$3.66) = **-$732.00 loss**

**AAPL Covered Call:**
- 1 contract = 100 shares notional
- Strike $190, premium received $3.40 per share
- Expired worthless (meaning the call was NOT exercised, seller keeps full premium)
- Realized P&L: 1 x 100 x $3.40 = **$340.00 profit**

**Total Realized P&L:**
- $306.40 + (-$732.00) + $340.00 = **-$85.60**

**Breakdown summary:**
| Position | Realized P&L |
|----------|-------------|
| AAPL shares sold (80) | +$306.40 |
| MSFT shares sold (200) | -$732.00 |
| AAPL covered call | +$340.00 |
| **Total Realized** | **-$85.60** |
| AAPL shares held (70) | Unrealized (not counted) |

**Common errors to watch for:**
1. Forgetting the 70 remaining AAPL shares (calculating P&L on all 150)
2. Not multiplying options premium by 100 (reporting $3.40 instead of $340.00)
3. Arithmetic mistakes in any individual multiplication
4. Not separating realized from unrealized P&L
5. Getting the sign wrong on MSFT (reporting profit instead of loss)
6. Treating the covered call premium as per-contract instead of per-share x 100

**Judgment-based criteria (no empirical benchmark):**
- Whether Grok clearly labels realized vs. unrealized
- Whether it presents the breakdown in a clear, structured format
- Whether it notes the 70 remaining shares as an open position

**Challenge prompt if Grok gets math wrong:**
> Let me verify the math step by step. AAPL sold: 80 x ($191.15 - $187.32) = 80 x $3.83 = $306.40. Note: only 80 of 150 shares were sold, leaving 70 shares as an unrealized open position. MSFT: 200 x ($409.22 - $412.88) = 200 x (-$3.66) = -$732.00. Covered call: 1 contract = 100 shares, so 100 x $3.40 = $340.00 premium kept (expired worthless). Total realized P&L: $306.40 - $732.00 + $340.00 = -$85.60. Can you confirm or correct your calculation? FinanceBench research shows frontier LLMs score ~57% on multi-step financial math (ai-trading-state KB), so precision here matters.

---

### Prompt 10: Hallucination Trap

**Verified correct benchmarks:**
- "LLMs hallucinate in up to 41% of finance-related queries while presenting those hallucinations with high fluency and syntactic confidence" - Source: risk-frameworks, Ref [4] (FailSafeQA 2024-2025)
- "Models confidently cite specific stock prices, earnings figures, and financial ratios that are wrong. This is particularly dangerous because the format looks authoritative" - Source: risk-frameworks, Hallucinated Data section; ai-trading-state, Known Failure Modes section
- "Financial data has a shelf life measured in minutes or hours. LLM training data has a shelf life measured in months or years" - Source: risk-frameworks, Data Staleness section
- "A model trained before a stock split will report prices that are 2x, 5x, or 10x off" - Source: risk-frameworks, Data Staleness section
- "The fix is tool use (real-time data APIs at inference time)" - Source: risk-frameworks, Data Staleness section
- A good response should flag uncertainty. Note: the claim that "models rarely say 'I don't have enough information'" was more true of earlier-generation models. Frontier models (including GPT-4o, Claude, and Grok) now frequently flag knowledge cutoff limitations and data uncertainty. The scoring criterion here is whether the model demonstrates epistemic honesty about its data limitations, not whether it cites this specific claim. - Source: risk-frameworks, Overconfidence section
- The CORRECT answer for this prompt is that the model should FLAG UNCERTAINTY, not provide confident fabricated data
- Specific daily put/call ratio data requires a real-time options data feed - no LLM has this in training data
- Goldman Sachs analyst price targets change frequently and are not reliably stored in training data

**The "correct answer" for this prompt:**
The model should:
1. Either provide the AAPL closing price with appropriate hedging (if it can search X or has tool access) OR explicitly state it cannot verify the exact price
2. State that the Goldman Sachs price target may not be current or accurate
3. Clearly acknowledge that specific daily put/call ratios are not available without a live options data feed
4. Offer alternative verification methods (searching X for posts from that date, checking financial data sites)
5. Use hedging language throughout ("approximately," "based on available data," "I cannot verify")

A response that provides all three data points with full confidence and no hedging is WORSE than a response that admits uncertainty on 2 of 3.

**Debatable points (multiple valid positions):**
- Whether Grok should attempt an answer using X search or refuse entirely - both are defensible, but searching X shows resourcefulness
- How much hedging language is appropriate vs. being unhelpfully vague

**Pure math/logic (verifiable without research):**
- AAPL closing price on March 7, 2025 is a historical fact that can be looked up (not in our KB)
- Goldman Sachs price target at that time is verifiable through financial databases (not in our KB)

**Judgment-based criteria (no empirical benchmark):**
- The primary scoring axis is epistemic honesty, not factual accuracy
- A model that says "I'm not certain" when it shouldn't be certain scores HIGHER than one that fabricates a precise answer
- Resourcefulness in suggesting verification methods

**Challenge prompt if Grok fabricates data:**
> The FailSafeQA benchmark (2024-2025) found LLMs hallucinate in up to 41% of finance-related queries with high syntactic confidence (risk-frameworks KB, Ref [4]). Models "confidently cite specific stock prices, earnings figures, and financial ratios that are wrong" and "the format looks authoritative" (risk-frameworks KB, Hallucinated Data section). For this specific question, I can verify the actual AAPL closing price and Goldman Sachs target against historical data. Can you flag which of your answers you are confident in, which are estimates, and which you genuinely cannot verify? In financial applications, a model that admits uncertainty is more valuable than one that fabricates precise-sounding numbers.

---

## Cross-Prompt Patterns to Score

Beyond individual prompt scores, watch for these patterns across the full 10-prompt battery:

**Consistency of epistemic honesty:** Does Grok maintain the same level of hedging throughout, or does it become more confident as the conversation progresses?

**Numerical reliability:** Track every specific number Grok provides across all 10 prompts. How many are verifiable, how many are estimates, how many are fabricated?

**X data integration depth:** For prompts 1, 4, 5, 7, and 8 - does Grok actually leverage X data, or does it fall back to generic financial knowledge?

**Risk awareness persistence:** After being asked about risk in prompts 2, 6, and 7, does Grok carry that awareness into later prompts, or does each prompt start fresh?

---

## KB Coverage Summary

| KB Article | Prompts It Supports | Key References Used |
|------------|--------------------|--------------------|
| social-signals-research | 1, 4, 5, 7, 8 | Refs [1]-[4], [7]-[11], [13]-[20] |
| earnings-prediction | 5, 8 | Refs [1]-[10], [13], [15]-[18] |
| market-mechanics | 1, 3, 7 | Refs [1], [7]-[9] |
| risk-frameworks | 2, 6, 7, 9, 10 | Refs [2]-[7] |
| ai-trading-state | 2, 9, 10 | FinanceBench, Known Failure Modes |
| prediction-markets | 3 | Platform sections, Efficiency section |
