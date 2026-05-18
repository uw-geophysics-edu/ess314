"""
fig_magnetic_ensemble.py

Scientific content: From data error to model uncertainty for the buried
induced magnetic dipole at the magnetic pole. A synthetic profile is
generated with true parameters (z*, m*) = (600 m, m*) and sampled at 31
stations spaced 100 m apart with Gaussian noise σ = 2 nT. Every candidate
(z, m) pair on a fine grid is scored by reduced chi-squared; models with
χ²/N ≤ 1.5 are accepted. The accepted cloud traces a curved valley along
m ∝ z³ — the magnetic-dipole analog of the gravity sphere's M ∝ z² ridge,
and a *stronger* depth-moment correlation because the magnetic field falls
off faster than the gravity field.

Reproduces the scientific content of:
  Adapted directly from the gravity-version figure
  fig_ensemble_fit in Lecture 20 (Gravity Anomalies and Subsurface Modeling),
  with the forward map exchanged for the magnetic dipole.
  Background reading: Tarantola, A. (2005), Inverse Problem Theory and
  Methods for Model Parameter Estimation, SIAM. (Cited only.)

Output: assets/figures/fig_magnetic_ensemble.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.colors import Normalize

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
amp_unit = mu0_over_4pi * 1.0e9   # T → nT


def dF_dipole_at_pole(x, z, m):
    r2 = x ** 2 + z ** 2
    return amp_unit * m * (2 * z ** 2 - x ** 2) / r2 ** 2.5


# Truth and synthetic observations
z_true = 600.0
peak_target_nT = 35.0
m_true = peak_target_nT / (2 * amp_unit / z_true ** 3)
sigma_F = 2.0   # noise (nT)

# Stations
N = 31
x_stations = np.linspace(-1500, 1500, N)

rng = np.random.default_rng(42)
dF_clean = dF_dipole_at_pole(x_stations, z_true, m_true)
dF_obs = dF_clean + rng.normal(0, sigma_F, size=N)

# Grid in (z, m)
z_grid = np.linspace(300, 1100, 121)
# Scale m around m_true; range spans a factor of ~6 either side
m_grid = np.linspace(m_true * 0.3, m_true * 4.0, 121)
ZZ, MM = np.meshgrid(z_grid, m_grid, indexing="ij")
chi2 = np.zeros_like(ZZ)

for i in range(ZZ.shape[0]):
    for j in range(ZZ.shape[1]):
        dF_model = dF_dipole_at_pole(x_stations, ZZ[i, j], MM[i, j])
        chi2[i, j] = np.sum(((dF_obs - dF_model) / sigma_F) ** 2)
chi2 /= N   # reduced chi-squared

# Acceptance threshold
threshold = 1.5
accepted = chi2 <= threshold

# Best-fit
i_best, j_best = np.unravel_index(chi2.argmin(), chi2.shape)
z_best = ZZ[i_best, j_best]
m_best = MM[i_best, j_best]
print(f"truth:    z = {z_true:.0f} m,  m = {m_true:.3e} A m^2")
print(f"best fit: z = {z_best:.0f} m,  m = {m_best:.3e} A m^2")
print(f"# accepted models: {accepted.sum()}")

# Layout
fig = plt.figure(figsize=(13.6, 5.6))
gs = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.0], wspace=0.30)

# ── Panel (a): observed data + family of acceptable model curves
ax1 = fig.add_subplot(gs[0])
x_dense = np.linspace(-1700, 1700, 401)

# Plot every Nth accepted model as a thin grey curve
acc_indices = list(zip(*np.where(accepted)))
# subsample for visual clarity
rng_pick = np.random.default_rng(0)
sample = rng_pick.choice(len(acc_indices),
                         size=min(200, len(acc_indices)),
                         replace=False)
for k in sample:
    i, j = acc_indices[k]
    z_k = ZZ[i, j]; m_k = MM[i, j]
    ax1.plot(x_dense / 1000,
             dF_dipole_at_pole(x_dense, z_k, m_k),
             color="grey", linewidth=0.5, alpha=0.30)

# Truth (dashed black) and best fit (orange)
ax1.plot(x_dense / 1000,
         dF_dipole_at_pole(x_dense, z_true, m_true),
         color="k", linewidth=1.6, linestyle="--",
         label="true model")
ax1.plot(x_dense / 1000,
         dF_dipole_at_pole(x_dense, z_best, m_best),
         color=COLORS[1], linewidth=2.0,
         label="best fit (min χ²/N)")

# Observed points with 1σ bars
ax1.errorbar(x_stations / 1000, dF_obs, yerr=sigma_F,
             fmt="o", color=COLORS[0], markersize=4,
             ecolor=COLORS[0], elinewidth=0.9, capsize=2.5,
             label=f"observations (σ = {sigma_F:.0f} nT)")

ax1.axhline(0, color="grey", linewidth=0.7, linestyle="--")
ax1.set_xlabel("Horizontal distance  (km)")
ax1.set_ylabel("Total-field anomaly  ΔF  (nT)")
ax1.set_title("(a) Observations and accepted-model family")
ax1.set_xlim(-1.7, 1.7)
ax1.grid(True, alpha=0.3)
ax1.legend(loc="upper right", framealpha=0.95, fontsize=10.5)

# ── Panel (b): accepted models in (z, m) space, with theoretical ridge m∝z³
ax2 = fig.add_subplot(gs[1])

# Shared normalisation across the whole panel
norm = Normalize(vmin=chi2.min(), vmax=threshold)

# Plot accepted models as a scatter, coloured by chi2
i_acc, j_acc = np.where(accepted)
z_acc = ZZ[i_acc, j_acc]
m_acc = MM[i_acc, j_acc]
chi2_acc = chi2[i_acc, j_acc]
sc = ax2.scatter(z_acc, m_acc, c=chi2_acc, cmap="viridis", norm=norm,
                 s=12, edgecolor="none")

# Theoretical ridge: m_required(z) such that peak ΔF stays fixed
z_curve = np.linspace(300, 1100, 200)
# peak amplitude = 2 · amp_unit · m / z^3 ; fix peak to true value
peak_true = 2 * amp_unit * m_true / z_true ** 3
m_ridge = peak_true / (2 * amp_unit) * z_curve ** 3
ax2.plot(z_curve, m_ridge, color="k", linewidth=1.4, linestyle=":",
         label=r"theoretical ridge  $m \propto z^3$")

# Truth marker
ax2.scatter([z_true], [m_true], marker="*", s=320, color=COLORS[1],
            edgecolor="k", linewidth=1.0, zorder=10,
            label="true (z*, m*)")

ax2.set_xlabel("Depth  z  (m)")
ax2.set_ylabel(r"Magnetic moment  $m$  (A m²)")
ax2.set_title("(b) Accepted-model cloud in (z, m) parameter space")
ax2.set_xlim(300, 1100)
ax2.set_ylim(m_grid[0], m_grid[-1])
ax2.grid(True, alpha=0.3)
ax2.legend(loc="upper left", framealpha=0.95)

cbar = fig.colorbar(sc, ax=ax2, label=r"$\chi^2 / N$", pad=0.02,
                    shrink=0.85)

# Force scientific notation for the m axis tick labels
ax2.ticklabel_format(axis="y", style="sci", scilimits=(0, 0))

fig.savefig("assets/figures/fig_magnetic_ensemble.png",
            dpi=300, bbox_inches="tight")
print("saved fig_magnetic_ensemble.png")
