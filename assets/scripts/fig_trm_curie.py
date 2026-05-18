"""
fig_trm_curie.py

Scientific content: Thermoremanent magnetization (TRM) acquisition during the
cooling of a magnetic mineral through its Curie temperature. The figure shows
two curves: (a) saturation magnetization J_s(T)/J_s(0) following the Brillouin-
like temperature dependence with J_s -> 0 at T = T_C, and (b) the cumulative
TRM acquired during cooling in an ambient field H_0, which is dominantly
acquired in the blocking-temperature range slightly below T_C.

Typical T_C values:
  magnetite (Fe3O4)            ≈ 580 °C
  hematite  (alpha-Fe2O3)      ≈ 680 °C
  titanomagnetite (TM60)       ≈ 150 °C  (e.g. seafloor basalt)
  pyrrhotite                   ≈ 320 °C

Reproduces the scientific content of:
  Dunlop, D. J. & Özdemir, Ö. (2001). Rock Magnetism: Fundamentals and
  Frontiers, Cambridge University Press, Fig. 8.1. (Cited only.)
  Tauxe, L. et al. (2018), Essentials of Paleomagnetism, 4th ed.,
  https://earthref.org/MagIC/books/Tauxe/Essentials/ (open access), Sec. 7.6.

Output: assets/figures/fig_trm_curie.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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

# Saturation magnetization curve, normalised: J_s(T)/J_s(0) ≈ (1 - T/T_C)^beta
# with beta near 0.43 for a Heisenberg ferromagnet — we use a smoothed model.
T_C = 580.0  # Curie temperature, °C (magnetite)
T = np.linspace(0, 700, 700)

# Saturation magnetization (zero above T_C)
Js = np.where(T < T_C, ((T_C - T) / T_C) ** 0.43, 0.0)

# TRM acquisition: in a constant cooling rate through T_C, the TRM is
# acquired in a narrow "blocking" interval just below T_C, where the
# relaxation time grows rapidly. A logistic model captures the essential
# shape.
T_block = 540.0   # blocking-temperature centre
width = 25.0      # blocking interval half-width
trm = 1.0 / (1.0 + np.exp((T - T_block) / width))
# Floor and ceiling: at T > T_C no remanence; below ~T_C - 100 fully blocked
trm[T > T_C] = 0.0

fig, ax = plt.subplots(figsize=(10.0, 5.8))

ax.plot(T, Js, color=COLORS[0], linewidth=2.4,
        label=r"$J_s(T) / J_s(0)$  —  saturation magnetization")
ax.plot(T, trm, color=COLORS[4], linewidth=2.4, linestyle="--",
        label="Cumulative TRM in H₀ during cooling")

# Curie-temperature marker
ax.axvline(T_C, color=COLORS[6], linewidth=1.0, linestyle=":")
ax.text(T_C - 8, 0.55, f"Curie T  = {T_C:.0f} °C\n(magnetite)",
        ha="right", va="center", fontsize=11, color=COLORS[6])

# Blocking interval shading
ax.axvspan(T_block - width, T_block + width, color=COLORS[1], alpha=0.18)
ax.text(T_block - 60, 0.30, "blocking\ninterval\n(TRM locked in)",
        ha="right", va="center", fontsize=11, color=COLORS[4])

# Other Curie temperatures of interest (tickers at the bottom edge, not top)
others = [(150, "TM60\n(seafloor basalt)"),
          (320, "pyrrhotite"),
          (680, "hematite")]
for T0, lab in others:
    ax.axvline(T0, color="grey", linewidth=0.7, linestyle=":", alpha=0.6)
    ax.text(T0, -0.05, lab, ha="center", va="top", fontsize=10,
            color="grey")

# Arrows showing cooling direction
ax.annotate("",
            xy=(40, 0.97), xytext=(180, 0.97),
            arrowprops=dict(arrowstyle="->", color=COLORS[6], linewidth=1.6))
ax.text(110, 1.00, "cooling", ha="center", va="bottom", fontsize=11,
        color=COLORS[6])

ax.set_xlabel("Temperature  T  (°C)")
ax.set_ylabel("Normalised magnetization")
ax.set_xlim(0, 720)
ax.set_ylim(-0.18, 1.10)
ax.set_title("Thermoremanent magnetization acquired on cooling through "
             "the Curie temperature")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper right", framealpha=0.95)

fig.tight_layout()
fig.savefig("assets/figures/fig_trm_curie.png",
            dpi=300, bbox_inches="tight")
print("saved fig_trm_curie.png")
