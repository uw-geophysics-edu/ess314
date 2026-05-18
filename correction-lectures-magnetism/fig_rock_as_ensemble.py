"""
fig_rock_as_ensemble.py

Scientific content: Four common rock types shown as schematic hand-sample
views with their magnetic mineral content, typical bulk magnetic
susceptibility k, and Königsberger ratio Q (= |M_rem| / |M_ind|). The
purpose is to make concrete the idea that a *rock* is an ensemble of
minerals, only some of which are magnetic, and that the bulk magnetic
response of the rock depends on (i) which minerals are present and
(ii) their volume fractions.

Rocks chosen for Pacific Northwest relevance:
  • Basalt — oceanic crust (Juan de Fuca plate, Columbia River Basalt)
  • Granite — Cascade plutons, Idaho batholith
  • Red bed sandstone — Triassic red beds (e.g. Spearfish Fm, generic
    analogue for Cordilleran red beds)
  • Marine mudstone — Olympic Peninsula accretionary sediments
    (analogue for fine-grained marine sediments)

Susceptibility ranges from Hunt et al. (1995), "Magnetic properties of
rocks and minerals", in *Rock Physics and Phase Relations*, AGU Reference
Shelf 3 (CC reproduced ranges, not figure).
DOI: 10.1029/RF003p0189

Output: assets/figures/fig_rock_as_ensemble.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Ellipse, Polygon
from matplotlib.colors import to_rgba

# ── Global rcParams ─────────────────────────────────────────────────
mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# Colorblind-safe accent palette
ACCENT_FERRI = "#D55E00"   # vermilion — ferrimagnetic (magnetite)
ACCENT_HEMA  = "#8B2C0F"   # dark red-brown — hematite
ACCENT_PARA  = "#0072B2"   # blue — paramagnetic (olivine, pyroxene, biotite)
ACCENT_DIA   = "#A8A8A8"   # grey — diamagnetic (quartz, feldspar, halite)

# ── Helper: draw a stylised hand-sample rock chip ──────────────────
def draw_rock(ax, mineral_recipe, title, k_range, Q_range,
              dominant_carrier, where_found, panel_color):
    """
    Draw a square hand-sample chip with random-shape mineral grains.

    mineral_recipe : list of (fraction, color, label, max_size, shape)
        fraction : volume fraction of this mineral
        color    : matplotlib colour
        label    : legend label
        max_size : maximum half-size of a grain (units of axes coords)
        shape    : "ellipse", "polygon", or "dot" (small ferrimagnetic grain)
    """
    # Frame
    rect = mpatches.Rectangle((0.05, 0.05), 0.90, 0.90,
                              edgecolor=panel_color, facecolor="white",
                              linewidth=2.2)
    ax.add_patch(rect)

    # Generate grains for each mineral type
    rng = np.random.default_rng(seed=hash(title) % 2**32)
    placed = []   # (x, y, r) to avoid overlap

    total_target_area = 0.81   # = 0.9 × 0.9, the frame interior
    for (fraction, color, label, max_size, shape) in mineral_recipe:
        target_area = fraction * total_target_area
        accumulated_area = 0.0
        attempts = 0
        while accumulated_area < target_area and attempts < 2500:
            attempts += 1
            x = rng.uniform(0.08, 0.92)
            y = rng.uniform(0.08, 0.92)
            size = rng.uniform(0.3 * max_size, max_size)
            # No strong overlap check for dia/para (they form the matrix)
            # but ferri/hema grains should not heavily overlap each other
            if shape == "dot" or shape == "polygon":
                clash = False
                for (xp, yp, rp) in placed:
                    if (x - xp)**2 + (y - yp)**2 < (size + rp)**2:
                        clash = True
                        break
                if clash:
                    continue
                placed.append((x, y, size))

            if shape == "ellipse":
                # Stretched, rotated ellipses for matrix grains
                a = size * rng.uniform(0.8, 1.6)
                b = size * rng.uniform(0.4, 1.0)
                ang = rng.uniform(0, 180)
                e = Ellipse((x, y), 2*a, 2*b, angle=ang,
                            facecolor=color, edgecolor="white",
                            linewidth=0.4, alpha=0.95)
                ax.add_patch(e)
                accumulated_area += np.pi * a * b
            elif shape == "polygon":
                # Angular polygons for accessory minerals
                n_sides = rng.integers(4, 8)
                angles = np.sort(rng.uniform(0, 2*np.pi, n_sides))
                rs = size * rng.uniform(0.7, 1.0, n_sides)
                verts = [(x + r*np.cos(a), y + r*np.sin(a))
                         for r, a in zip(rs, angles)]
                p = Polygon(verts, facecolor=color, edgecolor="black",
                            linewidth=0.5, alpha=0.95)
                ax.add_patch(p)
                accumulated_area += np.pi * size**2 * 0.7
            elif shape == "dot":
                # Round magnetic grain with a slight halo
                halo = Circle((x, y), size*1.3, facecolor=color, alpha=0.18,
                              edgecolor="none")
                ax.add_patch(halo)
                c = Circle((x, y), size, facecolor=color,
                           edgecolor="black", linewidth=0.5)
                ax.add_patch(c)
                accumulated_area += np.pi * size**2

    # Title plate above frame
    ax.text(0.5, 1.04, title, transform=ax.transAxes,
            fontsize=12.5, ha="center", va="bottom",
            fontweight="bold", color=panel_color)

    # Info plate below frame — three lines
    ax.text(0.5, -0.04,
            f"Bulk susceptibility: k ≈ {k_range}\n"
            f"Königsberger ratio: Q ≈ {Q_range}",
            transform=ax.transAxes,
            fontsize=11, ha="center", va="top",
            bbox=dict(boxstyle="round,pad=0.30", facecolor="#F4F4F4",
                      edgecolor=panel_color, linewidth=1.0))
    ax.text(0.5, -0.27,
            f"Carrier: {dominant_carrier}\n"
            f"Found in: {where_found}",
            transform=ax.transAxes,
            fontsize=11, ha="center", va="top",
            style="italic", color="#333333")

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


# ── Build figure ────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 4, figsize=(17, 6.0))

# ── Panel 1: BASALT (oceanic / CRB) ────────────────────────────────
# Plagioclase + clinopyroxene + olivine matrix, magnetite as 4–8 % accessory
basalt_recipe = [
    (0.55, "#7B8FA1", "plagioclase",      0.06, "ellipse"),   # grey-blue
    (0.28, "#3A2D24", "clinopyroxene",    0.06, "ellipse"),   # dark brown
    (0.10, ACCENT_PARA, "olivine (para)", 0.05, "polygon"),   # blue
    (0.07, ACCENT_FERRI, "magnetite (ferri)", 0.020, "dot"),  # vermilion
]
draw_rock(
    axes[0], basalt_recipe,
    title="Basalt (mafic, magnetite-rich)",
    k_range="$10^{-3}$ – $10^{-1}$ SI",
    Q_range="0.5 – 10",
    dominant_carrier="Magnetite / titanomagnetite (ferrimagnetic)",
    where_found="Juan de Fuca seafloor;\nColumbia River Basalt Group",
    panel_color="#0072B2",
)

# ── Panel 2: GRANITE (continental pluton) ─────────────────────────
granite_recipe = [
    (0.40, "#F2D7B6", "K-feldspar",     0.07, "ellipse"),   # pink-tan
    (0.30, "#D8D5CC", "plagioclase",    0.06, "ellipse"),   # off-white
    (0.20, ACCENT_DIA, "quartz",        0.05, "polygon"),   # grey
    (0.06, ACCENT_PARA, "biotite (para)", 0.04, "polygon"), # blue
    (0.015, ACCENT_FERRI, "magnetite (trace)", 0.015, "dot"),
]
draw_rock(
    axes[1], granite_recipe,
    title="Granite (felsic, low magnetite)",
    k_range="$10^{-5}$ – $10^{-3}$ SI",
    Q_range="0.1 – 1",
    dominant_carrier="Trace magnetite; mostly induced",
    where_found="Cascade arc plutons;\nIdaho Batholith",
    panel_color="#0072B2",
)

# ── Panel 3: RED BED SANDSTONE ────────────────────────────────────
redbed_recipe = [
    (0.55, "#E8B689", "hematite-coated quartz", 0.05, "ellipse"),
    (0.25, "#C97B4A", "iron-oxide cement",      0.06, "ellipse"),
    (0.12, ACCENT_DIA, "clean quartz",          0.05, "polygon"),
    (0.05, ACCENT_HEMA, "hematite (anti-ferri)", 0.018, "dot"),
]
draw_rock(
    axes[2], redbed_recipe,
    title="Red bed sandstone",
    k_range="$10^{-5}$ – $10^{-4}$ SI",
    Q_range="1 – 100",
    dominant_carrier="Hematite (chemical remanence)",
    where_found="Triassic red beds of the\nCordillera; arid-margin sediments",
    panel_color="#8B2C0F",
)

# ── Panel 4: MARINE MUDSTONE ──────────────────────────────────────
mud_recipe = [
    (0.65, "#5C5F66", "clay matrix",          0.04, "ellipse"),
    (0.20, "#363941", "organic-rich silt",    0.05, "ellipse"),
    (0.10, ACCENT_PARA, "biogenic Fe (para)", 0.030, "polygon"),
    (0.025, ACCENT_FERRI, "detrital magnetite", 0.012, "dot"),
]
draw_rock(
    axes[3], mud_recipe,
    title="Marine mudstone",
    k_range="$10^{-5}$ – $10^{-3}$ SI",
    Q_range="0.1 – 2",
    dominant_carrier="Detrital magnetite + biogenic Fe",
    where_found="Olympic Peninsula accretionary\nwedge sediments",
    panel_color="#0072B2",
)

# ── Master title ───────────────────────────────────────────────────
fig.suptitle(
    "A rock is an ensemble of minerals; only some of them are magnetic",
    fontsize=15, fontweight="bold", y=0.98,
)
fig.text(
    0.5, 0.918,
    "Bulk susceptibility $k$ and Königsberger ratio $Q$ are weighted averages over the mineral assemblage",
    fontsize=11.5, ha="center", va="bottom", style="italic", color="#444444",
)

# ── Shared mineral-colour legend ──────────────────────────────────
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], marker='o', color='w', label="Ferrimagnetic (magnetite, Fe$_3$O$_4$) — carries remanence",
           markerfacecolor=ACCENT_FERRI, markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label="Antiferromagnetic (hematite, α-Fe$_2$O$_3$) — weak remanence",
           markerfacecolor=ACCENT_HEMA, markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label="Paramagnetic matrix (olivine, biotite, pyroxene) — induced only",
           markerfacecolor=ACCENT_PARA, markersize=12, markeredgecolor='black'),
    Line2D([0], [0], marker='o', color='w', label="Diamagnetic / non-magnetic matrix (quartz, feldspar)",
           markerfacecolor=ACCENT_DIA, markersize=12, markeredgecolor='black'),
]
fig.legend(handles=legend_elements, loc="lower center",
           ncol=2, frameon=True, framealpha=0.95,
           fontsize=11, bbox_to_anchor=(0.5, -0.005))

fig.subplots_adjust(left=0.02, right=0.98, top=0.86, bottom=0.20, wspace=0.18)
fig.tight_layout(rect=[0, 0.10, 1, 0.88])
fig.savefig("../figures/fig_rock_as_ensemble.png",
            dpi=300, bbox_inches="tight")
plt.close(fig)
print("Wrote assets/figures/fig_rock_as_ensemble.png")
