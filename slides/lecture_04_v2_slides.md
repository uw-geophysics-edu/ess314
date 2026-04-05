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
  section.title-slide h1 { color: white; font-size: 1.45em; }
  section.title-slide h3 { color: #a8c8f0; }
  section.title-slide h4 { color: #cde; font-weight: normal; }
  h1 { font-size: 1.4em; color: #003366; }
  h2 { font-size: 1.15em; color: #0072B2; }
  img { border-radius: 4px; max-width: 100%; }
  .caption { font-size: 0.60em; color: #666; margin-top: 4px; font-style: italic; }
  .key-eq {
    background: #d4edda;
    border-left: 5px solid #28a745;
    padding: 10px 16px;
    border-radius: 4px;
    font-size: 0.92em;
    margin: 8px 0;
  }
  .callout {
    background: #eaf4fb;
    border-left: 5px solid #0072B2;
    padding: 10px 16px;
    border-radius: 4px;
    font-size: 0.88em;
    margin: 8px 0;
  }
  .warning {
    background: #fff3cd;
    border-left: 5px solid #E69F00;
    padding: 10px 16px;
    border-radius: 4px;
    font-size: 0.88em;
  }
  table { font-size: 0.82em; }
  td, th { padding: 4px 10px; }
---

<!-- _class: title-slide -->

# Seismic Wave Types — The Basics

### ESS 314 Geophysics · University of Washington
#### Week 1, Lecture 4 · April 2, 2026
#### Marine Denolle

---

# By the end of this lecture…

- **[LO-4.1]** *Classify* P, S, Rayleigh, Love waves by particle motion, polarization, and medium
- **[LO-4.2]** *Explain* physically why S-waves cannot travel in fluids — beyond stating $\mu = 0$
- **[LO-4.3]** *Compare* $V_P$ and $V_S$ across Earth materials; identify controlling properties
- **[LO-4.4]** *Apply* the S–P time method to estimate earthquake distance from one seismogram
- **[LO-4.5]** *Distinguish* Rayleigh from Love waves; explain why Love needs layering

---

<!-- backgroundImage: url('https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/2011_Tōhoku_earthquake_and_tsunami_seismograph_recording.svg/1200px-2011_Tōhoku_earthquake_and_tsunami_seismograph_recording.svg.png') -->
<!-- Source: Wikimedia Commons — Public Domain -->

<style scoped>
section {
  background: rgba(0,0,0,0.60);
  color: white;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.9);
}
h1, h2 { color: white; }
</style>

# One Earthquake, Three Arrivals

2011 Tōhoku M9.0 — recorded in Seattle 8,000 km away

The **P-wave** arrives first — fast, compressional, vertical motion

Then the **S-wave** — slower, shear, horizontal motion, larger amplitude

Then **surface waves** — slowest, largest, longest duration

*Same source. Same Earth. Different wave physics.*

---

# Why Multiple Wave Types?

The 3D elastic wave equation contains two independent solutions:

$$\rho\,\frac{\partial^2\mathbf{u}}{\partial t^2}
= (\lambda+2\mu)\,\nabla(\nabla\cdot\mathbf{u})
- \mu\,\nabla\times(\nabla\times\mathbf{u})$$

**Helmholtz decomposition** $\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}$ splits this into:

$$\frac{\partial^2\phi}{\partial t^2} = V_P^2\,\nabla^2\phi
\qquad
\frac{\partial^2\boldsymbol{\psi}}{\partial t^2} = V_S^2\,\nabla^2\boldsymbol{\psi}$$

<div class="callout">
The wave equation <em>must</em> produce exactly two body-wave types — because elastic deformation has exactly two independent modes: volume change and shape change.
</div>

---

# P-waves: Longitudinal Motion

**P = Primary, Compressional, Longitudinal**

Particle motion is **parallel** to propagation direction

→ Alternating compression (C) and rarefaction (R) zones along the ray

Exists in **solids and fluids** — fastest seismic arrival

$$V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}}$$

<div class="callout">
Think: a slinky pushed end-to-end. The compression pulse travels forward while individual coils move back-and-forth along the slinky's axis.
</div>

---

# P-wave and S-wave Particle Motion

![alt text: Two-panel figure. Top panel shows P-wave as alternating dark blue compression and sky blue rarefaction zones of particles, with orange longitudinal arrows parallel to the green propagation arrow. Bottom panel shows S-wave particles displaced transversely in a sinusoidal pattern, with orange arrows perpendicular to the propagation direction, and a callout stating S-waves cannot travel in fluids because mu equals zero.](../../assets/figures/fig_pwave_swave_motion.png)
<span class="caption">Figure 4.1. P-wave: longitudinal (top). S-wave: transverse (bottom). Color encodes compression state independently of arrow direction (WCAG AA). Python-generated — assets/scripts/fig_pwave_swave_motion.py</span>

---

# S-waves: Transverse Motion

**S = Secondary, Shear, Transverse**

Particle motion is **perpendicular** to propagation direction

Exists in **solids only** — arrives after P

$$V_S = \sqrt{\frac{\mu}{\rho}}$$

Two polarizations:

| Polarization | Plane of motion | Mode conversion at interface? |
|---|---|---|
| **SV** | Vertical plane of ray | Yes → P |
| **SH** | Horizontal, ⊥ to ray | No |

---

# SV and SH Polarization Geometry

![alt text: 3D perspective diagram showing a ray propagating to the right along the x-axis. A blue vertical plane contains the ray and a vertical double-headed vermilion arrow labeled SV for vertical shear. A plane perpendicular to the ray (sky blue) is shown at mid-distance. A horizontal double-headed green arrow labeled SH points in the y-direction perpendicular to the ray. Sinusoidal oscillation traces in each polarization direction are shown along the ray path. A label reads total S equals SV plus SH.](../../assets/figures/fig_sv_sh_polarization.png)
<span class="caption">Figure 4.2. SV motion lies in the vertical plane of the ray; SH motion is horizontal and perpendicular. Only SH is relevant to Love waves. Python-generated — assets/scripts/fig_sv_sh_polarization.py</span>

---

# Why No S-waves in Fluids?

In a fluid: $\mu = 0 \Rightarrow V_S = 0$

But the *formula* is not the *reason*. The physical argument:

1. An S-wave requires the medium to be **shear-distorted and spring back**
2. In a fluid, molecules **flow and rearrange** rather than storing shear elastic energy
3. No shear restoring force → no shear wave oscillation

<div class="warning">
Consequences you will see in this course:
<ul>
  <li>S-wave <strong>shadow zone</strong> → liquid outer core</li>
  <li>Seafloor surveys: S-waves reflect at the water–sediment interface</li>
  <li>High V_P/V_S in saturated sediments → fluid detection</li>
</ul>
</div>

---

# Surface Waves: Trapped at the Free Surface

Free surface boundary condition (zero traction) allows **guided waves** that:

- Decay exponentially with depth $\sim e^{-kz}$, $k = 2\pi/\lambda_\text{dom}$
- Significant only to depth $\approx 0.4\,\lambda_\text{dom}$
- Travel slower than body waves
- Are **dispersive** — phase speed depends on frequency

| Type | Motion | Speed | Requires |
|------|--------|-------|---------|
| Rayleigh | Retrograde ellipse (P+SV) | $\approx 0.92\,V_S$ | Any half-space |
| Love | Transverse SH only | $V_{S1} < V_L < V_{S2}$ | Velocity layering |

---

# Rayleigh and Love Waves

![alt text: Three-panel figure. Left shows retrograde elliptical Rayleigh wave orbits at multiple depths, with large ellipses near the surface shrinking to small circles at depth. Center shows amplitude versus depth decaying exponentially with a dashed reference at 0.4 wavelength depth and label V_R approximately 0.92 V_S. Right shows Love wave cross-section with a slow sky-blue surface layer over a green fast half-space, dashed orange zigzag rays showing SH trapping by total internal reflection, and dot symbols for horizontal transverse particle motion.](../../assets/figures/fig_surface_waves.png)
<span class="caption">Figure 4.3. Rayleigh: retrograde ellipse, depth $\approx 0.4\lambda_\text{dom}$ (left, center). Love: SH trapped in slow surface layer (right). Python-generated — assets/scripts/fig_surface_waves.py</span>

---

# Why Love Waves Need Layering

Rayleigh waves exist in **any** elastic half-space — they are a natural free-surface solution.

Love waves form only when there is a **slow layer over a faster half-space** ($V_{S2} > V_{S1}$):

1. SH waves in the slow layer hit the interface at subcritical angles → totally internally reflected
2. Multiple reflections between the free surface and interface **constructively interfere**
3. Result: a trapped guided wave with horizontal SH particle motion

<div class="callout">
A homogeneous half-space has Rayleigh but <em>not</em> Love waves.
Observing Love waves tells you the Earth is <em>layered</em>.
</div>

---

# Seismic Wave Speeds Across Earth Materials

![alt text: Horizontal bar chart with P-wave velocity on the horizontal axis from 0 to 8000 m/s. Dark blue bars for crystalline rocks (granite, basalt) range from 4800 to 6500 m/s. Sky blue bars for unconsolidated sediments (dry sand, clay) range from 60 to 2000 m/s. Green bars for fluids cluster near 1200 to 1540 m/s. Amber bars for engineering materials are near 5800 to 6400 m/s. A dotted vertical line marks 1480 m/s for water.](../../assets/figures/fig_seismic_velocities.png)
<span class="caption">Figure 4.4. V_P spans ~100× from dry clay (60 m/s) to steel (6000 m/s). Soft sediments can be 50× slower than basement rock. Python-generated — assets/scripts/fig_seismic_velocities.py</span>

---

# The $V_P/V_S$ Ratio as a Fluid Indicator

$$\frac{V_P}{V_S} = \sqrt{\frac{\lambda+2\mu}{\mu}} = \sqrt{\frac{2(1-\nu)}{1-2\nu}}$$

| Material state | $\nu$ | $V_P/V_S$ |
|---|---|---|
| Typical crustal rock | 0.25 | $\sqrt{3} \approx 1.73$ |
| Dry, cracked rock | 0.10–0.20 | 1.45–1.60 |
| Water-saturated sediment | 0.45–0.49 | 3.0–10.0 |
| Perfect fluid | 0.50 | $\infty$ |

<div class="callout">
High V_P/V_S → fluid saturation, magma, high pore pressure<br>
Low V_P/V_S → gas sand, dry fractured rock
</div>

---

# The S–P Time Method

P and S travel the same distance $d$ at speeds $V_P > V_S$:

<div class="key-eq">

$$\Delta t_{SP} = t_S - t_P = d\!\left(\frac{1}{V_S} - \frac{1}{V_P}\right)$$

$$\Rightarrow\quad d = \frac{\Delta t_{SP}}{\dfrac{1}{V_S} - \dfrac{1}{V_P}}$$

</div>

One seismometer + one clock = earthquake distance

Used in real time by **PNSN** and **ShakeAlert**

---

# Worked Example: S–P Distance Estimate

$t_P = 42.0$ s, $t_S = 74.8$ s, $V_P = 6.2$ km/s, $V_P/V_S = \sqrt{3}$

$$V_S = \frac{6.2}{\sqrt{3}} \approx 3.58 \text{ km/s}$$

$$\Delta t_{SP} = 74.8 - 42.0 = 32.8 \text{ s}$$

$$d = \frac{32.8}{\dfrac{1}{3.58} - \dfrac{1}{6.2}} = \frac{32.8}{0.279 - 0.161} = \frac{32.8}{0.118} \approx \mathbf{278 \text{ km}}$$

Seattle → Portland ≈ 280 km → consistent with a Cascades or Willamette Valley source

---

# What Each Seismometer Component Records

| Component | Most sensitive to |
|-----------|------------------|
| Vertical (Z) | P-wave (compressional, vertical motion), Rayleigh wave (vertical ellipse) |
| Horizontal N–S, E–W | S-wave (transverse), Love wave (horizontal SH), Rayleigh wave (horizontal ellipse) |

<div class="callout">
A Love wave has <em>no vertical component</em>.
If you only had a vertical seismometer, you would miss it entirely.
This is why three-component instruments are essential for full wave-type identification.
</div>

---

# AI Literacy: Phase Pickers and Wave Physics (LO-7)

Deep learning phase pickers (PhaseNet, EQTransformer) auto-identify P and S arrivals because of the physics from this lecture.

**In-class prompt — try this now:**

> *"A seismometer's vertical channel shows a sharp onset at 32 s; horizontal channels show a larger onset at 57 s. What wave types are these, and what can I estimate from the 25-second difference?"*

**Evaluate the response:**
- Does it identify vertical = P, horizontal = S? ✅
- Does it apply the S–P formula correctly? ✅
- Does it explain the *physical reason* vertical vs. horizontal (particle motion geometry)? ← the key test
- Does it give overconfident velocity values without acknowledging regional variability? ← flag this

<div class="warning">
AI passes the formula test easily. The harder test is physical reasoning.
</div>

---

# Concept Check

1. A seismometer records only P-wave arrivals — no S-wave. List **three distinct physical reasons** this could happen. (Think about source, path, and instrument.)

2. A seismogram shows $\Delta t_{SP} = 20$ s and the station is 120 km from the earthquake. What does this imply about $V_P/V_S$? Is this consistent with typical crustal rock?

3. Why does an SH wave not convert to a P-wave when it reflects from a horizontal interface, while an SV wave can? Answer using particle motion geometry.

---

# Summary

| Wave | Motion | Speed | Exists in |
|------|--------|-------|-----------|
| P | Longitudinal (∥ ray) | $\sqrt{(\lambda+2\mu)/\rho}$ | Solids + fluids |
| S | Transverse (⊥ ray) | $\sqrt{\mu/\rho}$ | Solids only |
| Rayleigh | Retrograde ellipse (P+SV) | $\approx 0.92\,V_S$ | Any half-space |
| Love | Horizontal SH | $V_{S1} < V_L < V_{S2}$ | Layered only |

$V_P > V_S > V_R$ always. S-waves need $\mu \neq 0$ (shear restoring force).

**Next class:** Lab 1 — Introduction to Python  
**Lecture 6 (Apr 6):** Wavefronts and Rays
