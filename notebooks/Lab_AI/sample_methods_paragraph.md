# Part 6 — Sample Methods Paragraph (intentionally weak)

The paragraph below is drawn from a real-style undergraduate report on a
multi-disciplinary geophysical survey. It is intentionally weak in
several ways — vague, missing parameters, missing software versions,
missing data provenance. Your job in Part 6 is to design a
"Methods Reviewer" AI agent that catches these weaknesses
automatically.

This paragraph is your **test case** for the agent. Do *not* fix the
paragraph yourself — feed it to your agent and evaluate whether the
agent's critique would be useful to a peer reviewer.

---

## Methods (excerpt from a hypothetical student report)

> We collected seismic refraction and reflection data along a survey
> line crossing the eastern flank of a Cascade volcano. The geophone
> array was deployed at the surface and we shot the line with a
> seismic source. The data were processed using standard methods in
> Python.  First arrivals were picked from the shot gathers, and we
> fit lines on a T–x plot to derive velocities. We also picked
> reflection events and applied NMO correction to remove the
> hyperbolic moveout. The velocities were then used to estimate the
> depth to the bedrock interface, which we found to be at a few tens
> of meters.
>
> Gravity data were collected at the same stations as the seismic
> survey, using a gravimeter. We applied the standard Bouguer
> correction, terrain correction, and latitude correction to obtain a
> Bouguer anomaly map. The gravity data showed a low anomaly over the
> western half of the survey, which we attributed to a low-density
> body. Magnetic data were collected with a magnetometer and processed
> in the usual way. We then interpreted all three datasets jointly to
> constrain the geometry of the subsurface magmatic system.

---

## Why this paragraph is a useful test case

A real reviewer reading this paragraph would have questions:

- Which seismic source was used (sledgehammer, weight drop, explosive,
  vibroseis)?
- What was the geophone spacing? Shot interval? Total line length?
- Which Python package handled the processing? With what version?
  Was the inversion linear, MASW, or tomographic?
- What filter was applied before picking? Corner frequencies?
- What is "a few tens of meters" quantitatively? With what uncertainty?
- What density was assumed for the Bouguer correction?
- Where was the magnetic survey calibrated? Diurnal correction applied?
- Where are the data stored? DOI, URL, repository?
- Which coordinate reference system?

These are exactly the kinds of issues a well-designed methods reviewer
agent should flag. If your v0 agent only flags one or two of them,
that's normal — iterating the agent until v1 catches more is itself a
learning artifact, and is what you will do in Week 8.
