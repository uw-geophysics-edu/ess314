---
marp: true
theme: default
paginate: true
math: katex
style: |
  section { font-family: 'Segoe UI', Arial, sans-serif; font-size: 26px;
            padding: 40px 52px; background: #ffffff; color: #1a1a1a; }
  h1 { color: #0072B2; font-size: 42px; margin-bottom: 0.3em; }
  h2 { color: #0072B2; font-size: 32px; border-bottom: 2px solid #0072B2; padding-bottom: 6px; }
  strong { color: #D55E00; }
  .lo  { background:#e8f4fd; border-left:4px solid #0072B2; padding:8px 14px;
          margin:0.4em 0; border-radius:4px; font-size:22px; }
  .keq { background:#fff8e1; border-left:4px solid #E69F00; padding:10px 16px;
          margin:0.5em 0; border-radius:4px; }
  .pnw { background:#e6f4ea; border-left:4px solid #009E73; padding:10px 16px;
          margin:0.5em 0; border-radius:4px; }
  .warn { background:#fdecea; border-left:4px solid #D55E00; padding:10px 16px;
           margin:0.5em 0; border-radius:4px; }
  section.title { background:#0072B2; color:white; }
  section.title h1 { color:white; font-size:46px; }
  section.title h2 { color:#56B4E9; border-bottom:2px solid #56B4E9; }
---

<!-- _class: title -->
# Seismic Reflection II
## Dipping Layers, Non-Idealities, and Modern Methods
### ESS 314 — Lecture 9 · Week 3
Marine Denolle · University of Washington · Spring 2026

---

## Learning Objectives

<div class="lo"><strong>[LO-2]</strong> Derive the dipping-layer travel-time equation; compute up-dip and down-dip apparent velocities; recover true velocity and dip</div>
<div class="lo"><strong>[LO-1]</strong> Identify multiple types; predict long-path multiple TWTT and NMO velocity; explain why stacking cannot remove it</div>
<div class="lo"><strong>[LO-1]</strong> State the diffraction equation; describe what migration accomplishes</div>
<div class="lo"><strong>[LO-2]</strong> Apply Shuey approximation $R(\theta) \approx R(0)+G\sin^2\theta$; classify AVO Classes I–IV</div>
<div class="lo"><strong>[LO-7]</strong> Evaluate DL denoising claims; identify two failure modes</div>

---

## Why the Flat-Layer Model Fails Here

<div class="pnw">Cascadia's accretionary wedge: dipping reflectors 5–25°, active thrust faults, intense ground roll on land surveys, multiples above shallow reflectors.</div>

Three failures of Lecture 8:
- **Dip**: CMP gather no longer samples a single point → smeared image
- **Multiples**: have same NMO velocity as primaries → not removed by stacking
- **Diffractions**: fault tips appear as broad hyperbolae → false structure

Each requires a distinct correction strategy.

---

## Dipping Layer: Geometry

For perpendicular depth $h$, dip $\delta$, velocity $V_1$:

$$t_d(x) = \frac{1}{V_1}\sqrt{x^2 + 4hx\sin\delta + 4h^2} \quad \text{(down-dip)}$$

$$t_u(x) = \frac{1}{V_1}\sqrt{x^2 - 4hx\sin\delta + 4h^2} \quad \text{(up-dip)}$$

Both have $t(0) = t_0 = 2h/V_1$ — **same zero-offset time**.

<div class="keq">Key difference: a LINEAR term $\pm(2t_0\sin\delta/V_1)\cdot x$ in $t^2$</div>

---

## Dipping Layer: Asymmetric Curves

![Three-panel: (A) geometry with source, up-dip and down-dip receivers, dipping green reflector and ray paths; (B) t(x) showing down-dip (orange) arriving later and up-dip (blue) earlier than flat (grey dashed), with linear shift annotations; (C) t-squared x-squared showing curved non-linear trends.](../../assets/figures/fig_dipping_layer_geometry.png)

*Down-dip: MORE moveout (slower apparent $V$). Up-dip: LESS moveout (faster apparent $V$). All curves share the same $t_0$.*

---

## CMP Reflection-Point Smear

![Two-panel: left shows flat reflector with all CMP gather reflection points coinciding at a single subsurface location; right shows dipping reflector with reflection points scattered up-dip as offset increases, with a red arrow.](../../assets/figures/fig_cmp_dipping_scatter.png)

*For dipping reflectors, stacking without **DMO correction** blurs subsurface images. DMO repositions reflection points before NMO stacking.*

---

## Dipping Layer: NMO Velocity and Dip Recovery

Taylor expansion of $t_d(x)$ at small $x$:

$$t_d(x) \approx t_0 + \frac{\sin\delta}{V_1}x + \frac{\cos^2\delta}{2V_1^2 t_0}x^2 + \ldots$$

<div class="keq">

$$V_\mathrm{NMO,dip} = \frac{V_1}{\cos\delta} \quad (> V_1 \text{ for any } \delta > 0)$$

</div>

Recover $V_1$ and $\delta$ from two-survey apparent velocities:

$$V_1 = \frac{2V_d V_u}{V_d + V_u} \qquad \sin\delta = \frac{V_u - V_d}{V_u + V_d}$$

---

## Multiple Reflections

![Three-panel: (A) schematic ray paths for primary P, long-path multiple M, peg-leg PL, interbed IB in a two-reflector earth; (B) synthetic CMP gather with four hyperbolic events; (C) t-squared x-squared showing primary (blue) and long-path multiple (orange) have the same slope, annotated 'Same slope (same V_rms)'.](../../assets/figures/fig_multiple_types.png)

---

## The Multiple Suppression Problem

Long-path surface multiple TWTT:

$$t_\mathrm{mult}^2(x) = (2t_0)^2 + \frac{x^2}{V_\mathrm{rms}^2}$$

<div class="warn">

**Same NMO velocity as the primary** → NMO correction flattens BOTH primary and multiple simultaneously. **Stacking cannot suppress the multiple.**

</div>

Suppression methods:
- **SRME** (surface-related multiple elimination): autocorrelation-based prediction and subtraction
- **DL in $\tau$-$p$ domain**: train CNN to separate primaries from multiples by slope

---

## Diffractions: Huygens Principle

Any sharp edge (fault tip, channel boundary, unconformity) acts as a **secondary source** of spherical waves.

<div class="keq">

$$t_\mathrm{diff}(x) = \frac{2}{V_1}\sqrt{(x-x_s)^2 + z_s^2}$$

</div>

Characteristics vs primary reflections:
- **Uniform amplitude** across all offsets (isotropic emission)
- Energy from a **single point**, not a planar interface
- Migration collapses it to the point $(x_s, z_s)$

---

## Diffractions in the Seismic Section

![Three-panel: (A) depth model with flat reflector at 600 m and fault-tip scatterer at 1000 m; (B) travel-time curves showing flat primary (blue dashed) vs broader diffraction hyperbola (red); (C) synthetic seismic section showing horizontal flat primary and the diffraction hyperbola below it, with annotation 'migration required to collapse diffraction to point'.](../../assets/figures/fig_diffraction_hyperbola.png)

*The bowtie pattern (syncline) and diffraction tails (fault tips) are unmigrated artefacts. Lecture 10: Kirchhoff migration collapses them.*

---

## Shot Gather Noise Types

**Coherent noise** in raw shot gathers:
- Ground roll: $V \approx 300$ m/s, $f \approx 5$–20 Hz, **high amplitude**
- Direct wave: $V \approx V_1$, linear, easily muted
- Air blast: $V \approx 340$ m/s
- Head wave: $V > V_1$, linear first arrival

In f-k space: noise events occupy **different velocity fans** than reflections.

**f–k filter:** reject all $|k| > f / V_\mathrm{cutoff}$, preserving $V > V_\mathrm{cutoff}$

$$\text{SNR}_\mathrm{stack} = \sqrt{N_\mathrm{fold}} \times \text{SNR}_\mathrm{single}$$

---

## f–k Ground Roll Suppression

![Three-panel: (A) raw shot gather with annotations pointing to slow-velocity ground roll, linear direct wave, and hyperbolic reflection; (B) f-k spectrum with velocity fan lines at 300, 600, 2000 m/s and shaded reject region; (C) filtered gather with ground roll removed.](../../assets/figures/fig_ground_roll_fk.png)

*Ground roll occupies the slow fan (high $|k|$ per Hz). Rejecting it preserves reflections ($V > 600$ m/s).*

---

## AVO: Zoeppritz + Shuey

At oblique incidence $\theta_i$, energy partitions into reflected P, S, transmitted P, S (Zoeppritz equations). Shuey (1985) linearisation:

<div class="keq">

$$R(\theta_i) \approx \underbrace{R(0)}_{\text{intercept}} + \underbrace{G}_{\text{gradient}} \sin^2\theta_i$$

</div>

$R(0)$ = normal-incidence coefficient $= (Z_2 - Z_1)/(Z_2 + Z_1)$

$G$ = AVO gradient, sensitive to $\Delta(V_P/V_S)$ and hence **fluid content**

Gas substitution (Gassmann) lowers $V_P$, raises $V_P/V_S$ contrast → large $|G|$

---

## AVO Classes I–IV

![Two-panel: (A) R(theta) vs theta curves for Classes I-IV and IIp; (B) R(0)-G crossplot with background trend, scatter clusters for each class, and quadrant labels.](../../assets/figures/fig_avo_classes.png)

*Gas sands (Class III) show **negative $R(0)$ and $G$** — amplitude brightens with offset. The $R(0)$–$G$ crossplot separates gas from brine-saturated sands.*

---

## Worked Example: Dipping Layer

$h = 800$ m, $V_1 = 2000$ m/s, $\delta = 10°$

**(a)** $t_0 = 2 \times 800 / 2000 = \mathbf{0.80}$ **s**

**(b)** $V_\mathrm{NMO} = 2000/\cos10° = \mathbf{2031}$ **m/s**

**(c)** Down-dip at $x=2400$ m:
$$t_d = \tfrac{1}{2000}\sqrt{5760000 + 1329360 + 2560000} = \mathbf{1.553}\ \text{s}$$

**(d)** Up-dip at $x=2400$ m: $t_u = \mathbf{1.322}$ **s**

**(e)** Check: $\sin\delta = (2421-1704)/(2421+1704) = 0.174 \approx \sin10°$ ✓

---

## DL Denoising: U-Net Architecture

![Three-panel: (A) U-Net schematic with encoder (green), bottleneck (orange), decoder (blue), skip connections (red arrows), input noisy gather (light blue) and output denoised gather (light blue); (B) noisy synthetic CMP gather; (C) denoised gather.](../../assets/figures/fig_dl_denoising_concept.png)

*Skip connections preserve fine spatial detail. Training: noisy/clean synthetic pairs → real field data requires self-supervised or transfer-learning strategies.*

---

## Beyond Denoising: Super-Resolution and Foundation Models

**Seismic super-resolution** (Wang et al. 2022): learn the inverse of the seismic PSF to recover sub-$\lambda/4$ detail — breaking the tuning-thickness limit.

**Self-supervised denoising** (Birnie et al. 2021): train on the noisy data alone by exploiting spatial incoherence of noise vs. coherence of signal.

**Seismic foundation models** (SeisFoundation, SegFM 2024):
- Large pretrained transformer backbones fine-tuned on seismic images
- Perform denoising, horizon picking, and facies classification from one model
- Training data: millions of synthetic and field seismic samples

---

## DL Failure Modes — Critical Evaluation

<div class="warn">

1. **Domain shift**: network trained on synthetic gathers may fail on field data where noise is non-stationary and geologically correlated
2. **Physics inconsistency**: denoised output may violate AVO, polarity, or reciprocity — creating fake bright spots
3. **Interpretability gap**: cannot determine whether amplitude anomaly is true DHI or network artifact

</div>

*These are not hypothetical — false bright spots from DL denoising have been documented in published case studies (Grobbe et al. 2022).*

---

## AI Literacy — Epistemics: Interrogating an Interpretation

A bright, negative-polarity reflection at 1.8 s TWTT with amplitude increasing with offset. An AI assistant says: *"likely a Class III AVO anomaly indicative of gas-saturated sand."*

**Before accepting, ask:**
1. Could it be a **long-path multiple**? (Parent primary at 0.9 s — does it exist?)
2. Could it be a **negative kick at base of hard layer**? (Impedance decreasing from dense limestone into shale also gives negative polarity)
3. What **additional data** would confirm? (Well control, 4D survey, CSEM resistivity)

Record the AI's response with your critical evaluation in your Geophysical Reasoning Portfolio.

---

## Concept Check

1. A flat-layer NMO correction is applied to a dipping reflector ($\delta = 12°$). Is the corrected gather over- or under-corrected? Quantify the velocity error.

2. A long-path multiple arrives at $t_0 = 1.4$ s with $V_\mathrm{rms} = 2400$ m/s. What is the parent primary TWTT? Compute the reflector depth assuming $V_1 = 2400$ m/s.

3. What distinguishes a diffraction hyperbola from a primary reflection on a seismic section? Name two geological features that commonly produce diffractions in the Cascadia wedge.

4. A sandstone–shale interface has $R(0) = -0.08$ and $G = -0.10$. What AVO class is this? Is the sand likely gas-saturated or brine-saturated?

---

## Further Reading

- Lowrie & Fichtner (2020) §6.5 — **Free via UW Libraries** ← start here
- Shuey (1985) *Geophysics* 50(4) — AVO linearisation: [doi:10.1190/1.1441936](https://doi.org/10.1190/1.1441936)
- Rutherford & Williams (1989) *Geophysics* 54(6) — AVO classes: [doi:10.1190/1.1442696](https://doi.org/10.1190/1.1442696)
- Birnie et al. (2021) *Geophys. Prosp.* 69 — DL denoising: [doi:10.1111/1365-2478.13095](https://doi.org/10.1111/1365-2478.13095)
- EarthScope/IRIS AVO module (CC-BY): iris.edu/hq/inclass/lesson/avo
