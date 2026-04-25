"""
fig_shadow_zones.py

Scientific content
------------------
Schematic Earth cross-sections illustrating why the P-wave and S-wave shadow
zones both begin at an epicentral distance of approximately 103 degrees, yet
have very different angular widths. The S-wave shadow extends from 103 degrees
to the antipode because the fluid outer core has zero shear modulus
(mu = 0 -> beta = 0) and cannot transmit shear waves. The P-wave shadow
spans 103 degrees to roughly 143 degrees because P energy refracts sharply
into the outer core (the K leg) and re-emerges as PKP at distances at or
beyond the PKP caustic near 143 degrees.

The figure is schematic. Mantle-turning rays are drawn as quadratic Bezier
curves connecting source, turning point, and emergence point. PKP rays are
drawn as three-segment paths (straight mantle legs plus a Bezier core leg
that bulges toward the core-mantle boundary). Emergence distances are
prescribed; a fully ray-traced figure would use a 1D radial Earth model
such as PREM or IASP91.

Reproduces the scientific content of (without copying):
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.
    Cambridge University Press, figures of Earth structure and shadow zones
    (Ch. 4, seismology).
  Stein, S. & Wysession, M. (2003). An Introduction to Seismology, Earthquakes,
    and Earth Structure. Blackwell.
  Shearer, P. M. (2009). Introduction to Seismology, 2nd ed. Cambridge.

ESS 314 module: Whole Earth & Tomography (Lectures 10 - 11)
Learning objectives addressed: LO-1, LO-2, LO-4
Output: assets/figures/fig_shadow_zones.png
License: CC-BY 4.0 (this script and its output)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Circle

# -- Global rcParams (mandatory at top of every ESS 314 figure script) -------
mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# -- WCAG AA colorblind-safe palette -----------------------------------------
P_COLOR        = "#0072B2"   # blue: P-wave segments
S_COLOR        = "#E69F00"   # orange: S-wave segments
SHADOW_COLOR   = "#D55E00"   # vermilion: shadow-zone shading and X markers
TEXT_COLOR     = "#000000"
ANNOT_GRAY     = "#444444"

MANTLE_FILL      = "#F4F0E8"
OUTER_CORE_FILL  = "#E8DCC0"
INNER_CORE_FILL  = "#D6C089"

# -- Earth structure (radii normalized to R_Earth = 1) -----------------------
R_EARTH = 1.0
R_CMB   = 3480.0 / 6371.0   # ~0.546 (core-mantle boundary)
R_IC    = 1220.0 / 6371.0   # ~0.191 (inner core boundary)


# ---------------------------------------------------------------------------
# Ray-path constructions
# ---------------------------------------------------------------------------

def mantle_ray(emergence_deg, turning_depth_frac, n=200):
    """Quadratic Bezier ray from the source at the top of the Earth."""
    delta = np.radians(emergence_deg)
    p0 = np.array([0.0, 1.0])
    p2 = np.array([np.sin(delta), np.cos(delta)])
    turning = (1.0 - turning_depth_frac) * np.array(
        [np.sin(delta / 2.0), np.cos(delta / 2.0)]
    )
    p1 = 2.0 * turning - 0.5 * (p0 + p2)
    t = np.linspace(0.0, 1.0, n)[:, None]
    return (1.0 - t) ** 2 * p0 + 2.0 * (1.0 - t) * t * p1 + t ** 2 * p2


def schematic_pkp(emergence_deg, cmb_offset_deg=42.0, core_bulge=1.0, n=240):
    """Three-segment schematic PKP ray emerging at the prescribed distance.

    1. Mantle leg in:  straight line from source (0, 1) to the CMB at
       angular distance cmb_offset_deg from the source.
    2. Core leg:  quadratic Bezier from CMB_in to CMB_out with a control
       point pulled toward the CMB at the midpoint angular position by
       core_bulge in [0, 1].
    3. Mantle leg out: straight line from CMB_out to the surface emergence
       point at angular distance emergence_deg.
    """
    a_in     = np.radians(cmb_offset_deg)
    a_out    = np.radians(emergence_deg - cmb_offset_deg)
    a_emerge = np.radians(emergence_deg)

    src     = np.array([0.0, 1.0])
    cmb_in  = R_CMB * np.array([np.sin(a_in),  np.cos(a_in)])
    cmb_out = R_CMB * np.array([np.sin(a_out), np.cos(a_out)])
    surf    = np.array([np.sin(a_emerge),       np.cos(a_emerge)])

    seg1 = np.linspace(src, cmb_in, n // 4)

    a_mid = 0.5 * (a_in + a_out)
    cmb_mid = R_CMB * np.array([np.sin(a_mid), np.cos(a_mid)])
    chord_mid = 0.5 * (cmb_in + cmb_out)
    p1_core = (1.0 - core_bulge) * chord_mid + core_bulge * cmb_mid
    t = np.linspace(0.0, 1.0, n // 2)[:, None]
    seg2 = (1.0 - t) ** 2 * cmb_in + 2.0 * (1.0 - t) * t * p1_core + t ** 2 * cmb_out

    seg3 = np.linspace(cmb_out, surf, n // 4)

    return np.vstack([seg1, seg2, seg3])


# ---------------------------------------------------------------------------
# Drawing primitives
# ---------------------------------------------------------------------------

def draw_earth(ax):
    ax.add_patch(Circle((0, 0), R_EARTH,
                        facecolor=MANTLE_FILL, edgecolor=TEXT_COLOR,
                        lw=1.4, zorder=1))
    ax.add_patch(Circle((0, 0), R_CMB,
                        facecolor=OUTER_CORE_FILL, edgecolor=TEXT_COLOR,
                        lw=1.1, zorder=2))
    ax.add_patch(Circle((0, 0), R_IC,
                        facecolor=INNER_CORE_FILL, edgecolor=TEXT_COLOR,
                        lw=1.1, zorder=3))

    ax.plot([0], [1.0], marker="*", markersize=22,
            color=SHADOW_COLOR, markeredgecolor="black",
            markeredgewidth=1.0, zorder=10)

    ax.text(0.0, 0.78, "Mantle\n(solid)", ha="center", va="center",
            fontsize=11, style="italic", color=ANNOT_GRAY, zorder=5)
    ax.text(0.0, 0.39, "Outer core\n(fluid, $\\mu = 0$)",
            ha="center", va="center",
            fontsize=11, style="italic", color=ANNOT_GRAY, zorder=5)
    ax.text(0.0, 0.0, "Inner\ncore", ha="center", va="center",
            fontsize=10, style="italic", color=ANNOT_GRAY, zorder=5)


def draw_shadow_arc(ax, start_deg, end_deg, color=SHADOW_COLOR, alpha=0.22):
    theta = np.linspace(np.radians(start_deg), np.radians(end_deg), 120)
    r_outer, r_inner = 1.16, 1.005
    for sign in (+1, -1):
        x_out = sign * r_outer * np.sin(theta)
        y_out = r_outer * np.cos(theta)
        x_in  = sign * r_inner * np.sin(theta[::-1])
        y_in  = r_inner * np.cos(theta[::-1])
        xs = np.concatenate([x_out, x_in])
        ys = np.concatenate([y_out, y_in])
        ax.fill(xs, ys, facecolor=color, alpha=alpha,
                edgecolor=color, lw=1.3, zorder=4)


def annotate_distance(ax, deg, label=None, label_radius=1.30):
    label = label if label is not None else f"{deg}\u00B0"
    for sign in (+1, -1):
        x_tick_inner = sign * 1.005 * np.sin(np.radians(deg))
        y_tick_inner = 1.005 * np.cos(np.radians(deg))
        x_tick_outer = sign * 1.06 * np.sin(np.radians(deg))
        y_tick_outer = 1.06 * np.cos(np.radians(deg))
        ax.plot([x_tick_inner, x_tick_outer],
                [y_tick_inner, y_tick_outer],
                color=ANNOT_GRAY, lw=1.3, zorder=7)
        x_lbl = sign * label_radius * np.sin(np.radians(deg))
        y_lbl = label_radius * np.cos(np.radians(deg))
        ax.text(x_lbl, y_lbl, label, fontsize=11, color=TEXT_COLOR,
                ha="center", va="center", zorder=8,
                bbox=dict(boxstyle="round,pad=0.20",
                          facecolor="white", edgecolor="none",
                          alpha=0.92))


# ---------------------------------------------------------------------------
# Panel constructions
# ---------------------------------------------------------------------------

MANTLE_RAY_SET = [
    (25.0,  0.10),
    (55.0,  0.20),
    (85.0,  0.32),
    (103.0, 0.44),
]


def panel_s_shadow(ax):
    draw_earth(ax)

    for d, depth in MANTLE_RAY_SET:
        path = mantle_ray(d, depth)
        ax.plot(path[:, 0], path[:, 1], color=S_COLOR, lw=2.2, zorder=6)
        ax.plot(-path[:, 0], path[:, 1], color=S_COLOR, lw=2.2, zorder=6)

    blocked_takeoffs = [12.0, 25.0]
    cmb_pts = []
    for to in blocked_takeoffs:
        theta = np.radians(to)
        disc = R_CMB ** 2 - np.sin(theta) ** 2
        t_hit = np.cos(theta) - np.sqrt(disc)
        cmb_pt = np.array([t_hit * np.sin(theta), 1.0 - t_hit * np.cos(theta)])
        cmb_pts.append(cmb_pt)
        for sign in (+1, -1):
            xs = np.linspace(0.0, sign * cmb_pt[0], 50)
            ys = np.linspace(1.0, cmb_pt[1], 50)
            ax.plot(xs, ys, color=S_COLOR, lw=2.0, ls="--",
                    alpha=0.85, zorder=6)
            ax.plot(sign * cmb_pt[0], cmb_pt[1], marker="x",
                    color=SHADOW_COLOR, markersize=12, mew=2.6, zorder=9)

    # Annotation off to the right side
    ax.annotate(
        "S cannot enter\nfluid outer core\n($\\mu = 0$)",
        xy=(cmb_pts[1][0], cmb_pts[1][1]),
        xytext=(1.18, 0.55),
        ha="left", va="center", fontsize=10.5, color=SHADOW_COLOR,
        arrowprops=dict(arrowstyle="->", color=SHADOW_COLOR, lw=1.0,
                        connectionstyle="arc3,rad=-0.25"),
        bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                  edgecolor=SHADOW_COLOR, lw=0.8, alpha=0.92),
        zorder=10)

    draw_shadow_arc(ax, 103.0, 180.0)

    annotate_distance(ax, 103, label="103\u00B0")
    annotate_distance(ax, 180, label="180\u00B0\n(antipode)", label_radius=1.22)

    ax.text(0.0, 1.13, "Source", ha="center", va="bottom",
            fontsize=11, color=TEXT_COLOR)

    ax.set_title(
        "(a)  S-wave shadow:  no direct S beyond 103\u00B0\n"
        "Outer core is fluid \u2192 cannot transmit shear waves",
        fontsize=14, pad=12)

    ax.text(0.0, -1.50,
            "S-wave shadow zone:  103\u00B0 \u2192 antipode (180\u00B0)",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=SHADOW_COLOR)

    ax.set_xlim(-1.75, 1.85)
    ax.set_ylim(-1.65, 1.50)
    ax.set_aspect("equal")
    ax.axis("off")


def panel_p_shadow(ax):
    draw_earth(ax)

    for d, depth in MANTLE_RAY_SET:
        path = mantle_ray(d, depth)
        ax.plot(path[:, 0], path[:, 1], color=P_COLOR, lw=2.2, zorder=6)
        ax.plot(-path[:, 0], path[:, 1], color=P_COLOR, lw=2.2, zorder=6)

    pkp_emergences = [148.0, 162.0, 175.0]
    pkp_offsets    = [36.0,  44.0,  52.0]
    for i, (em, off) in enumerate(zip(pkp_emergences, pkp_offsets)):
        path = schematic_pkp(em, cmb_offset_deg=off, core_bulge=1.0)
        ax.plot(path[:, 0], path[:, 1], color=P_COLOR, lw=2.0,
                alpha=0.95, zorder=6)
        ax.plot(-path[:, 0], path[:, 1], color=P_COLOR, lw=2.0,
                alpha=0.95, zorder=6)
        if i == 1:  # label the middle PKP ray
            mid = path[len(path) // 2]
            ax.text(mid[0] + 0.13, mid[1] + 0.05, "PKP",
                    fontsize=12, color=P_COLOR, fontweight="bold", zorder=11,
                    bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                              edgecolor="none", alpha=0.85))

    draw_shadow_arc(ax, 103.0, 143.0)

    annotate_distance(ax, 103, label="103\u00B0")
    annotate_distance(ax, 143, label="143\u00B0\n(PKP caustic)", label_radius=1.24)

    ax.text(0.0, 1.13, "Source", ha="center", va="bottom",
            fontsize=11, color=TEXT_COLOR)

    # Pick a CMB-entry point on one of the PKP rays for annotation arrow target
    target_pkp = schematic_pkp(162.0, cmb_offset_deg=44.0, core_bulge=1.0)
    target_pt = target_pkp[len(target_pkp) // 4]  # roughly at the CMB-in junction

    ax.annotate(
        "Snell's law:\n"
        "$\\dfrac{\\sin i}{\\alpha_m} = \\dfrac{\\sin r}{\\alpha_c}$\n"
        "$\\alpha_m \\!\\approx\\! 13.7$ km/s\n"
        "$\\alpha_c \\!\\approx\\! 8$ km/s\n"
        "ray bends toward normal",
        xy=(target_pt[0], target_pt[1]),
        xytext=(1.18, 0.55),
        ha="left", va="center", fontsize=10, color=ANNOT_GRAY,
        arrowprops=dict(arrowstyle="->", color=ANNOT_GRAY, lw=1.0,
                        connectionstyle="arc3,rad=-0.25"),
        bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                  edgecolor=ANNOT_GRAY, lw=0.8, alpha=0.92),
        zorder=10)

    ax.set_title(
        "(b)  P-wave shadow:  no direct P from 103\u00B0 to 143\u00B0\n"
        "P refracts into outer core (K leg) \u2192 emerges as PKP at \u2265143\u00B0",
        fontsize=14, pad=12)

    ax.text(0.0, -1.50,
            "P-wave shadow zone:  103\u00B0 \u2192 143\u00B0   "
            "(PKP fills in beyond 143\u00B0)",
            ha="center", va="center", fontsize=12, fontweight="bold",
            color=SHADOW_COLOR)

    ax.set_xlim(-1.75, 1.85)
    ax.set_ylim(-1.65, 1.50)
    ax.set_aspect("equal")
    ax.axis("off")


def main():
    fig, axes = plt.subplots(1, 2, figsize=(16, 8.5))
    panel_s_shadow(axes[0])
    panel_p_shadow(axes[1])

    fig.tight_layout(rect=[0, 0.07, 1, 1])

    fig.text(
        0.5, 0.025,
        "Both shadow zones begin at the same angular distance because the "
        "103\u00B0 threshold is a geometric property of the core-mantle "
        "boundary: it is the\nepicentral distance at which a direct mantle "
        "ray just grazes the CMB.  Beyond 103\u00B0, any direct ray must "
        "penetrate the core.  S energy cannot\npropagate as a shear wave in "
        "the fluid outer core, so the S shadow extends to the antipode.  "
        "P energy refracts into the core and re-emerges as PKP\nat distances "
        "at or beyond the PKP caustic near 143\u00B0, leaving a 40\u00B0 "
        "gap.  Rays drawn here are schematic; emergence angles depend on "
        "the\nfull radial velocity model (e.g. PREM, IASP91).",
        ha="center", va="bottom", fontsize=10.5, style="italic",
        color=TEXT_COLOR, wrap=True)

    out_path = "assets/figures/fig_shadow_zones.png"
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
