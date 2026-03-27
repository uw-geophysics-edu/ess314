---
title: "ESS 314 – Geophysics: Course Syllabus"
subtitle: "Spring 2026 · University of Washington"
---

# ESS 314 – Geophysics

**Spring 2026 · 5 Credits · MoTuWTh 1:30–2:20 pm · JHN 111**

| | |
|---|---|
| **Instructor** | Marine Denolle — mdenolle@uw.edu · ATG 204 · Office hours by appointment |
| **Teaching Assistant** | Emily Wilbur |
| **Course website** | [Canvas](https://canvas.uw.edu/courses/1883586) — all materials, assignments, and announcements |

---

## Course Description

ESS 314 introduces geophysics as the physics of learning about the Earth from indirect measurements. We study how seismic waves, gravity, magnetic fields, heat flow, and related observations respond to subsurface structure and material properties, and how geophysicists use models to infer Earth structure and physical processes from those observations.

Topics include seismic reflection, refraction, and travel-time tomography; earthquakes and Earth structure; gravity and magnetic anomalies; heat flow, buoyancy, and isostasy; and tectonic interpretation.

The course emphasizes physical intuition, simple quantitative models, computational exploration, uncertainty, and the logic of geophysical inference: *what we measure, how we model it, what assumptions are built in, and how we decide whether a model explains the data.*

**Prerequisites:** PHYS 122 or 115 & 118; MATH 126, 136, or ESS 310.

---

## Learning Objectives

By the end of this course, students will be able to:

**LO-1 · Analyze and explain geophysical observations**
Analyze and explain how geophysical observables (seismic travel times and amplitudes, gravity and magnetic anomalies, heat flow) arise from Earth properties and physical processes, including elastic structure, density variations, and thermal state.

**LO-2 · Apply physical and mathematical models**
Apply simplified physical models and mathematical frameworks (ray geometry, wave propagation, potential fields, scaling analysis) to predict how subsurface structure influences observations and to solve first-order geophysical problems.

**LO-3 · Formulate and interpret geophysical inference problems**
Formulate the relationship between data, model parameters, and forward models; interpret residuals and misfit to evaluate how well models explain observations; recognize non-uniqueness and uncertainty.

**LO-4 · Evaluate geophysical methods and their limitations**
Critically evaluate the strengths, assumptions, and limitations of core geophysical methods (seismic reflection/refraction/tomography, earthquake location, gravity, magnetics, heat-flow analysis) and determine their suitability for different Earth science questions and spatial scales.

**LO-5 · Use computational tools**
Use computational tools to implement forward models, explore parameter sensitivity, and compare predictions with observations.

**LO-6 · Communicate geophysical interpretations**
Communicate geophysical reasoning and results clearly through figures, written reports, and discussion, including explicit statements of assumptions, uncertainties, and limitations.

**LO-7 · Use generative AI tools responsibly**
Use generative AI tools to support coding, visualization, and self-assessment while critically evaluating outputs, documenting use, and maintaining scientific integrity.

---

## Learning Outcomes

By the end of this course you will be able to:

- Sketch a survey geometry and predict qualitatively how an interface, low-velocity zone, density contrast, or magnetized body will affect an observation.
- Compute simple travel times, ray paths, reflection/refraction geometry, or first-order gravity/magnetic responses.
- Explain *why* a method works physically, not just how to run it computationally.
- Set up a simple inverse problem by defining parameters, observations, a forward relation, and a residual.
- Interpret residuals and discuss non-uniqueness, uncertainty, and resolution in plain language.
- Decide which method is appropriate for a given Earth question and scale.
- Produce a reproducible notebook or short report with labeled figures, units, assumptions, and interpretation.
- Critique a current research figure or an AI-generated explanation for correctness, limitations, and hidden assumptions.

---

## Course Materials

**Textbook (recommended, not required)**
Lowrie & Fichtner, *Fundamentals of Geophysics*, 3rd ed. Available for free online reading via UW Libraries.

Additional readings (articles, book chapters) will be posted on Canvas or accessible via UW Libraries.

**Software and Technology**
- Python (via VSCode or UW JupyterHub)
- Reliable access to Canvas and UW email
- Local laptop + VSCode + Python strongly recommended

---

## Course Structure

**Lectures** meet four times weekly (Mon–Thu). Class materials are hosted on the course GitHub repository and linked JupyterBook, with everything linked through Canvas.

**Laboratory Sessions** provide weekly hands-on computing experience. Labs meet on Fridays. *Attendance is required to earn lab credit.*

**Discussion Sections** meet Wednesdays at 1:30 pm. Sections involve scientific literature reading, guest lectures, group activities connecting basic research to societal topics, communication workshops, and open problem framing. The Wednesday timeslot may swap with a lecture when the instructor travels.

**Participation** is graded on quality of engagement, not attendance alone. A rubric will be provided. Respectful dialogue and attentive listening are part of participation.

---

## Grading

| Component | Weight |
|---|---|
| Online tests / quizzes | 25% |
| Homework / assignments | 15% |
| Laboratory reports | 30% |
| Final project / paper | 20% |
| Participation and engagement | 10% |

Grades are reported on the UW 4.0 scale. **No curve is applied.**

**Final Project** includes a written report, a GitHub repository, and an in-class presentation. Graded on depth of research, analysis, and communication.

**Lab Reports** are graded on clarity, accuracy, and completeness. Lab attendance is required to earn credit for that week.

**Extra Credit** opportunities, if offered, are available to all students equally and will not replace core assignments.

**Incomplete Grades** are only assigned if you have completed satisfactory work through the last two weeks and are unable to finish due to illness or circumstances beyond your control. A written agreement with a completion timeline is required. See [UW Registrar Incomplete Policy](https://registrar.washington.edu/grades/incomplete-grade-policy/).

---

## Late Work and Make-up Policy

Work is due on the dates specified. Contact the instructor *before* a deadline if you anticipate difficulty — in many cases an extension can be granted for legitimate reasons. Without prior arrangement, late work may lose 10% per day and will not be accepted more than one week past the deadline.

Make-up exams or quizzes are only offered for verified, excused absences. Notify the instructor as soon as possible — preferably before the exam. Unexcused missed exams receive a zero.

---

## Course Schedule

Shading key: **Discussion section** · *Holiday* · Lab on Fridays

### Introduction to Geophysical Methods

| # | Date | Topic |
|---|---|---|
| 1 | Mon 3/30 | Introduction to the Course |
| 2 | Tue 3/31 | What is Geophysics? — Basics of Geophysical Concepts |
| 3 | Wed 4/1 | **Discussion — Why does the Earth make noise? Opening the field** |

### Seismic Waves, Refraction, and Reflection

| # | Date | Topic |
|---|---|---|
| 4 | Thu 4/2 | Seismic Waves — the basics |
| 5 | Fri 4/3 | *Lab 1: Introduction to Python* |
| 6 | Mon 4/6 | Wavefronts and Rays |
| 7 | Tue 4/7 | Snell's Law & Waves at Boundaries |
| 8 | Wed 4/8 | **Discussion — Radar eyes on ice: a different kind of reflection survey** |

### Subsurface Imaging

| # | Date | Topic |
|---|---|---|
| 9 | Thu 4/9 | Seismic Refraction I |
| 10 | Fri 4/10 | *Lab 2: Intro to Python II and Seismic Ray Tracing* |
| 11 | Mon 4/13 | Seismic Refraction II |
| 12 | Tue 4/14 | Introduction to Seismic Reflection |
| 13 | Wed 4/15 | **Discussion — Guest: A PhD student's first year in geophysics research** |
| 14 | Thu 4/16 | Seismic Reflections I |
| 15 | Fri 4/17 | *Lab 3: Refraction* |
| 16 | Mon 4/20 | Seismic Reflections II |
| 17 | Tue 4/21 | Whole Earth Structure I |
| 18 | Wed 4/22 | Whole Earth Structure II |
| 19 | Thu 4/23 | **Discussion — Inside the planet: what we know, what we don't, and why it matters** |
| 20 | Fri 4/24 | *Lab 4: Reflection* |
| 21 | Mon 4/27 | Seismic Tomography |

### Earthquake Phenomenology

| # | Date | Topic |
|---|---|---|
| 22 | Tue 4/28 | Earthquake Phenomena I |
| 23 | Wed 4/29 | **Discussion — Weighing the Earth: gravity, ice sheets, and CO₂** |
| 24 | Thu 4/30 | Earthquake Phenomena II |
| 25 | Fri 5/1 | *Lab 5: Earthquake Location* |
| 26 | Mon 5/4 | Ground Motions, Intensities, and Building Damage |
| 27 | Tue 5/5 | Tsunami |
| 28 | Wed 5/6 | **Discussion — Guest: A Pacific Northwest industry geophysicist** |

### Gravity

| # | Date | Topic |
|---|---|---|
| 29 | Thu 5/7 | Earth's Gravity |
| 30 | Fri 5/8 | *Lab 6: AI Literacy (remote / async)* |
| 31 | Mon 5/11 | Gravity II — Isostasy |
| 32 | Tue 5/12 | Using Gravity to Detect Anomalies I |
| 33 | Wed 5/13 | **Discussion — Explaining geophysics to someone who doesn't care (yet)** |
| 34 | Thu 5/14 | Using Gravity to Detect Anomalies II |
| 35 | Fri 5/15 | *Lab 7: Gravity* |

### Magnetism

| # | Date | Topic |
|---|---|---|
| 36 | Mon 5/18 | Density, Isostasy, and the Lithosphere |
| 37 | Tue 5/19 | Earth Magnetism & Mineral Magnetism |
| 38 | Wed 5/20 | **Discussion — Guest: A glaciologist / cryosphere geophysicist** |
| 39 | Thu 5/21 | The Magnetic Field, Magnetism, and Tectonic Plates |
| 40 | Fri 5/22 | *Lab 8: Magnetics* |

### Geodynamics and Tectonics — Synthesis

| # | Date | Topic |
|---|---|---|
| — | Mon 5/25 | *Memorial Day — No Class* |
| 41 | Tue 5/26 | Heat in the Earth and Geodynamics |
| 42 | Wed 5/27 | **Discussion — The inversion problem and the climate problem: two faces of ill-posedness** |
| 43 | Thu 5/28 | Plate Tectonics: Divergent Margins and Mid-Ocean Ridges |
| 44 | Fri 5/29 | *No Lab* |
| 45 | Mon 6/1 | Plate Tectonics: Convergent Margins, Subduction, and Seismotectonics |
| 46 | Tue 6/2 | Plate Tectonics: Transform Faults and Intraplate Processes |
| 47 | Wed 6/3 | **Discussion — The elevator pitch: your capstone, your story, your field** |
| 48 | Thu 6/4 | Putting it Together: Geophysics as a Tool for Earth Structure |
| 49 | Fri 6/5 | Student Presentations / Course Wrap-Up |

:::{note}
This schedule is a plan — it may be adjusted as needed. Changes will be announced on Canvas in advance.
:::

---

## University Policies

### Participation and Attendance

Students are expected to participate actively and come prepared (readings, prep work done). Inform the instructor and TA as soon as possible if you must miss class due to illness, family emergency, religious observance, or a university-sponsored activity. You are responsible for catching up on missed material.

### Religious Accommodations

Washington state law requires accommodation of absences for faith, conscience, or organized religious activities. Submit requests within the first two weeks via the [UW Religious Accommodations Request Form](https://registrar.washington.edu/students/religious-accommodations-request/).

### Disability Access and Accommodations

It is UW policy to create inclusive and accessible learning environments. If you have established accommodations with **Disability Resources for Students (DRS)**, activate them in myDRS and contact the instructor early in the term. To initiate the process, visit [disability.uw.edu](https://disability.uw.edu). All discussions are confidential.

### Academic Integrity

All submitted work must be your own and properly cited. Academic misconduct includes cheating, plagiarism, unauthorized collaboration, falsifying data, submitting the same work for multiple classes without permission, and uploading course materials to third-party study sites (Course Hero, Chegg, etc.). When in doubt, ask before proceeding. Suspected violations are handled under the [UW Student Conduct Code (WAC 478-121)](https://www.washington.edu/cssc/for-students/student-code-of-conduct/).

### Use of Generative AI Tools

AI tools (ChatGPT, Claude, Copilot, etc.) are **allowed with limitations** in this course. Each assignment will state whether AI tools are permitted and in what manner. **All AI-generated content must be cited** (e.g., "ChatGPT, personal communication, date"). Using AI beyond the allowed scope or without citation is academic misconduct. AI-generated content can be inaccurate — you are responsible for verifying any information and ensuring it meets assignment requirements.

### Use of Course Materials and Copyright

Course materials (slides, notes, recordings, assignments, exams) are for your personal learning only. Do not share or post them online without explicit permission. Sharing your own study notes with classmates is fine; posting instructor-provided materials to public forums is not.

### Title IX and Preventing Sexual Harassment

UW prohibits sex discrimination and sex-based harassment in any form. If you or someone you know experiences sexual harassment or assault, contact the [UW Title IX Office](https://www.washington.edu/titleix/) or email titleix@uw.edu. For confidential support, contact a UW Confidential Advocate. Note that instructors and TAs are Responsible Employees required to report disclosures to the Title IX Office.

### Safety and Wellness

Your well-being matters. If you feel unsafe or threatened, contact **SafeCampus** at 206-685-7233 (24/7). For health and wellness support including mental health counseling, visit [Husky Health & Well-Being](https://wellbeing.uw.edu).
