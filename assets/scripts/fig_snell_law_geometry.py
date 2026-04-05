"""
fig_snell_law_geometry.py

Scientific content: Geometric construction for deriving Snell's law from
Huygens' principle at a planar interface. Shows incident wavefront,
interface, two right triangles sharing hypotenuse AB, Huygens wavelet in
medium 2, and the refracted wavefront.

Replaces: Legacy slide 19 from 314_2023_4_seismic_waves.pdf (Fig. 6.17,
Cambridge University Press — copyrighted).

Output: assets/figures/fig_snell_law_geometry.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as patches

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE = "#0072B2"; SKY = "#56B4E9"; GREEN = "#009E73"
ORANGE = "#E69F00"; VERM = "#D55E00"; BLACK = "#000000"


def main():
    fig, ax = plt.subplots(figsize=(10, 8))

    # Interface
    ax.axhline(0, color=BLACK, lw=2)
    ax.fill_between([-2, 10], [0, 0], [5, 5], color="#E8F0FE", alpha=0.4)  # medium 1
    ax.fill_between([-2, 10], [0, 0], [-5, -5], color="#E8FAF0", alpha=0.4)  # medium 2

    ax.text(0.3, 4.0, "Medium 1: $V_1$", fontsize=13, color=BLUE, fontweight="bold")
    ax.text(0.3, -4.0, "Medium 2: $V_2 > V_1$", fontsize=13, color=GREEN, fontweight="bold")

    # Geometry parameters
    theta1 = np.radians(30)  # incidence angle
    V1, V2 = 3.0, 5.0  # relative speeds
    dt = 1.0
    AB = V1 * dt / np.sin(theta1)  # length of interface segment

    A = np.array([1.5, 0])
    B = np.array([1.5 + AB, 0])

    # Incident wavefront arrives at A; point C is where the wavefront
    # meets the surface at B after traveling V1*dt
    BC = V1 * dt
    # C is above B, along the incident wavefront direction
    theta2 = np.arcsin(V2 * np.sin(theta1) / V1)

    C = B + BC * np.array([-np.cos(np.pi/2 - theta1), np.sin(np.pi/2 - theta1)])

    # Huygens wavelet from A into medium 2
    AE_radius = V2 * dt
    # E is the tangent point below the interface
    wavelet_theta = np.linspace(-np.pi/2, np.pi/2, 100)
    wavelet_x = A[0] + AE_radius * np.sin(wavelet_theta)
    wavelet_y = A[1] - AE_radius * np.cos(wavelet_theta)
    # Only draw the part below the interface
    mask = wavelet_y <= 0
    ax.plot(wavelet_x[mask], wavelet_y[mask], color=GREEN, lw=1.5, ls="--")

    # E point: tangent to the wavelet from B
    E = A + AE_radius * np.array([np.sin(theta2), -np.cos(theta2)])

    # Draw incident wavefront (line through C perpendicular to incident ray)
    inc_dir = np.array([np.sin(theta1), -np.cos(theta1)])
    inc_normal = np.array([-np.cos(theta1), -np.sin(theta1)])
    # Extend the incident wavefront through C
    wf_ext = 2.0
    ax.plot([C[0] - wf_ext*inc_normal[0], C[0] + wf_ext*inc_normal[0]],
            [C[1] - wf_ext*inc_normal[1], C[1] + wf_ext*inc_normal[1]],
            color=BLUE, lw=2, label="Incident wavefront")

    # Incident rays (parallel to inc_dir, hitting A and near B)
    for start_frac in [0.0, 0.5, 1.0]:
        start = A + start_frac * (B - A) - 4.0 * inc_dir
        end = A + start_frac * (B - A)
        # Only draw above interface
        if end[1] >= -0.1:
            ax.annotate("", xy=end, xytext=start + 1.0*inc_dir,
                         arrowprops=dict(arrowstyle="-|>", color=BLUE, lw=1.2))
            ax.plot([start[0]+inc_dir[0], end[0]], [start[1]+inc_dir[1], end[1]],
                    color=BLUE, lw=1.0, alpha=0.5)

    # Refracted wavefront (tangent from B to wavelet, through E)
    ref_dir = np.array([np.sin(theta2), -np.cos(theta2)])
    ref_normal = np.array([-np.cos(theta2), -np.sin(theta2)])
    ax.plot([E[0] - 1.5*ref_normal[0], B[0]],
            [E[1] - 1.5*ref_normal[1], B[1]],
            color=GREEN, lw=2, label="Refracted wavefront")

    # Refracted rays
    for start_frac in [0.0, 0.5, 1.0]:
        origin_pt = A + start_frac * (B - A)
        end_pt = origin_pt + 3.5 * ref_dir
        if origin_pt[1] >= -0.1:
            ax.annotate("", xy=end_pt, xytext=origin_pt,
                         arrowprops=dict(arrowstyle="-|>", color=GREEN, lw=1.2))

    # Label points
    ax.plot(*A, "o", color=VERM, markersize=8, zorder=5)
    ax.plot(*B, "o", color=VERM, markersize=8, zorder=5)
    ax.plot(*C, "o", color=BLUE, markersize=6, zorder=5)
    ax.plot(*E, "o", color=GREEN, markersize=6, zorder=5)

    offset = 0.25
    ax.text(A[0]-0.4, A[1]+offset, "A", fontsize=14, fontweight="bold", color=VERM)
    ax.text(B[0]+0.15, B[1]+offset, "B", fontsize=14, fontweight="bold", color=VERM)
    ax.text(C[0]+0.15, C[1]+0.1, "C", fontsize=14, fontweight="bold", color=BLUE)
    ax.text(E[0]-0.5, E[1]-0.1, "E", fontsize=14, fontweight="bold", color=GREEN)

    # Distance labels
    ax.annotate("$V_1\\Delta t$", xy=((B[0]+C[0])/2 + 0.3, (B[1]+C[1])/2),
                fontsize=12, color=BLUE, fontweight="bold")
    ax.annotate("$V_2\\Delta t$", xy=((A[0]+E[0])/2 - 1.0, (A[1]+E[1])/2),
                fontsize=12, color=GREEN, fontweight="bold")

    # Angle arcs
    # theta_1 at B (angle between normal and incident ray)
    normal_angle = np.pi/2
    arc_r = 1.2
    arc_theta = np.linspace(normal_angle, normal_angle + theta1, 30)
    ax.plot(B[0] + arc_r*np.cos(arc_theta), B[1] + arc_r*np.sin(arc_theta),
            color=BLUE, lw=1.5)
    ax.text(B[0] + 0.3, B[1] + 1.5, "$\\theta_1$", fontsize=14, color=BLUE)

    # theta_2 at A (angle between downward normal and refracted ray)
    arc_theta2 = np.linspace(-np.pi/2, -np.pi/2 + theta2, 30)
    ax.plot(A[0] + arc_r*np.cos(arc_theta2), A[1] + arc_r*np.sin(arc_theta2),
            color=GREEN, lw=1.5)
    ax.text(A[0] + 0.5, A[1] - 1.7, "$\\theta_2$", fontsize=14, color=GREEN)

    # Normal at A (dashed vertical)
    ax.plot([A[0], A[0]], [-3.5, 2.5], ls=":", color="gray", lw=1)
    # Normal at B
    ax.plot([B[0], B[0]], [-1, 3.5], ls=":", color="gray", lw=1)

    # Equation box
    bbox_props = dict(boxstyle="round,pad=0.5", fc="#FFFFF0", ec=BLACK, lw=1.5)
    ax.text(6.5, -3.0,
            "$\\dfrac{\\sin\\theta_1}{V_1} = \\dfrac{\\sin\\theta_2}{V_2} = p$",
            fontsize=16, ha="center", va="center", bbox=bbox_props)

    ax.set_xlim(-1, 10)
    ax.set_ylim(-5, 5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Snell's Law: Geometric Derivation", fontsize=15,
                 fontweight="bold", pad=15)

    plt.tight_layout()
    plt.savefig("assets/figures/fig_snell_law_geometry.png", bbox_inches="tight")
    plt.close()
    print("Saved: assets/figures/fig_snell_law_geometry.png")


if __name__ == "__main__":
    main()
