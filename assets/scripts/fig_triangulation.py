"""
fig_triangulation.py

Scientific content: Multi-station earthquake epicenter location by
triangulation. Each station's S-minus-P time gives a hypocentral distance,
which on the surface becomes a circle of possible epicenter locations. With
three or more stations the circles intersect at a single point — the
epicenter. With imperfect velocity models or picking errors the circles do
not exactly meet at one point; the discrepancy is the residual that
formalizes the inverse problem.

Reproduces the scientific content of:
  Stein & Wysession (2003), An Introduction to Seismology, Earthquakes, and
  Earth Structure, Blackwell, Fig. 5.2 (triangulation).
  Lowrie & Fichtner (2020), Fundamentals of Geophysics, 3rd ed., Ch. 5.

Output: assets/figures/fig_triangulation.png
License: CC-BY 4.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import patches

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 130, "savefig.dpi": 200,
})

C_STA = "#009E73"
C_EPI = "#D55E00"
C_C1 = "#0072B2"
C_C2 = "#E69F00"
C_C3 = "#56B4E9"
C_RESID = "#CC79A7"

# True epicenter location
epi = np.array([0.0, 0.0])

# Three station locations (km, in epicentral coordinates)
stations = {
    "S1": np.array([55.0,  35.0]),
    "S2": np.array([-45.0, 40.0]),
    "S3": np.array([-30.0, -50.0]),
}

# Radii (true hypocentral distances)
radii_true = {name: np.linalg.norm(pos - epi) for name, pos in stations.items()}

# Imperfect picks: add small errors so circles don't exactly meet
np.random.seed(11)
radii_pick = {name: r * (1 + np.random.normal(0, 0.04))
              for name, r in radii_true.items()}

fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.5))

for k, (ax, radii, title) in enumerate([
    (axes[0], radii_true,
     "(a) Perfect picks → circles intersect at one point"),
    (axes[1], radii_pick,
     "(b) Real picks → circles bound a residual region"),
]):
    # Plot circles, stations, true epicenter
    colors = [C_C1, C_C2, C_C3]
    for (name, pos), color in zip(stations.items(), colors):
        r = radii[name]
        circ = patches.Circle(pos, radius=r, fill=False, edgecolor=color,
                              lw=2.0, zorder=3)
        ax.add_patch(circ)
        # Radius line
        ax.plot([pos[0], epi[0]], [pos[1], epi[1]], color=color, lw=1.0,
                ls=":", alpha=0.7, zorder=2)
        # Station marker
        ax.plot(pos[0], pos[1], marker="^", color=C_STA, ms=15,
                mec="#000", mew=1.0, zorder=5)
        # Station label
        offset = pos / np.linalg.norm(pos) * 9
        ax.annotate(f"{name}", xy=pos, xytext=pos + offset,
                    ha="center", va="center", fontsize=12.5,
                    fontweight="bold",
                    bbox=dict(facecolor="white", edgecolor=C_STA, lw=0.6,
                              boxstyle="round,pad=0.25"))
        # Radius label at midpoint
        mid = (pos + epi) / 2
        normal = np.array([-pos[1], pos[0]]) / np.linalg.norm(pos) * 4
        ax.text(mid[0] + normal[0], mid[1] + normal[1],
                f"$r_{{{name[1]}}} = {r:.0f}$ km",
                fontsize=11, color=color, ha="center", va="center",
                bbox=dict(facecolor="white", edgecolor="none", alpha=0.85,
                          boxstyle="round,pad=0.15"))

    # True epicenter
    ax.plot(epi[0], epi[1], marker="*", color=C_EPI, ms=22, mec="#000",
            mew=1.0, zorder=6, label="True epicenter")

    if k == 0:
        ax.annotate("Single intersection\n= epicenter",
                    xy=(2, 2), xytext=(35, -55),
                    fontsize=11.5, fontweight="bold", color=C_EPI,
                    arrowprops=dict(arrowstyle="->", color=C_EPI, lw=1.0),
                    bbox=dict(facecolor="white", edgecolor=C_EPI, lw=0.6,
                              boxstyle="round,pad=0.3"))
    else:
        # Highlight the "residual triangle" formed by the three intersections
        ax.annotate("Residual region\n(picking + velocity errors)",
                    xy=(2, 2), xytext=(35, -55),
                    fontsize=11.5, fontweight="bold", color=C_RESID,
                    arrowprops=dict(arrowstyle="->", color=C_RESID, lw=1.0),
                    bbox=dict(facecolor="white", edgecolor=C_RESID, lw=0.6,
                              boxstyle="round,pad=0.3"))

    ax.set_xlim(-110, 110)
    ax.set_ylim(-100, 100)
    ax.set_aspect("equal")
    ax.set_xlabel("East (km)")
    if k == 0:
        ax.set_ylabel("North (km)")
    ax.set_title(title, fontsize=13, pad=8)
    ax.grid(True, color="#DDDDDD", lw=0.6)

# Suptitle
fig.suptitle("Epicenter location by triangulation: three or more stations are required",
             fontsize=14, y=1.00)

fig.tight_layout()

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_triangulation.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
