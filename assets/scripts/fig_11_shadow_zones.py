"""
fig_11_shadow_zones.py

Scientific content: Cross-section of Earth showing the P-wave shadow
zone (103 deg - 143 deg) and S-wave shadow zone (beyond 103 deg), with
ray paths refracting at the core-mantle boundary (CMB) and reflecting
off the inner core boundary (ICB). This diagram encapsulates the
observational evidence that established (i) Earth has a fluid outer
core (Oldham 1906; Gutenberg 1914) and (ii) a solid inner core
(Lehmann 1936).

Reproduces the scientific content of:
  Stein, S. and Wysession, M., 2003. An Introduction to Seismology,
  Earthquakes and Earth Structure. Blackwell Publishing, Ch. 3.5
  (paywalled). Lowrie and Fichtner (2020), Fundamentals of Geophysics,
  3rd ed., Cambridge University Press, Fig. 3.29.

Output: assets/figures/fig_11_shadow_zones.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge

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


def draw_layered_earth(ax):
    """Draw mantle, outer core, inner core as concentric circles."""
    theta = np.linspace(0, 2 * np.pi, 400)
    # Mantle (outer)
    ax.fill(np.cos(theta) * R_EARTH, np.sin(theta) * R_EARTH,
            color="#F2E6D0", zorder=0)
    # Outer core
    ax.fill(np.cos(theta) * R_CMB, np.sin(theta) * R_CMB,
            color="#FFE9A6", zorder=1)
    # Inner core
    ax.fill(np.cos(theta) * R_ICB, np.sin(theta) * R_ICB,
            color="#FFD37A", zorder=2)
    # Outlines
    ax.plot(np.cos(theta) * R_EARTH, np.sin(theta) * R_EARTH,
            color=COLORS[6], lw=1.4, zorder=3)
    ax.plot(np.cos(theta) * R_CMB, np.sin(theta) * R_CMB,
            color=COLORS[6], lw=1.0, ls="--", alpha=0.7, zorder=3)
    ax.plot(np.cos(theta) * R_ICB, np.sin(theta) * R_ICB,
            color=COLORS[6], lw=1.0, ls="--", alpha=0.7, zorder=3)


def great_circle_arc(phi_src, phi_rec, r=R_EARTH, n=100):
    """Arc along the surface from source to receiver."""
    phi = np.linspace(phi_src, phi_rec, n)
    return r * np.cos(phi), r * np.sin(phi)


def mantle_ray(delta_deg, n=200, turn_frac=None):
    """Smooth circular-arc ray from source at top (0, R_EARTH) to receiver
    at epicentral distance delta_deg measured leftward.

    Uses a circular-arc approximation (exact for linear V gradient).
    The arc is concave toward Earth's surface — physically correct per
    Snell's law when V increases with depth.
    """
    delta = np.deg2rad(delta_deg)
    if turn_frac is None:
        r_t = R_EARTH - 0.85 * (R_EARTH - R_CMB) * np.sin(delta / 2.0) ** 1.2
    else:
        r_t = R_EARTH - turn_frac * (R_EARTH - R_CMB)

    # Source and receiver in Cartesian (source at top)
    phi_src = np.pi / 2
    x0 = R_EARTH * np.cos(phi_src)   # = 0
    y0 = R_EARTH * np.sin(phi_src)   # = R_EARTH
    phi_rec = phi_src - delta
    x1 = R_EARTH * np.cos(phi_rec)
    y1 = R_EARTH * np.sin(phi_rec)

    # Bisector unit vector (symmetry axis of the arc)
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    mid_r = np.sqrt(mx**2 + my**2)
    ux, uy = mx / mid_r, my / mid_r

    # Circle centre on bisector
    dot_src = x0 * ux + y0 * uy      # = R_EARTH * cos(delta/2)
    denom = 2.0 * (r_t - dot_src)
    if abs(denom) < 1.0:
        phi_arr = np.linspace(phi_src, phi_rec, n)
        return R_EARTH * np.cos(phi_arr), R_EARTH * np.sin(phi_arr)
    d_c = (r_t**2 - R_EARTH**2) / denom
    cx, cy = d_c * ux, d_c * uy
    R_c = np.sqrt((x0 - cx)**2 + (y0 - cy)**2)

    # Arc parametrisation going through the turning point
    ang0 = np.arctan2(y0 - cy, x0 - cx)
    ang1 = np.arctan2(y1 - cy, x1 - cx)
    tx, ty = r_t * ux, r_t * uy
    ang_t = np.arctan2(ty - cy, tx - cx)

    def norm(a, ref):
        return (a - ref) % (2 * np.pi)

    a1 = norm(ang1, ang0)
    at = norm(ang_t, ang0)
    if at > a1:           # turning point not between ang0→ang1 CW, flip direction
        dang = a1 - 2 * np.pi
    else:
        dang = a1
    t_arr = np.linspace(0.0, dang, n)
    x = cx + R_c * np.cos(ang0 + t_arr)
    y = cy + R_c * np.sin(ang0 + t_arr)
    return x, y


from obspy.taup import TauPyModel as _TauPyModel

_MODEL = _TauPyModel(model="ak135")


def _taup_ray_xy(phase, delta_deg, depth_km=10):
    """Return (x, y) Cartesian arrays for a given phase and epicentral distance,
    using obspy.taup ray paths. Source is placed at the top (phi=pi/2)."""
    try:
        arrivals = _MODEL.get_ray_paths(
            source_depth_in_km=depth_km,
            distance_in_degree=delta_deg,
            phase_list=[phase],
        )
    except Exception:
        return None, None
    if not arrivals:
        return None, None
    path = arrivals[0].path
    # path has fields: p (ray param), time, dist (rad), depth (km)
    r = (R_EARTH - path["depth"])          # radius in km
    phi_cw = np.rad2deg(path["dist"])      # degrees CW from source
    xarr, yarr = _pt_arr(r, phi_cw)
    return xarr, yarr


def _pt_arr(r_arr, phi_cw_arr):
    """Vectorised _pt."""
    ang = np.pi/2 - np.deg2rad(phi_cw_arr)
    return r_arr * np.cos(ang), r_arr * np.sin(ang)


def _arc_between(x0, y0, x1, y1, r_t, n=120):
    """Circular arc from (x0,y0) to (x1,y1) whose closest approach to the
    origin equals r_t.  Concave toward the surface (correct for V increasing
    with depth).  Returns (x_arr, y_arr)."""
    mx, my = (x0 + x1) / 2.0, (y0 + y1) / 2.0
    mid_r = np.sqrt(mx**2 + my**2)
    if mid_r < 1.0:
        t = np.linspace(0, 1, n)
        return x0 + t*(x1-x0), y0 + t*(y1-y0)
    ux, uy = mx / mid_r, my / mid_r

    r0 = np.sqrt(x0**2 + y0**2)
    dot_src = x0*ux + y0*uy
    denom = 2.0*(r_t - dot_src)
    if abs(denom) < 0.5:
        t = np.linspace(0, 1, n)
        return x0 + t*(x1-x0), y0 + t*(y1-y0)
    d_c = (r_t**2 - r0**2) / denom
    cx, cy = d_c*ux, d_c*uy
    R_c = np.sqrt((x0-cx)**2 + (y0-cy)**2)

    ang0 = np.arctan2(y0-cy, x0-cx)
    ang1 = np.arctan2(y1-cy, x1-cx)
    tx, ty = r_t*ux, r_t*uy
    ang_t = np.arctan2(ty-cy, tx-cx)

    def norm(a, ref):
        return (a - ref) % (2*np.pi)

    a1 = norm(ang1, ang0)
    at = norm(ang_t, ang0)
    dang = a1 if at <= a1 else a1 - 2*np.pi
    t_arr = np.linspace(0.0, dang, n)
    return cx + R_c*np.cos(ang0+t_arr), cy + R_c*np.sin(ang0+t_arr)


def _pt(r, phi_cw):
    """Cartesian point at radius r, phi_cw degrees clockwise from the top."""
    ang = np.pi/2 - np.deg2rad(phi_cw)
    return r*np.cos(ang), r*np.sin(ang)


def core_refracted_ray(delta_deg, **_):
    """PKP ray path from obspy.taup AK135."""
    return _taup_ray_xy("PKP", delta_deg)


def pkikp_ray(delta_deg, **_):
    """PKIKP ray path from obspy.taup AK135."""
    return _taup_ray_xy("PKIKP", delta_deg)


def main(outpath):
    fig, (ax_s, ax_p) = plt.subplots(1, 2, figsize=(14, 8),
                                      facecolor="white")
    draw_layered_earth(ax_s)
    _plot_s_panel(ax_s)
    draw_layered_earth(ax_p)
    _plot_p_panel(ax_p)
    fig.suptitle("Shadow zones: the observational evidence "
                 "for Earth's fluid outer core and solid inner core",
                 y=0.99, color=COLORS[6], fontsize=15)
    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


def _plot_s_panel(ax_s):
    # Mantle S rays
    for delta in np.linspace(10, 100, 8):
        x, y = mantle_ray(delta)
        ax_s.plot(x, y, color=COLORS[1], lw=1.5, alpha=0.85)
    phi_src_deg = 90
    wedge = Wedge(center=(0, 0), r=R_EARTH * 1.06,
                  theta1=phi_src_deg + 103 - 360,
                  theta2=phi_src_deg - 103,
                  color="#D55E00", alpha=0.12, zorder=0)
    ax_s.add_patch(wedge)
    ax_s.plot(0, R_EARTH, marker="*", color=COLORS[4],
              markersize=18, markeredgecolor=COLORS[6], zorder=5)
    ax_s.annotate("earthquake", xy=(0, R_EARTH),
                  xytext=(0, R_EARTH + 900),
                  ha="center", fontsize=11, color=COLORS[6])
    ax_s.text(0, -R_EARTH * 0.35,
              "S-wave\nshadow zone\n$\\Delta > 103^\\circ$",
              ha="center", va="center", fontsize=13, color=COLORS[4],
              fontweight="bold")
    ax_s.text(R_EARTH * 0.05, R_ICB * 0.0,
              "liquid\nouter core\n(no S)",
              ha="left", va="center", fontsize=10, color=COLORS[6], style="italic")
    for side, sign in [("L", -1), ("R", +1)]:
        for d in np.arange(0, 181, 30):
            if d == 0:
                continue
            rad = np.deg2rad(90 + sign * d)
            x_t = R_EARTH * 1.03 * np.cos(rad)
            y_t = R_EARTH * 1.03 * np.sin(rad)
            x_l = R_EARTH * 1.11 * np.cos(rad)
            y_l = R_EARTH * 1.11 * np.sin(rad)
            ax_s.plot([R_EARTH * np.cos(rad), x_t],
                      [R_EARTH * np.sin(rad), y_t],
                      color=COLORS[6], lw=0.5)
            ax_s.text(x_l, y_l, f"{d}$^\\circ$",
                      fontsize=8, ha="center", va="center", color=COLORS[6])
    ax_s.set_xlim(-R_EARTH * 1.25, R_EARTH * 1.25)
    ax_s.set_ylim(-R_EARTH * 1.25, R_EARTH * 1.25)
    ax_s.set_aspect("equal")
    ax_s.axis("off")
    ax_s.set_title("(a) S-wave shadow zone: $\\Delta > 103^\\circ$",
                   color=COLORS[6])


def _plot_p_panel(ax_p):
    # Mantle P rays up to ~100 deg
    for delta in np.linspace(10, 100, 7):
        x, y = mantle_ray(delta)
        ax_p.plot(x, y, color=COLORS[0], lw=1.5, alpha=0.9)
    # PKP rays that refract through outer core, emerging at ~143-180 deg
    for delta in [145, 155, 165, 175]:
        x, y = core_refracted_ray(delta)
        if x is not None:
            ax_p.plot(x, y, color=COLORS[2], lw=1.5, alpha=0.95)
    # PKIKP: passes through inner core
    for delta in [155, 170]:
        x, y = pkikp_ray(delta)
        if x is not None:
            ax_p.plot(x, y, color=COLORS[3], lw=1.3, alpha=0.95,
                      linestyle=(0, (5, 2)))
    # P shadow wedge
    for side in (+1, -1):
        theta1 = 90 - side * 143
        theta2 = 90 - side * 103
        if theta1 > theta2:
            theta1, theta2 = theta2, theta1
        wedge = Wedge(center=(0, 0), r=R_EARTH * 1.06,
                      theta1=theta1, theta2=theta2,
                      color="#D55E00", alpha=0.16, zorder=0)
        ax_p.add_patch(wedge)
    ax_p.plot(0, R_EARTH, marker="*", color=COLORS[4],
              markersize=18, markeredgecolor=COLORS[6], zorder=5)
    ax_p.text(-R_EARTH * 0.95, -R_EARTH * 0.25,
              "P-wave\nshadow",
              ha="center", va="center", fontsize=11, color=COLORS[4],
              fontweight="bold")
    ax_p.text(R_EARTH * 0.95, -R_EARTH * 0.25,
              "P-wave\nshadow",
              ha="center", va="center", fontsize=11, color=COLORS[4],
              fontweight="bold")
    ax_p.text(-R_EARTH * 0.38, -R_EARTH * 0.92, "PKP",
              fontsize=11, color=COLORS[2], fontweight="bold")
    ax_p.text(R_EARTH * 0.28, -R_EARTH * 0.95, "PKIKP",
              fontsize=11, color=COLORS[3], fontweight="bold")
    ax_p.text(R_EARTH * 0.55, R_EARTH * 0.45, "P",
              fontsize=12, color=COLORS[0], fontweight="bold")
    for side, sign in [("L", -1), ("R", +1)]:
        for d in np.arange(0, 181, 30):
            if d == 0:
                continue
            rad = np.deg2rad(90 + sign * d)
            x_t = R_EARTH * 1.03 * np.cos(rad)
            y_t = R_EARTH * 1.03 * np.sin(rad)
            x_l = R_EARTH * 1.11 * np.cos(rad)
            y_l = R_EARTH * 1.11 * np.sin(rad)
            ax_p.plot([R_EARTH * np.cos(rad), x_t],
                      [R_EARTH * np.sin(rad), y_t],
                      color=COLORS[6], lw=0.5)
            ax_p.text(x_l, y_l, f"{d}$^\\circ$",
                      fontsize=8, ha="center", va="center", color=COLORS[6])
    ax_p.set_xlim(-R_EARTH * 1.25, R_EARTH * 1.25)
    ax_p.set_ylim(-R_EARTH * 1.25, R_EARTH * 1.25)
    ax_p.set_aspect("equal")
    ax_p.axis("off")
    ax_p.set_title("(b) P-wave shadow zone: $103^\\circ < \\Delta < 143^\\circ$",
                   color=COLORS[6])


if __name__ == "__main__":
    main("assets/figures/fig_11_shadow_zones.png")
