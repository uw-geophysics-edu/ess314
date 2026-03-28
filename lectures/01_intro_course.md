---
title: "What Is Geophysics? Three Motivations, Five Physics Domains, and the Stakeholder Landscape"
week: 1
lecture: 1
date: "2026-03-31"
topic: "Scope of geophysics — geodynamics, natural hazards, resource management; physics domains; passive vs. active surveys"
course_lo: ["LO-1", "LO-4", "LO-6"]
learning_outcomes: ["LO-OUT-C", "LO-OUT-F", "LO-OUT-H"]
open_sources:
  - "Lowrie & Fichtner (2020), Ch. 1 — free via UW Libraries"
  - "MIT OCW 12.201 Essentials of Geophysics — ocw.mit.edu/courses/12-201"
  - "IRIS/EarthScope Teachable Moments — iris.edu"
  - "USGS Earthquake Hazards Program — earthquake.usgs.gov"
---

# Lecture 1 — What Is Geophysics? Three Motivations, Five Physics Domains, and the Stakeholder Landscape

## Syllabus Alignment

| | |
|---|---|
| **Course LOs addressed** | LO-1 (observables from Earth properties), LO-4 (evaluate methods and limits), LO-6 (communicate geophysical reasoning) |
| **Learning outcomes practiced** | LO-OUT-C (explain why a method works physically), LO-OUT-F (match method to question and scale), LO-OUT-H (critique an explanation for hidden assumptions) |
| **Lowrie & Fichtner** | Ch. 1, §1.1–1.3 (free via UW Libraries) |
| **Lab connection** | Lab 1: Introduction to Python and ObsPy — fetching a real seismogram from PNSN |
| **Next lecture** | Lecture 2: Scales, instruments, and the logic of geophysical inference |

---

## Learning Objectives

By the end of this lecture, students will be able to:

- **[LO-1.1]** State a precise definition of solid Earth geophysics and explain why indirect observation is the defining epistemological constraint of the discipline.
- **[LO-1.2]** Classify any geophysical study into one of three motivating contexts — geodynamics, natural hazards, or resource management — and identify the physical process and primary observable involved.
- **[LO-4.1]** Identify the branch of physics governing a given geophysical observable and name the Earth property that observable senses.
- **[LO-6.1]** Identify four distinct stakeholder communities that rely on geophysical knowledge and characterize what each requires from the discipline.

## Prerequisites

No technical prerequisites. Familiarity with basic SI units and with the qualitative concept of a physical wave from introductory physics is assumed.

---

## 1. The Geoscientific Question: Why Geophysics Exists

On the morning of January 26, 1700, the coastline of the Pacific Northwest dropped by more than a meter in minutes. A fault 1,300 km long — running offshore from northern California to British Columbia — ruptured after centuries of locked, silent strain accumulation. The magnitude 9 earthquake that followed sent tsunami waves across the Pacific; Japanese coastal records document their arrival. Those historical accounts, combined with drowned coastal forests with rings that stop in 1699, sand sheets deposited by the tsunami in coastal marshes, and oral traditions of Indigenous communities, constitute the complete observational basis for reconstructing an event for which no instrumental seismic record exists. Everything known about that rupture — its date, lateral extent, and magnitude — is the product of geophysical inference from indirect evidence.

This is the characteristic mode of the discipline. Earth's interior is permanently inaccessible to direct sampling beyond a few kilometers. The structures, dynamics, and physical state of that interior govern the planet's evolution, control the distribution of natural hazards, and determine the location of resources on which civilization depends. Geophysics addresses this constraint by measuring physical fields at or above the surface — seismic wave travel times, gravitational acceleration, magnetic field strength, surface deformation, heat flux — and reasoning backward through established physical theory to infer what must exist below.

:::{admonition} Definition
:class: important
**Solid Earth geophysics** is the quantitative study of Earth's internal structure, composition, and dynamics through observations of physical fields measured at or above the surface. Its defining epistemological challenge is that every surface measurement reflects the combined, overlapping response of multiple Earth properties, so the mapping from observation to subsurface structure is inherently non-unique. Additional physical constraints or multiple independent data types are always required to stabilize an inference.
:::

---

## 2. Three Motivating Contexts

Every geophysical investigation is driven by at least one of three scientific and societal motivations. These contexts determine the questions being asked, the required precision, and the criterion for an acceptable answer.

### 2.1 Geodynamics: Planetary and Landscape Evolution

Geodynamics addresses the long-term physical behavior of a planet whose interior is hot, slowly convecting, and chemically differentiated. Timescales of interest span millions to billions of years; spatial scales range from grain-scale melting of mantle peridotite to the global circulation of convection cells. No sample has been retrieved from the mantle under equilibrium conditions, and the pressures and temperatures of the lower mantle and core cannot be sustained in a laboratory at representative volumes. Geophysical inference through seismic wave velocities (sensitive to temperature and mineralogy), gravity anomalies (sensitive to density), and heat flow measurements (sensitive to the thermal state of the lithosphere) constitutes the only available window into this domain.

Key processes include mantle convection, lithospheric flexure, isostasy, magma migration, glacial isostatic adjustment, and seafloor spreading. The Juan de Fuca Plate subducts beneath North America at approximately 3 cm/yr — a rate determined not by drilling but by GPS geodesy, which measures the interseismic compression of the upper plate. The geometry of the subducting slab at depth is constrained by seismic tomography. Both measurements are made entirely at or above the surface.

### 2.2 Natural Hazards: Physics in Service of Public Safety

Hazard geophysics applies the physics of Earth processes to predicting, monitoring, and mitigating the consequences of earthquakes, volcanic eruptions, tsunamis, and landslides. Ground-shaking models feed into building codes; early-warning algorithms determine how many seconds of warning are physically achievable before destructive shaking arrives; fault geometry and coupling estimates constrain the probable magnitude of future events.

The ShakeAlert earthquake early warning system, operational from Alaska to California, uses real-time P-wave detection at dense seismic networks to estimate shaking magnitude and transmit warnings before the slower S-waves arrive. The available lead time — seconds to tens of seconds — is sufficient to slow high-speed trains, open fire station doors, and trigger automated safety shutoffs in industrial systems. The wave propagation physics underlying this system constitutes the content of Weeks 2 through 5 of this course.

### 2.3 Resource Management: Subsurface Characterization for Human Use

Resource geophysics employs subsurface imaging to locate and characterize economically and environmentally significant targets: petroleum reservoirs, groundwater aquifers, ore bodies, geothermal resources, and CO₂ storage formations. Before drilling a wildcat well, exploration companies acquire seismic reflection surveys in which airguns towed behind ships emit elastic pulses that reflect off subsurface rock interfaces, reconstructing stratigraphy kilometers below the seafloor. The global exploration geophysics market represents tens of billions of dollars annually.

The same physical methods now serve the clean-energy transition: geothermal resource assessment, critical mineral exploration for battery materials, and time-lapse monitoring of CO₂ injection sites all draw on the subsurface imaging toolkit originally developed for petroleum exploration.

:::{figure} ../assets/figures/fig_three_motivations.png
:name: fig-three-motivations
:alt: Three-column schematic diagram. Left column labeled Geodynamics shows a cross-section of Earth with two convection cells in the mantle and a subducting plate descending through the crust into the mantle. Center column labeled Natural Hazards shows a map view of a fault trace with concentric shaking intensity ellipses and a star at the epicenter and triangles marking seismic stations. Right column labeled Resource Management shows a seismic reflection section with wavy sedimentary horizons and a highlighted reservoir trap at depth. Each column lists the key physical process and primary observable beneath the schematic.
:width: 95%
**Figure 1.1.** The three motivating contexts for solid Earth geophysics. Every topic in this course connects to at least one of these pillars. The same physical methods frequently serve multiple motivations simultaneously. [Python-generated. Script: `assets/scripts/fig_three_motivations.py`]
:::

---

## 3. The Five Physics Domains

The governing equations of geophysical processes are the equations of classical physics, encountered in different forms and at different scales in introductory courses. In geophysics, these equations connect surface observables to subsurface Earth properties through the forward operator structure discussed in Lecture 2.

| Physics Domain | Governing Equation | Earth Property Sensed | Primary Observable |
|---|---|---|---|
| Continuum mechanics | $\rho\,\ddot{\mathbf{u}} = \nabla \cdot \boldsymbol{\sigma} + \mathbf{f}$ | Elastic moduli $\lambda$, $\mu$; density $\rho$ | Seismograms |
| Wave phenomena | $\nabla^2 u = v^{-2}\,\partial^2 u/\partial t^2$ | P-speed $\alpha$, S-speed $\beta$ | Travel times, waveforms |
| Newtonian gravity | $\nabla^2 \Phi = 4\pi G\rho$ | Density $\rho$ | Gravitational acceleration $\mathbf{g}$ |
| Electromagnetism | $\nabla\times\mathbf{B} = \mu_0\mathbf{J}$; $\mathbf{J} = \sigma_e\mathbf{E}$ | Conductivity $\sigma_e$, magnetization | Magnetic and EM anomalies |
| Thermodynamics | $\rho c_p \partial T/\partial t = \nabla\cdot(k\nabla T) + Q$ | Temperature $T$, conductivity $k$ | Heat flux $q$ (mW/m²) |

These equations are introduced here as an organizing map, not as material to be learned immediately. Each will be derived or applied in detail during the relevant module. The purpose at this stage is to establish the structural unity of geophysics as a discipline: in every domain, a surface measurement is connected to a subsurface Earth property through a well-understood physical operator.

:::{admonition} Key Concept
:class: important
Every geophysical observable is indirect. Travel time is measured — not seismic velocity. Gravitational acceleration is measured — not density. Magnetic field strength is measured — not rock composition. The Earth property of interest is always inferred through a physical model. This is not a methodological limitation to be overcome; it is the defining logical structure of the discipline.
:::

---

## 4. Passive vs. Active Surveys

All geophysical observation divides into two fundamental strategies distinguished by the origin of the measured signal.

### 4.1 Passive Methods

Passive surveys measure fields generated naturally by the Earth, without any artificial source. Natural sources include earthquakes (elastic waves), the geomagnetic field (generated by outer-core convection), gravity (produced by mass distributions), ambient seismic noise (ocean microseisms, wind, traffic), and radiogenic and primordial heat.

Passive methods carry no source cost and can operate continuously over years to decades. Their fundamental limitation is the absence of source control: the location, timing, frequency content, and amplitude of natural signals are not specified by the investigator, which constrains spatial resolution and produces uneven coverage tied to natural source distributions. Seismic tomography is substantially better resolved beneath seismically active plate margins than beneath stable cratons.

*Examples:* Earthquake seismology, global seismic tomography, gravity surveying, geomagnetic monitoring, GPS geodesy, ambient noise interferometry.

### 4.2 Active Methods

Active surveys generate a controlled signal and record how the Earth modifies it. Sources include explosive charges, vibroseis trucks, marine airguns, direct electrical current injection, and radar pulses. Full control over source parameters enables substantially higher spatial resolution than passive methods for equivalent target depths. Cost is correspondingly high — marine seismic reflection surveys can exceed $50 million — and environmental permitting is required for energetic sources.

*Examples:* Seismic reflection surveys, seismic refraction surveys, ground-penetrating radar, electrical resistivity tomography, controlled-source electromagnetic surveys.

:::{admonition} Key Contrast
:class: important
Passive methods provide continuous global coverage at resolution constrained by natural source distributions. Active methods provide high-resolution snapshots of specific targets at substantial cost. Most rigorous campaigns combine both: an active survey images static structure; a passive network monitors its evolving behavior over time. The 2021 Cascadia Seismic Imaging Experiment (CASIE21) combined active marine airgun sources with passive ocean-bottom seismometers — a paradigmatic example of integrated survey design.
:::

---

## 5. The Stakeholder Landscape

Geophysical knowledge flows into decisions made by a wide range of institutions with distinct requirements and distinct tolerance for uncertainty.

**Research universities and national laboratories** develop physical models, curate open datasets, and train the scientists who populate all other sectors. The ESS department at UW works directly on Cascadia hazard, deep Earth structure, and novel sensing methods through PNSN and collaborating research groups.

**Government agencies** use geophysical monitoring for public safety and regulatory compliance. The USGS monitors earthquakes and volcanoes and produces probabilistic seismic hazard maps that determine building code zones. NOAA operates the Pacific Tsunami Warning Center. The Comprehensive Nuclear-Test-Ban Treaty Organization (CTBTO) operates a global seismic monitoring network whose primary mission — discriminating nuclear explosions from earthquakes — draws on the same seismological methods used in academic research.

**Engineering and consulting firms** characterize subsurface conditions for construction. The Vs30 parameter — the time-averaged shear-wave velocity in the upper 30 m — appears in every modern seismic building code and is measured by active seismic refraction surveys. Dam stability assessment, underground tunnel routing, and high-rise foundation design all require geophysical site characterization.

**Energy and mining companies** use seismic, gravity, and electromagnetic surveys to locate and evaluate oil, gas, geothermal, and mineral resources. The same methods increasingly serve the clean-energy transition.

**Environmental agencies** apply resistivity, electromagnetic, and GPR methods to map groundwater, detect contaminated plumes, characterize landfill sites, and locate buried hazardous infrastructure.

**Defense and intelligence agencies** use seismic networks for nuclear test monitoring and underground facility characterization — signal discrimination problems that push the boundary of applied seismology.

---

## 6. Worked Example: Measurement Precision and Significant Figures

Magnetic lineation surveys of the seafloor near the Juan de Fuca Ridge show that the boundary between reversely magnetized crust (formed during the Brunhes–Matuyama polarity reversal) and normally magnetized crust lies approximately 21 km from the ridge axis. The Brunhes–Matuyama boundary has a radiometrically determined age of 0.78 Ma. The half-spreading rate is:

$$v = \frac{d}{t} = \frac{21 \times 10^5 \text{ cm}}{0.78 \times 10^6 \text{ yr}} = 2.692... \text{ cm/yr}$$

The raw arithmetic yields 2.692307... cm/yr. However, the distance $d = 21$ km carries at most two significant figures, reflecting measurement uncertainty in locating the reversal boundary in the magnetic anomaly profile. Propagating this constraint: $v \approx 2.7$ cm/yr.

The trailing digits in the raw result are physically meaningless — they encode no information about the real spreading rate. Misrepresenting precision propagates through geophysical analysis with concrete consequences: overconfident velocity models produce poorly resolved tomographic images; overconfident ground-motion predictions propagate into inappropriate building code specifications.

:::{admonition} Concept Check
:class: tip
1. The magnetic lineation method exploits a naturally occurring signal. What category of survey method does it represent, and what is the natural source it exploits?
2. If greater precision on the spreading rate were needed, which input — the distance or the age — would be more productive to refine, and on what physical or practical grounds?
3. The calculation assumes that the reversal boundary is uniformly located 21 km from the ridge axis along the entire profile. What geological processes could violate this assumption, and how would each affect the computed rate?
:::

---

## 7. Course Connections

- **Next lecture (Lecture 2):** The space–time scale diagram organizes all geophysical processes by characteristic length and duration and introduces the forward/inverse problem structure that unifies every subsequent topic.
- **Weeks 2–3:** The continuum mechanics and wave equations in the table above become the mathematical starting points for all seismological content.
- **Lab 1 (Friday):** ObsPy is introduced; a seismogram is retrieved from the IRIS FDSN client for a recent PNSN event. The goal at this stage is visual familiarity with the data type — P and S arrivals are identified before any wave theory has been developed.
- **Cross-topic link:** The passive/active distinction reappears in every module: natural seismicity vs. active-source reflection profiling, passive gravity mapping vs. active vibroseis, natural magnetic field measurement vs. controlled-source electromagnetic surveys.

---

## 8. Research Horizon

:::{admonition} Current Research Highlights (2022–2025)
:class: seealso

**Machine learning and passive seismic catalog expansion:** Deep learning models for seismic phase picking — EQTransformer (Mousavi et al., *Nature Communications*, 2020, DOI: [10.1038/s41467-020-17591-w](https://doi.org/10.1038/s41467-020-17591-w)) — have expanded earthquake catalogs by factors of 10–100 by detecting events previously below analyst-detection thresholds. Mousavi & Beroza (2022, *Science*, DOI: [10.1126/science.abm4470](https://doi.org/10.1126/science.abm4470)) survey the broader transformation of passive seismological analysis by deep learning, covering event detection, waveform classification, and ground-motion prediction.

**Distributed Acoustic Sensing on dark fiber:** Telecommunications fiber-optic cables function as dense passive seismic arrays when interrogated with laser pulses. Research groups are deploying DAS on dark fiber (unused buried cable) in Seattle and other urban areas, exploiting traffic noise and ocean microseisms as passive sources to image shallow subsurface structure at meter-scale resolution in four dimensions. Lindsey et al. (*Geophysical Research Letters*, 2020, DOI: [10.1029/2020GL088925](https://doi.org/10.1029/2020GL088925)) established foundational results for urban DAS ambient noise tomography.

**Active methods for the energy transition:** Time-lapse seismic monitoring of CO₂ injection sites requires integrating active and passive strategies simultaneously, raising new questions about source repeatability, noise characterization, and time-lapse signal detection. This is an active frontier in both academic research and industrial geophysics.

*Entry points for graduate research:* The SCOPED computational seismology workshop materials ([scoped.codes](https://scoped.codes)) and the IRIS FDSN data archive ([ds.iris.edu](https://ds.iris.edu)) are the primary open resources. PNSN maintains a public catalog and waveform archive for Pacific Northwest events at [pnsn.org](https://pnsn.org).
:::

---

## 9. Societal Relevance

:::{admonition} Why It Matters: Cascadia and the Pacific Northwest
:class: note

**Cascadia subduction zone hazard:** Paleoseismic and historical records establish that the Cascadia fault has generated full-margin magnitude 9+ earthquakes at recurrence intervals of roughly 200–500 years. Elastic strain has been accumulating since the January 1700 rupture. USGS probabilistic seismic hazard maps, which inform Washington State building codes, are derived from geophysical models of fault geometry, shear-wave velocity structure, and site amplification. The uncertainty in these models — propagated through careful inverse problem formulation — is itself a critical input to risk management and engineering design.

The ShakeAlert earthquake early warning system represents the operational deployment of passive seismic monitoring for direct public benefit. Real-time Pacific Northwest seismicity is accessible at [pnsn.org](https://pnsn.org).

**Further exploration:** Goldfinger et al. (2012), *USGS Professional Paper 1661-F* (open access, [pubs.usgs.gov/pp/pp1661f](https://pubs.usgs.gov/pp/pp1661f)) — the turbidite-based paleoseismic record of Cascadia. USGS ShakeAlert: [usgs.gov/programs/earthquake-hazards/shakealert](https://www.usgs.gov/programs/earthquake-hazards/shakealert).
:::

---

## AI Literacy

:::{admonition} Analytical Exercise 1.1 — Evaluating an AI-Generated Definition
:class: tip
The following prompt was submitted to a general-purpose AI assistant:

*"Define solid Earth geophysics in one paragraph and explain why geophysicists cannot simply drill to the locations they want to study."*

Evaluate a generated response against the content of this lecture:
- Does the response correctly state that Earth's interior is inaccessible to direct sampling beyond a few kilometers?
- Does it connect this inaccessibility to the necessity of indirect, surface-based measurement?
- Does it provide a specific example of a geophysical inference — a structural boundary, a fault location, a density anomaly?
- Identify one claim in the response that requires verification, and specify what source or calculation would provide that verification.

This exercise prepares for Discussion Section (Wednesday), where AI-generated geoscience content is evaluated systematically.
:::

---

## Further Reading

- Lowrie, W. & Fichtner, A. (2020). *Fundamentals of Geophysics*, 3rd ed. Cambridge University Press. DOI: [10.1017/9781108685917](https://doi.org/10.1017/9781108685917). §1.1–1.3. *(Free via UW Libraries)*
- MIT OpenCourseWare 12.201 Essentials of Geophysics. Lecture 1 notes. [ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004](https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004). CC BY NC SA.
- Mousavi, S.M. & Beroza, G.C. (2022). Deep-learning seismology. *Science*, 377(6607). DOI: [10.1126/science.abm4470](https://doi.org/10.1126/science.abm4470). *(Open access)*
- Goldfinger, C. et al. (2012). Turbidite event history — Cascadia subduction zone. *USGS Professional Paper 1661-F*. [pubs.usgs.gov/pp/pp1661f](https://pubs.usgs.gov/pp/pp1661f). *(Public domain)*
- Pacific Northwest Seismic Network. [pnsn.org](https://pnsn.org). *(Open access, real-time data)*
