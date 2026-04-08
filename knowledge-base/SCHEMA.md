# Knowledge Base Schema

Following the Karpathy LLM Wiki pattern. Each domain has its own wiki maintained by the LLM.

## Structure

```
knowledge-base/
├── SCHEMA.md              # This file - conventions and workflows
├── shared/                # Cross-domain research (eval methodology, model comparisons)
│   ├── index.md
│   └── log.md
├── investment-decisions/  # Domain 1 wiki
│   ├── raw/               # Source documents (papers, articles, data)
│   ├── wiki/              # LLM-maintained markdown wiki
│   │   ├── index.md       # Content catalog with one-line summaries
│   │   └── log.md         # Chronological record of ingests and queries
│   └── ...
├── marketing-behavior/    # Domain 2 wiki
│   ├── raw/
│   └── wiki/
└── health-longevity/      # Domain 3 wiki
    ├── raw/
    └── wiki/
```

## Conventions

- `raw/` is immutable. Drop source materials here. Never edit them.
- `wiki/` is LLM-maintained. Humans direct, LLM writes and maintains.
- `index.md` lists all wiki pages with one-line summaries, organized by category.
- `log.md` is append-only. Every ingest, query, and maintenance action gets logged.

## Workflows

### Ingest
1. Drop new source in `raw/` (article, paper, dataset, screenshot)
2. LLM reads source, extracts key takeaways
3. LLM writes summary page in `wiki/`
4. LLM updates `index.md` and relevant cross-reference pages
5. LLM appends entry to `log.md`

### Query
1. Ask a question against the wiki
2. LLM searches relevant pages, synthesizes answer with citations
3. If the answer is valuable, file it back into wiki as a new page
4. Append query + answer summary to `log.md`

### Lint
1. Run periodic health checks
2. Find contradictions, stale claims, orphan pages
3. Flag missing cross-references and data gaps
4. LLM suggests fixes and new research directions

## What Goes in Each Domain Wiki

### Shared
- Eval methodology (how to design good evals, scoring rubrics, RL environments)
- Model comparison data (benchmarks, head-to-head tests, public leaderboards)
- Cross-domain patterns (common failure modes, what makes models useful)

### Investment Decisions
- Current AI trading research and results
- Prediction market mechanics and analysis
- Financial benchmarks (FinanceBench, FinQA, etc.)
- Real-time signal analysis methods
- Risk management frameworks

### Marketing Behavior
- Behavioral economics research relevant to AI marketing
- Persuasion frameworks and their effectiveness
- Content strategy analysis and benchmarks
- Conversion optimization research
- AI content generation quality studies

### Health Longevity
- Supplement research and interaction databases
- Longevity protocol evidence (NMN, metformin, rapamycin debates)
- Biomarker interpretation guidelines (optimal vs normal ranges)
- AI safety in health contexts
- Regulatory landscape for AI health advice
