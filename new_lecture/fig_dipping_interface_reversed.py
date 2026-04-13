"""
fig_dipping_interface_reversed.py

Scientific content:
    Reversed refraction profiles over (a) a horizontal interface and
    (b) a dipping interface. Demonstrates that dip causes forward and
    reverse T-x head-wave segments to have different slopes (apparent
    velocities alpha_d and alpha_u). First arrivals are shown as solid
    lines; individual branches as dashed. Ray paths for both forward
    and reverse shots are drawn on the cross-sections. The reciprocal
    time is identical for both shot directions (consistency check).

Reproduces the scientific content of:
    Sheriff, R.E. & Geldart, L.P. (1995). Exploration Seismology,
    2nd ed. Cambridge University Press. Figure 4.15 (concept).
    Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics,
    3rd ed. Cambridge University Press. Figure 6.33 (concept).
    (No direct reproduction — original Python generation.)

Output: assets/figures/fig_dipping_interface_reversed.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, FancyArrowPatch

# ── Global rcParams (MANDATORY) ──────────────────────────────────────
mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# Colorblind-safe palette (WCAG AA)
C_LAYER1  = "#56B4E9"   # overburden fill
C_LAYER2  = "#D55E00"   # refractor fill (lighter)
C_FWD     = "#0072B2"   # forward shot / down-dip
C_REV     = "#E69F00"   # reverse shot / up-dip
C_DIRECT  = "#000000"   # direct wave
C_FIRST   = "#009E73"   # first-arrival envelope
C_RECIP   = "#CC79A7"   # reciprocal time
C_IFACE   = "#444444"   # interface line

# ── Model parameters ─────────────────────────────────────────────────
V1, V2   = 500.0, 1500.0   # m/s
h0_flat  = 20.0            # vertical depth (flat model)
dip_deg  = 6.0            # exaggerated so dip is clearly visible
delta    = np.radians(dip_deg)
L        = 120.0           # profile length (m)
x        = np.linspace(0.0, L, 3000)

tic      = np.arcsin(V1 / V2)    # critical angle (rad)

# ── Flat-interface travel times ───────────────────────────────────────
ti_flat      = 2 * h0_flat * np.cos(tic) / V1 * 1e3          # ms
t_dir        = x / V1 * 1e3
t_fwd_flat   = x / V2 * 1e3 + ti_flat                        # fwd = rev for flat
t_rev_flat   = (L - x) / V2 * 1e3 + ti_flat                  # rev source at x=L
t_recip_flat = L / V2 * 1e3 + ti_flat

# First arrivals (flat)
fa_fwd_flat = np.minimum(t_dir, t_fwd_flat)
fa_rev_flat = np.minimum((L - x) / V1 * 1e3, t_rev_flat)

# ── Dipping-interface travel times ────────────────────────────────────
# Perpendicular depth at forward source (x=0) and reverse source (x=L)
d_A = h0_flat                               # perp depth at fwd source
d_B = d_A + L * np.sin(delta)              # perp depth at rev source

slope_d = np.sin(tic + delta) / V1         # s/m down-dip
slope_u = np.sin(tic - delta) / V1         # s/m up-dip
ti_d    = 2 * d_A * np.cos(tic) / V1 * 1e3  # ms
ti_u    = 2 * d_B * np.cos(tic) / V1 * 1e3  # ms

# Forward shot (source at x=0, geophones at x): down-dip propagation
t_fwd_dip = slope_d * x * 1e3 + ti_d

# Reverse shot (source at x=L, geophones at x): offset from rev src = L - x
t_rev_dip = slope_u * (L - x) * 1e3 + ti_u

# Reciprocal time (both shots, full profile length)
t_recip_dip = slope_d * L * 1e3 + ti_d   # == slope_u * L * 1e3 + ti_u (by Snell)

# First arrivals (dipping)
fa_fwd_dip = np.minimum(t_dir, t_fwd_dip)
fa_rev_dip = np.minimum((L - x) / V1 * 1e3, t_rev_dip)

# Apparent velocities
alpha_d = 1.0 / slope_d   # m/s
alpha_u = 1.0 / slope_u   # m/s

# ── Dipping-interface vertical depth profile ──────────────────────────
# Vertical depth at position x along profile:
# z(x) = d_A / cos(delta) + x * tan(delta)
# (perpendicular depth d_A at x=0 converted to vertical)
def vert_depth(x_pos):
    return d_A / np.cos(delta) + x_pos * np.tan(delta)

x_cs  = np.array([0.0, L])
z_cs  = vert_depth(x_cs)

# ── Ray path helper functions ─────────────────────────────────────────
def head_wave_ray(direction="fwd"):
    """
    Compute the four-point head-wave (critically refracted) ray path:
      source → (down-going leg) → interface entry point →
      (horizontal propagation along interface) →
      interface exit point → (up-going leg) → surface receiver

    The path has the characteristic Z-shape / trapezoid geometry that
    distinguishes a head wave from a reflected wave.

    Returns (x_points, z_points) as lists of 4 coordinates.
    """
    if direction == "fwd":
        # Forward shot: source at x=0, head wave propagates rightward
        # Down-going at angle (tic + delta) from vertical
        theta_d = tic + delta
        theta_u = tic - delta
        # Interface entry: z_ray = x * tan(theta_d) = vert_depth(x)
        x_entry = (d_A / np.cos(delta)) / (np.tan(theta_d) - np.tan(delta))
        z_entry = vert_depth(x_entry)
        # Interface exit: receiver at x_recv = 0.79*L
        # x_recv = x_exit + z_exit * tan(theta_u)
        # x_recv = x_exit*(1 + tan(delta)*tan(theta_u)) + (d_A/cos(delta))*tan(theta_u)
        x_recv = 0.79 * L
        c = 1.0 + np.tan(delta) * np.tan(theta_u)
        x_exit = (x_recv - (d_A / np.cos(delta)) * np.tan(theta_u)) / c
        z_exit = vert_depth(x_exit)
        return ([0.0,     x_entry, x_exit, x_recv],
                [0.0,     z_entry, z_exit, 0.0   ])
    else:
        # Reverse shot: source at x=L, head wave propagates leftward
        # Down-going at angle (tic - delta) from vertical (shallower, up-dip)
        theta_d = tic - delta
        theta_u = tic + delta
        # Interface entry: ray from x=L going left
        # (L - x)*tan(theta_d) = vert_depth(x)
        x_entry = (L * np.tan(theta_d) - d_A / np.cos(delta)) /                   (np.tan(theta_d) + np.tan(delta))
        z_entry = vert_depth(x_entry)
        # Interface exit: head wave travels leftward to x_exit = x_entry - 13
        # chosen so up-going leg reaches the surface within the profile
        x_exit = x_entry - 13.0
        x_exit = max(x_exit, 3.0)
        z_exit = vert_depth(x_exit)
        # Receiver: up-going ray travels leftward at angle theta_u
        x_recv = x_exit - z_exit * np.tan(theta_u)
        x_recv = max(x_recv, 0.0)
        return ([L,       x_entry, x_exit, x_recv],
                [0.0,     z_entry, z_exit, 0.0   ])


# ── Figure layout ─────────────────────────────────────────────────────
# 3 rows × 2 cols:  row0 = cross-sections, row1 = individual T-x, row2 = combined
fig = plt.figure(figsize=(13, 11))
gs  = fig.add_gridspec(3, 2, hspace=0.72, wspace=0.38,
                       height_ratios=[1.1, 1.0, 1.4])

ax_cs_flat = fig.add_subplot(gs[0, 0])
ax_cs_dip  = fig.add_subplot(gs[0, 1])
ax_tx_flat = fig.add_subplot(gs[1, 0])
ax_tx_dip  = fig.add_subplot(gs[1, 1])
ax_big     = fig.add_subplot(gs[2, :])


# ═══════════════════════════════════════════════════════════════════════
# CROSS-SECTION: FLAT INTERFACE
# ═══════════════════════════════════════════════════════════════════════
depth_cs_flat = h0_flat + 12
ax_cs_flat.set_xlim(-5, L + 5)
ax_cs_flat.set_ylim(depth_cs_flat, -6)

ax_cs_flat.axhspan(0, h0_flat,          facecolor=C_LAYER1, alpha=0.30, zorder=1)
ax_cs_flat.axhspan(h0_flat, depth_cs_flat, facecolor=C_LAYER2, alpha=0.25, zorder=1)
ax_cs_flat.axhline(h0_flat, color=C_IFACE, lw=1.8, zorder=2)

ax_cs_flat.text(L * 0.5, h0_flat * 0.45, f"$V_1 = {int(V1)}$ m/s",
                ha="center", va="center", fontsize=11)
ax_cs_flat.text(L * 0.5, h0_flat + 6, f"$V_2 = {int(V2)}$ m/s",
                ha="center", va="center", fontsize=11)
ax_cs_flat.text(L * 0.5, -4.5, f"$h = {int(h0_flat)}$ m",
                ha="center", fontsize=10, color="#555")

# Source symbols: forward (left) and reverse (right), colored
for xp, col, lab, ha_ in [(0, C_FWD, "Fwd\nsource", "right"),
                           (L, C_REV, "Rev\nsource", "left")]:
    # Hammer-style: triangle marker + label
    ax_cs_flat.plot(xp, 0, "v", ms=11, color=col, zorder=6,
                    markeredgecolor="white", markeredgewidth=0.8)
    ax_cs_flat.text(xp + (-3 if ha_ == "right" else 3), -4.8, lab,
                    ha=ha_, fontsize=9, color=col, fontweight="bold")

# Geophone symbols along surface
x_geo_flat = np.linspace(10, L-10, 10)
ax_cs_flat.plot(x_geo_flat, np.zeros_like(x_geo_flat),
                "s", ms=5, color="#333", zorder=5, markeredgecolor="white")

# Forward ray path (blue)
ray_down = h0_flat * np.tan(tic)
xA_fwd = 2 + ray_down
ax_cs_flat.plot([2, xA_fwd, L - ray_down - 2, L - 2],
                [0, h0_flat, h0_flat, 0],
                color=C_FWD, lw=1.6, zorder=4, label="Forward ray")
# Arrow on down-going leg
ax_cs_flat.annotate("", xy=(xA_fwd * 0.6, h0_flat * 0.6),
                    xytext=(xA_fwd * 0.35, h0_flat * 0.35),
                    arrowprops=dict(arrowstyle="->", color=C_FWD, lw=1.3))

# Reverse ray path (orange) — symmetric for flat case
xA_rev = L - 2 - ray_down
ax_cs_flat.plot([L - 2, xA_rev, ray_down + 2, 2],
                [0, h0_flat, h0_flat, 0],
                color=C_REV, lw=1.6, ls="--", zorder=4, label="Reverse ray")
ax_cs_flat.annotate("", xy=(L - xA_fwd * 0.6, h0_flat * 0.6),
                    xytext=(L - xA_fwd * 0.35, h0_flat * 0.35),
                    arrowprops=dict(arrowstyle="->", color=C_REV, lw=1.3))

ax_cs_flat.set_ylabel("Depth (m)")
ax_cs_flat.set_title("(a) Horizontal interface — symmetric rays",
                     fontweight="bold", fontsize=11)
leg_flat_cs = ax_cs_flat.legend(loc="lower right", fontsize=9,
                                 framealpha=0.85, handlelength=1.5)


# ═══════════════════════════════════════════════════════════════════════
# CROSS-SECTION: DIPPING INTERFACE
# ═══════════════════════════════════════════════════════════════════════
depth_cs_dip = vert_depth(L) + 16
ax_cs_dip.set_xlim(-5, L + 5)
ax_cs_dip.set_ylim(depth_cs_dip, -6)

x_fill = np.array([0, L, L, 0])
z_fill_iface = vert_depth(np.array([0, L]))
ax_cs_dip.fill_between([0, L], [0, 0], z_fill_iface,
                       facecolor=C_LAYER1, alpha=0.30, zorder=1)
ax_cs_dip.fill_between([0, L], z_fill_iface, depth_cs_dip,
                       facecolor=C_LAYER2, alpha=0.25, zorder=1)
ax_cs_dip.plot([0, L], z_fill_iface, color=C_IFACE, lw=2.0, zorder=2)

ax_cs_dip.text(L * 0.22, vert_depth(L * 0.22) * 0.45,
               f"$V_1 = {int(V1)}$ m/s", ha="center", va="center", fontsize=11)
ax_cs_dip.text(L * 0.5, vert_depth(L * 0.5) + 6,
               f"$V_2 = {int(V2)}$ m/s", ha="center", va="center", fontsize=11)

# Dip angle arc annotation (at the right end of the interface)
x_arc = L * 0.68
z_arc = vert_depth(x_arc)
arc_radius = 8
arc = Arc((x_arc, z_arc), 2 * arc_radius, 2 * arc_radius,
          angle=0, theta1=180, theta2=180 + dip_deg,
          color="#333", lw=1.5, zorder=5)
ax_cs_dip.add_patch(arc)
ax_cs_dip.text(x_arc - arc_radius - 3, z_arc + 2.5,
               f"$\\delta={dip_deg:.0f}°$", fontsize=11, color="#333",
               ha="right", va="bottom")
# Horizontal reference line at the arc point
ax_cs_dip.plot([x_arc - arc_radius - 2, x_arc + 2], [z_arc, z_arc],
               color="#999", lw=0.8, ls=":", zorder=3)

# Source symbols
for xp, col, lab, ha_ in [(0, C_FWD, "Fwd\nsource", "right"),
                           (L, C_REV, "Rev\nsource", "left")]:
    ax_cs_dip.plot(xp, 0, "v", ms=11, color=col, zorder=6,
                   markeredgecolor="white", markeredgewidth=0.8)
    ax_cs_dip.text(xp + (-3 if ha_ == "right" else 3), -4.8, lab,
                   ha=ha_, fontsize=9, color=col, fontweight="bold")

# Geophone symbols
ax_cs_dip.plot(x_geo_flat, np.zeros_like(x_geo_flat),
               "s", ms=5, color="#333", zorder=5, markeredgecolor="white")

# ── Forward head-wave ray path (Z-shape: down → along interface → up) ──
rx_fwd, rz_fwd = head_wave_ray(direction="fwd")
ax_cs_dip.plot(rx_fwd, rz_fwd, color=C_FWD, lw=2.2, zorder=4,
               label="Forward ray (down-dip)")
# Arrow on down-going leg (segment 0→1)
mid_x0 = (rx_fwd[0] + rx_fwd[1]) / 2
mid_z0 = (rz_fwd[0] + rz_fwd[1]) / 2
ax_cs_dip.annotate("", xy=(mid_x0 + 2, mid_z0 + 2),
                    xytext=(mid_x0 - 2, mid_z0 - 2),
                    arrowprops=dict(arrowstyle="->", color=C_FWD, lw=1.4))
# Arrow along interface segment (1→2)
mid_x1 = (rx_fwd[1] + rx_fwd[2]) / 2
mid_z1 = (rz_fwd[1] + rz_fwd[2]) / 2
ax_cs_dip.annotate("", xy=(mid_x1 + 3, mid_z1 + 0.5),
                    xytext=(mid_x1 - 3, mid_z1 - 0.5),
                    arrowprops=dict(arrowstyle="->", color=C_FWD, lw=1.4))
# Arrow on up-going leg (segment 2→3)
mid_x2 = (rx_fwd[2] + rx_fwd[3]) / 2
mid_z2 = (rz_fwd[2] + rz_fwd[3]) / 2
ax_cs_dip.annotate("", xy=(mid_x2 + 2, mid_z2 - 2),
                    xytext=(mid_x2 - 2, mid_z2 + 2),
                    arrowprops=dict(arrowstyle="->", color=C_FWD, lw=1.4))

# ── Reverse head-wave ray path (Z-shape: down ← along interface ← up) ─
rx_rev, rz_rev = head_wave_ray(direction="rev")
ax_cs_dip.plot(rx_rev, rz_rev, color=C_REV, lw=2.2, ls="--", zorder=4,
               label="Reverse ray (up-dip)")
# Arrow on down-going leg (L → entry)
mid_xr0 = (rx_rev[0] + rx_rev[1]) / 2
mid_zr0 = (rz_rev[0] + rz_rev[1]) / 2
ax_cs_dip.annotate("", xy=(mid_xr0 - 2, mid_zr0 + 2),
                    xytext=(mid_xr0 + 2, mid_zr0 - 2),
                    arrowprops=dict(arrowstyle="->", color=C_REV, lw=1.4))
# Arrow along interface (entry → exit, leftward)
mid_xr1 = (rx_rev[1] + rx_rev[2]) / 2
mid_zr1 = (rz_rev[1] + rz_rev[2]) / 2
ax_cs_dip.annotate("", xy=(mid_xr1 - 3, mid_zr1 - 0.4),
                    xytext=(mid_xr1 + 3, mid_zr1 + 0.4),
                    arrowprops=dict(arrowstyle="->", color=C_REV, lw=1.4))
# Arrow on up-going leg (exit → receiver)
mid_xr2 = (rx_rev[2] + rx_rev[3]) / 2
mid_zr2 = (rz_rev[2] + rz_rev[3]) / 2
ax_cs_dip.annotate("", xy=(mid_xr2 - 2, mid_zr2 - 2),
                    xytext=(mid_xr2 + 2, mid_zr2 + 2),
                    arrowprops=dict(arrowstyle="->", color=C_REV, lw=1.4))

ax_cs_dip.set_title("(b) Dipping interface — asymmetric ray paths",
                     fontweight="bold", fontsize=11)
leg_dip_cs = ax_cs_dip.legend(loc="lower right", fontsize=9,
                               framealpha=0.85, handlelength=1.5)


# ═══════════════════════════════════════════════════════════════════════
# T-x PANEL: FLAT (forward shot only — symmetric, so one shot suffices)
# ═══════════════════════════════════════════════════════════════════════
# First arrivals: solid; individual branches: dashed

ax_tx_flat.plot(x, t_dir, color=C_DIRECT, lw=1.2, ls="--", alpha=0.7, label="Direct ($1/V_1$)")
ax_tx_flat.plot(x, t_fwd_flat, color=C_FWD, lw=1.2, ls="--", alpha=0.7,
                label=f"Head wave (fwd, $1/V_2$)")
ax_tx_flat.plot(L - x, t_rev_flat, color=C_REV, lw=1.2, ls="--", alpha=0.7,
                label=f"Head wave (rev)")
ax_tx_flat.axhline(t_recip_flat, color=C_RECIP, lw=1.0, ls=":",
                   alpha=0.8, label=f"$t_R$ = {t_recip_flat:.0f} ms")
# First arrivals solid
ax_tx_flat.plot(x, fa_fwd_flat, color=C_FWD, lw=2.5, ls="-", zorder=5,
                label="First arrivals (fwd)")
ax_tx_flat.plot(L - x, fa_rev_flat, color=C_REV, lw=2.5, ls="-", zorder=5,
                label="First arrivals (rev)")

# Source markers on T-x panel
ax_tx_flat.plot(0, 0, "v", ms=9, color=C_FWD, zorder=7, markeredgecolor="white")
ax_tx_flat.plot(L, 0, "v", ms=9, color=C_REV, zorder=7, markeredgecolor="white")

ax_tx_flat.set_xlim(0, L)
ax_tx_flat.set_ylim(0, np.max(t_dir) * 1.08)
ax_tx_flat.set_xlabel("Position $x$ (m)")
ax_tx_flat.set_ylabel("$t$ (ms)")
ax_tx_flat.set_title("(c) $T$-$x$: flat — fwd = rev (symmetric)",
                     fontweight="bold", fontsize=11)
# Legend: bottom right to avoid covering curves in upper-left
ax_tx_flat.legend(loc="lower right", fontsize=8.5, framealpha=0.88,
                  ncol=2, handlelength=1.4)


# ═══════════════════════════════════════════════════════════════════════
# T-x PANEL: DIPPING
# ═══════════════════════════════════════════════════════════════════════
ax_tx_dip.plot(x, t_dir, color=C_DIRECT, lw=1.2, ls="--", alpha=0.7,
               label="Direct ($1/V_1$)")
ax_tx_dip.plot(x, t_fwd_dip, color=C_FWD, lw=1.2, ls="--", alpha=0.7,
               label=f"Head wave (fwd, $\\alpha_d={alpha_d:.0f}$ m/s)")
ax_tx_dip.plot(L - x, t_rev_dip, color=C_REV, lw=1.2, ls="--", alpha=0.7,
               label=f"Head wave (rev, $\\alpha_u={alpha_u:.0f}$ m/s)")
ax_tx_dip.axhline(t_recip_dip, color=C_RECIP, lw=1.0, ls=":",
                  alpha=0.8, label=f"$t_R$ = {t_recip_dip:.0f} ms")
# First arrivals solid
ax_tx_dip.plot(x, fa_fwd_dip, color=C_FWD, lw=2.5, ls="-", zorder=5,
               label="First arrivals (fwd)")
ax_tx_dip.plot(L - x, fa_rev_dip, color=C_REV, lw=2.5, ls="-", zorder=5,
               label="First arrivals (rev)")

# Source markers
ax_tx_dip.plot(0, 0, "v", ms=9, color=C_FWD, zorder=7, markeredgecolor="white")
ax_tx_dip.plot(L, 0, "v", ms=9, color=C_REV, zorder=7, markeredgecolor="white")

# Slope arrows with labels — positioned to avoid legend
xA = L * 0.55; tA = slope_d * xA * 1e3 + ti_d
ax_tx_dip.annotate(f"$1/\\alpha_d$", xy=(xA, tA),
                   xytext=(xA + 8, tA - 18), fontsize=10, color=C_FWD,
                   arrowprops=dict(arrowstyle="->", color=C_FWD, lw=1.0))
xB_pos = L * 0.42; xB_off = L - xB_pos
tB = slope_u * xB_off * 1e3 + ti_u
ax_tx_dip.annotate(f"$1/\\alpha_u$", xy=(xB_pos, tB),
                   xytext=(xB_pos - 20, tB - 18), fontsize=10, color=C_REV,
                   arrowprops=dict(arrowstyle="->", color=C_REV, lw=1.0))

ax_tx_dip.set_xlim(0, L)
ax_tx_dip.set_ylim(0, np.max(t_dir) * 1.08)
ax_tx_dip.set_xlabel("Position $x$ (m)")
ax_tx_dip.set_ylabel("$t$ (ms)")
ax_tx_dip.set_title("(d) $T$-$x$: dipping — asymmetric slopes",
                    fontweight="bold", fontsize=11)
ax_tx_dip.legend(loc="lower right", fontsize=8.5, framealpha=0.88,
                 ncol=2, handlelength=1.4)


# ═══════════════════════════════════════════════════════════════════════
# COMBINED REVERSED-PROFILE PANEL
# ═══════════════════════════════════════════════════════════════════════
# Show both forward and reverse branches together, first arrivals solid

# Individual branches (dashed, light)
ax_big.plot(x, t_dir,     color=C_DIRECT,  lw=1.0, ls="--", alpha=0.5, zorder=3,
            label="Direct ($1/V_1$)")
ax_big.plot(x, t_fwd_dip, color=C_FWD, lw=1.2, ls="--", alpha=0.65, zorder=3,
            label=f"Fwd head wave branch ($\\alpha_d = {alpha_d:.0f}$ m/s)")
ax_big.plot(L - x, t_rev_dip, color=C_REV, lw=1.2, ls="--", alpha=0.65, zorder=3,
            label=f"Rev head wave branch ($\\alpha_u = {alpha_u:.0f}$ m/s)")

# First arrivals (solid, thick) — the critical observables
ax_big.plot(x,     fa_fwd_dip, color=C_FWD, lw=3.0, ls="-", zorder=5,
            label="First arrivals — forward shot (solid)")
ax_big.plot(L - x, fa_rev_dip, color=C_REV, lw=3.0, ls="-", zorder=5,
            label="First arrivals — reverse shot (solid)")

# Reciprocal time
ax_big.axhline(t_recip_dip, color=C_RECIP, lw=1.5, ls="-.", zorder=4,
               label=f"Reciprocal time $t_R$ = {t_recip_dip:.0f} ms (equal both ends)")

# Source markers (both ends, colored)
ax_big.plot(0, 0, "v", ms=13, color=C_FWD, zorder=7,
            markeredgecolor="white", markeredgewidth=1.0)
ax_big.plot(L, 0, "v", ms=13, color=C_REV, zorder=7,
            markeredgecolor="white", markeredgewidth=1.0)
ax_big.text(3,  5, "Forward\nsource", ha="left",  fontsize=11,
            color=C_FWD, fontweight="bold")
ax_big.text(L - 3, 5, "Reverse\nsource", ha="right", fontsize=11,
            color=C_REV, fontweight="bold")

# Inline slope labels (avoid upper-right where legend sits)
xL_fwd = L * 0.48; tL_fwd = slope_d * xL_fwd * 1e3 + ti_d
ax_big.text(xL_fwd + 3, tL_fwd + 8,
            f"slope = $1/\\alpha_d$ = {1/alpha_d*1e3:.3f} ms/m",
            fontsize=10, color=C_FWD,
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8, ec=C_FWD, lw=0.8))

xL_rev_pos = L * 0.48; xL_rev_off = L - xL_rev_pos
tL_rev = slope_u * xL_rev_off * 1e3 + ti_u
ax_big.text(xL_rev_pos - 3, tL_rev + 8,
            f"slope = $1/\\alpha_u$ = {1/alpha_u*1e3:.3f} ms/m",
            fontsize=10, color=C_REV, ha="right",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.8, ec=C_REV, lw=0.8))

# Reciprocal time annotation
ax_big.text(L / 2, t_recip_dip + 5, f"$t_R$ = {t_recip_dip:.0f} ms  ← equal for both shots →",
            ha="center", fontsize=10, color=C_RECIP,
            bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.85, ec=C_RECIP, lw=1.0))

# Legend: lower-right, compact
ax_big.legend(loc="lower right", fontsize=9.5, framealpha=0.90,
              ncol=1, handlelength=1.8, borderpad=0.6)

ax_big.set_xlim(0, L)
ax_big.set_ylim(-2, max(np.nanmax(fa_fwd_dip), np.nanmax(fa_rev_dip)) * 1.25)
ax_big.set_xlabel("Position along profile (m)")
ax_big.set_ylabel("Travel time $t$ (ms)")
ax_big.set_title(
    f"(e) Reversed profile — $V_1 = {int(V1)}$, $V_2 = {int(V2)}$ m/s, dip = {dip_deg:.0f}° "
    f"— solid = first arrivals, dashed = all branches",
    fontweight="bold", fontsize=12)

# ── Save ─────────────────────────────────────────────────────────────
fig.tight_layout()
fig.savefig("assets/figures/fig_dipping_interface_reversed.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_dipping_interface_reversed.png")

if __name__ == "__main__":
    plt.show()
