"""
fig_wavefronts_isotropic_hetero.py

Scientific content: Comparison of wavefronts and rays in (a) a homogeneous
isotropic medium (circular wavefronts, straight rays) and (b) a medium
containing a low-velocity anomaly (sedimentary basin / magma chamber).
Rays bend *into* the slow region; wavefronts retard inside it.

Output: assets/figures/fig_wavefronts_isotropic_hetero.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Ellipse

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE = "#0072B2"; SKY = "#56B4E9"; GREEN = "#009E73"
ORANGE = "#E69F00"; RED = "#D55E00"; BLACK = "#000000"

# ── Velocity model for panel (b) ──────────────────────────────────────────
# Low-velocity elliptical anomaly (basin / magma chamber)
ANOM_CX, ANOM_CY = 0.0, -2.8   # centre of the anomaly
ANOM_RX, ANOM_RY = 2.0, 1.2    # semi-axes (horizontal, vertical)
V_BG = 5.0                      # background velocity (arbitrary units)
V_SLOW = 2.5                    # anomaly velocity


def velocity(x, y):
    """Return velocity at (x, y). Smooth Gaussian low-velocity anomaly."""
    r2 = ((x - ANOM_CX) / ANOM_RX) ** 2 + ((y - ANOM_CY) / ANOM_RY) ** 2
    # Smooth Gaussian transition instead of hard boundary
    dv = (V_BG - V_SLOW) * np.exp(-2.0 * r2)
    return V_BG - dv


def grad_velocity(x, y):
    """Return (dV/dx, dV/dy) analytically."""
    r2 = ((x - ANOM_CX) / ANOM_RX) ** 2 + ((y - ANOM_CY) / ANOM_RY) ** 2
    common = (V_BG - V_SLOW) * np.exp(-2.0 * r2) * 4.0
    dvdx = common * (x - ANOM_CX) / ANOM_RX ** 2
    dvdy = common * (y - ANOM_CY) / ANOM_RY ** 2
    return dvdx, dvdy


def trace_ray(x0, y0, vx0, vy0, ds=0.02, nsteps=600):
    """Trace a ray through the velocity field using the ray-tracing ODE.

    The kinematic ray equations in 2-D:
        dx/ds = V * px,   dy/ds = V * py
        dpx/ds = -dV/dx / V,   dpy/ds = -dV/dy / V
    where (px, py) is the unit slowness direction.
    """
    # Normalise initial direction
    norm = np.hypot(vx0, vy0)
    px, py = vx0 / norm, vy0 / norm
    xs, ys = [x0], [y0]
    x, y = x0, y0
    for _ in range(nsteps):
        v = velocity(x, y)
        dvdx, dvdy = grad_velocity(x, y)
        # Advance position
        x += v * px * ds
        y += v * py * ds
        # Advance slowness direction
        px -= (dvdx / v) * ds
        py -= (dvdy / v) * ds
        # Re-normalise
        norm = np.hypot(px, py)
        px /= norm; py /= norm
        xs.append(x); ys.append(y)
        if y > 0.5 or y < -5.5 or abs(x) > 5.5:
            break
    return np.array(xs), np.array(ys)


def compute_wavefront(x0, y0, t_target, n_rays=360, ds=0.02):
    """Shoot rays in all downward directions and collect positions at travel time t_target."""
    wf_x, wf_y = [], []
    for angle_deg in np.linspace(181, 359, n_rays):
        angle = np.radians(angle_deg)
        vx0, vy0 = np.cos(angle), np.sin(angle)
        norm = np.hypot(vx0, vy0)
        px, py = vx0 / norm, vy0 / norm
        x, y = x0, y0
        t_accum = 0.0
        for _ in range(2000):
            v = velocity(x, y)
            dvdx, dvdy = grad_velocity(x, y)
            x += v * px * ds
            y += v * py * ds
            px -= (dvdx / v) * ds
            py -= (dvdy / v) * ds
            norm_p = np.hypot(px, py)
            px /= norm_p; py /= norm_p
            t_accum += ds / v
            if t_accum >= t_target:
                wf_x.append(x); wf_y.append(y)
                break
            if y > 0.5 or y < -6 or abs(x) > 6:
                break
    return np.array(wf_x), np.array(wf_y)


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
        theta = np.linspace(np.pi, 2 * np.pi, 100)
        ax.plot(r * np.cos(theta), r * np.sin(theta), color=BLUE, lw=1.8)

    # Straight rays
    for angle_deg in [-150, -130, -110, -90, -70, -50, -30]:
        angle = np.radians(angle_deg)
        ax.annotate("", xy=(4.3 * np.cos(angle), 4.3 * np.sin(angle)),
                     xytext=(0, 0),
                     arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.2))

    ax.text(0, -4.7, "Constant velocity\nStraight rays, circular wavefronts",
            ha="center", fontsize=11, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=BLUE, alpha=0.9))
    ax.axis("off")

    # ── Panel B: Low-velocity anomaly ───────────────────────────────
    ax = axes[1]
    ax.set_title("(b) Low-velocity anomaly", fontsize=14, fontweight="bold")
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 0.5)
    ax.set_aspect("equal")

    # Background velocity field as colour mesh
    xg = np.linspace(-5, 5, 200)
    yg = np.linspace(-5, 0.5, 120)
    Xg, Yg = np.meshgrid(xg, yg)
    Vg = velocity(Xg, Yg)
    ax.pcolormesh(Xg, Yg, Vg, cmap="RdYlBu", vmin=V_SLOW - 0.3,
                  vmax=V_BG + 0.3, shading="gouraud", zorder=0, alpha=0.35)

    # Anomaly outline (dashed ellipse)
    ell = Ellipse((ANOM_CX, ANOM_CY), 2 * ANOM_RX, 2 * ANOM_RY,
                  fill=False, edgecolor=RED, ls="--", lw=2.0, zorder=2)
    ax.add_patch(ell)
    ax.text(ANOM_CX, ANOM_CY + 0.05, "Low $V$\n(basin / magma)",
            ha="center", va="center", fontsize=10, color=RED,
            fontweight="bold", zorder=3)

    # Velocity labels
    ax.text(-4.2, -0.3, f"$V_0 = {V_BG:.0f}$", fontsize=11,
            color=BLUE, fontweight="bold")
    ax.text(ANOM_CX + 2.4, ANOM_CY, f"$V_{{\\rm slow}} = {V_SLOW:.1f}$",
            fontsize=10, color=RED, fontweight="bold")

    # Source
    ax.plot(0, 0, "*", color=ORANGE, markersize=14, zorder=5)
    ax.text(0.3, 0.2, "Source", fontsize=11, color=ORANGE)

    # Trace and draw rays
    ray_angles = [-155, -140, -125, -110, -95, -85, -70, -55, -40, -25]
    for angle_deg in ray_angles:
        angle = np.radians(angle_deg)
        rx, ry = trace_ray(0, 0, np.cos(angle), np.sin(angle))
        # Clip to axes
        mask = (ry <= 0.5) & (ry >= -5) & (np.abs(rx) <= 5)
        rx, ry = rx[mask], ry[mask]
        if len(rx) < 3:
            continue
        ax.plot(rx, ry, color=BLACK, lw=1.0, zorder=3)
        ax.annotate("", xy=(rx[-1], ry[-1]), xytext=(rx[-3], ry[-3]),
                     arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.0),
                     zorder=3)

    # Compute and draw wavefronts
    for t_target in [0.2, 0.45, 0.75, 1.05]:
        wfx, wfy = compute_wavefront(0, 0, t_target, n_rays=400)
        if len(wfx) < 5:
            continue
        # Sort by angle for smooth curve
        angles = np.arctan2(wfy, wfx)
        order = np.argsort(angles)
        ax.plot(wfx[order], wfy[order], color=BLUE, lw=1.8, zorder=2)

    ax.text(0, -4.7,
            "Rays bend into the slow anomaly\nWavefronts retard inside it",
            ha="center", fontsize=11, style="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=RED, alpha=0.9))
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("assets/figures/fig_wavefronts_isotropic_hetero.png",
                bbox_inches="tight")
    plt.close()
    print("Saved: assets/figures/fig_wavefronts_isotropic_hetero.png")


if __name__ == "__main__":
    main()
