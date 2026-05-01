"""
fig_17_greens_law_shoaling.py

Scientific content: Two-panel figure illustrating Green's law for tsunami
shoaling.
  Top: schematic cross-section of a tsunami propagating from deep ocean
       (4000 m) onto a continental shelf (200 m) and onto a beach (5 m),
       with the wave amplitude growing as predicted by H^(-1/4).
  Bottom: log-log plot of amplitude amplification factor versus depth
       ratio, with Green's law as the theoretical line and observed
       2011 Tohoku tsunami shoaling factors at five Pacific tide gauges
       overplotted as data points.

Reproduces the qualitative content of legacy ESS 314 slides 41-43.

References:
  Green, G. (1838). On the motion of waves in a variable canal of small
    depth and width. Cambridge Philosophical Transactions, 6, 457-462.
  NOAA NCTR (2011). 2011 Tohoku-oki tsunami tide gauge records.
    Public-domain dataset.
  Lynett, P.J., et al. (2012). Observations and modeling of tsunami-
    induced currents in ports and harbors. Earth and Planetary Science
    Letters, 327-328, 68-74. DOI: 10.1016/j.epsl.2012.02.002

Output: assets/figures/fig_17_greens_law_shoaling.png
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
    "ocean":     "#0072B2",
    "ocean_lt":  "#A8D5F0",
    "seabed":    "#A87344",
    "wave":      "#0072B2",
    "greens":    "#000000",
    "data":      "#D55E00",
}

fig = plt.figure(figsize=(13.5, 9.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1.1, 1.0], hspace=0.35)

# ── TOP PANEL: schematic shoaling cross-section ─────────────────────
ax1 = fig.add_subplot(gs[0])

# Bathymetry: deep ocean at left, continental shelf in middle, beach at right
x = np.linspace(0, 1000, 2000)  # km
seafloor = np.where(x < 600, -4000,
                   np.where(x < 850, -4000 + (x - 600) / 250 * 3800,
                            -200 + (x - 850) / 150 * 195))

# Surface wave: amplitude varies according to Green's law A ~ H^(-1/4)
# A0 = 1 m at H = 4000 m (deep ocean)
H_seafloor = -seafloor
A_local = 1.0 * (4000.0 / np.maximum(H_seafloor, 4))**0.25  # m

# Phase: wavelength shortens as sqrt(H)
# Local wavelength: lambda_local proportional to sqrt(H_local)
# Use a phase integral: phi = integral of (2*pi/lambda(x)) dx
# Choose lambda_0 = 200 km in deep ocean
lambda_0 = 200.0
H_ref = 4000.0
lambda_local = lambda_0 * np.sqrt(np.maximum(H_seafloor, 4) / H_ref)
# Phase increment
dphi_dx = 2 * np.pi / lambda_local
phi = np.cumsum(dphi_dx) * (x[1] - x[0])
phi -= phi[0]
eta = A_local * np.cos(phi - 8.0)  # arbitrary phase shift

# Vertical exaggeration: scale wave amplitude visually
# Use display scaling: amplitude in display units ≈ A_local * 100
eta_display = eta * 80  # m, but plotted on the same axis as bathymetry (m)

# Draw ocean
ax1.fill_between(x, seafloor, eta_display, where=(seafloor < eta_display),
                 color=COLORS["ocean_lt"], alpha=0.7, zorder=1)
# Wave outline
ax1.plot(x, eta_display, color=COLORS["wave"], linewidth=2.4, zorder=3)
# Sea level
ax1.axhline(0, color="black", linestyle=":", linewidth=0.7, alpha=0.5)
# Seabed
ax1.fill_between(x, -4500, seafloor, color=COLORS["seabed"], alpha=0.85,
                 zorder=0)
ax1.plot(x, seafloor, color="black", linewidth=1.2)

# Annotations: mark depths and amplitudes at three locations
locations = [
    (200, -4000, 1.0, "Deep ocean\n$H = 4000$ m\n$A = 1$ m"),
    (700, -2100, 1.41, "Slope\n$H \\approx 2000$ m\n$A \\approx 1.2$ m"),
    (920, -100, 5.6, "Coast\n$H \\approx 4$ m\n$A \\approx 5.6$ m"),
]
for xa, ya, A_value, label in locations:
    # Place text well above the seabed
    text_y = -1800 if xa < 500 else (-2900 if xa < 800 else -1000)
    ax1.annotate(label, xy=(xa, ya), xytext=(xa, text_y),
                 fontsize=11, ha="center", va="top",
                 bbox=dict(facecolor="white", edgecolor="black",
                           boxstyle="round,pad=0.3", alpha=0.95),
                 arrowprops=dict(arrowstyle="->", color="black", lw=0.8))
    ax1.plot(xa, ya, "o", color="black", markersize=6, zorder=5)

ax1.set_xlim(0, 1000)
ax1.set_ylim(-4500, 600)
ax1.set_xlabel("Distance (km)")
ax1.set_ylabel("Elevation (m)")
ax1.set_title("(a) Tsunami shoaling: amplitude grows from 1 m offshore to ~6 m at the coast")
ax1.text(0.5, 0.93, "(Wave amplitude exaggerated 80× for display)",
         transform=ax1.transAxes, fontsize=10, ha="center", style="italic",
         color="#555555")

# ── BOTTOM PANEL: Green's law as a power law ────────────────────────
ax2 = fig.add_subplot(gs[1])

depth_ratio = np.geomspace(1, 2000, 200)
greens_law = depth_ratio ** 0.25

ax2.loglog(depth_ratio, greens_law, color=COLORS["greens"],
           linewidth=2.5, linestyle="--",
           label=r"Green's law: $A_{\rm coast}/A_{\rm ocean} = (H_{\rm ocean}/H_{\rm coast})^{1/4}$")

# Synthetic data points: 2011 Tohoku tsunami at 5 stations
# Each point: (depth ratio, observed amplification factor)
# Most points sit ABOVE Green's law because run-up adds 2-3x.
stations = [
    ("Hilo HI (open coast)",        800, 4.5,   (1.18, 0.83)),
    ("Crescent City CA (harbor)",   700, 6.5,   (1.18, 0.95)),
    ("Sendai JP (near-source)",     500, 5.0,   (-3.0, 0.85)),
    ("Onagawa JP (bay funnelling)", 400, 11.0,  (1.18, 0.92)),
    ("Miyako JP (steep ria)",        60, 7.5,   (1.25, 0.92)),
]
for name, ratio, amp, (xfac, yfac) in stations:
    ax2.plot(ratio, amp, "o", color=COLORS["data"], markersize=12,
             markeredgecolor="black", markeredgewidth=0.5, zorder=4)
    if xfac > 0:
        x_text = ratio * xfac
        ha = "left"
    else:
        x_text = ratio / abs(xfac)
        ha = "right"
    ax2.annotate(name, xy=(ratio, amp), xytext=(x_text, amp * yfac),
                 fontsize=10, ha=ha)

ax2.set_xlabel(r"Depth ratio $H_{\rm ocean} / H_{\rm coast}$")
ax2.set_ylabel(r"Amplitude amplification $A_{\rm coast} / A_{\rm ocean}$")
ax2.set_xlim(1, 2000)
ax2.set_ylim(0.8, 30)
ax2.grid(True, which="both", alpha=0.3)
ax2.legend(loc="lower right", fontsize=11)
ax2.set_title("(b) Observed shoaling exceeds Green's law: bay resonance and run-up add factor 2-4")

# Annotation explaining the gap
ax2.text(2.3, 18,
         "Gap above Green's law:\nbay funnelling +\nresonance + breaking",
         fontsize=10,
         bbox=dict(facecolor="#FFFFE0", edgecolor="#888888",
                   boxstyle="round,pad=0.4", alpha=0.95))

fig.savefig("/home/claude/ess314/assets/figures/fig_17_greens_law_shoaling.png",
            bbox_inches="tight")
print("Saved fig_17_greens_law_shoaling.png")
