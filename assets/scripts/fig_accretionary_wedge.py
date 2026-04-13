"""
Accretionary wedge cross-section labelling the three main non-idealities
that break the flat-layer reflection assumption:
  ① Dipping reflectors
  ② Surface multiple
  ③ Fault-tip diffraction
Used on lecture 09 slides (slide 3: "Why the Flat-Layer Model Fails").
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

BLUE   = "#0072B2"
ORANGE = "#E69F00"
RED    = "#D55E00"
GREEN  = "#009E73"
LBLUE  = "#56B4E9"
DARK   = "#222222"

fig, ax = plt.subplots(figsize=(11, 4.8))
fig.subplots_adjust(left=0.04, right=0.97, top=0.90, bottom=0.10)

ax.set_xlim(0, 100)
ax.set_ylim(16, -2.5)
ax.set_aspect("equal")
ax.set_xlabel("Distance  →  (NW to SE, schematic)", fontsize=10)
ax.tick_params(labelleft=False, left=False)
ax.set_title("Cascadia Accretionary Wedge — Three Reflection Non-Idealities", fontsize=11)

# ── Ocean water / sea surface ─────────────────────────────────────────────────
ax.fill_between([0, 100], [-2.5, -2.5], [0, 0], color=LBLUE, alpha=0.25, zorder=0)
ax.axhline(0, color=LBLUE, lw=2, zorder=2)
ax.text(1.5, -1.6, "Sea surface", fontsize=8, color=LBLUE)
ax.text(1.5,  0.5, "Sea floor", fontsize=8, color="#0a4a7a")

# ── Subducting oceanic plate ───────────────────────────────────────────────────
slab_x = np.array([18, 100])
slab_y = np.array([3.2, 14.5])
ax.fill_between(slab_x, slab_y, slab_y + 2.5, color="#B0BEC5", alpha=0.70, zorder=1)
ax.plot(slab_x, slab_y, color=DARK, lw=1.8, zorder=2)

# ── Décollement (main dipping reflector) ─────────────────────────────────────
dec_x = np.array([14, 96])
dec_y = np.array([2.4, 13.0])
ax.plot(dec_x, dec_y, color=BLUE, lw=2.8, ls="--", zorder=3)
ax.text(16, 1.7, "Décollement", fontsize=8, color=BLUE, style="italic")

# ── Thrust packages (dipping internal reflectors) ────────────────────────────
pkgs = [
    (14, 36, [0.3, 1.4, 2.5], 0.45),
    (30, 54, [0.3, 1.3, 2.3], 0.45),
    (46, 70, [0.3, 1.2, 2.1], 0.40),
    (60, 84, [0.3, 1.1, 1.9], 0.35),
]
pcolors = ["#90CAF9", "#80DEEA", "#A5D6A7", "#FFCC80"]
for (x0, x1, fracs, alpha), pc in zip(pkgs, pcolors):
    # Package fill between seafloor and topmost reflector horizon
    ax.fill_between([x0, x1], [0.3, 0.3], [fracs[-1], fracs[-1]],
                    color=pc, alpha=alpha, zorder=1)
    # Internal dipping reflectors
    for frac in fracs:
        ax.plot([x0, x1], [frac, frac + 0.6 * (x1 - x0) / 22],
                color=pc, lw=1.4, alpha=0.95, zorder=2)

# ── ① Dipping reflectors annotation ──────────────────────────────────────────
ax.annotate("① Dipping reflectors\n(asymmetric NMO,\nreflection-point smear)",
            xy=(52, 2.2), xytext=(56, 0.2),
            fontsize=8, color=ORANGE, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.6),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", alpha=0.88), zorder=8)

# ── ② Surface multiple ray path ───────────────────────────────────────────────
# Source at 24, reflects at seafloor x=34 (z=0), then at reflector x=34,
# then back up to receiver at x=44
mx = [22, 28, 34, 40, 46]
my = [0,   3.0, 0,  3.5, 0]
ax.plot(mx, my, color=RED, lw=2, ls="-.", zorder=5)
ax.plot([22, 22], [-0.35, 0.35], color=RED, lw=2, zorder=5)
ax.annotate("② Surface multiple\n(same $V_\\mathrm{rms}$ as primary\n→ stacking can't remove it)",
            xy=(34, 2.5), xytext=(10, 6.0),
            fontsize=8, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.6),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", alpha=0.88), zorder=8)

# ── ③ Fault tip + diffraction fans ───────────────────────────────────────────
ft_x, ft_y = 71, 3.8
ax.plot([71, 65], [1.2, ft_y], color="#444", lw=2.2, zorder=4)  # fault trace
ax.plot(ft_x, ft_y, "^", ms=11, color=GREEN, zorder=6)
for ang in [-50, -25, 0, 25, 50]:
    dx =  np.sin(np.radians(ang)) * 10
    dy = -np.cos(np.radians(ang)) * 7
    ax.annotate("", xy=(ft_x + dx, ft_y + dy), xytext=(ft_x, ft_y),
                arrowprops=dict(arrowstyle="-", color=GREEN, lw=1.2, alpha=0.70))
ax.annotate("③ Fault-tip diffraction\n(hyperbola on raw section\n→ requires migration)",
            xy=(ft_x, ft_y), xytext=(73, 1.2),
            fontsize=8, color=GREEN, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6),
            bbox=dict(boxstyle="round,pad=0.25", fc="white", alpha=0.88), zorder=8)

# ── Legend ────────────────────────────────────────────────────────────────────
handles = [
    mpatches.Patch(color=ORANGE, label="① Dipping reflectors"),
    mpatches.Patch(color=RED,    label="② Multiples"),
    mpatches.Patch(color=GREEN,  label="③ Diffractions"),
]
ax.legend(handles=handles, fontsize=8, loc="lower right",
          framealpha=0.92, edgecolor="gray")

plt.savefig("assets/figures/fig_accretionary_wedge.png", dpi=150, bbox_inches="tight")
print("Saved: assets/figures/fig_accretionary_wedge.png")
