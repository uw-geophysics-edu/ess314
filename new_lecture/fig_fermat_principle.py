"""
fig_fermat_principle.py

Scientific content: Geometry for deriving Snell's law from Fermat's
principle of least time. Source A above interface, receiver B below,
optimal crossing point O, and three sub-optimal paths shown as dashed.

Replaces: Legacy slides 25-26 from 314_2023_4_seismic_waves.pdf
(Cambridge University Press figures — copyrighted).

Output: assets/figures/fig_fermat_principle.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE = "#0072B2"; SKY = "#56B4E9"; GREEN = "#009E73"
ORANGE = "#E69F00"; VERM = "#D55E00"; BLACK = "#000000"


def main():
    fig, ax = plt.subplots(figsize=(10, 7))

    h = 3.0    # height/depth
    d = 8.0    # horizontal separation
    V1 = 3.0   # speed in medium 1
    V2 = 5.0   # speed in medium 2

    A = np.array([1.0, h])
    B = np.array([1.0 + d, -h])

    # Optimal crossing point (from Snell's law)
    # sin(theta1)/V1 = sin(theta2)/V2
    # Solve numerically for x_opt
    from scipy.optimize import brentq
    def dTdx(x):
        return x / (V1 * np.sqrt(h**2 + x**2)) - (d-x) / (V2 * np.sqrt(h**2 + (d-x)**2))
    x_opt = brentq(dTdx, 0.1, d-0.1)
    O = np.array([A[0] + x_opt, 0])

    # Interface
    ax.axhline(0, color=BLACK, lw=2)
    ax.fill_between([-0.5, 11], [0, 0], [5, 5], color="#E8F0FE", alpha=0.3)
    ax.fill_between([-0.5, 11], [0, 0], [-5, -5], color="#E8FAF0", alpha=0.3)
    ax.text(0, 4.0, "Medium 1: $V_1$", fontsize=13, color=BLUE, fontweight="bold")
    ax.text(0, -4.0, "Medium 2: $V_2 > V_1$", fontsize=13, color=GREEN, fontweight="bold")

    # Sub-optimal paths (dashed gray)
    for x_sub in [x_opt - 2.5, x_opt - 1.2, x_opt + 1.5, x_opt + 3.0]:
        if 0 < x_sub < d:
            O_sub = np.array([A[0] + x_sub, 0])
            ax.plot([A[0], O_sub[0]], [A[1], 0], color="#BBBBBB", lw=1.2, ls="--")
            ax.plot([O_sub[0], B[0]], [0, B[1]], color="#BBBBBB", lw=1.2, ls="--")

    # Optimal path (solid, colored)
    ax.plot([A[0], O[0]], [A[1], 0], color=BLUE, lw=2.5, zorder=4)
    ax.plot([O[0], B[0]], [0, B[1]], color=GREEN, lw=2.5, zorder=4)

    # Points
    ax.plot(*A, "o", color=VERM, markersize=10, zorder=5)
    ax.plot(*B, "o", color=VERM, markersize=10, zorder=5)
    ax.plot(*O, "s", color=ORANGE, markersize=9, zorder=5)

    ax.text(A[0]-0.5, A[1]+0.3, "A (source)", fontsize=13, fontweight="bold", color=VERM)
    ax.text(B[0]+0.2, B[1]-0.4, "B (receiver)", fontsize=13, fontweight="bold", color=VERM)
    ax.text(O[0]+0.2, 0.3, "O", fontsize=13, fontweight="bold", color=ORANGE)

    # Dimension labels
    # h above
    ax.annotate("", xy=(A[0]-0.3, 0), xytext=(A[0]-0.3, h),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1))
    ax.text(A[0]-0.7, h/2, "$h$", fontsize=13, ha="center", color=BLACK)

    # h below
    ax.annotate("", xy=(B[0]+0.3, 0), xytext=(B[0]+0.3, -h),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1))
    ax.text(B[0]+0.7, -h/2, "$h$", fontsize=13, ha="center", color=BLACK)

    # x
    ax.annotate("", xy=(O[0], -0.4), xytext=(A[0], -0.4),
                arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1))
    ax.text((A[0]+O[0])/2, -0.8, "$x$", fontsize=13, ha="center", color=BLUE)

    # d - x
    ax.annotate("", xy=(B[0], -0.4), xytext=(O[0], -0.4),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1))
    ax.text((O[0]+B[0])/2, -0.8, "$d - x$", fontsize=13, ha="center", color=GREEN)

    # d
    ax.annotate("", xy=(B[0], 4.2), xytext=(A[0], 4.2),
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1, ls="--"))
    ax.text((A[0]+B[0])/2, 4.5, "$d$", fontsize=13, ha="center", color=BLACK)

    # Angle arcs
    # theta_i at O
    arc_r = 1.0
    # Incident angle from vertical
    theta_i = np.arctan2(x_opt, h)
    arc_th = np.linspace(np.pi/2, np.pi/2 + theta_i, 30)
    ax.plot(O[0] + arc_r*np.cos(arc_th), arc_r*np.sin(arc_th),
            color=BLUE, lw=1.5)
    ax.text(O[0] + 0.2, 1.2, "$\\theta_1$", fontsize=13, color=BLUE)

    # Refracted angle from vertical (downward)
    theta_r = np.arctan2(d - x_opt, h)
    arc_th2 = np.linspace(-np.pi/2, -np.pi/2 + theta_r, 30)
    ax.plot(O[0] + arc_r*np.cos(arc_th2), arc_r*np.sin(arc_th2),
            color=GREEN, lw=1.5)
    ax.text(O[0] + 0.5, -1.3, "$\\theta_2$", fontsize=13, color=GREEN)

    # Normal at O
    ax.plot([O[0], O[0]], [-2.0, 2.0], ls=":", color="gray", lw=1)

    # Travel time equation box
    bbox_props = dict(boxstyle="round,pad=0.5", fc="#FFF8F0", ec=VERM, lw=1.5)
    ax.text(7.5, 3.2,
            "$T(x) = \\dfrac{\\sqrt{h^2 + x^2}}{V_1} + \\dfrac{\\sqrt{h^2 + (d-x)^2}}{V_2}$",
            fontsize=13, ha="center", va="center", bbox=bbox_props)
    ax.text(7.5, 1.8, "Minimize: $dT/dx = 0$",
            fontsize=12, ha="center", color=VERM, fontweight="bold")

    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-4.5, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Fermat's Principle: Minimum Travel Time Path",
                 fontsize=15, fontweight="bold", pad=15)

    plt.tight_layout()
    plt.savefig("assets/figures/fig_fermat_principle.png", bbox_inches="tight")
    plt.close()
    print("Saved: assets/figures/fig_fermat_principle.png")


if __name__ == "__main__":
    main()
