"""
fig_seattle_basin.py

Scientific content: A schematic isostatic-residual gravity profile across the
Seattle Basin (E–W transect across Puget Lowland), illustrating the
characteristic large-amplitude (~50 mGal), broad-wavelength low produced by
several kilometres of low-density Quaternary and Eocene sediments.

This figure replaces a screenshot from the original course slide deck (whose
provenance traced to Blakely et al., 2002, GSA Bulletin, paywalled).
The profile shape and amplitude here are illustrative — sized to match
published values from open-access USGS reports — but the underlying numerical
data are synthetic (no proprietary data are reproduced).

Key open-access source for the science:
  Brocher, T.M., Wells, R.E., Lamb, A.P. & Weaver, C.S. (2017). Evidence for
  distributed clockwise rotation of the crust in the northwestern United
  States from fault geometries and focal mechanisms. Tectonics 36, 787–818.
  https://doi.org/10.1002/2016TC004223  (open access, AGU)
  USGS Open-File Report 02-401: Blakely, R.J. et al. — public domain.

Output:  assets/figures/fig_seattle_basin.png
License: CC-BY 4.0
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.size":       13,
    "axes.titlesize":  15,
    "axes.labelsize":  13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi":      150,
    "savefig.dpi":     300,
})

C_BLUE, C_ORANGE, C_SKY, C_GREEN, C_VERM, C_PINK, C_BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73",
    "#D55E00", "#CC79A7", "#000000",
)

# ── Synthetic basin geometry (E–W across Puget Sound region) ───────────────
x = np.linspace(-60, 60, 601)               # km, x=0 is basin centre

# Asymmetric basin floor: deeper on the south side (Seattle Fault N-vergent)
def basin_floor(x):
    """Return basin depth (m) below sea level."""
    main = 7000.0 / (1.0 + ((x + 5.0) / 22.0)**4)
    asym = 1500.0 * np.tanh(-(x - 5.0) / 12.0)        # asymmetric step
    return np.maximum(0.0, main + asym)

H = basin_floor(x)
H_smooth = np.where(H < 0, 0, H)

# ── Forward model: gravity anomaly from a 2-D variable-thickness slab ──────
# Density contrast Δρ = -400 kg/m³ (sediments vs. crystalline basement)
G   = 6.67430e-11
drho = -400.0

# 2-D gravity from a horizontal slab of thickness t at depth z_top is, to a
# good approximation: Δg = 2π G Δρ t (a flat-slab limit).
# For a basin of variable thickness we approximate by integrating the local
# slab with a half-width-dependent attenuation. Here we use a simple
# Gauss-broadened Bouguer term — adequate for an illustrative profile.
def basin_anomaly(x_km, H_m, drho, smoothing_km=8.0):
    bouguer_local = 2.0 * np.pi * G * drho * H_m * 1e5     # mGal
    # Smooth in x to mimic the sensitivity-kernel half-width of a basin
    sigma = smoothing_km / np.diff(x_km)[0]
    from scipy.ndimage import gaussian_filter1d
    return gaussian_filter1d(bouguer_local, sigma=sigma)

dg = basin_anomaly(x, H, drho)

# Add a regional gradient (mantle roots toward Cascades) — broad linear trend
regional = 0.3 * x                                 # mGal/km (illustrative)
dg_total = dg + regional
# Detrend to obtain "isostatic residual"
slope, intercept = np.polyfit(x, dg_total, 1)
dg_residual = dg_total - (slope * x + intercept)

# ── Figure: profile + cross-section ────────────────────────────────────────
fig, (ax_g, ax_geol) = plt.subplots(2, 1, figsize=(11, 7.5),
                                     gridspec_kw={"height_ratios": [1.0, 1.2],
                                                  "hspace": 0.30})

# (a) Gravity profile
ax_g.plot(x, dg_total, color=C_BLUE, lw=2.2, label="Modelled Bouguer anomaly")
ax_g.plot(x, dg_residual, color=C_VERM, lw=2.2,
          label="Isostatic residual (regional removed)")
ax_g.axhline(0, color=C_BLACK, lw=0.6, ls="--")
ax_g.set_xlabel("E–W distance from basin centre  (km)")
ax_g.set_ylabel(r"Gravity anomaly  (mGal)")
ax_g.set_title("(a)  Schematic gravity profile across the Seattle Basin",
                loc="left")
ax_g.legend(loc="lower right")
ax_g.grid(ls=":", lw=0.6, alpha=0.5)
ax_g.set_xlim(x.min(), x.max())

# Annotation
i_min = np.argmin(dg_residual)
ax_g.annotate(f"Basin gravity low\n(~{dg_residual.min():.0f} mGal)",
              xy=(x[i_min], dg_residual[i_min]),
              xytext=(-50, -52),
              arrowprops=dict(arrowstyle="->", color=C_BLACK, lw=0.9),
              fontsize=11, ha="left")

# (b) Geology cross-section
ax_geol.fill_between(x, np.full_like(H, 0), -H,
                      color=C_ORANGE, alpha=0.55,
                      label=r"Sediments  $\rho \approx 2.3$ g cm$^{-3}$")
ax_geol.fill_between(x, -H, np.full_like(H, -10000),
                      color=C_SKY, alpha=0.45,
                      label=r"Basement  $\rho \approx 2.7$ g cm$^{-3}$")
ax_geol.axhline(0, color=C_BLACK, lw=0.8)
# Mark Seattle Fault Zone (synthetic location, illustrative)
ax_geol.axvline(8, color=C_VERM, lw=2.0, ls="--",
                 label="Seattle Fault Zone (schematic)")
ax_geol.text(8.5, -8500, "SFZ", color=C_VERM, fontsize=12, fontweight="bold")
ax_geol.set_xlabel("E–W distance from basin centre  (km)")
ax_geol.set_ylabel("Depth  (m)")
ax_geol.set_title("(b)  Cross-section through the basin (illustrative)",
                   loc="left")
ax_geol.legend(loc="lower right", framealpha=0.95)
ax_geol.set_xlim(x.min(), x.max())
ax_geol.set_ylim(-10000, 800)
ax_geol.grid(ls=":", lw=0.6, alpha=0.5)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_seattle_basin.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
