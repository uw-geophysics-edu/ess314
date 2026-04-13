"""
CMP geometry: multiple source–receiver pairs sharing one common reflection point.
Panel A: cross-section with several shot-receiver pairs and a flat reflector.
Panel B: corresponding CMP gather (wiggle traces + hyperbola).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE   = "#0072B2"
RED    = "#D55E00"
ORANGE = "#E69F00"

h  = 600    # reflector depth  (m)
V1 = 2000   # velocity  (m/s)
t0 = 2 * h / V1
cmp_x = 1400   # CMP surface location
half_offsets = [250, 500, 750, 1000, 1250]
cmap_vals    = [0.25, 0.40, 0.55, 0.72, 0.90]
colors       = [plt.cm.Blues(v) for v in cmap_vals]

fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.8))
fig.subplots_adjust(wspace=0.38)

# ── Panel A: geometry ─────────────────────────────────────────────────────────
ax = axes[0]
ax.fill_between([0, 2900], [0, 0], [h, h],    color="#DEEFF9", zorder=0)
ax.fill_between([0, 2900], [h, h], [950, 950], color="#FFE4CC", zorder=0)
ax.axhline(0, color="k", lw=1.5, zorder=2)
ax.axhline(h, color=BLUE, lw=2.5, ls="--", zorder=2)
ax.text(100, h + 65, "Reflector", fontsize=9, color=BLUE)
ax.text(100, h / 2,  f"$V_1 = {V1}$ m/s", fontsize=9, va="center", color=BLUE)

# CMP vertical guide + common reflection point
ax.axvline(cmp_x, color="gray", ls=":", lw=1.4, alpha=0.8)
ax.plot(cmp_x, h, "D", ms=12, color=RED, zorder=6, label="Common reflection point")
ax.text(cmp_x + 40, h + 65, "Common\nreflection point", fontsize=8, color=RED)

for i, ho in enumerate(half_offsets):
    src = cmp_x - ho
    rec = cmp_x + ho
    ax.plot([src, cmp_x, rec], [0, h, 0], color=colors[i], lw=2, alpha=0.88)
    ax.plot(src, 0, "*", ms=13, color=colors[i], zorder=5)
    ax.plot(rec, 0, "v", ms=10, color=colors[i], zorder=5)

ax.plot([], [], "*", ms=11, color=colors[2], label="Sources")
ax.plot([], [], "v", ms=9,  color=colors[2], label="Receivers")

ax.annotate("", xy=(cmp_x - half_offsets[-1], -80), xytext=(cmp_x, -80),
            arrowprops=dict(arrowstyle="<->", color="gray", lw=1.4))
ax.text(cmp_x - half_offsets[-1] / 2, -115, "$x/2$", fontsize=9,
        ha="center", color="gray")

ax.set_xlim(0, 2800)
ax.set_ylim(900, -170)
ax.set_xlabel("Surface position (m)", fontsize=10)
ax.set_ylabel("Depth (m)", fontsize=10)
ax.set_title("(A) CMP geometry — every ray hits the same point", fontsize=10)
ax.legend(fontsize=8, loc="lower right", framealpha=0.9)

# ── Panel B: CMP gather (schematic wiggle traces) ─────────────────────────────
ax2 = axes[1]
dt_t  = 0.001
t_ax  = np.arange(0, 1.2, dt_t)
full_offsets = np.array(half_offsets) * 2
t_arrs = np.sqrt(t0**2 + full_offsets**2 / V1**2)

def ricker_wav(t_rel, f0=30):
    u = (np.pi * f0 * t_rel) ** 2
    return (1 - 2 * u) * np.exp(-u)

scale = 230

for i, (xo, ta) in enumerate(zip(full_offsets, t_arrs)):
    t_rel = t_ax - ta
    wav   = ricker_wav(t_rel, f0=30)
    wav[np.abs(t_rel) > 0.06] = 0
    ax2.fill_betweenx(t_ax, xo, xo + wav * scale,
                      where=wav > 0, color=colors[i], alpha=0.80)
    ax2.fill_betweenx(t_ax, xo, xo + wav * scale,
                      where=wav < 0, color=colors[i], alpha=0.30)
    ax2.plot(xo + wav * scale, t_ax, color=colors[i], lw=1.0)
    ax2.axvline(xo, color=colors[i], lw=0.5, ls=":", alpha=0.5)

ax2.plot(full_offsets, t_arrs, "D", ms=8, color=RED, zorder=5, label="Reflection peak")
x_c = np.linspace(0, 3200, 400)
t_c = np.sqrt(t0**2 + x_c**2 / V1**2)
ax2.plot(x_c, t_c, color=BLUE, lw=1.8, ls="--", alpha=0.55, label="Hyperbola")
ax2.axhline(t0, color="gray", ls=":", lw=1.2)
ax2.text(120, t0 - 0.025, f"$t_0 = {int(t0*1000)}$ ms", fontsize=9, color="gray")

ax2.set_xlim(0, 3100)
ax2.set_ylim(1.2, 0)
ax2.set_xlabel("Full offset  $x$  (m)", fontsize=10)
ax2.set_ylabel("Two-way travel time (s)", fontsize=10)
ax2.set_title(f"(B) CMP gather  ($h = {h}$ m,  $V_1 = {V1}$ m/s)", fontsize=10)
ax2.legend(fontsize=8, framealpha=0.9)
ax2.grid(alpha=0.20)

plt.savefig("assets/figures/fig_cmp_gather.png", dpi=150, bbox_inches="tight")
print("Saved: assets/figures/fig_cmp_gather.png")
