# Behavioral Frameworks for AI Marketing

Key frameworks from behavioral economics and persuasion science, and how each can be tested in an AI eval.

---

## Why Behavioral Frameworks Matter for Evals

If we want to test whether an AI can write persuasive content, we need to define what persuasion looks like. "I know it when I see it" doesn't scale.

Behavioral science gives us specific, testable mechanisms. Instead of asking "is this copy persuasive?", we can ask "does this copy correctly apply social proof to reduce purchase anxiety for a skeptical audience?"

The second question is evaluable. The first is vibes.


## Cialdini's Six Principles of Influence

Robert Cialdini's framework (from "Influence: The Psychology of Persuasion") identifies six universal principles that drive human compliance. These are the most well-validated persuasion mechanisms in the literature.

### 1. Reciprocity
People feel obligated to return favors.

**How it works in marketing:** Give something valuable first (free guide, free trial, useful content), then ask for something in return (email address, purchase, referral).

**Eval test:** Give the model a scenario where a brand needs to build goodwill before asking for a sale. Does the model:
- Lead with value, not with the ask?
- Choose an appropriate gift (relevant to the audience, not just generic)?
- Time the ask correctly (after value is delivered, not simultaneously)?
- Avoid making the reciprocity feel transactional?

### 2. Commitment and Consistency
People want to act consistently with their previous commitments.

**How it works in marketing:** Get a small "yes" first (sign up for newsletter, take a quiz, agree to a statement), then build toward bigger commitments.

**Eval test:** Give the model a high-ticket sale scenario. Does the model:
- Design a step-down commitment ladder?
- Start with a low-friction action?
- Reference the prospect's previous actions/statements?
- Build logical consistency between the small and large commitment?

### 3. Social Proof
People look to others' behavior to guide their own.

**How it works in marketing:** Testimonials, user counts, "most popular" labels, expert endorsements, case studies.

**Eval test:** Give the model a scenario for a new product with limited social proof. Does the model:
- Identify what types of social proof would be most credible for this audience?
- Prioritize quality of proof over quantity?
- Match the social proof source to the audience (peer testimonials for consumers, expert endorsements for B2B)?
- Avoid generic or unbelievable claims ("10,000 satisfied customers" for a week-old product)?

### 4. Authority
People defer to credible experts.

**How it works in marketing:** Expert endorsements, credentials, research citations, industry awards, media mentions.

**Eval test:** Give the model a scenario where the brand has limited authority. Does the model:
- Identify the most relevant authority signals for this audience?
- Borrow authority appropriately (citing research, referencing experts)?
- Avoid overstepping (claiming authority the brand doesn't have)?
- Build authority through demonstrated expertise, not just claimed expertise?

### 5. Liking
People are more easily persuaded by people they like.

**How it works in marketing:** Relatable brand voice, shared values, similarity to the audience, humor, attractiveness.

**Eval test:** Give the model an audience persona with specific values and communication style. Does the model:
- Match the audience's communication style naturally?
- Reference shared values without pandering?
- Use appropriate humor (if the audience responds to it)?
- Build genuine connection, not just rapport techniques?

### 6. Scarcity
People value things more when they're rare or running out.

**How it works in marketing:** Limited time offers, limited quantity, exclusive access, waitlists.

**Eval test:** Give the model a scenario where scarcity is real vs manufactured. Does the model:
- Apply scarcity honestly (not fabricating false urgency)?
- Choose the right type of scarcity for the context?
- Explain why something is scarce (justified scarcity is more persuasive)?
- Avoid overusing scarcity (which trains audiences to ignore it)?


## PAS (Problem - Agitate - Solve)

One of the most effective copywriting frameworks. Simple but powerful.

### The Structure
1. **Problem** - Name the reader's pain point specifically
2. **Agitate** - Make the problem feel urgent and emotionally real
3. **Solve** - Present your solution as the resolution

### Why It Works
People are motivated more by avoiding pain than by seeking gain (see loss aversion below). PAS hooks the pain, amplifies it, then offers relief. It creates emotional momentum toward the solution.

### Eval Test
Give the model a product and target audience. Ask it to write PAS-structured copy. Evaluate:
- Does it identify a real, specific pain point (not a generic one)?
- Does the agitation deepen the problem without being manipulative?
- Does the solution connect directly to the agitated pain?
- Is the transition from agitate to solve smooth and credible?
- Does it avoid agitating so hard that the reader feels hopeless?


## AIDA (Attention - Interest - Desire - Action)

The classic marketing funnel applied to a single piece of content.

### The Structure
1. **Attention** - Hook the reader with something unexpected or relevant
2. **Interest** - Provide information that deepens engagement
3. **Desire** - Build emotional want for the product/outcome
4. **Action** - Clear, specific CTA

### Why It Works
It mirrors the natural decision-making process. You can't want something you haven't noticed. You can't act on something you don't want.

### Eval Test
Give the model a landing page scenario. Evaluate:
- Does the attention hook earn 3 more seconds of reading?
- Does the interest section provide new, relevant information?
- Does the desire section connect features to outcomes the audience cares about?
- Is the CTA specific, clear, and low-friction?
- Is there a logical flow from each stage to the next?


## Loss Aversion

People feel losses roughly twice as strongly as equivalent gains (Kahneman & Tversky, prospect theory).

### How It Works in Marketing
- "Don't miss out" is stronger than "You could get"
- "Stop losing $500/month" is stronger than "Save $500/month"
- "Your competitors are already doing this" is stronger than "Get ahead of competitors"

### Eval Test
Give the model a scenario where the same product benefit can be framed as a gain or as an avoided loss. Does the model:
- Choose loss framing when appropriate for the audience and context?
- Avoid loss framing when it would feel manipulative (e.g., health contexts)?
- Calibrate the intensity of loss framing to the audience's sophistication?
- Use loss aversion without creating anxiety that prevents action?


## Social Proof (Extended)

Beyond Cialdini's basic principle, social proof has nuances that matter for evals.

### Types of Social Proof (ordered by typical persuasive power)
1. **Peer proof** - "People like you" are doing this (most persuasive for consumers)
2. **Expert proof** - Credentialed authorities endorse this
3. **Celebrity proof** - Famous people use this (effective for awareness, less for conversion)
4. **Crowd proof** - Large numbers of people use this ("1M users")
5. **Certification proof** - Official stamps of approval (FDA, ISO, awards)

### Eval Nuance
The right type of social proof depends on:
- Audience sophistication (experts trust peer proof, novices trust authority)
- Purchase risk level (high-risk purchases need stronger proof)
- Product category (B2B needs case studies, B2C needs reviews)


## Anchoring

The first number a person sees influences their perception of subsequent numbers.

### How It Works in Marketing
- Show the high price first, then the discount: "$199 $99"
- Compare to an expensive alternative: "Enterprise solutions cost $50K/year. Ours is $5K."
- Set expectations high: "Most agencies charge $10K for this. We built a tool that does it for $99/month."

### Eval Test
Give the model a pricing or value proposition scenario. Does the model:
- Set an appropriate anchor before presenting the price?
- Choose an anchor that's credible (too high breaks trust)?
- Use anchoring subtly rather than heavy-handedly?
- Apply different anchoring strategies for different price points?


## How to Use These in Evals

### The Meta-Framework

For each eval scenario:

1. **Define the audience** with specific psychological profile
2. **Define the objective** (click, sign up, purchase, share)
3. **Define constraints** (brand voice, ethical boundaries, platform)
4. **Ask the model to create content**
5. **Judge on:**
   - Did it select an appropriate persuasion strategy for this audience/objective combo?
   - Did it execute the strategy correctly?
   - Did it avoid strategies that would be inappropriate or unethical for the context?
   - Would a behavioral scientist recognize the technique being applied?

### Scoring Rubric Template

| Criterion | Weight | Description |
|-----------|--------|-------------|
| Strategy selection | 25% | Did it pick the right framework for this situation? |
| Execution quality | 30% | Was the framework applied skillfully? |
| Audience calibration | 20% | Is it tuned to this specific audience? |
| Ethical boundaries | 15% | Does it avoid manipulation and deception? |
| Actionability | 10% | Is there a clear, compelling next step? |

### What We Can't Test Without Real Data

These eval rubrics test whether a model understands and applies persuasion frameworks. They don't test whether the output actually persuades. For that, you need:
- Real audience testing (A/B experiments)
- Click-through data
- Conversion data
- Longitudinal engagement data

The eval is a proxy. A good proxy, but still a proxy. The RLVR signal will eventually need to come from real conversion outcomes.
