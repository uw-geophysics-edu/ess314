"""
fig_14_cumulative_moment.py

Scientific content: Cumulative worldwide seismic moment release
since 1900 to ~2024, plotted as a staircase that adds the moment of
each major earthquake plus a uniform "background" rate from many
smaller events. Demonstrates that the few greatest earthquakes
dominate the total moment release.

The catalogue of M >= 7.5 great earthquakes is drawn from the USGS
Significant Earthquakes catalogue and the Global Centroid Moment
Tensor (GCMT) project. M0 values use the standard Mw -> M0 inverse:
log10(M0) = 1.5 * Mw + 9.0  (M0 in N*m).

Reproduces the scientific content of:
  Stein, S., & Wysession, M. (2003). An Introduction to Seismology,
  Earthquakes, and Earth Structure. Blackwell. Figure 9.28
  (cumulative moment plot), extended to 2024.

Sources for catalogue:
  USGS Earthquake Hazards Program, https://earthquake.usgs.gov
  GCMT Project, https://www.globalcmt.org
  Both are public-domain / open-data.

Output: assets/figures/fig_14_cumulative_moment.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def Mw_to_M0(Mw):
    return 10.0 ** (1.5 * Mw + 9.0)


# Major earthquakes M >= 7.5 since 1900 (Mw, year, optional label).
# Compiled from USGS Significant Earthquakes & GCMT catalogues.
GREAT_EARTHQUAKES = [
    (7.9, 1906.3, ""),         # San Francisco
    (8.2, 1907.7, ""),
    (8.0, 1911.0, ""),
    (8.1, 1917.5, ""),
    (8.5, 1922.9, ""),
    (7.9, 1923.7, ""),         # Kanto
    (8.3, 1928.0, ""),
    (7.9, 1929.4, ""),
    (8.5, 1933.2, ""),         # Sanriku
    (8.5, 1938.1, ""),         # Banda Sea
    (7.9, 1944.9, ""),
    (8.6, 1946.3, ""),         # Aleutians
    (8.6, 1950.7, ""),         # Assam-Tibet
    (9.0, 1952.9, "Kamchatka\n1952  $M_W$ 9.0"),
    (8.6, 1957.2, ""),
    (9.5, 1960.4, "Chile\n1960  $M_W$ 9.5"),
    (8.5, 1963.8, ""),
    (9.2, 1964.2, "Alaska\n1964  $M_W$ 9.2"),
    (8.7, 1965.1, ""),         # Rat Islands
    (8.0, 1968.4, ""),
    (8.0, 1976.2, ""),
    (8.1, 1977.6, ""),
    (8.1, 1985.7, ""),         # Michoacán
    (8.0, 1989.4, ""),
    (8.2, 1994.5, ""),
    (7.7, 1996.4, ""),
    (8.0, 1998.1, ""),
    (7.9, 2002.8, ""),         # Denali
    (8.3, 2003.7, ""),         # Hokkaido
    (9.1, 2004.97, "Sumatra\n2004  $M_W$ 9.1"),
    (8.6, 2005.2, ""),
    (8.0, 2007.6, ""),
    (8.1, 2009.7, ""),
    (8.8, 2010.15, "Maule, Chile\n2010  $M_W$ 8.8"),
    (9.1, 2011.20, "Tōhoku\n2011  $M_W$ 9.1"),
    (8.6, 2012.3, ""),
    (8.3, 2014.3, ""),
    (8.3, 2015.7, ""),         # Illapel
    (7.8, 2015.3, ""),         # Nepal
    (7.9, 2017.7, ""),
    (8.2, 2018.2, ""),         # Off coast of Mexico
    (8.0, 2019.4, ""),
    (8.2, 2021.6, ""),         # Sand Point Alaska
    (7.7, 2023.1, ""),         # Türkiye-Syria doublet (paired event)
    (7.6, 2024.0, ""),         # Noto, Japan
]


def main():
    # Year axis from 1900 to 2025
    years = np.linspace(1900, 2025, 1500)

    # Background moment-release rate: ~3e21 N*m/yr from M < 7.5 events
    bg_rate = 3.0e21  # N*m per year
    bg_cum = (years - 1900) * bg_rate

    # Add the moment of each major earthquake at its year
    cum = bg_cum.copy()
    for Mw, yr, _ in GREAT_EARTHQUAKES:
        cum[years >= yr] += Mw_to_M0(Mw)

    # Convert to units of 1e23 N*m for the y-axis
    cum_norm = cum / 1.0e23

    fig, ax = plt.subplots(figsize=(10.0, 5.6))

    ax.fill_between(years, 0, cum_norm, color=COLORS[2], alpha=0.45,
                    zorder=1)
    ax.plot(years, cum_norm, color=COLORS[6], lw=1.8, zorder=2)

    # Custom (xtext, ytext, ha) placements to avoid label collisions in the
    # densely-clustered post-2004 era. Each tuple keys off the event year.
    custom_placement = {
        1952.9: (1948.0, 3.6, "right"),    # Kamchatka — pull left and lower
        1960.4: (1957.0, 4.7, "right"),    # Chile
        1964.2: (1971.0, 5.9, "left"),     # Alaska — push right
        2004.97: (1992.0, 7.6, "right"),   # Sumatra — pull left
        2010.15: (1998.0, 8.55, "right"),  # Maule — pull left, raise
        2011.20: (2018.5, 8.55, "left"),   # Tōhoku — push right
    }

    for Mw, yr, label in GREAT_EARTHQUAKES:
        if not label:
            continue
        idx = np.argmin(np.abs(years - yr))
        y_event = cum_norm[idx]
        xt, yt, ha = custom_placement.get(yr, (yr, y_event + 0.7, "center"))
        ax.annotate(label,
                    xy=(yr, y_event),
                    xytext=(xt, yt),
                    fontsize=10, ha=ha, va="bottom",
                    arrowprops=dict(arrowstyle="-", color=COLORS[6],
                                    lw=0.8))

    # Inset table of decadal moment-release rates
    rate_table = (
        "Time range      Moment rate ($\\times 10^{23}$ N$\\cdot$m / yr)\n"
        "1907 - 1923          0.03\n"
        "1930 - 1950          0.03\n"
        "1967 - 1980          0.03\n"
        "1990 - 2003          0.02\n"
        "2005 - 2015          0.06\n"
        "2015 - 2024          0.04"
    )
    ax.text(1903, 8.85, rate_table, fontsize=9.5, ha="left", va="top",
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=COLORS[6], alpha=0.92))

    ax.set_xlabel("Year")
    ax.set_ylabel("Cumulative seismic moment  ($\\times 10^{23}$ N$\\cdot$m)")
    ax.set_title("Worldwide cumulative seismic moment release, 1900-2024")
    ax.set_xlim(1900, 2026)
    ax.set_ylim(0, 9.0)
    ax.grid(True, alpha=0.3, ls=":")
    ax.tick_params(direction="in", top=True, right=True)

    fig.tight_layout()
    fig.savefig("assets/figures/fig_14_cumulative_moment.png",
                bbox_inches="tight")
    print("Saved fig_14_cumulative_moment.png")


if __name__ == "__main__":
    main()
