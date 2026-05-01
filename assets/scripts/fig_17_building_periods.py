"""
fig_16_building_periods.py

Scientific content: Two-panel figure illustrating the rule of thumb
T_building ~ N/10 s. Left panel: building height vs natural period for
real structures, with the linear scaling overlaid. Right panel: shows
which earthquake source types (crustal, intraslab, megathrust) produce
the most damaging shaking for each building class.

Reproduces the qualitative content of slides 12-13 of the legacy ESS 314
deck (tall buildings resonate at long periods). After:
  ATC-72-1 (2010). Modeling and Acceptance Criteria for Seismic Design
  and Analysis of Tall Buildings. Applied Technology Council.
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, §3.6.5.

Output: assets/figures/fig_16_building_periods.png
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

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.0, 5.5))

# ── LEFT: Period vs storeys ─────────────────────────────────────────
# Compiled from ATC-72 / engineering literature
buildings = [
    ("Single-family\nwood frame", 1, 0.10),
    ("4-storey\napartment", 4, 0.45),
    ("10-storey\noffice", 10, 1.05),
    ("20-storey\nbuilding", 20, 2.10),
    ("Columbia Tower\n(76 storeys)", 76, 6.4),
    ("Tokyo Skytree\n(634 m)", 130, 10.0),
    ("Akashi Bridge\n(1991 m span)", 0, 14.0),  # bridges separately
]

ax1.set_xlabel("Number of storeys $N$")
ax1.set_ylabel(r"Fundamental period $T$ (s)")
ax1.set_title("Tall buildings resonate at long periods")

# Rule-of-thumb line
N_grid = np.linspace(0, 140, 200)
T_rule = N_grid / 10.0
ax1.plot(N_grid, T_rule, color=COLORS[0], linewidth=2.4, linestyle="--",
         label=r"Rule of thumb: $T \approx N/10$ s")

# Data points (excluding bridges) - custom label offsets to avoid overlap
label_offsets = {
    "Single-family\nwood frame": (3, -0.7),
    "4-storey\napartment":       (8,  -0.4),
    "10-storey\noffice":         (12,  -0.3),
    "20-storey\nbuilding":       (16,  -0.5),
    "Columbia Tower\n(76 storeys)": (-22, 0.7),
    "Tokyo Skytree\n(634 m)":    (-30, -1.4),
}
for name, N, T in buildings[:-1]:
    if N > 0:
        ax1.plot(N, T, "o", color=COLORS[4], markersize=10, zorder=5,
                 markeredgecolor="black", markeredgewidth=0.5)
        dx, dy = label_offsets.get(name, (5, 0.5))
        ax1.annotate(name, xy=(N, T), xytext=(N + dx, T + dy),
                     fontsize=10)

ax1.set_xlim(-5, 145)
ax1.set_ylim(-0.5, 13)
ax1.grid(alpha=0.3)
ax1.legend(loc="lower right")

# ── RIGHT: Period bands vs source types ─────────────────────────────
ax2.set_xlabel(r"Period $T$ (s)")
ax2.set_title("Each source type excites a different period band")
ax2.set_xlim(0.05, 30)
ax2.set_xscale("log")

# Period bands for source types (semi-quantitative ranges)
sources = [
    ("Crustal earthquake\n($M_W$ 5-7, e.g. Seattle Fault)", 0.05, 1.5,
     COLORS[3], 0.85),
    ("Intraslab earthquake\n($M_W$ 6-7, e.g. 2001 Nisqually)", 0.1, 2.5,
     COLORS[1], 0.65),
    ("Megathrust earthquake\n($M_W$ 8-9, Cascadia)", 0.5, 30,
     COLORS[4], 0.45),
]

y_positions = [0.85, 0.55, 0.25]
for (name, T_lo, T_hi, color, alpha), y in zip(sources, y_positions):
    ax2.barh(y, width=T_hi - T_lo, left=T_lo, height=0.18,
             color=color, alpha=alpha, edgecolor="black", linewidth=0.6)
    # Place label outside the bar to avoid being washed out
    ax2.text(T_hi * 1.1, y, name, va="center", ha="left", fontsize=10)

# Building bands as vertical lines on the same axis
ax2.axvline(0.1, color=COLORS[6], linestyle=":", linewidth=1.2, alpha=0.7)
ax2.axvline(1.0, color=COLORS[6], linestyle=":", linewidth=1.2, alpha=0.7)
ax2.axvline(7.0, color=COLORS[6], linestyle=":", linewidth=1.2, alpha=0.7)

ax2.text(0.1, 0.04, "Wood-frame house",
         fontsize=10, ha="left", rotation=90, va="bottom")
ax2.text(1.0, 0.04, "10-storey building",
         fontsize=10, ha="left", rotation=90, va="bottom")
ax2.text(7.0, 0.04, "Columbia Tower",
         fontsize=10, ha="left", rotation=90, va="bottom")

ax2.set_yticks([])
ax2.set_ylim(0, 1.05)
ax2.grid(alpha=0.3, axis="x", which="both")
ax2.set_xticks([0.1, 0.3, 1, 3, 10, 30])
ax2.set_xticklabels(["0.1", "0.3", "1", "3", "10", "30"])

fig.tight_layout()
fig.savefig("/home/claude/ess314/assets/figures/fig_16_building_periods.png",
            bbox_inches="tight")
print("Saved fig_16_building_periods.png")
