# Session 9 — The Inversion Problem and the Climate Problem

<span class="ess-badge ess-b-teal">Format A — Paper Autopsy</span>
<span class="ess-badge ess-b-blue">Week 9</span>
<span class="ess-badge ess-b-teal">Relevance: CO₂ storage · ML limits · Ill-posedness</span>

*4D seismic CO₂ monitoring · What ML can and can't replace · Two faces of ill-posedness*

---

```{admonition} Pre-read required
:class: warning
Students receive a **2-page excerpt** 48 hours before the session: a short excerpt from a 4D seismic CO₂ monitoring paper (SEG 2024 CCUS special section or LLNL geophysical monitoring report). Come prepared to discuss the figures and the inversion approach.
```

```{dropdown} Hook (0 – 7 min)
Show two synthetic seismic images of the same subsurface: one with a clear bright spot (CO₂ present), one ambiguous. Ask:

**"How confident are you CO₂ is present in the second image? What would change your confidence?"**

Let students argue before any explanation. Note where they use qualitative vs. quantitative reasoning.
```

```{dropdown} Discussion (7 – 42 min)
Three organizing questions:

**1.** Tikhonov regularization controls model smoothness. In CO₂ monitoring, do you want a smooth model or a rough one — and why? What does the choice reveal about the physics you believe?

**2.** This paper uses ML to improve the inversion. What does the ML replace, and what physical knowledge does it use or ignore? Is that a problem?

**3.** If you were advising a CO₂ storage operator on what geophysical monitoring program to design, what would you recommend? What is your single biggest source of uncertainty?

Push hardest on question 2 — the relationship between data-driven and physics-driven approaches is genuinely contested in the literature.
```

```{dropdown} Relevance
**Climate/Energy:** Carbon capture, utilization, and storage (CCUS) is a major component of net-zero pathways. 4D seismic monitoring is the primary method for verifying that injected CO₂ stays where it was put. Getting this wrong has regulatory and climate consequences.

**Basic science:** The ill-posedness of inverse problems — the fact that many models fit the same data — is one of the deepest ideas in geophysics. It connects directly to how we think about model uncertainty in climate projections: many climate models also fit historical observations while predicting different futures.
```

```{dropdown} Go Deeper
SEG 2024 CCUS special section · Anjom et al., *Geophysics* 2024 (ML in seismic exploration review)

**One name:** Dr. Felix Herrmann, Georgia Tech — seismic inversion with deep learning. His group's work exemplifies the physics-ML interface this session explores.
```
