"""
fig_plate_boundary_focal.py

Scientific content: schematic map of the three principal plate-boundary
types — divergent, transform, convergent — annotated with the
characteristic focal-mechanism beach balls produced by earthquakes on
each.

Replaces (and reorganises) the conceptual content of:
  Lowrie (2007) Fig 3.41 (Mexico subduction); Plummer/Carlson 2003
  Fig 7.21–7.22 (mid-ocean ridge offsets).
  Both copyrighted; not reproduced.

Output: assets/figures/fig_plate_boundary_focal.png
License: CC-BY 4.0 (this script).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrow, Polygon, Rectangle
from obspy.imaging.beachball import beach

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

PLATE_A = "#FFE5D0"
PLATE_B = "#D9F2EA"
OCEAN = "#E5F0F8"


def main(out_path: str = "assets/figures/fig_plate_boundary_focal.png") -> None:
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 5.0))

    # --------------- (a) Divergent margin (mid-ocean ridge) ----------
    ax = axes[0]
    ax.add_patch(Rectangle((-1.0, -0.6), 2.0, 1.2, facecolor=OCEAN, lw=0))
    # two plates separated by a vertical ridge axis
    ax.add_patch(Rectangle((-1.0, -0.6), 1.0, 1.2, facecolor=PLATE_A,
                           edgecolor="#888888", lw=0.5, alpha=0.7))
    ax.add_patch(Rectangle((0.0, -0.6), 1.0, 1.2, facecolor=PLATE_B,
                           edgecolor="#888888", lw=0.5, alpha=0.7))
    # ridge axis
    ax.plot([0, 0], [-0.6, 0.6], color="#000000", lw=2.5)
    # plate motions (arrows)
    ax.annotate("", xy=(-0.7, 0.0), xytext=(-0.25, 0.0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2.0,
                                mutation_scale=18))
    ax.annotate("", xy=(0.7, 0.0), xytext=(0.25, 0.0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2.0,
                                mutation_scale=18))
    # focal mechanisms (normal faults) along the axis
    for y in (-0.35, 0.10, 0.45):
        bc = beach((0.0, 60.0, -90.0), xy=(0.0, y), width=0.18,
                   facecolor="#D55E00", edgecolor="black", linewidth=0.8)
        ax.add_collection(bc)
    ax.set_xlim(-1.0, 1.0); ax.set_ylim(-0.7, 0.7)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("(a) Divergent (rift / ridge)\nNormal faulting")

    # --------------- (b) Transform margin -----------------------------
    ax = axes[1]
    ax.add_patch(Rectangle((-1.0, -0.6), 2.0, 1.2, facecolor=OCEAN, lw=0))
    # two plates separated by a vertical strike-slip
    poly_top = [[-1.0, 0.05], [1.0, 0.05], [1.0, 0.6], [-1.0, 0.6]]
    poly_bot = [[-1.0, -0.05], [1.0, -0.05], [1.0, -0.6], [-1.0, -0.6]]
    ax.add_patch(Polygon(poly_top, facecolor=PLATE_A,
                         edgecolor="#888888", lw=0.5, alpha=0.7))
    ax.add_patch(Polygon(poly_bot, facecolor=PLATE_B,
                         edgecolor="#888888", lw=0.5, alpha=0.7))
    # transform fault (E-W trace)
    ax.plot([-1.0, 1.0], [0, 0], color="#000000", lw=2.5)
    # plate motions
    ax.annotate("", xy=(0.6, 0.32), xytext=(-0.6, 0.32),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2.0,
                                mutation_scale=18))
    ax.annotate("", xy=(-0.6, -0.32), xytext=(0.6, -0.32),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2.0,
                                mutation_scale=18))
    # strike-slip beach balls along trace
    for x in (-0.55, 0.0, 0.55):
        bc = beach((90.0, 90.0, 0.0), xy=(x, 0.0), width=0.18,
                   facecolor="#D55E00", edgecolor="black", linewidth=0.8)
        ax.add_collection(bc)
    ax.set_xlim(-1.0, 1.0); ax.set_ylim(-0.7, 0.7)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("(b) Transform\nStrike-slip faulting")

    # --------------- (c) Convergent margin (subduction) --------------
    ax = axes[2]
    ax.add_patch(Rectangle((-1.0, -0.6), 2.0, 1.2, facecolor=OCEAN, lw=0))
    # subducting slab (lower-right plate dips to left under upper-left plate)
    # upper plate continent on the LEFT
    cont = [[-1.0, 0.6], [0.10, 0.6], [0.10, 0.05], [-1.0, 0.05]]
    ax.add_patch(Polygon(cont, facecolor=PLATE_A,
                         edgecolor="#888888", lw=0.5, alpha=0.85))
    # ocean plate to the right, with downgoing slab beneath continent
    ocean_top = [[0.10, 0.05], [1.0, 0.05], [1.0, -0.05], [0.10, -0.05]]
    ax.add_patch(Polygon(ocean_top, facecolor=PLATE_B,
                         edgecolor="#888888", lw=0.5, alpha=0.85))
    slab = [[0.10, -0.05], [-0.45, -0.55], [-0.55, -0.55],
            [0.10, -0.05]]  # slab descending into mantle
    ax.add_patch(Polygon([[0.10, 0.05], [0.10, -0.05],
                          [-0.45, -0.55], [-0.55, -0.55]],
                         facecolor=PLATE_B, edgecolor="#888888", lw=0.5,
                         alpha=0.85))
    # trench arrow indicators
    ax.plot(0.10, 0.05, marker="v", color="black", markersize=11, zorder=8)
    # convergence motion arrows
    ax.annotate("", xy=(0.20, 0.20), xytext=(0.85, 0.20),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=2.0,
                                mutation_scale=18))
    # megathrust beach ball at trench
    bc1 = beach((0.0, 20.0, 90.0), xy=(0.10, 0.30),
                width=0.20,
                facecolor="#D55E00", edgecolor="black", linewidth=0.8)
    ax.add_collection(bc1)
    ax.text(0.15, 0.46, "megathrust", fontsize=9, color="#444444",
            ha="left")
    # intraslab beach ball deeper down
    bc2 = beach((0.0, 60.0, -90.0), xy=(-0.15, -0.30),
                width=0.16,
                facecolor="#D55E00", edgecolor="black", linewidth=0.8)
    ax.add_collection(bc2)
    ax.text(-0.18, -0.45, "intraslab\n(normal)", fontsize=9,
            color="#444444", ha="center")
    ax.text(-0.55, 0.40, "continent", fontsize=10, color="#444444",
            ha="center", style="italic")
    ax.text(0.55, 0.20, "ocean plate", fontsize=10, color="#444444",
            ha="center", style="italic")

    ax.set_xlim(-1.0, 1.0); ax.set_ylim(-0.7, 0.7)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("(c) Convergent (subduction)\nThrust + intraslab")

    fig.suptitle("Plate-boundary regimes and characteristic focal "
                 "mechanisms",
                 fontsize=15, y=1.02)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    main()
