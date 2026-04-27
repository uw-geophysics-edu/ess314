"""
fig_14_energy_christmas_tree.py

Scientific content: The IRIS earthquake "Christmas tree" — a
combined plot showing on a single magnitude axis (a) the annual
worldwide frequency of earthquakes at each magnitude, and (b) the
equivalent chemical-explosive energy (kilograms of TNT). Notable
historical earthquakes are anchored at their magnitude. Energy
scales as 10^(1.5 * M) so each magnitude unit is a factor of ~32
in energy.

Reproduces the scientific content of:
  IRIS / EarthScope (2024). "How often do earthquakes occur?"
  educational poster (CC-BY).
  https://www.iris.edu/hq/inclass/lesson/earthquakes_largest

Output: assets/figures/fig_14_energy_christmas_tree.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 12,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def annual_count(M):
    """Annual worldwide cumulative count for magnitude >= M (b=1, a~=8.5)."""
    return 10 ** (8.5 - 1.0 * M)


def energy_kg_tnt(M):
    """Equivalent kilograms of TNT for an earthquake of magnitude M.
    E (joules) = 10**(1.5 * M + 4.8); 1 kg TNT = 4.184e6 J.
    """
    E_joules = 10 ** (1.5 * M + 4.8)
    return E_joules / 4.184e6


def main():
    M_axis = np.linspace(2.0, 10.0, 200)
    # The "tree width" at each magnitude is proportional to log(annual count)
    width = np.log10(annual_count(M_axis))
    # Clamp negative widths (very high M) to a minimum so the tree stays visible
    width = np.maximum(width, 0.2)

    fig, ax = plt.subplots(figsize=(10.5, 7.0))

    # Fill the tree shape
    ax.fill_betweenx(M_axis, -width, +width, color="#D5D5D5",
                     edgecolor=COLORS[6], linewidth=1.2, zorder=1)

    # Notable earthquakes at left
    eqs_left = [
        (9.5, "Chile 1960"),
        (9.2, "Alaska 1964"),
        (9.1, "Tōhoku 2011 / Sumatra 2004"),
        (8.6, "Sumatra 2005 / 1957 Aleutians"),
        (8.0, "$M_W$ 8 class"),
        (7.9, "San Francisco 1906"),
        (6.9, "Loma Prieta 1989"),
        (6.7, "Northridge 1994"),
        (6.0, "Moderate"),
        (5.0, "Light"),
        (4.0, "Minor"),
    ]
    for mag, label in eqs_left:
        w = max(np.log10(annual_count(mag)), 0.3)
        ax.plot(-w, mag, marker="o", markersize=7,
                markerfacecolor=COLORS[6], markeredgecolor=COLORS[6],
                zorder=4)
        ax.text(-w - 0.4, mag, label, fontsize=10,
                ha="right", va="center", color=COLORS[6])

    # Energy equivalents at right
    energy_pts = [
        (10.0, "56 trillion kg TNT"),
        (9.0, "1.8 billion kg TNT"),
        (8.0, "56 million kg TNT  (Krakatoa eruption)"),
        (7.0, "1.8 million kg TNT  (largest nuclear test)"),
        (6.0, "56 000 kg TNT  (Hiroshima atomic bomb)"),
        (5.0, "1 800 kg TNT  (average tornado)"),
        (4.0, "56 kg TNT"),
        (3.0, "1.8 kg TNT  (large lightning bolt)"),
        (2.0, "56 g TNT"),
    ]
    for mag, label in energy_pts:
        w = max(np.log10(annual_count(mag)), 0.3)
        ax.plot(w, mag, marker="s", markersize=6,
                markerfacecolor=COLORS[1], markeredgecolor=COLORS[6],
                zorder=4)
        ax.text(w + 0.4, mag, label, fontsize=10,
                ha="left", va="center", color=COLORS[6])

    # Horizontal "frequency" annotations along the centre line
    freq_pts = [
        (8.5, "1 per year"),
        (7.5, "15 per year"),
        (6.5, "134 per year"),
        (5.5, "1 300 per year"),
        (4.5, "13 000 per year"),
        (3.5, "130 000 per year"),
        (2.5, "1 300 000 per year"),
    ]
    for mag, label in freq_pts:
        ax.text(0, mag, label, fontsize=9.5,
                ha="center", va="center", color=COLORS[0],
                bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                          edgecolor=COLORS[0], alpha=0.92))

    # Header labels
    ax.text(-3.5, 10.0, "Earthquakes",
            fontsize=14, ha="right", va="bottom",
            fontweight="bold", color=COLORS[6])
    ax.text(3.5, 10.0, "Energy equivalent",
            fontsize=14, ha="left", va="bottom",
            fontweight="bold", color=COLORS[6])
    ax.text(0.0, 10.0, "Annual worldwide rate",
            fontsize=12, ha="center", va="bottom",
            fontweight="bold", color=COLORS[0])

    ax.set_ylim(1.5, 10.6)
    ax.set_xlim(-9.0, 9.0)
    ax.set_ylabel("Magnitude")
    ax.set_xticks([])
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(direction="in", left=True, right=False, top=False)
    ax.set_title("Earthquake size, frequency, and energy on one diagram")

    fig.tight_layout()
    fig.savefig("assets/figures/fig_14_energy_christmas_tree.png",
                bbox_inches="tight")
    print("Saved fig_14_energy_christmas_tree.png")


if __name__ == "__main__":
    main()
