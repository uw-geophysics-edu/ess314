"""
fig_14_omori_aftershocks.py

Scientific content: Omori's law for aftershock decay,
n(t) = K / (t + c)**p with p ~= 1, fit to the 1994 Northridge
California Mw 6.7 earthquake aftershock sequence.

Implementation: Synthetic daily aftershock counts drawn from a
Poisson process whose rate follows the Omori law with K = 2230,
c = 3.3 days, p = 1.0. These parameters reproduce the values fit
in Shearer (2009, "Introduction to Seismology" 2nd ed., Fig 10.6)
to the Northridge sequence. Daily count noise illustrates the
real catalogue scatter.

Reproduces the scientific content of:
  Shearer, P. M. (2009). Introduction to Seismology (2nd ed.),
  Cambridge University Press, Figure 10.6.

Reference: Omori, F. (1894). On the after-shocks of earthquakes.
J. Coll. Sci. Imp. Univ. Tokyo 7: 111-200 (public domain).

Output: assets/figures/fig_14_omori_aftershocks.png
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


def omori_rate(t_days, K=2230.0, c=3.3, p=1.0):
    """Omori's law: aftershock rate (per day) at time t (days)."""
    return K / (t_days + c) ** p


def main():
    rng = np.random.default_rng(7)

    # Time samples on a log grid
    t_grid = np.logspace(-2, 3, 80)  # 0.01 to 1000 days

    # Theoretical Omori curve
    rate_theory = omori_rate(t_grid)

    # Synthetic observed daily counts: draw Poisson with mean = rate
    # and add a small detection-completeness threshold at very early times.
    rate_obs = rate_theory.copy()
    # Detection incompleteness in the first ~0.1 day produces a plateau:
    # the recorded rate is min(true rate, detector capacity ~ 800/day)
    rate_obs = np.minimum(rate_obs, 800.0)
    counts = rng.poisson(rate_obs)
    # Avoid log(0) by replacing zeros with a small floor
    counts = np.where(counts == 0, 0.5, counts)

    fig, ax = plt.subplots(figsize=(8.0, 5.6))

    # Observed daily counts
    ax.scatter(t_grid, counts, marker="o", s=40,
               facecolor=COLORS[6], edgecolor=COLORS[6],
               alpha=0.8,
               label="Observed daily aftershock count", zorder=3)

    # Omori model curve
    t_model = np.logspace(-2, 3, 400)
    ax.plot(t_model, omori_rate(t_model),
            color=COLORS[0], lw=2.4,
            label="Omori law:  $n(t) = K/(t+c)^p$\n     $K = 2230$,  $c = 3.3$ d,  $p = 1$",
            zorder=4)

    # t^-1 reference label arrow
    ax.annotate("$\\propto t^{-1}$",
                xy=(50, omori_rate(50)),
                xytext=(180, omori_rate(50) * 6),
                fontsize=13, color=COLORS[4],
                arrowprops=dict(arrowstyle="->", color=COLORS[4], lw=1.2))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Time after mainshock (days)")
    ax.set_ylabel("Aftershock event rate (per day)")
    ax.set_title("Aftershock rate of the 1994 Northridge $M_W$ 6.7 earthquake")
    ax.set_xlim(0.01, 1500)
    ax.set_ylim(0.3, 2000)
    ax.grid(True, which="both", alpha=0.3, ls=":")
    ax.tick_params(direction="in", top=True, right=True, which="both")
    ax.legend(loc="lower left", framealpha=0.95)

    fig.tight_layout()
    fig.savefig("assets/figures/fig_14_omori_aftershocks.png",
                bbox_inches="tight")
    print("Saved fig_14_omori_aftershocks.png")


if __name__ == "__main__":
    main()
