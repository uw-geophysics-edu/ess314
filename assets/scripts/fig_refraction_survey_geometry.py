"""
fig_refraction_survey_geometry.py

Scientific content:
    Cross-section of a two-layer refraction survey showing:
      - Surface with source (hammer) at left, geophones along the surface
      - Layer 1 (velocity V1, thickness H) over a half-space (velocity V2 > V1)
      - Three labeled ray paths: direct wave, reflected wave, and head wave
      - The head wave descends at the critical angle theta_c, travels along
        the interface at V2, and returns to the surface at theta_c.

    Model parameters: V1 = 800 m/s, V2 = 3200 m/s, H = 12 m (UW campus example).

Output: assets/figures/fig_refraction_survey_geometry.png
License: CC-BY 4.0
Author:  ESS 314 course, University of Washington, 2026
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 12,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 150,
})

BLUE      = "#0072B2"
ORANGE    = "#E69F00"
GREEN     = "#009E73"
BLACK     = "#000000"
VERMILION = "#D55E00"

# ── Model ──────────────────────────────────────────────────────────────────────
V1 = 800.0    # m/s — surface layer (glacial till)
V2 = 3200.0   # m/s — bedrock
H  = 12.0     # m — layer thickness

theta_c = np.arcsin(V1 / V2)  # critical angle

# ── Geometry ──────────────────────────────────────────────────────────────────
x_max = 72.0  # survey extent (m)
n_geophones = 12
x_geo = np.linspace(6, x_max, n_geophones)

# Source position
x_src, z_src = 0.0, 0.0

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 5))

# Fill layers
ax.fill_between([- 5, x_max + 10], 0, H, color="#D2B48C", alpha=0.25, label=None)
ax.fill_between([- 5, x_max + 10], H, H + 8, color="#8B7D6B", alpha=0.25, label=None)

# Interface line
ax.axhline(H, color=BLACK, lw=1.5, ls="--", alpha=0.6)
ax.axhline(0, color=BLACK, lw=1.5, alpha=0.8)

# Layer labels
ax.text(x_max + 6, H / 2, f"Layer 1\n$V_1 = {V1:.0f}$ m/s\n$H = {H:.0f}$ m",
        ha="left", va="center", fontsize=11, color=BLACK)
ax.text(x_max + 6, H + 3.5, f"Layer 2 (half-space)\n$V_2 = {V2:.0f}$ m/s",
        ha="left", va="center", fontsize=11, color=BLACK)

# Source (star)
ax.plot(x_src, z_src, marker="*", color=VERMILION, markersize=18, zorder=5,
        markeredgecolor="k", markeredgewidth=0.5)
ax.text(x_src, -1.5, "Source", ha="center", va="bottom", fontsize=11,
        fontweight="bold", color=VERMILION)

# Geophones (triangles)
for xg in x_geo:
    ax.plot(xg, 0, marker="v", color=GREEN, markersize=9, zorder=5,
            markeredgecolor="k", markeredgewidth=0.5)
ax.text(x_geo[-1], -1.5, "Geophones", ha="right", va="bottom", fontsize=10,
        color=GREEN)

# ── Ray paths ──────────────────────────────────────────────────────────────

# 1. Direct wave — to a near-offset geophone
x_direct = x_geo[2]
ax.annotate("", xy=(x_direct, 0.3), xytext=(x_src, 0.3),
            arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.25",
                            color=BLUE, lw=2.5))
ax.text((x_src + x_direct) / 2, 1.5, "Direct wave", ha="center",
        fontsize=11, fontweight="bold", color=BLUE)

# 2. Reflected wave — to a mid-offset geophone
x_refl = x_geo[5]
x_bounce = x_refl / 2.0
ax.plot([x_src, x_bounce], [z_src, H], color=ORANGE, lw=2, ls="-")
ax.plot([x_bounce, x_refl], [H, z_src], color=ORANGE, lw=2, ls="-")
# Reflection point marker
ax.plot(x_bounce, H, "o", color=ORANGE, markersize=5, zorder=5)
ax.text(x_bounce + 1, H + 1, "Reflected\nwave", ha="left",
        fontsize=10, fontweight="bold", color=ORANGE)

# 3. Head wave — to a far-offset geophone
x_head = x_geo[-2]
# Downgoing leg
x_down_end = H * np.tan(theta_c)
ax.plot([x_src, x_down_end], [z_src, H], color=VERMILION, lw=2.5)

# Interface segment
x_up_start = x_head - H * np.tan(theta_c)
ax.plot([x_down_end, x_up_start], [H, H], color=VERMILION, lw=2.5)

# Upgoing leg
ax.plot([x_up_start, x_head], [H, z_src], color=VERMILION, lw=2.5)

# Arrow on interface segment
x_arr_mid = (x_down_end + x_up_start) / 2
ax.annotate("", xy=(x_arr_mid + 3, H), xytext=(x_arr_mid - 3, H),
            arrowprops=dict(arrowstyle="->,head_width=0.25,head_length=0.2",
                            color=VERMILION, lw=1.5))

# Label
ax.text(x_up_start - 2, H / 2 + 1, "Head wave", ha="right",
        fontsize=11, fontweight="bold", color=VERMILION)

# Angle arcs
# Downgoing critical angle from vertical
angle_arc = mpatches.Arc((x_src, z_src), 8, 8,
                          angle=0, theta1=90 - np.degrees(theta_c), theta2=90,
                          color=VERMILION, lw=1.2)
ax.add_patch(angle_arc)
ax.text(x_src + 2.5, 3.0, r"$\theta_c$", fontsize=11, color=VERMILION)

# ── Formatting ─────────────────────────────────────────────────────────────────
ax.set_xlim(-5, x_max + 25)
ax.set_ylim(H + 8, -4)  # depth positive downward (surface at top)
ax.set_xlabel("Distance (m)", fontsize=12)
ax.set_ylabel("Depth (m)", fontsize=12)
ax.set_title("Refraction Survey Geometry — Two-Layer Model", fontsize=13,
             fontweight="bold")
ax.set_aspect("equal")

# ── Save ───────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "fig_refraction_survey_geometry.png")
fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved → {out_path}")
