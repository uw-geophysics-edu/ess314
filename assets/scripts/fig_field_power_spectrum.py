"""
fig_field_power_spectrum.py

Scientific content: The Mauersberger–Lowes power spectrum of Earth's magnetic
field as a function of spherical-harmonic degree n. Three regimes are visible:
the dipole-dominated core field (n = 1–13), the crustal/lithospheric field
(n ~ 16–100), and the ionospheric/external contribution superimposed at all
wavelengths but visible at short wavelengths once the lithospheric power has
decayed.

The wavelength axis on the top edge uses the relation
    lambda_n ~ 2 pi R / sqrt(n (n+1))   (R = 6371 km),
so degree n = 13 corresponds to lambda ~ 3000 km and n = 100 to lambda ~ 400 km.

Reproduces the scientific content of:
  Maus, S. (2008). The geomagnetic power spectrum. Geophysical Journal
  International 174, 135-142. https://doi.org/10.1111/j.1365-246X.2008.03820.x
  (open access). See also Hulot et al. (2015) for an overview.

Output: assets/figures/fig_field_power_spectrum.png
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

R_EARTH = 6371.2  # km

# Spherical-harmonic degree
n = np.arange(1, 120)

# Heuristic power spectrum: core field falls off rapidly above n = 13,
# crustal field is roughly flat in degree from n ~ 16 to n ~ 100, and an
# ionospheric "shelf" sits below them at short wavelengths.
# Magnitudes chosen to match the order-of-magnitude curves in Maus (2008).
P_core = 1.5e10 * np.exp(-0.55 * n)           # nT^2; dipole dominates
P_crust = 60.0 * np.exp(-0.013 * (n - 16)**2 / 60)  # nT^2; broad lithospheric
P_crust = np.where(n < 14, P_crust * 1e-3, P_crust)
P_ext = 4.0 + 0.0 * n                          # nT^2; ionospheric shelf

# Total (incoherent sum)
P_total = P_core + P_crust + P_ext

fig, ax = plt.subplots(figsize=(8.8, 5.6))

ax.semilogy(n, P_core, color=COLORS[0], linewidth=2.2,
            label="Core (geodynamo)")
ax.semilogy(n, P_crust, color=COLORS[1], linewidth=2.2, linestyle="--",
            label="Crust / lithosphere")
ax.semilogy(n, P_ext, color=COLORS[3], linewidth=1.8, linestyle=":",
            label="Ionosphere (external)")
ax.semilogy(n, P_total, color=COLORS[6], linewidth=1.2, alpha=0.6,
            label="Total observed")

# Highlight transition near n = 14
ax.axvspan(13, 16, color="grey", alpha=0.15)
ax.text(14.5, 1.5e2, "core → crust\ntransition", ha="center",
        va="bottom", fontsize=11, color="grey")

# Wavelength markers on top axis
for n_mark, lam_label in [(2, "20 000 km"), (13, "3 000 km"),
                          (40, "1 000 km"), (100, "400 km")]:
    ax.axvline(n_mark, color="grey", linewidth=0.4, linestyle=":",
               alpha=0.6)

ax_top = ax.twiny()
ax_top.set_xlim(ax.get_xlim())
ax_top.set_xscale(ax.get_xscale())
n_ticks = np.array([2, 13, 40, 100])
lam_ticks = 2 * np.pi * R_EARTH / np.sqrt(n_ticks * (n_ticks + 1))
ax_top.set_xticks(n_ticks)
ax_top.set_xticklabels([f"{int(round(la))} km" for la in lam_ticks])
ax_top.set_xlabel("Approximate horizontal wavelength λₙ")

ax.set_xlabel("Spherical-harmonic degree n")
ax.set_ylabel("Power per degree  R_n  (nT²)")
ax.set_title("Power spectrum of Earth's magnetic field at the surface")
ax.set_xlim(1, 110)
ax.set_ylim(1e-1, 5e9)
ax.grid(True, which="both", alpha=0.3)
ax.legend(loc="upper right", framealpha=0.95)

fig.tight_layout()
fig.savefig("assets/figures/fig_field_power_spectrum.png",
            dpi=300, bbox_inches="tight")
print("saved fig_field_power_spectrum.png")
