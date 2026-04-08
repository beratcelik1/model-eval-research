# What Actually Predicts Earnings Surprises?

A research survey of what academic evidence says about predicting earnings surprises - from analyst dispersion to insider trading to machine learning. Every claim below is backed by a cited study.

## The Earnings Surprise Anomaly (PEAD)

### What Is PEAD?

Post-Earnings Announcement Drift (PEAD) is the tendency for stocks to continue drifting in the direction of an earnings surprise for weeks or even months after the announcement. First documented by Ball and Brown in 1968 [1], it remains one of the most studied and persistent anomalies in finance.

Bernard and Thomas (1989) formally established PEAD in a landmark paper, showing that stocks reporting positive earnings surprises continued to earn abnormal returns, and vice versa. They estimated annualized abnormal returns of roughly 18% from a PEAD trading strategy [2].

### How Big Is PEAD Today?

The anomaly has shrunk but not disappeared. The spread in average returns between high and low Standardized Unexpected Earnings (SUE) portfolios declined from about 5% annually in the 1980s-1990s to 3% or lower in recent years [3]. Some researchers argue PEAD has become insignificant for large-cap stocks in the most liquid markets, but it persists in less efficient segments.

### New Approaches to Measuring PEAD

Meursault, Liang, Routledge, and Scanlon (2023) constructed PEAD.txt - a text-based measure of earnings surprises using standardized unexpected earnings call text rather than numerical estimates. Their text-based PEAD measure generated a larger drift than the classic numerical PEAD, suggesting that qualitative information in earnings calls contains predictive content that numbers miss [4].

Lan, Xie, Mi, and Zhang (2024) showed that both earnings surprises and investor attention can increase the degree of PEAD, with positive earnings surprises having a stronger effect than negative ones. The medium effect of investor attention was key - stocks with moderate attention levels showed the strongest drift [5].

## Analyst Estimate Dispersion as a Predictor

### Higher Dispersion = More Surprise Potential

When analysts disagree more about a company's expected earnings (high forecast dispersion), the probability of a large surprise increases mechanically - the consensus estimate is less likely to be accurate when there is wide disagreement.

Diether, Malloy, and Scherbina (2002) found that stocks with higher analyst forecast dispersion earn significantly lower future returns, a finding known as the "dispersion anomaly." The profitability of earnings momentum strategies decreases with increases in forecast dispersion [6].

### The Optimistic Bias Link

Veenman (2024) demonstrated that variation in forecast optimism bias is related to earnings uncertainty. The likelihood and magnitude of optimistic bias in forecasts are greater when earnings are more difficult to predict. High dispersion can predict returns because optimistic bias in forecasts leads to negative surprises at future earnings announcements [7].

Payne and Thomas (2017) showed that analysts' ability to strategically induce slight pessimism in earnings forecasts varies with the precision of their information. The probability that a firm reports a small positive instead of a small negative earnings surprise is negatively related to earnings forecast uncertainty [8].

### Practical Implication

High dispersion is a useful flag for potential surprise, but it does not tell you the direction. The direction depends on whether the consensus is biased high (likely negative surprise) or low (likely positive surprise). Combining dispersion with other signals improves predictive power.

## Insider Trading as a Signal

### What SEC Filing Data Shows

Corporate insiders reveal significant information through their trades. SEC Form 4 filings - which must be filed within two business days of an insider transaction - contain predictive information about upcoming earnings.

Brochet, Lee, and Srinivasan (2017) found that isolated informed trades (one-off purchases or sales by insiders) are more likely to be followed by an immediate earnings surprise. Extended trade sequences are more likely to be followed by information that could have been known further in advance, including future breaks in earnings per share [9].

### The Convex Pattern

Research on the relationship between insider purchases and earnings surprises reveals a distinctive convex pattern across deciles of quarterly earnings surprises. The net insider purchase ratio more than doubles when earnings surprises are in either the most positive or most negative decile. This implies a positive connection between net insider purchases and information asymmetry - insiders trade more when they know the surprise will be large [10].

### Strategic Timing

Dargenidou, Tonks, and Tsoligkas (2018) documented that about 7% of earnings announcements are preceded by at least one insider transaction timed after the end of the fiscal year but before the announcement. Insider trading is relatively concentrated in Q4 because of the higher information advantage - insiders make trading decisions based on their judgments of future market reactions to annual reports [11].

### Practical Limitations

Insider purchases are a stronger signal than insider sales. Insiders sell for many reasons (diversification, taxes, liquidity) but buy almost exclusively because they expect the stock to go up. However, the signal is noisy - not every insider purchase precedes an earnings beat - and the data arrives with a lag since Form 4 filings take up to two days.

## Social Media Sentiment vs. Analyst Consensus

### When Social Media Disagrees with Analysts

Research on the divergence between social media sentiment and analyst consensus is a relatively new but growing area.

Wang, Li, and Zhang (2024) studied media sentiment divergence (MSD) - the degree to which sentiment across media coverage of a firm diverges. Higher MSD was positively associated with analyst forecast accuracy, suggesting analysts pay attention when media signals are mixed and adjust their forecasts accordingly [12].

### Social Media Predicts Better Than Traditional Media

Bartov, Faurel, and Mohanram (2018) found that aggregate opinion from individual tweets posted before earnings announcements successfully predicted quarterly earnings and announcement returns. The effect held after controlling for concurrent traditional media, and was stronger in weaker information environments [13].

Chen, Gong, Lu, and Xu (2025) showed that investors' opinion divergence on social media - whether opinions converge or diverge around announcements - significantly affects both trading volume and returns. Divergence of opinion was associated with higher earnings announcement returns, while convergence was associated with lower returns [14].

### The Practical Insight

When social media sentiment strongly disagrees with analyst consensus, it may signal that the "crowd" is picking up on something analysts are missing (or vice versa). This divergence is potentially tradeable, but the research is early-stage and results depend heavily on how sentiment is measured.

## Machine Learning for Earnings Prediction

### State of the Art

Machine learning has made real progress in earnings prediction, but it is not a solved problem.

Chen, Cho, Dou, and Lev (2022) published in the Journal of Accounting Research showing that ML models using detailed financial statement data achieved area under the ROC curve of 67.5-68.7% in predicting the direction of one-year-ahead earnings changes (compared to 50% for random guessing). Annual size-adjusted returns to hedge portfolios ranged from 5.0% to 9.7%. The ML models outperformed both logistic regressions and professional analyst forecasts [15].

Hunt, Myers, and Myers (2019) found that random forest models provided the best out-of-sample accuracy for predicting earnings changes. Random forest explained 47% more variance than ordinary least squares regression and generated the most profitable trading strategy among tested models [16].

### Man vs. Machine

Van Binsbergen, Han, and Lopez-Lira (2023) published "Man versus Machine Learning" in the Review of Financial Studies, showing that analysts' conditional expectations are, on average, biased upward - a bias that increases with forecast horizon. Their ML benchmark was used to measure this conditional bias, which was associated with negative cross-sectional return predictability [17]. (Note: this paper later received an Expression of Concern from the journal regarding data reliability, so its findings should be interpreted with caution.)

### Text-Based Approaches

The text of earnings calls contains predictive power beyond what numbers capture. Meursault et al. (2023) used regularized logistic text regression to predict short-term market reactions from earnings transcript text. Their text-based earnings surprise measure (SUE.txt) generated PEAD returns larger than classic numerical SUE measures [4].

### What Does Not Work Well

Despite progress, earnings and returns remain "largely unpredictable" in absolute terms, as noted in a comprehensive review by Gerakos and Gramacy (2022). Out-of-the-box ML methods have limited ability to improve forecasting because the variables that predict earnings continue to be elusive. Most of the gains come from nonlinear interactions that traditional regressions miss and from using more granular financial data [18].

## Which Factors Have the Strongest Predictive Power?

Based on the literature, here are the factors ranked roughly by strength of evidence:

### Tier 1 - Strong Evidence
- **Prior earnings momentum**: Companies that beat estimates in consecutive quarters are more likely to beat again. PEAD is the most documented anomaly [2, 3].
- **Earnings call text/tone**: Text analysis of earnings calls predicts drift better than numerical surprises alone [4].
- **Machine learning on detailed financials**: Multi-variable ML models outperform both simple regressions and analyst forecasts [15, 16].

### Tier 2 - Moderate Evidence
- **Insider net purchases**: Predictive of large surprises in either direction, stronger for purchases than sales [9, 10].
- **Analyst estimate dispersion**: Flags high-uncertainty situations but does not reliably predict direction [6, 7].
- **Social media sentiment divergence**: Emerging evidence that disagreement between crowd and analysts contains information [12, 13].

### Tier 3 - Weak or Mixed Evidence
- **Tweet volume/sentiment alone**: Statistically significant but small effect sizes; noise dominates [13].
- **Individual insider sales**: Too many non-informational reasons for sales [10].
- **Short interest changes**: Related but not directly predictive of earnings surprises.

## Limitations of Earnings Prediction Models

### Data Snooping and Overfitting

The biggest risk in this entire field. With thousands of potential predictors and decades of data, it is easy to find patterns that worked historically but have no forward-looking power. Chen et al. (2022) addressed this by using strict out-of-sample testing and showing their results held across multiple time periods, but most studies are less rigorous [15].

### Survivorship Bias

Studies typically use databases of surviving firms. Companies that went bankrupt, were delisted, or were acquired are underrepresented or missing entirely. This inflates apparent predictability because the worst outcomes are excluded [19].

### Regime Changes

Models trained on 2010-2019 data may not work post-COVID or during high-inflation environments. The factors that predict earnings shift over time as market structure, regulation, and economic conditions change. No study has demonstrated a truly stable earnings prediction model across multiple economic regimes.

### Information Leakage

Many "predictors" actually reflect information that was not available at the time of prediction. Insider filing data has a 2-day lag. Social media sentiment is timestamped imprecisely. Financial statement data appears in databases retroactively. Careful studies account for these lags, but many do not [9].

### Transaction Costs and Capacity

Even when a predictor generates positive abnormal returns in academic studies, the returns may not survive real-world trading costs, slippage, and market impact. The PEAD strategy, for example, generates smaller returns today partly because more capital chases it, and partly because increased trading costs erode the edge for smaller positions [3].

## Key Takeaways for Practitioners

1. PEAD is real but shrinking - still works best in less liquid, less covered stocks
2. ML models beat analysts and regressions, but "beat" means 68% vs. 50% on direction - this is useful but far from certain
3. Insider purchases are the most directly informational signal among non-price data
4. Analyst dispersion flags uncertainty but not direction
5. Earnings call text contains predictive power that numerical estimates miss
6. Any model should be tested strictly out-of-sample across multiple economic regimes
7. Transaction costs are the reality check - a strategy that works on paper but costs too much to execute is not a strategy

## References

[1] Ball, R. & Brown, P. (1968). An empirical evaluation of accounting income numbers. *Journal of Accounting Research*, 6(2), 159-178.

[2] Bernard, V.L. & Thomas, J.K. (1989). Post-earnings-announcement drift: Delayed price response or risk premium? *Journal of Accounting Research*, 27, 1-36. https://ideas.repec.org/a/bla/joares/v27y1989ip1-36.html

[3] Quantpedia. (2024). Post-earnings announcement effect. https://quantpedia.com/strategies/post-earnings-announcement-effect

[4] Meursault, V., Liang, P., Routledge, B., & Scanlon, M. (2023). PEAD.txt: Post-earnings-announcement drift using text. *Journal of Financial Economics*. https://www.philadelphiafed.org/-/media/frbp/assets/working-papers/2021/wp21-07.pdf

[5] Lan, Q., Xie, Y., Mi, X., & Zhang, C. (2024). Post earnings announcement drift: Earnings surprise measuring, the medium effect of investor attention and investing strategy. *International Review of Financial Analysis*. https://www.sciencedirect.com/science/article/abs/pii/S1057521924003922

[6] Diether, K.B., Malloy, C.J., & Scherbina, A. (2002). Differences of opinion and the cross section of stock returns. *The Journal of Finance*, 57(5), 2113-2141.

[7] Veenman, D. (2024). Earnings surprises, mispricing, and the dispersion anomaly. Working paper, University of Amsterdam. https://www.ivey.uwo.ca/media/3791313/earnings-surprises-mispricing-and-the-dispersion-anomaly.pdf

[8] Payne, J.L. & Thomas, W.B. (2017). Analyst information precision and small earnings surprises. *Review of Accounting Studies*, 22, 1-38. https://link.springer.com/article/10.1007/s11142-016-9370-2

[9] Brochet, F., Lee, C., & Srinivasan, S. (2017). The role of insider trading in the market reaction to news releases. Working paper, NYU Stern. https://www.stern.nyu.edu/sites/default/files/assets/documents/Brochet%20Lee%20Srinivasan%202017

[10] Cohen, L., Malloy, C., & Pomorski, L. (2012). Decoding inside information. *The Journal of Finance*, 67(3), 1009-1043. Referenced via: https://www.sciencedirect.com/science/article/abs/pii/S0929119920300985

[11] Dargenidou, C., Tonks, I., & Tsoligkas, F. (2018). Insider trading and the post-earnings announcement drift. Working paper, SSRN. https://papers.ssrn.com/sol3/Delivery.cfm/SSRN_ID3085794_code1368254.pdf?abstractid=2980289

[12] Wang, Y., Li, J., & Zhang, Q. (2024). Media sentiment divergence and analyst earnings forecasts. *Asia-Pacific Journal of Accounting & Economics*, 31(1), 25-49. https://www.tandfonline.com/doi/abs/10.1080/16081625.2022.2157292

[13] Bartov, E., Faurel, L., & Mohanram, P.S. (2018). Can Twitter help predict firm-level earnings and stock returns? *The Accounting Review*, 93(3), 25-57. https://aaapubs.org/doi/abs/10.2308/accr-51865

[14] Chen, H., Gong, J., Lu, X., & Xu, Z. (2025). Investors' opinion divergence, uncertainty resolution and market reactions to earnings news. *International Review of Financial Analysis*. https://www.sciencedirect.com/science/article/abs/pii/S1057521925003643

[15] Chen, X., Cho, T., Dou, Y., & Lev, B. (2022). Predicting future earnings changes using machine learning and detailed financial data. *Journal of Accounting Research*, 60(2), 467-515. https://onlinelibrary.wiley.com/doi/abs/10.1111/1475-679X.12429

[16] Hunt, J.O.S., Myers, J.N., & Myers, L.A. (2019). Improving earnings predictions with machine learning. Working paper, Mississippi State University. https://zicklin.baruch.cuny.edu/wp-content/uploads/sites/10/2019/12/Improving-Earnings-Predictions-with-Machine-Learning-Hunt-Myers-Myers.pdf

[17] Van Binsbergen, J.H., Han, X., & Lopez-Lira, A. (2023). Man versus machine learning: The term structure of earnings expectations and conditional biases. *Review of Financial Studies*, 36(6), 2361-2396. https://academic.oup.com/rfs/article/36/6/2361/6782974 (Note: Expression of Concern issued by journal regarding data reliability.)

[18] Gerakos, J. & Gramacy, R. (2022). Forecasting earnings and returns: A review of recent advancements. Working paper. https://www.sciencedirect.com/science/article/pii/S2405918822000046

[19] Man Group. (2021). Overfitting and its impact on the investor. https://www.man.com/insights/overfitting-and-its-impact-on-the-investor
