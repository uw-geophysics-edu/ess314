"""
fig_space_time_scales.py

Scientific content:
    Log-log scatter plot of spatial vs. temporal scales for geophysical
    processes, demonstrating that scale determines the appropriate method
    and that no single technique spans the full range of Earth processes.
    Points are color-coded by motivating context (geodynamics, hazards,
    resources/engineering, multi-context).

Source: Original educational figure for ESS 314, UW.
    Process scales informed by:
    Lowrie & Fichtner (2020). Fundamentals of Geophysics, 3rd ed.
      Cambridge University Press. DOI: 10.1017/9781108685917

Output: assets/figures/fig_space_time_scales.png
License: CC-BY 4.0 (this script)

Colorblind-safe palette (WCAG AA compliant):
  #0072B2 (blue/geodynamics)  #E69F00 (orange/hazards)
  #009E73 (green/resources)   #CC79A7 (pink/multi-context)
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

YEAR = 3.156e7  # seconds per year

C_GEO = "#0072B2"
C_HAZ = "#E69F00"
C_RES = "#009E73"
C_MUL = "#CC79A7"

# (label, km, seconds, color, marker, x_offset_mult, y_offset_mult)
procs = [
    ("Mantle\nconvection",        8000,  2e8 * YEAR, C_GEO, "^", 1.30, 1.10),
    ("Subduction\ndynamics",      2000,  5e7 * YEAR, C_GEO, "^", 1.30, 0.88),
    ("Seismic\ntomography",       5000,  1e7 * YEAR, C_GEO, "^", 0.38, 0.50),
    ("Glacial\nrebound",          1000,  1e4 * YEAR, C_GEO, "^", 1.30, 1.10),
    ("Volcanic arc\nevolution",    500,  1e6 * YEAR, C_GEO, "^", 1.30, 1.10),
    ("Earthquake\ncycle (Cascadia)", 500, 300 * YEAR, C_HAZ, "o", 1.30, 1.10),
    ("Aftershock\nsequence",       50,  YEAR / 10, C_HAZ, "o", 1.30, 1.10),
    ("Local earthquake\n(M2–3)",    1,  1.0,        C_HAZ, "o", 1.30, 1.10),
    ("Seismic P-wave",           1e-3,  1e-3,       C_HAZ, "o", 1.30, 0.65),
    ("Active seismic\nsurvey",   0.05,  0.05,       C_RES, "s", 1.30, 1.10),
    ("Reflection\nsurvey",         30,  3600,       C_RES, "s", 1.30, 1.10),
    ("Gravity\nsurvey",           200,  86400,      C_RES, "s", 1.30, 1.10),
    ("Groundwater\ndepletion",    300,  10 * YEAR,  C_RES, "s", 1.30, 1.10),
    ("Slow-slip event\n(tremor)", 200,  14 * 86400, C_MUL, "D", 1.30, 1.10),
    ("DAS urban\nimaging",       0.01,  60,         C_RES, "s", 1.30, 1.10),
]


def make_figure():
    fig, ax = plt.subplots(figsize=(11, 8))

    for label, km, sec, col, mk, dx, dy in procs:
        ax.scatter(km, sec, s=110, color=col, marker=mk,
                   edgecolors="#333", linewidths=0.6, zorder=5)
        ax.annotate(label, (km, sec), xytext=(km * dx, sec * dy),
                    fontsize=12, color="#333",
                    arrowprops=dict(arrowstyle="-", color="#bbb",
                                   lw=0.7, shrinkA=5, shrinkB=2),
                    zorder=6)

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(3e-4, 3e4)
    ax.set_ylim(3e-4, 1e17)
    ax.set_xlabel("Spatial scale (km)", fontsize=14)
    ax.set_ylabel("Temporal scale (seconds)", fontsize=14)
    ax.grid(True, which="both", ls=":", lw=0.4, color="#ccc", zorder=0)

    # Secondary y-axis with human-readable times
    ax2 = ax.twinx()
    ax2.set_yscale("log"); ax2.set_ylim(ax.get_ylim())
    ytick_s = [1e-3, 1, 60, 3600, 86400,
               YEAR, 1e2 * YEAR, 1e4 * YEAR, 1e6 * YEAR, 1e8 * YEAR]
    ylabels = ["1 ms", "1 s", "1 min", "1 hr", "1 day",
               "1 yr", "100 yr", "10 kyr", "1 Myr", "100 Myr"]
    ax2.set_yticks(ytick_s)
    ax2.set_yticklabels(ylabels, fontsize=12)
    ax2.set_ylabel("Approximate timescale", fontsize=13)

    legend_elements = [
        mpatches.Patch(facecolor=C_GEO, edgecolor="#333", label="Geodynamics"),
        mpatches.Patch(facecolor=C_HAZ, edgecolor="#333", label="Natural Hazards"),
        mpatches.Patch(facecolor=C_RES, edgecolor="#333", label="Resources / Engineering"),
        mpatches.Patch(facecolor=C_MUL, edgecolor="#333", label="Multiple contexts"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", fontsize=12,
              framealpha=0.95, edgecolor="#ccc")

    ax.set_title(
        "Spatial and Temporal Scales of Geophysical Processes\n"
        "Scale determines method — no single technique spans the full range",
        fontsize=15, pad=10
    )

    fig.tight_layout()
    os.makedirs("assets/figures", exist_ok=True)
    fig.savefig("assets/figures/fig_space_time_scales.png", dpi=300,
                bbox_inches="tight", facecolor="white")
    print("Saved: assets/figures/fig_space_time_scales.png")
    plt.close(fig)


if __name__ == "__main__":
    make_figure()
