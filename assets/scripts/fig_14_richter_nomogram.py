"""
fig_14_richter_nomogram.py

Scientific content: The Richter nomogram. Shows how the local
magnitude ML is read from a station record by combining the peak
log-amplitude with the empirical distance correction -log10(A0(Delta)).
Three smooth curves of constant ML are drawn at ML = 2, 3, 4. The
dashed vertical line marks Richter's calibration distance of 100 km.

Reproduces the scientific content of:
  Lowrie, W., & Fichtner, A. (2020). Fundamentals of Geophysics
  (3rd ed.), Chapter 3. Cambridge University Press.

Distance correction:
  -log10(A0(Delta)) = 1.110*log10(Delta/100) + 0.00189*(Delta-100) + 3.0
  (Hutton & Boore 1987, BSSA 77: 2074-2094, Southern California
  calibration)

Output: assets/figures/fig_14_richter_nomogram.png
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


def neg_log_A0(Delta_km):
    return 1.110 * np.log10(Delta_km / 100.0) + 0.00189 * (Delta_km - 100.0) + 3.0


def main():
    Delta = np.linspace(5, 600, 600)
    decay = -neg_log_A0(Delta)

    fig, ax = plt.subplots(figsize=(7.6, 5.4))

    for i, (ML, ls) in enumerate(zip([4.0, 3.0, 2.0], ["-", "-", "-"])):
        logA = ML + decay
        ax.plot(Delta, logA, color=COLORS[i], lw=2.4, ls=ls,
                label=f"$M_L$ = {ML:.1f}")
        # Right-edge label
        ax.text(615, logA[-1], f"$M_L$ = {ML:.1f}",
                color=COLORS[i], fontsize=12, fontweight="bold",
                va="center", ha="left")

    # Calibration reference line at 100 km
    ax.axvline(100, color=COLORS[6], ls="--", lw=1.0, alpha=0.7)
    ax.text(102, 2.6, "$\\Delta = 100$ km\n(Richter's\ncalibration)",
            fontsize=10, va="top", ha="left",
            color=COLORS[6], alpha=0.85)

    # Mark M_L = 3, A = 1 mm @ 100 km (the calibration anchor)
    ax.plot(100, 0.0, marker="o", markersize=10,
            markerfacecolor=COLORS[1], markeredgecolor=COLORS[6],
            markeredgewidth=1.5, zorder=5)
    ax.annotate("$M_L = 3$ at $A = 1$ mm,\n$\\Delta = 100$ km",
                xy=(100, 0.0), xytext=(180, -1.0),
                fontsize=10,
                arrowprops=dict(arrowstyle="->", color=COLORS[6], lw=1.0))

    ax.set_xlabel("Epicentral distance, $\\Delta$ (km)")
    ax.set_ylabel("$\\log_{10}(A)$  [Wood-Anderson amplitude, mm]")
    ax.set_title("Reading the Richter local magnitude")
    ax.set_xlim(0, 660)
    ax.set_ylim(-2.5, 3.0)
    ax.grid(True, alpha=0.3, ls=":")
    ax.tick_params(direction="in", top=True, right=True)

    fig.tight_layout()
    fig.savefig("assets/figures/fig_14_richter_nomogram.png",
                bbox_inches="tight")
    print("Saved fig_14_richter_nomogram.png")


if __name__ == "__main__":
    main()
