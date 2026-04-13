"""
fig_lvz_traveltime.py

Scientific content:
    Demonstration of the Low-Velocity Zone (LVZ) problem in seismic
    refraction. Shows that a layer with V2 < V1 generates no head wave,
    rendering the intermediate layer invisible in the T-x diagram, and
    producing a systematic overestimate of depth to the underlying
    high-velocity refractor.

Reproduces the scientific content of:
    Reynolds, J.M. (2011). An Introduction to Applied and Environmental
    Geophysics, 2nd ed. John Wiley & Sons. Figure 5.x concept.
    (No direct reproduction — original Python generation.)

    Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics,
    3rd ed. Cambridge University Press. §3.4.

Output: assets/figures/fig_lvz_traveltime.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

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

# Colorblind-safe palette
C_LAYER1  = "#56B4E9"   # upper layer (light blue)
C_LVZ     = "#E69F00"   # low-velocity zone (orange)
C_LAYER3  = "#D55E00"   # high-velocity half-space
C_DIRECT  = "#000000"
C_HEAD3   = "#E69F00"   # only head wave V3 visible
C_GHOST   = "#CC79A7"   # "ghost" of what V2 head wave would look like
C_RAY     = "#0072B2"

# ── True model ───────────────────────────────────────────────────────
V1, V2_LVZ, V3 = 1000.0, 500.0, 4000.0   # m/s; V2 < V1 → LVZ
h1, h2         = 5.0, 10.0               # m
x_max          = 140.0

x = np.linspace(0.01, x_max, 2000)

# Critical angle for V3 (using V1, since V2 is transparent to refraction from above)
# The ray effectively sees V1 over V3 for the purpose of the head wave
tic13 = np.arcsin(V1 / V3)

# Apparent two-layer T-x (what is actually observed)
ti_apparent = (2 * (h1 + h2) * np.sqrt(V3**2 - V1**2) / (V3 * V1)) * 1e3
t_dir_obs   = (x / V1) * 1e3
t_head3_obs = (x / V3 + 2 * (h1 + h2) * np.cos(tic13) / V1) * 1e3

# "True" t_head3 accounting for the LVZ transit (what SHOULD be used):
# Ray travels at tic13 in V1 layer, then at critical angle in LVZ (bends away from
# the interface), but still passes through V2 at tic13 relative to V1-V2 boundary.
# Actual transit time correction per meter of LVZ:
# delta_t_LVZ = 2*h2/V2 * (1/cos(theta_at_LVZ) - ?) — complex; use simplified form
# For a low-velocity layer, the extra path cost compared to assuming V1 throughout:
# t_head3_true = x/V3 + 2*h1*sqrt(V3^2-V1^2)/(V3*V1) + 2*h2/V2*(1/cos(theta2_true))
# where sin(theta2_true)=V2/V3 (Snell from V2 to V3)... not a head wave scenario.
# For illustration: show what depth would be INFERRED incorrectly.
h1_inferred = (h1 + h2) * 1.0   # naive interpretation ignores LVZ, gets h_total

# "Ghost" of what V2 segment would look like if V2 > V1
V2_hyp = 1500.0   # hypothetical if layer 2 were faster
tic12_hyp = np.arcsin(V1 / V2_hyp)
t_head2_hyp = (x / V2_hyp + 2 * h1 * np.cos(tic12_hyp) / V1) * 1e3

# ── Figure layout ─────────────────────────────────────────────────────
fig, (ax_cs, ax_tt) = plt.subplots(
    2, 1, figsize=(9, 8.5),
    gridspec_kw={"hspace": 0.60, "height_ratios": [1, 1.3]}
)

# ── Top panel: cross-section ──────────────────────────────────────────
depth_max = h1 + h2 + 10
ax_cs.set_xlim(0, x_max)
ax_cs.set_ylim(depth_max, -2)   # depth positive downward

ax_cs.axhspan(0,     h1,       facecolor=C_LAYER1, alpha=0.4)
ax_cs.axhspan(h1,    h1+h2,    facecolor=C_LVZ,    alpha=0.4)
ax_cs.axhspan(h1+h2, depth_max, facecolor=C_LAYER3, alpha=0.4)

ax_cs.axhline(h1,    color="#444", lw=1.2)
ax_cs.axhline(h1+h2, color="#444", lw=1.2)

# LVZ annotation
ax_cs.text(x_max/2, h1 + h2/2, "LVZ: No head wave generated",
           ha="center", va="center", fontsize=12, color="#8B4513",
           bbox=dict(boxstyle="round,pad=0.4", fc="#FFF3CD", ec=C_LVZ, lw=1.5))

# Velocity labels
labels = [(h1/2, V1, "V_1"), (h1+h2/2, V2_LVZ, "V_2"), (h1+h2+5, V3, "V_3")]
for (d, v, lab) in labels:
    col = C_LVZ if "2" in lab else ("#333")
    ax_cs.text(10, d, f"${lab}$ = {int(v)} m/s", fontsize=11, va="center",
               color=col, fontweight="bold" if "2" in lab else "normal")

# Thickness brackets
for depth, thickness, lab in [(0, h1, "h₁=5 m"), (h1, h2, "h₂=10 m")]:
    ax_cs.annotate("", xy=(x_max*0.88, depth),
                   xytext=(x_max*0.88, depth+thickness),
                   arrowprops=dict(arrowstyle="<->", color="#555", lw=1.2))
    ax_cs.text(x_max*0.90, depth + thickness/2, lab, va="center", fontsize=11, color="#555")

# Show ray going through V2 without critical refraction (bends away from interface)
# Draw a ray incident at critical angle for V3, passing through all three layers
theta1 = tic13   # in layer 1
# Snell's law at V1-V2 interface: sin(theta2)/V2 = sin(theta1)/V1
sin_theta2 = np.sin(theta1) * V2_LVZ / V1
theta2 = np.arcsin(min(sin_theta2, 0.9999))  # refracted downward (V2<V1 → bends further)
sin_theta3_check = np.sin(theta1) * V3 / V1
# Ray path: source at x_src, shoot down through three layers
x_src = x_max * 0.20
x_A = x_src + h1 * np.tan(theta1)         # V1-V2 interface
x_B = x_A  + h2 * np.tan(theta2)          # V2-V3 interface (critical)
# On refractor V3, travels horizontally → no upward ray shown for simplicity
ax_cs.plot([x_src, x_A, x_B], [0, h1, h1+h2],
           color=C_RAY, lw=1.8, ls="-", zorder=5, label="Incident ray")
ax_cs.plot(x_src, 0, "v", ms=8, color="#555", zorder=6)

# Hammer label
ax_cs.text(x_src + 2, -1.2, "Source", fontsize=10, color="#555")

# Arrow indicating "no head wave at V1-V2 interface"
ax_cs.annotate("No critical\nrefraction here", xy=(x_A, h1),
               xytext=(x_A + 25, h1 - 3),
               fontsize=10, color=C_LVZ,
               arrowprops=dict(arrowstyle="->", color=C_LVZ, lw=1.2))

ax_cs.set_xlabel("Offset $x$ (m)")
ax_cs.set_ylabel("Depth (m)")
ax_cs.set_title(f"Cross-section: LVZ ({int(V1)} → {int(V2_LVZ)} → {int(V3)} m/s)", fontweight="bold")

# ── Bottom panel: T-x diagram ─────────────────────────────────────────
t_fa_obs = np.minimum(t_dir_obs, t_head3_obs)

ax_tt.plot(x, t_dir_obs,   color=C_DIRECT, lw=1.5, ls="-",
           label=f"Direct ($1/V_1$ = {int(V1)} m/s)")
ax_tt.plot(x, t_head3_obs, color=C_HEAD3,  lw=1.8, ls="--",
           label=f"Head wave $V_3$ = {int(V3)} m/s (only visible refractor)")
ax_tt.plot(x, t_fa_obs,    color="#009E73", lw=2.8, ls="-",
           label="First arrival (observed)")

# Ghost of what V2 head wave would look like if V2 were 1500 m/s
t_fa_ghost = np.minimum(t_dir_obs, np.minimum(t_head2_hyp, t_head3_obs))
ax_tt.plot(x, t_head2_hyp, color=C_GHOST, lw=1.2, ls=":",
           label=f"Ghost: $V_2$ = {int(V2_hyp)} m/s (hypothetical, not present)",
           alpha=0.6)

# LVZ hidden annotation
ti3 = (2 * (h1 + h2) * np.cos(tic13) / V1) * 1e3
ax_tt.axhline(ti3, color=C_HEAD3, lw=0.7, ls="--", alpha=0.4)
ax_tt.annotate(f"$t_{{i_3}}$ = {ti3:.1f} ms\n(interpreted as 2-layer)", xy=(0, ti3),
               xytext=(8, ti3 + 4), fontsize=10, color=C_HEAD3)

ax_tt.annotate("LVZ hidden:\nno $1/V_2$ segment",
               xy=(x_max*0.45, t_dir_obs[np.argmin(np.abs(x - x_max*0.45))]),
               xytext=(x_max*0.55, t_dir_obs[np.argmin(np.abs(x-x_max*0.45))] - 20),
               fontsize=11, color=C_LVZ, fontweight="bold",
               arrowprops=dict(arrowstyle="->", color=C_LVZ, lw=1.2),
               bbox=dict(boxstyle="round,pad=0.3", fc="#FFF3CD", ec=C_LVZ, alpha=0.9))

ax_tt.set_xlim(0, x_max)
ax_tt.set_ylim(0, np.max(t_dir_obs) * 1.05)
ax_tt.set_xlabel("Offset $x$ (m)")
ax_tt.set_ylabel("Travel time $t$ (ms)")
ax_tt.set_title("$T$–$x$ diagram: only two segments visible — LVZ is hidden", fontweight="bold")
ax_tt.legend(loc="upper left", framealpha=0.9, fontsize=10)

fig.tight_layout()
fig.savefig("assets/figures/fig_lvz_traveltime.png", dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_lvz_traveltime.png")

if __name__ == "__main__":
    plt.show()
