"""
fig_integrated_shot_gather.py

Scientific content:
  A synthetic common-shot gather for a 2-layer-over-halfspace Earth
  model that mimics a real marine Cascadia-style profile. The shot
  gather shows, simultaneously, the three event families that tie
  refraction and reflection seismology together:

    * Direct (water / sediment) wave — the near-surface first arrival
    * Head wave (refraction) — straight-line first arrival beyond the
      critical distance
    * Reflection hyperbolas — from the basement and the Moho

  This is the motivational figure for Lecture 16: the data contain
  both refracted and reflected events, and a unified processing
  framework must explain both. Inspired by record sections shown in
  the CASIE-21 experiment (Cascadia Seismic Imaging Experiment 2021,
  https://casie21.weebly.com/) but generated entirely from simple
  traveltime expressions.

Reproduces the scientific content of:
  Canales et al. (2017). "Seismic structure of the oceanic crust",
  and the general CASIE-21 experiment overview (Carbotte et al.,
  ongoing). Record-section layout follows Lowrie & Fichtner (2020),
  Chapter 3.

Output: assets/figures/fig_integrated_shot_gather.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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

C_BLUE = "#0072B2"; C_ORANGE = "#E69F00"; C_SKY = "#56B4E9"
C_GREEN = "#009E73"; C_VERM = "#D55E00"; C_PINK = "#CC79A7"; C_BLACK = "#000000"

# -- 2-layer-over-halfspace model -----------------------------------
# Layer 1 (water / shallow sediment): v1, h1
# Layer 2 (sediments / oceanic crust): v2, h2 (top of layer 2 is "basement")
# Halfspace: v3 (upper mantle below Moho)
v1 = 1.8      # km/s  (water + soft sediment average)
v2 = 3.5      # km/s  (consolidated sediment / oceanic layer 2)
v3 = 7.5      # km/s  (upper mantle / refractor)

h1 = 2.0      # km  depth to basement
h2 = 6.0      # km  depth to Moho

# Offsets
x = np.linspace(0.01, 24.0, 400)   # km (shot gather offset)

# -- Traveltime expressions -----------------------------------------

# Direct wave through layer 1
t_direct = x / v1

# Reflection from top of layer 2 (basement), sea-surface-shot:
t_refl_bas = np.sqrt(x**2 + (2*h1)**2) / v1

# Head wave along the basement (v2 > v1): refraction
# t_head_bas = x/v2 + 2 h1 cos(theta_c1) / v1, where sin theta_c1 = v1/v2
cos_thc1 = np.sqrt(1 - (v1/v2)**2)
t_head_bas = x / v2 + 2 * h1 * cos_thc1 / v1
# Only valid beyond crossover / critical distance
x_crit_bas = 2 * h1 * np.tan(np.arcsin(v1/v2))

# Reflection from Moho: two-way path
# We approximate with a two-layer RMS: Vrms^2 = (v1^2 t1 + v2^2 t2)/(t1+t2)
# Interval times at zero-offset
t1_0 = h1 / v1
t2_0 = (h2 - h1) / v2
t0_moho = 2 * (t1_0 + t2_0)
vrms_moho = np.sqrt((v1**2 * t1_0 + v2**2 * t2_0) / (t1_0 + t2_0))
t_refl_moho = np.sqrt(t0_moho**2 + (x/vrms_moho)**2)

# Head wave along Moho (refraction through upper mantle)
# Using effective two-layer refraction: t = x/v3 + 2 h1 cos(thc_1)/v1 + 2 (h2-h1) cos(thc_2)/v2
# where thc1,thc2 are critical angles for rays to reach v3
# sin(thc_1)/v1 = 1/v3; sin(thc_2)/v2 = 1/v3
cos_thc1_moho = np.sqrt(1 - (v1/v3)**2)
cos_thc2_moho = np.sqrt(1 - (v2/v3)**2)
ti_moho = 2 * h1 * cos_thc1_moho / v1 + 2 * (h2 - h1) * cos_thc2_moho / v2
t_head_moho = x / v3 + ti_moho
x_crit_moho = 2 * h1 * np.tan(np.arcsin(v1/v3)) + 2 * (h2-h1) * np.tan(np.arcsin(v2/v3))

# -- Figure ----------------------------------------------------------
fig, (axM, axT) = plt.subplots(
    1, 2, figsize=(14, 6.2),
    gridspec_kw={"width_ratios": [0.9, 1.3], "wspace": 0.28}
)

# === LEFT PANEL: Earth model ========================================
axM.axhspan(0, h1, facecolor=C_SKY, alpha=0.25, label=f"Layer 1 (v₁={v1} km/s)")
axM.axhspan(h1, h2, facecolor=C_ORANGE, alpha=0.25, label=f"Layer 2 (v₂={v2} km/s)")
axM.axhspan(h2, 9, facecolor=C_PINK, alpha=0.30, label=f"Halfspace (v₃={v3} km/s)")
# Interfaces
axM.axhline(h1, color=C_BLUE, lw=2.0, label="Basement (reflector)")
axM.axhline(h2, color=C_VERM, lw=2.2, label="Moho")
# Shot & receivers
axM.plot(0, 0, marker="*", markersize=22, color=C_ORANGE,
         markeredgecolor=C_BLACK, zorder=5, label="Shot")
rec_x = np.linspace(1, 23, 12)
axM.plot(rec_x, np.zeros_like(rec_x), marker="v", markersize=10, color=C_BLACK,
         ls="none", zorder=5, label="Receivers")

# Sketch a reflection path to basement + head wave sketch
# Reflection to basement at one receiver
xr = 12
axM.plot([0, xr/2, xr], [0, h1, 0], color=C_BLUE, lw=1.2, alpha=0.6)
# Head wave along basement
x_in = h1 * np.tan(np.arcsin(v1/v2))
axM.plot([0, x_in, xr - x_in, xr], [0, h1, h1, 0], color=C_GREEN, lw=1.2,
         alpha=0.7)
axM.text(xr/2, h1 + 0.3, "head wave\nalong basement", fontsize=9,
         ha="center", color=C_GREEN, style="italic")
axM.text(xr/2 - 1.2, h1/2 - 0.1, "reflection", fontsize=9, color=C_BLUE,
         style="italic", rotation=28)

axM.set_xlim(-0.5, 24)
axM.set_ylim(9, -0.8)
axM.set_xlabel("x, offset (km)")
axM.set_ylabel("z, depth (km)")
axM.set_title("Earth model: 2 layers over halfspace\n(Cascadia-style marine profile)")
axM.grid(alpha=0.25)
axM.legend(loc="lower right", fontsize=9, framealpha=0.96)

# === RIGHT PANEL: Record section ====================================
# Plot travel-time curves
axT.plot(x, t_direct, color=C_BLACK, lw=2.0, linestyle="--", label="Direct wave")
mask_head_bas = x > x_crit_bas
axT.plot(x[mask_head_bas], t_head_bas[mask_head_bas], color=C_GREEN, lw=2.6,
         label=f"Head wave on basement (v₂ = {v2} km/s)")
axT.plot(x, t_refl_bas, color=C_BLUE, lw=2.2,
         label=f"Reflection from basement (t₀ = {2*h1/v1:.2f} s)")
axT.plot(x, t_refl_moho, color=C_VERM, lw=2.2,
         label=f"Reflection from Moho (t₀ = {t0_moho:.2f} s)")
mask_head_moho = x > x_crit_moho
axT.plot(x[mask_head_moho], t_head_moho[mask_head_moho], color=C_PINK, lw=2.6,
         label=f"Head wave below Moho (v₃ = {v3} km/s)")

# Crossover distances as vertical dotted guides
axT.axvline(x_crit_bas, color=C_GREEN, lw=0.8, linestyle=":", alpha=0.6)
axT.text(x_crit_bas + 0.1, 0.35, f"x_crit\n(basement)\n={x_crit_bas:.2f} km",
         fontsize=9, color=C_GREEN)

# Annotations
axT.text(19, 0.9, "refractions dominate\n(straight lines)",
         fontsize=10, color=C_GREEN, ha="center",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                   edgecolor=C_GREEN, alpha=0.85))
axT.text(8, 5.2, "reflections\n(hyperbolas)",
         fontsize=10, color=C_BLUE, ha="center",
         bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                   edgecolor=C_BLUE, alpha=0.85))

axT.set_xlim(0, 24)
axT.set_ylim(8.0, 0)
axT.set_xlabel("x, source–receiver offset (km)")
axT.set_ylabel("t, two-way travel time (s)")
axT.set_title("Record section: refractions AND reflections on one shot")
axT.grid(alpha=0.3)
axT.legend(loc="upper right", fontsize=9.5, framealpha=0.95)

fig.suptitle("One shot, two methods: the unifying observation",
             fontsize=15, y=1.01, fontweight="bold")
fig.tight_layout()
fig.savefig("/tmp/lec16/assets/figures/fig_integrated_shot_gather.png",
            bbox_inches="tight", dpi=300)
plt.close(fig)
print("Saved fig_integrated_shot_gather.png")
