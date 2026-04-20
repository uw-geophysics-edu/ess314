"""
fig_kirchhoff_adjoint_pair.py

Scientific content:
  Four-panel figure illustrating the Kirchhoff adjoint pair — the
  foundational duality between forward modeling (diffraction) and
  migration (imaging).

  Top row (forward modeling, "adj=0"): a point scatterer at (x0, z0)
  in the earth maps to a hyperbola t = sqrt((2z0/v)^2 + (2(x-x0)/v)^2)
  in the zero-offset data space. This is the response of one buried
  diffractor recorded at every surface position.

  Bottom row (migration, "adj=1"): an isolated impulse in the data at
  (y0, t0) maps to a semicircle (x-y0)^2 + z^2 = (v*t0/2)^2 in the
  earth. The impulse is consistent with every reflector point on that
  semicircle — the migration spreads the impulse over all such
  possible source locations.

  The forward and adjoint operators are transposes of each other, and
  together they define both modeling and migration with the same loop.
  This is the central operational idea of Kirchhoff imaging.

Reproduces the scientific content of:
  Claerbout, J. F. (2010). Basic Earth Imaging. Stanford Exploration
  Project. http://sepwww.stanford.edu/sep/prof/bei11.2010.pdf
  (Chapter 5, Figures 5.5 and 5.6; subroutine kirchslow on p. 65).

Output: assets/figures/fig_kirchhoff_adjoint_pair.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

C_BLUE = "#0072B2"; C_ORANGE = "#E69F00"; C_SKY = "#56B4E9"
C_GREEN = "#009E73"; C_VERM = "#D55E00"; C_PINK = "#CC79A7"; C_BLACK = "#000000"

# -- Common parameters ----------------------------------------------
v = 2.0           # km/s (half-velocity in exploding-reflector interpretation)
x_range = np.linspace(0, 4.0, 300)
z_range = np.linspace(0, 2.0, 200)

# Scatterer in earth
x0, z0 = 2.0, 1.0

# Impulse in data
y0 = 2.0       # midpoint (km)
t0_s = 1.0     # two-way time (s)

fig, axs = plt.subplots(2, 2, figsize=(13, 9.5),
                        gridspec_kw={"hspace": 0.55, "wspace": 0.30})

# =====================================================================
# TOP ROW — FORWARD MODELING: point in earth  →  hyperbola in data
# =====================================================================

# Panel (0,0): point in earth model
ax = axs[0, 0]
ax.set_facecolor("white")
ax.plot(x0, z0, marker="*", markersize=22, color=C_VERM,
        markeredgecolor=C_BLACK, zorder=5)
ax.text(x0 + 0.12, z0 + 0.08, f"point scatterer\n(x₀={x0}, z₀={z0})",
        fontsize=11, color=C_BLACK)
ax.set_xlim(0, 4)
ax.set_ylim(2.0, 0.0)
ax.set_xlabel("x (km)")
ax.set_ylabel("z, depth (km)")
ax.set_title("(a) Earth model: one point at depth")
ax.set_aspect("equal")
ax.grid(alpha=0.3)

# Panel (0,1): hyperbola in data space
ax = axs[0, 1]
# Hyperbola: t = sqrt((2 z0/v)^2 + (2(x-x0)/v)^2)
x_h = np.linspace(0, 4.0, 400)
t_h = np.sqrt((2*z0/v)**2 + (2*(x_h - x0)/v)**2)  # seconds
ax.plot(x_h, t_h*1000, color=C_BLUE, lw=2.6,
        label=r"$t = \sqrt{(2z_0/v)^2 + (2(x-x_0)/v)^2}$")
# Mark the apex
t_apex_ms = 2*z0/v * 1000
ax.plot(x0, t_apex_ms, marker="o", markersize=10, color=C_VERM,
        markeredgecolor=C_BLACK, zorder=5,
        label=f"apex at (x₀, 2z₀/v) = ({x0}, {t_apex_ms:.0f} ms)")
ax.set_xlim(0, 4)
ax.set_ylim(2000, 0)
ax.set_xlabel("x, midpoint (km)")
ax.set_ylabel("t, two-way time (ms)")
ax.set_title("(b) Zero-offset data: hyperbolic diffraction")
ax.grid(alpha=0.3)
ax.legend(loc="lower center", fontsize=10)

# =====================================================================
# BOTTOM ROW — MIGRATION: impulse in data  →  semicircle in earth
# =====================================================================

# Panel (1,0): impulse in data
ax = axs[1, 0]
ax.plot(y0, t0_s*1000, marker="o", markersize=16, color=C_ORANGE,
        markeredgecolor=C_BLACK, zorder=5)
ax.text(y0 + 0.15, t0_s*1000 + 80, f"impulse\n(y₀={y0}, t₀={t0_s*1000:.0f} ms)",
        fontsize=11, color=C_BLACK)
ax.set_xlim(0, 4)
ax.set_ylim(2000, 0)
ax.set_xlabel("y, midpoint (km)")
ax.set_ylabel("t, two-way time (ms)")
ax.set_title("(c) Data: one nonzero sample")
ax.grid(alpha=0.3)

# Panel (1,1): semicircle in earth
ax = axs[1, 1]
# Semicircle radius = v * t0 / 2 (zero-offset: data time = 2 z/v if vertical, else slant)
r = v * t0_s / 2.0
th = np.linspace(0, np.pi, 200)
x_c = y0 + r * np.cos(th)
z_c = r * np.sin(th)
ax.plot(x_c, z_c, color=C_SKY, lw=2.6,
        label=f"semicircle: (x-y₀)² + z² = (v t₀/2)² ;\n  radius = {r:.2f} km")
ax.plot(y0, 0, marker="v", markersize=12, color=C_ORANGE,
        markeredgecolor=C_BLACK, zorder=5, label="y₀ (midpoint on surface)")
# Highlight the vertical depth: z = v t0 / 2
ax.plot([y0, y0], [0, r], color=C_PINK, lw=1.5, linestyle=":",
        label=f"z = v t₀/2 = {r:.2f} km (zero-dip case)")
ax.set_xlim(0, 4)
ax.set_ylim(2.0, 0.0)
ax.set_xlabel("x (km)")
ax.set_ylabel("z, depth (km)")
ax.set_title("(d) Earth model: semicircular smear")
ax.set_aspect("equal")
ax.grid(alpha=0.3)
ax.legend(loc="lower center", fontsize=9.5)

fig.suptitle(
    "The Kirchhoff adjoint pair\n"
    "TOP: point → hyperbola  (forward modeling, adj=0)     "
    "BOTTOM: impulse → semicircle  (migration, adj=1)",
    fontsize=14, y=0.995)

fig.savefig("/tmp/lec16/assets/figures/fig_kirchhoff_adjoint_pair.png",
            bbox_inches="tight", dpi=300)
plt.close(fig)
print("Saved fig_kirchhoff_adjoint_pair.png")
