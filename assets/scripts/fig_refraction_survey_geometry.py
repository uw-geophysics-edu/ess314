"""
fig_refraction_survey_geometry.py

Scientific content:
    Two-panel figure for a two-layer refraction survey:
      Panel (a) — Cross-section: source, 4 geophones, layer 1 (V1, H) over
        half-space (V2 > V1).  Three ray paths shown: direct wave (blue),
        reflected wave (orange, dashed), head wave (vermilion).  Each ray
        terminates at a specific labeled geophone.
      Panel (b) — Matching T(x) diagram with the same 4 geophones marked,
        showing direct, reflected, and head-wave travel-time curves.

    Model: V1 = 800 m/s, V2 = 3200 m/s, H = 12 m (UW campus example).

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
    "axes.titlesize": 13,
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
GRAY      = "#999999"

# ── Model ──────────────────────────────────────────────────────────────────────
V1 = 800.0    # m/s — surface layer
V2 = 3200.0   # m/s — bedrock
H  = 12.0     # m — layer thickness

theta_c = np.arcsin(V1 / V2)
t_i     = 2 * H * np.cos(theta_c) / V1
x_cross = 2 * H * np.sqrt((V2 + V1) / (V2 - V1))

# ── 4 geophones: near (direct), mid-near (direct), mid-far (head), far (head)
x_geo = np.array([10.0, 24.0, 45.0, 66.0])
geo_labels = ["G1", "G2", "G3", "G4"]

x_src, z_src = 0.0, 0.0
x_extent = 80.0

# Helper: travel times
def T_direct(x):
    return x / V1

def T_head(x):
    return x / V2 + t_i

def T_refl(x):
    return 2 * np.sqrt(H**2 + (x / 2)**2) / V1

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, (ax_top, ax_bot) = plt.subplots(
    2, 1, figsize=(10, 9), gridspec_kw={"height_ratios": [1, 1], "hspace": 0.30}
)

# ═══════════════════════════════════════════════════════════════════════════════
# PANEL (a): Cross-section
# ═══════════════════════════════════════════════════════════════════════════════
ax = ax_top

# Layers
ax.fill_between([-5, x_extent + 15], 0, H, color="#D2B48C", alpha=0.25)
ax.fill_between([-5, x_extent + 15], H, H + 8, color="#8B7D6B", alpha=0.20)
ax.axhline(H, color=BLACK, lw=1.5, ls="--", alpha=0.6)
ax.axhline(0, color=BLACK, lw=1.5, alpha=0.8)

# Layer labels
ax.text(x_extent + 3, H / 2, f"Layer 1\n$V_1 = {V1:.0f}$ m/s\n$H = {H:.0f}$ m",
        ha="left", va="center", fontsize=11, color=BLACK)
ax.text(x_extent + 3, H + 3.5, f"Layer 2\n$V_2 = {V2:.0f}$ m/s",
        ha="left", va="center", fontsize=11, color=BLACK)

# Source
ax.plot(x_src, z_src, marker="*", color=VERMILION, markersize=18, zorder=5,
        markeredgecolor="k", markeredgewidth=0.5)
ax.text(x_src, -1.8, "Source", ha="center", va="bottom", fontsize=11,
        fontweight="bold", color=VERMILION)

# Geophones
for i, xg in enumerate(x_geo):
    ax.plot(xg, 0, marker="v", color=GREEN, markersize=10, zorder=5,
            markeredgecolor="k", markeredgewidth=0.5)
    ax.text(xg, -1.8, geo_labels[i], ha="center", va="bottom", fontsize=10,
            fontweight="bold", color=GREEN)

# ── Ray 1: Direct wave → G1 (near offset) ──
ax.annotate("", xy=(x_geo[0], 0.5), xytext=(x_src + 0.5, 0.5),
            arrowprops=dict(arrowstyle="->,head_width=0.4,head_length=0.3",
                            color=BLUE, lw=2.5))
ax.text((x_src + x_geo[0]) / 2, 2.0, "Direct wave",
        ha="center", fontsize=11, fontweight="bold", color=BLUE)

# ── Ray 2: Reflected wave → G2 (mid-near offset, dashed) ──
x_bounce = x_geo[1] / 2.0
ax.plot([x_src, x_bounce], [z_src, H], color=ORANGE, lw=2.2, ls="--")
ax.plot([x_bounce, x_geo[1]], [H, z_src], color=ORANGE, lw=2.2, ls="--")
ax.plot(x_bounce, H, "o", color=ORANGE, markersize=5, zorder=5)
ax.text(x_bounce + 2, H - 2, "Reflected wave",
        ha="left", fontsize=11, fontweight="bold", color=ORANGE)

# ── Ray 3: Head wave → G4 (far offset, solid thick) ──
x_down_end = H * np.tan(theta_c)
x_up_start = x_geo[3] - H * np.tan(theta_c)

# Down leg
ax.plot([x_src, x_down_end], [z_src, H], color=VERMILION, lw=2.8, solid_capstyle="round")
# Interface segment
ax.plot([x_down_end, x_up_start], [H, H], color=VERMILION, lw=2.8, solid_capstyle="round")
# Up leg
ax.plot([x_up_start, x_geo[3]], [H, z_src], color=VERMILION, lw=2.8, solid_capstyle="round")

# Arrow on interface
x_mid_iface = (x_down_end + x_up_start) / 2
ax.annotate("", xy=(x_mid_iface + 4, H + 0.05), xytext=(x_mid_iface - 4, H + 0.05),
            arrowprops=dict(arrowstyle="->,head_width=0.3,head_length=0.25",
                            color=VERMILION, lw=1.5))
ax.text((x_down_end + x_up_start) / 2, H / 2,
        "Head wave", ha="center", fontsize=11, fontweight="bold", color=VERMILION)

# θ_c arc on downgoing leg
arc_r = 6
angle_arc = mpatches.Arc((x_src, z_src), arc_r, arc_r,
                          angle=0,
                          theta1=90 - np.degrees(theta_c),
                          theta2=90,
                          color=VERMILION, lw=1.2)
ax.add_patch(angle_arc)
ax.text(x_src + 1.5, 3.5, r"$\theta_c$", fontsize=11, color=VERMILION)

ax.set_xlim(-5, x_extent + 20)
ax.set_ylim(H + 8, -4)
ax.set_xlabel("Distance (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("(a) Refraction survey geometry", fontsize=13, fontweight="bold")

# ═══════════════════════════════════════════════════════════════════════════════
# PANEL (b): T(x) diagram
# ═══════════════════════════════════════════════════════════════════════════════
ax = ax_bot

x_line = np.linspace(0, x_extent, 500)
x_crit = 2 * H * np.tan(theta_c)

# Direct wave (full range)
ax.plot(x_line, T_direct(x_line) * 1e3, color=BLUE, lw=2.5, label="Direct wave ($V_1$)")

# Head wave (only for x >= x_crit)
mask_head = x_line >= x_crit
ax.plot(x_line[mask_head], T_head(x_line[mask_head]) * 1e3,
        color=VERMILION, lw=2.5, label="Head wave ($V_2$)")

# Reflected wave (dashed)
ax.plot(x_line, T_refl(x_line) * 1e3, color=ORANGE, lw=2, ls="--",
        label="Reflected wave")

# Mark the 4 geophones with symbols matching the cross-section
for i, xg in enumerate(x_geo):
    # Determine first arrival
    t_d = T_direct(xg) * 1e3
    t_h = T_head(xg) * 1e3
    t_first = min(t_d, t_h)
    first_color = BLUE if t_d <= t_h else VERMILION
    ax.plot(xg, t_first, "v", color=GREEN, markersize=10,
            markeredgecolor="k", markeredgewidth=0.5, zorder=5)
    ax.text(xg, t_first + 3.5, geo_labels[i], ha="center",
            fontsize=10, fontweight="bold", color=GREEN)

# Crossover vertical
ax.axvline(x_cross, color=GRAY, ls=":", lw=1.2)
ax.text(x_cross + 1, 3, f"$x_{{\\mathrm{{cross}}}}$",
        fontsize=11, color=GRAY, va="bottom")

# Intercept time
ax.plot(0, t_i * 1e3, "o", color=VERMILION, markersize=7, zorder=5)
ax.annotate(f"$t_i = {t_i*1e3:.1f}$ ms",
            xy=(0, t_i * 1e3), xytext=(6, t_i * 1e3 + 5),
            fontsize=10, color=VERMILION, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=VERMILION, lw=1))

ax.set_xlim(0, x_extent)
ax.set_ylim(0, T_direct(x_extent) * 1e3 * 1.05)
ax.set_xlabel("Offset $x$ (m)")
ax.set_ylabel("Travel time $T$ (ms)")
ax.set_title("(b) Travel-time diagram — same 4 geophones", fontsize=13, fontweight="bold")
ax.legend(loc="upper left", framealpha=0.9)
ax.grid(True, alpha=0.3)

# ── Save ───────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "fig_refraction_survey_geometry.png")
fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved → {out_path}")
