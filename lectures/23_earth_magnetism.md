---
title: "Earth Magnetism and Mineral Magnetism"
subtitle: "Where the field comes from, and how rocks remember it"
short_title: "Earth Magnetism"
week: 9
lecture: 23
date: "2026-06-01"
topic: "Magnetism I — the geomagnetic field and rock magnetism"
course_lo: ["LO-1", "LO-2", "LO-4"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-C"]
open_sources:
  - "Lowrie & Fichtner (2020), Fundamentals of Geophysics, 3rd ed., Ch. 5.1–5.3 (UW Libraries e-book)"
  - "Tauxe et al. (2018), Essentials of Paleomagnetism, 5th Web Edition (open access, EarthRef.org)"
  - "Butler (1992), Paleomagnetism: Magnetic Domains to Geologic Terranes (electronic edition freely available)"
  - "IGRF-13 model and field calculator: NOAA NCEI / IAGA (public domain, https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html)"
keywords: [geomagnetism, geodynamo, declination, inclination, IGRF, paleomagnetism, magnetite, Curie temperature, TRM, secular variation]
---

# Earth Magnetism and Mineral Magnetism

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_23_slides.html" target="_blank">open in new tab ↗</a>
:::

::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-23.1]** Decompose the geomagnetic field vector at a station into declination $D$, inclination $I$, and total intensity $F$, and convert between $(D, I, F)$ and the local $(X, Y, Z)$ Cartesian components.
- **[LO-23.2]** Identify the three principal sources of the surface field — core (geodynamo), lithosphere, and ionosphere — on the field's spatial power spectrum, and assign each source a characteristic wavelength range.
- **[LO-23.3]** Distinguish the five categories of magnetic ordering at the mineral scale (dia-, para-, ferro-, antiferro-, ferrimagnetic) and predict their behaviour in a geophysical setting.
- **[LO-23.4]** Describe how thermoremanent magnetization (TRM) is acquired on cooling through the Curie temperature, and identify the principal magnetic minerals encountered in Pacific Northwest rocks (magnetite, titanomagnetite, hematite, pyrrhotite) by their Curie temperatures.
- **[LO-23.5]** Apply the geocentric axial dipole equation $\tan I = 2 \tan \lambda$ as a forward problem (predict $I$ given $\lambda$) and as an inverse problem (estimate $\lambda$ with propagated uncertainty given a measured $I$).

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1 (observables ↔ Earth properties), LO-2 (forward model from source physics to surface field), LO-4 (method strengths, limitations, and uncertainty) |
| **Learning outcomes practiced** | LO-OUT-A (predict surface signature from a simple source model), LO-OUT-C (interpret a measurement as a constraint on subsurface structure with appropriate uncertainty) |
| **Prior lecture** | [L22 — Density and the Lithosphere](22_density_lithosphere.md) |
| **Next lecture** | [L24 — Magnetism and Plate Tectonics](24_magnetic_field_tectonics.md) |
| **Lab connection** | Lab 7 — Magnetic Anomaly Modeling (forward + inverse, induced dipole) |
| **Textbook** | Lowrie & Fichtner (2020), Ch. 5.1–5.3 |

::::

## Prerequisites

Students should be comfortable with the vector calculus introduced in the gravity module (Lectures 19–22) — in particular, the idea that a scalar potential generates a vector field by gradient, and that surface measurements can be projected onto local Cartesian components. Familiarity with the inverse-square law and with the concept of a non-uniqueness/ensemble-fit framework from gravity will transfer directly. No prior exposure to electromagnetism beyond an introductory-physics treatment of a bar magnet is required.

---

## 1. The Geoscientific Question

```{epigraph}
A compass needle in Seattle today points 15.5° east of true north.
In 1955 it pointed 22.1° east. The asphalt of Seattle-Tacoma's main runway
was repainted in 2019 to keep its name, "16R", honest.
```


A pilot lining up on runway 16R at Seattle-Tacoma International Airport is
flying along a heading numbered to match Earth's magnetic field. The number
"16" means the runway points along magnetic bearing 160°. That number has to
be repainted every decade or two, because the magnetic field at Seattle is
not static: its declination — the horizontal angle between magnetic north
and true (geographic) north — has decreased from about +22° in 1955 to about
+15.5° in 2026. KSEA's main runway was renamed from 16L/34R to 16R/34L in
2019 to keep up with this drift.

That a planetary-scale physical quantity changes fast enough to alter
aviation infrastructure is itself a clue to what the field is and what makes
it. Three observations frame this lecture:

1. The field has a dominantly **dipolar** geometry, with its axis tilted
   about 11° from the rotation axis (Figure {numref}`fig-dipole-geom`a).
2. The field has multiple **sources**, with very different spatial scales.
3. The field is recorded — imperfectly but persistently — in **rocks**,
   through the alignment of magnetic minerals during their geologic history.

The first two are observed at the surface today. The third is the bridge
that lets us read the field's history backward in time, and it is the
foundation of paleomagnetism and plate-tectonic reconstructions
(developed in Lecture 24).

## 2. The dipole field and the (D, I, F) system

Earth's surface magnetic field at most non-equatorial locations is, to first
order, the field of a centred magnetic dipole, tilted about 11° from the
rotation axis. The dipole accounts for roughly 90% of the surface field's
power. Field lines emerge from the magnetic south pole (in the geographic
southern hemisphere) and re-enter at the magnetic north pole
({numref}`fig-dipole-geom`a). By the historical convention, the "north"
pole of a compass needle is attracted to Earth's magnetic *north*, so the
geographic north magnetic pole is, in the language of bar magnets, a
*south* pole.

```{figure} ../assets/figures/fig_dipole_field_geometry.png
:name: fig-dipole-geom
:alt: Three-panel figure: (a) Earth shown in cross-section with the
 outer core highlighted as the geodynamo, dipole field lines emerging
 outward, the rotation axis vertical and the dipole axis tilted 11
 degrees; (b) Map view showing true north along the X axis and the
 horizontal magnetic-field component H rotated 15.5 degrees east of
 true north, illustrating declination D; (c) Side view showing the
 horizontal line of the ground, the down axis Z, the total-field
 vector F at inclination 68.9 degrees below horizontal, and its
 decomposition into horizontal H equal to F cos I and vertical Z
 equal to F sin I.

The geomagnetic field as seen from outside (a) and at a station (b, c).
**Panel (a)** shows the dipolar geometry of Earth's field in a meridional
section; the dipole axis is tilted about 11° from the rotation axis.
**Panel (b)** defines declination D as the angle between magnetic north
(the horizontal projection of the total field) and true (geographic) north.
**Panel (c)** defines inclination I as the angle of the total field below
horizontal; the total intensity F decomposes into a horizontal component
$H = F \cos I$ and a vertical (downward-positive) component $Z = F \sin I$.
Values for Seattle in 2026 (D = +15.5°, I = +68.9°, F = 52 900 nT) are
from the 13th-generation International Geomagnetic Reference Field
{cite}`alken2021igrf`.
```

At any surface station, the field is fully described by three numbers — the
**declination** $D$, the **inclination** $I$, and the **total intensity**
$F$ — or equivalently by the three components in a local Cartesian frame
with $X$ pointing to true north, $Y$ pointing east, and $Z$ pointing
*downward*:

$$
X = F \cos I \cos D, \quad
Y = F \cos I \sin D, \quad
Z = F \sin I.
$$ (eq-DIF-to-XYZ)

Here $D$ is positive when the horizontal component points east of true
north, and $I$ is positive when the field points into the ground (into the
lower hemisphere), as is the case throughout the northern hemisphere at
non-equatorial latitudes. The horizontal magnitude is $H = F \cos I$. The
units of $F$, $X$, $Y$, $Z$, and $H$ are nanoteslas (nT), with
$1\,\text{nT} = 10^{-9}\,\text{T}$. Typical surface values range from
about 25 000 nT near the magnetic equator to about 65 000 nT near the poles.

```{admonition} Worked example: Seattle 2026 station components
:class: note

For Seattle (47.65° N, 122.30° W) in 2026, the IGRF-13 model gives
D = +15.5°, I = +68.9°, F = 52 900 nT. Applying {eq}`eq-DIF-to-XYZ`:

- $X = 52900 \cdot \cos(68.9°)\cdot \cos(15.5°) = 18\,300$ nT  (toward true north)
- $Y = 52900 \cdot \cos(68.9°)\cdot \sin(15.5°) =  5\,070$ nT  (toward east)
- $Z = 52900 \cdot \sin(68.9°)               = 49\,360$ nT  (downward)

The horizontal component $H = F \cos I = 19\,000$ nT is small compared
with the vertical $Z = 49\,400$ nT: at Seattle's latitude, the field is
strongly inclined, and a compass needle, which responds only to the
horizontal component, is correspondingly weak.
```

## 3. Three sources, three wavelength regimes

The surface field is the sum of three contributions with very different
spatial scales:

- **The core field** (the *main field*) is generated by the
  *geodynamo* — turbulent convection of liquid iron in the outer core,
  about 2 900 km below the surface. The field that escapes the outer-
  core boundary and reaches the surface is filtered by depth: short
  spatial wavelengths attenuate strongly, so the surface core field
  is dominated by the lowest spherical-harmonic degrees, $n \leq 13$,
  corresponding to wavelengths longer than about 3 000 km.
- **The crustal (lithospheric) field** is a *static* contribution due to
  permanently magnetised rocks in the upper few tens of kilometres of the
  lithosphere. It is much weaker than the core field but has its power
  concentrated at shorter wavelengths, roughly $n \sim 16$ to $n \sim 100$
  (about 3 000 km down to 400 km).
- **The external (ionospheric and magnetospheric) field** is generated by
  currents flowing in the conducting ionosphere and the magnetosphere; it
  varies on timescales of seconds to days and has a broad spatial
  spectrum. It is what makes magnetic surveys harder than gravity surveys:
  the field measured at a station includes a slowly drifting external
  contribution that must be removed before the static (core + crust) signal
  can be interpreted.

The fingerprints of these three sources are visible in the
**Mauersberger–Lowes power spectrum** of the surface field
({numref}`fig-power-spectrum`), which plots the power per spherical-
harmonic degree $R_n$ against $n$. The steep drop-off from $n = 1$ to
$n \sim 13$ is the dipole-dominated core field. The plateau from
$n \sim 16$ outward is the crustal contribution. The faint floor at
$R_n \sim$ a few nT² is the ionospheric residual at the time of the
satellite mission used to build the model.

```{figure} ../assets/figures/fig_field_power_spectrum.png
:name: fig-power-spectrum
:alt: Log-log plot of magnetic-field power per spherical-harmonic degree
 R_n in units of nT-squared as a function of degree n from 1 to 110.
 A steeply decreasing solid blue line labelled "Core (geodynamo)" falls
 from about 10^10 nT-squared at n=1 to below 10^-1 at n=45. A dashed
 orange line labelled "Crust / lithosphere" rises from near zero at
 n=14 to a plateau of about 50 nT-squared between n=20 and n=60, then
 decays slowly. A dotted green horizontal line at about 4 nT-squared
 marks the ionospheric external floor. The grey total-observed curve
 follows the core line at low n and the crust line at high n. A grey
 shaded region between n=13 and n=16 is labelled "core-to-crust
 transition". The top axis shows the approximate horizontal wavelengths
 in km corresponding to selected n values.

Power spectrum of Earth's magnetic field at the surface. The three principal
sources occupy non-overlapping wavelength regimes — the core dominates
$n \leq 13$, the crust dominates $n \gtrsim 16$, and the ionosphere
contributes a roughly degree-independent floor. Reproduces the form of
Fig. 1 in {cite}`maus2008powerspectrum`.
```

This is why magnetic surveys at different scales sample different sources:
a satellite mission averaging over hundreds of kilometres sees the core
field; a continental-scale aeromagnetic compilation sees the lithosphere;
a high-resolution ground survey along a road traverse sees individual
crustal bodies whose horizontal sizes are tens to hundreds of metres.

## 4. The surface field changes — secular variation

The core field is generated by fluid motions whose characteristic timescales
are decades to millennia. It therefore *drifts*, and the drift —
**secular variation** — is recorded at every magnetic observatory on Earth.

The recent history at Seattle ({numref}`fig-seattle-sv`) tells the story
through three quantities: declination D dropped from about +22° in 1955 to
+15.5° in 2026; inclination I dropped from 71° to 68.9°; total intensity F
fell by about 3 000 nT over the same seven decades.

```{figure} ../assets/figures/fig_seattle_secular_variation.png
:name: fig-seattle-sv
:alt: Three stacked line plots sharing an x-axis from 1955 to 2026 in
 years. The top plot is declination in degrees east of north, dropping
 from +22.1 degrees in 1955 to +15.5 degrees in 2026 with the
 endpoints annotated. The middle plot is inclination in degrees,
 dropping from 71 degrees to 68.9 degrees. The bottom plot is total
 intensity F in nanoteslas, dropping from about 56 000 nT to 52 900 nT,
 with a double-headed arrow on the right side annotating
 "delta F is approximately 3080 nT".

Secular variation of declination D, inclination I, and total intensity F
at Seattle (47.65° N, 122.30° W) for 1955–2026, derived from the
IGRF/DGRF historical models {cite}`alken2021igrf`. The pace and direction
of the drift are reasonably stable on the seven-decade scale but vary
appreciably from one decade to the next, occasionally exhibiting an abrupt
**geomagnetic jerk** (a rapid change in $dB/dt$, on a timescale of months).
```

This drift means that two surface field-measurements made at the same
location decades apart constrain something about *core* dynamics — not
about the crust beneath the station. For lithospheric magnetic surveys
the implication is operational: every measurement is corrected to a
reference epoch (the current IGRF epoch) by subtracting the modelled
core-field value at the time of observation.

## 5. The mineral scale — five categories of magnetic ordering

The crustal-field contribution to the surface signal arises because some
minerals carry a *permanent* magnetisation set by their geologic history.
Whether a mineral can do so is determined by how the electron spins of its
atoms align — by the *magnetic ordering* in its crystal structure. There
are five categories ({numref}`fig-mineral-mag`):

1. **Diamagnetic** materials (e.g. quartz, halite) have no permanent
   atomic moments. In an applied field they develop a tiny induced
   moment *opposite* to the field (negative susceptibility,
   $k \approx -10^{-5}$). They contribute essentially nothing to crustal
   anomalies.
2. **Paramagnetic** minerals (e.g. olivine, pyroxene at room temperature)
   have permanent atomic moments but no spontaneous order: in zero field
   the moments point in random directions and the net magnetisation is
   zero. In an applied field the moments preferentially align with it,
   giving a small positive susceptibility, $k \approx +10^{-4}$.
3. **Ferromagnetic** materials have parallel spontaneous alignment of
   atomic moments via the *exchange interaction*, giving very large
   susceptibility, $k \gg 1$. Pure iron is ferromagnetic, but pure iron is
   rare in geology — the everyday ferromagnetic mineral in rocks is
   actually ferrimagnetic (see below).
4. **Antiferromagnetic** minerals (e.g. hematite, $\alpha$-Fe$_2$O$_3$, to
   first order) have antiparallel sublattices that cancel: the net moment
   is nearly zero. In hematite a small spin-canting in the basal plane
   produces a weak parasitic moment, but it is small.
5. **Ferrimagnetic** minerals (magnetite, Fe$_3$O$_4$, and the
   titanomagnetite series) have *unequal* antiparallel sublattices,
   so the cancellation is partial and a substantial net moment remains.
   Magnetite is the workhorse of rock magnetism: most natural remanence
   in basalt, dolerite, and many sediments is carried by magnetite or its
   titanium-substituted relatives.

```{figure} ../assets/figures/fig_mineral_magnetism.png
:name: fig-mineral-mag
:alt: Five side-by-side schematic panels showing crystal-lattice
 representations of the five magnetic-ordering categories. Each panel
 has a 5-by-4 grid of lattice sites. In the diamagnetic panel
 ("quartz, halite", k ≈ -10^-5) the sites are open circles with no
 arrows, labelled "no permanent moments". In the paramagnetic panel
 ("olivine, pyroxene", k ≈ +10^-4) sites have randomly oriented
 blue arrows, labelled "weak alignment in H". In the ferromagnetic
 panel ("iron (rare in nature)", k >> 1) all arrows are green and
 point up, labelled "all parallel". In the antiferromagnetic panel
 ("hematite", k ≈ 0) rows alternate up green arrows and down orange
 arrows, labelled "antiparallel, net = 0". In the ferrimagnetic
 panel ("magnetite", k > 1) rows alternate long up green arrows and
 short down orange arrows, labelled "unequal antiparallel, net ≠ 0".

The five categories of magnetic ordering at the mineral scale, with a
representative mineral, the order-of-magnitude volume susceptibility k,
and the alignment mechanism. Most natural rock remanence is carried by
ferrimagnetic minerals — primarily magnetite and the titanomagnetite
series. Adapted from {cite}`tauxe2018essentials`.
```

The *volume magnetic susceptibility* $k$ relates an induced magnetisation
$M$ (A m$^{-1}$) to the applied field $H$ (A m$^{-1}$) through

$$
\mathbf{M} = k \mathbf{H}.
$$ (eq-susc)

For magnetic surveys conducted in Earth's ambient field, $k$ is small
(typically $10^{-4}$ to $10^{-2}$ for crustal rocks, dominated by magnetite
content), and the induced magnetisation is approximately
$M_\text{ind} \approx k H_\text{earth}$. For magnetite-bearing volcanic
rocks of the Cascade arc, $k$ commonly falls in the range
$10^{-3}$ to $10^{-1}$ — wide enough to produce strong, mappable anomalies
above shallow plutons.

## 6. Temperature unlocks (and locks in) magnetisation

Ferro- and ferrimagnetic ordering depend on the exchange interaction
between neighbouring atomic moments. Above a critical temperature — the
**Curie temperature** $T_C$ — thermal agitation overwhelms the exchange
coupling and the spontaneous alignment is destroyed. The mineral becomes
paramagnetic.

For the four magnetic minerals most relevant in Pacific Northwest rocks:

- **Titanomagnetite (TM60)**, common in basalts of the Juan de Fuca plate:
  $T_C \approx 150\,°\text{C}$.
- **Pyrrhotite**, found in some hydrothermal ore deposits and
  metamorphosed sediments: $T_C \approx 320\,°\text{C}$.
- **Magnetite** (Fe$_3$O$_4$), the dominant remanence carrier in most
  continental rocks: $T_C \approx 580\,°\text{C}$.
- **Hematite** ($\alpha$-Fe$_2$O$_3$), the main carrier in red beds and
  some metamorphic rocks: $T_C \approx 680\,°\text{C}$ (though as an
  antiferromagnet, its remanence amplitude is much smaller than
  magnetite's).

When a magnetic mineral *cools* through $T_C$ in an external field, it
acquires a **thermoremanent magnetization** (TRM) parallel to that field.
The acquisition is not instantaneous: it happens in a narrow temperature
interval (the **blocking interval**) where the relaxation time of the
mineral grains crosses the experimental timescale and the spins, having
been free to fluctuate, become locked in place ({numref}`fig-trm-curie`).

```{figure} ../assets/figures/fig_trm_curie.png
:name: fig-trm-curie
:alt: Plot of normalised magnetisation versus temperature in degrees
 Celsius, from 0 to 720. A solid blue curve labelled Js(T)/Js(0) shows
 the saturation magnetisation falling from 1.0 at T=0 to 0 at T=580
 degrees C, with a Brillouin-like shape. A dashed orange curve labelled
 "Cumulative TRM in H_0 during cooling" stays near 1.0 from T=0 up to
 about T=520 degrees C, then drops steeply through an orange-shaded
 blocking interval (515 to 565 degrees C, labelled "blocking interval
 (TRM locked in)"), and reaches 0 at 580 degrees C. A vertical dotted
 line at 580 degrees C is labelled "Curie T = 580 degrees C (magnetite)".
 Three thin grey vertical lines along the bottom edge mark TM60
 (150 degrees C), pyrrhotite (320 degrees C), and hematite (680 degrees
 C). A leftward arrow at the top of the plot is labelled "cooling".

Thermoremanent magnetization acquired by a magnetite grain cooling through
its Curie temperature in a field $H_0$. The saturation magnetization
$J_s(T)$ drops to zero at $T_C \approx 580\,°\text{C}$; the cumulative
remanence acquired during slow cooling is locked in over a narrow
blocking interval just below $T_C$. Tick marks at 150 °C, 320 °C, and
680 °C indicate the Curie temperatures of titanomagnetite (TM60),
pyrrhotite, and hematite, respectively. Adapted from
{cite}`dunlop2001rockmagnetism` and {cite}`tauxe2018essentials`.
```

TRM is the dominant mechanism by which igneous rocks record the field at
the time of their last cooling. Two other mechanisms matter elsewhere:

- **Detrital remanent magnetization (DRM)** is acquired by sedimentary
  rocks when magnetic grains physically rotate to align with the ambient
  field as they settle from suspension, and are then locked in by
  subsequent compaction and lithification. DRM is weaker and noisier than
  TRM, but it is the only mechanism available to record the field during
  most of marine sedimentation.
- **Chemical remanent magnetization (CRM)** is acquired when a magnetic
  mineral *grows* below its Curie temperature, e.g. when hematite forms
  during diagenesis of red beds. CRM is locked in at the moment the
  growing grain crosses a critical size threshold, not at the Curie
  temperature.

Together, TRM in volcanics, DRM in marine sediments, and CRM in red beds
provide the three principal classes of paleomagnetic recorder, with very
different age resolutions and signal-to-noise properties.

## 7. The forward and inverse problems — paleo-latitude from inclination

For a *geocentric axial dipole* (GAD) — the simplest model of the
time-averaged field, in which the dipole axis is assumed to coincide with
the rotation axis — the inclination $I$ at geographic latitude $\lambda$
is

$$
\tan I = 2 \tan \lambda.
$$ (eq-gad)

The factor of 2 comes from the dipole field expression in polar
coordinates: at the surface, the radial component is twice as large as the
tangential component at any latitude. Equation {eq}`eq-gad` is the
**forward problem** of paleo-latitude: given a paleo-latitude $\lambda$
inferred from a plate reconstruction, predict the inclination that a
magnetic mineral would record on cooling at that latitude.

The **inverse problem** is more useful in practice. A basalt that
crystallised at unknown latitude carries a TRM whose inclination can be
measured in the lab. Inverting {eq}`eq-gad`:

$$
\lambda = \arctan\!\left(\frac{\tan I}{2}\right).
$$ (eq-gad-inverse)

```{figure} ../assets/figures/fig_paleolatitude_from_inclination.png
:name: fig-paleolatitude
:alt: Two side-by-side plots. The left panel "Forward I from lambda"
 plots inclination I in degrees on the y axis from 0 to 90 against
 paleo-latitude lambda in degrees on the x axis from 0 to 90. The
 curve tan I = 2 tan lambda passes through the origin and reaches I
 = 90 degrees at lambda = 90 degrees, with circle markers labelled
 "equator: I = 0 degrees", "30 degrees N: I = 49 degrees", "Seattle
 (47.65 degrees): I = 65 degrees" (note: GAD prediction, not modern
 measured value), and "pole: I = 90 degrees". The right panel
 "Inverse lambda from I (with sigma_I = 2 degrees)" plots inferred
 paleo-latitude lambda against measured inclination I, both in
 degrees from 0 to 90. The curve lambda = arctan(tan I divided by 2)
 is plotted in blue with a light-blue shaded uncertainty band that
 is widest near the equator and narrowest near the pole. Annotations
 indicate "largest sigma_lambda near equator" near (10, 5) and
 "smallest sigma_lambda near pole" near (82, 76).

(a) Forward problem: inclination predicted from paleo-latitude using the
geocentric axial dipole equation. (b) Inverse problem: paleo-latitude
recovered from a measured inclination, with the $\pm 1\sigma_\lambda$
uncertainty band that results from a $\sigma_I = 2°$ measurement error
propagated through {eq}`eq-gad-inverse`. The error is largest near the
equator and shrinks toward the pole — a consequence of the slope of the
forward curve.
```

Uncertainty propagation through {eq}`eq-gad-inverse` is direct:
differentiating gives

$$
\frac{d\lambda}{dI}
= \frac{1}{2}\,\frac{\sec^2 I}{1 + \tfrac{1}{4}\tan^2 I},
$$

so $\sigma_\lambda \approx (d\lambda/dI)\,\sigma_I$ to first order. The
slope $d\lambda/dI$ is large near $I = 0$ (equator) and small near
$I = 90°$ (pole): a $\pm 2°$ measurement error in inclination becomes
roughly $\pm 1°$ in paleo-latitude at the pole but $\pm 4°$ at the
equator. Inverting a paleo-magnetic inclination is more reliable at high
paleo-latitudes than at low ones.

```{admonition} Limits of the GAD assumption
:class: warning

Equation {eq}`eq-gad` is exact only for a perfect dipole. The actual surface
field deviates from a centred axial dipole both because the dipole axis
itself is tilted (the 11° tilt visible in {numref}`fig-dipole-geom`a) and
because higher-degree harmonics contribute about 10% of the surface power.

These deviations average out over time: when many lava flows spanning
$\gtrsim 10\,000$ years are averaged at the same site, the mean inclination
matches the GAD prediction to within a few degrees. But a single lava flow
records a *snapshot* that may deviate by 5–10°. Paleomagnetic latitudes are
therefore reliable only when based on many independent samples covering
enough geologic time to average over secular variation. Lecture 24 returns
to this issue when reconstructing plate motions from oceanic stripes.
```

## 8. Research horizon — the Swarm satellites and geomagnetic jerks

The IGRF is built every five years from observatory data and from
*satellite* measurements that map the field globally to spherical-harmonic
degrees $n \lesssim 130$ {cite}`alken2021igrf`. The currently flying
satellite constellation is **Swarm**, a three-spacecraft ESA mission
launched in 2013 (operating beyond its design lifetime). Swarm measures
the vector field at 460 km altitude with sub-nT precision, which is good
enough to:

1. Track **westward drift** of the magnetic equator at a rate of about
   0.2° per year — a signature of azimuthal flow at the top of the outer
   core, consistent with hydrodynamic models of the geodynamo.
2. Detect **geomagnetic jerks** — abrupt, year-scale changes in the
   rate of secular variation — which appear to originate in the
   bulk of the outer core but whose physical mechanism is debated.
3. Image the **lithospheric field** at degree $n \sim 130$, exposing
   features such as oceanic-spreading fabrics, large impact structures
   (e.g. Vredefort, Sudbury), and continental-margin gradient zones.

The geophysical question driving this work — "What is happening in the
outer core *right now*?" — is central to long-range climate-grade
geomagnetic reference models for civil aviation, satellite navigation,
and military operations, and to ongoing efforts to understand whether
the present declining dipole moment foreshadows a polarity reversal on
the geologic timescale. (It probably does not, but the question is
open.)

## 9. AI literacy — using a language model as a derivation partner

Equation {eq}`eq-gad` is one of the cleanest examples of a single-formula
forward problem in geophysics. It is also short enough that a competent
large language model (LLM) can be asked to *derive* it from the standard
expression for the field of a magnetic dipole in polar coordinates. This is
a useful test of the model's mathematical reasoning, and of the student's
ability to check the result.

```{admonition} Reasoning Partner activity
:class: tip

**Step 1 — Ask the LLM to derive equation {eq}`eq-gad`.** Prompt: "Starting
from the magnetic dipole field $B_r = (2m\cos\theta) / r^3$,
$B_\theta = (m\sin\theta) / r^3$ in spherical polar coordinates with
$\theta$ measured from the dipole axis, derive the relation between the
inclination of the surface field and the magnetic colatitude. Show each
step."

**Step 2 — Verify, do not trust.** Three checks the student must perform:

1. Does the LLM correctly identify that *inclination* is the angle of the
   total field below horizontal, not below vertical? (A common mistake.)
2. Does the algebra go through cleanly, or does the LLM drop a factor of 2?
3. Is the final formula written in terms of *colatitude* (the angle from
   the pole) or *latitude* (the angle from the equator)? The two differ
   by $\pi/2$ and the difference matters: equation {eq}`eq-gad` is
   $\tan I = 2 \tan\lambda$ with $\lambda$ = latitude, but it becomes
   $\tan I = 2 \cot\theta$ if $\theta$ = colatitude.

**Step 3 — Disagree productively.** If the LLM's derivation has an error,
write a one-sentence prompt that identifies the specific step and asks for
a correction. Do *not* simply ask "is this right?" — that elicits agreement
regardless of the actual answer. Effective prompts name the line or step
that is in question.

The student deliverable is a one-page record showing: (i) the LLM's
derivation, (ii) at least one identified error or unclear step, and
(iii) the corrected derivation in the student's own notation, signed.
```

## 10. Concept check

```{admonition} Concept-check questions
:class: tip

1. **D, I, F at Seattle in 1955.** Given the 1955 IGRF values
   D = +22.1°, I = +71.0°, F = 55 980 nT, compute the local components
   (X, Y, Z) at Seattle. Compare with the 2026 values quoted in §2.
   Which component has changed the most in *relative* terms? Which has
   changed the most in *absolute* (nT) terms?

2. **Curie temperature and lava flow age.** A basalt sample carries a
   stable remanence whose direction is consistent across the entire flow
   thickness. The flow is known to have erupted at 1 200 °C and cooled
   over a few weeks. Which mineral or minerals could be carrying the
   remanence? Could any of magnetite, titanomagnetite TM60, hematite, or
   pyrrhotite be ruled out solely from the cooling history?

3. **Paleo-latitude error budget.** A paleomagnetic study of a 50-Myr-old
   basalt yields a site-mean inclination of $I = 35°\pm 3°$. Compute the
   inferred paleo-latitude and its $1\sigma$ uncertainty using
   {eq}`eq-gad-inverse`. The same study finds $I = 75°\pm 3°$ at a second
   site. Compare the two paleo-latitude uncertainties. Explain in one
   sentence why one is larger than the other.
```

```{admonition} Concept-check answers
:class: hint, dropdown

*Answers and worked solutions are provided in the instructor materials
(see `concept_check_lecture23.md` in the `ess314-instructor` repository).*
```

## 11. Looking ahead

Lecture 24 takes the surface-field framework of this lecture and turns it
into a tool for *imaging the subsurface*. The same dipole equations that
describe Earth's field also describe — to within a constant of
proportionality — the local field of a magnetised body buried in the crust.
The result is the magnetic *anomaly*: a small perturbation, of order
$10^{-3}$ of the ambient field, that betrays the presence and shape of
buried bodies and, by virtue of plate tectonics, encodes the age structure
of the entire ocean floor.

## 12. Further reading

```{bibliography}
:filter: docname in docnames

alken2021igrf
maus2008powerspectrum
tauxe2018essentials
dunlop2001rockmagnetism
butler1992paleomagnetism
lowrie2020fundamentals
```

::::{grid} 1 1 2 2

:::{grid-item-card} Companion notebook (next step)
The accompanying Jupyter notebook **`magnetics_forward.ipynb`** (in the
course `notebooks/` directory, scheduled for release with Lab 6) implements
the GAD equation, the (D, I, F) ↔ (X, Y, Z) transformation, and an IGRF-13
field calculator that students will use in the discussion section.
:::

:::{grid-item-card} Open data and tools
- **NOAA Geomagnetism Calculator**: <https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml> — IGRF/WMM field model lookup at any point.
- **MagIC database**: <https://earthref.org/MagIC/> — open paleomagnetic data.
- **PmagPy**: <https://github.com/PmagPy/PmagPy> — open paleomagnetism Python tools.
:::

::::
