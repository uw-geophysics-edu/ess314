---
name: geophysics-lecture-author
description: >
  Use this skill whenever the user wants to convert, refactor, or author geophysics lecture content
  from existing slide decks (PDF/ZIP format with JPEG slides + text extracts) into polished,
  open-access JupyterBook-compatible MyST Markdown lecture files for ESS 314 Geophysics at UW.
  Triggers include: "convert this lecture", "build lecture notes from slides", "refactor the slide
  deck", "generate the markdown for this lecture", "analyze this lecture", "audit this deck",
  "replace figures", "find open-access sources for", "add research context to", or any request to
  transform raw slide content into structured, open, accessible course material aligned with the
  course syllabus. Always use this skill when project files include .pdf files that are actually
  ZIP archives of JPEG slide images. Always use this skill when the user asks to generate or
  improve any ESS 314 lecture, even if no slides are attached.
---

# Geophysics Lecture Author — ESS 314 (UW)

Converts raw slide decks into open, accessible, pedagogically coherent JupyterBook lecture files
for ESS 314 Geophysics at the University of Washington. Every lecture must be grounded in
open-access source material, aligned to the course syllabus learning objectives (LOs 1–7) and
learning outcomes, and enriched with a research horizon section and a societal relevance hook.

---

## Course Context (Always Keep in Mind)

**Course:** ESS 314 – Geophysics, UW, 5 credits, Spring 2026  
**Instructor:** Marine Denolle  
**Textbook (recommended, available free via UW Libraries):** Lowrie & Fichtner, *Fundamentals of Geophysics*, 3rd ed. (2020), Cambridge. DOI: 10.1017/9781108685917

### Syllabus Learning Objectives (LO 1–7)
Every lecture must explicitly map to at least two of these:

| ID | Objective |
|----|-----------|
| LO-1 | Analyze and explain how geophysical observables arise from Earth properties and physical processes |
| LO-2 | Apply simplified physical models and mathematical frameworks to predict how subsurface structure influences observations |
| LO-3 | Formulate the relationship between data, model parameters, and forward models; interpret misfit; recognize non-uniqueness |
| LO-4 | Critically evaluate the strengths, assumptions, and limitations of geophysical methods |
| LO-5 | Use computational tools to implement forward models, explore parameter sensitivity, and compare with observations |
| LO-6 | Communicate geophysical reasoning through figures, written reports, and discussion with explicit assumptions and uncertainties |
| LO-7 | Use generative AI tools responsibly to support coding, visualization, and self-assessment while critically evaluating outputs |

### Syllabus Learning Outcomes (LO-OUT)
At least two of these must be directly practiced or assessed in each lecture:

- **LO-OUT-A**: Sketch a survey geometry and predict qualitatively how an interface/anomaly affects an observation
- **LO-OUT-B**: Compute simple travel times, ray paths, reflection/refraction geometry, or gravity/magnetic responses
- **LO-OUT-C**: Explain *why* a method works physically, not just how to run it
- **LO-OUT-D**: Set up a simple inverse problem (parameters, observations, forward relation, residual)
- **LO-OUT-E**: Interpret residuals and discuss non-uniqueness, uncertainty, and resolution
- **LO-OUT-F**: Decide which method fits a given Earth question and scale
- **LO-OUT-G**: Produce a reproducible notebook with labeled figures, units, assumptions, and interpretation
- **LO-OUT-H**: Critique a research figure or AI-generated explanation for correctness and hidden assumptions

---

## Input Format

Project PDFs are **ZIP archives** (despite the `.pdf` extension) containing:
- `manifest.json` — page metadata: page count, per-page `has_visual_content` flag, image paths
- `N.jpeg` — rasterized slide images (1456×840px)
- `N.txt` — extracted text per slide (often sparse; treat as a hint, not ground truth)

**Always extract and read the slides before writing anything.**

### Slide Extraction Protocol

```bash
cp /mnt/project/LECTURE_FILE.pdf /tmp/lecture.zip
unzip -o /tmp/lecture.zip -d /tmp/lecture_slides/
cat /tmp/lecture_slides/manifest.json   # check page count + visual flags
```

Then `view` each slide image. Read ALL slides before writing. Capture exact equation notation.
For `has_visual_content: true` slides, always view the image — it is the content.

---

## Phase 1: Slide Audit (Output Before Writing)

Produce this structured audit first. Present it to the instructor for confirmation.

```markdown
## Slide Audit: [Lecture Title]
**File:** filename.pdf | **Slides:** N | **Date:** [course date]

### Content Inventory
| # | Type | Summary | Figure Source | Copyright | Action |
|---|------|---------|---------------|-----------|--------|
| 1 | Title | ... | ... | ⚠️/❌/✅ | [PYTHON-REGEN/AI-GEN/OPEN] |

### Pedagogical Gap Analysis
| Criterion | Status | Gap to Fill |
|-----------|--------|-------------|
| LOs stated in deck | ❌/⚠️/✅ | |
| Geoscientific motivation | ❌/⚠️/✅ | |
| Mathematical framework complete | ❌/⚠️/✅ | |
| Forward problem addressed | ❌/⚠️/✅ | |
| Inverse problem addressed | ❌/⚠️/✅ | |
| Research horizon present | ❌ (always missing) | Add §8 |
| Societal relevance hook | ❌ (always missing) | Add §9 |
| Course LO alignment | ❌/⚠️/✅ | |

### Copyright Inventory
[List every figure with external source. Tag: [PYTHON-REGEN] | [AI-GEN] | [OPEN-CC] | [OPEN-PD]]

### Open-Access Sources to Search
[List 3-5 specific topics to search for supplementary open-access material]
```

---

## Phase 2: Open-Access Source Research (Required Before Writing)

Before writing the lecture, search for open-access material to supplement and enrich slide content.
This is not optional — the whole point is to build a textbook *independent* of paywalled sources.

### Priority Source Hierarchy

**Tier 1 — Cite freely, reproduce with attribution:**
- **MIT OCW:** `ocw.mit.edu` — 12.201 Essentials of Geophysics (Van Der Hilst), 12.510 Introduction to Seismology. CC BY NC SA.
- **EarthScope/IRIS:** `iris.edu/hq/programs/epo` — Teachable Moments, animations, workshop Jupyter notebooks (CC BY)
- **seismo-live:** `seismo-live.org` — Community Jupyter notebooks for seismology (open source)
- **USGS:** `usgs.gov` — Public domain. Earthquake catalogs, hazard maps, educational publications
- **SCOPED project:** `scoped.codes` — Open computational seismology notebooks (NSF-funded, CC BY)
- **Lowrie & Fichtner (2020):** *Available free via UW Libraries* — cite chapters, paraphrase (do NOT reproduce text)
- **AGU/EGU open-access journals:** GRL, JGR Solid Earth, Earth and Planetary Science Letters (check individual article licenses)
- **arXiv:** `arxiv.org` — preprints, often open access

**Tier 2 — Use for citations and concept grounding (no reproduction):**
- Stein & Wysession (2003) — standard seismology reference, cite section numbers
- Sheriff & Geldart (1995) — exploration seismology, cite only
- Any paywalled journal paper — cite DOI, paraphrase concepts, never reproduce figures or text

### Search Protocol

For each lecture, perform these searches BEFORE writing:

```
1. web_search: "[topic] open access lecture notes geophysics undergraduate site:ocw.mit.edu OR site:iris.edu"
2. web_search: "[topic] review 2022 2023 2024 open access geophysics"  
3. web_search: "[topic] Jupyter notebook tutorial seismology obspy earthscope"
4. web_search: "[topic] societal applications hazards climate resources 2023 2024"
```

Spend ~5 minutes (4–6 searches) on research. Record findings in a source table before writing:

```markdown
### Open-Access Sources Found
| Source | Type | Relevance | License | URL |
|--------|------|-----------|---------|-----|
| MIT OCW 12.201 §4.5 | Lecture notes | Wave equation derivation | CC BY NC SA | ocw.mit.edu/... |
| IRIS Teachable Moment | Animation + worksheet | P/S wave types | CC BY | iris.edu/... |
| Kubo et al. 2024, EPS | Review paper | ML in seismology (AI literacy) | CC BY | doi:... |
```

---

## Phase 3: Write the Lecture Markdown

Output path: `chapters/WW_TOPIC/lecture_NN.md`

### Required File Structure

```markdown
---
title: "[Lecture Title]"
week: W
lecture: N
date: "[YYYY-MM-DD]"
topic: "[Topic]"
course_lo: ["LO-1", "LO-2", "LO-5"]        # from syllabus
learning_outcomes: ["LO-OUT-B", "LO-OUT-C"] # from syllabus
open_sources:
  - "Lowrie & Fichtner 2020 Ch. N (UW Libraries)"
  - "MIT OCW 12.201 §4.X"
  - "IRIS/EarthScope [resource name]"
---

# [Lecture Title]

## Syllabus Alignment

| | |
|---|---|
| **Course LOs addressed** | LO-1 (observables from Earth properties), LO-2 (mathematical models), LO-5 (computation) |
| **Learning outcomes practiced** | LO-OUT-B (compute travel times), LO-OUT-C (explain why method works) |
| **Lowrie & Fichtner chapter** | Ch. N, §N.N–N.N |
| **Lab connection** | Lab N: [title] |

---

## Learning Objectives

By the end of this lecture, students will be able to:
- **[LO-W.1]** [Bloom verb — Analysis or higher] [concept] [in context]
- **[LO-W.2]** ...
- **[LO-W.3]** ...

*Bloom's level guide: define/identify (Knowledge) → explain/describe (Comprehension) →
calculate/apply (Application) → derive/analyze/compare (Analysis) → design/predict (Synthesis)*

---

## Prerequisites

Students should be comfortable with:
- [Concept — link to specific prior lecture, e.g., "Stress-strain relations (Lecture 3)"]
- [Math tool, e.g., "Partial derivatives and the chain rule (Calculus II)"]

---

## 1. The Geoscientific Question  *(~10% of lecture)*

[Motivating narrative. Open with a field observation, a scientific puzzle, a recent event,
or a real dataset. Answer: "Why would a geoscientist care about this?"
1–3 paragraphs. Active voice. Direct address. Do NOT start with definitions.]

---

## 2. Governing Physics  *(~20% of lecture)*

[Physical principles behind the method. Connect explicitly to prior lectures.
Use Key Concept admonitions for encapsulations.]

:::{admonition} Key Concept
:class: important
[1–2 sentence encapsulation of the core physical idea, in plain language]
:::

---

## 3. Mathematical Framework  *(~30% of lecture)*

:::{admonition} Notation
:class: note
| Symbol | Quantity | Units | Type |
|--------|----------|-------|------|
| $u$ | particle displacement | m | scalar/vector/tensor |
| $\rho$ | density | kg/m³ | scalar |
...
:::

[Derivation with ALL intermediate steps. Label equations. Define variables before use.
Show physical interpretation of each term, not just algebra.]

$$
\text{[equation]}
$$ (eq:label)

:::{admonition} Key Equation
:class: important
Eq. {eq}`eq:label` says physically: [one sentence plain-language interpretation].
Check dimensions: [explicit unit check].
:::

---

## 4. The Forward Problem  *(~15% of lecture)*

[Given a model of Earth structure, what does the theory predict we should observe?
Make the mapping explicit: model parameters → observable quantities.
Connect to the companion Python notebook.]

**Model parameters:** [list what you need to specify]
**Observables predicted:** [list what the forward model outputs]

See companion notebook: `notebooks/lecture_NN_forward.ipynb`

---

## 5. The Inverse Problem  *(~10% of lecture)*

[How do we infer Earth structure from observations? Even if brief, always present.
State: what we measure, what we want to know, what assumptions connect them,
and what limits uniqueness.]

:::{admonition} Inverse Problem Setup
:class: tip
- **Data (d):** [what is measured]
- **Model (m):** [what we want to infer]
- **Forward relation:** $d = G(m)$ where $G$ is [describe]
- **Key non-uniqueness:** [why the solution is not unique]
- **Resolution limit:** [what spatial/depth scale is resolvable]
:::

---

## 6. Worked Example  *(~10% of lecture)*

[Tie to a specific, concrete calculation. Numerical values. Reference lab if applicable.]

:::{admonition} Concept Check
:class: tip
1. [Question requiring application of section 3 or 4]
2. [Question requiring interpretation — connects observation to model]
3. [Question probing a common misconception]
:::

---

## 7. Course Connections

[Explicit links to other ESS 314 lectures and labs. Use bullet points.]

- **Prior lectures:** [what physical foundations this builds on]
- **Future lectures:** [what this enables — be specific]
- **Companion lab:** [Lab N — what students will compute or observe]
- **Cross-topic link:** [connection across geophysics methods, e.g., seismic ↔ gravity ↔ magnetics]

---

## 8. Research Horizon  *(new section — always required)*

[3–5 paragraph section. Based on open-access literature from the past 3 years (2022–2025).
Covers: what is actively being researched in this area, what methods are being pushed,
what open questions remain. This is the "5-minute Google Scholar search" section.
Every claim must cite an open-access paper or preprint. DO NOT make up citations.
Write for a student who wants to pursue graduate research in this area.]

:::{admonition} Current Research Highlights (2022–2025)
:class: seealso

**[Theme 1]:** [2–3 sentences on an active research direction with open-access citation]

**[Theme 2]:** [2–3 sentences, different angle]

**[Theme 3 — AI/ML if applicable]:** [ML applications in this domain with citation]

*For students interested in graduate research: [1–2 sentences on where to look for entry points —
key groups, open datasets, open software, relevant workshops like EarthScope SSBW]*
:::

---

## 9. Societal Relevance  *(new section — always required)*

[1–2 paragraphs. Concrete connection to real-world problems students care about.
At least one of: hazard, climate, energy, environment, policy, public health.
Include a specific example — a real event, a real application, a real stakeholder.
This is the hook for independent learning and career awareness.]

:::{admonition} Why It Matters Beyond the Classroom
:class: note

**[Application domain, e.g., Earthquake Hazard in the Pacific Northwest]:**
[2–3 sentences. What specific societal problem does this lecture's physics address?
Who uses this knowledge and how? What decisions does it inform?]

**For further exploration:** [1–2 open-access resources a student can follow up with independently —
USGS page, EarthScope animation, news article, agency report]
:::

---

## AI Literacy

[See `references/ai_literacy_templates.md`. Choose the most fitting category.
Required: at least one template per lecture. Include a Prompt Lab whenever possible.]

---

## Further Reading

[Open-access only. Minimum 4 references. Format: Author(s), Year. *Title*. Source. DOI/URL]

*Textbook:* Lowrie & Fichtner (2020), §N.N–N.N. Free via UW Libraries.  
*MIT OCW:* ...  
*IRIS/EarthScope:* ...  
*Open-access paper:* ...  

## References

[BibTeX keys — `@lowrie2020`, `@stein2003`, `@mitocw_12201`, etc.]
```

---

## Phase 4: Figure Handling

Every figure needs one of these dispositions. Decide during the audit.

### Option A — Python Regeneration ✅ preferred

Write `assets/scripts/fig_DESCRIPTION.py`. Required docstring:

```python
"""
fig_DESCRIPTION.py

Scientific content: [what the figure shows]

Reproduces the scientific content of:
  [Full citation: Author(s), Year. Title. Journal/Source. DOI/URL]

Output: assets/figures/fig_DESCRIPTION.png
License: CC-BY 4.0 (this script)
"""
# Colorblind-safe palette — WCAG AA compliant:
# #0072B2 (blue), #E69F00 (orange), #56B4E9 (sky), #009E73 (green),
# #F0E442 (yellow), #D55E00 (vermilion), #CC79A7 (pink), #000000 (black)
```

Cite in figure directive:
```markdown
:::{figure} ../../assets/figures/fig_DESCRIPTION.png
:name: fig-label
:alt: [Full alt text conveying scientific meaning WITHOUT the image]
:width: 75%
**Figure N.M.** Caption conveying full scientific meaning independently.
[Python-generated. Script: `assets/scripts/fig_DESCRIPTION.py`]
:::
```

### Option B — AI Image Generation (conceptual/illustrative figures)

```markdown
:::{admonition} Figure Replacement Needed
:class: warning
**Original source:** [Full citation with DOI/URL]
**Scientific content:** [Precise description of what must be shown]
**AI generation prompt:**
> "[Detailed prompt: geometry, labels, style, color scheme, no text unless specified,
>  white background, scientific illustration style]"
:::
```

### Option C — Open-Licensed Figure ✅ cite and use

If CC-BY, CC0, or public domain: include directly with caption attribution.
Format: `Source: [Author, Year, License, URL]`

---

## Phase 5: Write the Marp Slide Deck  *(required deliverable — every lecture)*

Output path: `slides/weekWW/lecture_NN_slides.md`

The Marp slide deck is a **required companion deliverable** for every lecture. It is not a summary of the `.md` file — it is the in-class presentation vehicle. Generate it immediately after the lecture markdown.

### File Header (copy verbatim, fill placeholders)

```markdown
---
marp: true
theme: uncover
html: true
paginate: true
backgroundColor: '#ffffff'
style: |
  section {
    font-family: 'Helvetica Neue', Arial, sans-serif;
    font-size: 26px;
    color: #1a1a1a;
  }
  section.title-slide {
    background-color: #003366;
    color: white;
  }
  h1 { font-size: 1.6em; }
  h2 { font-size: 1.3em; color: #0072B2; }
  img { border-radius: 4px; }
  .caption { font-size: 0.65em; color: #666; margin-top: 4px; }
---
```

### Required Slide Sequence

**Slide 1 — Title (class: title-slide)**
```markdown
<!-- _class: title-slide -->
# [Lecture Title]
### ESS 314 Geophysics · University of Washington
#### Week W, Lecture N · [Date]
```

**Slide 2 — Learning Objectives (always slide 2)**
```markdown
# By the end of this lecture…
- **[LO-W.1]** [verb] [concept]
- **[LO-W.2]** ...
- **[LO-W.3]** ...
```

**Slides 3–N — Pedagogical Arc**
Follow the same arc as the lecture `.md`:
motivation → governing physics → math → forward problem → inverse problem → worked example → connections → societal relevance

**Final slide — Concept Check**
```markdown
# Concept Check
1. [Application question — requires calculating or applying a formula]
2. [Interpretation question — connects data to model]
3. [Critical thinking question — tests an assumption]
```

---

### Embedding Python-Generated and AI-Generated Figures

**Rule:** Every figure in the slide deck must come from one of these three sources — no screenshots, no paywalled captures.

#### Source A — Python-generated figures (assets/figures/)
Reference by **relative path from the slides directory**:
```markdown
![alt text: [full scientific description of what the figure shows]](../../assets/figures/fig_DESCRIPTION.png)
<span class="caption">Figure N: [caption]. Python-generated — `assets/scripts/fig_DESCRIPTION.py`</span>
```

#### Source B — AI-generated figures (assets/figures/ai_gen/)
Same path convention, note the source in the caption:
```markdown
![alt text: [description]](../../assets/figures/ai_gen/fig_DESCRIPTION.png)
<span class="caption">Figure N: [caption]. AI-generated illustration — prompt logged in `assets/scripts/fig_DESCRIPTION_prompt.md`</span>
```

#### Source C — Open-licensed figures (CC-BY / CC0 / Public Domain) via URL
Embed directly via URL **only if** the figure's license is CC-BY, CC0, or Public Domain. Do NOT embed figures from paywalled journals even if the URL is accessible. Copernicus/EGU, USGS, NASA, NOAA, and Wikimedia Commons are safe sources.
```markdown
![alt text: [description]](https://doi.org/STABLE_FIGURE_URL)
<span class="caption">Source: Author et al., Year, *Journal*, CC BY 4.0. DOI: [doi]</span>
```

**Verification rule before embedding a URL figure:**
1. Confirm the article is published under CC-BY (check "This article is distributed under the terms of…" in the paper)
2. Confirm the URL is a stable direct image link (e.g., Copernicus figure URLs are stable; CDN URLs may not be)
3. If in doubt, download and save to `assets/figures/` with attribution metadata in a companion `.txt` file

---

### Background Image Slides

Use background images for motivating/context slides (e.g., opening geoscience question, societal relevance). Apply a **50% dark overlay** so body text remains readable against any image.

#### Template — NASA / USGS / Wikimedia public domain image
```markdown
---
<!-- NASA ISS Earth photo — Public Domain, no attribution required -->
<!-- Source: https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS042&roll=E&frame=294596 -->
backgroundImage: url('https://assets.science.nasa.gov/dynamicimage/assets/science/esd/eo/images/imagerecords/86000/86041/iss042e294596.jpg?w=1280&h=853&fit=clip&crop=faces%2Cfocalpoint')
backgroundSize: cover
---
<style scoped>
section {
  background: rgba(0, 0, 0, 0.50);
  color: white;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
}
h1, h2 { color: white; }
</style>

# [Slide Title]
[1–2 lines of text max on a background image slide]
```

**NASA image policy:** Images from `nasa.gov`, `eol.jsc.nasa.gov`, and `earthobservatory.nasa.gov` are U.S. Government works in the public domain. No license required; attribution is courteous.

**Other approved background image sources (all public domain or CC0):**
- USGS: `usgs.gov` (public domain)
- NOAA: `noaa.gov` (public domain)
- NASA Earth Observatory: `earthobservatory.nasa.gov` (public domain)
- Wikimedia Commons: filter by CC0 or Public Domain
- ESA: `esa.int` — check per image (many are CC BY-SA)

**The 50% overlay rule is mandatory** for any background image with body text. Use `rgba(0,0,0,0.50)` for dark images and `rgba(255,255,255,0.55)` for light images where dark text is preferred.

---

### Marp Slide Design Rules

- **≤5 bullet points per slide.** Prefer 3. If you need more, split the slide.
- **One idea per slide.** Equations get their own slide; figures get their own slide.
- **Equations:** Use inline `$...$` or display `$$...$$` — Marp renders KaTeX.
- **Font size floor:** Never below 22px effective. Captions may be 16px minimum.
- **Color:** Use the WCAG AA colorblind-safe palette for any in-slide colored elements: `#0072B2`, `#E69F00`, `#56B4E9`, `#009E73`, `#D55E00`, `#CC79A7`, `#000000`.
- **Alt text on every image:** Required. Written as the `![alt text]` field. Must convey scientific meaning without the image.
- **Max slides per lecture:** 25. If you're over, merge or cut — do not create dense text slides.

### Quality Gate Addition for Slide Deck

Add these checks to the Phase 5 deliverable before outputting:
```
[ ] Slide 1: title + course info
[ ] Slide 2: learning objectives (LO tags present)
[ ] Final slide: Concept Check with 3 questions
[ ] Every figure: relative path (assets) or verified CC-BY/PD URL
[ ] Every figure: alt text present
[ ] Background image slides: 50% overlay applied, text readable
[ ] No slide exceeds 5 bullet points
[ ] All equations KaTeX-compatible (no \eqref — use plain labels)
[ ] Total slides ≤ 25
[ ] Slide deck file saved to slides/weekWW/lecture_NN_slides.md
```

---

## Equation Standards

- Inline: `$...$` | Display: `$$...$$` with `(eq:label)` | Reference: `{eq}\`eq:label\``
- All variables defined in a **Notation** table **before** first use
- Scalars: $u$ | Vectors: $\mathbf{u}$ | Tensors: $\boldsymbol{\sigma}$
- Show ALL intermediate steps — never skip from assumption to result
- Every display equation: explicitly check units in the text immediately after
- Key equations in `:::{admonition} Key Equation\n:class: important` with plain-language interpretation

---

## Syllabus Alignment Rules

Before writing, assign each lecture to syllabus LOs and LO-OUTs. Then verify these are PRACTICED (not just mentioned) in the lecture:

| LO | How it's practiced |
|----|--------------------|
| LO-1 | Section 1 (geoscientific question) ties observation to physical process |
| LO-2 | Section 3 (math framework) applies model to predict observable |
| LO-3 | Section 5 (inverse problem) explicitly sets up d=G(m) |
| LO-4 | Section 4 or 6 discusses assumptions and limitations |
| LO-5 | Companion notebook reference; worked example with numbers |
| LO-6 | Concept Check questions require written interpretation |
| LO-7 | AI Literacy section (mandatory) |

---

## Research Horizon Protocol

The §8 Research Horizon is not optional. Here's how to write it:

1. **Search** (before writing): `web_search("[topic] review 2022 2024 open access")` — find 2–3 recent open-access papers or preprints. Record DOIs.
2. **Topics to always cover** (mix as appropriate):
   - New observational datasets or instrumentation (DAS, OBS, dense arrays)
   - Machine learning applications in this subdomain
   - Unresolved physical questions in current literature
   - Connections to climate, hazard, or planetary science if present
3. **Format**: Named subsections in the admonition box. Each has a citation.
4. **Student pointer**: End with a specific entry point (workshop, open dataset, open software).

Key open-access resources to mine for research horizon content:
- `seismosoc.org/publications/srl/` — Seismological Research Letters (open access articles)
- `agupubs.onlinelibrary.wiley.com/journal/21699291` — JGR Solid Earth (check OA)
- `earth-planets-space.springeropen.com` — Earth Planets Space (fully OA)
- `se.copernicus.org` — Solid Earth (EGU, fully OA)
- `gji.oxfordjournals.org` — GJI (check individual OA articles)
- `arxiv.org/list/physics.geo-ph/recent` — preprints

---

## Societal Relevance Protocol

The §9 Societal Relevance section must be concrete, not vague. Rules:

- Name a specific event, community, or decision (not "earthquakes can be dangerous")
- Connect to the Pacific Northwest when possible (Cascadia subduction zone, Seattle basin, volcanic arc)
- Draw from: USGS hazard assessments, PNSN (Pacific Northwest Seismic Network), DOGAMI, WA EMD
- Cover at least one non-hazard application per module (resource exploration, climate monitoring, infrastructure)
- End with something a student can do today: a website to visit, a map to explore, a dataset to download

---

## AI Literacy Integration

Every lecture requires one section. Read `references/ai_literacy_templates.md` for templates.
Choose from:

1. **AI as a Tool** — ML/AI actively deployed in this subdomain (e.g., phase picking, fault detection)
2. **AI as a Reasoning Partner** — prompting strategies for derivations and concept-checking
3. **AI Epistemics** — when to trust AI-generated geoscience content; failure modes
4. **Prompt Lab** — 2–3 student-facing prompts with evaluation criteria (always include one per chapter)

Tie AI literacy to LO-7 explicitly: students should see AI as part of scientific workflow, with documented, critically evaluated use.

---

## Accessibility Checklist

- [ ] Every figure: `:alt:` text conveys meaning without seeing the image
- [ ] No color-only information (use shape/pattern/label as secondary encoding)
- [ ] All Python figures: colorblind-safe palette (WCAG AA — see color codes above)
- [ ] Figure captions: scientifically complete as standalone text
- [ ] Equations: all variables defined, units explicit
- [ ] No screenshots of copyrighted figures

## Copyright Checklist

- [ ] No verbatim text from paywalled sources
- [ ] Every figure: Python-generated | AI-generated (prompt logged) | Open-licensed (CC noted)
- [ ] All citations: full reference with DOI or URL
- [ ] Open-access alternatives found and used for every key concept

---

## Quality Gate — Run Before Delivering

```
[ ] Slides fully read before writing
[ ] Open-access source research completed (≥4 sources found and recorded)
[ ] Slide audit produced and includes copyright inventory
[ ] Syllabus LOs and LO-OUTs mapped (≥2 each)
[ ] Learning objectives stated (3–5, ≥1 at Analysis level or above per Bloom's)
[ ] All 9 sections present (including §8 Research Horizon, §9 Societal Relevance)
[ ] Notation table present, all variables defined before use
[ ] All equations LaTeXed, labeled, with unit check
[ ] Forward problem and inverse problem both addressed
[ ] All figures: Python-gen OR AI-gen prompt OR open-license verified
[ ] AI literacy section present and tied to LO-7
[ ] §8: ≥2 citations to open-access papers from 2022–2025 (verified DOIs)
[ ] §9: specific PNW or real-world example, specific follow-up resource
[ ] Accessibility: alt text + colorblind-safe palette
[ ] Further Reading: ≥4 open-access references with DOIs/URLs
[ ] Cross-reference to companion notebook and lab
[ ] Marp slide deck generated (slides/weekWW/lecture_NN_slides.md)
[ ] Slide deck: all figures use relative paths (assets/) or verified CC-BY/PD URLs
[ ] Slide deck: background image slides use 50% rgba overlay
[ ] Slide deck: ≤25 slides, ≤5 bullets/slide, alt text on every image
```

---

## Slide Render Pipeline

Marp `.md` files must be compiled to HTML before they can be served from JupyterBook or GitHub Pages. This section defines the canonical build process for the course repo.

### Dependencies

Add to `pixi.toml` under `[tool.pixi.tasks]` and `[dependencies]`:

```toml
[dependencies]
nodejs = ">=18"

[tool.pixi.tasks]
install-marp = "npm install -g @marp-team/marp-cli"
slides-html  = "marp --html --theme slides/ess314.css --output-dir slides/html slides/**/*_slides.md"
slides-pdf   = "marp --pdf --theme slides/ess314.css --output-dir slides/pdf  slides/**/*_slides.md"
build-all    = { depends_on = ["slides-html", "build-book"] }
```

Or for conda users, document in `environment.yml`:
```yaml
  - nodejs>=18        # for npm / marp-cli
```

After `pixi install` (or `conda activate ess314`), run once:
```bash
npm install -g @marp-team/marp-cli
```

Verify: `marp --version`

### CSS Theme File

Every slide deck uses `slides/ess314.css` as its shared theme. Keep this file in the repo root of `slides/`. The Marp file header references it via:
```yaml
theme: ess314
```
and the CLI flag `--theme slides/ess314.css` resolves it at build time.

**Canonical `slides/ess314.css`:**

```css
/* ESS 314 Geophysics — Marp custom theme
   WCAG AA colorblind-safe palette throughout
   Requires: Marp CLI >= 3.x                   */

@import 'default';

:root {
  --uw-purple:  #4B2E83;
  --uw-gold:    #E8D078;
  --deep-blue:  #0072B2;
  --text-dark:  #1a1a1a;
  --text-light: #ffffff;
  --caption:    #555555;
}

section {
  font-family: 'Helvetica Neue', Arial, sans-serif;
  font-size: 26px;
  color: var(--text-dark);
  padding: 48px 64px;
  background-color: #ffffff;
}

h1 {
  font-size: 1.55em;
  color: var(--deep-blue);
  border-bottom: 2px solid var(--deep-blue);
  padding-bottom: 6px;
  margin-bottom: 0.6em;
}

h2 { font-size: 1.25em; color: #333; }

strong { color: var(--deep-blue); }

table { font-size: 0.85em; }

.caption {
  font-size: 0.62em;
  color: var(--caption);
  margin-top: 4px;
  display: block;
}

/* ── Title slide ─────────────────────────────── */
section.title-slide {
  background-color: var(--uw-purple);
  color: var(--text-light);
  display: flex;
  flex-direction: column;
  justify-content: center;
}
section.title-slide h1,
section.title-slide h2,
section.title-slide h3 { color: var(--text-light); border: none; }

/* ── Background-image slides ─────────────────── */
/* Apply .bg-overlay to any slide with a photo background.
   The CSS pseudo-element creates the 50% dark veil so text
   remains readable regardless of image brightness.          */
section.bg-overlay {
  position: relative;
  color: var(--text-light);
}
section.bg-overlay::before {
  content: '';
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.50);
  z-index: 0;
}
section.bg-overlay > * { position: relative; z-index: 1; }
section.bg-overlay h1,
section.bg-overlay h2,
section.bg-overlay p { color: var(--text-light); text-shadow: 1px 1px 3px rgba(0,0,0,0.7); }

/* ── Two-column layout ───────────────────────── */
.columns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2em;
}

/* ── Pagination ──────────────────────────────── */
section::after {
  font-size: 0.7em;
  color: #999;
}
```

### Background Image Slide Pattern

**Exact template** for any slide that uses a public-domain photo background with 50% overlay:

```markdown
---
<!-- Photo: NASA ISS042-E-294596, public domain — no attribution required -->
<!-- https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS042&roll=E&frame=294596 -->
_class: bg-overlay
backgroundImage: "url('https://assets.science.nasa.gov/dynamicimage/assets/science/esd/eo/images/imagerecords/86000/86041/iss042e294596.jpg?w=1280&h=853&fit=clip&crop=faces%2Cfocalpoint')"
backgroundSize: cover
---

# Slide Title
One or two lines of body text maximum on a photo background.
```

Key points:
- `_class: bg-overlay` activates the CSS `::before` pseudo-element overlay — no inline `<style scoped>` needed
- `backgroundImage` is set in the slide front matter — Marp renders this natively
- `backgroundSize: cover` ensures the image fills the slide regardless of aspect ratio
- The `::before` overlay in `ess314.css` handles the 50% transparency uniformly across all photo slides
- Use `rgba(0,0,0,0.50)` for dark overlay; change to `rgba(255,255,255,0.55)` in the CSS for slides where light overlay with dark text is preferred

### Build and Serve

```bash
# Build all slides to HTML (run from repo root)
pixi run slides-html
# → outputs to slides/html/lecture_NN_slides.html

# Or run marp directly for a single file:
marp --html --theme slides/ess314.css slides/week01/lecture_01_slides.md

# Serve locally to preview
npx @marp-team/marp-cli --preview slides/week01/lecture_01_slides.md
```

### JupyterBook Integration

Commit all `slides/html/*.html` files to the repo. JupyterBook serves them as static assets. Reference from lecture `.md` pages:

```markdown
:::{admonition} Lecture Slides
:class: tip
📊 [Open slide deck](../../slides/html/lecture_01_slides.html) — opens as a fullscreen HTML presentation.
Use arrow keys or spacebar to advance. Press `F` for fullscreen.
:::
```

Alternatively, embed inline with a raw HTML iframe:
````markdown
```{raw} html
<iframe src="../../slides/html/lecture_01_slides.html"
        width="100%" height="520px"
        style="border:1px solid #ddd; border-radius:6px;">
</iframe>
```
````

### GitHub Actions Integration

Add to `.github/workflows/deploy-book.yml` before the `jupyter-book build` step:

```yaml
    - name: Install Marp CLI
      run: npm install -g @marp-team/marp-cli

    - name: Build slide decks to HTML
      run: |
        for f in slides/week*/*_slides.md; do
          marp --html --theme slides/ess314.css "$f"
        done
```

This ensures GitHub Pages always serves the latest compiled HTML alongside the JupyterBook.

---

## Reference Files

Read these when indicated:
- `references/ai_literacy_templates.md` — Four AI literacy templates with geophysics examples
- `references/open_source_registry.md` — Curated registry of open-access sources by topic
- `references/myst_cheatsheet.md` — MyST Markdown / JupyterBook syntax quick reference
- `references/syllabus_lo_matrix.md` — Full LO-to-lecture mapping matrix for ESS 314
