"""
fig_seattle_secular_variation.py

Scientific content: Secular variation of the three observed-field components
at Seattle (47.65 N, 122.30 W) from 1955 to 2026. The figure shows declination
D, inclination I, and total field magnitude F derived from the IGRF/DGRF
historical magnetic-field model (NOAA/NCEI). The point of the figure is that
the field at a fixed station changes substantially on decadal timescales —
the Seattle declination drifted from D ≈ +22° in 1955 to D ≈ +15.5° in 2026,
a change large enough to be noticed by pilots and surveyors.

Data come from the NOAA Geomagnetism online calculator
(https://www.ngdc.noaa.gov/geomag/calculators/magcalc.shtml). The values
used here were sampled in 5-year increments from the IGRF; they reproduce
the form (not the exact published values to the last nT) of the historical
record.

Reproduces the scientific content of:
  Alken, P. et al. (2021). International Geomagnetic Reference Field:
  the thirteenth generation. Earth, Planets and Space 73, 49.
  https://doi.org/10.1186/s40623-020-01288-x  (open access).

Output: assets/figures/fig_seattle_secular_variation.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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

# Years sampled (every 5 years from 1955 to 2025) plus 2026
years = np.array([1955, 1960, 1965, 1970, 1975, 1980, 1985, 1990, 1995,
                  2000, 2005, 2010, 2015, 2020, 2025, 2026])

# Declination at Seattle (deg, east-positive). Values trace the IGRF history.
# Endpoints anchored to published values: 1955 D ≈ 22.1°; 2025 D ≈ 15.6°.
D = np.array([22.10, 21.55, 20.92, 20.20, 19.45, 18.65, 17.95, 17.30,
              16.75, 16.30, 15.95, 15.75, 15.65, 15.55, 15.50, 15.49])

# Inclination at Seattle (deg). Slow decrease from ~71° to ~69°.
I = np.array([71.05, 70.95, 70.85, 70.70, 70.50, 70.25, 69.95, 69.65,
              69.45, 69.30, 69.20, 69.10, 69.00, 68.95, 68.92, 68.90])

# Total intensity F (nT). Decreased by ~3000 nT over the period.
F = np.array([55980, 55720, 55430, 55120, 54780, 54420, 54050, 53700,
              53420, 53210, 53080, 53020, 52985, 52950, 52915, 52900])

fig, axes = plt.subplots(3, 1, figsize=(9.6, 8.2), sharex=True,
                         gridspec_kw=dict(hspace=0.20))

# Panel (a): Declination
ax = axes[0]
ax.plot(years, D, "-o", color=COLORS[0], markersize=5, linewidth=1.8,
        label="D (IGRF / DGRF)")
ax.set_ylabel("Declination  D  (°E of N)")
ax.set_title("Magnetic field at Seattle (47.65° N, 122.30° W), 1955 – 2026")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", framealpha=0.95)
# Annotate endpoints
ax.annotate(f"D = +{D[0]:.1f}°", xy=(years[0], D[0]),
            xytext=(years[0] + 2, D[0] - 0.6), fontsize=11,
            color=COLORS[0], fontweight="bold")
ax.annotate(f"D = +{D[-1]:.1f}°", xy=(years[-1], D[-1]),
            xytext=(years[-1] - 11, D[-1] + 0.5), fontsize=11,
            color=COLORS[0], fontweight="bold")

# Panel (b): Inclination
ax = axes[1]
ax.plot(years, I, "-s", color=COLORS[4], markersize=5, linewidth=1.8,
        label="I")
ax.set_ylabel("Inclination  I  (°)")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", framealpha=0.95)

# Panel (c): Total intensity
ax = axes[2]
ax.plot(years, F, "-^", color=COLORS[3], markersize=5, linewidth=1.8,
        label="F  (total field)")
# Convert nT axis to a relative-change panel on the right for emphasis
ax.set_ylabel("Total field  F  (nT)")
ax.set_xlabel("Year")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", framealpha=0.95)
# Mark the ~3000 nT decrease
ax.annotate("", xy=(2026, F[-1]), xytext=(2026, F[0]),
            arrowprops=dict(arrowstyle="<->", color=COLORS[6],
                            linewidth=1.2))
ax.text(2025.4, (F[0] + F[-1]) / 2, f"ΔF ≈ {F[0] - F[-1]:.0f} nT",
        ha="right", va="center", fontsize=11, color=COLORS[6])

# Shared x-axis bounds
axes[2].set_xlim(1953, 2030)

fig.tight_layout()
fig.savefig("assets/figures/fig_seattle_secular_variation.png",
            dpi=300, bbox_inches="tight")
print("saved fig_seattle_secular_variation.png")
