"""
fig_dipole_field_geometry.py

Scientific content: Earth's magnetic dipole field-line geometry, together with
the definition of the three observed-field properties at a surface station —
declination D, inclination I, and total field magnitude F — and their
decomposition into the local (X, Y, Z) components. Panel (b) shows two
orthographic views (map view = declination geometry, and side view =
inclination geometry) so that both angles are unambiguous.

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, Figs. 11.6, 11.8.

Output: assets/figures/fig_dipole_field_geometry.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch, Circle, Arc

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


def dipole_field_line(theta0_deg, r_earth=1.0, n=200):
    theta = np.linspace(np.radians(theta0_deg),
                        np.pi - np.radians(theta0_deg), n)
    r0 = r_earth / np.sin(np.radians(theta0_deg))**2
    r = r0 * np.sin(theta)**2
    x = r * np.sin(theta)
    z = r * np.cos(theta)
    return x, z


fig = plt.figure(figsize=(14.0, 6.6))
gs = fig.add_gridspec(1, 3, width_ratios=[1.0, 0.9, 0.9], wspace=0.32)

# Panel (a): meridional section
ax1 = fig.add_subplot(gs[0, 0])
earth = Circle((0, 0), 1.0, facecolor="#EAEAEA", edgecolor="k", linewidth=1.2,
               zorder=2)
ax1.add_patch(earth)
core = Circle((0, 0), 0.55, facecolor="#FFE0B2", edgecolor=COLORS[4],
              linewidth=1.0, linestyle="--", zorder=3)
ax1.add_patch(core)
ax1.text(0, 0, "outer core\n(geodynamo)", ha="center", va="center",
         fontsize=11, color=COLORS[4], zorder=4)
for theta0 in [25, 35, 50, 70]:
    xL, zL = dipole_field_line(theta0)
    ax1.plot(xL, zL, color=COLORS[0], linewidth=1.4, zorder=1)
    ax1.plot(-xL, zL, color=COLORS[0], linewidth=1.4, zorder=1)
ax1.plot([0, 0], [-1.55, 1.55], color="k", linewidth=0.8, linestyle=":",
         zorder=2)
ax1.text(0.04, 1.62, "rotation axis", fontsize=10, ha="left", va="bottom")
tilt = np.radians(11)
x_dip = 1.55 * np.sin(tilt)
z_dip = 1.55 * np.cos(tilt)
ax1.plot([-x_dip, x_dip], [-z_dip, z_dip], color=COLORS[4], linewidth=1.2,
         linestyle="--", zorder=2)
ax1.text(x_dip + 0.04, z_dip, "dipole axis\n(11°)", fontsize=10,
         ha="left", va="center", color=COLORS[4])
ax1.text(0, 1.12, "N", ha="center", va="bottom", fontsize=13, fontweight="bold")
ax1.text(0, -1.12, "S", ha="center", va="top", fontsize=13, fontweight="bold")
ar = FancyArrowPatch((0.45, 1.85), (0.40, 1.55), arrowstyle="->",
                     color=COLORS[0], linewidth=1.6, mutation_scale=14)
ax1.add_patch(ar)
ax1.text(0.50, 1.70, "B", fontsize=13, color=COLORS[0], fontstyle="italic")
ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-2.0, 2.0)
ax1.set_aspect("equal")
ax1.set_xticks([]); ax1.set_yticks([])
ax1.set_title("(a) Earth's dipole field — meridional section")
for spine in ax1.spines.values():
    spine.set_visible(False)

# Panel (b): map view, declination D
ax2 = fig.add_subplot(gs[0, 1])
L = 1.0
ax2.add_patch(Circle((0, 0), L, fill=False, edgecolor="grey", linewidth=0.6,
                     linestyle="--"))
ax2.annotate("", xy=(0, L), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="k", linewidth=1.5))
ax2.text(0, L + 0.05, "true N (X)", ha="center", va="bottom",
         fontsize=12, fontweight="bold")
ax2.annotate("", xy=(L, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="k", linewidth=1.5))
ax2.text(L + 0.04, 0, "E (Y)", ha="left", va="center", fontsize=12)
ax2.annotate("", xy=(0, -L), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="grey", linewidth=1.0))
ax2.text(0, -L - 0.04, "S", ha="center", va="top", fontsize=11, color="grey")
ax2.annotate("", xy=(-L, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="grey", linewidth=1.0))
ax2.text(-L - 0.04, 0, "W", ha="right", va="center", fontsize=11, color="grey")

D = 15.5
# H points to magnetic N: from +true_N (90 deg in conventional polar angle),
# rotate by D clockwise. With y = up = true N: x = sin(D), y = cos(D).
xH = 0.85 * np.sin(np.radians(D))
yH = 0.85 * np.cos(np.radians(D))
ax2.annotate("", xy=(xH, yH), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLORS[0],
                             linewidth=2.4, mutation_scale=14))
ax2.text(xH + 0.06, yH, "H  (mag N)", fontsize=12, color=COLORS[0],
         fontweight="bold", va="center")

# Arc from true N (90 deg in matplotlib polar) clockwise by D
arc = Arc((0, 0), 0.55, 0.55, angle=0, theta1=90 - D, theta2=90,
          color=COLORS[0], linewidth=1.6)
ax2.add_patch(arc)
ax2.text(0.13, 0.34, f"D = +{D:.1f}°", fontsize=12, color=COLORS[0],
         fontweight="bold")

ax2.set_xlim(-1.35, 1.35)
ax2.set_ylim(-1.30, 1.40)
ax2.set_aspect("equal")
ax2.set_xticks([]); ax2.set_yticks([])
ax2.set_title("(b) Map view — declination D")
for spine in ax2.spines.values():
    spine.set_visible(False)

# Panel (c): side view, inclination I
ax3 = fig.add_subplot(gs[0, 2])
ax3.plot([-1.0, 1.0], [0, 0], color="k", linewidth=1.4)
ax3.text(1.02, 0, "horizontal (H)", ha="left", va="center", fontsize=12)
ax3.annotate("", xy=(0, -1.0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="->", color="k", linewidth=1.0))
ax3.text(-0.04, -1.0, "Z (Down)", ha="right", va="top", fontsize=11)
ax3.plot([0, 0], [0, 0.55], color="grey", linewidth=0.6, linestyle=":")
ax3.text(0.02, 0.55, "up", ha="left", va="bottom", fontsize=10, color="grey")

I = 68.9
xF = 0.9 * np.cos(np.radians(I))
yF = -0.9 * np.sin(np.radians(I))
ax3.annotate("", xy=(xF, yF), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLORS[4],
                             linewidth=2.4, mutation_scale=14))
ax3.text(xF + 0.04, yF - 0.04, "F  (total field)", color=COLORS[4],
         fontsize=12, fontweight="bold", va="top", ha="left")

xH2 = 0.9 * np.cos(np.radians(I))
ax3.annotate("", xy=(xH2, 0), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLORS[0],
                             linewidth=2.0, mutation_scale=12))
ax3.text(xH2 + 0.02, 0.06, "H = F cos I", color=COLORS[0], fontsize=11)

ax3.annotate("", xy=(xH2, yF), xytext=(xH2, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLORS[3],
                             linewidth=2.0, mutation_scale=12))
ax3.text(xH2 + 0.04, yF / 2, "Z = F sin I", color=COLORS[3],
         fontsize=11, va="center")

arc2 = Arc((0, 0), 0.50, 0.50, angle=0, theta1=-I, theta2=0,
           color=COLORS[4], linewidth=1.6)
ax3.add_patch(arc2)
ax3.text(0.26, -0.10, f"I = +{I:.1f}°", fontsize=12, color=COLORS[4],
         fontweight="bold")

txt = ("Seattle 2026 (IGRF-13):\n"
       "D = +15.5°    I = +68.9°\n"
       "F = 52 900 nT")
ax3.text(0.02, 0.98, txt, transform=ax3.transAxes, fontsize=11,
         va="top", ha="left",
         bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                   edgecolor=COLORS[6], linewidth=0.8))

ax3.set_xlim(-1.15, 1.40)
ax3.set_ylim(-1.20, 0.75)
ax3.set_aspect("equal")
ax3.set_xticks([]); ax3.set_yticks([])
ax3.set_title("(c) Side view — inclination I")
for spine in ax3.spines.values():
    spine.set_visible(False)

fig.tight_layout()
fig.savefig("assets/figures/fig_dipole_field_geometry.png",
            dpi=300, bbox_inches="tight")
print("saved fig_dipole_field_geometry.png")
