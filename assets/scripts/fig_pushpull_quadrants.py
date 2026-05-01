"""
fig_pushpull_quadrants.py

Scientific content: First-motion polarity around an earthquake source.
Shows a vertical strike-slip fault in map view with the four quadrants
of compression and dilatation, three example seismic stations, and the
corresponding first-motion polarities on their vertical-component
seismograms.

Reproduces (and pivots from) the conceptual content of:
  Plummer, McGeary & Carlson (2003). Physical Geology, 9th ed.
  Figures 4.2-4 and 7.14.  W.W. Norton.  (Copyrighted; not reproduced.)
  Stein & Wysession (2003). An Introduction to Seismology,
  Earthquakes, and Earth Structure. Blackwell. §4.2.

Output: assets/figures/fig_pushpull_quadrants.png
License: CC-BY 4.0 (this script).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrow, Wedge

# -- Global rcParams (mandatory) -----------------------------------------
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

# Colorblind-safe palette (WCAG AA)
C_PUSH = "#D55E00"   # vermilion - compression
C_PULL = "#0072B2"   # blue - dilatation
C_FAULT = "#000000"  # black - fault trace
C_AUX = "#666666"    # mid-grey - auxiliary plane


def main(out_path: str = "assets/figures/fig_pushpull_quadrants.png") -> None:
    fig = plt.figure(figsize=(11.5, 5.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.05, 1.0], wspace=0.32)

    # ---------------- Panel A: Map view, four quadrants ----------------
    ax = fig.add_subplot(gs[0, 0])

    # Background quadrants:  fault strikes N-S; auxiliary plane E-W.
    # For a right-lateral N-S fault (n_hat = x, d_hat = y) the moment
    # tensor has only M_xy = M_yx components, so the P-wave radiation
    # pattern is F^P ~ sin(2*phi) for horizontal takeoff azimuth phi
    # measured from north.  Compression (F^P > 0) sits in NE & SW
    # quadrants; dilatation (F^P < 0) in NW & SE.
    R = 1.0
    # matplotlib Wedge angles are measured CCW from +x = east:
    #   0-90  -> NE (compression)
    #   90-180 -> NW (dilatation)
    #   180-270 -> SW (compression)
    #   270-360 -> SE (dilatation)
    ax.add_patch(Wedge((0, 0), R, 0, 90, color=C_PUSH, alpha=0.32))
    ax.add_patch(Wedge((0, 0), R, 180, 270, color=C_PUSH, alpha=0.32))
    ax.add_patch(Wedge((0, 0), R, 90, 180, color=C_PULL, alpha=0.32))
    ax.add_patch(Wedge((0, 0), R, 270, 360, color=C_PULL, alpha=0.32))

    # Fault plane (N-S) + auxiliary plane (E-W)
    ax.plot([0, 0], [-R, R], color=C_FAULT, lw=3.0, label="Fault plane")
    ax.plot([-R, R], [0, 0], color=C_AUX, lw=2.0, ls="--",
            label="Auxiliary plane")

    # Slip arrows (right-lateral): east block moves north, west block south
    ax.annotate("", xy=(0.18, 0.28), xytext=(0.18, -0.28),
                arrowprops=dict(arrowstyle="->", lw=2.2, color=C_FAULT))
    ax.annotate("", xy=(-0.18, -0.28), xytext=(-0.18, 0.28),
                arrowprops=dict(arrowstyle="->", lw=2.2, color=C_FAULT))

    # Quadrant labels (NE & SW are now compressional, NW & SE dilatational)
    ax.text(0.55, 0.55, "compression\n(push)", color=C_PUSH,
            ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(-0.55, -0.55, "compression\n(push)", color=C_PUSH,
            ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(-0.55, 0.55, "dilatation\n(pull)", color=C_PULL,
            ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(0.55, -0.55, "dilatation\n(pull)", color=C_PULL,
            ha="center", va="center", fontsize=12, fontweight="bold")

    # Three example stations: pick one per polarity-defining quadrant.
    # Sta 1 (NW): dilatation -> first motion DOWN.
    # Sta 2 (NE): compression -> first motion UP.
    # Sta 3 (SE): dilatation -> first motion DOWN.
    stations = [(-0.78, 0.42, "1"), (0.55, 0.72, "2"), (0.82, -0.36, "3")]
    for sx, sy, lbl in stations:
        ax.plot(sx, sy, marker="^", color="white", markeredgecolor="black",
                markersize=12, markeredgewidth=1.5, zorder=5)
        ax.text(sx + 0.04, sy + 0.06, lbl, fontsize=12, fontweight="bold")

    # Epicenter
    ax.plot(0, 0, marker="*", color="#FFD700", markeredgecolor="black",
            markersize=20, markeredgewidth=1.0, zorder=6)

    # North arrow (top-left of the panel)
    ax.annotate("", xy=(-0.92, 0.95), xytext=(-0.92, 0.78),
                arrowprops=dict(arrowstyle="->", lw=1.6, color="black"))
    ax.text(-0.92, 1.00, "N", ha="center", va="bottom",
            fontsize=12, fontweight="bold")

    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.set_title("(a) Map view: right-lateral N-S fault")
    ax.legend(loc="lower left", framealpha=0.92, fontsize=10)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ["top", "right", "bottom", "left"]:
        ax.spines[s].set_visible(False)

    # ---------------- Panel B: Three station seismograms ----------------
    ax2 = fig.add_subplot(gs[0, 1])

    t = np.linspace(0, 4.0, 1200)
    # Synthetic P pulse: Ricker wavelet
    def ricker(t, t0=0.7, f=4.0):
        a = (np.pi * f * (t - t0)) ** 2
        return (1.0 - 2.0 * a) * np.exp(-a)

    # Station polarities:
    # Sta 1 (NW, dilatation) -> DOWN
    # Sta 2 (NE, compression) -> UP
    # Sta 3 (SE, dilatation) -> DOWN
    polarities = [(-1, "DOWN", C_PULL),
                  (+1, "UP",   C_PUSH),
                  (-1, "DOWN", C_PULL)]

    yshift = [2.5, 0.0, -2.5]
    for k, ((pol, txt, col), ys) in enumerate(zip(polarities, yshift)):
        rng = np.random.default_rng(seed=42 + k)
        coda = 0.06 * rng.standard_normal(t.size)
        coda *= np.where(t > 1.0, np.exp(-(t - 1.0) / 1.6), 0)
        wave = pol * ricker(t) + coda
        ax2.plot(t, wave + ys, color="black", lw=1.0)
        ax2.axhline(ys, color="#999999", lw=0.6, ls=":")
        ax2.text(-0.18, ys, f"Sta {k + 1}", fontsize=12,
                 fontweight="bold", va="center", ha="right")
        # Compact polarity badge to the right of each trace, no arrow overlap
        badge = "↑ UP\n(compression)" if pol > 0 else "↓ DOWN\n(dilatation)"
        ax2.text(3.55, ys, badge, fontsize=10, color=col,
                 fontweight="bold", va="center", ha="left",
                 bbox=dict(boxstyle="round,pad=0.25", fc="white",
                          ec=col, lw=1.0))

    ax2.set_xlim(-0.05, 5.4)
    ax2.set_ylim(-4.2, 4.2)
    ax2.set_xticks([0, 1, 2, 3])
    ax2.set_xlabel("Time after origin (s)")
    ax2.set_yticks([])
    ax2.set_title("(b) Vertical-component seismograms")
    for s in ["top", "right", "left"]:
        ax2.spines[s].set_visible(False)

    fig.suptitle("Quadrants of compression and dilatation around a fault",
                 fontsize=15, y=1.02)
    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    main()
