"""
fig_reduction_to_pole.py

Scientific content: Reduction-to-pole (RTP) is a filtering operation in
which a measured magnetic anomaly recorded at non-vertical inclination is
mathematically transformed to what it would look like at the magnetic pole,
where the inducing field is vertical and the anomaly over a vertically-
magnetised body is symmetric and centred over the source. RTP simplifies
the visual interpretation of edges and source locations in low- to mid-
latitude surveys.

The figure shows a side-by-side comparison: (a) the observed total-field
anomaly above the same buried induced dipole as in fig_dipole_anomaly_shapes,
at inclination I = 45 deg (the asymmetric "Seattle-like" case); (b) the
same body after reduction-to-pole, which sharpens and centres the anomaly
directly over the source.

RTP is implemented in the Fourier domain as a multiplicative phase filter
that depends on (declination, inclination) and the orientation of the body.
Here we approximate the effect by recomputing the anomaly for the same body
at I = 90 deg.

Reproduces the scientific content of:
  Baranov, V. (1957). A new method for interpretation of aeromagnetic maps:
  Pseudo-gravimetric anomalies. Geophysics 22, 359-383. (Cited only.)
  Blakely (1995), Potential Theory, Section 12.3.

Output: assets/figures/fig_reduction_to_pole.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Circle

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def induced_dipole_anomaly(x, z, I_deg, m=1.0):
    I = np.radians(I_deg)
    r_vec_x = x
    r_vec_z = -z
    r = np.sqrt(r_vec_x ** 2 + r_vec_z ** 2)
    rhx = r_vec_x / r
    rhz = r_vec_z / r
    mx = np.cos(I)
    mz = np.sin(I)
    mdotr = mx * rhx + mz * rhz
    Bx = (3 * mdotr * rhx - mx) / r ** 3
    Bz = (3 * mdotr * rhz - mz) / r ** 3
    dF = Bx * mx + Bz * mz
    return m * dF


x = np.linspace(-3000, 3000, 601)
z = 600.0
m = 1.0e10

dF_obs = induced_dipole_anomaly(x, z, I_deg=45, m=m)
dF_rtp = induced_dipole_anomaly(x, z, I_deg=90, m=m)

fig, axes = plt.subplots(2, 2, figsize=(12.6, 7.4),
                         gridspec_kw=dict(height_ratios=[1.0, 0.55],
                                          hspace=0.06, wspace=0.20))

# Top row: anomaly profiles
ax_obs = axes[0, 0]
ax_rtp = axes[0, 1]

ax_obs.plot(x / 1000, dF_obs, color=COLORS[0], linewidth=2.4,
            label="Observed at I = 45°")
ax_obs.axhline(0, color="grey", linewidth=0.7, linestyle="--")
ax_obs.axvline(0, color=COLORS[6], linewidth=0.5, linestyle=":")
ax_obs.set_title("(a) Observed anomaly — asymmetric (mid-latitude)")
ax_obs.set_ylabel("ΔF  (arb. units)")
ax_obs.grid(True, alpha=0.3)
ax_obs.legend(loc="upper right", framealpha=0.95)
ax_obs.set_xticklabels([])

ax_rtp.plot(x / 1000, dF_rtp, color=COLORS[4], linewidth=2.4,
            label="After RTP  (effective I = 90°)")
ax_rtp.axhline(0, color="grey", linewidth=0.7, linestyle="--")
ax_rtp.axvline(0, color=COLORS[6], linewidth=0.5, linestyle=":")
ax_rtp.set_title("(b) After reduction-to-pole — symmetric peak")
ax_rtp.grid(True, alpha=0.3)
ax_rtp.legend(loc="upper right", framealpha=0.95)
ax_rtp.set_xticklabels([])

# Use shared y-limits for direct comparison
ymax = max(abs(dF_obs).max(), abs(dF_rtp).max()) * 1.15
for ax in (ax_obs, ax_rtp):
    ax.set_ylim(-ymax, ymax)
    ax.set_xlim(-3, 3)

# Bottom row: cross-section showing source location
for ax, color in [(axes[1, 0], COLORS[0]), (axes[1, 1], COLORS[4])]:
    ax.axhline(0, color=COLORS[6], linewidth=1.4)
    ax.text(2.8, -50, "surface", fontsize=11, color=COLORS[6],
            ha="right", va="bottom")
    # Source dipole at depth
    ax.scatter([0], [z], color=color, s=180, marker="D", zorder=5)
    ax.text(0.04, z, " induced dipole\n(z = 600 m)", fontsize=11,
            color=color, va="center")
    ax.set_xlim(-3, 3)
    ax.set_ylim(1200, -100)    # depth axis: 0 at top, positive down
    ax.set_xlabel("Distance from source  (km)  →  magnetic N")
    ax.set_ylabel("Depth  (m)")
    ax.grid(True, alpha=0.25)

fig.savefig("assets/figures/fig_reduction_to_pole.png",
            dpi=300, bbox_inches="tight")
print("saved fig_reduction_to_pole.png")
