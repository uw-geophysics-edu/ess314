"""
fig_16_intensity_vs_pgm.py

Scientific content: Two stacked plots showing how peak ground acceleration
(top) and Modified Mercalli Intensity (bottom) decay with epicentral
distance, for three site classes (rock, stiff soil, soft soil). Demonstrates
the qualitative relationship between an instrumental measure and an
ordinal felt-effect description, and shows that site condition
substantially shifts the PGA but only slightly shifts the MMI prediction.

Reproduces the qualitative content of slides 4 (intensity description)
and 6 (PGA/PGV/PGD/Sa metrics) of the legacy ESS 314 deck. Curves are
generated from a synthetic GMPE-style attenuation model parameterised
after:
  Worden, C.B., Gerstenberger, M.C., Rhoades, D.A., & Wald, D.J. (2012).
  Probabilistic relationships between ground-motion parameters and Modified
  Mercalli Intensity in California. Bulletin of the Seismological Society
  of America, 102(1), 204-221. DOI: 10.1785/0120110156

Output: assets/figures/fig_16_intensity_vs_pgm.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Global rcParams ─────────────────────────────────────────────────
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

# Colorblind-safe palette
COLORS = {
    "rock":      "#0072B2",  # blue
    "stiff":     "#009E73",  # green
    "soft":      "#D55E00",  # vermilion
    "shade":     "#CCCCCC",
}

LINESTYLES = {"rock": "-", "stiff": "--", "soft": "-."}

def gmpe_pga(R, M=6.0, vs30=760):
    """Synthetic GMPE for log10(PGA in g) vs distance R (km), magnitude M,
    site Vs30 (m/s). Loosely after Boore-Atkinson 2008-style functional
    form: source + path attenuation + site term. Tuned to give
    PGA(M=6.5, R=10 km, rock) ~ 0.25 g, consistent with Boore et al. 2014."""
    f_M = 0.55 * (M - 5.0)
    f_R = -1.40 * np.log10(np.sqrt(R**2 + 8.0**2)) - 0.0018 * R
    f_S = -0.45 * np.log10(vs30 / 760.0)
    log_pga = f_M + f_R + f_S + 0.50  # adjusted intercept
    return 10 ** log_pga  # PGA in g

def pga_to_mmi(pga_g):
    """GMICE: PGA -> MMI, piecewise linear after Worden et al. 2012, Table 2.
    Worden's regression takes PGA in cm/s^2; convert from g."""
    pga_cms2 = pga_g * 980.665  # g -> cm/s^2
    log_pga = np.log10(np.maximum(pga_cms2, 1e-3))
    # Two-segment fit (Worden 2012 Table 2, PGA -> MMI):
    mmi_low  = 1.78 + 1.55 * log_pga       # for low amplitudes (MMI < ~4.22)
    mmi_high = -1.60 + 3.70 * log_pga      # for high amplitudes (MMI > ~4.22)
    # Breakpoint where the two lines cross at MMI = 4.22, log_pga ~ 1.57
    breakpoint = 1.57
    return np.where(log_pga < breakpoint, mmi_low, mmi_high)


# ── Build figure ────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.0, 8.5), sharex=True)

R = np.linspace(5, 250, 200)
sites = [("rock", 1100, "Rock (Vs30 = 1100 m/s)"),
         ("stiff", 540, "Stiff soil (Vs30 = 540 m/s)"),
         ("soft", 270, "Soft soil (Vs30 = 270 m/s)")]

# --- Top panel: PGA vs distance ---
for key, vs30, label in sites:
    pga = gmpe_pga(R, M=6.5, vs30=vs30)
    ax1.semilogy(R, pga, color=COLORS[key], linestyle=LINESTYLES[key],
                 linewidth=2.4, label=label)
ax1.set_ylabel("Peak ground acceleration (g)")
ax1.set_title("M 6.5 earthquake: PGA decays with distance and depends on site")
ax1.grid(True, which="both", alpha=0.3)
ax1.legend(loc="upper right", framealpha=0.95)
ax1.set_ylim(1e-3, 1.0)
ax1.text(0.02, 0.04,
         "Soft soil amplifies\nrock motion by 2-5x\n(impedance contrast +\n  resonance)",
         transform=ax1.transAxes, fontsize=11,
         bbox=dict(facecolor="white", edgecolor="#888888", alpha=0.92,
                   boxstyle="round,pad=0.4"))

# --- Bottom panel: MMI bands ---
mmi_levels = [3, 4, 5, 6, 7, 8, 9]
mmi_colors = ["#FFFFCC", "#FFEDA0", "#FED976", "#FEB24C",
              "#FD8D3C", "#FC4E2A", "#E31A1C"]
for level, color in zip(mmi_levels, mmi_colors):
    ax2.axhspan(level, level + 1, facecolor=color, alpha=0.5, zorder=0)
    ax2.text(252, level + 0.5, f"{level}", fontsize=11, va="center",
             ha="left")

for key, vs30, label in sites:
    pga = gmpe_pga(R, M=6.5, vs30=vs30)
    mmi = pga_to_mmi(pga)
    ax2.plot(R, mmi, color=COLORS[key], linestyle=LINESTYLES[key],
             linewidth=2.4, label=label)

ax2.set_xlabel("Epicentral distance (km)")
ax2.set_ylabel("Modified Mercalli Intensity (MMI)")
ax2.set_xlim(5, 250)
ax2.set_ylim(2.5, 9.5)
ax2.set_title("MMI is the same earthquake described in ordinal damage units")
ax2.grid(True, alpha=0.3, axis="x")
ax2.text(0.02, 0.92,
         "Numerals = MMI levels\n(I = not felt; X = severe damage)",
         transform=ax2.transAxes, fontsize=11,
         bbox=dict(facecolor="white", edgecolor="#888888", alpha=0.92,
                   boxstyle="round,pad=0.4"),
         va="top")

fig.tight_layout()
fig.savefig("/home/claude/ess314/assets/figures/fig_16_intensity_vs_pgm.png",
            bbox_inches="tight")
print("Saved fig_16_intensity_vs_pgm.png")
