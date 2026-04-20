---
title: "From Travel Times to Images: Migration and the Unity of Active-Source Seismology"
week: 4
lecture: 10
date: "2026-04-27"
topic: "Migration, velocity, and the reflection–refraction bridge"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4", "LO-5", "LO-7"]
learning_outcomes: ["LO-OUT-B", "LO-OUT-C", "LO-OUT-D", "LO-OUT-E", "LO-OUT-F", "LO-OUT-H"]
open_sources:
  - "Claerbout 2010, Basic Earth Imaging (Stanford Exploration Project, open)"
  - "Lowrie & Fichtner 2020 Ch. 3 (UW Libraries)"
  - "MIT OCW 12.510 Introduction to Seismology"
  - "EarthScope/IRIS Active Source Educational Materials"
---

# From Travel Times to Images: Migration and the Unity of Active-Source Seismology

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_10_slides.html" target="_blank">open in new tab ↗</a>
:::

::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-10.1]** Explain why a zero-offset seismic section mispositions dipping reflectors, and derive the geometric corrections $\Delta x = d\sin\theta$ and $\tau = t\cos\theta$.
- **[LO-10.2]** State the exploding-reflector analogy, explain why it requires the propagation velocity to be halved, and identify two situations in which it breaks down.
- **[LO-10.3]** Describe the Kirchhoff adjoint pair — that forward modeling spreads a scatterer into a data-space hyperbola, while migration sums data along the same hyperbola back into model space — and use this to explain why modeling and migration are transposes of each other.
- **[LO-10.4]** Argue from a migrated image whether the migration velocity was correct, too slow, or too fast, using the geometry of residual curvature.
- **[LO-10.5]** Diagram how refraction (first-arrival tomography) and reflection (NMO/migration) imaging share a single Earth model $v(x,z)$, and articulate how each method constrains a different part of it.
- **[LO-10.6]** Identify one task in the active-source processing chain where deep learning provides a useful surrogate, and state explicitly what physical knowledge was required to produce the surrogate's training data.

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1, LO-2, LO-3, LO-4, LO-5, LO-7 |
| **Learning outcomes practiced** | LO-OUT-B (compute travel times), LO-OUT-C (explain physical why), LO-OUT-D (set up inverse problem), LO-OUT-E (interpret residuals), LO-OUT-F (choose methods), LO-OUT-H (critique AI outputs) |
| **Prior lecture** | Lecture 9 — Seismic Reflections II (dipping layers, diffractions, AVO, noise filtering) |
| **Next lecture** | Lecture 11 — Whole Earth Structure I |
| **Lab connection** | Lab 4: Design → Simulate → Image — students build a synthetic dataset from their own survey design and migrate with correct and deliberately incorrect velocities |
| **Discussion connection** | Revisits the Discussion 2 survey-design theme (radar on ice) with a broader active-source survey-design checklist |

::::

## Prerequisites

Students should be comfortable with: ray geometry and Snell's law (Lecture 5); refraction head waves and intercept-time analysis (Lectures 6–7); reflection coefficients, normal moveout, and CMP stacking (Lectures 8–9); the hyperbolic travel-time curve $t(x) = \sqrt{t_0^2 + x^2/V_{\rm rms}^2}$.

---

## 1 — The Geoscientific Question

Off the Pacific Northwest coast, the Juan de Fuca plate dives beneath North America at the Cascadia subduction zone. The plate interface lies between about 5 and 25 km below the seafloor, and its geometry — where it is locked, where it is slipping, and how its properties change along strike — controls the size and location of the megathrust earthquakes that will eventually strike Washington, Oregon, and British Columbia. No borehole reaches this interface. Every constraint on its position and properties comes from seismic imaging.

In the summer of 2021, the CASIE-21 experiment towed a $15$-km hydrophone streamer behind the R/V *Marcus G. Langseth* along a set of long profiles off the Oregon and Washington coast, while ocean-bottom seismometers (OBS) recorded the same shots at larger offsets. One pass, one set of airgun shots, two datasets: a streamer record dominated by near-offset *reflections*, and an OBS record dominated by long-offset *refractions*. Both constrain the same Earth — the same $v(x,z)$ — but they emphasize different arrivals and different sensitivities.

```{figure} ../assets/figures/fig_integrated_shot_gather.png
:name: fig-integrated-shot-gather
:alt: Left panel: two-layer-over-halfspace Earth model with shot at x=0, receivers along the surface to 23 km offset, and ray paths drawn for a basement reflection (blue) and a head wave along the basement (green). Right panel: travel-time curves on the record section, showing a dashed black direct wave, a green straight-line head wave along the basement at v2 = 3.5 km/s, a blue reflection hyperbola from the basement with two-way zero-offset time 2.22 s, an orange reflection hyperbola from the Moho with t0 = 4.51 s, and a pink straight-line head wave below the Moho at v3 = 7.5 km/s.
:width: 100%

A single synthetic Cascadia-style shot gather contains both reflections (hyperbolas) and refractions (straight lines). The two event families are not separate experiments — they are two views of one Earth model $v(x,z)$.
```

A single shot gather in {numref}`fig-integrated-shot-gather` contains five distinct event families — a direct wave, two reflection hyperbolas, and two head waves. Prior lectures treated these separately: refraction in Lectures 6–7, reflection in Lectures 8–9. This lecture unifies them. The claim is simple: every method of active-source seismology is a strategy for turning travel-time data into an Earth model, and all of them share the same underlying problem — the *image* depends on the *velocity*, and the velocity is inferred from the same data.

---

## 2 — Governing Physics

### 2.1 The mispositioning problem

To understand why a zero-offset seismic section plots dipping reflectors in the wrong place, follow the chain of physical reasoning step by step.

**Step 1 — What the experiment actually records.** In a zero-offset survey, the source and receiver sit at the same surface location $S$. A seismic pulse travels down from $S$, bounces off the subsurface interface, and returns to $S$. The instrument records exactly one number from this round trip: the **two-way travel time** $t = 2d/v$, where $d$ is the total one-way path length and $v$ is the velocity. The instrument knows nothing about the direction the ray traveled.

**Step 2 — Why the ray travels at an angle.** The law of reflection requires the angle of incidence to equal the angle of reflection. For a zero-offset geometry (source = receiver), the only ray that departs from $S$ and returns to the same point $S$ is one that strikes the reflector at exactly 90° — the so-called **normal ray** (shown in vermilion in {numref}`fig-mispositioning`). If the reflector dips at angle $\theta$ from horizontal, this normal ray is not vertical — it travels at angle $\theta$ from the vertical, hitting the reflector at the true reflection point $R$ which lies *updip* and at a *shallower depth* than the point directly beneath $S$. The small right-angle square where the ray meets the reflector reminds us of this geometric constraint.

**Step 3 — The wrong assumption.** Because the recorder has no knowledge of ray direction, the conventional seismic display makes the simplest possible assumption: it plots the event **directly beneath the surface station** $S$, at a depth $z_{\rm apparent} = vt/2 = d$. This places the reflector at point $C$ in {numref}`fig-mispositioning` — straight below $S$ at the slant-path distance $d$.

**Step 4 — The two errors.** Comparing $C$ (where the event is plotted) with $R$ (where the reflection actually occurred) reveals two systematic errors:

- **Horizontal mispositioning**: $R$ lies updip of $C$ by a distance $\Delta x = d\sin\theta$. The event is plotted too far downdip.
- **Vertical mispositioning**: the true depth of $R$ is $z_R = d\cos\theta$, but $C$ is plotted at depth $d$. Because $\cos\theta < 1$ for any nonzero dip, the event is plotted **too deep** by a factor of $1/\cos\theta$.

Both errors vanish when $\theta = 0$ (a flat reflector): the normal ray *is* vertical, and the assumption is correct. The steeper the dip, the larger the mispositioning.

```{figure} ../assets/figures/fig_migration_mispositioning.png
:name: fig-mispositioning
:alt: Left panel: earth cross-section with a dipping reflector (blue), source-receiver S (orange triangle) at x = 1.5 km, the actual normal ray (vermilion, perpendicular to the reflector) of length d traveling at angle theta to the true reflection point R (star) at (2.10 km, 1.04 km), and the assumed vertical path (pink dashed) descending from S to the apparent position C (pink circle) at (1.5 km, 1.20 km depth). An italic annotation reads "Recorder knows only t = 2d/v; assumes ray went straight down." Right panel: zero-offset time section showing the unmigrated event as a blue line, the apparent position (pink circle) at (1.5 km, 1200 ms) and the correct migrated position (star) at (2.10 km, 1039 ms), with a migration-shift arrow connecting them and the equation tau = t cos theta.
:width: 100%

**Why zero-offset sections misposition dipping reflectors.** The instrument records only the round-trip time $t = 2d/v$ and has no information about ray direction. Plotted beneath $S$ at depth $d$ (pink dashed line → point C), the event ends up too deep and too far downdip. The true reflection point $R$ lies updip at a shallower depth ($z = d\cos\theta$). Migration corrects both errors: $\Delta x = d\sin\theta$ horizontally and $\tau = t\cos\theta$ vertically.
```

The operation that moves events from their apparent positions to their true positions is called **migration**. The name is historical: early interpreters using light tables literally moved reflection events on their unmigrated sections to where they calculated the reflections ought to be. Modern migration is performed numerically on millions of traces, but the kinematic problem it solves has not changed.

### 2.2 The exploding-reflector analogy

Zero-offset acquisition records thousands of separate field experiments — one shot for each source–receiver pair. Each shot sends a wave down to the reflector and receives the echo upward. {cite:t}`Claerbout2010` observed that all of these experiments are kinematically equivalent to a single thought experiment: imagine that every reflector in the Earth *explodes* simultaneously at $t = 0$ and the resulting upgoing wavefield is recorded by a receiver array at the surface. The ray paths are the same in both cases. The only difference is that in the real zero-offset experiment the wave travels down and back up, while in the exploding-reflector thought experiment it travels only up.

```{figure} ../assets/figures/fig_exploding_reflector.png
:name: fig-exploding-reflector
:alt: Left panel shows the real experiment: a dipping blue reflector, four orange source-receiver triangles on the surface, each with a vermilion down-and-up normal ray to the reflection point on the reflector. Italic text reads wave travels DOWN then UP, velocity v. Right panel shows the thought experiment: the same dipping reflector, a dense orange receiver array along the surface, faint green upgoing rays from points distributed along the reflector, and faint pink arcs representing upgoing wavefronts at two time snapshots. Italic text reads waves travel ONLY UP, velocity v/2.
:width: 100%

The exploding-reflector analogy. Real zero-offset data (left) and the hypothetical upgoing-wavefield experiment (right) produce identical wavefronts at the surface, provided the propagation velocity in the thought experiment is reduced by a factor of two.
```

To preserve travel times, the exploding-reflector model uses a propagation velocity equal to half the true Earth velocity. The factor of two accounts for the round-trip compression: in the real experiment, the ray travels a total distance $2d$ at velocity $v$; in the thought experiment, it travels $d$ at velocity $v/2$. The arrival times match.

The analogy is powerful because it collapses a multi-experiment acquisition into a single-experiment inverse problem. The question "what does the data look like?" becomes "what does one upgoing wavefield, sampled only at the surface, look like?" — and the tools of wave propagation and Fourier analysis can be brought to bear on that single wavefield.

:::{admonition} Key Concept — When the analogy breaks
:class: warning

The exploding-reflector analogy is kinematically exact for single-bounce reflections at non-critical angles in a constant-velocity medium. It fails for three important phenomena that real data frequently contain:

1. **Multiples.** A sea-floor multiple in real data arrives at time $2t_1$; the exploding-reflector model, with its v/2 and round-trip collapse, predicts $3t_1$.
2. **Lateral velocity variations.** Rays that bend laterally before reaching the reflector are not reproduced by an upgoing wavefield in an equivalent half-velocity medium.
3. **Reflection coefficient polarity.** The exploding reflector radiates the same polarity in all directions; a real reflection flips sign between waves approaching from above and below the interface.

Migration algorithms that go beyond the exploding-reflector model — notably full-wave reverse-time migration — do exist, but they are more expensive and conceptually more demanding.
:::

---

## 3 — Mathematical Framework

### 3.1 Notation

| Symbol | Meaning | Units |
|--------|---------|-------|
| $x, y$ | Surface coordinates (midpoint, crossline) | km |
| $z$ | Depth, positive downward | km |
| $t$ | Two-way travel time, zero-offset data space | s |
| $\tau$ | Two-way vertical travel time, $\tau = 2z/v$ | s |
| $v$ | Propagation velocity (Earth) | km/s |
| $\theta$ | Dip of reflector from horizontal | rad |
| $d$ | Length of normal ray from $S$ to $R$ | km |
| $\mathbf{d}$ | Data (observed zero-offset traces) | — |
| $\mathbf{m}$ | Model (reflectivity at each $(x,z)$) | — |
| $F$ | Forward modeling operator | — |
| $F^\top$ | Adjoint (migration) operator | — |

### 3.2 The hand-migration equations

Let the reflector at point $R$ have dip $\theta$, and let a zero-offset source–receiver pair at surface position $S$ record the reflected arrival at two-way travel time $t$. The length of the normal ray from $S$ to $R$ is

```{math}
:label: eq-d
d = \frac{v\,t}{2}.
```

From the geometry in {numref}`fig-mispositioning`, the true depth of $R$ beneath its true lateral position is

```{math}
:label: eq-z-cos
z = d\cos\theta,
```

and the true lateral position of $R$ is displaced from $S$ by

```{math}
:label: eq-deltax
\Delta x = d\sin\theta = \frac{v\,t}{2}\sin\theta.
```

Rewriting {eq}`eq-z-cos` in terms of the vertical two-way time $\tau = 2z/v$,

```{math}
:label: eq-tau
\tau = t\cos\theta.
```

Both the horizontal shift $\Delta x$ and the vertical compression $t \to \tau$ vanish when $\theta = 0$. Flat reflectors are plotted correctly by a simple $t \to z$ time-to-depth conversion; dipping reflectors require migration.

In practice, the dip $\theta$ is not known a priori — it is read from the local slope of the event on the zero-offset section,

```{math}
:label: eq-p0
p_0 = \frac{\partial t}{\partial y}.
```

The slope $p_0$ and the dip $\theta$ are related by

```{math}
:label: eq-tuchel
\sin\theta = \frac{v\,p_0}{2},
```

which is the zero-offset analogue of Snell's parameter $p = \sin\theta/v$ familiar from Lecture 5, with a factor of two for the two-way path. Substituting {eq}`eq-tuchel` into {eq}`eq-deltax` and {eq}`eq-tau` yields the hand-migration formulas

```{math}
:label: eq-hand-migration
\Delta x = \frac{v^2 p_0 t}{4}, \qquad
\tau = t\sqrt{1 - \frac{v^2 p_0^2}{4}}.
```

### 3.3 From hand migration to the Kirchhoff sum

Hand migration works on one event at a time, but real data contain crossing events, diffractions from edges and faults, and superimposed hyperbolas. What is needed is an operator that acts on the entire zero-offset section without first separating it into individual events.

The construction rests on two dual observations, illustrated in {numref}`fig-kirchhoff-adjoint`.

**Forward modeling (diffraction).** Place a single point scatterer at $(x_0, z_0)$ in the Earth model. In the exploding-reflector model with velocity $v/2$, the upgoing wavefront reaches the surface at a midpoint $x$ at time

```{math}
:label: eq-hyperbola-forward
t(x) = \sqrt{ \left(\frac{2 z_0}{v}\right)^2 + \left(\frac{2(x - x_0)}{v}\right)^2 }.
```

This is a hyperbola in $(x, t)$-space with apex at $(x_0,\ 2z_0/v)$. The forward operator $F$ takes a point in model space and spreads it along this hyperbola in data space. Any extended reflector is modeled as a superposition of such points, each contributing its own hyperbola.

**Migration (imaging).** Consider the dual question: a single data-space impulse at $(y_0, t_0)$. What Earth model could have produced it? Any scatterer lying on the semicircle

```{math}
:label: eq-semicircle
(x - y_0)^2 + z^2 = \left(\frac{v\,t_0}{2}\right)^2
```

would produce an arrival at $(y_0, t_0)$. The migration operator $F^\top$ therefore spreads a data sample over the corresponding semicircle in model space. Any extended event is imaged as a superposition of such semicircles.

```{figure} ../assets/figures/fig_kirchhoff_adjoint_pair.png
:name: fig-kirchhoff-adjoint
:alt: Four-panel figure arranged in two rows. Top row shows forward modeling. Panel a: earth model with a single orange-vermilion star scatterer at x0 = 2 km, z0 = 1 km, against a blank background. Panel b: zero-offset data showing a blue hyperbola opening downward from its apex at midpoint 2 km and time 1000 ms, with equation t equals square root of open bracket 2 z0 over v close bracket squared plus open bracket 2 open parenthesis x minus x0 close parenthesis over v close bracket squared. Bottom row shows migration. Panel c: data space with a single orange circular impulse at midpoint 2 km, time 1000 ms, on an otherwise blank time section. Panel d: earth model showing a sky-blue semicircle of radius 1 km centered on the surface at x = 2 km, with a pink dotted vertical line marking z = v t0 over 2 = 1 km.
:width: 100%

The Kirchhoff adjoint pair. A point scatterer spreads into a hyperbola in the data (top); conversely, a data impulse is consistent with an entire semicircle of possible scatterers in the Earth (bottom). Forward modeling and migration are transpose operations that act by copying data along the same kinematic curves in opposite directions.
```

These two operations are *adjoints* of one another. {cite:t}`Claerbout2010` gives a minimal implementation — subroutine `kirchslow` — that performs both with a single set of three nested loops, differing only by whether a copy flag points from model space to data space (forward modeling) or from data space to model space (migration). In pseudocode:

```text
for every (ix, iz) in the model:
    for every midpoint x' in the data:
        compute t = sqrt( (2*z[iz]/v)^2 + (2*(x[ix] - x')/v)^2 )
        if flag == "forward":  data[t, x'] += model[iz, ix]
        else:                  model[iz, ix] += data[t, x']
```

The geometry — the relationship between a point in the Earth and a hyperbola in the data — is the same in both directions. What changes is which index is written and which is read.

:::{admonition} Key Equation — Kirchhoff migration
:class: important

The Kirchhoff migration image at location $(x, z)$ is the weighted sum of data values along the hyperbola that would have been produced by a point scatterer at $(x, z)$:

```{math}
:label: eq-kirchhoff
m(x, z) = \sum_{x'} w(x, z, x')\, d\!\left(x',\ t(x, z, x')\right),
\quad \text{where}\quad
t(x, z, x') = \sqrt{\left(\tfrac{2z}{v}\right)^2 + \left(\tfrac{2(x - x')}{v}\right)^2}.
```

The weight $w$ accounts for geometrical spreading and is approximately $z/t \cdot t^{-1/2}$ for the tutorial implementation {cite:p}`Claerbout2010`.
:::

---

## 4 — The Forward Problem

Given a model $m(x, z)$ and a velocity $v$, the forward operator $F$ in equation {eq}`eq-hyperbola-forward` produces the predicted zero-offset section. {numref}`fig-velocity-image-duality`(a) shows the result for a toy Earth model consisting of three isolated point scatterers and a short dipping segment: each scatterer contributes one hyperbola, the dipping segment contributes a band of overlapping hyperbolas whose constructive interference traces out a straight line offset and rotated from the true reflector position.

```{figure} ../assets/figures/fig_velocity_image_duality.png
:name: fig-velocity-image-duality
:alt: Four-panel migration experiment using the same synthetic zero-offset data. Panel a in the top left shows the data as a grayscale image of hyperbolic diffraction patterns from three point scatterers plus a short dipping band of overlapping hyperbolas, displayed against two-way time down to 2400 ms and offset 0 to 4 km. Panel b in the top right shows the migration result using the correct velocity of 2 km per second: three crisp focused point images at the true scatterer positions marked with orange plus signs, and a clean dipping segment aligned with the green reference line. Panel c in the bottom left shows migration with velocity too slow, at 0.80 times the correct velocity: the point images are left as downward-frowning arcs of uncollapsed hyperbola, and the dipping segment is under-migrated and offset from the green reference. Panel d in the bottom right shows migration with velocity too fast, at 1.25 times correct: the point images become upward-smiling arcs of over-migrated semicircular sweeps, and the dipping segment is over-rotated past the green reference. A bold suptitle reads: the image IS the velocity diagnostic.
:width: 100%

Kirchhoff migration applied to the same synthetic zero-offset data (a) with three migration velocities. Correct velocity (b) collapses each diffraction hyperbola back to its source point and aligns the dipping segment with its true position. Velocity too slow (c) leaves residual downward curvature — frowns. Velocity too fast (d) leaves residual upward curvature — smiles. The migrated image itself is the diagnostic of whether the velocity is right.
```

Equation {eq}`eq-hyperbola-forward` is the kinematic forward operator. A complete forward operator also includes the amplitude weighting (spherical spreading, reflection coefficient, free-surface effects). For the remainder of this lecture the kinematic form is sufficient: it is what determines *where* events are plotted, which is what migration is correcting.

---

## 5 — The Inverse Problem

The inverse problem is to recover $m(x, z)$ given observed data $\mathbf{d}$ and a velocity $v$. If $F$ is the forward operator, the adjoint $F^\top$ is Kirchhoff migration. In operator notation,

```{math}
:label: eq-forward-inverse
\mathbf{d} = F\,\mathbf{m}, \qquad \hat{\mathbf{m}} = F^\top \mathbf{d}.
```

The migrated image $\hat{\mathbf{m}} = F^\top \mathbf{d}$ is not the true inverse $F^{-1}\mathbf{d}$ — it is the *adjoint* applied to the data. For a well-sampled, constant-velocity acquisition with infinite aperture, the adjoint and inverse agree up to a filter. In practice, finite apertures, missing traces, and spatial aliasing introduce artifacts: concentric semicircles at the survey ends (from abruptly terminated summation) and a characteristic $1/|\omega|$ low-frequency boost from the hyperbola summation acting as an integrator over time {cite:p}`Claerbout2010`. Least-squares migration and reverse-time migration are refinements that attempt to approximate $F^{-1}$ rather than $F^\top$ alone.

### 5.1 The velocity–image duality

The migration operator $F^\top$ in equation {eq}`eq-kirchhoff` depends explicitly on the velocity $v$. Using the wrong $v$ does not simply rescale the image — it produces a characteristic distortion that is visually diagnostic.

- **Correct velocity.** Each diffraction hyperbola collapses exactly to its source point. Reflectors align with their true positions. The image is *focused*.
- **Velocity too slow.** The migration hyperbolas are narrower than the true data hyperbolas. The summation catches only the apex of each true hyperbola, leaving the flanks behind as a downward-opening residual arc. These residuals are called *frowns*; the image is *under-migrated*.
- **Velocity too fast.** The migration hyperbolas are broader than the true ones. Each migrated point is spread into a partial semicircle because the summation reaches beyond the true data. These residuals are called *smiles*; the image is *over-migrated*.

{numref}`fig-velocity-image-duality` shows all three cases for the same synthetic data. This is the operational basis of **migration velocity analysis**: the velocity model is adjusted until residual moveout on image gathers is flat and diffractions collapse to points. In practice the process is iterative — a starting velocity from refraction tomography, a first migration, residual analysis, update, re-migrate — and the starting model often comes from the very refraction methods Lectures 6–7 developed.

:::{admonition} Concept Check 5.1
:class: tip

A marine zero-offset section shows a prominent reflection hyperbola with apex at $(x = 5\text{ km},\ t_0 = 2.0\text{ s})$. After migration with $v = 2.5$ km/s, the hyperbola is replaced by a crisp point near $(x = 5\text{ km},\ z = 2.5\text{ km})$. After migration with $v = 3.0$ km/s, the point is replaced by an upward-curving arc.

1. Which migration velocity is more nearly correct, and how can you tell?
2. Estimate the depth of the reflector from the correct-velocity image.
3. What would you expect to see if the velocity were set to $v = 2.0$ km/s?

:::

### 5.2 The refraction–reflection bridge

Migration requires a velocity model $v(x,z)$. Where does that velocity come from? The answer is that **no single method can build it alone** — refraction and reflection each constrain a different part of the Earth, for reasons rooted in the physics of each wave type.

#### Why refraction alone is not enough

Refraction (Lectures 6–7) uses head waves — energy that travels *horizontally* along a velocity interface and radiates back to the surface. The intercept-time method or {cite:t}`ZeltBarton1998`-style tomography inverts first-arrival travel times into a velocity-versus-depth profile $v(z)$. But head waves exist only along interfaces where velocity *increases* with depth. There are two hard limits:

- **Depth ceiling**: the deepest refractor a survey can detect is the one whose crossover distance fits within the survey aperture (recall the crossover formula from Lecture 6).
- **Low-velocity zones**: any layer where $v$ decreases is invisible to refraction — head waves are never generated, so the layer is simply skipped (the "hidden layer" problem from Lecture 7).

Result: refraction gives a reliable, absolute $v(z)$ for the **shallow section** (typically the upper 1–5 km in crustal studies) but says nothing about deeper structure.

#### Why reflection alone is not enough

Reflection (Lectures 8–9) uses echoes from impedance contrasts at any depth. NMO analysis on CMP gathers yields the stacking velocity $V_{\rm rms}(t_0)$, and the Dix equation converts $V_{\rm rms}$ to interval velocities. But these velocities are:

- **Relative, not absolute**: NMO velocities are best-fit hyperbolae; they constrain velocity *ratios* between layers better than they constrain absolute values.
- **Contaminated by the near-surface**: if the shallow velocity is wrong, every Dix-inverted interval velocity below it inherits that error, because $V_{\rm rms}$ is a running average from the surface down.
- **Measured in time, not depth**: without an independent velocity to convert from $t$ to $z$, reflectors are positioned in time, not in the Earth.

Result: reflection gives excellent **structural detail** (interfaces, faults, stratigraphic horizons) at all depths but needs an external velocity anchor.

#### What each method contributes

| | Refraction (Lecs 6–7) | Reflection (Lecs 8–9) |
|---|---|---|
| **Wave type used** | Head waves (first arrivals) | Reflected waves (later arrivals) |
| **What it measures** | Absolute layer velocities $v_1, v_2, \ldots$ | Stacking velocity $V_{\rm rms}(t_0)$ at each reflector |
| **Depth range** | Surface to deepest refractor (~1–5 km) | Any depth with an impedance contrast |
| **Strengths** | Accurate absolute $v$; robust to noise | Detailed structural image; works at all depths |
| **Blind spots** | Cannot see below deepest refractor; misses low-velocity zones | Velocity estimates are relative, not absolute; sensitive to near-surface errors |
| **Governing equation** | $t_i(x)$ intercept-time (Lec 6); tomographic inversion $\mathbf{d} = G\mathbf{m}$ (Lec 7) | $t^2(x^2)$ hyperbola → $V_{\rm rms}$ → Dix equation (Lec 8) |

#### The unified processing checklist

The two methods are not competitors — they are **complementary constraints on the same model** $v(x,z)$. In practice, an active-source imaging project proceeds through the following steps:

::::{admonition} Active-source imaging workflow — from data to image
:class: important

| Step | Action | Method | What it produces | Equations / tools |
|:----:|--------|--------|-----------------|-------------------|
| **1** | **Pick first breaks** on near-offset traces | Refraction | Observed first-arrival times $t_{\rm fb}(x)$ | Visual picking or AI autopicker ({cite:t}`Mardan2024`) |
| **2** | **Invert first-arrival times** | Refraction tomography | Shallow velocity model $v_{\rm refr}(x, z)$ from surface to ~3–5 km depth | Intercept-time (Lec 6) or $\mathbf{d} = G\mathbf{m}$ tomography ({cite:t}`ZeltBarton1998`) |
| **3** | **Pick NMO velocities** on CMP gathers | Reflection | Stacking velocity $V_{\rm rms}(t_0)$ for each reflector | Semblance analysis (Lec 8) |
| **4** | **Convert to interval velocities** | Reflection | Interval velocities $v_{\rm int}(t_0)$ below the refraction zone | Dix equation (Lec 8): $v_n^2 = \frac{V_{{\rm rms},n}^2 t_n - V_{{\rm rms},n-1}^2 t_{n-1}}{t_n - t_{n-1}}$ |
| **5** | **Stitch the two models** | Both | An initial $v_0(x, z)$: refraction model on top, Dix-inverted model below, blended at the transition depth | — |
| **6** | **Migrate** the zero-offset (stacked) section | Migration | A first image $\hat{\mathbf{m}}_0 = F^\top \mathbf{d}$ using $v_0$ | Kirchhoff sum, Eq. {eq}`eq-kirchhoff` |
| **7** | **Diagnose** the image | Velocity analysis | Residual curvature on common-image gathers: frowns = too slow, smiles = too fast, flat = correct | Visual inspection ({numref}`fig-velocity-image-duality`) |
| **8** | **Update** the velocity model | Iterative refinement | Corrected $v_1(x,z)$; return to Step 6 | Repeat Steps 6–8 until residuals are flat |

The loop **6 → 7 → 8 → 6** is iterated until the image is focused. In CASIE-21 (Section 9), the shallow model from OBS first arrivals (Step 2) was the essential anchor without which the reflection migration (Step 6) would have started from a wrong velocity.

::::

The key insight is that **refraction supplies the absolute velocity anchor, and reflection supplies the structural detail**. Without the refraction model, migration starts from an incorrect velocity and produces an unfocused image. Without reflection, the refraction model alone cannot see the plate interface or deep sedimentary layers. Migration is the operation that fuses both constraints into a single image — and the image itself is the diagnostic of whether the combined velocity model is correct.

---

## 6 — Worked Example

The data in {numref}`fig-velocity-image-duality`(a) were generated from a model with three point scatterers at $(0.8, 0.5)$, $(2.0, 1.0)$, and $(3.0, 0.7)$ km, plus a dipping segment from $(1.0, 1.3)$ to $(1.8, 1.7)$ km, in a constant-velocity medium with $v = 2.0$ km/s. Each scatterer produced a hyperbola via equation {eq}`eq-hyperbola-forward`.

Consider the rightmost scatterer at $(x_0 = 3.0,\ z_0 = 0.7)$ km. Its forward-modeled hyperbola has apex at

```{math}
t_{\rm apex} = \frac{2 z_0}{v} = \frac{2 \times 0.7}{2.0} = 0.70\ \text{s}.
```

At an offset of 1 km from the apex ($x = 4.0$ km), the predicted arrival time is

```{math}
t = \sqrt{(0.70)^2 + \left(\frac{2 \times 1.0}{2.0}\right)^2} = \sqrt{0.49 + 1.00} = 1.22\ \text{s}.
```

Under the correct-velocity migration, the summation over the hyperbola through $(x = 3.0,\ z = 0.7)$ collects all the energy the forward operator placed along that hyperbola and deposits it back at the point — {numref}`fig-velocity-image-duality`(b) confirms this at the third scatterer location, marked by the orange cross.

Now consider migrating with $v = 2.5$ km/s. The migration hyperbola for the same output pixel has a different shape: its apex is still at $t = 2 z/v = 0.56$ s, but the flank curvature is gentler. The summation samples data points that lie on a different curve from the one the data were actually placed along, so the summation misses the flanks, and the flank energy appears as a residual partial-semicircle "smile" in {numref}`fig-velocity-image-duality`(d).

This is the velocity–image duality in one concrete example. The image was not merely scaled; its geometry encodes whether the velocity was right.

---

## 7 — Course Connections

- **Lecture 5 — Snell's law.** Equation {eq}`eq-tuchel` is the zero-offset version of Snell's parameter; the factor of two traces to the round-trip path.
- **Lectures 6–7 — Seismic refraction.** First-arrival times and the intercept-time equation provide the shallow velocity model that seeds migration.
- **Lectures 8–9 — Seismic reflection.** NMO, CMP stacking, and Dix inversion provide the deeper part of the same velocity model.
- **Lecture 11 — Whole-Earth structure.** The same physical framework — travel times through a layered medium — produces the global 1-D Earth model (PREM) by stacking seismograms from earthquakes instead of shots.
- **Lecture 13 — Seismic tomography.** The local refraction/reflection velocity model is the small-scale analogue of the global tomographic models; both solve $\mathbf{d} = F(\mathbf{m})$ for $\mathbf{m}$.
- **Lab 4 — Design → Simulate → Image.** Students take the survey design from the companion discussion session, generate a synthetic shot gather, migrate it with three velocities, and report which velocity is correct and how they could tell from the image alone.

---

## 8 — Research Horizon

Active-source seismic imaging is an area of vigorous methodological development, and one of the most active sub-fields is the application of deep learning to accelerate or replace steps of the processing chain. The three references below, all from peer-reviewed academic outlets in 2019–2024, illustrate three different places where a neural network serves as a **surrogate** for a physics-based operator.

1. **First-break picking {cite:p}`Mardan2024`.** A residual U-Net is initialized with weights pretrained on natural images (ImageNet), then fine-tuned on fewer than 10 % of hand-picked shots from a real refraction survey. The remaining 90 % are picked automatically with expert-level accuracy. The surrogate learns a mapping from waveform shapes to arrival times — the same mapping a human expert performs when reading a record section.

2. **Denoising reflection shot gathers {cite:p}`LiTradLiu2024`.** A self-supervised U-Net removes erratic, non-Gaussian noise from shot gathers without requiring paired noisy/clean training data. The network trains only on the noisy data itself, exploiting the statistical difference between coherent seismic signals and incoherent noise. The surrogate learns a projection from noisy data to the signal subspace that the physics of wave propagation defines.

3. **Velocity model building {cite:p}`YangMa2019`.** A fully-convolutional encoder–decoder network takes raw multi-shot gathers as input and produces a $v(x, z)$ model as output, in effect performing traveltime picking, NMO analysis, and Dix inversion in a single forward pass. Trained on synthetic data generated from known velocity models, the network learns a surrogate for the inverse operator $F^{-1}$.

Each of these networks is a surrogate for an operator that geophysics already understands. The networks are trained on data that only exist *because* the physics-based operator exists: Mardan's network needs hand-picked first breaks (an expert using the intercept-time method); Li's network needs a statistical model of what constitutes "signal" versus "noise" that derives from the wave equation; Yang & Ma's network needs a training set of $(v, \text{shot gather})$ pairs where the shot gathers were produced by a finite-difference wave-equation solver.

:::{admonition} A principle for the rest of this course
:class: important

Deep learning methods in active-source imaging are **accelerators, not replacements**, for physical understanding. Every surrogate network currently deployed requires training data that were produced by — or labeled by — someone who already understood the physics. The question for a student of geophysics is not "will AI replace the physics?" (it has not, and the training-data dependency is structural, not temporary). The question is: *where in the processing chain is a surrogate valuable, and what are the failure modes when the operator it replaces is applied to data outside the training distribution?*
:::

---

## 9 — Societal Relevance

The Cascadia subduction zone hosts the largest earthquake hazard in the continental United States. A full-margin M9+ rupture is a once-per-500-year event; the last one occurred on 26 January 1700 and produced a tsunami that crossed the Pacific {cite:p}`Atwater2005`. Every plan for coastal resilience — shakemaps, tsunami inundation forecasts, land-use restrictions, building codes — rests on a model of where the plate interface is, how deeply it couples, and how far updip the rupture can propagate.

CASIE-21, the Cascadia Seismic Imaging Experiment, acquired the densest multi-channel reflection and OBS refraction dataset ever collected along the Cascadia margin in the summer of 2021. Its purpose was not incremental: it was to build a kilometer-scale image of the plate interface between the Nootka fracture zone and Cape Mendocino, from which the locked, transitional, and creeping zones could be mapped. The processing applies exactly the refraction–reflection–migration loop this lecture has developed. The velocity model built from OBS first arrivals is the starting model for the reflection migration that reveals the plate interface. The image is the velocity diagnostic.

**Follow-up resource:** the CASIE-21 project overview at <https://casie21.weebly.com/> documents the experiment, the acquisition geometry, and the evolving data release. The Cascadia Recurrence Probability Workshop reports issued by USGS and Oregon DOGAMI translate these images into hazard parameters that are used in Washington, Oregon, and British Columbia for building codes and tsunami evacuation mapping.

---

## AI Literacy — Epistemics + Prompt Lab

:::{admonition} AI Literacy — Evaluating surrogate networks
:class: seealso

The three deep-learning methods in Section 8 are all *data-driven surrogates* for physics-based operators. Two activities — one epistemic, one generative — deepen the critical stance.

**Activity A — Epistemics (paired reading, 15 min).** Each pair selects one of {cite:t}`Mardan2024`, {cite:t}`LiTradLiu2024`, or {cite:t}`YangMa2019` and answers three questions from the paper's text alone, with no outside sources:

1. What Earth-science problem is the network designed to solve, and which physics-based operator does it replace?
2. Where did the training data come from? What physical knowledge or human labor produced them?
3. What evidence in the paper would warrant using this method on a Cascadia dataset that is *not* in the training distribution? If the authors do not provide such evidence, what would you demand before trusting the method?

**Activity B — Prompt Lab (paired, 10 min).** Each pair crafts a prompt for a large language model that asks it to explain *why* the Kirchhoff migration of Figure 4(c) shows "frowns" when the velocity is too slow. Evaluate the response against the derivation in Section 3.3 and Section 5.1. Report one thing the model got right and one thing that was subtly (or obviously) wrong. A useful rubric:

| Dimension | Question |
|-----------|----------|
| Physical correctness | Is the direction (frown vs. smile) attributed correctly to under- vs. over-migration? |
| Causal explanation | Does the response invoke the shape mismatch between the migration hyperbola and the true data hyperbola, or does it offer a superficial curve-fitting account? |
| Calibration | Does the response signal uncertainty where appropriate, or state incorrect claims with confidence? |
| Use of mathematics | Does the response cite or reconstruct equation {eq}`eq-hyperbola-forward`, or avoid mathematics entirely? |

:::

LO-7 is exercised directly through these activities: the goal is not to reject AI tools, but to use them in a way that is *anchored in the physics of the problem*. A surrogate network — whether a picked-for-this-lecture ImageNet-pretrained U-Net or a large language model explaining a figure — is only as trustworthy as the understanding one brings to evaluate it.

---

## Further Reading

- {cite:t}`Claerbout2010`, *Basic Earth Imaging*. Stanford Exploration Project. Open-access: <http://sepwww.stanford.edu/sep/prof/bei11.2010.pdf>. Chapters 3–5 cover the same material developed here at a deeper level; Chapters 6–8 extend to Fourier-domain phase-shift migration, downward continuation, and prestack migration.
- {cite:t}`LowrieFichtner2020`, *Fundamentals of Geophysics* (3rd ed., Cambridge University Press). Chapter 3. Available free via UW Libraries.
- {cite:t}`ZeltBarton1998`, "Three-dimensional seismic refraction tomography: A comparison of two methods applied to data from the Faeroe Basin", *J. Geophys. Res.* 103, 7187–7210. doi:10.1029/97JB03536. Foundational open-access paper for refraction tomography as practiced today.
- {cite:t}`Stolt1978`, "Migration by Fourier transform", *Geophysics* 43, 23–48. The original f-k migration method. Paywalled; cite only.
- MIT OCW 12.510 Introduction to Seismology, lecture notes on migration: <https://ocw.mit.edu/courses/12-510-introduction-to-seismology-spring-2010>. CC BY-NC-SA.
- EarthScope/IRIS Active Source Recording Resources: <https://www.earthscope.org/data/active-source/>. Recording geometries and sample datasets.

```{bibliography}
:filter: docname in docnames
```
