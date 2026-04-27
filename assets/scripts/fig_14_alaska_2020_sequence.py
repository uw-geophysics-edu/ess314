"""
fig_14_alaska_2020_sequence.py

Scientific content: Magnitude-vs-time view of the 2020 Alaska
Peninsula subduction-zone earthquake sequence. Two large events
mark the sequence:
  - Mw 7.8 Simeonof earthquake on 22 July 2020
  - Mw 7.6 Sand Point earthquake on 19 October 2020
Each is followed by a decaying aftershock cloud whose density
reflects Omori's law. The two clusters are partly overlapping in
time, illustrating that aftershock sequences from neighbouring
patches superpose.

Synthetic catalogue: We generate aftershock times from an
inhomogeneous Poisson process with rate following Omori's law,
seeded after each mainshock. Aftershock magnitudes are drawn from a
Gutenberg-Richter distribution with b = 0.95 and a maximum
magnitude one unit below the mainshock (Bath's law). Background
seismicity is drawn at uniform low rate. The synthetic catalogue
matches the real USGS ComCat catalogue qualitatively and is used
here for pedagogical purposes only.

Real catalogue available from USGS ComCat at:
  https://earthquake.usgs.gov/earthquakes/search/

Output: assets/figures/fig_14_alaska_2020_sequence.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

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


def gr_magnitudes(n, mmin=1.5, mmax=6.5, b=0.95, rng=None):
    """Sample n magnitudes from a truncated Gutenberg-Richter distribution."""
    if rng is None:
        rng = np.random.default_rng(0)
    u = rng.uniform(0, 1, n)
    # Inverse CDF for truncated GR with b-value
    beta = b * np.log(10)
    return mmin - np.log(1 - u * (1 - np.exp(-beta * (mmax - mmin)))) / beta


def omori_times(n_total, K, c, p, t_window, rng):
    """Sample n_total event times (days after mainshock) from Omori rate."""
    # Cumulative Omori: N(t) = K * ((t+c)^(1-p) - c^(1-p)) / (1-p)  (p != 1)
    # For p = 1: N(t) = K * (log(t+c) - log(c))
    # Use rejection sampling for safety.
    # Maximum rate is at t = 0 -> K/c^p
    max_rate = K / c ** p
    # Generate candidate times uniformly in [0, t_window], accept with prob rate/max_rate
    times = []
    while len(times) < n_total:
        n_try = (n_total - len(times)) * 3
        t_try = rng.uniform(0, t_window, n_try)
        accept_prob = (K / (t_try + c) ** p) / max_rate
        keep = rng.uniform(0, 1, n_try) < accept_prob
        times.extend(t_try[keep])
    return np.array(times[:n_total])


def main():
    rng = np.random.default_rng(2020)

    # Mainshocks
    t_M78 = datetime(2020, 7, 22, 6, 12)  # M7.8 Simeonof
    t_M76 = datetime(2020, 10, 19, 20, 54)  # M7.6 Sand Point

    # Background seismicity, July-November 2020
    t_start = datetime(2020, 7, 1)
    t_end = datetime(2020, 11, 15)
    days_total = (t_end - t_start).days
    n_bg = 300
    bg_times = rng.uniform(0, days_total, n_bg)
    bg_mags = gr_magnitudes(n_bg, mmin=1.5, mmax=4.0, b=1.05, rng=rng)
    bg_dates = [t_start + timedelta(days=t) for t in bg_times]

    # Aftershocks of M7.8 (decay window ~120 days)
    n_after_78 = 1100
    aft_78_days = omori_times(n_after_78, K=400, c=0.05, p=1.0,
                              t_window=120, rng=rng)
    aft_78_mags = gr_magnitudes(n_after_78, mmin=1.5, mmax=6.1, b=0.95, rng=rng)
    aft_78_dates = [t_M78 + timedelta(days=t) for t in aft_78_days]

    # Aftershocks of M7.6 (decay window ~30 days)
    n_after_76 = 600
    aft_76_days = omori_times(n_after_76, K=380, c=0.05, p=1.0,
                              t_window=30, rng=rng)
    aft_76_mags = gr_magnitudes(n_after_76, mmin=1.5, mmax=5.8, b=0.95, rng=rng)
    aft_76_dates = [t_M76 + timedelta(days=t) for t in aft_76_days]

    # Combine
    all_dates = bg_dates + aft_78_dates + aft_76_dates
    all_mags = np.concatenate([bg_mags, aft_78_mags, aft_76_mags])

    # Filter to time window
    keep = [(d >= t_start) and (d <= t_end) for d in all_dates]
    all_dates = [d for d, k in zip(all_dates, keep) if k]
    all_mags = all_mags[keep]

    fig, ax = plt.subplots(figsize=(10.0, 5.4))

    # Aftershocks/background as open squares with size scaling with magnitude
    sizes = 4 ** all_mags / 8  # exaggerated for visibility
    ax.scatter(all_dates, all_mags, s=sizes, marker="s",
               facecolor="none", edgecolor=COLORS[6],
               linewidths=0.7, alpha=0.65, zorder=2)

    # Mainshocks as gold stars
    ax.scatter([t_M78], [7.8], marker="*", s=600,
               facecolor="#FFD400", edgecolor=COLORS[6],
               linewidths=1.5, zorder=5, label="$M_W$ 7.8 mainshock")
    ax.scatter([t_M76], [7.6], marker="*", s=600,
               facecolor="#FFD400", edgecolor=COLORS[6],
               linewidths=1.5, zorder=5)

    # Annotations
    ax.annotate("$M_W$ 7.8 Simeonof\n22 July 2020",
                xy=(t_M78, 7.8), xytext=(t_M78 + timedelta(days=2), 7.95),
                fontsize=11, ha="left", va="bottom",
                arrowprops=dict(arrowstyle="-", color=COLORS[6], lw=0.8))
    ax.annotate("$M_W$ 7.6 Sand Point\n19 October 2020",
                xy=(t_M76, 7.6), xytext=(t_M76 - timedelta(days=22), 7.85),
                fontsize=11, ha="right", va="bottom",
                arrowprops=dict(arrowstyle="-", color=COLORS[6], lw=0.8))

    # Format x-axis
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
    ax.xaxis.set_minor_locator(mdates.WeekdayLocator())
    ax.set_xlim(t_start, t_end)
    ax.set_ylim(1.0, 8.3)
    ax.set_xlabel("Time, 2020")
    ax.set_ylabel("Magnitude")
    ax.set_title("2020 Alaska Peninsula sequence: superposed Omori-law aftershock decays")
    ax.grid(True, alpha=0.3, ls=":")
    ax.tick_params(direction="in", top=True, right=True)

    # Mark the year boundary
    ax.text(0.99, 0.04, "(synthetic catalogue, Omori + GR scaled to event)",
            transform=ax.transAxes, fontsize=9, ha="right", va="bottom",
            color=COLORS[6], alpha=0.7, fontstyle="italic")

    fig.tight_layout()
    fig.savefig("assets/figures/fig_14_alaska_2020_sequence.png",
                bbox_inches="tight")
    print("Saved fig_14_alaska_2020_sequence.png")


if __name__ == "__main__":
    main()
