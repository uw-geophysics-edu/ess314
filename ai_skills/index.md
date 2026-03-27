# AI Skills & Skill Threads

```{admonition} Learning Objectives
:class: tip
- Understand the five persistent skill threads woven across all 10 weeks
- Know how AI literacy progresses through three developmental stages
- Apply reproducibility milestones to your own lab workflow
```

Instead of front-loading geophysics content and back-loading professional skills, the course distributes **five threads across all 10 weeks**. Each week advances every thread, not just the geophysics content.

## The five threads

| Thread | What it builds |
|--------|---------------|
| 🌊 **Geophysics content** | Domain knowledge: waves → seismics → gravity → magnetics → earth interior → inversion |
| 🐍 **Python / computing** | Scientific Python stack, ObsPy, scipy, matplotlib, ObsPy, PyTorch |
| 📋 **Reproducibility** | Git, conda environments, data provenance, pipeline automation |
| ✍️ **Technical writing** | Figure standards, IMRaD structure, citation, methods/results/interpretation |
| 🤖 **AI literacy** | Tutor → writing coach → fact-checker → rubric-defined agent |

## Thread map — all 10 weeks

| Thread | Wk 1 | Wk 2 | Wk 3 | Wk 4 | Wk 5 | Wk 6 | Wk 7 | Wk 8 | Wk 9 | Wk 10 |
|--------|------|------|------|------|------|------|------|------|------|-------|
| 🌊 Geophysics | Waves | Snell | Refl. | Signal | Grav. | Mag. | Earth int. | — | Inv. | ML |
| 🐍 Python | env | fig | NMO | FFT | grav | mag | TauP | — | inv | CNN |
| 📋 Repro | Git | commit | env | doc | cite | pipeline | DOI | — | test | audit |
| ✍️ Writing | — | fig | IMRaD | para | cite | data | methods | rubric | results | full |
| 🤖 AI literacy | tutor | quiz | debug | paper | coach | check | fact | agent | rubric | eval |

*Week 8 is the AI agent design week — the geophysics content thread pauses while students learn to write rubric-driven AI agents.*

## Reproducibility arc — 4 milestones

::::{grid} 1 2 2 2
:gutter: 3

:::{grid-item-card} Week 1 — Environment setup
<span class="ess-badge ess-b-amber">Milestone 1</span>

Set up conda environment + Git repo. Every notebook goes in the repo from day one. Standard end-of-session workflow: one meaningful commit.
:::

:::{grid-item-card} Week 3 — Data provenance
<span class="ess-badge ess-b-amber">Milestone 2</span>

Add `environment.yml` to repo. Verify your NMO notebook runs in a clean environment. Add `data/README.md` with data provenance for all external datasets.
:::

:::{grid-item-card} Week 6 — Pipeline automation
<span class="ess-badge ess-b-amber">Milestone 3</span>

Add a `run_all.sh` script that runs all notebooks in order via `jupyter nbconvert`. Test it on a clean environment. Add DOIs or persistent URLs for all datasets.
:::

:::{grid-item-card} Week 10 — Reproducibility audit
<span class="ess-badge ess-b-amber">Milestone 4</span>

`git clone` into a new directory, run `run_all.sh`, verify all figures regenerate. Target: under 10 minutes. Fix what breaks. Tag the final commit `v1.0`.
:::
::::

## AI literacy arc — 3 stages

### Stage 1 · Weeks 1–4 · AI as tutor

Use an AI assistant to derive equations interactively, get quizzed on concepts, debug code, and have papers explained. The goal is building the habit of **asking well-specified questions**.

Example prompts:
- *"Derive the acoustic wave equation from Newton's second law, one step at a time. Stop after each step and check that I follow."*
- *"Quiz me on wave impedance and reflection/transmission coefficients."*
- *"I'm a junior undergrad in geophysics at UW. I have solid math through PDEs and Python basics. Explain [concept]."*

### Stage 2 · Weeks 5–7 · AI as writing coach + fact-checker

Submit your paragraph to an AI assistant with an **explicit rubric you wrote**:

> "Does this methods paragraph have (a) what was done, (b) why, (c) what software with version, (d) what parameters, (e) enough detail to reproduce?"

Then fact-check the AI's critique against your notebook and textbook. Document **one wrong AI claim per session**. This builds the critical evaluation reflex that Stage 3 depends on.

### Stage 3 · Weeks 8–10 · AI as designable agent

Write your own system prompt for a *"Geophysics Report Reviewer"* agent. Define what a good geophysics results section looks like. Run your draft through it. Evaluate whether the agent caught real problems. Revise the rubric if it missed things.

The system prompt lives in your Git repo as `agent_instructions/report_reviewer_v1.md` — a genuine 2026 portfolio artifact.

See {doc}`ai_literacy` for the full prompting guide and the Week 8 agent design deliverable.
