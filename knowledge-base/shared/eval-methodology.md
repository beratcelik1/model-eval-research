# Eval Methodology

How to build evals that actually measure usefulness, not just knowledge.

---

## What Makes a Good Eval

A good eval has five properties:

1. **Discriminative** - It separates good models from bad ones. If every model scores 90%+, the eval is too easy or too narrow.
2. **Stable** - Running the same eval twice gives similar results. High variance means the eval is measuring noise.
3. **Valid** - It measures what you claim it measures. A "financial reasoning" eval that mostly tests reading comprehension is not valid.
4. **Practical** - It reflects real-world tasks, not toy problems. Academic benchmarks often fail here.
5. **Resistant to gaming** - Models shouldn't be able to score well through shortcuts that don't reflect actual capability.

The single biggest failure mode: building an eval that tests knowledge retrieval when you actually care about decision quality.


## The 60/25/15 Distribution

For domain-specific evals, a useful split:

- **60% Foundational** - Core knowledge and reasoning. Does the model understand the domain? These questions have clear right answers. Example: "What is the P/E ratio of a stock priced at $50 with EPS of $5?"
- **25% Applied** - Judgment calls with defensible answers. The model must synthesize information and make recommendations. Example: "Given these three biomarkers trending in opposite directions, what would you investigate first?"
- **15% Edge Cases** - Deliberately tricky scenarios that test honesty, uncertainty handling, and refusal to hallucinate. Example: "Based on this incomplete dataset, predict next quarter's revenue to two decimal places." (The right answer involves expressing uncertainty, not giving a precise number.)

This distribution ensures you're testing depth, not just surface pattern matching. The 15% edge cases are where models diverge most.


## Multi-Axis Scoring

Single-score evals hide important information. A model might score 80% overall but be terrible at safety and great at accuracy. You need multiple axes.

Recommended axes for domain evals:

| Axis | What It Measures | Weight (varies by domain) |
|------|-----------------|--------------------------|
| Accuracy | Is the information correct? | High for health, medium for marketing |
| Reasoning | Does the logic chain hold up? | High across all domains |
| Calibration | Does the model know what it doesn't know? | Critical for investment and health |
| Actionability | Can someone act on this advice? | High for all three domains |
| Safety | Does it avoid harmful recommendations? | Critical for health, important for investment |
| Freshness | Does it use current information? | High for investment and marketing |

Each axis gets scored independently. The final composite score uses domain-specific weights.

Avoid averaging everything into one number until the very end. Keep axis scores visible so you can diagnose where a model is weak.


## LLM-as-Judge (G-Eval Pattern)

Using one LLM to evaluate another. This is the most scalable approach, but it has real pitfalls.

### How It Works

1. Generate a response from the model being tested
2. Send the response plus a rubric to the judge model
3. The judge scores the response on each axis
4. Aggregate scores across many examples

### The G-Eval Approach

G-Eval (Liu et al., 2023) showed that LLM judges correlate well with human judgments when you:

- Provide detailed evaluation criteria (not just "rate quality 1-5")
- Ask the judge to generate chain-of-thought reasoning before scoring
- Use token probabilities to get finer-grained scores
- Average across multiple judge calls to reduce variance

### Known Problems

**Self-preference bias**: GPT-4 rates GPT-4 outputs higher than equivalent Claude outputs, and vice versa. Mitigation: use a different model family as judge, or use multiple judges and average.

**Position bias**: Judges prefer whichever response appears first in a comparison. Mitigation: randomize order and run both orderings.

**Verbosity bias**: Judges prefer longer responses even when shorter ones are more accurate. Mitigation: explicitly penalize unnecessary length in the rubric.

**Ceiling effects**: Judge models struggle to evaluate responses that exceed their own capability. If the judge can't solve the problem, it can't reliably judge solutions.

### Practical Setup

For a three-domain eval suite:
- Use at least two judge models from different families
- Run each judgment 3x to measure variance
- Include 20% human-judged calibration set to catch systematic bias
- Track inter-judge agreement. If judges disagree more than 30% of the time, the rubric needs work


## RL Environments: RLHF, RLAIF, RLVR

Evals and training are deeply connected. The eval you build today becomes the training signal tomorrow.

### RLHF (RL from Human Feedback)
- Humans rank model outputs
- A reward model learns from those rankings
- The model is trained to maximize the reward model's score
- **Limitation**: Expensive, slow, doesn't scale. Humans are inconsistent judges. Preference data goes stale.

### RLAIF (RL from AI Feedback)
- Replace human rankers with an AI judge (see G-Eval above)
- Much cheaper and faster
- **Limitation**: Inherits all biases of the judge model. Can create feedback loops where the model optimizes for judge quirks.

### RLVR (RL from Verifiable Rewards)
- Use objective, verifiable outcomes as the reward signal
- Example: Did the trade recommendation actually make money? Did the health advice align with clinical outcomes?
- **This is the gold standard for domain evals** because it measures real-world impact
- **Limitation**: Requires ground truth, which is hard to get. Long feedback loops (a trade takes days to resolve, health outcomes take months).

### The Eval-to-Training Pipeline

The progression looks like this:

1. Build an eval with human-verified ground truth
2. Use the eval to measure current model capability
3. Convert the eval into a training signal (RLAIF or RLVR)
4. Train the model against that signal
5. Re-evaluate to measure improvement
6. Update the eval to avoid overfitting

Step 6 is critical. If you don't update the eval, the model learns to game it. This is why the 15% edge cases should rotate.


## How Evals Become Training Signals

The transition from "eval" to "training data" is where most of the value gets created.

An eval is a dataset of (input, expected_output, scoring_rubric) triples. Once you have this:

1. **Direct fine-tuning**: Use high-scoring examples as training data
2. **Reward modeling**: Train a reward model on the scored examples, then use it for RL
3. **Synthetic data generation**: Use the eval rubric to generate more training examples that meet the quality bar

The key insight: a well-designed eval is worth more than a large training dataset. A 500-example eval with rigorous scoring produces better training signal than 50,000 uncurated examples.

This is why eval design deserves serious investment upfront.


## Practical Recommendations

1. Start with 100-200 examples per domain. Quality over quantity.
2. Get human expert validation on at least 20% of your ground truth.
3. Use multi-axis scoring from day one. It's painful to add later.
4. Track model performance over time, not just point-in-time snapshots.
5. Rotate 15-20% of edge cases quarterly to prevent overfitting.
6. Always run the same eval across all models you're comparing. Never compare scores from different eval sets.
7. Document your methodology so results are reproducible.
