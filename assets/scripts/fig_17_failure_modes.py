"""
fig_16_failure_modes.py

Scientific content: Four side-by-side line drawings showing characteristic
building failure modes under strong ground shaking: (1) undeformed reference,
(2) soft-storey collapse with ground floor sheared, (3) frame collapse with
roof on the ground, (4) foundation failure with the building tilted.
Geometry redrawn from the legacy ESS 314 deck slides 14, 15, 17, 18, 22, 24,
26 (building schematic) and slides 16-19 (failure photographs, replaced).

After:
  ATC-72-1 (2010). Modeling and Acceptance Criteria for Seismic Design and
  Analysis of Tall Buildings. Applied Technology Council.
  FEMA P-58 (2018). Seismic Performance Assessment of Buildings.
  Federal Emergency Management Agency.

Output: assets/figures/fig_16_failure_modes.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]

GROUND_COLOR = "#8B7355"
FRAME_COLOR  = "#0072B2"
DAMAGE_COLOR = "#D55E00"


def draw_ground(ax, y0=0):
    """Hatched ground line."""
    ax.fill_between([-2, 6], y0 - 0.5, y0,
                    facecolor=GROUND_COLOR, alpha=0.7, zorder=0)
    ax.plot([-2, 6], [y0, y0], color="black", linewidth=1.5)


def draw_undeformed(ax):
    """A simple two-storey, two-bay frame, undeformed."""
    draw_ground(ax)
    # Outer rectangle
    rect = mpatches.Rectangle((1, 0), 3, 4, fill=False,
                              edgecolor=FRAME_COLOR, linewidth=2.0)
    ax.add_patch(rect)
    # Vertical column at midspan
    ax.plot([2.5, 2.5], [0, 4], color=FRAME_COLOR, linewidth=2.0)
    # Horizontal beam at mid-height
    ax.plot([1, 4], [2, 2], color=FRAME_COLOR, linewidth=2.0)
    # Force arrow
    ax.annotate("", xy=(1, 3.0), xytext=(-0.5, 3.0),
                arrowprops=dict(arrowstyle="->", color="black", lw=2.0))
    ax.text(-0.5, 3.4, r"Force $F=ma_{ground}(t)$", fontsize=11)
    ax.set_title("(a) Undeformed reference")


def draw_soft_story(ax):
    """Soft-storey: ground floor parallelogram-sheared, upper floor intact."""
    draw_ground(ax)
    # Ground floor (parallelogram)
    shear = 1.2
    poly = mpatches.Polygon([[1, 0], [4, 0],
                             [4 + shear, 2], [1 + shear, 2]],
                            closed=True, fill=False,
                            edgecolor=DAMAGE_COLOR, linewidth=2.5)
    ax.add_patch(poly)
    # Upper floor (still rectangular but offset)
    rect = mpatches.Rectangle((1 + shear, 2), 3, 2, fill=False,
                              edgecolor=FRAME_COLOR, linewidth=2.0)
    ax.add_patch(rect)
    # Crack at the kink
    ax.plot([1 + shear, 4 + shear], [2, 2], color=DAMAGE_COLOR,
            linewidth=2.5)
    # Force arrow
    ax.annotate("", xy=(1, 3.0), xytext=(-0.5, 3.0),
                arrowprops=dict(arrowstyle="->", color="black", lw=2.0))
    ax.text(2.5, -1.2, "Open ground floor\n(parking, shopfronts)",
            ha="center", fontsize=10, color=DAMAGE_COLOR, style="italic")
    ax.set_title("(b) Soft-storey collapse")


def draw_frame_collapse(ax):
    """Full frame collapse: vertical columns failed, roof slumps."""
    draw_ground(ax)
    # Tilted, partially collapsed frame
    poly = mpatches.Polygon([[1, 0], [4, 0],
                             [3.5, 1.2], [1.2, 1.4]],
                            closed=True, fill=False,
                            edgecolor=DAMAGE_COLOR, linewidth=2.5)
    ax.add_patch(poly)
    # Rubble lines
    for x_l, x_r in [(1.4, 2.0), (2.2, 2.8), (3.0, 3.6)]:
        ax.plot([x_l, x_r], [0.6, 1.0], color=DAMAGE_COLOR, linewidth=1.0)
    ax.annotate("", xy=(1, 3.0), xytext=(-0.5, 3.0),
                arrowprops=dict(arrowstyle="->", color="black", lw=2.0))
    ax.text(2.5, -1.2, "Inadequate shear\nstrength in columns",
            ha="center", fontsize=10, color=DAMAGE_COLOR, style="italic")
    ax.set_title("(c) Frame collapse")


def draw_foundation_failure(ax):
    """Tipping settlement: building rotates as a rigid body."""
    draw_ground(ax)
    # Tilt angle
    theta = np.deg2rad(15)
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    # Original corners
    corners = np.array([[1, 0], [4, 0], [4, 4], [1, 4]])
    # Rotate around (2.5, 0)
    pivot = np.array([2.5, 0])
    rotated = (corners - pivot) @ np.array([[cos_t, -sin_t],
                                            [sin_t,  cos_t]]) + pivot
    poly = mpatches.Polygon(rotated, closed=True, fill=False,
                            edgecolor=FRAME_COLOR, linewidth=2.0)
    ax.add_patch(poly)
    # Internal beam at mid-height (rotated)
    beam = np.array([[1, 2], [4, 2]])
    beam_rot = (beam - pivot) @ np.array([[cos_t, -sin_t],
                                          [sin_t, cos_t]]) + pivot
    ax.plot(beam_rot[:, 0], beam_rot[:, 1], color=FRAME_COLOR, linewidth=2.0)
    # Liquefaction zone under one foundation
    rect = mpatches.Rectangle((3.0, -0.45), 1.0, 0.45,
                              facecolor=DAMAGE_COLOR, alpha=0.6,
                              hatch="...", edgecolor="black", linewidth=0.5)
    ax.add_patch(rect)
    ax.annotate("", xy=(1, 3.0), xytext=(-0.5, 3.0),
                arrowprops=dict(arrowstyle="->", color="black", lw=2.0))
    ax.text(3.5, -1.2, "Liquefied\nfoundation soil",
            ha="center", fontsize=10, color=DAMAGE_COLOR, style="italic")
    ax.set_title("(d) Foundation failure")


# ── Build figure ────────────────────────────────────────────────────
fig, axs = plt.subplots(1, 4, figsize=(15.0, 5.0))

draw_undeformed(axs[0])
draw_soft_story(axs[1])
draw_frame_collapse(axs[2])
draw_foundation_failure(axs[3])

for ax in axs:
    ax.set_xlim(-2, 6.5)
    ax.set_ylim(-2, 5.5)
    ax.set_aspect("equal")
    ax.axis("off")

fig.tight_layout()
fig.savefig("/home/claude/ess314/assets/figures/fig_16_failure_modes.png",
            bbox_inches="tight")
print("Saved fig_16_failure_modes.png")
