"""
fig_14_richter_amplitude_decay.py

Scientific content: Charles Richter's 1935 empirical observation that
peak seismic-wave amplitudes from different earthquakes decay with
distance along *parallel* curves on log10(A) vs distance plots. The
shape of the curve is a property of the medium (geometric spreading
+ anelastic attenuation); the vertical offset is a property of the
source. This is the foundation of every magnitude scale used since.

Reproduces the scientific content of:
  Stein, S., & Wysession, M. (2003). An Introduction to Seismology,
  Earthquakes, and Earth Structure. Blackwell. Figure 9.23.

Path attenuation model used here is a simplified Hutton-Boore (1987)
Southern California ML calibration:
  -log10(A0(Delta)) = 1.110 * log10(Delta/100) + 0.00189 * (Delta - 100) + 3.0

Output: assets/figures/fig_14_richter_amplitude_decay.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# Global rcParams - mandatory at top of every script
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

# Colorblind-safe palette
COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def neg_log_A0(Delta_km):
    """Hutton-Boore-style ML distance correction."""
    return 1.110 * np.log10(Delta_km / 100.0) + 0.00189 * (Delta_km - 100.0) + 3.0


def main():
    # Three synthetic earthquakes with ML = 4.5, 3.5, 2.5
    rng = np.random.default_rng(42)
    Delta = np.linspace(5, 500, 400)
    decay = -neg_log_A0(Delta)  # log10(A) = ML + decay

    events = [
        {"ML": 4.5, "label": "event 1", "color": COLORS[0],
         "marker": "x", "n": 14},
        {"ML": 3.5, "label": "event 2", "color": COLORS[1],
         "marker": "o", "n": 14},
        {"ML": 2.5, "label": "event 3", "color": COLORS[4],
         "marker": "+", "n": 14},
    ]

    fig, ax = plt.subplots(figsize=(8.4, 5.6))

    for ev in events:
        # Smooth model curve
        ax.plot(Delta, ev["ML"] + decay, color=ev["color"], lw=2.0,
                zorder=3)
        # Scattered observations
        Delta_obs = rng.uniform(20, 480, ev["n"])
        decay_obs = -neg_log_A0(Delta_obs)
        scatter = rng.normal(0, 0.18, ev["n"])
        ax.scatter(Delta_obs, ev["ML"] + decay_obs + scatter,
                   marker=ev["marker"], s=70,
                   facecolor="none" if ev["marker"] == "o" else ev["color"],
                   edgecolor=ev["color"], linewidths=2.0, zorder=4)
        # Right-edge label
        ax.text(Delta[-5] + 8, (ev["ML"] + decay)[-5],
                ev["label"], color=ev["color"], fontsize=12,
                va="center", ha="left", fontweight="bold")

    # Schematic axes - emphasise the shape, not the values
    ax.set_xlabel("Epicentral distance, $\\Delta$ (km)")
    ax.set_ylabel("$\\log_{10}(A)$  [arbitrary units]")
    ax.set_title("Parallel amplitude decay: Richter's foundational observation")
    ax.set_xlim(0, 540)
    ax.set_ylim(-2.5, 3.0)
    ax.grid(True, alpha=0.3, ls=":")
    ax.tick_params(direction="in", top=True, right=True)

    # Annotation explaining the takeaway
    ax.text(0.02, 0.04,
            "The three curves have different vertical offsets but the same shape.\n"
            "Source size is encoded in the offset; path effects in the shape.",
            transform=ax.transAxes, fontsize=11, va="bottom",
            bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                      edgecolor=COLORS[6], alpha=0.9))

    fig.tight_layout()
    fig.savefig("assets/figures/fig_14_richter_amplitude_decay.png",
                bbox_inches="tight")
    print("Saved fig_14_richter_amplitude_decay.png")


if __name__ == "__main__":
    main()
