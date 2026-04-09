# AI Model Usefulness Evaluation

A research project evaluating how useful Grok is across three high-value domains. Not just "can the model answer questions" but "is it actually useful for real work in these areas."

Grok is the primary model under evaluation, with comparisons to other models where data exists. Each domain has its own Karpathy-style knowledge base (research wiki), a structured evaluation protocol, and a proposed evaluation framework.

## Repo Map

This repo is organized so a reader can quickly understand the target user groups, the evaluation method, the final runs, and the main conclusions.

- **Three priority-ordered areas of usefulness**
  - [Investment Decisions](areas/investment-decisions/README.md)
  - [Marketing Behavior](areas/marketing-behavior/README.md)
  - [Health Longevity](areas/health-longevity/README.md)
- **Why I care about each area + how good I think Grok is there**
  - At the top of each area README
- **Representative Grok conversation artifacts and eval-building direction**
  - Summarized in the area READMEs, [experiments/final/conversation_artifacts.md](experiments/final/conversation_artifacts.md), and the final report
- **Power-user X profiles to guide future eval work**
  - Listed in each area README
- **Final research report**
  - [Evaluating Grok's Usefulness (PDF)](Evaluating_Groks_Usefulness_Berat_Celik_April_2026.pdf)
- **Canonical final-run audit trail**
  - [experiments/final/README.md](experiments/final/README.md)
  - [experiments/final/improvement_loop.md](experiments/final/improvement_loop.md)
- **Knowledge base and source catalogs**
  - [Knowledge base schema](knowledge-base/SCHEMA.md)
  - [Investment research wiki](knowledge-base/investment-decisions/wiki/index.md) | [sources](knowledge-base/investment-decisions/raw/sources.md)
  - [Marketing research wiki](knowledge-base/marketing-behavior/wiki/index.md) | [sources](knowledge-base/marketing-behavior/raw/sources.md)
  - [Health research wiki](knowledge-base/health-longevity/wiki/index.md) | [sources](knowledge-base/health-longevity/raw/sources.md)
- **Answer keys and scoring rubrics**
  - [Investment answer key](areas/investment-decisions/answer-key.md)
  - [Marketing answer key](areas/marketing-behavior/answer-key.md)
  - [Health answer key](areas/health-longevity/answer-key.md)
- **Scores and grading**
  - [Final grades with Phase 1 baselines](experiments/final/final_grades.md)

## Canonical Results

The canonical conclusion of this repo is based on the **April 8, 2026 final run**.

- Each prompt has **one published score**
- That score is computed as **75% cold-response usefulness + 25% challenge review** when a challenge is issued
- Unchallenged prompts keep their cold-response score
- Published domain usefulness scores:
  - Investment Decisions: `56.2/100`
  - Marketing Behavior: `54.1/100`
  - Health Longevity: `61.4/100`
  - Overall: `57.2/100`
- The report also preserves the Phase 1 baseline (`54.2/100` overall) so the reader can see what Grok volunteered before challenge

Canonical artifacts:

- [Evaluating Grok's Usefulness (PDF)](Evaluating_Groks_Usefulness_Berat_Celik_April_2026.pdf)
- [report/main.tex](report/main.tex)
- [final_grades.md](experiments/final/final_grades.md)
- [experiments/final/README.md](experiments/final/README.md)

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
│   │   ├── answer-key.md        # Verified correct benchmarks with real citations
│   │   └── prompts/             # Individual prompt files for API testing
│   ├── marketing-behavior/
│   └── health-longevity/
├── experiments/                 # API test runs and final audit artifacts
│   ├── validate/                # Cheap model prompt validation
│   └── final/                   # Production model runs, summaries, and audit docs
├── scripts/                     # Testing and analysis tools
│   ├── run_eval.py              # Run eval with optional --challenge for Phase 2
│   ├── extract_prompts.py       # Extract prompts from README files
│   ├── grade_responses.py       # Checklist-based scoring with weighted rubrics
│   ├── eval_schema.py           # Shared parsing helpers and data models
│   └── fact_check.py            # Verify factual claims in responses
└── report/                      # Final research report (LaTeX)
    └── main.tex
```

## Approach

1. **Research first** - Build domain knowledge bases before writing evals. Understand what's out there, what other models do, what benchmarks exist.
2. **Design evals** - 10 test prompts per area (60% core, 25% edge cases, 15% adversarial) with multi-axis scoring rubrics.
3. **Ground in research** - Every "correct answer" is backed by cited research from the knowledge base. Answer keys provide verified benchmarks with sources.
4. **Validate and iterate cheap** - Run prompts against cheaper models and local review to tighten wording, clarify rubrics, and catch answer-key mistakes before spending production tokens.
5. **Fact-check the benchmark** - Verify factual claims in prompts and answer keys before trusting the final battery.
6. **Test expensive** - Run final evaluations on the highest Grok model with response recording.
7. **Challenge-response** - If a first answer looks weak, send a challenge in the same prompt thread and observe how Grok revises. The published prompt score weights the cold response at 75% and the challenge review at 25%, so revision can improve or worsen the final result.
8. **Report** - Compile findings into a LaTeX research report focused on usefulness, failure modes, improvement requirements, and next steps.

## Areas of Focus

1. **Investment Decision-Making** - Can Grok reason about markets, extract signals from X data, and make decisions that generate returns? Tested from the perspective of someone running live trading bots on Kalshi and Polymarket.
2. **Marketing and Human Behavior** - Can Grok understand what makes people act, not just write grammatically correct copy? Tested from the perspective of running an AI agent on X that produces content but fails to convert.
3. **Health Optimization and Longevity** - Can Grok personalize health protocols based on individual biomarkers and genetics, and navigate scientific uncertainty safely? Tested from the perspective of following an AI-designed supplement and fitness protocol daily.

## Running Experiments

```bash
pip install -r requirements.txt
cp .env.example .env
# Add your API key to .env

# Verify the local pipeline first
python -m unittest discover -s tests -v
python scripts/extract_prompts.py --area investment-decisions

# Validate prompts on cheap model first
python scripts/run_eval.py --mode validate --area investment-decisions --dry-run
python scripts/run_eval.py --mode validate --area investment-decisions

# Run final evaluation on production model
python scripts/run_eval.py --mode final --area investment-decisions

# Run with challenge-response (Phase 1 + Phase 2 in the same prompt thread)
python scripts/run_eval.py --mode final --area investment-decisions --challenge

# Re-score an existing run with the local checklist grader
python scripts/grade_responses.py \
  --results experiments/final/investment-decisions_challenge_YYYYMMDD_HHMMSS.json \
  --area investment-decisions

# Fact-check responses
python scripts/fact_check.py \
  --run experiments/final/investment-decisions_challenge_YYYYMMDD_HHMMSS.json
```

## Reliability Notes

- Prompt files are generated from the area README files. Use `scripts/extract_prompts.py` after editing any prompt battery.
- Each prompt is evaluated in its own fresh conversation. In challenge mode, the follow-up stays in the same prompt-level thread so answer-key evidence does not leak into later prompts.
- Challenge review is part of the published scoring logic. The cold response remains dominant, but second-round behavior can still move the final prompt score.
- The tracked raw final-run JSONs live in `experiments/final/`. File hashes, challenge coverage, conversation excerpts, and score-provenance notes are documented in `experiments/final/README.md`.
- `python -m unittest discover -s tests -v` is the minimum local integrity check before trusting regenerated prompts or scoring output.
- The current canonical published score is the April 8, 2026 final run result: `57.2/100` overall (`56.2` investment, `54.1` marketing, `61.4` health).
