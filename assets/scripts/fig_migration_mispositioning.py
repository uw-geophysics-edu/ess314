"""
fig_migration_mispositioning.py

Scientific content:
  Two-panel figure showing why zero-offset sections misplace dipping
  reflectors. Left panel: earth cross-section with a dipping reflector,
  a source/receiver pair at the surface, the normal ray of length d
  from S to the true reflection point R, and the apparent position C
  at slant depth d beneath S. Right panel: the zero-offset time section
  showing where the reflection event is plotted versus where migration
  moves it.

  KEY PEDAGOGICAL POINT: In zero-offset recording the wave travels
  perpendicular to the reflector (the shortest path to and from the
  interface). The instrument records only the round-trip time — it does
  NOT know the ray direction. The conventional display assumes the ray
  went straight down, so it plots the reflector directly beneath S at
  depth d. The true reflection point R is actually updip and shallower.

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
y_src = 1.5          # source–receiver pair at surface position S
d = 1.2              # length of the normal ray S → R

# True reflection point R
R_x = y_src + d * np.sin(theta)   # 2.10 km
R_z = d * np.cos(theta)            # 1.04 km
# Apparent (wrong) position C  —  directly beneath S at slant depth d
C_x = y_src
C_z = d
# Event time on the zero-offset section
t_event_ms = 2.0 * d / v * 1000   # 1200 ms
tau_event_ms = 2.0 * R_z / v * 1000  # 1039 ms

fig = plt.figure(figsize=(14, 8.0))
# Use gridspec: main plots on top, shared legend strip on bottom
gs = fig.add_gridspec(2, 2, height_ratios=[5.6, 1.4],
                      width_ratios=[1.1, 1.0], hspace=0.08, wspace=0.30)
axE = fig.add_subplot(gs[0, 0])   # left: earth cross-section
axT = fig.add_subplot(gs[0, 1])   # right: time section
ax_legL = fig.add_subplot(gs[1, 0])  # legend area left
ax_legR = fig.add_subplot(gs[1, 1])  # legend area right
ax_legL.axis("off")
ax_legR.axis("off")

# === LEFT PANEL: Earth cross-section ================================
# Surface line
x_surf = np.linspace(0, 3.5, 200)
axE.plot(x_surf, np.zeros_like(x_surf), color=C_BLACK, lw=1.2)

# Dipping reflector
s = np.linspace(-1.0, 1.8, 200)
refl_x = R_x + s * np.cos(theta)
refl_z = R_z + s * np.sin(theta)
h_refl, = axE.plot(refl_x, refl_z, color=C_BLUE, lw=2.8,
                    label="Dipping reflector")

# ------------------------------------------------------------------
# The ACTUAL ray path (vermilion):  S → R, perpendicular to reflector.
# At zero offset the reflection obeys the law of reflection; the only
# ray that returns to the same surface point is the one that hits the
# interface at a right angle — the "normal ray".
# ------------------------------------------------------------------
h_ray, = axE.plot([y_src, R_x], [0, R_z], color=C_VERM, lw=2.4,
                   label="Actual ray path S → R\n(⊥ to reflector, length $d$)")

# Small square at R showing perpendicularity to reflector
sq = 0.08
refl_u = np.array([np.cos(theta), np.sin(theta)])   # along reflector
norm_u = np.array([-np.sin(theta), np.cos(theta)])   # outward normal (upward)
sq_pts = np.array([
    [R_x, R_z],
    [R_x + sq*refl_u[0], R_z + sq*refl_u[1]],
    [R_x + sq*refl_u[0] + sq*norm_u[0],
     R_z + sq*refl_u[1] + sq*norm_u[1]],
    [R_x + sq*norm_u[0], R_z + sq*norm_u[1]],
])
axE.plot(sq_pts[[0,1,2,3,0], 0], sq_pts[[0,1,2,3,0], 1],
         color=C_VERM, lw=1.0)

# ------------------------------------------------------------------
# The ASSUMED ray path (pink dashed): straight down from S to depth d.
# The instrument records only the round-trip time; the conventional
# display assumes the ray went vertically.
# ------------------------------------------------------------------
h_assumed, = axE.plot([y_src, y_src], [0, d], color=C_PINK, lw=2.0,
                       linestyle=":",
                       label="Assumed vertical path\n→ wrong depth $d$ beneath S")

# Annotation explaining the wrong assumption
axE.annotate(
    "Recorder knows only\n$t = 2d/v$; assumes\nray went straight down",
    xy=(y_src, d*0.48), xytext=(0.12, 0.55),
    fontsize=9.0, color=C_PINK, fontstyle="italic",
    arrowprops=dict(arrowstyle="->", color=C_PINK, lw=1.0),
)

# Source/receiver symbol
h_src = axE.plot(y_src, 0, marker="v", markersize=16, color=C_ORANGE,
                  markeredgecolor=C_BLACK, zorder=6,
                  label="Source = receiver (S)")[0]
# Apparent position C
h_Cpt = axE.plot(C_x, C_z, marker="o", markersize=13, color=C_PINK,
                  markeredgecolor=C_BLACK, zorder=6,
                  label=f"Apparent position C\n  ({C_x:.1f} km, {C_z:.2f} km depth)")[0]
# True reflection point R
h_Rpt = axE.plot(R_x, R_z, marker="*", markersize=20, color=C_VERM,
                  markeredgecolor=C_BLACK, zorder=6,
                  label=f"True reflection point R\n  ({R_x:.2f} km, {R_z:.2f} km depth)")[0]

# Dip angle arc and label
arc_r = 0.22
arc_th = np.linspace(0, theta, 40)
axE.plot(R_x - arc_r*np.cos(arc_th), R_z + arc_r*np.sin(arc_th),
         color=C_BLACK, lw=1.0)
axE.text(R_x - 0.50, R_z + 0.10,
         rf"$\theta = {theta_deg:.0f}°$", fontsize=12)

# Label d on the actual ray
mid_ray_x = (y_src + R_x) / 2 + 0.06
mid_ray_z = (0 + R_z) / 2 - 0.06
axE.text(mid_ray_x, mid_ray_z, r"$d$",
         fontsize=15, color=C_VERM, fontweight="bold")

# Δx annotation at top
axE.annotate("", xy=(R_x, -0.06), xytext=(y_src, -0.06),
             arrowprops=dict(arrowstyle="<->", color=C_BLACK, lw=1.2))
axE.text((y_src + R_x) / 2, -0.17, r"$\Delta x = d\,\sin\theta$",
         fontsize=11, ha="center")

axE.set_xlim(0.0, 3.5)
axE.set_ylim(1.8, -0.35)
axE.set_xlabel("x (km)")
axE.set_ylabel("z, depth (km)")
axE.set_title("Earth: true vs. apparent reflection point")
axE.set_aspect("equal")
axE.grid(alpha=0.25)

# Legend below the left panel  — NO in-plot legend
handles_L = [h_refl, h_ray, h_assumed, h_src, h_Rpt, h_Cpt]
ax_legL.legend(handles=handles_L, loc="upper center", ncol=2,
               fontsize=9.5, framealpha=0.95, columnspacing=1.5)

# === RIGHT PANEL: Zero-offset time section ==========================
y_range = np.linspace(0, 3.5, 200)
p0_ms_per_km = 2.0 * np.sin(theta) / v * 1000  # slope ms/km
t_line_ms = t_event_ms + p0_ms_per_km * (y_range - y_src)
mask = (t_line_ms >= 0) & (t_line_ms <= 2000)
h_event, = axT.plot(y_range[mask], t_line_ms[mask], color=C_BLUE, lw=2.4,
                     label="Reflection event on\nunmigrated section")

h_plotted = axT.plot(y_src, t_event_ms, marker="o", markersize=13,
                      color=C_PINK, markeredgecolor=C_BLACK, zorder=5,
                      label=f"Plotted at ($y$ = {y_src:.1f} km, "
                            f"$t$ = {t_event_ms:.0f} ms)")[0]

h_migrated = axT.plot(R_x, tau_event_ms, marker="*", markersize=20,
                       color=C_VERM, markeredgecolor=C_BLACK, zorder=5,
                       label=f"Migrated to ($x$ = {R_x:.2f} km, "
                             f"$\\tau$ = {tau_event_ms:.0f} ms)")[0]

# Migration shift arrow
axT.annotate("", xy=(R_x, tau_event_ms), xytext=(y_src, t_event_ms),
             arrowprops=dict(arrowstyle="->", color=C_BLACK, lw=1.8,
                             connectionstyle="arc3,rad=-0.20"))
axT.text((y_src + R_x) / 2 + 0.08, (t_event_ms + tau_event_ms) / 2 + 70,
         "migration\nshift", fontsize=11, ha="center")

# Equation box
axT.text(0.15, 300, r"$\tau = t\cos\theta$", fontsize=12,
         color=C_VERM, fontstyle="italic",
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_VERM, alpha=0.85))

axT.set_xlim(0.0, 3.5)
axT.set_ylim(2000, 0)
axT.set_xlabel("y, midpoint (km)")
axT.set_ylabel("t, two-way time (ms)")
axT.set_title("Zero-offset section: apparent event position")
axT.grid(alpha=0.25)

# Legend below the right panel — NO in-plot legend
handles_R = [h_event, h_plotted, h_migrated]
ax_legR.legend(handles=handles_R, loc="upper center", ncol=1,
               fontsize=9.5, framealpha=0.95, columnspacing=1.5)

fig.savefig("assets/figures/fig_migration_mispositioning.png",
            bbox_inches="tight", dpi=300)
plt.close(fig)
print("Saved fig_migration_mispositioning.png")
