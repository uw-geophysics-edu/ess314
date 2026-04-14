"""
fig_dipping_interface_reversed.py

Scientific content:
    Reversed refraction profiles over (a) a horizontal interface and
    (b) a dipping interface. Demonstrates that dip causes forward and
    reverse T-x head-wave segments to have different slopes (apparent
    velocities alpha_d and alpha_u). First arrivals are shown as solid
    lines; individual branches as dashed. Ray paths for both forward
    and reverse shots are drawn on the cross-sections. In subplot (b)
    both shots share the same surface source and receiver positions so
    the asymmetry comes from the geometry, not from different endpoints.
    The reciprocal time is identical for both shot directions.

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
from matplotlib.patches import Arc

# ── Global rcParams ──────────────────────────────────────────────────
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
C_LAYER1 = "#56B4E9"   # overburden fill
C_LAYER2 = "#E69F00"   # refractor fill (warm)
C_FWD    = "#0072B2"   # forward shot / down-dip
C_REV    = "#E69F00"   # reverse shot / up-dip
C_DIRECT = "#333333"   # direct wave
C_RECIP  = "#CC79A7"   # reciprocal time
C_IFACE  = "#444444"   # interface line

# ── Model parameters ─────────────────────────────────────────────────
V1, V2  = 500.0, 1500.0   # m/s
h0_flat = 20.0             # vertical depth (flat model), m
dip_deg = 6.0              # dip angle (degrees) — exaggerated for clarity
delta   = np.radians(dip_deg)
L       = 120.0            # profile length, m
x       = np.linspace(0.0, L, 3000)
tic     = np.arcsin(V1 / V2)    # critical angle, rad

# ── Flat-interface travel times ───────────────────────────────────────
ti_flat      = 2 * h0_flat * np.cos(tic) / V1 * 1e3   # ms
t_dir        = x / V1 * 1e3
t_fwd_flat   = x / V2 * 1e3 + ti_flat
t_rev_flat   = (L - x) / V2 * 1e3 + ti_flat
t_recip_flat = L / V2 * 1e3 + ti_flat
fa_fwd_flat  = np.minimum(t_dir, t_fwd_flat)
fa_rev_flat  = np.minimum((L - x) / V1 * 1e3, t_rev_flat)

# ── Dipping-interface travel times ────────────────────────────────────
# Perpendicular depth at each surface source
d_A     = h0_flat                          # perp depth under fwd source (x=0)
d_B     = d_A + L * np.sin(delta)         # perp depth under rev source (x=L)

slope_d = np.sin(tic + delta) / V1        # s/m  (down-dip apparent slowness)
slope_u = np.sin(tic - delta) / V1        # s/m  (up-dip apparent slowness)
ti_d    = 2 * d_A * np.cos(tic) / V1 * 1e3
ti_u    = 2 * d_B * np.cos(tic) / V1 * 1e3

t_fwd_dip   = slope_d * x * 1e3 + ti_d          # fwd: source at x=0
t_rev_dip   = slope_u * (L - x) * 1e3 + ti_u    # rev: source at x=L
t_recip_dip = slope_d * L * 1e3 + ti_d          # == slope_u*L*1e3 + ti_u

fa_fwd_dip  = np.minimum(t_dir, t_fwd_dip)
fa_rev_dip  = np.minimum((L - x) / V1 * 1e3, t_rev_dip)

alpha_d = 1.0 / slope_d   # apparent velocity down-dip, m/s
alpha_u = 1.0 / slope_u   # apparent velocity up-dip,   m/s

# ── Vertical depth of dipping interface ──────────────────────────────
def vert_depth(x_pos):
    """Vertical depth of the dipping interface at surface position x_pos."""
    return d_A / np.cos(delta) + x_pos * np.tan(delta)

# ── Shared receiver for subplot (b) ──────────────────────────────────
# Both forward (shot at x=0) and reverse (shot at x=L) rays emerge at
# the SAME receiver position x_shared, so the asymmetry is purely
# geometrical (different incidence angles, not different endpoints).
x_shared = 0.75 * L   # shared receiver / surface emergence point

def dip_head_wave_ray(shot_x, recv_x):
    """
    Compute the 4-point head-wave ray path for a dipping interface:
      shot_x → entry point on interface → exit point on interface → recv_x

    Angles are measured from the vertical.  Down-dip (shot_x < recv_x):
      incidence angle = tic + delta,  emergence angle = tic - delta.
    Up-dip (shot_x > recv_x):
      incidence angle = tic - delta,  emergence angle = tic + delta.

    Derivation (correct closed-form for arbitrary endpoints):
      Let Z0 = d_A / cos(delta)  [vert depth of interface at x=0].
      Entry (going right):
        x_entry = (shot_x + Z0*tan(ti)) / (1 - tan(delta)*tan(ti))
      Exit (going right):
        x_exit  = (recv_x - Z0*tan(te)) / (1 + tan(delta)*tan(te))
      Entry (going left):
        x_entry = (shot_x - Z0*tan(ti)) / (1 + tan(delta)*tan(ti))
      Exit (going left):
        x_exit  = (recv_x + Z0*tan(te)) / (1 - tan(delta)*tan(te))
    where ti = theta_inc, te = theta_eme.
    """
    going_right = recv_x > shot_x
    Z0 = d_A / np.cos(delta)   # vertical depth of interface at x=0

    if going_right:
        ti = tic + delta   # incidence angle from vertical (down-dip)
        te = tic - delta   # emergence angle from vertical
        x_entry = (shot_x + Z0 * np.tan(ti)) / (1.0 - np.tan(delta) * np.tan(ti))
        x_exit  = (recv_x - Z0 * np.tan(te)) / (1.0 + np.tan(delta) * np.tan(te))
    else:
        ti = tic - delta   # incidence angle (up-dip, shallower)
        te = tic + delta   # emergence angle
        x_entry = (shot_x - Z0 * np.tan(ti)) / (1.0 + np.tan(delta) * np.tan(ti))
        x_exit  = (recv_x + Z0 * np.tan(te)) / (1.0 - np.tan(delta) * np.tan(te))

    z_entry = vert_depth(x_entry)
    z_exit  = vert_depth(x_exit)

    return ([shot_x, x_entry, x_exit, recv_x],
            [0.0,    z_entry, z_exit, 0.0   ])


# ── Flat interface ray helper ─────────────────────────────────────────
def flat_head_wave_ray(shot_x, recv_x, h):
    """Head-wave ray on a flat interface at vertical depth h."""
    dx = h * np.tan(tic)
    if recv_x > shot_x:
        x_entry = shot_x + dx
        x_exit  = recv_x - dx
    else:
        x_entry = shot_x - dx
        x_exit  = recv_x + dx
    return ([shot_x, x_entry, x_exit, recv_x],
            [0.0, h, h, 0.0])


# ── Figure layout ────────────────────────────────────────────────────
# 3 rows × 2 cols: row0 = cross-sections, row1 = individual T-x, row2 = combined
fig = plt.figure(figsize=(13, 12))
gs  = fig.add_gridspec(3, 2, hspace=0.75, wspace=0.38,
                       height_ratios=[1.2, 1.0, 1.5])

ax_cs_flat = fig.add_subplot(gs[0, 0])
ax_cs_dip  = fig.add_subplot(gs[0, 1])
ax_tx_flat = fig.add_subplot(gs[1, 0])
ax_tx_dip  = fig.add_subplot(gs[1, 1])
ax_big     = fig.add_subplot(gs[2, :])

# Helper: annotation kwargs for text boxes that always appear on top
def tbox(color, alpha=0.90):
    return dict(boxstyle="round,pad=0.25", fc="white", ec=color,
                lw=0.9, alpha=alpha)

def arrow_kw(color):
    return dict(arrowstyle="->", color=color, lw=1.3)

def add_ray_arrows(ax, xs, zs, color):
    """Add direction arrows at midpoint of each segment of a ray path."""
    for i in range(len(xs) - 1):
        mx = (xs[i] + xs[i+1]) / 2
        mz = (zs[i] + zs[i+1]) / 2
        dx = xs[i+1] - xs[i]; dz = zs[i+1] - zs[i]
        norm = np.hypot(dx, dz)
        if norm < 1e-6:
            continue
        ax.annotate("", xy=(mx + 0.3*dx/norm*2, mz + 0.3*dz/norm*2),
                    xytext=(mx - 0.3*dx/norm*2, mz - 0.3*dz/norm*2),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.3),
                    zorder=8)


# ═══════════════════════════════════════════════════════════════════════
# (a) CROSS-SECTION: FLAT INTERFACE
# Only 2 surface locations: A (x=0) and B (x=L).
# Forward shot: A = source, B = receiver  → blue solid ray
# Reverse shot: B = source, A = receiver  → orange dashed ray (same path,
#   reciprocity makes the geometry identical; arrows show opposite direction)
# ═══════════════════════════════════════════════════════════════════════
depth_cs = h0_flat + 14
ax_cs_flat.set_xlim(-8, L + 8)
ax_cs_flat.set_ylim(depth_cs, -10)

ax_cs_flat.axhspan(0, h0_flat,        facecolor=C_LAYER1,  alpha=0.25, zorder=1)
ax_cs_flat.axhspan(h0_flat, depth_cs, facecolor="#E69F00", alpha=0.15, zorder=1)
ax_cs_flat.axhline(h0_flat, color=C_IFACE, lw=2.0, zorder=2)

ax_cs_flat.text(L*0.5, h0_flat*0.45, f"$V_1 = {int(V1)}$ m/s",
                ha="center", va="center", fontsize=11, zorder=9,
                bbox=tbox("#555", 0.7))
ax_cs_flat.text(L*0.5, h0_flat + 6, f"$V_2 = {int(V2)}$ m/s",
                ha="center", va="center", fontsize=11, zorder=9,
                bbox=tbox("#555", 0.7))
ax_cs_flat.text(L*0.5, -7.5, f"$h = {int(h0_flat)}$ m",
                ha="center", fontsize=10, color="#555", zorder=9)

# Location A (left) and B (right) — roles swap between shots
for xp, col, top_label, bot_label in [
        (0, C_FWD, "A",  "source\n(fwd) / receiver\n(rev)"),
        (L, C_REV, "B",  "receiver\n(fwd) / source\n(rev)")]:
    ax_cs_flat.plot(xp, 0, "o", ms=13, color=col, zorder=7,
                   markeredgecolor="white", markeredgewidth=1.2)
    ax_cs_flat.text(xp, -1.8, top_label, ha="center", fontsize=12,
                   fontweight="bold", color=col, zorder=9)
    ax_cs_flat.text(xp, -5.5 if xp == 0 else -5.5, bot_label,
                   ha="center", fontsize=7.5, color=col, zorder=9,
                   bbox=tbox(col, 0.80))

# Forward ray: A (x=0) → B (x=L)
rfx, rfz = flat_head_wave_ray(0, L, h0_flat)
ax_cs_flat.plot(rfx, rfz, color=C_FWD, lw=2.2, zorder=4, label="Forward ray (A→B)")
add_ray_arrows(ax_cs_flat, rfx, rfz, C_FWD)

# Reverse ray: B (x=L) → A (x=0)  — same geometry, opposite arrows
rrx, rrz = flat_head_wave_ray(L, 0, h0_flat)
ax_cs_flat.plot(rrx, rrz, color=C_REV, lw=2.2, ls="--", zorder=4, label="Reverse ray (B→A)")
add_ray_arrows(ax_cs_flat, rrx, rrz, C_REV)

ax_cs_flat.set_ylabel("Depth (m)")
ax_cs_flat.set_title("(a) Horizontal interface — swap A↔B: identical path",
                     fontweight="bold", fontsize=11)


# ═══════════════════════════════════════════════════════════════════════
# (b) CROSS-SECTION: DIPPING INTERFACE
# Same 2 locations as (a): A (x=0) and B (x=L).
# Forward: source=A, receiver=B  → ray travels down-dip (blue)
# Reverse: source=B, receiver=A  → ray travels up-dip   (orange dashed)
# The interface dip makes these physically different ray paths, even though
# the endpoints are identical — the interface segment sits deeper on the
# down-dip (right) side, so the critical angles are asymmetric.
# ═══════════════════════════════════════════════════════════════════════
depth_cs_dip = vert_depth(L) + 18
ax_cs_dip.set_xlim(-8, L + 8)
ax_cs_dip.set_ylim(depth_cs_dip, -10)

z_iface = vert_depth(np.array([0.0, L]))
ax_cs_dip.fill_between([0, L], [0, 0], z_iface,
                       facecolor=C_LAYER1, alpha=0.25, zorder=1)
ax_cs_dip.fill_between([0, L], z_iface, depth_cs_dip,
                       facecolor="#E69F00", alpha=0.15, zorder=1)
ax_cs_dip.plot([0, L], z_iface, color=C_IFACE, lw=2.0, zorder=2)

ax_cs_dip.text(L*0.22, vert_depth(L*0.22)*0.42, f"$V_1 = {int(V1)}$ m/s",
               ha="center", fontsize=11, zorder=9, bbox=tbox("#555", 0.7))
ax_cs_dip.text(L*0.50, vert_depth(L*0.50)+8, f"$V_2 = {int(V2)}$ m/s",
               ha="center", fontsize=11, zorder=9, bbox=tbox("#555", 0.7))

# Dip arc annotation (near left end, avoids ray clutter on right)
x_arc = L * 0.20; z_arc_pos = vert_depth(x_arc)
r_arc = 7
arc = Arc((x_arc, z_arc_pos), 2*r_arc, 2*r_arc,
          angle=0, theta1=180, theta2=180+dip_deg,
          color="#333", lw=1.5, zorder=5)
ax_cs_dip.add_patch(arc)
ax_cs_dip.text(x_arc - r_arc - 2, z_arc_pos + 2,
               f"$\\delta={dip_deg:.0f}°$", fontsize=11, color="#333",
               ha="right", va="bottom", zorder=9)
ax_cs_dip.plot([x_arc - r_arc - 1, x_arc + 2], [z_arc_pos, z_arc_pos],
               color="#999", lw=0.8, ls=":", zorder=3)

# Location A and B — same meaning as panel (a)
for xp, col, top_label, bot_label in [
        (0, C_FWD, "A",  "source\n(fwd) / receiver\n(rev)"),
        (L, C_REV, "B",  "receiver\n(fwd) / source\n(rev)")]:
    ax_cs_dip.plot(xp, 0, "o", ms=13, color=col, zorder=7,
                  markeredgecolor="white", markeredgewidth=1.2)
    ax_cs_dip.text(xp, -1.8, top_label, ha="center", fontsize=12,
                  fontweight="bold", color=col, zorder=9)
    ax_cs_dip.text(xp, -5.5, bot_label, ha="center", fontsize=7.5,
                  color=col, zorder=9, bbox=tbox(col, 0.80))

# Forward head-wave ray: A (x=0) → B (x=L), down-dip
dfx, dfz = dip_head_wave_ray(0, L)
ax_cs_dip.plot(dfx, dfz, color=C_FWD, lw=2.2, zorder=4,
               label="Forward ray A→B (down-dip)")
add_ray_arrows(ax_cs_dip, dfx, dfz, C_FWD)

# Reverse head-wave ray: B (x=L) → A (x=0), up-dip
drx, drz = dip_head_wave_ray(L, 0)
ax_cs_dip.plot(drx, drz, color=C_REV, lw=2.2, ls="--", zorder=4,
               label="Reverse ray B→A (up-dip)")
add_ray_arrows(ax_cs_dip, drx, drz, C_REV)

# Annotate the interface entry points to show incidence angle asymmetry
ax_cs_dip.annotate(f"steeper entry\n($\\theta_{{ic}}+\\delta$)",
                   xy=(dfx[1], dfz[1]),
                   xytext=(dfx[1] - 20, dfz[1] + 6),
                   fontsize=8, color=C_FWD, zorder=10,
                   bbox=tbox(C_FWD, 0.88),
                   arrowprops=dict(arrowstyle="->", color=C_FWD, lw=0.9))
ax_cs_dip.annotate(f"shallower entry\n($\\theta_{{ic}}-\\delta$)",
                   xy=(drx[1], drz[1]),
                   xytext=(drx[1] + 5, drz[1] + 8),
                   fontsize=8, color=C_REV, zorder=10,
                   bbox=tbox(C_REV, 0.88),
                   arrowprops=dict(arrowstyle="->", color=C_REV, lw=0.9))

ax_cs_dip.set_title("(b) Dipping interface — swap A↔B: different ray paths",
                    fontweight="bold", fontsize=11)


# ═══════════════════════════════════════════════════════════════════════
# (c) T-x: FLAT (no per-panel legend — handled by bottom panel)
# ═══════════════════════════════════════════════════════════════════════
ax_tx_flat.plot(x, t_dir,        color=C_DIRECT, lw=1.0, ls="--", alpha=0.7)
ax_tx_flat.plot(x, t_fwd_flat,   color=C_FWD,    lw=1.0, ls="--", alpha=0.6)
ax_tx_flat.plot(L-x, t_rev_flat, color=C_REV,    lw=1.0, ls="--", alpha=0.6)
ax_tx_flat.axhline(t_recip_flat, color=C_RECIP,  lw=1.0, ls=":", alpha=0.8)
ax_tx_flat.plot(x, fa_fwd_flat,   color=C_FWD, lw=2.5, zorder=5)
ax_tx_flat.plot(L-x, fa_rev_flat, color=C_REV, lw=2.5, zorder=5)
ax_tx_flat.plot(0, 0, "v", ms=9, color=C_FWD, zorder=7, markeredgecolor="white")
ax_tx_flat.plot(L, 0, "v", ms=9, color=C_REV, zorder=7, markeredgecolor="white")

# Annotation: equal slopes
ax_tx_flat.text(L*0.5, t_recip_flat + 8,
                f"$t_R$ = {t_recip_flat:.0f} ms", ha="center", fontsize=9.5,
                color=C_RECIP, zorder=10, bbox=tbox(C_RECIP))
ax_tx_flat.text(L*0.35, 0.42*(t_fwd_flat[int(0.35*3000)]),
                "fwd = rev\n(symmetric)", ha="center", fontsize=9, color=C_FWD,
                zorder=10, bbox=tbox(C_FWD, 0.85))

ax_tx_flat.set_xlim(0, L)
ax_tx_flat.set_ylim(0, np.max(t_dir) * 1.10)
ax_tx_flat.set_xlabel("Position $x$ (m)")
ax_tx_flat.set_ylabel("$t$ (ms)")
ax_tx_flat.set_title(r"(c) $T$-$x$: flat — fwd = rev (symmetric)",
                     fontweight="bold", fontsize=11)


# ═══════════════════════════════════════════════════════════════════════
# (d) T-x: DIPPING (no per-panel legend)
# ═══════════════════════════════════════════════════════════════════════
ax_tx_dip.plot(x, t_dir,         color=C_DIRECT, lw=1.0, ls="--", alpha=0.7)
ax_tx_dip.plot(x, t_fwd_dip,     color=C_FWD,    lw=1.0, ls="--", alpha=0.6)
ax_tx_dip.plot(L-x, t_rev_dip,   color=C_REV,    lw=1.0, ls="--", alpha=0.6)
ax_tx_dip.axhline(t_recip_dip,   color=C_RECIP,  lw=1.0, ls=":", alpha=0.8)
ax_tx_dip.plot(x, fa_fwd_dip,     color=C_FWD, lw=2.5, zorder=5)
ax_tx_dip.plot(L-x, fa_rev_dip,   color=C_REV, lw=2.5, zorder=5)
ax_tx_dip.plot(0, 0, "v", ms=9, color=C_FWD, zorder=7, markeredgecolor="white")
ax_tx_dip.plot(L, 0, "v", ms=9, color=C_REV, zorder=7, markeredgecolor="white")

ax_tx_dip.set_xlim(0, L)
ax_tx_dip.set_ylim(0, np.max(t_dir) * 1.10)
ax_tx_dip.set_xlabel("Position $x$ (m)")
ax_tx_dip.set_ylabel("$t$ (ms)")
ax_tx_dip.set_title(r"(d) $T$-$x$: dipping — asymmetric slopes",
                    fontweight="bold", fontsize=11)

# Slope labels — placed ON the head-wave lines, with white bbox
xA = L * 0.60; tA = slope_d * xA * 1e3 + ti_d
ax_tx_dip.text(xA + 4, tA - 15, f"$1/\\alpha_d$",
               fontsize=10, color=C_FWD, zorder=10, bbox=tbox(C_FWD))

xB_pos = L * 0.38; xB_off = L - xB_pos; tB = slope_u * xB_off * 1e3 + ti_u
ax_tx_dip.text(xB_pos - 4, tB + 6, f"$1/\\alpha_u$",
               ha="right", fontsize=10, color=C_REV, zorder=10, bbox=tbox(C_REV))

ax_tx_dip.text(L*0.5, t_recip_dip + 8,
               f"$t_R$ = {t_recip_dip:.0f} ms", ha="center", fontsize=9.5,
               color=C_RECIP, zorder=10, bbox=tbox(C_RECIP))


# ═══════════════════════════════════════════════════════════════════════
# (e) COMBINED REVERSED-PROFILE PANEL  —  single legend for ALL panels
# ═══════════════════════════════════════════════════════════════════════
handles = []  # collect all legend handles here

h1, = ax_big.plot(x, t_dir, color=C_DIRECT, lw=1.0, ls="--", alpha=0.5, zorder=3,
                  label="Direct wave ($1/V_1$)")
h2, = ax_big.plot(x, t_fwd_dip, color=C_FWD, lw=1.2, ls="--", alpha=0.65, zorder=3,
                  label=f"Fwd head wave ($\\alpha_d = {alpha_d:.0f}$ m/s)")
h3, = ax_big.plot(L-x, t_rev_dip, color=C_REV, lw=1.2, ls="--", alpha=0.65, zorder=3,
                  label=f"Rev head wave ($\\alpha_u = {alpha_u:.0f}$ m/s)")
h4, = ax_big.plot(x,   fa_fwd_dip, color=C_FWD, lw=3.0, zorder=5,
                  label="First arrivals — forward shot")
h5, = ax_big.plot(L-x, fa_rev_dip, color=C_REV, lw=3.0, zorder=5,
                  label="First arrivals — reverse shot")
h6  = ax_big.axhline(t_recip_dip, color=C_RECIP, lw=1.5, ls="-.", zorder=4,
                     label=f"Reciprocal time $t_R$ (equal both ends)")

# Source markers
ax_big.plot(0, 0, "v", ms=13, color=C_FWD, zorder=7,
            markeredgecolor="white", markeredgewidth=1.0)
ax_big.plot(L, 0, "v", ms=13, color=C_REV, zorder=7,
            markeredgecolor="white", markeredgewidth=1.0)
ax_big.text(3, 5, "Forward\nsource", ha="left", fontsize=10,
            color=C_FWD, fontweight="bold", zorder=10)
ax_big.text(L-3, 5, "Reverse\nsource", ha="right", fontsize=10,
            color=C_REV, fontweight="bold", zorder=10)

# Slope labels on the head-wave branches (fully above other elements)
xL_fwd = L * 0.46
tL_fwd = slope_d * xL_fwd * 1e3 + ti_d
ax_big.text(xL_fwd + 2, tL_fwd + 9,
            f"slope = $1/\\alpha_d$ = {1/alpha_d*1e3:.3f} ms/m",
            fontsize=10, color=C_FWD, zorder=10,
            bbox=tbox(C_FWD))

xL_rev_pos = L * 0.52
tL_rev = slope_u * (L - xL_rev_pos) * 1e3 + ti_u
ax_big.text(xL_rev_pos - 2, tL_rev + 9,
            f"slope = $1/\\alpha_u$ = {1/alpha_u*1e3:.3f} ms/m",
            ha="right", fontsize=10, color=C_REV, zorder=10,
            bbox=tbox(C_REV))

# Reciprocal time annotation
ax_big.text(L/2, t_recip_dip + 6,
            f"$t_R$ = {t_recip_dip:.0f} ms  ← equal for both shots →",
            ha="center", fontsize=10, color=C_RECIP, zorder=10,
            bbox=tbox(C_RECIP))

ax_big.set_xlim(0, L)
ax_big.set_ylim(-2, max(np.nanmax(fa_fwd_dip), np.nanmax(fa_rev_dip)) * 1.30)
ax_big.set_xlabel("Position along profile (m)")
ax_big.set_ylabel("Travel time $t$ (ms)")
ax_big.set_title(
    f"(e) Reversed profile — $V_1={int(V1)}$, $V_2={int(V2)}$ m/s, "
    f"dip={dip_deg:.0f}° — solid = first arrivals, dashed = all branches",
    fontweight="bold", fontsize=12)

# ── SINGLE legend for the whole figure (placed inside bottom panel) ──
# Add cross-section entries manually so the one legend explains all panels
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
leg_handles = [
    h1, h2, h3, h4, h5, h6,
    Line2D([0], [0], marker="v", color="w", markerfacecolor=C_FWD,
           ms=10, label="Forward source (▼)"),
    Line2D([0], [0], marker="v", color="w", markerfacecolor=C_REV,
           ms=10, label="Reverse source (▼)"),
    Line2D([0], [0], marker="^", color="w", markerfacecolor="#009E73",
           ms=10, label="Shared receiver (▲)"),
]
ax_big.legend(handles=leg_handles, loc="lower right",
              fontsize=9.5, framealpha=0.93, ncol=1,
              handlelength=1.8, borderpad=0.7, title="Legend — all panels",
              title_fontsize=9.5)

# ── Save ─────────────────────────────────────────────────────────────
fig.tight_layout()
fig.savefig("assets/figures/fig_dipping_interface_reversed.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_dipping_interface_reversed.png")

if __name__ == "__main__":
    plt.show()
