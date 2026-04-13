---
marp: true
theme: default
paginate: true
size: 16:9
math: katex
style: |
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
  section {
    font-family: 'Inter', sans-serif;
    font-size: 22px;
    background: #FAFAFA;
    color: #1a1a1a;
    padding: 40px 56px;
  }
  h1 { font-size: 40px; font-weight: 700; color: #0072B2; margin-bottom: 0.3em; }
  h2 { font-size: 30px; font-weight: 600; color: #0072B2; margin-bottom: 0.4em; }
  h3 { font-size: 24px; font-weight: 600; color: #333; }
  table { font-size: 18px; border-collapse: collapse; width: 100%; }
  th { background: #0072B2; color: white; padding: 6px 12px; }
  td { padding: 5px 12px; border-bottom: 1px solid #ddd; }
  .keyeq { background: #e8f4fd; border-left: 4px solid #0072B2; padding: 12px 18px; border-radius: 4px; margin: 10px 0; }
  .warning { background: #fff3cd; border-left: 4px solid #E69F00; padding: 10px 16px; border-radius: 4px; }
  .important { background: #fde8e8; border-left: 4px solid #D55E00; padding: 10px 16px; border-radius: 4px; }
  .tip { background: #e8f5e9; border-left: 4px solid #009E73; padding: 10px 16px; border-radius: 4px; }
  section.title-slide { background: #0072B2; color: white; }
  section.title-slide h1, section.title-slide h2 { color: white; }
---

<!-- _class: title-slide -->

# Seismic Refraction II
## Beyond the Flat Layer: Special Cases and Uncertainty

**ESS 314 — Introduction to Geophysics**
Week 3, Lecture 11 | 13 April 2026

*Marine Denolle | University of Washington*

---

## Learning Objectives

By the end of this lecture:

- **[LO-2]** Derive the $N$-layer travel-time generalization and the dipping-interface equations
- **[LO-1]** Explain why low-velocity zones and thin layers are invisible to refraction surveys
- **[LO-3]** Apply the delay-time method to map irregular refractors from reversed profiles
- **[LO-4]** Enumerate principal sources of data uncertainty and their effect on depth estimates
- **[LO-5]** Implement a forward model predicting $T$-$x$ curves for layered and dipping geometries

---

## Where We Left Off

**Single-layer horizontal model:**

$$t_2(x) = \frac{x}{V_2} + \frac{2h_1 \cos\theta_{ic}}{V_1}, \quad \theta_{ic} = \sin^{-1}\!\frac{V_1}{V_2}$$

- Slope $\Rightarrow$ velocity; intercept $\Rightarrow$ depth
- Works when: horizontal layers, monotonically increasing velocity

**Today:** What happens when these assumptions fail?

---

## Multi-Layer Generalization

For $N$ horizontal layers ($V_1 < V_2 < \cdots < V_N$):

<div class="keyeq">

$$t_n(x) = \frac{x}{V_n} + \frac{2}{V_n} \sum_{i=1}^{n-1} h_i \frac{\sqrt{V_n^2 - V_i^2}}{V_i}$$

</div>

- Each head wave yields one $T$-$x$ segment with slope $1/V_n$
- Intercept times solved **sequentially**: $h_1$ from $t_{i_2}$, then $h_2$ from $t_{i_3}$ using known $h_1$, etc.
- Layer thicknesses are **not** independent: every deeper estimate depends on all shallower ones

---

## Multi-Layer $T$-$x$ Diagram

![alt text: Travel-time vs offset diagram with three linear segments labeled direct wave (black), head wave V2 (blue dashed), head wave V3 (orange dotted); intercept times t_i1=0, t_i2, t_i3 labeled on time axis; shadow zones shaded grey near source for each head wave](../../assets/figures/fig_multilayer_traveltime.png)

*Three layers, three slope segments. The first head wave from each interface is the first arrival only beyond its crossover distance.*

---

## Complication 1: Low-Velocity Zone

**What if $V_2 < V_1$?**

- $\sin\theta_{ic} = V_1/V_2 > 1$ → **no critical angle exists**
- No head wave from the $V_1$–$V_2$ interface
- The intermediate layer is **invisible** to refraction

<div class="important">

**Consequence:** The $T$-$x$ diagram looks like a simple two-layer Earth. The interpreted depth to $V_3$ is too large. There is no warning in the data.

</div>

*Common cause: saturated clays over indurated bedrock; gas-bearing sands; weathered zones*

---

## LVZ: The Hidden Layer

![alt text: Two-panel figure. Upper panel shows three-layer cross-section with V1=1000 m/s light grey over h1=5m, then V2=500 m/s medium grey over h2=10m labeled LVZ in orange, then V3=4000 m/s dark grey; downward-pointing arrows show refracted rays bending away from the first interface. Lower panel shows T-x diagram with only two straight-line segments, slope 1/V1 in black and slope 1/V3 in orange dashed, with annotation box reading LVZ hidden in orange](../../assets/figures/fig_lvz_traveltime.png)

*No $1/V_2$ segment appears. P-wave first-arrival refraction alone cannot detect the LVZ — active seismic alternatives and independent constraints are required.*

---

## Detecting the LVZ: What Works?

P-wave first-arrival refraction **cannot** detect an LVZ — but these active seismic methods can:

| Method | Why it works |
|--------|-------------|
| **Seismic reflection** | Needs only impedance contrast $Z = \rho V$, not $V_2 > V_1$ |
| **Refraction tomography (SRT)** | Inverts all first arrivals for a smooth velocity model — partially mitigates blind zones |
| **MASW** (surface waves) | Rayleigh wave dispersion is independent of the head-wave condition; directly images $V_S$ inversions |
| **S-wave refraction** | Useful *only* if $V_{S,2} > V_{S,1}$ while $V_{P,2} < V_{P,1}$ — a specific geological case, not a general fix |

<div class="tip">

**Reflection** is the direct remedy. **MASW** is the most powerful for velocity inversions. S-wave refraction has the same fundamental limitation as P-wave refraction.

</div>

---

## Complication 2: Thin Intermediate Layer

Even when $V_1 < V_2 < V_3$, a thin layer may be undetectable.

The $V_2$ head wave is first arrival only over a **limited offset window**:

$$x_{c,1} = 2h_1\sqrt{\frac{V_2+V_1}{V_2-V_1}}, \qquad x_{c,2} = 2(h_1+h_2)\sqrt{\frac{V_3+V_1}{V_3-V_1}}$$

<div class="warning">

**Rule of thumb:** Layer $n$ is detectable only if $\Delta x_{c,n} = x_{c,n+1} - x_{c,n} \gtrsim \Delta x_{station}$.

For typical ratios: station spacing $\lesssim 0.6\, h_n$.

</div>

---

## Complication 3: Dipping Interface

Dipping layers still produce head waves — but apparent velocity **depends on the direction of shooting**.

<div class="keyeq">

**Down-dip:** $\displaystyle t_d(x) = \frac{x}{V_1}\sin(\theta_{ic}+\delta) + t_{id}$

**Up-dip:** $\displaystyle t_u(x) = \frac{x}{V_1}\sin(\theta_{ic}-\delta) + t_{iu}$

</div>

- Down-dip: apparent velocity $\alpha_d < V_2$ (underestimates refractor velocity)
- Up-dip: apparent velocity $\alpha_u > V_2$ (overestimates refractor velocity)

**Solution: shoot from both ends** (reversed profile)

---

## Dipping Interface: Reversed Profile

![alt text: Three-panel figure. Top left: horizontal interface cross-section with V1=500 m/s over V2=1500 m/s, hammers at both ends, refracted ray paths shown as black arrows. Top right: dipping interface at 4-degree dip, same velocities. Bottom: T-x diagram with four linear segments; forward and reverse direct waves both slope 1/V1 as solid black lines; forward head wave labeled slope 1/alpha_d in blue dashed; reverse head wave labeled slope 1/alpha_u in orange dashed; horizontal dashed line at top labeled reciprocal times must be equal.](../../assets/figures/fig_dipping_interface_reversed.png)

*Reversed profiling resolves the ambiguity between dip and velocity. The reciprocal time is a critical quality check.*

---

## Recovering True Velocity and Dip

From apparent velocities $\alpha_d$ (down-dip) and $\alpha_u$ (up-dip):

$$\delta = \frac{1}{2}\left[\sin^{-1}\!\frac{V_1}{\alpha_d} - \sin^{-1}\!\frac{V_1}{\alpha_u}\right]$$

For small dips ($\delta \lesssim 15$–$20°$):

$$\frac{1}{V_2} \approx \frac{1}{2}\left(\frac{1}{\alpha_d} + \frac{1}{\alpha_u}\right)$$

**Reciprocal time check:** The travel time from source $A$ to the far receiver must equal the travel time from source $B$ to the near receiver. Failure indicates either a timing error or lateral velocity variation.

---

## The Delay-Time Method

For irregular refractors — a smooth but non-planar boundary — the **delay time** at geophone $G$ is:

$$\delta t_G = \frac{h_G \cos\theta_{ic}}{V_1}$$

Depth from **both** forward and reverse delay times:

<div class="keyeq">

$$h_G = \frac{V_1 V_2}{2\sqrt{V_2^2 - V_1^2}}\left[\delta t_{F,G} + \delta t_{R,G}\right]$$

</div>

Result: a point-by-point refractor profile beneath every geophone position.

---

## Delay-Time Method: The Tangent-Arc Construction

![alt text: Two-panel figure. Upper panel: cross-section with undulating refractor boundary separating V1 (light grey) above from V2 (dark grey) below. Hammer symbols at both ends labeled E_F and E_R. Six geophone positions G1 through G6. Dashed lines show ray paths from each source to each geophone via the refractor. Lower panel: same cross-section but circular arc segments of radius h_G are drawn beneath each geophone in blue (forward) and orange (reverse) as quarter-circles; solid black line shows the refractor as the common tangent envelope to all arcs.](../../assets/figures/fig_delay_time_method.png)

*The refractor surface is the common tangent to all depth arcs. This construction is equivalent to solving Eq. {delay_time_depth} at each geophone.*

---

## Sources of Uncertainty

| Source | Effect | Magnitude |
|--------|--------|-----------|
| First-arrival picking error ($\pm$1 ms) | Depth error $\delta h = V_1 \delta t / 2\cos\theta_{ic}$ | 0.1–5 m |
| Velocity gradient in top layer | Curved direct-wave segment; biased intercepts | Depends on gradient |
| Lateral velocity variation | Apparent dip artifact; false structure | Can be large |
| LVZ (undetected) | Systematic underestimate of depth to refractor | Proportional to LVZ thickness |
| Station spacing too large | Missing intermediate layer | $\delta h \sim \Delta x / 0.6$ |

<div class="warning">
Non-uniqueness: different models can fit the same $T$-$x$ data within noise. Integration with borehole and other geophysical data is essential.
</div>

---

## Worked Example: Puget Lowland

| Layer | Geology | Velocity |
|-------|---------|----------|
| 1 | Loose fill / organic soil | 350 m/s |
| 2 | Dense glacial outwash gravel | 1650 m/s |
| 3 | Renton Fm. sandstone | 4200 m/s |

From field $T$-$x$ slopes and intercepts: $h_1 = 1.1$ m, $h_2 = 14.6$ m

**Bedrock at ~15.7 m depth** — but is there a LVZ in the gravel? Is the bedrock dipping toward the Seattle Fault?

→ Reversed profiling and borehole control needed for a reliable site characterization.

---

## Applications in the Pacific Northwest

- **Liquefaction hazard**: depth to water table and bearing material in Holocene sediments beneath Seattle
- **Debris flow characterization**: bedrock-colluvium interface on Cascades volcano flanks
- **Transportation infrastructure**: WSDOT and Sound Transit use refraction to characterize the Seattle Basin for tunneling

**Modern extension:** DAS (distributed acoustic sensing) fiber-optic refraction surveys in urban environments — Emily Wilbur's PNSN research brings this directly to the course.

---

## AI Prompt Lab

**Try this with an AI assistant:**

*"In a seismic refraction survey, the T-x diagram shows only two straight-line segments (slopes 1/V₁ and 1/V₃) even though a nearby borehole shows three velocity units. What geological and interpretive explanations should a geophysicist consider?"*

**Evaluate:** Does the AI distinguish between the LVZ problem and the thin-layer problem? Does it recommend additional data? Does it state the assumptions of refraction analysis explicitly?

<div class="tip">

A good AI response will **name the assumptions** (monotonically increasing velocity, horizontal layers, no lateral variation) and **flag when they might be violated** — not just give the textbook answer.

</div>

---

## Concept Check

**Q1.** A two-layer site has $V_1 = 400$ m/s and $V_2 = 3000$ m/s. A reversed profile shows $\alpha_d = 2750$ m/s and $\alpha_u = 3300$ m/s. Estimate the dip angle of the refractor.

**Q2.** A 1 ms timing error in the source trigger propagates to what depth error in $h_1$ if $V_1 = 600$ m/s and $\theta_{ic} = 25°$?

**Q3.** Why does the delay-time method produce a more reliable refractor profile than simple intercept-time analysis when the refractor is irregular?

---

## Summary

- The $N$-layer $T$-$x$ equation generalizes directly; depths solved sequentially
- **Low-velocity zones** are completely invisible to refraction — no head wave is generated
- **Thin layers** may fall below the resolution of the station spacing
- **Dipping interfaces** require reversed profiling to separate velocity from geometry
- The **delay-time method** maps irregular refractors point-by-point from reversed delay times
- Uncertainty in depth estimates arises from picking error, velocity gradients, lateral heterogeneity, and undetected special cases

*Next lecture: Seismic Reflection I — the other branch of the wavefield*

