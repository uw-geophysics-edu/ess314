"""
fig_11_prem_profile.py

Scientific content: Preliminary Reference Earth Model (PREM) showing
P-wave velocity, S-wave velocity, and density as functions of depth
from the surface to Earth's centre. Major discontinuities are
annotated: Moho, 410 km, 660 km, core-mantle boundary (CMB), and
inner-core boundary (ICB). This 1-D model is the reference against
which all seismic observations are compared and against which 3-D
tomographic anomalies are defined.

Reproduces the scientific content of:
  Dziewonski, A.M. and Anderson, D.L., 1981. Preliminary reference
  Earth model. Physics of the Earth and Planetary Interiors 25(4),
  297-356. https://doi.org/10.1016/0031-9201(81)90046-7

Output: assets/figures/fig_11_prem_profile.png
License: CC-BY 4.0 (this script). PREM values are tabulated in the
original publication; numerical values used here are from the public
IRIS/EarthScope EMC service (https://ds.iris.edu/ds/products/emc-prem/).
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

# --- PREM tabulated values (isotropic), sampled from Dziewonski & Anderson 1981
# Depth (km), Vp (km/s), Vs (km/s), rho (g/cc). Representative points only.
# For a continuous curve we interpolate within major layers and impose
# sharp discontinuities at named boundaries.
PREM = np.array([
    [0,     5.80,  3.20,  2.60],
    [15,    5.80,  3.20,  2.60],
    [15.01, 6.80,  3.90,  2.90],
    [24,    6.80,  3.90,  2.90],
    [24.01, 8.11,  4.49,  3.38],
    [80,    8.08,  4.47,  3.37],
    [80.01, 8.08,  4.47,  3.37],
    [220,   7.99,  4.42,  3.35],
    [220.01, 8.56, 4.64,  3.43],
    [400,   8.90,  4.77,  3.54],
    [400.01, 9.13, 4.93,  3.72],
    [600,   10.15, 5.51,  3.97],
    [670,   10.27, 5.57,  4.00],
    [670.01, 10.75, 5.94, 4.38],
    [771,   11.07, 6.24,  4.44],
    [1000,  11.44, 6.37,  4.58],
    [2000,  12.56, 6.80,  5.04],
    [2741,  13.68, 7.27,  5.49],
    [2891,  13.72, 7.26,  5.57],   # CMB top
    [2891.01, 8.06, 0.0,  9.90],   # CMB bottom - S disappears
    [3000,  8.19,  0.0,   9.97],
    [4000,  9.51,  0.0,  10.85],
    [5000,  10.29, 0.0,  11.91],
    [5149.5, 10.36, 0.0, 12.17],   # ICB top
    [5149.51, 11.03, 3.50, 12.76], # ICB bottom - S reappears
    [5500,  11.14, 3.54, 12.93],
    [6000,  11.24, 3.60, 13.06],
    [6371,  11.26, 3.67, 13.09],
])


def main(outpath):
    depth = PREM[:, 0]
    vp = PREM[:, 1]
    vs = PREM[:, 2]
    rho = PREM[:, 3]

    fig, ax = plt.subplots(figsize=(7.2, 9.0))

    ax.plot(vp, depth, color=COLORS[0], lw=2.6, label="$V_P$ (km/s)")
    # Mask Vs=0 in outer core so the line breaks visually
    vs_plot = np.where(vs <= 0.01, np.nan, vs)
    ax.plot(vs_plot, depth, color=COLORS[1], lw=2.6, label="$V_S$ (km/s)")
    ax.plot(rho, depth, color=COLORS[3], lw=2.6, ls="--",
            label="$\\rho$ (g/cm$^3$)")

    # Discontinuities - horizontal annotation lines
    discontinuities = [
        (24, "Moho",          0.50),
        (220, "LAB ~ 220",    0.50),
        (410, "410 km",       0.50),
        (670, "660 km",       0.50),
        (2891, "CMB",         0.55),
        (5150, "ICB",         0.55),
    ]
    for z, name, frac in discontinuities:
        ax.axhline(z, color=COLORS[6], lw=0.7, alpha=0.35, zorder=0)
        ax.text(14.3, z, name, ha="right", va="center",
                fontsize=10, color=COLORS[6], style="italic")

    # Layer labels on the right
    ax.text(1.5, 150,    "crust / lithosphere", fontsize=10, color=COLORS[6])
    ax.text(1.5, 1700,   "mantle",              fontsize=11, color=COLORS[6])
    ax.text(1.5, 4000,   "outer core\n(liquid - no $V_S$)",
            fontsize=11, color=COLORS[6])
    ax.text(1.5, 5800,   "inner core\n(solid)", fontsize=11, color=COLORS[6])

    ax.set_xlim(0, 14.5)
    ax.set_ylim(6371, 0)    # depth positive downward; 0 at top
    ax.set_xlabel("Velocity (km/s)  or  density (g/cm$^3$)")
    ax.set_ylabel("Depth (km)")
    ax.set_title("PREM: 1-D reference Earth model\n(Dziewonski & Anderson, 1981)",
                 color=COLORS[6])
    ax.grid(True, alpha=0.3)
    ax.legend(loc="lower right", frameon=False)

    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")


if __name__ == "__main__":
    main("assets/figures/fig_11_prem_profile.png")
