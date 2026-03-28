---
marp: true
theme: default
paginate: true
math: mathjax
style: |
  section {
    font-size: 28px;
    padding: 50px 60px;
  }
  h1 {
    font-size: 36px;
    color: #0072B2;
    border-bottom: 2px solid #0072B2;
    padding-bottom: 8px;
  }
  h2 {
    font-size: 30px;
    color: #333;
  }
  .columns {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2em;
  }
  ul { margin-top: 0.5em; }
  li { margin-bottom: 0.3em; }
  strong { color: #0072B2; }
  table { font-size: 24px; }
---

# The Inaccessible Earth
### Scales, Instruments, and the Logic of Geophysical Inference

**ESS 314 — Geophysics** | Lecture 2 | April 1, 2026
Marine Denolle · University of Washington

---

# Learning Objectives

By the end of this lecture:

- **[LO-2.1]** Calculate the fraction of Earth accessible to direct sampling; explain why geophysical inference is unavoidable
- **[LO-1.3]** Place geophysical processes on a space–time scale diagram; explain why no single method spans the full range
- **[LO-4.2]** Describe what each of five geophysical instruments actually records, and identify one intrinsic limitation per instrument
- **[LO-3.1]** Formulate the forward problem for two methods; explain why the inverse problem is non-unique

---

# How Little Have We Seen?

The Kola Superdeep Borehole (Russia, 1970–1989):
- Deepest borehole: **12.262 km**
- Stopped because rock temperature > 180°C — not technology failure

$$f = \frac{z_\text{max}}{R_\oplus} = \frac{12.262}{6{,}371} = \mathbf{0.19\%}$$

| Access mode | Depth | Fraction of $R_\oplus$ |
|------------|-------|----------------------|
| Mponeng Mine | 4 km | 0.06% |
| Kola borehole | 12.2 km | 0.19% |
| Seismic refraction | ~50 km | 0.8% |
| Global seismic waves | 6,371 km | **100%** |

**Key point:** Seismic waves are the only tool that samples the entire Earth. Every deep layer boundary was found by listening to earthquakes.

---

# Eratosthenes (230 BCE): First Geophysical Measurement

Two observations, one distance, one result:

- At Syene (Aswan): Sun directly overhead at summer solstice noon
- At Alexandria (800 km north): rod casts shadow at **7.2°** from vertical

$$C_\oplus = \frac{360°}{7.2°} \times 800\text{ km} = 40{,}000\text{ km}$$

$$R_\oplus = \frac{C_\oplus}{2\pi} \approx 6{,}366\text{ km} \quad (\text{modern: } 6{,}371\text{ km})$$

**Assumptions:** parallel Sun rays, spherical Earth, same meridian, known distance

**Key point:** Every geophysical measurement embeds model assumptions. Identifying those assumptions is the first step in evaluating an inference.

---

# Scale Diagram: Scale Determines Method

![width:900px](../../assets/figures/fig_space_time_scales.png)

**Key point:** No single instrument spans 15 orders of magnitude in time and 10 in space. The scale of the process dictates the appropriate method.

---

# Three Insights from the Scale Diagram

**1. Same material, different physics**
- Mantle = elastic solid on seismic timescales (seconds)
- Mantle = viscous fluid on convection timescales (millions of years)
- Which description applies depends on the ratio of observation time to material relaxation time

**2. Scale dictates resolution**
- A seismometer measuring arrivals in seconds cannot sense million-year flow
- A continental gravity survey cannot resolve a 10-cm void in concrete

**3. Gap distance and non-uniqueness**
- The further an observable is from the process of interest, the more assumptions are needed to connect them — and the more non-unique the inference

**Key point:** Before choosing a method, identify the spatial and temporal scale of the target process.

---

# What Seismometers Actually Record

A seismometer measures **ground velocity** (or displacement/acceleration) as a function of time.

Every seismogram entangles:
1. **Source** — the earthquake's rupture history and radiation pattern
2. **Path** — modifications from Earth's heterogeneous velocity structure
3. **Site** — amplification or attenuation by local geology

Separating these three contributions is itself an inverse problem.

Frequency range: 0.003 Hz (Earth free oscillations, ~300 s) to 50+ Hz (local microseismicity)

**Key point:** A seismogram is not a direct recording of the earthquake — it is a convolution of source, path, and site effects. Every interpretation requires a model for at least two of these three.

---

# What Gravimeters, Magnetometers, and Heat Flow Probes Record

**Gravimeter:**
- Measures $g$ to ~1 μGal ($10^{-8}$ m/s²) = 1 part per billion
- Lateral density contrasts → gravity anomalies
- GRACE-FO: measures monthly gravity change from satellites (ice, groundwater, postseismic)

**Magnetometer:**
- Measures **B** to a few nanotesla against Earth's ~50,000 nT background
- Remanent magnetization in crustal rocks → magnetic anomalies → seafloor spreading history

**Heat flow probe:**
$$q = -k \frac{dT}{dz} \quad [\text{W/m}^2]$$
- Temperature gradient + thermal conductivity → surface heat flux
- Maps age-dependence of oceanic heat flow; geothermal resources

**Key point:** Each instrument records a field, not a property. The property requires a model.

---

# GPS and InSAR: Measuring Surface Deformation

**GPS (continuous):**
- Position accuracy: millimeters in 3D
- Time series: daily to sub-hourly at fixed stations
- Captures: interseismic strain (1–10 mm/yr), coseismic displacement (cm–m), postseismic relaxation, volcanic inflation, glacial rebound

**InSAR (spatially dense snapshots):**
- Satellite radar phase difference between two acquisitions → displacement map
- Covers: thousands of km² at cm–mm precision
- Limitation: line-of-sight only; temporal aliasing possible

**Key point:** GPS gives continuous time series at points; InSAR gives spatially dense maps at moments. Both are passive — the signal source is satellite navigation or microwave radar, not the Earth.

---

# The Forward Problem

**Given a model of Earth properties, predict the observations:**

$$\mathbf{d} = \mathbf{G}(\mathbf{m})$$

- $\mathbf{d}$ = observed data (travel times, gravity values, magnetic readings, ...)
- $\mathbf{m}$ = model parameters (density, velocity, conductivity at every point)
- $\mathbf{G}$ = physical operator derived from the governing equation

**Two examples:**

| Method | Model $\mathbf{m}$ | Operator $\mathbf{G}$ | Observable $\mathbf{d}$ |
|--------|------|------|------|
| Gravity | $\rho(\mathbf{r})$ | $\nabla^2\Phi = 4\pi G\rho$; $g = -\partial_z\Phi$ | $g(x,y)$ at surface |
| Travel time | $\alpha(\mathbf{r})$ | $t = \int ds/\alpha$ (ray tracing) | $t_P$ at stations |

**Key point:** The forward problem is well-posed — a unique answer exists for any given model. Solving it is computation, not inference.

---

# The Inverse Problem

**Given observations, infer the model:**

Find $\mathbf{m}$ such that $\mathbf{G}(\mathbf{m}) \approx \mathbf{d}$

This is **almost always non-unique** — many models fit the same data within measurement uncertainty.

**Gravity example:**
- Deeper, denser body ↔ shallower, less-dense body → identical surface $g$
- Solution requires additional constraints: drill data, geological knowledge, density bounds

**Tomography example:**
- Velocity anomalies smear along ray paths
- Resolution uneven where earthquakes or stations are sparse

Non-uniqueness is **not a failure** — it is a statement about what the data actually constrain.

**Key point:** Every geophysical inference requires additional constraints beyond the data alone. Characterizing what those constraints are, and what they imply, is the geophysicist's core scientific task.

---

# Three Pillars of Geophysical Science

<div class="columns">
<div>

**Theory & Computation**
- Derive governing equations
- Solve numerically for realistic geometries
- SPECFEM3D, ASPECT (open source)

**Field Observations**
- Deploy instruments, collect data
- CASIE21: active airguns + passive OBS on Cascadia margin
- PNSN: continuous Pacific Northwest monitoring

</div>
<div>

**Laboratory Experiments**
- Measure rock properties under pressure and temperature
- Diamond-anvil cells → lower mantle pressures
- Links tomographic images to real mineralogy

**No pillar is sufficient alone.** Theory without observation is speculation. Observation without theory is cataloguing. Lab data without field context is unanchored.

</div>
</div>

**Key point:** Geophysics advances through integration of all three modes — each constrains the others.

---

# Concept Check

1. A seismic reflection survey images a bright flat reflector at 2-second two-way travel time. What assumptions are embedded in concluding this is a sedimentary layer boundary? Name two that could be tested.

2. GPS stations on the Washington coast move eastward at ~10 mm/yr. Write out the forward problem: what is $\mathbf{m}$, what is $\mathbf{d}$, and what is $\mathbf{G}$?

3. A gravity survey shows a negative anomaly over a known salt dome (salt is less dense than surrounding sediment). Why cannot the gravity anomaly alone uniquely determine the dome's depth?

*Discuss in pairs — 5 minutes*

---

# Summary: Lecture 2 Key Takeaways

- The Kola Borehole (12 km) penetrated 0.19% of Earth's radius — everything deeper is from geophysical inference
- **Scale determines method**: no single technique spans 10–15 orders of magnitude in space and time
- The same material (mantle) is elastic on seismic timescales and viscous on convection timescales
- Five instruments: seismometer (ground motion), gravimeter ($g$), magnetometer (**B**), GPS/InSAR (displacement), heat flow probe ($q = -k\,dT/dz$)
- **Forward problem** $\mathbf{d} = \mathbf{G}(\mathbf{m})$: well-posed, unique; it is computation
- **Inverse problem** — almost always non-unique; requires additional constraints; characterizing non-uniqueness is a scientific obligation

---

# Further Reading

- Lowrie & Fichtner (2020) Ch. 1–2 — **free via UW Libraries**
- MIT OCW 12.201: [ocw.mit.edu/courses/12-201](https://ocw.mit.edu/courses/12-201-essentials-of-geophysics-fall-2004)
- Lehmann et al. (2024) Neural operators for seismic FWI: [doi.org/10.1029/2023JB027856](https://doi.org/10.1029/2023JB027856)
- SPECFEM3D open source: [github.com/geodynamics/specfem3d](https://github.com/geodynamics/specfem3d)
- CASIE21 experiment: [casie21.weebly.com](https://casie21.weebly.com)
- IRIS data services: [ds.iris.edu](https://ds.iris.edu)

**Lab 1 (Friday):** Fetch PNSN seismogram · Plot P and S arrivals · Compute source distance from $t_S - t_P = \Delta(1/\beta - 1/\alpha)$
