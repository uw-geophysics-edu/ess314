---
title: "Seismic Wave Types and Ray Propagation"
week: 1
lecture: 4
date: "2026-04-09"
topic: "Body waves (P, S) and surface waves (Rayleigh, Love), particle motion geometry, seismic wave speeds, Huygens' principle, Snell's law and its geometric derivation, Fermat's principle, and critical refraction"
course_lo: ["LO-1", "LO-2", "LO-3"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-B", "LO-OUT-C"]
open_sources:
  - "Lowrie & Fichtner (2020) Ch. 3, §3.3 (free via UW Libraries)"
  - "MIT OCW 12.201 §4.6–4.10 (CC BY NC SA, ocw.mit.edu)"
  - "IRIS/EarthScope wave animations (CC BY, iris.edu)"
  - "Stein & Wysession (2003) §3.1–3.3 (cite only)"
---

# Seismic Wave Types and Ray Propagation

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_04_slides.html" target="_blank">open in new tab ↗</a>
:::

## Syllabus Alignment

| | |
|---|---|
| **Course LOs addressed** | LO-1 (wave types as observables arising from elastic Earth properties), LO-2 (Snell's law as forward model predicting ray geometry), LO-3 (inverse: inferring velocity structure from travel-time observations) |
| **Learning outcomes practiced** | LO-OUT-A (sketch a survey geometry and predict qualitatively how a velocity contrast affects ray paths), LO-OUT-B (compute travel-time differences, critical angles), LO-OUT-C (explain why S-waves cannot travel through fluids) |
| **Lowrie & Fichtner chapter** | Ch. 3, §3.3; Ch. 4 introduction |
| **Next lecture** | Lecture 5 — Reflection Seismology |
| **Lab connection** | Lab 2: Seismic Ray Tracing |

---

## Learning Objectives

By the end of this lecture, students will be able to:

- **[LO-4.1]** *Distinguish* P, S, Rayleigh, and Love waves by particle motion direction, polarization, and speed relative to $V_S$.
- **[LO-4.2]** *Explain* why S-waves cannot propagate in a fluid, connecting the physical argument ($\mu = 0$) to the material requirement for shear restoring force.
- **[LO-4.3]** *Apply* Huygens' principle to describe how a wavefront evolves as it encounters a velocity contrast.
- **[LO-4.4]** *Derive* Snell's law from wavefront geometry and apply it to predict refracted and reflected ray angles at a planar interface.
- **[LO-4.5]** *Calculate* the critical angle for total internal reflection and predict the geometry of head-wave arrivals.

---

## Prerequisites

Students should be comfortable with:
- The 1D wave equation and wave speeds $V_P = \sqrt{(\lambda+2\mu)/\rho}$, $V_S = \sqrt{\mu/\rho}$ (Lecture 3)
- Elastic moduli: $\mu = 0$ for fluids (Lecture 3)
- Basic trigonometry: Snell's law involves $\sin\theta$ and right-triangle geometry

---

## 1. The Geoscientific Question

An earthquake strikes off the coast of Oregon. Within 90 seconds, seismometers in Seattle record the first motion — a rapid compressional pulse. About 50 seconds later, a larger transverse shake arrives. Minutes later, a long, rolling disturbance rumbles through. These are not different earthquakes; they are the same energy release, partitioned into different wave types, each traveling at a different speed and carrying different information.

Why do these different wave types exist? Why does the ground shake differently in the transverse direction than in the vertical direction? And why — as the Cascadia earthquake scenario so vividly illustrates — does shaking intensity vary so dramatically between a bedrock site on Capitol Hill and a sediment site three kilometers away in Pioneer Square?

The answers require understanding the zoo of seismic wave types that emerge from the elastic wave equation, and the ray-optics framework that predicts how their paths bend as they encounter velocity contrasts. This lecture provides both.

:::{admonition} Key Connection to Lecture 3
:class: important
Every wave type in this lecture emerges from the same equation derived in Lecture 3: $\rho\,\partial^2 \mathbf{u}/\partial t^2 = (\lambda+2\mu)\nabla(\nabla\cdot\mathbf{u}) - \mu\nabla\times(\nabla\times\mathbf{u})$. The Helmholtz decomposition of this vector equation separates it into two scalar wave equations — one governing the irrotational (P-wave) component and one governing the rotational (S-wave) component.
:::

---

## 2. Governing Physics: Body Waves and Surface Waves

### 2.1 The Two Body Wave Types

The 3D vector equation of motion separates into two families. Any displacement field $\mathbf{u}$ can be written (Helmholtz decomposition) as the sum of a curl-free part (pure compression/dilation) and a divergence-free part (pure rotation/shear):

$$
\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}
$$ (eq:helmholtz)

where $\phi$ is the scalar potential (dilatational wave) and $\boldsymbol{\psi}$ is the vector potential (shear wave). Substituting into the equation of motion yields two independent wave equations:

$$
\frac{\partial^2\phi}{\partial t^2} = V_P^2\,\nabla^2\phi,
\qquad
\frac{\partial^2\boldsymbol{\psi}}{\partial t^2} = V_S^2\,\nabla^2\boldsymbol{\psi}
$$ (eq:two-wave-eqns)

These two equations describe the two body wave types.

**P-waves (Primary, Compressional, Longitudinal)**

P-waves are solutions to the dilatational wave equation. Particle motion is **parallel to the propagation direction** — the medium alternately compresses and expands, creating zones of compression (C) and rarefaction (R) along the ray path. P-waves travel at $V_P$ and are always the first seismic arrivals at a distant station.

**S-waves (Secondary, Shear, Transverse)**

S-waves are solutions to the shear wave equation. Particle motion is **perpendicular to the propagation direction**. S-waves come in two polarizations:
- **SV**: particle motion in the vertical plane containing the ray
- **SH**: particle motion horizontal, perpendicular to the ray

Because $\mu = 0$ in any fluid, the S-wave speed $V_S = \sqrt{\mu/\rho} = 0$, meaning **S-waves cannot propagate through any fluid** — water, magma, or the liquid outer core. This is not a mathematical coincidence; it reflects the physical fact that a fluid has no elastic restoring force to oppose transverse deformation: the molecules flow and rearrange rather than springing back.

:::{figure} ../assets/figures/fig_pwave_swave_motion.png
:name: fig-pwave-swave-lec4
:alt: Two-panel figure. Top panel shows P-wave particle motion as alternating clusters of close-spaced particles (compression, dark blue) and widely-spaced particles (rarefaction, sky blue) with orange arrows showing longitudinal displacement parallel to the propagation direction. Bottom panel shows S-wave motion as particles displaced transversely above and below the equilibrium line, tracing a sinusoidal path, with orange arrows showing perpendicular displacement and a callout box noting that S-waves cannot propagate in fluids because mu equals zero.
:width: 92%

**Figure 4.1.** P-wave (top) and S-wave (bottom) particle motions. Colors encode compression state in the P-wave (blue = compression, sky = rarefaction) independently of arrow direction. [Python-generated. Script: `assets/scripts/fig_pwave_swave_motion.py`]
:::

### 2.2 Surface Waves: Trapped Near the Free Surface

When body waves impinge on the Earth's free surface, boundary conditions (zero traction at the surface) allow new solutions that are bound to the surface and decay exponentially with depth. These are surface waves.

**Rayleigh Waves**

Rayleigh waves combine P and SV motion. Particles trace **retrograde ellipses** in the vertical plane containing the ray — moving backward and upward at the wave crest. Their phase speed is:

$$
V_R \approx 0.92\,V_S
$$ (eq:vrayleigh)

(The exact value depends weakly on Poisson's ratio.) Rayleigh waves exist in any homogeneous half-space and do not require velocity layering. Their amplitude decays as $\sim e^{-kz}$ (where $k = 2\pi/\lambda_\text{dom}$), becoming negligible below approximately $0.4\lambda_\text{dom}$.

**Love Waves**

Love waves require a velocity gradient: a slower surface layer over a faster half-space. They are formed by constructive interference of SH waves totally internally reflected between the free surface and the layer interface. Particle motion is purely horizontal (SH polarization). Love waves have no vertical component.

Both wave types are **dispersive**: their phase velocity depends on frequency (longer periods sample deeper, faster material). This frequency-dependent velocity is the basis for **surface wave tomography** — by measuring dispersion, one can infer $V_S(z)$.

:::{figure} ../assets/figures/fig_surface_waves.png
:name: fig-surface-waves-lec4
:alt: Three-panel figure. Left panel shows Rayleigh wave retrograde elliptical particle trajectories at multiple depths, with ellipses shrinking from large near the surface to small at depth. Center panel shows an amplitude-versus-depth curve decaying exponentially with a dashed line marking 0.4 wavelength and a label V_R approximately 0.92 V_S. Right panel shows a cross-section with a light blue slow surface layer over a green fast half-space with orange dashed zigzag rays illustrating SH wave trapping by total internal reflection, and dot symbols showing transverse particle motion.
:width: 92%

**Figure 4.2.** Surface waves: Rayleigh retrograde elliptical motion (left, center) and Love wave formation by SH trapping in a slow surface layer (right). [Python-generated. Script: `assets/scripts/fig_surface_waves.py`]
:::

---

## 3. Mathematical Framework

### 3.1 Notation

:::{admonition} Notation
:class: note
| Symbol | Quantity | Units | Type |
|--------|----------|-------|------|
| $V_P$, $V_S$ | P- and S-wave speeds | m/s | scalars |
| $V_R$ | Rayleigh wave speed | m/s | scalar |
| $\theta_1$, $\theta_2$ | Angle of incidence, refraction (from normal) | rad or ° | scalars |
| $p$ | Ray parameter (Snell's law invariant) | s/m | scalar |
| $\lambda_\text{dom}$ | Dominant wavelength | m | scalar |
| $T$ | Wave period | s | scalar |
| $f$ | Frequency | Hz = s⁻¹ | scalar |
| $k$ | Wavenumber $= 2\pi/\lambda_\text{dom}$ | m⁻¹ | scalar |
| $V_1$, $V_2$ | Wave speed in medium 1, medium 2 | m/s | scalars |
| $\theta_c$ | Critical angle | rad or ° | scalar |
:::

### 3.2 Typical P-wave Velocities

Wave speeds span nearly two orders of magnitude across Earth materials:

:::{figure} ../assets/figures/fig_seismic_velocities.png
:name: fig-seismic-velocities-lec4
:alt: Horizontal bar chart with material names on the vertical axis and P-wave velocity in meters per second on the horizontal axis from 0 to 8000 m/s. Bars are colored by category: dark blue for crystalline and sedimentary rocks (Granite, Basalt, Limestone, Sandstone, Salt rock, Shale) spanning roughly 2000 to 6500 m/s; sky-blue for unconsolidated sediments (Dry sand, Wet sand, Clay) with shorter bars from 60 to 2000 m/s; green for fluids (Seawater, Freshwater, Oil) near 1200 to 1540 m/s; and amber for engineering materials (Steel, Aluminum, Concrete, Ice).
:width: 82%

**Figure 4.3.** Representative $V_P$ ranges for Earth and engineering materials. Dry, unconsolidated sediments are extremely slow (60–270 m/s), causing severe ground-motion amplification. Crystalline rocks range from ~2000 to 6500 m/s. [Python-generated. Script: `assets/scripts/fig_seismic_velocities.py`]
:::

The key ratios to internalize:
- Typical crustal rock: $V_P \approx 5000$–$6500$ m/s, $V_S \approx 3000$–$3800$ m/s, $V_P/V_S \approx 1.73$ for $\nu = 0.25$
- Water: $V_P \approx 1480$ m/s, $V_S = 0$
- Soft sediment: $V_P \approx 200$–$1800$ m/s, $V_S$ as low as 60 m/s

### 3.3 Huygens' Principle

Huygens' principle states: every point on a wavefront can be treated as a secondary point source, radiating new spherical (or circular, in 2D) wavelets. The new wavefront at time $t + \Delta t$ is the surface tangent to all secondary wavelets.

This principle is not just a geometric construction — it is a consequence of the Green's function representation of the wave equation (Kirchhoff integral). For seismic wave propagation, it provides the geometric intuition behind:

1. Why plane waves remain plane in a homogeneous medium
2. Why wavefronts bend (refract) when the wave speed changes
3. Why energy spreads (geometrical spreading) as waves propagate away from a source

:::{figure} ../assets/figures/fig_snell_law.png
:name: fig-snell-law
:alt: Three-panel figure. Left panel shows Huygens' principle with a horizontal initial wavefront at time t-zero, secondary circular wavelets centered on each point source, and an envelope wavefront at t-zero plus delta-t above, with propagation arrows between the two wavefronts. Middle panel shows the geometric derivation of Snell's law with a medium 1 (blue shading) above an interface and medium 2 (green shading) below, an incident ray A to B with angle theta-1 from the normal, a refracted ray from B with larger angle theta-2, and a geometric construction labeling segments a-1-t and a-2-t on the two triangles. Right panel shows the general Snell's law with an incident P-wave, a reflected P-wave at the same angle, a refracted P-wave at larger angle in medium 2, and a converted refracted S-wave at smaller angle, all labeled with the generalized Snell's law equation.
:width: 95%

**Figure 4.4.** (a) Huygens' principle: wavefront evolution. (b) Geometric derivation of Snell's law. (c) General Snell's law: incident, reflected, refracted, and converted waves at a planar interface. [Python-generated. Script: `assets/scripts/fig_snell_law.py`]
:::

### 3.4 Snell's Law: Geometric Derivation

Consider a plane wave impinging on a planar interface between two homogeneous half-spaces with wave speeds $V_1$ and $V_2$. Let the wavefront strike point $B$ on the interface at time $t = 0$. At the same time, a second point on the wavefront is still in medium 1, at a distance $V_1 t$ from the interface.

In time $t$, the refracted wave in medium 2 has traveled distance $V_2 t$ from $B$. The new refracted wavefront must be tangent to both the secondary wavelet (radius $V_2 t$ from $B$) and the Huygens wavelet propagating in medium 1 from the second point.

Comparing the two triangles formed by the wavefront segments and the interface:

$$
\frac{BC}{AB} = \sin\theta_1 = \frac{V_1 t}{AB}
\qquad\text{and}\qquad
\frac{AE}{AB} = \sin\theta_2 = \frac{V_2 t}{AB}
$$

Taking the ratio and canceling $t/AB$:

$$
\frac{\sin\theta_1}{\sin\theta_2} = \frac{V_1}{V_2}
$$ (eq:snell-basic)

Rearranged into the canonical form:

$$
\frac{\sin\theta_1}{V_1} = \frac{\sin\theta_2}{V_2} = p
$$ (eq:snell)

:::{admonition} Key Equation: Snell's Law
:class: important
$$
\frac{\sin\theta_1}{V_1} = \frac{\sin\theta_2}{V_2} = p
$$
The quantity $p$ is the **ray parameter**, invariant along the entire ray path through any number of layers. It has units of s/m (= reciprocal of the horizontal phase velocity). A ray bends *toward* the normal when it enters a slower medium ($V_2 < V_1$, $\theta_2 < \theta_1$) and *away* from the normal into a faster medium — directly analogous to Snell's law in optics, with wave speed replacing the refractive index.
:::

*Units check:* $[\sin\theta] / [V] = \text{dimensionless}/(\text{m/s}) = \text{s/m}$ ✓

### 3.5 The General Snell's Law

At a real seismic interface, the incident wave generates four outgoing waves: reflected P, reflected S, refracted P, refracted S. All of these share the same ray parameter:

$$
\frac{\sin\theta_i}{V_{P1}} = \frac{\sin\theta_{P1r}}{V_{P1}} = \frac{\sin\theta_{P2}}{V_{P2}} = \frac{\sin\theta_{S2}}{V_{S2}} = p
$$ (eq:snell-general)

where subscripts indicate the medium and wave type. The critical point: use the *appropriate wave speed for the wave type and medium in which it travels*. An incident P-wave converts to an S-wave at the interface; the S-wave angle is governed by $V_{S2}$, not $V_{P2}$.

### 3.6 Fermat's Principle and Ray Tracing

Snell's law is a consequence of the more general **Fermat's principle**: a ray takes the path of stationary travel time between any two points. In a medium with velocity $V(x, z)$, the travel time along a ray path $\Gamma$ is:

$$
T = \int_\Gamma \frac{ds}{V(x,z)}
$$ (eq:fermat-integral)

where $ds$ is an infinitesimal arc length element. Setting $\delta T = 0$ (requiring the first variation to vanish) yields the ray equation, which in a layered medium reduces to Snell's law at each interface.

For a simple two-layer model — surface layer of velocity $V_1$ and thickness $H$, half-space of velocity $V_2 > V_1$ — the direct wave travel time is:

$$
T_\text{direct} = \frac{x}{V_1}
$$ (eq:direct)

The reflected wave travel time (hyperbolic moveout):

$$
T_\text{refl}(x) = \frac{\sqrt{x^2 + 4H^2}}{V_1}
$$ (eq:reflection-tt)

For small offsets $x \ll H$, this approximates to:

$$
T_\text{refl}(x) \approx \frac{2H}{V_1}\sqrt{1 + \frac{x^2}{4H^2}} \approx T_0\sqrt{1 + \frac{x^2}{V_1^2 T_0^2}}
$$ (eq:nmo)

where $T_0 = 2H/V_1$ is the zero-offset two-way travel time. This hyperbolic relationship is the foundation of reflection seismology.

### 3.7 Critical Refraction and Head Waves

When $V_2 > V_1$, there exists a critical angle $\theta_c$ at which the refracted ray travels exactly along the interface:

$$
\sin\theta_c = \frac{V_1}{V_2}
$$ (eq:critical-angle)

At this angle, the refracted ray ($\theta_2 = 90°$) grazes the interface and generates a **head wave** (also called a refracted wave or first-arrival wave) that travels along the interface at speed $V_2$ while continuously radiating energy back up into medium 1 at angle $\theta_c$.

The head wave travel time is:

$$
T_\text{head}(x) = \frac{x}{V_2} + \frac{2H\cos\theta_c}{V_1}
$$ (eq:head-wave)

The second term is the **intercept time** — the extra time to travel down and back up through the surface layer at the critical angle. The head wave overtakes the direct wave at the **crossover distance**:

$$
x_\text{cross} = 2H\sqrt{\frac{V_2 + V_1}{V_2 - V_1}}
$$ (eq:crossover)

:::{admonition} Key Concept: Head Waves and Refraction Surveys
:class: important
Head waves arrive *before* direct waves beyond the crossover distance. Their slope on a time–distance plot is $1/V_2$ (the deeper velocity), while the direct wave slope is $1/V_1$. By measuring these slopes and the intercept time, one can recover *both* $V_1$ (from direct arrivals) and $V_2$ (from refraction arrivals), and calculate the layer depth $H$ from the intercept time. This is the basis for seismic refraction surveying.
:::

---

## 4. The Forward Problem

Given a velocity model — $V_P(z)$, $V_S(z)$ as functions of depth — the forward problem predicts:

**Model parameters:** Layer velocities $V_1, V_2, \ldots$, layer thicknesses $H_1, H_2, \ldots$, interfaces depth and dip

**Observables predicted:**
- Travel-time curves $T(x)$ for direct, reflected, and refracted arrivals
- Critical distances and crossover distances
- Particle motion polarization and amplitude on seismograms

See companion notebook: `notebooks/lecture_04_ray_tracing.ipynb`

**Worked Example — S–P Time Method:**

A seismogram records $t_P = 42.0$ s and $t_S = 74.8$ s after an earthquake. Assuming $V_P = 6.2$ km/s and $V_P/V_S = \sqrt{3}$:

$V_S = 6.2/\sqrt{3} = 3.58$ km/s

$\Delta t = t_S - t_P = 32.8$ s

Distance $d$:

$$
d = \frac{\Delta t}{1/V_S - 1/V_P} = \frac{32.8}{1/3.58 - 1/6.2} = \frac{32.8}{0.279 - 0.161} = \frac{32.8}{0.118} \approx 278 \text{ km}
$$

---

## 5. The Inverse Problem

:::{admonition} Inverse Problem Setup
:class: tip
- **Data $d$:** Travel times $T(x)$ of direct, reflected, and refracted arrivals at an array of receivers
- **Model $m$:** Layer velocities $V_1, V_2, \ldots$ and thicknesses $H_1, H_2, \ldots$
- **Forward relation:** $d = G(m)$ via the travel-time equations {eq}`eq:direct`–{eq}`eq:head-wave`
- **Key non-uniqueness:** The same travel-time curve can be reproduced by different velocity–depth models, especially if velocity varies continuously rather than in discrete layers
- **Resolution limit:** Interfaces shallower than roughly one wavelength below the surface are poorly resolved by refraction; vertical velocity gradients are difficult to separate from interface depth
:::

---

## 6. Worked Example: Refraction Survey

A seismic refraction survey on the Olympic Peninsula measures:

- Direct wave slope: $1/V_1 = 1/1800$ s/m → $V_1 = 1800$ m/s (alluvial sediment)
- Refracted wave slope: $1/V_2 = 1/5400$ s/m → $V_2 = 5400$ m/s (basalt basement)
- Intercept time at $x=0$: $t_i = 0.085$ s

Solve for layer thickness $H$:

$$
H = \frac{t_i V_1}{2\cos\theta_c}
$$

where $\theta_c = \arcsin(V_1/V_2) = \arcsin(1800/5400) = \arcsin(0.333) = 19.5°$

$$
H = \frac{0.085 \times 1800}{2\cos(19.5°)} = \frac{153}{2 \times 0.943} = \frac{153}{1.886} \approx 81 \text{ m}
$$

Crossover distance:

$$
x_\text{cross} = 2 \times 81 \times \sqrt{\frac{5400 + 1800}{5400 - 1800}} = 162\sqrt{\frac{7200}{3600}} = 162\sqrt{2} \approx 229 \text{ m}
$$

At distances greater than 229 m, the refracted head wave arrives first — before the direct wave through the slow alluvium.

:::{admonition} Concept Check
:class: tip
1. A Love wave at period 10 s has phase velocity 3.2 km/s. At period 30 s, it has phase velocity 3.8 km/s. What does this tell you about how $V_S$ changes with depth? Estimate the depth sampled by each period. (Use depth $\approx 0.4\lambda = 0.4 V_R T$.)
2. A seismologist observes that S-waves from a distant earthquake are absent at a station directly antipodal to the source (on the opposite side of Earth). Using only the physics of this lecture, explain which property of the outer core is responsible. What does this imply about $\mu$ for the outer core?
3. Two layers: $V_1 = 2000$ m/s, $V_2 = 3500$ m/s, $H = 150$ m. (a) What is the critical angle? (b) What is the crossover distance? (c) At $x = 400$ m, which arrival — direct or head wave — arrives first? Show your calculation.
:::

---

## 7. Course Connections

- **Prior lectures:** The wave speeds $V_P$ and $V_S$ derived in Lecture 3 are the velocities $V_1$, $V_2$ in every formula in this lecture. Snell's law and Huygens' principle are the ray-geometric equivalents of the wave-equation physics.
- **Next lecture (Lecture 5):** Reflection seismology — the reflection travel-time curve and the Normal Moveout (NMO) correction derive directly from the hyperbolic travel-time equation {eq}`eq:reflection-tt`.
- **Lecture 7:** Tomography — the full 3D inversion of travel times for velocity structure. The ray parameter $p$ introduced here is the central quantity in teleseismic ray tracing.
- **Lab 2:** Students will write a Python ray tracer that computes direct, reflected, and refracted travel times for a layered model and plots $T(x)$ curves. The slope and intercept are then inverted for $V_1$, $V_2$, and $H$.
- **Cross-topic link:** Snell's law for seismic rays is mathematically identical to Snell's law for electromagnetic waves in optics, with wave speed replacing $c/n$. The same principle governs how gravity waves refract in the ocean and how light bends at a glass surface.

---

## 8. Research Horizon

:::{admonition} Current Research Highlights (2022–2025)
:class: seealso

**Ambient noise tomography and surface wave imaging.** Traditional surface-wave tomography required distant earthquakes. Since the early 2000s, it has been recognized that cross-correlating ambient seismic noise between station pairs extracts the Green's function between them — essentially creating a virtual source at every station. This technique, now mature, is being pushed to finer scales using dense nodal arrays (100s to 1000s of instruments in an area of a few km²), resolving shallow $V_S$ structure relevant to earthquake site effects at scales previously inaccessible. A major application is mapping the 3D shape of sedimentary basins like the Seattle Basin (Boaga et al., 2023, *BSSA*, doi:10.1785/0120220108).

**Distributed Acoustic Sensing (DAS) and head waves.** DAS converts existing telecommunication fiber into dense linear arrays of strain sensors. Because fiber records axial strain (not ground velocity), it is naturally sensitive to P-wave arrivals along the cable — including head waves from shallow interfaces. A new generation of refraction surveys using DAS cables in urban boreholes and submarine settings can image 10-meter-scale velocity contrasts that are invisible to sparse conventional arrays (Viens et al., 2023, *GJI*, doi:10.1093/gji/ggac420).

**Machine-learning phase pickers and Snell's law.** Modern seismological workflows use ML to automatically identify P and S arrivals (phase picking). The arrival-time differences between P and S — directly computed from Snell's law and the velocity model — are now used to retrain and calibrate these pickers in real time. The EarthScope Community Noise and Seismicity Explorer (CNSE) provides open access to waveform data and ML-based phase catalogs for classroom use.

*Student entry point:* The seismo-live library (`seismo-live.org`) has open Jupyter notebooks on ray tracing, travel-time computation, and seismic refraction — a direct hands-on implementation of this lecture's math.
:::

---

## 9. Societal Relevance

:::{admonition} Why It Matters: Subsurface Imaging for Infrastructure and Hazard
:class: note

**Shallow seismic refraction for geotechnical site characterization.** Before any large infrastructure project — a bridge foundation, a dam, a tunnel — engineers need to know the depth to bedrock and the shear wave velocity of the surface soils. A shallow seismic refraction survey (exactly the method in §3.7) provides both in hours for a few thousand dollars, compared to weeks and much higher cost for a drilling campaign. The $V_S$ measurement directly enters the building code site class determination (ASCE/SEI 7 uses $V_{S30}$ — the average shear wave velocity in the top 30 m — to set earthquake design forces). In Seattle, the difference between a Site Class B (rock, $V_{S30} > 760$ m/s) and Site Class E (soft soil, $V_{S30} < 180$ m/s) translates to roughly a factor of three difference in the earthquake design force for a structure — a profound economic consequence.

**ShakeAlert and real-time wave type identification.** ShakeAlert, the USGS earthquake early warning system for the Pacific Northwest and California, detects the fast-arriving P-wave (which carries less shaking energy) to issue alerts before the slower, more damaging S-wave and surface waves arrive. The success of the system depends on correctly distinguishing wave types in real time — exactly the physics of this lecture. For a Cascadia M9 earthquake, P-wave detection could provide 60–90 seconds of warning to Seattle, enough to stop trains, pause surgeries, and move people away from windows.

**For further exploration:**
- ShakeAlert system status and Pacific Northwest coverage: `shakealert.org`
- USGS site amplification factors and $V_{S30}$ maps: `earthquake.usgs.gov/hazards/vs30`
- PNSN live seismograms and ShakeAlert integration: `pnsn.org`
:::

---

## AI Literacy

:::{admonition} AI as a Tool: Machine Learning for Phase Picking
:class: seealso

Identifying the precise arrival time of P and S waves on a seismogram — **phase picking** — is one of the oldest and most labor-intensive tasks in seismology. A human analyst examines a waveform and places a pick: "the P arrived at 14:23:07.83 UTC." Multiply by millions of earthquakes and thousands of stations and it becomes impossible to do manually.

Deep learning models (PhaseNet, EQTransformer, GPD) trained on millions of labeled picks now achieve human-level accuracy on P arrivals and near-human accuracy on S arrivals. These are not black-box magic; they exploit the same physics from this lecture: P-waves produce compressional (vertical) first motions while S-waves produce shear (horizontal) first motions, and the waveform envelope shapes differ predictably.

**AI Prompt Lab — evaluating an AI explanation of phase picking:**

> *"Explain how a deep learning model like PhaseNet detects P and S wave arrivals on a seismogram. What features of the waveform does it use? How does the physics of P and S waves as described in the lecture help you understand why the model works?"*

Evaluate: Does the AI correctly note that P-wave arrivals typically show dominant vertical motion (SV) while S-arrivals show strong horizontal motion? Does it explain the role of the waveform's higher-frequency content (P-waves are generally higher frequency in near-source records)? Does it acknowledge uncertainty about what features the neural network has actually learned vs. what we hope it has learned?

**Epistemics prompt:**

> *"A ML phase picker labels an arrival as a P-wave with 97% confidence, but the arrival is on the horizontal component only. Is this consistent or inconsistent with P-wave physics? What might explain this?"*

Evaluate: Does the AI correctly flag the tension (P-waves should have dominant vertical motion at near-normal incidence; strong horizontal P is possible for steep incidence but should be noted) and suggest alternative explanations (converted wave, surface wave, instrument issue)?
:::

---

## Further Reading

- **Lowrie, W. & Fichtner, A.** (2020). *Fundamentals of Geophysics*, 3rd ed. Cambridge University Press. Ch. 3, §3.3; Ch. 4. Free via UW Libraries. DOI: 10.1017/9781108685917
- **MIT OCW 12.201** (Van Der Hilst, 2004). Essentials of Geophysics §4.6–4.10: Wave types, Huygens' principle, Snell's law, head waves. CC BY NC SA. URL: ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004
- **IRIS EarthScope Animations.** P-wave, S-wave, Rayleigh, Love, head wave — interactive visual animations. CC BY. URL: iris.edu/hq/inclass/animation
- **Viens, L. et al.** (2023). Understanding surface wave modal content for high-resolution imaging of submarine sediments with DAS. *Geophysical Journal International*, 232(3), 1668–1683. DOI: 10.1093/gji/ggac420
- **ShakeAlert.** USGS Earthquake Early Warning System — how P-wave detection enables early warning. Public domain. URL: shakealert.org

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
  title  = {12.201 Essentials of Geophysics, \S4.6--4.10},
  year   = {2004},
  note   = {MIT OpenCourseWare, CC BY NC SA},
  url    = {https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004}
}

@misc{iris_animations,
  title  = {{IRIS EarthScope Seismic Wave Animations}},
  note   = {CC BY, accessed 2026},
  url    = {https://www.iris.edu/hq/inclass/animation}
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
