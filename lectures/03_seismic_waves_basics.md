---
title: "Stress, Strain, and Seismic Waves"
week: 1
lecture: 3
date: "2026-04-02"
topic: "Elastic deformation, the stress and strain tensors, Hooke's law, the 1D wave equation, and seismic wave types"
course_lo: ["LO-1", "LO-2", "LO-5"]
learning_outcomes: ["LO-OUT-B", "LO-OUT-C"]
open_sources:
  - "Lowrie & Fichtner (2020) Ch. 3, §3.1–3.3 (free via UW Libraries)"
  - "MIT OCW 12.201 §4.3–4.6 (CC BY NC SA, ocw.mit.edu)"
  - "MIT OCW 12.510 Lec 2-3 (CC BY NC SA, ocw.mit.edu)"
  - "IRIS/EarthScope wave animations (CC BY, iris.edu)"
  - "Fukushima et al. (2024), GJI, doi:10.1093/gji/ggae103 [Research Horizon]"
---

# Stress, Strain, and Seismic Waves

## Syllabus Alignment

| | |
|---|---|
| **Course LOs addressed** | LO-1 (how elastic deformation gives rise to seismic observables), LO-2 (wave equation predicts wave speeds from material properties), LO-5 (companion notebook explores Vp/Vs sensitivity) |
| **Learning outcomes practiced** | LO-OUT-B (compute Vp, Vs from moduli; identify wave type from particle motion), LO-OUT-C (explain *why* S-waves cannot travel through fluids) |
| **Lowrie & Fichtner chapter** | Ch. 3, §3.1–3.3 (free via UW Libraries) |
| **Next lecture** | Lecture 4 — Wavefronts and Rays |
| **Lab connection** | Lab 2: Python II and Seismic Ray Tracing |

---

## Learning Objectives

By the end of this lecture, students will be able to:

- **[LO-3.1]** *Define* the stress tensor $\boldsymbol{\sigma}$ and strain tensor $\boldsymbol{\varepsilon}$ in 3D Cartesian coordinates and identify normal versus shear components.
- **[LO-3.2]** *Explain* Hookean (linear elastic) behavior and write the isotropic form of Hooke's law using the Lamé parameters $\lambda$ and $\mu$.
- **[LO-3.3]** *Derive* the 1D elastic wave equation from Newton's second law applied to a continuum element, and identify the P-wave speed $V_P = \sqrt{(\lambda + 2\mu)/\rho}$.
- **[LO-3.4]** *Distinguish* body waves (P, S) from surface waves (Rayleigh, Love) by particle motion geometry, polarization, and speed relative to $V_S$.
- **[LO-3.5]** *Analyze* why S-waves cannot propagate in a fluid by connecting particle motion physics to the requirement $\mu \neq 0$.

---

## Prerequisites

Students should be comfortable with:
- Vectors and Cartesian coordinates (MATH 126)
- Newton's second law and force balance (PHYS 122/115)
- The concept of a derivative and basic partial differentiation
- Lecture 2 definitions: stress = F/A, strain = ΔL/L

---

## 1. The Geoscientific Question

Every time an earthquake shakes Seattle, instruments around the world record its waves within minutes. From those recordings alone — without ever drilling a single hole — geophysicists reconstruct where the rupture occurred, how deep it was, how much energy it released, and even details about the rocks it traveled through. This remarkable capability rests on a single physical foundation: **the Earth deforms elastically under seismic stresses, and that deformation propagates as waves whose speed is set by the material properties of the rock**.

To use seismic waves as a probe of Earth structure, we need to understand what kinds of waves exist, how they move, and how their speed connects to the elastic properties of the medium. That is the subject of this lecture. We begin with the mechanics of deformation — stress and strain — and build from there to the wave equation and the four fundamental seismic wave types you will encounter throughout this course.

:::{admonition} The Central Connection
:class: important
The elastic moduli of rock ($\lambda$, $\mu$, $\rho$) control seismic wave speeds. Measuring wave speeds from seismograms allows us to infer elastic moduli at depth — the foundation of the entire field of seismic imaging.
:::

---

## 2. Governing Physics: Elastic Deformation

### 2.1 What is Elastic Deformation?

When a seismic wave passes through rock, it deforms the rock slightly — stretching, compressing, or shearing it — and then the rock springs back. This behavior is called **elastic deformation**: the material returns to its original shape once the stress is removed. The key assumption underlying almost all of seismology is that **seismic strains are small enough that the rock behaves linearly and elastically**.

Contrast this with what happens at very high stresses (deep in a subduction zone, near a fault, under a volcano): the rock may deform permanently, creep, or fracture. Seismic waves are not in that regime — their strain amplitudes are typically $\sim 10^{-6}$ to $10^{-8}$, far below the elastic limit.

:::{figure} ../_static/images/fig_stress_strain_curve.png
:name: fig-stress-strain
:alt: Stress-strain curve for an elastic solid showing four zones: a blue linear region labeled "Hooke's law" where stress and strain are proportional, an amber nonlinear elastic zone, an orange plastic deformation zone beyond the elastic limit, and a dashed green unloading path from the elastic limit back to a permanent strain offset. Bracket annotations indicate the elastic range and plastic deformation range along the top. Vertical dashed lines mark the linearity limit and elastic limit.
:width: 85%

**Figure 3.1.** Stress–strain behavior of an elastic solid. Seismic waves operate entirely in the blue linear-elastic (Hookean) region, where strain is proportional to stress and fully recoverable. The amber and orange zones represent higher-stress behavior relevant to fault mechanics and rock failure, not wave propagation. [Python-generated. Script: `../assets/scripts/fig_stress_strain_curve.py`]
:::

### 2.2 The Two Types of Elastic Deformation

All elastic deformation of a 3D solid can be decomposed into two fundamental modes:

**Volumetric strain (dilatation)** — a change in volume without change in shape. Confining pressure acts equally from all sides, compressing or expanding the material. This is the deformation mode relevant to P-waves.

**Shear strain** — a change in shape without change in volume. One face slides relative to an opposite face, distorting rectangles into parallelograms. This is the deformation mode relevant to S-waves. Crucially, **fluids cannot sustain shear stress** — they flow rather than resist shearing — which is why S-waves do not propagate in water, magma, or the outer core.

---

## 3. Mathematical Framework

### 3.1 The Stress Tensor

:::{admonition} Notation
:class: note
| Symbol | Quantity | Units | Type |
|--------|----------|-------|------|
| $\mathbf{F}$ | Force vector | N | vector |
| $A$ | Surface area | m² | scalar |
| $\sigma_{ij}$ | Stress component: force in $i$-direction on face with normal in $j$-direction | Pa = N/m² | tensor component |
| $\boldsymbol{\sigma}$ | Stress tensor | Pa | 2nd-order tensor |
| $\varepsilon_{ij}$ | Strain component | dimensionless | tensor component |
| $\boldsymbol{\varepsilon}$ | Strain tensor | — | 2nd-order tensor |
| $u_i$ | Displacement in direction $i$ | m | vector component |
| $\lambda, \mu$ | Lamé parameters | Pa | scalars |
| $\rho$ | Density | kg/m³ | scalar |
| $\theta$ | Dilatation (volumetric strain) | dimensionless | scalar |
| $\delta_{ij}$ | Kronecker delta ($=1$ if $i=j$, $=0$ otherwise) | — | — |
:::

Stress is the force per unit area acting across a surface inside a material. In 3D, the full stress state at a point requires specifying the force components on three mutually perpendicular surfaces, giving nine components $\sigma_{ij}$ — the **stress tensor**:

$$
\boldsymbol{\sigma} = \begin{pmatrix}
\sigma_{xx} & \sigma_{xy} & \sigma_{xz} \\
\sigma_{yx} & \sigma_{yy} & \sigma_{yz} \\
\sigma_{zx} & \sigma_{zy} & \sigma_{zz}
\end{pmatrix}
$$ (eq:stress-tensor)

The diagonal components ($\sigma_{xx}$, $\sigma_{yy}$, $\sigma_{zz}$) are **normal stresses** — they act perpendicular to the surface face, either compressing or stretching the material. The off-diagonal components ($\sigma_{xy}$, etc.) are **shear stresses** — they act parallel to the surface, distorting the shape.

By conservation of angular momentum (no net rotation), the stress tensor is symmetric: $\sigma_{ij} = \sigma_{ji}$. This reduces the 9 independent components to just **6**.

:::{figure} ../_static/images/fig_stress_tensor.png
:name: fig-stress-tensor
:alt: Two 3D diagrams side by side. Left panel shows a square surface element in the y-z plane with three force arrows: a blue normal force perpendicular to the surface labeled Fy, and two orange shear forces parallel to the surface labeled Fx and Fz. Right panel shows a unit cube with blue normal stress arrows labeled sigma_xx, sigma_yy, sigma_zz pointing outward from each face, and orange dashed shear stress arrows labeled sigma_xy, sigma_xz, sigma_yx, sigma_yz pointing tangentially along the faces.
:width: 88%

**Figure 3.2.** The stress tensor in 3D. Left: forces on a single surface element decompose into one normal stress and two shear stresses. Right: the full stress tensor on a unit cube — 9 components, reduced to 6 by symmetry ($\sigma_{ij} = \sigma_{ji}$). [Python-generated. Script: `../assets/scripts/fig_stress_tensor.py`]
:::

### 3.2 The Strain Tensor

Strain measures how much a material deforms. Consider two neighboring points at positions $x$ and $x + \Delta x$ along one axis. If the material stretches, both points displace, but by different amounts $u$ and $u + \Delta u$. The **longitudinal strain** in the $x$-direction is:

$$
\varepsilon_{xx} = \frac{\Delta u}{\Delta x} \xrightarrow{\Delta x \to 0} \frac{\partial u_x}{\partial x}
$$ (eq:longitudinal-strain)

*Units check:* displacement [m] / length [m] = dimensionless ✓

In 3D, stretch can occur along all three axes independently, giving three normal strains. Shear strain measures angular distortion. If a square element tilts by angle $\psi$ under shear stress, the shear strain is:

$$
\varepsilon_{xy} = \frac{1}{2}\left(\frac{\partial u_x}{\partial y} + \frac{\partial u_y}{\partial x}\right)
$$ (eq:shear-strain)

The factor of $\frac{1}{2}$ ensures that pure rotation (which is not a deformation) contributes zero strain.

The full **strain tensor** is:

$$
\varepsilon_{ij} = \frac{1}{2}\left(\frac{\partial u_i}{\partial x_j} + \frac{\partial u_j}{\partial x_i}\right)
$$ (eq:strain-tensor)

:::{admonition} Key Equation
:class: important
Equation {eq}`eq:strain-tensor` expresses strain as the symmetric part of the displacement gradient. It automatically separates deformation from rigid rotation. Like stress, the strain tensor is symmetric ($\varepsilon_{ij} = \varepsilon_{ji}$) and has 6 independent components.
:::

The **dilatation** $\theta$ — the fractional change in volume — is the trace of the strain tensor:

$$
\theta = \varepsilon_{xx} + \varepsilon_{yy} + \varepsilon_{zz} = \nabla \cdot \mathbf{u}
$$ (eq:dilatation)

**Poisson's ratio** connects lateral and axial strains. When you compress a material along $x$, it bulges outward in $y$ and $z$:

$$
\nu = -\frac{\varepsilon_{yy}}{\varepsilon_{xx}} = -\frac{\Delta y / y}{\Delta x / x}
$$ (eq:poisson)

For most rocks, $0.2 \lesssim \nu \lesssim 0.35$. For fluids, $\nu = 0.5$ (incompressible). The ratio $V_P/V_S$ depends only on $\nu$ and is a powerful diagnostic of fluid saturation.

:::{figure} ../_static/images/fig_strain_types.png
:name: fig-strain-types
:alt: Three-panel figure. Panel (a) shows longitudinal strain: a tall blue rectangle (original cylinder) with a shorter dark blue rectangle (compressed state) below it, with dimension labels h and delta-h and a downward force arrow F at the bottom. Panel (b) shows volumetric strain: a light blue square (original volume V) with a smaller dark blue square (V minus delta V) inside it, with four pressure arrows pointing inward from each side labeled P. Panel (c) shows shear strain: a dashed light blue rectangle (original shape) and a dark blue parallelogram (sheared shape), with a horizontal orange shear stress arrow at the top and a small angle arc labeled psi at the lower-left corner.
:width: 90%

**Figure 3.3.** The three fundamental modes of elastic strain. (a) Longitudinal strain: $\varepsilon_{xx} = \Delta h/h$ — change in length along the stress direction. (b) Volumetric strain (dilatation): $\theta = \Delta V/V$ — change in volume under isotropic pressure. (c) Shear strain: $\gamma = \tan\psi$ — angular distortion. P-waves involve (a) and (b); S-waves involve (c) only. [Python-generated. Script: `../assets/scripts/fig_strain_types.py`]
:::

### 3.3 Hooke's Law: Connecting Stress to Strain

For an **isotropic** (direction-independent) linear elastic solid, the stress–strain relationship is:

$$
\sigma_{ij} = \lambda \, \delta_{ij} \, \theta + 2\mu \, \varepsilon_{ij}
$$ (eq:hookes-law)

*Units check:* $[\lambda]$ = Pa, $[\theta]$ = dimensionless, so $\lambda \theta$ = Pa. $[\mu]$ = Pa, $[\varepsilon_{ij}]$ = dimensionless, so $2\mu\varepsilon_{ij}$ = Pa. ✓

This is the **generalized Hooke's law** for isotropic media. The two **Lamé parameters** $\lambda$ and $\mu$ completely characterize the elastic behavior:

- $\mu$ (shear modulus / rigidity): resistance to shear deformation. $\mu = 0$ for fluids — they cannot sustain shear stress.
- $\lambda$ (first Lamé parameter): related to the bulk modulus via $K = \lambda + \frac{2}{3}\mu$.

For hydrostatic conditions (equal normal stresses = $-p$, no shear), equation {eq}`eq:hookes-law` gives:

$$
K = \lambda + \frac{2}{3}\mu
$$ (eq:bulk-modulus)

Writing out the $xx$ component explicitly:

$$
\sigma_{xx} = \lambda \theta + 2\mu \varepsilon_{xx}
$$ (eq:hookeslaw-xx)

The first term says: even if there is no elongation in the $x$ direction ($\varepsilon_{xx} = 0$), any volumetric change ($\theta \neq 0$) generates a normal stress in $x$ — the two deformation modes are coupled through $\lambda$.

### 3.4 Deriving the 1D P-wave Equation

We now derive the equation governing how a compressional disturbance propagates through an elastic rod — the 1D version of the P-wave equation.

Consider a thin element of elastic material between positions $x$ and $x + dx$, with cross-sectional area $A_x$ and density $\rho$. Its mass is:

$$
m = \rho \, A_x \, dx
$$ (eq:mass-element)

The force on the left face is $F_x = A_x \sigma_{xx}$. The force on the right face is $F_x + dF_x = A_x (\sigma_{xx} + \frac{\partial \sigma_{xx}}{\partial x} dx)$. The net force on the element is:

$$
dF_x = A_x \frac{\partial \sigma_{xx}}{\partial x} \, dx
$$ (eq:net-force)

Applying Newton's second law $\Sigma F = ma$ (where $a = \partial^2 u/\partial t^2$ is the particle acceleration):

$$
A_x \frac{\partial \sigma_{xx}}{\partial x} \, dx = \rho \, A_x \, dx \, \frac{\partial^2 u}{\partial t^2}
$$

$$
\rho \frac{\partial^2 u}{\partial t^2} = \frac{\partial \sigma_{xx}}{\partial x}
$$ (eq:motion-1d)

Now substitute Hooke's law. For a 1D longitudinal wave, $\varepsilon_{xx} = \partial u / \partial x$ and $\sigma_{xx} = (\lambda + 2\mu) \varepsilon_{xx}$, so:

$$
\rho \frac{\partial^2 u}{\partial t^2} = (\lambda + 2\mu) \frac{\partial^2 u}{\partial x^2}
$$ (eq:wave-equation-1d)

:::{admonition} Key Equation: 1D P-wave Equation
:class: important
$$
\rho \frac{\partial^2 u}{\partial t^2} = (\lambda + 2\mu) \frac{\partial^2 u}{\partial x^2}
$$

This has the standard wave equation form $\partial^2 u/\partial t^2 = V^2 \, \partial^2 u/\partial x^2$ with:

$$
V_P = \sqrt{\frac{\lambda + 2\mu}{\rho}}
$$ (eq:vp)

**Left side:** the inertial term — how much mass must be accelerated.
**Right side:** the elastic restoring term — how strongly the medium resists strain.
**Their ratio** sets the wave speed. Stiffer rock ($\lambda + 2\mu$ large) → faster waves. Denser rock ($\rho$ large) → slower waves.
:::

By the same derivation for shear motion, the S-wave equation gives:

$$
\rho \frac{\partial^2 u}{\partial t^2} = \mu \frac{\partial^2 u}{\partial x^2} \qquad \Rightarrow \qquad V_S = \sqrt{\frac{\mu}{\rho}}
$$ (eq:vs)

*Units check for $V_P$:* $\sqrt{\text{Pa}/(\text{kg/m}^3)} = \sqrt{(\text{kg/m·s}^2)/(\text{kg/m}^3)} = \sqrt{\text{m}^2/\text{s}^2}$ = m/s ✓

Since $\lambda + 2\mu > \mu$ (for any stable elastic material, $\lambda > 0$), we always have $V_P > V_S$.

---

## 4. Types of Seismic Waves

### 4.1 Body Waves: Traveling Through the Interior

**P-waves** (Primary or Compressional) are longitudinal waves: particle motion is **parallel** to the propagation direction, alternating between compression and rarefaction. They travel at speed $V_P$ and are the fastest seismic arrivals.

**S-waves** (Secondary or Shear) are transverse waves: particle motion is **perpendicular** to the propagation direction. Their speed is $V_S < V_P$. S-waves come in two polarizations:
- **SV**: particle motion in the vertical plane containing the ray
- **SH**: particle motion horizontal and perpendicular to the ray

Because $\mu = 0$ in a fluid, equation {eq}`eq:vs` gives $V_S = 0$ — **S-waves cannot propagate in fluids**. This is not a quirk of the math; it reflects the physical fact that a fluid cannot sustain the shear stress that would provide the restoring force for transverse oscillation.

:::{figure} ../_static/images/fig_pwave_illustration.png
:name: fig-pwave
:alt: A horizontal band of elastic medium contains a row of circles representing particles. Dark blue clusters of closely-spaced circles mark compression zones labeled C; light blue widely-spaced circles mark rarefaction zones labeled R, alternating across two full wavelengths. Orange arrows between adjacent particles indicate longitudinal displacement parallel to the green propagation arrow at top. A wavelength brace spans one C-R cycle. A callout box gives V_P equals square root of (lambda plus 2 mu) over rho, noting it travels in solids and fluids.
:width: 92%

**Figure 3.4a.** P-wave particle motion: compression (C) and rarefaction (R) zones alternate as particles oscillate *parallel* to the propagation direction. Color (dark vs. light blue) and arrow direction both encode the compression state, independently of each other (colorblind-accessible). [Python-generated. Script: `../assets/scripts/fig_pwave_swave_motion.py`]
:::

:::{figure} ../_static/images/fig_swave_illustration.png
:name: fig-swave
:alt: A horizontal band of elastic medium contains a row of gray-blue circles tracing a sinusoidal transverse path, alternating above and below a dashed equilibrium line. Orange arrows from the equilibrium line to each displaced particle show vertical (transverse) displacement perpendicular to the horizontal propagation arrow at top. An amplitude brace at left labels A. A callout box reads: V_S equals square root of mu over rho, so mu equals zero in fluids means V_S equals zero, so S-waves CANNOT travel in fluids. Labels on the right identify SV as vertical shear and SH as horizontal shear.
:width: 92%

**Figure 3.4b.** S-wave particle motion: particles oscillate *perpendicular* to the propagation direction (transverse). Because the restoring force requires $\mu \neq 0$, S-waves are absent in any fluid (the liquid outer core, ocean water, magma). [Python-generated. Script: `../assets/scripts/fig_pwave_swave_motion.py`]
:::

### 4.2 Surface Waves: Trapped Near the Free Surface

When body waves reach the free surface, boundary conditions allow new wave types that are trapped near the surface and decay exponentially with depth.

**Rayleigh waves** combine P and SV motion. Particles trace **retrograde ellipses** in the vertical plane containing the ray — moving backward and upward at the wave crest. Their speed is $V_R \approx 0.92 V_S$, slightly slower than shear waves. Amplitude decays as $e^{-kz}$ (where $k = 2\pi/\lambda$), becoming negligible below depths of about $0.4\lambda$. This depth sensitivity is the basis for **surface wave tomography**: longer-wavelength Rayleigh waves sample deeper, so measuring dispersion gives a depth profile of $V_S$.

**Love waves** require a velocity gradient: a slower surface layer over a faster half-space. They are formed by constructive interference of SH waves trapped between the free surface and the layer interface by total internal reflection. Particle motion is purely horizontal (SH), with phase velocity between $V_{S1}$ and $V_{S2}$.

:::{admonition} Key Contrast
:class: note
- Rayleigh waves exist in any homogeneous half-space; they always involve both P and SV motion.
- Love waves require a velocity layering — they are absent in a homogeneous half-space.
- Both are **dispersive** (phase velocity depends on frequency/wavelength), unlike body waves in a homogeneous medium.
:::

:::{figure} ../_static/images/fig_surface_waves.png
:name: fig-surface-waves
:alt: Three-panel figure. Left panel shows Rayleigh wave retrograde elliptical particle trajectories at multiple depths, with ellipses shrinking from large near the surface to tiny at depth. Middle panel shows a depth versus amplitude curve, with amplitude decreasing exponentially from 1.0 at the surface to near-zero at depth about 2 wavelengths, with a dashed horizontal line marking the 0.4-wavelength depth and a label V_R approximately 0.92 V_S. Right panel shows a cross-section with a light blue slow surface layer over a green fast half-space, with orange dashed zigzag rays bouncing between the free surface (top) and the interface, illustrating SH wave trapping by total internal reflection. Dot symbols on the rays show horizontal transverse particle motion.
:width: 92%

**Figure 3.5.** Surface waves. Left: Rayleigh wave retrograde elliptical motion, decaying exponentially with depth. Center: amplitude vs. depth — significant only to about $0.4\lambda$. Right: Love wave formation by total internal reflection of SH waves in a slow surface layer ($\beta_1$) over a fast half-space ($\beta_2 > \beta_1$). [Python-generated. Script: `../assets/scripts/fig_surface_waves.py`]
:::

### 4.3 The Point-Source Radiation Pattern

A seismic source (earthquake or explosion) near the surface generates both body waves and surface waves simultaneously. Body waves expand as spherical shells (hemispheres in the downward-propagating sense), while surface waves expand as concentric circles on the surface. Rays — the lines perpendicular to wavefronts — indicate the direction of energy propagation.

:::{figure} ../_static/images/fig_point_source_wavefronts.png
:name: fig-point-source
:alt: A 3D perspective view with a horizontal plane representing the Earth surface and a curved lower hemisphere representing the subsurface. From a central source point P, concentric hemispherical shells in orange-red (labeled "body wave wavefront") expand downward through the subsurface. At the surface, concentric circles in blue (labeled "surface wave") expand outward. Green arrows radiate from the source point in all directions, labeled "rays perpendicular to wavefront."
:width: 80%

**Figure 3.6.** Seismic radiation from a point source $P$: body waves propagate as expanding spherical wavefronts through the interior; surface waves propagate as expanding circles on the free surface. Rays are everywhere perpendicular to wavefronts. [Python-generated. Script: `../assets/scripts/fig_point_source_wavefronts.py`]
:::

### 4.4 Typical P-wave Velocities

Wave speeds vary enormously across Earth materials, spanning nearly two orders of magnitude:

:::{figure} ../_static/images/fig_seismic_velocities.png
:name: fig-seismic-velocities
:alt: Horizontal bar chart with material names on the vertical axis and P-wave velocity in meters per second on the horizontal axis from 0 to 8000 m/s. Bars are colored by category: dark blue bars for crystalline and sedimentary rocks (Granite, Basalt, Limestone, Sandstone, Salt rock, Shale) spanning roughly 2000 to 6500 m/s; sky-blue bars for unconsolidated sediments (Dry sand, Wet sand, Clay) with much shorter bars from 60 to 2000 m/s; green bars for fluids (Seawater, Freshwater, Oil) near 1200 to 1540 m/s; and amber bars for engineering materials (Steel, Aluminum, Concrete, Ice). A vertical dotted reference line marks 1480 m/s for water. Each bar has a white dot at its midpoint and a numeric range label at the right end.
:width: 85%

**Figure 3.7.** Representative $V_P$ ranges for Earth and engineering materials. Note: (1) rocks with higher stiffness or lower porosity have faster velocities; (2) fluids cluster near 1200–1540 m/s and have $V_S = 0$; (3) unconsolidated soil (dry sand, clay) can be extremely slow, causing dangerous ground-motion amplification in earthquakes. [Python-generated. Script: `../assets/scripts/fig_seismic_velocities.py`]
:::

A useful rule of thumb: for typical crustal rock with $\nu \approx 0.25$ (Poisson's ratio), $V_P / V_S \approx \sqrt{3} \approx 1.73$. Fluid-saturated rocks have $\nu$ closer to 0.5, giving higher $V_P/V_S$ — this is a key diagnostic used in seismic exploration and volcanic monitoring.

---

## 5. The Forward and Inverse Problems

### 5.1 The Forward Problem

Given the elastic properties of a rock column ($\lambda(z)$, $\mu(z)$, $\rho(z)$), the forward problem predicts:
- P-wave speed $V_P(z) = \sqrt{(\lambda + 2\mu)/\rho}$
- S-wave speed $V_S(z) = \sqrt{\mu/\rho}$
- The travel time for a seismic ray from source to receiver
- The waveform and amplitude of ground motion

See companion notebook: `notebooks/lecture_03_wave_speeds.ipynb`

### 5.2 The Inverse Problem (First Look)

:::{admonition} Inverse Problem Setup
:class: tip
- **Data $d$:** P-wave and S-wave travel times measured at seismometers
- **Model $m$:** velocity structure $V_P(z)$ and $V_S(z)$ at depth
- **Forward relation:** $d = G(m)$ where $G$ computes travel times from the velocity model
- **Key non-uniqueness:** Many different velocity models can produce the same set of travel times
- **What we can't directly infer:** Density $\rho$ is not independently recoverable from travel times alone (you need amplitude information too)
:::

---

## 6. Worked Example

**Problem:** A seismograph records a P-wave arrival at $t_P = 42.0$ s and an S-wave arrival at $t_S = 74.8$ s after an earthquake. The crustal P-wave velocity is $V_P = 6.2$ km/s. Assuming $V_P / V_S = \sqrt{3}$, estimate the distance to the earthquake.

**Solution:**

First, find $V_S$: $V_S = V_P / \sqrt{3} = 6.2 / 1.732 = 3.58$ km/s

The S–P time difference is:
$$
\Delta t = t_S - t_P = 74.8 - 42.0 = 32.8 \text{ s}
$$

Since both waves travel the same distance $d$ at their respective speeds:
$$
\Delta t = \frac{d}{V_S} - \frac{d}{V_P} = d\left(\frac{1}{V_S} - \frac{1}{V_P}\right)
$$

Solving for $d$:
$$
d = \frac{\Delta t}{\frac{1}{V_S} - \frac{1}{V_P}} = \frac{32.8}{\frac{1}{3.58} - \frac{1}{6.2}} = \frac{32.8}{0.2793 - 0.1613} = \frac{32.8}{0.1180} \approx 278 \text{ km}
$$

This technique — known as the **S–P method** — is how seismologists rapidly estimate earthquake distances from a single station.

:::{admonition} Concept Check
:class: tip
1. A rock has $\lambda = 30$ GPa, $\mu = 25$ GPa, and $\rho = 2700$ kg/m³. Calculate $V_P$ and $V_S$. Show units. What is $V_P/V_S$ and what Poisson's ratio does it correspond to?
2. You measure that $V_S$ in a sediment layer is 120 m/s but $V_P$ is 1500 m/s — much larger than you'd expect for $\nu \approx 0.25$. What does this tell you about the sediment's physical state?
3. A surface wave tomography study uses Rayleigh waves with periods of 10 s and 30 s. If $V_R \approx 3.5$ km/s, approximately what depths do these two periods sample? (Use $\lambda = V_R \cdot T$ and depth $\approx 0.4\lambda$.)
:::

---

## 7. Course Connections

- **Prior lectures:** This lecture applies the stress–strain foundations from Lecture 2 directly to wave propagation. The key step is combining Hooke's law with Newton's second law to get a wave equation.
- **Next lecture (Lecture 4):** Wavefronts and rays — building the geometric framework for predicting where seismic energy travels.
- **Lecture 7:** Snell's Law and wave behavior at boundaries — what happens when waves cross the interface between two elastic materials.
- **Lab 2:** Seismic ray tracing — you'll write code that numerically traces rays through a layered velocity model using the velocities derived here.
- **Module connection:** The $V_P/V_S$ ratio derived here reappears in every geophysical method. In earthquake seismology it diagnoses fluids; in exploration seismology it identifies gas sands; in volcanology it detects magma chambers.

---

## 8. Research Horizon

:::{admonition} Current Research Highlights (2022–2025)
:class: seealso

**Fiber-optic seismology (DAS) is transforming surface wave imaging.** Distributed Acoustic Sensing (DAS) converts existing fiber-optic telecommunication cables into dense seismic arrays with meter-scale spacing over tens of kilometers. Because DAS records strain (not displacement), it is naturally sensitive to Rayleigh waves — the surface wave type introduced in this lecture. Recent studies demonstrate that DAS arrays deployed along submarine cables can image shallow sediment structure and ancient river channels using Rayleigh-wave dispersion inversion (Viens et al., 2023, *Geophys. J. Int.*, doi:10.1093/gji/ggac420). New methods combine DAS with conventional seismometers to separately extract Rayleigh and Love wave signals, improving velocity model resolution (Fukushima et al., 2024, *Geophys. J. Int.*, doi:10.1093/gji/ggae103).

**The $V_P/V_S$ ratio as a fluid monitor.** The wave speed equations derived in this lecture ($V_P = \sqrt{(\lambda+2\mu)/\rho}$, $V_S = \sqrt{\mu/\rho}$) predict that $V_P/V_S$ rises sharply when pore fluids replace gas (because pore fluids raise $K$ but do not contribute to $\mu$). Researchers are now using time-lapse seismic measurements of $V_P/V_S$ changes to monitor $\text{CO}_2$ injection in carbon storage projects and fluid migration around volcanoes — applying the same physics you derived today.

**Open-source learning resource:** The seismo-live library (seismo-live.org) contains runnable Jupyter notebooks on elastic wave propagation, including hands-on derivations of the wave equation and interactive visualizations of P/S/Rayleigh/Love motion. These directly complement this lecture.

*For students interested in research in this area:* The EarthScope Seismology Skill Building Workshop (SSBW) runs each summer and teaches ObsPy-based surface wave analysis to undergraduates — directly applying the wave types you just learned. See iris.edu/hq/workshops for current offerings.
:::

---

## 9. Societal Relevance

:::{admonition} Why It Matters: Seismic Hazard in the Pacific Northwest
:class: note

**The Seattle Basin effect:** Seattle sits on a deep sedimentary basin — the Seattle Basin — filled with soft, water-saturated sediments with $V_S$ as low as 200–400 m/s, compared to 3000+ m/s in bedrock. When seismic waves enter this slow material, they slow down (wave energy is conserved: slower = larger amplitude), and surface waves become trapped, causing shaking to last much longer than in nearby bedrock areas. The 2001 Nisqually earthquake (M6.8) demonstrated this dramatically, with significantly more damage in Seattle's Pioneer Square (on the basin) than in surrounding higher-elevation areas.

Understanding this requires knowing exactly the physics developed in this lecture: how wave speeds depend on elastic moduli (which depend on sediment properties and water content), and how surface waves are generated and trapped when velocity contrasts exist.

**The Cascadia Subduction Zone:** The Pacific Northwest faces a potential magnitude 8.0–9.0 Cascadia megathrust earthquake. The elastic energy accumulated on this fault will release as body waves (felt immediately) and generate large surface waves and a tsunami. The USGS and PNSN (Pacific Northwest Seismic Network) use the wave physics from this lecture to model shaking scenarios for emergency planning.

**For further exploration:**
- PNSN "Did you feel it?" map and real-time seismograms: pnsn.org
- USGS ShakeMap for the 2001 Nisqually earthquake: earthquake.usgs.gov/earthquakes/eventpage/usp0005mge
- USGS probabilistic seismic hazard maps for the Pacific Northwest: earthquake.usgs.gov/hazards/hazmaps
:::

---

## AI Literacy

:::{admonition} AI as a Reasoning Partner: Checking Your Derivation
:class: seealso

The 1D wave equation derivation in §3.4 is a gateway skill: you'll use the same pattern (force balance on an infinitesimal element → Newton's 2nd law → wave equation) in many future contexts. AI can help you check your reasoning — but you must evaluate its response carefully.

**After working through the derivation yourself, try this prompt:**

> *"I derived the 1D P-wave equation by considering a mass element ρ·dx·Ax, applying Newton's second law, and substituting Hooke's law σ_xx = (λ+2μ)·∂u/∂x. I got ρ·∂²u/∂t² = (λ+2μ)·∂²u/∂x². Can you check whether my physics reasoning is correct and identify any step where students commonly make errors?"*

**What to look for in the response:**
- Does it correctly identify the physical origin of each term (inertia vs. elastic restoring force)?
- Does it catch any ambiguity in your notation (e.g., did you use $E$ vs. $\lambda + 2\mu$)?
- Does it mention the implicit assumptions: small-strain, linear elastic, isotropic, homogeneous medium?

**Prompt 2 — Testing the fluid case:**

> *"Using V_S = sqrt(mu/rho), explain physically why S-waves cannot propagate in a fluid. Your answer should not just cite mu=0 — explain what physical property of fluids makes mu zero."*

*Evaluate:* Does the AI explain that fluids flow rather than resist shear stress — that molecules rearrange rather than spring back? Or does it just repeat the formula without physical insight?

**LO-7 connection:** Using AI as a derivation checker models good scientific practice: get an independent check, evaluate the response critically, and note any discrepancies. Document what you asked and how you evaluated the answer.
:::

:::{admonition} AI Prompt Lab
:class: tip

Try these prompts and evaluate each response before trusting it.

**Prompt 1:**
> *"A seismic survey in a sedimentary basin measures Vp = 1800 m/s and Vs = 300 m/s. What is the Poisson's ratio? What does this tell you about the physical state of the sediment?"*
Evaluate: Does the AI use the correct formula $\nu = (V_P^2 - 2V_S^2) / (2(V_P^2 - V_S^2))$? Does it correctly interpret the high $V_P/V_S$ as evidence of water saturation?

**Prompt 2:**
> *"What is the difference between the shear modulus mu and the Lamé parameter lambda? Which one controls S-wave speed and which one controls the difference between P-wave and S-wave speeds?"*
Evaluate: Does the response clearly state that $\mu$ controls $V_S$ while $\lambda$ contributes only to $V_P$? Does it note that $\lambda$ has no simple geometric interpretation, unlike $\mu$ (rigidity) or $K$ (incompressibility)?

**Prompt 3 (epistemics):**
> *"Is the equation V_P = sqrt(E/rho) or V_P = sqrt((lambda+2*mu)/rho)?"*
Evaluate: Both can be correct in specific contexts — $E$ (Young's modulus) applies to a thin rod in uniaxial stress; $\lambda + 2\mu$ applies to a 3D bulk wave. Does the AI explain this context dependence, or does it give one answer confidently without qualification?
:::

---

## Further Reading

Open-access sources used in preparing this lecture:

- **Lowrie, W. & Fichtner, A.** (2020). *Fundamentals of Geophysics*, 3rd ed. Cambridge University Press. §3.1–3.3. Free via UW Libraries. DOI: 10.1017/9781108685917
- **MIT OCW 12.201** (Van Der Hilst, 2004). Essentials of Geophysics, §4.3–4.6: Strain, stress, wave equation, P and S waves. CC BY NC SA. URL: ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004
- **MIT OCW 12.510** (2010). Introduction to Seismology, Lectures 2–3: Hooke's law, equations of motion, wave equation. CC BY NC SA. URL: ocw.mit.edu/courses/12-510-introduction-to-seismology-spring-2010
- **IRIS EarthScope Animations.** P-wave, S-wave, Rayleigh wave, Love wave — visual animations. CC BY. URL: iris.edu/hq/inclass/animation
- **Fukushima, S. et al.** (2024). Retrieval and precise phase-velocity estimation of Rayleigh waves by the spatial autocorrelation method between distributed acoustic sensing and seismometer data. *Geophysical Journal International*, 237(2), 1174–1188. DOI: 10.1093/gji/ggae103
- **Viens, L. et al.** (2023). Understanding surface wave modal content for high-resolution imaging of submarine sediments with distributed acoustic sensing. *Geophysical Journal International*, 232(3), 1668–1683. DOI: 10.1093/gji/ggac420
- **USGS.** ShakeMap for the 2001 Nisqually Earthquake. Public domain. URL: earthquake.usgs.gov/earthquakes/eventpage/usp0005mge

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
  title  = {12.201 Essentials of Geophysics, §4.3--4.6},
  year   = {2004},
  note   = {MIT OpenCourseWare, CC BY NC SA},
  url    = {https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004}
}

@article{fukushima2024,
  author  = {Fukushima, S. and others},
  title   = {Retrieval and precise phase-velocity estimation of {Rayleigh} waves by spatial autocorrelation between {DAS} and seismometer data},
  journal = {Geophysical Journal International},
  volume  = {237},
  number  = {2},
  pages   = {1174--1188},
  year    = {2024},
  doi     = {10.1093/gji/ggae103}
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
