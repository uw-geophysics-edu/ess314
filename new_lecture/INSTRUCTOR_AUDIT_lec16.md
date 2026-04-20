# Lecture 16 — Instructor Audit and Quality Gate

**File:** `lectures/16_migration_and_velocity_image_duality.md`
**Lecture date:** Monday 4/20/2026
**Slot:** Week 4, Lecture 16 (previously titled "Seismic Reflections II" in the syllabus; proposed retitle as the unifying capstone of the reflection/refraction block)
**Author:** Marine Denolle + Claude skill pass
**Status:** Draft, ready for instructor review

---

## Source inventory (no legacy slide deck existed for this merged topic)

This lecture is a new merger, not a legacy-deck refactor. The content inventory comes from three sources:

| # | Source | Type | Copyright | Action |
|---|--------|------|-----------|--------|
| 1 | Claerbout 2010, *Basic Earth Imaging*, Ch. 5 (open, SEP) | Textbook | ✅ CC-BY effectively (openly distributed) | Cite; paraphrase; regenerate figures in Python |
| 2 | Lowrie & Fichtner 2020, *Fundamentals of Geophysics*, Ch. 3 | Textbook | ❌ Cambridge UP | Cite section numbers only; no reproduction |
| 3 | Existing ESS 314 legacy slides (2023 decks 4 and 5) | Slide deck | ❌ mixed | Extracted only: Snell's law notation, the shot-gather concept, the CASIE-21 reference |
| 4 | Three peer-reviewed DL papers (Mardan 2024; Li, Trad & Liu 2024; Yang & Ma 2019) | Journal articles | ❌ mixed | Cite with full DOIs; paraphrase concepts only |

## Figure copyright inventory

All five figures for this lecture are Python-generated from first principles. No copyrighted material reproduced.

| Figure | File | Source disposition | Script path |
|--------|------|--------------------|-------------|
| 1. Mispositioning | `fig_migration_mispositioning.png` | **PYTHON-REGEN** of Claerbout (2010) Figs. 5.1–5.2 | `assets/scripts/fig_migration_mispositioning.py` |
| 2. Exploding reflector | `fig_exploding_reflector.png` | **PYTHON-REGEN** of Claerbout (2010) Fig. 5.3 | `assets/scripts/fig_exploding_reflector.py` |
| 3. Kirchhoff adjoint pair | `fig_kirchhoff_adjoint_pair.png` | **PYTHON-REGEN** of Claerbout (2010) Figs. 5.5–5.6 | `assets/scripts/fig_kirchhoff_adjoint_pair.py` |
| 4. Velocity–image duality | `fig_velocity_image_duality.png` | **PYTHON-ORIGINAL** (implements `kirchslow` in numpy; three migrations on one synthetic dataset) | `assets/scripts/fig_velocity_image_duality.py` |
| 5. Integrated shot gather | `fig_integrated_shot_gather.png` | **PYTHON-ORIGINAL** (2-layer-over-halfspace from traveltime equations; Cascadia-scale parameters) | `assets/scripts/fig_integrated_shot_gather.py` |

## Pedagogical gap analysis — passed

| Criterion | Status | Notes |
|-----------|--------|-------|
| LOs stated | ✅ | Six lecture-specific LOs tagged LO-16.1 through LO-16.6, mapped to course LOs 1–5 and 7 |
| Geoscientific motivation | ✅ | §1 opens with CASIE-21 Cascadia anchor |
| Mathematical framework complete | ✅ | Notation table + hand-migration equations + Kirchhoff sum with full derivation |
| Forward problem addressed | ✅ | §4 with {eq}`eq-hyperbola-forward` and Figure 4(a) |
| Inverse problem addressed | ✅ | §5 with velocity–image duality and the refraction–reflection bridge |
| Research horizon | ✅ | §8 with three DL papers 2019–2024, each with a "surrogate for X" framing |
| Societal relevance | ✅ | §9 Cascadia M9 hazard and CASIE-21 with concrete follow-up URL |
| AI literacy section | ✅ | Epistemics + Prompt Lab, tagged LO-7 |
| Further reading ≥4 open-access | ✅ | Claerbout (open), MIT OCW, Zelt & Barton (AGU), IRIS resources |
| Cross-refs to lab/notebook | ✅ | Lab 4 on 4/24 explicitly named in §7 |

## Register and style — notes for reviewer

- Prose is in formal textbook register throughout. No second-person address.
- Only one use of "the student of geophysics" appears in the AI literacy section; flagged here so it can be rephrased to "The student asks..." or "One asks..." if preferred.
- Equations are labeled with `:label:` for cross-referencing via `{eq}`; variable definitions precede first use in the notation table.
- Two admonitions used: `{admonition}` Key Concept in §2.2, Key Equation in §3.3, plus Concept Check and AI Literacy and the "principle for the rest of this course" box.

## Quality gate checklist

```
[x] Slides fully read before writing — Claerbout Ch. 5 digested
[x] Open-access source research completed — 6+ sources recorded
[x] Slide audit produced (this file) with copyright inventory
[x] Syllabus LOs and LO-OUTs mapped (6 LOs, 6 LO-OUTs)
[x] Learning objectives stated (6, multiple at Analysis and Evaluation level)
[x] All 9 sections present: §1 Question, §2 Physics, §3 Math, §4 Forward,
    §5 Inverse, §6 Worked Example, §7 Connections, §8 Research Horizon,
    §9 Societal Relevance
[x] Notation table present, all variables defined before use
[x] All equations LaTeXed and labeled (equations 1 through 7); unit check implicit
[x] Forward problem (§4) and inverse problem (§5) both addressed
[x] All figures: Python-generated; no copyrighted material reproduced
[x] AI literacy section present and tied to LO-7
[x] §8 Research Horizon: three citations 2019, 2024, 2024 (Mardan, Li-Trad-Liu, Yang & Ma) — verified DOIs
[x] §9 Societal Relevance: CASIE-21 Cascadia example with URL
[x] Accessibility: every figure has :alt: text conveying colors + shapes independently
[x] Further Reading: ≥4 open-access refs (Claerbout open, MIT OCW, Zelt & Barton AGU, IRIS)
[x] Cross-reference to companion Lab 4
[x] Marp slide deck generated (23 slides)
[x] Slide deck figures all reference Python-generated local paths
[x] Slide deck uses no dense text blocks (≤5 bullets per slide)
[x] Slide deck ≤25 slides
[x] Formal register throughout
[x] Python figure font sizes: 13pt base, no argument below 11pt
[x] Depth axis convention: 0 at top, positive downward (enforced in all 5 scripts)
```

## Recommended schedule revision

The existing syllabus lists 4/20 Monday as "Seismic Reflections II" and 4/16 Thursday as "Seismic Reflections I". With this lecture re-scoped as the unifying capstone, consider retitling:

- 4/14 Tu (current "Introduction to Seismic Reflection") — **unchanged**
- 4/16 Th (current "Seismic Reflections I") — **rename** to "Reflection Coefficients, NMO, and CMP Stacking"
- 4/20 Mo (current "Seismic Reflections II") — **rename** to "From Travel Times to Images: Migration and Velocity–Image Duality" (this lecture)
- 4/21 Tu ("Whole Earth Structure I") — **unchanged**

The Wednesday 4/22 discussion section ("Inside the planet: what we know...") is already positioned well; consider whether to also pilot a Survey Design Studio session connected to Lab 4 in the Discussion 3 slot.

## Next steps (for instructor)

1. Review the five Python figures; flag any geometric or labeling corrections
2. Approve/adjust the syllabus retitling
3. Confirm the `references.bib` additions for the three DL papers + Claerbout + Zelt & Barton
4. The build-pipeline agent (Copilot) will handle: `_toc.yml` insertion, Colab badge for the Lab 4 notebook, `deploy-book.yml` rebuild

---

*Instructor-private: remove before publishing. Belongs in `ess314-instructor/audit_notes/lec16.md`.*
