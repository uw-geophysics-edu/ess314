"""
fig_17_shallow_water_setup.py

Scientific content: Schematic cross-section defining the variables of the
shallow-water wave equation: equilibrium depth H, surface displacement
eta(x,t), wavelength lambda, depth-averaged horizontal velocity v(x,t).
This is the canonical introductory figure for c = sqrt(gH) derivation
and reproduces the geometry of legacy ESS 314 slide 39.

After:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, §3.6.6.
  Pedlosky, J. (1987). Geophysical Fluid Dynamics, 2nd ed., Springer.

Output: assets/figures/fig_17_shallow_water_setup.png
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
    "legend.fontsize": 12,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = {
    "ocean": "#0072B2",
    "ocean_lt": "#A8D5F0",
    "seabed": "#A87344",
    "wave": "#0072B2",
    "annotation": "#D55E00",
}

fig, ax = plt.subplots(figsize=(11.0, 5.5))

# Domain: x from 0 to 2*lambda, depth H = 1 unit
H = 1.0
wavelength = 4.0
x = np.linspace(0, 2 * wavelength, 800)
eta = 0.10 * np.cos(2 * np.pi * x / wavelength)  # surface displacement

# Sea surface
ax.fill_between(x, -H, eta, color=COLORS["ocean_lt"], alpha=0.7, zorder=1)
ax.plot(x, eta, color=COLORS["wave"], linewidth=2.5, zorder=3)
# Still-water level
ax.axhline(0, color="black", linestyle=":", linewidth=0.8, alpha=0.5)
# Seabed
ax.fill_between(x, -H - 0.3, -H, color=COLORS["seabed"], alpha=0.85, zorder=0)
ax.axhline(-H, color="black", linewidth=1.5)

# Coordinate axes
ax.annotate("", xy=(0.05, 0.4), xytext=(0.05, -1.2),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
ax.annotate("", xy=(8.4, 0), xytext=(0, 0),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
ax.text(8.5, 0.05, r"$x$", fontsize=14, ha="left", va="bottom")
ax.text(0.10, 0.42, r"$y$", fontsize=14, ha="left", va="bottom")

# Wavelength bracket between two crests
crest1, crest2 = 0.0, wavelength
y_bracket = 0.50
ax.annotate("", xy=(crest1, y_bracket), xytext=(crest2, y_bracket),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.5))
ax.text((crest1 + crest2)/2, y_bracket + 0.05,
        r"$\lambda \;=\; c\,T$",
        ha="center", fontsize=14, fontweight="bold")

# Depth bracket
ax.annotate("", xy=(7.5, 0), xytext=(7.5, -H),
            arrowprops=dict(arrowstyle="<->", color="black", lw=1.5))
ax.text(7.65, -H/2, r"$H$", fontsize=14, fontweight="bold", va="center")

# Surface displacement label - point at a crest
crest_x = wavelength / 4   # at x = lambda/4 the cosine = cos(pi/2) = 0...
# pick where displacement is positive — at x = 0 cos=1
crest_x = 0.6
crest_y = 0.10 * np.cos(2 * np.pi * crest_x / wavelength)
ax.annotate(r"$\eta(x,t)$",
            xy=(crest_x, crest_y),
            xytext=(crest_x + 0.5, 0.30),
            fontsize=14, fontweight="bold", color=COLORS["wave"],
            arrowprops=dict(arrowstyle="->", color=COLORS["wave"], lw=1.2))
ax.text(crest_x + 0.6, 0.40, r"surface", fontsize=11, color=COLORS["wave"])
ax.text(crest_x + 0.6, 0.46, r"displacement", fontsize=11, color=COLORS["wave"])

# Velocity arrow at midpoint depth
v_x = 5.0
ax.annotate("", xy=(v_x + 0.6, -H/2), xytext=(v_x, -H/2),
            arrowprops=dict(arrowstyle="->", color=COLORS["annotation"],
                            lw=2.5))
ax.text(v_x + 0.30, -H/2 + 0.10, r"$\boldsymbol{v}(x,t)$",
        fontsize=14, color=COLORS["annotation"], fontweight="bold")
ax.text(v_x + 0.0, -H/2 - 0.14,
        "depth-averaged\nhorizontal velocity",
        fontsize=10, color=COLORS["annotation"])

# Total water column depth = H + eta annotation
hx = 2.5
ax.annotate("", xy=(hx, eta[np.searchsorted(x, hx)]),
            xytext=(hx, -H),
            arrowprops=dict(arrowstyle="<->", color="#555555", lw=1.0))
ax.text(hx + 0.05, -0.5, r"$h = H + \eta$", fontsize=12, color="#555555",
        rotation=90, va="center")

# Assumption note
ax.text(0.5 * (2 * wavelength), -1.1,
        r"Shallow-water assumption: $\eta \;\ll\; H \;\ll\; \lambda$",
        fontsize=13, ha="center", fontweight="bold",
        bbox=dict(facecolor="#FFFFE0", edgecolor="#888888",
                  boxstyle="round,pad=0.4", alpha=0.95))

# Limits and styling
ax.set_xlim(-0.4, 8.5)
ax.set_ylim(-H - 0.35, 0.65)
ax.set_aspect(2.5)
ax.axis("off")
ax.set_title("Shallow-water wave: definitions and assumptions")

fig.tight_layout()
fig.savefig("/home/claude/ess314/assets/figures/fig_17_shallow_water_setup.png",
            bbox_inches="tight")
print("Saved fig_17_shallow_water_setup.png")
