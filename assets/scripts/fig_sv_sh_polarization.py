"""
fig_sv_sh_polarization.py

Scientific content: Three-dimensional diagram showing the decomposition of
S-wave polarization into SV (in the vertical plane containing the ray) and
SH (horizontal, perpendicular to the ray plane). The P-wave direction, SV,
and SH form an orthogonal triad.

Replaces: Figure 2.8g from W.W. Norton "Introduction to Applied Geophysics"
(Copyright © 2006 W.W. Norton & Company) — legacy slide 11.

Output: assets/figures/fig_sv_sh_polarization.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D

# ── Global rcParams ─────────────────────────────────────────────────
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

BLUE   = "#0072B2"
ORANGE = "#E69F00"
VERM   = "#D55E00"
SKY    = "#56B4E9"
BLACK  = "#000000"


def main():
    fig = plt.figure(figsize=(8, 7))
    ax = fig.add_subplot(111, projection="3d")

    # Define ray direction: propagating downward and to the right
    # in the x-z plane (z positive downward convention for geophysics,
    # but for 3D plotting we use z-up and flip labels)
    ray_angle_deg = 40  # angle from horizontal
    ray_angle = np.radians(ray_angle_deg)

    # Ray direction unit vector (x forward, y to side, z up)
    ray_dir = np.array([np.cos(ray_angle), 0, -np.sin(ray_angle)])

    # SV: in the vertical plane containing the ray, perpendicular to ray
    sv_dir = np.array([np.sin(ray_angle), 0, np.cos(ray_angle)])

    # SH: horizontal, perpendicular to ray plane
    sh_dir = np.array([0, 1, 0])

    origin = np.array([0, 0, 0])
    scale = 1.5

    # Draw the ray (P direction)
    ray_start = origin - 1.0 * ray_dir
    ray_end = origin + 2.0 * ray_dir
    ax.plot(*zip(ray_start, ray_end), color=BLUE, lw=2.5, zorder=5)
    # Arrowhead at the end
    ax.quiver(*origin, *(ray_dir * scale), color=BLUE, lw=2.5,
              arrow_length_ratio=0.15, zorder=5)
    ax.text(*(origin + ray_dir * (scale + 0.3)), "P (ray direction)",
            fontsize=12, color=BLUE, fontweight="bold", ha="left")

    # Draw SV (double-headed arrow)
    sv_end1 = origin + sv_dir * scale * 0.8
    sv_end2 = origin - sv_dir * scale * 0.8
    ax.quiver(*origin, *(sv_dir * scale * 0.8), color=VERM, lw=2.5,
              arrow_length_ratio=0.18, zorder=5)
    ax.quiver(*origin, *(-sv_dir * scale * 0.8), color=VERM, lw=2.5,
              arrow_length_ratio=0.18, zorder=5)
    ax.text(*(origin + sv_dir * (scale * 0.8 + 0.3)), "SV",
            fontsize=13, color=VERM, fontweight="bold")

    # Draw SH (double-headed arrow)
    ax.quiver(*origin, *(sh_dir * scale * 0.8), color=ORANGE, lw=2.5,
              arrow_length_ratio=0.18, zorder=5)
    ax.quiver(*origin, *(-sh_dir * scale * 0.8), color=ORANGE, lw=2.5,
              arrow_length_ratio=0.18, zorder=5)
    ax.text(*(origin + sh_dir * (scale * 0.8 + 0.3)), "SH",
            fontsize=13, color=ORANGE, fontweight="bold")

    # Draw the vertical plane containing the ray (semi-transparent)
    xx = np.array([[-1.5, 2.5], [-1.5, 2.5]])
    yy = np.array([[0, 0], [0, 0]])
    zz = np.array([[1.5, 1.5], [-2.0, -2.0]])
    ax.plot_surface(xx, yy, zz, alpha=0.08, color=SKY, zorder=1)
    ax.text(2.2, 0, 1.3, "Vertical plane\n(sagittal plane)",
            fontsize=10, color=SKY, ha="center", style="italic")

    # Draw the surface (horizontal plane at z=0 for reference)
    xs = np.array([[-2, 3], [-2, 3]])
    ys = np.array([[-2, -2], [2, 2]])
    zs = np.array([[0, 0], [0, 0]])
    # Don't draw surface to keep it clean

    # Formatting
    ax.set_xlim(-2, 3)
    ax.set_ylim(-2, 2)
    ax.set_zlim(-2, 2)
    ax.set_xlabel("Horizontal (propagation)", fontsize=11)
    ax.set_ylabel("Horizontal (transverse)", fontsize=11)
    ax.set_zlabel("Vertical", fontsize=11)
    ax.view_init(elev=20, azim=-55)

    # Remove grid for cleaner look
    ax.grid(False)
    ax.xaxis.pane.fill = False
    ax.yaxis.pane.fill = False
    ax.zaxis.pane.fill = False
    ax.xaxis.pane.set_edgecolor("gray")
    ax.yaxis.pane.set_edgecolor("gray")
    ax.zaxis.pane.set_edgecolor("gray")

    ax.set_title("S-wave Polarization Decomposition", fontsize=14, fontweight="bold", pad=15)

    plt.savefig("assets/figures/fig_sv_sh_polarization.png")
    plt.close()
    print("Saved: assets/figures/fig_sv_sh_polarization.png")


if __name__ == "__main__":
    main()
