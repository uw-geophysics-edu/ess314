"""
fig_dipole_anomaly_shapes.py

Scientific content: The total-field anomaly above a buried, induced-only
magnetic dipole depends strongly on the inclination I of the inducing
geomagnetic field. At the magnetic pole (I = 90 deg), the field points
straight down and the induced dipole creates a symmetric positive total-
field anomaly directly over the source. At the magnetic equator (I = 0 deg),
the inducing field is horizontal and the resulting total-field anomaly is
strongly antisymmetric, with a negative lobe to the magnetic north of the
source and a positive lobe to the south (for a north-magnetised source, the
geometry of the anomaly is reversed). At mid-latitudes the anomaly is
intermediate — slightly asymmetric, with a small negative trough on one side
of the main positive peak. This latitude dependence is the central
complication that distinguishes magnetic from gravity interpretation.

This figure plots the total-field anomaly ΔF(x) along a north-south profile
for a dipole at depth z = 600 m and magnetic moment m = 1.0 A m^2 (arbitrary
normalisation), evaluated at three inclinations: I = 0, 45, 90 deg.

Reproduces the scientific content of:
  Blakely, R. J. (1995). Potential Theory in Gravity and Magnetic Applications,
  Cambridge University Press, Fig. 5.6. (Cited only.)
  Reford, M. S. & Sumner, J. S. (1964). Aeromagnetics. Geophysics 29, 482-516.
  (Cited only.)

Output: assets/figures/fig_dipole_anomaly_shapes.png
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

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def induced_dipole_anomaly(x, z, I_deg, m=1.0):
    """Total-field anomaly along a N-S profile above a buried induced dipole.

    Coordinates: x is the horizontal offset (positive to magnetic north of
    the source); z is the depth of the dipole (positive downward).

    The source is induced by an ambient field of inclination I_deg (and zero
    declination, so F_earth lies in the x-z plane). For an induced dipole,
    the magnetisation direction equals the ambient-field direction. The
    total-field anomaly is approximately the component of the dipole field
    along the direction of F_earth (valid because |ΔF| << |F_earth|).

    Returns ΔF in arbitrary units proportional to m / (4π).
    """
    I = np.radians(I_deg)
    # Source location: (0, 0, z) in (x, y, z) with z down; observation at
    # (x, 0, 0) on the surface. Vector from source to observation:
    r_vec_x = x
    r_vec_z = -z       # observation is at z=0; source at z; so dz = -z
    r = np.sqrt(r_vec_x ** 2 + r_vec_z ** 2)
    # Unit vector r-hat
    rhx = r_vec_x / r
    rhz = r_vec_z / r
    # Direction of magnetisation = direction of F_earth.
    # F_earth points to magnetic N with component (cos I, sin I) in (x, z)
    # since z is down: at the pole (I=90) the field points straight down,
    # so (mx, mz) = (0, 1). At the equator (I=0) it points along +x,
    # (1, 0).
    mx = np.cos(I)
    mz = np.sin(I)
    # m . r-hat
    mdotr = mx * rhx + mz * rhz
    # Dipole vector field components:
    # B_i = (mu0 m / 4 pi r^3) (3 (m.r-hat) r-hat_i - m_i)
    Bx = (3 * mdotr * rhx - mx) / r ** 3
    Bz = (3 * mdotr * rhz - mz) / r ** 3
    # Project onto F_earth direction to get total-field anomaly
    dF = Bx * mx + Bz * mz
    return m * dF


# Profile setup
x = np.linspace(-3000, 3000, 601)
z = 600.0    # depth, m
m = 1.0e10   # arbitrary moment to give readable amplitudes

inclinations = [0, 45, 90]
labels = ["I = 0°   (magnetic equator)",
          "I = 45°  (mid-latitude)",
          "I = 90°  (magnetic pole)"]
linestyles = ["-", "-", "-"]

fig, axes = plt.subplots(1, 3, figsize=(15.0, 5.0),
                         gridspec_kw=dict(wspace=0.30))

for ax, I, lab in zip(axes, inclinations, labels):
    dF = induced_dipole_anomaly(x, z, I, m=m)
    ax.plot(x / 1000, dF, color=COLORS[0], linewidth=2.4)
    ax.axhline(0, color="grey", linewidth=0.7, linestyle="--")
    ax.axvline(0, color=COLORS[6], linewidth=0.5, linestyle=":")
    # Mark source location and depth
    ax.scatter([0], [ax.get_ylim()[0] * 0.05], color=COLORS[4], s=80,
               marker="v", zorder=5)
    ax.set_title(lab, color=COLORS[0])
    ax.set_xlabel("Distance from source  (km)")
    if ax is axes[0]:
        ax.set_ylabel("Total-field anomaly  ΔF  (arb. units)")
    ax.grid(True, alpha=0.3)
    ax.set_xlim(-3, 3)
    # Add a note in the upper-right with the qualitative description
    if I == 0:
        note = "symmetric (even):\ncentral negative\nwith side positives"
    elif I == 45:
        note = "asymmetric:\npositive peak with\nnegative shoulder"
    else:
        note = "symmetric positive\npeak directly over\nsource"
    ax.text(0.97, 0.97, note, transform=ax.transAxes, fontsize=10.5,
            ha="right", va="top",
            bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                      edgecolor=COLORS[6], linewidth=0.6))

fig.suptitle("Magnetic anomaly shape over a buried induced dipole "
             "(z = 600 m) versus inclination of the inducing field",
             fontsize=14, y=1.02)

fig.tight_layout()
fig.savefig("assets/figures/fig_dipole_anomaly_shapes.png",
            dpi=300, bbox_inches="tight")
print("saved fig_dipole_anomaly_shapes.png")
