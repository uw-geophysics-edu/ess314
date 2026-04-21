"""
fig_12_global_mantle_tomography.py

Scientific content: Schematic pole-to-pole cross-section of Earth's
mantle showing the tomographic picture of mantle convection:
subducting slabs descending as fast/cold anomalies through the 660-km
boundary into the lower mantle; deep-mantle plumes rising from the
core-mantle boundary as slow/hot features; ultra-low velocity zones
(ULVZ) and large low-shear-velocity provinces (LLSVP) at the base of
the mantle; and the D" layer. This is the view that global seismic
tomography has assembled over the past 30 years and the picture that
Lecture 12 students will learn to read.

Reproduces the scientific content of (does not reproduce the figures):
  Garnero, E.J. and McNamara, A.K., 2008. Structure and dynamics of
  Earth's lower mantle. Science 320(5876), 626-628.
  https://doi.org/10.1126/science.1148028

  Ritsema, J., Deuss, A., van Heijst, H.J., Woodhouse, J.H., 2011.
  S40RTS: a degree-40 shear-velocity model for the mantle from new
  Rayleigh wave dispersion, teleseismic traveltime and normal-mode
  splitting function measurements. Geophys. J. Int. 184, 1223-1236.
  https://doi.org/10.1111/j.1365-246X.2010.04884.x (open access)

Output: assets/figures/fig_12_global_mantle_tomography.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

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

R_EARTH = 6371.0
R_CMB = 3480.0
R_ICB = 1220.0
R_660 = R_EARTH - 660


def main(outpath):
    fig, ax = plt.subplots(figsize=(12.0, 7.5))

    theta = np.linspace(0, np.pi, 400)
    # Show top hemisphere only
    ax.plot(np.cos(theta) * R_EARTH, np.sin(theta) * R_EARTH,
            color=COLORS[6], lw=1.5)
    ax.fill(np.cos(theta) * R_EARTH, np.sin(theta) * R_EARTH,
            color="#F2E6D0", alpha=0.5, zorder=0)
    # Upper/lower mantle boundary (660 km)
    ax.plot(np.cos(theta) * R_660, np.sin(theta) * R_660,
            color=COLORS[6], lw=0.7, ls=":", alpha=0.7, zorder=1)
    # CMB
    ax.plot(np.cos(theta) * R_CMB, np.sin(theta) * R_CMB,
            color=COLORS[6], lw=1.3, zorder=2)
    ax.fill(np.cos(theta) * R_CMB, np.sin(theta) * R_CMB,
            color="#FFE9A6", alpha=0.8, zorder=1)
    # Inner core fill
    ax.plot(np.cos(theta) * R_ICB, np.sin(theta) * R_ICB,
            color=COLORS[6], lw=0.9, ls="--", alpha=0.7, zorder=2)
    ax.fill(np.cos(theta) * R_ICB, np.sin(theta) * R_ICB,
            color="#FFD37A", alpha=0.9, zorder=1)

    # Ground line
    ax.plot([-R_EARTH, R_EARTH], [0, 0], color=COLORS[6], lw=1.2)

    # --- Subducting slabs (fast/cold, blue) ---
    # Slab A: left side (e.g., Farallon / Cascadia)
    slab_A = np.array([
        [-R_EARTH * 0.92, 0],
        [-R_EARTH * 0.70, 800],
        [-R_EARTH * 0.55, 1800],
        [-R_EARTH * 0.42, 2600],
        [-R_EARTH * 0.36, 2891],     # reaches CMB
        [-R_EARTH * 0.38, 2700],
        [-R_EARTH * 0.50, 1800],
        [-R_EARTH * 0.63, 800],
        [-R_EARTH * 0.86, 0],
    ])
    # Convert (x, depth) to (x, y_above_centre) = (x, R - depth) then plot
    x_A = slab_A[:, 0]
    y_A = R_EARTH - slab_A[:, 1]
    ax.fill(x_A, y_A, color="#0072B2", alpha=0.55,
            edgecolor="#0072B2", lw=1.0, zorder=3)

    # Slab B: right side (e.g., western Pacific)
    slab_B = np.array([
        [R_EARTH * 0.50, 0],
        [R_EARTH * 0.38, 500],
        [R_EARTH * 0.30, 1100],
        [R_EARTH * 0.32, 1600],     # stagnates at 660, then descends
        [R_EARTH * 0.22, 2300],
        [R_EARTH * 0.15, 2891],
        [R_EARTH * 0.19, 2500],
        [R_EARTH * 0.30, 1800],
        [R_EARTH * 0.40, 1100],
        [R_EARTH * 0.47, 500],
        [R_EARTH * 0.55, 0],
    ])
    x_B = slab_B[:, 0]
    y_B = R_EARTH - slab_B[:, 1]
    ax.fill(x_B, y_B, color="#0072B2", alpha=0.55,
            edgecolor="#0072B2", lw=1.0, zorder=3)

    # --- Deep-mantle plume (slow/hot, red) ---
    plume = np.array([
        [R_EARTH * 0.75, 0],
        [R_EARTH * 0.78, 600],
        [R_EARTH * 0.60, 1400],
        [R_EARTH * 0.40, 2400],
        [R_EARTH * 0.35, 2891],
        [R_EARTH * 0.43, 2891],
        [R_EARTH * 0.50, 2400],
        [R_EARTH * 0.68, 1400],
        [R_EARTH * 0.82, 600],
        [R_EARTH * 0.80, 0],
    ])
    ax.fill(plume[:, 0], R_EARTH - plume[:, 1],
            color="#D55E00", alpha=0.50,
            edgecolor="#D55E00", lw=1.0, zorder=3)

    # --- LLSVP at base of mantle (very slow/hot) ---
    llsvp = np.array([
        [-R_EARTH * 0.20, 2891],
        [-R_EARTH * 0.10, 2700],
        [R_EARTH * 0.10,  2680],
        [R_EARTH * 0.22,  2891],
    ])
    ax.fill(llsvp[:, 0], R_EARTH - llsvp[:, 1],
            color="#D55E00", alpha=0.65,
            edgecolor="#CC2200", lw=1.3, zorder=4)

    # --- ULVZ patches (very slow, tiny, right at CMB) ---
    for x0 in [-R_EARTH * 0.30, R_EARTH * 0.25, R_EARTH * 0.05]:
        angle = np.linspace(0, 2 * np.pi, 100)
        r_ulvz = 80.0  # small
        # Place ULVZ on CMB: y = R - 2891
        y0 = R_EARTH - 2891
        ax.fill(x0 + r_ulvz * np.cos(angle),
                y0 + r_ulvz * 0.5 * np.sin(angle),
                color="#800020", alpha=0.85, zorder=5)

    # --- D" marker on left side ---
    x_dd = np.linspace(-R_EARTH * 0.55, -R_EARTH * 0.35, 50)
    y_dd = R_EARTH - 2700 + 10 * np.sin(5 * x_dd / R_EARTH)
    ax.plot(x_dd, y_dd, color=COLORS[6], lw=2.0, zorder=4)

    # Labels
    ax.annotate("subducting slab\n(fast, cold)",
                xy=(-0.45 * R_EARTH, R_EARTH - 1500),
                xytext=(-0.95 * R_EARTH, R_EARTH - 400),
                fontsize=11, color="#0072B2", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#0072B2", lw=1.1))

    ax.annotate("slab stagnates\nnear 660 km",
                xy=(0.30 * R_EARTH, R_EARTH - 700),
                xytext=(0.65 * R_EARTH, R_EARTH - 350),
                fontsize=10, color="#0072B2",
                arrowprops=dict(arrowstyle="->", color="#0072B2", lw=1.0))

    ax.annotate("mantle plume\n(slow, hot)",
                xy=(0.57 * R_EARTH, R_EARTH - 1200),
                xytext=(0.90 * R_EARTH, R_EARTH - 800),
                fontsize=11, color="#D55E00", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#D55E00", lw=1.1))

    ax.annotate("LLSVP\n(Large Low Shear\nVelocity Province)",
                xy=(0.0, R_EARTH - 2800),
                xytext=(-0.20 * R_EARTH, R_EARTH - 3400),
                fontsize=10, color="#CC2200", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#CC2200", lw=1.0),
                ha="center")

    ax.annotate("ULVZ\n(Ultra-Low\nVelocity Zone)",
                xy=(-0.30 * R_EARTH, R_EARTH - 2891),
                xytext=(-0.65 * R_EARTH, R_EARTH - 3300),
                fontsize=9, color="#800020", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#800020", lw=1.0),
                ha="center")

    ax.annotate('D" reflector\n(phase change)',
                xy=(-0.45 * R_EARTH, R_EARTH - 2700),
                xytext=(-0.80 * R_EARTH, R_EARTH - 2400),
                fontsize=9, color=COLORS[6], style="italic",
                arrowprops=dict(arrowstyle="->", color=COLORS[6], lw=0.9))

    # Surface volcanoes / arcs
    for x0 in [-0.94 * R_EARTH, -0.88 * R_EARTH, 0.78 * R_EARTH]:
        ax.plot(x0, 0, marker="^", color="#D55E00",
                markersize=13, markeredgecolor=COLORS[6], zorder=6)

    # 660 label
    ax.text(-0.02 * R_EARTH, R_EARTH - 660 + 30,
            "660 km", fontsize=9, color=COLORS[6], ha="center")
    # CMB label
    ax.text(0.02 * R_EARTH, R_EARTH - 2891 - 60,
            "CMB (2891 km)", fontsize=9, color=COLORS[6], ha="center")

    # Layer labels at side
    ax.text(-R_EARTH * 1.01, R_EARTH - 330, "upper mantle",
            fontsize=10, color=COLORS[6], ha="right", style="italic")
    ax.text(-R_EARTH * 1.01, R_EARTH - 1700, "lower mantle",
            fontsize=10, color=COLORS[6], ha="right", style="italic")
    ax.text(-R_EARTH * 1.01, R_EARTH - 4300, "outer core",
            fontsize=10, color=COLORS[6], ha="right", style="italic")

    ax.set_xlim(-R_EARTH * 1.25, R_EARTH * 1.25)
    ax.set_ylim(-R_EARTH * 0.10, R_EARTH * 1.12)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Global mantle tomography: the picture that three decades "
                 "of data have built",
                 color=COLORS[6])

    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main("assets/figures/fig_12_global_mantle_tomography.png")
