# AI Session Card — Template

Copy this template into `ai_logs/lab6_session_NN.md` (one file per
session) and fill in the bracketed sections. The session cards
together form a portfolio artifact you will reference in your final
project's reproducibility statement.

---

```yaml
session_id: lab6_session_NN
date: YYYY-MM-DD
tool: [ChatGPT-4 / Claude 3 / Copilot / other — include version if known]
duration_minutes: NN
context_block_used: [yes / no — paste the block you used]
```

## What I asked the AI to do

[One or two sentences describing the task. Be specific — not
"help me with refraction" but "derive the intercept-time formula
for a flat 2-layer refractor, step by step."]

## My exact opening prompt

```
[paste verbatim — including any context block]
```

## What the AI returned (summary)

[3–5 bullets summarising the response. Do NOT paste the full
response — instead, capture the gist.]

## What I cross-checked, and against what

[Name the specific page, equation, or notebook cell you verified the
response against. Examples:
- "Lowrie & Fichtner Ch. 4 §4.2.2, equation 4.34"
- "Lab 3 notebook, cell labelled `# Step 5 — fit V2`"
- "ESS 314 lecture 06_seismic_refraction_I, §3 Mathematical Framework"]

## What the AI got right

[Bullet list.]

## What the AI got wrong, or what it missed

[Bullet list. If nothing, write "Nothing detected at this depth of
checking — flag for re-verification later."]

## What I would do differently next time

[One sentence on prompt strategy, e.g., "I would supply the
two-layer geometry as a sketch description first, before asking
for the derivation."]

## Citation block for my final report

[A short, paste-ready citation, e.g.:
"ChatGPT-4 (OpenAI). Conversation on derivation of refraction
intercept time. Personal communication, 5 May 2026.
Used to scaffold §3.1 of methods section; all equations independently
re-derived from Lowrie & Fichtner Ch. 4."]
```

---

## Why these fields?

- **`tool` + `date`**: Required by the course AI use policy.
- **Context block**: Forces you to use Pattern 1 consistently.
- **Exact opening prompt**: Lets you (and a grader) see whether your
  prompt was well-specified or vague.
- **Cross-check against**: This is the *Stage 2 → Stage 3* discipline.
  An AI session with no cross-check is *not* a learning session.
- **Got wrong / missed**: Building the catalogue of AI failure modes
  is itself a learning artifact.
- **Citation block**: This is what goes in your final report's
  acknowledgements or methods section, per the ESS 314 syllabus.
