"""
fig_multiple_types.py

Scientific content:
    Multiple reflections are coherent events that have bounced more than
    once before reaching the receiver. Key types:
      (1) Long-path (surface) multiple: source → reflector → surface → reflector → receiver.
          TWTT = 2 * t_0 (double the primary), SAME NMO velocity as primary.
          → Cannot be removed by NMO/stacking alone.
      (2) Peg-leg (short-path) multiple: one extra leg at a shallower interface.
          TWTT between primary and long-path multiple; different NMO velocity.
      (3) Interbed multiple: bounces between two sub-surface interfaces.

    Panel A: schematic ray-path diagram for each multiple type.
    Panel B: synthetic CMP gather showing primary and multiples as
             distinct hyperbolic events at different TWTT values.
    Panel C: t^2–x^2 comparison — long-path multiple has the same slope
             (same V_rms) but twice the intercept of the primary.

Reproduces scientific content of:
    Sheriff, R.E. & Geldart, L.P. (1995). Exploration Seismology, 2nd ed.
    Cambridge University Press. Chapter 6, §6.1 (Multiple reflections).
    Verschuur, D.J. (1991). Surface-related multiple elimination. PhD thesis,
    Delft University of Technology.

Output: assets/figures/fig_multiple_types.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

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

BLUE   = "#0072B2"
ORANGE = "#E69F00"
GREEN  = "#009E73"
RED    = "#D55E00"
PINK   = "#CC79A7"
GRAY   = "#888888"
BLACK  = "#000000"

rng = np.random.default_rng(7)

# ── Seismic model ─────────────────────────────────────────────────────────────
V_rms   = 2000.0   # m/s (primary NMO velocity)
t0_prim = 0.50     # s   (primary zero-offset TWTT)
t0_mult = 2*t0_prim  # s  long-path multiple (same V_rms)
t0_peg  = 0.75     # s   peg-leg (between primary and multiple)
t0_ib   = 0.90     # s   interbed multiple

dt      = 0.002    # s
nt      = 751      # 0–1.5 s
t_full  = np.arange(nt) * dt
offsets = np.arange(0, 2001, 200)   # m, 0–2000

def ricker(f0, dt, t_half=0.10):
    tw = np.arange(-t_half, t_half, dt)
    u  = (np.pi * f0 * tw)**2
    return (1 - 2*u) * np.exp(-u)

wav = ricker(25.0, dt)

# ── Build synthetic gather ────────────────────────────────────────────────────
reflectors = [
    {"t0": t0_prim, "V": V_rms,   "amp": 1.00, "color": BLUE,   "label": "Primary"},
    {"t0": t0_mult, "V": V_rms,   "amp": -0.45, "color": RED,    "label": "Long-path multiple"},
    {"t0": t0_peg,  "V": 2200.,   "amp": 0.30, "color": ORANGE, "label": "Peg-leg"},
    {"t0": t0_ib,   "V": 2400.,   "amp": -0.20, "color": GREEN,  "label": "Interbed"},
]

gather = np.zeros((nt, len(offsets)))
for ix, x in enumerate(offsets):
    spike = np.zeros(nt)
    for r in reflectors:
        tx  = np.sqrt(r["t0"]**2 + x**2 / r["V"]**2)
        idx = int(round(tx / dt))
        if idx < nt:
            spike[idx] += r["amp"]
    trace = fftconvolve(spike, wav, mode="same")
    trace += rng.standard_normal(nt) * 0.04
    gather[:, ix] = trace

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(17, 8))
gs  = fig.add_gridspec(1, 3, wspace=0.38)
ax_ray   = fig.add_subplot(gs[0, 0])
ax_gath  = fig.add_subplot(gs[0, 1])
ax_t2x2  = fig.add_subplot(gs[0, 2])

# ── Panel A: ray-path schematic ───────────────────────────────────────────────
ax = ax_ray
ax.set_xlim(-0.5, 4.5)
ax.set_ylim(3.2, -0.6)
ax.set_aspect("equal", adjustable="box")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("(A) Multiple reflection types", fontsize=13)

# Surface
ax.axhline(0, color=BLACK, lw=2, xmin=0.05, xmax=0.95)
# Reflector 1 (shallow)
ax.axhline(1.0, color=GRAY, lw=1.5, ls="--", alpha=0.6, xmin=0.05, xmax=0.95)
# Reflector 2 (main)
ax.axhline(2.0, color=BLUE, lw=2.2, xmin=0.05, xmax=0.95)

ax.text(4.3, 0,   "Surface",   ha="right", fontsize=10, color=BLACK, va="center")
ax.text(4.3, 1.0, "Refl. 1",  ha="right", fontsize=10, color=GRAY,  va="center")
ax.text(4.3, 2.0, "Refl. 2",  ha="right", fontsize=10, color=BLUE,  va="center")

def draw_ray(ax, pts, color, lw=1.5, label=None):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=lw, label=label)

# (1) Primary: S → R2 → G
draw_ray(ax, [(0.2,0),(0.9,2),(1.6,0)], BLUE, lw=2.0, label="Primary")
ax.plot(0.2, 0, "^", color=RED,   ms=9, zorder=5)
ax.plot(1.6, 0, "v", color=BLACK, ms=7, zorder=5)
ax.text(0.90, -0.3, "P", ha="center", fontsize=12, color=BLUE, fontweight="bold")

# (2) Long-path multiple: S → R2 → surface → R2 → G
draw_ray(ax, [(0.5,0),(0.9,2),(1.3,0),(1.7,2),(2.1,0)],
         RED, lw=2.0, label="Long-path multiple")
ax.plot(0.5, 0, "^", color=RED,   ms=9, zorder=5)
ax.plot(2.1, 0, "v", color=BLACK, ms=7, zorder=5)
ax.text(1.30, -0.3, "M", ha="center", fontsize=12, color=RED, fontweight="bold")

# (3) Peg-leg: S → R2 → R1 → G  (short-path)
draw_ray(ax, [(2.4,0),(2.85,2),(3.05,1),(3.4,0)],
         ORANGE, lw=2.0, label="Peg-leg")
ax.plot(2.4, 0, "^", color=RED,   ms=9, zorder=5)
ax.plot(3.4, 0, "v", color=BLACK, ms=7, zorder=5)
ax.text(2.9, -0.3, "PL", ha="center", fontsize=11, color=ORANGE, fontweight="bold")

# (4) Interbed: S → R1 → R2 → R1 → G
draw_ray(ax, [(3.6,0),(3.7,1),(3.85,2),(4.0,1),(4.2,0)],
         GREEN, lw=2.0, label="Interbed")
ax.plot(3.6, 0, "^", color=RED,   ms=9, zorder=5)
ax.plot(4.2, 0, "v", color=BLACK, ms=7, zorder=5)
ax.text(3.9, -0.3, "IB", ha="center", fontsize=11, color=GREEN, fontweight="bold")

ax.legend(loc="lower left", fontsize=10, ncol=1)

# ── Panel B: synthetic CMP gather ────────────────────────────────────────────
ax = ax_gath
t_ms = t_full * 1000
scale = 55.0

for ix, x in enumerate(offsets):
    tr = gather[:, ix]
    ax.fill_betweenx(t_ms, x, x + tr * scale,
                      where=tr > 0, facecolor=BLACK, alpha=0.65)
    ax.plot(x + tr * scale, t_ms, color=BLACK, lw=0.35, alpha=0.5)

# Overlay predicted hyperbolae
for r in reflectors:
    t_hyp = np.sqrt(r["t0"]**2 + offsets**2 / r["V"]**2) * 1000
    ax.plot(offsets, t_hyp, color=r["color"], lw=2.0, ls="--", alpha=0.9,
            label=r["label"])

ax.set_xlim(-80, 2080)
ax.set_ylim(1500, 0)
ax.set_xlabel("Offset (m)")
ax.set_ylabel("Two-way time (ms)")
ax.set_title("(B) CMP gather with multiples", fontsize=13)
ax.legend(loc="lower right", fontsize=10)

# ── Panel C: t^2–x^2 ─────────────────────────────────────────────────────────
ax = ax_t2x2
x2 = offsets**2 / 1e6   # km^2
for r in reflectors:
    t2 = (r["t0"]**2 + offsets**2 / r["V"]**2) * 1e6   # ms^2
    ax.plot(x2, t2, color=r["color"], lw=2.2,
            label=f"{r['label']} $t_0={r['t0']:.2f}$ s")

# Highlight that primary and long-path multiple have the same slope
ax.annotate("Same slope\n(same $V_{rms}$)", xy=(3.5, 1.8e6),
            xytext=(1.2, 1.5e6),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.3),
            fontsize=11, color=RED)
ax.annotate("", xy=(3.5, 3.0e6),
            xytext=(2.2, 2.2e6),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.3))

ax.set_xlabel("$x^2$ (km$^2$)")
ax.set_ylabel("$t^2$ (ms$^2$)")
ax.set_title("(C) $t^2$–$x^2$: same slope for\nprimary and long-path multiple", fontsize=13)
ax.legend(loc="upper left", fontsize=10)
ax.set_xlim(0, None)
ax.set_ylim(0, None)

fig.tight_layout()
fig.savefig("assets/figures/fig_multiple_types.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_multiple_types.png")

if __name__ == "__main__":
    plt.show()
