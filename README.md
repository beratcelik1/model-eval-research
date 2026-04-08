# AI Model Usefulness Evaluation

A research project evaluating how useful Grok is across three high-value domains. Not just "can the model answer questions" but "is it actually useful for real work in these areas."

Grok is the primary model under evaluation, with comparisons to other models where data exists. Each domain has its own Karpathy-style knowledge base (research wiki), a structured evaluation protocol, and a proposed evaluation framework.

## Structure

```
.
├── knowledge-base/              # Karpathy-style research wikis
│   ├── SCHEMA.md                # Wiki conventions and workflows
│   ├── shared/                  # Cross-domain: eval methodology, model comparisons
│   ├── investment-decisions/    # Domain 1 research wiki
│   │   ├── raw/                 # Source documents (papers, articles)
│   │   └── wiki/                # LLM-maintained markdown wiki
│   ├── marketing-behavior/      # Domain 2 research wiki
│   │   ├── raw/
│   │   └── wiki/
│   └── health-longevity/        # Domain 3 research wiki
│       ├── raw/
│       └── wiki/
├── areas/                       # Evaluation protocols and results
│   ├── investment-decisions/
│   │   ├── README.md            # Full eval protocol with 10 prompts
│   │   ├── answer-key.md        # Verified correct benchmarks with KB citations
│   │   ├── prompts/             # Individual prompt files for API testing
│   │   └── results/             # Scored responses and analysis
│   ├── marketing-behavior/
│   └── health-longevity/
├── experiments/                 # API test runs (gitignored JSONs)
│   ├── validate/                # Cheap model prompt validation
│   └── final/                   # Production model evaluation runs
├── scripts/                     # Testing and analysis tools
│   ├── run_eval.py              # Phase 1: Run prompts against models via API
│   ├── challenge_response.py    # Phase 2: Challenge Grok with evidence on gaps
│   ├── fact_check.py            # Verify factual claims in responses
│   └── extract_prompts.py       # Extract prompts from README files
└── report/                      # Final research report (LaTeX)
    └── main.tex
```

## Approach

1. **Research first** - Build domain knowledge bases before writing evals. Understand what's out there, what other models do, what benchmarks exist.
2. **Design evals** - 10 test prompts per area (60% core, 25% edge cases, 15% adversarial) with multi-axis scoring rubrics.
3. **Ground in research** - Every "correct answer" is backed by cited research from the knowledge base. Answer keys provide verified benchmarks with sources.
4. **Validate cheap** - Run prompts against cheaper models to check prompt quality and rubric clarity.
5. **Test expensive** - Run final evaluations on production models with response recording.
6. **Challenge-response** - When Grok misses something, present our evidence with sources and see if Grok accepts the correction or pushes back with counter-evidence. Three outcomes:
   - **PASS** - Grok's answer aligns with our research
   - **FAIL-ACCEPTED** - Grok missed something, accepted correction when shown evidence
   - **FAIL-CONTESTED** - Grok pushed back with different evidence (our research may be incomplete)
7. **Fact-check** - Verify all factual claims in model responses against external sources.
8. **Report** - Compile findings into a LaTeX research report with quantitative results.

## Areas of Focus

1. **Investment Decision-Making** - Can Grok reason about markets, extract signals from X data, and make decisions that generate returns? Tested from the perspective of someone running live trading bots on Kalshi and Polymarket.
2. **Marketing and Human Behavior** - Can Grok understand what makes people act, not just write grammatically correct copy? Tested from the perspective of running an AI agent on X that produces content but fails to convert.
3. **Health Optimization and Longevity** - Can Grok personalize health protocols based on individual biomarkers and genetics, and navigate scientific uncertainty safely? Tested from the perspective of following an AI-designed supplement and fitness protocol daily.

## Running Experiments

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your API key to .env

# Validate prompts on cheap model first
python scripts/run_eval.py --mode validate --area investment-decisions

# Run final evaluation on production model
python scripts/run_eval.py --mode final --area investment-decisions

# Fact-check responses
python scripts/fact_check.py --run experiments/final/latest.json

# Challenge-response: present evidence for gaps, see if Grok accepts or contests
python scripts/challenge_response.py --results experiments/final/latest.json --area investment-decisions
```
