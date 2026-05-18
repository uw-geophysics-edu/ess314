"""
fig_dipole_field_geometry.py

Scientific content: Earth's magnetic dipole field-line geometry, together with
the definition of the three observed-field properties at a surface station —
declination D, inclination I, and total field magnitude F — and their
decomposition into the local (X, Y, Z) components. Panel (b) shows two
orthographic views (map view = declination geometry, and side view =
inclination geometry) so that both angles are unambiguous.

Panel (a) draws the outer-core geodynamo as a *cylinder* (the tangent cylinder
of dynamo theory) whose axis is aligned with the rotation/dipole axis: the
cylinder is tangent to the solid inner core and runs through the full height
of the outer core, capturing the geometry of the columnar convection rolls
that generate the main field. The Earth is drawn large relative to all
annotation, so that the planetary geometry dominates the visual.

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, Figs. 11.6, 11.8.

Output: assets/figures/fig_dipole_field_geometry.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import FancyArrowPatch, Circle, Arc, Rectangle, Ellipse

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


fig = plt.figure(figsize=(15.5, 7.2))
gs = fig.add_gridspec(1, 3, width_ratios=[1.55, 0.80, 0.80], wspace=0.22)

# ---------------------------------------------------------------------------
# Panel (a): meridional section through Earth
# ---------------------------------------------------------------------------
ax1 = fig.add_subplot(gs[0, 0])

R_EARTH = 1.0
R_CMB = 0.547      # outer-core / mantle boundary (3 480 km / 6 371 km)
R_IC = 0.191       # inner-core boundary           (1 220 km / 6 371 km)

earth = Circle((0, 0), R_EARTH, facecolor="#DCDCDC", edgecolor="k",
               linewidth=1.6, zorder=2)
ax1.add_patch(earth)

oc = Circle((0, 0), R_CMB, facecolor="#FFD27F", edgecolor=COLORS[4],
            linewidth=1.0, zorder=3)
ax1.add_patch(oc)

# Tangent cylinder, axis aligned with rotation axis (vertical).
tc_color = COLORS[4]
tc = Rectangle((-R_IC, -R_CMB), 2 * R_IC, 2 * R_CMB,
               facecolor=tc_color, alpha=0.30, edgecolor=tc_color,
               linewidth=1.4, linestyle="--", zorder=4)
ax1.add_patch(tc)
for zlid in (R_CMB, -R_CMB):
    ax1.add_patch(Ellipse((0, zlid), 2 * R_IC, 0.045,
                          facecolor=tc_color, alpha=0.55,
                          edgecolor=tc_color, linewidth=1.0, zorder=5))

# Inner core
ic = Circle((0, 0), R_IC, facecolor="#E65A2F", edgecolor="k",
            linewidth=0.8, zorder=6)
ax1.add_patch(ic)

# Convective columns outside the tangent cylinder, parallel to rotation axis.
for x_col in (-0.40, -0.30, 0.30, 0.40):
    ax1.plot([x_col, x_col], [-R_CMB + 0.04, R_CMB - 0.04],
             color=COLORS[4], linewidth=0.9, alpha=0.55, zorder=5)
    for z_curl in (-0.30, 0.0, 0.30):
        ax1.annotate("", xy=(x_col + 0.05, z_curl + 0.06),
                     xytext=(x_col - 0.05, z_curl - 0.06),
                     arrowprops=dict(arrowstyle="->", color=COLORS[4],
                                     linewidth=0.7, alpha=0.7),
                     zorder=5)

# Dipole field lines
for theta0 in [22, 32, 45, 62]:
    xL, zL = dipole_field_line(theta0)
    ax1.plot(xL, zL, color=COLORS[0], linewidth=1.5, zorder=1)
    ax1.plot(-xL, zL, color=COLORS[0], linewidth=1.5, zorder=1)

ax1.plot([0, 0], [-1.55, 1.55], color="k", linewidth=0.9, linestyle=":",
         zorder=2)
ax1.text(0.0, 1.60, "rotation axis", fontsize=10, ha="center", va="bottom")

tilt = np.radians(11)
x_dip = 1.40 * np.sin(tilt)
z_dip = 1.40 * np.cos(tilt)
ax1.plot([-x_dip, x_dip], [-z_dip, z_dip], color=COLORS[4], linewidth=1.3,
         linestyle="--", zorder=2)
ax1.text(x_dip + 0.04, z_dip + 0.02, "dipole axis (11°)", fontsize=10,
         ha="left", va="bottom", color=COLORS[4])

ax1.text(0, R_EARTH + 0.05, "N", ha="center", va="bottom",
         fontsize=14, fontweight="bold")
ax1.text(0, -R_EARTH - 0.05, "S", ha="center", va="top",
         fontsize=14, fontweight="bold")

ar = FancyArrowPatch((0.50, 1.78), (0.42, 1.42), arrowstyle="->",
                     color=COLORS[0], linewidth=1.8, mutation_scale=15)
ax1.add_patch(ar)
ax1.text(0.55, 1.62, "B", fontsize=14, color=COLORS[0], fontstyle="italic")


def leader(ax, x0, y0, x1, y1, text, color="k", ha="left"):
    ax.annotate(text, xy=(x0, y0), xytext=(x1, y1),
                fontsize=10.5, ha=ha, va="center", color=color,
                arrowprops=dict(arrowstyle="-", color=color, linewidth=0.8))


leader(ax1, 0.00, 0.00, -2.20, 0.05, "inner core\n(solid Fe)",
       color="#E65A2F", ha="left")
leader(ax1, 0.40, 0.20, 1.65, 0.55,
       "outer core\n(liquid Fe–Ni)", color=COLORS[4], ha="left")
leader(ax1, -0.16, -0.45, -2.20, -0.60,
       "tangent cylinder\n(coaxial with rotation axis;\ncolumnar dynamo flow)",
       color=tc_color, ha="left")
leader(ax1, 0.85, 0.40, 1.65, 1.10, "mantle &\nlithosphere",
       color="#555555", ha="left")

ax1.set_xlim(-2.65, 2.35)
ax1.set_ylim(-1.85, 1.95)
ax1.set_aspect("equal")
ax1.set_xticks([]); ax1.set_yticks([])
ax1.set_title("(a) Meridional section — dipole field and tangent-cylinder geodynamo")
for spine in ax1.spines.values():
    spine.set_visible(False)

# ---------------------------------------------------------------------------
# Panel (b): map view, declination D
# ---------------------------------------------------------------------------
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
xH = 0.85 * np.sin(np.radians(D))
yH = 0.85 * np.cos(np.radians(D))
ax2.annotate("", xy=(xH, yH), xytext=(0, 0),
             arrowprops=dict(arrowstyle="-|>", color=COLORS[0],
                             linewidth=2.4, mutation_scale=14))
ax2.text(xH + 0.06, yH, "H  (mag N)", fontsize=12, color=COLORS[0],
         fontweight="bold", va="center")

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

# ---------------------------------------------------------------------------
# Panel (c): side view, inclination I
# ---------------------------------------------------------------------------
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
ax3.text(0.02, 0.98, txt, transform=ax3.transAxes, fontsize=10.5,
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
