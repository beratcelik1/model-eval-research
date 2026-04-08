# Model Comparisons

How to compare models fairly, what data exists, and how to run head-to-head tests.

---

## The Problem with Model Comparisons

Most public model comparisons are unreliable because:

1. **Different eval sets** - Comparing GPT-4's MMLU score to Claude's MMLU score is only valid if they ran the exact same version of the benchmark with the same prompts.
2. **Cherry-picked examples** - Companies showcase their best results. Nobody tweets their model's worst outputs.
3. **Version drift** - "GPT-4" in March 2024 is not the same model as "GPT-4" in January 2025. API models change silently.
4. **Prompt sensitivity** - The same question phrased differently can flip which model wins. A 5% difference in benchmark scores can disappear with prompt tuning.
5. **Contamination** - Models may have been trained on benchmark data. High scores on public benchmarks don't prove capability.


## Existing Comparison Frameworks

### LMArena (formerly Chatbot Arena)
- Crowdsourced head-to-head comparisons
- Users vote on which response they prefer
- Produces Elo ratings across models
- **Strengths**: Large sample size, real user preferences, updated regularly
- **Weaknesses**: Biased toward conversational quality over domain expertise. Users prefer confident-sounding wrong answers over hedged correct ones. Demographic skew toward tech-literate English speakers.

### HELM (Stanford)
- Holistic Evaluation of Language Models
- Tests across many scenarios with standardized prompts
- **Strengths**: Consistent methodology, broad coverage
- **Weaknesses**: Scenarios are academic, not practical. Doesn't test real-world task completion.

### Open LLM Leaderboard (HuggingFace)
- Standardized benchmarks: MMLU, ARC, HellaSwag, TruthfulQA, Winogrande, GSM8K
- **Strengths**: Reproducible, open methodology
- **Weaknesses**: Only tests open-weight models on the main leaderboard. Benchmarks are saturated for frontier models.

### Simple Evals (OpenAI)
- OpenAI's minimal eval framework
- Tests on MMLU, MATH, GPQA, HumanEval, DROP
- **Strengths**: Clean, simple code. Easy to add new models.
- **Weaknesses**: Small set of benchmarks. Doesn't cover domain-specific capability.

### Domain-Specific
- **Finance**: FinanceBench, FinQA, FLUE (see existing-benchmarks.md)
- **Medical**: MedQA, MedMCQA, PubMedQA
- **Marketing**: EQ-Bench3 (emotional intelligence), LMArena (text quality)

None of these frameworks test the thing that matters most: can this model help a real person make a better decision?


## Public Data: Grok vs GPT-4 vs Claude vs Gemini

What we know as of early 2026, with appropriate caveats:

### General Capability (LMArena Elo, approximate)
| Model | Elo Range | Notes |
|-------|-----------|-------|
| GPT-4o / GPT-4 Turbo | 1250-1280 | Strong all-rounder |
| Claude 3.5 Sonnet / Opus | 1240-1270 | Best at nuance, safety-aware |
| Gemini 1.5 Pro / Ultra | 1230-1260 | Strong on long context, multimodal |
| Grok-2 / Grok-3 | 1220-1260 | Fast iteration, real-time X access |

These numbers shift constantly. Don't treat them as ground truth.

### Domain Observations

**Finance**:
- All models struggle with multi-step financial math (FinanceBench: ~57% average)
- Grok has unique access to real-time X data, which could be a significant edge for sentiment
- GPT-4 tends to give the most structured financial analysis
- Claude is most cautious about financial advice disclaimers

**Marketing**:
- Grok ranked #1 on EQ-Bench3 (emotional intelligence proxy)
- Claude produces the most human-sounding copy
- GPT-4 is strongest at structured marketing strategy
- All models generate content that "sounds good" but conversion data is essentially nonexistent

**Health**:
- GPT-4 leads on MedQA benchmarks
- Claude is most consistent about safety caveats
- All models show bimodal failure: either too cautious ("consult your doctor") or too specific (hallucinated dosages)
- Grok shows promise on interpreting recent research due to real-time data access


## Methodology for Head-to-Head Testing

### Principles

1. **Same prompts, same order** - Every model gets identical inputs. Randomize question order to avoid position effects in the dataset.
2. **Blind judging** - Judges (human or LLM) should not know which model produced which response.
3. **Multiple runs** - Run each prompt at least 3 times per model. Models are stochastic. A single run proves nothing.
4. **Temperature control** - Use the same temperature setting across models. Default to temperature=0 for reproducibility, but also test at temperature=0.7 for creative tasks.
5. **Version pinning** - Record the exact model version/snapshot. "gpt-4" is not a version. "gpt-4-0125-preview" is.

### Sample Size

How many examples do you need?

- To detect a 10% difference with 95% confidence: ~100 examples per model
- To detect a 5% difference with 95% confidence: ~400 examples per model
- To detect a 3% difference with 95% confidence: ~1,000 examples per model

Most public comparisons use 50-200 examples. This is enough to detect large differences but not enough to make claims about small edges.

### Design

```
For each test question:
  1. Send to all models with identical prompt
  2. Collect responses (3 runs each)
  3. Strip model identifiers
  4. Send to judge(s) with scoring rubric
  5. Record scores per axis
  6. Repeat with reversed response order (for LLM judges)
```

### Statistical Significance

Don't just compare averages. Use:

- **Paired t-test or Wilcoxon signed-rank** for comparing two models on the same questions
- **Bootstrap confidence intervals** for estimating the range of likely true scores
- **Cohen's d** for effect size (how meaningful is the difference, not just whether it exists)

A statistically significant difference of 1% is real but probably not meaningful. Focus on effect size, not just p-values.


## What Comparisons Miss

Even a well-designed comparison doesn't capture:

1. **Latency** - A model that's 20% better but 5x slower may be worse for real-time applications
2. **Cost** - Price per token varies 10x across providers
3. **Reliability** - Uptime, rate limits, and API stability matter in production
4. **Context window** - Models with larger context can handle more complex inputs
5. **Tool use** - Some models are much better at using tools (search, code execution, APIs)
6. **Real-time data** - Grok's X integration is a structural advantage that benchmarks don't capture
7. **Customizability** - Can you fine-tune it? How much does fine-tuning help?

A comprehensive comparison needs to include these operational factors, not just quality scores.


## Recommendations

1. Never trust a single benchmark. Look at patterns across multiple evaluations.
2. Build your own domain-specific eval before drawing conclusions. Generic benchmarks don't predict domain performance.
3. Run head-to-heads on YOUR use case with YOUR data. Public comparisons tell you about average performance, not your specific situation.
4. Track performance over time. Models get updated. Today's winner might not be tomorrow's.
5. Weight recent results more heavily. A comparison from 6 months ago is ancient in this field.
6. When in doubt, run both models and measure which produces better outcomes for your users.

---

## References

1. LMArena (formerly Chatbot Arena). LMSYS Org. https://lmarena.ai/ - Elo ratings are approximate and shift frequently; the ranges cited here reflect early 2026 snapshots and should not be treated as fixed values.
2. HELM: Holistic Evaluation of Language Models. Stanford CRFM. https://crfm.stanford.edu/helm/
3. Open LLM Leaderboard. HuggingFace. https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
4. OpenAI Simple Evals. https://github.com/openai/simple-evals
5. EQ-Bench3 Leaderboard. https://eqbench.com/ - Grok models have ranked #1; current leaderboard shows Grok-4.1 Thinking leading with an Elo of 1586.
