# Do Social Media Signals Actually Predict Market Moves?

A research survey of academic evidence on social media sentiment, prediction markets, and their relationship to financial returns. Every claim below is backed by a cited study.

## Twitter/X Sentiment and Stock Returns

### The Foundational Studies

The field began with Bollen, Mao, and Zeng (2011), who analyzed 9.8 million tweets to measure collective mood using OpinionFinder and Google-Profile of Mood States (GPOMS). They found that including Twitter mood dimensions - particularly "Calm" - improved prediction of DJIA daily up/down movements to 86.7% accuracy and reduced Mean Average Percentage Error by over 6% [1]. This paper launched an entire subfield of research.

Sprenger, Sandner, Tumasjan, and Welpe (2014) went further, examining firm-specific Twitter sentiment. They found that tweet sentiment was significantly correlated with abnormal stock returns and trading volume. Using a Naive Bayesian classifier trained on 2,500 manually classified tweets, they showed that Twitter contained real information content - not just noise [2].

### Twitter Predicting Earnings

Bartov, Faurel, and Mohanram (2018) published a rigorous study in The Accounting Review showing that aggregate opinion from individual tweets posted just before a firm's earnings announcement successfully predicted both quarterly earnings and announcement returns. The effect was stronger for firms in weaker information environments - meaning Twitter filled a genuine information gap. Results held even after controlling for concurrent traditional media coverage [3].

### The Replication Problem

However, Lachanski and Pav (2017) revisited the Bollen et al. results in "Shy of the Character Limit" and raised significant concerns about the original methodology, including potential data mining and sensitivity to parameter choices [4]. This is a recurring theme - initial results in social sentiment research often shrink or disappear under closer examination.

## Does Tweet Volume Predict Volatility?

Multiple studies say yes, but the effect is modest.

Research has found a statistically significant relationship between tweet volume one to two days before an event and subsequent stock volatility measured by percent change. Tweet volume also predicted volatility measured by trading volume [5].

Mao, Counts, and Bollen (2011) showed that Twitter-based market uncertainty measures had meaningful predictive ability for stock volatility in both in-sample and out-of-sample tests. However, tweet volume's explanatory power was described as "significant but small" - it adds information, but should not be the primary volatility forecast [6].

More recently, Koukaras, Nousi, and Tjortjis (2022) found that social media sentiment exerted a "consistently positive and significant influence on stock market outcomes" when compared with traditional news media and web search activity. But sentiment scores - even when disaggregated into firm-specific and non-firm-specific components - showed weak predictive power on their own [7].

## The Elon Musk Tweet Effect

Academic research on Musk's tweets shows surprisingly mixed results.

Dam (2023) at Georgia Southern University found that when Musk's tweets were Tesla-related, abnormal returns increased - but that more tweets per day reduced the absolute magnitude of returns, suggesting a saturation effect [8].

Mendoza (2022) at ASU, using event study methodology and sentiment analysis, found significant cumulative abnormal returns for five of eight examined tweet events [9].

However, a ten-year longitudinal study of Musk's Tesla tweets concluded that his tweets did not significantly impact Tesla's stock price over the full sample period, suggesting that the market is informationally efficient on longer horizons [10].

The divergence in findings likely depends on time period, tweet content, and whether researchers cherry-pick high-impact events. Individual tweet studies are particularly vulnerable to survivorship bias - researchers tend to study the tweets that moved markets, not the hundreds that did not.

## Prediction Market Accuracy

### How Accurate Are Polymarket, Kalshi, and PredictIt?

Clinton and Huang at Vanderbilt University analyzed over 2,500 political prediction markets traded across Iowa Electronic Markets, Kalshi, PredictIt, and Polymarket during the final five weeks of the 2024 U.S. presidential campaign, covering more than $2 billion in transactions [11].

Their findings challenged conventional wisdom about prediction markets:

- **PredictIt**: 93% accuracy rate
- **Kalshi**: 78% accuracy rate
- **Polymarket**: 67% accuracy rate (despite being the largest by volume)

The study found that niche or low-information markets - such as whether a candidate would say a specific word - were the least accurate. National presidential markets "frequently exhibited short-term reversals rather than smooth convergence toward the eventual outcome" due to speculative trading and overreaction [11].

PredictIt's higher accuracy was attributed to its $850 individual bet cap, which discouraged massive market-moving positions and favored smaller, more informed participants [11].

### Prediction Markets vs. Polls

The evidence is mixed. In the 2024 election, national Polymarket data was superior to polling averages in predicting Trump's win, while major polling averages (FiveThirtyEight, RealClearPolitics, The Economist) showed a near-dead-heat through October into early November [12]. But this is a single data point - it does not prove systematic superiority.

## The Signal-to-Noise Ratio Problem

This is the central challenge of social media trading signals.

Most social media posts provide limited value for trading predictions due to their noisy nature. A user expressing enthusiasm for an asset boosts positive sentiment scores without offering a clear actionable recommendation, leading to weak signal-to-noise ratios [7].

Loughran and McDonald (2011) demonstrated that generic sentiment dictionaries (like the Harvard Dictionary) misclassify nearly three-fourths of "negative" words in financial contexts - the word "liability" is negative in general English but neutral in financial text. Their finance-specific word lists became the standard for textual analysis of 10-Ks and earnings calls [13].

To address noise, recent research has proposed dynamic expert-tracing algorithms that attempt to separate true experts and consistent "inverse experts" (who are reliably wrong) from pure noise [14].

## Alpha Decay - How Quickly Social Signals Lose Value

Social media alpha decays fast - often faster than traditional signals.

Di Mascio, Lines, and Naik documented that institutional alpha from new stock purchases decays over approximately 12 months. Greater competition for information and more highly correlated signals are associated with more aggressive trading and lower alpha [15].

For high-frequency social signals, the decay is dramatically faster. In market-making contexts, estimated alpha half-lives can be less than 0.02 seconds for liquid stocks [16]. Large-cap stocks experience up to 60% faster alpha decay compared to small-cap counterparts, likely because large-caps attract more attention and faster arbitrage [16].

The mechanism is crowding. As more participants replicate the same strategy, the inefficiency being exploited becomes widely recognized, leading to decreased alpha generation. Social media signals are particularly vulnerable because they are publicly observable by definition - unlike proprietary data feeds, anyone can read Twitter [16].

## Retail Sentiment as a Contrarian Indicator

There is growing academic evidence that extreme retail sentiment predicts reversals rather than continuations.

Cao, Li, Zhan, and Zhou (2022) examined retail equity option trading and found that when retail investors were "overly-optimistic about future stock market performance, accompanied with greater gambling activities in the equity option market, aggregate stocks are likely to be overpriced...leading to lower stock market returns in the future." Their call option imbalance measure (ACIB) showed strong contrarian predictive power [17].

Research examining the AAII Investor Sentiment Survey and similar retail sentiment measures confirms that longer-run components of investor sentiment indices show strong contrarian predictive power, especially for hard-to-arbitrage stocks where mispricing persists until fundamentals are revealed [18].

The time horizon matters. Retail sentiment is a poor short-term timing indicator but becomes more useful as a contrarian signal over intermediate and long-run periods (months, not days) [18].

## Limitations and Pitfalls

### Survivorship Bias

Social media is dominated by survivors. Successful traders gain followers and media coverage while those who followed similar strategies but lost money disappear from the conversation. This creates a self-reinforcing feedback loop that makes strategies appear more effective than they are [19].

Hedge fund databases show average annual returns of 6-8%, but academic research tracking both living and dead funds found the true average closer to 3-4% annually - a 1-4% annual inflation from survivorship bias alone [19].

### Cherry-Picking and Overfitting

Backtesting social media strategies is vulnerable to multiple biases: survivorship bias (ignoring failed assets), look-ahead bias (using future data inappropriately), and overfitting (over-optimizing for historical data). Overfitting means a model describes noise rather than signal and has good in-sample performance but little predictive power on new data [20].

The implicit survivorship bias in available data means researchers are automatically looking at markets and time periods that went "rather well" - data from failed exchanges or delisted stocks is often missing entirely [20].

### Data Quality Issues

Social media data is inherently messy: bots inflate volumes, coordinated campaigns manipulate sentiment scores, sarcasm confuses NLP models, and the demographic of active social media users does not represent the investor population. No major academic study has fully solved these problems.

## Key Takeaways for Practitioners

1. Social media sentiment contains real information, but the effect sizes are small and decay quickly
2. Twitter volume predicts volatility modestly - it supplements but does not replace traditional models
3. Extreme retail sentiment is more useful as a contrarian indicator than a momentum signal
4. Prediction markets are better than their critics claim but worse than their advocates claim
5. Any backtested social media strategy should be treated with extreme skepticism until validated out-of-sample
6. The signal-to-noise ratio is the binding constraint - invest in filtering, not in more data

## References

[1] Bollen, J., Mao, H., & Zeng, X. (2011). Twitter mood predicts the stock market. *Journal of Computational Science*, 2(1), 1-8. https://arxiv.org/abs/1010.3003

[2] Sprenger, T.O., Sandner, P.G., Tumasjan, A., & Welpe, I.M. (2014). Tweets and trades: The information content of stock microblogs. *European Financial Management*, 20(5), 926-957.

[3] Bartov, E., Faurel, L., & Mohanram, P.S. (2018). Can Twitter help predict firm-level earnings and stock returns? *The Accounting Review*, 93(3), 25-57. https://aaapubs.org/doi/abs/10.2308/accr-51865

[4] Lachanski, M. & Pav, S. (2017). Shy of the character limit: "Twitter Mood Predicts the Stock Market" revisited. *Econ Journal Watch*, 14(3), 302-345. https://ideas.repec.org/a/ejw/journl/v14y2017i3p302-345.html

[5] Rao, T. & Srivastava, S. (2012). Analyzing stock market movements using Twitter sentiment analysis. *Proceedings of the 2012 International Conference on Advances in Social Networks Analysis and Mining*.

[6] Mao, H., Counts, S., & Bollen, J. (2011). Predicting financial markets: Comparing survey, news, Twitter and search engine data. *arXiv preprint*.

[7] Koukaras, P., Nousi, C., & Tjortjis, C. (2022). Stock market prediction using social media sentiment analysis. *Journal of Risk and Financial Management*, 18(12), 660.

[8] Dam, J.G. (2023). CEO's tweets and firm stock returns: A case study of Elon Musk and Tesla. Honors thesis, Georgia Southern University. https://digitalcommons.georgiasouthern.edu/honors-theses/850/

[9] Mendoza, S. (2022). The effect of Elon Musk's tweets on Tesla stock price. Barrett Honors thesis, Arizona State University. https://repository.asu.edu/items/56372

[10] Pham, N.K. et al. (2021). Elon Musk's Twitter and its correlation with Tesla's stock market. *International Journal of Data Science and Analysis*, 7(1). https://www.sciencepublishinggroup.com/article/10.11648/j.ijdsa.20210701.14

[11] Clinton, J. & Huang, T. (2025). The perils of election prediction markets. Vanderbilt University. https://goodauthority.org/news/the-perils-of-election-prediction-markets/

[12] Token Metrics Research. (2024). Are prediction markets more accurate than polls? https://tokenmetrics.com/blog/prediction-markets/

[13] Loughran, T. & McDonald, B. (2011). When is a liability not a liability? Textual analysis, dictionaries, and 10-Ks. *The Journal of Finance*, 66(1), 35-65. https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2010.01625.x

[14] Liu, Q. et al. (2025). Unleashing expert opinion from social media for stock prediction. *arXiv preprint*. https://arxiv.org/html/2504.10078v1

[15] Di Mascio, R., Lines, A., & Naik, N.Y. (2015). Alpha decay. Working paper, Columbia Business School / London Business School. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2580551

[16] Cartea, A. & Wang, Y. (2020). Market making with alpha signals. Working paper, University of Oxford. https://ora.ox.ac.uk/objects/uuid:c2ba6656-8eab-4b2e-a24a-e9e842d1378f

[17] Cao, J., Li, G., Zhan, X., & Zhou, G. (2022). Betting against the crowd: Option trading and market risk premium. Working paper. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4301015

[18] AAII Investor Sentiment Survey research. https://www.aaii.com/sentimentsurvey

[19] Man Group. (2021). Overfitting and its impact on the investor. https://www.man.com/insights/overfitting-and-its-impact-on-the-investor

[20] LuxAlgo Research. (2024). Survivorship bias in backtesting explained. https://www.luxalgo.com/blog/survivorship-bias-in-backtesting-explained/
