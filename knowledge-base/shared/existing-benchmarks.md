# Existing Benchmarks

What benchmarks exist in each domain, what they actually measure, and why there's a critical gap.

---

## Finance Benchmarks

### FinanceBench
- **What it tests**: Financial question answering from SEC filings and financial documents
- **Format**: Question-answer pairs with source documents
- **Typical scores**: ~57% accuracy across frontier models
- **The problem**: Tests whether a model can extract information from a document. Does not test whether the model can make a good investment decision. A model that scores 100% on FinanceBench could still lose money on every trade recommendation.

### FinQA
- **What it tests**: Numerical reasoning over financial data (earnings reports, balance sheets)
- **Format**: Questions requiring multi-step math on tables
- **Typical scores**: 60-75% for frontier models
- **The problem**: The math is pre-defined. Real financial analysis requires choosing which calculations matter, not just executing them correctly. Also, all data is historical and static.

### ConvFinQA
- **What it tests**: Conversational financial QA (multi-turn)
- **Format**: Follow-up questions building on previous answers
- **Typical scores**: Similar range to FinQA
- **The problem**: Same as FinQA but with dialogue. Still tests extraction and computation, not judgment.

### FLUE (Financial Language Understanding Evaluation)
- **What it tests**: Sentiment analysis, named entity recognition, question answering, and other NLP tasks on financial text
- **Format**: Multiple subtasks
- **The problem**: Tests language understanding, not financial understanding. A model that perfectly classifies financial sentiment still can't tell you whether to buy or sell.

### What's Missing in Finance
- No benchmark tests forward-looking analysis ("should I buy X given these conditions?")
- No benchmark uses real-time data
- No benchmark measures calibration ("how confident should you be?")
- No benchmark tracks whether AI recommendations actually make money
- No benchmark tests risk-adjusted reasoning


## Marketing Benchmarks

### EQ-Bench3
- **What it tests**: Emotional intelligence, empathy, social perception
- **Format**: Scenarios requiring emotional understanding and appropriate responses
- **Notable**: Grok ranked #1 as of early 2026
- **The problem**: Emotional intelligence is a proxy for persuasion ability, but it's not the same thing. A model can be emotionally intelligent and still write ads that don't convert.

### LMArena (Marketing-Adjacent)
- **What it tests**: General text quality as judged by humans
- **Format**: Head-to-head comparisons, users pick the better response
- **The problem**: Users pick what sounds better, not what converts better. The most eloquent email subject line is not necessarily the one with the highest open rate. There's no conversion data in the loop.

### BIG-Bench (Persuasion Tasks)
- **What it tests**: A few subtasks around persuasive writing and social reasoning
- **Format**: Multiple choice and free-form
- **The problem**: Tiny sample sizes for persuasion-specific tasks. Not a dedicated benchmark.

### What's Missing in Marketing
- No benchmark tests actual conversion (click-through, sign-up, purchase)
- No benchmark tests personalization effectiveness
- No benchmark measures whether AI copy outperforms human copy
- No benchmark tests A/B testing design capability
- No benchmark uses real audience data
- No benchmark tests trend awareness or cultural relevance


## Health Benchmarks

### MedQA
- **What it tests**: Medical knowledge at the level of USMLE (US Medical Licensing Exam)
- **Format**: Multiple choice questions from medical exams
- **Typical scores**: 85-92% for frontier models (GPT-4 leads)
- **The problem**: Tests clinical knowledge, not health optimization. Passing a medical exam doesn't mean you can design a supplement protocol. These questions have one right answer. Real health decisions rarely do.

### MedMCQA
- **What it tests**: Similar to MedQA but sourced from Indian medical entrance exams (AIIMS, NEET)
- **Format**: Multiple choice
- **The problem**: Same issues as MedQA. Static knowledge, not practical advice.

### PubMedQA
- **What it tests**: Whether a model can correctly answer questions based on PubMed abstracts
- **Format**: Yes/no/maybe questions with supporting abstract
- **Typical scores**: 75-82% for frontier models
- **The problem**: Tests reading comprehension of medical literature, not synthesis across multiple studies. Real health advice requires weighing conflicting evidence, understanding effect sizes, and accounting for individual variation.

### MultiMedQA (Google)
- **What it tests**: Combination of MedQA, MedMCQA, PubMedQA, and others
- **Format**: Mixed
- **The problem**: Aggregation of existing benchmarks doesn't fix their fundamental limitations.

### What's Missing in Health
- No benchmark tests supplement interaction analysis
- No benchmark tests personalized protocol design
- No benchmark tests biomarker interpretation with reference ranges
- No benchmark tests handling of scientific controversy (e.g., NMN vs NR debate)
- No benchmark tests safety reasoning for edge cases (contraindications, dosage limits)
- No benchmark distinguishes between "normal range" and "optimal range" reasoning


## The Gap: Knowledge vs Usefulness

This is the core insight that drives the entire eval project.

### What Benchmarks Test
- Can the model retrieve factual information?
- Can the model do math on provided data?
- Can the model pass an exam designed for humans?
- Can the model classify text correctly?

### What Benchmarks Don't Test
- Can the model help someone make a better decision?
- Can the model handle uncertainty and conflicting evidence?
- Can the model adapt its advice to individual context?
- Can the model use real-time information effectively?
- Can the model explain its reasoning in a way that builds appropriate trust?
- Can the model refuse gracefully when it doesn't know enough?

### The Usefulness Gap, Quantified

Consider finance. A model that scores 90% on FinanceBench:
- Knows what P/E ratio means (knowledge)
- Can calculate P/E from given numbers (computation)
- Cannot tell you whether a specific P/E is high or low for a given sector right now (judgment)
- Cannot weigh multiple conflicting signals to form a view (synthesis)
- Cannot tell you how much to risk on that view (calibration)

The gap between "knows financial concepts" and "gives useful financial advice" is enormous. Existing benchmarks sit entirely on the knowledge side.

The same pattern holds in marketing (knows persuasion theory vs. writes copy that converts) and health (passes medical exams vs. designs safe supplement protocols).

### Why This Gap Exists

1. **Knowledge is easy to evaluate** - There's a right answer. You can grade it automatically.
2. **Usefulness is hard to evaluate** - It requires real-world outcomes, which take time and money to measure.
3. **Academic incentives** - Papers need clean metrics. "Our model scored 92% on MedQA" is publishable. "Our model gave advice that helped 60% of users" requires a clinical trial.
4. **Legal risk** - Nobody wants to create a benchmark that implies AI should give financial or medical advice.

### What We're Building

Evals that sit in the usefulness zone:
- Test judgment, not just knowledge
- Include real-world context and constraints
- Measure calibration (does the model know what it doesn't know?)
- Use multi-axis scoring (accuracy alone is insufficient)
- Can evolve into training signals (RLVR)

This is harder to build and harder to score. But it's the only way to measure what actually matters.

---

## References

1. FinanceBench. https://financebench.com/ - ~57% accuracy for frontier models is directionally correct per published evaluations.
2. FinQA: Zhiyu Chen et al. "FinQA: A Dataset of Numerical Reasoning over Financial Data." EMNLP 2021.
3. FLUE: Shah, D. et al. "FLUE: Financial Language Understanding Evaluation." arXiv:2211.00083.
4. EQ-Bench3. https://eqbench.com/ - Grok ranked #1 as of early 2026 confirmed via leaderboard.
5. MedQA: Jin, D. et al. "What Disease does this Patient Have? A Large-scale Open Domain Question Answering Dataset from Medical Exams." Applied Sciences, 2021. 85-92% for frontier models is consistent with published GPT-4 results (86.7% on MedQA in the original GPT-4 technical report).
6. PubMedQA: Jin, Q. et al. "PubMedQA: A Dataset for Biomedical Research Question Answering." EMNLP 2019. 75-82% for frontier models is a reasonable range per published evaluations.
7. MultiMedQA: Singhal, K. et al. "Large Language Models Encode Clinical Knowledge." Nature, 2023.
