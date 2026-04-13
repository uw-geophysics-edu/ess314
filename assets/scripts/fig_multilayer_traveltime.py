"""
fig_multilayer_traveltime.py

Scientific content:
    Travel-time vs. offset ($T$-$x$) diagram and cross-section for a
    three-layer horizontal Earth model, illustrating the generalized
    multi-layer refraction travel-time equation.

Reproduces the scientific content of:
    Sheriff, R.E. & Geldart, L.P. (1995). Exploration Seismology,
    2nd ed. Cambridge University Press. Figure 4.1 (concept).
    (No direct reproduction — original Python generation.)

    Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics,
    3rd ed. Cambridge University Press. Ch. 3.

Output: assets/figures/fig_multilayer_traveltime.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Global rcParams (MANDATORY) ──────────────────────────────────────
mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# Colorblind-safe palette (WCAG AA)
C_DIRECT  = "#000000"   # direct wave
C_HEAD1   = "#0072B2"   # head wave from V2
C_HEAD2   = "#E69F00"   # head wave from V3
C_LAYER1  = "#56B4E9"   # top layer fill
C_LAYER2  = "#E69F00"   # middle layer fill (alpha)
C_LAYER3  = "#D55E00"   # bottom layer fill (alpha)
C_RAY     = "#0072B2"   # ray path
C_SHADOW  = "#AAAAAA"   # shadow zone

# ── Model parameters ─────────────────────────────────────────────────
V1, V2, V3 = 500.0, 1800.0, 4200.0   # m/s
h1, h2     = 8.0, 20.0               # m
x_max      = 180.0                   # m
x          = np.linspace(0.01, x_max, 2000)

# Critical angles
tic12 = np.arcsin(V1 / V2)
tic13 = np.arcsin(V1 / V3)
tic23 = np.arcsin(V2 / V3)

# Travel times (s → ms)
t_dir = (x / V1) * 1e3

t_head2 = (x / V2 + 2 * h1 * np.cos(tic12) / V1) * 1e3

t_head3 = (x / V3
           + 2 * h1 * np.sqrt(V3**2 - V1**2) / (V3 * V1)
           + 2 * h2 * np.sqrt(V3**2 - V2**2) / (V3 * V2)) * 1e3

# Intercept times (ms)
ti2 = (2 * h1 * np.cos(tic12) / V1) * 1e3
ti3 = (2 * h1 * np.sqrt(V3**2 - V1**2) / (V3 * V1)
       + 2 * h2 * np.sqrt(V3**2 - V2**2) / (V3 * V2)) * 1e3

# First arrivals
t_fa = np.minimum(t_dir, np.minimum(t_head2, t_head3))

# Crossover distances (approx)
xc12 = 2 * h1 * np.sqrt((V2 + V1) / (V2 - V1))
xc13 = 2 * (h1 + h2) * np.sqrt((V3 + V1) / (V3 - V1))  # approx

# ── Figure layout ─────────────────────────────────────────────────────
fig, (ax_tt, ax_cs) = plt.subplots(
    2, 1, figsize=(9, 8),
    gridspec_kw={"hspace": 0.55, "height_ratios": [1.3, 1]}
)

# ── Top panel: T-x diagram ────────────────────────────────────────────
# Shadow zone shading for head waves
mask_shadow2 = x < xc12
mask_shadow3 = x < xc13

ax_tt.fill_between(x, 0, t_head2, where=mask_shadow2,
                   color=C_SHADOW, alpha=0.18, label="_nolegend_")
ax_tt.fill_between(x, 0, t_head3, where=mask_shadow3,
                   color=C_SHADOW, alpha=0.10, label="_nolegend_")

# Full model lines (dashed, extrapolated)
ax_tt.plot(x, t_dir,   color=C_DIRECT, lw=1.4, ls="-",  label=f"Direct ($1/V_1$, {int(V1)} m/s)")
ax_tt.plot(x, t_head2, color=C_HEAD1,  lw=1.6, ls="--", label=f"Head wave $V_2$ = {int(V2)} m/s")
ax_tt.plot(x, t_head3, color=C_HEAD2,  lw=1.6, ls=":",  label=f"Head wave $V_3$ = {int(V3)} m/s")

# First-arrival envelope (bold)
ax_tt.plot(x, t_fa, color="#009E73", lw=2.8, ls="-", label="First arrival")

# Intercept time markers
ax_tt.axhline(ti2, color=C_HEAD1, lw=0.7, ls="--", alpha=0.5)
ax_tt.axhline(ti3, color=C_HEAD2, lw=0.7, ls=":",  alpha=0.5)
ax_tt.annotate(f"$t_{{i_2}}$ = {ti2:.1f} ms", xy=(0, ti2),
               xytext=(5, ti2 + 3), fontsize=11, color=C_HEAD1)
ax_tt.annotate(f"$t_{{i_3}}$ = {ti3:.1f} ms", xy=(0, ti3),
               xytext=(5, ti3 + 3), fontsize=11, color=C_HEAD2)

# Crossover markers
ax_tt.axvline(xc12, color=C_HEAD1, lw=0.7, ls="--", alpha=0.5)
ax_tt.axvline(xc13, color=C_HEAD2, lw=0.7, ls=":",  alpha=0.5)
ax_tt.annotate(f"$x_{{c,1}}$\n{xc12:.0f} m", xy=(xc12, ax_tt.get_ylim()[0] if ax_tt.get_ylim()[0] > 0 else 2),
               xytext=(xc12 + 3, 8), fontsize=10, color=C_HEAD1)

ax_tt.set_xlim(0, x_max)
ax_tt.set_ylim(0, np.max(t_dir) * 1.05)
ax_tt.set_xlabel("Offset $x$ (m)")
ax_tt.set_ylabel("Travel time $t$ (ms)")
ax_tt.set_title("$T$–$x$ diagram: three-layer horizontal model", fontweight="bold")
ax_tt.legend(loc="upper left", framealpha=0.9)

# ── Bottom panel: cross-section ────────────────────────────────────────
# Layer rectangles
depth_max = h1 + h2 + 15
ax_cs.set_xlim(0, x_max)
ax_cs.set_ylim(depth_max, -3)      # depth positive downward

ax_cs.axhspan(-3, 0,          alpha=0.0)                         # surface
ax_cs.axhspan(0,  h1,         facecolor=C_LAYER1, alpha=0.35)    # layer 1
ax_cs.axhspan(h1, h1+h2,      facecolor=C_LAYER2, alpha=0.35)    # layer 2
ax_cs.axhspan(h1+h2, depth_max, facecolor=C_LAYER3, alpha=0.35)  # layer 3

# Interface lines
ax_cs.axhline(h1,    color="#333", lw=1.2, ls="-")
ax_cs.axhline(h1+h2, color="#333", lw=1.2, ls="-")

# Velocity labels
for depth_mid, vel, idx in [(h1/2, V1, 1), (h1+h2/2, V2, 2), (h1+h2+7, V3, 3)]:
    ax_cs.text(x_max * 0.78, depth_mid, f"$V_{idx}$ = {int(vel)} m/s",
               ha="center", va="center", fontsize=11,
               bbox=dict(boxstyle="round,pad=0.3", fc="white", alpha=0.8, ec="none"))

# Thickness labels
for ypos, lab in [(h1/2, f"$h_1$ = {h1:.0f} m"), (h1 + h2/2, f"$h_2$ = {h2:.0f} m")]:
    ax_cs.annotate("", xy=(5, ypos - (h1/2 if ypos == h1/2 else h2/2) + (h1 if ypos != h1/2 else 0)),
                   xytext=(5, ypos + (h1/2 if ypos == h1/2 else h2/2) - (h1 if ypos != h1/2 else 0)))
    ax_cs.text(12, ypos, lab, ha="left", va="center", fontsize=11, color="#333")

# Example ray path E→A→B→C→D→F (head wave V3)
# Source E at x=0, surface. Ray goes down at critical angle to interface h1+h2
# then horizontal, then back up.
x_src = 0.0
x_rec = x_max * 0.90
# Down-going critical angle in layer 1 relative to V3 interface
theta1_to_3 = tic13            # angle in layer 1 for refraction to V3
# Ray bends at h1 interface according to Snell's law
# sin(theta_in_V2) = V2/V3 * sin(90deg) → theta_in_V2 = tic23
theta2_to_3 = tic23

# Down-going horizontal positions
x_A = x_src + h1 * np.tan(theta1_to_3)
x_B = x_A + h2 * np.tan(theta2_to_3)
# Up-going (symmetric)
x_D = x_rec - h1 * np.tan(theta1_to_3)
x_C = x_D - h2 * np.tan(theta2_to_3)

ray_x = [x_src, x_A, x_B, x_C, x_D, x_rec]
ray_y = [0,     h1,  h1+h2, h1+h2, h1,   0]

ax_cs.plot(ray_x, ray_y, color=C_RAY, lw=1.8, zorder=5)
# Arrow at midpoint
mid = len(ray_x) // 2
ax_cs.annotate("", xy=(ray_x[mid+1], ray_y[mid+1]),
               xytext=(ray_x[mid], ray_y[mid]),
               arrowprops=dict(arrowstyle="->", color=C_RAY, lw=1.5))

# Label points
for pt, name in zip(zip(ray_x, ray_y), list("EABCDF")):
    offset_x = -6 if name in ("E",) else (4 if name in ("F",) else 0)
    offset_y = -2 if name in ("E", "F") else 2
    ax_cs.text(pt[0] + offset_x, pt[1] + offset_y, name,
               fontsize=11, fontweight="bold", color=C_RAY, ha="center")

# Source and receiver markers
ax_cs.plot([x_src, x_rec], [0, 0], "v", ms=8, color=C_DIRECT, zorder=6)

ax_cs.set_xlabel("Offset $x$ (m)")
ax_cs.set_ylabel("Depth (m)")
ax_cs.set_title("Cross-section with head-wave ray path $EABCDF$", fontweight="bold")

fig.tight_layout()
fig.savefig("assets/figures/fig_multilayer_traveltime.png", dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_multilayer_traveltime.png")


if __name__ == "__main__":
    plt.show()
