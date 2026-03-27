# AI Literacy Guide

```{admonition} Learning Objectives
:class: tip
- Apply effective prompting patterns for technical learning in geophysics
- Progress through the three-stage AI literacy arc
- Design a rubric-driven AI agent as a portfolio artifact
- Critically evaluate AI outputs against primary sources
```

This curriculum was itself designed, critiqued, and redesigned using AI assistance. Here is how to integrate AI tools deliberately — and how not to.

## Effective prompting patterns for technical learning

### Give context first
<span class="ess-badge ess-b-teal">Pattern 1</span>

Start every session with a context-setting statement:

> *"I'm a junior undergrad in geophysics at UW. I have solid math through PDEs and Python basics. I'm studying [topic]."*

Context dramatically improves response quality. Without it, you get a generic answer; with it, you get one calibrated to your background.

### Explain-then-quiz
<span class="ess-badge ess-b-blue">Pattern 2</span>

Ask the AI to explain a concept, then immediately:

> *"Now ask me 5 conceptual questions and tell me if my answers are correct."*

More efficient than passive reading. The back-and-forth forces you to retrieve, not just recognize.

### Derivation walkthrough
<span class="ess-badge ess-b-blue">Pattern 3</span>

> *"Walk me through the derivation of the NMO equation one step at a time. Stop after each step and check if I understand."*

### Code debugging
<span class="ess-badge ess-b-amber">Pattern 4</span>

Paste your cell and ask:

> *"Does this Tikhonov inversion code look correct? Are there numerical issues? What happens as λ → 0?"*

### Writing coach with rubric
<span class="ess-badge ess-b-coral">Pattern 5</span>

> *"Critique this methods paragraph using this rubric: (1) states what was done, (2) names software with version, (3) gives enough detail to reproduce, (4) uses past tense, (5) under 150 words."*

### Paper reading assistant
<span class="ess-badge ess-b-coral">Pattern 6</span>

Paste an abstract:

> *"I'm an undergrad in geophysics. Explain the key contribution and what background knowledge I need to understand it."*

### Always push back
<span class="ess-badge ess-b-purple">Pattern 7 — Critical evaluation</span>

> *"I still don't understand step 3. Can you explain it differently using an analogy from wave mechanics?"*

And always:

> *"Is this claim consistent with what Sherriff & Geldart says about this?"*

**Never accept an AI claim about geophysics without checking it against a primary source.** Document every AI error you catch — this is itself a learning artifact.

---

## Week 8 deliverable — writing a geophysics report reviewer agent

This is the most novel skill in the curriculum. A rubric-driven AI agent is not the same as asking an AI to "proofread my text." The difference is specificity: you write explicit, testable criteria, and the AI applies them mechanically. Vague instructions produce vague feedback; specific rubrics produce specific, actionable feedback.

### Step 1 — Derive your rubric criteria

Read the Methods section of one real published geophysics paper. Identify 5–6 criteria that the section meets:

- Does it state what was done (not just "data were processed")?
- Does it name all software with version numbers?
- Does it give parameter values (filter corner frequencies, regularization λ, etc.)?
- Does it specify data source with URL or DOI and access date?
- Is it written consistently (past tense; passive or active voice throughout)?
- Does it contain enough detail that another student could reproduce it?

### Step 2 — Write the system prompt

Below is an example structure — you write your own version based on the criteria you derived:

```
You are a peer reviewer for an undergraduate geophysics report.

When reviewing a Methods section, evaluate it against these criteria:
1. States clearly what was done (not just "data were processed")
2. Names all software with version numbers
3. Gives parameter values (e.g., filter corner frequencies, λ value)
4. Specifies data source with URL or DOI and access date
5. Written in past tense, passive or active voice consistently
6. Contains enough detail that another student could reproduce it

For each criterion: quote the relevant sentence(s), state whether it
passes or fails, and if it fails, suggest a specific revision.

Do not praise vaguely. Do not suggest content that is not already
implied by the student's own data and methods.
```

### Step 3 — Test and iterate

1. Run your Week 7 Methods draft through the agent
2. Evaluate: did it catch real problems? Did it hallucinate any geophysical facts?
3. Cross-check one claim against your textbook
4. Revise the rubric to fix gaps — a v2 that catches things v1 missed is itself a learning artifact

Save as `agent_instructions/report_reviewer_v1.md` in your Git repo. This is a 2026 portfolio artifact that very few geophysics students will have.

---

## AI fluency as a career asset

AI tool fluency now appears explicitly in geoscience and data science job listings. The skill is not "knowing how to type prompts" — it is knowing how to:

1. Decompose a complex technical problem into well-specified sub-problems
2. Direct an AI tool efficiently
3. Critically evaluate its output against primary sources

That meta-skill, combined with deep domain knowledge in geophysics, is exactly what employers mean when they say they want someone who can "leverage AI." Build it deliberately. Document it on your résumé. Put your system prompt in your GitHub.

```{note}
Students with advanced prompt engineering and critical questioning skills can substantially improve both quality and efficiency of AI-supported content while mitigating hallucination risks ([Farrokhnia et al., 2024](https://doi.org/10.1007/s10462-024-10937-8)). The rubric quality is the primary determinant of AI assessment accuracy — which means designing the rubric forces you to articulate what "good" means in your domain, which is itself the deepest learning activity.
```
