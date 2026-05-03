---
marp: true
theme: ess314
paginate: true
math: katex
title: "Lecture 21 — Isostasy & Lithospheric Flexure"
description: "ESS 314 Spring 2026 · Module 5 — Gravity III"
---

<!-- _class: title -->

# Lecture 21 — Isostasy & Lithospheric Flexure

**ESS 314 — Introduction to Geophysics**
University of Washington · Spring 2026

Marine Denolle · Wed May 6, 2026 · JHN 111

---

## By the end of this lecture, you should be able to…

- **[LO-21.1]** Apply Archimedes — compute crustal-root thickness (Airy) and column density (Pratt).
- **[LO-21.2]** Distinguish *local* (Airy/Pratt) vs. *regional* (flexural) compensation.
- **[LO-21.3]** Interpret a Bouguer profile as evidence for compensation; describe the *isostatic-residual*.
- **[LO-21.4]** Estimate post-glacial rebound timescale and connect to mantle viscosity.
- **[LO-21.5]** Use the flexural parameter $\alpha$ to predict forebulge wavelength.

> Course objectives addressed: **LO-1**, **LO-2**, **LO-3**, **LO-4**.

---

## A puzzle from Lecture 19

The Bouguer anomaly **over a mountain range** is **broadly negative**, not positive.

→ The mountain is **not** an uncompensated excess mass.

Beneath every large topographic feature there is a *mass deficit at depth* — a **root** of light material — that almost exactly balances the topographic excess.

The mountain is **floating**.

---

## Archimedes for mountains

**Hydrostatic equilibrium** at the depth of compensation:

$$ \int \rho_{\text{column,1}} \, g \, dz \;=\; \int \rho_{\text{column,2}} \, g \, dz $$

Below the depth of compensation, the asthenosphere flows freely on geological timescales.
Any pressure imbalance there drives lateral flow that restores equilibrium.

→ Two end-member ways to satisfy this: **Airy** and **Pratt**.

---

## Airy and Pratt — two end-member compensation styles

![Airy and Pratt isostasy compared](../../assets/figures/fig_airy_pratt.png)

- **Airy**: same density, variable thickness. High mountain → deep root.
- **Pratt**: same depth, variable density. High mountain → low-density column.

Both satisfy hydrostatic equilibrium but make different deep-Earth predictions.

---

## Airy — the root formula

$$ \rho_{c} h = (\rho_{m} - \rho_{c}) r \quad\Rightarrow\quad r = \frac{\rho_{c}}{\rho_{m}-\rho_{c}} \, h $$

For $\rho_{c} = 2700$, $\rho_{m} = 3300$ kg m⁻³:

$$ r/h = 4.5 $$

A 1-km mountain → 4.5-km root.

The Tibetan Plateau ($h \approx 5$ km, Moho $\approx 70$ km) is approximately Airy.

---

## Pratt — the density formula

$$ \rho_{c} H_{\text{ref}} = \rho_{\text{block}} (H_{\text{ref}} + h) \quad\Rightarrow\quad \rho_{\text{block}} = \rho_{c} \, \frac{H_{\text{ref}}}{H_{\text{ref}} + h} $$

For $H_{\text{ref}} = 35$ km, $h = 5$ km: $\rho_{\text{block}} = 0.875\,\rho_{c} \approx 2362$ kg m⁻³ (12% lower).

Mid-ocean-ridge crests, hot spots, and oceanic plateaus are approximately Pratt.

---

## Real Earth: a *mixture*

Neither model is solely correct. Earth applies both.

- **Airy** dominates large-scale crustal features (continents, plateaus).
- **Pratt-type** density variations dominate at the oceanic-continental boundary and near hot spots.

→ The choice is a **scale and setting** question.

---

## The isostatic-residual anomaly

$$ \Delta g_{\text{iso}} = \Delta g_{\text{Bouguer}} - \Delta g_{\text{compensation prediction}} $$

- **Zero residual** → load is fully compensated.
- **Positive residual** → uncompensated excess mass; load supported elastically (e.g. recent volcano).
- **Negative residual** → uncompensated deficit; load not yet equilibrated (e.g. active glacier).

Transient residuals are diagnostic of **active geodynamic processes**.

---

## Time-dependent compensation — post-glacial rebound

![Post-glacial rebound](../../assets/figures/fig_postglacial_rebound.png)

Ice sheet removed → lithosphere rebounds toward equilibrium.
Rate set by **mantle viscosity**:

$$ \tau \sim \frac{4\pi\eta}{\rho_{m} g L} $$

For Fennoscandia ($L \sim 1000$ km, $\eta \sim 10^{21}$ Pa s): $\tau \approx 4\!-\!5$ ka — uplift continues at ~9 mm/yr today.

---

## Inverse problem: get viscosity from rebound

Two pieces of data:
- Total post-glacial uplift (Fennoscandia: $\sim 300$ m).
- Present-day uplift rate ($\sim 9$ mm/yr).

→ Ratio gives $\tau$ → equation gives $\eta$.

This single inverse problem has driven mantle-viscosity research for 50 years (Whitehouse 2018 review, CC BY 4.0, https://doi.org/10.5194/esurf-6-401-2018).

---

## Beyond local compensation — flexure

Real lithosphere has **elastic strength**. A vertical load at one point produces **regional** deformation that extends 100s of km.

The thin-plate equation:
$$ D \, \frac{d^{4}w}{dx^{4}} \;+\; (\rho_{m}-\rho_{w}) \, g \, w \;=\; q(x) $$

with **flexural rigidity** $D = E T_{e}^{3} / [12(1-\nu^{2})]$
and **flexural parameter** $\alpha = \bigl[ 4D / (\rho_{m}\!-\!\rho_{w}) g \bigr]^{1/4}$.

---

## What flexure looks like

![Lithospheric flexure under a line load](../../assets/figures/fig_flexural_bulge.png)

Load → central depression + **forebulge** at $x \approx \pi\alpha$ + zero crossing.
Increasing $T_{e}$ widens *and* reduces the deflection.
Inverting the observed forebulge geometry → estimates $T_{e}$.

---

## When does each model apply?

| Feature | Width | Compensation |
|---|---|---|
| Continent / plateau | $\gg \alpha$ | Local (Airy) |
| Mountain range | $\sim$ a few $\alpha$ | Mixed |
| Single seamount | $\ll \alpha$ | Regional (flexural) |
| Subduction trench | bend in plate | Flexural |

A continental craton has $T_{e} \approx 80$ km; an oceanic spreading centre has $T_{e}$ near zero.

---

## Worked example — Mount Olympus (PNW)

Olympic Mountains: $h \approx 2.4$ km. Treat as Airy-compensated.

**Predicted root:** $r = (\rho_{c}/(\rho_{m}-\rho_{c}))\, h = 4.5 \times 2.4 = 10.8$ km.
**Predicted Bouguer (slab approx of root):**
$$ \Delta g_{\text{root}} \approx -2\pi G (\rho_{m}-\rho_{c}) r \approx -272 \text{ mGal} $$

Free-air anomaly should remain small ($<50$ mGal) — root and topography roughly cancel.

→ The Olympics sit on the Cascadia accretionary prism — active loading. The **isostatic residual** is the signal of that active process.

---

## Course connections

- **Backward**: L19 (Bouguer construction) and L20 (regional vs residual).
- **Forward**: L22 — rheological structure of the lithosphere; viscoelasticity.
- **Forward**: Module 7 — *dynamic topography*, vertical motion driven by mantle convection.
- **Cross-link**: present-day GIA is a key correction to GPS-measured vertical land motion → tide gauges → sea-level reconstruction.

---

## Research horizon

- **Whitehouse (2018)** — GIA modelling review (CC BY 4.0). Key open question: depth profile of mantle viscosity.
- **Forte & Rowley (2022)** — much of long-wavelength Bouguer / geoid is **dynamic topography**, *not* local isostasy.
- **Antarctic / Greenland mass balance** — disentangling present-day ice loss from underlying GIA is the largest single uncertainty in 21st-century sea-level projections.

---

## Societal — Cascadia subsidence and the tide gauge

PNW tide gauges show *slower* sea-level rise than the global mean.

This is not measurement error — it is **inter-seismic uplift** from Cascadia locking.

In the next M9 megathrust event:
- Coastal Washington will **drop 0.5–2 m** in minutes.
- Tide-gauge baseline resets.
- Locally, "sea level" is redefined.

→ Vertical land motion (this lecture's mechanics, on a transient timescale) directly informs Cascadia hazard.

USGS Cascadia resource (public domain): https://www.usgs.gov/programs/earthquake-hazards/science/cascadia-subduction-zone

---

## AI Literacy — Prompt Lab

Three prompts that test whether AI handles this lecture's reasoning.

**P1.** *Compare Airy and Pratt for the Tibetan Plateau. Which fits observations and why?*
→ Good: derives both, computes amplitudes, notes empirical mixture. Poor: qualitative-only.

**P2.** *Estimate mantle viscosity from Fennoscandian uplift (9 mm/yr; total 300 m).*
→ Good: $\tau \approx 33$ ka → $\eta \approx 10^{21}$ Pa s. Common error: confuses rebound *amplitude* with *load* amplitude.

**P3.** *Why do oceanic seamounts produce forebulges but individual continental peaks rarely do?*
→ Good: invokes $T_{e}$ contrast *and* notes that continental peaks usually sit within larger compensating structures. Either side alone is incomplete.

---

## Concept Check

1. Two ranges of identical surface elevation produce Bouguer anomalies of $-100$ mGal and $-200$ mGal. **Which is more nearly locally compensated**, and what does the difference suggest about lithospheric strength?
2. A continental margin shows a forebulge **250 km offshore** of a deltaic load. With $\rho_{m}-\rho_{w} = 2270$ kg m⁻³, $E = 70$ GPa, $\nu = 0.25$ — **estimate $T_{e}$**.
3. Fennoscandia: $\sim 9$ mm yr⁻¹ uplift, total $\sim 300$ m post-glacial. **Estimate $\tau$ and $\eta$**. Are they in the canonical range?
