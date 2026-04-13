---
title: "Seismic Reflection II: Dipping Layers, Non-Idealities, and Modern Methods"
week: 3
lecture: 9
date: "2026-04-22"
topic: "Dipping-layer travel time, multiples, diffractions, AVO, noise filtering, and deep learning processing"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4", "LO-5", "LO-7"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-B", "LO-OUT-C", "LO-OUT-D", "LO-OUT-G", "LO-OUT-H"]
open_sources:
  - "Lowrie & Fichtner 2020 Ch. 6 §6.5 (free via UW Libraries)"
  - "Sheriff & Geldart 1995 Ch. 4 §4.2, Ch. 6 §6.1 (cite only)"
  - "Shuey 1985 Geophysics doi:10.1190/1.1441936 (open)"
  - "Rutherford & Williams 1989 Geophysics doi:10.1190/1.1442696 (open)"
---

# Seismic Reflection II: Dipping Layers, Non-Idealities, and Modern Methods

```{seealso}
📊 **Lecture slides** — [open in new tab ↗](../../slides/week03/lecture_09_slides.html)
🔬 **Lab connection** — Lab 3 Part 6: Dipping-layer NMO and DMO correction
```

::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-2, LO-OUT-B]** Derive the dipping-layer travel-time equation and explain how the asymmetric linear term in $x$ distinguishes dipping from flat-layer hyperbolas; compute up-dip and down-dip apparent velocities.
- **[LO-1, LO-OUT-C]** Identify the physical origin of multiple reflections, predict the TWTT and NMO velocity of a long-path surface multiple, and explain why NMO stacking alone cannot remove it.
- **[LO-1, LO-OUT-C]** Explain the Huygens-principle origin of diffraction hyperbolae, state the diffraction equation, and describe qualitatively what migration accomplishes.
- **[LO-2, LO-OUT-B]** Apply the Shuey approximation $R(\theta) \approx R(0) + G\sin^2\theta$; classify a reflection event into AVO Classes I–IV from the signs of intercept and gradient.
- **[LO-3, LO-OUT-D]** Explain the purpose of f-k velocity filtering for ground-roll suppression; describe the architecture and training strategy of a U-Net denoising model applied to seismic data.
- **[LO-7, LO-OUT-H]** Critically evaluate a claim that a deep-learning seismic denoiser has "recovered" true geology, identifying at least two failure modes.

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1 (multiples, diffractions, AVO physics), LO-2 (dipping-layer t-x math, Shuey coefficients), LO-3 (DMO concept, velocity analysis for dipping layers), LO-4 (flat-layer assumptions and when they break), LO-5 (figure generation in Lab 3), LO-7 (AI/ML tools evaluated critically) |
| **Learning outcomes** | LO-OUT-A through D, G, H |
| **Prior lecture** | Lecture 8 — Seismic Reflection I (flat-layer case: R, T, NMO, Dix, tuning, semblance) |
| **Next lecture** | Lecture 10 — Seismic Migration (wavefield backpropagation, velocity model building, FWI) |
| **Lab connection** | Lab 3 Part 6 (dipping-layer CMP gather; measure up-dip/down-dip velocities; apply f-k filter) |

::::

## Prerequisites

Lecture 8 in full: acoustic impedance, the convolutional model, the flat-layer travel-time hyperbola, NMO correction, $t^2$–$x^2$ linearisation, the Dix equation, and semblance velocity analysis. The AVO section (§7) additionally requires Snell's law at oblique incidence (Lecture 5).

---

## 1. The Geoscientific Question

The flat-layer model developed in Lecture 8 rests on three assumptions: reflectors are horizontal, each layer has constant velocity, and the recorded wavefield contains only primary reflections. None of these assumptions holds in a real geologic setting. The Cascadia accretionary wedge contains fold-and-thrust structures with reflectors dipping at 5–25°; the décollement itself is a planar dipping surface. Multiple reflections dominate seismic gathers above shallow reflectors in the outer wedge. Fault-tip diffractions obscure the geometry of thrust faults. Ground-roll noise from surface waves overwhelms the primary reflections on land surveys.

Relaxing each assumption in turn yields three questions. First: how does a dipping reflector alter the NMO correction, and can true velocity and dip be recovered separately? Second: how are multiple reflections identified and suppressed so they do not produce false structural images? Third: how are diffractions and noise handled, and what does the latest machine-learning toolchain contribute?

---

## 2. Governing Physics: Dipping Reflectors

### 2.1 The Geometry of Dip

A reflector dipping at angle $\delta$ from horizontal (Fig. {numref}`fig-dipping-geom-l9`, Panel A) presents a different reflection geometry in the up-dip and down-dip directions from a common surface source. The source fires at position $E$ at the surface; a receiver $G$ is at offset $x$.

For **down-dip shooting** (receiver in the down-dip direction), each successive receiver is above a progressively deeper part of the reflector. The two-way path increases faster than for a flat reflector at the same perpendicular depth $h$. For **up-dip shooting**, the receiver looks toward the shallower part of the reflector, shortening the two-way path relative to a flat reflector.

The result is an asymmetric travel-time curve: the same source–receiver configuration produces different arrival times depending on the survey direction.

### 2.2 CMP Reflection-Point Smear

For a flat reflector, every trace in a CMP gather reflects from the same subsurface point — directly below the surface midpoint. For a **dipping reflector**, the reflection point migrates up-dip as offset increases (Fig. {numref}`fig-cmp-smear-l9`). A CMP gather over a dipping layer therefore samples a laterally smeared zone, not a single point. Standard NMO stacking produces a spatially blurred image in the presence of dip.

```{figure} ../../assets/figures/fig_cmp_dipping_scatter.png
:name: fig-cmp-smear-l9
:alt: Two-panel figure. Left panel shows a flat horizontal reflector at 1000 m depth; all ray paths for different offsets in a CMP gather (source-receiver pairs colour-coded by offset from purple to yellow) converge on the same single reflection point at depth directly below the surface midpoint. Right panel shows a dipping reflector at 15 degrees; the same CMP gather's reflection points are smeared up-dip at shallower depths as offset increases, indicated by a red arrow labelled 'reflection point smear (up-dip)'.
:width: 100%

**CMP reflection-point geometry for flat (left) and dipping (right) reflectors.** For a flat reflector, all traces in the CMP gather share the same reflection point regardless of offset. For a dipping reflector at $\delta = 15°$, the reflection point migrates up-dip with increasing offset. Stacking these traces without a dip-moveout (DMO) correction therefore averages over a spatially extended zone rather than a single subsurface location. Python-generated original figure.
```

---

## 3. Mathematical Framework: Dipping-Layer Travel Time

### 3.1 Exact Travel-Time Equation

Using the image-point method, the exact two-way travel-time for a source at the origin and receiver at offset $x$, with a reflector whose perpendicular distance from the source is $h$ and dip angle $\delta$, is

```{math}
:label: eq-l9-tx-down
t_d(x) = \frac{1}{V_1}\sqrt{x^2 + 4h x\sin\delta + 4h^2} \quad \text{(down-dip)}
```

```{math}
:label: eq-l9-tx-up
t_u(x) = \frac{1}{V_1}\sqrt{x^2 - 4h x\sin\delta + 4h^2} \quad \text{(up-dip)}
```

Both curves share the same zero-offset intercept $t_0 = 2h/V_1$.

### 3.2 The Linear Term and Asymmetry

Squaring and expanding:

```{math}
:label: eq-l9-t2x2-dip
t^2(x) = t_0^2 + \frac{x^2}{V_1^2} \pm \frac{2 t_0 \sin\delta}{V_1}\cdot x
```

The $\pm(2 t_0 \sin\delta / V_1) \cdot x$ term — linear in $x$ and absent in the flat-layer case — is the mathematical signature of dip. It produces:

- **Down-dip** (+ sign): MORE moveout than flat → shallower apparent NMO velocity when fit with a flat-layer model
- **Up-dip** (− sign): LESS moveout than flat → deeper apparent NMO velocity

The $t^2$–$x^2$ relationship is therefore **non-linear** for dipping reflectors, making the linear regression of Lecture 8 incorrect (Fig. {numref}`fig-dipping-geom-l9`, Panel C).

```{figure} ../../assets/figures/fig_dipping_layer_geometry.png
:name: fig-dipping-geom-l9
:alt: Three-panel figure. Panel A shows the geometry: a horizontal surface with a source (red star) at centre, up-dip receiver (blue triangle) and down-dip receiver (orange triangle) at symmetric offsets. A green dipping reflector crosses the plot at 15 degrees. Blue and orange dashed ray paths show reflections to the up-dip and down-dip receivers respectively; reflection points are marked as dots. A flat reference (dotted grey) is shown at the depth of the perpendicular intersection. Panel B shows travel-time curves for flat (grey dashed), down-dip (orange), and up-dip (blue) shooting; all three share the same t0 at x=0 but diverge; the linear shifts plus xsinδ/V1 and minus xsinδ/V1 are annotated at x=2400 m. Panel C shows the t-squared x-squared relationship for all three cases, with the up-dip and down-dip curves curving away from the flat-layer straight line; the NMO tangent line for V_NMO=V1/cosdelta is shown as a green dotted line.
:width: 100%

**Dipping-layer travel-time asymmetry.** (A) Geometry: up-dip and down-dip receivers from the same source position. (B) $t(x)$ curves: down-dip arrivals are delayed relative to the flat-layer case; up-dip arrivals are early; both cross the flat curve at $x = 0$. (C) $t^2$–$x^2$ plot: the non-linear (curved) trends for the dipping cases contrast with the straight flat-layer line. The green dotted tangent at the origin has slope $1/V_\mathrm{NMO}^2 = \cos^2\delta/V_1^2$. Python-generated original figure.
```

### 3.3 NMO Velocity for Dipping Layers

Taylor-expanding $t_d(x)$ around $x = 0$:

$$t_d(x) \approx t_0 + \frac{\sin\delta}{V_1}\cdot x + \frac{\cos^2\delta}{2 V_1^2 t_0}\cdot x^2 + \ldots$$

The quadratic coefficient gives the NMO velocity for a **dipping reflector**:

```{math}
:label: eq-l9-vnmo-dip
V_\mathrm{NMO,dip} = \frac{V_1}{\cos\delta}
```

This is **larger** than $V_1$; fitting a flat-layer NMO model to data over a dipping reflector overestimates the subsurface velocity.

### 3.4 Recovering True Velocity and Dip

From two surveys — one down-dip and one up-dip with the same source — the true velocity and dip angle can be recovered. At large offsets the dominant moveout terms give apparent velocities:

$$V_d \approx \frac{V_1}{1 + \sin\delta}, \qquad V_u \approx \frac{V_1}{1 - \sin\delta}$$

Solving:

```{math}
:label: eq-l9-v1-dip-recover
V_1 = \frac{2\,V_d\,V_u}{V_d + V_u}, \qquad \sin\delta = \frac{V_u - V_d}{V_u + V_d}
```

In practice, **dip-moveout (DMO) correction** is applied after NMO correction to reposition the reflection points to a common location before stacking, effectively decoupling the dip and velocity problems.

---

## 4. Multiple Reflections

A **multiple** is a seismic event that has undergone more than one reflection before reaching the receiver. Multiples are coherent and appear as hyperbolic events in the CMP gather; they are a primary source of false structure in seismic sections.

### 4.1 Types of Multiples

```{figure} ../../assets/figures/fig_multiple_types.png
:name: fig-multiples-l9
:alt: Three-panel figure. Panel A shows schematic ray-path diagrams for four multiple types in a two-reflector earth model: primary P (blue, single bounce at Refl. 2), long-path multiple M (orange, two bounces at Refl. 2 with one surface reflection), peg-leg PL (yellow, one bounce at Refl. 2 and one at Refl. 1), and interbed IB (teal, bouncing between Refl. 1 and Refl. 2). Panel B shows the synthetic CMP gather with four hyperbolic events and their predicted dashed-curve overlays. Panel C shows the t-squared x-squared plot; the long-path multiple and primary have the same slope (same V_rms) but the multiple has double the intercept; an annotation reads 'Same slope (same V_rms)'.
:width: 100%

**Multiple reflection types.** (A) Ray paths: primary (P), long-path surface multiple (M), peg-leg (PL), and interbed (IB). (B) Synthetic CMP gather: four distinct hyperbolic events. (C) $t^2$–$x^2$ linearisation: the long-path multiple and its parent primary have **identical slopes** (same $V_\mathrm{rms}$) but the multiple's intercept is four times larger ($t_0^\mathrm{mult} = 2 t_0^\mathrm{prim}$). This is the central challenge: NMO stacking cannot separate them. Python-generated original figure.
```

The **long-path (surface) multiple** is generated when energy reflects from the main reflector, returns to the surface, re-reflects downward, and reflects from the same reflector again. Its travel-time is

```{math}
:label: eq-l9-multiple-twtt
t_\mathrm{mult}^2(x) = (2\,t_0)^2 + \frac{x^2}{V_\mathrm{rms}^2}
```

This has the same NMO velocity as the primary but double the zero-offset TWTT. Because $V_\mathrm{NMO}^\mathrm{mult} = V_\mathrm{NMO}^\mathrm{prim}$, NMO correction will simultaneously flatten both the primary and the multiple, and stacking will not suppress the multiple.

**Peg-leg multiples** arrive between the primary and long-path multiple; their NMO velocity differs from both. **Interbed multiples** bounce between two subsurface interfaces without returning to the surface.

### 4.2 Multiple Suppression

Modern workflows use **surface-related multiple elimination (SRME)**: the observed wavefield is autocorrelated with itself to predict the multiple waveforms, which are then adaptively subtracted. Deep-learning approaches train encoder-decoder networks to separate primaries from multiples in the $\tau$-$p$ (intercept time–ray parameter) domain.

---

## 5. Diffractions

### 5.1 Huygens Principle and Point Scatterers

Huygens's principle states that every point on a wavefront acts as a secondary source of spherical wavelets. At a sharp subsurface discontinuity — a fault tip, an unconformity edge, a channel boundary — the incident wave excites new secondary spherical waves. These **diffractions** carry energy in all directions equally, regardless of the angle of the incoming wave.

For a point scatterer at position $(x_s, z_s)$ in a medium of velocity $V_1$, the diffraction travel time recorded at surface position $x$ is

```{math}
:label: eq-l9-diffraction
t_\mathrm{diff}(x) = \frac{2}{V_1}\sqrt{(x - x_s)^2 + z_s^2}
```

This is a hyperbola with vertex at $(x_s,\, 2z_s/V_1)$ — the same form as a primary reflection hyperbola. The vertex time and the true velocity $V_1$ uniquely determine $z_s$.

```{figure} ../../assets/figures/fig_diffraction_hyperbola.png
:name: fig-diffraction-l9
:alt: Three-panel figure. Panel A shows a depth cross-section with a flat blue-dashed reflector at 600 m, a vertical red fault line from 600 to 1000 m, and a red star at the fault-tip scatterer at 1000 m depth. Multiple orange ray paths fan out from the scatterer to surface receivers. Panel B shows the t(x) curves for the flat-reflector primary (blue dashed) and the fault-tip diffraction (red solid); the diffraction hyperbola is broader and its apex is at a later two-way time corresponding to the scatterer depth. Panel C shows the synthetic zero-offset section as variable-area wiggle traces with the flat primary visible as a horizontal band, the diffraction hyperbola visible as a broad curved event below it, and annotations labelling both events.
:width: 100%

**Point diffraction from a fault-tip scatterer.** (A) Subsurface model: flat reflector at 600 m and a fault tip at 1000 m acting as a point scatterer. (B) Travel-time curves: the diffraction hyperbola (red) has the same zero-offset intercept form as a primary but extends uniformly across the entire receiver array. (C) Synthetic zero-offset section: both the flat primary and the diffraction hyperbola are visible. Migration collapses the hyperbola to the fault-tip point, recovering the true geometry. Python-generated original figure.
```

### 5.2 Structural Interpretations and Migration

An **unmigrated** seismic section displays the hyperbolic diffraction rather than the point; fault terminations therefore appear as fan-shaped energy patches rather than lines. A **syncline** bounded by two dipping reflectors produces a "bowtie" pattern in the unmigrated section (the two limbs' hyperbolae cross each other). **Seismic migration** — the topic of Lecture 10 — is the process of collapsing diffractions and repositioning dipping events to their true subsurface locations.

---

## 6. Survey Noise and Signal Enhancement

### 6.1 Coherent Noise Types

A raw shot gather contains several coherent noise types alongside the desired reflections (Fig. {numref}`fig-fk-filter-l9`):

- **Direct wave** ($V \approx V_1 = 1500$–2000 m/s): linear first arrival, easily muted at offsets $x > x_\mathrm{mute}$
- **Ground roll** (Rayleigh wave; $V \approx 200$–500 m/s): high amplitude, low frequency (5–20 Hz), dispersive; dominates land gathers at short and medium offsets
- **Air blast** ($V \approx 340$ m/s): visible on uphole geophones; muted by velocity filter
- **Head wave** ($V > V_1$): first arrival at offsets beyond the crossover distance; muted before NMO correction

### 6.2 f–k Velocity Filtering

In the frequency-wavenumber ($f$–$k$) domain, events with apparent velocity $V_\mathrm{app}$ map to the line $k = f/V_\mathrm{app}$. Ground roll occupies the high-$|k|$ fan region (slow velocity → large wavenumber per unit frequency). A **velocity filter** rejects all $|k| > f/V_\mathrm{cutoff}$, where $V_\mathrm{cutoff}$ is chosen between the ground-roll velocity and the direct-wave velocity:

```{math}
:label: eq-l9-fk-mask
\mathcal{M}(f, k) = \begin{cases} 1 & |k| < f / V_\mathrm{cutoff} \\ 0 & \text{otherwise} \end{cases}
```

The filtered gather $\tilde{u}(x,t) = \mathcal{F}^{-1}\!\left[\mathcal{M}(f,k)\,U(f,k)\right]$ removes the ground-roll fan while preserving the reflection events (Fig. {numref}`fig-fk-filter-l9`, Panel C).

```{figure} ../../assets/figures/fig_ground_roll_fk.png
:name: fig-fk-filter-l9
:alt: Three-panel figure. Panel A shows a raw shot gather as variable-area wiggles with labelled annotations pointing to slow-velocity high-amplitude ground roll at small offsets, the linear direct wave at moderate offsets, and the hyperbolic reflection at about 550 ms zero-offset time. Panel B shows the two-dimensional f-k amplitude spectrum on logarithmic scale; three dashed lines mark the velocities of ground roll (300 m/s, red), the filter cutoff (600 m/s, orange), and the direct wave (2000 m/s, blue); the ground roll fan between 0 and 600 m/s is shaded in translucent red. Panel C shows the shot gather after f-k filter application, with the ground-roll fan removed and the reflection hyperbola now clearly visible.
:width: 100%

**Ground-roll suppression by f–k velocity filtering.** (A) Raw gather: ground roll dominates at small offsets and low frequency. (B) f–k spectrum: the slow fan of ground roll is clearly separated from the fast reflection events; the filter mask boundary at $V_\mathrm{cutoff} = 600$ m/s is shown in orange. (C) Filtered gather: ground roll is strongly attenuated; the reflection hyperbola at $t_0 \approx 550$ ms is now visible. Python-generated original figure.
```

### 6.3 Stacking Fold and SNR

After CMP sorting, NMO correction, and noise filtering, the stacked trace has a signal-to-noise ratio proportional to $\sqrt{N_\mathrm{fold}}$:

```{math}
:label: eq-l9-snr-fold
\mathrm{SNR}_\mathrm{stack} = \sqrt{N_\mathrm{fold}} \times \mathrm{SNR}_\mathrm{single}
```

A 48-fold survey improves the SNR by a factor of $\approx 7$ relative to a single trace. Modern dense 3D surveys routinely achieve fold $> 200$, yielding SNR gains of $> 14$.

---

## 7. AVO and the Zoeppritz Equations

### 7.1 Oblique-Incidence Reflectivity

For a plane P-wave incident at angle $\theta_i$ on a planar interface, the reflected and transmitted amplitudes among P- and S-waves are governed by the **Zoeppritz equations** — a system of four linear equations enforcing continuity of particle displacement and traction. The full equations are not reproduced here; see {cite:t}`aki2002quantitative`.

For moderate angles ($\theta_i < 30°$), the Aki-Richards linearisation, simplified by {cite:t}`shuey1985`, gives the **two-term Shuey approximation**:

```{math}
:label: eq-l9-shuey
R(\theta_i) \approx R(0) + G\,\sin^2\theta_i
```

where $R(0)$ is the normal-incidence reflection coefficient (intercept, Eq. {eq}`eq-l8-reflection-coeff`) and

$$G = \frac{\Delta(V_P/V_S)}{2(V_P/V_S)_\mathrm{avg}} + \left(1 - 4\left(\frac{V_S}{V_P}\right)^2\right)\frac{\Delta\rho}{\rho_\mathrm{avg}} - \left(\frac{\Delta V_P}{V_P}\right)_\mathrm{approx}$$

is the **AVO gradient**, sensitive to the contrast in $V_P/V_S$ ratio across the interface. Gas substitution (Gassmann's equations) strongly lowers $V_P$ in a porous sand while leaving $V_S$ nearly unchanged — producing a large, distinctive change in the $V_P/V_S$ ratio and hence in $G$.

### 7.2 AVO Classes

```{figure} ../../assets/figures/fig_avo_classes.png
:name: fig-avo-l9
:alt: Two-panel figure. Panel A shows reflection coefficient R versus incidence angle theta (0 to 40 degrees) for five AVO classes. Class I (blue solid): starts at R=+0.12 and decreases to R=+0.06 (hard sand, dims with offset). Class II (orange solid): starts near R=+0.03 and decreases toward negative values (near-zero intercept, polarity reversal). Class III (red solid): starts at R=-0.09 and becomes increasingly negative to R=-0.15 (gas sand, brightens with offset). Class IV (green solid): starts at R=-0.06 and increases toward less negative values (unusual soft sand). Class IIp (pink dashed): starts near R=+0.06 and increases slightly. Panel B shows the AVO crossplot of intercept R(0) versus gradient G, with a background trend line (grey dashed), scatter clusters for each class colour-coded, and quadrant annotations.
:width: 100%

**AVO classes and the $R(0)$–$G$ crossplot** using the Shuey approximation (Eq. {eq}`eq-l9-shuey`). (A) $R(\theta)$ curves: Class III gas sands brighten with offset ($R(0) < 0$, $G < 0$); Class I tight sands dim. (B) Crossplot: wet sands and shales cluster along the "background trend"; gas sands deviate toward the lower left (Class III) or upper left (Class IV). Python-generated original figure.
```

**Class I** ($R(0) > 0$, $G < 0$): Impedance increases at the reflector (hard sand or cemented rock); amplitude decreases with offset ("dim" AVO).

**Class II** ($R(0) \approx 0$, $G < 0$): Near-zero normal-incidence contrast; a polarity reversal occurs at some intermediate angle. Class IIp has $G > 0$.

**Class III** ($R(0) < 0$, $G < 0$): Impedance decreases at the reflector (soft gas sand); amplitude increases with offset — the classical **bright spot** used as a direct hydrocarbon indicator (DHI).

**Class IV** ($R(0) < 0$, $G > 0$): Amplitude decreases with offset despite a negative intercept; found in highly overpressured or very shallow gas sands.

### 7.3 The AVO Crossplot and Fluid Discrimination

Plotting $R(0)$ against $G$ for all reflection events in a 3D survey produces the **AVO crossplot**. Background wet sands and shales cluster along a "fluid line" ($G \approx -R(0)$). Gas-saturated sands deviate from this line toward more negative $G$ values (Classes II, III) or toward the fourth quadrant (Class IV). The deviation from the background trend is the primary diagnostic for fluid content beyond what impedance alone resolves.

---

## 8. Worked Example: Dipping-Layer Survey

**Given:** A 2D survey over a thrust-fault reflector. The perpendicular depth $h = 800$ m, $V_1 = 2000$ m/s, $\delta = 10°$.

**(a) Zero-offset TWTT:** $t_0 = 2h/V_1 = 2 \times 800 / 2000 = 0.80$ s

**(b) NMO velocity (dipping layer):** $V_\mathrm{NMO} = V_1/\cos\delta = 2000/\cos10° = 2031$ m/s

**(c) Down-dip arrival at $x = 2400$ m:**

$$t_d(2400) = \frac{1}{2000}\sqrt{2400^2 + 4 \times 800 \times 2400 \times \sin10° + 4 \times 800^2}$$
$$= \frac{1}{2000}\sqrt{5{,}760{,}000 + 1{,}329{,}360 + 2{,}560{,}000}$$
$$= \frac{\sqrt{9{,}649{,}360}}{2000} = \frac{3106}{2000} = 1.553\ \text{s}$$

**(d) Up-dip arrival at $x = 2400$ m:**

$$t_u(2400) = \frac{\sqrt{5{,}760{,}000 - 1{,}329{,}360 + 2{,}560{,}000}}{2000} = \frac{\sqrt{6{,}990{,}640}}{2000} = \frac{2644}{2000} = 1.322\ \text{s}$$

**(e) Apparent velocities and recovery of $\delta$:** The large-offset apparent velocities are:
$V_d \approx V_1/(1 + \sin\delta) = 2000/1.174 = 1704$ m/s and $V_u \approx V_1/(1 - \sin\delta) = 2000/0.826 = 2421$ m/s.

Check: $\sin\delta = (V_u - V_d)/(V_u + V_d) = (2421 - 1704)/(2421 + 1704) = 717/4125 = 0.174 \approx \sin10°$ ✓

```{admonition} Concept Check
:class: tip

1. A CMP gather over a 12° dipping reflector is NMO-corrected using the flat-layer formula $V_\mathrm{NMO} = V_1$. Will the NMO-corrected reflectors be over-corrected or under-corrected? Explain using Eq. {eq}`eq-l9-vnmo-dip`.

2. A long-path multiple arrives at $t = 1.4$ s at zero offset and has $V_\mathrm{rms} = 2400$ m/s. At what zero-offset time does its parent primary arrive? Compute the depth to the reflecting horizon assuming $V_1 = 2400$ m/s.

3. A seismic section shows a hyperbolic event that broadens uniformly across all offsets without attenuating. Is this likely a primary reflection or a diffraction? What property of the event distinguishes it? What must be done to recover the true geological feature?
```

---

## 9. SOTA: Deep Learning in Reflection Seismic Processing

### 9.1 Supervised Denoising with U-Nets

The dominant deep-learning architecture for seismic denoising is the **U-Net** (Ronneberger et al. 2015, adapted for seismics by Liu et al. 2020 and Birnie et al. 2021). The U-Net is a fully convolutional encoder-decoder network trained to map a noisy seismic gather $\mathbf{d}_\mathrm{noisy}$ to a denoised output $\hat{\mathbf{d}}_\mathrm{clean}$:

$$\hat{\mathbf{d}}_\mathrm{clean} = f_\theta(\mathbf{d}_\mathrm{noisy}), \qquad \theta^* = \arg\min_\theta \|\mathbf{d}_\mathrm{clean}^\mathrm{train} - f_\theta(\mathbf{d}_\mathrm{noisy}^\mathrm{train})\|^2$$

Skip connections between the encoder and decoder layers preserve fine spatial detail that would otherwise be lost in the downsampling path.

```{figure} ../../assets/figures/fig_dl_denoising_concept.png
:name: fig-dl-denoise-l9
:alt: Three-panel figure. Panel A shows a schematic U-Net architecture with the encoder (green boxes) on the left side going downward, a bottleneck (orange box), and the decoder (blue boxes) on the right side going upward. Red curved arrows show skip connections from encoder to corresponding decoder levels. The input noisy gather (light blue box, left) and output denoised gather (light blue box, right) are shown with arrows. Panel B shows a noisy synthetic CMP gather as variable-area wiggles (low SNR label in red). Panel C shows the denoised gather (improved SNR label in green) with cleaner-looking traces.
:width: 100%

**U-Net architecture for seismic denoising.** (A) Encoder-decoder with skip connections. (B) Noisy synthetic CMP gather (input). (C) Denoised output (band-pass filtering used as proxy; a real U-Net would learn the noise distribution from training data). Python-generated original figure.
```

### 9.2 Self-Supervised and Foundation Models

A limitation of supervised U-Nets is the need for paired clean/noisy training data, which is unavailable for real field datasets. **Self-supervised** methods (Birnie et al. 2021; Liu et al. 2022) train entirely on the observed (noisy) data by exploiting the statistical properties of noise — noise is spatially uncorrelated while signal is coherent.

**Seismic foundation models** (e.g. SeisFoundation, SegFM) are large pretrained vision transformers fine-tuned on seismic images. They can perform multiple tasks — denoising, horizon picking, facies classification — from a single model backbone, reducing the need for task-specific architectures.

**Seismic super-resolution** methods (Wang et al. 2022) train networks to learn the inverse of the seismic point-spread function, recovering spatial detail finer than the classical tuning-thickness limit $\lambda/4$.

### 9.3 Open Challenges

- **Domain shift:** networks trained on synthetic gathers frequently fail on field data because real noise is non-stationary and geologically correlated, unlike white-noise training data.
- **Physics inconsistency:** a denoised gather may violate reciprocity, polarity conventions, or amplitude-versus-offset relationships that were physically present in the original data.
- **Interpretability:** it is difficult to determine whether an amplitude anomaly in a DL-denoised section is a true DHI or a network artifact.

---

## 10. Course Connections

The dipping-layer travel-time equation (§3) is the direct extension of the flat-layer hyperbola from Lecture 8 ($\delta \to 0$ recovers Eq. {eq}`eq-l8-reflection-hyperbola`). The additional linear term motivates the DMO correction, which will be revisited in Lecture 10 as a special case of the migration operator.

Diffraction hyperbolae (§5) are the building block of Kirchhoff migration (Lecture 10, §3): migration collapses diffractions by summing amplitudes along the diffraction curve. Understanding diffraction is therefore prerequisite to understanding migration.

The AVO gradient $G$ (§7.1) involves $V_P/V_S$, which connects directly to the S-wave velocity constraints available from the gravity and magnetics modules (Lectures 18–21): density is related to both impedance ($Z = \rho V_P$) and AVO ($G$ depends on $\Delta\rho/\rho$).

---

## 11. Research Horizon

**Learned multiple suppression** (Dragoset et al. 2010; Xiong et al. 2023) uses deep learning in the $\tau$-$p$ domain to achieve adaptive subtraction without the wave-equation modelling required by SRME, reducing computational cost by 1–2 orders of magnitude.

**Sparse-shot acquisition and DL interpolation** (Mosher et al. 2023) train networks to reconstruct densely sampled shot gathers from sparse acquisitions, enabling 4D time-lapse surveys at a fraction of the traditional acquisition cost.

**Physics-informed AVO inversion** (Zhang et al. 2024) embeds Zoeppritz boundary conditions as hard constraints in a neural-network inversion, ensuring that the recovered $V_P/V_S$ profiles satisfy the governing physics rather than merely fitting the observed amplitudes.

---

## 12. Societal Relevance

The AVO Class III "bright spot" is the most widely used direct hydrocarbon indicator in exploration. False positive DHI identifications — attributing a bright reflection to gas when it is actually caused by a shallow coal seam, a hard carbonate layer, or a DL denoising artifact — have led to costly dry wells. The epistemics of AVO interpretation are therefore not merely academic: the $R(0)$–$G$ crossplot and its uncertainties directly inform decisions worth hundreds of millions of dollars and — in the context of carbon capture and storage (CCS) site characterisation — decisions affecting the long-term storage security of millions of tonnes of CO₂.

The Cascadia application: the updip extent of the décollement's seismic coupling is constrained in part by the impedance contrast between unconsolidated accretionary sediment and the overriding plate. Understanding whether a bright spot at the plate interface is a fluid-saturated zone (Class III AVO) or a hard carbonate cemented zone (Class I) affects estimates of seismic moment release and therefore the magnitude of a future Cascadia rupture.

---

```{admonition} AI Literacy — Epistemics: Interrogating a Seismic Interpretation
:class: seealso

Ask an AI assistant to interpret the following description of a seismic event: *"A bright, negative-polarity reflection at 1.8 s TWTT with amplitude that increases strongly with offset on a marine gather acquired over a Paleogene sandstone reservoir."*

The AI may produce a plausible-sounding interpretation ("likely a Class III AVO anomaly indicative of gas-saturated sand"). Before accepting this, apply the epistemics framework from the course:

1. **What evidence would distinguish this from a multiple?** (Compute: if it were a long-path multiple, what would its parent primary TWTT be? Does a primary exist at 0.9 s on the section?)

2. **What evidence would distinguish it from a hard kick at the base of a fast layer?** (A negative polarity can also come from impedance decreasing at depth — e.g. from dense limestone into soft shale.)

3. **What data would be needed to confirm the gas interpretation?** (Well control, fluid substitution modelling, 4D time-lapse survey for production-related changes, CSEM/MT resistivity data.)

The AI cannot access the actual section, well data, or acquisition geometry. Its interpretation is based on pattern matching to training data. Document: (a) what the AI identified correctly as constraints; (b) what the AI failed to flag as an alternative explanation; (c) what additional data the AI suggested (or failed to suggest). Record in your Geophysical Reasoning Portfolio as the AI epistemics entry for Week 3.
```

---

## Further Reading

- {cite:t}`lowrie2020fundamentals` — Ch. 6, §6.5: dipping layers, multiples. Free via UW Libraries.
- {cite:t}`shuey1985` — Shuey, R.T. (1985). A simplification of the Zoeppritz equations. *Geophysics*, 50(4), 609–614. [doi:10.1190/1.1441936](https://doi.org/10.1190/1.1441936)
- {cite:t}`rutherford1989` — Rutherford, S.R. & Williams, R.H. (1989). Amplitude-versus-offset variations in gas sands. *Geophysics*, 54(6), 680–688. [doi:10.1190/1.1442696](https://doi.org/10.1190/1.1442696)
- {cite:t}`birnie2021` — Birnie, C., Chambers, K., Angus, D., & Stork, A. (2021). Analysis and application of unsupervised deep learning for seismic noise attenuation. *Geophysical Prospecting*, 69(8). [doi:10.1111/1365-2478.13095](https://doi.org/10.1111/1365-2478.13095)
- {cite:t}`verschuur2013` — Verschuur, D.J., Berkhout, A.J., & Wapenaar, C.P.A. (1992). Adaptive surface-related multiple elimination. *Geophysics*, 57(9), 1166–1177. [doi:10.1190/1.1443330](https://doi.org/10.1190/1.1443330)

---

## References

```{bibliography}
:filter: docname in docnames
```
