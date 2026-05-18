"""
fig_magnetic_halfwidth.py

Scientific content: The half-width depth rule for a buried induced magnetic
dipole at the magnetic pole (or after RTP). At the pole, the total-field
anomaly has the closed form
    ΔF(x) = (μ₀ m / 4π) · (2 z² − x²) / (x² + z²)^{5/2},
which peaks at x = 0 with ΔF_max = (μ₀ m / 4π) · 2 / z³ and falls to
half its peak at x_{1/2} ≈ 0.5 z, giving the depth rule
    z ≈ 2 · x_{1/2}.
The figure shows three points:

(a) Geometry — three identical-moment dipoles at z = 300 / 600 / 1200 m.
(b) Shape comparison — the same profiles normalised by their own peaks,
    showing that deeper sources produce wider anomalies. Half-width
    markers x_{1/2} are annotated for each.
(c) Realistic noise propagation — the deepest profile (peak ≈ 50 nT) with a
    ±2σ noise band (σ = 2 nT) typical of regional aeromagnetic surveys,
    the half-max construction, and the inferred depth with the propagated
    uncertainty σ_z ≈ (1/3)(σ_F / F_max) · z.

Reproduces the scientific content of:
  Reford & Sumner (1964), Aeromagnetics. Geophysics 29, 482-516, eq. 28.
  Blakely (1995), Potential Theory, Eq. 5.11. (Cited only.)

Output: assets/figures/fig_magnetic_halfwidth.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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

mu0_over_4pi = 1.0e-7
amp_unit = mu0_over_4pi * 1.0e9    # T -> nT scaling


def dF_dipole_at_pole(x, z, m):
    """Total-field anomaly (nT) over a vertically magnetised buried dipole
    at the magnetic pole. x, z in m; m in A m^2."""
    r2 = x ** 2 + z ** 2
    return amp_unit * m * (2 * z ** 2 - x ** 2) / r2 ** 2.5


x = np.linspace(-3000, 3000, 2401)
depths = [300, 600, 1200]
depth_colors = [COLORS[0], COLORS[1], COLORS[3]]
# Same physical moment for all three (the depth-only sensitivity)
m_value = 25 * 1200 ** 3 / amp_unit  # so deepest gives peak ≈ 50 nT

# ──────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13.2, 10.0))
gs = fig.add_gridspec(3, 1, height_ratios=[0.6, 0.9, 1.0], hspace=0.40)

# Panel (a) — geometry
ax_geom = fig.add_subplot(gs[0])
ax_geom.axhline(0, color=COLORS[6], linewidth=1.3)
ax_geom.text(2.85, -40, "surface", fontsize=11, color=COLORS[6],
             ha="right", va="bottom")
ax_geom.scatter(np.linspace(-2.8, 2.8, 15), np.zeros(15), marker="v",
                color=COLORS[6], s=40, zorder=5)
for z, c, lab in zip(depths, depth_colors, [f"z = {d} m" for d in depths]):
    ax_geom.scatter([0], [z], color=c, s=240, marker="D", zorder=5,
                    label=lab, edgecolor="k", linewidth=0.6)

ax_geom.annotate("", xy=(-2.2, 200), xytext=(-2.2, -200),
                 arrowprops=dict(arrowstyle="->", color=COLORS[4],
                                 linewidth=2.0, mutation_scale=14))
ax_geom.text(-2.05, 0, "F_earth\n(vertical at pole)", fontsize=11,
             color=COLORS[4], va="center", ha="left")
ax_geom.set_xlim(-3, 3)
ax_geom.set_ylim(1500, -300)
ax_geom.set_xlabel("Horizontal distance  (km)")
ax_geom.set_ylabel("Depth  (m)")
ax_geom.set_title("(a) Geometry: three identical-moment dipoles at "
                  "increasing depth")
ax_geom.legend(loc="lower right", framealpha=0.95, ncol=3)
ax_geom.grid(True, alpha=0.25)

# Panel (b) — normalised profiles for shape comparison
ax_norm = fig.add_subplot(gs[1])
for z, c, lab in zip(depths, depth_colors, [f"z = {d} m" for d in depths]):
    dF = dF_dipole_at_pole(x, z, m_value)
    peak = dF.max()
    ax_norm.plot(x / 1000, dF / peak, color=c, linewidth=2.4, label=lab)
    # Mark half-width on positive side
    idx_pos = np.where((x > 0) & (dF > 0))[0]
    crossing = np.argmin(np.abs(dF[idx_pos] / peak - 0.5))
    x_half = float(x[idx_pos[crossing]])
    ax_norm.scatter([x_half / 1000, -x_half / 1000],
                    [0.5, 0.5], color=c, s=60, zorder=5)
    ax_norm.annotate(f"x₁/₂ = ±{round(x_half)} m",
                     xy=(x_half / 1000, 0.50),
                     xytext=(x_half / 1000 + 0.10, 0.55 - 0.10 * depths.index(z)),
                     fontsize=10.5, color=c,
                     arrowprops=dict(arrowstyle="->", color=c, linewidth=0.8))

ax_norm.axhline(0.5, color="grey", linewidth=0.8, linestyle=":")
ax_norm.text(2.9, 0.52, "½ peak", color="grey", fontsize=10, ha="right")
ax_norm.axhline(0, color="grey", linewidth=0.7, linestyle="--")
ax_norm.axvline(0, color=COLORS[6], linewidth=0.5, linestyle=":")
ax_norm.set_xlabel("Horizontal distance  (km)")
ax_norm.set_ylabel("Normalised ΔF / ΔF_max")
ax_norm.set_title("(b) Shape comparison (each curve normalised) — "
                  "deeper = wider;  half-width  x₁/₂ ≈ ½ z")
ax_norm.set_xlim(-3, 3)
ax_norm.set_ylim(-0.15, 1.10)
ax_norm.grid(True, alpha=0.3)
ax_norm.legend(loc="upper left", framealpha=0.95)

# Panel (c) — realistic-amplitude deepest case with noise band and σ_z
ax_real = fig.add_subplot(gs[2])
z = 1200
dF = dF_dipole_at_pole(x, z, m_value)
peak = dF.max()
half = peak / 2.0

ax_real.plot(x / 1000, dF, color=depth_colors[2], linewidth=2.4,
             label=f"z = {z} m,  peak = {peak:.1f} nT")
# Noise band
sigma = 2.0
ax_real.fill_between([-3, 3], -2 * sigma, +2 * sigma, color="grey",
                     alpha=0.22, label=f"±2σ noise band (σ = {sigma:.0f} nT)")
# Half-max line
ax_real.axhline(half, color=depth_colors[2], linewidth=0.9, linestyle=":")
ax_real.text(2.8, half + 1.0, f"½ peak = {half:.1f} nT",
             color=depth_colors[2], fontsize=10.5, ha="right")
# x_half markers
idx_pos = np.where((x > 0) & (dF > 0))[0]
crossing = np.argmin(np.abs(dF[idx_pos] - half))
x_half = float(x[idx_pos[crossing]])
for xh in (-x_half / 1000, +x_half / 1000):
    ax_real.axvline(xh, color=depth_colors[2], linewidth=0.9, linestyle="--")
ax_real.annotate("",
                 xy=(x_half / 1000, half * 0.55),
                 xytext=(-x_half / 1000, half * 0.55),
                 arrowprops=dict(arrowstyle="<->", color=depth_colors[2],
                                 linewidth=1.4))
ax_real.text(0, half * 0.55 + 1.5,
             f"2·x₁/₂ ≈ {round(2 * x_half)} m",
             color=depth_colors[2], ha="center", fontsize=11,
             fontweight="bold")
# Inferred-depth box
z_inferred = 2 * x_half
rel_err = (1 / 3) * sigma / peak
sigma_z = rel_err * z_inferred
txt = (f"half-width rule:  z ≈ 2·x₁/₂\n"
       f"inferred z = {z_inferred:.0f} m  (true {z} m)\n"
       f"S/N at peak = {peak / sigma:.0f}\n"
       f"σ_z/z ≈ (1/3)(σ_F/F_max) ≈ {rel_err * 100:.1f}%\n"
       f"σ_z ≈ {sigma_z:.0f} m")
ax_real.text(0.99, 0.97, txt, transform=ax_real.transAxes,
             fontsize=10.5, va="top", ha="right",
             bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                       edgecolor=COLORS[6], linewidth=0.8))

ax_real.axhline(0, color="grey", linewidth=0.7, linestyle="--")
ax_real.axvline(0, color=COLORS[6], linewidth=0.5, linestyle=":")
ax_real.set_xlabel("Horizontal distance  (km)")
ax_real.set_ylabel("Total-field anomaly  ΔF  (nT)")
ax_real.set_title("(c) Realistic case (deepest source) — measurement noise "
                  "propagates to depth uncertainty σ_z")
ax_real.set_xlim(-3, 3)
ax_real.grid(True, alpha=0.3)
ax_real.legend(loc="lower right", framealpha=0.95, fontsize=10.5)

fig.savefig("assets/figures/fig_magnetic_halfwidth.png",
            dpi=300, bbox_inches="tight")
print("saved fig_magnetic_halfwidth.png")
