"""
fig_trm_curie.py — REVISED 2026-05

Scientific content: Acquisition of thermoremanent magnetisation (TRM) by a
magnetite grain cooling through its Curie temperature in an external
field H_0. The figure shows:

  • The temperature dependence of the saturation magnetisation J_s(T),
    which falls smoothly from J_s(0) at T = 0 to zero at T_C ≈ 580 °C.
  • The cumulative TRM acquired during cooling, which is locked in over
    a narrow blocking interval just below T_C.

REVISION (Marine, 2026-05): The temperature axis is now reversed so that
*cooling* — the physical process — proceeds from LEFT to RIGHT on the
plot, matching the natural reading direction. The x-axis runs from
high temperature (left) to low temperature (right). The y-axis shows
*normalised* magnetisation J/J_s(0), defined explicitly in the caption
and via an inset.

Pacific Northwest Curie temperatures shown as tick marks for context:
  • Titanomagnetite TM60: T_C ≈ 150 °C (Juan de Fuca seafloor basalt)
  • Pyrrhotite:           T_C ≈ 320 °C (hydrothermal ore deposits)
  • Magnetite:            T_C ≈ 580 °C (most continental rocks)
  • Hematite:             T_C ≈ 680 °C (red beds, metamorphics)

Reference: Tauxe et al. (2018), *Essentials of Paleomagnetism*, 5th Web
Edition, Ch. 7. Open access: https://earthref.org/MagIC/books/Tauxe/2010/
Reference: Dunlop, D. J. and Özdemir, Ö. (1997). *Rock Magnetism:
Fundamentals and Frontiers*. Cambridge University Press.
DOI: 10.1017/CBO9780511612794

Output: assets/figures/fig_trm_curie.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Global rcParams ─────────────────────────────────────────────────
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

# Colorblind-safe palette
C_JS    = "#0072B2"   # blue — saturation magnetisation curve
C_TRM   = "#E69F00"   # orange — cumulative TRM curve
C_BLOCK = "#E69F00"   # orange — blocking-interval shading

# ── Curie temperatures (°C) ──────────────────────────────────────
T_C_TM60      = 150.0
T_C_PYR       = 320.0
T_C_MAGNETITE = 580.0
T_C_HEMATITE  = 680.0

# ── Build curves (use magnetite as the reference mineral) ────────
T = np.linspace(0.0, 720.0, 1001)

# J_s(T): Brillouin-like form normalised so that J_s(0) = 1 and J_s(T_C) = 0.
# Use J_s(T) = (1 - (T/T_C))**beta with beta ~ 0.4 for a magnetite-like curve.
beta = 0.43
T_C = T_C_MAGNETITE
Js  = np.zeros_like(T)
below = T < T_C
Js[below] = (1.0 - T[below] / T_C)**beta

# Blocking interval — narrow window just below T_C where the TRM is locked in.
T_block_top    = T_C - 15.0    # 565 °C
T_block_bottom = T_C - 65.0    # 515 °C

# Cumulative TRM acquired during cooling: zero above the blocking interval,
# rises through the blocking interval, plateaus below it.
def trm_acquired(T):
    """TRM normalised so that the low-T plateau value is 1."""
    out = np.zeros_like(T)
    above_block = T >= T_block_top
    in_block    = (T < T_block_top) & (T > T_block_bottom)
    below_block = T <= T_block_bottom
    # Smooth S-shape in the blocking interval
    s = (T_block_top - T[in_block]) / (T_block_top - T_block_bottom)
    out[in_block]    = 0.5 * (1 - np.cos(np.pi * s))
    out[below_block] = 1.0
    return out

trm = trm_acquired(T)

# ── Figure layout ───────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(11.0, 6.6))

# Blocking interval shading
ax.axvspan(T_block_bottom, T_block_top, color=C_BLOCK, alpha=0.20,
           zorder=1, label=None)
# Label the blocking interval (place text inside the band, mid-height)
ax.text((T_block_top + T_block_bottom) / 2, 0.50,
        "Blocking\ninterval\n(TRM locked\nin here)",
        fontsize=11, ha="center", va="center", color="#8C5A00",
        style="italic", zorder=2)

# Plot J_s(T)
ax.plot(T, Js, color=C_JS, linewidth=3.2,
        label=r"$J_s(T)\,/\,J_s(0)$  —  spontaneous magnetisation of magnetite", zorder=3)

# Plot cumulative TRM
ax.plot(T, trm, color=C_TRM, linewidth=3.2, linestyle="--",
        label=r"Cumulative TRM acquired during cooling in $H_0$", zorder=4)

# Vertical line at T_C
ax.axvline(T_C_MAGNETITE, color=C_JS, linestyle=":", linewidth=1.6, alpha=0.7,
           zorder=2)
ax.text(T_C_MAGNETITE + 10, 0.83,
        f"$T_C$ = {T_C_MAGNETITE:.0f} °C\n(magnetite)",
        fontsize=11, ha="left", va="center", color=C_JS,
        bbox=dict(boxstyle="round,pad=0.30", facecolor="white",
                  edgecolor=C_JS, linewidth=1.2))

# Other PNW-relevant Curie temperatures: shown as vertical reference lines
# (no axis-bottom labels — those clip too easily; use an inline label box)
for tT, tag, col in [
    (T_C_TM60,     "TM60: 150°C",       "#444444"),
    (T_C_PYR,      "pyrrhotite: 320°C", "#444444"),
    (T_C_HEMATITE, "hematite: 680°C",   "#444444"),
]:
    ax.axvline(tT, color="#888888", linewidth=0.8, linestyle=":",
               alpha=0.65, zorder=1)

# Reference-temperature annotation box at middle-top, between the data and the cooling arrow
ax.text(0.42, 0.85,
        "Other Curie temperatures in PNW rocks\n"
        " ▪ TM60 (basalt seafloor): $T_C$ ≈ 150 °C\n"
        " ▪ Pyrrhotite (ore deposits): $T_C$ ≈ 320 °C\n"
        " ▪ Hematite (red beds): $T_C$ ≈ 680 °C\n"
        "(dotted vertical lines show their positions)",
        transform=ax.transAxes,
        fontsize=11, ha="left", va="top", color="#333333",
        bbox=dict(boxstyle="round,pad=0.40", facecolor="#FAFAFA",
                  edgecolor="#888888", linewidth=1.0),
        zorder=10)

# ── Cooling arrow at the top (now points LEFT-TO-RIGHT visually,
#    because the x-axis is reversed: high T on left, low T on right) ─
ax.annotate("",
            xy=(60, 1.13), xytext=(660, 1.13),
            arrowprops=dict(arrowstyle="-|>", lw=3.0, color="#222222",
                            mutation_scale=22))
ax.text(360, 1.18, "  cooling  →  ", fontsize=13, ha="center", va="bottom",
        fontweight="bold", color="#222222")

# ── Inset / explanation box: what "normalised magnetisation" means ─
# Placed at upper-right (low-T side, where data is fully saturated)
ax.text(0.985, 0.55,
        "Why ‘normalised’?\n"
        "Both curves are divided by the\n"
        "low-temperature saturation value\n"
        "$J_s(0)$, so the y-axis runs from 0 to 1\n"
        "regardless of the absolute magnetic\n"
        "moment of the grain. This lets the\n"
        "temperature dependence of any\n"
        "ferri/ferromagnetic mineral be\n"
        "plotted on a common scale.",
        transform=ax.transAxes,
        fontsize=11, ha="right", va="top",
        bbox=dict(boxstyle="round,pad=0.45", facecolor="#FAFAFA",
                  edgecolor="#444444", linewidth=1.0),
        zorder=10)

# ── Axes settings — INVERT X so cooling reads left→right ──────────
ax.set_xlim(720, 0)        # NB: reversed (high T on left)
ax.set_ylim(-0.05, 1.30)

ax.set_xlabel("Temperature  T  (°C)   —   high T on the left, low T on the right",
              fontsize=12.5)
ax.set_ylabel(r"Normalised magnetisation  $J\,/\,J_s(0)$"+"\n(zero to one, dimensionless)",
              fontsize=12.5)
ax.set_title("Thermoremanent magnetisation (TRM) is acquired as the grain cools through $T_C$",
             fontsize=13.5, pad=14)
ax.grid(True, alpha=0.25, zorder=0)

# Move legend to the lower-left (data fills the top-right)
ax.legend(loc="lower left", framealpha=0.95)

fig.tight_layout()
fig.savefig("../figures/fig_trm_curie.png",
            dpi=300, bbox_inches="tight")
plt.close(fig)
print("Wrote assets/figures/fig_trm_curie.png")
