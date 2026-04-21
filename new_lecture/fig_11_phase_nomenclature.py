"""
fig_11_phase_nomenclature.py

Scientific content: Schematic cross-section of a spherically symmetric
Earth with true AK135 ray paths for the major body-wave phases: P, S
(direct mantle); PP (surface reflection); PcP (CMB reflection); PKP
(P in mantle -> P in outer core -> P in mantle); PKIKP (P legs through
mantle, outer core, and inner core). Ray paths are computed with
obspy.taup using the AK135 1-D reference Earth model. Includes the
phase-naming key (P = P in mantle, K = P in outer core, I = P in
inner core, J = S in inner core, c = reflection at CMB, i =
reflection at ICB).

Reproduces the scientific content of:
  Lowrie, W. and Fichtner, A., 2020. Fundamentals of Geophysics, 3rd
  ed. Cambridge University Press. Fig. 3.5-5 (UW Libraries electronic
  access).

Computed with:
  Kennett, B.L.N., Engdahl, E.R., Buland, R., 1995. Constraints on
  seismic velocities in the Earth from travel times. Geophys. J. Int.
  122(1), 108-124. https://doi.org/10.1111/j.1365-246X.1995.tb03540.x
  (AK135 model, open access.)

  obspy.taup: Krischer, L., Megies, T., Barsch, R., et al., 2015.
  ObsPy: a bridge for seismology into the scientific Python ecosystem.
  Computational Science & Discovery 8, 014003.
  https://doi.org/10.1088/1749-4699/8/1/014003

Output: assets/figures/fig_11_phase_nomenclature.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from obspy.taup import TauPyModel

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

R_EARTH = 6371.0
R_CMB = 3480.0
R_ICB = 1220.0


def draw_layered_earth(ax):
    theta = np.linspace(0, 2 * np.pi, 400)
    ax.fill(np.cos(theta) * R_EARTH, np.sin(theta) * R_EARTH,
            color="#F2E6D0", zorder=0)
    ax.fill(np.cos(theta) * R_CMB, np.sin(theta) * R_CMB,
            color="#FFE9A6", zorder=1)
    ax.fill(np.cos(theta) * R_ICB, np.sin(theta) * R_ICB,
            color="#FFD37A", zorder=2)
    ax.plot(np.cos(theta) * R_EARTH, np.sin(theta) * R_EARTH,
            color=COLORS[6], lw=1.4, zorder=3)
    ax.plot(np.cos(theta) * R_CMB, np.sin(theta) * R_CMB,
            color=COLORS[6], lw=0.9, ls="--", alpha=0.7, zorder=3)
    ax.plot(np.cos(theta) * R_ICB, np.sin(theta) * R_ICB,
            color=COLORS[6], lw=0.9, ls="--", alpha=0.7, zorder=3)


def taup_ray_to_xy(arrival, mirror=False):
    """Convert an obspy.taup Arrival's ray path to Cartesian (x, y)
    with the source at the top of the Earth (phi = pi/2), the ray
    travelling either clockwise (mirror=False, toward the right) or
    counter-clockwise (mirror=True, toward the left).

    obspy stores ray path entries with fields 'depth' (km) and
    'dist' (radians) measured along the great circle from the source.
    """
    path = arrival.path
    depth = path["depth"]           # km from surface downward
    dist = path["dist"]             # radians, 0 at source
    r = R_EARTH - depth             # distance from Earth centre, km
    sign = -1.0 if mirror else +1.0
    phi = np.pi / 2 + sign * dist
    x = r * np.cos(phi)
    y = r * np.sin(phi)
    return x, y


def main(outpath):
    model = TauPyModel(model="ak135")
    src_depth = 10.0

    phases = [
        {"name": "P",     "delta": 70,  "mirror": False,
         "color": COLORS[0], "ls": "-",  "lw": 2.4, "label_offset": 1.08},
        {"name": "S",     "delta": 55,  "mirror": True,
         "color": COLORS[1], "ls": "--", "lw": 2.4, "label_offset": 1.08},
        {"name": "PP",    "delta": 110, "mirror": False,
         "color": COLORS[2], "ls": "-",  "lw": 2.0, "label_offset": 1.08},
        {"name": "PcP",   "delta": 40,  "mirror": False,
         "color": COLORS[5], "ls": "-",  "lw": 2.0, "label_offset": 1.10},
        {"name": "PKP",   "delta": 150, "mirror": False,
         "color": COLORS[3], "ls": "-",  "lw": 2.0, "label_offset": 1.06},
        {"name": "PKIKP", "delta": 170, "mirror": False,
         "color": "#6a0dad", "ls": "-",  "lw": 2.0, "label_offset": 1.04},
    ]

    fig = plt.figure(figsize=(14.0, 7.5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 0.55], wspace=0.08)

    ax = fig.add_subplot(gs[0, 0])
    draw_layered_earth(ax)

    # Source
    ax.plot(0.0, R_EARTH, marker="*", color=COLORS[4],
            markersize=18, markeredgecolor=COLORS[6], zorder=10)
    ax.annotate("source", xy=(0.0, R_EARTH),
                xytext=(0.0, R_EARTH + 900),
                ha="center", fontsize=10, color=COLORS[6])

    # Plot each phase using real obspy ray paths
    for ph in phases:
        arrivals = model.get_ray_paths(
            source_depth_in_km=src_depth,
            distance_in_degree=ph["delta"],
            phase_list=[ph["name"]],
        )
        if not arrivals:
            print(f"WARNING: no arrival for {ph['name']} at {ph['delta']} deg")
            continue
        arr = arrivals[0]
        x, y = taup_ray_to_xy(arr, mirror=ph["mirror"])
        ax.plot(x, y, color=ph["color"], lw=ph["lw"], ls=ph["ls"],
                zorder=6)
        off = ph["label_offset"]
        ax.text(x[-1] * off, y[-1] * off, ph["name"],
                fontsize=13, color=ph["color"], fontweight="bold",
                ha="center", va="center", zorder=11)
        print(f"{ph['name']:>6s} at {ph['delta']:>3d} deg: "
              f"t = {arr.time:6.1f} s, "
              f"max depth = {arr.path['depth'].max():5.0f} km")

    # Distance ticks every 30 deg on each side from source (0-180)
    for sign in [-1, +1]:
        for d in np.arange(0, 181, 30):
            if d == 0:
                continue
            rad = np.deg2rad(90 + sign * d)
            x0, y0 = R_EARTH * np.cos(rad), R_EARTH * np.sin(rad)
            x1 = R_EARTH * 1.03 * np.cos(rad)
            y1 = R_EARTH * 1.03 * np.sin(rad)
            xl = R_EARTH * 1.10 * np.cos(rad)
            yl = R_EARTH * 1.10 * np.sin(rad)
            ax.plot([x0, x1], [y0, y1], color=COLORS[6], lw=0.5)
            ax.text(xl, yl, f"{d}$^\\circ$",
                    fontsize=8, ha="center", va="center", color=COLORS[6])

    ax.set_xlim(-R_EARTH * 1.25, R_EARTH * 1.25)
    ax.set_ylim(-R_EARTH * 1.25, R_EARTH * 1.25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("Major body-wave phases: AK135 ray paths "
                 "(obspy.taup)",
                 color=COLORS[6])

    # ===== Right panel: nomenclature key =====
    ax_k = fig.add_subplot(gs[0, 1])
    ax_k.axis("off")
    key_lines = [
        ("Phase nomenclature:", "bold", COLORS[6], 16),
        ("", "", "", 0),
        ("P", "bold", COLORS[0], 14),
        ("  P-wave leg in the mantle", "normal", COLORS[6], 12),
        ("S", "bold", COLORS[1], 14),
        ("  S-wave leg in the mantle", "normal", COLORS[6], 12),
        ("K", "bold", COLORS[3], 14),
        ("  P-wave leg in the outer core", "normal", COLORS[6], 12),
        ("I", "bold", "#6a0dad", 14),
        ("  P-wave leg in the inner core", "normal", COLORS[6], 12),
        ("J", "bold", COLORS[5], 14),
        ("  S-wave leg in the inner core", "normal", COLORS[6], 12),
        ("", "", "", 0),
        ("c", "bold", COLORS[6], 14),
        ("  reflection at the CMB", "normal", COLORS[6], 12),
        ("i", "bold", COLORS[6], 14),
        ("  reflection at the ICB", "normal", COLORS[6], 12),
        ("", "", "", 0),
        ("Reading a phase name:", "bold", COLORS[6], 13),
        ("", "", "", 0),
        ("PcP = P down to CMB,", "normal", COLORS[6], 11),
        ("      reflects, P back up", "normal", COLORS[6], 11),
        ("PKIKP = P down, K in OC,", "normal", COLORS[6], 11),
        ("        I through IC, K, P up", "normal", COLORS[6], 11),
        ("SKS = S down, converts to K", "normal", COLORS[6], 11),
        ("      in OC, converts back to S", "normal", COLORS[6], 11),
    ]
    y_pos = 1.0
    for line, weight, color, size in key_lines:
        if size > 0:
            ax_k.text(0.0, y_pos, line, transform=ax_k.transAxes,
                      fontsize=size, color=color,
                      fontweight=weight, ha="left", va="top")
        y_pos -= 0.035 if size > 0 else 0.022

    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main("/home/claude/work/ess314/assets/figures/fig_11_phase_nomenclature.png")
