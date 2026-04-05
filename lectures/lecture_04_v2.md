---
title: "Seismic Wave Types — The Basics"
week: 1
lecture: 4
date: "2026-04-02"
topic: "Body waves (P, S) and surface waves (Rayleigh, Love): what they are, how particles move, why S-waves cannot travel in fluids, and representative wave speeds across Earth materials"
course_lo: ["LO-1", "LO-2", "LO-4"]
learning_outcomes: ["LO-OUT-B", "LO-OUT-C", "LO-OUT-F"]
open_sources:
  - "Lowrie & Fichtner (2020) Ch. 3, §3.3.1–3.3.3 (free via UW Libraries)"
  - "MIT OCW 12.201 §4.6–4.9 (CC BY NC SA, ocw.mit.edu)"
  - "IRIS/EarthScope wave animations (CC BY, iris.edu/hq/inclass/animation)"
  - "USGS Earthquake Hazards, ShakeAlert (Public Domain, usgs.gov)"
---

# Seismic Wave Types — The Basics

## Syllabus Alignment

| | |
|---|---|
| **Course LOs addressed** | LO-1 (wave types as observables arising from elastic Earth properties), LO-2 (wave speeds predicted from moduli and density), LO-4 (evaluate why S-waves are absent in fluids — a testable physical prediction) |
| **Learning outcomes practiced** | LO-OUT-B (compute $V_P$, $V_S$, and $V_P/V_S$ from material parameters; apply S–P timing), LO-OUT-C (explain why each wave type exists physically, not just its formula), LO-OUT-F (decide which wave type a seismometer component records and why) |
| **Lowrie & Fichtner chapter** | Ch. 3, §3.3.1–3.3.3 |
| **Next lecture** | Lecture 5: Lab 1 — Introduction to Python |
| **Lecture 6** | Wavefronts and Rays |
| **Lab connection** | Lab 2: Seismic Ray Tracing (Week 2) |

---

## Learning Objectives

By the end of this lecture, students will be able to:

- **[LO-4.1]** *Classify* each seismic wave type (P, S, Rayleigh, Love) by its particle motion geometry, polarization, and propagation medium.
- **[LO-4.2]** *Explain* why S-waves cannot propagate in a fluid using a physical argument that goes beyond stating $\mu = 0$.
- **[LO-4.3]** *Compare* P-wave and S-wave speeds across representative Earth materials and identify what rock or fluid properties control each.
- **[LO-4.4]** *Apply* the S–P time difference method to estimate earthquake distance from a single seismogram.
- **[LO-4.5]** *Distinguish* Rayleigh from Love waves by particle motion and explain why Love waves require velocity layering while Rayleigh waves do not.

---

## Prerequisites

Students should be comfortable with:
- The wave equation and wave speeds $V_P = \sqrt{(\lambda+2\mu)/\rho}$, $V_S = \sqrt{\mu/\rho}$ (Lecture 3)
- The physical meaning of $\mu$ (shear modulus = resistance to shear deformation) and why $\mu = 0$ in fluids (Lecture 3)
- Vectors and directions in 3D (MATH 126)

---

## 1. The Geoscientific Question

On March 11, 2011, a magnitude 9.0 earthquake ruptured the seafloor off northeastern Japan. Within eight minutes, seismometers in Seattle recorded its arrival — a faint, high-frequency compression of the ground. Two minutes later, a stronger horizontal shake arrived. An hour later, a long, slow undulation rolled through, lasting for thirty minutes. These were not three separate events. They were three families of elastic waves — P, S, and surface — all generated at the same instant, all traveling through the same Earth, each arriving at a different time because each travels at a different speed and along a different geometric path.

This lecture answers a deceptively simple question: what are these wave types, why do they exist, and what does each one tell us? The answer flows directly from the wave equation derived in Lecture 3. That equation contains two independent solutions corresponding to two fundamentally different modes of elastic deformation — compressional and shear — and boundary conditions at the Earth's free surface introduce two more. By the end of this lecture, every seismogram you look at for the rest of the course will have a physical interpretation.

:::{admonition} The Central Insight
:class: important
All four seismic wave types emerge from the same equation of motion. Their differences in speed, particle motion geometry, and sensitivity to Earth structure are direct consequences of the elastic physics developed in Lecture 3 — not independent facts to be memorized.
:::

---

## 2. Governing Physics: The Helmholtz Decomposition

### 2.1 Separating Compressional from Shear Motion

The 3D vector equation of motion derived in Lecture 3 is:

$$
\rho\,\frac{\partial^2 \mathbf{u}}{\partial t^2}
= (\lambda + 2\mu)\,\nabla(\nabla\cdot\mathbf{u})
- \mu\,\nabla\times(\nabla\times\mathbf{u})
$$ (eq:3d-eom)

Any vector field $\mathbf{u}$ can be written as the sum of a curl-free (irrotational) part and a divergence-free (rotational) part — the **Helmholtz decomposition**:

$$
\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}
$$ (eq:helmholtz)

Substituting into {eq}`eq:3d-eom` and separating terms, the single vector equation splits into **two independent scalar wave equations**:

$$
\frac{\partial^2 \phi}{\partial t^2} = V_P^2\,\nabla^2\phi
\qquad\text{(compressional wave, speed } V_P\text{)}
$$ (eq:p-wave-eq)

$$
\frac{\partial^2 \boldsymbol{\psi}}{\partial t^2} = V_S^2\,\nabla^2\boldsymbol{\psi}
\qquad\text{(shear wave, speed } V_S\text{)}
$$ (eq:s-wave-eq)

The wave equation does not generate two wave types arbitrarily — it *must* produce exactly two, because elastic deformation itself has exactly two independent modes: volume change and shape change.

### 2.2 Why Fluids Support Only One Type

In a fluid, $\mu = 0$. Then $V_S = \sqrt{\mu/\rho} = 0$: the shear wave equation {eq}`eq:s-wave-eq` has no propagating solution. The physical reason is not the formula but the mechanics: a shear wave requires the medium to exert a restoring force when it is shear-distorted. A fluid has no such restoring force — it flows. Molecules rearrange rather than spring back. The energy that would drive a shear wave instead drives viscous flow, which dissipates rather than propagates.

:::{admonition} Key Concept: Why No S-waves in Fluids
:class: important
An S-wave needs the medium to *resist shear distortion and spring back*. Fluids resist compression (finite $K$, $\lambda$) but not shear ($\mu = 0$). Without a shear restoring force, the transverse oscillation has nothing to sustain it. This is why the liquid outer core creates an S-wave shadow zone, why ocean water carries only P-waves (hydroacoustics), and why fluid-saturated sediments have anomalously high $V_P/V_S$.
:::

---

## 3. Body Waves: P and S

### 3.1 P-waves (Primary, Compressional, Longitudinal)

P-waves correspond to the compressional potential $\phi$ in {eq}`eq:helmholtz`. Their defining characteristic is that **particle motion is parallel to the propagation direction**: the medium alternately compresses (condensation) and expands (rarefaction) along the ray path.

Because $\lambda + 2\mu > \mu$ for any stable elastic material, $V_P > V_S$ always. P-waves therefore arrive first at any seismometer — hence "Primary." They exist in both solids and fluids.

:::{admonition} Notation
:class: note
| Symbol | Quantity | Units |
|--------|----------|-------|
| $V_P$ | P-wave speed $= \sqrt{(\lambda+2\mu)/\rho}$ | m/s |
| $V_S$ | S-wave speed $= \sqrt{\mu/\rho}$ | m/s |
| $V_R$ | Rayleigh wave phase speed $\approx 0.92\,V_S$ | m/s |
| $V_{L}$ | Love wave phase speed, $V_{S1} < V_L < V_{S2}$ | m/s |
| $\lambda_\text{dom}$ | Dominant wavelength $= V/f$ | m |
| $T$ | Wave period | s |
| $f$ | Frequency | Hz |
| $\Delta t_{SP}$ | S minus P arrival time difference | s |
:::

:::{figure} ../../assets/figures/fig_pwave_swave_motion.png
:name: fig-pwave-lec4
:alt: Two-panel figure. Top panel shows P-wave particle motion as alternating dark blue compression clusters and sky-blue rarefaction clusters of particles, with orange arrows showing displacement parallel to the horizontal propagation direction. Bottom panel shows S-wave particle motion as particles displaced transversely in a sinusoidal path perpendicular to the propagation direction, with a callout noting S-waves cannot travel in fluids because mu equals zero.
:width: 90%

**Figure 4.1.** P-wave (top) and S-wave (bottom) particle motions. The key distinction: P-wave displacement is *parallel* to propagation (longitudinal); S-wave displacement is *perpendicular* (transverse). Colors encode the compression state in the P-wave independently of the arrow direction. [Python-generated. Script: `assets/scripts/fig_pwave_swave_motion.py`]
:::

### 3.2 S-waves (Secondary, Shear, Transverse)

S-waves correspond to the shear potential $\boldsymbol{\psi}$. **Particle motion is perpendicular to the propagation direction.** S-waves carry more energy than P-waves for a given source and are responsible for most structural damage in earthquakes. They arrive second — hence "Secondary."

S-waves decompose into two orthogonal polarizations:

- **SV** (Vertical Shear): particle motion lies in the **vertical plane** containing the ray. SV waves can convert to P-waves at interfaces (mode conversion).
- **SH** (Horizontal Shear): particle motion is **horizontal and perpendicular** to the ray. SH waves do not convert to P at a horizontal interface. Love waves form from constructively interfering SH waves.

:::{figure} ../../assets/figures/fig_sv_sh_polarization.png
:name: fig-sv-sh
:alt: 3D perspective diagram of an S-wave propagating to the right. The horizontal propagation direction is labeled with an arrow. Two planes are shown: a vertical plane containing the propagation direction with a vertical double-headed arrow labeled SV, and a horizontal plane perpendicular to propagation with a horizontal double-headed arrow labeled SH. The full S-wave particle motion on the plane perpendicular to propagation shows both components. A label reads: total S-wave = SV plus SH.
:width: 72%

**Figure 4.2.** S-wave polarization geometry. The particle motion on the plane perpendicular to the ray decomposes into SV (in the vertical plane of the ray) and SH (horizontal, out of the vertical plane). [Python-generated. Script: `assets/scripts/fig_sv_sh_polarization.py`]
:::

:::{admonition} Figure Replacement Needed
:class: warning
**Original source (slide 22):** Telford, W.M. et al. (1990). *Applied Geophysics*, 2nd ed. Cambridge University Press. Fig. 2.8g. © W.W. Norton — **cannot be reused.**

**Scientific content:** 3D perspective of an S-wave showing the wavefront plane perpendicular to the ray, with SV and SH component arrows labeled. The wavefront is a vertical plane, the ray is horizontal.

**Replacement:** `fig_sv_sh_polarization.py` above generates an equivalent original Python figure. Run: `python assets/scripts/fig_sv_sh_polarization.py`
:::

### 3.3 The S–P Time Method

Because P and S waves travel the same path from source to receiver but at different speeds, the difference in their arrival times provides a direct estimate of the source distance. If a station is at distance $d$:

$$
\Delta t_{SP} = t_S - t_P = \frac{d}{V_S} - \frac{d}{V_P} = d\left(\frac{1}{V_S} - \frac{1}{V_P}\right)
$$ (eq:sp-time)

Solving for distance:

$$
d = \frac{\Delta t_{SP}}{\dfrac{1}{V_S} - \dfrac{1}{V_P}}
$$ (eq:sp-distance)

*Units check:* $[s] / [(s/m) - (s/m)] = [s] / [s/m] = [m]$ ✓

This technique requires only a single three-component seismometer and a clock — no array, no source information. It is the oldest and most robust distance estimator in seismology, still used in real time by PNSN and ShakeAlert.

---

## 4. Surface Waves: Trapped at the Free Surface

Body waves reaching the Earth's free surface encounter a boundary condition of zero traction (no forces act across the air–ground interface). This boundary condition permits new wave solutions that are confined to the near-surface region, decaying exponentially with depth, and that travel along the surface. These are **surface waves**.

Surface waves carry the largest amplitudes in most earthquake seismograms at teleseismic distances, persist long after body waves have passed, and are responsible for most tsunami generation and structural resonance in tall buildings.

### 4.1 Rayleigh Waves

Rayleigh waves couple P and SV motion. A particle traces a **retrograde ellipse** in the vertical plane containing the ray: as the crest passes, the particle moves backward (opposite to propagation) and upward; in the trough it moves forward and downward. The sense of rotation is retrograde — the same as the apparent rotation of the Sun as seen from Earth's surface.

Their phase speed is approximately:

$$
V_R \approx 0.92\,V_S
$$ (eq:vrayleigh)

(The exact value depends on Poisson's ratio; for $\nu = 0.25$, $V_R / V_S \approx 0.9194$.) Rayleigh waves exist in any homogeneous elastic half-space — they require no velocity layering.

Amplitude decays as $\sim e^{-kz}$ where $k = 2\pi/\lambda_\text{dom}$, becoming negligible below approximately $0.4\,\lambda_\text{dom}$. This depth sensitivity is the basis of **surface wave tomography**: long-period Rayleigh waves ($T \sim 100$ s, $\lambda_\text{dom} \sim 400$ km) sample the upper mantle; short-period waves ($T \sim 1$ s, $\lambda_\text{dom} \sim 3$ km) sample the shallow crust.

:::{figure} ../../assets/figures/fig_surface_waves.png
:name: fig-surface-waves-lec4
:alt: Three-panel figure. Left panel shows retrograde elliptical Rayleigh wave particle orbits at multiple depths, with large ellipses near the surface shrinking to small circles at depth. Center panel shows amplitude versus depth, decaying exponentially with a dashed line at 0.4 wavelength depth. Right panel shows Love wave geometry with a slow surface layer (sky blue) over a fast half-space (green), with dashed orange zigzag rays showing SH wave trapping by total internal reflection at the interface, and horizontal dot symbols on each ray segment showing transverse particle motion.
:width: 92%

**Figure 4.3.** Rayleigh wave: retrograde elliptical motion decaying to $\sim 0.4\,\lambda_\text{dom}$ depth (left, center). Love wave: formed by total internal reflection of SH waves in a slow surface layer (right). [Python-generated. Script: `assets/scripts/fig_surface_waves.py`]
:::

### 4.2 Love Waves

Love waves require **velocity layering**: a slow surface layer ($V_{S1}$) over a faster half-space ($V_{S2} > V_{S1}$). They are formed by SH waves that are totally internally reflected between the free surface and the layer interface, constructively interfering to produce a guided wave. Particle motion is **purely horizontal (SH)** — there is no vertical component.

Their phase speed lies between the two S-wave speeds:

$$
V_{S1} < V_L < V_{S2}
$$ (eq:love-speed)

Because Love waves cannot exist in a homogeneous half-space, their observation implies the presence of velocity structure. Like Rayleigh waves, Love waves are dispersive, and measuring their dispersion curve is a powerful constraint on $V_S(z)$.

:::{admonition} Key Comparison: Rayleigh vs. Love
:class: note
| Property | Rayleigh | Love |
|---------|---------|------|
| Motion | Retrograde ellipse (P + SV) | Horizontal transverse (SH only) |
| Speed | $\approx 0.92\,V_S$ | $V_{S1} < V_L < V_{S2}$ |
| Requires layering? | No | Yes |
| Vertical component? | Yes | No |
| Dispersion? | Yes | Yes |
| Recorded on | Vertical + horizontal | Horizontal only |
:::

---

## 5. Mathematical Framework: Wave Speeds and the $V_P/V_S$ Ratio

### 5.1 The $V_P/V_S$ Ratio as a Material Diagnostic

The ratio of P-wave to S-wave speed depends only on Poisson's ratio $\nu$:

$$
\frac{V_P}{V_S} = \sqrt{\frac{\lambda + 2\mu}{\mu}} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}
$$ (eq:vpvs-ratio)

For $\nu = 0.25$ (Poisson solid, typical crust): $V_P/V_S = \sqrt{3} \approx 1.73$

As $\nu \to 0.5$ (fluid-saturated or nearly incompressible): $V_P/V_S \to \infty$

This makes $V_P/V_S$ one of the most informative seismic observables:

- High $V_P/V_S$ (> 2): fluid saturation, high pore pressure, partial melt
- Low $V_P/V_S$ (< 1.6): gas sands, cracked dry rock, felsic crust
- $V_P/V_S \approx \sqrt{3}$: typical consolidated crustal rock

:::{figure} ../../assets/figures/fig_seismic_velocities.png
:name: fig-seismic-velocities-lec4
:alt: Horizontal bar chart with material names on the vertical axis and P-wave velocity in meters per second on the horizontal axis, from 0 to 8000. Dark blue bars for crystalline and sedimentary rocks range from 2000 to 6500 m/s. Sky-blue bars for unconsolidated sediments range from 60 to 2000 m/s. Green bars for fluids cluster between 1200 and 1540 m/s. Amber bars for engineering materials like steel and aluminum are between 5800 and 6400 m/s. A vertical dotted line marks 1480 m/s for water.
:width: 80%

**Figure 4.4.** Representative $V_P$ ranges for Earth and engineering materials. Note the three-order-of-magnitude span from dry clay ($\sim 60$ m/s) to steel ($\sim 6000$ m/s). Soft sediments can be 50× slower than basement rock — the origin of earthquake site amplification. [Python-generated. Script: `assets/scripts/fig_seismic_velocities.py`]
:::

---

## 6. The Forward Problem

Given elastic properties of a rock column — $V_P(z)$, $V_S(z)$, $\rho(z)$ — the forward problem predicts:

**Model parameters:** $V_P(z)$, $V_S(z)$, $\rho(z)$, layer interfaces

**Observables predicted:**
- Arrival time of P-wave at a seismometer at distance $d$: $t_P = d/V_P$
- Arrival time of S-wave: $t_S = d/V_S$
- S–P time difference: $\Delta t_{SP} = d(1/V_S - 1/V_P)$
- Which seismometer components record which wave (vertical ↔ P+Rayleigh, horizontal ↔ S+Love)
- Relative amplitudes of body vs. surface wave arrivals as functions of distance

See companion notebook: `notebooks/lecture_04_wave_types.ipynb`

---

## 7. The Inverse Problem

:::{admonition} Inverse Problem Setup
:class: tip
- **Data $d$:** P and S arrival times $t_P$, $t_S$ at a seismometer
- **Model $m$:** velocity structure $V_P(z)$, $V_S(z)$; source distance $d$
- **Forward relation:** $\Delta t_{SP} = d\,(1/V_S - 1/V_P)$
- **Key non-uniqueness:** $\Delta t_{SP}$ constrains the *product* of distance and velocity ratio, not each independently. An assumed crustal velocity model is required to convert $\Delta t_{SP}$ to distance.
- **Resolution limit:** For a single station, only distance is recoverable. Source location requires at least three stations (triangulation).
:::

---

## 8. Worked Example: Reading a Seismogram

A seismograph in Seattle records a P arrival at $t_P = 42.0$ s and an S arrival at $t_S = 74.8$ s after an earthquake. The regional crustal P-wave velocity is $V_P = 6.2$ km/s.

**Step 1 — Find $V_S$:**

Assuming a Poisson solid ($\nu = 0.25$, $V_P/V_S = \sqrt{3}$):

$$
V_S = \frac{V_P}{\sqrt{3}} = \frac{6.2}{\sqrt{3}} \approx 3.58 \text{ km/s}
$$

**Step 2 — S–P time difference:**

$$
\Delta t_{SP} = 74.8 - 42.0 = 32.8 \text{ s}
$$

**Step 3 — Distance:**

$$
d = \frac{32.8}{\dfrac{1}{3.58} - \dfrac{1}{6.2}} = \frac{32.8}{0.2793 - 0.1613} = \frac{32.8}{0.1180} \approx 278 \text{ km}
$$

Seattle to Portland is about 280 km. This is consistent with a Cascades volcanic arc source or a crustal earthquake near the Oregon border.

:::{admonition} Concept Check
:class: tip
1. A seismometer records only a P-wave arrival — no S-wave. List three physical reasons this could happen. (Hint: think about source location, wave propagation medium, and seismometer orientation.)
2. A seismogram shows $\Delta t_{SP} = 20$ s, and the station is known to be 120 km from the earthquake. What P-wave and S-wave velocities are implied? What crustal rock type is consistent with these velocities and with the $V_P/V_S$ ratio?
3. Why does the vertical component of a seismometer record P and Rayleigh waves but not Love waves? Answer using particle motion geometry, not just observation.
:::

---

## 9. Course Connections

- **Prior lecture (Lecture 3):** The wave equation derived in Lecture 3 generates these wave types through the Helmholtz decomposition. The Lamé parameters $\lambda$ and $\mu$ control which wave types exist ($\mu = 0$ kills S-waves) and at what speeds.
- **Lecture 6 (Wavefronts and Rays):** The geometric framework for tracing where these waves travel — Huygens' principle and ray theory.
- **Lecture 7 (Snell's Law):** What happens to these wave types at interfaces: reflection, refraction, mode conversion.
- **Lectures 9–11 (Seismic Refraction):** Using the travel-time differences between P-wave arrivals at different distances to image subsurface velocity structure — a direct application of the S–P method extended to arrays.
- **Lab 2 (Week 2):** Students will write Python code to compute $t_P(d)$, $t_S(d)$, and $\Delta t_{SP}(d)$ for a layered crustal model and plot travel-time curves.
- **Cross-topic:** The concept of wave speed depending on material stiffness and density reappears in acoustics (sound in fluids, P-waves only), optics (electromagnetic waves, different restoring force), and ocean waves (gravity waves, entirely different restoring force — buoyancy rather than elasticity).

---

## 10. Research Horizon

:::{admonition} Current Research Highlights (2022–2025)
:class: seealso

**Distributed Acoustic Sensing (DAS) and urban seismology.** DAS converts existing telecommunication fiber-optic cables into dense linear seismic arrays with meter-scale spacing. Because DAS records axial strain rather than ground velocity, it has different sensitivity to wave types: it is strongly sensitive to P-waves and Rayleigh waves propagating along the cable but less sensitive to SH and Love waves. Understanding this instrument response in terms of the wave-type physics from this lecture is an active research area. Recent work demonstrates DAS-based monitoring of shallow $V_S$ structure in urban settings using ambient noise Rayleigh waves on horizontal cables (Viens et al., 2023, *GJI*, doi:10.1093/gji/ggac420).

**Machine learning phase pickers and wave type identification.** Deep learning models (PhaseNet, EQTransformer) trained on millions of labeled picks now auto-identify P and S arrivals in real time on PNSN and global networks. The models work precisely because P and S waves have different waveform envelopes, frequency content, and particle motion geometries on three-component seismometers — the physics from this lecture. A critical ongoing question is whether these models generalize to unusual source types (volcanic, induced, glacial) where the P/S waveform characteristics differ from tectonic earthquakes.

**Surface wave tomography at city scale.** Passive seismic methods using ambient noise cross-correlation extract Rayleigh and Love wave Green's functions between pairs of stations without any earthquake. When dense arrays are deployed in cities (Seattle, Istanbul, Los Angeles), 3D $V_S$ models at 50–100 m resolution become achievable — sufficient to map individual fault zones and sedimentary basin edges. The depth sensitivity of Rayleigh waves ($\sim 0.4\,\lambda_\text{dom}$) derived in this lecture is the basis for multi-scale inversion strategies.

*Student entry point:* The IRIS Teachable Moments library (`iris.edu/hq/inclass`) includes wave animation tools and worksheets that directly illustrate P, S, Rayleigh, and Love wave particle motions. EarthScope's ObsPy tutorial notebooks on `seismo-live.org` demonstrate how to download and identify wave types on real seismograms.
:::

---

## 11. Societal Relevance

:::{admonition} Why It Matters: ShakeAlert and the Cascadia Scenario
:class: note

**Earthquake early warning depends on wave-type physics.** ShakeAlert, the USGS earthquake early warning system covering the Pacific Northwest and California, exploits the speed difference between P and S waves. The system detects the fast-arriving P-wave (which carries less energy but is measurable seconds earlier) and issues alerts before the slower, more damaging S-wave and surface waves arrive. For a Cascadia M9 rupture, P-wave detection could provide Seattle with 45–90 seconds of warning — enough time to open fire station doors, stop trains, pause surgeries, and move people away from windows.

The system works *only because* P-waves arrive first. If the Earth's crust were a fluid ($\mu = 0$), there would be no S-waves to warn about — but also no S-waves to damage buildings. The very material property that makes the Pacific Northwest vulnerable to seismic damage (crustal rock is elastic, transmits shear) is also what makes early warning possible.

**Seismometer components and what they record.** Emergency managers and engineers use seismometer data to assess shaking intensity. A vertical seismometer is most sensitive to P-waves and Rayleigh waves (both have vertical particle motion). Horizontal seismometers record S-waves and Love waves. Understanding which wave type dominates each component is essential for correctly interpreting peak ground acceleration (PGA) and peak ground velocity (PGV) — the quantities that determine structural damage.

**For further exploration:**
- ShakeAlert real-time status and PNW coverage map: `shakealert.org`
- PNSN live seismograms — try identifying P and S arrivals: `pnsn.org`
- IRIS wave animations — P, S, Rayleigh, Love: `iris.edu/hq/inclass/animation`
:::

---

## AI Literacy

:::{admonition} AI as a Tool: Phase Picking and Wave Type Identification (LO-7)
:class: seealso

Identifying the precise arrival time of P and S waves on a seismogram — **phase picking** — is foundational to nearly every seismological workflow: earthquake location, ShakeAlert, tomography, and hazard assessment all depend on accurate picks. Traditionally done by human analysts, this task is now largely automated using deep learning models.

**How the ML models work — and why the physics matters:**

Models like PhaseNet and EQTransformer are trained on millions of labeled three-component seismograms. They classify each time sample as P, S, or noise. The features they learn correspond to the wave physics from this lecture:

- P arrivals: onset on vertical component, higher frequency, impulsive
- S arrivals: onset on horizontal component, lower frequency, emergent
- The P-to-S polarity pattern on three components encodes the radiation direction

**In-class AI literacy activity:**

First, load a real seismogram in your head (or sketch one from the Concept Check above). Then ask an AI:

> *"I have a three-component seismogram from a magnitude 5 earthquake 200 km away. The vertical channel shows a sharp onset at 32 s, and the horizontal channels show a larger onset at 57 s. What wave types are these arrivals, and what can I estimate from the 25-second difference?"*

**Evaluate the response against this lecture:**
- Does it correctly identify the first arrival as P (vertical, 32 s) and the second as S (horizontal, 57 s)? ✅
- Does it apply the S–P formula {eq}`eq:sp-distance` correctly with a reasonable $V_P/V_S$ assumption? ✅
- Does it explain the *physical* reason the vertical and horizontal components show different arrivals (particle motion geometry)? This is the deeper answer. ✅ or ❌?
- Does it make up a specific rock type or give overconfident velocity values without acknowledging regional variability? ❌

**LO-7 connection:** Document your prompt and evaluate whether the AI answer would pass the Concept Check questions in §8. Note any errors or oversimplifications.
:::

:::{admonition} AI Prompt Lab
:class: tip

**Prompt 1 — Physical reasoning:**
> *"A seismologist records S-waves from shallow crustal earthquakes but not from deep earthquakes that have paths going through the Earth's outer core. Using only the physics of elastic wave propagation, explain why S-waves are absent on paths that go through the outer core."*

Evaluate: Does the AI correctly invoke $\mu = 0$ for the liquid outer core and explain the physical mechanism (fluids flow under shear, no restoring force)? Or does it just cite the S-wave shadow zone as a fact?

**Prompt 2 — Numerical check:**
> *"A seismic station records a P-wave arrival 28 seconds after an earthquake, and an S-wave 51 seconds after. Assuming Vp/Vs = sqrt(3) and Vp = 6.0 km/s, what is the distance to the earthquake? Show your calculation."*

Check the arithmetic: $\Delta t = 23$ s, $V_S = 3.46$ km/s, $d = 23 / (1/3.46 - 1/6.0) = 23/0.122 \approx 188$ km. Does the AI get this right?
:::

---

## Further Reading

Open-access sources used in preparing this lecture:

- **Lowrie, W. & Fichtner, A.** (2020). *Fundamentals of Geophysics*, 3rd ed. Cambridge University Press. §3.3.1–3.3.3. Free via UW Libraries. DOI: 10.1017/9781108685917
- **MIT OCW 12.201** (Van Der Hilst, 2004). Essentials of Geophysics §4.6–4.9: P-waves, S-waves, surface waves, particle motion. CC BY NC SA. URL: ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004
- **IRIS EarthScope Animations.** P-wave, S-wave, Rayleigh, Love — interactive particle motion animations. CC BY. URL: iris.edu/hq/inclass/animation
- **Viens, L. et al.** (2023). Understanding surface wave modal content for high-resolution imaging of submarine sediments with DAS. *Geophysical Journal International*, 232(3), 1668–1683. DOI: 10.1093/gji/ggac420
- **USGS ShakeAlert.** Earthquake early warning system, Pacific Northwest. Public domain. URL: shakealert.org
- **PNSN.** Pacific Northwest Seismic Network — live seismograms and educational resources. URL: pnsn.org

## References

```bibtex
@book{lowrie2020,
  author    = {Lowrie, W. and Fichtner, A.},
  title     = {Fundamentals of Geophysics},
  edition   = {3rd},
  publisher = {Cambridge University Press},
  year      = {2020},
  doi       = {10.1017/9781108685917}
}

@misc{mitocw12201,
  author = {Van Der Hilst, R.},
  title  = {12.201 Essentials of Geophysics, \S4.6--4.9},
  year   = {2004},
  note   = {MIT OpenCourseWare, CC BY NC SA},
  url    = {https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004}
}

@misc{iris_animations,
  title = {{IRIS EarthScope Seismic Wave Animations}},
  note  = {CC BY, accessed 2026},
  url   = {https://www.iris.edu/hq/inclass/animation}
}

@article{viens2023,
  author  = {Viens, L. and others},
  title   = {Understanding surface wave modal content for high-resolution imaging of submarine sediments with {DAS}},
  journal = {Geophysical Journal International},
  volume  = {232},
  number  = {3},
  pages   = {1668--1683},
  year    = {2023},
  doi     = {10.1093/gji/ggac420}
}
```
