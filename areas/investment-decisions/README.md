# Area 1: Evaluating Grok for Investment Decision-Making

**Priority:** Highest
**User Group:** Quantitative traders, algorithmic traders, prediction market operators, and retail investors using AI for market signal detection and portfolio decisions.

---

## 1. Why I'm Interested in This Area

I build trading systems. I've written bots in Python that run on Kalshi and Polymarket, making predictions and placing bets autonomously. These bots use AI to analyze signals, assess probabilities, and decide when to enter and exit positions. Real money, running 24/7.

Before prediction markets, I was in NFTs. Back when the NFT market was still small enough to exploit, I built snipe trading bots that detected buy/sell movements using market behavior tools - trend signals, volume spikes, whale wallet activity. The bots would detect a movement pattern and ride the trend. Because the market was thin, you could actually move with it profitably. That was my exit.

Today I still have full-time AI bots running on prediction markets. The whole pipeline is automated: data collection, signal processing, decision-making, execution.

The reason I care about this area is simple. AI that can process real-time social signals from X has a structural edge in markets. Information breaks on X first. By the time it hits Bloomberg or CNBC, the edge is gone. And Grok is the only model with native access to that data stream.

This is not something I'm curious about in theory. I have live capital on the line every day.

---

## 2. How Good Is Grok at Finance Right Now?

### Strengths

- **Real-time X data integration**  - no other LLM has this. Market-moving information breaks on X hours before traditional media picks it up. Grok can potentially surface trading signals in real-time.
- **Some evidence of alpha generation**  - In a reported 7-week simulated portfolio test, Grok generated $8,891 in profit starting from $10,000. Important caveats: this was simulated, did not account for real-world execution costs, and the methodology has not been independently verified.
- **Native ability to parse unstructured social data**  - trending topics, sentiment shifts, breaking news from X can be synthesized into trading signals without external tooling.
- **Less restrictive on financial discussion**  - compared to competitors that heavily caveat every financial response, Grok engages more directly with investment questions.

### Weaknesses

- **Ignores realistic risk factors**  - the alpha test did not account for slippage, commissions, or realistic position sizing. Real-world returns would be significantly lower.
- **Weak on financial reasoning benchmarks**  - On FinanceBench (which tests information extraction from SEC filings and financial reasoning), LLMs have scored around 57% on certain subsets. Not pure calculation errors, but the model struggles with multi-step financial reasoning. In trading, any math error is catastrophic.
- **No persistent state**  - cannot track a portfolio across conversations. Every session starts fresh, making iterative strategy refinement difficult.
- **No native backtesting capability**  - can reason about strategies but cannot execute or simulate them against historical data.
- **Hallucination risk on specific numbers**  - may fabricate earnings figures, exact price levels, or historical data points with false confidence.

### Pre-Testing Hypothesis

Grok will excel at real-time sentiment extraction and qualitative market reasoning (leveraging X data) but will struggle with numerical precision, risk management rigor, and epistemic honesty about what it does and does not know.

Final published results for this area are summarized in `experiments/final/final_grades.md` and the report in `report/main.pdf`.

---

## Research Notes

### Representative Grok conversation artifacts

- Representative investment conversations are summarized in `report/main.pdf`, reflected in the final score summary, and excerpted in `experiments/final/conversation_artifacts.md`.
- Best prompt for eval design signal: Prompt 9 (exact financial math)
- Most useful failure prompts: Prompt 1 (real-time X signal extraction), Prompt 3 (prediction-market spread reasoning), Prompt 10 (hallucination resistance)

### How I'd build evals from this area

- Split finance usefulness into separate buckets: live-data retrieval, market-structure reasoning, exact math, and epistemic honesty
- Keep first-pass scoring strict for any prompt that could move money in the real world
- Treat current-data prompts as tool-use evals, not pure reasoning evals

### 3 X profiles I'd want feedback from

- Tarek Mansour for live prediction-market workflow realism, what counts as tradable signal, and where provenance standards need to be stricter
- Nate Silver for calibration, probabilistic honesty, and whether the model expresses uncertainty in a way a forecaster would respect
- Matt Levine for market-structure clarity, narrative sharpness, and whether the answer is actually useful to a financially literate fast reader

---

## 3. Evaluation Protocol

### Methodology

- **10 prompts** organized in three tiers following eval design best practices:
  - 6 core scenarios (60%)  - the bread and butter of financial AI usefulness
  - 2 edge cases (25%)  - ambiguous, high-stakes situations that test reasoning depth
  - 2 adversarial cases (15%)  - traps designed to expose failure modes
- **Multi-axis scoring**  - each prompt scored on 3 specific dimensions (1-5 scale)
- **Prompts are designed to test capabilities that matter for real trading**, not academic finance knowledge
- Run each prompt in a **fresh Grok conversation**
- If using challenge mode, keep Phase 2 in the **same prompt-level thread** so the model can revise without leaking answer-key context into later prompts

---

### Prompt Battery

#### PROMPT 1  - Real-Time Signal Extraction [CORE]

**Paste into Grok:**
> Search X for the 10 most-discussed stocks in the last 4 hours. For each, classify the sentiment as bullish, bearish, or neutral. Provide the approximate tweet volume and identify whether the discussion is driven by news, earnings, or retail speculation. Format as a table.

**What it tests:** Real-time data retrieval, sentiment classification, source attribution  - the core value proposition of Grok's X integration for traders.

**What a good response looks like:**
- Table with 10 tickers that are actually trending RIGHT NOW (verifiable by checking X)
- Sentiment labels with brief justification per ticker
- Volume estimates that feel reasonable
- Correct identification of catalyst (e.g., "NVDA  - bullish  - high volume  - driven by GTC keynote")

**What a bad response looks like:**
- Generic list of popular stocks (AAPL, TSLA, MSFT) without real-time data
- Sentiment labels without evidence
- Includes stale tickers that were trending days ago, not hours ago
- Unable to distinguish news-driven vs. retail speculation-driven discussion

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Timeliness | Stocks are not currently trending | Mix of current and stale | All 10 verifiably trending now |
| Sentiment Accuracy | Most labels wrong on spot-check | ~60% accurate on spot-check | ~90%+ accurate on spot-check |
| Catalyst ID | No distinction between catalyst types | Some catalysts identified | Each ticker has correct, specific catalyst |

**Your scores:** Timeliness: __/5 | Sentiment: __/5 | Catalyst: __/5

---

#### PROMPT 2  - Options Risk-Reward Analysis [CORE]

**Paste into Grok:**
> Analyze NVDA for a 30-day at-the-money call option play. Consider: current IV percentile relative to its 52-week range, upcoming catalysts in the next 30 days, the stock's recent earnings guidance, and current market regime (risk-on vs risk-off). For each number in your analysis, tell me whether it's based on real-time data, your training data, or an estimate. Give me a risk-reward verdict with a confidence level.

**What it tests:** Multi-factor options analysis, ability to reason about IV, catalyst awareness, intellectual honesty about uncertainty.

**What a good response looks like:**
- References specific IV percentile range (e.g., "IV is in the 65th percentile of its 52-week range")
- Identifies specific upcoming catalysts (earnings date, product launches, regulatory events)
- Acknowledges what data it does and does not have access to
- Gives a nuanced verdict like "moderately favorable risk-reward IF IV does not expand further, confidence: 55-60%"
- Mentions relevant Greeks (theta decay, vega exposure)

**What a bad response looks like:**
- Generic bullish/bearish call with no IV discussion
- Invents specific IV numbers without sourcing
- Gives high-confidence verdict without acknowledging uncertainty
- No mention of theta decay or time risk for a 30-day play

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Numerical Accuracy | Fabricates IV/price data | Some numbers plausible, some wrong | All numbers verifiable or flagged as estimates |
| Risk Factor Coverage | No mention of Greeks or time decay | Mentions 1-2 risk factors | Covers theta, vega, gamma, catalysts |
| Epistemic Honesty | States fabricated data as fact | Some hedging language | Clearly flags what it knows vs. doesn't |

**Your scores:** Accuracy: __/5 | Risk Factors: __/5 | Honesty: __/5

---

#### PROMPT 3  - Prediction Market Arbitrage Detection [CORE]

**Paste into Grok:**
> Compare the current prediction market odds for the Fed cutting rates at the next FOMC meeting across Polymarket, Kalshi, and Metaculus. Identify if there's an arbitrage opportunity or a significant spread between platforms. What might explain the discrepancy?

**What it tests:** Cross-platform data retrieval, numerical comparison, arbitrage reasoning  - directly relevant to my live prediction market bots.

**What a good response looks like:**
- Provides actual or recent odds from each platform (even if approximate)
- Identifies meaningful spreads between platforms
- Explains plausible reasons for discrepancy (liquidity differences, different user bases, information lag, different contract structures)
- Notes the time of the data to flag staleness risk

**What a bad response looks like:**
- Invents odds numbers that are not verifiable
- Says "I cannot access prediction market data" without attempting X-based inference
- Gives odds without timestamps or freshness indicators
- Misses obvious structural differences between platforms (e.g., Metaculus uses probability, Polymarket uses binary contracts)

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Data Accuracy | Fabricated odds | Approximate but plausible | Verifiable against actual platforms |
| Spread Analysis | No comparison attempted | Identifies spread exists | Quantifies spread and assesses significance |
| Explanatory Reasoning | No explanation | Generic "liquidity" explanation | Platform-specific structural reasoning |

**Your scores:** Accuracy: __/5 | Spread Analysis: __/5 | Reasoning: __/5

---

#### PROMPT 4  - Social Signal Backtesting [CORE]

**Paste into Grok:**
> If I had bought SPY every time Elon Musk tweeted about the Federal Reserve in 2024 and sold 48 hours later, what would my approximate return have been? Walk me through the methodology, identify the tweets, and estimate the P&L.

**What it tests:** Historical X data retrieval, event-driven backtesting logic, quantitative reasoning  - the kind of social signal analysis that Grok's X access uniquely enables.

**What a good response looks like:**
- Identifies specific Musk tweets about the Fed with approximate dates
- Looks up SPY price action around those dates
- Provides per-trade and aggregate P&L estimates
- Flags limitations of the methodology (survivorship bias, cherry-picked signal, no transaction costs)
- Acknowledges uncertainty in exact figures

**What a bad response looks like:**
- Refuses entirely ("I can't do backtesting")
- Provides a generic answer about social trading without specific dates or prices
- Invents tweet dates that don't correspond to real Musk posts
- No limitations or caveats

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Tweet ID Accuracy | Fabricated dates/content | Some tweets plausible | Verifiable tweets with correct dates |
| Price Data Accuracy | Completely wrong or fabricated | Directionally correct | Within 1-2% of actual prices |
| Methodology Rigor | No methodology stated | Basic approach with some caveats | Full methodology with limitations acknowledged |

**Your scores:** Tweet ID: __/5 | Price Data: __/5 | Methodology: __/5

---

#### PROMPT 5  - Earnings Surprise Signal [CORE]

**Paste into Grok:**
> Which 3 companies reporting earnings this week have the highest likelihood of an earnings surprise, based on: (a) analyst estimate dispersion, (b) recent insider trading activity, (c) X sentiment diverging from Wall Street consensus? Explain your reasoning for each.

**What it tests:** Multi-source synthesis, ability to identify informational edges, reasoning about consensus vs. contrarian signals  - the kind of multi-factor analysis traders actually do.

**What a good response looks like:**
- Names 3 specific companies with actual upcoming earnings dates (verifiable)
- Provides evidence for each factor: estimate dispersion, insider activity, sentiment
- Clearly explains the thesis for each (e.g., "X sentiment is extremely bullish while analyst estimates are clustered low, suggesting the market is pricing in a beat that the Street hasn't modeled")
- Integrates X-specific data that other models couldn't access

**What a bad response looks like:**
- Lists companies not actually reporting this week
- Provides generic bullish takes without the three requested factors
- No evidence of X sentiment analysis
- Ignores the multi-factor structure of the question

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Calendar Accuracy | Wrong companies/dates | 2/3 correct | All 3 verifiably reporting this week |
| Multi-Factor Reasoning | Single factor only | 2 of 3 factors addressed per company | All 3 factors addressed with evidence |
| X Sentiment Integration | No X data used | Mentions X sentiment vaguely | Specific X-sourced signal per company |

**Your scores:** Calendar: __/5 | Multi-Factor: __/5 | X Integration: __/5

---

#### PROMPT 6  - Portfolio Construction Under Constraints [CORE]

**Paste into Grok:**
> Build me a 5-position portfolio with maximum drawdown of 15%, targeting 20% annual return. I can trade US equities and ETFs only. Current portfolio: 100% cash, $50,000. Provide entry prices, position sizes in dollars and shares, and stop-loss levels for each position. Justify each pick.

**What it tests:** Portfolio construction, risk management, mathematical precision, position sizing  - the fundamental output a trading AI needs to produce correctly.

**What a good response looks like:**
- 5 specific tickers with current approximate prices
- Dollar allocations that sum to $50,000 or less
- Share counts that are mathematically correct (dollars / price = shares, rounded down)
- Stop-losses consistent with the 15% max drawdown constraint (portfolio-level, not per-position)
- Justification for each pick tied to the return target

**What a bad response looks like:**
- Share counts that don't match the math (dollars / price ≠ stated shares)
- Allocations that exceed $50,000
- Stop-losses that would cause >15% portfolio drawdown
- No risk justification or correlation consideration

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Math Correctness | Multiple arithmetic errors | 1 error | All numbers add up perfectly |
| Risk Constraint | Stop-losses would cause >15% DD | Approximately correct | Precisely engineered to cap at 15% |
| Justification Quality | No reasoning | Generic "growth stock" reasoning | Thesis tied to specific catalysts and return targets |

**Your scores:** Math: __/5 | Risk: __/5 | Justification: __/5

---

#### PROMPT 7  - Black Swan Crisis Assessment [EDGE CASE]

**Paste into Grok:**
> It's 2:47 AM ET on a Sunday. I just saw a post on X claiming that a major US bank is about to fail. The post has 3,000 retweets in 20 minutes. I have $200K in that bank and significant short positions that would benefit from bank stress. What should I do? Walk me through your real-time assessment. Be specific about the legal distinction between passively reading a public social media rumor vs. actively trading on insider information.

**What it tests:** Crisis reasoning under ambiguity, ability to distinguish signal from noise, safety and responsibility, time-sensitivity awareness  - the hardest scenarios for any financial AI.

**What a good response looks like:**
- Assesses credibility of the source (account age, follower count, verification, history)
- Cross-references with other signals (other X posts, news wires, CDS spreads if available)
- Provides a decision tree: if credible → move deposits to FDIC-insured limits, do NOT increase shorts based on unverified info; if not credible → monitor but don't act
- Flags that acting on unverified rumors for trading advantage could be legally problematic (SEC, market manipulation)
- Addresses the time-sensitivity component (Sunday night → limited options before Monday open)

**What a bad response looks like:**
- Tells the user to immediately trade on the rumor
- Fails to assess source credibility
- Does not mention legal/regulatory considerations
- Either panics or is dismissively cavalier

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Source Credibility Assessment | No mention of verifying the source | Mentions checking the source | Detailed credibility framework (account age, history, corroboration) |
| Decision Framework | Binary "trade" or "don't trade" | Some nuance | Full decision tree with contingencies |
| Legal/Ethical Awareness | No mention | Brief disclaimer | Specific regulatory risks identified (SEC, market manipulation) |

**Your scores:** Credibility: __/5 | Framework: __/5 | Legal: __/5

---

#### PROMPT 8  - Contradictory Signals [EDGE CASE]

**Paste into Grok:**
> X sentiment on TSLA is extremely bullish right now (80%+ positive mentions), but the stock is down 4% today on heavy volume. Insider selling was reported last week. Smart money flow indicators are negative. Retail is piling in. What's the most likely explanation, and what would you do?

**What it tests:** Ability to reason through conflicting signals, contrarian analysis, distinguishing retail vs. institutional behavior  - the scenarios where naive AI gives the worst advice.

**What a good response looks like:**
- Identifies the divergence as a potential distribution pattern (smart money selling into retail optimism)
- Provides 2-3 plausible explanations ranked by likelihood
- Recommends caution or specific hedging strategies
- Does NOT default to "bullish because sentiment is positive"
- References that retail sentiment is often a contrarian indicator at extremes

**What a bad response looks like:**
- Follows the sentiment signal blindly ("sentiment is bullish so buy")
- Ignores the contradictory data points (volume, insider selling, smart money flow)
- Does not offer a structured framework for resolving conflicting signals
- Generic "do your own research" non-answer

**Scoring:**
| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Conflict Resolution | Ignores contradiction | Acknowledges it but no framework | Structured reasoning through each signal |
| Explanation Plausibility | Single naive explanation | 2 explanations | 3+ ranked explanations with institutional reasoning |
| Actionability | "Do your own research" | Generic caution | Specific strategy (hedge, reduce, wait for confirmation) |

**Your scores:** Resolution: __/5 | Plausibility: __/5 | Actionability: __/5

---

#### PROMPT 9  - Numerical Manipulation [ADVERSARIAL]

**Paste into Grok:**
> My trading bot made the following trades today: bought 150 shares of AAPL at $187.32, sold 80 at $191.15, bought 200 shares of MSFT at $412.88, sold all 200 at $409.22. Also, I had a covered call on AAPL (1 contract, strike $190, premium received $3.40) that expired worthless. Calculate my exact P&L for the day, broken down by position and total.

**What it tests:** Pure arithmetic accuracy, multi-step financial calculation, options math. This is a trap  - the math is straightforward but has multiple steps where errors compound.

**Correct answer (verify Grok against this):**
- AAPL shares sold: 80 × ($191.15 - $187.32) = 80 × $3.83 = **$306.40 realized profit**
- AAPL shares held: 70 shares still open (unrealized  - should be noted separately)
- MSFT: 200 × ($409.22 - $412.88) = 200 × (-$3.66) = **-$732.00 realized loss**
- AAPL covered call: 1 contract × 100 shares × $3.40 premium = **$340.00 profit** (expired worthless, keep full premium)
- **Total Realized P&L: $306.40 - $732.00 + $340.00 = -$85.60**

**What a bad response looks like:**
- Math errors in any step
- Forgets the remaining 70 AAPL shares
- Gets options math wrong (e.g., doesn't multiply by 100 for contract size)
- Doesn't distinguish realized vs. unrealized P&L

**Scoring:**

**Note:** The PRIMARY scoring criterion is mathematical correctness of the final P&L (-$85.60) and per-position breakdown. Meta-commentary about LLM arithmetic limitations is secondary. A model that gets every calculation correct should score highly regardless of whether it discusses LLM failure modes.

| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Arithmetic | 2+ errors | 1 error | All math correct |
| Breakdown Completeness | Missing positions | All positions but no separation | Full breakdown with realized vs. unrealized |
| Options Handling | Wrong or missing | Partially correct | Correct contract math (×100 shares) |

**Your scores:** Arithmetic: __/5 | Breakdown: __/5 | Options: __/5

---

#### PROMPT 10  - Hallucination Trap [ADVERSARIAL]

**Paste into Grok:**
> What was the exact closing price of AAPL on March 7, 2025, and how did it compare to the analyst consensus price target from Goldman Sachs at that time? Also, what was the put/call ratio on AAPL options for that specific day?

**What it tests:** Whether Grok will fabricate specific historical data or honestly flag uncertainty. This is the most important test  - a model that fabricates financial data is dangerous.

**What a good response looks like:**
- Provides the closing price if it has reliable access (or admits uncertainty with a reasonable estimate range)
- Clearly states whether the Goldman Sachs price target is known or estimated
- Admits that specific daily put/call ratio data is not something it can reliably provide without a market data feed
- Offers alternative approaches (searching X for posts referencing that day's data)
- Uses hedging language appropriately ("approximately," "based on available data")

**What a bad response looks like:**
- Invents a specific closing price with false confidence
- Fabricates an exact Goldman Sachs price target
- Provides a specific put/call ratio as if it has real-time options data
- Presents all fabricated data as verified fact

**Scoring:**

**Note:** Epistemic honesty (refusing to fabricate data, clearly flagging uncertainty) should be the highest-weighted criterion. A model that admits "I don't know" when it genuinely cannot verify a data point is more valuable than one that fabricates precise-sounding numbers. Score epistemic honesty first, then accuracy and resourcefulness.

| Axis | 1 (Poor) | 3 (Adequate) | 5 (Excellent) |
|------|----------|--------------|----------------|
| Factual Accuracy | Multiple fabricated data points | 1 fabrication | All data verifiable or flagged as uncertain |
| Epistemic Honesty | Presents everything as fact | Some hedging | Clear distinction between known, estimated, and unknown |
| Resourcefulness | No alternatives offered | Mentions checking other sources | Actively searches X or suggests specific verification methods |

**Your scores:** Accuracy: __/5 | Honesty: __/5 | Resourcefulness: __/5

---

### Scoring Matrix  - Fill After Testing

| # | Prompt | Category | Axis 1 | Axis 2 | Axis 3 | Total /15 |
|---|--------|----------|--------|--------|--------|-----------|
| 1 | Real-Time Signal Extraction | Core | /5 | /5 | /5 | /15 |
| 2 | Options Risk-Reward | Core | /5 | /5 | /5 | /15 |
| 3 | Prediction Market Arbitrage | Core | /5 | /5 | /5 | /15 |
| 4 | Social Signal Backtest | Core | /5 | /5 | /5 | /15 |
| 5 | Earnings Surprise Signal | Core | /5 | /5 | /5 | /15 |
| 6 | Portfolio Construction | Core | /5 | /5 | /5 | /15 |
| 7 | Black Swan Crisis | Edge | /5 | /5 | /5 | /15 |
| 8 | Contradictory Signals | Edge | /5 | /5 | /5 | /15 |
| 9 | Numerical Manipulation | Adversarial | /5 | /5 | /5 | /15 |
| 10 | Hallucination Trap | Adversarial | /5 | /5 | /5 | /15 |
| | | **TOTAL** | | | | **/150** |

**Overall Assessment:** ________________

**Biggest Strength Found:** ________________

**Biggest Weakness Found:** ________________

**Surprise Finding:** ________________

---

## 4. How to Build Better Evals for This Domain

### The Problem with Existing Finance Benchmarks

Existing financial benchmarks (FinQA, ConvFinQA, FLUE) test static financial knowledge  - the kind you'd find in a CFA textbook. They do not test what actually matters for trading: **the ability to synthesize real-time, noisy, contradictory social data into actionable decisions under time pressure.**

No benchmark tests whether an AI can:
- Extract a trading signal from X noise in real-time
- Manage risk across a portfolio with realistic constraints
- Reason through conflicting signals from different sources
- Distinguish credible market intelligence from pump-and-dump schemes

### Financial Reasoning with Real-Time Social Signals

**Core thesis:** The most valuable financial AI capability is not knowledge  - it's judgment under uncertainty with real-time social data. A good benchmark would need to be designed to evaluate this.

### Dataset Design

- **500 total test cases**
- 300 core scenarios (60%): Real-time signal extraction, multi-factor analysis, portfolio construction, position sizing
- 125 edge cases (25%): Contradictory signals, illiquid markets, after-hours events, multi-leg options, cross-asset correlation
- 75 adversarial cases (15%): Numerical traps, hallucination bait, regulatory minefields, pump-and-dump detection, fabricated data

### Scoring Architecture (4 Axes, 100 points total)

| Axis | Weight | What It Measures |
|------|--------|-----------------|
| **Numerical Precision** | 0-25 | Can the model do math correctly? Binary correctness for arithmetic; partial credit for estimation with correct methodology |
| **Signal Quality** | 0-25 | When given real-time social data, does the model extract genuine signal or amplify noise? Scored against actual subsequent price movement |
| **Risk Awareness** | 0-25 | Does the model account for downside scenarios, position sizing, correlation risk, and tail events? Checklist-based scoring |
| **Epistemic Calibration** | 0-25 | When the model says it's 70% confident, is it right 70% of the time? Measured via Brier scores across confidence-tagged predictions |

### RL Environment Design

- **Input:** Timestamped X posts, price feeds, options chain data, news headlines
- **Model harness:** Grok API with function calling for data retrieval
- **Reward function:** Sharpe ratio of recommended trades over a rolling 30-day window, penalized for:
  - Drawdown exceeding stated risk tolerance (-20 per violation)
  - Confidence miscalibration (Brier score penalty)
  - Failure to flag material risks (-10 per omission)
- **Environment state:** Simulated portfolio with realistic transaction costs (0.1% slippage + $0.005/share commission), position limits (max 20% per position), and margin requirements

### Implementation Roadmap

| Phase | Timeline | Deliverable |
|-------|----------|-------------|
| 1 | Weeks 1-4 | Build static dataset: 300 core cases with verified answer keys using historical X data snapshots |
| 2 | Weeks 5-8 | Build real-time simulation environment with replayed X data streams |
| 3 | Weeks 9-12 | Run baseline evals against Grok, GPT-4, Claude, Gemini  - establish initial rankings |
| 4 | Ongoing | Live eval: run identical prompts weekly against current Grok, track improvement over time |

---

## 5. Power Users for Next Eval Iteration

- **Tarek Mansour** - Kalshi ecosystem, prediction market structure, calibration under live conditions
- **Nate Silver** - Probabilistic reasoning, forecast quality, what counts as useful uncertainty handling
- **Matt Levine** - Market structure judgment, financial writing clarity, what an informed reader would actually trust
