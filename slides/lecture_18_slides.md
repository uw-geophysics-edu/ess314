---
marp: true
theme: ess314
paginate: true
math: katex
title: "Lecture 18 — Tsunami"
---

<!-- _class: title -->

# Tsunami

**ESS 314 — Introduction to Geophysics**
University of Washington · Spring 2026 · Lecture 18

Marine Denolle · 14 May 2026

---

## By the end of this lecture, you will be able to:

- **[LO-18.1]** Identify and contrast the three principal tsunami generation mechanisms (earthquake, mass failure, volcanic edifice collapse).
- **[LO-18.2]** Derive the shallow-water wave speed $c = \sqrt{gH}$ from conservation of mass and momentum, and apply it to predict tsunami arrival times.
- **[LO-18.3]** State and apply Green's law $A_{\text{coast}}/A_{\text{ocean}} = (H_{\text{ocean}}/H_{\text{coast}})^{1/4}$ for shoaling, and explain run-up factors of 2–4.
- **[LO-18.4]** Set up the inverse problem of paleotsunami from coastal sand deposits and offshore turbidites.
- **[LO-18.5]** Critique an AI-generated tsunami evacuation recommendation by checking arrival time, peak amplitude, and warning protocol.

---

## The framing question — Tōhoku 2011

11 March 2011, 14:46 local time, Japan Trench megathrust:

- **500 × 200 km** rupture, **25 m** mean slip, **150 s** duration
- 27 minutes later: **9.5 m wave at Sendai**
- At Miyako (Tarō): **38 m run-up**
- At Fukushima Daiichi: wave overtopped the **14 m sea wall**

**Of ~19,000 deaths: more than 90% were caused by the tsunami, not the shaking.**

How does an earthquake become a wall of water — and how do we predict it?

---

## Three generation mechanisms

![h:480](../../assets/figures/fig_18_tsunami_generation.png)

Submarine **earthquake**, submarine **mass failure**, volcanic **edifice collapse**.

---

## Generation: earthquakes

The dominant mechanism. **Vertical seafloor displacement** $u_z(x, y)$ from the @Okada1985 elastic dislocation formula.

| Source | Notable cases |
|---|---|
| Megathrust ($M_W$ 8–9, dip-slip) | 2011 Tōhoku, 2004 Sumatra |
| Strike-slip ($M_W$ 7–8) | 1906 SF, 1999 İzmit (small tsunamis) |
| Outer-rise normal | 1933 Sanriku |

**Strike-slip earthquakes generate weak tsunamis** — the slip is mostly horizontal, no vertical seafloor motion.

---

## Generation: mass failures and volcanoes

**1929 Grand Banks** ($M_W$ 7.2): submarine landslide displaced 200 km³ of sediment, 3–8 m tsunami, severed every transatlantic telegraph cable.

**2018 Anak Krakatau:** flank collapse during eruption → 13 m wave → 437 deaths. **No earthquake warning at all.**

**1883 Krakatau:** 36 m wave, 36,600 deaths.

Modern objects of concern:
- **Cumbre Vieja** (Canary Islands)
- **Hilina Slump** (Kīlauea)

These mechanisms produce *short-wavelength*, *dispersive* tsunamis — different physics from earthquake-generated waves.

---

## Shallow-water wave physics

In the open ocean: $H \approx 4$ km, $\lambda \approx 200$ km, so

$$
\frac{H}{\lambda} \approx 0.01 \;\ll\; 1
$$

This puts a tsunami in the **shallow-water limit** — even though 4 km is, by any other standard, a deep ocean.

In this limit, the wave is **non-dispersive** and the dispersion relation collapses to:

$$
\boxed{\;c \;=\; \sqrt{g\,H}\;}
$$

---

## Shallow-water schematic

![h:430](../../assets/figures/fig_18_shallow_water_setup.png)

Total depth $h(x,t) = H + \eta(x,t)$, with $\eta \ll H \ll \lambda$.

$v(x,t)$ is depth-averaged; that's the shallow-water assumption.

---

## Deriving $c = \sqrt{gH}$ — setup

Take a 1-D water column of length $\lambda$, unit width, depth $h \approx H$.

**Mass per unit length** in one wavelength:
$$ m_\lambda \;=\; \rho \, V_\lambda \;=\; \rho\,\lambda\,H $$

**Net horizontal force** (pressure differential due to surface displacement $\eta$):
$$ F \;=\; \Delta p \cdot H \;=\; \rho\,g\,\eta\,H $$

**Newton's second law** gives the acceleration:
$$ a \;=\; \frac{F}{m_\lambda} \;=\; \frac{\rho g \eta H}{\rho \lambda H} \;=\; \frac{g\,\eta}{\lambda} $$

---

## Deriving $c = \sqrt{gH}$ — close with mass conservation

The horizontal water velocity over one period:
$$ v \;=\; a\,T \;=\; \frac{g\,\eta\,T}{\lambda} $$

**Mass conservation:** mass flux through the column over one period must equal the volume "stored" by the rising surface:

$$ \rho\,v\,T\,H \;=\; \rho\,\lambda\,\eta $$

Substitute $v$:
$$ \rho \cdot \tfrac{g\eta T}{\lambda} \cdot T \cdot H \;=\; \rho\,\lambda\,\eta $$

$$ \frac{\lambda^2}{T^2} = gH \quad\Longrightarrow\quad \boxed{\;c = \sqrt{g\,H}\;} $$

---

## What $c = \sqrt{gH}$ tells us

| Region | $H$ (m) | $c$ (m/s) | $c$ (km/h) |
|---|---|---|---|
| Pacific abyssal plain | 4000 | 198 | 713 |
| Continental shelf | 200 | 44 | 159 |
| Coastal shelf | 50 | 22 | 79 |
| Just offshore | 10 | 9.9 | 36 |

**Three predictions:**
1. Wave speed depends only on water depth (not amplitude!) — travel times are computable from bathymetry alone.
2. Tsunamis are **non-dispersive** — a pulse stays a pulse across an ocean.
3. Energy flux $\propto A^2 \sqrt{H}$ is conserved → **Green's law** for shoaling.

---

## Green's law for shoaling

Conservation of energy flux $\Phi = \tfrac{1}{2}\rho g A^2 \sqrt{gH}$ requires:

$$
A^2 \sqrt{H} \;=\; \text{const.} \qquad\Longrightarrow\qquad
\boxed{\;\frac{A_{\text{coast}}}{A_{\text{ocean}}} \;=\; \left(\frac{H_{\text{ocean}}}{H_{\text{coast}}}\right)^{1/4}\;}
$$

Numerical example: a 1 m wave in 4000 m of water becomes

$$
A_{\text{coast}} = 1\,\text{m} \times (1000)^{1/4} \approx 5.6\,\text{m}
$$

at 4 m water depth — *before* breaking and run-up.

---

## Shoaling — visualised

![h:480](../../assets/figures/fig_18_greens_law_shoaling.png)

---

## Run-up: the additional factor 2–4

Green's law gives the *offshore* amplitude. Run-up — how far up the beach the water reaches — adds an **additional factor of 2–4**.

![h:380](../../assets/figures/fig_18_tohoku_runup.png)

Three mechanisms enhance run-up:
1. **Bay funnelling** (converging shoreline)
2. **Resonance** (bay seiche period matches wave period)
3. **Transient currents and harbour vortices**

---

## The forward computational pipeline

Real-time tsunami forecasting in 5 steps:

1. **Source** estimated from earthquake (USGS *W-phase* CMT) or seafloor pressure
2. **Initial sea-surface displacement** computed via @Okada1985
3. **Propagation**: shallow-water equations on bathymetry — **GeoClaw** (open-source, UW), MOST (NOAA)
4. **Inundation**: non-linear shallow-water with a moving wet-dry boundary, fine grid (5–15 m)
5. **Warning** issued by Pacific Tsunami Warning Center

Steps 1–3 are pure physics. Step 4 is increasingly augmented with machine learning.

---

## Inverse problem: DART buoys

NOAA **DART** (Deep-ocean Assessment and Reporting of Tsunamis):
- ~50 ocean-bottom pressure recorders across the Pacific and Atlantic
- Detect pressure perturbations as small as 1 mm of water
- Transmit via acoustic modem → satellite

A DART arrival, combined with an earthquake source location, constrains the source through linear @Percival2014 inversion of precomputed Green's functions for unit slip.

**The Pacific tsunami warning system uses ~30 minutes of DART data to refine warnings — typically before the wave reaches Hawaii.**

---

## Inverse problem: paleotsunami

**Coastal marsh sand layers** (Atwater et al. 2015):
- Tsunami floods coastal marsh, deposits sand on peat/mud
- Subsequent burial preserves the layer
- Radiocarbon dating brackets each event

**Offshore turbidites** (Goldfinger 2012, USGS PP 1661-F):
- Megathrust shaking triggers submarine landslides at every canyon
- Synchronous turbidity-current deposits along the entire margin
- Correlation along strike → margin-wide rupture (i.e., $M_W \gtrsim 8.7$)

Together: **19 events in the Cascadia record, past 10,000 years.**

---

## The Cascadia paleoseismic record

![h:470](../../assets/figures/fig_18_cascadia_paleoseismic.png)

Mean recurrence ~530 yr; std ~140 yr; range 310–810 yr; **326 yr since 1700**.

---

## Connecting to Cascadia: the timeline

| Time after rupture | Observable | Physics |
|---|---|---|
| **0–3 min** | **Strong shaking on the coast** | **Crustal P-, S-, surface waves** |
| **5–15 min** | **First tsunami at the coast** | **Local shallow-water propagation** |
| 15–60 min | Tsunami at far PNW | Continental-shelf shoaling |
| 4–9 hr | Tsunami in Hawaii | Trans-Pacific propagation |
| 9–14 hr | Tsunami in Japan | Antipodal propagation |

**The "natural warning" — strong, prolonged shaking — is the *only* warning local communities will receive in time.**

The next Cascadia tsunami will arrive within ~15 minutes of the shaking that announced it.

---

## Research Horizon

**Real-time inversion from offshore arrays.** Mulia et al. 2022 (DOI 10.1038/s41467-022-33253-5): deep-learning model trained on simulated S-net pressure records predicts near-field inundation within seconds.

**Bayesian tsunami forecasting at extreme scale.** Rim et al. 2025: 3D coupled acoustic-gravity wave simulations + 1-billion-parameter Bayesian inversion → quantified uncertainty in real time.

**Full physics simulation of Cascadia.** 3D dynamic-rupture simulations + GeoClaw inundation, anchored to paleo-subsidence and coupling models (Wirth 2025, Glehman 2025).

---

## Societal Relevance

**The most important policy question is no longer "is there hazard?" — it is "can we make evacuation work in 15 minutes?"**

- WGS 2024 *Tsunami Hazard* DDS-22, v2.2 (open data)
- WA State CSZ Tsunami Loss Estimate (Extended L1 $M_W$ 9.0)
- NOAA NCTR DART program (open data)
- UW GeoClaw simulations for WA coast

The **geophysics** of this lecture supplies the inputs:
- $c = \sqrt{gH}$ → travel times
- Green's law → amplitudes
- Paleoseismic recurrence → conditional probability

The **engineering** answer needs vertical-evacuation structures, land-use planning, and continuous community education.

---

## AI Literacy — *Critique a generated tsunami advisory*

Try this prompt with an AI assistant:

> "I live in Aberdeen, Washington. A magnitude 9.0 Cascadia earthquake just happened. How long before the tsunami arrives, how high will it be, and what should I do?"

Evaluate the response on:

1. **Travel time** consistent with $c = \sqrt{gH}$? For ~1500 m shelf depth, $c \approx 120$ m/s, so for 80 km offshore source, $t \approx 11$ min. Anything saying "an hour" is qualitatively wrong.
2. **Amplitude** uses Green's law (factor of ~5–6) plus run-up (factor of 2–3)?
3. **Warning protocol**: identifies that **the shaking itself is the only effective warning**?
4. **Acknowledges uncertainty** in rupture distribution + bay-specific run-up?

Submit a 250-word critique. (Lab 5 has the rubric.)

---

## Concept Checks

1. A 1 m tsunami in 4000 m water. Compute (a) the open-ocean speed in m/s and km/h; (b) the amplitude on a 4 m shelf using Green's law; (c) the run-up at a converging bay head with a factor of 2.5.

2. Two $M_W$ 9 earthquakes: one thrust with 25 m of vertical slip, one strike-slip with 15 m of horizontal slip. Which produces the larger tsunami, and *why*?

3. A core through a Cascadia coastal marsh shows 5 sand layers with overlying organic peats radiocarbon-dated 320, 850, 1300, 1700, 2200 yr BP. Mean recurrence interval, std deviation, and the time-since-the-last-event contribution to a 50-yr conditional probability?

4. Pacific transit time, Aleutians → Hilo: depth 4280 m, distance 3700 km. Compare to observed 4–5 h.

---

## Summary

- Three generation mechanisms: **earthquakes, mass failures, volcanic collapse**.
- **$c = \sqrt{gH}$** — derived from F=ma + mass conservation; non-dispersive.
- **Green's law $(H_{\text{ocean}}/H_{\text{coast}})^{1/4}$** — predicts shoaling amplification.
- **Run-up adds another factor of 2–4** from bay funnelling, resonance, breaking.
- Forward problem: Okada → GeoClaw → inundation.
- Inverse problem: **DART buoys** + **paleoseismic record**.
- Cascadia: **19 events / 10 ka, mean recurrence ~530 yr, last in 1700**.
- The next tsunami will arrive within **15 min of the shaking**.

**Next lecture (Module 5):** the gravity field — another integral observable of subsurface mass distribution.
