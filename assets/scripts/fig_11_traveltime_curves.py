"""
fig_11_traveltime_curves.py

Scientific content: Global travel-time curves for the major body-wave
phases (P, S, PcP, ScS, PP, SS, PKP, PKIKP, SKS) as a function of
epicentral distance Delta, computed from the AK135 1-D Earth model
using obspy.taup. This is the modern, reproducible version of the
Jeffreys-Bullen travel-time tables that seismologists have used since
the 1940s to identify phases on global seismograms.

Reproduces the scientific content of:
  Kennett, B.L.N., Engdahl, E.R., Buland, R., 1995. Constraints on
  seismic velocities in the Earth from travel times. Geophys. J. Int.
  122(1), 108-124. https://doi.org/10.1111/j.1365-246X.1995.tb03540.x
  (open access - AK135 model).

  IRIS/EarthScope Global Stacks (open access):
  https://ds.iris.edu/spud/eventplot

Output: assets/figures/fig_11_traveltime_curves.png
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
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def compute_tt(model, phase_list, distances, source_depth_km=10.0):
    """Return dict of phase -> list of (delta, t_min)."""
    out = {ph: [] for ph in phase_list}
    for d in distances:
        arrivals = model.get_travel_times(
            source_depth_in_km=source_depth_km,
            distance_in_degree=d,
            phase_list=phase_list,
        )
        seen = set()
        for arr in arrivals:
            # Take only first arrival of each named phase at this distance
            if arr.name in seen:
                continue
            seen.add(arr.name)
            if arr.name in out:
                out[arr.name].append((d, arr.time / 60.0))
    return out


def main(outpath):
    model = TauPyModel(model="ak135")

    phases = {
        "P":     dict(color=COLORS[0], ls="-",  lw=2.2),
        "S":     dict(color=COLORS[1], ls="-",  lw=2.2),
        "PP":    dict(color=COLORS[0], ls=":",  lw=1.8),
        "SS":    dict(color=COLORS[1], ls=":",  lw=1.8),
        "PcP":   dict(color=COLORS[2], ls="--", lw=1.6),
        "ScS":   dict(color=COLORS[4], ls="--", lw=1.6),
        "PKP":   dict(color=COLORS[3], ls="-",  lw=1.8),
        "PKIKP": dict(color=COLORS[5], ls="-",  lw=1.8),
        "SKS":   dict(color=COLORS[6], ls="--", lw=1.6),
    }

    distances = np.arange(1, 180, 1)
    tt = compute_tt(model, list(phases.keys()), distances,
                    source_depth_km=10.0)

    fig, ax = plt.subplots(figsize=(10.5, 7.2))

    for ph, style in phases.items():
        pts = tt[ph]
        if not pts:
            continue
        d_arr = np.array([p[0] for p in pts])
        t_arr = np.array([p[1] for p in pts])
        # Break curve where distance jumps (e.g. PKP gap)
        gaps = np.where(np.diff(d_arr) > 2.5)[0]
        if len(gaps) == 0:
            ax.plot(d_arr, t_arr, label=ph, **style)
        else:
            start = 0
            first = True
            for g in gaps:
                ax.plot(d_arr[start:g + 1], t_arr[start:g + 1],
                        label=(ph if first else None), **style)
                first = False
                start = g + 1
            ax.plot(d_arr[start:], t_arr[start:], **style)

    # Shadow zone shading
    ax.axvspan(103, 143, color="#D55E00", alpha=0.10, zorder=0)
    ax.text(123, 43, "P shadow\n$103^\\circ$ - $143^\\circ$",
            ha="center", va="top", fontsize=10, color=COLORS[4])

    # Inline phase labels at right edge
    label_positions = {
        "P":     (175, None),
        "S":     (130, None),
        "PP":    (175, None),
        "SS":    (175, None),
        "PcP":   (70, None),
        "ScS":   (70, None),
        "PKP":   (170, None),
        "PKIKP": (175, None),
        "SKS":   (125, None),
    }
    for ph, (xpos, _) in label_positions.items():
        pts = tt[ph]
        if not pts:
            continue
        # Find closest point
        best = min(pts, key=lambda p: abs(p[0] - xpos))
        ax.annotate(ph, xy=best, xytext=(5, 2),
                    textcoords="offset points",
                    fontsize=10, color=phases[ph]["color"],
                    fontweight="bold")

    ax.set_xlabel("Epicentral distance $\\Delta$ (degrees)")
    ax.set_ylabel("Travel time $T$ (minutes)")
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 45)
    ax.set_xticks(np.arange(0, 181, 30))
    ax.grid(True, alpha=0.3)
    ax.set_title("Global travel-time curves: AK135 model, 10-km source depth",
                 color=COLORS[6])
    ax.legend(loc="upper left", ncol=3, frameon=False, fontsize=9.5)

    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main("assets/figures/fig_11_traveltime_curves.png")
