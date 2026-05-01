"""
fig_cascadia_focal_mechanisms.py

Scientific content: schematic map of the Pacific Northwest showing
focal mechanisms for representative recent earthquakes — the 2001
M6.8 Nisqually intraslab event, a representative Cascadia megathrust
mechanism, a Seattle Fault thrust, and an oceanic transform on the
Blanco fracture zone.  The diversity of mechanisms in a small region
reflects three superimposed sources of stress: subduction loading,
trench-parallel deformation in the upper plate, and slab-pull at
depth.

Plate boundary geometry generalised from:
  USGS Open-File Report 2008-1128: Geologic map of the PNW (public domain)
  McCrory et al. (2012) JGR  https://doi.org/10.1029/2012JB009407
Focal-mechanism parameters from:
  Global CMT catalog (https://www.globalcmt.org)
  USGS Comprehensive Catalog (https://earthquake.usgs.gov)
  PNSN catalog (https://pnsn.org)

Output: assets/figures/fig_cascadia_focal_mechanisms.png
License: CC-BY 4.0 (this script).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Polygon, Rectangle
from obspy.imaging.beachball import beach

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

OCEAN = "#D8E8F2"
LAND = "#F0E5D5"
SLAB = "#C8D5C0"


def main(out_path: str = "assets/figures/fig_cascadia_focal_mechanisms.png") -> None:
    fig, ax = plt.subplots(figsize=(10.5, 9.0))

    # --- Map extent (degrees, approximate) ---
    LON_W, LON_E = -130.5, -120.5
    LAT_S, LAT_N = 40.0, 51.0

    # ocean background
    ax.add_patch(Rectangle((LON_W, LAT_S), LON_E - LON_W, LAT_N - LAT_S,
                            facecolor=OCEAN, lw=0))

    # --- Coast and political outlines (highly schematic; for context only) ---
    # Schematic coastline: from Cape Mendocino north to BC.
    coast = np.array([
        [-124.40, 40.00], [-124.30, 40.50], [-124.10, 41.20],
        [-124.20, 42.00], [-124.30, 43.20], [-124.10, 44.40],
        [-124.00, 45.50], [-123.95, 46.20], [-124.20, 47.10],
        [-124.65, 48.40], [-124.85, 48.55], [-124.40, 48.40],
        [-123.20, 48.45], [-123.10, 49.20], [-123.20, 49.55],
        [-122.90, 50.10], [-122.40, 50.60],
    ])
    # Land polygon (close back along the eastern map edge)
    land_poly = np.vstack([coast,
                            [[LON_E, LAT_N], [LON_E, LAT_S], coast[0]]])
    ax.add_patch(Polygon(land_poly, facecolor=LAND, edgecolor="#666666",
                         lw=0.8, alpha=0.95))

    # --- Cascadia subduction trench (offshore) ---
    trench = np.array([
        [-126.30, 40.20], [-126.10, 41.10], [-126.00, 42.10],
        [-125.90, 43.00], [-125.85, 44.00], [-125.85, 45.00],
        [-126.00, 46.00], [-126.30, 47.00], [-126.50, 48.00],
        [-127.20, 48.80], [-128.00, 49.60],
    ])
    ax.plot(trench[:, 0], trench[:, 1], color="#000000", lw=2.4, zorder=4)
    # trench teeth (triangles pointing east, into upper plate)
    for k in range(0, len(trench) - 1, 2):
        x0, y0 = trench[k]
        # small triangle pointing east
        tri = np.array([[x0, y0 - 0.08], [x0, y0 + 0.08],
                        [x0 + 0.18, y0]])
        ax.add_patch(Polygon(tri, facecolor="#000000",
                              edgecolor="#000000", zorder=5))
    ax.text(-127.2, 44.5, "Cascadia\nsubduction\ntrench",
            color="#000000", fontsize=10, ha="center",
            fontweight="bold", style="italic")

    # --- Mendocino triple junction & Blanco fracture zone (transform) ---
    blanco = np.array([[-126.30, 40.20], [-128.40, 43.50]])
    ax.plot(blanco[:, 0], blanco[:, 1], color="#444444", lw=1.8,
            ls=(0, (8, 4)), zorder=3)
    ax.text(-128.4, 42.4, "Blanco FZ", fontsize=9, color="#333333",
            ha="left", style="italic")
    # Mendocino fault trace
    mend = np.array([[-124.40, 40.00], [-127.00, 40.20]])
    ax.plot(mend[:, 0], mend[:, 1], color="#444444", lw=1.8,
            ls=(0, (8, 4)), zorder=3)
    ax.text(-126.0, 39.8, "Mendocino FZ", fontsize=9, color="#333333",
            ha="center", style="italic")

    # --- Plate motion arrows ---
    # Juan de Fuca / Gorda plate moves NE (~25 mm/yr)
    ax.annotate("", xy=(-126.5, 47.5), xytext=(-128.0, 46.5),
                arrowprops=dict(arrowstyle="-|>", color="#0072B2", lw=2.2,
                                mutation_scale=18))
    ax.text(-128.1, 46.2, "JdF\n~25 mm/yr",
            color="#0072B2", fontsize=10, ha="center", fontweight="bold")
    # Pacific plate moves NW
    ax.annotate("", xy=(-128.7, 41.3), xytext=(-128.0, 40.6),
                arrowprops=dict(arrowstyle="-|>", color="#0072B2", lw=2.2,
                                mutation_scale=18))
    ax.text(-128.6, 40.5, "Pacific",
            color="#0072B2", fontsize=10, ha="left", fontweight="bold")

    # --- City markers ---
    cities = [
        ("Seattle",   -122.33, 47.61),
        ("Portland",  -122.68, 45.52),
        ("Vancouver", -123.12, 49.28),
        ("Eureka",    -124.15, 40.80),
    ]
    for nm, lon, lat in cities:
        ax.plot(lon, lat, marker="s", color="white",
                markeredgecolor="black", markersize=8, markeredgewidth=1.0,
                zorder=8)
        ax.text(lon + 0.18, lat + 0.06, nm, fontsize=10, color="#222222")

    # --- Focal mechanisms (strike, dip, rake) ---
    # 2001 Nisqually M6.8 intraslab: USGS Mw 6.8, depth 53 km
    #   Approx focal mech: phi=357, delta=83, lambda=-104 (normal-strike-slip)
    #   Source: USGS event page / Ichinose et al. 2004
    nis = (357.0, 83.0, -104.0)
    bc1 = beach(nis, xy=(-122.7, 47.15), width=0.85,
                facecolor="#D55E00", edgecolor="black", linewidth=0.9,
                zorder=10)
    ax.add_collection(bc1)
    ax.annotate("2001 Nisqually\nM6.8 intraslab\nh = 53 km",
                xy=(-122.30, 47.15), xytext=(-121.30, 46.45),
                arrowprops=dict(arrowstyle="-", color="#444444", lw=0.9),
                fontsize=10, ha="left", color="#222222",
                bbox=dict(boxstyle="round,pad=0.30", fc="white",
                          ec="#cccccc"))

    # Representative megathrust mechanism (low-angle thrust)
    mt = (10.0, 14.0, 90.0)
    bc2 = beach(mt, xy=(-126.50, 45.60), width=0.85,
                facecolor="#D55E00", edgecolor="black", linewidth=0.9,
                zorder=10)
    ax.add_collection(bc2)
    ax.annotate("Cascadia megathrust\n(M9 in 1700)",
                xy=(-126.10, 45.60), xytext=(-125.00, 44.50),
                arrowprops=dict(arrowstyle="-", color="#444444", lw=0.9),
                fontsize=10, ha="left", color="#222222",
                bbox=dict(boxstyle="round,pad=0.30", fc="white",
                          ec="#cccccc"))

    # Seattle Fault thrust event (2017 M3.4 illustrative; mechanism ~strike 280, dip 45, rake 90)
    sf = (280.0, 45.0, 90.0)
    bc3 = beach(sf, xy=(-121.80, 47.85), width=0.65,
                facecolor="#D55E00", edgecolor="black", linewidth=0.9,
                zorder=10)
    ax.add_collection(bc3)
    ax.annotate("Seattle Fault\nshallow thrust",
                xy=(-121.5, 47.85), xytext=(-121.40, 48.65),
                arrowprops=dict(arrowstyle="-", color="#444444", lw=0.9),
                fontsize=10, ha="left", color="#222222",
                bbox=dict(boxstyle="round,pad=0.30", fc="white",
                          ec="#cccccc"))

    # Blanco transform fault strike-slip mechanism
    bf = (110.0, 88.0, 175.0)
    bc4 = beach(bf, xy=(-127.50, 42.50), width=0.85,
                facecolor="#D55E00", edgecolor="black", linewidth=0.9,
                zorder=10)
    ax.add_collection(bc4)
    ax.annotate("Blanco transform\nright-lateral",
                xy=(-127.10, 42.40), xytext=(-126.30, 41.50),
                arrowprops=dict(arrowstyle="-", color="#444444", lw=0.9),
                fontsize=10, ha="left", color="#222222",
                bbox=dict(boxstyle="round,pad=0.30", fc="white",
                          ec="#cccccc"))

    # --- Map cosmetics ---
    ax.set_xlim(LON_W, LON_E); ax.set_ylim(LAT_S, LAT_N)
    ax.set_xlabel("Longitude (°E)")
    ax.set_ylabel("Latitude (°N)")
    ax.set_title("Cascadia margin: a single subduction system, "
                 "three fault types")

    # north arrow
    ax.annotate("", xy=(-130.0, 50.6), xytext=(-130.0, 50.0),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1.6,
                                mutation_scale=14))
    ax.text(-130.0, 50.75, "N", ha="center", va="bottom",
            fontsize=12, fontweight="bold")
    # scale (degrees not meters; just a visual reference)
    ax.plot([-129.5, -128.5], [40.5, 40.5], color="black", lw=2.0)
    ax.text(-129.0, 40.65, "~110 km",
            ha="center", fontsize=9, color="#333333")

    # subtle grid
    ax.grid(True, which="both", color="#cccccc", lw=0.5, alpha=0.5)
    ax.set_aspect(1.0 / np.cos(np.deg2rad(45.5)))  # cylindrical aspect

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    main()
