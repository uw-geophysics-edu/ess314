"""
fig_three_sources_cross_section.py

Scientific content: A half-Earth cross-section locating the three sources of
the geomagnetic field — the geodynamo in the outer core, the magnetised
lithosphere, and the ionospheric/magnetospheric current systems — at their
correct radial positions and with schematic indications of the physical
process at each level.

Pedagogical purpose: Establish the *spatial* identity of the three sources
before introducing their *spectral* signature in the Mauersberger–Lowes
power spectrum. Replaces the slide that opens with the spectrum directly.

Original concept inspired by: Lowrie & Fichtner (2020) Fig. 12.4
(schematic of the geomagnetic field and its sources). DOI of textbook:
10.1017/9781108685917. Reproduces only the scientific content; all
graphical elements original.

Output: assets/figures/fig_three_sources_cross_section.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

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

# Colorblind-safe palette (Okabe & Ito / WCAG AA)
C_CORE      = "#D55E00"   # vermilion — geodynamo
C_OUTERCORE = "#F0C97A"   # light orange — outer core fluid
C_MANTLE    = "#8B5A3C"   # warm brown — silicate mantle
C_LITHO     = "#0072B2"   # blue — magnetised lithosphere
C_ATMOS     = "#56B4E9"   # sky blue — ionosphere
C_FIELD     = "#000000"   # black — field-line annotations

# ── Earth radii (km) ────────────────────────────────────────────────
R_EARTH = 6371.0
R_CMB   = 3480.0   # core-mantle boundary
R_ICB   = 1220.0   # inner-core boundary
R_LITHO = 6271.0   # base of lithosphere ~100 km
R_IONO  = 6471.0   # ~100 km altitude (E-region)
R_MAGSPH = 6871.0  # ~500 km altitude — illustrative boundary

# ── Figure layout ───────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11, 9))

# Background sky for atmosphere
sky = mpatches.Wedge((0, 0), R_MAGSPH, 0, 180,
                     facecolor=C_ATMOS, alpha=0.18, edgecolor="none", zorder=0)
ax.add_patch(sky)

# Mantle
mantle = mpatches.Wedge((0, 0), R_EARTH, 0, 180,
                        facecolor=C_MANTLE, alpha=0.30, edgecolor="none", zorder=1)
ax.add_patch(mantle)

# Lithosphere (thin shell, exaggerated visually but labelled)
litho = mpatches.Wedge((0, 0), R_EARTH, 0, 180,
                       width=350, # visually exaggerated shell thickness
                       facecolor=C_LITHO, alpha=0.85, edgecolor="none", zorder=2)
ax.add_patch(litho)

# Outer core
outercore = mpatches.Wedge((0, 0), R_CMB, 0, 180,
                           facecolor=C_OUTERCORE, alpha=0.85,
                           edgecolor="none", zorder=3)
ax.add_patch(outercore)

# Inner core
innercore = mpatches.Wedge((0, 0), R_ICB, 0, 180,
                           facecolor=C_CORE, alpha=0.85,
                           edgecolor="none", zorder=4)
ax.add_patch(innercore)

# Earth's surface line
theta = np.linspace(0, np.pi, 400)
ax.plot(R_EARTH * np.cos(theta), R_EARTH * np.sin(theta),
        color="black", linewidth=1.4, zorder=5)
ax.plot(R_CMB * np.cos(theta), R_CMB * np.sin(theta),
        color="black", linewidth=0.9, linestyle="--", zorder=5, alpha=0.5)

# ── (1) Geodynamo: curved convection arrows in outer core ─────────
def add_curved_arrow(ax, center, r1, r2, theta_start, theta_end, color, lw=2.4):
    """Draw a curved arrow following an arc between two radii at given angles."""
    thetas = np.linspace(theta_start, theta_end, 30)
    # Helical-looking path: radius grows then shrinks
    rs = r1 + (r2 - r1) * np.sin(np.pi * (thetas - theta_start) / (theta_end - theta_start))
    xs = rs * np.cos(thetas)
    ys = rs * np.sin(thetas)
    ax.plot(xs, ys, color=color, linewidth=lw, alpha=0.85, zorder=4)
    # Arrow head
    arrow = FancyArrowPatch((xs[-2], ys[-2]), (xs[-1], ys[-1]),
                            arrowstyle='-|>', mutation_scale=18,
                            color=color, linewidth=lw, zorder=4)
    ax.add_patch(arrow)

# Three convection cells in the outer core
add_curved_arrow(ax, (0, 0), R_ICB + 200, R_CMB - 200,
                 np.deg2rad(150), np.deg2rad(110), C_CORE)
add_curved_arrow(ax, (0, 0), R_ICB + 200, R_CMB - 200,
                 np.deg2rad(80),  np.deg2rad(40),  C_CORE)
add_curved_arrow(ax, (0, 0), R_ICB + 300, R_CMB - 300,
                 np.deg2rad(125), np.deg2rad(95),  C_CORE)
add_curved_arrow(ax, (0, 0), R_ICB + 300, R_CMB - 300,
                 np.deg2rad(70),  np.deg2rad(45),  C_CORE)

# ── (2) Lithosphere: little magnetic dipole symbols ───────────────
# Show that the crust carries permanent magnetisation
np.random.seed(7)
n_dipoles = 14
dipole_angles = np.linspace(np.deg2rad(15), np.deg2rad(165), n_dipoles)
dipole_r = R_EARTH - 180   # set well inside the lithosphere band
for ang in dipole_angles:
    x0 = dipole_r * np.cos(ang)
    y0 = dipole_r * np.sin(ang)
    flip = 1 if np.random.rand() > 0.35 else -1
    dx = 240 * np.cos(ang) * flip
    dy = 240 * np.sin(ang) * flip
    arrow = FancyArrowPatch((x0 - dx/2, y0 - dy/2), (x0 + dx/2, y0 + dy/2),
                            arrowstyle='-|>', mutation_scale=14,
                            color="white", linewidth=2.0,
                            path_effects=[],
                            zorder=6)
    ax.add_patch(arrow)

# ── (3) Ionosphere: horizontal current arrows ────────────────────
iono_r = R_IONO + 50
iono_angles = np.linspace(np.deg2rad(30), np.deg2rad(150), 6)
for i, ang in enumerate(iono_angles):
    x0 = iono_r * np.cos(ang)
    y0 = iono_r * np.sin(ang)
    # Tangential direction (perpendicular to radial)
    tx = -np.sin(ang) * 220
    ty =  np.cos(ang) * 220
    arrow = FancyArrowPatch((x0 - tx/2, y0 - ty/2), (x0 + tx/2, y0 + ty/2),
                            arrowstyle='-|>', mutation_scale=14,
                            color=C_ATMOS, linewidth=2.0, zorder=6)
    ax.add_patch(arrow)

# ── (4) Schematic dipole field lines in space (the main field) ────
# Drawn outside the Earth, faintly, to indicate where the core field ends up
for r_factor in [1.10, 1.20, 1.32]:
    r = R_EARTH * r_factor
    # A dipole field line is r = r0 sin^2(theta), with theta from the dipole axis.
    # Plot a few of these emerging from the upper half.
    theta_line = np.linspace(np.deg2rad(2), np.deg2rad(178), 200)
    r_line = r * np.sin(theta_line)**2
    xs = r_line * np.cos(theta_line - np.pi/2)
    ys = r_line * np.sin(theta_line - np.pi/2) + 0  # rotate so axis is vertical
    # Keep only points above the surface and within plot bounds
    mask = (xs**2 + ys**2 >= R_EARTH**2) & (ys >= 0)
    ax.plot(xs[mask], ys[mask], color=C_FIELD, linewidth=0.7,
            alpha=0.35, linestyle="--", zorder=3)

# ── Source labels with leader lines ───────────────────────────────
# Core
ax.annotate("Source 1 — Core (geodynamo)\n"
            "Turbulent convection of\n"
            "liquid iron in the outer core\n"
            "Depth: 2 900–5 150 km\n"
            "λ ≳ 3 000 km at the surface",
            xy=(0.5 * R_ICB, 0.85 * R_ICB),
            xytext=(-13500, 2400),
            fontsize=11.5, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor=C_CORE, linewidth=1.8),
            arrowprops=dict(arrowstyle="->", color=C_CORE, lw=1.6,
                            connectionstyle="arc3,rad=-0.20"))

# Lithosphere
ax.annotate("Source 2 — Lithosphere (crust)\n"
            "Permanently magnetised rocks\n"
            "in the upper ~30 km\n"
            "λ ≈ 400–3 000 km",
            xy=(R_EARTH * np.cos(np.deg2rad(45)),
                R_EARTH * np.sin(np.deg2rad(45))),
            xytext=(8200, 3500),
            fontsize=11.5, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor=C_LITHO, linewidth=1.8),
            arrowprops=dict(arrowstyle="->", color=C_LITHO, lw=1.6,
                            connectionstyle="arc3,rad=0.20"))

# Ionosphere
ax.annotate("Source 3 — Ionosphere / magnetosphere\n"
            "Currents in the conducting upper\n"
            "atmosphere (~80–500 km altitude)\n"
            "Broad spectrum; time-varying\n"
            "(seconds to days)",
            xy=(R_IONO * np.cos(np.deg2rad(135)),
                R_IONO * np.sin(np.deg2rad(135))),
            xytext=(-13500, 7100),
            fontsize=11.5, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.45", facecolor="white",
                      edgecolor="#1F8FC9", linewidth=1.8),
            arrowprops=dict(arrowstyle="->", color="#1F8FC9", lw=1.6,
                            connectionstyle="arc3,rad=-0.20"))

# Interior labels (in-place, smaller, italic)
ax.text(0, R_ICB / 2, "Inner\ncore", fontsize=11, ha="center", va="center",
        color="white", style="italic", zorder=5)
ax.text(0, (R_ICB + R_CMB) / 2, "Outer core\n(liquid Fe-Ni)",
        fontsize=11, ha="center", va="center", color="#5C2F00",
        style="italic", zorder=5)
ax.text(0, (R_CMB + R_LITHO) / 2 - 200, "Mantle",
        fontsize=11.5, ha="center", va="center", color="#4D3221",
        style="italic", zorder=5)

# Tag the field lines
ax.text(0, R_EARTH * 1.42, "Surface field = sum of all three sources",
        fontsize=11, ha="center", va="center", color=C_FIELD,
        style="italic", alpha=0.75)

# ── Surface "ground line" tag ─────────────────────────────────────
ax.text(R_EARTH + 80, -120, "Earth's surface",
        fontsize=11, ha="left", va="top", color="black", style="italic")

# ── Axes cosmetics ────────────────────────────────────────────────
ax.set_xlim(-15500, 15500)
ax.set_ylim(-2000, 10200)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

# Title and subtitle
ax.set_title("Three sources of Earth's magnetic field, located in their physical context",
             fontsize=14, pad=14, fontweight="bold")

# Legend (custom proxy artists)
from matplotlib.lines import Line2D
legend_handles = [
    Line2D([0], [0], color=C_CORE, lw=3, label="Core convection (geodynamo)"),
    Line2D([0], [0], marker=r'$\nearrow$', color='w', label="Magnetised crust (remanence)",
           markerfacecolor='white', markersize=14, markeredgecolor='black', lw=0),
    Line2D([0], [0], color=C_ATMOS, lw=3, label="Ionospheric currents"),
    Line2D([0], [0], color=C_FIELD, lw=1, linestyle="--",
           label="Surface field lines (schematic)"),
]
ax.legend(handles=legend_handles, loc="upper center",
          ncol=4, frameon=True, framealpha=0.95,
          bbox_to_anchor=(0.5, -0.01), fontsize=11)

# ── Save ──────────────────────────────────────────────────────────
fig.tight_layout()
fig.savefig("../figures/fig_three_sources_cross_section.png",
            dpi=300, bbox_inches="tight")
plt.close(fig)
print("Wrote assets/figures/fig_three_sources_cross_section.png")
