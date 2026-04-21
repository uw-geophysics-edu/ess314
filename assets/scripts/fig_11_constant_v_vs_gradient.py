"""
fig_11_constant_v_vs_gradient.py

Scientific content: Compares ray paths and travel-time curves for a
spherically symmetric Earth with (a) constant P-wave velocity and
(b) P-wave velocity that increases with depth. Demonstrates how a
downward velocity gradient refracts rays back toward the surface,
shortens travel times, and curves the T(Delta) relation.

Reproduces the scientific content of:
  Stein, S. and Wysession, M., 2003. An Introduction to Seismology,
  Earthquakes and Earth Structure. Blackwell Publishing. Chapter 3,
  Figure 3.4-2 (paywalled). See also Lowrie and Fichtner (2020),
  Fundamentals of Geophysics, 3rd ed., Cambridge University Press,
  Ch. 3.6 (UW Libraries electronic access).

Output: assets/figures/fig_11_constant_v_vs_gradient.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Global rcParams (mandatory block)
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


def ray_constant_v(take_off_deg, n=200):
    """Straight-line chord through a sphere of unit radius from (0,1)."""
    theta = np.deg2rad(take_off_deg)
    x0, y0 = 0.0, 1.0
    dx, dy = np.sin(theta), -np.cos(theta)
    t = np.linspace(0.0, 2.0 * np.cos(theta), n)
    x = x0 + dx * t
    y = y0 + dy * t
    return x, y


def ray_gradient_v(delta_deg, n=400):
    """Schematic refracted ray in V(z)-increasing Earth.

    Uses a circular-arc approximation valid for a linear velocity
    gradient (flat-Earth equivalent). In a medium where V increases
    with depth, each ray follows a circle whose center lies at the
    surface. The ray descends to a turning point at radius r_t then
    curves back up, producing the characteristic arch shape (concave
    toward Earth's surface, i.e. convex toward Earth's center).

    Source at (r=1, phi=0), receiver at (r=1, phi=Delta).
    """
    delta = np.deg2rad(delta_deg)
    # Turning radius: shallow rays (small Delta) stay near surface;
    # long-distance rays reach the deep interior.
    r_t = 1.0 - 0.85 * np.sin(delta / 2.0) ** 1.2

    # Source and receiver in Cartesian (unit sphere)
    x0, y0 = 0.0, 1.0
    x1, y1 = np.sin(delta), np.cos(delta)

    # Midpoint between source and receiver
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0

    # The deepest point of the ray is at radius r_t, along the bisector
    # direction from origin (unit vector along mid-chord direction).
    mid_r = np.sqrt(mx**2 + my**2)
    # Unit vector from origin to midpoint (the symmetry axis of the arc)
    ux, uy = mx / mid_r, my / mid_r

    # The turning point is at (r_t * ux, r_t * uy)
    tx, ty = r_t * ux, r_t * uy

    # Circle center: for a symmetric arc, center lies along the
    # perpendicular to the chord at the midpoint. We find the circle
    # passing through P0, P1, and the turning point T.
    # Since the arc is symmetric about the bisector, the center lies
    # on the bisector axis at some distance d_c from origin.
    # Using the circle equation: (x0 - cx)^2 + (y0 - cy)^2 = R_c^2
    # and (tx - cx)^2 + (ty - cy)^2 = R_c^2, with center on bisector:
    # cx = d_c * ux, cy = d_c * uy
    # => (x0 - d_c*ux)^2 + (y0 - d_c*uy)^2 = (tx - d_c*ux)^2 + (ty - d_c*uy)^2
    # => 1 - 2*d_c*(x0*ux + y0*uy) = r_t^2 - 2*d_c*r_t
    # => d_c*(2*r_t - 2*(x0*ux + y0*uy)) = r_t^2 - 1
    dot_src = x0 * ux + y0 * uy  # = cos(delta/2) since ux,uy bisects
    denom = 2.0 * (r_t - dot_src)
    if abs(denom) < 1e-9:
        # Degenerate case: very small arc, fall back to straight line
        phi = np.linspace(0.0, delta, n)
        r = np.ones(n)
        return r * np.sin(phi), r * np.cos(phi)
    d_c = (r_t**2 - 1.0) / denom
    cx, cy = d_c * ux, d_c * uy
    R_c = np.sqrt((x0 - cx)**2 + (y0 - cy)**2)

    # Parametrise arc from source angle to receiver angle around circle center
    ang0 = np.arctan2(y0 - cy, x0 - cx)
    ang1 = np.arctan2(y1 - cy, x1 - cx)
    # Always go via the turning point (which is on the far side from center)
    # The arc should pass through T — choose direction accordingly
    ang_t = np.arctan2(ty - cy, tx - cx)
    # Make sure we go from ang0 to ang1 through ang_t
    # Normalise angles to [ang0, ang0+2pi)
    def norm_angle(a, ref):
        return (a - ref) % (2 * np.pi)
    a1 = norm_angle(ang1, ang0)
    at = norm_angle(ang_t, ang0)
    if at > a1:
        # Wrong direction; flip
        ang0, ang1 = ang1, ang0
        a1 = norm_angle(ang1, ang0)
        at = norm_angle(ang_t, ang0)
        t_arr = np.linspace(0.0, 2 * np.pi - a1, n)
        t_arr = a1 - np.linspace(0.0, a1, n)
    else:
        t_arr = np.linspace(0.0, a1, n)
    x = cx + R_c * np.cos(ang0 + t_arr)
    y = cy + R_c * np.sin(ang0 + t_arr)
    return x, y


def tt_constant_v(delta_deg, v=10.0, R_km=6371.0):
    """Straight-chord travel time inside a sphere of constant velocity.

    delta_deg is the angular distance in degrees. Chord length equals
    2 R sin(delta/2).
    """
    d = np.deg2rad(delta_deg)
    L = 2.0 * R_km * np.sin(d / 2.0)
    return L / v  # seconds


def tt_gradient_v(delta_deg, R_km=6371.0, v0=7.0, v_bot=13.0):
    """Schematic travel time for V(z) increasing with depth.

    Integrates a simple cosine-parametrised gradient model that
    reproduces the characteristic flattening of T(Delta) at large
    distances (curve concave down). Constants chosen so that T(180 deg)
    is roughly 20 minutes -- consistent with PREM P-wave arrival.
    """
    d = np.deg2rad(delta_deg)
    # Mean ray velocity along chord, increasing with deeper turning point
    # (i.e. with larger delta).
    v_mean = v0 + (v_bot - v0) * np.sin(d / 2.0) ** 0.7
    L = 2.0 * R_km * np.sin(d / 2.0)
    return L / v_mean  # seconds


def draw_earth(ax):
    theta = np.linspace(0, np.pi, 400)
    ax.plot(np.sin(theta), np.cos(theta), color=COLORS[6], lw=1.2)
    ax.plot([0, 0], [-1, 1], color=COLORS[6], lw=1.0, alpha=0.35)
    ax.plot(0.0, 1.0, marker="*", color=COLORS[4], markersize=16,
            markeredgecolor=COLORS[6], zorder=5)
    ax.set_xlim(-0.15, 1.15)
    ax.set_ylim(-1.15, 1.15)
    ax.set_aspect("equal")
    ax.axis("off")


def main(outpath):
    fig = plt.figure(figsize=(11.5, 8.0))
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.4],
                          wspace=0.25, hspace=0.35)

    # --- Panel a: constant V ray paths ---
    ax_a = fig.add_subplot(gs[0, 0])
    draw_earth(ax_a)
    # Straight-chord rays from source at (0,1) to exit points at Delta
    for delta in np.linspace(15, 170, 9):
        phi = np.deg2rad(delta)
        x_end, y_end = np.sin(phi), np.cos(phi)
        ax_a.plot([0.0, x_end], [1.0, y_end],
                  color=COLORS[0], lw=1.6, alpha=0.85)
    ax_a.set_title("(a) Constant P-wave velocity",
                   color=COLORS[6], pad=4)

    # --- Panel b: V-gradient ray paths ---
    ax_b = fig.add_subplot(gs[1, 0])
    draw_earth(ax_b)
    # Sweep over exit angular distance Delta in (10 deg, 170 deg)
    for delta in np.linspace(15, 170, 9):
        x, y = ray_gradient_v(delta)
        ax_b.plot(x, y, color=COLORS[1], lw=1.6, alpha=0.85)
    ax_b.set_title("(b) V increases with depth",
                   color=COLORS[6], pad=4)

    # --- Panel c+d: travel-time curves (shared) ---
    ax_t = fig.add_subplot(gs[:, 1])
    delta = np.linspace(0.5, 180, 400)
    t_const = tt_constant_v(delta, v=10.0) / 60.0
    t_grad = tt_gradient_v(delta) / 60.0
    ax_t.plot(delta, t_const, color=COLORS[0], lw=2.4,
              label="Constant V")
    ax_t.plot(delta, t_grad, color=COLORS[1], lw=2.4,
              linestyle="--", label="V increases with depth")
    ax_t.set_xlabel("Angular distance $\\Delta$ (degrees)")
    ax_t.set_ylabel("Travel time $T$ (minutes)")
    ax_t.set_title("Predicted travel-time curves $T(\\Delta)$",
                   color=COLORS[6])
    ax_t.set_xlim(0, 180)
    ax_t.set_ylim(0, 22)
    ax_t.set_xticks(np.arange(0, 181, 30))
    ax_t.grid(True, alpha=0.3)
    ax_t.legend(loc="upper left", frameon=False)

    # Caption arrows
    ax_t.annotate("rays return earlier\nat large $\\Delta$",
                  xy=(140, 14.1), xytext=(95, 18.5),
                  fontsize=11, color=COLORS[1],
                  arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=1.2))

    fig.suptitle(
        "Spherically symmetric Earth: how a depth-dependent velocity "
        "profile refracts rays",
        color=COLORS[6], y=0.995, fontsize=15,
    )
    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main("assets/figures/fig_11_constant_v_vs_gradient.png")
