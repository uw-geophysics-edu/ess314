"""
fig_migration_mispositioning.py

Scientific content:
  Two-panel figure showing why zero-offset sections misplace dipping
  reflectors. Left panel: earth cross-section with a dipping reflector,
  a source/receiver pair at the surface, the normal ray of length d
  from S to the true reflection point R, and the apparent position C
  at slant depth d beneath S. Right panel: the zero-offset time section
  showing where the reflection event is plotted versus where migration
  moves it. Illustrates Claerbout (2010), Chapter 5, Section 5.1.1.

Reproduces the scientific content of:
  Claerbout, J. F. (2010). Basic Earth Imaging. Stanford Exploration
  Project. Open-access: http://sepwww.stanford.edu/sep/prof/bei11.2010.pdf
  (Chapter 5, Figures 5.1 and 5.2).

Output: assets/figures/fig_migration_mispositioning.png
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
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

C_BLUE = "#0072B2"; C_ORANGE = "#E69F00"; C_SKY = "#56B4E9"
C_GREEN = "#009E73"; C_VERM = "#D55E00"; C_PINK = "#CC79A7"; C_BLACK = "#000000"

# -- Geometry (distances km, velocity km/s) --------------------------
v = 2.0
theta_deg = 30.0
theta = np.deg2rad(theta_deg)
y_src = 1.5
d = 1.2

R_x = y_src + d * np.sin(theta)
R_z = d * np.cos(theta)
C_x = y_src
C_z = d
t_event_ms = 2.0 * d / v * 1000

fig, (axE, axT) = plt.subplots(
    1, 2, figsize=(13, 5.6),
    gridspec_kw={"width_ratios": [1.1, 1.0], "wspace": 0.30}
)

# === LEFT PANEL =====================================================
x_surf = np.linspace(0, 3.5, 200)
axE.plot(x_surf, np.zeros_like(x_surf), color=C_BLACK, lw=1.2)

s = np.linspace(-1.0, 1.8, 200)
refl_x = R_x + s * np.cos(theta)
refl_z = R_z + s * np.sin(theta)
axE.plot(refl_x, refl_z, color=C_BLUE, lw=2.8, label="Dipping reflector")

axE.plot([y_src, R_x], [0, R_z], color=C_VERM, lw=2.4,
         label="Normal ray, length d")
axE.plot([y_src, y_src], [0, d], color=C_PINK, lw=2.0, linestyle=":",
         label="Apparent depth = d")

axE.plot(y_src, 0, marker="v", markersize=16, color=C_ORANGE,
         markeredgecolor=C_BLACK, zorder=6, label="Source = receiver (S)")
axE.plot(C_x, C_z, marker="o", markersize=13, color=C_PINK,
         markeredgecolor=C_BLACK, zorder=6, label="Apparent point C")
axE.plot(R_x, R_z, marker="*", markersize=20, color=C_VERM,
         markeredgecolor=C_BLACK, zorder=6, label="True point R")

arc_r = 0.22
arc_th = np.linspace(0, theta, 40)
axE.plot(R_x - arc_r*np.cos(arc_th), R_z + arc_r*np.sin(arc_th),
         color=C_BLACK, lw=1.0)
axE.text(R_x - 0.42, R_z + 0.08,
         rf"$\theta={theta_deg:.0f}^\circ$", fontsize=12)

axE.text((y_src+R_x)/2 + 0.04, (0+R_z)/2 - 0.04, "d",
         fontsize=14, color=C_VERM, fontweight="bold")
axE.text(y_src + 0.03, d*0.55, "d", fontsize=12, color=C_PINK)

axE.annotate("", xy=(R_x, -0.06), xytext=(y_src, -0.06),
             arrowprops=dict(arrowstyle="<->", color=C_BLACK, lw=1.2))
axE.text((y_src+R_x)/2, -0.17, r"$\Delta x = d \sin\theta$",
         fontsize=11, ha="center")

axE.set_xlim(0.0, 3.5)
axE.set_ylim(1.8, -0.35)
axE.set_xlabel("x (km)")
axE.set_ylabel("z, depth (km)")
axE.set_title("Earth: true vs. apparent reflection point")
axE.set_aspect("equal")
axE.grid(alpha=0.25)
axE.legend(loc="lower right", fontsize=9.5, framealpha=0.95)

# === RIGHT PANEL ====================================================
y_range = np.linspace(0, 3.5, 200)
p0_ms_per_km = 2.0 * np.sin(theta) / v * 1000
t_line_ms = t_event_ms + p0_ms_per_km * (y_range - y_src)
mask = (t_line_ms >= 0) & (t_line_ms <= 2000)
axT.plot(y_range[mask], t_line_ms[mask], color=C_BLUE, lw=2.4,
         label="Event on unmigrated section")

axT.plot(y_src, t_event_ms, marker="o", markersize=13, color=C_PINK,
         markeredgecolor=C_BLACK, zorder=5,
         label=f"Plotted at (y={y_src:.1f} km,\n  t={t_event_ms:.0f} ms)")

tau_event_ms = 2.0 * R_z / v * 1000
axT.plot(R_x, tau_event_ms, marker="*", markersize=20, color=C_VERM,
         markeredgecolor=C_BLACK, zorder=5,
         label=f"Migrated to (x={R_x:.2f} km,\n  τ={tau_event_ms:.0f} ms)")

axT.annotate("", xy=(R_x, tau_event_ms), xytext=(y_src, t_event_ms),
             arrowprops=dict(arrowstyle="->", color=C_BLACK, lw=1.8,
                             connectionstyle="arc3,rad=-0.20"))
axT.text((y_src+R_x)/2 + 0.05, (t_event_ms+tau_event_ms)/2 + 60,
         "migration\nshift", fontsize=11, ha="center")

axT.set_xlim(0.0, 3.5)
axT.set_ylim(2000, 0)
axT.set_xlabel("y, midpoint (km)")
axT.set_ylabel("t, two-way time (ms)")
axT.set_title("Zero-offset section: apparent event position")
axT.grid(alpha=0.25)
axT.legend(loc="lower left", fontsize=9.5, framealpha=0.95)

fig.tight_layout()
fig.savefig("/tmp/lec16/assets/figures/fig_migration_mispositioning.png",
            bbox_inches="tight", dpi=300)
plt.close(fig)
print("Saved fig_migration_mispositioning.png")
