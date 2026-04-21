"""
fig_12_cascadia_slab.py

Scientific content: Schematic east-west cross-section of the Cascadia
subduction zone beneath Washington state, showing the Juan de Fuca
plate descending beneath North America. Fast (blue) anomalies in
tomographic images mark the cold subducted slab; slow (red) anomalies
mark mantle wedge melting, the low-velocity layer at the slab top
associated with dehydration, and the westward-tilted mantle beneath
the Cascade volcanic arc. This is the pedagogical anchor that connects
the global mantle-tomography physics to the Pacific Northwest.

Reproduces the scientific content of (does not reproduce the figures):
  Schmandt, B. and Humphreys, E., 2010. Complex subduction and
  small-scale convection revealed by body-wave tomography of the
  western United States upper mantle. Earth and Planetary Science
  Letters 297(3-4), 435-445. https://doi.org/10.1016/j.epsl.2010.06.047

  Bodmer, M., Toomey, D.R., Hooft, E.E.E., Schmandt, B., 2018.
  Buoyant asthenosphere beneath Cascadia influences megathrust
  segmentation. Geophysical Research Letters 45(13), 6083-6091.
  https://doi.org/10.1029/2018GL078700

Output: assets/figures/fig_12_cascadia_slab.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def main(outpath):
    fig, ax = plt.subplots(figsize=(12.0, 6.5))

    # Axes: x in km (distance west-to-east across Cascadia); depth in km
    ax.set_xlim(-400, 400)
    ax.set_ylim(400, 0)
    ax.set_xlabel("Distance across margin (km, west $\\rightarrow$ east)")
    ax.set_ylabel("Depth (km)")

    # --- Background: mantle (light fill), crust (top band)
    ax.axhspan(0, 35, color="#F2E6D0", alpha=0.6, zorder=0)      # continental crust
    ax.axhspan(35, 400, color="#FFE9A6", alpha=0.30, zorder=0)   # mantle wedge bg

    # Ocean (left of trench)
    ax.axhspan(0, 5, xmin=0.0, xmax=0.45, color="#B0D4E3",
               alpha=0.7, zorder=1)

    # --- Subducting Juan de Fuca slab (fast/cold anomaly) as a polygon
    # top and bottom surfaces of ~80-km-thick slab, dipping ~15-25 deg
    x_top = np.linspace(-300, 300, 200)
    # Trench at x = -100 km (approx); slab descends with increasing dip
    dip_model = np.piecewise(
        x_top,
        [x_top < -100, (x_top >= -100) & (x_top < 100), x_top >= 100],
        [lambda x: 5.0,                                    # oceanic crust at surface
         lambda x: 5.0 + (x + 100) * 0.35,                 # 15-20 deg dip
         lambda x: 5.0 + 200 * 0.35 + (x - 100) * 0.8],    # steepening
    )
    bottom = dip_model + 80.0
    slab_poly = np.concatenate([
        np.stack([x_top, dip_model], axis=1),
        np.stack([x_top[::-1], bottom[::-1]], axis=1),
    ])
    ax.add_patch(Polygon(slab_poly, closed=True,
                         facecolor="#0072B2", alpha=0.45,
                         edgecolor="#0072B2", lw=1.5, zorder=3))

    # Slow low-velocity layer hugging slab top (serpentinized / hydrated mantle)
    lvl_top = dip_model
    lvl_bot = dip_model + 10
    lvl_poly = np.concatenate([
        np.stack([x_top, lvl_top], axis=1),
        np.stack([x_top[::-1], lvl_bot[::-1]], axis=1),
    ])
    ax.add_patch(Polygon(lvl_poly, closed=True,
                         facecolor="#D55E00", alpha=0.45,
                         edgecolor="none", zorder=4))

    # Mantle wedge melt zone (slow) above the slab beneath the arc
    arc_melt = np.array([
        [40, 35], [150, 50], [150, 110], [80, 100], [40, 80]
    ])
    ax.add_patch(Polygon(arc_melt, closed=True,
                         facecolor="#D55E00", alpha=0.35,
                         edgecolor="#D55E00", lw=1.0, zorder=4))

    # Arc volcanism
    for arc_x in [70, 90, 110]:
        ax.plot(arc_x, 0, marker="^", color="#D55E00",
                markersize=16, markeredgecolor=COLORS[6], zorder=5)
    ax.text(90, -12, "Cascade arc", ha="center", color=COLORS[4],
            fontsize=11, fontweight="bold")

    # Trench
    ax.plot(-100, 0, marker="v", color=COLORS[6],
            markersize=14, zorder=5)
    ax.text(-100, -12, "Cascadia trench",
            ha="center", color=COLORS[6], fontsize=11, fontweight="bold")

    # Coast
    ax.plot(-10, 0, marker="|", color=COLORS[6], markersize=14, zorder=5)
    ax.text(-10, -12, "coast", ha="center", color=COLORS[6], fontsize=10)

    # Seattle
    ax.plot(180, 0, marker="s", color=COLORS[6],
            markersize=9, markerfacecolor="white", zorder=5)
    ax.text(180, -12, "Seattle", ha="center", color=COLORS[6], fontsize=10)

    # Labels for tomographic anomalies
    ax.annotate("fast anomaly\n(cold subducted slab)",
                xy=(190, 150), xytext=(260, 80),
                fontsize=11, color="#0072B2", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#0072B2", lw=1.2))

    ax.annotate("slow anomaly\n(hydrated slab top)",
                xy=(50, 35), xytext=(-300, 110),
                fontsize=11, color="#D55E00", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#D55E00", lw=1.2))

    ax.annotate("slow anomaly\n(partial melt in\nmantle wedge)",
                xy=(90, 70), xytext=(-190, 220),
                fontsize=11, color="#D55E00", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#D55E00", lw=1.2))

    # Arrow showing plate motion
    ax.annotate("", xy=(-60, 12), xytext=(-260, 12),
                arrowprops=dict(arrowstyle="->",
                                color=COLORS[6], lw=2.2))
    ax.text(-160, 2, "Juan de Fuca plate $\\approx$ 4 cm/yr",
            ha="center", fontsize=10, color=COLORS[6], style="italic")

    # Lithosphere label (continental)
    ax.text(250, 15, "North American continental lithosphere",
            fontsize=10, color=COLORS[6], ha="center", style="italic")

    # Depth tick annotations for common Cascadia earthquakes
    ax.axhline(50, color=COLORS[6], lw=0.4, alpha=0.3)
    ax.text(-380, 48, "typical intraslab EQs\n(e.g., Nisqually 2001)",
            fontsize=9, color=COLORS[6], va="bottom")

    ax.set_title("Cascadia subduction zone: tomographic structure beneath Washington",
                 color=COLORS[6], pad=22)
    ax.grid(True, alpha=0.25)

    # Give negative y room for labels above the surface
    ax.set_ylim(400, -25)

    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main("assets/figures/fig_12_cascadia_slab.png")
