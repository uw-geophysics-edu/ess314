---
marp: true
theme: ess314
size: 16:9
html: true
paginate: true
math: mathjax
---

<!-- _class: title-slide -->

# Seismic Wave Types and Ray Propagation

### ESS 314 Geophysics · University of Washington
#### Week 1, Lecture 4 · April 9, 2026
#### Marine Denolle

---

# By the end of this lecture…

- **[LO-4.1]** *Distinguish* P, S, Rayleigh, Love by particle motion, polarization, and speed
- **[LO-4.2]** *Explain* why S-waves cannot travel in fluids — physics, not just formula
- **[LO-4.3]** *Apply* Huygens' principle to describe wavefront evolution at a contrast
- **[LO-4.4]** *Derive* Snell's law from wavefront geometry; predict refracted ray angles
- **[LO-4.5]** *Calculate* the critical angle and head-wave arrival geometry

---

# What Does a Seismogram Record?

A Cascadia earthquake signal at a Seattle station arrives in three distinct bursts:

| Arrival | Wave type | Travel time | Character |
|---------|-----------|-------------|-----------|
| First | P-wave | ~90 s | Sharp, vertical motion |
| Second | S-wave | ~140 s | Larger, transverse |
| Third | Surface waves | ~300 s | Long, rolling |

**Why different wave types? Why different speeds?**

→ The Helmholtz decomposition of the 3D wave equation produces two independent families

---

# Helmholtz Decomposition

Any displacement field can be split:

$$\mathbf{u} = \underbrace{\nabla\phi}_\text{irrotational} + \underbrace{\nabla\times\boldsymbol{\psi}}_\text{divergence-free}$$

Each part satisfies its own wave equation:

$$\frac{\partial^2\phi}{\partial t^2} = V_P^2\nabla^2\phi \qquad \frac{\partial^2\boldsymbol{\psi}}{\partial t^2} = V_S^2\nabla^2\boldsymbol{\psi}$$

<div class="callout">
The wave equation from Lecture 3 automatically contains TWO wave types.
We don't add them by hand — they emerge from the vector nature of elasticity.
</div>

---

# P-waves and S-waves: Particle Motion

![alt text: two-panel figure. Top panel shows P-wave with alternating dark blue compression zones and sky blue rarefaction zones of closely and widely spaced particles respectively, with orange arrows showing particle motion parallel to the green propagation arrow. Bottom panel shows S-wave with gray-blue particles displaced transversely above and below an equilibrium dashed line, with orange arrows perpendicular to the propagation direction and a callout noting S-waves require mu not equal to zero and cannot travel in fluids.](../assets/figures/fig_pwave_swave_motion.png)
<span class="caption">Figure 4.1. P-wave: longitudinal motion (top). S-wave: transverse motion (bottom). Blue/sky encodes compression state; arrow direction encodes displacement. Python-generated — assets/scripts/fig_pwave_swave_motion.py</span>

---

# Why No S-waves in Fluids?

From Lecture 3: $V_S = \sqrt{\mu/\rho}$

In any fluid: **$\mu = 0$** (no resistance to shear)

→ $V_S = 0$ — S-waves don't propagate

**Physical reason (not just the formula):**

An S-wave requires the medium to spring back from shear distortion. In a fluid, molecules flow and rearrange instead of storing elastic shear energy.

<div class="warning">
S-wave shadow zone → liquid outer core: no S-waves through Earth's core
Water table: S-waves reflect at water-saturated layer (V_S drops sharply)
Magma chamber: S-wave attenuation → bright reflector in imaging
</div>

---

# S-wave Polarizations

**SV** — particle motion in the *vertical* plane containing the ray

**SH** — particle motion *horizontal*, perpendicular to the ray

Both travel at $V_S$ but interact differently with boundaries:
- **SV** converts to P at interfaces (mode conversion)
- **SH** does not convert to P → Love waves form from SH trapping

<div class="callout">
In earthquake seismology: vertical-component seismometers emphasize P + SV; 
horizontal seismometers emphasize SH + Love waves
</div>

---

# Surface Waves: Trapped at the Free Surface

Boundary condition at Earth's surface: zero traction

→ New solutions that decay exponentially with depth and travel along the surface

| Type | Motion | Speed | Requires |
|------|--------|-------|---------|
| Rayleigh | Retrograde ellipse (P + SV) | $\approx 0.92\,V_S$ | Any half-space |
| Love | Transverse (SH only) | $V_{S1} < V_L < V_{S2}$ | Velocity layering |

Both are **dispersive**: phase velocity depends on frequency

→ Longer periods sample deeper → **surface wave tomography**

---

# Rayleigh and Love Waves

![alt text: three-panel figure. Left panel shows Rayleigh wave retrograde elliptical particle orbits at multiple depths, with ellipses shrinking from large at the surface to tiny at depth, indicating exponential decay. Center panel shows amplitude versus depth curve decaying exponentially with a dashed reference line at 0.4 wavelengths depth and label V_R approximately 0.92 V_S. Right panel shows a cross-section with a slow surface layer over a fast half-space, with dashed orange zigzag rays bouncing by total internal reflection between the free surface and the interface, and dot symbols on rays showing horizontal transverse (SH) particle motion.](../assets/figures/fig_surface_waves.png)
<span class="caption">Figure 4.2. Rayleigh retrograde ellipses (left), amplitude decay with depth (center), Love wave SH trapping (right). Python-generated — assets/scripts/fig_surface_waves.py</span>

---

# Point Source Radiation

![alt text: 3D perspective with a horizontal surface plane and a curved lower hemisphere. From a central source point P, concentric orange-red hemispherical shells expand downward labeled body wave wavefront, and concentric blue circles expand outward on the surface labeled surface wave. Green arrows labeled rays radiate from the source perpendicular to the wavefronts in all directions.](../assets/figures/fig_point_source_wavefronts.png)
<span class="caption">Figure 4.3. Body waves: spherical wavefronts in the interior. Surface waves: circular wavefronts on the surface. Rays always perpendicular to wavefronts. Python-generated — assets/scripts/fig_point_source_wavefronts.py</span>

---

# Huygens' Principle

> Every point on a wavefront is a new **point source** of secondary spherical wavelets
> 
> The new wavefront = envelope (tangent surface) of all secondary wavelets

This is not just geometry — it is the Green's function representation of the wave equation.

**It explains:**
- Why plane waves stay plane in a homogeneous medium
- Why wavefronts *bend* (refract) at a velocity contrast
- Why seismic energy *spreads* (geometrical spreading)

---

# Huygens → Snell's Law: Geometry

![alt text: three-panel figure. Left panel shows Huygens principle with an initial horizontal wavefront at t-zero, secondary circular wavelets on each point, and a new envelope wavefront at t-zero plus delta-t above with propagation arrows. Middle panel shows Snell's law geometry with incident ray from A to B at angle theta-1 from the normal in medium 1 (blue) and refracted ray from B at larger angle theta-2 in medium 2 (green), with segments a-1-t and a-2-t labeled on the geometric triangles. Right panel shows the general Snell's law with incident P-wave, reflected P-wave at same angle, refracted P-wave at larger angle, and converted S-wave at smaller angle, all sharing the same ray parameter p.](../assets/figures/fig_snell_law.png)
<span class="caption">Figure 4.4. (a) Huygens principle. (b) Snell's law geometric derivation. (c) General Snell's law for all wave types. Python-generated — assets/scripts/fig_snell_law.py</span>

---

# Deriving Snell's Law

In time $\Delta t$, wavefront segment in medium 1 travels $V_1 \Delta t$; in medium 2, $V_2 \Delta t$.

Comparing the two right triangles sharing hypotenuse $AB$:

$$\sin\theta_1 = \frac{V_1\,\Delta t}{AB}, \qquad \sin\theta_2 = \frac{V_2\,\Delta t}{AB}$$

<div class="key-eq">

$$\frac{\sin\theta_1}{V_1} = \frac{\sin\theta_2}{V_2} = p \quad\text{(ray parameter)}$$

- Ray bends **toward** normal when entering a **slower** medium
- Ray bends **away** when entering a **faster** medium
- $p$ [s/m] is constant along the entire ray path

</div>

---

# Snell's Law: General Form

At any interface, one incident wave produces four outgoing waves:

$$\frac{\sin\theta_i}{V_{P1}} = \frac{\sin\theta_{P\text{refl}}}{V_{P1}} = \frac{\sin\theta_{P\text{refr}}}{V_{P2}} = \frac{\sin\theta_{S\text{refr}}}{V_{S2}} = p$$

**Key rule:** use the velocity of the *wave type* in the *medium it travels in*

- Incident P at 30°, $V_{P1} = 3$ km/s, $V_{P2} = 5$ km/s:
  $\theta_{P2} = \arcsin(5/3 \times \sin 30°) = \arcsin(0.833) = 56.4°$

- Converted S ($V_{S2} = 3$ km/s):
  $\theta_{S2} = \arcsin(3/3 \times \sin 30°) = \arcsin(0.5) = 30°$

---

# Fermat's Principle

> A seismic ray takes the path of **stationary travel time** between two points

$$T = \int_\Gamma \frac{ds}{V(x,z)}$$

Setting $\delta T = 0$ → **ray equation** → reduces to Snell's law at each interface

For a single layer (velocity $V_1$, thickness $H$, over half-space $V_2$):

| Arrival | Travel time $T(x)$ |
|---------|-------------------|
| Direct | $x / V_1$ |
| Reflected | $\sqrt{x^2 + 4H^2}\,/\,V_1$ (hyperbola) |
| Refracted (head) | $x/V_2 + 2H\cos\theta_c/V_1$ (linear) |

---

# Critical Refraction and Head Waves

When $V_2 > V_1$, there exists an angle at which $\theta_2 = 90°$:

<div class="key-eq">

$$\sin\theta_c = \frac{V_1}{V_2} \qquad\Rightarrow\qquad \theta_c = \arcsin\!\left(\frac{V_1}{V_2}\right)$$

The refracted wave travels **along the interface** at $V_2$, radiating energy back at angle $\theta_c$ → **head wave**

Head wave $T(x) = \dfrac{x}{V_2} + \underbrace{\dfrac{2H\cos\theta_c}{V_1}}_{\text{intercept time}}$

</div>

Slope of $T$–$x$ line = $1/V_2$ → read off $V_2$ directly

---

# Reading a Travel-Time Plot

**Two-layer model:** $V_1 = 2000$ m/s, $V_2 = 5000$ m/s, $H = 100$ m

- Direct wave: slope $= 1/V_1 = 0.5$ ms/m
- Head wave: slope $= 1/V_2 = 0.2$ ms/m
- Crossover distance: $x_\text{cross} = 2H\sqrt{(V_2+V_1)/(V_2-V_1)} \approx 224$ m
- Intercept time: $t_i = 2H\cos\theta_c/V_1$; from $t_i$ and slopes → recover $H$

<div class="callout">
The entire method depends on reading slopes on a T–x plot.
Lab 2 will have you do exactly this in Python.
</div>

---

# Worked Example: S–P Method

Seismogram: $t_P = 42.0$ s, $t_S = 74.8$ s; $V_P = 6.2$ km/s, $V_P/V_S = \sqrt{3}$

$$V_S = 6.2/\sqrt{3} = 3.58 \text{ km/s}$$

$$\Delta t = 74.8 - 42.0 = 32.8 \text{ s}$$

$$d = \frac{\Delta t}{1/V_S - 1/V_P} = \frac{32.8}{0.279 - 0.161} = \frac{32.8}{0.118} \approx 278 \text{ km}$$

**Single-station distance estimate from wave-type timing difference**

---

# AI Literacy: Machine-Learning Phase Picking

PhaseNet, EQTransformer: deep learning models that auto-pick P and S arrivals

They exploit the *same physics*:
- P arrives first (vertical motion)
- S arrives ~73% later with transverse motion
- Waveform envelope shape differs between P and S

**Epistemics prompt:**
> *"A phase picker labels an arrival as P with 97% confidence, but it appears only on horizontal components. Is this consistent with P-wave physics? What could explain it?"*

Evaluate: Does the AI flag the tension? Suggest alternative explanations (steep incidence, mode conversion, instrument issue)?

---

# Concept Check

1. A Love wave at period 10 s has phase speed 3.2 km/s; at 30 s, 3.8 km/s. What does this tell you about how $V_S$ changes with depth? Estimate the depth sampled by each period.

2. S-waves from distant earthquakes are absent at the antipodal station. Using *only* the physics of this lecture, explain what this tells us about the outer core.

3. $V_1 = 2000$ m/s, $V_2 = 3500$ m/s, $H = 150$ m. Find: critical angle, crossover distance, and which arrival (direct or head wave) comes first at $x = 400$ m.

---

# Summary

| Wave | Motion | Speed | Medium |
|------|--------|-------|--------|
| P | Longitudinal (∥ prop.) | $\sqrt{(\lambda+2\mu)/\rho}$ | Solid + fluid |
| S | Transverse (⊥ prop.) | $\sqrt{\mu/\rho}$ | Solid only |
| Rayleigh | Retrograde ellipse | $\approx 0.92\,V_S$ | Any half-space |
| Love | Transverse (SH) | $V_{S1}<V_L<V_{S2}$ | Layered only |

**Snell's law:** $\sin\theta_1/V_1 = \sin\theta_2/V_2 = p$ (constant)

**Critical angle:** $\sin\theta_c = V_1/V_2$ → head waves → refraction surveys

**Next lecture:** Reflection seismology and the NMO correction
