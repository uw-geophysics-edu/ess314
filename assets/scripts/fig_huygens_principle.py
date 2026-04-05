"""
fig_huygens_principle.py

Scientific content: Huygens' principle construction showing an initial
wavefront, secondary point sources, circular wavelets, and the new
wavefront as the envelope tangent to all wavelets.

Replaces: Legacy slide 16 from 314_2023_4_seismic_waves.pdf (likely
textbook figure of unknown provenance).

Output: assets/figures/fig_huygens_principle.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

BLUE = "#0072B2"; SKY = "#56B4E9"; ORANGE = "#E69F00"
VERM = "#D55E00"; BLACK = "#000000"


def main():
    fig, ax = plt.subplots(figsize=(9, 7))

    # Initial curved wavefront (arc)
    n_sources = 7
    arc_radius = 5.0
    arc_center = np.array([0, -3])
    angles = np.linspace(55, 125, 200)
    angles_rad = np.radians(angles)
    wf_x = arc_center[0] + arc_radius * np.cos(angles_rad)
    wf_y = arc_center[1] + arc_radius * np.sin(angles_rad)
    ax.plot(wf_x, wf_y, color=BLUE, lw=2.5, label="Wavefront at $t_0$")

    # Point sources on the initial wavefront
    source_angles = np.linspace(65, 115, n_sources)
    source_angles_rad = np.radians(source_angles)
    src_x = arc_center[0] + arc_radius * np.cos(source_angles_rad)
    src_y = arc_center[1] + arc_radius * np.sin(source_angles_rad)
    ax.plot(src_x, src_y, "o", color=VERM, markersize=7, zorder=5,
            label="Secondary sources")

    # Secondary wavelets
    wavelet_radius = 1.2  # = V * Δt
    theta_circle = np.linspace(0, 2*np.pi, 100)
    for sx, sy in zip(src_x, src_y):
        wx = sx + wavelet_radius * np.cos(theta_circle)
        wy = sy + wavelet_radius * np.sin(theta_circle)
        ax.plot(wx, wy, color=SKY, lw=1.0, alpha=0.7)

    # New wavefront (envelope) at t0 + Δt
    new_radius = arc_radius + wavelet_radius
    new_angles = np.linspace(58, 122, 200)
    new_angles_rad = np.radians(new_angles)
    nwf_x = arc_center[0] + new_radius * np.cos(new_angles_rad)
    nwf_y = arc_center[1] + new_radius * np.sin(new_angles_rad)
    ax.plot(nwf_x, nwf_y, color=ORANGE, lw=2.5, ls="--",
            label="Wavefront at $t_0 + \\Delta t$")

    # Propagation arrows (between wavefronts, radial direction)
    for a_deg in [75, 90, 105]:
        a_rad = np.radians(a_deg)
        x0 = arc_center[0] + arc_radius * np.cos(a_rad)
        y0 = arc_center[1] + arc_radius * np.sin(a_rad)
        x1 = arc_center[0] + new_radius * np.cos(a_rad)
        y1 = arc_center[1] + new_radius * np.sin(a_rad)
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                     arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.5))

    # Labels
    ax.text(-2.8, 3.0, "Wavefront at $t_0$", fontsize=12, color=BLUE,
            fontweight="bold")
    ax.text(1.5, 4.5, "Wavefront at $t_0 + \\Delta t$", fontsize=12,
            color=ORANGE, fontweight="bold")
    ax.text(1.8, 1.2, "Secondary\nwavelets\n($r = V\\Delta t$)", fontsize=11,
            color=SKY, ha="center")

    # Annotate wavelet radius
    mid_src = n_sources // 2
    ax.annotate("$V\\Delta t$",
                xy=(src_x[mid_src] + wavelet_radius*0.7,
                    src_y[mid_src] + wavelet_radius*0.7),
                fontsize=12, color=VERM, fontweight="bold")

    ax.set_xlim(-5, 5)
    ax.set_ylim(-1, 6)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Huygens' Principle", fontsize=15, fontweight="bold", pad=15)

    plt.tight_layout()
    plt.savefig("assets/figures/fig_huygens_principle.png", bbox_inches="tight")
    plt.close()
    print("Saved: assets/figures/fig_huygens_principle.png")


if __name__ == "__main__":
    main()
