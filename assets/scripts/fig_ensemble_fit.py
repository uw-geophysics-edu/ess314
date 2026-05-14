"""
fig_ensemble_fit.py

Scientific content: a tutorial-grade visualisation of the data-error →
model-uncertainty pipeline for a buried-sphere gravity anomaly.

Panel (a) — Noisy gravity profile.
  A synthetic Δg(x) generated for a sphere at (z*, M*) is contaminated with
  Gaussian noise σ_Δg = 0.05 mGal (typical land-survey value) and plotted
  with 1σ error bars.

Panel (b) — Ensemble of acceptable sphere solutions.
  Many (z, M) pairs are drawn from a coarse grid; every pair whose
  predicted profile fits the noisy data within χ²/N ≤ 1.5 is plotted in
  panel (a) as a thin grey line and is retained for panel (c).

Panel (c) — Parameter-space view.
  The accepted (z, M) ensemble is plotted as a scatter, with the true
  values starred.  The locus traces out a curved valley in parameter
  space — the depth-mass tradeoff — and is the visual statement of
  potential-field non-uniqueness *under finite data error*.

Pedagogical message: data error is finite → many models fit equally well
→ the "answer" is a *family*, not a point.  This is the textbook entry
point to Bayesian / ensemble inversion in geophysics.

Output:  assets/figures/fig_ensemble_fit.png
License: CC-BY 4.0
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.size":       12,
    "axes.titlesize":  13,
    "axes.labelsize":  12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi":      150,
    "savefig.dpi":     300,
})

C_BLUE, C_ORANGE, C_GREEN, C_VERM, C_GREY, C_BLACK = (
    "#0072B2", "#E69F00", "#009E73", "#D55E00", "#9C9C9C", "#000000",
)

G = 6.67430e-11
MGAL = 1.0e5            # m/s^2 → mGal

# ── True ("buried") sphere parameters ─────────────────────────────────
z_true    = 600.0                              # m
R_true    = 180.0                              # m
drho_true = 600.0                              # kg/m^3
M_true    = (4.0/3.0) * np.pi * R_true**3 * drho_true   # kg

def dg_sphere(x, z, M):
    """Δg(x) in mGal for a sphere of mass M at depth z below x = 0."""
    return G * M * z / (x**2 + z**2) ** 1.5 * MGAL

# ── Synthetic survey profile ──────────────────────────────────────────
x_obs = np.linspace(-1500.0, 1500.0, 31)        # 31 stations, 100 m spacing
sigma_g = 0.05                                  # mGal, 1σ measurement noise

rng = np.random.default_rng(seed=42)
y_clean = dg_sphere(x_obs, z_true, M_true)
y_obs   = y_clean + rng.normal(0.0, sigma_g, size=x_obs.shape)

# ── Build a coarse (z, M) grid and score every model by χ²/N ──────────
z_grid = np.linspace(300.0, 1100.0, 81)         # 10 m steps
M_grid = np.linspace(0.3 * M_true, 2.5 * M_true, 110)
N_data = x_obs.size
chi2_thresh = 1.5                               # accept if χ²/N ≤ 1.5

accepted_z, accepted_M, accepted_chi2 = [], [], []
for z in z_grid:
    for M in M_grid:
        y_pred = dg_sphere(x_obs, z, M)
        chi2_per_n = np.mean(((y_pred - y_obs) / sigma_g) ** 2)
        if chi2_per_n <= chi2_thresh:
            accepted_z.append(z)
            accepted_M.append(M)
            accepted_chi2.append(chi2_per_n)

accepted_z   = np.array(accepted_z)
accepted_M   = np.array(accepted_M)
accepted_chi2 = np.array(accepted_chi2)

print(f"Accepted {len(accepted_z)} of {len(z_grid)*len(M_grid)} grid points "
      f"(χ²/N ≤ {chi2_thresh}).")
print(f"z range: {accepted_z.min():.0f}–{accepted_z.max():.0f} m, "
      f"M range: {accepted_M.min()/1e10:.2f}–{accepted_M.max()/1e10:.2f} × 1e10 kg")

# ── Figure ────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(13.5, 5.4))
gs  = fig.add_gridspec(1, 2, width_ratios=[1.5, 1.0], wspace=0.30)
axP = fig.add_subplot(gs[0, 0])     # profile + ensemble of fits
axM = fig.add_subplot(gs[0, 1])     # parameter-space scatter

# Panel (a) — profile with error bars and ensemble of accepted fits
x_dense = np.linspace(x_obs.min(), x_obs.max(), 400)

# Plot a representative subset (≤ 200) of accepted models as thin lines
n_plot = min(len(accepted_z), 200)
sub = rng.choice(len(accepted_z), size=n_plot, replace=False)
for k in sub:
    axP.plot(x_dense,
             dg_sphere(x_dense, accepted_z[k], accepted_M[k]),
             color=C_GREY, lw=0.5, alpha=0.30, zorder=1)

# True profile (no noise) — black dashed
axP.plot(x_dense, dg_sphere(x_dense, z_true, M_true),
         color=C_BLACK, lw=1.6, ls="--", zorder=3,
         label=f"True sphere ($z={z_true:.0f}$ m, $M={M_true:.2e}$ kg)")

# Best-fit model — minimum χ² in the accepted set
k_best = np.argmin(accepted_chi2)
axP.plot(x_dense,
         dg_sphere(x_dense, accepted_z[k_best], accepted_M[k_best]),
         color=C_VERM, lw=2.0, zorder=4,
         label=(rf"Best fit ($z={accepted_z[k_best]:.0f}$ m, "
                rf"$M={accepted_M[k_best]:.2e}$ kg)"))

# Observed data with 1σ error bars
axP.errorbar(x_obs, y_obs, yerr=sigma_g,
             fmt="o", color=C_BLUE, ms=5, capsize=3, lw=1.2, zorder=5,
             label=rf"Observed $\Delta g \pm 1\sigma$ ($\sigma={sigma_g}$ mGal)")

axP.set_xlabel("Profile distance $x$  (m)")
axP.set_ylabel(r"$\Delta g$  (mGal)")
axP.set_title("(a)  Noisy profile + ensemble of acceptable sphere fits "
              r"($\chi^{2}/N \leq 1.5$)", loc="left", pad=10)
axP.grid(ls=":", lw=0.6, alpha=0.5)
axP.legend(loc="upper right", framealpha=0.92)

# Panel (b) — parameter-space view: accepted (z, M) cloud
sc = axM.scatter(accepted_z, accepted_M / 1e10,
                 c=accepted_chi2, cmap="viridis_r",
                 s=14, alpha=0.85, edgecolors="none",
                 vmin=accepted_chi2.min(), vmax=chi2_thresh)
axM.scatter([z_true], [M_true / 1e10],
            marker="*", s=260, color=C_VERM,
            edgecolors=C_BLACK, lw=1.0, zorder=5, label="True $(z, M)$")
axM.scatter([accepted_z[k_best]], [accepted_M[k_best] / 1e10],
            marker="X", s=120, color=C_BLUE,
            edgecolors=C_BLACK, lw=0.8, zorder=5, label="Best fit")

# Theoretical depth–mass tradeoff at fixed peak amplitude:
# g_max = G M / z^2  →  M = (g_max / G) · z^2
g_max_true = G * M_true / z_true ** 2 * MGAL
z_line = np.linspace(z_grid.min(), z_grid.max(), 200)
M_line = (g_max_true / MGAL) / G * z_line ** 2
axM.plot(z_line, M_line / 1e10, color=C_BLACK, lw=1.2, ls=":",
         label=r"Depth-mass tradeoff:  $M = (g_{\max}/G)\,z^{2}$")

axM.set_xlabel("Sphere depth $z$  (m)")
axM.set_ylabel(r"Sphere mass $M$  ($\times 10^{10}$ kg)")
axM.set_title(r"(b)  Acceptable models in $(z, M)$ space",
              loc="left", pad=10)
axM.grid(ls=":", lw=0.6, alpha=0.5)
axM.legend(loc="upper left", framealpha=0.92, fontsize=9)

cb = fig.colorbar(sc, ax=axM, fraction=0.05, pad=0.03)
cb.set_label(r"$\chi^{2}/N$")

fig.suptitle(
    "From data error to model uncertainty — an ensemble of sphere "
    "anomalies that fit the data equally well",
    fontsize=14, y=1.02)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_ensemble_fit.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
