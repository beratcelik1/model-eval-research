# Current State of AI in Health Optimization

What AI gets right, where it fails, and why health is the hardest domain to eval.

---

## The Overall Picture

AI in health optimization is in an awkward position. Models know an enormous amount of medical information. They can pass licensing exams. They can explain complex biochemistry. But when someone asks "should I take NMN?", the responses range from dangerously specific to uselessly vague.

The fundamental tension: health advice needs to be both personalized and safe. These goals pull in opposite directions. Personalization requires making specific recommendations. Safety requires hedging and disclaimers. Most models haven't figured out how to do both.


## Mixed Accuracy

### What Models Get Right
- **Factual medical knowledge** - Models score 85-92% on MedQA (USMLE-level questions). They know the science.
- **Drug interaction basics** - Well-documented interactions (warfarin + aspirin, SSRIs + MAOIs) are reliably flagged.
- **Mechanism explanation** - Models can explain how supplements work at a biochemical level, often better than most clinicians can.
- **Literature awareness** - Models know about major studies, meta-analyses, and systematic reviews.

### What Models Get Wrong
- **Dosage precision** - Models sometimes hallucinate specific dosages, especially for supplements that don't have FDA-established doses.
- **Individual variation** - Models give population-level advice to individual people. "Most people tolerate X well" is not the same as "you will tolerate X well."
- **Interaction complexity** - Beyond well-documented pairs, models miss subtle interactions (supplement-supplement, supplement-medication, supplement-condition).
- **Evidence quality assessment** - Models cite studies without adequately weighing their quality. A single rat study and a large RCT get similar treatment.
- **Temporal context** - Models don't know if their information is current. A recommendation based on a 2019 study may have been contradicted by a 2025 study.


## The Bimodal Failure Pattern

This is the most important observation about AI health advice. Models don't fail in the middle. They fail at both extremes.

### Failure Mode 1: Too Cautious
- "I recommend consulting with your healthcare provider before making any changes to your supplement regimen."
- "I cannot provide medical advice. Please see a doctor."
- "Every individual is different, so I cannot make a specific recommendation."

This response is safe but useless. The person asking already knows they could see a doctor. They're asking the AI because they want a more informed starting point. When the model refuses to engage, it provides zero value.

**When this happens:** Models default to extreme caution when:
- The question touches anything that could be construed as medical advice
- The topic is controversial (like the NMN debate)
- The model detects health-related keywords

### Failure Mode 2: Too Aggressive
- "Based on your description, you should take 1000mg of NMN daily, 500mg of resveratrol, and 2g of omega-3s."
- "Your vitamin D level of 35 ng/mL is suboptimal. I recommend supplementing with 5000 IU daily."
- Specific protocol recommendations without knowing the person's full medical history, medications, or conditions.

This response sounds helpful but could be harmful. The model doesn't know enough about the individual to make these specific recommendations safely.

**When this happens:** Models give overly specific advice when:
- The question is framed as a direct request ("what should I take?")
- The prompt includes some personal data (blood work results, age, goals)
- The model has been system-prompted to be helpful and specific

### The Missing Middle Ground
What good health advice looks like:
- "Based on the research, NMN at 250-500mg/day has shown [specific effects] in [specific studies]. However, [limitations of the evidence]. Given your [specific context], the key considerations are [A, B, C]. Here's what I'd want to know before making a stronger recommendation: [questions]."

This gives the person useful information, appropriate context, clear limitations, and a path forward. Almost no model consistently hits this middle ground.


## Legal Concerns

### Georgetown Law Research
Georgetown Law published research examining the legal liability landscape for AI health advice. Key findings:

- **No established legal framework** for AI-generated health recommendations
- **Potential liability paths**: product liability (AI as defective product), professional liability (AI practicing medicine without a license), negligence
- **The gray zone**: Information vs advice. "Vitamin D helps with bone health" is information. "You should take 5000 IU of vitamin D" is advice. The line between them is legally unclear.
- **Platform liability**: Companies providing AI health tools may face different liability than companies providing search results
- **Disclosure requirements**: Growing legal consensus that AI health outputs should be clearly labeled as non-medical

### Why This Matters for Evals
Evals need to test whether models navigate this legal landscape appropriately:
- Do they distinguish information from advice?
- Do they include appropriate disclaimers without hiding behind them?
- Do they flag when a question requires professional medical judgment?
- Do they avoid specific dosage recommendations without sufficient context?


## The MRI Pathology Detection Win (May 2025)

A bright spot. In May 2025, studies confirmed that AI systems can match or exceed radiologist accuracy in detecting certain pathologies on MRI scans. This is significant because:

- **Concrete, measurable outcome** - Either the AI found the tumor or it didn't
- **Well-defined task** - Image classification, not open-ended advice
- **Clear ground truth** - Pathology reports confirm the correct answer
- **High stakes with clear benefit** - Faster, more consistent screening

### Why This Doesn't Transfer
MRI analysis is a pattern recognition task with:
- Clear inputs (image)
- Binary outputs (pathology present/absent)
- Definitive ground truth (biopsy results)
- No personalization needed

Health optimization is the opposite:
- Complex inputs (lifestyle, genetics, goals, medical history)
- Open-ended outputs (protocol recommendations)
- No definitive ground truth (optimal health is not binary)
- Deeply personal (what works for one person may not work for another)

The success of AI in medical imaging does not predict success in health optimization advice.


## The Normal vs Optimal Range Problem

This is a critical concept for health evals.

### Normal Ranges
Medical reference ranges define "normal" as roughly the middle 95% of a population. If your vitamin D is between 30-100 ng/mL, it's "normal." A model trained on medical texts will confirm this.

### Optimal Ranges
The longevity/optimization community argues that "normal" is not the goal. They point to research suggesting that optimal ranges are narrower:
- Vitamin D: 40-60 ng/mL (vs normal 30-100)
- Ferritin: 40-100 ng/mL for women, 40-150 for men (vs normal 12-300)
- fasting glucose: 70-85 mg/dL (vs normal <100)
- HbA1c: 4.5-5.2% (vs normal <5.7%)

### The AI Challenge
Models face a genuine dilemma:
- Citing normal ranges is safe but may be suboptimal
- Citing optimal ranges is potentially more useful but has weaker evidence support
- The difference matters: someone with a vitamin D of 32 is "normal" but potentially sub-optimal
- Different experts disagree on what "optimal" means

### Eval Implications
A good health eval should test:
1. Does the model know the difference between normal and optimal ranges?
2. Does it communicate which standard it's using and why?
3. Does it acknowledge the uncertainty in optimal range claims?
4. Does it adapt its recommendation based on the person's goals (e.g., general wellness vs longevity optimization)?


## Hallucination Risk

Health is where hallucination is most dangerous. Specific failure patterns:

### Fabricated Studies
Models cite studies that don't exist, with plausible-sounding journal names, authors, and findings. In health, a fabricated study could justify a harmful recommendation.

### Invented Dosages
Models generate specific dosages (e.g., "take 750mg of berberine twice daily") that sound precise but may be made up. The specificity creates false confidence.

### False Interactions
Models sometimes claim interactions exist that don't, or miss interactions that do. Both are dangerous. False positive interactions lead to unnecessary avoidance. False negative interactions lead to harm.

### Confident Uncertainty
The most subtle form: the model is wrong but its language is confident. "Research clearly shows..." when the research is actually mixed. "It's well established that..." when there's genuine scientific debate.


## Where the Eval Opportunity Is

| What Benchmarks Test | What Matters |
|---------------------|-------------|
| Can it pass a medical exam? | Can it give useful health advice? |
| Does it know drug interactions? | Can it reason about novel supplement combinations? |
| Can it explain a mechanism? | Can it weigh conflicting evidence? |
| Does it know reference ranges? | Does it know the difference between normal and optimal? |
| Can it read a study? | Can it assess study quality and relevance to an individual? |

The eval needs to test:
1. Navigation of the cautious-to-aggressive spectrum
2. Evidence quality assessment (not just "does a study exist" but "how good is it?")
3. Handling of scientific controversy (see longevity-debates.md)
4. Safety reasoning (contraindications, interactions, dosage limits)
5. Personalization quality (does it use available context appropriately?)
6. Honest uncertainty ("I don't know" when appropriate)
