"""
fig_seismic_velocities.py

Scientific content: Horizontal bar chart of representative P-wave velocities
for common Earth and engineering materials. Data compiled from standard
references (Lowrie & Fichtner 2020 Table 3.1; Sheriff & Geldart 1995 Ch. 5).

Replaces: Legacy slide 15 from 314_2023_4_seismic_waves.pdf (velocity table).

Output: assets/figures/fig_seismic_velocities.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Global rcParams ─────────────────────────────────────────────────
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

BLUE   = "#0072B2"
ORANGE = "#E69F00"
SKY    = "#56B4E9"
GREEN  = "#009E73"
VERM   = "#D55E00"
BLACK  = "#000000"


def main():
    # Data: (material, V_P_min, V_P_max, category)
    data = [
        # Crystalline / sedimentary rocks
        ("Basalt",        5400, 6400, "rock"),
        ("Granite",       4800, 5800, "rock"),
        ("Limestone",     4000, 7000, "rock"),
        ("Salt rock",     4200, 5000, "rock"),
        ("Sandstone",     2000, 5500, "rock"),
        ("Shale",         2000, 4500, "rock"),
        # Unconsolidated
        ("Wet sand",       200, 1800, "sediment"),
        ("Dry sand",       120,  270, "sediment"),
        ("Clay ($V_S$)",    60,  150, "sediment"),
        # Fluids
        ("Seawater",      1530, 1530, "fluid"),
        ("Freshwater",    1480, 1480, "fluid"),
        # Engineering / other
        ("Steel",         5900, 5900, "other"),
        ("Aluminum",      6400, 6400, "other"),
        ("Ice",           3000, 4000, "other"),
    ]

    materials = [d[0] for d in data]
    vmin = [d[1] for d in data]
    vmax = [d[2] for d in data]
    cats = [d[3] for d in data]

    cat_colors = {
        "rock":     BLUE,
        "sediment": SKY,
        "fluid":    GREEN,
        "other":    ORANGE,
    }
    cat_labels = {
        "rock":     "Crystalline & sedimentary rocks",
        "sediment": "Unconsolidated sediments",
        "fluid":    "Fluids",
        "other":    "Engineering materials",
    }

    fig, ax = plt.subplots(figsize=(10, 7))

    y_pos = np.arange(len(materials))
    bar_heights = [mx - mn for mn, mx in zip(vmin, vmax)]
    colors = [cat_colors[c] for c in cats]

    # Draw bars (horizontal)
    bars = ax.barh(y_pos, bar_heights, left=vmin, height=0.6,
                   color=colors, edgecolor="white", linewidth=0.5)

    # For single-value entries (range = 0), draw a marker instead
    for i, (mn, mx) in enumerate(zip(vmin, vmax)):
        if mx - mn < 50:
            ax.plot(mn, y_pos[i], "D", color=colors[i], markersize=8, zorder=5)

    ax.set_yticks(y_pos)
    ax.set_yticklabels(materials)
    ax.invert_yaxis()
    ax.set_xlabel("$V_P$ (m/s)", fontsize=13)
    ax.set_title("Representative P-wave Velocities", fontsize=14, fontweight="bold")
    ax.set_xlim(0, 8000)

    # Legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=cat_colors[c], label=cat_labels[c])
                       for c in ["rock", "sediment", "fluid", "other"]]
    ax.legend(handles=legend_elements, loc="lower right", fontsize=11,
              framealpha=0.9)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.savefig("assets/figures/fig_seismic_velocities.png")
    plt.close()
    print("Saved: assets/figures/fig_seismic_velocities.png")


if __name__ == "__main__":
    main()
