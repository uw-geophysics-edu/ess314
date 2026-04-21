"""
fig_12_tomography_raycones.py

Scientific content: The geometric core idea of seismic tomography.
Rays from a single earthquake illuminate a velocity anomaly along a
"cone" of possible locations; rays from a second earthquake illuminate
a different cone; the intersection of cones from many earthquakes and
many stations localises the anomaly. This is why source-receiver
coverage controls spatial resolution.

Reproduces the scientific content of:
  Thurber, C.H., 2003. Seismic tomography of the lithosphere with body
  waves. Pure and Applied Geophysics 160, 717-737.
  https://doi.org/10.1007/PL00012555

Output: assets/figures/fig_12_tomography_raycones.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

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


def draw_panel(ax, n_sources, anomaly_xy=(0.50, 0.55),
               anomaly_size=(0.12, 0.12),
               sources_xy=[(-0.45, -0.40)],
               title=""):
    """Draw a schematic panel with stations (triangles), one or two
    sources (stars), and ray cones illuminating the anomaly."""
    # Box
    ax.add_patch(Rectangle((-1.0, -1.0), 2.0, 2.0, fill=False,
                           edgecolor=COLORS[6], lw=1.2))
    # Stations across the top
    n_sta = 11
    station_x = np.linspace(-0.85, 0.85, n_sta)
    station_y = np.full(n_sta, 0.95)
    for sx in station_x:
        ax.plot(sx, 0.95, marker="^", color=COLORS[6],
                markersize=9, markeredgecolor=COLORS[6])

    # Anomaly (square)
    ax_cx, ax_cy = anomaly_xy
    aw, ah = anomaly_size
    ax.add_patch(Rectangle((ax_cx - aw / 2, ax_cy - ah / 2), aw, ah,
                           facecolor="#D55E00", alpha=0.65,
                           edgecolor=COLORS[4], lw=1.5, zorder=4))

    # Cone(s): for each source, find the set of stations whose rays
    # pass through the anomaly bounding box
    cone_colors = [COLORS[0], COLORS[3]]
    for i, (sx, sy) in enumerate(sources_xy[:n_sources]):
        # Source marker
        ax.plot(sx, sy, marker="*", color=COLORS[4], markersize=18,
                markeredgecolor=COLORS[6], zorder=5)

        # Determine which stations have rays that pass through the anomaly
        hit_stations = []
        for stx, sty in zip(station_x, station_y):
            # Parametric ray from source to station: (sx,sy) -> (stx,sty)
            # Sample along ray and check if any point is inside anomaly
            t = np.linspace(0, 1, 100)
            rx = sx + t * (stx - sx)
            ry = sy + t * (sty - sy)
            in_anom = np.any(
                (rx > ax_cx - aw / 2) & (rx < ax_cx + aw / 2)
                & (ry > ax_cy - ah / 2) & (ry < ax_cy + ah / 2)
            )
            if in_anom:
                hit_stations.append((stx, sty))

        # Draw all rays thinly
        for stx, sty in zip(station_x, station_y):
            ax.plot([sx, stx], [sy, sty], color=COLORS[6],
                    lw=0.4, alpha=0.30, zorder=1)

        # Highlight cone
        if len(hit_stations) >= 2:
            left = hit_stations[0]
            right = hit_stations[-1]
            cone_poly = Polygon([(sx, sy), left, right], closed=True,
                                facecolor=cone_colors[i], alpha=0.20,
                                edgecolor=cone_colors[i], lw=1.2, zorder=2)
            ax.add_patch(cone_poly)
            # Thicker rays
            for stx, sty in hit_stations:
                ax.plot([sx, stx], [sy, sty], color=cone_colors[i],
                        lw=1.4, alpha=0.85, zorder=3)

    # Labels
    ax.text(ax_cx, ax_cy + ah / 2 + 0.05, "velocity anomaly",
            ha="center", va="bottom", fontsize=10, color=COLORS[4],
            fontweight="bold")
    for i, (sx, sy) in enumerate(sources_xy[:n_sources]):
        ax.text(sx, sy - 0.06, f"source {i + 1}",
                ha="center", va="top", fontsize=10, color=COLORS[6])

    ax.set_xlim(-1.05, 1.05)
    ax.set_ylim(-1.05, 1.05)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, color=COLORS[6], fontsize=13)


def main(outpath):
    fig, axes = plt.subplots(1, 3, figsize=(14.5, 5.3))

    draw_panel(axes[0], n_sources=1,
               sources_xy=[(-0.60, -0.55)],
               anomaly_xy=(0.10, 0.35),
               anomaly_size=(0.18, 0.18),
               title="(a) One earthquake: illuminate the anomaly along a cone")

    draw_panel(axes[1], n_sources=1,
               sources_xy=[(0.55, -0.60)],
               anomaly_xy=(0.10, 0.35),
               anomaly_size=(0.18, 0.18),
               title="(b) A second earthquake: a different cone")

    draw_panel(axes[2], n_sources=2,
               sources_xy=[(-0.60, -0.55), (0.55, -0.60)],
               anomaly_xy=(0.10, 0.35),
               anomaly_size=(0.18, 0.18),
               title="(c) Intersecting cones localise the anomaly")

    fig.suptitle(
        "Seismic tomography: using many earthquakes and many stations "
        "to localise subsurface velocity anomalies",
        y=1.00, color=COLORS[6], fontsize=14,
    )
    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main("assets/figures/fig_12_tomography_raycones.png")
