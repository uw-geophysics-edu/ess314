---
title: "Seismic Refraction II — Beyond the Flat Layer: Special Cases and Uncertainty"
week: 3
lecture: 11
date: "2026-04-13"
topic: "Seismic Refraction — Special Cases"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4", "LO-5", "LO-6"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-B", "LO-OUT-C", "LO-OUT-D", "LO-OUT-E"]
open_sources:
  - "Lowrie & Fichtner 2020 Ch. 3 (UW Libraries)"
  - "Sheriff & Geldart 1995 §4.3–4.5 (cite only)"
  - "Telford, Geldart & Sheriff 1990 Applied Geophysics (cite only)"
  - "Reynolds 2011 An Introduction to Applied and Environmental Geophysics Ch.5 (cite only)"
  - "IRIS/EarthScope Education Resources: Refraction Seismology"
  - "Haeni 1988 USGS Open-File Report 88-296 (public domain)"
---

:::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-2]** Derive the travel-time equation for head waves in a multi-layer horizontal model and generalize it to $N$ layers.
- **[LO-1]** Explain why low-velocity zones and thin intermediate layers produce diagnostic blind spots in refraction surveys, and predict qualitatively how each pathology manifests in the $T$-$x$ record.
- **[LO-2]** Derive the travel-time equations for head waves from a single dipping interface (down-dip and up-dip), and relate the apparent velocities to the true refractor velocity and dip angle.
- **[LO-3]** Apply the delay-time method to compute depth to an irregular refractor from reversed-profile data.
- **[LO-4]** Critically evaluate the assumptions underlying each approximation and enumerate the principal sources of data uncertainty that limit model resolution.
- **[LO-5]** Implement a forward model in Python that predicts $T$-$x$ curves for multi-layer and dipping-interface geometries.

:::::

:::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1, LO-2, LO-3, LO-4, LO-5, LO-6 |
| **Learning outcomes practiced** | LO-OUT-A, LO-OUT-B, LO-OUT-C, LO-OUT-D, LO-OUT-E |
| **Prior lecture** | Lecture 9 — Seismic Refraction I (horizontal single-layer model, critical angle, $T$-$x$ straight-line interpretation) |
| **Next lecture** | Lecture 12 — Introduction to Seismic Reflection |
| **Lab connection** | Lab 3: Refraction — students fit multi-layer models to real field shot gathers |

:::::

## Prerequisites

Students should be comfortable with: the critical angle condition and derivation of the single-layer head-wave travel-time equation ($t = x/V_2 + 2h_1\cos\theta_{ic}/V_1$); Snell's law in vector and scalar form; the concept of apparent velocity; and basic Python array operations.

---

## 1. The Geoscientific Question

The refraction surveys described in Lecture 9 assumed the simplest possible Earth: a single horizontal layer overlying a faster half-space. Real near-surface geology is far more complex. The Cascadia forearc, the glacially reworked lowlands of the Puget Sound region, the Columbia River Basalt province — all present geologists and engineers with subsurface architectures that include multiple distinct velocity units, layers that thin laterally, interfaces that dip, and zones where velocity decreases with depth. Each of these configurations leaves a distinctive signature in the $T$-$x$ diagram, and each produces a different class of interpretive ambiguity.

The motivating question is therefore two-fold. First, can the analytical framework developed for the single-layer case be extended systematically to more realistic Earth models? Second — and crucially — what are the limits of that framework? When refraction surveying is used to site a dam foundation, assess liquefaction potential, or map the depth to bedrock beneath a future highway corridor, the cost of misinterpreting a low-velocity zone or a hidden thin layer is not merely academic. Understanding model non-uniqueness and data uncertainty is as important as knowing the forward solution.

This lecture develops the generalized travel-time equations for multi-layer models, derives the dipping-interface solution from first principles, exposes the diagnostic failure modes of refraction analysis (the low-velocity zone problem, the thin-layer problem), and introduces the delay-time method for mapping irregular refractors. Throughout, sources of data uncertainty and their propagation into depth estimates are made explicit.

---

## 2. Governing Physics

### 2.1 The Head Wave as a Boundary-Traveling Disturbance

A head wave, or refracted wave, exists because at the critical angle $\theta_{ic} = \sin^{-1}(V_1/V_2)$ the refracted ray travels along the interface at velocity $V_2 > V_1$. This boundary-constrained propagation continuously re-radiates energy upward into the slower upper medium at the same critical angle. The physical mechanism is analogous to the Mach cone produced by a supersonic body: the refractor surface acts as a secondary source, and interference among secondary wavelets constructively reinforces the upward-going critically refracted wavefront.

```{admonition} Key Physical Insight
:class: important

The head wave exists **only** when $V_2 > V_1$. If the lower medium is slower than the upper medium ($V_2 < V_1$), no critical angle exists, and no head wave is generated at that interface. This is the physical basis of the low-velocity zone problem developed in Section 3.3.
```

### 2.2 The $N$-Layer Generalization

For a horizontally layered model with $N$ layers, the travel-time for the head wave refracted along the $n$-th interface ($n \geq 2$, with the refractor velocity $V_n$) is obtained by summing the slant-path transit times through each overlying layer and the horizontal propagation time along the refractor.

:::{math}
:label: eq:multilayer_tt

t_n(x) = \frac{x}{V_n} + \frac{2}{V_n} \sum_{i=1}^{n-1} h_i \frac{\sqrt{V_n^2 - V_i^2}}{V_i}

:::

where:

| Symbol | Meaning | Units |
|--------|---------|-------|
| $x$ | Source-receiver offset | m |
| $V_n$ | Velocity of the $n$-th refractor | m s$^{-1}$ |
| $V_i$ | Velocity of the $i$-th layer ($i < n$) | m s$^{-1}$ |
| $h_i$ | Thickness of the $i$-th layer | m |
| $t_n$ | Head-wave travel time for refractor $n$ | s |

This result reduces correctly to the single-interface equation when $n = 2$:

$$t_2(x) = \frac{x}{V_2} + \frac{2h_1}{V_2} \cdot \frac{\sqrt{V_2^2 - V_1^2}}{V_1} = \frac{x}{V_2} + \frac{2h_1 \cos\theta_{ic}}{V_1}$$

since $\cos\theta_{ic} = \sqrt{V_2^2 - V_1^2}/V_2$ by the identity $\cos(\sin^{-1}(V_1/V_2)) = \sqrt{1 - V_1^2/V_2^2}$.

The intercept time for the $n$-th head wave is:

$$t_{i_n} = \frac{2}{V_n} \sum_{i=1}^{n-1} h_i \frac{\sqrt{V_n^2 - V_i^2}}{V_i}$$

This is the time-axis intercept of the $1/V_n$-slope segment in the $T$-$x$ diagram. Given all layer velocities from slope measurements and all overlying intercept times, the layer thicknesses are solved sequentially from top to bottom: $h_1$ from $t_{i_2}$, then $h_2$ from $t_{i_3}$ using the already-known $h_1$, and so on.

The depth to the second interface follows by isolating $h_2$:

:::{math}
:label: eq:h2_solve

h_2 = \left[ t_{i_3} - \frac{2h_1}{V_3} \frac{\sqrt{V_3^2 - V_1^2}}{V_1} \right] \frac{V_3 V_2}{2\sqrt{V_3^2 - V_2^2}}

:::

```{figure} ../../assets/figures/fig_multilayer_traveltime.png
:name: fig-multilayer-traveltime
:alt: Two-panel figure. Top panel: travel-time vs. offset diagram showing three straight-line segments with slopes 1/V1 (solid black line), 1/V2 (dashed blue line), and 1/V3 (dotted orange line), intersecting the time axis at intercept times t_i1=0, t_i2, and t_i3 respectively; the zone near the source where head waves have not yet overtaken the direct wave is shaded grey. Bottom panel: cross-section showing three horizontal layers labeled with velocities V1, V2 greater than V1, V3 greater than V2, and thicknesses h1 and h2, with the ray path E-A-B-C-D-F drawn as solid blue lines showing down-going ray through V1 layer, horizontal propagation along V2-V3 interface, and up-going ray through V1 layer.
:width: 85%

Three-layer horizontal model and its $T$-$x$ diagram. The ray path *EABCDF* is the head wave refracted along the second interface ($V_3$). The three linear segments have slopes $1/V_1$, $1/V_2$, and $1/V_3$; their time-axis intercepts yield the layer thicknesses via Eq. {eq}`eq:multilayer_tt`. The shaded region near the source is the shadow zone where the corresponding head wave has not yet overtaken the direct arrival.
[Python-generated: `fig_multilayer_traveltime.py`]
```

---

## 3. Pathological Cases — When the Simple Model Fails

The derivation above assumes that $V_1 < V_2 < V_3 < \cdots < V_n$ — a monotonically increasing velocity profile. Real near-surface geology routinely violates this assumption. The following cases describe the three most consequential departures, each of which introduces a characteristic interpretive error if unrecognized.

### 3.1 The Low-Velocity Zone (LVZ)

If a layer of velocity $V_2$ is sandwiched between an upper layer of velocity $V_1 > V_2$ and a lower layer of velocity $V_3 > V_1$, then $\sin\theta_{ic} = V_1/V_2 > 1$. No critical angle exists for the $V_1$-$V_2$ interface: rays incident from above are refracted *away* from the interface rather than along it, and no head wave is generated from this boundary.

The consequence for the $T$-$x$ record is severe. The LVZ is **invisible**: the observed diagram shows only two linear segments with slopes $1/V_1$ and $1/V_3$, identical in appearance to the record from a simple two-layer Earth with $V_1$ over $V_3$. The intercept time $t_{i_3}$, interpreted naively, yields a depth estimate that is larger than the actual depth to the $V_3$ refractor, because the travel-time correction for the slow intermediate layer ($V_2 < V_1$) is underestimated. The interpreted $V_3$ refractor depth is therefore systematically too deep, and the existence of the LVZ is entirely suppressed from the refraction record alone.

```{figure} ../../assets/figures/fig_lvz_traveltime.png
:name: fig-lvz-traveltime
:alt: Two-panel figure. Top panel: cross-section with three layers. Upper layer labeled h1=5m, V1=1000 m/s shown as light grey. Middle layer labeled h2=10m, V2=500 m/s shown as medium grey with dashed outlines indicating refracted rays that cannot travel critically along the first interface. Lower half-space labeled V3=4000 m/s shown as dark grey. Arrows indicate rays passing through the upper and lower layer but bending away at the middle interface. Bottom panel: travel-time vs. offset plot with two linear segments only; slope 1/V1 black solid and slope 1/V3 orange dashed, with a single intercept time t_i labeled. The absence of a 1/V2 segment is highlighted with a grey annotation box reading 'LVZ hidden'.
:width: 85%

The low-velocity zone problem. When $V_2 < V_1$, no critical refraction occurs at the first interface, no head wave from the $V_2$ layer is recorded, and the $T$-$x$ diagram is indistinguishable from a simple two-layer geometry. The interpreted depth to $V_3$ is greater than the true depth.
[Python-generated: `fig_lvz_traveltime.py`]
```

The systematic depth error introduced by a LVZ of thickness $h_2$ and velocity $V_2 < V_1$ is:

$$\Delta h = h_2 \left( \frac{V_1}{V_3}\sqrt{V_3^2 - V_2^2} - \sqrt{V_3^2 - V_1^2} \right) / \sqrt{V_3^2 - V_1^2}$$

Within the active seismic toolkit, three methods can expose what P-wave first-arrival refraction cannot see.

**Seismic reflection** is the most direct remedy: reflected waves require only an acoustic impedance contrast ($Z_2 = 
ho_2 V_2 
eq 
ho_1 V_1$), not a velocity increase. A LVZ interface produces a reflection regardless of whether $V_2 < V_1$ or $V_2 > V_1$, so seismic reflection surveys directly image boundaries that are invisible to refraction. This is why shallow reflection is routinely paired with refraction in site investigations where velocity inversions are suspected.

**Refraction traveltime tomography (SRT)** partially mitigates the LVZ problem by inverting the full first-arrival time dataset for a smooth continuous velocity model rather than fitting discrete head-wave segments. Because the tomographic inversion uses all arrivals — not just those that have undergone critical refraction — it is less susceptible to the blind-zone problem than slope-intercept analysis. However, ray coverage in LVZ regions is inherently sparse (rays are deflected around slow zones rather than through them), so tomography tends to underestimate the velocity contrast and may not resolve sharp, thin LVZs; this limitation was confirmed by a community blind test of near-surface refraction methods {cite}`zelt2013`.

**Multichannel Analysis of Surface Waves (MASW)** and related Rayleigh wave dispersion methods are the most powerful active seismic tool for directly imaging LVZs. Because the phase velocity of surface waves is governed by the shear modulus structure at depth — not by the head-wave condition — MASW has no requirement that velocity increase with depth. A velocity inversion that is completely invisible to P-wave first-arrival refraction produces a diagnostic signature in the Rayleigh wave dispersion curve {cite}`park1999`. MASW is therefore commonly deployed alongside P-wave refraction precisely in environments where velocity inversions are anticipated (saturated sediments, weathered bedrock, karst).

**S-wave refraction** is sometimes suggested on the grounds that $V_{P,2} < V_{P,1}$ does not necessarily imply $V_{S,2} < V_{S,1}$: in certain settings (e.g., gas-bearing sands, where compressional velocity drops dramatically while shear velocity changes little) an S-wave LVZ may not coincide with the P-wave LVZ. Where this condition holds, S-wave refraction can detect the interface that P-wave refraction misses. However, S-wave refraction is subject to the same fundamental constraint as P-wave refraction: it cannot generate a head wave when $V_{S,2} < V_{S,1}$, so it offers no general solution to the LVZ problem and must be used with geological judgment about whether a P-wave and S-wave velocity inversion are likely to decouple.

Independent non-seismic constraints — borehole velocity logs, outcrop mapping, gravity surveys, and DC resistivity — remain valuable complements to all of the above. Geologically, LVZs arise from saturated soft sediments overlying indurated rock, weathered zones within otherwise competent bedrock, or gas-bearing formations in the shallow subsurface.

### 3.2 The Thin Intermediate Layer

Even when $V_1 < V_2 < V_3$, the intermediate layer may be too thin to be detected. A head wave from the $V_2$ interface becomes the first arrival only over a crossover distance range:

$$x_{c,1} = 2h_1\sqrt{\frac{V_2 + V_1}{V_2 - V_1}}$$

and the corresponding range over which the $V_2$ head wave is first arrival before the $V_3$ head wave overtakes it is:

$$\Delta x_{c,12} = x_{c,2} - x_{c,1}$$

where $x_{c,2}$ is the crossover distance between $V_1$ and $V_3$. If $h_2$ is small, $\Delta x_{c,12}$ may be less than the station spacing, so the intermediate refractor never appears as a distinct first-arrival segment. The interpreter then fits only two slopes to the record, attributes all the delay to the uppermost layer, and produces an incorrect depth to the $V_3$ refractor — with an overestimate of $h_1$ and no indication that $V_2$ exists.

```{admonition} Rule of Thumb
:class: note

For reliable detection of a layer of velocity $V_n$ and thickness $h_n$ beneath a layer of velocity $V_1$, the station spacing $\Delta x$ must satisfy approximately $\Delta x \lesssim h_n \sqrt{(V_n - V_1)/(V_n + V_1)}$. For typical geologic ratios ($V_n/V_1 \sim 2$), this implies $\Delta x \lesssim 0.6 \, h_n$. Layers thinner than the station spacing will not be resolved.
```

### 3.3 The Dipping Interface

When the refractor is not horizontal but dips at angle $\delta$ to the horizontal, a single forward-shot profile produces an apparent velocity that depends on both the true refractor velocity and the dip. To recover the true velocity and dip, a reversed profile is required — sources deployed at both ends of the geophone array so that head waves are recorded propagating both down-dip and up-dip.

Define $d_A$ as the perpendicular distance from the source to the refractor, $d_B = d_A + x\sin\delta$ as the perpendicular distance from the receiver to the refractor, $V_1$ as the velocity of the overburden, and $V_2$ as the true refractor velocity. The critical angle is $\theta_{ic} = \sin^{-1}(V_1/V_2)$.

For a **down-dip** shot (source at the shallow end of the interface):

:::{math}
:label: eq:dipping_downdip

t_d(x) = \frac{x}{V_1}\sin(\theta_{ic} + \delta) + t_{id}

:::

where the intercept time is $t_{id} = 2d_A\cos\theta_{ic}/V_1$.

For an **up-dip** shot (source at the deep end):

:::{math}
:label: eq:dipping_updip

t_u(x) = \frac{x}{V_1}\sin(\theta_{ic} - \delta) + t_{iu}

:::

where $t_{iu} = 2d_B\cos\theta_{ic}/V_1$.

```{admonition} Key Equations: Dipping Interface Apparent Velocities
:class: important

The apparent velocities $\alpha_d$ (down-dip) and $\alpha_u$ (up-dip) measured from the $T$-$x$ slopes are:

$$\frac{1}{\alpha_d} = \frac{\sin(\theta_{ic} + \delta)}{V_1}, \qquad \frac{1}{\alpha_u} = \frac{\sin(\theta_{ic} - \delta)}{V_1}$$

Down-dip shooting yields an **overestimate** of the refractor velocity ($\alpha_d < V_2$), and up-dip shooting yields an **underestimate** ($\alpha_u > V_2$). The true velocity and dip are recovered from:

$$\delta = \frac{1}{2}\left[\sin^{-1}\!\left(\frac{V_1}{\alpha_d}\right) - \sin^{-1}\!\left(\frac{V_1}{\alpha_u}\right)\right]$$

For small dip angles ($\delta \lesssim 15$–$20°$):

$$\frac{1}{V_2} \approx \frac{1}{2}\left(\frac{1}{\alpha_d} + \frac{1}{\alpha_u}\right)$$
```

A fundamental consistency check for any reversed profile is the **reciprocal time**: the travel time from source $A$ to the far end of the geophone array must equal the travel time from source $B$ to the near end — both measuring the same distance at the same apparent velocity. If the reciprocal times do not match, there is either a timing error in the field data or a lateral velocity variation that violates the layered-Earth assumption.

```{figure} ../../assets/figures/fig_dipping_interface_reversed.png
:name: fig-dipping-interface-reversed
:alt: Three-panel figure. Top left panel: cross-section labeled (a) showing a horizontal interface at 20m depth with V1=500 m/s above and V2=1500 m/s below; two hammer symbols at the ends of the geophone array; black arrows showing refracted ray paths. Top right panel: cross-section labeled (b) showing a dipping interface at 4-degree dip with the same velocity values; refracted ray paths shown. Bottom panel: travel-time vs. offset diagram showing four linear segments — forward and reverse direct arrivals both with slope 1/V1 as solid black lines; forward and reverse head-wave arrivals as blue and orange dashed lines respectively, with slope labels 1/V_app_down and 1/V_app_up; horizontal dashed line at top showing that reciprocal times are equal; the two head-wave lines are parallel for case (a) and non-parallel for case (b).
:width: 90%

Reversed refraction profiles over horizontal (a) and dipping (b) interfaces. For a horizontal interface, forward and reverse head-wave segments are parallel; apparent velocity equals true velocity. For a dipping interface, forward and reverse segments converge, yielding different apparent velocities $\alpha_d$ and $\alpha_u$ from which the true velocity and dip are recovered.
[Python-generated: `fig_dipping_interface_reversed.py`]
```

---

## 4. The Forward Problem

The forward problem for seismic refraction consists of predicting $T$-$x$ curves given a complete specification of layer velocities, thicknesses, and, in the dipping case, interface orientation. For a horizontally layered model the forward solution is analytic (Eq. {eq}`eq:multilayer_tt`). For irregular refractors, it must be computed numerically.

The complete forward model predicts:
- The **direct wave** arrival: $t_{dir}(x) = x/V_1$
- The **head wave** from each interface $n$: $t_n(x)$ via Eq. {eq}`eq:multilayer_tt`
- The **crossover distance** $x_{c,n}$ at which head wave $n$ overtakes the direct wave or the preceding head wave

For the two-layer case, the crossover distance between direct and head waves is:

$$x_{c} = 2h_1\sqrt{\frac{V_2 + V_1}{V_2 - V_1}}$$

At offsets $x < x_c$, the direct wave arrives first; at $x > x_c$, the head wave arrives first. The first-arrival time at any offset is therefore:

$$t_{FA}(x) = \min\!\left[t_{dir}(x),\; t_2(x),\; t_3(x),\; \ldots\right]$$

The companion notebook implements this forward model interactively, allowing students to explore how changes in layer thickness and velocity contrast affect the $T$-$x$ diagram:

```{seealso}
**Companion notebook:** `notebooks/Lab3-Refraction.ipynb` — Forward modeling of multi-layer refraction; interactive $T$-$x$ diagram; parameter sensitivity analysis.
```

---

## 5. The Inverse Problem

### 5.1 Slope-Intercept Inversion

Given observed first-arrival times as a function of offset, the standard refraction inversion proceeds as follows:

1. Identify linear segments in the $T$-$x$ diagram and fit them by least squares.
2. Extract slope = $1/V_n$ and intercept $t_{i_n}$ for each segment.
3. Solve sequentially for layer thicknesses using Eq. {eq}`eq:multilayer_tt` (or Eq. {eq}`eq:h2_solve` for the two-interface case).
4. In dipping-interface situations, use reversed-profile apparent velocities and Eqs. {eq}`eq:dipping_downdip`–{eq}`eq:dipping_updip` to recover true velocity and dip.

This procedure is linear in the intercept times once the velocities are known, which makes it computationally simple but sensitive to two sources of error: (i) picking error in the first-arrival times, and (ii) misidentification of the number of segments (which directly impacts the number of layers inferred).

### 5.2 The Delay-Time Method for Irregular Refractors

The slope-intercept method assumes piecewise-planar refractors. For surveys where the refractor depth varies smoothly but not linearly along the profile — a common situation over glacially sculpted bedrock or alluvial basins — the **delay-time method** provides a more appropriate framework.

The delay time $\delta t_G$ at a geophone position $G$ is defined as the additional transit time incurred by the ray traveling up through the overburden layer at $G$, relative to the time it would take to travel the same horizontal distance at refractor velocity $V_2$:

:::{math}
:label: eq:delay_time_def

\delta t_G = \frac{h_G}{V_1}\cos\theta_{ic} - \frac{h_G\tan\theta_{ic}}{V_2} = \frac{h_G\cos\theta_{ic}}{V_1}

:::

where the last equality uses $\sin\theta_{ic} = V_1/V_2$. This result states that the delay time is simply proportional to the overburden thickness at $G$, with proportionality constant $\cos\theta_{ic}/V_1$.

The depth to the refractor at $G$ is then recovered from the sum of forward and reverse delay times:

:::{math}
:label: eq:delay_time_depth

h_G = \frac{V_1 V_2}{2V_1 \cos\theta_{ic}} \left[\delta t_{F,G} + \delta t_{R,G}\right] = \frac{V_1 V_2}{2\sqrt{V_2^2 - V_1^2}}\left[\delta t_{F,G} + \delta t_{R,G}\right]

:::

where $\delta t_{F,G}$ is the delay time computed from the forward-shot record at $G$, and $\delta t_{R,G}$ from the reverse-shot record. The depth is plotted beneath each geophone position, producing a point-by-point refractor profile. This is graphically equivalent to drawing circular arcs of radius $h_G$ beneath each geophone and constructing the envelope surface tangent to all arcs.

```{figure} ../../assets/figures/fig_delay_time_method.png
:name: fig-delay-time-method
:alt: Two-panel figure stacked vertically. Top panel: cross-section with a gently undulating refractor boundary separating two layers V1 above and V2 below. Hammer symbols at the two ends labeled E_F (left) and E_R (right). Six geophone positions labeled G1 through G6 along the surface. Two sets of dashed lines show the forward ray path from E_F to each geophone via the refractor, and reverse ray paths from E_R to each geophone via the refractor. Vertical dashed lines from each geophone to the refractor labeled h_G. Bottom panel: the same cross-section but now showing circular arc segments of radius h_G centered beneath each geophone, drawn as dashed quarter-circles in blue (from forward delay times) and orange (from reverse delay times); the solid black line showing the refractor surface is the common tangent to all the arcs. Both layers are labeled with their velocities.
:width: 90%

The delay-time method for mapping an irregular refractor. The depth $h_G$ at each geophone is computed from Eq. {eq}`eq:delay_time_depth` using forward and reverse delay times. Circular arcs of radius $h_G$ are drawn beneath each geophone; the refractor surface is the common tangent (envelope) to all arcs.
[Python-generated: `fig_delay_time_method.py`]
```

### 5.3 Crossover Distance as a Diagnostic

The crossover distance between the $n$-th and $(n+1)$-th head wave segments indicates where those arrivals arrive simultaneously. In a multi-layer record, breaks or offsets in the slope pattern (a parallel segment shifted in intercept time, or a curved region between linear segments) are diagnostic of structural complications: a step in the refractor, a fault, or a zone of lateral velocity variation. These features cannot be uniquely resolved from a single forward-shot profile; reversed profiling or multiple shot points are required.

---

## 6. Worked Example: Puget Lowland Site Investigation

Consider a shallow refraction survey conducted across a Quaternary terrace in the Puget Lowland — a common scenario for dam-foundation investigations, liquefaction hazard assessment, or buried channel mapping in the Seattle metropolitan area. The site is interpreted to have three layers:

| Layer | Description | True velocity |
|-------|-------------|---------------|
| 1 | Loose fill and organic soil | $V_1 = 350$ m/s |
| 2 | Dense glacial outwash gravel | $V_2 = 1\,650$ m/s |
| 3 | Competent sandstone (Renton Fm.) | $V_3 = 4\,200$ m/s |

A 72-m geophone spread (24 geophones at 3 m spacing) records a forward shot. The following slopes and intercepts are read from the $T$-$x$ diagram:

| Segment | Slope (ms/m) | Velocity (m/s) | Intercept $t_i$ (ms) |
|---------|-------------|---------------|----------------------|
| Direct | 2.857 | 350 | 0 |
| Head wave $V_2$ | 0.606 | 1650 | 6.1 |
| Head wave $V_3$ | 0.238 | 4200 | 19.4 |

**Step 1:** Compute $h_1$ from the $V_2$ intercept time:

$$t_{i_2} = \frac{2h_1\cos\theta_{ic,12}}{V_1}, \quad \theta_{ic,12} = \sin^{-1}\!\left(\frac{350}{1650}\right) = 12.3°$$

$$h_1 = \frac{t_{i_2} V_1}{2\cos\theta_{ic,12}} = \frac{0.0061 \times 350}{2 \times 0.9770} = 1.09 \text{ m}$$

**Step 2:** Compute $h_2$ from the $V_3$ intercept time using Eq. {eq}`eq:h2_solve`:

$$\theta_{ic,13} = \sin^{-1}\!\left(\frac{350}{4200}\right) = 4.78°$$

$$h_2 = \left[0.0194 - \frac{2\times 1.09}{4200} \times \frac{\sqrt{4200^2 - 350^2}}{350}\right] \times \frac{4200 \times 1650}{2\sqrt{4200^2 - 1650^2}} \approx 14.6 \text{ m}$$

The bedrock surface lies approximately 15.7 m below the surface ($h_1 + h_2 = 1.09 + 14.6$ m).

```{admonition} Concept Check
:class: tip

**Q1.** If the outwash gravel layer ($V_2 = 1650$ m/s) did not exist — replaced instead by clay with $V_2 = 300$ m/s — how would the $T$-$x$ diagram appear, and how would the interpreted depth to bedrock compare with the true depth?

**Q2.** Suppose the hammer-source timing has an uncertainty of $\pm 1$ ms. Propagate this timing uncertainty through the $h_1$ calculation. Is the depth uncertainty acceptable for a dam-foundation application?

**Q3.** A reversed shot is fired from the far end of the array. The $V_3$ segment has a slope of 0.255 ms/m (apparent velocity 3921 m/s). Using the small-dip approximation, estimate the dip angle of the sandstone surface.
```

---

## 7. Uncertainty in Refraction Interpretation

Understanding the sources and magnitudes of uncertainty is as important as the forward equations themselves. The principal sources of error are:

**Picking uncertainty.** First arrivals in field records are identified by the onset of ground motion. In noisy records, picking errors of 0.5–2 ms are common. A 1 ms error in the intercept time propagates to a depth error of approximately $\delta h = V_1 \delta t / (2\cos\theta_{ic})$. For $V_1 = 500$ m/s and $\theta_{ic} = 20°$, a 1 ms error yields $\delta h \approx 0.27$ m — acceptably small for many applications. For deeper refractors with small velocity contrasts, the error can be several metres.

**Velocity gradient effects.** The derivation of Eq. {eq}`eq:multilayer_tt` assumes each layer is homogeneous. In reality, compaction and diagenesis produce velocity gradients. A gradient in the shallowest layer causes the $T$-$x$ direct-wave segment to curve upward rather than remain straight, systematically biasing intercept-time estimates.

**Lateral heterogeneity.** The delay-time and slope-intercept methods assume that velocity varies only with depth along the profile. A lateral velocity gradient (e.g., a buried channel or a fault with contrasting hanging-wall and footwall lithologies) modifies the apparent velocity of head-wave segments, producing an artifact that is indistinguishable from dip in a single-profile survey. Reversed profiles constrain — but do not eliminate — this ambiguity.

**Non-uniqueness.** Different combinations of layer velocities, thicknesses, and dip angles can produce $T$-$x$ curves that are indistinguishable within the noise level of a survey. This is the fundamental inverse problem: the data underconstrain the model. Common strategies for reducing non-uniqueness include using geological prior information (borehole logs, outcrop maps), collecting data from multiple shot points, combining refraction with reflection data, and integrating other geophysical methods (gravity, DC resistivity, or downhole logging).

---

## 8. Research Horizon

Near-surface velocity imaging has undergone a methodological revolution over the past decade, driven by the combination of dense ambient-noise recordings and machine-learning phase pickers. Key developments include:

- **Full-waveform inversion (FWI) of shallow seismic data**: Rather than picking only first arrivals, FWI minimizes the waveform misfit across the entire shot gather, recovering smooth velocity models that resolve both first-order interfaces and gradual transitions. See Virieux & Operto (2009) and the open-access tutorial by Köhn et al. (2012, CPC) for the mathematical framework.

- **Distributed Acoustic Sensing (DAS) refraction surveys**: Fiber-optic cables buried in urban environments record ambient seismic noise and active-source shots with centimetre-scale spatial sampling, enabling refraction imaging at unprecedented resolution in settings where traditional geophones cannot be deployed. Emily Wilbur's DAS research with PNSN is directly relevant here.

- **Machine-learning first-arrival pickers**: Phase-picking models (e.g., PhaseNet, EQTransformer) trained on earthquake waveforms transfer surprisingly well to shallow active-source gathers, reducing picking time from hours to seconds and providing automated uncertainty estimates. See Zhu et al. (2019, *Seismological Research Letters*).

---

## 9. Societal Relevance

Shallow seismic refraction is among the most widely deployed geophysical methods in geotechnical practice. In the Pacific Northwest, the technique is applied routinely to:

- **Liquefaction hazard assessment**: Mapping the depth to the water table and to competent bearing materials beneath Seattle neighborhoods built on Holocene deltaic and glaciolacustrine deposits.
- **Debris flow and landslide investigations**: Mapping the depth to bedrock on the steep volcanic slopes of Mount Rainier and the Cascades, where the bedrock-colluvium interface controls pore-pressure accumulation and slope failure initiation.
- **Transportation infrastructure**: The WSDOT and Sound Transit use refraction surveys to characterize the Renton Formation and Vashon Drift for tunnel and light-rail alignment in the Seattle basin.

A particularly instructive local case is the refraction characterization of the Seattle Basin sediment-bedrock interface, which controls site amplification of earthquake ground motions during Cascadia megathrust and crustal earthquake events. The Seattle Fault is directly imaged by near-vertical incidence refraction, with the sharp velocity contrast at the Crescent Formation basalt providing a strong head-wave arrival.

---

## AI Literacy: AI as a Reasoning Partner in Inverse Problems

:::{admonition} AI Prompt Lab — Checking Your Refraction Inversion
:class: tip

The refraction inverse problem involves algebraic manipulation of the intercept-time equations. AI tools can serve as a useful derivation-checking partner, but require careful evaluation.

**Prompt 1 (Derivation check):**
*"I am solving for layer thickness in a three-layer seismic refraction problem. My travel-time equation for the second head wave is $t_3 = x/V_3 + 2h_1\sqrt{V_3^2 - V_1^2}/(V_3 V_1) + 2h_2\sqrt{V_3^2 - V_2^2}/(V_3 V_2)$. Please derive the expression for $h_2$ in terms of the intercept time $t_{i_3}$, the already-known thickness $h_1$, and the layer velocities."*

Evaluate the AI response: Does it correctly handle the dimensional consistency? Does it isolate $h_2$ without introducing errors in the square-root factors? Verify the result by substituting back into the travel-time equation.

**Prompt 2 (Failure mode recognition):**
*"In a seismic refraction survey, the $T$-$x$ diagram shows only two straight-line segments (slopes $1/V_1$ and $1/V_3$) with no intermediate segment, even though a borehole nearby shows three distinct velocity units. What geological and interpretive explanations should a geophysicist consider?"*

Evaluate: Does the AI distinguish between the LVZ problem and the thin-layer problem? Does it mention lateral heterogeneity? Does it recommend specific additional data collection strategies?

**Evaluation criterion:** A reliable AI response to refraction questions will state the assumptions explicitly (horizontal layers, no lateral variation, monotonically increasing velocity) and flag when those assumptions may be violated. Responses that give only the "textbook" answer without noting its domain of validity should be treated with skepticism.
:::

---

## 10. Course Connections

This lecture connects to the following parts of the course:

- **Prior lectures:** The critical angle derivation (Lecture 7) and the single-layer $T$-$x$ equations (Lecture 9) are the direct precursors. The Snell's Law framework developed in Lecture 7 is applied here to the dipping-interface geometry.
- **Next lecture:** Lecture 12 (Seismic Reflection I) treats the same layered-Earth geometry but focuses on the reflection branch of the wavefield — the part of the wavefront that turns back at the interface rather than continuing along it.
- **Lab 3:** Students pick first arrivals from a real field shot gather from the Puget Lowland area, fit multi-layer models, and quantify the depth uncertainty from picking error.
- **Lecture 21 (Seismic Tomography):** The delay-time concept introduced here is a pedagogical precursor to tomographic ray-path integrals, where the "delay" accumulated along a ray through a heterogeneous medium plays an analogous role.
- **Cross-method connection:** The velocity contrasts that drive refraction head waves also control electrical resistivity contrasts, acoustic impedance contrasts for reflection, and density anomalies detectable by gravity. The same sediment-bedrock interface that produces a strong head wave also produces a gravity anomaly and an SP anomaly in DC resistivity surveys.

---

## Further Reading

All sources open-access or available via UW Libraries:

1. Haeni, F.P. (1988). *Application of seismic refraction methods in groundwater modeling studies in New England.* USGS Open-File Report 88-296. [Public domain] [https://pubs.usgs.gov/of/1988/0296/](https://pubs.usgs.gov/of/1988/0296/)

2. Sheriff, R.E. & Geldart, L.P. (1995). *Exploration Seismology*, 2nd ed. Cambridge University Press. §4.3–4.5. [UW Libraries]

3. Lowrie, W. & Fichtner, A. (2020). *Fundamentals of Geophysics*, 3rd ed. Cambridge University Press. Ch. 3. [UW Libraries, free access]

4. Palmer, D. (1980). *The Generalized Reciprocal Method of Seismic Refraction Interpretation.* Society of Exploration Geophysicists. [cite only]

5. Virieux, J. & Operto, S. (2009). An overview of full-waveform inversion in exploration geophysics. *Geophysics*, 74(6), WCC1–WCC26. [DOI: 10.1190/1.3238367]

6. Zhu, W. & Beroza, G.C. (2019). PhaseNet: A deep-neural-network-based seismic arrival-time picking method. *Geophysical Journal International*, 216(1), 261–273. [DOI: 10.1093/gji/ggy423] [arXiv:1803.03211]

7. IRIS/EarthScope Education: *Seismic Wave Animations and Educational Resources.* [https://www.iris.edu/hq/inclass](https://www.iris.edu/hq/inclass)

8. Zelt, C.A., Haines, S., Powers, M.H., Sheehan, J., Rohdewald, S., et al. (2013). Blind test of methods for obtaining 2-D near-surface seismic velocity models from first-arrival traveltimes. *Journal of Environmental and Engineering Geophysics*, 18(3), 183–194. [USGS Open-Access: https://pubs.usgs.gov/publication/70093890](https://pubs.usgs.gov/publication/70093890)

9. Park, C.B., Miller, R.D. & Xia, J. (1999). Multichannel analysis of surface waves. *Geophysics*, 64(3), 800–808. [DOI: 10.1190/1.1444590] — The foundational MASW paper; demonstrates LVZ detection via Rayleigh wave dispersion.

