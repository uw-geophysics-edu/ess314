"""
fig_error_ellipse.py

Scientific content: Earthquake-location uncertainty has a strong geometric
component that depends on the distribution of recording stations relative
to the source.

(a) Stations forming a tight cluster — for example, a small regional array
    that lies entirely on one side of the event — produce an error ellipse
    that is highly elongated *away* from the array. There is far less
    information to constrain the radial direction (toward the array) than
    the transverse direction.

(b) When all the stations are far away (teleseismic-only configuration),
    the rays approach the source from below at similar takeoff angles. As
    a result, focal depth and origin time become strongly correlated: an
    earthquake that is shallower-and-earlier predicts almost exactly the
    same arrival times as one that is deeper-and-later. This trade-off
    appears as an elongated ridge in the joint depth–origin-time
    misfit surface.

Reproduces the scientific content of:
  Stein & Wysession (2003), Figs. 5.13 and 5.14 (error ellipses and the
  depth–origin-time trade-off).
  Lowrie & Fichtner (2020), Ch. 5.

Output: assets/figures/fig_error_ellipse.png
License: CC-BY 4.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import patches
from matplotlib.patches import Ellipse

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 130, "savefig.dpi": 200,
})

C_STA = "#009E73"
C_EQ = "#D55E00"
C_ELL = "#0072B2"
C_RAY = "#0072B2"
C_BAD = "#CC79A7"
C_FAULT = "#000000"

fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.0),
                         gridspec_kw=dict(width_ratios=[1.0, 1.15]))

# ── Panel (a): error ellipse for a clustered network ──────────────────
ax = axes[0]
xmin, xmax = -120, 120
ymin, ymax = -90, 90
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymin, ymax)
ax.set_aspect("equal")
ax.set_xlabel("East (km)")
ax.set_ylabel("North (km)")
ax.set_title("(a) Network on one side → ellipse elongates away",
             fontsize=13, pad=8)
ax.grid(True, color="#DDDDDD", lw=0.6)

# Cluster of stations on the eastern side
rng = np.random.default_rng(7)
sta_x = rng.uniform(60, 100, 8)
sta_y = rng.uniform(-30, 30, 8)
ax.plot(sta_x, sta_y, marker="^", color=C_STA, ms=12, mec="#000",
        mew=0.8, ls="", zorder=4, label="Stations (clustered)")

# Earthquake well outside the array
eq = np.array([-60.0, 0.0])
ax.plot(eq[0], eq[1], marker="*", color=C_EQ, ms=22, mec="#000", mew=1.0,
        zorder=6, label="Earthquake")

# Error ellipse — elongated radially toward the network
ell = Ellipse(xy=eq, width=70, height=22, angle=0, fill=True,
              facecolor=C_ELL, edgecolor="#003a5d", lw=1.4, alpha=0.30,
              zorder=3, label="1-σ error ellipse")
ax.add_patch(ell)
# Add an outline for clarity
ell_out = Ellipse(xy=eq, width=70, height=22, angle=0, fill=False,
                  edgecolor=C_ELL, lw=1.6, zorder=4)
ax.add_patch(ell_out)

# Ray paths from source to each station (light)
for sx, sy in zip(sta_x, sta_y):
    ax.plot([eq[0], sx], [eq[1], sy], color="#88AABB", lw=0.6, alpha=0.55,
            zorder=2)

ax.annotate("Long axis points\nbetween source\nand network",
            xy=(-30, 0), xytext=(-95, 55),
            fontsize=11.5, color="#003a5d",
            arrowprops=dict(arrowstyle="->", color="#003a5d", lw=1.0),
            bbox=dict(facecolor="white", edgecolor="#003a5d", lw=0.6,
                      boxstyle="round,pad=0.3"))

ax.legend(loc="upper right", framealpha=0.95, fontsize=10)

# ── Panel (b): depth–origin-time trade-off (teleseismic-only case) ─────
ax = axes[1]
xmin, xmax = -50, 1100
ymin, ymax = -10, 350
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymax, ymin)
ax.set_aspect("auto")
ax.set_xlabel("Epicentral distance (km — schematic)")
ax.set_ylabel("Depth (km)\n[positive down]", fontsize=11)
ax.set_title("(b) Distant stations only → depth and origin time trade off",
             fontsize=13, pad=8)

# Surface
ax.axhline(0, color=C_FAULT, lw=1.4, zorder=2)
ax.axhspan(0, ymax, color="#F0E5D0", zorder=0)

# Station cluster on the right
sta_xs = np.linspace(820, 1000, 4)
for sx in sta_xs:
    ax.plot(sx, 0, marker="^", color=C_STA, ms=14, mec="#000", mew=1.0,
            zorder=6)
ax.text(np.mean(sta_xs), -25, "Distant stations",
        ha="center", va="bottom", fontsize=11.5, fontweight="bold",
        color="#005a3d")

# Two candidate hypocenters: shallow-and-early vs. deep-and-late
hypo_shallow = np.array([0, 60])
hypo_deep = np.array([0, 220])

ax.plot(hypo_shallow[0], hypo_shallow[1], marker="*", color=C_EQ, ms=22,
        mec="#000", mew=0.8, zorder=6)
ax.plot(hypo_deep[0], hypo_deep[1], marker="*", color=C_BAD, ms=22,
        mec="#000", mew=0.8, zorder=6)

# Ray paths from each candidate to the station cluster
for sx in sta_xs:
    # Shallow source rays
    t = np.linspace(0, 1, 50)
    x = hypo_shallow[0] + (sx - hypo_shallow[0]) * t
    y = hypo_shallow[1] * (1 - t)
    ax.plot(x, y, color=C_EQ, lw=1.2, alpha=0.6, zorder=3)
    # Deep source rays
    x2 = hypo_deep[0] + (sx - hypo_deep[0]) * t
    y2 = hypo_deep[1] * (1 - t)
    ax.plot(x2, y2, color=C_BAD, lw=1.2, alpha=0.55, zorder=3)

# Annotations
ax.annotate("Shallow + early\n(t₀ small)",
            xy=hypo_shallow, xytext=(150, 15),
            fontsize=11, color=C_EQ, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=C_EQ, lw=1.0),
            bbox=dict(facecolor="white", edgecolor=C_EQ, lw=0.6,
                      boxstyle="round,pad=0.25"))
ax.annotate("Deep + later\n(t₀ larger)",
            xy=hypo_deep, xytext=(150, 240),
            fontsize=11, color=C_BAD, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=C_BAD, lw=1.0),
            bbox=dict(facecolor="white", edgecolor=C_BAD, lw=0.6,
                      boxstyle="round,pad=0.25"))

ax.text(550, 320, "Both models predict nearly the same\nteleseismic arrival "
        "times → unresolvable",
        ha="center", va="bottom", fontsize=11, color="#222",
        bbox=dict(facecolor="white", edgecolor="#444", lw=0.8,
                  boxstyle="round,pad=0.3"))

fig.suptitle("Why earthquake location uncertainty is geometric",
             fontsize=15, y=1.00)
fig.tight_layout(rect=[0, 0, 1, 0.96])

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_error_ellipse.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
