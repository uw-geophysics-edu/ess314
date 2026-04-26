"""
fig_seismometer_principle.py

Scientific content: A seismometer measures ground motion by exploiting the
inertia of a suspended mass. The mass tries to remain stationary in
inertial space while the housing — and the ground beneath it — accelerates
during a passing wave. The relative displacement between mass and housing
is converted into an electrical signal (typically by sensing the motion of
a coil through a magnetic field). Two configurations are shown: a vertical
geometry that responds to vertical ground motion, and a pendulum geometry
that responds to one horizontal component.

Reproduces the scientific content of:
  Stein & Wysession (2003), Ch. 6 (instrumentation, mass-spring
  seismometer schematic).
  Lowrie & Fichtner (2020), Ch. 4 §4.4.

Output: assets/figures/fig_seismometer_principle.png
License: CC-BY 4.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import patches

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 130, "savefig.dpi": 200,
})

C_HOUSE = "#666666"
C_MASS = "#0072B2"
C_SPRING = "#444444"
C_MAG = "#D55E00"
C_GROUND = "#F0E5D0"
C_ARROW = "#222222"
C_COIL = "#7E2360"

fig, axes = plt.subplots(1, 2, figsize=(13.5, 6.0))


def draw_spring(ax, x, y0, y1, n_turns=10, width=0.18, lw=2.0, color=C_SPRING):
    """Draw a zigzag spring between (x, y0) and (x, y1)."""
    ys = np.linspace(y0, y1, n_turns * 2 + 1)
    xs = np.full_like(ys, x)
    xs[1:-1:2] = x - width
    xs[2:-1:2] = x + width
    ax.plot(xs, ys, color=color, lw=lw, zorder=4)


# ── Panel (a): vertical seismometer ─────────────────────────────────
ax = axes[0]
ax.set_xlim(-2, 2)
ax.set_ylim(-1, 5)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("(a) Vertical seismometer", fontsize=13, pad=8)

# Ground
ax.fill_between([-2, 2], -1, 0, color=C_GROUND, zorder=0)
ax.axhline(0, color="#000", lw=1.4, zorder=2)

# Housing (frame attached to ground)
housing = patches.Rectangle((-1.4, 0), 2.8, 4.5, fill=False,
                            edgecolor=C_HOUSE, lw=2.0, zorder=2)
ax.add_patch(housing)

# Spring from top of housing to mass
draw_spring(ax, x=0.0, y0=4.5, y1=2.7)

# Mass (suspended from spring)
mass = patches.FancyBboxPatch((-0.6, 1.95), 1.2, 0.75,
                              boxstyle="round,pad=0.02",
                              fill=True, facecolor=C_MASS,
                              edgecolor="#003a5d", lw=1.6, zorder=5)
ax.add_patch(mass)
ax.text(0, 2.32, "M", ha="center", va="center", fontsize=18, color="white",
        fontweight="bold", zorder=6)

# Coil + magnet (sensing element)
coil = patches.Rectangle((-0.4, 1.05), 0.8, 0.55, fill=True,
                         facecolor="white", edgecolor=C_COIL, lw=1.6,
                         zorder=4)
ax.add_patch(coil)
# Diagonal lines indicating coil windings
for f in (0.20, 0.45, 0.70, 0.95):
    ax.plot([-0.4 + 0.8 * f - 0.06, -0.4 + 0.8 * f + 0.06],
            [1.05, 1.60], color=C_COIL, lw=1.0, zorder=5)

# Permanent magnets (fixed to housing) flanking the coil
for x in (-1.0, 0.6):
    mag = patches.Rectangle((x, 0.85), 0.4, 0.95, fill=True,
                            facecolor=C_MAG, edgecolor="#7e3300", lw=1.0,
                            zorder=3)
    ax.add_patch(mag)
ax.text(-0.8, 1.32, "N", ha="center", va="center", fontsize=12,
        color="white", fontweight="bold", zorder=4)
ax.text(0.8, 1.32, "S", ha="center", va="center", fontsize=12,
        color="white", fontweight="bold", zorder=4)

# Output leads from coil
ax.plot([-0.4, -1.45], [1.30, 1.30], color="#000", lw=1.0, zorder=5)
ax.plot([0.4, 1.45], [1.30, 1.30], color="#000", lw=1.0, zorder=5)
ax.text(1.55, 1.30, "V(t)", ha="left", va="center", fontsize=11,
        color="#000")

# Ground motion arrow (vertical)
ax.annotate("", xy=(-1.75, -0.55), xytext=(-1.75, -0.05),
            arrowprops=dict(arrowstyle="<->", color=C_ARROW, lw=2.0))
ax.text(-1.95, -0.30, "ground\nmotion\n(vertical)",
        ha="right", va="center", fontsize=10.5, color=C_ARROW)

# Labels
ax.annotate("Spring", xy=(0.0, 3.6), xytext=(1.0, 3.95),
            fontsize=11, color=C_SPRING,
            arrowprops=dict(arrowstyle="->", color=C_SPRING, lw=0.8))
ax.annotate("Inertial mass", xy=(0.5, 2.3), xytext=(1.0, 3.0),
            fontsize=11, color=C_MASS,
            arrowprops=dict(arrowstyle="->", color=C_MASS, lw=0.8))
ax.annotate("Coil + magnet\n(velocity sensor)", xy=(0.0, 1.30),
            xytext=(-1.95, 0.40),
            fontsize=11, color=C_COIL, ha="left",
            arrowprops=dict(arrowstyle="->", color=C_COIL, lw=0.8))

# ── Panel (b): horizontal-component pendulum seismometer ───────────
ax = axes[1]
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-1, 5)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("(b) Horizontal-component (pendulum) seismometer",
             fontsize=13, pad=8)

# Ground
ax.fill_between([-2.5, 2.5], -1, 0, color=C_GROUND, zorder=0)
ax.axhline(0, color="#000", lw=1.4, zorder=2)

# Housing frame
housing = patches.Rectangle((-2.2, 0), 4.4, 4.5, fill=False,
                            edgecolor=C_HOUSE, lw=2.0, zorder=2)
ax.add_patch(housing)

# Pivot at left
pivot = np.array([-1.7, 3.0])
ax.plot(pivot[0], pivot[1], marker="o", color="#000", ms=10, zorder=6)
ax.text(pivot[0] - 0.05, pivot[1] + 0.20, "Pivot",
        ha="right", va="bottom", fontsize=11)

# Boom (rigid arm) extending to mass
mass_pos = np.array([1.3, 2.2])
ax.plot([pivot[0], mass_pos[0]], [pivot[1], mass_pos[1]],
        color="#000", lw=2.5, zorder=4)

# Mass at end of boom
mass = patches.Circle(mass_pos, radius=0.32, fill=True, facecolor=C_MASS,
                      edgecolor="#003a5d", lw=1.6, zorder=5)
ax.add_patch(mass)
ax.text(mass_pos[0], mass_pos[1], "M", ha="center", va="center",
        fontsize=14, color="white", fontweight="bold", zorder=6)

# Restoring spring from top of housing to boom midpoint
spring_anchor = np.array([0.0, 4.5])
spring_target = (pivot + mass_pos) / 2
ax.plot([spring_anchor[0], spring_target[0]],
        [spring_anchor[1], spring_target[1]], color=C_SPRING, lw=2.0,
        zorder=3)
# Draw a small zigzag overlay near the spring
n = 8
ts = np.linspace(0.05, 0.95, n)
sx = spring_anchor[0] + (spring_target[0] - spring_anchor[0]) * ts
sy = spring_anchor[1] + (spring_target[1] - spring_anchor[1]) * ts
perp = np.array([-(spring_target[1] - spring_anchor[1]),
                 (spring_target[0] - spring_anchor[0])])
perp = 0.10 * perp / np.linalg.norm(perp)
sxz = sx + perp[0] * np.sign(np.sin(np.linspace(0, 4 * np.pi, n)))
syz = sy + perp[1] * np.sign(np.sin(np.linspace(0, 4 * np.pi, n)))
ax.plot(sxz, syz, color=C_SPRING, lw=1.5, zorder=4)

# Sensor (coil + magnet) under the mass
mag = patches.Rectangle((mass_pos[0] - 0.3, 1.1), 0.6, 0.6, fill=True,
                        facecolor=C_MAG, edgecolor="#7e3300", lw=1.0,
                        zorder=3)
ax.add_patch(mag)
ax.text(mass_pos[0], 1.4, "N  S", ha="center", va="center", fontsize=11,
        color="white", fontweight="bold")

# Output leads
ax.plot([mass_pos[0] - 0.3, -2.25], [1.40, 1.40], color="#000", lw=1.0,
        zorder=5)
ax.text(-2.35, 1.40, "V(t)", ha="right", va="center", fontsize=11,
        color="#000")

# Ground motion arrow (horizontal)
ax.annotate("", xy=(-2.35, -0.50), xytext=(2.35, -0.50),
            arrowprops=dict(arrowstyle="<->", color=C_ARROW, lw=2.0))
ax.text(0.0, -0.75, "ground motion (horizontal)",
        ha="center", va="top", fontsize=10.5, color=C_ARROW)

# Labels
ax.annotate("Boom (rigid)",
            xy=((pivot[0] + mass_pos[0]) / 2, (pivot[1] + mass_pos[1]) / 2),
            xytext=(-1.5, 4.0),
            fontsize=11, color="#000",
            arrowprops=dict(arrowstyle="->", color="#000", lw=0.8))
ax.annotate("Restoring\nspring",
            xy=spring_target,
            xytext=(1.4, 4.0),
            fontsize=11, color=C_SPRING,
            arrowprops=dict(arrowstyle="->", color=C_SPRING, lw=0.8))

fig.suptitle("Seismometer principle: a suspended mass senses motion of the ground",
             fontsize=14, y=1.00)
fig.tight_layout(rect=[0, 0, 1, 0.96])

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_seismometer_principle.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
