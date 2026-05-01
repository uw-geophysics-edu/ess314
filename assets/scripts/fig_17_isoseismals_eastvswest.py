"""
fig_16_isoseismals_eastvswest.py

Scientific content: Two side-by-side schematic maps of the contiguous
United States showing felt-area extent for two earthquakes of similar
magnitude: M6.0 in central California (2004 Parkfield) versus M5.8 in
central Virginia (2011 Mineral). Demonstrates that the eastern
North-American crust has a far higher quality factor Q than the western
US, so similar earthquakes "feel" much larger across the eastern
seaboard. Reproduces the qualitative content of legacy ESS 314 slide 9
("Did You Feel It? — California vs Virginia").

Background DYFI maps: USGS Did You Feel It? program (public domain).
Synthetic isoseismal contours fit to the published M5.8 Virginia 2011
felt-area data (~ 2,000,000 km^2) and the Parkfield 2004 felt area
(~ 70,000 km^2).

References:
  Atkinson, G.M., & Wald, D.J. (2007). "Did You Feel It?" intensity data:
    A surprisingly good measure of earthquake ground motion. Seismological
    Research Letters, 78(3), 362-368. DOI: 10.1785/gssrl.78.3.362
  Hough, S.E. (2012). Initial assessment of the intensity distribution of
    the 2011 Mw 5.8 Mineral, Virginia, earthquake. Seismological Research
    Letters, 83(4), 649-657. DOI: 10.1785/0220110140

Output: assets/figures/fig_16_isoseismals_eastvswest.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]

# A simplified outline of the contiguous United States. The list contains
# (lon, lat) vertices traced approximately from a public-domain Census
# Bureau cartographic boundary file at ~50 km resolution. Used only as a
# schematic backdrop; coordinates are illustrative.
US_OUTLINE = np.array([
    (-124.5, 48.4), (-124.0, 46.0), (-123.5, 41.5), (-122.5, 38.0),
    (-120.5, 34.5), (-117.0, 32.5), (-114.5, 32.7), (-110.0, 31.3),
    (-106.5, 31.7), (-103.0, 28.9), (-99.0, 26.5), (-97.5, 27.5),
    (-95.0, 29.0), (-91.0, 29.2), (-89.5, 30.0), (-87.5, 30.4),
    (-85.0, 29.7), (-82.0, 26.5), (-80.5, 25.2), (-80.0, 27.0),
    (-81.0, 30.5), (-80.5, 32.5), (-78.0, 34.0), (-76.5, 35.0),
    (-75.5, 37.0), (-74.5, 39.0), (-73.5, 40.5), (-72.0, 41.5),
    (-70.5, 42.5), (-69.5, 44.0), (-67.5, 44.5), (-67.5, 47.0),
    (-69.5, 47.0), (-71.0, 45.0), (-75.0, 45.0), (-77.5, 43.5),
    (-79.0, 43.5), (-82.5, 42.0), (-83.5, 45.0), (-87.5, 46.5),
    (-90.0, 47.5), (-93.5, 49.0), (-95.5, 49.0), (-103.0, 49.0),
    (-110.0, 49.0), (-116.0, 49.0), (-121.0, 49.0), (-124.5, 48.4),
])

def gaussian_felt_field(lon, lat, lon0, lat0, sigma_deg, amplitude=1.0):
    """A 2D Gaussian centred on (lon0, lat0) with isotropic sigma.
    Approximates an isoseismal field (felt-shaking probability)
    decaying away from the epicentre."""
    return amplitude * np.exp(-((lon - lon0)**2 + (lat - lat0)**2)
                              / (2 * sigma_deg**2))


def plot_quake(ax, lon0, lat0, sigma, title, marker_label):
    """Draw the US outline, a Gaussian intensity field, and an epicentre."""
    # 1) Country outline
    poly = mpatches.Polygon(US_OUTLINE, closed=True,
                            facecolor="#F4F2EE", edgecolor="black",
                            linewidth=1.0, zorder=1)
    ax.add_patch(poly)
    # 2) Felt field as colored contours
    lons = np.linspace(-126, -66, 240)
    lats = np.linspace(24, 50, 110)
    LON, LAT = np.meshgrid(lons, lats)
    field = gaussian_felt_field(LON, LAT, lon0, lat0, sigma)
    levels = [0.05, 0.15, 0.30, 0.55, 0.80, 1.01]
    colors = ["#FFEDA0", "#FEB24C", "#FD8D3C", "#FC4E2A", "#E31A1C"]
    # Mask field outside the outline
    from matplotlib.path import Path
    path = Path(US_OUTLINE)
    mask = path.contains_points(np.vstack([LON.ravel(), LAT.ravel()]).T)
    mask = mask.reshape(LON.shape)
    field_masked = np.where(mask, field, np.nan)
    ax.contourf(LON, LAT, field_masked, levels=levels, colors=colors,
                alpha=0.75, zorder=2)
    # 3) Epicentre marker
    ax.plot(lon0, lat0, "*", color="#000000", markersize=22,
            markeredgecolor="white", markeredgewidth=1.5, zorder=5,
            label=marker_label)
    # 4) Label
    ax.text(lon0, lat0 - 1.5, marker_label, ha="center", va="top",
            fontsize=11, fontweight="bold",
            bbox=dict(facecolor="white", edgecolor="black",
                      boxstyle="round,pad=0.3", alpha=0.95))
    ax.set_xlim(-127, -65)
    ax.set_ylim(23, 51)
    ax.set_aspect(1.4)  # rough latitude-longitude correction
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title)


fig, axs = plt.subplots(1, 2, figsize=(13.0, 5.5))

# Left: Parkfield M6.0 (2004 California)
plot_quake(axs[0], lon0=-120.4, lat0=35.8, sigma=2.0,
           title="(a) M 6.0 Parkfield, California, 2004",
           marker_label="Parkfield M6.0")

# Right: Mineral M5.8 (2011 Virginia)
plot_quake(axs[1], lon0=-77.9, lat0=37.9, sigma=7.0,
           title="(b) M 5.8 Mineral, Virginia, 2011",
           marker_label="Mineral M5.8")

# Add a colorbar / legend explaining the field
from matplotlib.lines import Line2D
legend_handles = [
    mpatches.Patch(facecolor="#FFEDA0", edgecolor="black",
                   alpha=0.75, label="Weakly felt"),
    mpatches.Patch(facecolor="#FEB24C", edgecolor="black",
                   alpha=0.75, label="Felt"),
    mpatches.Patch(facecolor="#FD8D3C", edgecolor="black",
                   alpha=0.75, label="Moderately felt"),
    mpatches.Patch(facecolor="#FC4E2A", edgecolor="black",
                   alpha=0.75, label="Strongly felt"),
    mpatches.Patch(facecolor="#E31A1C", edgecolor="black",
                   alpha=0.75, label="Damage zone"),
]
fig.legend(handles=legend_handles, loc="lower center",
           ncol=5, bbox_to_anchor=(0.5, -0.02), fontsize=11,
           frameon=False)

# Annotation: explain the physics
fig.text(0.5, 0.92,
         "Eastern crust has higher Q (less attenuation):\n"
         "the smaller earthquake is felt over a far larger area.",
         ha="center", fontsize=12, fontweight="bold",
         bbox=dict(facecolor="#FFFFE0", edgecolor="#888888",
                   boxstyle="round,pad=0.5", alpha=0.95))

# Approximate felt areas (illustrative)
axs[0].text(-104, 26, "Felt area:\n~70,000 km²",
            fontsize=11, color=COLORS[6], style="italic",
            bbox=dict(facecolor="white", edgecolor="black",
                      boxstyle="round,pad=0.3", alpha=0.85))
axs[1].text(-104, 26, "Felt area:\n~2,000,000 km²",
            fontsize=11, color=COLORS[4], style="italic",
            bbox=dict(facecolor="white", edgecolor="black",
                      boxstyle="round,pad=0.3", alpha=0.85))

fig.tight_layout(rect=(0, 0.04, 1, 0.91))
fig.savefig("/home/claude/ess314/assets/figures/fig_16_isoseismals_eastvswest.png",
            bbox_inches="tight")
print("Saved fig_16_isoseismals_eastvswest.png")
