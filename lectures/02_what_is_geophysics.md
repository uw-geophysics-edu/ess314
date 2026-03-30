---
title: "The Inaccessible Earth: Scales, Instruments, and the Logic of Geophysical Inference"
week: 1
lecture: 2
date: "2026-04-01"
topic: "Spatial and temporal scales of Earth processes; five geophysical instruments; the forward/inverse problem structure; three pillars of scientific method"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-B", "LO-OUT-C", "LO-OUT-D"]
open_sources:
  - "Lowrie & Fichtner (2020), Ch. 1–2 — free via UW Libraries"
  - "MIT OCW 12.201 Essentials of Geophysics §1 — ocw.mit.edu"
  - "IRIS/EarthScope — iris.edu"
  - "CASIE21 Cascadia Seismic Imaging — casie21.weebly.com"
---

# Lecture 2 — The Inaccessible Earth: Scales, Instruments, and the Logic of Geophysical Inference

:::{seealso}
📊 **Lecture slides** — [open in new tab](https://uw-geophysics-edu.github.io/ess314/slides/lecture_02_slides.html)
:::

## Syllabus Alignment

| | |
|---|---|
| **Course LOs addressed** | LO-1 (observables from Earth properties), LO-2 (apply models to predict observations), LO-3 (formulate inference problems), LO-4 (evaluate methods and limitations) |
| **Learning outcomes practiced** | LO-OUT-A (sketch geometry and predict qualitative effect), LO-OUT-B (compute depth fractions, spreading rate), LO-OUT-C (explain why indirect measurement is necessary), LO-OUT-D (set up a simple inference problem with data, model, and forward relation) |
| **Lowrie & Fichtner** | Ch. 1 §1.1–1.4; Ch. 2 §2.1 *(free via UW Libraries)* |
| **Lab connection** | Lab 1 (Friday): download and plot a PNSN seismogram; identify P and S arrivals; compute source distance from the S–P time difference |
| **Next lecture** | Lecture 4 (Thursday): Seismic waves — fundamentals |

---

## Learning Objectives

By the end of this lecture, students will be able to:

- **[LO-2.1]** Calculate the fraction of Earth's interior accessible to direct sampling and explain why this makes geophysical inference the only available approach to studying the deep Earth.
- **[LO-1.3]** Place six geophysical processes on a log-log space–time scale diagram and explain why no single instrument or method spans the full range.
- **[LO-4.2]** Describe what each of the five major geophysical instruments records physically, and identify at least one limitation or ambiguity intrinsic to each measurement type.
- **[LO-3.1]** Formulate the forward problem for two different geophysical methods by specifying model parameters, observables, and the physical operator connecting them, and explain why the corresponding inverse problem is non-unique.

## Prerequisites

Lecture 1 (motivations, physics domains, passive vs. active surveys). Basic algebra and dimensional analysis.

---

## 1. The Geoscientific Question: Quantifying Inaccessibility

Lecture 1 established the defining constraint of geophysics: Earth's interior is permanently inaccessible to direct sampling. This lecture places precise numbers on that inaccessibility and then addresses what can be measured and how physical reasoning connects those measurements to knowledge of the interior.

The Kola Superdeep Borehole, drilled in Russia from 1970 to 1989, reached 12.262 km — a depth record that has not been surpassed. Drilling was halted not by technological limits but by temperature: at depth, the rock exceeded 180°C, causing the material to behave plastically rather than as a brittle solid and rendering drill bits unusable. Earth's mean radius is 6,371 km. The accessible fraction is:

$$f = \frac{z_\text{max}}{R_\oplus} = \frac{12.262}{6{,}371} = 0.0019 = 0.19\%$$

Less than two-tenths of one percent. The Mponeng gold mine in South Africa — the deepest working mine — reaches approximately 4 km (0.06% of Earth's radius). A typical crustal seismic refraction survey images to roughly 50 km (0.8%). Every layer boundary in the standard reference Earth model — the Moho at approximately 35 km, the 410 and 660 km mantle transition zones, the core–mantle boundary at 2,900 km, the inner-core boundary at 5,150 km — was identified from seismic wave observations, not from samples.

### 1.1 Eratosthenes and the Scale of the Problem

Before the inaccessibility of Earth's interior could be quantified, its size had to be known. Around 230 BCE, Eratosthenes of Cyrene determined Earth's circumference from two shadow observations and a known distance. On the summer solstice at noon in Syene (modern Aswan, Egypt), sunlight reached the bottom of a well, indicating the Sun was directly overhead. On the same date and time in Alexandria, approximately 800 km north, a vertical rod cast a shadow at 7.2° from vertical. Assuming the Sun's rays are effectively parallel (justified by the Sun's great distance) and Earth is spherical, the angle 7.2° subtends the arc between the two cities:

$$\frac{\theta}{360°} = \frac{d}{C_\oplus} \quad \Rightarrow \quad C_\oplus = \frac{360°}{7.2°} \times 800 \text{ km} = 40{,}000 \text{ km}$$

$$R_\oplus = \frac{C_\oplus}{2\pi} \approx 6{,}366 \text{ km}$$

The modern value is 6,371 km; the discrepancy is less than 0.1%. The result rests on assumptions: that the Sun's rays are parallel, that Earth is spherical, that the two cities share the same meridian, and that the inter-city distance is known accurately. Each assumption represents a model choice embedded in what appears to be a simple geometric measurement — a pattern that pervades all geophysical inference.

:::{admonition} Key Equation
:class: important
**Eratosthenes' determination of Earth's radius:**

$$R_\oplus = \frac{d}{\theta}$$

where $d$ is the surface distance between two points and $\theta$ is the angle between their local vertical directions, expressed in radians.

| Symbol | Quantity | Value |
|--------|----------|-------|
| $R_\oplus$ | Earth's mean radius | 6,371 km |
| $d$ | Distance between Syene and Alexandria | ~800 km |
| $\theta$ | Shadow angle at Alexandria | 7.2° = 0.1257 rad |

Dimensional check: $[R_\oplus] = \text{km} / \text{rad} = \text{km}$ ✓ (radians are dimensionless).
:::

:::{figure} ../assets/figures/fig_inaccessible_earth.png
:name: fig-inaccessible-earth
:alt: Two-panel depth diagram. Left panel shows a vertical axis from 0 to 6371 km depth with color-coded bands for each Earth layer: crust (sky blue, 0-70 km), upper mantle (green, 70-660 km), lower mantle (orange, 660-2900 km), outer core (vermilion, 2900-5150 km), inner core (pink, 5150-6371 km). A small dark shaded band near the top represents human-accessible depths, barely visible at this scale. Right panel shows a zoomed view of the top 80 km with three labeled horizontal lines indicating the Mponeng Mine at 4 km, the Kola Superdeep Borehole at 12.2 km, and a typical seismic refraction survey depth at 50 km. A secondary axis on the right shows each depth as a percentage of Earth's radius.
:width: 90%
**Figure 2.1.** The inaccessible Earth, to scale. At the scale of the full Earth (left), human-accessible depths are too thin to see. The zoomed crustal view (right) shows that the Kola Superdeep Borehole, which took 19 years to drill, barely penetrates the middle crust. All knowledge of the mantle, outer core, and inner core derives from geophysical inference. [Python-generated. Script: `assets/scripts/fig_inaccessible_earth.py`]
:::

---

## 2. Governing Physics: The Space–Time Scale Diagram

The most important organizing principle for understanding geophysical methods is that **scale determines method**. Every Earth process occupies a characteristic range of spatial and temporal scales; no single instrument or technique spans the full range; and the appropriate physical description, mathematical framework, and measurement strategy all depend on which scale regime is relevant.

The range across geophysical problems is extreme: from the milliseconds and centimeters of an acoustic pulse in a borehole to the billions of years and thousands of kilometers of mantle convection — fifteen orders of magnitude in time and ten in space. No instrument bridges this range, and no equation works in the same form across all of it.

:::{figure} ../assets/figures/fig_space_time_scales.png
:name: fig-space-time-scales
:alt: Log-log scatter plot with spatial scale in kilometers on the x-axis ranging from 0.001 to 10,000 km, and temporal scale in seconds on the y-axis ranging from 0.001 seconds to 10 to the 17th seconds. Points representing geophysical processes are color-coded and marked by shape: blue triangles for geodynamics processes including mantle convection, subduction dynamics, seismic tomography, glacial rebound, and volcanic arc evolution; orange circles for hazards processes including the Cascadia earthquake cycle, aftershock sequences, local earthquakes, and seismic P-waves; green squares for resources and engineering including active seismic surveys, reflection surveys, gravity surveys, and groundwater depletion; and a pink diamond for slow-slip events. A secondary y-axis on the right shows human-readable timescales from milliseconds to 100 million years.
:width: 90%
**Figure 2.2.** Spatial and temporal scales of geophysical processes. Color indicates the motivating context from Lecture 1 (geodynamics: blue; hazards: orange; resources/engineering: green; multi-context: pink). No single method spans the full range plotted here. [Python-generated. Script: `assets/scripts/fig_space_time_scales.py`]
:::

Three structural observations from this diagram are foundational to the rest of the course:

**The same material admits different physical descriptions at different scales.** The mantle behaves as a rigid elastic solid on timescales of seismic wave propagation (seconds), allowing elastic waves to traverse the entire planet without permanent deformation. On timescales of mantle convection (millions of years), the same rock flows as a very viscous fluid. Which physical description is appropriate depends entirely on the ratio of the observation timescale to the material's relaxation time — a concept made precise in the study of viscoelasticity (Week 9).

**Scale dictates resolution.** A seismometer that captures seismic arrivals in seconds cannot directly sense million-year mantle flow. A gravimeter that maps density at continental scales cannot resolve a 10-cm void in a concrete foundation. The scale diagram provides the first-order criterion for deciding whether a proposed method can even in principle resolve the target of interest.

**The inverse problem becomes harder as the scale gap increases.** The farther the observable is from the process of interest in space or time, the more physical assumptions are required to connect them, and the more non-unique the inference becomes. This relationship between observational distance and non-uniqueness is discussed formally in Section 5.

---

## 3. Mathematical Framework: What Instruments Actually Record

Every physical field must be transduced into an electrical signal — a voltage, a frequency, a phase — by an instrument. Understanding what instruments actually record, and what they do not, is prerequisite to interpreting any geophysical dataset.

### 3.1 The Seismometer

A seismometer converts ground motion into an electrical signal by exploiting the inertia of a suspended mass: when the ground moves, the mass tends to remain stationary, and the relative displacement is measured inductively or capacitively. Modern broadband seismometers respond over seven orders of magnitude in frequency — from below 0.003 Hz (Earth's free oscillations excited by great earthquakes, periods of ~300 s) to above 50 Hz (local microseismicity and active-source surveys). The output is ground velocity (or displacement or acceleration, depending on instrument design) as a function of time.

A seismogram entangles contributions from three physically distinct sources:

1. **The source** — the earthquake's rupture history, spatial extent, and radiation pattern
2. **The propagation path** — modifications imposed by Earth's heterogeneous velocity structure
3. **The site** — amplification or attenuation by local geology beneath the instrument

Separating these contributions is one of the central problems of observational seismology and is, in formal terms, an inverse problem.

### 3.2 The Gravimeter

A gravimeter measures local gravitational acceleration $g$ to a precision of approximately 1 microgal (1 μGal = 10⁻⁸ m/s²), one part per billion of Earth's mean surface gravity. The measurement principle involves a known mass suspended from a spring; variation in $g$ changes the spring extension, which is measured by laser interferometry or capacitance sensing.

Variations in $g$ across space reflect lateral density contrasts in the subsurface. The GRACE-FO satellite mission measures monthly changes in Earth's gravity field globally, detecting Greenland ice sheet mass loss (~270 Gt/yr), aquifer depletion in the Central Valley of California, and postseismic viscoelastic relaxation following great earthquakes. The formal connection between measured $g$ and subsurface density is established by Poisson's equation $\nabla^2\Phi = 4\pi G\rho$ (Week 7).

### 3.3 The Magnetometer

A magnetometer measures the local magnetic field vector **B** with precision of a few nanotesla against Earth's background field of ~50,000 nT. Proton precession magnetometers exploit the Larmor precession frequency of hydrogen nuclei, which is proportional to field strength; fluxgate magnetometers measure field components through the saturation of a permeable ferromagnetic core.

Crustal rocks carry remanent magnetization — a frozen record of the ambient field polarity at the time of solidification. Magnetic anomalies relative to a smooth reference model reveal the magnetization of subsurface rocks, which depends on mineralogy (iron-bearing minerals vs. silicates), temperature (rocks above the Curie temperature carry no remanence), and magnetic history. The seafloor magnetic lineations used to reconstruct plate motion rates are measured by ship-towed magnetometers.

### 3.4 GPS and InSAR

GPS (Global Navigation Satellite System) geodesy measures the position of a ground antenna to millimeter accuracy by analyzing phase differences in signals received from multiple satellites. A continuous GPS station records a time series of three-dimensional position at daily to sub-hourly resolution. The signal captures interseismic strain accumulation on locked faults (1–10 mm/yr), coseismic displacement (centimeters to meters), postseismic viscoelastic relaxation (years to decades), volcanic inflation from magma intrusion, and glacial isostatic adjustment.

Interferometric Synthetic Aperture Radar (InSAR) processes pairs of satellite radar images acquired at different times to map surface displacement over broad areas — thousands of square kilometers — at centimeter to millimeter precision. GPS provides continuous time series at individual points; InSAR provides spatially dense snapshots over extended regions.

### 3.5 Heat Flow Probes

A heat flow probe measures the temperature gradient in a borehole or seafloor sediment column using thermistors at known depth spacing. Combined with laboratory thermal conductivity measurements on core samples, the surface heat flux is:

$$q = -k \frac{dT}{dz}$$

where $k$ is thermal conductivity (W m⁻¹ K⁻¹) and $dT/dz$ is the measured temperature gradient (K/m), giving $q$ in W/m² (typically reported in mW/m²). The global heat flow compilation reveals the age-dependence of oceanic heat flow, anomalously high values over mantle plumes, and the geothermal gradient relevant to geothermal energy resource assessment (Week 9).

---

## 4. The Forward Problem

Every geophysical method shares a common logical structure that must be identified before any quantitative work begins.

**The forward problem:** Given a model of Earth properties $\mathbf{m}$, predict the observations $\mathbf{d}$ that would result.

$$\mathbf{d} = \mathbf{G}(\mathbf{m}) \label{eq:forward}$$

where $\mathbf{d}$ is the vector of observations (travel times, gravity values, magnetic field measurements), $\mathbf{m}$ is the vector of model parameters (density, elastic moduli, conductivity at every point in the Earth), and $\mathbf{G}$ is the physical operator — derived from one of the five governing equations in Lecture 1 — that connects model to data.

Solving the forward problem is generally straightforward: given a density distribution, integrate Poisson's equation to predict the surface gravity field; given a velocity structure, trace rays and compute travel times. The forward problem is well-posed in the sense that a unique answer exists for any given model.

**Model parameters and predicted observables — two examples:**

*Gravity forward problem:*
- Model parameters: density $\rho(\mathbf{r})$ at every point in the subsurface
- Observables predicted: gravitational acceleration $g(x,y)$ at surface stations
- Operator: $g = -\partial\Phi/\partial z$ where $\nabla^2\Phi = 4\pi G\rho$

*Seismic travel-time forward problem:*
- Model parameters: P-wave velocity $\alpha(\mathbf{r})$ at every point
- Observables predicted: P-wave arrival times $t_P$ at seismometers
- Operator: ray-tracing integral $t = \int \frac{ds}{\alpha}$ along the minimum-time path

---

## 5. The Inverse Problem

The inverse problem is the actual scientific goal: given observations $\mathbf{d}$, estimate the Earth model $\mathbf{m}$ that produced them.

The inverse problem is almost always **non-unique**: many different Earth models can reproduce any given dataset within measurement uncertainty. This is not a failure of the method — it is a fundamental mathematical property of the underlying physics.

:::{admonition} Inverse Problem Setup
:class: tip
**Gravity inversion:**
- **Data ($\mathbf{d}$):** Gravitational acceleration $g$ measured at a grid of surface points (mGal)
- **Model ($\mathbf{m}$):** Density distribution $\rho(\mathbf{r})$ in the subsurface (kg/m³)
- **Forward relation:** $g = \mathbf{G}(\rho)$ where $\mathbf{G}$ integrates Newton's law over $\rho$
- **Key non-uniqueness:** An infinite family of density distributions produces identical surface gravity — deeper, denser bodies cannot be distinguished from shallower, less-dense bodies without additional constraints
- **Resolution limit:** Lateral resolution improves with station density; depth resolution requires borehole constraints or auxiliary data types

**Seismic travel-time tomography:**
- **Data ($\mathbf{d}$):** P-wave arrival times $t_P$ at seismic stations from many earthquakes (seconds)
- **Model ($\mathbf{m}$):** P-wave velocity $\alpha(\mathbf{r})$ at every point in the subsurface (km/s)
- **Forward relation:** $t_P = \int ds/\alpha$ along the minimum-time ray path
- **Key non-uniqueness:** Limited earthquake and station distribution leaves large Earth volumes unsampled; velocity anomalies may be smeared along ray paths
- **Resolution limit:** Wavelength of seismic waves at dominant frequency; ray coverage geometry
:::

:::{admonition} Key Concept
:class: important
The forward problem — predicting data from a model — is well-posed and generally straightforward to solve. The inverse problem — inferring a model from data — is almost always non-unique. Non-uniqueness is not a methodological limitation to be eliminated; it is a statement about what the data actually constrain. Additional physical constraints, multiple independent datasets, or explicit regularization are always required to stabilize an inverse solution. Characterizing and communicating this non-uniqueness is a fundamental professional responsibility of the geophysicist.
:::

---

## 6. Three Pillars of Geophysical Science

Geophysics advances through the interplay of three complementary modes of inquiry. All three appear throughout this course.

**Theory and numerical simulation** — deriving governing equations analytically in tractable limiting cases and solving them computationally for realistic geometries. Open-source spectral-element codes such as SPECFEM3D ([github.com/geodynamics/specfem3d](https://github.com/geodynamics/specfem3d)) simulate seismic wave propagation in three-dimensional Earth models with millions of grid points. Mantle convection codes such as ASPECT simulate flows spanning geological timescales.

**Field observations** — deploying instruments, collecting data, and processing signals. This is the point of contact with the actual Earth. The 2021 Cascadia Seismic Imaging Experiment (CASIE21) combined passive ocean-bottom seismometers with an active marine airgun survey to image the Cascadia subduction zone at resolution required for hazard assessment. The resulting datasets are being used to constrain fault coupling models and refine ground-motion predictions.

**Laboratory experiments** — measuring physical properties of Earth materials under controlled conditions of temperature, pressure, and composition. High-pressure experiments at diamond-anvil cells reach pressures of the lower mantle and outer core; multi-anvil presses reproduce mantle conditions in centimeter-scale samples. The measured relationships between seismic velocity, temperature, and mineralogy are the links that make tomographic images interpretable in terms of real geology.

No pillar is sufficient in isolation. Theory without observational constraint is speculation. Observations without interpretive theory produce no understanding. Laboratory data without field context is unanchored. The history of geophysics is the history of these three modes becoming increasingly integrated through advances in instrumentation, computing power, and mathematical frameworks.

:::{admonition} Concept Check
:class: tip
1. A seismic reflection survey images a bright, flat reflector at 2-second two-way travel time. The inference drawn is that this reflector marks a sedimentary layer boundary. What assumptions are embedded in this inference, and what additional measurements could test at least two of them?
2. GPS stations on the Washington coast move eastward at approximately 10 mm/yr. State the forward problem that connects this observation to elastic strain accumulation on the Cascadia fault: identify the model parameters, the observable, and the physical operator.
3. A gravity survey is conducted over a known salt dome (salt has lower density than the surrounding sedimentary rock). Describe qualitatively the expected gravity anomaly over the dome. Explain, using the inverse problem structure, why the gravity anomaly alone cannot uniquely determine the dome's depth.
:::

---

## 7. Course Connections

- **Prior lecture (Lecture 1):** The three motivations and five physics domains map directly onto the five instruments described here. Each instrument makes the abstract connection between a governing equation and an Earth property concrete.
- **Thursday (Lecture 4):** The seismic wave equation — the wave phenomena entry in the Lecture 1 table — is derived from continuum mechanics. The forward problem for seismic travel times is formalized.
- **Lab 1 (Friday):** A seismogram is retrieved from PNSN through the IRIS FDSN client, plotted, and P and S arrivals are identified. The source distance is then computed from the S–P travel time difference — a direct application of the forward problem: $t_S - t_P = \Delta(1/\beta - 1/\alpha)$, solved for $\Delta$ given observed arrival times and assumed velocities.
- **Cross-topic link:** The forward/inverse problem structure introduced here is the unifying framework for every method in the course — seismic tomography, gravity inversion, magnetic anomaly interpretation, heat flow modeling.

---

## 8. Societal Relevance

:::{admonition} Why It Matters: The Cascadia Inverse Problem
:class: note

**Fault coupling as a non-unique inverse problem:** GPS stations, seismometers, and ocean-bottom pressure sensors around the Cascadia subduction zone provide the data vector $\mathbf{d}$ for an inference of fault coupling $\mathbf{m}$ — the distribution of locked vs. creeping regions on the subduction interface. Different research groups, using the same GPS data with different regularization choices and different assumptions about interseismic loading geometry, produce significantly different coupling models and therefore different predictions of expected ground shaking in a future megathrust rupture.

This is not a scientific failure. It is the honest expression of what the data constrain. The uncertainty in the coupling inverse solution propagates into probabilistic hazard calculations and ultimately into building code specifications for hospitals, schools, and bridges. Quantifying and communicating that uncertainty — rather than suppressing it in favor of a single preferred model — is what distinguishes rigorous geophysical practice from overconfident analysis.

**Further exploration:** CASIE21 experiment overview and publications at [casie21.weebly.com](https://casie21.weebly.com). IRIS/EarthScope Cascadia educational resources at [iris.edu/hq/inclass/lesson/cascadia_subduction_zone](https://www.iris.edu/hq/inclass/lesson/cascadia_subduction_zone). Real-time Pacific Northwest seismicity at [pnsn.org](https://pnsn.org).
:::

---

## AI Literacy

:::{admonition} Analytical Exercise 2.1 — Evaluating the Forward/Inverse Distinction
:class: tip
The following prompt was submitted to a general-purpose AI assistant:

*"Explain the difference between the forward problem and the inverse problem in geophysics, and explain why the inverse problem is usually non-unique."*

Evaluate a generated response against the content of this lecture:
- Is the forward problem correctly defined as: given a model, predict the data?
- Is the inverse problem correctly defined as: given data, infer the model?
- Does the response correctly identify non-uniqueness and give a physically grounded reason for it?
- Does the response propose at least one real strategy for managing non-uniqueness (regularization, multiple data types, physical constraints, Bayesian methods)?
- Does the response give a concrete geophysical example?

Identify one statement that is correct and well-supported, and one statement that is incomplete, vague, or potentially misleading. The forward/inverse structure is the conceptual core of this course; evaluating how an AI describes it provides useful calibration for future use of such tools.
:::

---

## Further Reading

- Lowrie, W. & Fichtner, A. (2020). *Fundamentals of Geophysics*, 3rd ed. Cambridge University Press. DOI: [10.1017/9781108685917](https://doi.org/10.1017/9781108685917). Ch. 1–2. *(Free via UW Libraries)*
- MIT OpenCourseWare 12.201. [ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004](https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004). CC BY NC SA.
- Lehmann, F. et al. (2024). Uncertainty quantification for full waveform inversion with neural operators. *JGR Solid Earth*, 129. DOI: [10.1029/2023JB027856](https://doi.org/10.1029/2023JB027856). *(Open access)*
- Fichtner, A. et al. (2022). Fiber-optic observations for tomography. *JGR Solid Earth*, 127. DOI: [10.1029/2022JB024690](https://doi.org/10.1029/2022JB024690). *(Open access)*
- SPECFEM3D open-source seismic wave propagation code. [github.com/geodynamics/specfem3d](https://github.com/geodynamics/specfem3d). *(Open source)*
- IRIS FDSN data services. [ds.iris.edu](https://ds.iris.edu). *(Open data)*
