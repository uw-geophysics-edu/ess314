"""
fig_17_tsunami_generation.py

Scientific content: Three stacked schematic cross-sections of a subduction-
zone setting showing tsunami generation by a megathrust earthquake:
(top) pre-seismic state with the locked plate interface; (middle) co-seismic
uplift of the seafloor and resulting initial sea-surface bump; (bottom)
two-sided tsunami propagation outward from the source. Reproduces the
qualitative content of legacy slide 32 (Tsunami causes / GFZ Potsdam
schematic) of the legacy ESS 314 deck.

Geometry of the cross-section is consistent with:
  Atwater, B.F., Musumi-Rokkaku, S., Satake, K., Tsuji, Y., Ueda, K., &
  Yamaguchi, D.K. (2015). The Orphan Tsunami of 1700, 2nd ed.
  USGS Professional Paper 1707, Fig. 14. Public domain.

Output: assets/figures/fig_17_tsunami_generation.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = {
    "ocean":     "#0072B2",
    "ocean_lt":  "#7AB8E0",
    "overriding":"#E69F00",
    "subducting":"#999999",
    "rupture":   "#D55E00",
    "wave":      "#CC79A7",
    "land":      "#A87344",
}


def draw_subduction(ax, dz_seafloor=0, eta_surface=None, x=None,
                    show_rupture=False, title=""):
    """Draw a subduction-zone cross-section.
    Parameters:
      dz_seafloor: scalar uplift to apply to the seafloor (m)
      eta_surface: array, surface displacement (None for sea level)
      show_rupture: highlight the slipping fault patch
      x: x-coordinate grid (km)
    """
    # Coordinate grid (km horizontally, m vertically)
    if x is None:
        x = np.linspace(-300, 300, 600)
    # Sea surface
    if eta_surface is None:
        eta_surface = np.zeros_like(x)
    # Smooth seafloor topography:
    #  -300 to -50:  abyssal plain at -4500 m, shallowing slightly
    #     -50 to 0:   trench (down to -5500)
    #       0 to 200: continental slope rising to coast
    #     200 to 300: land at +500 m
    seafloor_base = np.zeros_like(x)
    # Abyssal-plain to trench
    abyssal = -4200 - 1300 * np.exp(-((x + 0)**2) / 1500)  # trench centered at x=0
    # Continental slope: rise from -5000 at x=0 to 0 at x=200
    slope = -5000 * (1 - np.maximum(0, np.minimum(1, x / 200)))
    # Above coast (x > 200): land
    land_pad = np.where(x > 200, 500 * np.minimum(1, (x - 200) / 80), 0)
    # Compose: use slope when x>=0, abyssal when x<0, with smoothing at trench
    seafloor_base = np.where(x < 0, abyssal,
                             np.where(x < 200, slope, land_pad))
    # Apply uplift in the rupture zone
    uplift = np.zeros_like(x)
    in_rupture = (x > 0) & (x < 180)
    if dz_seafloor != 0:
        # Bell-shaped uplift profile
        x_center = 90
        sigma = 60
        uplift[in_rupture] = dz_seafloor * np.exp(
            -((x[in_rupture] - x_center)**2) / (2 * sigma**2))
        # Subsidence on the down-dip side
        uplift[(x > 180) & (x < 280)] -= 0.4 * dz_seafloor * np.exp(
            -((x[(x > 180) & (x < 280)] - 230)**2) / (2 * 40**2))
    seafloor = seafloor_base + uplift

    # Land surface to the right
    land_x = np.array([200, 300])
    land_y = np.array([0, 700])

    # Ocean fill
    ax.fill_between(x, seafloor, eta_surface, where=(seafloor < 0),
                    color=COLORS["ocean_lt"], alpha=0.7, zorder=1)
    # Seafloor (overriding plate)
    poly_x = np.concatenate([x, x[::-1]])
    poly_y = np.concatenate([seafloor, np.full_like(x, -7000)])
    ax.fill(poly_x, poly_y, color=COLORS["overriding"], alpha=0.55, zorder=0)
    # Subducting slab (a tilted region from offshore to depth)
    slab_top_x = np.array([-300, -200, -100, 0, 100, 200, 300])
    slab_top_y = np.array([-3500, -3700, -4500, -6000, -7500, -9000, -10500])
    slab_bot_y = slab_top_y - 2500
    ax.fill_between(slab_top_x, slab_top_y, slab_bot_y,
                    color=COLORS["subducting"], alpha=0.7, zorder=-1)
    ax.plot(slab_top_x, slab_top_y, color="black", linewidth=1.0)
    # Subduction direction arrows
    for xa, ya in [(-200, -3700), (-100, -4500)]:
        ax.annotate("", xy=(xa + 60, ya - 200), xytext=(xa, ya),
                    arrowprops=dict(arrowstyle="->", color="black", lw=1.4))

    # Sea level reference
    ax.axhline(0, color="black", linestyle=":", linewidth=0.7, alpha=0.5)

    # Surface displacement
    if np.any(np.abs(eta_surface) > 0.5):
        ax.fill_between(x, 0, eta_surface, color=COLORS["wave"],
                        alpha=0.8, zorder=3)
        ax.plot(x, eta_surface, color=COLORS["wave"], linewidth=2.0, zorder=4)

    # Rupture highlight
    if show_rupture:
        # Densely sample the slab top in the rupture range and highlight
        x_rupt = np.linspace(-50, 120, 50)
        # Use the same parameterisation as slab_top to put it on the slab
        from numpy import interp
        y_rupt = interp(x_rupt, slab_top_x, slab_top_y)
        ax.plot(x_rupt, y_rupt, color=COLORS["rupture"], linewidth=5.5,
                zorder=5, solid_capstyle="round")
        # Slip arrows on the overriding plate
        ax.annotate("", xy=(80, -1500), xytext=(40, -3000),
                    arrowprops=dict(arrowstyle="->", color=COLORS["rupture"],
                                    lw=2.5))

    # Limits
    ax.set_xlim(-300, 300)
    ax.set_ylim(-7500, 2200)  # extra space for in-axes labels
    # Axis label
    ax.set_xlabel("Horizontal distance from trench (km)")
    ax.set_ylabel("Elevation (m)")
    ax.set_title(title, pad=8)


# ── Build figure ────────────────────────────────────────────────────
fig, axs = plt.subplots(3, 1, figsize=(11.0, 10.5))
x = np.linspace(-300, 300, 600)

# Top: pre-seismic state (no uplift, no surface displacement)
draw_subduction(axs[0], dz_seafloor=0, eta_surface=np.zeros_like(x), x=x,
                title="(a) Pre-seismic: locked interface accumulates strain")
# Annotation
axs[0].annotate("Locked plate interface\n(elastic loading)",
                xy=(50, -5000), xytext=(-280, -1000),
                fontsize=11,
                arrowprops=dict(arrowstyle="->", color="black", lw=1.0))
axs[0].text(220, 600, "Coast", fontsize=11, ha="center")

# Middle: co-seismic uplift, initial sea-surface bump
eta_co = np.zeros_like(x)
in_rupture = (x > 0) & (x < 180)
eta_co[in_rupture] = 4.0 * np.exp(-((x[in_rupture] - 90)**2) / (2 * 60**2))
# subsidence onshore
behind = (x > 180) & (x < 280)
eta_co[behind] = -1.6 * np.exp(-((x[behind] - 230)**2) / (2 * 40**2))
# Scale eta to be visible on the figure (5 m -> 1500 m on this y-axis)
eta_visible = eta_co * 200
draw_subduction(axs[1], dz_seafloor=4.0, eta_surface=eta_visible, x=x,
                show_rupture=True,
                title="(b) Co-seismic: rupture, seafloor uplift, sea-surface bump")
axs[1].text(90, 1700, r"Initial bump: $\eta_0 \approx 5$ m, 100 km wide",
            fontsize=11, ha="center", color=COLORS["wave"], fontweight="bold")
axs[1].text(230, -1100, "Subsidence",
            fontsize=11, ha="center", color="#555555", fontweight="bold")

# Bottom: tsunami propagating outward
xx = np.linspace(-300, 300, 600)
eta_prop = np.zeros_like(xx)
# Two-sided wave
left_wave = -1.5 * np.exp(-((xx + 120)**2) / (2 * 40**2))
right_wave = 1.5 * np.exp(-((xx - 120)**2) / (2 * 40**2))
eta_prop = (left_wave + right_wave) * 200
draw_subduction(axs[2], dz_seafloor=4.0, eta_surface=eta_prop, x=xx,
                show_rupture=False,
                title="(c) Minutes later: two-sided tsunami propagation")
# Arrows showing propagation direction
axs[2].annotate("", xy=(-220, 1200), xytext=(-100, 1200),
                arrowprops=dict(arrowstyle="->", color=COLORS["wave"], lw=2.5))
axs[2].annotate("", xy=(220, 1200), xytext=(100, 1200),
                arrowprops=dict(arrowstyle="->", color=COLORS["wave"], lw=2.5))
axs[2].text(-160, 1750, r"$c = \sqrt{gH}$ ~ 700 km/h", fontsize=11,
            ha="center", fontweight="bold", color=COLORS["wave"])
axs[2].text(160, 1750, r"$c = \sqrt{gH}$ ~ 700 km/h", fontsize=11,
            ha="center", fontweight="bold", color=COLORS["wave"])
# Note that surface displacements are not to scale
axs[2].text(0, -7000, "(Surface displacements drawn ×200 for visibility)",
            fontsize=10, ha="center", color="#555555", style="italic")

fig.tight_layout()
fig.savefig("/home/claude/ess314/assets/figures/fig_17_tsunami_generation.png",
            bbox_inches="tight")
print("Saved fig_17_tsunami_generation.png")
