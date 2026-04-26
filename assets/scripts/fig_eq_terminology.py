"""
fig_eq_terminology.py

Scientific content: Schematic block diagram defining the basic terminology
of earthquake source geometry — fault plane, focus (hypocenter), epicenter,
fault scarp at the surface, and concentric wavefronts radiating outward
from the focus.

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.
  Cambridge University Press, Ch. 1 §1.1, terminology figure.
  Stein, S. & Wysession, M. (2003). An Introduction to Seismology,
  Earthquakes, and Earth Structure. Blackwell, Ch. 1, terminology figure.

Output: assets/figures/fig_eq_terminology.png
License: CC-BY 4.0 (this script and its output).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import patches
from matplotlib.lines import Line2D

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 130, "savefig.dpi": 200,
})

# Colorblind-safe palette
C_FAULT = "#000000"
C_FOCUS = "#D55E00"
C_EPI = "#0072B2"
C_WAVE = "#56B4E9"
C_SCARP = "#CC79A7"
C_GROUND = "#E8DCC8"
C_DEEP = "#C8B89A"

fig, ax = plt.subplots(figsize=(11.5, 6.5))

# ── Surface and "ground" rendering ────────────────────────────────────
xmin, xmax = -10, 10
zmin, zmax = -3, 8        # negative z = elevation above datum
# Ground polygon — slightly rolling surface to make it three-dimensional
xs = np.linspace(xmin, xmax, 200)
surface_z = -0.4 + 0.18 * np.sin(0.6 * xs) - 0.10 * np.sin(1.3 * xs + 1.0)
# Insert a step (the fault scarp) at x = +1.5 km
scarp_x = 1.5
scarp_jump = 0.55
surface_z = np.where(xs > scarp_x, surface_z + scarp_jump, surface_z)

ax.fill_between(xs, surface_z, zmax, color=C_GROUND, zorder=1)
# A deeper "rock layer" for a sense of depth
deep_z = surface_z + 4.5 + 0.4 * np.sin(0.4 * xs)
ax.fill_between(xs, deep_z, zmax, color=C_DEEP, zorder=0)
ax.plot(xs, deep_z, color="#9D8866", lw=0.8, zorder=1)

# Surface line (ground)
ax.plot(xs, surface_z, color=C_FAULT, lw=1.5, zorder=4)

# ── Fault plane (dashed line through focus, breaks surface at the scarp) ──
focus_x, focus_z = 0.0, 4.5
fault_x = np.array([focus_x - 2.6, focus_x, focus_x + 2.4])
fault_z = np.array([focus_z + 3.6, focus_z, focus_z - 4.6])
# Resample along the line and split at the surface for visibility
ax.plot(fault_x, fault_z, color=C_FAULT, ls="--", lw=2.0, zorder=5)
# Fault arrows showing relative motion (normal-fault sense)
ax.annotate("", xy=(focus_x - 0.55, focus_z + 1.10),
            xytext=(focus_x - 1.10, focus_z + 0.55),
            arrowprops=dict(arrowstyle="->", color=C_FAULT, lw=1.4), zorder=6)
ax.annotate("", xy=(focus_x + 1.10, focus_z - 0.55),
            xytext=(focus_x + 0.55, focus_z - 1.10),
            arrowprops=dict(arrowstyle="->", color=C_FAULT, lw=1.4), zorder=6)

# ── Wavefronts (concentric circles from focus) ────────────────────────
for r in (1.5, 2.7, 3.9, 5.1, 6.3):
    circ = patches.Circle((focus_x, focus_z), radius=r, fill=False,
                          edgecolor=C_WAVE, lw=1.4, alpha=0.85, zorder=2)
    ax.add_patch(circ)
# Label one wavefront
ax.annotate("Wavefronts", xy=(focus_x - 5.0, focus_z + 0.2),
            xytext=(-9.3, 1.1), fontsize=12, color="#005a8a",
            arrowprops=dict(arrowstyle="-", color="#005a8a", lw=1.0),
            zorder=7)

# ── Focus (hypocenter) ───────────────────────────────────────────────
ax.plot(focus_x, focus_z, marker="*", color=C_FOCUS, ms=24, mec=C_FAULT,
        mew=1.0, zorder=8)
ax.annotate("Focus\n(hypocenter)", xy=(focus_x + 0.10, focus_z + 0.10),
            xytext=(focus_x + 2.6, focus_z + 1.6),
            fontsize=12.5, color=C_FAULT,
            arrowprops=dict(arrowstyle="->", color=C_FAULT, lw=1.0),
            zorder=8, ha="left",
            bbox=dict(facecolor="white", edgecolor=C_FAULT, lw=0.6,
                      boxstyle="round,pad=0.25"))

# ── Epicenter (vertical projection of focus to the surface) ──────────
epi_z = -0.4 + 0.18 * np.sin(0.6 * focus_x) - 0.10 * np.sin(1.3 * focus_x + 1.0)
ax.plot(focus_x, epi_z, marker="o", mec=C_FAULT, mfc=C_EPI, ms=14, mew=1.2,
        zorder=9)
ax.plot([focus_x, focus_x], [epi_z, focus_z], color=C_EPI, ls=":", lw=1.5,
        zorder=7)
ax.annotate("Epicenter", xy=(focus_x - 0.1, epi_z - 0.05),
            xytext=(-6.0, -1.6), fontsize=12.5, color=C_EPI, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=C_EPI, lw=1.0),
            ha="left",
            bbox=dict(facecolor="white", edgecolor=C_EPI, lw=0.6,
                      boxstyle="round,pad=0.25"),
            zorder=9)

# Depth annotation between epicenter and focus
ax.annotate("", xy=(focus_x + 0.30, focus_z),
            xytext=(focus_x + 0.30, epi_z),
            arrowprops=dict(arrowstyle="<->", color="#444444", lw=1.0),
            zorder=7)
ax.text(focus_x + 0.50, (focus_z + epi_z) / 2, "focal\ndepth, h",
        fontsize=11, color="#444444", ha="left", va="center")

# ── Fault scarp at the surface ───────────────────────────────────────
ax.annotate("Fault scarp",
            xy=(scarp_x + 0.05, -0.4 + 0.18 * np.sin(0.6 * scarp_x)
                                  - 0.10 * np.sin(1.3 * scarp_x + 1.0) + 0.25),
            xytext=(5.5, -2.0), fontsize=12, color=C_SCARP, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=C_SCARP, lw=1.0),
            ha="left",
            bbox=dict(facecolor="white", edgecolor=C_SCARP, lw=0.6,
                      boxstyle="round,pad=0.25"),
            zorder=9)

# ── Fault label ──────────────────────────────────────────────────────
ax.annotate("Fault", xy=(focus_x - 1.3, focus_z + 1.8),
            xytext=(-7.5, 4.0), fontsize=12.5, color=C_FAULT, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=C_FAULT, lw=1.0),
            ha="left",
            bbox=dict(facecolor="white", edgecolor=C_FAULT, lw=0.6,
                      boxstyle="round,pad=0.25"),
            zorder=9)

# ── Axis cosmetics ───────────────────────────────────────────────────
ax.set_xlim(xmin, xmax)
ax.set_ylim(zmax, zmin)         # invert: depth increases downward
ax.set_xlabel("Horizontal distance along the fault strike (km)")
ax.set_ylabel("Depth below datum (km)")
ax.set_title("Earthquake source geometry: fault, focus, epicenter, wavefronts",
             fontsize=14, pad=8)
ax.set_aspect("equal")
ax.grid(False)

fig.tight_layout()

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_eq_terminology.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
