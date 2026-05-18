"""
fig_jdf_stripes.py

Scientific content: Magnetic anomaly stripes recorded across the Juan de
Fuca Ridge, offshore the Pacific Northwest. The figure shows three panels:

(a) The geomagnetic polarity timescale for the last 5 Myr (Cande & Kent 1995
and Ogg 2020), which encodes the history of polarity reversals as a sequence
of "normal" and "reversed" intervals of variable duration.

(b) The predicted total-field anomaly along a profile perpendicular to the
ridge axis, assuming a constant half-spreading rate of 30 mm/yr and a
1-km-thick magnetic source layer that locks in TRM at the field direction
of the time of emplacement. The result is the characteristic symmetric
striped pattern that proved seafloor spreading in Vine & Matthews (1963).

(c) Schematic cross-section of the seafloor showing the magnetized crustal
stripes with depth positive downward.

Polarity timescale used: Brunhes (0–0.78 Ma), Jaramillo subchron
(0.99–1.07 Ma), Matuyama reversed (0.78–1.78 Ma, except Jaramillo + Olduvai
1.78–1.95 Ma), Gauss (2.58–3.60 Ma with small reversed substages), and
Gilbert (3.60–5.0 Ma). Boundary ages rounded to ±10 kyr.

Reproduces the scientific content of:
  Cande, S. C. & Kent, D. V. (1995). Revised calibration of the geomagnetic
  polarity timescale. JGR 100, 6093-6095.
  Ogg, J. G. (2020). Geomagnetic polarity timescale. In Geologic Time Scale
  2020, Elsevier. (Cited only.)
  Vine, F. J. & Matthews, D. H. (1963). Magnetic anomalies over oceanic
  ridges. Nature 199, 947-949. (Cited only.)

Output: assets/figures/fig_jdf_stripes.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 13,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]

GPTS = [
    (0.00, 0.78, +1, "Brunhes"),
    (0.78, 0.99, -1, ""),
    (0.99, 1.07, +1, "Jaramillo"),
    (1.07, 1.78, -1, "Matuyama"),
    (1.78, 1.95, +1, "Olduvai"),
    (1.95, 2.58, -1, ""),
    (2.58, 3.04, +1, ""),
    (3.04, 3.11, -1, ""),
    (3.11, 3.22, +1, ""),
    (3.22, 3.33, -1, ""),
    (3.33, 3.60, +1, "Gauss"),
    (3.60, 5.00, -1, "Gilbert"),
]


def polarity_at_age(t_Ma):
    if t_Ma < 0:
        return +1
    for start, end, pol, _ in GPTS:
        if start <= t_Ma < end:
            return pol
    return +1


half_rate = 30.0  # mm/yr  =  km/Myr
x_km = np.linspace(-200, 200, 4001)
age = np.abs(x_km) / half_rate
pol = np.array([polarity_at_age(a) for a in age])

sigma_km = 4.0
dx_km = x_km[1] - x_km[0]
sigma_pix = sigma_km / dx_km
kernel = np.exp(-0.5 * ((np.arange(-int(4 * sigma_pix),
                                   int(4 * sigma_pix) + 1))
                        / sigma_pix) ** 2)
kernel /= kernel.sum()
dF_smooth = np.convolve(pol.astype(float), kernel, mode="same")
dF_smooth *= 400.0 / max(abs(dF_smooth.min()), abs(dF_smooth.max()))

# Layout: 3 stacked panels, generous hspace
fig = plt.figure(figsize=(13.0, 10.0))
gs = fig.add_gridspec(3, 1, height_ratios=[0.45, 1.0, 0.65], hspace=0.70)

# (a) Polarity timescale bar
ax_ts = fig.add_subplot(gs[0])
for start, end, pol_v, name in GPTS:
    color = COLORS[6] if pol_v == +1 else "white"
    ax_ts.add_patch(Rectangle((start, 0), end - start, 1.0,
                              facecolor=color, edgecolor=COLORS[6],
                              linewidth=0.8))
    if name:
        ax_ts.text((start + end) / 2, 1.40, name, ha="center", va="bottom",
                   fontsize=10, color=COLORS[6])
ax_ts.set_xlim(0, 5.0)
ax_ts.set_ylim(0, 2.2)
ax_ts.set_yticks([])
ax_ts.set_xlabel("Age  (Ma)")
ax_ts.set_title("(a) Geomagnetic polarity timescale  —  black = normal, "
                "white = reversed",
                pad=10)
for t in [0.78, 2.58, 3.60]:
    ax_ts.axvline(t, color="grey", linewidth=0.5, linestyle=":")

# (b) Anomaly profile
ax_an = fig.add_subplot(gs[1])
ax_an.fill_between(x_km, 0, dF_smooth,
                   where=(dF_smooth > 0), color=COLORS[6], alpha=0.85,
                   label="positive (normal polarity)")
ax_an.fill_between(x_km, 0, dF_smooth,
                   where=(dF_smooth <= 0), color=COLORS[2], alpha=0.55,
                   label="negative (reversed polarity)")
ax_an.plot(x_km, dF_smooth, color=COLORS[6], linewidth=1.2)
ax_an.axhline(0, color="grey", linewidth=0.7, linestyle="--")
ax_an.axvline(0, color=COLORS[4], linewidth=1.4, linestyle="-")
# Place "ridge axis" label INSIDE the plot, below the title
ax_an.text(0, -480, "RIDGE AXIS\n(spreading center)", color=COLORS[4],
           ha="center", va="top", fontsize=10, fontweight="bold")

ax_an.set_xlim(-200, 200)
ax_an.set_ylim(-550, 550)
ax_an.set_xlabel("Distance from ridge axis  (km)")
ax_an.set_ylabel("Total-field anomaly  ΔF  (nT)")
ax_an.set_title("(b) Predicted magnetic-anomaly profile across "
                "Juan de Fuca Ridge  (half-rate = 30 mm/yr)", pad=10)
ax_an.grid(True, alpha=0.3)
ax_an.legend(loc="upper right", framealpha=0.95, fontsize=10.5)

# (c) Seafloor cross-section. Use depth positive downward (km).
ax_geom = fig.add_subplot(gs[2])
# Magnetized crust band lies between depth 3.0 (seafloor) and 4.0 km
seafloor_depth = 3.0
crust_bottom = 4.0
# Stripes across the crust
n_stripes = 100
stripe_width = 400 / n_stripes  # km
for i in range(n_stripes):
    x_lo = -200 + i * stripe_width
    x_hi = x_lo + stripe_width
    age_mid = abs((x_lo + x_hi) / 2) / half_rate
    pol_v = polarity_at_age(age_mid)
    color = COLORS[6] if pol_v == +1 else "white"
    ax_geom.add_patch(Rectangle((x_lo, seafloor_depth), x_hi - x_lo,
                                crust_bottom - seafloor_depth,
                                facecolor=color, edgecolor="lightgrey",
                                linewidth=0.3))

# Ocean water column (0 to seafloor)
ax_geom.add_patch(Rectangle((-200, 0), 400, seafloor_depth,
                            facecolor="#CFE2F3", edgecolor="grey",
                            alpha=0.45))
ax_geom.text(-180, 1.5, "ocean", fontsize=11, color=COLORS[0])

# Ridge marker
ax_geom.plot([0, 0], [seafloor_depth, 0], color=COLORS[4], linewidth=2.5)
ax_geom.text(0, -0.25, "ridge axis", color=COLORS[4], ha="center",
             va="bottom", fontsize=11, fontweight="bold")

# Spreading arrows
ax_geom.annotate("", xy=(180, 4.7), xytext=(20, 4.7),
                 arrowprops=dict(arrowstyle="->", color=COLORS[6],
                                 linewidth=1.6))
ax_geom.annotate("", xy=(-180, 4.7), xytext=(-20, 4.7),
                 arrowprops=dict(arrowstyle="->", color=COLORS[6],
                                 linewidth=1.6))
ax_geom.text(100, 4.85, "spreading", color=COLORS[6], ha="center",
             va="top", fontsize=10)
ax_geom.text(-100, 4.85, "spreading", color=COLORS[6], ha="center",
             va="top", fontsize=10)

ax_geom.set_xlim(-200, 200)
ax_geom.set_ylim(5.5, -0.6)   # depth axis: 0 at top, positive down
ax_geom.set_xlabel("Distance from ridge axis  (km)")
ax_geom.set_ylabel("Depth below sea surface  (km)")
ax_geom.set_title("(c) Schematic seafloor: stripes lock in the polarity "
                  "at the time of crustal emplacement", pad=10)
ax_geom.grid(True, alpha=0.25)

fig.savefig("assets/figures/fig_jdf_stripes.png",
            dpi=300, bbox_inches="tight")
print("saved fig_jdf_stripes.png")
