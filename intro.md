# ESS 314 – Geophysics
## University of Washington, Spring 2026

**Instructor:** Marine Denolle (mdenolle@uw.edu) · **TA & Lab:** Emily Wilbur (ewilbur5@uw.edu) and Nicolas Chang (mehffin@uw.edu)  
**Meets:** Mon–Thu 1:30–2:20 pm · JHN 111

---

```{image} _static/images/ess314-front3.png
:width: 100%
:alt: ESS 314 Geophysics — marine seismic survey, coastline, subsurface structure, monitoring instruments
```


This is the open course companion for ESS 314. It collects lecture notes, lab notebooks, and Python demos in one place so that everything you need — derivations, figures, code, data — is reproducible and freely accessible.

Geophysics is the *physics of the inaccessible*. We cannot drill to the mantle, sample the outer core, or watch a fault slip in real time. Instead, we measure physical quantities at or near Earth's surface — the travel time of a seismic wave, the pull of gravity, the direction of a magnetic field — and use physical models to infer what lies beneath. Every chapter in this book follows that same logic: **observation → model → inference → interpretation**.

The course covers the solid Earth, from seismic waves and earthquake phenomenology through gravity, magnetics, heat flow, and plate tectonics. Throughout, we emphasize three habits of mind that define the discipline:

- **Physical reasoning first.** Equations are tools for making sense of the Earth, not ends in themselves. We always ask: *what does this formula actually say about rocks, faults, or fluids?*
- **Uncertainty is part of the answer.** Geophysical inference is non-unique. A good result includes an honest account of what the data cannot constrain.
- **Computation is part of the science.** Every major concept in this book has a companion Python notebook. We use [ObsPy](https://www.obspy.org), NumPy, SciPy, and Matplotlib — the same tools used in research.

A fourth thread runs through the whole course: **AI literacy**. Geophysics already uses machine learning for earthquake detection, phase picking, and tomographic imaging. We treat AI as a scientific tool that requires the same critical scrutiny as any other — you will practice using it, evaluating it, and knowing when not to trust it.

---

## How This Book Is Organized

| Module | Topics |
|--------|--------|
| **1 · Seismic Waves** | Wave types, ray theory, Snell's law, refraction & reflection |
| **2 · Subsurface Imaging** | Seismic refraction/reflection surveys, whole-Earth structure, tomography |
| **3 · Earthquake Phenomenology** | Earthquake location, ground motion, intensity, tsunami |
| **4 · Gravity** | Earth's gravity field, isostasy, gravity anomalies |
| **5 · Magnetism** | Earth's magnetic field, mineral magnetism, plate kinematics |
| **6 · Geodynamics & Tectonics** | Heat flow, divergent/convergent/transform margins, synthesis |

Each module contains lecture notes, a Python notebook, and a lab. Labs meet on Fridays; all materials are linked from Canvas.

---

## Prerequisites and Textbook

You should be comfortable with introductory calculus (through Math 126) and introductory physics (Phys 115/122 or equivalent). We will introduce new math as needed and always define notation before using it.

The recommended textbook is **Lowrie & Fichtner, *Fundamentals of Geophysics*, 3rd ed. (Cambridge, 2020)**, available free as an e-book through UW Libraries. The book assumes more mathematical maturity than this course requires; lecture notes here are written to be self-contained at the sophomore level.

---

## Learning Objectives and Outcomes

Each lecture in this book tags its content to one or more of the learning objectives (LO) and learning outcomes (LO-OUT) listed here. The tags appear at the top of every lecture file so you can see at a glance what each session is building toward — and trace any skill back to where it was first introduced.

### Learning Objectives

By the end of this course, students will be able to:

| ID | Learning Objective |
|----|--------------------|
| **LO-1** | Analyze and explain how geophysical observables (seismic travel times and amplitudes, gravity and magnetic anomalies, heat flow) arise from Earth properties and physical processes, including elastic structure, density variations, and thermal state. |
| **LO-2** | Apply simplified physical models and mathematical frameworks (ray geometry, wave propagation, potential fields, scaling analysis) to predict how subsurface structure influences observations and to solve first-order geophysical problems. |
| **LO-3** | Formulate the relationship between data, model parameters, and forward models; interpret residuals and misfit to evaluate how well a model explains observations; recognize non-uniqueness and uncertainty. |
| **LO-4** | Critically evaluate the strengths, assumptions, and limitations of core geophysical methods (seismic reflection/refraction/tomography, earthquake location, gravity, magnetics, heat-flow analysis) and determine their suitability for different Earth science questions and spatial scales. |
| **LO-5** | Use computational tools to implement forward models, explore parameter sensitivity, and compare model predictions with observations. |
| **LO-6** | Communicate geophysical reasoning and results clearly through figures, written reports, and discussion, including explicit statements of assumptions, uncertainties, and limitations. |
| **LO-7** | Use generative AI tools responsibly to support coding, visualization, and self-assessment while critically evaluating outputs, documenting use, and maintaining scientific integrity. |

### Learning Outcomes

These are the specific, demonstrable things you should be able to *do* by the end of the course:

| ID | Learning Outcome |
|----|-----------------|
| **LO-OUT-A** | Sketch a survey geometry and predict qualitatively how an interface, low-velocity zone, density contrast, or magnetized body will affect an observation. |
| **LO-OUT-B** | Compute simple travel times, ray paths, reflection/refraction geometry, or first-order gravity and magnetic responses. |
| **LO-OUT-C** | Explain why a method works physically, not just how to run it computationally. |
| **LO-OUT-D** | Set up a simple inverse problem by defining parameters, observations, a forward relation, and a residual. |
| **LO-OUT-E** | Interpret residuals and discuss non-uniqueness, uncertainty, and resolution in plain language. |
| **LO-OUT-F** | Decide which geophysical method is appropriate for a given Earth question and spatial scale. |
| **LO-OUT-G** | Produce a reproducible notebook or short report with labeled figures, units, assumptions, and interpretation. |
| **LO-OUT-H** | Critique a current research figure or an AI-generated explanation for correctness, limitations, and hidden assumptions. |

---

## A Note on Open Materials

All figures in this book are either generated from Python scripts (included in `assets/scripts/`) or sourced from openly licensed publications. No screenshots of paywalled figures appear here. If you find something that should be attributed differently, please open an issue on the course GitHub repository.

```{admonition} Getting started
:class: tip
The fastest way to run the notebooks is via the launch buttons at the top of each page (Binder or Google Colab). To work locally, clone the repository and install the environment with `pip install -r requirements.txt`.
```
