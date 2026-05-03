"""
fig_g_inverse_square.py

Scientific content: Variation of gravitational acceleration g with distance r
from Earth's centre, illustrating the inverse-square law and the smallness of
elevation effects (Mt. Everest) compared with orbital effects (ISS).

Reproduces conceptually the content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, §3.1. (UW Libraries e-book; not reproduced here.)

Output:  assets/figures/fig_g_inverse_square.png
License: CC-BY 4.0 (this script and its output)
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

# Colorblind-safe palette ───────────────────────────────────────────────────
C_BLUE, C_ORANGE, C_SKY, C_GREEN, C_VERM, C_PINK, C_BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73",
    "#D55E00", "#CC79A7", "#000000",
)

# Physical constants ────────────────────────────────────────────────────────
G   = 6.67430e-11      # m^3 kg^-1 s^-2
M_E = 5.9722e24        # kg
R_E = 6.371e6          # m  (mean Earth radius)

def g_of_r(r):
    """Newtonian g for a point mass at radius r ≥ R_E."""
    return G * M_E / r ** 2

# ── Compute curve from R_E to 10 R_E ───────────────────────────────────────
r = np.linspace(R_E, 10.0 * R_E, 600)
g = g_of_r(r)

# Reference points
points = {
    "Sea level":          (R_E,                  g_of_r(R_E)),
    "Mt. Everest (8.85 km)": (R_E + 8_850.0,    g_of_r(R_E + 8_850.0)),
    "ISS orbit (~408 km)":   (R_E + 408_000.0,  g_of_r(R_E + 408_000.0)),
    "Geostationary (~35 786 km)": (R_E + 35_786_000.0, g_of_r(R_E + 35_786_000.0)),
}

# ── Figure ─────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.0),
                                gridspec_kw={"width_ratios": [1.05, 1]})

# Left panel — global profile, log-log -------------------------------------
ax1.plot(r / R_E, g, color=C_BLUE, lw=2.4, label=r"$g(r) = G M_E / r^{\,2}$")
for name, (rp, gp) in points.items():
    ax1.plot(rp / R_E, gp, "o", color=C_VERM, ms=8, mec=C_BLACK, mew=0.8)
    ax1.annotate(name, (rp / R_E, gp),
                 xytext=(8, 6), textcoords="offset points", fontsize=11)

ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel(r"$r / R_E$  (Earth radii)")
ax1.set_ylabel(r"Gravitational acceleration $g$  (m s$^{-2}$)")
ax1.set_title("Gravity falls off with the square of distance")
ax1.set_xlim(0.95, 12)
ax1.grid(which="both", ls=":", lw=0.6, alpha=0.5)
ax1.legend(loc="upper right")

# Right panel — zoom near surface ------------------------------------------
z = np.linspace(0.0, 1.0e4, 400)             # 0 to 10 km elevation
g_surface = g_of_r(R_E + z)
free_air_linear = g_of_r(R_E) - 0.3086e-5 * z   # mGal/m → m/s²/m  (1 mGal = 1e-5 m/s²)

ax2.plot(z / 1e3, (g_surface - g_of_r(R_E)) * 1e5, color=C_BLUE, lw=2.4,
         label="Inverse-square law")
ax2.plot(z / 1e3, (free_air_linear - g_of_r(R_E)) * 1e5, color=C_ORANGE,
         lw=2.0, ls="--", label=r"Linear approx. $-0.3086\,\mathrm{mGal\,m^{-1}}$")

# Annotate Everest
zE = 8.85
gE = (g_of_r(R_E + 8850.0) - g_of_r(R_E)) * 1e5
ax2.plot(zE, gE, "o", color=C_VERM, ms=9, mec=C_BLACK, mew=0.8)
ax2.annotate(f"Everest\n$\\Delta g \\approx {gE:.0f}$ mGal", (zE, gE),
             xytext=(-95, -10), textcoords="offset points", fontsize=11,
             arrowprops=dict(arrowstyle="->", color=C_BLACK, lw=0.8))

ax2.set_xlabel("Elevation above sea level  (km)")
ax2.set_ylabel(r"Gravity decrement  $g - g(R_E)$  (mGal)")
ax2.set_title("Free-air gradient near the surface")
ax2.grid(ls=":", lw=0.6, alpha=0.5)
ax2.legend(loc="lower left")

fig.tight_layout()

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_g_inverse_square.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
