"""
fig_shape_overlay.py

Scientific content: Overlay of normalised gravity anomaly profiles for the
three localised canonical bodies (buried sphere, horizontal cylinder, and
finite Bouguer slab) on a single axis, all anchored to the same depth-to-
centre z = 600 m.  Each profile is normalised to its peak amplitude so the
comparison is about *shape*, not amplitude.  The right panel overlays the
*absolute* (un-normalised) anomalies together with a band representing
typical field-survey measurement noise (±0.05 mGal, 1σ) to motivate the
discussion of how measurement error propagates into the inferred depth and
density-contrast estimates.

Reproduces conceptually:
  Lowrie & Fichtner (2020), Ch. 3.4–3.5; Telford, Geldart & Sheriff (1990),
  Applied Geophysics, §2.7 (citation only — paywalled).

Output:  assets/figures/fig_shape_overlay.png
License: CC-BY 4.0
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.size":       13,
    "axes.titlesize":  14,
    "axes.labelsize":  13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi":      150,
    "savefig.dpi":     300,
})

C_BLUE, C_ORANGE, C_GREEN, C_VERM, C_BLACK = (
    "#0072B2", "#E69F00", "#009E73", "#D55E00", "#000000",
)

G = 6.67430e-11

# Forward formulas (Δg in mGal) ──────────────────────────────────────────
def dg_sphere(x, z, R, drho):
    M = (4.0 / 3.0) * np.pi * R**3 * drho
    return (G * M * z / (x**2 + z**2) ** 1.5) * 1e5

def dg_horiz_cyl(x, z, R, drho):
    lam = np.pi * R**2 * drho
    return (2 * G * lam * z / (x**2 + z**2)) * 1e5

def dg_finite_slab(x, z_top, z_bot, drho, x0, x1):
    def semi_inf(x, z, drho, edge):
        return 2 * G * drho * (np.pi / 2.0 + np.arctan2(x - edge, z))
    zs = np.linspace(z_top, z_bot, 300)
    dz = zs[1] - zs[0]
    out = np.zeros_like(x)
    for zi in zs:
        out += (semi_inf(x, zi, drho, x0)
                - semi_inf(x, zi, drho, x1)) * dz
    return out * 1e5

# Common geometry: depth-to-centre z = 600 m ─────────────────────────────
x = np.linspace(-3000.0, 3000.0, 1201)
z_common = 600.0

dg_sph = dg_sphere(x, z=z_common, R=180.0, drho=600.0)
dg_cyl = dg_horiz_cyl(x, z=z_common, R=180.0, drho=600.0)
# A finite slab 100 m thick centred at z = 600 m, lateral extent ±300 m
dg_slab = dg_finite_slab(x, z_top=550.0, z_bot=650.0,
                          drho=600.0, x0=-300.0, x1=300.0)

# ── Figure: two panels ──────────────────────────────────────────────────
fig, (axN, axA) = plt.subplots(1, 2, figsize=(13, 5.2),
                                gridspec_kw={"wspace": 0.28})

# Panel A — normalised shapes (peak = 1) ────────────────────────────────
axN.plot(x, dg_sph / dg_sph.max(), color=C_BLUE,   lw=2.4,
         label="Sphere ($x_{1/2} \\approx 0.766\\,z$)")
axN.plot(x, dg_cyl / dg_cyl.max(), color=C_ORANGE, lw=2.4,
         label="Horizontal cylinder ($x_{1/2} = z$)")
axN.plot(x, dg_slab / dg_slab.max(), color=C_GREEN, lw=2.4,
         label="Finite slab (flat-topped)")

# Mark the half-max line and the half-width locations for sphere & cylinder
axN.axhline(0.5, color=C_BLACK, lw=0.6, ls="--", alpha=0.7)
axN.axvline( 0.766 * z_common, color=C_BLUE,   lw=0.8, ls=":", alpha=0.8)
axN.axvline(-0.766 * z_common, color=C_BLUE,   lw=0.8, ls=":", alpha=0.8)
axN.axvline( z_common, color=C_ORANGE, lw=0.8, ls=":", alpha=0.8)
axN.axvline(-z_common, color=C_ORANGE, lw=0.8, ls=":", alpha=0.8)
axN.text(0.766*z_common + 60, 0.52, "sphere\n$x_{1/2}$",
         color=C_BLUE, fontsize=10, va="bottom")
axN.text(z_common + 60, 0.36, "cylinder\n$x_{1/2}$",
         color=C_ORANGE, fontsize=10, va="bottom")

axN.set_xlim(-2500, 2500)
axN.set_ylim(-0.05, 1.08)
axN.set_xlabel("Profile distance $x$  (m)")
axN.set_ylabel(r"$\Delta g(x) / \Delta g_{\max}$")
axN.set_title("(a)  Normalised shapes, all at depth $z = 600$ m",
              loc="left", pad=10)
axN.grid(ls=":", lw=0.6, alpha=0.5)
axN.legend(loc="upper right", framealpha=0.9)

# Panel B — absolute amplitudes + measurement-error band ────────────────
axA.plot(x, dg_sph,  color=C_BLUE,   lw=2.4, label="Sphere")
axA.plot(x, dg_cyl,  color=C_ORANGE, lw=2.4, label="Horizontal cylinder")
axA.plot(x, dg_slab, color=C_GREEN,  lw=2.4, label="Finite slab")

# A typical land-survey measurement-noise band: ±0.05 mGal (1σ).  Shade ±2σ.
sigma_g = 0.05
axA.axhspan(-2 * sigma_g, 2 * sigma_g,
            color=C_BLACK, alpha=0.10,
            label=r"Measurement noise $\pm 2\sigma$ ($\sigma = 0.05$ mGal)")
axA.axhline(0, color=C_BLACK, lw=0.6, ls="--")

axA.set_xlim(-2500, 2500)
axA.set_xlabel("Profile distance $x$  (m)")
axA.set_ylabel(r"$\Delta g$  (mGal)")
axA.set_title("(b)  Absolute amplitudes vs. measurement noise",
              loc="left", pad=10)
axA.grid(ls=":", lw=0.6, alpha=0.5)
axA.legend(loc="upper right", framealpha=0.9, fontsize=10)

# Annotate where each anomaly falls below the noise floor
def first_below(x, y, thr):
    """Smallest |x| at which |y| < thr (anomaly drops into noise)."""
    half = len(x) // 2
    xs = x[half:]
    ys = np.abs(y[half:])
    idx = np.argmax(ys < thr)
    return xs[idx] if ys[idx] < thr else np.nan

x_lost_sph  = first_below(x, dg_sph,  2 * sigma_g)
x_lost_cyl  = first_below(x, dg_cyl,  2 * sigma_g)
x_lost_slab = first_below(x, dg_slab, 2 * sigma_g)
print(f"Anomaly drops below 2σ at  sphere: ±{x_lost_sph:.0f} m, "
      f"cylinder: ±{x_lost_cyl:.0f} m, slab: ±{x_lost_slab:.0f} m")

fig.suptitle(
    "Comparison of canonical gravity anomalies at common depth — "
    "shape (left) and the noise floor (right)",
    fontsize=14, y=1.02)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_shape_overlay.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
