---
marp: true
theme: default
paginate: true
math: mathjax
style: |
  section {
    font-size: 28px;
    padding: 50px 60px;
  }
  h1 {
    font-size: 36px;
    color: #0072B2;
    border-bottom: 2px solid #0072B2;
    padding-bottom: 8px;
  }
  h2 {
    font-size: 30px;
    color: #333;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2em;
  }
  ul { margin-top: 0.5em; }
  li { margin-bottom: 0.3em; }
  strong { color: #0072B2; }
  .footer { font-size: 18px; color: #777; border-top: 1px solid #ddd; margin-top: 1em; padding-top: 0.4em; }
---

# What Is Geophysics?
### Three Motivations, Five Physics Domains, and the Stakeholder Landscape

**ESS 314 — Geophysics** | Lecture 1 | March 31, 2026
Marine Denolle · University of Washington

---

# Learning Objectives

By the end of this lecture:

- **[LO-1.1]** State a precise definition of solid Earth geophysics and explain why indirect observation is the defining constraint
- **[LO-1.2]** Classify any geophysical study into geodynamics, hazards, or resource management — with process and observable
- **[LO-4.1]** Identify which physics domain governs a given observable and which Earth property it senses
- **[LO-6.1]** Identify four stakeholder communities and their distinct requirements from geophysical knowledge

---

# The Defining Constraint

**On January 26, 1700** — the entire Cascadia fault ruptured

- A 1,300 km rupture — no instrumental seismic record existed
- Date reconstructed from: Japanese tsunami records, drowned coastal forests, Indigenous oral traditions, coastal sediment stratigraphy
- **Everything known about this event is geophysical inference from indirect evidence**

> Earth's interior is permanently inaccessible to direct sampling beyond a few kilometers. Geophysics exists to address this constraint.

**Key point:** The inability to sample directly is not a limitation of current technology — it is a permanent physical constraint on what Earth science can do without geophysics.

---

# Definition

$$\boxed{\text{Solid Earth Geophysics} = \text{Quantitative inference of Earth's interior from surface observations}}$$

Physical fields measured at or above the surface:
- Seismic wave travel times
- Gravitational acceleration
- Magnetic field strength
- Surface deformation (GPS, InSAR)
- Heat flux

Every observable is **indirect** — the Earth property of interest is always inferred through a physical model.

**Key point:** Geophysics is applied physics working backward — from effect to cause, from measurement to structure.

---

# Three Motivating Contexts

Every geophysical study belongs to at least one:

| Context | Physical Process | Key Observable |
|---------|-----------------|----------------|
| **Geodynamics** | Mantle convection, subduction, glacial rebound | Seismic velocity, gravity, heat flow |
| **Natural Hazards** | Fault rupture, wave propagation, site amplification | Seismograms, GPS, InSAR |
| **Resource Management** | Stratigraphy, fluid-bearing reservoirs, ore bodies | Seismic reflection, resistivity |

The same methods frequently serve multiple contexts simultaneously.

**Key point:** Knowing which motivation drives a study tells what precision is required and what constitutes a satisfactory answer.

---

# Geodynamics: How the Planet Works

- Juan de Fuca Plate subducts at ~3 cm/yr — measured by GPS, not by drilling
- Subducting slab geometry — imaged by seismic tomography, not by sampling
- Mantle convection drives plate tectonics — inferred from seismic velocity, gravity, and heat flow

**No sample has ever been retrieved from the mantle under equilibrium conditions.**

![FIGURE: seismic tomography of Juan de Fuca slab](../../assets/figures/fig_three_motivations.png)

**Key point:** Every layer boundary in the Earth model was found by listening to earthquakes — not by drilling.

---

# Natural Hazards: Physics in Service of Public Safety

- **ShakeAlert** (Alaska to California): real-time P-wave detection → shaking estimate → warning before S-wave arrives
- Lead time: seconds to tens of seconds — enough to slow trains, open fire station doors, trigger shutoffs
- Built on: wave propagation physics (Weeks 2–5), site response models, network design

Uncertainty matters:
- Underestimating shaking → inadequate building design → casualties
- Overestimating → wasted resources, public distrust

**Key point:** The wave physics in this course is the direct scientific foundation for operational public safety systems.

---

# Resource Management: Knowing What Is Underground

- Before drilling: **seismic reflection surveys** image stratigraphy kilometers below the seafloor
- Marine airguns → elastic pulses → reflections off rock interfaces → subsurface image
- Same methods now serve: geothermal, critical minerals, CO₂ storage monitoring

Global exploration geophysics: tens of billions of dollars annually

**Key point:** The same physical methods serve petroleum, geothermal, groundwater, and carbon storage — the motivation changes, the physics does not.

---

# The Five Physics Domains

| Domain | Governing Equation | Earth Property | Observable |
|--------|-------------------|----------------|------------|
| Continuum mechanics | $\rho\ddot{\mathbf{u}} = \nabla\cdot\boldsymbol{\sigma}$ | $\lambda, \mu, \rho$ | Seismograms |
| Wave theory | $\nabla^2 u = v^{-2}\partial_{tt}u$ | $\alpha, \beta$ | Travel times |
| Gravity | $\nabla^2\Phi = 4\pi G\rho$ | Density $\rho$ | $g$ anomaly |
| Electromagnetism | $\nabla\times\mathbf{B} = \mu_0\mathbf{J}$ | $\sigma_e$, magnetization | EM anomaly |
| Thermodynamics | $\rho c_p \partial_t T = \nabla\cdot(k\nabla T)$ | $T$, $k$ | Heat flux $q$ |

These equations will be derived or applied in detail during each module.

**Key point:** Every observable is connected to an Earth property through a physical operator. This structure is the forward problem.

---

# Passive vs. Active Surveys

<div class="columns">
<div>

**Passive** — measure natural signals
- No source cost; continuous; global
- Earthquakes, geomagnetic field, gravity, ambient noise
- Coverage limited by natural source distribution
- *Examples:* earthquake seismology, GPS, gravity

</div>
<div>

**Active** — generate controlled signals
- Full control over source parameters → higher resolution
- Expensive; limited spatial coverage
- Explosions, vibroseis, airguns, GPR
- *Examples:* seismic reflection, resistivity

</div>
</div>

The 2021 CASIE21 experiment combined both: active airguns + passive ocean-bottom seismometers.

**Key point:** Most rigorous campaigns integrate both strategies — active surveys image structure; passive networks monitor behavior over time.

---

# Who Uses Geophysics?

- **Research universities** — physical models, open datasets, trained scientists
- **Government agencies** — USGS (hazard maps), NOAA (tsunami warning), CTBTO (nuclear test monitoring)
- **Engineering firms** — site characterization, Vs30 for building codes, dam safety
- **Energy / mining** — petroleum, geothermal, critical minerals, CO₂ storage
- **Environmental agencies** — groundwater mapping, contaminant detection, GPR
- **Defense** — nuclear test monitoring, underground facility characterization

**Key point:** Geophysics graduates work across all these sectors. The physical reasoning, signal processing, and Python skills in this course are directly transferable.

---

# Worked Example: Precision Matters

Magnetic lineation survey, Juan de Fuca Ridge:
- Reversal boundary at **21 km** from ridge axis
- Brunhes–Matuyama reversal age: **0.78 Ma**

$$v = \frac{d}{t} = \frac{21 \times 10^5 \text{ cm}}{0.78 \times 10^6 \text{ yr}} = 2.692307... \text{ cm/yr}$$

But $d = 21$ km has **2 significant figures** → $v \approx \mathbf{2.7}$ cm/yr

The trailing digits are physically meaningless. **Misrepresenting precision propagates through all downstream analysis.**

**Key point:** An answer can only be as precise as the least precise input. This applies to every geophysical inference.

---

# Concept Check

1. The magnetic lineation method exploits a naturally occurring signal. What category of survey is it, and what is the natural source?

2. If greater precision on the spreading rate were needed, which input — distance or age — would be more productive to refine, and on what grounds?

3. The calculation assumes the reversal boundary is uniformly located 21 km from the ridge axis. What geological processes could violate this assumption?

*Discuss in pairs — 3 minutes*

---

# Summary: Lecture 1 Key Takeaways

- Solid Earth geophysics infers interior structure from surface observations — indirect measurement is unavoidable
- Three motivating contexts: **geodynamics**, **natural hazards**, **resource management**
- Five physics domains connect observables to Earth properties: mechanics, waves, gravity, EM, heat
- **Passive methods**: continuous, global, source-limited resolution
- **Active methods**: high-resolution snapshots, controlled source, high cost
- Many stakeholder communities rely on geophysical knowledge — with different precision requirements
- Significant figures are the minimum expression of measurement uncertainty

---

# Further Reading

- Lowrie & Fichtner (2020) §1.1–1.3 — **free via UW Libraries**
- MIT OCW 12.201 Essentials of Geophysics: [ocw.mit.edu/courses/12-201](https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004)
- Mousavi & Beroza (2022) Deep-learning seismology, *Science*: [doi.org/10.1126/science.abm4470](https://doi.org/10.1126/science.abm4470)
- PNSN real-time seismicity: [pnsn.org](https://pnsn.org)
- USGS ShakeAlert: [usgs.gov/programs/earthquake-hazards/shakealert](https://www.usgs.gov/programs/earthquake-hazards/shakealert)

**Lab 1 (Friday):** Install ObsPy · Fetch a PNSN seismogram · Identify P and S arrivals by eye
