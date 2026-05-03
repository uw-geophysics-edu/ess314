"""
fig_geoid_ellipsoid.py

Scientific content: Three concentric profiles illustrating Earth's shape at
successively finer levels — the spherical first approximation, the rotational
oblate spheroid (reference ellipsoid), and the geoid as a deviation from
the ellipsoid (vertical exaggeration ×500 000 for visibility).

Reproduces conceptually:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, §3.2 (UW Libraries e-book).

Geoid undulation values are illustrative within the global range (-105 m to
+85 m) reported by the GRACE-FO mission (NASA/JPL, public domain).

Output:  assets/figures/fig_geoid_ellipsoid.png
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

# WGS84 reference ellipsoid parameters
a    = 6_378_137.0          # semi-major axis (equatorial)
b    = 6_356_752.3          # semi-minor axis (polar)
f    = 1.0 / 298.257223563  # flattening
R0   = (a + b) / 2.0        # mean radius

theta = np.linspace(0.0, 2 * np.pi, 720)
ct, st = np.cos(theta), np.sin(theta)

# Sphere of mean radius
r_sphere = R0 * np.ones_like(theta)
x_sph, y_sph = r_sphere * ct, r_sphere * st

# Oblate spheroid (latitude φ measured from equator)
phi = theta                  # treat θ as latitude for cross-section
r_ell = a * b / np.sqrt((b * np.cos(phi))**2 + (a * np.sin(phi))**2)
x_ell, y_ell = r_ell * np.cos(phi), r_ell * np.sin(phi)

# Synthetic geoid undulation: dominant 2nd–4th order spherical harmonic pattern
# ranging roughly from -100 m to +80 m. Pattern chosen to look like the
# canonical "potato" geoid map (qualitative).
N = (-90.0 * np.cos(2 * theta + 0.6)
     + 35.0 * np.cos(3 * theta - 1.2)
     + 25.0 * np.cos(4 * theta + 2.4)
     + 12.0 * np.cos(5 * theta + 0.3)) / 1.6
N = N - N.mean()                                    # ensure zero mean
exaggeration = 8000                                  # visualise N at ×8 000
r_geoid = r_ell + exaggeration * N
x_geoid, y_geoid = r_geoid * np.cos(phi), r_geoid * np.sin(phi)

# ── Figure: 3 panels ──────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 3, figsize=(13, 4.6),
                          subplot_kw=dict(aspect="equal"))

titles = [
    "(a)  Sphere  $R = 6371$ km",
    "(b)  Oblate spheroid (WGS84)\n$f = 1/298.257$, exaggerated ×100",
    "(c)  Geoid undulations $N$\n(deviation from ellipsoid, ×8000)",
]

# Exaggerate flattening for visibility in panel b
f_show = 0.05
b_show = a * (1 - f_show)
r_ell_show = a * b_show / np.sqrt((b_show * np.cos(phi))**2 + (a * np.sin(phi))**2)
x_ell_show, y_ell_show = r_ell_show * np.cos(phi), r_ell_show * np.sin(phi)

for ax, title in zip(axes, titles):
    ax.set_title(title, pad=14)
    ax.axis("off")

# (a) Sphere
axes[0].fill(x_sph / 1e6, y_sph / 1e6, color=C_SKY, alpha=0.55,
              edgecolor=C_BLACK, lw=1.8)
axes[0].plot(0, 0, "+", color=C_BLACK, ms=10, mew=1.5)

# (b) Spheroid (with reference circle)
axes[1].plot(np.cos(theta) * a / 1e6, np.sin(theta) * a / 1e6,
              ls=":", color=C_BLACK, lw=0.9, label="Equatorial sphere")
axes[1].fill(x_ell_show / 1e6, y_ell_show / 1e6, color=C_ORANGE, alpha=0.55,
              edgecolor=C_BLACK, lw=1.8)
axes[1].annotate("", xy=(0, b_show / 1e6), xytext=(0, a / 1e6),
                  arrowprops=dict(arrowstyle="->", color=C_VERM, lw=1.4))
axes[1].text(0.45, 0.30 + b_show / 1e6 / 2, "polar\nflattening",
              color=C_VERM, fontsize=11)
axes[1].legend(loc="upper right", frameon=True)

# (c) Geoid (overlay onto reference)
axes[2].plot(x_ell / 1e6, y_ell / 1e6, ls="--", color=C_BLACK,
              lw=1.0, label="Reference ellipsoid")
axes[2].fill(x_geoid / 1e6, y_geoid / 1e6, color=C_GREEN, alpha=0.55,
              edgecolor=C_BLACK, lw=1.6, label="Geoid (exaggerated)")
axes[2].legend(loc="upper right")

# Add scale label to all
for ax in axes:
    ax.set_xlim(-7.2, 7.2)
    ax.set_ylim(-7.2, 7.2)

fig.suptitle("Three approximations to Earth's shape",
              fontsize=15, y=1.02)
fig.tight_layout()

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_geoid_ellipsoid.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
