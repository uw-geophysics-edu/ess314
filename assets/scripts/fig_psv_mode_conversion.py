"""
fig_psv_mode_conversion.py

Scientific content: When a P-wave strikes a planar interface at oblique
incidence, four outgoing waves are generated — reflected P, reflected SV,
transmitted P, and transmitted SV — each governed by the generalized
Snell's law with a single ray parameter p.

The figure shows:
  - A horizontal interface between two media
  - Incident P-wave ray
  - Four outgoing rays (reflected P, reflected SV, transmitted P, transmitted SV)
  - All angles labelled from the interface normal
  - Particle-motion arrows (longitudinal for P, transverse for SV)
  - The generalized Snell's law equation

Output: assets/figures/fig_psv_mode_conversion.png
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

BLUE = "#0072B2"
SKY = "#56B4E9"
GREEN = "#009E73"
ORANGE = "#E69F00"
VERM = "#D55E00"
PURPLE = "#882255"
BLACK = "#000000"


def draw_ray(ax, origin, angle_from_normal, length, color, lw=2.5,
             label=None, going_up=True, particle_motion="P"):
    """
    Draw a ray from *origin* at *angle_from_normal* (radians, measured
    from the vertical).  going_up=True means the ray goes into y>0;
    going_up=False means y<0.
    """
    sign = 1.0 if going_up else -1.0
    dx = length * np.sin(angle_from_normal)
    dy = sign * length * np.cos(angle_from_normal)
    end = np.array([origin[0] + dx, origin[1] + dy])

    ax.annotate("", xy=end, xytext=origin,
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.25",
                                color=color, lw=lw))

    # Particle-motion indicator (small double arrow near midpoint)
    mid = 0.55 * np.array([dx, dy]) + origin
    ray_dir = np.array([dx, dy])
    ray_dir /= np.linalg.norm(ray_dir)
    if particle_motion == "P":
        # Longitudinal: along ray
        pm_dir = ray_dir
    else:
        # Transverse: perpendicular to ray
        pm_dir = np.array([-ray_dir[1], ray_dir[0]])
    pm_len = 0.22
    p1 = mid - pm_len * pm_dir
    p2 = mid + pm_len * pm_dir
    ax.annotate("", xy=p2, xytext=p1,
                arrowprops=dict(arrowstyle="<->", color=color, lw=1.5))

    if label:
        # Place label near the end
        offset = 0.15 * pm_dir + 0.2 * ray_dir
        ax.text(end[0] + offset[0], end[1] + offset[1], label,
                fontsize=12, color=color, fontweight="bold",
                ha="center", va="center")

    return end


def draw_angle_arc(ax, center, angle_start, angle_end, radius, color,
                   label=None, label_radius=None):
    """Draw an arc showing the angle from the normal."""
    if label_radius is None:
        label_radius = radius + 0.15
    theta = np.linspace(angle_start, angle_end, 50)
    xs = center[0] + radius * np.sin(theta)
    ys = center[1] + radius * np.cos(theta)
    ax.plot(xs, ys, color=color, lw=1.5)
    if label:
        mid_theta = 0.5 * (angle_start + angle_end)
        lx = center[0] + label_radius * np.sin(mid_theta)
        ly = center[1] + label_radius * np.cos(mid_theta)
        ax.text(lx, ly, label, fontsize=11, color=color,
                ha="center", va="center")


def main():
    fig, ax = plt.subplots(figsize=(10, 9))

    O = np.array([0.0, 0.0])  # incidence point

    # ---- Media ----
    ax.axhline(0, color=BLACK, lw=2.5, zorder=3)
    ax.fill_between([-5, 5], [0, 0], [5, 5], color="#E8F0FE", alpha=0.35)
    ax.fill_between([-5, 5], [0, 0], [-5, -5], color="#E8FAF0", alpha=0.35)

    ax.text(-4.4, 4.2, "Medium 1", fontsize=14, color=BLUE, fontweight="bold")
    ax.text(-4.4, 3.5, r"$V_{P1},\; V_{S1},\; \rho_1$", fontsize=12, color=BLUE)
    ax.text(-4.4, -4.2, "Medium 2", fontsize=14, color=GREEN, fontweight="bold")
    ax.text(-4.4, -3.5, r"$V_{P2},\; V_{S2},\; \rho_2$", fontsize=12, color=GREEN)

    # ---- Interface normal (dashed) ----
    ax.plot([0, 0], [-4.5, 4.5], color="gray", ls="--", lw=1.2, zorder=1)
    ax.text(0.15, 4.3, "normal", fontsize=10, color="gray", fontstyle="italic")

    # ---- Velocities (for computing angles) ----
    VP1, VS1 = 5000, 2900
    VP2, VS2 = 6500, 3750

    theta_P1 = np.radians(35)  # incident P angle
    p = np.sin(theta_P1) / VP1  # ray parameter

    theta_S1 = np.arcsin(p * VS1)
    theta_P2 = np.arcsin(p * VP2)
    theta_S2 = np.arcsin(p * VS2)

    ray_len = 4.0

    # ---- Incident P-wave (from upper-left, going DOWN-RIGHT to O) ----
    inc_dx = ray_len * np.sin(theta_P1)
    inc_dy = ray_len * np.cos(theta_P1)
    inc_start = np.array([O[0] - inc_dx, O[1] + inc_dy])
    ax.annotate("", xy=O, xytext=inc_start,
                arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.25",
                                color=BLACK, lw=2.5))
    # Particle motion for incident P
    mid_inc = 0.5 * (inc_start + O)
    inc_dir = (O - inc_start)
    inc_dir /= np.linalg.norm(inc_dir)
    pm_len = 0.22
    ax.annotate("", xy=mid_inc + pm_len * inc_dir,
                xytext=mid_inc - pm_len * inc_dir,
                arrowprops=dict(arrowstyle="<->", color=BLACK, lw=1.5))
    ax.text(inc_start[0] - 0.6, inc_start[1] - 0.1,
            "Incident P", fontsize=12, color=BLACK, fontweight="bold",
            ha="center")

    # ---- Reflected P (upper-RIGHT, mirror of incident about normal) ----
    draw_ray(ax, O, theta_P1, ray_len, BLUE, label="Reflected P",
             going_up=True, particle_motion="P")

    # ---- Reflected SV (upper-RIGHT, steeper than reflected P) ----
    draw_ray(ax, O, theta_S1, ray_len * 0.9, PURPLE, label="Reflected SV",
             going_up=True, particle_motion="SV")

    # ---- Transmitted P (lower-RIGHT) ----
    draw_ray(ax, O, theta_P2, ray_len, GREEN, label="Transmitted P",
             going_up=False, particle_motion="P")

    # ---- Transmitted SV (lower-RIGHT, steeper than transmitted P) ----
    draw_ray(ax, O, theta_S2, ray_len * 0.9, ORANGE, label="Transmitted SV",
             going_up=False, particle_motion="SV")

    # ---- Angle arcs ----
    # Incident P (LEFT of normal: arc from 0 toward negative angle)
    draw_angle_arc(ax, O, -theta_P1, 0, 1.2, BLACK,
                   label=r"$\theta_{P1}$", label_radius=1.55)
    # Reflected P (RIGHT of normal)
    draw_angle_arc(ax, O, 0, theta_P1, 1.5, BLUE,
                   label=r"$\theta_{P1}$", label_radius=1.85)
    # Reflected SV (RIGHT of normal, smaller angle — steeper)
    draw_angle_arc(ax, O, 0, theta_S1, 1.0, PURPLE,
                   label=r"$\theta_{S1}$", label_radius=1.3)
    # Transmitted P (RIGHT of downward normal)
    draw_angle_arc(ax, O, -theta_P2, 0, -1.5, GREEN,
                   label=r"$\theta_{P2}$", label_radius=-1.85)
    # Transmitted SV
    draw_angle_arc(ax, O, -theta_S2, 0, -1.0, ORANGE,
                   label=r"$\theta_{S2}$", label_radius=-1.3)

    # ---- Generalized Snell's law label ----
    eq = (r"$p = \dfrac{\sin\theta_{P1}}{V_{P1}}"
          r" = \dfrac{\sin\theta_{S1}}{V_{S1}}"
          r" = \dfrac{\sin\theta_{P2}}{V_{P2}}"
          r" = \dfrac{\sin\theta_{S2}}{V_{S2}}$")
    ax.text(0, -4.7, eq, fontsize=13, ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.4", fc="white", ec="gray", alpha=0.9))

    # ---- Particle-motion legend ----
    ax.text(3.3, 4.3, r"$\leftrightarrow$ along ray = P",
            fontsize=10, color="gray")
    ax.text(3.3, 3.7, r"$\leftrightarrow$ $\perp$ ray = SV",
            fontsize=10, color="gray")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-5.2, 5)
    ax.set_aspect("equal")
    ax.axis("off")

    fig.tight_layout()
    fig.savefig("assets/figures/fig_psv_mode_conversion.png",
                bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("Saved: assets/figures/fig_psv_mode_conversion.png")


if __name__ == "__main__":
    main()
