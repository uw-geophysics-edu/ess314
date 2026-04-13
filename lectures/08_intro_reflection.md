---
title: "Introduction to Seismic Reflection: Flat-Layer Travel Time, NMO, and CMP Stacking"
week: 3
lecture: 8
date: "2026-04-15"
topic: "Reflection coefficient, flat-layer hyperbola, NMO correction, RMS velocity, Dix equation, semblance velocity analysis, CMP stacking"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4", "LO-5"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-B", "LO-OUT-C", "LO-OUT-D"]
open_sources:
  - "Lowrie & Fichtner 2020 Ch. 6 §6.1–6.4 (free via UW Libraries)"
  - "Sheriff & Geldart 1995 Ch. 4 §4.1, Ch. 5 §5.1–5.4 (cite only)"
  - "Yilmaz 2001 Seismic Data Analysis Ch. 1–2 (open excerpt via SEG)"
---

# Seismic Reflections I: Flat-Layer Travel Time, NMO, and CMP Stacking

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_08_slides.html" target="_blank">open in new tab ↗</a>
:::

:::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-8.1]** Define acoustic impedance and derive the normal-incidence reflection and transmission coefficients from boundary conditions; compute the energy reflection coefficient.
- **[LO-8.2]** Derive the flat-layer reflection travel-time hyperbola $t^2(x) = t_0^2 + x^2/V_1^2$ from the image-point construction; identify $t_0$, $V_1$, and $h$ in the equation.
- **[LO-8.3]** Define the NMO correction, apply it to a CMP gather, and explain quantitatively why stacking NMO-corrected traces improves SNR.
- **[LO-8.4]** State the definition of RMS velocity and apply the Dix equation to recover interval velocities from stacking velocities of successive reflectors.
- **[LO-8.5]** Describe how a semblance panel is constructed and interpret a velocity spectrum to pick stacking velocities.

:::::

:::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1 (reflection coefficient physics), LO-2 (hyperbola derivation, NMO math, Dix equation), LO-3 (CMP stacking workflow), LO-4 (flat-layer assumptions), LO-5 (Lab 2 NMO exercise) |
| **Learning outcomes** | LO-OUT-A, B, C, D |
| **Prior lecture** | Lecture 7 — Seismic Refraction II (multi-layer models, dipping interfaces, delay-time method) |
| **Next lecture** | Lecture 9 — Seismic Reflections I (dipping layers, multiples, diffractions, AVO, f-k filtering) |
| **Lab connection** | Lab 2: apply NMO correction to a synthetic CMP gather; pick velocities from a semblance panel; stack and compare SNR |

:::::

## Prerequisites

Students should be comfortable with acoustic impedance ($Z = \rho V$), Snell's law at oblique incidence (Lecture 5), the concept of the CMP gather, and basic signal processing (Fourier transform, SNR definition). The refraction travel-time equation (Lectures 6–7) provides the contrasting context.

---

## 1. The Geoscientific Question

Seismic reflection surveys image the Earth by recording the echoes of controlled sources from subsurface interfaces. In contrast to refraction methods, which require the refracted wave to return along the surface and can only constrain velocity in the shallowest layers, **reflection surveys image structure at any depth** — from the shallow sedimentary column to the Moho and beyond.

The fundamental challenge is extracting signal from noise: reflected P-waves are typically 1–3 orders of magnitude weaker than the direct first arrival, and the same receiver array simultaneously records surface waves, head waves, and scattered energy. The **Common Midpoint (CMP) method** solves this by summing many redundant traces that share the same reflection point, boosting signal while averaging down incoherent noise.

The Cascadia subduction system provides the motivating application. High-resolution multichannel reflection profiles offshore Washington reveal the geometry of the accretionary wedge, the dipping décollement, and fluid-migration pathways — all resolved from reflection traveltimes using the methods developed in this lecture.

---

## 2. Reflection Physics

### 2.1 Acoustic Impedance

The **acoustic impedance** of a layer is the product of density $\rho$ and P-wave velocity $V_P$:

```{math}
:label: eq-l8-impedance
Z = \rho\, V_P \quad [\text{Pa·s/m} = \text{kg m}^{-2}\text{s}^{-1}]
```

Impedance contrasts cause reflections. A high-impedance layer (dense, fast rock) strongly reflects downgoing energy.

### 2.2 Normal-Incidence Reflection and Transmission

At normal incidence ($\theta = 0$), the **reflection coefficient** $R$ and **transmission coefficient** $T$ follow directly from boundary conditions (continuity of acoustic pressure and particle velocity):

```{math}
:label: eq-l8-rc
R = \frac{Z_2 - Z_1}{Z_2 + Z_1}, \qquad T = \frac{2 Z_2}{Z_1 + Z_2}
```

Note: $|R| \leq 1$ and the relationship $R + T \cdot (Z_1/Z_2) = 1$ conserves energy. Typical crustal interfaces have $|R| = 0.01$–$0.15$; the water–seafloor interface $|R| \approx 0.25$.

### 2.3 Energy Reflection and Transmission Coefficients

The fraction of **energy** (intensity) reflected and transmitted:

```{math}
:label: eq-l8-energy
\mathcal{R} = R^2, \qquad \mathcal{T} = 1 - R^2 = \frac{4 Z_1 Z_2}{(Z_1 + Z_2)^2}
```

For a typical sedimentary contrast ($R = 0.10$), only 1% of energy is reflected and 99% is transmitted — which is why reflections are weak and stacking is essential.

### 2.4 The Reflectivity Profile

A **synthetic seismogram** for a 1D layered Earth convolves the reflectivity series $r(t) = \{R_1, R_2, \ldots\}$ with the source wavelet $w(t)$:

$$d(t) = w(t) * r(t) = \sum_i R_i\, w(t - t_{0,i})$$

where $t_{0,i} = 2 z_i / V_i$ is the two-way travel time to reflector $i$. This **convolutional model** is the foundation of seismic interpretation: picking a reflector on a seismic section reads the acoustic impedance structure of the crust.

---

## 3. Acquisition Geometry and the CMP Method

### 3.1 Shot Gather and CMP Gather

A **shot gather** collects all receiver traces from a single source. Sources and receivers are arranged in a 2D line (or 3D grid), typically spaced $\Delta x = 12.5$–$25$ m. The **source–receiver offset** $x$ ranges from near-trace ($x \approx \Delta x$) to far-trace ($x \approx N\Delta x$).

A **CMP gather** collects all source–receiver pairs whose midpoint is at the same surface location $x_m$. If the subsurface is flat and horizontally homogeneous, every trace in a CMP gather reflects from the same subsurface point — directly below $x_m$ at depth $z = h$. This is the crucial geometric property that makes NMO stacking coherent.

The **CMP fold** $N_\mathrm{fold}$ is the number of traces in each gather. For a land line with source spacing $\Delta s$, receiver spacing $\Delta r$, and spread length $L = N\Delta r$:

$$N_\mathrm{fold} = \frac{L}{2\,\Delta s}$$

Modern marine surveys achieve fold of 60–240; dense land surveys may reach 300+.

### 3.2 Why Redundant Traces Matter

Each trace in a CMP gather has a different source-receiver offset, so it samples the reflector at a slightly different reflection angle. If reflections are the same on all traces (after accounting for travel time), they are coherent signal; ambient and instrumental noise is incoherent and averages to zero when traces are summed.

---

## 4. Travel Time for a Flat Horizontal Reflector

### 4.1 The Image-Point Construction

For a flat reflector at depth $h$ with velocity $V_1$ above it, the travel time from source at origin to surface receiver at offset $x$ (down-path + up-path) can be computed using the **method of images**: reflect the source through the interface to create an image source at $(0, -h)$. The total raypath length is the straight-line distance from the image source to the receiver:

$$\ell(x) = \sqrt{x^2 + (2h)^2}$$

### 4.2 The Reflection Hyperbola

Dividing by $V_1$:

```{math}
:label: eq-l8-hyperbola
t(x) = \frac{\sqrt{x^2 + 4h^2}}{V_1}
```

Squaring:

```{math}
:label: eq-l8-t2x2
t^2(x) = t_0^2 + \frac{x^2}{V_1^2}
```

where $t_0 = 2h/V_1$ is the zero-offset two-way travel time. This is the equation of a **hyperbola** in the $t$–$x$ plane, with:
- **Asymptotic slope** $\pm 1/V_1$ (straight lines at large $x$)
- **Vertex** at $(0, t_0)$
- **Curvature** controlled by $h/V_1$: deep reflectors are flatter hyperbolas

```{admonition} Key insight
:class: tip

Plotting $t^2$ vs $x^2$ transforms the reflection hyperbola into a **straight line** with slope $1/V_1^2$ and intercept $t_0^2$. This is the foundation of velocity analysis: a linear regression on $t^2$–$x^2$ simultaneously recovers $h = V_1 t_0 / 2$ and $V_1$.
```

---

## 5. Normal Moveout (NMO) Correction

### 5.1 Definition

The **normal moveout** is the incremental travel-time delay at offset $x$ relative to zero offset:

```{math}
:label: eq-l8-nmo-delta
\Delta t_\mathrm{NMO}(x) = t(x) - t_0 = \sqrt{t_0^2 + \frac{x^2}{V_\mathrm{NMO}^2}} - t_0
```

For small-to-moderate offsets ($x \ll V_\mathrm{NMO} t_0$, i.e. $x < h$), the Taylor expansion gives:

```{math}
:label: eq-l8-nmo-approx
\Delta t_\mathrm{NMO}(x) \approx \frac{x^2}{2\, V_\mathrm{NMO}^2\, t_0}
```

### 5.2 Applying NMO

The NMO correction shifts each trace in the CMP gather upward by $\Delta t_\mathrm{NMO}(x)$. After a **correct** NMO correction (using the true velocity $V_1$), all traces in the gather show the reflection at the same time $t_0$. The gather is then said to be **flattened**. Summing (stacking) the flattened traces:

- Coherent reflection energy adds constructively ($\propto N_\mathrm{fold}$)
- Incoherent noise averages down ($\propto \sqrt{N_\mathrm{fold}}$)
- Net SNR improvement: $\sqrt{N_\mathrm{fold}}$ (as in Lecture 9, Eq. {eq}`eq-l9-snr-fold`)

### 5.3 NMO Stretch

At large offsets, the NMO correction is asymptotically large; the corrected wavelet is stretched in time ("NMO stretch"). Stretched traces at offsets $x > x_\mathrm{mute}$ are discarded before stacking. The mute zone typically excludes $x/h > 1.0$–$1.5$.

---

## 6. RMS Velocity and the Dix Equation

For a stack of $N$ flat horizontal layers with interval velocities $V_i$ and one-way thicknesses $h_i$, the NMO velocity for the $n$-th reflector is the **root-mean-square (RMS) velocity**:

```{math}
:label: eq-l8-vrms
V_\mathrm{rms,n}^2 = \frac{\sum_{i=1}^{n} V_i^2\, \Delta t_i}{\sum_{i=1}^{n} \Delta t_i}
```

where $\Delta t_i = 2h_i/V_i$ is the two-way travel time within layer $i$.

### 6.1 The Dix Equation

Given the stacking velocities $V_\mathrm{rms,n}$ and $V_\mathrm{rms,n-1}$ for two adjacent reflectors at zero-offset TWTTs $t_{0,n}$ and $t_{0,n-1}$, the **interval velocity** of layer $n$ is:

```{math}
:label: eq-l8-dix
V_n = \sqrt{\frac{V_\mathrm{rms,n}^2\, t_{0,n} - V_\mathrm{rms,n-1}^2\, t_{0,n-1}}{t_{0,n} - t_{0,n-1}}}
```

This is the **Dix equation** (Dix, 1955). It converts stacking velocities (observable from NMO analysis) into interval velocities (geologically meaningful layer properties).

```{admonition} Limitation
:class: warning

The Dix equation is exact only for flat, horizontal, isotropic layers. It is an approximation for dipping, anisotropic, or laterally heterogeneous media — corrections for dipping layers are derived in Lecture 9.
```

---

## 7. Velocity Analysis: Semblance Panel

### 7.1 The Semblance Function

The **semblance** measures the coherence of the NMO-corrected CMP gather as a function of trial velocity $V$ and zero-offset time $\tau$:

```{math}
:label: eq-l8-semblance
S(V, \tau) = \frac{\left[\sum_{j=1}^{N} d_j\!\left(\tau + \Delta t_j(V)\right)\right]^2}{N \cdot \sum_{j=1}^{N} \left[d_j\!\left(\tau + \Delta t_j(V)\right)\right]^2}
```

where $d_j(t)$ is trace $j$, $N$ is the fold, and $\Delta t_j(V)$ is the NMO delay for trace $j$ using trial velocity $V$.

$S \in [0, 1]$: $S = 1$ when all traces are perfectly coherent (ideal signal); $S = 0$ for incoherent noise.

### 7.2 Reading a Semblance Panel

The semblance is computed over a grid of $(V, \tau)$ values and displayed as a colour image — the **velocity spectrum** or **semblance panel**. Picks are made at **local maxima** of $S$ corresponding to flat-layer reflectors:

- A **broad, smeared** semblance peak indicates low redundancy (few traces) or a complicated wavelet
- A **sharp, high-amplitude** peak indicates high fold and a well-resolved primary reflector
- Multiple peaks at the same $\tau$ may indicate **multiples** (with lower $V_\mathrm{NMO}$ than the primary)

```{admonition} Practical Rule
:class: tip

Velocity picks are made by following the **highest semblance** from shallow to deep. The velocity function typically increases with depth because deeper layers are faster. A sudden implausible velocity reversal usually indicates a multiple or noise.
```

---

## 8. CMP Stacking

### 8.1 The Stacking Operator

After NMO correction and muting, the stacked trace $s(t)$ at CMP location $x_m$ is:

```{math}
:label: eq-l8-stack
s(t) = \frac{1}{N_\mathrm{fold}} \sum_{j=1}^{N_\mathrm{fold}} d_j^\mathrm{NMO}(t)
```

where $d_j^\mathrm{NMO}(t) = d_j(t + \Delta t_j)$ is the NMO-corrected trace.

### 8.2 SNR After Stacking

Signal amplitudes add coherently while Gaussian random noise adds incoherently:

- Signal component: $A_s \cdot N_\mathrm{fold}$ after sum → amplitude $A_s$ after dividing by $N_\mathrm{fold}$
- Noise component: $A_n \sqrt{N_\mathrm{fold}}$ after sum → $A_n / \sqrt{N_\mathrm{fold}}$ after dividing

$$\mathrm{SNR}_\mathrm{stack} = \sqrt{N_\mathrm{fold}} \times \mathrm{SNR}_\mathrm{single}$$

For a 96-fold survey: SNR improvement of $\sqrt{96} \approx 10\times$. This is the primary motivation for the CMP method.

### 8.3 After Stacking: Post-Stack Processing

The stacked section is a **zero-offset approximation** to the subsurface. It is typically followed by:
1. **Deconvolution**: compress the wavelet to improve vertical resolution
2. **Post-stack migration**: collapse diffractions and reposition dipping events (Lecture 10)
3. **Seismic attribute extraction**: amplitude, frequency, phase for facies interpretation

---

## 9. Worked Example: Two-Layer NMO Analysis

**Setup:** Layer 1, $V_1 = 1800$ m/s, thickness $h_1 = 900$ m. Layer 2, $V_2 = 2600$ m/s, thickness $h_2 = 700$ m.

**Step 1: Zero-offset TWTTs**

$$t_{0,1} = \frac{2 \times 900}{1800} = 1.000 \text{ s}, \qquad t_{0,2} = 1.000 + \frac{2 \times 700}{2600} = 1.538 \text{ s}$$

**Step 2: RMS velocities** (using Eq. {eq}`eq-l8-vrms`)

$$V_\mathrm{rms,1}^2 = V_1^2 = 3.24 \times 10^6 \; \Rightarrow \; V_\mathrm{rms,1} = 1800 \text{ m/s}$$

$$V_\mathrm{rms,2}^2 = \frac{1800^2 \times 1.000 + 2600^2 \times 0.538}{1.538} = 4.20 \times 10^6 \; \Rightarrow \; V_\mathrm{rms,2} = 2048 \text{ m/s}$$

**Step 3: Recover $V_2$ with Dix** (Eq. {eq}`eq-l8-dix`)

$$V_2 = \sqrt{\frac{2048^2 \times 1.538 - 1800^2 \times 1.000}{0.538}} = 2600 \text{ m/s} \checkmark$$

```{admonition} Concept Check
:class: tip

1. A CMP gather has a reflector at $t_0 = 0.80$ s with NMO velocity $V_\mathrm{NMO} = 2200$ m/s. Estimate the depth to the reflector assuming a single flat layer.

2. How does the NMO correction change if you use a velocity that is 10% too high? Will the corrected gather be over-corrected or under-corrected? Sketch the resulting CMP gather geometry.

3. A semblance panel shows a peak at $(V = 2000 \text{ m/s},\; t_0 = 1.2 \text{ s})$ and another at $(V = 1500 \text{ m/s},\; t_0 = 2.4 \text{ s})$. The second peak has exactly twice the TWTT of the first and a lower velocity. What is the second event likely to be?

4. Reflectors 1 and 2 have $V_\mathrm{rms,1} = 1800$ m/s at $t_{0,1} = 0.6$ s and $V_\mathrm{rms,2} = 2100$ m/s at $t_{0,2} = 1.0$ s. Use the Dix equation to find $V_2$.
```

---

## 10. SOTA: Automated Velocity Analysis with Deep Learning

### 10.1 Traditional Velocity Picking

Traditional velocity analysis requires a geophysicist to manually pick semblance maxima for every CMP location — a time-consuming, subjective task in large 3D surveys with millions of CMPs.

### 10.2 CNN-Based Semblance Pickers

Convolutional neural networks (CNNs) trained on labelled examples from well-constrained areas learn to identify semblance maxima automatically. The network input is the semblance image; the output is a velocity-time curve. Published comparisons show CNN pickers match expert picks within 1–2% RMS velocity in production surveys.

### 10.3 Uncertainty Quantification

Modern DL velocity analysis uses **Bayesian neural networks** or **Monte Carlo Dropout** to output a probability distribution $p(V_\mathrm{NMO} \mid t_0)$ rather than a single pick. The uncertainty is largest at:
- High TWTTs (low semblance due to attenuation)
- Depths with multiple overlapping hyperbolas (complex geology)
- Locations far from well control

### 10.4 Open Questions

The DL picker is trained on a specific survey's noise characteristics and reflectivity. Performance drops when applied to a new basin (domain shift). Physics-constrained networks embed the Dix equation as a hard constraint, ensuring that inverted interval velocities produce the observed RMS velocities.

---

## 11. Course Connections

The flat-layer reflection hyperbola (§4) is the direct counterpart to the refraction travel-time line (Lectures 6–7): both can be plotted on $t^2$–$x^2$ axes to linearize the moveout, but refraction uses the linear slope beyond the crossover distance while reflection uses the parabolic portion at intermediate offsets.

The NMO-corrected stacked section is the standard input to post-stack migration (Lecture 10). The velocity field from semblance picking (§7) is also the primary input to pre-stack depth migration.

The Dix equation (§6) provides the **interval velocity** structure needed to convert TWTT sections to depth sections. This depth conversion is critical for geological interpretation and directly connects to the gravity and density models discussed in Lectures 18–22.

---

## 12. Societal Relevance

:::{admonition} Why It Matters Beyond the Classroom
:class: note

**Hydrocarbon Exploration and Net-Zero Transition:** CMP stacking and velocity analysis are the core steps in every commercial seismic processing workflow. While hydrocarbons remain the primary application, the same workflow now drives:
- **CO₂ storage monitoring** at sites like Sleipner (North Sea), where time-lapse reflection surveys track CO₂ plume migration
- **Geothermal exploration** in sedimentary basins: velocity structure and reflective stratigraphy guide well placement
- **Earthquake hazard** near Seattle: reflection profiling of the Seattle fault zone by USGS and UW researchers images the geometry of potentially M7+ fault segments at shallow depth

**Open Data:** These methods are demonstrated on the Mobil Viking Graben dataset (freely available from SEG Wiki) and the USGS Puget Sound reflection profiles (public domain, PNSN archive).
:::

---

## AI Literacy — Attribution and Reproducibility

:::{admonition} AI Prompt Lab
:class: tip

Ask an AI assistant: *"Explain how to pick NMO velocities from a semblance panel and then apply the Dix equation to get interval velocities. Show me a numerical example."*

Evaluate the response:

1. **Is the math correct?** Check the formula for $V_\mathrm{rms}^2$ — does it correctly weight by two-way travel time, not by thickness?

2. **Is the Dix equation properly stated?** The formula involves $V_\mathrm{rms,n}^2 t_{0,n} - V_\mathrm{rms,n-1}^2 t_{0,n-1}$ in the numerator; does the AI's version match Eq. {eq}`eq-l8-dix`?

3. **Does the AI cite sources?** If it quotes specific numbers ("typical reflection coefficients are 0.05–0.15"), ask it to cite the reference. Is the claim verifiable?

4. **Reproducibility:** Can you reproduce the numerical example yourself from the formulas provided? Run the numbers from the worked example (§9) as a check.

Record: what the AI got right, what it got wrong, and one concept it failed to clarify that you had to look up.
:::

---

## Further Reading

1. Lowrie, W. & Fichtner, A. (2020). *Fundamentals of Geophysics*, 3rd ed. Ch. 6, §6.1–6.4. [Free via UW Libraries]
2. Dix, C.H. (1955). Seismic velocities from surface measurements. *Geophysics*, 20(1), 68–86. [doi:10.1190/1.1438126](https://doi.org/10.1190/1.1438126)
3. Sheriff, R.E. & Geldart, L.P. (1995). *Exploration Seismology*, 2nd ed. Ch. 4–5.
4. Yilmaz, Ö. (2001). *Seismic Data Analysis* (2 vols.). SEG. [Excerpt open via seg.org]
5. Biondi, B.L. (2006). *3D Seismic Imaging*. SEG Investigations in Geophysics No. 14.

```{bibliography}
:filter: docname in docnames
```
