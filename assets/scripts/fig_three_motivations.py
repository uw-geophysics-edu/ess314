"""
fig_three_motivations.py

Scientific content:
    Three-column schematic showing the three motivating contexts for solid
    Earth geophysics: geodynamics (planetary and landscape evolution), natural
    hazards, and resource management. Each column contains a schematic
    illustration, the key physical process, and the primary observable.

Source: Original pedagogical figure for ESS 314, UW (no external source).

Output: assets/figures/fig_three_motivations.png
License: CC-BY 4.0 (this script)

Colorblind-safe palette (WCAG AA compliant):
  #0072B2 (blue)  #E69F00 (orange)  #009E73 (green)
  #56B4E9 (sky)   #D55E00 (vermilion)  #CC79A7 (pink)
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os

# ── Mandatory font defaults ───────────────────────────────────────────────────
mpl.rcParams.update({
    'font.size': 13,
    'axes.titlesize': 15,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 16,
    'axes.linewidth': 1.2,
})

C_GEO = "#0072B2"
C_HAZ = "#E69F00"
C_RES = "#009E73"
PANEL_BG = "#F8F8F8"


def draw_geodynamics(ax):
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    ax.fill_between([0, 10], [0.6, 0.6], [6.0, 6.0], color="#D4956A", alpha=0.30)
    ax.fill_between([0, 10], [6.0, 6.0], [6.6, 6.6], color="#6DBF8F", alpha=0.80)
    ax.text(5, 6.35, "Surface", ha="center", fontsize=12, color="#333")
    core = plt.Circle((5, 0.55), 0.45, color="#CC79A7", alpha=0.75, zorder=4)
    ax.add_patch(core)
    ax.text(5, 0.55, "Core", ha="center", va="center", fontsize=11,
            color="white", fontweight="bold")
    for cx, side in [(2.5, +1), (7.5, -1)]:
        t = np.linspace(0, 2 * np.pi, 200)
        x = cx + side * 0.65 * np.cos(t)
        y = 3.3 + 1.55 * np.sin(t)
        ax.plot(x, y, color=C_GEO, lw=1.5, alpha=0.80)
        idx = len(t) // 4
        ax.annotate("", xy=(x[idx + 2], y[idx + 2]), xytext=(x[idx], y[idx]),
                    arrowprops=dict(arrowstyle="->", color=C_GEO, lw=1.5))
    plate_x = np.array([6.5, 5.0, 3.8])
    plate_y = np.array([6.0, 4.1, 2.3])
    ax.plot(plate_x, plate_y, color="#333", lw=3.0, solid_capstyle="round")
    ax.annotate("", xy=(4.5, 3.2), xytext=(5.5, 4.8),
                arrowprops=dict(arrowstyle="->", color="#444", lw=1.8))
    ax.text(7.5, 5.7, "Plate", fontsize=12, color="#333", rotation=-5)


def draw_hazards(ax):
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    ax.fill_between([0, 10], [0, 0], [7, 7], color="#ECECEC", alpha=0.7)
    x = np.linspace(0.5, 9.5, 80)
    y = 3.5 + 0.25 * np.sin(3 * np.pi * x / 8)
    ax.plot(x, y, color="#333", lw=2.5, zorder=5)
    for (a, b), col, alp in zip(
            [(2.2, 1.6), (3.8, 2.6), (5.4, 3.6), (7.0, 4.8)],
            ["#D55E00", "#E69F00", "#56B4E9", "#009E73"],
            [0.30, 0.22, 0.16, 0.10]):
        e = mpatches.Ellipse((5, 3.5), a, b, angle=12,
                             facecolor=col, alpha=alp, edgecolor=col,
                             linewidth=0.8, zorder=4)
        ax.add_patch(e)
    ax.plot(5, 3.5, marker="*", ms=16, color="#D55E00", zorder=6,
            markeredgecolor="#9B0000", markeredgewidth=0.6)
    for sx, sy in [(1.5, 5.5), (8.5, 5.5), (1.5, 1.5), (8.5, 1.5)]:
        ax.plot(sx, sy, "^", ms=9, color="#333", zorder=6)
    ax.text(5.4, 4.2, "Epicenter", fontsize=12, color="#9B0000")
    ax.text(5, 0.5, "Shaking intensity (decreasing outward)",
            ha="center", fontsize=11, color="#555", style="italic")


def draw_resources(ax):
    ax.set_xlim(0, 10); ax.set_ylim(0, 7); ax.axis("off")
    colors_l = ["#D4C5A0", "#C0A875", "#A89060", "#8A7250", "#6E5840"]
    bounds = [6.6, 5.5, 4.1, 2.7, 1.5, 0.3]
    for i in range(len(bounds) - 1):
        top, bot = bounds[i], bounds[i + 1]
        x = np.linspace(0, 10, 120)
        wave = 0.08 * np.sin(2 * np.pi * x / 5 + i * 0.7)
        ax.fill_between(x, bot + wave - 0.05, top + wave + 0.05,
                        color=colors_l[i], alpha=0.55)
    tx = np.linspace(5.0, 9.5, 80)
    ty = 1.7 + 0.55 * np.exp(-0.5 * ((tx - 7.2) / 0.9) ** 2)
    ax.fill_between(tx, 0.85, ty, color=C_RES, alpha=0.65, zorder=3)
    ax.plot(tx, ty, color=C_RES, lw=1.5, zorder=4)
    ax.text(7.2, 1.2, "Reservoir", ha="center", fontsize=12,
            color="white", fontweight="bold", zorder=5)
    ax.annotate("", xy=(0.4, 0.6), xytext=(0.4, 6.4),
                arrowprops=dict(arrowstyle="->", color="#555", lw=1.2))
    ax.text(0.15, 3.5, "Depth", fontsize=12, rotation=90, va="center", color="#555")
    for y, lbl in zip([6.6, 5.5, 4.1, 2.7],
                      ["Surface", "Horizon A", "Horizon B", "Horizon C"]):
        ax.text(0.7, y - 0.12, lbl, fontsize=11, va="top", color="#444")


def make_figure():
    fig = plt.figure(figsize=(14, 7.5))
    fig.patch.set_facecolor("white")

    cols = [C_GEO, C_HAZ, C_RES]
    titles = ["Geodynamics\n(Planetary & Landscape Evolution)",
              "Natural Hazards",
              "Resource Management"]
    processes = ["Mantle convection · subduction\nglacial rebound · isostasy",
                 "Fault rupture · seismic wave propagation\nsite amplification · tsunami",
                 "Fluid-bearing reservoirs · stratigraphy\nore bodies · aquifers"]
    observables = ["Seismic velocity (temperature & composition)\ngravity anomaly · heat flow",
                   "Seismograms · GPS displacement\nInSAR · strong-motion records",
                   "Seismic reflection sections · resistivity\ngravity anomaly · EM surveys"]
    drawers = [draw_geodynamics, draw_hazards, draw_resources]

    for col_idx, (col, title, proc, obs, drawer) in enumerate(
            zip(cols, titles, processes, observables, drawers)):
        left = 0.03 + col_idx * 0.335
        ax_fig = fig.add_axes([left, 0.37, 0.30, 0.55])
        ax_fig.set_facecolor(PANEL_BG)
        drawer(ax_fig)
        ax_bar = fig.add_axes([left, 0.925, 0.30, 0.042])
        ax_bar.set_facecolor(col); ax_bar.axis("off")
        ax_bar.text(0.5, 0.5, title, ha="center", va="center",
                    fontsize=13, fontweight="bold", color="white",
                    transform=ax_bar.transAxes)
        ax_txt = fig.add_axes([left, 0.02, 0.30, 0.33])
        ax_txt.set_facecolor("white"); ax_txt.axis("off")
        ax_txt.text(0.5, 0.94, "Key Process:", ha="center", va="top",
                    fontsize=13, fontweight="bold", color=col,
                    transform=ax_txt.transAxes)
        ax_txt.text(0.5, 0.73, proc, ha="center", va="top",
                    fontsize=12, color="#333", transform=ax_txt.transAxes,
                    linespacing=1.5)
        ax_txt.text(0.5, 0.44, "Primary Observable:", ha="center", va="top",
                    fontsize=13, fontweight="bold", color=col,
                    transform=ax_txt.transAxes)
        ax_txt.text(0.5, 0.23, obs, ha="center", va="top",
                    fontsize=12, color="#333", transform=ax_txt.transAxes,
                    linespacing=1.5)

    fig.text(0.5, 0.985, "Three Motivating Contexts for Solid Earth Geophysics",
             ha="center", va="top", fontsize=16, fontweight="bold")

    os.makedirs("assets/figures", exist_ok=True)
    fig.savefig("assets/figures/fig_three_motivations.png", dpi=300,
                bbox_inches="tight", facecolor="white")
    print("Saved: assets/figures/fig_three_motivations.png")
    plt.close(fig)


if __name__ == "__main__":
    make_figure()
