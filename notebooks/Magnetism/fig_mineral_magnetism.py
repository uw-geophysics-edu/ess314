"""
fig_mineral_magnetism.py

Scientific content: Schematic spin alignment in the five categories of magnetic
materials encountered in geophysics — diamagnetic (k < 0), paramagnetic
(k > 0, small, alignment only in an applied field), ferromagnetic (large k,
parallel alignment by exchange interaction), antiferromagnetic (antiparallel
sublattices, net k ~ 0, e.g. hematite), and ferrimagnetic (unequal antiparallel
sublattices, large net k, e.g. magnetite). The figure also indicates the
typical susceptibility magnitude for each category and a representative mineral.

Reproduces the scientific content of:
  Butler, R. F. (1992). Paleomagnetism: Magnetic Domains to Geologic Terranes.
  Blackwell, Chapter 2. (Cited only; figure is original.)
  Tauxe, L. et al. (2018). Essentials of Paleomagnetism, 4th ed. (open access,
  https://earthref.org/MagIC/books/Tauxe/Essentials/), Section 3.2.

Output: assets/figures/fig_mineral_magnetism.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch

mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def draw_spin(ax, x, y, direction, length=0.30, color=COLORS[0]):
    """Draw a single spin arrow centred at (x, y) with given direction
    (+1 = up, -1 = down)."""
    dy = length * direction
    ax.add_patch(FancyArrowPatch(
        (x, y - dy / 2), (x, y + dy / 2),
        arrowstyle="-|>", mutation_scale=12,
        color=color, linewidth=1.6,
    ))


categories = [
    ("Diamagnetic",     "quartz, halite",       "k ≈ −10⁻⁵",
        "no permanent\nmoments", "diamag"),
    ("Paramagnetic",    "olivine, pyroxene",    "k ≈ +10⁻⁴",
        "weak alignment\nin H", "para"),
    ("Ferromagnetic",   "iron (rare in nature)",  "k ≫ 1",
        "all parallel", "ferro"),
    ("Antiferromagnetic", "hematite",           "k ≈ 0",
        "antiparallel\nnet = 0", "antiferro"),
    ("Ferrimagnetic",   "magnetite",            "k > 1",
        "unequal antipar.\nnet ≠ 0", "ferri"),
]

fig, axes = plt.subplots(1, 5, figsize=(15.0, 5.6))
fig.subplots_adjust(top=0.78, bottom=0.10, wspace=0.20)

rng = np.random.default_rng(7)

for ax, (name, mineral, susc, mech, kind) in zip(axes, categories):
    # Background lattice points
    xs, ys = np.meshgrid(np.arange(0, 5), np.arange(0, 4))
    xs = xs.ravel()
    ys = ys.ravel()

    if kind == "diamag":
        # No spins (no permanent moments); shown as small circles
        for x, y in zip(xs, ys):
            ax.plot(x, y, "o", color=COLORS[6], markersize=5,
                    markerfacecolor="white", markeredgewidth=1.0)
        arrow_caption = "no permanent moments"

    elif kind == "para":
        # Random spin directions; weak average alignment
        for x, y in zip(xs, ys):
            d = rng.choice([+1, -1, +1])      # slight bias upward
            draw_spin(ax, x, y, d, length=0.55, color=COLORS[0])
        arrow_caption = "random; weak\nalignment in H"

    elif kind == "ferro":
        # All parallel up
        for x, y in zip(xs, ys):
            draw_spin(ax, x, y, +1, length=0.65, color=COLORS[3])
        arrow_caption = "all parallel"

    elif kind == "antiferro":
        # Antiparallel sublattices (row-alternating)
        for x, y in zip(xs, ys):
            d = +1 if (y % 2 == 0) else -1
            color = COLORS[3] if d == +1 else COLORS[4]
            draw_spin(ax, x, y, d, length=0.6, color=color)
        arrow_caption = "antiparallel; net = 0"

    elif kind == "ferri":
        # Unequal antiparallel sublattices: up arrows long, down arrows short
        for x, y in zip(xs, ys):
            if y % 2 == 0:
                draw_spin(ax, x, y, +1, length=0.90, color=COLORS[3])
            else:
                draw_spin(ax, x, y, -1, length=0.30, color=COLORS[4])
        arrow_caption = "unequal antiparallel\nnet ≠ 0"

    # Axes cosmetics
    ax.set_xlim(-0.7, 4.7)
    ax.set_ylim(-1.6, 5.0)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])

    # Draw only a rectangle around the lattice region (y in [-0.5, 3.5])
    from matplotlib.patches import Rectangle
    rect = Rectangle((-0.55, -0.55), 5.10, 4.10, fill=False,
                     edgecolor="grey", linewidth=0.8)
    ax.add_patch(rect)
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Title and labels — title at top, mineral above box, mechanism INSIDE box, k below
    ax.set_title(name, color=COLORS[0], fontweight="bold", pad=8)
    # Mineral name (italic) above the lattice box
    ax.text(2, 4.10, mineral, ha="center", va="bottom", fontsize=10.5,
            fontstyle="italic", color=COLORS[6])
    # Mechanism caption INSIDE the box, near the top
    ax.text(2, 3.20, arrow_caption, ha="center", va="bottom", fontsize=10,
            color="grey",
            bbox=dict(boxstyle="round,pad=0.20", facecolor="white",
                      edgecolor="none", alpha=0.85))
    # Susceptibility magnitude below the lattice
    ax.text(2, -1.10, f"{susc}", ha="center", va="top", fontsize=11.5,
            color=COLORS[4], fontweight="bold")

fig.suptitle("Magnetic ordering at the mineral scale — five categories of "
             "geological materials", fontsize=14, y=0.99)

fig.savefig("assets/figures/fig_mineral_magnetism.png",
            dpi=300, bbox_inches="tight")
print("saved fig_mineral_magnetism.png")
