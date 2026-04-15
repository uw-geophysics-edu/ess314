---
marp: true
theme: ess314
paginate: true
math: katex
html: true
style: |
  .lo  { background:#e8f4fd; border-left:4px solid #0072B2; padding:6px 14px;
         margin:0.3em 0; border-radius:4px; font-size:0.88em; }
  .keq { background:#fff8e1; border-left:4px solid #E69F00; padding:8px 14px;
         margin:0.4em 0; border-radius:4px; }
  .pnw { background:#e6f4ea; border-left:4px solid #009E73; padding:8px 14px;
         margin:0.4em 0; border-radius:4px; }
  .warn { background:#fdecea; border-left:4px solid #D55E00; padding:8px 14px;
          margin:0.4em 0; border-radius:4px; }
---

<!-- _class: title -->

# Seismic Reflections II
## Beyond the Flat-Layer Model

### ESS 314 Geophysics · University of Washington

#### Week 3, Lecture 9 · April 22, 2026

#### Marine Denolle

---

# By the end of this lecture…

<div class="lo"><strong>[LO-9.1]</strong> <em>Derive</em> the dipping-layer travel-time equation; compute up-dip and down-dip apparent velocities; recover true velocity and dip</div>
<div class="lo"><strong>[LO-9.2]</strong> <em>Identify</em> multiple types; predict long-path multiple TWTT and NMO velocity; explain why stacking cannot remove it</div>
<div class="lo"><strong>[LO-9.3]</strong> <em>State</em> the diffraction equation; describe what migration accomplishes</div>
<div class="lo"><strong>[LO-9.4]</strong> <em>Apply</em> Shuey approximation $R(\theta) \approx R(0)+G\sin^2\theta$; classify AVO Classes I–IV</div>
<div class="lo"><strong>[LO-9.5]</strong> <em>Evaluate</em> DL denoising claims; identify two failure modes</div>

---

# Why the Flat-Layer Model Fails: Cascadia

![h:380px alt text: Accretionary wedge schematic cross-section showing dipping thrust packages with labelled decorations for three non-idealities: orange label for dipping reflectors, red dashed ray path for a surface multiple, and green triangles with fan arrows for a fault-tip diffraction.](../assets/figures/fig_accretionary_wedge.png)

<div class="pnw" style="font-size:0.83em">Each non-ideality requires a distinct correction: DMO for ①, SRME for ②, migration for ③.</div>

---

# Five Assumptions That Fail

In Lecture 8, the CMP stacking pipeline assumed:

1. **Reflectors are horizontal** — no linear term in $t^2(x)$
2. **Only primary reflections** — every event is a single bounce
3. **Continuous interfaces** — no point scatterers
4. **Noise-free wavefield** — no ground roll or surface waves
5. **Only travel times matter** — amplitude constant with offset

This lecture relaxes each assumption in turn:

<div class="keq"><strong>Why it matters → What breaks → The math → How to fix it</strong></div>

---

# ① Dipping Reflectors: Geometry

For perpendicular depth $h$, dip $\delta$, velocity $V_1$:

$$t_d(x) = \frac{1}{V_1}\sqrt{x^2 + 4hx\sin\delta + 4h^2} \quad \text{(down-dip)}$$

$$t_u(x) = \frac{1}{V_1}\sqrt{x^2 - 4hx\sin\delta + 4h^2} \quad \text{(up-dip)}$$

Both have $t(0) = t_0 = 2h/V_1$ — **same zero-offset time**.

<div class="keq">Key: a <strong>linear term</strong> $\pm\,(2t_0\sin\delta/V_1)\cdot x$ appears in $t^2$ — the mathematical signature of dip</div>

---

# ① Dipping Layer: Asymmetric Curves

![h:400px alt text: Three-panel figure showing (A) dipping reflector geometry with source and up-dip/down-dip receivers; (B) t(x) curves where down-dip (orange) arrives later and up-dip (blue) earlier than flat (grey dashed); (C) t-squared x-squared plot with curved non-linear trends for dipping cases](../assets/figures/fig_dipping_layer_geometry.png)

*Down-dip: MORE moveout (slower apparent $V$). Up-dip: LESS moveout (faster apparent $V$). All share the same $t_0$.*

---

# ① CMP Reflection-Point Smear

![h:410px alt text: Two-panel figure; left shows flat reflector with all CMP gather reflection points coinciding at one location; right shows dipping reflector with reflection points scattered up-dip as offset increases](../assets/figures/fig_cmp_dipping_scatter.png)

*For dipping reflectors, stacking without **DMO correction** blurs the subsurface image. DMO repositions reflection points before NMO stacking.*

---

# ① NMO Velocity and Dip Recovery

Taylor expansion of $t_d(x)$ at small $x$ gives:

<div class="keq">

$$V_\mathrm{NMO,dip} = \frac{V_1}{\cos\delta} \quad (> V_1 \text{ for any } \delta > 0)$$

</div>

Recover $V_1$ and $\delta$ from two-survey apparent velocities $V_d$, $V_u$:

$$V_1 = \frac{2V_d V_u}{V_d + V_u} \qquad \sin\delta = \frac{V_u - V_d}{V_u + V_d}$$

---

# ② Multiple Reflections

![h:400px alt text: Three-panel figure showing (A) ray paths for primary P, long-path multiple M, peg-leg PL, interbed IB; (B) synthetic CMP gather with four hyperbolic events; (C) t-squared x-squared plot where primary and long-path multiple have the same slope annotated as same V_rms](../assets/figures/fig_multiple_types.png)

---

# ② The Multiple Suppression Problem

Long-path surface multiple TWTT:

$$t_\mathrm{mult}^2(x) = (2t_0)^2 + \frac{x^2}{V_\mathrm{rms}^2}$$

<div class="warn">

**Same NMO velocity as the primary** → NMO correction flattens BOTH simultaneously. **Stacking cannot suppress the multiple.**

</div>

Suppression methods:
- **SRME** (surface-related multiple elimination): autocorrelation-based prediction and subtraction
- **DL in $\tau$-$p$ domain**: CNN trained to separate primaries from multiples by slope

---

# ③ Diffractions: Huygens Principle

Any sharp edge (fault tip, channel boundary, unconformity) acts as a **secondary point source** of spherical waves.

<div class="keq">

$$t_\mathrm{diff}(x) = \frac{2}{V_1}\sqrt{(x-x_s)^2 + z_s^2}$$

</div>

Key properties vs primary reflections:
- **Uniform amplitude** across all offsets (isotropic emission)
- Energy from a **single point**, not a planar interface
- Migration collapses it to the point $(x_s, z_s)$

---

# ③ Diffractions in the Seismic Section

![h:400px alt text: Three-panel figure showing (A) depth model with flat reflector at 600 m and fault-tip scatterer at 1000 m; (B) travel-time curves showing flat primary and broader diffraction hyperbola; (C) synthetic seismic section with both events visible](../assets/figures/fig_diffraction_hyperbola.png)

*Bowtie patterns (synclines) and diffraction tails (fault tips) are unmigrated artefacts. Migration (Lecture 10) collapses them.*

---

# ④ Shot Gather Noise and f–k Filtering

**Coherent noise in raw shot gathers:**
- Ground roll: $V \approx 300$ m/s, $f \approx 5$–20 Hz — **high amplitude**
- Direct wave: $V \approx V_1$, linear, easily muted
- Air blast: $V \approx 340$ m/s

**f–k filter:** reject all $|k| > f / V_\mathrm{cutoff}$, preserving $V > V_\mathrm{cutoff}$

<div class="keq">Velocity cone: $|k| \leq f / V_\mathrm{cutoff}$ in $f$–$k$ space defines the slope threshold separating slow noise from faster reflections.</div>

---

# ④ f–k Ground Roll Suppression

![h:400px alt text: Three-panel figure showing (A) raw shot gather with annotations for ground roll, direct wave and reflection; (B) f-k spectrum with velocity fan lines at 300, 600, 2000 m/s; (C) filtered gather with ground roll removed](../assets/figures/fig_ground_roll_fk.png)

*Ground roll occupies the slow fan (high $|k|$ per Hz). Rejecting it preserves reflections ($V > 600$ m/s).*

---

# ⑤ AVO: Zoeppritz + Shuey

At oblique incidence $\theta_i$, energy partitions into reflected P, S, transmitted P, S (Zoeppritz equations). Shuey (1985) linearisation:

<div class="keq">

$$R(\theta_i) \approx \underbrace{R(0)}_{\text{intercept}} + \underbrace{G}_{\text{gradient}} \sin^2\theta_i$$

</div>

- $R(0) = (Z_2 - Z_1)/(Z_2 + Z_1)$ — normal-incidence reflectivity
- $G$ = AVO gradient, sensitive to $\Delta(V_P/V_S)$ — **fluid content**
- Gas substitution lowers $V_P$, leaves $V_S$ unchanged → large $|G|$

---

# ⑤ AVO Classes I–IV

![h:400px alt text: Two-panel figure showing (A) R(theta) vs theta curves for Classes I through IV and IIp with different slopes and (B) R(0)-G crossplot with background trend, scatter clusters for each class, and quadrant annotations](../assets/figures/fig_avo_classes.png)

*Gas sands (Class III): **negative $R(0)$ and $G$** — amplitude brightens with offset. The $R(0)$–$G$ crossplot separates gas from brine-saturated sands.*

---

# DL Denoising: U-Net Architecture

![h:390px alt text: Three-panel figure showing (A) U-Net schematic with encoder green blocks bottleneck orange decoder blue and red skip connections; (B) noisy synthetic CMP gather; (C) denoised gather with improved SNR](../assets/figures/fig_dl_denoising_concept.png)

*Skip connections preserve fine spatial detail. Supervised training requires paired noisy/clean data — unavailable for field data; self-supervised methods train on the noisy data alone.*

---

# DL Failure Modes — Critical Evaluation

<div class="warn">

1. **Domain shift**: network trained on synthetic gathers fails on field data where noise is non-stationary and geologically correlated
2. **Physics inconsistency**: denoised output may violate AVO, polarity, or reciprocity — creating spurious bright spots
3. **Interpretability gap**: cannot determine whether amplitude anomaly is a true DHI or a network artifact

</div>

*False bright spots from DL denoising have been documented in published case studies.*

---

# Worked Example: Dipping Layer

$h = 800$ m, $V_1 = 2000$ m/s, $\delta = 10°$

| Quantity | Formula | Result |
|---|---|---|
| $t_0$ | $2h/V_1$ | **0.80 s** |
| $V_\mathrm{NMO}$ | $V_1/\cos\delta$ | **2031 m/s** |
| $t_d(2400\,\text{m})$ | Exact dip eq. | **1.553 s** |
| $t_u(2400\,\text{m})$ | Exact dip eq. | **1.322 s** |

Check: $\sin\delta = (2421-1704)/(2421+1704) = 0.174 \approx \sin10°$ ✓

---

# Concept Check

1. A flat-layer NMO correction is applied to a dipping reflector ($\delta = 12°$). Is the corrected gather over- or under-corrected? Quantify the velocity error.

2. A long-path multiple arrives at $t_0 = 1.4$ s with $V_\mathrm{rms} = 2400$ m/s. What is the parent primary TWTT? Compute the reflector depth.

3. What distinguishes a diffraction hyperbola from a primary reflection? Name two geological features in the Cascadia wedge that commonly produce diffractions.

4. A sand–shale interface has $R(0) = -0.08$ and $G = -0.10$. What AVO class is this? Is the sand likely gas- or brine-saturated?
