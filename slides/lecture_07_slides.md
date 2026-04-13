---
marp: true
theme: ess314
paginate: true
math: katex
html: true
---

<!-- _class: title -->

# Seismic Refraction II
## Beyond the Flat Layer: Special Cases and Uncertainty

### ESS 314 Geophysics · University of Washington

#### Week 3, Lecture 7 · April 13, 2026

#### Marine Denolle

---

# By the end of this lecture…

- **[LO-7.1]** *Derive* the $N$-layer travel-time generalization and the dipping-interface equations
- **[LO-7.2]** *Explain* why low-velocity zones and thin layers are invisible to refraction surveys
- **[LO-7.3]** *Apply* the delay-time method to map irregular refractors from reversed profiles
- **[LO-7.4]** *Enumerate* principal sources of data uncertainty and their effect on depth estimates
- **[LO-7.5]** *Implement* a forward model predicting $T$-$x$ curves for layered and dipping geometries

---

# Where We Left Off

**Single-layer horizontal model (Lecture 6):**

$$t_2(x) = \frac{x}{V_2} + \frac{2h_1 \cos\theta_{ic}}{V_1}, \quad \theta_{ic} = \sin^{-1}\!\frac{V_1}{V_2}$$

- Slope $\Rightarrow$ velocity; intercept $\Rightarrow$ depth
- Works when: horizontal layers, monotonically increasing velocity

**Today:** What happens when these assumptions fail?

---

# Multi-Layer Generalization

For $N$ horizontal layers ($V_1 < V_2 < \cdots < V_N$):

$$t_n(x) = \frac{x}{V_n} + \frac{2}{V_n} \sum_{i=1}^{n-1} h_i \frac{\sqrt{V_n^2 - V_i^2}}{V_i}$$

- Each head wave yields one $T$-$x$ segment with slope $1/V_n$
- Intercept times solved **sequentially**: $h_1$ from $t_{i_2}$, then $h_2$ from $t_{i_3}$ using known $h_1$, etc.
- Layer thicknesses are **not** independent: every deeper estimate depends on all shallower ones

---

# Multi-Layer $T$-$x$ Diagram

![h:390px alt text: Travel-time vs offset diagram with three linear segments labeled direct wave (black), head wave V2 (blue dashed), head wave V3 (orange dotted); intercept times labeled on time axis; shadow zones shaded grey near source for each head wave. Below: cross-section with three horizontal layers and head-wave ray path E-A-B-C-D-F](../assets/figures/fig_multilayer_traveltime.png)

*Three layers, three slope segments. The first head wave from each interface is the first arrival only beyond its crossover distance.*
[Python-generated: `assets/scripts/fig_multilayer_traveltime.py`]

---

# Complication 1: Low-Velocity Zone

**What if $V_2 < V_1$?**

- $\sin\theta_{ic} = V_1/V_2 > 1$ → **no critical angle exists**
- No head wave from the $V_1$–$V_2$ interface
- The intermediate layer is **invisible** to refraction

**Consequence:** The $T$-$x$ diagram looks like a simple two-layer Earth. The interpreted depth to $V_3$ is too large. There is **no warning** in the data.

*Common cause: saturated clays over indurated bedrock; gas-bearing sands; weathered zones*

---

# LVZ: The Hidden Layer

![h:390px alt text: Two-panel figure. Upper panel: three-layer cross-section with V1=1000 m/s over LVZ layer V2=500 m/s over V3=4000 m/s; arrows show rays cannot travel critically along the first interface. Lower panel: T-x diagram with only two straight-line segments, slope 1/V1 and slope 1/V3, with annotation showing LVZ hidden](../assets/figures/fig_lvz_traveltime.png)

*No $1/V_2$ segment appears. P-wave first-arrival refraction alone cannot detect the LVZ.*
[Python-generated: `assets/scripts/fig_lvz_traveltime.py`]

---

# Detecting the LVZ: What Works?

P-wave first-arrival refraction **cannot** detect an LVZ — but these methods can:

| Method | Why it works |
|--------|-------------|
| **Seismic reflection** | Needs only impedance contrast $Z = \rho V$, not $V_2 > V_1$ |
| **Refraction tomography (SRT)** | Inverts all first arrivals for smooth velocity model |
| **MASW** (surface waves) | Rayleigh dispersion is independent of the head-wave condition |
| **S-wave refraction** | Only if $V_{S,2} > V_{S,1}$ while $V_{P,2} < V_{P,1}$ — not a general fix |

**Reflection** is the direct remedy. **MASW** is the most powerful for velocity inversions.

---

# Complication 2: Thin Intermediate Layer

Even when $V_1 < V_2 < V_3$, a thin layer may be undetectable.

The $V_2$ head wave is first arrival only over a **limited offset window**:

$$x_{c,1} = 2h_1\sqrt{\frac{V_2+V_1}{V_2-V_1}}$$

**Rule of thumb:** Layer $n$ is detectable only if the window width $\gtrsim \Delta x_{station}$.

For typical ratios: station spacing $\lesssim 0.6\, h_n$.

---

# Complication 3: Dipping Interface

Dipping layers still produce head waves — but apparent velocity **depends on shooting direction**.

**Down-dip:** $t_d(x) = \dfrac{x}{V_1}\sin(\theta_{ic}+\delta) + t_{id}$

**Up-dip:** $t_u(x) = \dfrac{x}{V_1}\sin(\theta_{ic}-\delta) + t_{iu}$

- Down-dip: $\alpha_d < V_2$ (underestimates true refractor velocity)
- Up-dip: $\alpha_u > V_2$ (overestimates true refractor velocity)

**Solution: shoot from both ends** (reversed profile)

---

# Dipping Interface: Reversed Profile

![h:420px alt text: Multi-panel figure showing cross-sections of horizontal and dipping interfaces with forward and reverse ray paths, and T-x diagrams with parallel (horizontal) and converging (dipping) head-wave segments; forward head wave labeled slope 1/alpha_d in blue dashed; reverse head wave labeled slope 1/alpha_u in orange dashed; horizontal dashed line at top labeled reciprocal times must be equal](../assets/figures/fig_dipping_interface_reversed.png)

*Reversed profiling resolves the ambiguity between dip and velocity.*
[Python-generated: `assets/scripts/fig_dipping_interface_reversed.py`]

---

# Recovering True Velocity and Dip

From apparent velocities $\alpha_d$ (down-dip) and $\alpha_u$ (up-dip):

$$\delta = \frac{1}{2}\left[\sin^{-1}\!\frac{V_1}{\alpha_d} - \sin^{-1}\!\frac{V_1}{\alpha_u}\right]$$

For small dips ($\delta \lesssim 15$–$20°$):

$$\frac{1}{V_2} \approx \frac{1}{2}\left(\frac{1}{\alpha_d} + \frac{1}{\alpha_u}\right)$$

**Reciprocal time check:** Travel time from source $A$ to far receiver must equal travel time from source $B$ to near receiver. Failure indicates timing error or lateral velocity variation.

---

# The Delay-Time Method

For irregular refractors, the **delay time** at geophone $G$ is:

$$\delta t_G = \frac{h_G \cos\theta_{ic}}{V_1}$$

Depth from **both** forward and reverse delay times:

$$h_G = \frac{V_1 V_2}{2\sqrt{V_2^2 - V_1^2}}\left[\delta t_{F,G} + \delta t_{R,G}\right]$$

Result: a point-by-point refractor profile beneath every geophone position.

---

# Delay-Time Method: The Tangent-Arc Construction

![h:390px alt text: Two-panel figure. Upper panel: cross-section with undulating refractor between V1 and V2 layers, showing forward rays (blue) and reverse rays (orange) to geophone positions G1 through G8, with vertical dashed lines showing depths. Lower panel: same cross-section but circular arc segments of radius h_G drawn beneath each geophone in blue and orange; solid green line shows the refractor as the common tangent envelope to all arcs](../assets/figures/fig_delay_time_method.png)

*The refractor surface is the common tangent to all depth arcs.*
[Python-generated: `assets/scripts/fig_delay_time_method.py`]

---

# Sources of Uncertainty

| Source | Effect | Magnitude |
|--------|--------|-----------|
| First-arrival picking error ($\pm$1 ms) | Depth error $\delta h = V_1 \delta t / 2\cos\theta_{ic}$ | 0.1–5 m |
| Velocity gradient in top layer | Curved direct-wave segment; biased intercepts | Depends on gradient |
| Lateral velocity variation | Apparent dip artifact; false structure | Can be large |
| LVZ (undetected) | Systematic underestimate of depth to refractor | Proportional to LVZ thickness |
| Station spacing too large | Missing intermediate layer | $\delta h \sim \Delta x / 0.6$ |

<span class="caption">⚠ Non-uniqueness: different model combinations can fit the same T-x data within noise — always integrate with borehole and independent geophysical data.</span>

---

# Worked Example: Puget Lowland

| Layer | Geology | Velocity |
|-------|---------|----------|
| 1 | Loose fill / organic soil | 350 m/s |
| 2 | Dense glacial outwash gravel | 1650 m/s |
| 3 | Renton Fm. sandstone | 4200 m/s |

From field $T$-$x$ slopes and intercepts: $h_1 = 1.1$ m, $h_2 = 14.6$ m

**Bedrock at ~15.7 m depth** — but is there a LVZ in the gravel? Is the bedrock dipping toward the Seattle Fault?

→ Reversed profiling and borehole control needed for reliable site characterization.

---

# Applications in the Pacific Northwest

- **Liquefaction hazard:** Depth to water table and bearing material in Holocene sediments beneath Seattle
- **Debris flow characterization:** Bedrock-colluvium interface on Cascades volcano flanks
- **Transportation:** WSDOT/Sound Transit tunnel and light-rail corridor characterization
- **Seattle Basin:** Sediment-bedrock interface controls site amplification for Cascadia megathrust events

---

# Concept Check

1. A $T$-$x$ diagram shows only two linear segments even though a borehole shows three velocity units. Name two geological explanations and describe how you would distinguish them.

2. A reversed refraction profile gives apparent velocities $\alpha_d = 1163$ m/s and $\alpha_u = 2146$ m/s with overburden $V_1 = 500$ m/s. Calculate the refractor dip angle $\delta$ and true velocity $V_2$.

3. A geophone array has 3 m spacing. A thin gravel layer with $V_2/V_1 = 2$ is suspected. What is the minimum thickness you could confidently detect?
