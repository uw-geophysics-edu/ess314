"""
fig_flat_vs_dipping_migration.py

Scientific content:
  Three-panel figure showing why migration complexity increases with dip.
  Panel (a): Flat reflector — the normal ray IS vertical. Plotting
  beneath S at depth vt/2 is exactly correct. Migration = time-to-depth.
  Panel (b): Weak dip (10°) — the normal ray tilts slightly off vertical.
  Small but real horizontal and vertical mispositioning appears.
  Panel (c): Steep dip (30°) — the full mispositioning problem from the
  main lecture figure.

  Key pedagogical progression:
    flat → "migration is just z = vt/2"
    weak dip → "small errors creep in"
    steep dip → "migration is essential"

Output: assets/figures/fig_flat_vs_dipping_migration.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 9.5,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

C_BLUE = "#0072B2"; C_ORANGE = "#E69F00"; C_SKY = "#56B4E9"
C_GREEN = "#009E73"; C_VERM = "#D55E00"; C_PINK = "#CC79A7"; C_BLACK = "#000000"

v = 2.0  # km/s

# Three cases: flat (0°), weak dip (10°), steep dip (30°)
cases = [
    {"theta_deg": 0,  "label": "(a)  Flat reflector ($\\theta = 0°$)",
     "sublabel": "No mispositioning — $z = vt/2$ is exact"},
    {"theta_deg": 10, "label": "(b)  Weak dip ($\\theta = 10°$)",
     "sublabel": "$\\Delta x = 0.21$ km,  depth error = 2%"},
    {"theta_deg": 30, "label": "(c)  Steep dip ($\\theta = 30°$)",
     "sublabel": "$\\Delta x = 0.60$ km,  depth error = 13%"},
]

d = 1.2  # normal-ray length for all cases
y_src = 1.5  # source position

fig, axes = plt.subplots(1, 3, figsize=(16, 5.5), sharey=True)

for ax, case in zip(axes, cases):
    theta_deg = case["theta_deg"]
    theta = np.deg2rad(theta_deg)

    # True reflection point R
    R_x = y_src + d * np.sin(theta)
    R_z = d * np.cos(theta)
    # Apparent position C
    C_x = y_src
    C_z = d

    # Surface line
    x_surf = np.linspace(0, 3.5, 200)
    ax.plot(x_surf, np.zeros_like(x_surf), color=C_BLACK, lw=1.2)

    # Reflector
    if theta_deg == 0:
        # Flat reflector across the panel
        ax.plot([0, 3.5], [R_z, R_z], color=C_BLUE, lw=2.8)
    else:
        # Dipping reflector centered on R
        s = np.linspace(-1.2, 1.8, 200)
        refl_x = R_x + s * np.cos(theta)
        refl_z = R_z + s * np.sin(theta)
        mask = (refl_x >= -0.1) & (refl_x <= 3.6)
        ax.plot(refl_x[mask], refl_z[mask], color=C_BLUE, lw=2.8)

    # Actual ray path S → R (vermilion)
    ax.plot([y_src, R_x], [0, R_z], color=C_VERM, lw=2.2, zorder=4)

    # Right-angle square at R (if dipping)
    if theta_deg > 0:
        sq = 0.06
        refl_u = np.array([np.cos(theta), np.sin(theta)])
        norm_u = np.array([-np.sin(theta), np.cos(theta)])
        sq_pts = np.array([
            [R_x, R_z],
            [R_x + sq*refl_u[0], R_z + sq*refl_u[1]],
            [R_x + sq*refl_u[0] + sq*norm_u[0],
             R_z + sq*refl_u[1] + sq*norm_u[1]],
            [R_x + sq*norm_u[0], R_z + sq*norm_u[1]],
        ])
        ax.plot(sq_pts[[0,1,2,3,0], 0], sq_pts[[0,1,2,3,0], 1],
                color=C_VERM, lw=0.8)

    # Assumed vertical path (pink dashed) — only if dipping
    if theta_deg > 0:
        ax.plot([y_src, y_src], [0, d], color=C_PINK, lw=1.8, linestyle=":")
        # Apparent position C
        ax.plot(C_x, C_z, marker="o", markersize=11, color=C_PINK,
                markeredgecolor=C_BLACK, zorder=6)
        ax.text(C_x - 0.22, C_z + 0.06, "C", fontsize=12, color=C_PINK,
                fontweight="bold")

    # Source/receiver
    ax.plot(y_src, 0, marker="v", markersize=14, color=C_ORANGE,
            markeredgecolor=C_BLACK, zorder=6)
    ax.text(y_src + 0.08, -0.12, "S", fontsize=12, color=C_ORANGE,
            fontweight="bold")

    # True reflection point R
    ax.plot(R_x, R_z, marker="*", markersize=18, color=C_VERM,
            markeredgecolor=C_BLACK, zorder=6)
    if theta_deg == 0:
        ax.text(R_x + 0.10, R_z + 0.04, "R", fontsize=12, color=C_VERM,
                fontweight="bold")
    else:
        ax.text(R_x + 0.10, R_z - 0.08, "R", fontsize=12, color=C_VERM,
                fontweight="bold")

    # Label d on the ray
    mid_x = (y_src + R_x) / 2
    mid_z = (0 + R_z) / 2
    if theta_deg == 0:
        ax.text(mid_x + 0.08, mid_z, "$d$", fontsize=13, color=C_VERM,
                fontweight="bold")
    else:
        ax.text(mid_x + 0.06, mid_z - 0.06, "$d$", fontsize=13,
                color=C_VERM, fontweight="bold")

    # Δx arrow if dipping
    if theta_deg > 0:
        ax.annotate("", xy=(R_x, -0.06), xytext=(y_src, -0.06),
                    arrowprops=dict(arrowstyle="<->", color=C_BLACK, lw=1.0))
        dx_val = d * np.sin(theta)
        ax.text((y_src + R_x) / 2, -0.16,
                f"$\\Delta x = {dx_val:.2f}$ km",
                fontsize=10, ha="center")

    # Depth annotations
    if theta_deg == 0:
        # For flat: z = vt/2 = d, which is correct
        ax.annotate(
            "$z = vt/2 = d$\n(exact for flat layers)",
            xy=(y_src, R_z), xytext=(0.15, 0.45),
            fontsize=10, color=C_GREEN, fontstyle="italic",
            arrowprops=dict(arrowstyle="->", color=C_GREEN, lw=1.0),
        )
    else:
        # Show true depth vs apparent depth
        depth_err_pct = (1 - np.cos(theta)) * 100
        ax.annotate(
            f"true depth\n$d\\cos\\theta = {R_z:.2f}$ km",
            xy=(R_x, R_z), xytext=(2.4, 0.45),
            fontsize=9.5, color=C_VERM, fontstyle="italic",
            arrowprops=dict(arrowstyle="->", color=C_VERM, lw=0.8),
        )
        ax.annotate(
            f"plotted at\n$d = {d:.2f}$ km",
            xy=(C_x, C_z), xytext=(0.15, 1.55),
            fontsize=9.5, color=C_PINK, fontstyle="italic",
            arrowprops=dict(arrowstyle="->", color=C_PINK, lw=0.8),
        )

    # Panel formatting
    ax.set_xlim(0.0, 3.5)
    ax.set_ylim(1.8, -0.30)
    ax.set_xlabel("x (km)")
    ax.set_title(case["label"], fontsize=12, fontweight="bold")
    ax.set_aspect("equal")
    ax.grid(alpha=0.25)

    # Sublabel at bottom of panel
    ax.text(1.75, 1.72, case["sublabel"], fontsize=10, ha="center",
            color=C_BLACK, fontstyle="italic",
            bbox=dict(boxstyle="round,pad=0.3", fc="wheat", ec="gray",
                      alpha=0.7))

axes[0].set_ylabel("z, depth (km)")

fig.suptitle("From flat to dipping: why migration complexity grows with dip",
             fontsize=14, fontweight="bold", y=1.01)

fig.tight_layout()
fig.savefig("assets/figures/fig_flat_vs_dipping_migration.png",
            bbox_inches="tight", dpi=300)
plt.close(fig)
print("Saved fig_flat_vs_dipping_migration.png")
