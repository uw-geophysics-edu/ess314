"""
Reflection survey acquisition geometry and travel-time hyperbola.
Panel A: cross-section showing source, receivers, flat reflector, two-way ray paths.
Panel B: t-x hyperbola with asymptote, marking the same receiver offsets.
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Colorblind-safe palette (Wong 2011)
BLUE   = "#0072B2"
ORANGE = "#E69F00"
RED    = "#D55E00"
LBLUE  = "#56B4E9"

h  = 500    # reflector depth (m)
V1 = 2000   # velocity (m/s)
src_x = 0   # source at origin
offsets = [500, 1000, 1500, 2000]   # receiver offsets (m)
rec_cols = [plt.cm.Blues(v) for v in [0.40, 0.55, 0.72, 0.90]]

fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
fig.subplots_adjust(wspace=0.38)

# ── Panel A: geometry ─────────────────────────────────────────────────────────
ax = axes[0]
ax.fill_between([-100, 2600], [0, 0], [h, h],    color="#DEEFF9", zorder=0)
ax.fill_between([-100, 2600], [h, h], [750, 750], color="#FFE4CC", zorder=0)
ax.axhline(0, color="k", lw=1.5, zorder=2)
ax.axhline(h, color=BLUE, lw=2.5, ls="--", zorder=2, label=f"Reflector  $h = {h}$ m")
ax.text(50, h / 2, f"$V_1 = {V1}$ m/s", fontsize=9, va="center", color=BLUE)
ax.text(50, h + 70, "$V_2$", fontsize=9, va="center", color=ORANGE)

ax.plot(src_x, 0, "*", ms=18, color=RED, zorder=5, label="Source")
for i, xr in enumerate(offsets):
    xmid = xr / 2          # midpoint (source at 0)
    ax.plot([src_x, xmid, xr], [0, h, 0], color=rec_cols[i], lw=1.8, alpha=0.9)
    ax.plot(xr, 0, "v", ms=11, color=rec_cols[i], zorder=5)
ax.plot([], [], "v", ms=10, color=BLUE, label="Receivers")

ax.set_xlim(-50, 2500)
ax.set_ylim(720, -120)
ax.set_xlabel("Offset  $x$  (m)", fontsize=10)
ax.set_ylabel("Depth  $z$  (m)", fontsize=10)
ax.set_title("(A) Survey geometry", fontsize=10)
ax.legend(fontsize=8, loc="lower right", framealpha=0.9)

# ── Panel B: t–x hyperbola ────────────────────────────────────────────────────
ax2 = axes[1]
t0 = 2 * h / V1
x_plot = np.linspace(0, 2500, 600)
t_hyp  = np.sqrt(t0**2 + x_plot**2 / V1**2) * 1000   # ms

ax2.plot(x_plot, t_hyp, color=BLUE, lw=2.5, label="Reflection hyperbola")
ax2.axhline(t0 * 1000, color="gray", ls=":", lw=1.5, label=f"$t_0 = {int(t0*1000)}$ ms")
t_asym = x_plot / V1 * 1000
ax2.plot(x_plot[x_plot > 200], t_asym[x_plot > 200], color=ORANGE, ls="--", lw=1.8,
         label=f"Asymptote  (slope $1/V_1$)")

for i, xr in enumerate(offsets):
    t_r = np.sqrt(t0**2 + xr**2 / V1**2) * 1000
    ax2.plot(xr, t_r, "v", ms=11, color=rec_cols[i], zorder=5)

ax2.set_xlim(0, 2500)
ax2.set_ylim(1600, 0)
ax2.set_xlabel("Source–receiver offset  $x$  (m)", fontsize=10)
ax2.set_ylabel("Two-way travel time  (ms)", fontsize=10)
ax2.set_title("(B) Travel-time curve", fontsize=10)
ax2.legend(fontsize=8, framealpha=0.9)
ax2.grid(alpha=0.25)

plt.savefig("assets/figures/fig_reflection_geometry.png", dpi=150, bbox_inches="tight")
print("Saved: assets/figures/fig_reflection_geometry.png")
