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
  - "Hunt, Moskowitz & Banerjee (1995), Magnetic Properties of Rocks and Minerals, AGU Reference Shelf 3 (Wiley)"
  - "IGRF-13 model and field calculator: NOAA NCEI / IAGA (public domain, https://www.ngdc.noaa.gov/IAGA/vmod/igrf.html)"
keywords: [geomagnetism, geodynamo, declination, inclination, IGRF, paleomagnetism, magnetite, Curie temperature, TRM, DRM, CRM, secular variation, Königsberger ratio]
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
- **[LO-23.2]** Identify the three principal sources of the surface field — core (geodynamo), lithosphere, and ionosphere — locate them in their physical context, and assign each source a characteristic spatial wavelength range.
- **[LO-23.3]** Distinguish between *induced* and *remanent* magnetisation in rocks, relate the bulk magnetic response of a rock to its mineral assemblage via the Königsberger ratio $Q$, and identify the five categories of magnetic ordering at the mineral scale (dia-, para-, ferro-, antiferro-, ferrimagnetic).
- **[LO-23.4]** Describe the three principal mechanisms by which rocks acquire a remanent magnetisation — thermoremanent (TRM), detrital (DRM), and chemical (CRM) — and identify the Curie temperatures of the magnetic minerals encountered in Pacific Northwest rocks (magnetite, titanomagnetite, hematite, pyrrhotite).
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
2. The field has multiple **sources**, with very different spatial scales
   and very different physical mechanisms.
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

## 3. Three Sources of Magnetism

The dipole geometry of §2 is the *shape* of the field seen at the surface.
Where the field actually *comes from* is a different question, and the
answer is that the surface field is the sum of three contributions
produced by three different physical processes occurring at three
different depths inside and above the Earth.

{numref}`fig-three-sources` locates these sources in their physical
context. The **core field** is generated thousands of kilometres below
the surface by fluid motion in the outer core. The **lithospheric
field** is a static remnant of magnetisation locked into rocks within
the top ~30 km of the crust. The **ionospheric and magnetospheric
field** is produced by electrical currents flowing in the conducting
upper atmosphere, hundreds of kilometres above the surface. All three
contribute to what a magnetometer measures at ground level, and the
practical task of any magnetic survey is to separate them.

```{figure} ../assets/figures/fig_three_sources_cross_section.png
:name: fig-three-sources
:alt: A half-Earth cross-section showing the three principal sources
 of the geomagnetic field in their physical context. The deep interior
 is shown with a small bright orange inner core, a yellow-orange outer
 core containing curved arrows that represent turbulent convection
 (the geodynamo), a brown mantle, and a thin bold blue band at the
 top representing the magnetised lithosphere with small white arrows
 indicating remanent magnetisation directions that vary in
 orientation. Above the surface a pale blue band represents the
 ionosphere, marked with curved horizontal arrows that depict electric
 currents flowing in the conducting upper atmosphere. Dashed grey
 curves on the right side trace dipole field lines emerging from the
 Earth. Three labelled callout boxes identify Source 1 (Core,
 geodynamo) with its depth range 2900 to 5150 km and wavelengths
 longer than 3000 km, Source 2 (Lithosphere, crust) in the upper 30
 km with wavelengths from 400 to 3000 km, and Source 3 (Ionosphere or
 magnetosphere) at 80 to 500 km altitude with a broad spectrum that
 is time-varying on timescales of seconds to days. A label at the top
 reads "Surface field equals sum of all three sources."
:width: 100%

The three sources of Earth's magnetic field located in their physical
context. **Source 1 — the core (geodynamo)** lies between 2 900 km and
5 150 km depth, where turbulent convection of liquid iron generates
the *main field*. **Source 2 — the magnetised lithosphere** lies in
the upper ~30 km of the crust, where rocks carrying a remanent
magnetisation from their geologic past contribute a static, spatially
heterogeneous signal. **Source 3 — the ionosphere and magnetosphere**
sit above the surface (~80–500 km altitude), where currents flowing
in the conducting upper atmosphere produce a time-varying contribution.
The surface field measured at any station is the *sum* of all three.
```

### 3.1 Source 1 — The core (geodynamo)

The dominant source of the surface field is the **geodynamo**:
self-sustaining turbulent convection of electrically conducting liquid
iron in the outer core, between approximately 2 900 km and 5 150 km
depth. Heat escaping from the inner core and chemical buoyancy from
the freezing-out of light elements at the inner-core boundary drive
this flow, and the rotating, conducting fluid generates a magnetic
field through the **magnetohydrodynamic dynamo** mechanism (analogous
to, but vastly more complex than, the disc dynamo in an introductory
physics textbook).

The field that emerges from the core-mantle boundary is filtered by
depth on its way to the surface: short spatial wavelengths attenuate
strongly, so the surface signature of the geodynamo is dominated by
**long-wavelength** structure (wavelengths $\gtrsim 3\,000$ km, or
spherical-harmonic degree $n \leq 13$). This long-wavelength character
is why the dipole approximation works so well at the surface: short
wavelengths simply do not survive the propagation from $r = 3\,480$ km
out to $r = 6\,371$ km. The core field also *drifts* on decadal
timescales — the topic of §4.

### 3.2 Source 2 — The lithosphere (crust)

The second source is the **magnetised lithosphere**: rocks in the
upper ~30 km of the crust carrying a *permanent* magnetisation
locked in during their cooling, sedimentation, or chemical history.
This source is much weaker than the core field on absolute scale —
contributing typically 10–100 nT to the surface measurement against
a core background of order 30 000–60 000 nT — but it has its power
concentrated at **shorter wavelengths** ($n \sim 16$ to $n \sim 100$,
or wavelengths from about 3 000 km down to 400 km), where the core
field has fallen off. The lithospheric field is *static* on human
timescales: the rocks carrying it cool and re-magnetise only on
geological timescales.

The physical mechanism by which crustal rocks acquire and carry a
permanent magnetisation is the subject of §5 and §6. For now it is
enough to note that the lithospheric field is the geophysical
*signal* that magnetic surveys of the crust seek to map: the part of
the surface measurement that carries information about the rocks
beneath the station.

### 3.3 Source 3 — The ionosphere and magnetosphere

The third source is the **time-varying external field** produced by
electrical currents flowing in the conducting upper atmosphere — the
**ionosphere** (the E and F regions, roughly 80–500 km altitude) and
the **magnetosphere** beyond it. These currents are driven by solar
ultraviolet ionisation (the *Sq* — solar quiet — daily variation) and
by the interaction of the solar wind with Earth's magnetic field
(geomagnetic storms, substorms, magnetospheric ring currents). The
ionospheric contribution varies on timescales from seconds to days and
has a broad spatial spectrum.

This third source is what makes magnetic surveys operationally harder
than gravity surveys. The gravity field at a station is essentially
static; the magnetic field is not. Every measurement made at a moving
platform (a ship, an aircraft, a satellite) includes a slowly drifting
external contribution that must be removed by reference to a fixed
**base station** before the static (core + crust) signal can be
interpreted. Discussion section 7 takes up this base-station correction
in practice.

### 3.4 The spectral fingerprint — separating the three sources

The three sources occupy different spatial wavelength regimes, and
they leave a distinct fingerprint on the field's power spectrum. The
**Mauersberger–Lowes spectrum** ({numref}`fig-power-spectrum`) plots
the power per spherical-harmonic degree $R_n$ against $n$. The steep
drop-off from $n = 1$ to $n \sim 13$ is the dipole-dominated core
field. The plateau from $n \sim 16$ outward is the crustal
contribution. The faint floor at $R_n \sim$ a few nT² is the
ionospheric residual at the time of the satellite mission used to
build the model.

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

This separation in wavelength is what allows magnetic surveys at
different scales to *target* different sources. A satellite mission
averaging over hundreds of kilometres samples the core field. A
continental-scale aeromagnetic compilation isolates the lithosphere. A
high-resolution ground survey along a road traverse resolves
individual crustal bodies whose horizontal sizes are tens to hundreds
of metres. The choice of survey scale is, in effect, a choice of which
source to keep and which to filter out.

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

## 5. The mineral scale — why some rocks "remember" the field and others do not

The lithospheric contribution to the surface signal arises because some
crustal rocks carry a permanent magnetisation, and some do not. Whether
a particular rock contributes a measurable signal — and whether that
signal records geological history or just the present-day surveying
field — depends on the **mineral assemblage** of the rock.

### 5.1 A rock is an ensemble of minerals

No single mineral makes up an entire rock. Even a "magnetite-rich"
basalt is mostly plagioclase, clinopyroxene, and olivine, with magnetite
present as a few volume percent of the total. The bulk magnetic
response of a rock is therefore a **weighted average** over its mineral
assemblage: each mineral contributes according to its volume fraction
and its own magnetic character.

{numref}`fig-rock-ensemble` shows four common rock types as schematic
hand-sample views, each with its dominant magnetic carrier, its typical
bulk volume susceptibility $k$, its Königsberger ratio $Q$ (defined
below), and where the rock is encountered in Pacific Northwest geology.

```{figure} ../assets/figures/fig_rock_as_ensemble.png
:name: fig-rock-ensemble
:alt: Four side-by-side schematic hand-sample panels showing the
 mineral makeup of four common rock types. The basalt panel is
 dominated by grey-blue plagioclase ellipses and dark clinopyroxene,
 with blue olivine polygons and scattered bright orange dots
 representing magnetite grains; labelled "bulk susceptibility k
 approximately 10^-3 to 10^-1 SI" and "Königsberger ratio Q
 approximately 0.5 to 10". The granite panel is dominated by light
 tan K-feldspar and off-white plagioclase ellipses with grey quartz
 polygons and a few blue biotite polygons and trace orange magnetite
 dots; labelled "k approximately 10^-5 to 10^-3 SI" and "Q
 approximately 0.1 to 1". The red bed sandstone panel is dominated
 by tan hematite-coated quartz with orange iron-oxide cement and
 dark red hematite dots; labelled "k approximately 10^-5 to 10^-4
 SI" and "Q approximately 1 to 100". The marine mudstone panel is
 dominated by dark grey clay matrix with smaller blue paramagnetic
 grains and small orange detrital magnetite dots; labelled "k
 approximately 10^-5 to 10^-3 SI" and "Q approximately 0.1 to 2".
 A shared legend at the bottom identifies four colour categories:
 ferrimagnetic (magnetite, vermilion) carries remanence,
 antiferromagnetic (hematite, dark red) weak remanence, paramagnetic
 (blue, olivine, biotite, pyroxene) induced only, and diamagnetic
 (grey, quartz, feldspar) non-magnetic matrix.
:width: 100%

Four common rock types shown as ensembles of minerals. **Basalt** —
mafic, magnetite-rich — has high bulk susceptibility and a Königsberger
ratio of order unity to ten, dominated by the ferrimagnetic minerals
magnetite and titanomagnetite (the Juan de Fuca seafloor and the
Columbia River Basalt Group are PNW examples). **Granite** — felsic,
with only trace magnetite — has much lower susceptibility, dominated
by induced rather than remanent magnetisation (Cascade arc plutons,
Idaho Batholith). **Red bed sandstone** — characterised by hematite
cement and grain coatings — has low overall susceptibility but a high
Königsberger ratio, because the hematite carries a strong *chemical*
remanence (Triassic red beds, arid-margin Cordilleran sediments).
**Marine mudstone** — a fine-grained clay matrix with disseminated
detrital magnetite — has variable susceptibility and weak-to-moderate
remanence (Olympic Peninsula accretionary wedge sediments). Susceptibility
ranges from {cite}`hunt1995magprops`.
```

### 5.2 Two regimes — induced versus remanent magnetisation

Within this ensemble, every mineral contributes magnetic moment in one
of two physically distinct ways. The distinction is the central
organising idea of crustal magnetism.

In the **induced regime**, the mineral has no intrinsic magnetic moment
when isolated from any external field, but in the presence of an
applied field $\mathbf{H}$ it develops a magnetisation proportional to
that field:

$$
\mathbf{M}_\text{ind} = k \, \mathbf{H}.
$$ (eq-susc)

The proportionality constant $k$ is the **volume magnetic susceptibility**
(dimensionless in SI units). Diamagnetic minerals have small *negative*
$k$ ($\approx -10^{-5}$); paramagnetic minerals have small *positive*
$k$ ($\approx 10^{-4}$). The defining feature of the induced regime is
that the magnetisation **vanishes when the applied field is removed**.
A diamagnetic or paramagnetic mineral has no memory of past fields.

In the **remanent regime**, by contrast, the mineral carries a
magnetisation locked in by its history — a *permanent* moment that
persists when the applied field is removed. Remanent magnetisation is
the property that makes magnetic minerals into recorders of the
ancient field. Ferrimagnetic minerals (magnetite, titanomagnetite) and,
to a lesser extent, antiferromagnetic minerals with parasitic moments
(hematite) sit in this regime.

{numref}`fig-induced-remanent` shows the two regimes side by side as
$M$-versus-$H$ curves.

```{figure} ../assets/figures/fig_induced_vs_remanent.png
:name: fig-induced-remanent
:alt: Two-panel plot of magnetisation M versus applied field H. The
 left panel "Induced-only regime, M equals kH, vanishes when H equals
 zero" shows two straight lines crossing at the origin: a grey line
 with negative slope labelled "Diamagnetic (quartz, halite), k less
 than zero" and a blue line with small positive slope labelled
 "Paramagnetic (olivine, biotite), k greater than zero, small". A
 black dot marks the origin with an annotation "Turn H off, M equals
 zero for both". The right panel "Remanent regime, ferri-slash-ferro
 magnetic, hysteresis, M not equal to zero at H equals zero" shows
 a closed hysteresis loop drawn in vermilion: a solid sweep-up branch
 and a dashed sweep-down branch. Two saturation levels plus and
 minus M sub s are marked by horizontal dotted lines. A black dot
 at the intersection of the upper branch with H equals zero is
 annotated "M sub r (remanence) equals 0.72 M sub s"; a second black
 dot at the intersection of the lower branch with M equals zero is
 annotated "H sub c (coercivity) equals 0.25". A grey caption strip
 at the bottom reads "Königsberger ratio Q equals magnitude of M sub
 r divided by magnitude of M sub ind measures which regime dominates
 the rock's bulk response."
:width: 100%

The two regimes of crustal magnetism, shown as magnetisation $M$ versus
applied field $H$. **Induced regime (left):** diamagnetic and paramagnetic
materials produce a magnetisation linear in $H$ that vanishes at $H = 0$.
They have no memory of past fields. **Remanent regime (right):**
ferri- and ferromagnetic materials trace a *hysteresis loop*. At
$H = 0$ on the upper branch, the magnetisation has a non-zero value
$M_r$ — the **remanence**. To return $M$ to zero requires reversing
the field to a finite **coercive field** $H_c$. The Königsberger ratio
$Q = |M_r| / |M_\text{ind}|$ summarises which regime dominates the
bulk response of a real rock in Earth's ambient field. After {cite}`tauxe2018essentials`.
```

The single most useful number for characterising a rock's magnetic
behaviour in a field survey is the **Königsberger ratio**:

$$
Q = \frac{|\mathbf{M}_\text{rem}|}{|\mathbf{M}_\text{ind}|}.
$$ (eq-Q)

Here $\mathbf{M}_\text{rem}$ is the rock's natural remanent
magnetisation (NRM) and $\mathbf{M}_\text{ind}$ is the magnetisation
that the rock acquires by induction in Earth's ambient field. When
$Q \ll 1$ the rock responds primarily by induction, and its magnetic
signature points along Earth's *present-day* field. When $Q \gg 1$ the
rock's signal is dominated by its *remanent* moment, which points
along the field that prevailed when the rock formed — possibly tens
or hundreds of millions of years ago. The latter case is what makes
oceanic crust into a recorder of plate motion (Lecture 24).

### 5.3 Five categories of magnetic ordering at the mineral scale

The two regimes of §5.2 are emergent properties of how electron spins
align inside the crystal lattice of each mineral. The classification of
this **magnetic ordering** has five members, and it determines which
regime a given mineral falls into.

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
representative mineral and the order-of-magnitude single-mineral
susceptibility $k$. Diamagnetic and paramagnetic minerals fall in the
induced regime (no remanence). Ferromagnetic, antiferromagnetic with
spin canting, and ferrimagnetic minerals can fall in the remanent regime
(they carry their own magnetisation locked in by history). Adapted from
{cite}`tauxe2018essentials`.
```

1. **Diamagnetic** minerals (quartz, halite, calcite) have no permanent
   atomic moments. In an applied field they develop a tiny induced
   moment *opposite* to the field, with susceptibility $k \approx -10^{-5}$.
   They are *induced-only* and contribute essentially nothing to
   crustal anomalies. Most of the volume of common sedimentary rocks
   and felsic plutons is diamagnetic.

2. **Paramagnetic** minerals (olivine, pyroxene, biotite at room
   temperature) have permanent atomic moments but no spontaneous order:
   in zero field the moments point in random directions and the net
   magnetisation is zero. In an applied field the moments preferentially
   align with it, giving a small positive susceptibility,
   $k \approx +10^{-4}$. Paramagnetic minerals are also *induced-only*.
   They dominate the volume of fresh basalt, dolerite, and many mantle
   xenoliths, but their contribution to the surface anomaly is small
   compared with the much rarer ferrimagnetic accessory minerals.

3. **Ferromagnetic** minerals have parallel spontaneous alignment of
   atomic moments via the *exchange interaction*, giving very large
   susceptibility, $k \gg 1$ for the pure mineral. Pure iron is
   ferromagnetic, but pure iron is exceedingly rare in geology — it
   occurs only in some meteorites and at the inner core. The everyday
   "ferromagnetic" mineral in rocks is, strictly, *ferrimagnetic* (see
   below). Ferromagnets fall in the **remanent regime**.

4. **Antiferromagnetic** minerals (hematite, $\alpha$-Fe$_2$O$_3$, in
   first approximation; ilmenite; goethite) have antiparallel
   sublattices that cancel: the *first-order* net moment is zero. In
   hematite a small spin-canting in the basal plane produces a weak
   *parasitic* remanence that is much smaller than magnetite's but
   nevertheless non-zero. This weak remanence is what records the
   field in red beds — see §6.

5. **Ferrimagnetic** minerals (magnetite, Fe$_3$O$_4$, and the
   titanomagnetite series) have *unequal* antiparallel sublattices,
   so the cancellation is partial and a substantial net moment remains.
   Magnetite is the workhorse of rock magnetism: most natural remanence
   in basalt, dolerite, and many sediments is carried by magnetite or
   its titanium-substituted relatives.

The mapping from ordering category to regime is therefore:

| Ordering | Single-mineral $k$ | Regime | Carries remanence? |
|---|---|---|---|
| Diamagnetic | $-10^{-5}$ (negative) | Induced | No |
| Paramagnetic | $+10^{-4}$ | Induced | No |
| Ferromagnetic | $\gg 1$ | Remanent | Yes |
| Antiferromagnetic | $\approx 0$ | Remanent (weak parasitic) | Yes (weak) |
| Ferrimagnetic | $\gg 1$ | Remanent | Yes (strong) |

```{admonition} Pacific Northwest mineral inventory
:class: note

The minerals carrying the great majority of the remanent signal in
Pacific Northwest rocks are:

- **Magnetite and titanomagnetite (TM60, TM30, …)** — in basalts of
  the Juan de Fuca plate, the Columbia River Basalt Group, and arc
  volcanics of the Cascade Range. The dominant remanence carrier in
  almost every igneous rock in the region.
- **Hematite** — in Mesozoic red bed sandstones, in oxidised tops of
  basalt flows (the "weathered horizon" between successive Columbia
  River flows), and in some metamorphic rocks.
- **Pyrrhotite** — in some Cascade hydrothermal ore deposits and in
  metamorphosed sedimentary horizons.
- **Detrital magnetite** — disseminated through the marine sediments
  of the Cascadia accretionary wedge (Olympic Peninsula) and through
  Puget Sound glaciolacustrine deposits.

Granitic plutons of the Cascade arc and Idaho Batholith carry only
trace magnetite and contribute primarily through *induced*
magnetisation. This is why the geophysical contrast between a magnetite-bearing
intrusion and its surrounding granite host is often visible as a
positive magnetic anomaly at the surface, even when the gravity
contrast is small.
```

## 6. Remanent magnetisation — how rocks remember the field

The lithospheric signal of §3.2 exists because a *subset* of crustal
minerals carries a permanent magnetisation, and §5 established which
minerals — the ferri-, ferro-, and (weakly) antiferromagnetic ones.
This section turns to the *mechanism* by which those minerals acquire
their remanence in the first place.

A magnetic mineral can be locked into a particular magnetisation
direction by any process that brings the mineral through a critical
condition under which its electron spins lose the freedom to
fluctuate. There are three such processes, each tied to a distinct
geological setting, and together they form the three pillars of
paleomagnetism.

### 6.1 Thermoremanent magnetisation (TRM) — cooling through the Curie temperature

The simplest, strongest, and best-understood remanence is
**thermoremanent magnetisation (TRM)**, acquired when a magnetic
mineral *cools* through a critical temperature in an ambient field.

Ferri- and ferromagnetic ordering depends on the exchange interaction
between neighbouring atomic moments. Above a critical temperature — the
**Curie temperature** $T_C$ — thermal agitation overwhelms the exchange
coupling, the spontaneous alignment is destroyed, and the mineral
becomes paramagnetic. Below $T_C$, ordering returns: as the grain
cools further, the spins lock progressively into an alignment with the
prevailing ambient field. This progressive locking happens in a
narrow **blocking interval** just below $T_C$, where the *relaxation
time* of the grain crosses the experimental timescale and what was a
fluctuating moment becomes a permanent one.

The four magnetic minerals most relevant in Pacific Northwest rocks
have well-separated Curie temperatures:

| Mineral | $T_C$ (°C) | Where it occurs |
|---|---|---|
| Titanomagnetite (TM60) | 150 | Basalts of the Juan de Fuca plate |
| Pyrrhotite | 320 | Hydrothermal ore deposits; metasediments |
| Magnetite (Fe$_3$O$_4$) | 580 | Most continental igneous rocks |
| Hematite ($\alpha$-Fe$_2$O$_3$) | 680 | Red beds; oxidised basalt tops |

These spread of Curie temperatures is exploited in laboratory
**stepwise thermal demagnetisation**: heating a rock sample to
progressively higher temperatures and measuring the surviving moment
at each step removes the carriers in order, separating multiple
components of remanence by the temperature at which each unblocks.

{numref}`fig-trm-curie` shows the temperature dependence of a single
magnetite grain's magnetisation and the cumulative TRM it acquires
during slow cooling in a field. The plot is drawn with the temperature
axis *reversed* so that the physical process of cooling reads from
left to right, matching the natural narrative.

```{admonition} What does "normalised magnetisation" mean?
:class: tip

Both curves in {numref}`fig-trm-curie` plot magnetisation *divided by*
the low-temperature saturation value $J_s(0)$. This division — the
*normalisation* — has two purposes. First, the absolute magnetic moment
of a grain depends on its volume and composition, which are not
universal; normalising by $J_s(0)$ makes the y-axis run from 0 to 1
for every ferri- or ferromagnetic mineral, regardless of grain size or
absolute moment. Second, it isolates the *temperature dependence* of
the magnetisation from its absolute amplitude: the curve $J_s(T)/J_s(0)$
is a property of the *mineral*, not of the *sample*. Different minerals
can therefore be compared on a common axis without worrying about
which one has the bigger absolute moment.
```

```{figure} ../assets/figures/fig_trm_curie.png
:name: fig-trm-curie
:alt: Plot of normalised magnetisation versus temperature in degrees
 Celsius. The x-axis is reversed so that temperature decreases from
 left (about 720 degrees C) to right (zero degrees C), with a thick
 black arrow at the top labelled "cooling" pointing rightward. The
 y-axis is normalised magnetisation J divided by J sub s at zero
 kelvin, dimensionless, running from zero to about 1.2. A solid blue
 curve labelled "J sub s of T divided by J sub s of zero, spontaneous
 magnetisation of magnetite" rises from zero at T equals 580 degrees
 C (drawn on the left of the plot because of the reversed axis) up
 to a value of 1 as T approaches zero on the right. A dashed orange
 curve labelled "cumulative TRM acquired during cooling in H sub
 zero" stays at zero from high temperature down through 580 degrees
 C, rises steeply through an orange-shaded blocking interval between
 about 565 and 515 degrees C (labelled "blocking interval, TRM locked
 in here"), and plateaus at 1 for lower temperatures. A blue dotted
 vertical line at 580 degrees C carries a small box labelled "T sub
 C equals 580 degrees C, magnetite". A grey annotation box near the
 top reads "Other Curie temperatures in PNW rocks: TM60 (basalt
 seafloor) 150 degrees C, pyrrhotite (ore deposits) 320 degrees C,
 hematite (red beds) 680 degrees C; dotted vertical lines show their
 positions". A second grey annotation box at the lower right
 explains the meaning of normalised magnetisation. The x-axis label
 reads "Temperature T in degrees C, high T on the left, low T on
 the right".
:width: 100%

Acquisition of thermoremanent magnetisation by a magnetite grain
cooling through its Curie temperature in an ambient field $H_0$. The
temperature axis is reversed so that **cooling reads left to right**.
The solid blue curve is the spontaneous magnetisation $J_s(T)/J_s(0)$;
it rises from zero at $T_C = 580$ °C to its full saturation value as
the grain cools toward room temperature. The dashed orange curve is
the *cumulative* TRM acquired during cooling: zero above $T_C$, then
locked in across the narrow blocking interval (shaded orange) just
below $T_C$, and plateauing at its low-temperature value thereafter.
Dotted vertical lines mark the Curie temperatures of the other
PNW-relevant magnetic minerals (TM60, pyrrhotite, hematite). Adapted
from {cite}`dunlop2001rockmagnetism` and {cite}`tauxe2018essentials`.
```

TRM is the dominant mechanism by which **igneous rocks** record the
field at the time of their last cooling. A basalt flow erupted at
1 200 °C cools through magnetite's Curie temperature in days to weeks,
locking in a magnetisation parallel to whatever the geomagnetic field
direction is at the eruption site at the moment of cooling. The TRM
in oceanic basalts of the Juan de Fuca plate is what Lecture 24 will
read out as the famous magnetic-anomaly *stripes* of seafloor
spreading.

### 6.2 Detrital remanent magnetisation (DRM) — sediment grains aligning

In environments where rocks form by sedimentation rather than by
cooling, a different mechanism is at work. Ferrimagnetic grains
(magnetite, in particular) eroded from older source rocks are
transported and deposited along with the rest of the sedimentary
load. As each grain settles through the water column, it experiences
a torque from the ambient field that tends to rotate it into
alignment with the field direction — a small magnetic compass in
suspension. When the grain comes to rest at the sediment-water
interface, that alignment is preserved as long as the grain is not
subsequently re-oriented by bioturbation, current shear, or
compaction.

The result is a **detrital remanent magnetisation (DRM)**: the bulk
sediment carries a weak, statistically averaged moment pointing along
the ambient field. DRM is the dominant remanence carrier in **marine
and lacustrine sediments**. The signal is much weaker than TRM in a
volcanic — a typical DRM intensity is $10^{-4}$ to $10^{-3}$ of the
TRM in a basalt — and considerably noisier, because individual grain
alignments are partial, and because compaction and bioturbation
introduce systematic deviations (notably the *inclination shallowing*
correction needed when paleo-latitudes are computed from sediment
records).

DRM is, however, the only mechanism available to record the field
during most of the open-ocean sedimentary record. The high-resolution
record of geomagnetic reversals through the Cenozoic is built almost
entirely from deep-sea sediment DRM, recovered by ocean-drilling cores.
For Pacific Northwest geology, the analogue is the marine sedimentary
sequence of the Cascadia accretionary wedge, which records both the
inclination of the Pleistocene–Holocene field and the rotation
history of the accreted blocks themselves.

### 6.3 Chemical remanent magnetisation (CRM) — minerals growing in place

The third mechanism is **chemical remanent magnetisation (CRM)**:
acquired not by cooling a pre-existing grain, nor by aligning a
settling grain, but by *growing* a new magnetic mineral in the
ambient field at a temperature below its Curie point. A common
example is the growth of fine-grained hematite during diagenesis of a
red bed sandstone: an originally non-magnetic iron-bearing precursor
oxidises to hematite, and the hematite grain locks in a remanence the
instant it crosses a critical size threshold (above which its
relaxation time exceeds the geological timescale).

CRM is the dominant mechanism in **red beds** and in **oxidised
horizons** at the tops of basalt flows (where late hydrothermal
alteration replaces the primary magnetite with hematite). It is also
relevant in some metamorphic rocks where new magnetic minerals
crystallise during prograde or retrograde reactions.

CRM is interpretively trickier than TRM or DRM, because the *age* of
the remanence is the age of mineral growth, not the age of the host
rock. A Triassic red bed whose hematite grew during Jurassic
diagenesis records a Jurassic, not a Triassic, field. Separating CRM
from any earlier TRM in the same sample is one of the routine
demagnetisation tasks of a paleomagnetic laboratory.

### 6.4 Other remanences — a brief inventory

For completeness, two other remanences are worth naming, although
neither plays a leading role in interpreting the lithospheric anomaly:

- **Isothermal remanent magnetisation (IRM)** — acquired when a rock
  is exposed to a strong field (such as a lightning strike) at room
  temperature. IRM is the standard form of *artificial* remanence
  imposed in the laboratory for rock-magnetic characterisation. In
  nature, lightning-induced IRM is a common nuisance overprint at
  mountaintop and exposed-ridge sites.
- **Viscous remanent magnetisation (VRM)** — acquired slowly over
  long times in a weak ambient field; physically, the long-time tail
  of the distribution of grain relaxation times. VRM tends to align
  with the *present-day* field and is the first component removed by
  routine demagnetisation.

Together with TRM, DRM, and CRM, these mechanisms make rocks into
recorders of the magnetic field across the full range of geological
processes — cooling, deposition, mineral growth, and lightning. The
practical task of paleomagnetism is to disentangle which mechanism
is responsible for which component of a measured remanence, and to
date each component independently.

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

3. **Induced or remanent?** A surveyor measures a +800 nT magnetic
   anomaly above a granitic pluton ($Q \approx 0.3$) and a +800 nT
   anomaly above a basalt flow ($Q \approx 6$). She then collects
   oriented samples from each, demagnetises them in zero field, and
   re-measures. Which anomaly will mostly disappear in the lab, and
   which will mostly persist? Explain.

4. **Paleo-latitude error budget.** A paleomagnetic study of a 50-Myr-old
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
hunt1995magprops
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
