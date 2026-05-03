"""
fig_buried_sphere.py

Scientific content: The classical gravity anomaly Δg(x) over a buried sphere
of density contrast Δρ at depth z, demonstrating the half-max rule for
estimating depth from anomaly width: z = x_(1/2) / 0.766. Three depths
are overlaid to show the depth-vs-width tradeoff.

Reproduces conceptually:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, §3.4 (UW Libraries e-book; not reproduced).
  Reynolds, J.M. (2011). An Introduction to Applied and Environmental
  Geophysics, 2nd ed., Wiley, §2.6 (citation only — paywalled).

Output:  assets/figures/fig_buried_sphere.png
License: CC-BY 4.0
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.size":       13,
    "axes.titlesize":  15,
    "axes.labelsize":  13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi":      150,
    "savefig.dpi":     300,
})

C_BLUE, C_ORANGE, C_SKY, C_GREEN, C_VERM, C_PINK, C_BLACK = (
    "#0072B2", "#E69F00", "#56B4E9", "#009E73",
    "#D55E00", "#CC79A7", "#000000",
)

G = 6.67430e-11

def delta_g_sphere(x, z, R, drho):
    """Vertical-component gravity anomaly (mGal) above a sphere centred at
    (0, z) with radius R and density contrast Δρ (kg/m³). x in metres."""
    M = (4.0 / 3.0) * np.pi * R**3 * drho
    return (G * M * z / (x**2 + z**2)**1.5) * 1e5    # m/s² → mGal

# ── Three depths to compare ────────────────────────────────────────────────
R_const, drho_const = 200.0, 600.0    # 200-m radius body, +600 kg/m³
depths = [400.0, 800.0, 1600.0]
labels = [f"$z = {int(z)}$ m" for z in depths]
colors = [C_BLUE, C_VERM, C_GREEN]

x_m = np.linspace(-3000.0, 3000.0, 1201)

fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(10, 8.0),
                                      gridspec_kw={"height_ratios": [1.0, 1.4],
                                                   "hspace": 0.30})

# (a) Geometry sketch ------------------------------------------------------
ax_top.set_xlim(-3000, 3000)
ax_top.set_ylim(2000, -300)               # depth positive downward, surface at top
ax_top.axhline(0, color=C_BLACK, lw=1.4)
ax_top.text(-2900, -150, "Surface  (gravimeter stations  ▼)", fontsize=11, va="bottom")
# stations
for xs in np.linspace(-2800, 2800, 15):
    ax_top.plot(xs, 0, "v", color=C_BLACK, ms=6, mec=C_BLACK)
# bodies
theta = np.linspace(0, 2*np.pi, 120)
for z, col, lbl in zip(depths, colors, labels):
    ax_top.fill(R_const*np.cos(theta), z + R_const*np.sin(theta),
                color=col, alpha=0.60, edgecolor=C_BLACK, lw=1.2,
                label=lbl + r",  $R=200$ m,  $\Delta\rho=+600$ kg m$^{-3}$")
ax_top.set_xlabel("Profile distance $x$  (m)")
ax_top.set_ylabel("Depth $z$  (m)")
ax_top.set_title("(a)  Three buried spheres, identical mass, varying depth",
                 loc="left")
ax_top.legend(loc="lower right", fontsize=10)
ax_top.grid(ls=":", lw=0.6, alpha=0.5)

# (b) Anomalies + half-max construction -----------------------------------
for z, col, lbl in zip(depths, colors, labels):
    dg = delta_g_sphere(x_m, z, R_const, drho_const)
    ax_bot.plot(x_m, dg, color=col, lw=2.2, label=lbl)

# Mark half-max construction on the deepest curve only (z = 1600 m)
z_demo = 1600.0
dg_demo = delta_g_sphere(x_m, z_demo, R_const, drho_const)
gmax = dg_demo.max()
half = 0.5 * gmax
# Find x where dg = half (positive side)
ix = np.argmin(np.abs(dg_demo[x_m > 0] - half))
x_half = x_m[x_m > 0][ix]

ax_bot.axhline(half, color=C_BLACK, ls=":", lw=1.0)
ax_bot.axhline(gmax, color=C_BLACK, ls=":", lw=1.0)
ax_bot.axvline(x_half, color=C_GREEN, ls="--", lw=1.4)
ax_bot.axvline(-x_half, color=C_GREEN, ls="--", lw=1.4)
ax_bot.annotate("", xy=(x_half, half - 0.0009), xytext=(-x_half, half - 0.0009),
                arrowprops=dict(arrowstyle="<->", color=C_GREEN, lw=1.4))
ax_bot.text(0, half - 0.0028, r"$2\,x_{1/2}$", color=C_GREEN, ha="center",
            fontsize=12, fontweight="bold")
# half-max rule annotation
z_est = x_half / 0.766
ax_bot.text(0.99, 0.97,
            f"Half-max rule for sphere:\n"
            r"$z = x_{1/2}/0.766$" + f"\n"
            r"$x_{1/2}=$" + f" {x_half:.0f} m  "
            r"$\Rightarrow z\approx$" + f" {z_est:.0f} m\n"
            f"(actual $z = {int(z_demo)}$ m)",
            transform=ax_bot.transAxes, ha="right", va="top",
            fontsize=11,
            bbox=dict(boxstyle="round,pad=0.4", fc="white",
                      ec=C_BLACK, lw=0.8))

ax_bot.set_xlabel("Profile distance $x$  (m)")
ax_bot.set_ylabel(r"Gravity anomaly $\Delta g$  (mGal)")
ax_bot.set_title("(b)  Surface gravity profiles — wider and weaker with depth",
                 loc="left")
ax_bot.legend(loc="upper left")
ax_bot.set_xlim(-3000, 3000)
ax_bot.grid(ls=":", lw=0.6, alpha=0.5)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_buried_sphere.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
