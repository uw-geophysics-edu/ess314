---
title: "Isostasy and Lithospheric Flexure"
week: 7
lecture: 21
date: "2026-05-06"
topic: "Gravity III — How the lithosphere supports topography"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-C", "LO-OUT-D", "LO-OUT-F"]
open_sources:
  - "Lowrie & Fichtner (2020), Fundamentals of Geophysics, 3rd ed., Ch. 3.6 (UW Libraries)"
  - "Whitehouse (2018), Earth Surface Dynamics 6, 401–429 (CC BY 4.0)"
  - "Forte & Rowley (2022), Earth Planet. Sci. Lett. — open access via author manuscript"
  - "MIT OCW 12.201 lecture notes on isostasy and lithospheric strength (CC BY-NC-SA)"
---

# Isostasy and Lithospheric Flexure

::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-21.1]** State Archimedes' principle in the form used by isostasy and apply it to compute crustal-root thickness in Airy compensation and column density in Pratt compensation.
- **[LO-21.2]** Distinguish between *local* compensation (Airy / Pratt) and *regional* compensation (lithospheric flexure), and explain when each model is appropriate.
- **[LO-21.3]** Interpret a Bouguer anomaly profile across a mountain range as evidence for compensation, and describe the diagnostic value of the *isostatic-residual* anomaly.
- **[LO-21.4]** Estimate the timescale of post-glacial rebound from a measured uplift rate, and connect the timescale to mantle viscosity.
- **[LO-21.5]** Set up the thin-plate flexural equation and use the flexural parameter $\alpha$ to predict the wavelength of a forebulge near a topographic load.

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1, LO-2, LO-3 (forward and inverse), LO-4 |
| **Learning outcomes practiced** | LO-OUT-A, LO-OUT-C (explain *why*), LO-OUT-D (set up an inverse problem), LO-OUT-F (choose the right method for the scale) |
| **Prior lecture** | [L20 — Gravity Anomalies and Subsurface Modeling](20_gravity_anomalies.md) |
| **Next lecture** | [L22 — Density and Lithospheric Structure](22_density_lithosphere.md) |
| **Lab connection** | Lab 5 — Gravity Surveys (isostatic residual workflow) |
| **Discussion** | [Session 5 — Gravity, Ice Sheets, and CO₂](../discussions/session_05.md) |

::::

## Prerequisites

This lecture assumes facility with the gravity-reduction chain of Lecture 19 and the forward-modelling vocabulary of Lecture 20. The flexural-rigidity discussion in §3.5 builds on the elastic moduli introduced in the wave-physics module. Students unfamiliar with the equation $\nabla^{4} w$ can read it operationally — fourth derivative in space — and trust that the wave-physics module's Hookean elasticity is the same physics.

---

## 1. The Geoscientific Question

Mount Rainier rises 4392 m above sea level. The simplest cosmological argument places that much rock above the geoid as an *excess mass* — a deficit of equipotential, in the language of Lecture 19 — and predicts a $\sim 250$ mGal positive Bouguer anomaly over the summit. Measurements show the opposite: the Bouguer anomaly over the Cascade volcanic arc is broadly negative, of order $-100$ mGal, and the negative anomaly extends as a long-wavelength feature beneath the entire Cascadia mountain belt.

If the mountain were uncompensated, gravity over its summit would record the rock above sea level. It does not. The negative Bouguer anomaly says that beneath the mountain there is a *mass deficit* — light rock at depth — that almost exactly balances the topographic excess. The mountain is *floating*.

The same argument, made first by Pratt and Airy in the 1850s for the Himalaya, is the foundation of *isostasy*: the principle that topographic loads are supported, on geological timescales, by buoyancy. Two end-member implementations of this idea — Airy and Pratt isostasy — predict different deep-Earth structures from the same surface topography. Both models are useful idealisations of the real Earth, which compensates loads by some mixture of root-thickening and density-variation, modulated by the *strength* of the lithosphere itself.

This lecture develops the mathematical machinery for isostatic compensation, demonstrates how the *isostatic-residual* gravity anomaly diagnoses departures from full local compensation, and introduces lithospheric flexure as the regional-scale generalisation.

---

## 2. Governing Physics

### 2.1 Archimedes in cross-section

Hydrostatic equilibrium in a static fluid requires that the pressure at any horizontal depth be the same regardless of the column above it. Applied to an iceberg, this is Archimedes' principle: a floating body displaces its own weight of water. Applied to a mountain, the principle becomes the working statement of isostasy:

```{math}
:label: eq-isostasy
\rho_{\text{column,1}}(z) \cdot g \cdot dz \;=\; \rho_{\text{column,2}}(z) \cdot g \cdot dz \quad \text{at the depth of compensation}.
```

The *depth of compensation* is the level below which all columns produce the same pressure. Above it, columns differ. Below it, the asthenosphere flows freely on the relevant timescale, and any pressure imbalance drives lateral flow that restores equilibrium.

### 2.2 Two end-member compensation styles

The Airy and Pratt models are two ways of satisfying equation {eq}`eq-isostasy`.

In the **Airy** model, all crustal columns have the same density $\rho_{c}$. Topography is supported by *thickness variations* — high mountains have deep "roots" extending into the denser mantle, and ocean basins are underlain by *thin* crust whose base is shallower than the reference crust.

In the **Pratt** model, all columns extend to the same depth (the compensation depth) but have *different densities*. High topography sits on a less-dense column; low topography sits on a denser column. The equal-pressure condition at the compensation depth determines the density of each column.

```{figure} ../assets/figures/fig_airy_pratt.png
:name: fig-airy-pratt
:alt: Two side-by-side cross-sections illustrating the Airy and Pratt isostatic models. Panel a shows four crustal columns at heights 0, 1, 3, and 5 km, all with the same blue colour indicating uniform crustal density of 2700 kg per cubic metre, but with progressively deeper crustal roots extending below the 35-km reference crustal base into the underlying 3300 kg per cubic metre mantle. The roots are 0, 4.5, 13.5, and 22.5 km deep respectively. Panel b shows the same four heights compensated instead by varying density: all four columns extend to the same compensation depth of 35 km but their colours grade from dark blue (highest density 2700 at h equals 0) through olive green to orange (lowest density 2362 at h equals 5 km). A horizontal dashed line marks the compensation depth where pressure is uniform in the Pratt model.
:width: 100%

The two end-member models for compensating high topography. Both satisfy hydrostatic equilibrium at the depth of compensation, but they make different predictions for the deep structure: Airy implies thick roots; Pratt implies low-density columns. Real Earth applies a mixture — Airy dominates large-scale crustal features such as continents, while Pratt-type density variations dominate at the oceanic-continental boundary and near hot spots.
```

### 2.3 The flexural correction — a finite-strength lithosphere

The Airy and Pratt models assume *local* compensation: each column floats independently. Real lithosphere has elastic strength, and a vertical load at one point produces *regional* deformation that extends laterally for hundreds of kilometres. Flexural compensation produces a deflection that is broader and flatter than local compensation would predict, and creates a characteristic *forebulge* — a shallow-amplitude, long-wavelength upward deflection — beyond the load.

The choice of model is a question of *scale*: features wider than the lithosphere's flexural wavelength (typically several hundred kilometres) are well-approximated by local Airy isostasy. Features narrower than the flexural wavelength — single seamounts, submarine ridges, individual mountain ranges — are supported regionally and cannot be analysed with the local-compensation formulas alone.

```{admonition} Key concept — three dimensionless numbers govern compensation style
:class: important

The transition between local and regional compensation is set by three numbers:

- The *width of the load* relative to the flexural parameter $\alpha = (4D / \Delta\rho g)^{1/4}$, which scales with the elastic thickness $T_{e}$ of the lithosphere.
- The *time since loading* relative to the relaxation time of the asthenosphere, $\tau \sim 4\pi\eta / (\rho g L)$.
- The *temperature* of the lithosphere, which controls whether deformation is elastic, viscoelastic, or fully viscous on the relevant timescale.

A continental craton has $T_{e} \approx 80$ km and supports loads regionally; an oceanic spreading centre has $T_{e}$ near zero and behaves locally.

```

---

## 3. Mathematical Framework

```{admonition} Notation used throughout this lecture
:class: note

| Symbol | Meaning | Units |
|---|---|---|
| $h$ | Topographic elevation above sea level | m or km |
| $r$ | Crustal-root thickness (Airy model) | m or km |
| $\rho_{c}$ | Crustal density | kg m⁻³ |
| $\rho_{m}$ | Mantle density | kg m⁻³ |
| $\rho_{w}$ | Water density (oceans) | kg m⁻³ |
| $H_{\text{ref}}$ | Reference crustal thickness | m |
| $g$ | Gravitational acceleration | m s⁻² |
| $\eta$ | Mantle viscosity | Pa s |
| $\tau$ | Relaxation time for post-glacial rebound | s or ka |
| $E$ | Young's modulus | Pa |
| $\nu$ | Poisson's ratio | dimensionless |
| $T_{e}$ | Effective elastic thickness of the lithosphere | m or km |
| $D$ | Flexural rigidity, $E T_{e}^{3} / [12(1-\nu^{2})]$ | N m |
| $\alpha$ | Flexural parameter, $(4D/\Delta\rho g)^{1/4}$ | m |
| $w(x)$ | Vertical deflection of the lithosphere | m |

```

### 3.1 The Airy root formula

For an Airy-compensated mountain of height $h$, supported by a root of thickness $r$ of density $\rho_{c}$ in a mantle of density $\rho_{m}$, the equal-pressure condition gives

```{math}
:label: eq-airy
\rho_{c} \, h \;=\; (\rho_{m} - \rho_{c}) \, r,
```

so the root is

```{math}
:label: eq-airy-root
r = \frac{\rho_{c}}{\rho_{m} - \rho_{c}} \, h.
```

For $\rho_{c} = 2700$ kg m⁻³ and $\rho_{m} = 3300$ kg m⁻³, the ratio is $r/h = 4.5$ — a 1-km mountain is supported by a 4.5-km root. The Tibetan Plateau, with $h \approx 5$ km and a measured Moho at $\sim 70$ km depth (relative to $\sim 35$ km reference), is approximately Airy-compensated.

### 3.2 The Pratt density formula

In the Pratt model, the pressure at the compensation depth is the same for all columns. For a reference column of density $\rho_{c}$ and depth $H_{\text{ref}}$, and a column of height $h$ extending from elevation $h$ down to the same compensation depth at $-H_{\text{ref}}$, the pressure-equality condition gives

```{math}
:label: eq-pratt
\rho_{c} \, H_{\text{ref}} \;=\; \rho_{\text{block}} \, (H_{\text{ref}} + h),
```

so

```{math}
:label: eq-pratt-density
\rho_{\text{block}} = \rho_{c} \, \frac{H_{\text{ref}}}{H_{\text{ref}} + h}.
```

For $H_{\text{ref}} = 35$ km and $h = 5$ km, the column density is $\rho_{c} \cdot 35/40 = 2362$ kg m⁻³ — about 12% lower than the reference. The mid-ocean-ridge system, where high topography sits on hot, low-density columns, is approximately Pratt-compensated.

### 3.3 The isostatic-residual anomaly

A surveyed Bouguer anomaly that *exactly* matches the prediction of one of the compensation models is, by definition, "fully compensated" at the model's chosen scale. The *isostatic-residual* anomaly is the Bouguer anomaly minus the predicted compensation effect:

```{math}
:label: eq-iso-residual
\Delta g_{\text{iso}} = \Delta g_{\text{Bouguer}} - \Delta g_{\text{compensation prediction}}.
```

A positive isostatic residual indicates an *uncompensated* excess mass — a load that the lithosphere is supporting elastically rather than buoyantly, or a recently emplaced load that has not yet equilibrated. A negative residual indicates uncompensated mass deficit. Over geological timescales, residuals must remain bounded; transient residuals are diagnostic of active geodynamic processes.

### 3.4 Post-glacial rebound — the time-domain inverse problem

When an ice sheet thousands of metres thick is removed from the lithosphere, the surface that had been depressed by Airy compensation rises back toward equilibrium. The rate of rise is set by *mantle viscosity*: the higher the viscosity, the slower the rebound. The characteristic relaxation time for a load of horizontal scale $L$ in a half-space of viscosity $\eta$ and density $\rho_{m}$ is

```{math}
:label: eq-relaxation
\tau \;\sim\; \frac{4 \pi \eta}{\rho_{m} \, g \, L}.
```

For Fennoscandia ($L \sim 1000$ km), with $\eta \approx 10^{21}$ Pa s, this gives $\tau \approx 4$–5 ka — long enough that ongoing uplift today, ten thousand years after deglaciation, is still measurable at $\sim 9$ mm per year over the dome.

```{figure} ../assets/figures/fig_postglacial_rebound.png
:name: fig-postglacial-rebound
:alt: Three-panel figure illustrating glacial isostatic adjustment. Panel a is a cartoon cross-section showing an ice sheet on top of a depressed lithosphere, with mantle flow arrows indicating asthenosphere flowing outward beneath the ice and inward to fill the depression. Panel b plots three exponential rebound curves of remaining depression versus time since deglaciation in thousands of years, for low, Earth-like, and high mantle viscosity; the low-viscosity case decays to zero in about 10 ka, the Earth-like case in about 15 ka, and the high-viscosity case still has 50 m of remaining depression at 25 ka. Panel c is a contour map of synthetic present-day uplift rates over a formerly-glaciated region, showing two peaks of about 9 and 6 mm per year separated by about 750 km, with smooth concentric contours.
:width: 100%

Glacial isostatic adjustment. (a) An ice load depresses the lithosphere; mantle material flows laterally to balance the load. (b) After deglaciation, the rebound is exponential with timescale set by mantle viscosity. (c) Present-day uplift rates over a glaciated region trace the unrecovered depression; the spatial pattern constrains the *radial* viscosity structure of the mantle, while the rate at the centre constrains the integrated *amount* of viscosity along the flow path.
```

The inverse logic of post-glacial rebound is a reproducible classroom example. The *measured* present-day uplift rate at any location is the time derivative of the unrecovered displacement; the *amplitude* of the original depression follows from the local Airy-equivalent root for the original ice load. Inverting time-history data for $\eta(z)$ — the depth profile of mantle viscosity — has been an active research programme since the 1970s. The Whitehouse (2018) review listed in §8 is the canonical recent open-access entry point.

### 3.5 Flexural rigidity and the thin-plate equation

When the lithosphere has finite elastic strength, vertical load $q(x)$ produces deflection $w(x)$ governed by the thin-plate equation

```{math}
:label: eq-thin-plate
D \, \frac{d^{4} w}{d x^{4}} \;+\; (\rho_{m} - \rho_{w}) \, g \, w \;=\; q(x),
```

where the flexural rigidity is

```{math}
:label: eq-rigidity
D \;=\; \frac{E \, T_{e}^{\,3}}{12 \, (1 - \nu^{2})}.
```

For an isolated line load $V_{0}$ (force per unit length) at $x = 0$, the deflection is

```{math}
:label: eq-flexure-line
w(x) \;=\; \frac{V_{0} \, \alpha^{3}}{8 \, D} \; e^{-|x|/\alpha} \; \bigl( \cos|x|/\alpha + \sin|x|/\alpha \bigr),
```

where the *flexural parameter* is

```{math}
:label: eq-alpha
\alpha = \left( \frac{4 \, D}{(\rho_{m} - \rho_{w}) \, g} \right)^{\!1/4}.
```

The flexural parameter sets two scales in the deflection profile: the wavelength of the forebulge (peaks at $x \approx \pi \alpha$) and the rate of decay of the deflection. Increasing $T_{e}$ increases $D$ as the cube, increases $\alpha$ as the cube root of $D$, and so widens *and* flattens the deflection. {numref}`fig-flexure` illustrates the full picture.

```{figure} ../assets/figures/fig_flexural_bulge.png
:name: fig-flexure
:alt: Three-panel figure on lithospheric flexure. Panel a is a cartoon cross-section of an elastic plate flexing under a topographic load, with the plate dipping under the load and curving back up to form a shallow forebulge to the right of the load before returning to zero deflection. Panel b plots the deflection profile w(x) for an elastic thickness Te of 25 km, showing a pronounced central depression of about 950 m, two zero-crossings, and small forebulges of about 25 m peak amplitude at distances of plus and minus alpha equals 220 km from the load. Panel c overlays four deflection profiles for elastic thicknesses 10, 25, 50, and 80 km, illustrating that increasing Te both widens the deflection (flexural parameter alpha grows from 130 to 360 km) and reduces the central amplitude.
:width: 100%

Lithospheric flexure under a line load. The forebulge is the diagnostic feature: its position, width, and amplitude all encode the elastic thickness $T_{e}$ of the underlying lithosphere. Inverting an observed flexural profile for $T_{e}$ is a classic geophysical inverse problem; published values range from $T_{e} < 5$ km at oceanic spreading centres to $T_{e} > 80$ km in stable cratons.
```

---

## 4. The Forward Problem

The forward problem in isostasy is to predict the surface gravity (and the surface elevation, where they are independent) given a model of the subsurface. Two cases bracket what comes up in practice.

For *local compensation* (Airy or Pratt), the prediction is one-dimensional in the column. Given $h(x)$ everywhere, equation {eq}`eq-airy-root` gives $r(x)$; the gravity contribution at any surface point is then the integral of the resulting density model. Because $h$ and $r$ are linked, the Bouguer anomaly produced by an Airy-compensated topography is *long-wavelength and negative* — the deep, low-density root dominates because gravity falls off slowly with depth.

For *regional compensation* (flexure), the deflection $w(x)$ is solved from equation {eq}`eq-thin-plate` for a given load distribution $q(x)$, and the resulting $w(x)$ is converted into a Bouguer anomaly via the $2\pi G \Delta\rho$ Bouguer-slab relation in Lecture 19. Forward calculations of regional compensation are the staple of marine-trench studies (e.g. forearc bulge across Cascadia) and continental-loading studies (Tibetan Plateau, Andes).

The companion notebook *flexure_demo.ipynb* solves equation {eq}`eq-thin-plate` for user-specified load distributions and elastic thicknesses, and overlays the predicted Bouguer anomaly on synthetic data.

---

## 5. The Inverse Problem

The most useful inverse problem in this lecture is *recover $T_{e}$ from observed flexural geometry*. Given a measured profile of bathymetry or topography across a load (a seamount, a trench, a sedimentary basin), the inverse problem is to find the elastic thickness that best reproduces the observed flexural wavelength.

Three observations carry the bulk of the information.

- The *position* of the forebulge, located at $x = \pi \alpha$ from the load. Measuring this distance gives $\alpha$ directly and therefore $D$ and $T_{e}$.
- The *amplitude* of the forebulge, which encodes the load magnitude $V_{0}$ given $D$.
- The *decay length* of the deflection beyond the forebulge, which provides an independent estimate of $\alpha$.

Inversions for $T_{e}$ are rarely perfect. The lithosphere does not have a single, sharply-defined elastic thickness; the apparent $T_{e}$ depends on the loading history, the temperature structure, and the assumed rheology. A useful rule of thumb is that the inverted $T_{e}$ is the *minimum* elastic thickness consistent with the data — increasing $T_{e}$ in the model can usually be compensated by increasing the load magnitude.

Post-glacial rebound provides the *time-domain* analogue. Given a uplift-rate map and the known history of ice loading, the inverse problem is to recover the depth profile of mantle viscosity $\eta(z)$. The Whitehouse (2018) review surveys current open-access workflows.

---

## 6. Worked Example — Compensating Mount Olympus

The Olympic Mountains in western Washington reach $\sim 2.4$ km elevation. Treat the range as locally Airy-compensated by a deep root of standard crust ($\rho_{c} = 2700$ kg m⁻³) into a mantle of $\rho_{m} = 3300$ kg m⁻³.

**(a) Predicted root thickness.**

$$
r = \frac{\rho_{c}}{\rho_{m} - \rho_{c}} \, h = \frac{2700}{600} \times 2400\,\text{m} = 10\,800\,\text{m}.
$$

The Olympics are predicted to have a $\sim 11$-km root.

**(b) Predicted Bouguer anomaly.**

The negative Bouguer anomaly produced by the root is, to first order, the Bouguer-slab signal of the root:

$$
\Delta g_{\text{root}} \approx -\,2 \pi G \, (\rho_{m} - \rho_{c}) \, r \;\approx\; -\,2 \pi \cdot 6.674 \!\times\! 10^{-11} \cdot 600 \cdot 10\,800 \;\approx\; -\,272\,\text{mGal}.
$$

Converting from m s⁻² to mGal — multiplying by $10^{5}$ — gives a predicted Bouguer-anomaly amplitude of $\approx -272$ mGal at the centre of the range. The free-air anomaly should remain small ($< 50$ mGal), because the root and topography roughly cancel at the surface. Both predictions are broadly consistent with measurements from the USGS regional gravity grid.

**(c) What if the Olympics are not in local equilibrium?**

The Olympic Peninsula sits on the Cascadia accretionary prism, where active subduction continually loads and uplifts the wedge. The *isostatic residual* anomaly across the Olympics — the Bouguer anomaly with the predicted Airy-compensation prediction subtracted — therefore departs from zero, and that departure is itself the signal of an uncompensated load. Reading the residual is the third step in the worked example, and is the bridge from the static Airy framework of this lecture to the dynamic geodynamics of the synthesis module.

```{admonition} Concept check
:class: tip

1. Two mountain ranges of identical surface elevation produce Bouguer anomalies of $-100$ mGal and $-200$ mGal respectively. Which range is more nearly locally compensated, and how does the difference suggest the role of lithospheric strength?
2. A continental margin shows a forebulge $250$ km offshore of the toe of a deltaic load. Estimate the flexural parameter $\alpha$ and, given $\rho_{m} - \rho_{w} = 2270$ kg m⁻³, the elastic thickness $T_{e}$. (Use $E = 70$ GPa and $\nu = 0.25$.)
3. Fennoscandian uplift rates at the dome centre are $\sim 9$ mm yr⁻¹. The total post-glacial uplift since deglaciation has been about $300$ m. Estimate the relaxation time $\tau$ and confirm whether the implied mantle viscosity is in the canonical range $10^{20}$–$10^{21}$ Pa s.
```

---

## 7. Course Connections

- **Backward** to Lecture 19, whose Bouguer-anomaly construction is the input to the isostatic-residual calculation in §3.3.
- **Backward** to Lecture 20, where regional anomalies were noted as long-wavelength features to be subtracted before residual interpretation. The present lecture identifies *what* the regional represents physically.
- **Forward** to Lecture 22 (*Density and Lithospheric Structure*), where the rheological structure of the lithosphere is taken up in detail and the elastic, viscoelastic, and viscous behaviours invoked here are derived from microphysical constitutive laws.
- **Forward** to Module 7 (*Geodynamics & Tectonics*), where dynamic topography — vertical motions driven by mantle convection rather than buoyancy — is introduced as a third compensation mechanism complementing isostasy and flexure.
- **Cross-link** to climate change (Discussion Session 5): present-day GIA in formerly-glaciated regions is a key correction to GPS-measured vertical land motion, which in turn feeds tide-gauge sea-level reconstructions.

---

## 8. Research Horizon

**Glacial isostatic adjustment in the satellite age.** Whitehouse (2018), *Earth Surface Dynamics* 6, 401–429, <https://doi.org/10.5194/esurf-6-401-2018> (CC BY 4.0), reviews the state of GIA modelling and identifies the key open problems: the depth profile of mantle viscosity, the mechanical coupling between the lithosphere and the asthenosphere, and the inversion of GRACE-FO gravity time series for present-day GIA versus contemporary ice-sheet mass loss.

**Dynamic topography and the residual challenge.** Forte & Rowley (2022), *Earth and Planetary Science Letters*, demonstrate that a substantial fraction of the long-wavelength geoid and the Bouguer anomaly has been mistakenly attributed to local isostasy when it is, in fact, *dynamic topography* — vertical surface motion driven by mantle convection. The implication is that classical Airy interpretations of long-wavelength features systematically overestimate the depth of the compensating roots. The author manuscript is open access via the journal preprint server.

**Antarctic and Greenland ice-sheet response and 21st-century sea level.** A rapidly evolving literature, exemplified by papers in *The Cryosphere* (open-access EGU journal), demonstrates that the present-day ice-sheet mass loss measured by GRACE-FO requires a careful disentangling from underlying GIA. This disentangling is one of the largest sources of uncertainty in projecting 21st-century sea-level rise — an issue that returns directly to the climate framing of Discussion Session 9.

---

## 9. Societal Relevance — Cascadia Subsidence and the Tide-Gauge Record

Tide-gauge records along the Pacific Northwest coast appear to show, at first glance, a much slower local sea-level rise than the global mean. The discrepancy is *not* primarily a measurement error and *not* primarily a regional climate anomaly: it is a tectonic signal. The Cascadia subduction zone is locked in the inter-seismic period, accumulating elastic strain that *uplifts* the coastal forearc by several millimetres per year. Subtracting the inter-seismic uplift from the tide-gauge record recovers the true sea-level signal.

Inter-seismic uplift is, in the language of this lecture, a transient elastic response — closely analogous to the flexural deflection of equation {eq}`eq-flexure-line`, but driven by fault-locking rather than a static load. In the next great subduction-zone earthquake, the strain will be released abruptly, dropping coastal Washington by 0.5–2 m within minutes — a co-seismic event that resets the tide-gauge baseline and, regionally, redefines "sea level".

The USGS open-access resource *Cascadia Subduction Zone* (<https://www.usgs.gov/programs/earthquake-hazards/science/cascadia-subduction-zone>) is the standard public-domain entry point. The resource explicitly connects vertical land motion to long-term seismic hazard — a connection whose physical mechanism is exactly the elastic-deformation reasoning of this lecture.

---

## AI Literacy — Prompt Lab

Three prompts that connect this lecture to broader scientific reasoning, with evaluation criteria for the responses.

**Prompt 1.** *"Compare Airy and Pratt isostasy by predicting the gravity anomaly each model would produce for the Tibetan Plateau. Which model better fits observations, and why?"*

A useful response derives equations {eq}`eq-airy-root` and {eq}`eq-pratt-density`, computes the predicted Bouguer anomaly amplitudes, and notes that observations broadly favour Airy but cannot exclude a Pratt-like contribution from the high-temperature crust beneath the plateau. Mediocre responses describe the two models qualitatively without computing predicted amplitudes. Misleading responses confidently assert that one model is "right" without acknowledging the empirical mixture observed in nature.

**Prompt 2.** *"Estimate the mantle viscosity from the present-day Fennoscandian uplift rate of 9 mm/yr and the known total post-glacial uplift of about 300 m."*

A useful response identifies the relaxation timescale from the ratio of these two numbers ($\tau \approx 33$ ka), connects $\tau$ to the relaxation formula in equation {eq}`eq-relaxation`, and recovers $\eta \approx 10^{21}$ Pa s — within the canonical range. Common errors: confusing the rebound *amplitude* with the *load* amplitude; using the formula as a single-step "plug and chug" without understanding the underlying Maxwell-time logic.

**Prompt 3.** *"Why do oceanic seamounts produce flexural forebulges while individual mountain peaks in continental settings often do not?"*

A useful response invokes the difference in lithospheric elastic thickness — oceanic lithosphere is thinner ($T_{e} \sim 10$–$20$ km) and bends regionally; continental lithosphere can have $T_{e} \gg 50$ km and supports loads more locally — *and* notes that single peaks in mountain ranges are typically components of a larger compensating structure that masks the individual flexure. A response that ignores either side of this dichotomy is incomplete.

The Discussion Session 5 design uses Prompts 1 and 2 as opening exercises; students design their own answer first, then compare with a generated response, then critique the AI's transparency about its assumptions. This is the *AI Epistemics* template applied at the small-group level.

---

## Further Reading

- Lowrie, W. & Fichtner, A. (2020). *Fundamentals of Geophysics*, 3rd ed., Cambridge University Press, Ch. 3.6. (Free e-book via UW Libraries.)
- Turcotte, D. L. & Schubert, G. (2014). *Geodynamics*, 3rd ed., Cambridge University Press, Ch. 3 (cited only — paywalled).
- Whitehouse, P. L. (2018). Glacial isostatic adjustment modelling: historical perspectives, recent advances, and future directions. *Earth Surface Dynamics* 6, 401–429. <https://doi.org/10.5194/esurf-6-401-2018> (CC BY 4.0).
- Caron, L. *et al.* (2018). GIA model statistics for GRACE hydrology, cryosphere, and ocean science. *Geophysical Research Letters* 45, 2203–2212. <https://doi.org/10.1002/2017GL076644> (open access).
- IPCC (2021). *AR6 Working Group I Report*, Chapter 9 (sea-level change), <https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-9/> (open access).
- Forte, A. M. & Rowley, D. B. (2022). Earth's isostatic and dynamic topography. *Earth Planet. Sci. Lett.* (open-access author manuscript).
- Watts, A. B. & Burov, E. B. (2003). Lithospheric strength and its relationship to the elastic and seismogenic layer thickness. *Earth Planet. Sci. Lett.* 213, 113–131. <https://doi.org/10.1016/S0012-821X(03)00289-9> (cited only — paywalled).
- USGS Cascadia Subduction Zone resource (public domain): <https://www.usgs.gov/programs/earthquake-hazards/science/cascadia-subduction-zone>.
