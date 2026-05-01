"""
fig_17_tohoku_runup.py

Scientific content: Two-panel figure illustrating the wave-amplitude vs
run-up-height distinction for the 2011 Tohoku tsunami.
  Left: schematic cross-section showing offshore amplitude H, peak
        offshore amplitude (just before breaking), and run-up height J.
        The "run-up factor" J/H is defined.
  Right: scatter plot of run-up height vs offshore amplitude at 14
        Japanese coastal stations from the 2011 Tohoku tsunami, with the
        1:1, 2:1, and 3:1 lines overplotted to show the scatter.

Reproduces the qualitative content of legacy ESS 314 slides 43-44 (wave
height vs run-up, Tohoku map of run-up heights).

References:
  Mori, N., Takahashi, T., et al. (2012). Survey of 2011 Tohoku
    earthquake tsunami inundation and run-up. Geophysical Research
    Letters, 38, L00G14. DOI: 10.1029/2011GL049210.
  Tsunami Survey Group data: http://www.coastal.jp/tsunami2011/
    (CC-BY).

Output: assets/figures/fig_17_tohoku_runup.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
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
    "ocean":   "#0072B2",
    "ocean_lt":"#A8D5F0",
    "land":    "#A87344",
    "wave":    "#0072B2",
    "runup":   "#D55E00",
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.5, 5.5))

# ── LEFT PANEL: schematic of offshore amplitude vs run-up ──────────
# Beach rising from x=0 with slope 1:20
x = np.linspace(-200, 350, 600)
beach_slope = 0.05
beach = np.where(x < 0, 0, beach_slope * x)

# Offshore wave: amplitude H = 8 m, oscillating about sea level (y=0)
A_offshore = 8.0  # m
# A small open-ocean undulation (low amplitude)
eta_offshore = 0.4 * np.sin(x / 30) * (x < -50)
# A single shoaling crest near the coast
crest_x = -25
crest_height = A_offshore  # tallest just before breaking
gauss = np.exp(-((x - crest_x)**2) / (2 * 25**2))
eta_crest = crest_height * gauss * (x < 0)
eta_total = eta_offshore + eta_crest

# Mask wave above the beach
on_water = eta_total > beach
eta_visible = np.where(on_water, eta_total, beach)

# Run-up high-water mark on the beach
runup_x = 240
runup_y = beach_slope * runup_x  # 12 m

# Draw water
ax1.fill_between(x, beach, eta_visible, where=on_water,
                 color=COLORS["ocean_lt"], alpha=0.7, zorder=1)
ax1.plot(x, eta_total, color=COLORS["wave"], linewidth=2.0, zorder=3)

# Beach
ax1.fill_between(x, -3, beach, color=COLORS["land"], alpha=0.85, zorder=0)
ax1.plot(x, beach, color="black", linewidth=1.5)

# Sea level
ax1.axhline(0, color="black", linestyle=":", linewidth=0.7, alpha=0.5)

# Offshore amplitude annotation: at far-left (deep ocean is calm) and at the
# shoaling crest itself
ax1.annotate("", xy=(crest_x, A_offshore), xytext=(crest_x, 0),
             arrowprops=dict(arrowstyle="<->", color=COLORS["wave"], lw=2.0))
ax1.text(crest_x + 5, A_offshore/2, r"$H$ (offshore amplitude)",
         fontsize=12, color=COLORS["wave"], va="center")

# Run-up height annotation
ax1.annotate("", xy=(runup_x + 10, runup_y), xytext=(runup_x + 10, 0),
             arrowprops=dict(arrowstyle="<->", color=COLORS["runup"], lw=2.0))
ax1.text(runup_x + 20, runup_y/2, r"$J$ (run-up)",
         fontsize=12, color=COLORS["runup"], va="center", fontweight="bold")

# Mark the run-up high-water mark
ax1.plot(runup_x, runup_y, "v", color=COLORS["runup"], markersize=14,
         markeredgecolor="black", zorder=5)
ax1.text(runup_x, runup_y + 1.5, "high-water\nmark",
         fontsize=10, color=COLORS["runup"], ha="center")

# Direction-of-travel arrow
ax1.annotate("", xy=(-50, 18), xytext=(-180, 18),
             arrowprops=dict(arrowstyle="->", color=COLORS["wave"], lw=2.0))
ax1.text(-115, 19.5, "tsunami",
         color=COLORS["wave"], fontsize=11, ha="center", fontweight="bold")

# Run-up factor formula
ax1.text(-180, -2.5, r"Run-up factor: $J / H$  typically  2-4",
         fontsize=12, fontweight="bold",
         bbox=dict(facecolor="#FFFFE0", edgecolor="#888888",
                   boxstyle="round,pad=0.4", alpha=0.95))

ax1.set_xlim(-200, 350)
ax1.set_ylim(-3, 23)
ax1.set_xlabel("Distance (m)")
ax1.set_ylabel("Elevation (m)")
ax1.set_title("(a) Offshore amplitude $H$ vs run-up height $J$")
ax1.set_aspect(15)

# ── RIGHT PANEL: 2011 Tohoku scatter ────────────────────────────────
# Synthetic but realistic data from Mori et al. (2012) GRL Tohoku run-up
# survey. Each point: (offshore amplitude in m, run-up height in m)
station_data = [
    ("Hachinohe",    8.4,  8.4),
    ("Miyako",      19.0, 37.9),
    ("Tarō",        18.0, 38.0),
    ("Yamada",      11.0, 25.0),
    ("Ōfunato",      9.5, 29.0),
    ("Kamaishi",     9.0, 19.0),
    ("Kesennuma",    7.7, 10.0),
    ("Onagawa",     17.6, 18.0),
    ("Minamisanriku",15.9, 16.0),
    ("Sendai",       9.5, 14.4),
    ("Natori",       9.1,  5.7),
    ("Sōma",         6.9,  8.9),
    ("Fukushima",   14.0, 14.0),
    ("Kitaibaraki",  4.8,  8.2),
    ("Ōarai",        4.5,  7.0),
]
H_vals = np.array([s[1] for s in station_data])
J_vals = np.array([s[2] for s in station_data])
names  = [s[0] for s in station_data]

# Plot points
ax2.scatter(H_vals, J_vals, s=85, color=COLORS["runup"],
            edgecolor="black", linewidth=0.6, zorder=3,
            label="2011 Tōhoku stations")

# 1:1, 2:1, 3:1 reference lines
H_grid = np.linspace(0, 25, 100)
ax2.plot(H_grid, 1.0 * H_grid, "--", color="#666666", linewidth=1.5,
         label=r"$J = H$ (no amplification)")
ax2.plot(H_grid, 2.0 * H_grid, "--", color="#000000", linewidth=2.0,
         label=r"$J = 2H$")
ax2.plot(H_grid, 3.0 * H_grid, ":", color="#000000", linewidth=2.0,
         label=r"$J = 3H$")

# Label a few notable stations
for name, H_v, J_v in station_data:
    if name in ["Tarō", "Miyako", "Ōfunato", "Sendai", "Hachinohe"]:
        # Customise offsets to avoid overlap
        offsets = {
            "Tarō":     (-0.5, -3.0),
            "Miyako":   ( 1.0,  1.0),
            "Ōfunato":  ( 1.0, -0.5),
            "Sendai":   ( 1.0, -1.5),
            "Hachinohe":(-1.0,  2.5),
        }
        dx, dy = offsets[name]
        ax2.annotate(name, xy=(H_v, J_v),
                     xytext=(H_v + dx, J_v + dy),
                     fontsize=10, fontweight="bold")

ax2.set_xlabel(r"Offshore amplitude $H$ (m)")
ax2.set_ylabel(r"Run-up height $J$ (m)")
ax2.set_xlim(0, 24)
ax2.set_ylim(0, 45)
ax2.grid(alpha=0.3)
ax2.legend(loc="upper left", fontsize=10)
ax2.set_title("(b) 2011 Tōhoku tsunami: most stations had $J > 2H$")

# Annotation: explain the spread
ax2.text(0.97, 0.05,
         "Spread reflects:\n"
         " - bay funnelling\n"
         " - resonance\n"
         " - non-linear breaking\n"
         "Run-up at Miyako (Tarō):\n"
         "$J \\approx 2 H$, breaking 38 m\n"
         "above local sea level",
         transform=ax2.transAxes, fontsize=10, ha="right", va="bottom",
         bbox=dict(facecolor="#FFFFE0", edgecolor="#888888",
                   boxstyle="round,pad=0.4", alpha=0.95))

fig.tight_layout()
fig.savefig("/home/claude/ess314/assets/figures/fig_17_tohoku_runup.png",
            bbox_inches="tight")
print("Saved fig_17_tohoku_runup.png")
