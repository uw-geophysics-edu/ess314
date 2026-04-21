"""
Multi-layer depth conversion comparison.

Three-panel figure showing why a layered velocity model (from refraction + Dix)
is needed even for perfectly flat, horizontal reflectors:

  (a) True Earth model — three horizontal layers with different velocities
  (b) Depth image using a single constant average velocity  → large depth errors
  (c) Depth image using the correct Dix + refraction velocities → exact depths

Numerical values
----------------
  Layer 1:  v1 = 1.8 km/s,  base at z = 0.80 km
  Layer 2:  v2 = 2.8 km/s,  base at z = 2.00 km
  Layer 3:  v3 = 4.5 km/s,  base at z = 3.50 km

  Two-way zero-offset times:
    t1 = 2*0.80/1.8        = 0.889 s
    t2 = t1 + 2*1.20/2.8  = 1.746 s
    t3 = t2 + 2*1.50/4.5  = 2.413 s

  With v_assumed = 2.0 km/s:
    z1 = 0.889 km  (true 0.80 → +11 %)
    z2 = 1.746 km  (true 2.00 → −13 %)
    z3 = 2.413 km  (true 3.50 → −31 %)
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch

# Colorblind-safe palette
C_BLUE   = "#0072B2"
C_VERM   = "#D55E00"
C_GREEN  = "#009E73"
C_BLACK  = "#000000"
C_GREY   = "#888888"

# ---------------------------------------------------------------------------
# Model parameters
# ---------------------------------------------------------------------------
v_true   = [1.8, 2.8, 4.5]          # layer interval velocities (km/s)
z_true   = [0.80, 2.00, 3.50]       # true interface depths (km)
v_assumed = 2.0                      # constant velocity for wrong image

# Two-way zero-offset travel times
t = [2 * z_true[0] / v_true[0],
     0.0,
     0.0]
t[1] = t[0] + 2 * (z_true[1] - z_true[0]) / v_true[1]
t[2] = t[1] + 2 * (z_true[2] - z_true[1]) / v_true[2]

# Depth images
z_wrong = [v_assumed * ti / 2 for ti in t]
z_dix   = [
    v_true[0] * t[0] / 2,
    z_true[0] + v_true[1] * (t[1] - t[0]) / 2,
    z_true[1] + v_true[2] * (t[2] - t[1]) / 2,
]

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
ZMAX = 4.3
XMAX = 1.0   # dimensionless, just for fill_between
layer_colors  = ["#BDD7EE", "#FFE0A3", "#B8E0B8"]   # blue, tan, green
halfspace_col = "#D8C8B8"

fig, axes = plt.subplots(1, 3, figsize=(13, 6.5), sharey=True,
                          gridspec_kw={"wspace": 0.08})

# ---- helper -----------------------------------------------------------
def horz_bands(ax, z_list, colors):
    """Draw horizontal coloured bands for layers."""
    bounds = [0.0] + list(z_list) + [ZMAX]
    for i, (zt, zb) in enumerate(zip(bounds[:-1], bounds[1:])):
        c = colors[i] if i < len(colors) else halfspace_col
        ax.fill_between([0, XMAX], zt, zb, color=c, alpha=0.85)

def draw_interface(ax, z, color, ls="-", lw=2.5, zorder=5):
    ax.axhline(z, color=color, lw=lw, ls=ls, zorder=zorder)

def vel_label(ax, zmid, text, color="#333333"):
    if 0 < zmid < ZMAX:
        ax.text(0.50, zmid, text, ha="center", va="center",
                fontsize=9, style="italic", color=color, zorder=7)

def depth_label(ax, z, text, color):
    ax.text(0.97, z, text, ha="right", va="bottom",
            fontsize=8.5, color=color, zorder=8,
            bbox=dict(fc="white", ec="none", alpha=0.7, pad=1))

# -----------------------------------------------------------------------
# Panel (a) — True Earth model
# -----------------------------------------------------------------------
ax = axes[0]
horz_bands(ax, z_true, layer_colors + [halfspace_col])

for iz, z in enumerate(z_true):
    draw_interface(ax, z, C_BLACK, lw=2.8)
    depth_label(ax, z - 0.04, f" z = {z:.2f} km", C_BLACK)

bounds_a = [0.0] + z_true + [ZMAX]
v_strs   = [f"v₁ = {v_true[0]} km/s\n(Layer 1)",
            f"v₂ = {v_true[1]} km/s\n(Layer 2)",
            f"v₃ = {v_true[2]} km/s\n(Layer 3)",
            "Half-space"]
for i, vs in enumerate(v_strs):
    zm = (bounds_a[i] + min(bounds_a[i+1], ZMAX)) / 2
    vel_label(ax, zm, vs)

ax.set_title("(a)  True Earth model", fontsize=11, fontweight="bold", pad=8)
ax.text(0.5, -0.10, "What we want to recover",
        transform=ax.transAxes, ha="center", fontsize=9, style="italic")
ax.set_ylabel("Depth (km)", fontsize=11)
ax.set_ylim(ZMAX, 0)
ax.set_xlim(0, XMAX)
ax.set_xticks([])
ax.grid(axis="y", alpha=0.25, lw=0.5)

# -----------------------------------------------------------------------
# Panel (b) — Constant-velocity depth image
# -----------------------------------------------------------------------
ax = axes[1]
horz_bands(ax, z_wrong, layer_colors + [halfspace_col])

# True model as grey dotted reference
for z in z_true:
    draw_interface(ax, z, C_GREY, ls=":", lw=1.5, zorder=4)

# Wrong interfaces
for iz, (z, zt) in enumerate(zip(z_wrong, z_true)):
    draw_interface(ax, z, C_VERM, ls="--", lw=2.5)
    err = z - zt
    pct = 100 * err / zt
    sign = "+" if err >= 0 else ""
    depth_label(ax, z - 0.04,
                f" z = {z:.2f} km  ({sign}{err:.2f} km, {sign}{pct:.0f}%)", C_VERM)

vel_label(ax, 0.4, f"v = {v_assumed} km/s\nassumed everywhere", "#555555")

ax.set_title(f"(b)  Constant-velocity migration\n     ($v = {v_assumed}$ km/s throughout)",
             fontsize=11, fontweight="bold", pad=4)
ax.text(0.5, -0.18,
        "Red — — — depth image.   Gray ····· true position.\n"
        "Errors: +11 %, −13 %, −31 % — geology is wrong.",
        transform=ax.transAxes, ha="center", fontsize=8.5, style="italic",
        color=C_VERM)
ax.set_xlim(0, XMAX);  ax.set_xticks([])
ax.grid(axis="y", alpha=0.25, lw=0.5)

# -----------------------------------------------------------------------
# Panel (c) — Correct Dix + refraction velocities
# -----------------------------------------------------------------------
ax = axes[2]
horz_bands(ax, z_dix, layer_colors + [halfspace_col])

# True model reference (should overlap exactly)
for z in z_true:
    draw_interface(ax, z, C_GREY, ls=":", lw=1.5, zorder=4)

# Correct interfaces
for iz, z in enumerate(z_dix):
    draw_interface(ax, z, C_BLUE, ls="-", lw=2.8)
    depth_label(ax, z - 0.04,
                f" z = {z:.2f} km  (exact ✓)", C_BLUE)

bounds_c = [0.0] + z_dix + [ZMAX]
src_strs = [f"v₁ = {v_true[0]} km/s  ← refraction",
            f"v₂ = {v_true[1]} km/s  ← Dix",
            f"v₃ = {v_true[2]} km/s  ← Dix",
            "Half-space"]
for i, vs in enumerate(src_strs):
    zm = (bounds_c[i] + min(bounds_c[i+1], ZMAX)) / 2
    c  = C_GREEN if i == 0 else C_BLUE
    vel_label(ax, zm, vs, color=c)

ax.set_title("(c)  Refraction + Dix velocity migration\n     (correct layer velocities)",
             fontsize=11, fontweight="bold", pad=4)
ax.text(0.5, -0.18,
        "Blue —— depth image = true model.\n"
        "Refraction pins v₁ (absolute); Dix gives v₂, v₃ from NMO.",
        transform=ax.transAxes, ha="center", fontsize=8.5, style="italic",
        color=C_BLUE)
ax.set_xlim(0, XMAX);  ax.set_xticks([])
ax.grid(axis="y", alpha=0.25, lw=0.5)

# -----------------------------------------------------------------------
# Shared legend + title
# -----------------------------------------------------------------------
legend_handles = [
    Line2D([0], [0], color=C_BLACK,  lw=2.8, label="True interface"),
    Line2D([0], [0], color=C_VERM,   lw=2.0, ls="--", label=f"Constant-$v$ image ($v={v_assumed}$ km/s)"),
    Line2D([0], [0], color=C_BLUE,   lw=2.8, label="Dix + refraction image"),
    Line2D([0], [0], color=C_GREY,   lw=1.5, ls=":", label="True position (reference)"),
]
fig.legend(handles=legend_handles, loc="lower center", ncol=4, fontsize=9,
           framealpha=0.9, bbox_to_anchor=(0.5, -0.02))

fig.suptitle(
    "Multi-layer depth conversion: why even flat reflectors need a layered velocity model\n"
    "Same two-way times, two velocity assumptions → very different depth images",
    fontsize=12, fontweight="bold", y=1.02)

plt.tight_layout(rect=[0, 0.06, 1, 1])
fig.savefig("assets/figures/fig_multilayer_depth_conversion.png",
            dpi=180, bbox_inches="tight")
print("Saved fig_multilayer_depth_conversion.png")
