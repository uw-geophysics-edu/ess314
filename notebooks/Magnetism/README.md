# Magnetism — figure-generation scripts (Module 6)

This folder contains the Python scripts used to generate every figure in
**Lecture 23 (Earth Magnetism)** and **Lecture 24 (Magnetism & Tectonics)**.

Each script is self-contained: it builds a synthetic toy model (induced
dipole anomaly, geomagnetic polarity timescale + JdF stripes, paleolatitude
inversion, TRM cooling curve, etc.) using only `numpy` and `matplotlib`,
and writes a 300 DPI PNG into `assets/figures/`. They are copied here so
that students can open them, tweak parameters, and re-run individual
figures as part of homework, the final project, or independent exploration.

## Running a script

From the repo root:

```bash
pixi run python notebooks/Magnetism/fig_dipole_anomaly_shapes.py
```

The script will write its PNG into `assets/figures/` (relative path —
always launch from the repo root).

## Scripts and the concepts they illustrate

| Script | Lecture | Concept |
|---|---|---|
| `fig_dipole_field_geometry.py` | 23 §2 | Dipole field lines, (D, I, F) decomposition at a station |
| `fig_field_power_spectrum.py` | 23 §2 | Lowes–Mauersberger power spectrum → core / crust / ionosphere |
| `fig_seattle_secular_variation.py` | 23 §3 | IGRF time series at Seattle (1955–2026) |
| `fig_mineral_magnetism.py` | 23 §4 | Dia-/para-/ferro-/antiferro-/ferrimagnetic ordering |
| `fig_trm_curie.py` | 23 §5 | Thermoremanent magnetization and Curie blocking |
| `fig_paleolatitude_from_inclination.py` | 23 §6 | $\tan I = 2 \tan \lambda$ forward + inverse |
| `fig_dipole_anomaly_shapes.py` | 24 §3 | Induced-dipole anomaly vs latitude (equator/mid/pole) |
| `fig_reduction_to_pole.py` | 24 §4 | Reduction-to-pole transformation |
| `fig_magnetic_halfwidth.py` | 24 §5 | Half-width depth rule and noise propagation |
| `fig_magnetic_ensemble.py` | 24 §5 | $\chi^2$ ensemble + $m \propto z^3$ trade-off |
| `fig_jdf_stripes.py` | 24 §7 | Vine–Matthews stripes across the Juan de Fuca Ridge |

## Notes

- These are **figure generators**, not full notebooks. They are kept as
  `.py` files (not `.ipynb`) so they remain easy to diff, re-run from the
  command line, and version-control cleanly. Open them in JupyterLab and
  run cell-by-cell with `# %%` cell markers, or convert with
  `jupytext --to ipynb fig_*.py` if you prefer notebook form.
- The canonical copies used by the JupyterBook build live in
  `assets/scripts/`. The copies here are for student exploration.
