---
marp: true
theme: ess314
html: true
paginate: true
math: mathjax
---

<!-- ============================================================
     ESS 314 — Lecture 1
     What Is Geophysics? Three Motivations, Five Physics Domains,
     and the Stakeholder Landscape
     Marine Denolle · University of Washington · March 31, 2026
     ============================================================ -->

<!-- Slide 1 — Title (UW purple, no background photo) -->
<!-- _class: title-slide -->

# What Is Geophysics?
### Three Motivations · Five Physics Domains · Stakeholder Landscape

**ESS 314 — Geophysics** | Lecture 1 | March 31, 2026
Marine Denolle · University of Washington

---

<!-- Slide 2 — Learning Objectives -->

# Learning Objectives

By the end of this lecture:

- **[LO-1.1]** State a precise definition of solid Earth geophysics and explain why indirect observation is the defining epistemological constraint
- **[LO-1.2]** Classify any geophysical study into geodynamics, hazards, or resource management — with process and observable named
- **[LO-4.1]** Identify the physics domain governing a given observable and the Earth property it senses
- **[LO-6.1]** Identify four stakeholder communities and their distinct requirements from geophysical knowledge

---

<!-- Slide 3 — Opening hook: Earth from ISS as motivation for "why geophysics"
     Photo: NASA ISS042-E-294596, public domain.
     Source: https://eol.jsc.nasa.gov/SearchPhotos/photo.pl?mission=ISS042&roll=E&frame=294596
     50% overlay handled by .bg-overlay class in ess314.css               -->
<!-- _class: bg-overlay -->
<!-- backgroundImage: url('https://assets.science.nasa.gov/dynamicimage/assets/science/esd/eo/images/imagerecords/86000/86041/iss042e294596.jpg?w=1280&h=853&fit=clip&crop=faces%2Cfocalpoint') -->
<!-- backgroundSize: cover -->

# A Planet We Can Only See the Surface Of

Everything we know about what lies beneath
was inferred — not sampled.

> *Seismic waves, gravity, magnetics, heat flow:*
> **physics as a telescope pointed inward.**

---

<!-- Slide 4 — The 1700 Cascadia event -->

# The Defining Constraint

**January 26, 1700 — the entire Cascadia fault ruptured**

- 1,300 km rupture — **no instrumental seismic record existed**
- Date reconstructed from:
  - Japanese tsunami records
  - Drowned coastal forests (tree rings stop 1699)
  - Coastal sand sheets from tsunami inundation
  - Indigenous oral traditions of Cascadia peoples

> Everything known about this event is geophysical inference from indirect evidence.

**Key point:** The inability to sample directly is not a technology failure — it is a permanent physical constraint.

---

<!-- Slide 5 — Definition -->

# Definition

$$\boxed{\text{Solid Earth Geophysics} = \text{Quantitative inference of Earth's interior from surface observations}}$$

Physical fields measured at or above the surface:

| Observable | Field | Earth property sensed |
|---|---|---|
| Seismograms | Elastic displacement | Velocity $\alpha$, $\beta$; density $\rho$ |
| $g$ anomaly | Gravitational acceleration | Density $\rho$ |
| Magnetic anomaly | **B** field | Remanent magnetization |
| Heat flux | $q = -k\,dT/dz$ | Thermal conductivity $k$ |
| GPS / InSAR | Surface displacement | Strain accumulation |

**Every observable is indirect.** The Earth property is always inferred through a physical model.

---

<!-- Slide 6 — Three motivating contexts -->

# Three Motivating Contexts

| Context | Physical Process | Key Observable |
|---------|-----------------|----------------|
| **Geodynamics** | Mantle convection, subduction, glacial rebound | Seismic velocity, gravity, heat flow |
| **Natural Hazards** | Fault rupture, wave propagation, site amplification | Seismograms, GPS, InSAR |
| **Resource Management** | Stratigraphy, fluid reservoirs, ore bodies | Seismic reflection, resistivity |

The same methods frequently serve multiple contexts simultaneously.

**Key point:** The motivation determines the required precision and what counts as a satisfactory answer.

---

<!-- Slide 7 — Geodynamics (figure slide) -->

# Geodynamics: How the Planet Works

![alt text: Schematic diagram showing three panels. Left panel: Earth cross-section with two convection cells in the mantle and a subducting plate. Center panel: map view of a fault trace with concentric shaking-intensity ellipses and a star at the epicenter. Right panel: seismic reflection section with wavy sedimentary horizons and a highlighted reservoir trap at depth.](../assets/figures/fig_three_motivations.png)
<span class="caption">Figure 1.1 — Three motivating contexts. Python-generated · <code>assets/scripts/fig_three_motivations.py</code></span>

- Juan de Fuca Plate subducts at ~3 cm/yr — **measured by GPS, not drilling**
- Slab geometry at depth — **imaged by seismic tomography, not sampling**

---

<!-- Slide 8 — Natural Hazards -->

# Natural Hazards: Physics for Public Safety

- **ShakeAlert** (Alaska → California): real-time P-wave detection → shaking estimate → warning before S-wave arrives
- Lead time: seconds to tens of seconds
  - Slow high-speed trains · open fire station doors · trigger industrial shutoffs

Uncertainty matters directly:

> Underestimate shaking → inadequate building design → casualties
> Overestimate shaking → wasted resources, public distrust

**Key point:** The wave propagation physics in Weeks 2–5 is the direct scientific foundation for this operational system.

---

<!-- Slide 9 — Resource Management -->

# Resource Management: Knowing What Is Underground

- Before drilling: **seismic reflection surveys** image stratigraphy kilometers below the seafloor
  - Marine airguns → elastic pulses → reflections off rock interfaces → subsurface image
- Same methods now serve the clean-energy transition:
  - Geothermal resource assessment
  - Critical minerals for batteries
  - CO₂ storage monitoring

Global exploration geophysics: **tens of billions of dollars annually**

**Key point:** The motivation changes (petroleum → climate); the physics does not.

---

<!-- Slide 10 — Five physics domains -->

# Five Physics Domains

| Domain | Governing Equation | Earth Property | Observable |
|--------|-------------------|----------------|------------|
| Continuum mechanics | $\rho\ddot{\mathbf{u}} = \nabla\cdot\boldsymbol{\sigma}$ | $\lambda, \mu, \rho$ | Seismograms |
| Wave theory | $\nabla^2 u = v^{-2}\partial_{tt}u$ | $\alpha, \beta$ | Travel times |
| Gravity | $\nabla^2\Phi = 4\pi G\rho$ | Density $\rho$ | $g$ anomaly |
| Electromagnetism | $\nabla\times\mathbf{B} = \mu_0\mathbf{J}$ | $\sigma_e$, magnetization | EM anomaly |
| Thermodynamics | $\rho c_p \partial_t T = \nabla\cdot(k\nabla T)$ | $T$, $k$ | Heat flux $q$ |

These equations will be derived in detail during each module.

**Key point:** Every observable connects to an Earth property through a physical operator. This is the forward problem.

---

<!-- Slide 11 — Passive vs Active (two-column) -->

# Passive vs. Active Surveys

<div class="columns">
<div>

**Passive** — measure natural signals
- No source cost; continuous; global
- Earthquakes, gravity, ambient noise, GPS
- Coverage limited by natural source distribution
- *Examples:* earthquake seismology, gravity, GPS

</div>
<div>

**Active** — generate controlled signals
- Full source control → higher resolution
- Expensive; requires permitting
- Explosions, vibroseis, airguns, GPR
- *Examples:* seismic reflection, resistivity

</div>
</div>

**CASIE21 (2021):** Combined active airguns + passive ocean-bottom seismometers on Cascadia margin — a paradigmatic integrated survey.

**Key point:** Active surveys image structure; passive networks monitor behavior. Rigorous campaigns integrate both.

---

<!-- Slide 12 — Stakeholders -->

# Who Uses Geophysics?

- 🎓 **Research universities** — physical models, open datasets, trained scientists
- 🏛️ **Government agencies** — USGS (hazard maps), NOAA (tsunami warning), CTBTO (nuclear monitoring)
- 🏗️ **Engineering firms** — site characterization, Vs30, dam safety, tunnel routing
- ⛽ **Energy / mining** — petroleum, geothermal, critical minerals, CO₂ storage
- 🌿 **Environmental agencies** — groundwater, contaminant mapping, GPR
- 🛡️ **Defense** — nuclear test monitoring, underground facility characterization

**Key point:** Geophysics graduates work across all these sectors. Physical reasoning, signal processing, and Python are directly transferable.

---

<!-- Slide 13 — Worked example -->

# Worked Example: Precision Matters

Magnetic lineation survey, Juan de Fuca Ridge:

- Reversal boundary at **21 km** from ridge axis
- Brunhes–Matuyama reversal age: **0.78 Ma**

$$v = \frac{d}{t} = \frac{21 \times 10^5 \text{ cm}}{0.78 \times 10^6 \text{ yr}} = 2.692307... \text{ cm/yr}$$

$d = 21$ km has **2 significant figures** → $v \approx \mathbf{2.7 \text{ cm/yr}}$

The trailing digits encode no physical information. **Overconfident precision propagates into all downstream analysis.**

---

<!-- Slide 14 — Concept check -->

# Concept Check

*Discuss in pairs — 3 minutes*

1. The magnetic lineation method exploits a naturally occurring signal. What category of survey is it, and what is the natural source it exploits?

2. If greater precision on the spreading rate were needed, which input — distance or age — would be more productive to refine, and on what physical or practical grounds?

3. The calculation assumes the reversal boundary is uniformly 21 km from the ridge axis. What geological processes could violate this assumption?

---

<!-- Slide 15 — Summary -->

# Summary: Lecture 1

- Solid Earth geophysics **infers interior structure from surface observations** — indirect measurement is unavoidable
- Three motivating contexts: **geodynamics · natural hazards · resource management**
- Five physics domains connect observables to Earth properties: mechanics · waves · gravity · EM · heat
- **Passive methods**: continuous, global, source-limited resolution
- **Active methods**: high-resolution snapshots, controlled source, high cost
- Significant figures = minimum expression of measurement uncertainty

---

<!-- Slide 16 — Further reading -->

# Further Reading & Lab 1

**Reading:**
- Lowrie & Fichtner (2020) §1.1–1.3 — **free via UW Libraries**
- MIT OCW 12.201: [ocw.mit.edu/courses/12-201](https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004)
- Mousavi & Beroza (2022) Deep-learning seismology, *Science*: [doi.org/10.1126/science.abm4470](https://doi.org/10.1126/science.abm4470)
- PNSN real-time seismicity: [pnsn.org](https://pnsn.org)

**Lab 1 (Friday):**
1. Install ObsPy
2. Fetch a PNSN seismogram via IRIS FDSN client
3. Identify P and S arrivals by eye
4. Compute source distance from $t_S - t_P = \Delta(1/\beta - 1/\alpha)$
