---
marp: true
theme: ess314
paginate: true
header: "ESS 314 · Lecture 10 · 4/27/2026"
footer: "From Travel Times to Images · Migration & Velocity–Image Duality"
math: katex
---

<!-- _class: title -->

# From Travel Times to Images
## Migration and the Unity of Active-Source Seismology

**ESS 314 — Introduction to Geophysics**
Lecture 10 · Monday 4/27/2026
Marine Denolle · University of Washington

---

## Learning objectives

By the end of this lecture, students will be able to:

- Derive the zero-offset migration shifts $\Delta x = d\sin\theta$ and $\tau = t\cos\theta$
- State the exploding-reflector analogy and its failure modes
- Describe the Kirchhoff forward–migration adjoint pair
- Diagnose whether a migration velocity was correct, too slow, or too fast from the image
- Articulate where deep learning serves as a surrogate for a physics-based operator — and what it does not replace

Tagged: **LO-1, LO-2, LO-3, LO-4, LO-5, LO-7**

---

## One shot, two methods

![w:1000 One shot gather contains refractions (straight lines) and reflections (hyperbolas) — two views of the same Earth model v(x,z)](../assets/figures/fig_integrated_shot_gather.png)

CASIE-21 (Cascadia, 2021) records reflections on the streamer and refractions on the OBS — **one acquisition, one Earth, two data modes**.

---

## Why dipping reflectors are mispositioned

![w:950 Left: earth cross-section — dipping reflector, actual normal ray (vermilion, perpendicular to reflector) vs. assumed vertical path (pink dashed). Right: zero-offset time section, migration shift arrow from apparent to true position.](../assets/figures/fig_migration_mispositioning.png)

Four-step reasoning → **the instrument records only $t = 2d/v$, nothing about direction**.

---

## The mispositioning chain — step by step

1. **What is recorded:** round-trip time $t = 2d/v$ — no directional information
2. **Why the ray is not vertical:** law of reflection + zero offset → the only returning ray hits the reflector at **90°** (the *normal ray*). If the reflector dips at $\theta$, the ray travels at $\theta$ off vertical
3. **The wrong assumption:** the display plots the event **straight below** $S$ at depth $d$ — as if the ray were vertical
4. **Two errors result:**
   - Horizontal: true point $R$ is **updip** of plotted point $C$ by $\Delta x = d\sin\theta$
   - Vertical: $R$ is **shallower** — true depth $d\cos\theta < d$

Both errors vanish for flat reflectors ($\theta = 0$). **Migration** corrects both.

---

## Hand migration: the kinematic shifts

Two-way time from the normal ray:

$$ d = \frac{v\,t}{2} $$

Horizontal shift and vertical compression:

$$ \Delta x = \frac{v^2 p_0\, t}{4}, \qquad \tau = t\sqrt{1 - \frac{v^2 p_0^2}{4}} $$

- $p_0 = \partial t/\partial y$ is the **slope of the event** on the unmigrated section
- $\sin\theta = v\,p_0/2$ is **Snell's parameter with the round-trip factor of two**
- Hand migration: apply to each event segment independently

---

## The "powerful analogy": exploding reflectors

![w:1000 Left panel shows real zero-offset experiment with waves going down and up at velocity v. Right panel shows the thought experiment: reflectors explode at t=0, waves travel only upward at velocity v/2, and are recorded by a surface array.](../assets/figures/fig_exploding_reflector.png)

**Thought experiment:** reflectors explode at $t=0$; upgoing waves at $v/2$
One hypothetical wavefield, not thousands of shots

---

## When the analogy breaks

The exploding-reflector analogy is **kinematically exact for primary reflections at non-critical angles in a constant-velocity medium**. It fails for:

- **Multiples.** Sea-floor multiple arrives at $2t_1$ in reality, $3t_1$ in the model
- **Lateral velocity variations.** Laterally-bent rays are not reproduced by an upgoing-only wavefield
- **Polarity.** A true reflection flips sign between waves approaching from above and below; the exploding reflector does not

Reverse-time migration and one-way wave-equation migration extend beyond these limits — at higher computational cost.

---

## The Kirchhoff adjoint pair

![w:1000 Four-panel figure. Top row: a point at depth spreads into a hyperbola in the data. Bottom row: an impulse in the data is consistent with an entire semicircle of scatterers in the earth.](../assets/figures/fig_kirchhoff_adjoint_pair.png)

Forward modeling and migration are **transposes** of each other.
Same geometric curve, copy direction reversed.

---

## One loop, two operations

```text
for every (ix, iz) in the model:
  for every midpoint x' in the data:
    t = sqrt( (2 z[iz]/v)^2 + (2 (x[ix] - x')/v)^2 )
    if flag == "forward":  data[t, x']      += model[iz, ix]
    else:                  model[iz, ix]    += data[t, x']
```

- **Forward (diffraction):** spreads a scatterer into its hyperbola
- **Adjoint (migration):** sums along the hyperbola back to the scatterer

*Source:* {cite:t}`Claerbout2010`, subroutine `kirchslow`, Chapter 5.

---

## The migration image depends on velocity

$$ m(x,z) = \sum_{x'} w\cdot d\!\left(x',\ \sqrt{\left(\tfrac{2z}{v}\right)^2 + \left(\tfrac{2(x - x')}{v}\right)^2}\right) $$

Migration integrates data along a **hyperbola whose shape depends on $v$**.

- Right $v$ → right hyperbola → **energy collapses to a point**
- Wrong $v$ → wrong hyperbola → **energy left behind as residual**

The image is **the velocity diagnostic**.

---

## Correct, too slow, too fast

![w:1000 Four-panel migration experiment. Top left: zero-offset data with overlapping diffraction hyperbolas. Top right: migration with correct velocity, three focused points and a straight dipping segment. Bottom left: migration too slow, points left as downward frowns. Bottom right: migration too fast, points smeared into upward smiles.](../assets/figures/fig_velocity_image_duality.png)

---

## Reading the residuals

| Migration velocity | Image signature | Name |
|---|---|---|
| Correct | diffractions collapse to points | focused |
| Too slow | residual arcs opening downward | **frowns** (under-migrated) |
| Too fast | residual arcs opening upward | **smiles** (over-migrated) |

Frowns and smiles are the operational basis of **migration velocity analysis** — iterate until the image is focused.

---

## Concept check

A marine reflection hyperbola has apex at $(x = 5\text{ km},\ t_0 = 2.0\text{ s})$.

1. After migration with $v = 2.5$ km/s the hyperbola collapses to a point at $z = 2.5$ km.
2. After migration with $v = 3.0$ km/s the point becomes an **upward-curving** arc.

Which velocity is more nearly correct, and how can you tell?
What would $v = 2.0$ km/s produce?

*Discuss with your neighbor. Write your answer on the index card.*

---

## Why neither method works alone

| | Refraction (Lecs 6–7) | Reflection (Lecs 8–9) |
|---|---|---|
| **Wave type** | Head waves (first arrivals) | Reflected waves (later arrivals) |
| **Measures** | Absolute velocities $v_1, v_2, \ldots$ | Stacking velocity $V_{\rm rms}(t_0)$ |
| **Depth range** | Surface → deepest refractor (~1–5 km) | Any depth with impedance contrast |
| **Strength** | Accurate absolute $v$; robust | Structural detail at all depths |
| **Blind spot** | Can't see below deepest refractor; misses LVZs | Velocities relative, not absolute; near-surface errors propagate down |

**Refraction anchors the velocity; reflection reveals the structure.**
Migration fuses both and tests whether the combined model is correct.

---

## The unified processing checklist

| Step | Action | Method | Product |
|:---:|--------|--------|--------|
| **1** | Pick first breaks | Refraction | $t_{\rm fb}(x)$ |
| **2** | Invert first arrivals | Refraction tomography | Shallow $v_{\rm refr}(x,z)$ |
| **3** | Pick NMO velocities | Reflection | $V_{\rm rms}(t_0)$ |
| **4** | Dix equation | Reflection | Interval $v_{\rm int}(t_0)$ |
| **5** | Stitch models | Both | Initial $v_0(x,z)$ |
| **6** | Migrate | Kirchhoff sum | Image $\hat{\mathbf{m}}_0$ |
| **7** | Diagnose | Velocity QC | Frowns / smiles / flat |
| **8** | Update $v$, re-migrate | Iterate 6→7→8 | Focused image |

Every active-source imaging workflow — academic or industrial — is a variant of this loop.
In CASIE-21, OBS first arrivals (Step 2) anchored the migration (Step 6).

---

## The Cascadia hook

- CASIE-21 (2021): 15-km streamer + OBS, Nootka to Mendocino
- Same airgun shots recorded as reflections **and** refractions
- Plate interface lies $5$–$25$ km below seafloor — too deep for direct observation, too shallow to ignore
- Image geometry controls: locked-zone mapping, tsunami forecasts, M9 rupture modeling

Project overview: <https://casie21.weebly.com/>

---

## Deep learning in the processing chain — three examples

- **First-break picking.** U-Net pretrained on ImageNet, fine-tuned on <10 % of hand-picked shots {cite:p}`Mardan2024`
- **Shot-gather denoising.** Self-supervised U-Net that removes non-Gaussian noise without clean training labels {cite:p}`LiTradLiu2024`
- **Velocity model building.** Encoder–decoder that maps raw shot gathers → $v(x,z)$ in one pass {cite:p}`YangMa2019`

Each network is a **surrogate** for an operator the physics already defines.

---

## Accelerators, not replacements

Every surrogate requires training data that only exist *because* the physics exists:

- Mardan's U-Net needs hand-picked first breaks from experts who understand intercept times
- Li's denoiser needs a signal/noise statistical model grounded in wave propagation
- Yang & Ma's network is trained on $(v, \text{gather})$ pairs produced by a finite-difference wave-equation solver

**The physics is upstream of the data. The data is upstream of the network. Remove the physics and the training data disappears.**

---

## AI literacy — the question to ask

When a paper reports a neural network for an imaging task, the student of geophysics asks:

1. **What operator** does the network replace?
2. **What data trained it**, and **who produced those data**?
3. **What is the training distribution**, and does the evidence in the paper justify deployment outside it?

These are the same epistemic questions one asks of any surrogate model — regression, empirical formula, or neural network. Deep learning changes the technology, not the questions.

---

## Tying it together

- Migration and modeling are **transposes** of each other (Kirchhoff `adj=0` vs `adj=1`)
- The migrated image **depends on velocity**; wrong velocity leaves residual curvature
- **Refraction + reflection + migration** are one iterative workflow to estimate $v(x, z)$
- Deep learning accelerates steps of this workflow; it does **not** replace the physics that produces the training data

---

## What to do for Lab 4

The lab notebook ships with a synthetic-data generator and a Kirchhoff migration routine (~30 lines of NumPy). Students will:

- Design a survey (from the Wednesday discussion section)
- Generate synthetic zero-offset data for a chosen velocity model
- Migrate with the **correct** velocity, **0.80×** the correct velocity, and **1.25×** the correct velocity
- Report which image is correct and **how they could tell from the image alone**

---

## Further reading

- Claerbout (2010). *Basic Earth Imaging*, Chapters 3–5. Open: <http://sepwww.stanford.edu/sep/prof/bei11.2010.pdf>
- Lowrie & Fichtner (2020), *Fundamentals of Geophysics*, Ch. 3 (UW Libraries)
- Zelt & Barton (1998). Refraction tomography, *JGR* 103, 7187–7210
- MIT OCW 12.510, migration lecture notes (CC BY-NC-SA)
- EarthScope/IRIS Active Source Resources: <https://www.earthscope.org/data/active-source/>

---

<!-- _class: end -->

## Questions?

Office hours: Tu/Th 3:00–4:00 pm · ATG 204
**Next lecture:** Whole Earth Structure I
**Lab 4:** Design → Simulate → Image
