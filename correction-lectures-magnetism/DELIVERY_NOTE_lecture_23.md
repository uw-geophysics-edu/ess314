# Lecture 23 — Revision delivery note

**Date:** 2026-05-18  
**Scope:** Marine's feedback on the live lecture, addressed in one pass.

---

## What changed in `lectures/23_earth_magnetism.md`

| Section | Before | After |
|---|---|---|
| **§3** "Three sources, three wavelength regimes" | Opened straight with the wavelength regimes; spectrum-first. | Renamed **"Three Sources of Magnetism"**. Opens with new cross-section figure locating the three sources physically. Three labelled sub-sections (§3.1 core / §3.2 lithosphere / §3.3 ionosphere) discuss the physics of each source before §3.4 introduces the Mauersberger–Lowes spectrum as the *fingerprint* view. |
| **§5** "The mineral scale — five categories of magnetic ordering" | One-shot list of five ordering categories with a single figure. | Re-titled "**The mineral scale — why some rocks 'remember' the field and others do not**". Restructured into three sub-sections: **§5.1 A rock is an ensemble of minerals** (new figure), **§5.2 Two regimes — induced versus remanent magnetisation** (new figure, Königsberger ratio introduced), **§5.3 Five categories of magnetic ordering** (existing mineral-magnetism figure now serves to explain the atomic-scale origin of the two regimes). New admonition box lists PNW-specific mineral occurrences. |
| **§6** "Temperature unlocks (and locks in) magnetisation" | TRM with DRM and CRM mentioned as a brief afterthought. | Re-titled "**Remanent magnetisation — how rocks remember the field**". Restructured into four sub-sections — **§6.1 TRM** (with the revised Curie figure and an explicit "what does normalised mean?" callout), **§6.2 DRM** (sediments), **§6.3 CRM** (red beds), **§6.4 Other remanences** (IRM, VRM brief mention). All three primary mechanisms now sit at parallel structural depth. |
| **§10** Concept check | 3 questions. | 4 questions (added an induced-vs-remanent question that exercises the Königsberger framing). |
| Learning objective **LO-23.3** | "Distinguish the five categories of magnetic ordering …" | Reworded to lead with *induced vs. remanent* and the Königsberger ratio, with the five ordering categories as a sub-clause. |
| Front-matter `keywords` | … | Added `DRM`, `CRM`, `Königsberger ratio`. |
| Front-matter `open_sources` | … | Added Hunt, Moskowitz & Banerjee (1995) for the susceptibility ranges used in the rock-ensemble figure. |

## Figures: four scripts, four PNGs

| File | New / Revised | Purpose |
|---|---|---|
| `assets/scripts/fig_three_sources_cross_section.py` | **NEW** | Earth half-section locating the geodynamo, magnetised lithosphere, and ionospheric currents; opens §3. |
| `assets/scripts/fig_rock_as_ensemble.py` | **NEW** | Four-panel rock plate (basalt, granite, red bed sandstone, marine mudstone) with mineral assemblages, $k$ ranges, $Q$ ratios, and PNW context; opens §5.1. |
| `assets/scripts/fig_induced_vs_remanent.py` | **NEW** | M–H curves: linear induced response on the left, hysteresis loop with $M_r$ and $H_c$ on the right; anchors §5.2. |
| `assets/scripts/fig_trm_curie.py` | **REVISED** | Curie/blocking figure with x-axis reversed so **cooling reads left → right**, and an explicit "Why ‘normalised’?" inset explaining $J/J_s(0)$; PNW Curie temperatures consolidated into a single annotation box rather than clipped axis ticks. |

All four follow the project quality gate: 13 pt base font (no argument below 11 pt), WCAG AA colorblind-safe palette, `fig.tight_layout()` before `savefig()`, `bbox_inches="tight"` only at `savefig()` call site, explicit `loc=` on every legend.

## BibTeX entry to add to `references.bib`

The new figure script `fig_rock_as_ensemble.py` cites Hunt et al. (1995) for its susceptibility ranges. The lecture's bibliography filter expects the key `hunt1995magprops`. Add this entry to `references.bib`:

```bibtex
@incollection{hunt1995magprops,
  author    = {Hunt, Christopher P. and Moskowitz, Bruce M. and Banerjee, Subir K.},
  title     = {Magnetic Properties of Rocks and Minerals},
  booktitle = {Rock Physics and Phase Relations: A Handbook of Physical Constants},
  editor    = {Ahrens, Thomas J.},
  series    = {AGU Reference Shelf},
  volume    = {3},
  pages     = {189--204},
  publisher = {American Geophysical Union},
  address   = {Washington, DC},
  year      = {1995},
  doi       = {10.1029/RF003p0189}
}
```

## What was deferred (per Marine's "we'll iterate next")

- **Slide deck** (`slides/lecture_23_slides.md`). The slide deck currently still has the original §3 structure (the slide titled "Three sources, three wavelength regimes" with empty/broken inline equations) and the original §5/§6 framing. The revised lecture is the source of truth; the slide deck can be rebuilt in the next iteration with these new figures dropped in.
- **Updated concept-check answer key** in `ess314-instructor/concept_check_lecture23.md` (new Q3 on Königsberger / induced-vs-remanent now needs a worked answer).
- **Actual photographs** of rock samples. Marine asked for "actual photos of what these rocks might look like." The current `fig_rock_as_ensemble.png` uses Python-generated schematic hand-sample views with realistic mineral colour palettes; this complies with the project's Python-first copyright stance. If true photographs are wanted, the cleanest open-licensed path is the USGS Photo Library or the National Park Service Geology Image Library — both fully public-domain — with per-image verification before commit.

## Files touched / produced

```
ess314/
├── lectures/
│   └── 23_earth_magnetism.md                       # REVISED
└── assets/
    ├── scripts/
    │   ├── fig_three_sources_cross_section.py       # NEW
    │   ├── fig_rock_as_ensemble.py                  # NEW
    │   ├── fig_induced_vs_remanent.py               # NEW
    │   └── fig_trm_curie.py                         # REVISED
    └── figures/
        ├── fig_three_sources_cross_section.png      # NEW
        ├── fig_rock_as_ensemble.png                 # NEW
        ├── fig_induced_vs_remanent.png              # NEW
        └── fig_trm_curie.png                        # REVISED (cooling L→R)
```

The existing figures `fig_dipole_field_geometry.png`, `fig_field_power_spectrum.png`, `fig_seattle_secular_variation.png`, `fig_mineral_magnetism.png`, and `fig_paleolatitude_from_inclination.png` are unchanged and still referenced from the revised lecture.
