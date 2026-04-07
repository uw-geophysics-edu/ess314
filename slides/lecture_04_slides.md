---
marp: true
theme: ess314
size: 16:9
html: true
paginate: true
math: katex
---

<!-- _class: title -->

# Seismic Wave Types

### ESS 314 Geophysics · University of Washington

#### Week 1, Lecture 4 · April 2, 2026

#### Marine Denolle

---

# By the end of this lecture…

- **[LO-4.1]** *Classify* P, S, Rayleigh, Love waves by particle motion, polarization, and medium
- **[LO-4.2]** *Explain* physically why S-waves cannot travel in fluids — beyond stating $\mu = 0$
- **[LO-4.3]** *Compare* $V_P$ and $V_S$ across Earth materials; identify the controlling properties
- **[LO-4.4]** *Apply* the S–P time method to estimate earthquake distance from one seismogram
- **[LO-4.5]** *Distinguish* Rayleigh from Love waves; explain why Love requires layering

---

<!-- backgroundImage: url('https://upload.wikimedia.org/wikipedia/commons/thumb/2/2e/2011_T%C5%8Dhoku_earthquake_and_tsunami_seismograph_recording.svg/1200px-2011_T%C5%8Dhoku_earthquake_and_tsunami_seismograph_recording.svg.png') -->
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
*(The same question has been asked — and answered — on the Moon and Mars.)*

---

# Why Multiple Wave Types?

The 3D elastic wave equation has two independent solutions:

$$\rho\,\frac{\partial^2\mathbf{u}}{\partial t^2}
= (\lambda+2\mu)\,\nabla(\nabla\cdot\mathbf{u})
- \mu\,\nabla\times(\nabla\times\mathbf{u})$$

**Helmholtz decomposition** $\mathbf{u} = \nabla\phi + \nabla\times\boldsymbol{\psi}$ splits this into:

$$\frac{\partial^2\phi}{\partial t^2} = V_P^2\,\nabla^2\phi
\qquad\quad
\frac{\partial^2\boldsymbol{\psi}}{\partial t^2} = V_S^2\,\nabla^2\boldsymbol{\psi}$$

<div class="callout">
The wave equation <em>must</em> produce exactly two body-wave families — elastic deformation has exactly two independent modes: <strong>volume change</strong> (P) and <strong>shape change</strong> (S).
</div>

---

# P-waves: Longitudinal Motion

**P = Primary · Compressional · Longitudinal**

Particle motion **parallel** to propagation — alternating compression (C) and rarefaction (R)

Exists in **solids and fluids** — fastest seismic arrival

$$V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}} = \sqrt{\frac{K + \tfrac{4}{3}\mu}{\rho}}$$

<div class="callout">
Think: a slinky pushed end-to-end. The compression pulse travels forward while individual coils oscillate back-and-forth <em>along</em> the slinky's axis.
</div>

---

# P-wave Particle Motion

![alt text: P-wave particle motion diagram showing alternating clusters of close-spaced dark blue dots labeled C for compression zones and widely-spaced sky-blue dots labeled R for rarefaction zones along a horizontal axis. Orange horizontal arrows show longitudinal displacement parallel to the green propagation arrow at the bottom. Particle motion is parallel to the direction of wave propagation.](../assets/figures/fig_pwave_motion.png)
<span class="caption">Figure 4.1. P-wave: longitudinal (compressional) particle motion — particles move parallel to the ray. Python-generated — assets/scripts/fig_pwave_swave_motion.py</span>

---

# S-waves: Transverse Motion

**S = Secondary · Shear · Transverse**

Particle motion **perpendicular** to propagation — exists in **solids only**

$$V_S = \sqrt{\frac{\mu}{\rho}} \qquad (V_S < V_P \text{ always})$$

Two independent polarizations:

| Polarization | Plane of motion | Mode conversion at interface? |
|---|---|---|
| **SV** | Vertical plane of the ray | Yes → converts to P or Rayleigh |
| **SH** | Horizontal, ⊥ to ray plane | No → generates Love waves only |

---

# S-wave Particle Motion

![alt text: S-wave particle motion diagram showing vermilion particles displaced transversely above and below the equilibrium line in a sinusoidal pattern. Orange vertical arrows indicate displacement perpendicular to the green propagation arrow pointing to the right. A callout annotation states that S-waves cannot propagate in fluids because the shear modulus mu equals zero.](../assets/figures/fig_swave_motion.png)
<span class="caption">Figure 4.2. S-wave: transverse (shear) particle motion — particles move perpendicular to the ray. Python-generated — assets/scripts/fig_pwave_swave_motion.py</span>

---

# SV and SH Polarization Geometry

![alt text: 3D perspective diagram showing a ray propagating to the right along the x-axis. A light blue vertical plane contains the ray and a vertical double-headed vermilion arrow labeled SV for vertical shear polarization. A horizontal double-headed amber arrow labeled SH points in the y-direction perpendicular to the ray. A label reads total S equals SV plus SH.](../assets/figures/fig_sv_sh_polarization.png)
<span class="caption">Figure 4.3. SV motion lies in the vertical plane of the ray; SH motion is horizontal and perpendicular to it. Python-generated — assets/scripts/fig_sv_sh_polarization.py</span>

---

# Why No S-waves in Fluids?

In a fluid: $\mu = 0 \Rightarrow V_S = 0$ — but the *formula* is not the *reason*.

The physical argument:

1. An S-wave requires the medium to **shear-distort and elastically spring back**
2. In a fluid, molecules **flow and rearrange** rather than storing shear elastic energy
3. No shear restoring force → no transverse oscillation propagates

<div class="warning">
Consequences in this course:
<ul>
  <li>S-wave <strong>shadow zone</strong> → liquid outer core (Lectures 17–18)</li>
  <li>For those interested in ocean physics: ocean basins are <strong>transparent to P-waves</strong> (hydroacoustic <em>T</em>-phases) but <strong>opaque to S</strong></li>
  <li>High $V_P/V_S$ in saturated sediments → direct fluid detection</li>
</ul>
</div>

---

# Surface Waves: Trapped at the Free Surface

Free surface boundary (zero traction) allows **guided waves** that decay as $e^{-kz}$ and are **dispersive**:

| Type | Particle motion | Speed | Requires |
|------|-----------------|-------|---------|
| **Rayleigh** | Retrograde ellipse (P + SV) | $\approx 0.92\,V_S$ | Any elastic half-space |
| **Love** | Horizontal SH only | $V_{S1} < V_L < V_{S2}$ | Velocity layering |

Both are **slower** than body waves and carry the **largest amplitudes** at teleseismic distances.

---

# Rayleigh and Love Waves

![alt text: Three-panel figure. Left panel shows retrograde elliptical Rayleigh wave particle orbits at multiple depths, with large ellipses near the surface shrinking to small circles at depth. Center panel shows amplitude versus depth decaying exponentially with a dashed reference at 0.4 wavelength depth and label V_R approximately 0.92 V_S. Right panel shows Love wave cross-section with a slow sky-blue surface layer over a green fast half-space, dashed orange zigzag rays showing SH trapping by total internal reflection, and dot symbols for horizontal transverse particle motion.](../assets/figures/fig_surface_waves.png)
<span class="caption">Figure 4.4. Rayleigh: retrograde elliptical decay with depth (left, center). Love: SH trapped in slow surface layer by total internal reflection (right). Python-generated — assets/scripts/fig_surface_waves.py</span>

---

# Why Love Waves Need Layering

Rayleigh waves exist in **any** elastic half-space — they are a natural free-surface solution.

Love waves require a **slow layer over a faster half-space** ($V_{S2} > V_{S1}$):

1. SH waves hit the base at subcritical angles → **total internal reflection**
2. Repeated reflections between the free surface and the interface **constructively interfere**
3. Result: a trapped guided wave with purely horizontal SH particle motion

<div class="callout">
A homogeneous half-space has Rayleigh but <em>not</em> Love waves — observing Love waves requires a layered Earth.<br><br>
For those interested in planetary science: NASA's InSight used surface wave dispersion from marsquakes to map the Martian crustal layering.
</div>

---

# Seismic Wave Speeds Across Earth Materials

![alt text: Horizontal bar chart with P-wave velocity on the horizontal axis from 0 to 8000 m/s. Dark blue bars for crystalline rocks (granite, basalt) range from 4800 to 6500 m/s. Sky blue bars for unconsolidated sediments (dry sand, clay) range from 60 to 2000 m/s. Green bars for fluids cluster near 1200 to 1540 m/s. Amber bars for engineering materials are near 5800 to 6400 m/s. A dotted vertical line marks 1480 m/s for water.](../assets/figures/fig_seismic_velocities.png)
<span class="caption">Figure 4.5. $V_P$ spans ~100× from dry clay (60 m/s) to steel (~6000 m/s). Soft sediments can be 50× slower than basement rock. Python-generated — assets/scripts/fig_seismic_velocities.py</span>

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
<strong>High</strong> $V_P/V_S$ → fluid saturation, magma, high pore pressure<br>
<strong>Low</strong> $V_P/V_S$ → gas sand, dry fractured rock<br>
<em>Seattle example:</em> Duwamish Valley $V_P/V_S = 7.95$ (water-saturated alluvium) — why Pioneer Square shakes harder than Capitol Hill.
</div>

---

# The S–P Time Method

P and S travel the same distance $d$ at speeds $V_P > V_S$:

<div class="key-eq">

$$\Delta t_{SP} = t_S - t_P = d\!\left(\frac{1}{V_S} - \frac{1}{V_P}\right)
\qquad\Rightarrow\qquad
d = \frac{\Delta t_{SP}}{\dfrac{1}{V_S} - \dfrac{1}{V_P}}$$

</div>

**One seismometer + one clock = earthquake distance**

Used in real time by **PNSN** and **ShakeAlert**

---

# Worked Example: S–P Distance Estimate

$t_P = 42.0$ s, $t_S = 74.8$ s, $V_P = 6.2$ km/s, $V_P/V_S = \sqrt{3}$

$$V_S = \frac{6.2}{\sqrt{3}} \approx 3.58 \text{ km/s} \qquad \Delta t_{SP} = 74.8 - 42.0 = 32.8 \text{ s}$$

$$d = \frac{32.8}{\dfrac{1}{3.58} - \dfrac{1}{6.2}} = \frac{32.8}{0.279 - 0.161} = \frac{32.8}{0.118} \approx \mathbf{278 \text{ km}}$$

Seattle → Portland ≈ 280 km — consistent with a Cascades or Willamette Valley source.

---

# What Each Seismometer Component Records

| Component | Most sensitive to |
|-----------|------------------|
| **Vertical (Z)** | P-wave (compressional, vertical motion); Rayleigh wave (vertical ellipse component) |
| **Horizontal N–S, E–W** | S-wave (transverse); Love wave (horizontal SH); Rayleigh wave (horizontal ellipse component) |

<div class="callout">
A Love wave has <em>no vertical component</em> — a vertical-only seismometer misses it entirely.<br>
This is why three-component instruments are essential for full wave-type identification.
</div>

---

# ShakeAlert: P-waves Save Lives

The USGS ShakeAlert system detects **fast-arriving P-waves** to issue alerts before **more damaging S-waves** arrive.

For a **Cascadia M9**:
- P-wave reaches coast: ~15 s after rupture
- Strong S-wave shaking reaches Seattle: 60–90 s later

That **60–90 s warning window** = time to stop trains, pause surgeries, move away from windows.

The physics: **$V_P > V_S$** — always.

<!-- Instructor note: If the student who experienced the 2001 Nisqually earthquake (M6.8) from Tacoma is present, invite them to describe what they felt — the succession of sharp jolt, strong shaking, and rolling motion maps directly onto P, S, and surface wave arrivals. They indicated willingness in the intake survey. -->

---

# $V_{S30}$ and Building Codes

**$V_{S30}$** = time-averaged shear velocity in the top 30 m of soil

| Site Class | $V_{S30}$ (m/s) | Description |
|---|---|---|
| A | > 1500 | Hard rock |
| B | 760–1500 | Rock |
| C | 360–760 | Dense soil / soft rock |
| D | 180–360 | Stiff soil |
| **E** | **< 180** | **Soft soil** |

Design earthquake force for Class E is **3–5× larger** than Class B.

In Seattle: Capitol Hill (glacial till, ~500 m/s) vs. Pioneer Square (artificial fill, ~180 m/s).

---

# AI Literacy: Phase Pickers and Wave Physics (LO-7)

Deep learning models (PhaseNet, EQTransformer) pick P and S arrivals because of the physics from this lecture.

**In-class prompt — try this now:**

> *"A seismometer's vertical channel shows a sharp onset at 32 s; horizontal channels show a larger onset at 57 s. What wave types are these, and what can I estimate from the 25-second difference?"*

**Evaluate the AI response:**
- Does it identify vertical = P, horizontal = S? ✅
- Does it apply the S–P formula correctly? ✅
- Does it explain the *physical reason* for vertical vs. horizontal particle motion? ← key test
- Does it give overconfident velocities without acknowledging regional variability? ← flag this

<div class="warning">
AI passes the formula test easily. The harder test is physical reasoning — not algebra.
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
| **P** | Longitudinal (∥ ray) | $\sqrt{(\lambda+2\mu)/\rho}$ | Solids + fluids |
| **S** | Transverse (⊥ ray) | $\sqrt{\mu/\rho}$ | Solids only |
| **Rayleigh** | Retrograde ellipse (P+SV) | $\approx 0.92\,V_S$ | Any half-space |
| **Love** | Horizontal SH | $V_{S1} < V_L < V_{S2}$ | Layered only |

$V_P > V_S > V_R$ always. S-waves require $\mu \neq 0$ (shear restoring force).

**Next class:** Lab 1 — Introduction to Python — computing $V_P$, $V_S$ for different rock types

**Lecture 6 (Apr 6):** Wavefronts, Rays, and Snell's Law

