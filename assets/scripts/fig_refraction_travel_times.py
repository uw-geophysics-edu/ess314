"""
fig_refraction_travel_times.py

Scientific content:
    Travel-time (T-x) diagram for a two-layer refraction model showing:
      - Direct wave: straight line through origin, slope 1/V1 (blue)
      - Head wave: straight line with slope 1/V2, intercept t_i (green)
      - Reflected wave: hyperbola (orange, dashed)
      - Critical distance x_crit and crossover distance x_cross marked
      - Bold first-arrival envelope

    Model: V1 = 800 m/s, V2 = 3200 m/s, H = 12 m (UW campus example).

Output: assets/figures/fig_refraction_travel_times.png
License: CC-BY 4.0
Author:  ESS 314 course, University of Washington, 2026
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
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
V1 = 800.0    # m/s
V2 = 3200.0   # m/s
H  = 12.0     # m

theta_c = np.arcsin(V1 / V2)

# Derived quantities
t_i     = 2 * H * np.cos(theta_c) / V1
x_crit  = 2 * H * np.tan(theta_c)
x_cross = 2 * H * np.sqrt((V2 + V1) / (V2 - V1))

# ── Offsets ────────────────────────────────────────────────────────────────────
x = np.linspace(0, 80, 500)

# Travel times
T_direct = x / V1
T_head   = x / V2 + t_i
T_refl   = 2 * np.sqrt(H**2 + (x / 2)**2) / V1  # reflection hyperbola

# Head wave only exists for x >= x_crit
T_head_valid = np.where(x >= x_crit, T_head, np.nan)

# First arrival envelope
T_first = np.where(x <= x_cross, T_direct, T_head)

# ── Figure ─────────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(9, 6))

# First-arrival envelope (bold background)
ax.plot(x, T_first * 1e3, color=BLACK, lw=4, alpha=0.15, zorder=1)

# Direct wave
ax.plot(x, T_direct * 1e3, color=BLUE, lw=2.5, label="Direct wave ($V_1$)",
        zorder=3)

# Head wave (only where it exists)
ax.plot(x, T_head_valid * 1e3, color=GREEN, lw=2.5,
        label="Head wave ($V_2$)", zorder=3)

# Reflected wave (dashed)
ax.plot(x, T_refl * 1e3, color=ORANGE, lw=2, ls="--",
        label="Reflected wave", zorder=2)

# ── Annotations ────────────────────────────────────────────────────────────────

# Intercept time
ax.plot(0, t_i * 1e3, "o", color=GREEN, markersize=8, zorder=5)
ax.annotate(f"$t_i = {t_i*1e3:.1f}$ ms",
            xy=(0, t_i * 1e3), xytext=(5, t_i * 1e3 + 4),
            fontsize=11, color=GREEN, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.2))

# Crossover distance
ax.axvline(x_cross, color=BLACK, ls=":", lw=1.2, alpha=0.5)
ax.text(x_cross + 0.5, 2, f"$x_{{\\mathrm{{cross}}}} = {x_cross:.1f}$ m",
        fontsize=10, color=BLACK, rotation=90, va="bottom")

# Critical distance
ax.axvline(x_crit, color=VERMILION, ls=":", lw=1.2, alpha=0.5)
ax.text(x_crit + 0.5, 2, f"$x_{{\\mathrm{{crit}}}} = {x_crit:.1f}$ m",
        fontsize=10, color=VERMILION, rotation=90, va="bottom")

# Slope annotations
x_slope1 = 20
ax.annotate(f"slope $= 1/V_1$",
            xy=(x_slope1, x_slope1 / V1 * 1e3),
            xytext=(x_slope1 + 10, x_slope1 / V1 * 1e3 + 8),
            fontsize=10, color=BLUE,
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1))

x_slope2 = 60
ax.annotate(f"slope $= 1/V_2$",
            xy=(x_slope2, (x_slope2 / V2 + t_i) * 1e3),
            xytext=(x_slope2 - 15, (x_slope2 / V2 + t_i) * 1e3 + 8),
            fontsize=10, color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1))

# ── Formatting ─────────────────────────────────────────────────────────────────
ax.set_xlabel("Offset $x$ (m)", fontsize=12)
ax.set_ylabel("Travel time $T$ (ms)", fontsize=12)
ax.set_title("Travel-Time Curves — Two-Layer Refraction Model", fontsize=13,
             fontweight="bold")
ax.set_xlim(0, 80)
ax.set_ylim(0, T_direct[-1] * 1e3 * 1.05)
ax.legend(loc="upper left", framealpha=0.9)
ax.grid(True, alpha=0.3)

# Model parameters box
info = (f"$V_1 = {V1:.0f}$ m/s\n$V_2 = {V2:.0f}$ m/s\n$H = {H:.0f}$ m\n"
        f"$\\theta_c = {np.degrees(theta_c):.1f}°$")
ax.text(0.98, 0.98, info, transform=ax.transAxes, fontsize=10,
        va="top", ha="right",
        bbox=dict(facecolor="white", edgecolor="gray", alpha=0.9, pad=5))

fig.tight_layout()

# ── Save ───────────────────────────────────────────────────────────────────
out_dir = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "fig_refraction_travel_times.png")
fig.savefig(out_path, dpi=200, bbox_inches="tight", facecolor="white")
plt.close(fig)
print(f"Saved → {out_path}")
