"""
fig_paleolatitude_from_inclination.py

Scientific content: The geocentric axial dipole relation
    tan(I) = 2 tan(lambda),
which relates the inclination I measured from a paleomagnetic sample to the
paleo-latitude lambda at which the rock was formed. The figure shows the
function (a) directly as I(lambda), and (b) inverted as lambda(I), with
example values for a basalt formed at the equator (lambda = 0, I = 0), at
30° (I ≈ 49°), and at the pole (lambda = 90°, I = 90°). The right-hand axis
on panel (b) shows uncertainty: a ±2° error in I propagates to a paleo-
latitude error that depends strongly on lambda.

Reproduces the scientific content of:
  Butler, R. F. (1992). Paleomagnetism: Magnetic Domains to Geologic
  Terranes, Blackwell, Eq. 1.15 and Fig. 1.10. (Cited only.)
  Tauxe, L. et al. (2018). Essentials of Paleomagnetism, 4th ed.
  https://earthref.org/MagIC/books/Tauxe/Essentials/ Sec. 2.2 (open access).

Output: assets/figures/fig_paleolatitude_from_inclination.png
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

# Paleo-latitude lambda from 0 to 90 deg
lam = np.linspace(0, 90, 901)
# I(lambda) from the dipole formula
I = np.degrees(np.arctan(2 * np.tan(np.radians(lam))))

# Inverse: given I, recover lambda
I_grid = np.linspace(0, 90, 901)
lam_inv = np.degrees(np.arctan(np.tan(np.radians(I_grid)) / 2))

# Inclination uncertainty propagation: dlam/dI for a fixed sigma_I = 2 deg
# Derivative computed from the inverse:
#   lam = arctan( tan(I)/2 )   =>   dlam/dI = (1/2) sec^2(I) / (1 + (tan(I)/2)^2)
sigma_I = 2.0   # deg
sec2I = 1.0 / np.cos(np.radians(I_grid)) ** 2
dlam_dI = 0.5 * sec2I / (1 + (np.tan(np.radians(I_grid)) / 2) ** 2)
sigma_lam = dlam_dI * sigma_I   # deg

fig, axes = plt.subplots(1, 2, figsize=(13.6, 5.4),
                         gridspec_kw=dict(wspace=0.40))

# ──────────────────────────────────────────────────────────────────────
# Panel (a): I as a function of lambda (forward)
# ──────────────────────────────────────────────────────────────────────
ax = axes[0]
ax.plot(lam, I, color=COLORS[0], linewidth=2.4,
        label=r"$\tan I = 2\,\tan\lambda$")
# Marker points
for lam0, color, name in [(0, COLORS[3], "equator"),
                          (30, COLORS[1], "30° N"),
                          (47.65, COLORS[5], "Seattle (47.65°)"),
                          (90, COLORS[4], "pole")]:
    I0 = float(np.degrees(np.arctan(2 * np.tan(np.radians(lam0)))))
    ax.plot(lam0, I0, "o", markersize=7, color=color,
            label=f"{name}: I = {round(I0)}°")
ax.set_xlabel("Paleo-latitude  λ  (°)")
ax.set_ylabel("Inclination  I  (°)")
ax.set_xlim(-2, 95)
ax.set_ylim(-2, 95)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.legend(loc="lower right", framealpha=0.95, fontsize=10.5)
ax.set_title("(a) Forward:  I from λ")

# ──────────────────────────────────────────────────────────────────────
# Panel (b): lambda(I) with uncertainty band
# ──────────────────────────────────────────────────────────────────────
ax = axes[1]
ax.plot(I_grid, lam_inv, color=COLORS[0], linewidth=2.4,
        label=r"$\lambda = \arctan(\tan I / 2)$")
ax.fill_between(I_grid, lam_inv - sigma_lam, lam_inv + sigma_lam,
                color=COLORS[0], alpha=0.20,
                label=r"$\pm 1\sigma_\lambda$  for  $\sigma_I = 2°$")
ax.set_xlabel("Measured inclination  I  (°)")
ax.set_ylabel("Inferred paleo-latitude  λ  (°)")
ax.set_xlim(0, 90)
ax.set_ylim(0, 90)
ax.set_aspect("equal")
ax.grid(True, alpha=0.3)
ax.legend(loc="lower right", framealpha=0.95, fontsize=10.5)
ax.set_title("(b) Inverse:  λ from I  (with σᵢ = 2°)")

# Annotation: the uncertainty is largest near the equator
ax.annotate("largest σ_λ\nnear equator", xy=(8, 4),
            xytext=(22, 12), fontsize=11, color=COLORS[4],
            arrowprops=dict(arrowstyle="->", color=COLORS[4],
                            linewidth=1.0))
ax.annotate("smallest σ_λ\nnear pole", xy=(82, 76),
            xytext=(50, 80), fontsize=11, color=COLORS[3],
            arrowprops=dict(arrowstyle="->", color=COLORS[3],
                            linewidth=1.0))

fig.tight_layout()
fig.savefig("assets/figures/fig_paleolatitude_from_inclination.png",
            dpi=300, bbox_inches="tight")
print("saved fig_paleolatitude_from_inclination.png")
