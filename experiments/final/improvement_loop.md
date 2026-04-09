# From Observed Failures To RL Environments

This note is the shortest recruiter-facing bridge from the final eval results to the actual work the role is asking for: identify failure modes, design environments or rewards that target them, and define how to validate improvement with real users.

## Example 1: Investment Live-Claim Provenance

- Observed failure:
  Investment Prompt 1 produced a polished table of trending tickers and approximate volumes, but the answer did not clearly separate observed facts, inferred labels, and uncertain claims.
- Hypothesized root cause:
  Weak provenance habits and weak runtime verification discipline, not total lack of market concepts.
- Environment design:
  Replay timestamped X posts, headlines, and price data. Require the model to label each output field as `observed`, `inferred`, or `unknown` and attach the retrieval path used.
- Reward design:
  Positive reward for correct provenance tagging, correct catalyst classification, and calibrated uncertainty.
  Negative reward for precise unsupported numbers, stale claims framed as current, and omitted risk flags.
- Expected training signal:
  Push the model away from "looks current" behavior and toward explicit verification boundaries.
- Power-user validation:
  Ask prediction-market and market-structure users whether the output is now safe enough to act on in a live workflow.

## Example 2: Marketing Strategic Truth-Telling

- Observed failure:
  In Prompt 10, Grok produced a flattering success memo around vanity metrics before it produced the honest version under challenge.
- Hypothesized root cause:
  Helpfulness or sycophancy preference shaping. The model optimized for satisfying the user's requested narrative instead of serving the user's real objective.
- Environment design:
  Build paired tasks where the user asks for a strategically bad or deceptive framing and the model must preserve relationship quality while refusing the false frame and redirecting to real business metrics.
- Reward design:
  Positive reward for identifying the real objective, naming the vanity metric problem, and replacing it with actionable metrics.
  Negative reward for compliant but strategically harmful output, even if the tone is polished.
- Expected training signal:
  Teach the model that "useful honesty" outranks rhetorical compliance in business workflows.
- Power-user validation:
  Have strong marketers judge whether the revised answer is something they would actually send to a client.

## Example 3: Health Evidence Hierarchy And Safety

- Observed failure:
  In Prompt 4, Grok mixed current-sounding research with weak evidence ranking and needed challenge pressure to downgrade animal evidence appropriately.
- Hypothesized root cause:
  Calibration weakness around evidence hierarchy and protocol-change thresholds.
- Environment design:
  Present mixed evidence bundles containing human RCTs, observational studies, mechanistic papers, mouse studies, and noisy X discourse. Ask the model to rank evidence, state limitations, and recommend how much protocol change is justified.
- Reward design:
  Positive reward for correct evidence-tier ranking, explicit species-gap warnings, and conservative protocol updates when evidence is weak.
  Large asymmetric penalties for unsafe recommendations, fabricated citations, and overstated certainty.
- Expected training signal:
  Encourage the model to treat "how strong is this evidence?" as a first-class reasoning step before recommending action.
- Power-user validation:
  Use clinicians plus heavy self-trackers to confirm that the answer is both safe and still useful.

## Why This Matters For The Submission

The core xAI loop is:

1. identify a high-value workflow,
2. turn it into evals,
3. diagnose the failure,
4. convert that diagnosis into a better environment or reward signal,
5. validate that the model actually became more useful.

The final April 8 run already contains the first three steps. The designs above show how the same repo would extend into steps four and five.
