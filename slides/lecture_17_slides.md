---
marp: true
theme: ess314
paginate: true
math: katex
title: "Lecture 17 — Ground Motions, Intensities, and Building Damage"
---

<!-- _class: title -->

# Ground Motions, Intensities, and Building Damage

**ESS 314 — Introduction to Geophysics**
University of Washington · Spring 2026 · Lecture 17

Marine Denolle · 13 May 2026

---

## By the end of this lecture, you will be able to:

- **[LO-17.1]** Distinguish *intensity* (felt-effect) from *magnitude* (source) from *peak ground motion* (waveform measurement).
- **[LO-17.2]** Define PGA, PGV, PGD, and 5%-damped $S_a(T)$, and explain physically which carries the dominant energy at each band.
- **[LO-17.3]** Predict three site/source effects — distance attenuation, soft-soil amplification, soil liquefaction — and apply $T_{\text{building}} \approx N/10$ s.
- **[LO-17.4]** Critique an AI-generated explanation of expected shaking by separating source, path, and site contributions.

---

## The framing question

The 2001 Nisqually earthquake was **$M_W$ 6.8** — one number for the *source*.

But people in Olympia and Seattle did not experience $M_W$ 6.8. They experienced:

- A **time history** of acceleration, lasting ~30 s
- With a **PGA of ~0.16 g** downtown
- With **MMI VI–VII** (felt by all, slight damage)
- All depending on **soil class, building height, and location**

**Magnitude, ground motion, and intensity are three different things.** Confusing them is the most common single error in earthquake reporting.

---

## Three observables, three time derivatives

For a record $\boldsymbol{u}(\boldsymbol{x}, t)$ at a station:

$$
\boldsymbol{u} \xrightarrow{\partial_t} \boldsymbol{v} = \dfrac{\partial \boldsymbol{u}}{\partial t}
\xrightarrow{\partial_t} \boldsymbol{a} = \dfrac{\partial^2 \boldsymbol{u}}{\partial t^2}
$$

| Quantity | Spectral emphasis | Engineering use |
|---|---|---|
| **Displacement** $u$ | Long periods | Static offsets, GPS |
| **Velocity** $v$ | Intermediate periods | Damage potential |
| **Acceleration** $a$ | Short periods | Force on a rigid object: $F = ma$ |

A factor of $\omega$ in the spectrum at each derivative.

---

## PGA, PGV, PGD, and $S_a(T)$

![h:380](../../assets/figures/fig_17_response_spectrum.png)

A real building responds to a **band of frequencies**, not just to PGA.

$S_a(T)$ = peak acceleration of a 5%-damped oscillator of period $T$.

---

## Why $S_a(T)$ matters: the building rule of thumb

$$
T_{\text{building}} \;\approx\; \frac{N}{10}\,\text{s} \qquad (N = \text{storeys})
$$

| Building | $N$ | $T$ |
|---|---|---|
| Wood-frame house | 1 | 0.1 s |
| 4-storey apartment | 4 | 0.4 s |
| 10-storey office | 10 | 1.0 s |
| Columbia Tower (Seattle) | 76 | ~6 s |
| Tokyo Skytree | — | ~10 s |

**As cities build taller, the relevant period band lengthens** — exactly where megathrust earthquakes radiate.

---

## Buildings × Source types

![h:480](../../assets/figures/fig_17_building_periods.png)

---

## The forward problem: GMPE

A **Ground-Motion Prediction Equation** (GMPE) relates ground motion to source, path, and site:

$$
\ln Y \;=\; f_{\text{source}}(M)\;+\;f_{\text{path}}(M, R)\;+\;f_{\text{site}}(V_{S30})\;+\;\varepsilon
$$

- $Y$: PGA, PGV, or $S_a(T)$
- $\sigma(\varepsilon) \approx 0.6$ in natural log → factor of ~1.8 in linear scatter

**Even the best modern GMPE disagrees with observation by a factor of two routinely.**

USGS **ShakeMap** (Worden et al., 2020) implements this prediction in real time.

---

## Site amplification: impedance contrast

For an SH wave going from rock ($Z_1$) into soft soil ($Z_2 \ll Z_1$):

$$
\frac{A_{\text{surface}}}{A_{\text{rock}}} \;=\; \frac{2\,Z_1}{Z_1 + Z_2} \;\approx\; 2
$$

Plus **resonance** of a layer of thickness $H$ over rigid rock:

$$
f_0 \;=\; \frac{\beta_2}{4 H}
$$

Duwamish flats: $H \approx 200$ m, $\beta_2 \approx 350$ m/s → $T_0 \approx 2.3$ s — close to mid-rise resonance!

(1985 Mexico City: $T_0 \approx 2$ s, amplification ~50.)

---

## Site amplification — visualised

![h:500](../../assets/figures/fig_17_intensity_vs_pgm.png)

---

## The inverse problem: Modified Mercalli Intensity (MMI)

For a historical earthquake (1556 Shaanxi, 1700 Cascadia) — no instrumental record exists.

Only the **felt and damage descriptions** survive: the **MMI scale** (I–XII).

| MMI | Effect | PGA |
|---|---|---|
| III | Indoor vibrations like a passing truck | ~0.005 g |
| V | Plaster cracks, dishes broken | 0.04–0.09 g |
| VII | Slight damage in well-built; considerable in poorly built | 0.18–0.34 g |
| IX | Considerable damage in special structures | 0.65–1.24 g |
| X+ | Most masonry destroyed; rails bent | > 1.24 g |

Modern **Ground Motion / Intensity Conversion Equations** (GMICE, Worden 2012) convert PGA ↔ MMI statistically.

---

## Three caveats on intensity

**1. Ordinal, not interval.** The step VI → VII is not the same physical jump as VII → VIII.

**2. Mixes source, path, and site.** Soft soil + URM construction reads higher MMI for the same source.

**3. Depends on the building stock.** A modern wood-frame house fails at higher PGA than a 1900 brick building. The same shaking is reported as *different* MMI in different decades.

> Intensity is not a measure of an *earthquake* — it is a measure of an earthquake **at a place**.

---

## Same magnitude, different felt area: the East–West contrast

![h:480](../../assets/figures/fig_17_isoseismals_eastvswest.png)

The 2011 M5.8 Virginia event was felt by **20× more people** than the M6.0 Parkfield 2004. Reason: eastern crust has higher $Q$ (less attenuation), not bigger source.

---

## Liquefaction

Saturated, loose sand + sustained shaking → pore pressure rises until the granular skeleton fails.

**Three conditions:**
1. Loose sandy soil below the water table
2. PGA $\gtrsim 0.1\,g$ for ~10+ cycles
3. Shallow ground water (within a few metres of the surface)

**Examples:**
- 1964 Niigata (buildings tilted on intact foundations)
- 2011 Christchurch (sand boils throughout the city)
- 2001 Nisqually (Duwamish flats and Harbor Island)

In Seattle: Washington Geological Survey *Liquefaction Susceptibility* maps show extensive risk in fill areas.

---

## Building failure modes

![h:380](../../assets/figures/fig_17_failure_modes.png)

Each failure mode has an engineering counterpart:
- **Soft-storey** → shear walls, especially at ground level
- **Frame collapse** → cross-bracing, gussets
- **Foundation failure** → ground improvement, deep piles

---

## Earthquake-resistant retrofit strategies

Three classical approaches plus modern dampers:

1. **Shear walls** — vertical reinforced-concrete plates between window openings absorb lateral shear.
2. **Cross-bracing / gussets** — diagonal members add shear strength to existing frames.
3. **Base isolation** — laminated rubber-and-steel bearings decouple building from ground; **shifts $T$ longer** to escape the high-frequency band.
4. **Viscous dampers** — convert kinetic energy to heat (the big "X" piston in retrofits).

Cost of base isolation: ~5–10% of building cost. Used in hospitals, City Halls, the LA Civic Centre.

---

## Cascadia: three source types, three signatures

| Source | Mechanism | Periods | Buildings at risk |
|---|---|---|---|
| **Crustal** | Seattle Fault, etc. | 0.1–1 s (high-freq.) | Wood-frame houses, low-rise |
| **Intraslab** | Within Juan de Fuca slab (e.g. Nisqually 2001) | 0.1–2 s | Mid-rise |
| **Megathrust** | Plate-interface (last 1700, next ?) | **3–30 s** | **High-rises, bridges** |

A Cascadia $M_W$ 9 will produce **modest PGA** in Seattle but **record-setting $S_a(3\text{ s})$** — exactly the band that excites the city's high-rise inventory.

---

## Research Horizon

**Site-specific GMPEs from machine learning**
$V_{S30}$ alone misses ~50% of the residual; full $V_S$ profiles + microtremor H/V + deep learning halve the residual at well-instrumented stations (Bahrampouri 2024).

**Earthquake Early Warning (ShakeAlert)**
Deployed across WA/OR/CA 2021–2023. The first few seconds of the P-wave forecast the much larger S- and surface-wave shaking.

**Physics-based Cascadia simulation**
No instrumental record of a Cascadia $M_W$ 9 exists; 3D dynamic-rupture simulations (Frankel 2018, Wirth 2018) anchored to paleoseismic constraints provide the forecast.

---

## Societal Relevance — Cascadia building codes

The 2018 Washington State Building Code adopted Cascadia-specific $S_a(1\text{ s})$ design values for coastal counties.

- WGS 2024 *CSZ Tsunami Loss Estimate Study*
- USGS *ShakeAlert* deployment (statewide 2023)
- WA DNR *HAZUS* loss-estimation maps

**Every new mid-rise apartment from Bellingham to Astoria is being designed today against an explicit Cascadia long-period shaking forecast — a forecast that did not exist a generation ago.**

---

## AI Literacy — *Critique a generated shaking forecast*

Try this prompt with Claude or ChatGPT:

> "I live in Seattle in a wood-frame house. A magnitude 9.0 earthquake happens on the Cascadia subduction zone, 200 km west of me. How strong will the shaking feel?"

Then evaluate the response for:

1. **Source / path / site separation** — does it acknowledge the question is underspecified?
2. **Quantitative uncertainty** — does it give a range, or a confident number?
3. **Period dependence** — does it note that wood-frame at $T = 0.1$ s is *not* the band that megathrusts excite most?
4. **Non-uniqueness flagging** — does it ask about soil class, building age, distance precision?

**Submit a 250-word critique.** Lab 4 has the rubric.

---

## Concept Checks

1. A 30-storey building and a wood-frame house stand on the same lot in downtown Seattle. A crustal $M_W$ 6 earthquake gives PGA = 0.20 g, $S_a(3\,\text{s}) = 0.05\,g$. Which is at greater risk? How does the answer change for a Cascadia $M_W$ 9 with PGA = 0.15 g, $S_a(3\,\text{s}) = 0.4\,g$?

2. Sketch (qualitatively) PGA vs distance for two earthquakes: identical $M_W$ 6, both at 30 km from downtown Seattle, one on basement rock and one in the Duwamish fill. Which is higher at the surface, and *why*?

3. Why is using "intensity" to compare the 1556 Shaanxi (830,000 deaths) and the 2010 Maule, Chile ($M_W$ 8.8, 521 deaths) more informative than using "magnitude" — and why is the inverse *also* true?

---

## Summary

- **Three quantities, not interchangeable:** magnitude (source), ground motion (waveform), intensity (felt effect).
- **PGA dominates short-period band; $S_a(T)$ is the engineering quantity** that matches a building of period $T$.
- $T_{\text{building}} \approx N/10$ s links architecture to seismology.
- **Site effects are first-order:** impedance + resonance can amplify by 2–10×.
- **GMPEs predict mean and scatter;** ShakeMap conditions on observations.
- **Liquefaction and four failure modes** explain most damage; engineering retrofits address each.
- **Cascadia long-period forecasts** are now embedded in WA building codes.

**Next lecture:** the same Cascadia rupture, viewed as an oceanic forcing — the tsunami.
