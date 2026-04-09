"""
fig_refraction_wavefield_animation.py

Scientific content:
    Animation showing how the T(x) diagram for seismic refraction is built up
    as the wavefield propagates outward from a surface source over a two-layer
    model (V2 = 5 V1).  Each frame:
      - Reveals the next geophone pick on the T(x) diagram (top panel)
      - Draws the ray path to the current receiver (bottom panel)
      - RETAINS all previous ray paths (cumulative, faded to gray)
      - Colors the INTERFACE segment of each head wave by its lag time —
        the time spent traveling along the interface — using the plasma
        colormap (purple=short lag, yellow=long lag).  The same scalar
        maps onto the T(x) head-wave scatter points so both panels share
        the same physical variable.

    Conceptual reproduction of:
      Denolle, M. (2026). ESS 314 Lecture 6 slides (refraction2a.pdf).
      University of Washington.
    Physics: Lowrie & Fichtner (2020) Fundamentals of Geophysics 3rd ed.
      Cambridge University Press, S6.3.2. (via UW Libraries)

Output:
    assets/figures/fig_refraction_wavefield_animation.gif
    assets/figures/fig_refraction_wavefield_frame_final.png
License: CC-BY 4.0
Author:  ESS 314 course, UW, 2026
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import os

mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 110,
})

BLUE      = "#0072B2"
ORANGE    = "#E69F00"
BLACK     = "#000000"
VERMILION = "#D55E00"
GRAY_PREV = "#AAAAAA"
CMAP_LAG  = plt.get_cmap("plasma")

# ── Model ──────────────────────────────────────────────────────────────────────
V1, V2 = 1.0, 5.0
H = 0.20
N_GEO = 18
x_max = 1.0
geo_x = np.linspace(0.05, x_max, N_GEO)

theta_c = np.arcsin(V1 / V2)
x_leg   = H * np.tan(theta_c)

def t_direct(x):
    return np.atleast_1d(np.asarray(x, float)) / V1

def t_head(x):
    x = np.atleast_1d(np.asarray(x, float))
    t = x / V2 + 2 * H * np.cos(theta_c) / V1
    t[x < 2 * x_leg] = np.nan
    return t

is_head = np.zeros(N_GEO, dtype=bool)
t_fa    = np.zeros(N_GEO)
for i, xg in enumerate(geo_x):
    th = float(t_head(np.array([xg]))[0])
    td = float(t_direct(xg)[0])
    if not np.isnan(th) and th < td:
        is_head[i] = True
        t_fa[i] = th
    else:
        t_fa[i] = td

# Lag time on interface: physical time = (horizontal interface distance) / V2
# Both panels use t_lag directly (not normalised) through the shared LAG_NORM.
t_lag     = np.where(is_head, np.clip(geo_x - 2 * x_leg, 0, None) / V2, 0.0)
t_lag_max = t_lag.max() if t_lag.max() > 0 else 1.0

# Single shared normalisation — applied identically in BOTH panels
LAG_NORM = mcolors.Normalize(vmin=0, vmax=t_lag_max)

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, (ax_tx, ax_model) = plt.subplots(
    2, 1, figsize=(8.2, 7.2),
    gridspec_kw={"height_ratios": [1, 1]},
)
fig.subplots_adjust(hspace=0.42, right=0.82)   # leave room for colorbar

y_surface   =  0.0
y_interface = -H
y_bottom    = -H * 2.4

# ── Model panel ────────────────────────────────────────────────────────────────
ax_model.set_xlim(-0.04, x_max + 0.04)
ax_model.set_ylim(y_bottom, H * 0.60)
ax_model.set_xlabel("Distance (normalised)")
ax_model.set_ylabel("Depth (normalised)")
ax_model.set_title("Subsurface ray paths (cumulative; interface color = lag time)")

ax_model.axhspan(y_interface, y_surface, color="#DDEEFF", alpha=0.55, zorder=0)
ax_model.axhspan(y_bottom, y_interface,  color="#BBCCAA", alpha=0.45, zorder=0)
ax_model.axhline(y_interface, color="k", lw=1.5, ls="--", zorder=1)
ax_model.axhline(y_surface,   color="k", lw=1.0, zorder=1)

# Layer labels: right-aligned, pushed far enough right and vertically separated
ax_model.text(x_max + 0.02, -0.04,  r"$V_1$",
              ha="left", va="center", fontsize=11, color="navy")
ax_model.text(x_max + 0.02, -H * 1.5, r"$V_2=5V_1$",
              ha="left", va="center", fontsize=11, color="saddlebrown")

for xg in geo_x:
    ax_model.plot(xg, 0, "v", ms=6, color=BLACK, zorder=5, clip_on=False)
ax_model.plot(0, 0, "*", ms=16, color=VERMILION, zorder=7, clip_on=False)
ax_model.text(0.00, H * 0.46, "Source",
              ha="center", va="bottom", fontsize=9, color=VERMILION)

# Colorbar spanning BOTH panels — same norm as scatter and ray segments
# [left, bottom, width, height] in figure-fraction coordinates.
# right=0.82 leaves ~18% margin; cax sits at 0.84-0.865, spanning y=0.08-0.92.
cax = fig.add_axes([0.84, 0.08, 0.022, 0.84])
sm  = plt.cm.ScalarMappable(cmap=CMAP_LAG, norm=LAG_NORM)
sm.set_array([])
cbar = fig.colorbar(sm, cax=cax)
cbar.set_label("Interface lag time\n(normalised units)", fontsize=8, labelpad=4)
cbar.ax.tick_params(labelsize=8)

# ── T(x) panel ─────────────────────────────────────────────────────────────────
t_max  = float(t_direct(x_max)[0]) * 1.18
x_ref  = np.linspace(0, x_max, 500)
th_ref = t_head(x_ref)

ax_tx.plot(x_ref, t_direct(x_ref), color=BLUE, lw=1.5, ls="--",
           alpha=0.18, zorder=1)
ax_tx.plot(x_ref, np.where(np.isnan(th_ref), np.nan, th_ref),
           color=ORANGE, lw=1.5, ls="--", alpha=0.18, zorder=1)

ax_tx.set_xlim(-0.04, x_max + 0.04)
ax_tx.set_ylim(0, t_max)
ax_tx.set_xlabel("Distance (normalised)")
ax_tx.set_ylabel("Travel time (normalised)")
ax_tx.set_title("T(x) — picks coloured by wave type (head wave by lag time)")

# Legend anchored top-left — well clear of the data which plots lower-right
_leg_h = [
    plt.Line2D([0], [0], marker="o", color="w",
               markerfacecolor=BLUE,   markersize=8, label="Direct (first arrival)"),
    plt.Line2D([0], [0], marker="o", color="w",
               markerfacecolor=ORANGE, markersize=8, label="Head wave (first arrival)\n— colour = lag time"),
]
ax_tx.legend(handles=_leg_h, loc="upper left",
             fontsize=9, framealpha=0.90, edgecolor="gray")

# ── Animated artists ────────────────────────────────────────────────────────────
tx_direct_sc = ax_tx.scatter([], [], s=55, color=BLUE, zorder=5)
# cmap and norm are applied after first data arrives (avoids init warning).
# norm=LAG_NORM guarantees the same mapping as the model-panel interface segments.
tx_head_sc   = ax_tx.scatter([], [], s=55, zorder=5)
all_ray_lines = []   # accumulates across frames
ann = ax_model.text(x_max - 0.02, H * 0.50, "",
                    fontsize=9, color="dimgray", ha="right", va="top")


def draw_ray(xr, is_current):
    """Draw one ray to receiver xr.  Returns list of Line2D artists."""
    th_v = float(t_head(np.array([xr]))[0])
    td_v = float(t_direct(xr)[0])
    use_head = (not np.isnan(th_v)) and (th_v < td_v)

    lw   = 1.8 if is_current else 0.7
    alph = 1.0 if is_current else 0.30

    # Colour interface segment using physical lag time + shared LAG_NORM
    idx   = int(np.argmin(np.abs(geo_x - xr)))
    lag_v = float(t_lag[idx])                          # physical lag time
    ifc_c = CMAP_LAG(LAG_NORM(lag_v)) if (is_current and use_head) else GRAY_PREV

    arts = []
    if use_head:
        x_D  = xr - x_leg
        c_dn = BLUE   if is_current else GRAY_PREV
        c_up = ORANGE if is_current else GRAY_PREV
        l1, = ax_model.plot([0, x_leg],  [y_surface, y_interface],
                             color=c_dn, lw=lw, alpha=alph, zorder=3)
        l2, = ax_model.plot([x_leg, x_D], [y_interface, y_interface],
                             color=ifc_c, lw=lw * 1.4, alpha=alph, zorder=3,
                             solid_capstyle="round")
        l3, = ax_model.plot([x_D, xr],   [y_interface, y_surface],
                             color=c_up, lw=lw, alpha=alph, zorder=3)
        arts.extend([l1, l2, l3])
    else:
        c_d = BLUE if is_current else GRAY_PREV
        l1, = ax_model.plot([0, xr], [y_surface, y_surface],
                             color=c_d, lw=lw, alpha=alph, zorder=3)
        arts.append(l1)
    return arts


def init():
    tx_direct_sc.set_offsets(np.empty((0, 2)))
    tx_head_sc.set_offsets(np.empty((0, 2)))
    tx_head_sc.set_array(np.array([]))
    for ln in all_ray_lines:
        try: ln.remove()
        except Exception: pass
    all_ray_lines.clear()
    ann.set_text("")
    return [tx_direct_sc, tx_head_sc, ann]


def update(fi):
    # Fade all existing rays to historical appearance
    for ln in all_ray_lines:
        ln.set_linewidth(0.7)
        ln.set_alpha(0.28)
        ln.set_color(GRAY_PREV)

    # Draw current frame ray at full style
    new_arts = draw_ray(geo_x[fi], is_current=True)
    all_ray_lines.extend(new_arts)

    # T(x) scatter — direct
    dm = ~is_head[:fi + 1]
    if dm.any():
        tx_direct_sc.set_offsets(
            np.c_[geo_x[:fi + 1][dm], t_fa[:fi + 1][dm]])

    # T(x) scatter — head wave: physical lag values, same norm as model panel
    hm = is_head[:fi + 1]
    if hm.any():
        tx_head_sc.set_offsets(
            np.c_[geo_x[:fi + 1][hm], t_fa[:fi + 1][hm]])
        tx_head_sc.set_cmap(CMAP_LAG)
        tx_head_sc.set_norm(LAG_NORM)
        tx_head_sc.set_array(t_lag[:fi + 1][hm])          # physical units

    label = (f"Geophone {fi + 1}/{N_GEO}: "
             + ("head wave" if is_head[fi] else "direct wave") + " first")
    ann.set_text(label)
    return all_ray_lines + [tx_direct_sc, tx_head_sc, ann]


anim = animation.FuncAnimation(
    fig, update, frames=N_GEO,
    init_func=init, interval=750,
    blit=False, repeat=True, repeat_delay=2500,
)

os.makedirs("assets/figures", exist_ok=True)

gif_path = "assets/figures/fig_refraction_wavefield_animation.gif"
anim.save(gif_path, writer="pillow", fps=2, dpi=110)
print(f"GIF saved: {gif_path}")

# Final frame static PNG
init()
for fi in range(N_GEO):
    update(fi)
png_path = "assets/figures/fig_refraction_wavefield_frame_final.png"
fig.savefig(png_path, dpi=150, bbox_inches="tight")
print(f"Static frame: {png_path}")
plt.close()
print("Done.")
