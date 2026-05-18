"""
fig_field_power_spectrum.py

Scientific content: A two-part figure that grounds the abstract
Mauersberger–Lowes power spectrum in a concrete *spatial* example.

Top block — panel (a): three stacked sub-traces showing the geomagnetic
anomaly along a 20 000-km great-circle traverse, decomposed into the
three physical sources of the surface field:

  • core (geodynamo) — a long-wavelength signal of order ≳ 10 000 km,
    here amplitude ≈ 25 000 nT;
  • crust / lithosphere — overlapping anomalies in the 400–3 000 km
    band, amplitude ≈ 100 nT;
  • ionosphere / external — short-wavelength fluctuations of order
    100 km, amplitude ≈ a few nT.

Each sub-trace has its own y-axis so all three scales are visible at
once. The same colour coding carries into panel (b).

Bottom — panel (b): a Mauersberger–Lowes-style power spectrum, plotting
R_n versus spherical-harmonic degree n. The three components of panel
(a) appear in the same colours and map onto the well-known regimes:
core dominates n ≤ 13, crust dominates n ≈ 16–100, and an ionospheric
floor sets in at the highest degrees. A top axis converts n to
approximate horizontal wavelength λ_n = 2 π R / √(n(n+1)).

Reproduces the scientific form of:
  Maus, S. (2008). The geomagnetic power spectrum. Geophysical Journal
  International 174, 135–142. doi:10.1111/j.1365-246X.2008.03820.x

Output: assets/figures/fig_field_power_spectrum.png
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

COLORS = {
    "core":  "#0072B2",
    "crust": "#E69F00",
    "ext":   "#009E73",
    "total": "#222222",
}

R_EARTH = 6371.2  # km

# ---------------------------------------------------------------------------
# Synthetic spatial profile along a 20 000-km great-circle traverse
# ---------------------------------------------------------------------------
rng = np.random.default_rng(seed=20260601)
L_total = 20000.0
nx = 4001
x = np.linspace(0.0, L_total, nx)

core = (25000.0 * np.cos(2 * np.pi * x / 25000.0)
        + 6000.0 * np.cos(2 * np.pi * x / 12000.0 + 1.2))

crust = np.zeros_like(x)
for lam_km in np.linspace(400.0, 3000.0, 28):
    amp = 22.0 * (lam_km / 1000.0) ** 0.5
    phase = rng.uniform(0, 2 * np.pi)
    crust += amp * np.cos(2 * np.pi * x / lam_km + phase)

ext = np.zeros_like(x)
for lam_km in np.linspace(60.0, 250.0, 30):
    amp = 1.6
    phase = rng.uniform(0, 2 * np.pi)
    ext += amp * np.cos(2 * np.pi * x / lam_km + phase)

# ---------------------------------------------------------------------------
# Figure layout: 3 stacked traces for (a) + spectrum (b)
# ---------------------------------------------------------------------------
fig = plt.figure(figsize=(12.0, 11.5))
outer = fig.add_gridspec(2, 1, height_ratios=[1.0, 0.95], hspace=0.42)
gs_top = outer[0].subgridspec(3, 1, hspace=0.20)
gs_bot = outer[1].subgridspec(1, 1)

ax_core  = fig.add_subplot(gs_top[0, 0])
ax_crust = fig.add_subplot(gs_top[1, 0], sharex=ax_core)
ax_ext   = fig.add_subplot(gs_top[2, 0], sharex=ax_core)

ax_core.plot(x / 1000.0, core, color=COLORS["core"], linewidth=2.0)
ax_core.set_ylabel("Core\nΔF (nT)", color=COLORS["core"])
ax_core.set_title("(a) The same surface field, three superposed spatial scales",
                  loc="left")
ax_core.text(0.985, 0.92, "λ ≳ 10 000 km   |   ΔF ≈ 25 000 nT",
             transform=ax_core.transAxes, ha="right", va="top",
             color=COLORS["core"], fontsize=11,
             bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                       edgecolor=COLORS["core"], linewidth=0.8))
ax_core.set_ylim(-32000, 32000)
ax_core.set_yticks([-25000, 0, 25000])
ax_core.axhline(0, color="grey", linewidth=0.4, linestyle=":")
ax_core.grid(True, alpha=0.3)

ax_crust.plot(x / 1000.0, crust, color=COLORS["crust"], linewidth=1.4)
ax_crust.set_ylabel("Crust\nΔF (nT)", color=COLORS["crust"])
ax_crust.text(0.985, 0.92, "λ ≈ 400–3 000 km   |   ΔF ≈ ±100 nT",
              transform=ax_crust.transAxes, ha="right", va="top",
              color=COLORS["crust"], fontsize=11,
              bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                        edgecolor=COLORS["crust"], linewidth=0.8))
ax_crust.axhline(0, color="grey", linewidth=0.4, linestyle=":")
ax_crust.grid(True, alpha=0.3)

ax_ext.plot(x / 1000.0, ext, color=COLORS["ext"], linewidth=1.0)
ax_ext.set_ylabel("External\nΔF (nT)", color=COLORS["ext"])
ax_ext.text(0.985, 0.92, "λ ≈ 60–250 km   |   ΔF ≈ ±5 nT",
            transform=ax_ext.transAxes, ha="right", va="top",
            color=COLORS["ext"], fontsize=11,
            bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                      edgecolor=COLORS["ext"], linewidth=0.8))
ax_ext.axhline(0, color="grey", linewidth=0.4, linestyle=":")
ax_ext.grid(True, alpha=0.3)
ax_ext.set_xlabel("Distance along great-circle traverse  (× 1 000 km)")
ax_ext.set_xlim(0, L_total / 1000.0)

for a in (ax_core, ax_crust):
    plt.setp(a.get_xticklabels(), visible=False)

# Inset wavelength markers in each subpanel
def lam_marker(ax, x_center, lam_km, y_frac, color, label):
    half = (lam_km / 2.0) / 1000.0
    y_lo, y_hi = ax.get_ylim()
    y = y_lo + y_frac * (y_hi - y_lo)
    ax.annotate("", xy=(x_center - half, y), xytext=(x_center + half, y),
                arrowprops=dict(arrowstyle="<->", color=color, linewidth=1.4))
    ax.text(x_center, y - 0.07 * (y_hi - y_lo), label,
            ha="center", va="top", color=color, fontsize=10)

# Apply after limits are set
ax_core.set_ylim(-32000, 32000)
ax_crust.set_ylim(-120, 120)
ax_ext.set_ylim(-7.5, 7.5)

lam_marker(ax_crust, 10.0, 2000.0, 0.18, COLORS["crust"], "λ ≈ 2 000 km")

# ---------------------------------------------------------------------------
# Panel (b): Mauersberger–Lowes power spectrum
# ---------------------------------------------------------------------------
ax_b = fig.add_subplot(gs_bot[0, 0])

n = np.arange(1, 130)
P_core  = 1.5e10 * np.exp(-0.55 * n)
P_crust = 60.0 * np.exp(-((n - 30) ** 2) / (2 * 28 ** 2))
P_crust = np.where(n < 14, P_crust * 1e-3, P_crust)
P_ext   = 4.0 + 0.0 * n
P_total = P_core + P_crust + P_ext

ax_b.semilogy(n, P_core,  color=COLORS["core"],  linewidth=2.2,
              label="Core (geodynamo)")
ax_b.semilogy(n, P_crust, color=COLORS["crust"], linewidth=2.2,
              linestyle="--", label="Crust / lithosphere")
ax_b.semilogy(n, P_ext,   color=COLORS["ext"],   linewidth=1.8,
              linestyle=":", label="Ionosphere (external)")
ax_b.semilogy(n, P_total, color=COLORS["total"], linewidth=1.2,
              alpha=0.55, label="Total observed")

ax_b.axvspan(13, 16, color="grey", alpha=0.15)
ax_b.text(14.5, 5e2, "core → crust\ntransition", ha="center",
          va="bottom", fontsize=11, color="grey")

ax_top = ax_b.twiny()
ax_top.set_xlim(ax_b.get_xlim())
n_ticks = np.array([2, 13, 40, 100])
lam_ticks = 2 * np.pi * R_EARTH / np.sqrt(n_ticks * (n_ticks + 1))
ax_top.set_xticks(n_ticks)
ax_top.set_xticklabels([f"{int(round(la))} km" for la in lam_ticks])
ax_top.set_xlabel("Approximate horizontal wavelength  λₙ", labelpad=8)

ax_b.set_xlabel("Spherical-harmonic degree  n")
ax_b.set_ylabel("Power per degree  Rₙ  (nT²)")
ax_b.set_title("(b) Mauersberger–Lowes spectrum — the same three components",
               loc="left", pad=28)
ax_b.set_xlim(1, 120)
ax_b.set_ylim(1e-1, 5e9)
ax_b.grid(True, which="both", alpha=0.3)
ax_b.legend(loc="upper right", framealpha=0.95)

fig.savefig("assets/figures/fig_field_power_spectrum.png",
            dpi=300, bbox_inches="tight")
print("saved fig_field_power_spectrum.png")
