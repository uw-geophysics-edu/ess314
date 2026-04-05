"""
fig_wavefronts_isotropic_hetero.py

Scientific content: Comparison of wavefronts and rays in (a) a homogeneous
isotropic medium (circular wavefronts, straight rays) and (b) a laterally
heterogeneous medium (distorted wavefronts, curved rays bending toward the
slow region).

Replaces: Legacy slide 17 from 314_2023_4_seismic_waves.pdf and slide 5
from 314_2023_5_seismic_waves_II.pdf (likely textbook figure).

Output: assets/figures/fig_wavefronts_isotropic_hetero.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE = "#0072B2"; SKY = "#56B4E9"; GREEN = "#009E73"
ORANGE = "#E69F00"; BLACK = "#000000"


def main():
    fig, axes = plt.subplots(1, 2, figsize=(13, 6))

    # ── Panel A: Homogeneous ────────────────────────────────────────
    ax = axes[0]
    ax.set_title("(a) Homogeneous medium", fontsize=14, fontweight="bold")
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 0.5)
    ax.set_aspect("equal")
    ax.set_facecolor("#F0F4FF")

    # Source
    ax.plot(0, 0, "*", color=ORANGE, markersize=14, zorder=5)
    ax.text(0.3, 0.2, "Source", fontsize=11, color=ORANGE)

    # Circular wavefronts
    for r in [1.0, 2.0, 3.0, 4.0]:
        theta = np.linspace(np.pi, 2*np.pi, 100)
        ax.plot(r*np.cos(theta), r*np.sin(theta), color=BLUE, lw=1.8)

    # Straight rays
    for angle_deg in [-150, -130, -110, -90, -70, -50, -30]:
        angle = np.radians(angle_deg)
        ax.annotate("", xy=(4.3*np.cos(angle), 4.3*np.sin(angle)),
                     xytext=(0, 0),
                     arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.2))

    ax.text(0, -4.7, "Constant velocity\nStraight rays, circular wavefronts",
            ha="center", fontsize=11, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=BLUE, alpha=0.9))
    ax.axis("off")

    # ── Panel B: Heterogeneous ──────────────────────────────────────
    ax = axes[1]
    ax.set_title("(b) Heterogeneous medium", fontsize=14, fontweight="bold")
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 0.5)
    ax.set_aspect("equal")

    # Background: slow left, fast right
    ax.axvspan(-5, 0, color="#E8F0FE", zorder=0)    # slow = blue tint
    ax.axvspan(0, 5, color="#E8FAF0", zorder=0)      # fast = green tint
    ax.text(-3, -0.3, "$V_1$ (slow)", fontsize=12, color=BLUE, fontweight="bold")
    ax.text(2, -0.3, "$V_2$ (fast)", fontsize=12, color=GREEN, fontweight="bold")

    # Source
    ax.plot(0, 0, "*", color=ORANGE, markersize=14, zorder=5)

    # Distorted wavefronts — fast side extends further
    for t_idx, r_base in enumerate([1.0, 2.0, 3.0, 4.0]):
        theta = np.linspace(np.pi, 2*np.pi, 100)
        # Stretch radii on the right (fast) side
        stretch = 1.0 + 0.3 * (np.cos(theta) + 1) / 2  # more stretch toward right
        r = r_base * stretch
        ax.plot(r*np.cos(theta), r*np.sin(theta), color=BLUE, lw=1.8)

    # Curved rays — bend toward slow (left)
    for angle_deg in [-150, -130, -110, -90, -70, -50, -30]:
        angle = np.radians(angle_deg)
        t_arr = np.linspace(0, 4.2, 50)
        # Simple curvature: bend toward left (slow side)
        curve_strength = 0.04 * np.cos(angle)
        x = t_arr * np.cos(angle) - curve_strength * t_arr**2
        y = t_arr * np.sin(angle)
        ax.plot(x, y, color=BLACK, lw=1.0)
        ax.annotate("", xy=(x[-1], y[-1]), xytext=(x[-3], y[-3]),
                     arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.0))

    ax.text(0, -4.7, "Variable velocity\nCurved rays, distorted wavefronts",
            ha="center", fontsize=11, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GREEN, alpha=0.9))
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("assets/figures/fig_wavefronts_isotropic_hetero.png", bbox_inches="tight")
    plt.close()
    print("Saved: assets/figures/fig_wavefronts_isotropic_hetero.png")


if __name__ == "__main__":
    main()
