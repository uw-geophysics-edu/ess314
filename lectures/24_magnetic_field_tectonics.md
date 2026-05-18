---
title: "Magnetic Field, Magnetism, and Tectonic Plates"
subtitle: "Anomalies, ensembles, and the floor of the Pacific"
short_title: "Magnetism & Tectonics"
week: 9
lecture: 24
date: "2026-06-03"
topic: "Magnetism II — anomalies, inversion, and seafloor spreading"
course_lo: ["LO-1", "LO-2", "LO-3", "LO-4", "LO-5"]
learning_outcomes: ["LO-OUT-A", "LO-OUT-B", "LO-OUT-D", "LO-OUT-E"]
open_sources:
  - "Lowrie & Fichtner (2020), Fundamentals of Geophysics, 3rd ed., Ch. 5.4–5.7 (UW Libraries e-book)"
  - "Blakely (1995), Potential Theory in Gravity and Magnetic Applications, Cambridge (UW Libraries)"
  - "Vine & Matthews (1963), Magnetic anomalies over oceanic ridges, Nature, doi:10.1038/199947a0"
  - "USGS aeromagnetic surveys of the Pacific Northwest (public domain, https://mrdata.usgs.gov/magnetic/)"
  - "NOAA NCEI EMAG2 global magnetic anomaly grid (public domain)"
keywords: [magnetic anomaly, dipole, reduction-to-pole, half-width depth rule, ensemble inversion, seafloor spreading, Vine-Matthews, Juan de Fuca, Seattle Fault Zone, paleomagnetism]
---

# Magnetic Field, Magnetism, and Tectonic Plates

:::{seealso}
📊 **Lecture slides** — <a href="https://uw-geophysics-edu.github.io/ess314/slides/lecture_24_slides.html" target="_blank">open in new tab ↗</a>
:::

::::{dropdown} Learning Objectives
:color: primary
:icon: target
:open:

By the end of this lecture, students will be able to:

- **[LO-24.1]** Define the **total-field magnetic anomaly** $\Delta F$ and explain why it is approximately the projection of the source field onto the local $\mathbf{F}_\text{earth}$ direction.
- **[LO-24.2]** Use the closed-form expression for a buried induced magnetic dipole to predict the **anomaly shape** above the source, including the dependence on the inclination $I$ of the inducing field.
- **[LO-24.3]** Apply the **half-width depth rule** $z \approx 2\,x_{1/2}$ for an induced dipole at the magnetic pole (or after reduction-to-pole), and propagate measurement noise $\sigma_F$ to depth uncertainty $\sigma_z / z \approx (1/3)\,\sigma_F / F_\text{max}$.
- **[LO-24.4]** Generate and interpret an **ensemble-fit cloud** in $(z, m)$ parameter space, identify the theoretical ridge $m \propto z^3$ along which depth and moment trade off, and discuss how induced + remanent ambiguity widens the cloud relative to the gravity case.
- **[LO-24.5]** Use a magnetic stripe sequence offshore the Pacific Northwest to estimate a **seafloor half-spreading rate**, and explain the role of magnetic data in mapping the **Seattle Fault Zone**.

::::

::::{dropdown} Syllabus Alignment
:color: secondary
:icon: list-task

| | |
|---|---|
| **Course LOs addressed** | LO-1 (observables ↔ Earth properties), LO-2 (forward model), LO-3 (inverse problem with $d = G(m)$), LO-4 (uncertainty and non-uniqueness), LO-5 (multi-physics integration with gravity and seismic reflection) |
| **Learning outcomes practiced** | LO-OUT-A (forward problem from governing equation), LO-OUT-B (inverse problem with model uncertainty), LO-OUT-D (multi-physics interpretation), LO-OUT-E (societal-relevance reasoning, via the Seattle Fault aeromagnetic survey) |
| **Prior lecture** | [L23 — Earth Magnetism and Mineral Magnetism](23_earth_magnetism.md) |
| **Next lecture** | [L25 — Heat and Geodynamics](25_heat_geodynamics.md) |
| **Lab connection** | Lab 7 — Magnetic Anomaly Modeling (ensemble inversion of an induced dipole, JdF stripe interpretation) |
| **Textbook** | Lowrie & Fichtner (2020), Ch. 5.4–5.7 |

::::

## Prerequisites

This lecture builds directly on **Lecture 23** (geomagnetic field components, dipole geometry, mineral magnetism, TRM) and on the gravity-inversion framework introduced in **Lecture 20**. Students should be comfortable with the closed-form dipole field, with the idea of an ensemble fit and a $\chi^2/N$ misfit, and with the half-width depth rule for a buried point source. Familiarity with how IGRF separates main field from anomaly is assumed.

---

## 1. The Geoscientific Question

```{epigraph}
"If the floor of the oceans is spreading apart at mid-ocean ridges and
new sea floor is being formed there, then this new sea floor should be
magnetised in the direction of the Earth's magnetic field at the time of
its formation; and if … the direction of Earth's magnetic field reverses
at intervals … the floor should now consist of strips of normal and
reversed material running parallel to the ridge crest."
— F. J. Vine & D. H. Matthews, *Nature*, 1963
```


In 1963, Fred Vine and Drummond Matthews proposed that the alternating
magnetic anomalies recorded across the Carlsberg Ridge in the Indian Ocean
could be explained if (i) the seafloor was *spreading* outward from a
ridge crest, and (ii) Earth's magnetic field had repeatedly *reversed* its
polarity in the geologic past. Each new strip of seafloor would lock in the
polarity at the moment of its crystallisation, building up a striped
record of plate motion and field history simultaneously.

Within a decade the hypothesis had been confirmed across every major mid-
ocean ridge on Earth — including the **Juan de Fuca Ridge** offshore the
Pacific Northwest. The JdF system is one of the smallest mid-ocean
ridges currently active, but its half-spreading rate of about 30 mm/yr
generates a perfectly legible striped magnetic-anomaly map between
British Columbia and northern California.

This lecture is about how to turn a magnetic anomaly profile — the
small perturbation to Earth's main field above a buried source — into a
*physical model* of what lies underneath. Three threads run through
the lecture:

1. The **forward problem** has an extra complication compared with
   gravity: the anomaly shape depends not only on source depth and
   magnetisation strength, but also on the **inclination of the inducing
   field**.
2. The **inverse problem** is non-unique in the same way as gravity, but
   *more so*, because the source magnetisation is a vector quantity with
   both induced and remanent contributions.
3. Despite these complications, the half-width depth rule and the
   ensemble-fit framework from Lecture 20 *transfer* — and we can write
   closed-form expressions for how measurement noise propagates to depth
   uncertainty.


ground survey, a cesium-vapour scalar magnetometer towed behind an
aircraft — measures the **magnitude** of the total magnetic field $|F|$ at
each station. The signal of interest is the small perturbation produced by
buried magnetised sources, on top of the much larger main field
($F_\text{earth} \sim 50\,000$ nT in the mid-latitudes). After removing
the IGRF-modelled main field, the diurnal variation (Lecture 23), and any
known external disturbance, what remains is the **total-field anomaly**:

$$
\Delta F(\mathbf{r}) = |\mathbf{F}_\text{earth}(\mathbf{r}) +
                       \mathbf{B}_\text{source}(\mathbf{r})|
                       - |\mathbf{F}_\text{earth}(\mathbf{r})|.
$$ (eq-totalF-defn)

Because $|\mathbf{B}_\text{source}| \ll |\mathbf{F}_\text{earth}|$ for
most crustal targets (typical anomalies are 1–500 nT against a
50 000-nT background), {eq}`eq-totalF-defn` linearises to

$$
\Delta F(\mathbf{r}) \approx
\mathbf{B}_\text{source}(\mathbf{r}) \cdot \hat{\mathbf{F}}_\text{earth},
$$ (eq-totalF-approx)

i.e. the anomaly is the **projection of the source field onto the
direction of the ambient main field**. This linearisation is the
analog of the Bouguer/free-air step in gravity (Lecture 20), and it
is what makes anomaly maps additive and superposable.

## 3. Forward problem — the buried induced dipole

The simplest magnetic body that has a closed-form solution is a small
sphere or compact volume of uniformly magnetised material — equivalent
in its external field to a point **magnetic dipole** of moment $\mathbf{m}$.
For a body in Earth's ambient field, the dipole moment has two
components:

$$
\mathbf{m} = \mathbf{m}_\text{induced} + \mathbf{m}_\text{remanent}
        = k V \mathbf{H}_\text{earth} + \mathbf{m}_\text{remanent},
$$ (eq-m-decomp)

where $V$ is the body volume, $k$ is the volume magnetic susceptibility
(Lecture 23, eq. {eq}`eq-susc`), $\mathbf{H}_\text{earth}$ is the local
ambient field (in A m$^{-1}$), and $\mathbf{m}_\text{remanent}$ is the
permanent (e.g. TRM) component. For a freshly intruded volcanic body
the two terms can be comparable; for an old plutonic body whose
remanence has decayed by viscous re-magnetisation, the induced term
usually dominates. **For the remainder of §3 we restrict attention to
the induced case**, returning to the vector ambiguity in §6.

For an induced dipole of moment $\mathbf{m}$ buried at depth $z$ in an
ambient field of inclination $I$, the total-field anomaly along a
profile in the magnetic-meridian plane is

$$
\Delta F(x) = \frac{\mu_0\, m}{4\pi}\,
\frac{[2(\hat{\mathbf{m}} \cdot \hat{\mathbf{r}}) (\hat{\mathbf{m}} \cdot
\hat{\mathbf{r}}) - 1]\;(3\,m_x^2 + m_z^2) - \ldots}{r^5},
$$

which is more useful in coordinate form. Place the dipole at $(0, z)$
with $z > 0$ measured downward; place the observation at $(x, 0)$ on the
surface. The vector from source to observation is
$\mathbf{r} = (x, -z)$ with $r = \sqrt{x^2 + z^2}$.
The induced moment direction is $\hat{\mathbf{m}} = (\cos I, \sin I)$,
so the magnetisation lies parallel to the inducing field. The general
dipole field is

$$
\mathbf{B}_\text{dipole} = \frac{\mu_0\, m}{4\pi}
\,\frac{3(\hat{\mathbf{m}} \cdot \hat{\mathbf{r}})\hat{\mathbf{r}}
- \hat{\mathbf{m}}}{r^3},
$$ (eq-Bdipole)

and the total-field anomaly is its projection onto $\hat{\mathbf{F}}_\text{earth} =
\hat{\mathbf{m}}$:

$$
\Delta F(x) = \mathbf{B}_\text{dipole}(x, 0) \cdot \hat{\mathbf{m}}
= \frac{\mu_0\, m}{4\pi\, r^5}
\,\bigl[3(\hat{\mathbf{m}}\cdot\hat{\mathbf{r}})^2 r^2 - r^2\bigr],
$$ (eq-deltaF-general)

which can be expanded to give $\Delta F(x)$ explicitly in terms of $(x,
z, I)$.

### 3.1 The shape of the anomaly depends on $I$

The result of {eq}`eq-deltaF-general` is plotted in
{numref}`fig-anomaly-shapes` for the same buried dipole evaluated at
$I = 0$ (magnetic equator), $I = 45°$ (mid-latitude), and $I = 90°$
(magnetic pole).

```{figure} ../assets/figures/fig_dipole_anomaly_shapes.png
:name: fig-anomaly-shapes
:alt: Three side-by-side line plots of total-field anomaly delta F in
 arbitrary units versus distance from source in km from -3 to +3, for
 a buried induced dipole at depth 600 m. The left panel (I = 0,
 magnetic equator) shows a profile with a deep negative trough at
 x = 0 of about -45 units, with small positive lobes of about +10
 units at x = +/- 700 m, symmetric about x = 0; annotated "symmetric
 (even): central negative with side positives". The middle panel
 (I = 45°, mid-latitude) shows an asymmetric profile with a positive
 peak of about +57 units near x = -200 m and a smaller negative
 shoulder of about -25 units near x = +400 m, with annotation
 "asymmetric: positive peak with negative shoulder". The right panel
 (I = 90°, magnetic pole) shows a perfectly symmetric Gaussian-like
 positive peak of about +90 units centered at x = 0, with annotation
 "symmetric positive peak directly over source".

Anomaly shape over a buried induced dipole at $z = 600$ m, as a function
of the inclination of the inducing field. **Magnetic equator** ($I = 0$):
symmetric "central negative + side positives" pattern. **Mid-latitude**
($I = 45°$): asymmetric profile, positive peak displaced toward the
magnetic equator, with a small negative shoulder on the high-latitude
side. **Magnetic pole** ($I = 90°$): symmetric positive peak directly over
the source. Reproduces the qualitative content of Fig. 5.6 in
{cite}`blakely1995potential`.
```

The pole-symmetric case is the cleanest, and it is the geometry in which
the half-width depth rule has its simplest form. At any other latitude,
the asymmetric anomaly is harder to read — the apparent "centre" of the
positive peak is *not* directly above the source. This is the central
practical complication of magnetic versus gravity interpretation, and it
motivates the most common processing step in magnetic-survey reduction:
**reduction to pole**.

### 3.2 Reduction to pole

Reduction-to-pole (RTP) is a frequency-domain filter that converts an
anomaly measured at any (inclination, declination) into the anomaly that
*would have been* measured at the magnetic pole. The filter is exact for
an induced source whose direction of magnetisation equals the inducing-
field direction, and approximate in general. Applied to a midlatitude
anomaly, RTP centres the peak over the source and makes it symmetric
({numref}`fig-rtp`).

```{figure} ../assets/figures/fig_reduction_to_pole.png
:name: fig-rtp
:alt: Two-by-two figure. Top-left panel: observed total-field anomaly
 profile at inclination I = 45 degrees, showing an asymmetric curve
 with a positive peak near -200 m offset and a negative shoulder near
 +400 m. Top-right panel: same anomaly after reduction-to-pole, now a
 symmetric positive peak centred at x = 0. Bottom-left and bottom-right
 panels: schematic cross-sections at depth showing a diamond marker
 labelled "induced dipole (z = 600 m)" at depth 600 m below the
 surface; surface line at y = 0 labelled "surface". Both bottom
 panels show the same source geometry; only the displayed anomaly
 above changes.

Reduction-to-pole. **(a)** The asymmetric anomaly observed at mid-latitude
($I = 45°$) above the buried dipole is hard to centre by eye. **(b)** After
RTP, the anomaly becomes a symmetric positive peak directly over the
source — recovering the geometry that would have been measured at the
magnetic pole. Both panels show the **same** subsurface body. Adapted
from {cite}`blakely1995potential`, Section 12.3.
```

For a Pacific-Northwest survey at $I \approx 69°$, the un-reduced anomaly
is already mostly symmetric, and the practical benefit of RTP is modest.
For a survey near the magnetic equator (Brazil, southeast Asia,
equatorial Africa), the un-reduced anomaly is *strongly* asymmetric and
RTP is essential.

### 3.3 The half-width depth rule

At the pole (or after RTP), {eq}`eq-deltaF-general` reduces to

$$
\Delta F(x) = \frac{\mu_0\, m}{4\pi}\, \frac{2 z^2 - x^2}{(x^2 + z^2)^{5/2}},
$$ (eq-pole-anomaly)

which has its maximum

$$
\Delta F_\text{max} = \frac{\mu_0\, m}{4\pi}\, \frac{2}{z^3}
$$ (eq-pole-peak)

at $x = 0$ and falls to **half** its peak at

$$
x_{1/2} \approx 0.5\, z,
\qquad \text{equivalently} \qquad
\boxed{\; z \;\approx\; 2\, x_{1/2}\;}
$$ (eq-halfwidth-rule)

({numref}`fig-halfwidth`b). The factor 0.5 is exact for an induced point
dipole at the pole and approximate for any other geometry; it follows
from solving $\Delta F(x_{1/2}) = \Delta F_\text{max} / 2$ in
{eq}`eq-pole-anomaly`. Compared with the corresponding rule for the
gravity sphere, $x_{1/2}^\text{grav} \approx 0.766\, z$
(Lecture 20, §3.4), the magnetic rule has a *smaller* prefactor —
the magnetic anomaly falls off faster than the gravity anomaly because
the dipole field decays as $r^{-3}$ rather than $r^{-2}$.

```{figure} ../assets/figures/fig_magnetic_halfwidth.png
:name: fig-halfwidth
:alt: Three stacked panels. Panel (a) is a cross-section showing three
 diamond markers at the same horizontal position x = 0 but at depths
 of 300 m (blue), 600 m (orange), and 1200 m (green), with an orange
 vertical down-arrow labelled "F_earth (vertical at pole)" on the left
 side. Receiver triangles are spaced along the surface line. Panel
 (b) is a plot of normalised delta F over delta F_max versus
 horizontal distance from -3 to +3 km, showing three peaked
 curves; the z = 300 m curve is narrow, the z = 600 m intermediate,
 and the z = 1200 m wide. A dotted horizontal line at 0.5 is labelled
 "1/2 peak"; markers and annotations indicate half-widths of x_1/2 =
 +/- 150 m for z = 300 m, +/- 300 m for z = 600 m, and +/- 600 m for
 z = 1200 m. Panel (c) is a plot of total-field anomaly in nT versus
 horizontal distance for the deepest case (z = 1200 m) only, showing
 a green Gaussian-like peak of 50 nT, a grey shaded horizontal band
 between -4 and +4 nT labelled "±2 sigma noise band (sigma = 2 nT)",
 a dotted horizontal line at 25 nT labelled "½ peak = 25.0 nT", and
 two vertical dashed lines at +/- 600 m connected by a double-headed
 arrow labelled "2·x_1/2 ≈ 1200 m". An inset box on the right reports
 "half-width rule: z ≈ 2·x_1/2; inferred z = 1200 m (true 1200 m);
 S/N at peak = 25; sigma_z / z ≈ (1/3)(sigma_F / F_max) ≈ 1.3%;
 sigma_z ≈ 16 m".

The half-width depth rule, with measurement-noise propagation.
**(a)** Three identical-moment dipoles at $z = 300, 600, 1200$ m.
**(b)** The same anomalies normalised by their peaks — deeper sources
produce wider profiles. The half-width $x_{1/2}$ scales linearly with
$z$. **(c)** For the deepest source, the realistic peak amplitude is
50 nT; a $\pm 2\sigma$ noise band of $\sigma = 2$ nT (typical of a
regional aeromagnetic survey) gives a signal-to-noise ratio of 25 at
the peak. The inferred depth $z = 2\,x_{1/2} = 1200$ m matches truth.
Propagating $\sigma_F = 2$ nT through the half-width formula gives
$\sigma_z \approx 16$ m, or roughly 1% of the depth — see §3.4.
```

### 3.4 Measurement errors and the noise → depth chain

The half-width rule {eq}`eq-halfwidth-rule` is exact for clean data, but
real magnetic surveys are noisy at several stages:

- **Sensor noise**. A proton-precession magnetometer measures total field
  by precession of proton magnetic moments; sensor noise is roughly
  0.1 nT in a single one-second reading. Cesium-vapour magnetometers
  (the standard for high-resolution aeromagnetics) achieve 0.01 nT.
  Both are far below the typical anomaly amplitudes of interest.
- **Positioning error**. Modern GPS gives a station location to
  $\sim 1$ m horizontally — small compared with the survey-line spacing
  of 100 m–1 km that ordinarily controls the spatial resolution of an
  anomaly map.
- **External (diurnal) variation**. Earth's external field changes by
  10–50 nT during a typical day, with much larger swings during magnetic
  storms. This is the dominant source of error in a magnetic survey and
  is removed by a **base-station correction**: a stationary magnetometer
  at the survey site records the time-varying external field, which is
  then subtracted from every roving measurement. Surveys are also
  designed to *cross over* themselves (looped traverses) so that any
  residual drift can be estimated from the closure error.
- **Regional gradients and the IGRF**. The main field varies on the
  scale of hundreds of kilometres. For a survey of a few-km extent, an
  affine regional trend is subtracted; for a continental-scale survey,
  the IGRF model is removed point by point.

After all corrections, a typical regional aeromagnetic survey delivers
total-field anomalies with $\sigma_F \approx$ 1–5 nT. To translate this
into a depth uncertainty, note that the peak amplitude in
{eq}`eq-pole-peak` depends on $z$ as $\Delta F_\text{max} \propto z^{-3}$.
Differentiating the half-width rule {eq}`eq-halfwidth-rule` with respect
to the measured peak gives, at fixed $m$:

$$
\frac{\sigma_z}{z} \;\approx\; \frac{1}{3}\,\frac{\sigma_F}{\Delta F_\text{max}}.
$$ (eq-magnetic-sigma-rule)

The factor 1/3 in {eq}`eq-magnetic-sigma-rule` is the analog of the
1/2 factor in the gravity formula (Lecture 20, eq. 3.6.4), and it is
*smaller* because the magnetic field falls off more steeply with
distance. **For a fixed signal-to-noise ratio, magnetic depths are
inferred more precisely than gravity depths** — provided one stays in the
regime of induced-only magnetisation.

```{admonition} SNR rule of thumb
:class: note

| $\Delta F_\text{max} / \sigma_F$ | Depth uncertainty $\sigma_z / z$ | Verdict |
|---:|---:|---|
| > 50 | < 0.7% | Excellent — depth pinned. |
| 10 – 50 | 0.7% – 3% | Good — depth well-constrained. |
| < 10 | > 3% | Poor — quote bounds, not a number. |

For the example in {numref}`fig-halfwidth`c, SNR = 25 gives
$\sigma_z / z = 1.3\%$, or $\sigma_z = 16$ m on a 1 200 m source —
better than the depth resolution of most seismic-reflection surveys at
that depth.
```

### 3.5 From data error to model uncertainty — the ensemble fit

The half-width rule gives a single best-fit depth and a single propagated
uncertainty, but it commits to the *form* of the source (a point induced
dipole at the pole) before reading the data. A more honest treatment is
to scan over the full $(z, m)$ parameter space, compute the
$\chi^2$-misfit of the predicted profile against the observations, and
*accept* every model whose reduced $\chi^2$ falls below a threshold —
the same protocol used in Lecture 20 §3.7 for the gravity sphere.

The result is the **ensemble cloud** in {numref}`fig-ensemble`. The
accepted models — those with $\chi^2/N \leq 1.5$, given $\sigma_F = 2$
nT and 31 stations — line up along a curved valley in $(z, m)$ space:

$$
m \;\propto\; z^3
\qquad \text{(magnetic ridge, induced point dipole, at the pole)}.
$$ (eq-mzcubed-ridge)

```{figure} ../assets/figures/fig_magnetic_ensemble.png
:name: fig-ensemble
:alt: Two side-by-side panels. Left panel (a) "Observations and
 accepted-model family" shows a Gaussian-like peak. Approximately
 31 blue circle markers with error bars (sigma = 2 nT) trace a
 profile peaking at delta F = 33 nT at x = 0 and falling to zero
 by x = +/- 1.5 km. A family of grey thin curves spans roughly the
 same shape, representing 200 accepted models. A dashed black line
 labelled "true model" is centred and overlaps closely with an
 orange solid line labelled "best fit (min chi-squared per N)".
 Right panel (b) "Accepted-model cloud in (z, m) parameter space"
 plots magnetic moment m (A m^2, scaled by 10^8) versus depth z (m)
 from 300 to 1100 m. A cluster of small colored dots forms a curved
 elongated cloud (color-coded by chi-squared/N value via a viridis
 colour bar from 0.7 to 1.5) running along a dotted black line
 labelled "theoretical ridge m proportional to z^3", from low
 (z=520 m, m=2e7) to high (z=730 m, m=6e7). An orange star marker
 with black edge is plotted at (600, 3.78e7), labelled "true (z*,
 m*)".

From data error to model uncertainty for the induced point dipole at the
pole. **(a)** 31 synthetic stations with $\sigma_F = 2$ nT, the true
model (dashed), the best-fit minimum-$\chi^2$ model (orange), and 200
randomly selected accepted models (grey). **(b)** The accepted models
in $(z, m)$ space, coloured by reduced chi-squared. The cloud lies along
the theoretical $m \propto z^3$ ridge, which is the magnetic analog of
the $M \propto z^2$ ridge for a gravity sphere. The depth and the moment
are strongly correlated; neither can be pinned down independently from
peak amplitude alone — only the *combination* $m/z^3$ is.
```

The ridge {eq}`eq-mzcubed-ridge` has a steeper exponent than the gravity
case ($M \propto z^2$) because the magnetic field decays as $r^{-3}$.
The depth-moment correlation is therefore *stronger* in the magnetic
case: a 10% error in inferred depth translates into a 30% error in
inferred moment. The half-width measurement breaks this degeneracy by
constraining the *width* of the profile in addition to its amplitude —
hence the importance of having stations spaced finely enough to resolve
$x_{1/2}$, not merely the peak.

## 4. Inverse problem — and a complication unique to magnetics

For a gravity survey, the only physical ambiguity in inversion is the
trade-off between source mass and depth: a deep heavy source produces
the same anomaly as a shallow light one. For a magnetic survey, *two*
ambiguities operate together:

1. The same $(z, m)$ trade-off, intensified to $m \propto z^3$.
2. An additional *vector* ambiguity in the magnetisation direction:
   $\mathbf{m} = \mathbf{m}_\text{induced} + \mathbf{m}_\text{remanent}$
   {eq}`eq-m-decomp`. The induced component is parallel to
   $\mathbf{H}_\text{earth}$, but the remanent component can point in
   *any* direction — its orientation was set when the body last cooled
   through the Curie temperature, possibly at a different geographic
   latitude, possibly during a different polarity epoch.

The consequence is that a single magnetic-anomaly profile cannot, in
general, separate induced from remanent magnetisation. If a body is
known to be young and to have low Königsberger ratio
$Q = |\mathbf{m}_\text{remanent}| / |\mathbf{m}_\text{induced}| \ll 1$,
the induced-only assumption is safe. If the body is volcanic and recent
($Q \gg 1$, e.g. fresh basalt), the induced-only assumption fails
spectacularly.

**Resolution requires more data**: gradiometry to constrain the
direction of $\mathbf{B}_\text{source}$ at multiple stations,
laboratory measurements of representative samples, or joint inversion
with gravity (which sees only mass and is blind to remanence). All
three approaches are in standard use today.

## 5. A worked example — Juan de Fuca stripes and seafloor spreading

The Juan de Fuca Ridge sits offshore between Vancouver Island and
northern California, generating new oceanic crust at a *half*-rate of
$\sim 30$ mm/yr. As each new strip of basalt crystallises and cools
through magnetite's Curie temperature of 580 °C, it locks in a TRM
parallel to the polarity of Earth's field *at that moment*. Sequential
polarity reversals — recorded in the **Geomagnetic Polarity Timescale**
({numref}`fig-jdf`a) — generate a striped pattern of crustal
magnetisation that is preserved indefinitely once the rock cools below
the blocking interval.

A ship-towed total-field magnetometer crossing the ridge perpendicular
to its axis measures the integrated anomaly of all stripes within its
footprint, producing the characteristic symmetric striped pattern in
{numref}`fig-jdf`b.

```{figure} ../assets/figures/fig_jdf_stripes.png
:name: fig-jdf
:alt: Three stacked panels. Panel (a) shows a horizontal bar from age
 0 to 5 Ma divided into black (normal polarity) and white (reversed)
 segments, with labels for the Brunhes (0-0.78 Ma), Jaramillo
 subchron (~1 Ma), Matuyama reversed (0.78-1.78 Ma), Olduvai (1.78-
 1.95 Ma), Gauss (2.58-3.60 Ma), and Gilbert (3.60-5.00 Ma) chrons.
 Panel (b) plots total-field anomaly delta F in nT versus distance
 from ridge axis in km from -200 to +200, showing a symmetric striped
 pattern with positive (black) and negative (light blue) lobes
 alternating, peak amplitudes of about +/- 400 nT, centred on the
 ridge axis (orange vertical line at x = 0) labelled "RIDGE AXIS
 (spreading center)". The pattern is the mirror image to the left and
 right of the ridge axis. Panel (c) is a schematic cross-section
 showing a 3-km-deep ocean (light blue) on top of a 1-km-thick
 magnetised crust band (depth 3 to 4 km below sea surface) striped
 in black (normal) and white (reversed) intervals. A central orange
 vertical line labelled "ridge axis" rises from the seafloor to the
 surface. Black arrows on each side at depth ~5 km labelled
 "spreading" point outward.

Magnetic stripes across the Juan de Fuca Ridge at a half-spreading rate
of 30 mm/yr. **(a)** Geomagnetic polarity timescale for the last 5 Myr,
following {cite}`candekent1995gpts` and {cite}`ogg2020gts`. Black =
normal polarity, white = reversed. **(b)** Predicted total-field
anomaly profile across the ridge: each polarity stripe in the
seafloor below contributes a band of constant magnetisation, and the
boundary between stripes produces a peak or trough in the anomaly.
**(c)** Schematic cross-section: the basalt layer (1 km thick at the
top of the seafloor) is the magnetised carrier; the polarity at each
horizontal position reflects the field direction at the moment that
piece of crust was emplaced. The picture is symmetric about the ridge
because both flanks were generated at the same epoch and have spread
outward at the same rate.
```

The half-rate $v$ is read directly from the spacing of stripes:
the Brunhes/Matuyama boundary at 0.78 Ma sits at a distance
$x_B = v \cdot 0.78\,\text{Ma}$ from the ridge axis. For
$v = 30$ mm/yr = 30 km/Myr, that distance is $x_B = 23.4$ km. Across
the JdF system, $x_B$ is observed in the range 20–25 km depending
on the segment, consistent with half-rates of 25–32 mm/yr.

This is the **single most decisive piece of evidence** for seafloor
spreading and plate tectonics: a quantitative correlation between
polarity reversals dated independently in continental lava flows and
the geometry of magnetic anomalies in mid-ocean basins. By 1968 the
correlation had been measured on every major ridge on Earth.

```{admonition} Why magnetics — not gravity, not seismics — proved seafloor spreading
:class: tip

Mid-ocean ridges have gravity anomalies (mass deficit above a hot rising
plume) and seismic-velocity anomalies (slower mantle beneath the
ridge), but neither encodes *time*. Magnetic stripes do, because the
polarity timescale provides an *independent clock* calibrated from
continental volcanics. This is a textbook example of the kind of
*joint constraint* that modern integrated geophysical inversion seeks
to exploit: a property that is non-unique in one observable
(magnetisation strength, by itself, is ambiguous) becomes diagnostic
when combined with an independent stratigraphic constraint
(polarity reversal ages).
```

## 6. Societal relevance — the Seattle Fault Zone from the air

In the Pacific Northwest, magnetic methods are central to one of the
most consequential applied-geophysics projects of the past quarter
century: high-resolution aeromagnetic mapping of the **Seattle Fault
Zone (SFZ)**, an east-west zone of active blind reverse faults that
crosses Puget Sound directly beneath downtown Seattle and Bainbridge
Island.

The SFZ was mapped first from paleoseismic trenching and LIDAR-imaged
fault scarps; it was placed on the regional geophysical map by a 1997
USGS aeromagnetic survey at 300-m line spacing
{cite}`blakely2002seattlefault`. Tertiary volcanic units uplifted on
the hanging wall produce strong positive magnetic anomalies (peaks
of several hundred nT); the contrast against the sedimentary footwall
defines a linear edge that traces the fault for tens of kilometres.

The maximum earthquake credible on the SFZ is approximately
$M_w$ 7 — a large enough event to cause heavy damage in downtown
Seattle. The Washington State seismic hazard maps used by code
authorities for building design lean directly on the fault geometry
recovered from this aeromagnetic survey.

Magnetic methods cannot identify *when* the next earthquake will
occur, but they *can* — and do — establish where it is most likely to
nucleate, which is the prior input to every probabilistic hazard
calculation.

## 7. Research horizon — magnetic methods today

The 60-year-old Vine-Matthews framework still grounds magnetic
interpretation, but the modern frontier sits in three places:

- **Joint magnetic-gravity inversion** for ore-deposit exploration
  (gold, nickel sulfide, lithium pegmatites): combined sensitivity
  to density and magnetisation breaks ambiguities that neither dataset
  resolves on its own.
- **UAV-borne magnetics**: drone-mounted total-field and gradient
  magnetometers now achieve 0.05 nT precision at 30 m line spacing,
  delivering near-surface anomaly maps once limited to ground surveys.
  The 2024–2025 Cascadia Magnetic Anomaly Reconnaissance project
  flew a series of UAV traverses over hidden faults on Bainbridge
  Island as a hazard-mapping pilot.
- **Magnetotelluric (MT) imaging**, which uses the time-varying
  external field as an EM source to image deep electrical
  conductivity — the topic of Lecture 25.

Deep-learning surrogate models have begun to replace the bulk of the
forward simulations in iterative inversion, but every surrogate so
far in production use is trained on *physics-based* simulations of
the dipole-Maxwell equations of §3. The neural network is a
substitute for the matrix-vector multiplication, not for the physics.

## 8. AI literacy — the latitude trap

A common failure mode of large language models on magnetic-anomaly
problems is to treat the anomaly *shape* as if the survey were always
at the pole — that is, to ignore the latitude dependence of the
forward problem.

```{admonition} AI Epistemics activity
:class: tip

**Step 1.** Sketch (by hand, on graph paper) a magnetic anomaly profile
over a small buried induced dipole at three different latitudes:
the magnetic pole, a mid-latitude site at $I = 45°$, and the magnetic
equator. Use {numref}`fig-anomaly-shapes` as a guide if needed.

**Step 2.** Hand the *equator* profile (only — without telling the LLM
where it was measured) to a chat model and ask it to infer the depth
of the source using the half-width rule.

**Step 3.** Check whether the LLM:

1. *Asks* for the latitude before applying the half-width rule. (Good.)
2. *Applies* the half-width rule directly. (Bad — the rule does not
   work without RTP.)
3. Generates a confidently wrong number. (Worst.)

**Step 4.** Whichever the case, write a single-paragraph rebuttal that
either (i) explains why your LLM's question for the latitude was
appropriate, or (ii) demonstrates that the LLM's answer is wrong by
deriving the correct procedure (RTP first, then half-width).

The deliverable is the LLM transcript + your rebuttal. The grading
criterion is not whether the LLM was right, but whether *you* caught the
error and could defend the correct procedure.
```

## 9. Concept check

```{admonition} Concept-check questions
:class: tip

1. **Half-width and SNR.** A regional aeromagnetic survey over a basalt
   plug at the magnetic pole gives a peak anomaly of $\Delta F_\text{max}
   = 80$ nT with surveyed half-width $x_{1/2} = 240$ m and a measurement
   noise of $\sigma_F = 4$ nT. Compute the depth using the half-width
   rule, the SNR, and the propagated depth uncertainty from
   {eq}`eq-magnetic-sigma-rule`. Is this an "excellent / good / poor"
   determination by the rule of thumb in §3.4?

2. **Half-rate from a stripe.** A magnetic profile across the southern
   JdF system shows the central peak of the Brunhes (normal) anomaly at
   $x = 0$ and the central peak of the Matuyama (reversed) anomaly at
   $x = \pm 17$ km. Using the polarity-timescale midpoint of the
   Matuyama at $t = 1.78$ Ma, estimate the half-spreading rate of the
   JdF Ridge over the last two million years.

3. **Induced or remanent?** A small buried body in eastern Oregon
   produces a strongly *negative* magnetic anomaly at a station above
   it (peak $\Delta F = -200$ nT) — the opposite sign from what would
   be expected for an induced dipole at $I = +69°$. Sketch two
   physical scenarios that could produce this signature. Which
   additional measurement would you make to discriminate between them?
```

```{admonition} Concept-check answers
:class: hint, dropdown

*Answers and worked solutions are provided in the instructor materials
(see `concept_check_lecture24.md` in the `ess314-instructor` repository).*
```

## 10. Looking ahead

This lecture closes the magnetics block. Lecture 25 turns to
**electromagnetic methods** — magnetotellurics and controlled-source EM
— which use the *time variation* of Earth's external field (and its
induced response in conductive Earth) as a probe of electrical
conductivity at depths of 1 km to 100 km. The physics that links this
lecture's static dipole to next lecture's time-varying field is
Maxwell's equations; the linking quantity is the magnetic vector
potential $\mathbf{A}$.

## 11. Further reading

```{bibliography}
:filter: docname in docnames

blakely1995potential
blakely2002seattlefault
candekent1995gpts
ogg2020gts
vine1963magnetic
tauxe2018essentials
lowrie2020fundamentals
```

::::{grid} 1 1 2 2

:::{grid-item-card} Companion notebook (next step)
The accompanying Jupyter notebook **`magnetics_ensemble.ipynb`** (in the
course `notebooks/` directory, scheduled for release with Lab 6)
implements the forward operator of §3 and the ensemble grid-search of
§3.5, and asks students to invert a synthetic JdF profile for both
spreading rate and source depth distribution. A second notebook,
`magnetics_forward.ipynb` (companion to Lecture 23), supplies the IGRF
field-calculator that those students will use as a baseline.
:::

:::{grid-item-card} Open data and tools
- **USGS Aeromagnetic Compilations**: <https://mrdata.usgs.gov/magnetic/>.
- **MagIC (paleomagnetism)**: <https://earthref.org/MagIC/>.
- **Marine Magnetic Anomaly Profiles**: NGDC Marine Geophysical Data Browser, <https://www.ncei.noaa.gov/maps/geophysics/>.
- **PmagPy**: <https://github.com/PmagPy/PmagPy>.
:::

::::
