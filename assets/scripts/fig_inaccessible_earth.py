"""
fig_inaccessible_earth.py

Scientific content:
    Dual-panel scale diagram. Left panel: full Earth depth axis 0–6371 km
    with internal layers labeled; human-accessible depths are invisible at
    this scale. Right panel: zoomed view of the top 80 km showing the
    Mponeng Mine (4 km), the Kola Superdeep Borehole (12.2 km), and a
    typical seismic refraction survey depth (50 km), with a secondary axis
    showing each as a percentage of Earth's radius.

Source: Original educational figure for ESS 314, UW.
    Layer boundary depths from:
    Lowrie & Fichtner (2020). Fundamentals of Geophysics, 3rd ed.
      Cambridge University Press. DOI: 10.1017/9781108685917

Output: assets/figures/fig_inaccessible_earth.png
License: CC-BY 4.0 (this script)

Colorblind-safe palette (WCAG AA compliant):
  #56B4E9 (sky blue)  #009E73 (green)  #E69F00 (orange)
  #D55E00 (vermilion)  #CC79A7 (pink)  #0072B2 (blue)
"""

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
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

EARTH_R = 6371.0  # km

layers = [
    (0,    70,    "Crust\n5–70 km",                     "#56B4E9"),
    (70,   660,   "Upper Mantle\n70–660 km",             "#009E73"),
    (660,  2900,  "Lower Mantle\n660–2900 km",           "#E69F00"),
    (2900, 5150,  "Outer Core (liquid Fe)\n2900–5150 km","#D55E00"),
    (5150, 6371,  "Inner Core (solid Fe)\n5150–6371 km", "#CC79A7"),
]

access = [
    (4.0,   "Mponeng Mine\n(4 km)",              "#D55E00"),
    (12.2,  "Kola Superdeep\nBorehole (12.2 km)","#0072B2"),
    (50.0,  "Seismic refraction\nsurvey (~50 km)","#E69F00"),
]


def make_figure():
    fig = plt.figure(figsize=(12, 8.5))
    fig.patch.set_facecolor("white")

    # ── Left: full Earth ─────────────────────────────────────────────────────
    ax_l = fig.add_axes([0.06, 0.10, 0.34, 0.82])
    ax_l.set_xlim(0, 1); ax_l.set_ylim(0, EARTH_R); ax_l.invert_yaxis()
    ax_l.set_xticks([])
    ax_l.set_ylabel("Depth below surface (km)", fontsize=14)
    ax_l.yaxis.set_major_locator(ticker.MultipleLocator(500))
    ax_l.yaxis.set_minor_locator(ticker.MultipleLocator(100))

    for top, bot, label, color in layers:
        ax_l.axhspan(top, bot, color=color, alpha=0.38, linewidth=0)
        mid = (top + bot) / 2
        ax_l.text(0.5, mid, label, va="center", ha="center",
                  fontsize=12, color="#222", style="italic")
        if bot < EARTH_R:
            ax_l.axhline(bot, color="#777", lw=0.7, ls="--")

    ax_l.axhspan(0, 50, color="#333", alpha=0.18, linewidth=0, zorder=5)
    ax_l.text(0.5, 140, "← zoomed →", va="center", ha="center",
              fontsize=12, color="#555")
    ax_l.set_title("Full Earth scale", fontsize=15, pad=8)

    # ── Right: crustal zoom 0–82 km ──────────────────────────────────────────
    ZOOM = 82
    ax_r = fig.add_axes([0.54, 0.10, 0.40, 0.82])
    ax_r.set_xlim(0, 1); ax_r.set_ylim(0, ZOOM); ax_r.invert_yaxis()
    ax_r.set_xticks([])
    ax_r.set_ylabel("Depth (km)  —  zoomed view", fontsize=14)
    ax_r.yaxis.set_major_locator(ticker.MultipleLocator(10))
    ax_r.yaxis.set_minor_locator(ticker.MultipleLocator(5))

    ax_r.axhspan(0, 70, color="#56B4E9", alpha=0.35, linewidth=0)
    ax_r.axhspan(70, ZOOM, color="#009E73", alpha=0.35, linewidth=0)
    ax_r.axhline(70, color="#777", lw=1.3, ls="--")
    ax_r.text(0.5, 35, "Crust (5–70 km)", va="center", ha="center",
              fontsize=13, color="#222", style="italic")
    ax_r.text(0.5, 76.5, "Upper Mantle begins", va="center", ha="center",
              fontsize=12, color="#222", style="italic")

    for depth, label, col in access:
        ax_r.axhline(depth, color=col, lw=3.0, ls="-", zorder=6)
        xa = 0.04 if depth < 30 else 0.54
        va = "bottom" if depth < 6 else "top"
        dy = -0.9 if va == "bottom" else 0.9
        ax_r.text(xa, depth + dy, label, va=va, ha="left",
                  fontsize=12, color=col, fontweight="bold")

    ax_r.set_title("Crustal zoom (0–80 km)", fontsize=15, pad=8)

    # Secondary axis showing % of R_earth
    ax_r2 = ax_r.twinx()
    ax_r2.set_ylim(0, ZOOM); ax_r2.invert_yaxis()
    pct_ticks = [4, 12.2, 50, 70]
    pct_labels = [f"{100*d/EARTH_R:.2f}%\nof $R_\\oplus$" for d in pct_ticks]
    ax_r2.set_yticks(pct_ticks)
    ax_r2.set_yticklabels(pct_labels, fontsize=12, color="#777")
    ax_r2.set_ylabel("Fraction of Earth's radius", fontsize=13, color="#777")

    fig.text(0.465, 0.92, "zoom →", ha="center", fontsize=13, color="#555",
             style="italic")
    fig.text(0.465, 0.50, "↕", ha="center", fontsize=20, color="#bbb")

    fig.suptitle(
        r"The Inaccessible Earth — Human-Accessible Depths vs. $R_\oplus = 6{,}371$ km",
        fontsize=16, y=0.98, fontweight="bold"
    )

    os.makedirs("assets/figures", exist_ok=True)
    fig.savefig("assets/figures/fig_inaccessible_earth.png", dpi=300,
                bbox_inches="tight", facecolor="white")
    print("Saved: assets/figures/fig_inaccessible_earth.png")
    plt.close(fig)


if __name__ == "__main__":
    make_figure()
