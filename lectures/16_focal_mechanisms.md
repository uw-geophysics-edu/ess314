---
title: "Earthquake Focal Mechanisms and Faults"
week: 4
lecture: 16
date: "2026-05-04"
topic: "Focal mechanisms, the double couple, and Cascadia source diversity"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4", "LO-7"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-C", "LO-OUT-D", "LO-OUT-E", "LO-OUT-H"]
open_sources:
  - "Lowrie & Fichtner (2020) Ch. 3.5 (UW Libraries)"
  - "Aki & Richards (2002) Ch. 4 (cite only)"
  - "Global CMT Project: globalcmt.org"
  - "PNSN focal-mechanism catalog: pnsn.org"
  - "USGS Comprehensive Earthquake Catalog"
---

# Earthquake Focal Mechanisms and Faults

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_16_slides.html" target="_blank">open in new tab ↗</a>
:::

::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-1]** Explain the four-quadrant compression / dilatation P-wave radiation pattern produced by a slipping fault, and connect it to the underlying double-couple representation of a shear dislocation.
- **[LO-2]** Read a beach-ball diagram and identify the fault style (strike-slip, normal, thrust) and approximate strike, dip, and rake.
- **[LO-3]** Pose focal-mechanism determination as an inverse problem: given a set of P-wave first-motion polarities at a network of stations, infer $(\phi_s, \delta, \lambda)$.
- **[LO-4]** Explain the fault-plane / auxiliary-plane ambiguity and identify the independent observations (aftershocks, geology, geodesy) needed to resolve it.
- **[LO-7]** Critique a machine-learning polarity picker or focal-mechanism estimator by identifying the assumptions inherited from training data and station distribution.

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1, LO-2, LO-3, LO-4, LO-7 |
| **Learning outcomes practiced** | LO-OUT-A (radiation pattern), LO-OUT-C (read beach balls), LO-OUT-D (interpret ambiguity), LO-OUT-E (connect to plate tectonics), LO-OUT-H (critique ML solutions) |
| **Prior lecture** | [Lecture 15 — Earthquake Phenomena II](../lectures/15_earthquake_phenomena_II.html): magnitude, energy, and the seismic moment $M_0$ |
| **Next lecture** | [Lecture 17 — Tsunami](../lectures/17_tsunami.html): coupling source mechanism to ocean dynamics |
| **Lab connection** | Lab 6 — first-motion focal-mechanism analysis with `ObsPy` on PNSN waveforms (week 5) |

::::

## Prerequisites

Before reading this lecture, students should be comfortable with the seismic-wave types and the location problem of [Lecture 14](14_earthquake_phenomena_I.md), and with the magnitude and seismic-moment formalism of [Lecture 15](15_earthquake_phenomena_II.md). The forward / inverse-problem framework introduced in the refraction (Lectures 6, 7) and tomography (Lecture 12) chapters is reused: focal-mechanism determination is one of the cleanest small inverse problems in geophysics.

---

## 1. The framing question: what does the first wiggle tell us about the fault?

On the morning of 28 February 2001, a magnitude 6.8 earthquake nucleated 53 km beneath Anderson Island in southern Puget Sound. Buildings in downtown Seattle swayed for nearly 45 seconds, the State Capitol in Olympia was damaged, and a quarter of a million people felt strong shaking from Bellingham to Eugene. The earthquake was deep — far below the locked Cascadia megathrust — and it was extensional: the descending Juan de Fuca slab was pulling itself apart under its own weight.

How is any of that *known*? No one was at the hypocentre. No fault was ruptured to the surface. The depth and the style of faulting were both inferred from the first wiggles to arrive at seismic stations across western North America — from the polarity, amplitude, and timing of the P-wave.

The instrument that converts those wiggles into a tectonic statement is the **focal mechanism**: a compact summary of the geometry of the source — the orientation of the fault plane, the direction of slip on it, and the resulting four-lobed pattern of compressional and dilatational P-wave radiation. Every earthquake catalogued by the Pacific Northwest Seismic Network (PNSN) larger than about $M$ 3 has one. The Global Centroid-Moment Tensor (Global CMT) project has produced more than 65,000 of them since 1976. They populate every published map of plate boundaries and underlie nearly every regional stress inversion.

This lecture builds the focal mechanism from the ground up: from the four-quadrant push–pull pattern, through the fault-plane / auxiliary-plane ambiguity, to the strike–dip–rake parameterization that connects the seismic source to plate tectonics. Cascadia provides the running example, because four different fault styles — megathrust, intraslab normal, crustal thrust, and oceanic transform — coexist within a few hundred kilometres of Seattle.

---

## 2. The physics: faults as double couples

### 2a. Faults as double couples

When two blocks of rock slide past each other on a planar fault, the elastic medium surrounding the fault is loaded with a very specific pattern of stress. To leading order — that is, ignoring fault curvature and finite source dimensions — that pattern is mathematically equivalent to a **double couple**: two pairs of equal and opposite forces, with no net force or net torque, oriented at 45° to the fault and slip directions.

The double-couple equivalence was not obvious at first. In the early twentieth century, several seismologists assumed earthquakes were point explosions or single force couples. Both predictions disagreed with observation. The double-couple representation, formalized by {cite:t}`BurridgeKnopoff1964`, is the one that reproduces the observed first-motion polarity pattern of natural earthquakes — and it does so without requiring net mass or net torque to disappear, both of which would violate conservation laws.

```{admonition} Key concept — Double-couple equivalent body force
:class: tip

A point shear dislocation on a fault is mathematically equivalent to a pair of perpendicular force couples acting at the source. The two couples cannot be distinguished from far-field seismic radiation alone. This equivalence is the geometric origin of the **fault-plane / auxiliary-plane ambiguity**: two perpendicular planes produce identical P-wave radiation patterns.
```

### 2b. The four-quadrant push–pull pattern

The key physical observation is that a slipping fault does not radiate seismic energy uniformly in all directions. Two quadrants of the surrounding rock are pushed *outward* (the P-wave begins as a **compression**); the other two quadrants are pulled *inward* (the P-wave begins as a **dilatation**, sometimes called a rarefaction). The boundary between the two quadrant pairs is formed by the fault plane and the **auxiliary plane** — a second plane perpendicular to the slip vector and to the fault plane.

```{figure} ../assets/figures/fig_pushpull_quadrants.png
:name: fig-pushpull
:alt: Map view of a right-lateral north-striking strike-slip fault. Four quadrants are shaded by P-wave first-motion polarity: northeast and southwest in vermilion (compression, "push"), northwest and southeast in blue (dilatation, "pull"). Three seismograms at the surface show first motions consistent with the quadrant in which each station sits.
:width: 92%

The four-quadrant first-motion pattern for a right-lateral, north-striking strike-slip fault. Stations in the compressional quadrants (NE, SW) record a P-wave that begins with an upward (positive) first motion. Stations in the dilatational quadrants (NW, SE) record a downward (negative) first motion. The boundary between quadrants is the nodal plane, where the P amplitude vanishes.
```

### 2c. Reading first motions

A vertical-component seismometer near a station in a compressional quadrant records ground motion that begins by moving *upward*. A station in a dilatational quadrant sees ground motion that begins by moving *downward*. With a sufficiently dense network — historically a dozen stations distributed around the source were enough — the locations of stations with upward first motions can be separated from those with downward first motions by two perpendicular nodal planes. One of those planes is the fault.

This is the essential idea of **first-motion focal mechanism analysis**, developed in the 1930s and 40s by Byerly, Hodgson, and others, refined by Honda (1962) and {cite:t}`AkiRichards2002`, and still in routine use at PNSN, USGS, and every major seismic network.

### 2d. The focal sphere

To organise station observations geometrically, seismologists construct an imaginary sphere of small radius around the hypocentre, called the **focal sphere**. The take-off direction of the ray that reaches each station — that is, the direction the P-wave was travelling when it left the source — pierces this sphere at one point. Each point is then tagged with the polarity recorded at the corresponding station. Because rays leaving the source toward the surface generally take off downward into the lower hemisphere (for shallow events recorded at teleseismic distances) or are mapped there by convention, only the lower hemisphere is plotted. A stereographic projection converts the lower hemisphere to a 2-D disk: the **beach ball**.

```{figure} ../assets/figures/fig_focal_sphere.png
:name: fig-focal-sphere
:alt: Three-panel illustration of the focal sphere. Left panel shows a 3D sphere around the hypocentre with two perpendicular nodal planes carving four quadrants; rays from the source pierce the sphere outward. Centre panel shows the lower hemisphere isolated as a bowl, with shaded compression quadrants and unshaded dilatation quadrants. Right panel shows the stereographic projection of the lower hemisphere as a 2D disk — the beach ball — with the same shading.
:width: 96%

Construction of the beach-ball diagram. (a) The focal sphere is an imaginary sphere centred on the hypocentre; rays leaving the source pierce it at the take-off direction toward each station. (b) The lower hemisphere is retained and shaded by polarity. (c) A stereographic projection of the lower hemisphere produces the 2-D beach ball used in catalogues and maps. Filled (dark) quadrants are compressional; open (white) quadrants are dilatational.
```

By convention, **filled quadrants represent compression** and **open quadrants represent dilatation**. The two great circles dividing the four quadrants are the projections of the fault plane and the auxiliary plane.

---

## 3. The mathematical framework: moment tensor and radiation pattern

### 3a. Notation

| Symbol | Meaning | Units |
|--------|---------|-------|
| $\mathbf{u}$ | Slip vector on the fault (displacement of hanging wall relative to footwall) | m |
| $\mathbf{n}$ | Unit normal to the fault plane | dimensionless |
| $\hat{\mathbf{d}}$ | Unit vector in the slip direction | dimensionless |
| $A$ | Fault area | m² |
| $\mu$ | Shear modulus of the source region | Pa |
| $M_0$ | Scalar seismic moment | N·m |
| $M_{ij}$ | Components of the moment tensor | N·m |
| $\phi_s$ | Strike: azimuth of the fault trace, 0–360° from north | degrees |
| $\delta$ | Dip: angle of the fault plane below horizontal, 0–90° | degrees |
| $\lambda$ | Rake: angle of slip vector measured in the fault plane from strike, $-180°$ to $180°$ | degrees |
| $F^P$ | P-wave radiation pattern coefficient | dimensionless |
| $\phi$ | Azimuth from source to station, measured from north | degrees |
| $i$ | Take-off angle from vertical at the source | degrees |

### 3b. The seismic moment tensor

For a planar shear dislocation, the equivalent body-force distribution is the **seismic moment tensor**:

$$
M_{ij} = M_0 \, (n_i \, d_j + n_j \, d_i)
$$ (eq:moment-tensor)

where $\mathbf{n}$ is the fault normal and $\hat{\mathbf{d}}$ is the unit slip direction. The scalar moment is

$$
M_0 = \mu \, A \, |\mathbf{u}|
$$ (eq:scalar-moment)

with units of N·m. The symmetry of equation {eq}`eq:moment-tensor` under the interchange $\mathbf{n} \leftrightarrow \hat{\mathbf{d}}$ is the algebraic origin of the **fault-plane / auxiliary-plane ambiguity**: swapping the role of the normal and slip vectors leaves the moment tensor unchanged. Far-field seismic radiation depends only on $M_{ij}$, so no purely seismic measurement can resolve which of the two perpendicular planes is the actual fault.

### 3c. The P-wave radiation pattern

The far-field P-wave displacement radiated by a double-couple source has a well-known angular dependence. For a vertical strike-slip fault striking north (so that $\mathbf{n}$ points east and $\hat{\mathbf{d}}$ points north), the P-wave radiation pattern observed in the horizontal plane reduces to:

$$
F^P(\phi) = \sin(2\phi)
$$ (eq:fp-strike-slip)

where $\phi$ is the azimuth measured from north. Equation {eq}`eq:fp-strike-slip` is positive (compression) in the quadrants $0 < \phi < 90°$ (northeast) and $180° < \phi < 270°$ (southwest), and negative (dilatation) in the other two quadrants. This is the algebraic form of the four-lobed pattern visible in {numref}`fig-pushpull`.

The general formula, valid for an arbitrary double couple and arbitrary take-off direction, is given in {cite:t}`AkiRichards2002` (eq. 4.84):

$$
F^P = \cos\lambda \sin\delta \sin^2 i \, \sin 2(\phi - \phi_s)
- \cos\lambda \cos\delta \sin 2i \, \cos(\phi - \phi_s)
+ \sin\lambda \sin 2\delta \, (\cos^2 i - \sin^2 i \sin^2(\phi - \phi_s))
+ \sin\lambda \cos 2\delta \sin 2i \, \sin(\phi - \phi_s)
$$ (eq:fp-general)

The sign of $F^P$ at the take-off direction $(i, \phi)$ predicts the polarity recorded at the corresponding station; its magnitude predicts the relative amplitude. Equation {eq}`eq:fp-general` is dimensionless. The full P-wave displacement carries an additional factor $M_0 / (4\pi \rho \alpha^3 r)$ for density $\rho$, P-wave speed $\alpha$, and source–receiver distance $r$.

### 3d. Strike, dip, and rake

Three angles fully specify the orientation of a fault and the direction of slip on it.

```{figure} ../assets/figures/fig_fault_geometry.png
:name: fig-fault-geometry
:alt: 3D block diagram of a fault plane cutting through a horizontal slab. The strike direction φ_s is shown as a green arrow along the trace of the fault on the horizontal surface, measured clockwise from north. The dip angle δ is a vermilion arc between the horizontal and the fault plane. The slip vector u lies in the fault plane; the rake λ is a pink arc measured from the strike direction to the slip vector, in the plane of the fault.
:width: 92%

Definitions of the three fault-orientation angles. **Strike** $\phi_s$ is the azimuth of the fault trace on the horizontal surface, measured clockwise from north (0° to 360°). **Dip** $\delta$ is the angle of the fault plane below horizontal, measured perpendicular to the strike (0° to 90°). **Rake** $\lambda$ is the direction of slip of the hanging wall relative to the footwall, measured in the fault plane from the strike direction ($-180°$ to $180°$).
```

The convention for rake follows {cite:t}`AkiRichards2002`:

```{figure} ../assets/figures/fig_rake_convention.png
:name: fig-rake
:alt: Polar wheel diagram showing the rake angle convention. Rake of 0° is labelled left-lateral strike-slip; 90° is reverse (thrust); 180° (and -180°) is right-lateral strike-slip; -90° is normal. Diagonal angles 45°, 135°, -135°, -45° label oblique slip directions.
:width: 80%

Rake convention. A rake of $\lambda = 0°$ corresponds to **left-lateral** strike-slip motion; $\lambda = 90°$ is pure **thrust** (reverse) faulting; $\lambda = 180°$ (or $-180°$) is **right-lateral** strike-slip; $\lambda = -90°$ is pure **normal** faulting. Intermediate values describe oblique slip.
```

The four end-member faulting styles, together with their typical ranges of dip and rake, are summarised in {numref}`tbl-fault-styles`.

```{table} Typical dip and rake ranges for the three end-member fault styles.
:name: tbl-fault-styles

| Style          | Dip $\delta$ | Rake $\lambda$ | Tectonic setting                          |
|----------------|--------------|----------------|-------------------------------------------|
| Strike-slip    | 70°–90°      | 0° or ±180°    | Transform boundaries, intracontinental    |
| Normal         | 40°–70°      | $-135°$ to $-45°$ | Rifts, mid-ocean ridges, back-arc        |
| Thrust/reverse | 5°–40°       | 45° to 135°    | Subduction megathrusts, fold-and-thrust belts |
```

```{figure} ../assets/figures/fig_three_faults.png
:name: fig-three-faults
:alt: Three-row figure. Row a (strike-slip) shows a 3D block diagram with vertical fault plane and horizontal slip arrows, beach ball with four black-and-white quadrants, and tectonic-context box noting transform boundaries. Row b (normal) shows a block diagram with hanging wall down-dropping along a 60-degree dipping fault, beach ball with white centre and dark outer crescents, and context box noting rifts and ridges. Row c (reverse) shows a block diagram with hanging wall thrusting up along a 30-degree dipping fault, beach ball with dark centre and white outer crescents, and context box noting subduction zones.
:width: 96%

The three end-member fault styles, each shown as a 3D block diagram, beach ball, and tectonic-context summary. The beach-ball signatures are distinctive: strike-slip events show four quadrants meeting at the centre; normal events have a white ("open") inner section flanked by dark crescents; thrust events show the inverse — dark inner section flanked by white crescents.
```

---

## 4. The forward problem: predicting polarity at every station

The forward problem is straightforward in principle: given the source parameters $(\phi_s, \delta, \lambda)$ and the source–station geometry, predict the P-wave first-motion polarity and relative amplitude at every station. Three steps are required.

1. **Compute the moment tensor** $M_{ij}$ from $(\phi_s, \delta, \lambda)$ using the standard transformation ({cite:t}`AkiRichards2002`, eq. 4.85). This is a fixed mapping: given three angles, the six-component symmetric moment tensor is determined.

2. **Compute the take-off direction $(i, \phi)$** of the ray that reaches each station. For shallow earthquakes recorded at regional distances, $i$ depends on the velocity model and the epicentral distance through ray tracing. For the simple case of a half-space, $i$ ranges from near-vertical (for nearby stations) to near-horizontal (for distant stations).

3. **Evaluate the radiation pattern** $F^P(i, \phi; \phi_s, \delta, \lambda)$ from equation {eq}`eq:fp-general`. The sign of $F^P$ predicts the polarity; the magnitude predicts the relative amplitude.

The companion lab notebook implements this forward calculation with [`ObsPy`](https://docs.obspy.org/) and reproduces the beach-ball diagrams in this lecture.

---

## 5. The inverse problem: from polarities to strike, dip, and rake

In practice, seismologists rarely run the forward calculation in isolation. The everyday task is the inverse: given a set of observed polarities (and possibly amplitudes) at a network of stations, infer $(\phi_s, \delta, \lambda)$.

The inverse problem can be posed as:

> **Find the strike, dip, and rake that best separate the stations with positive first motions from those with negative first motions on the focal sphere.**

Algorithmically, this is a search over the three-dimensional space of orientations. Classical methods such as **FPFIT** {cite:p}`Reasenberg1985FPFIT` grid-search the three angles and minimise the number of misfit stations. Modern implementations such as **HASH** {cite:p}`Hardebeck2002HASH` additionally use first-motion amplitudes and weight the search by station-coverage uncertainty. Full waveform inversions (e.g., the Global CMT method) fit the long-period waveforms of body and surface waves and recover all six independent moment-tensor components, including non-double-couple parts.

The single most important caveat is the **fault-plane / auxiliary-plane ambiguity** introduced in section 3b.

```{admonition} Key concept — Resolving the ambiguity
:class: warning

The two nodal planes of a focal mechanism are mathematically equivalent in their P-wave radiation. Choosing which one is the fault requires *external* information:

- **Aftershock distribution** — the cloud of small earthquakes following a mainshock typically delineates the actual rupture plane.
- **Surface rupture** — when the fault breaks the surface, geological mapping resolves the ambiguity directly.
- **Geodesy** — InSAR or GPS displacement fields fit better to one plane than the other.
- **Tectonic context** — for the 2001 Nisqually intraslab event, the plane consistent with the geometry of the descending Juan de Fuca slab is the fault.

A focal mechanism alone is consistent with two different earthquakes. Closing the gap is a research problem in itself.
```

---

## 6. A worked example: the 2001 Nisqually earthquake

The Nisqually mainshock (28 February 2001, $M_w$ 6.8, depth 53 km, beneath southern Puget Sound) is the largest earthquake to strike the central Puget Lowland in the modern instrumental era. Its focal mechanism, as determined by both first-motion analysis and full-waveform inversion {cite:p}`Ichinose2004Nisqually`, is

$$
\phi_s = 357°, \quad \delta = 83°, \quad \lambda = -104°.
$$

Two questions clarify what these numbers mean.

**Worked check 1 — fault style.** The rake $\lambda = -104°$ falls in the **normal** range ($-135°$ to $-45°$), so the Nisqually event is a normal-faulting earthquake. Physically, the steeply-dipping fault separated a hanging wall block that *dropped* relative to the footwall. This is consistent with **downdip extension within the descending Juan de Fuca slab** — the slab is being stretched by its own weight as it sinks into the upper mantle.

**Worked check 2 — predicted polarity at a regional station.** Suppose a vertical-component seismometer at PNSN station LON (Longmire, ≈80 km southeast of the epicentre at azimuth ≈135° from the source) records the first motion. Using equation {eq}`eq:fp-strike-slip` as a rough proxy (treating the event approximately as vertical strike-slip for the demonstration), we substitute $\phi - \phi_s \approx 135° - 357° = -222° \equiv 138°$ into $\sin 2(\phi - \phi_s) = \sin 276° \approx -0.99$. The simplified pattern predicts a **dilatational (downward) first motion** at LON. (For the *actual* Nisqually mechanism — which is not vertical strike-slip but a steeply-dipping normal fault — the full equation {eq}`eq:fp-general` must be used. The point of the exercise is the procedure, not the precise answer.)

**Worked check 3 — which nodal plane is the fault?** The focal mechanism has nodal planes striking ≈177° (north–south) and dipping 83°W, and ≈342° dipping 14°E. The shallowly-dipping plane (14°) would correspond to a low-angle thrust geometry inconsistent with the deep, normal-faulting tectonic setting. The steep, near-vertical plane is geometrically consistent with **slab-internal, downdip-extensional rupture** within the Juan de Fuca slab, which dips ≈14°E in this region {cite:p}`McCrory2012Slab`. Independent constraints — slab geometry from PNSN earthquake locations and from receiver-function imaging — therefore support the steep N–S plane as the fault. This is exactly the kind of tectonic-context argument referenced in section 5.

---

## 7. Connecting to Cascadia: one margin, four mechanisms

The Cascadia margin hosts at least four distinct earthquake source types, each with a characteristic focal mechanism and a distinct hazard profile.

```{figure} ../assets/figures/fig_cascadia_focal_mechanisms.png
:name: fig-cascadia
:alt: Map of the Pacific Northwest from 40°N to 51°N showing the Cascadia subduction trench (sawtooth line offshore from northern California to Vancouver Island), the Blanco fracture zone offshore of Oregon, and four focal mechanisms. The 2001 Nisqually intraslab event near Seattle shows a normal-faulting beach ball; a Cascadia megathrust mechanism offshore central Oregon shows a shallow-thrust beach ball; a Seattle Fault crustal thrust shows a steep-thrust mechanism; the Blanco transform fault shows a strike-slip mechanism. Plate motion arrows show Juan de Fuca moving east-northeast at ~25 mm/yr and Pacific moving northwest at ~110 mm/yr relative to North America.
:width: 96%

Four representative focal mechanisms in the Pacific Northwest illustrate that a single subduction system contains multiple earthquake source types. The Cascadia megathrust (offshore) ruptures every ~500 years on average; the most recent event was $M$~9 in 1700. Crustal faults such as the Seattle Fault produce shallow thrust events directly beneath population centres. Intraslab events such as the 2001 Nisqually earthquake reflect downdip extension within the descending Juan de Fuca slab. The Blanco transform fault, offshore of Cape Mendocino, accommodates relative motion between the Juan de Fuca and Pacific plates with right-lateral strike-slip earthquakes.
```

Each style has a different shaking signature: subduction megathrusts produce long-duration shaking with strong long-period energy that excites tall buildings; crustal faults produce shorter, sharper pulses with potentially extreme peak accelerations directly above the rupture; deep intraslab events produce broadly distributed, moderate shaking but, because of their depth, do not generate tsunamis.

For Washington-state hazard planning, the focal-mechanism catalogue is therefore a *forecast input*, not a museum exhibit. Probabilistic shaking maps published by the Washington Department of Natural Resources and the USGS National Seismic Hazard Model rely on it, as do building-code revisions and emergency-response plans. The PNSN focal-mechanism catalogue is openly available at <https://pnsn.org>.

```{figure} ../assets/figures/fig_plate_boundary_focal.png
:name: fig-plate-boundary
:alt: Three panels showing characteristic focal mechanisms at each of the three plate-boundary types. Panel (a) is a divergent ridge with normal-fault beach balls along the spreading axis. Panel (b) is a transform fault with strike-slip beach balls along the offset. Panel (c) is a convergent margin showing a megathrust thrust beach ball above the subducting slab and a deep intraslab normal beach ball within the descending plate.
:width: 96%

Plate-boundary focal-mechanism signatures. Each plate-boundary type carries its own characteristic style. Subduction zones host *multiple* styles within the same kinematic framework — a key reason Cascadia is so geophysically rich.
```

---

## 8. Research Horizon

Three open problems in focal-mechanism research are accessible at the senior-undergraduate / first-year-graduate level.

**Real-time focal mechanisms for tsunami warning.** For very large earthquakes, the difference between an interplate thrust and an intraplate normal event determines tsunami potential. Operational systems must produce a reliable mechanism within minutes. The W-phase moment-tensor method now used at the USGS National Earthquake Information Center reduced this latency from hours (in 2004) to under 15 minutes today {cite:p}`Hayes2017Wphase`. The integration of these real-time mechanisms with the GFAST geodetic estimator discussed in [Lecture 14](14_earthquake_phenomena_I.md) is an active operational research area at the PNSN.

**Machine-learning focal mechanisms.** Because polarity picking is a binary classification on a noisy waveform, it lends itself naturally to deep learning. EQTransformer {cite:p}`Mousavi2020EQT` and related neural-network polarity pickers match or exceed analyst performance on dense networks. The open question — and the one that connects to the AI-literacy theme of this course — is whether such models *generalise* to networks with sparse station coverage, where their training distributions are not well represented.

**Stress-field inversion from mechanism catalogues.** A population of focal mechanisms in a region constrains the orientation of the regional principal stress axes. {cite:t}`Vavrycuk2014Stress` provides an open-source code (now ported to Python) for this inversion. Applied to the PNSN catalogue, the method recovers a stress field consistent with N–S compression in the forearc and downdip extension within the slab — the same physics that drove the Nisqually event of section 6.

---

## 9. AI Literacy: when to trust an automated focal mechanism

```{admonition} AI Epistemics — focal mechanisms as a test case
:class: warning

Focal mechanisms are an unusually good test case for AI literacy because the underlying inverse problem is small, well-posed, and produces visualisations that *look* informative even when they are wrong. Three habits matter:

1. **Always know the network geometry.** A beach ball produced from a network with poor azimuthal coverage — say, all stations on one side of the source — is consistent with a wide range of $(\phi_s, \delta, \lambda)$. The reported "best" solution is a single point in a flat misfit landscape. A pre-trained ML estimator does not know whether it is operating on data inside or outside its training distribution unless told.

2. **Always check both nodal planes.** No purely seismic measurement can distinguish the fault plane from the auxiliary plane. If an AI tool declares one plane to be "the fault" without citing aftershocks, geology, or geodesy, treat the claim as a hypothesis, not a result.

3. **Always carry the velocity-model assumption forward.** The take-off angles $i$ that map a station to the focal sphere are computed by ray tracing through a velocity model. ML estimators that consume travel-time picks inherit every error in that velocity model.
```

```{admonition} Prompt Lab — interrogating an AI explanation of a focal mechanism
:class: tip

**Activity (≈15 minutes, in groups of 3).**

1. **Design first.** Before consulting any AI tool, sketch on paper the workflow you would use to determine the focal mechanism of a hypothetical $M$ 5 earthquake in the central Puget Lowland. List inputs, processing steps, and outputs. Identify two assumptions you would have to make.

2. **Query.** Now ask a generative-AI tool the same question: *"How do I determine the focal mechanism of an M5 earthquake in the central Puget Lowland?"* Save the response.

3. **Evaluate.** Score the AI response on:

   - **Physics correctness** — Does it correctly distinguish polarity from amplitude? Does it mention the fault-plane ambiguity?
   - **Assumption transparency** — Does it state the velocity-model assumption? Does it mention station-coverage requirements?
   - **Operational feasibility** — Does it tell you which catalogue to query (PNSN, USGS), or does it imply the data are immediately available?
   - **Failure modes flagged** — Does the response warn about polarity-pick errors, networks with poor azimuthal coverage, or non-double-couple sources?

4. **Compare.** Two-paragraph writeup: where did your design exceed the AI response? Where did the AI response exceed your design? Identify one place where the AI was confidently wrong.

The goal is not to discredit AI tools — they are increasingly useful — but to develop the habit of treating their outputs as *hypotheses to be tested against the physics*.
```

---

## 10. Concept Checks

```{admonition} Synthesis questions
:class: tip

1. **Polarity reading.** A vertical-component seismometer records a downward first motion for the P-wave from a nearby earthquake. What does that tell you about the geometry between the station and the source?
2. **Beach-ball recognition.** A focal mechanism shows two nodal planes: one striking 005° and dipping 12°E, the other striking 185° and dipping 78°W. Aftershocks lie in a thin layer dipping ≈12°E. Which is the fault, and what style?
3. **Ambiguity.** Why can no purely seismic measurement distinguish the fault plane from the auxiliary plane? Name three independent observations that can.
4. **Tōhoku 2011.** The Global CMT solution for the 2011 $M_w$ 9 Tōhoku earthquake has $\phi_s = 203°$, $\delta = 10°$, $\lambda = 88°$. What is the fault style and what plate-boundary type does it represent?
5. **Cascadia comparison.** List the four Cascadia source types in {numref}`fig-cascadia` from largest to smallest expected tsunami threat, and justify the ordering using the physics of section 7.
6. **Forward problem.** Given $(\phi_s, \delta, \lambda) = (90°, 60°, 90°)$, sketch the predicted beach ball. Then identify the fault style.
7. **Network design.** A regional network has all stations within a 30°-azimuth wedge of the source. Which of the three angles $(\phi_s, \delta, \lambda)$ will be most poorly resolved, and why?
```

---

## 11. Connections

The focal mechanism is the bridge between the *seismogram* of [Lecture 14](14_earthquake_phenomena_I.md) and the *seismic moment* of [Lecture 15](15_earthquake_phenomena_II.md): the location problem fixes *where* the rupture happened, the magnitude problem fixes *how big*, and the focal mechanism fixes *what kind of motion*. The three together specify the source for every downstream calculation in this module.

Two upcoming lectures pick up the focal mechanism as input. The radiation pattern $F^P$ derived in section 3c governs the spatial distribution of strong ground motion near a rupture; the same physics is hidden inside ShakeMap's directivity correction. [Lecture 17 — Tsunami](17_tsunami.md) takes the focal mechanism as its primary source-side input: the vertical seafloor displacement that initiates a tsunami is determined entirely by the dip, rake, and seismic moment of the underlying fault.

Looking forward, [Lecture 18 (Earth's gravity)](18_earths_gravity.md) and [Lecture 23 (Earth's magnetic field)](23_earth_magnetism.md) reuse the forward / inverse-problem framework with very different observables. The fault-plane / auxiliary-plane ambiguity introduced here is one example of the broader non-uniqueness that pervades all geophysical inverse problems.

Looking backward, the take-off angle $i$ that maps a station to the focal sphere is computed by ray tracing through a velocity model — exactly the Snell's-law / ray-tracing machinery built up in Lectures 5 and 6. Every part of this lecture stands on machinery developed earlier in the term.

---

## Further Reading

- {cite:t}`AkiRichards2002` — Quantitative Seismology, Chapter 4 (radiation patterns from point sources). UW Libraries.
- {cite:t}`LowrieFichtner2020` — Fundamentals of Geophysics, 3rd ed., Chapter 3 §3.5 (earthquake source mechanisms). Free via UW Libraries.
- **Global CMT Project** — catalogue of moment-tensor solutions for earthquakes from 1976 to present. <https://www.globalcmt.org/>
- **Pacific Northwest Seismic Network** — regional earthquake catalogue and focal-mechanism solutions for PNW events. <https://pnsn.org/>
- **USGS Earthquake Hazards Program** — W-phase moment-tensor solutions for global $M \gtrsim 6$ events. <https://earthquake.usgs.gov/>

```{bibliography}
:filter: docname in docnames
```
