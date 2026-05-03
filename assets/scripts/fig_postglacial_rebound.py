"""
fig_postglacial_rebound.py

Scientific content: Three companion panels illustrating glacial isostatic
adjustment (GIA): (a) the cartoon mantle-flow geometry beneath an ice sheet;
(b) a synthetic exponential rebound time-history with mantle-viscosity
sensitivity; (c) modelled present-day vertical uplift rates over a
formerly-glaciated region.

Reproduces conceptually:
  Whitehouse, P.L. (2018). Glacial isostatic adjustment modelling: historical
  perspectives, recent advances, and future directions. Earth Surf. Dynam. 6,
  401–429. https://doi.org/10.5194/esurf-6-401-2018  (CC BY 4.0)

  Steffen, H. & Wu, P. (2011). Glacial isostatic adjustment in Fennoscandia
  — A review of data and modelling. J. Geodyn. 52, 169–204.
  Citation only (paywalled).

Data shown are synthetic — chosen to match the order of magnitude (peak
~9 mm/yr) reported in published Fennoscandian and Laurentian models.

Output:  assets/figures/fig_postglacial_rebound.png
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

fig = plt.figure(figsize=(13.5, 9.0))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.05], hspace=0.40, wspace=0.30)

# ── Panel (a): cartoon — ice sheet pushes crust into mantle ───────────────
ax_a = fig.add_subplot(gs[0, 0])
ax_a.set_title("(a)  Loading and unloading of the lithosphere",
                loc="left", pad=10)
ax_a.set_xlim(-200, 200)
ax_a.set_ylim(-220, 80)
ax_a.set_aspect("auto")
ax_a.axis("off")

# Sea level
ax_a.axhline(0, color=C_BLUE, lw=1.0, ls="--", alpha=0.6)
# Lithosphere shape (depressed under ice)
x = np.linspace(-200, 200, 401)
litho = -50.0 - 60.0 * np.exp(-(x / 90.0)**2)
ax_a.fill_between(x, litho, np.full_like(x, -220), color=C_SKY, alpha=0.45,
                   edgecolor=C_BLACK, lw=1.0, label="Asthenosphere")
ax_a.fill_between(x, litho + 35, litho, color=C_ORANGE, alpha=0.65,
                   edgecolor=C_BLACK, lw=1.0, label="Lithosphere")
# Ice sheet
ice_top = 70.0 * np.exp(-(x / 100.0)**2)
ax_a.fill_between(x, litho + 35, litho + 35 + ice_top,
                   color="#E0F4FF", edgecolor=C_BLACK, lw=1.0, label="Ice sheet")

# Mantle flow arrows
for x0 in [-180, -160, 160, 180]:
    ax_a.annotate("", xy=(x0 * 0.5, litho[200] + 5), xytext=(x0, -150),
                   arrowprops=dict(arrowstyle="->", color=C_VERM, lw=1.5))
ax_a.text(-180, -170, "mantle flow", color=C_VERM, fontsize=11)
ax_a.text(0, 50, "ICE SHEET", ha="center", color=C_BLUE, fontsize=12,
           fontweight="bold")
ax_a.text(-160, -38, "litho-\nsphere", fontsize=10, color=C_BLACK)

ax_a.legend(loc="lower right", fontsize=10, framealpha=0.95)

# ── Panel (b): exponential rebound time-history ──────────────────────────
ax_b = fig.add_subplot(gs[0, 1])
t = np.linspace(0, 25, 500)        # ka after deglaciation
viscosities = [(0.5, "low η ($0.5\\times 10^{21}$ Pa s)", C_VERM),
               (1.0, "Earth-like η ($1\\times 10^{21}$ Pa s)", C_BLUE),
               (3.0, "high η ($3\\times 10^{21}$ Pa s)", C_GREEN)]
amplitude = 300.0   # m of total rebound after full deglaciation

for tau_norm, label, col in viscosities:
    tau = 4.5 * tau_norm     # ka — illustrative relaxation time
    u = amplitude * (1.0 - np.exp(-t / tau))
    ax_b.plot(t, amplitude - u, color=col, lw=2.4, label=label)

ax_b.axhline(0, color=C_BLACK, lw=0.6, ls="--")
ax_b.set_xlabel("Time since deglaciation  (ka)")
ax_b.set_ylabel("Remaining depression  (m)")
ax_b.set_title("(b)  Time-history depends on mantle viscosity",
                loc="left", pad=10)
ax_b.legend(loc="upper right", fontsize=10)
ax_b.grid(ls=":", lw=0.6, alpha=0.5)
ax_b.set_xlim(0, 25)

# ── Panel (c): present-day uplift map ────────────────────────────────────
ax_c = fig.add_subplot(gs[1, :])
# Synthetic radially-symmetric uplift bulls-eye, with a peak ~9 mm/yr
xx = np.linspace(-1000, 1000, 401)        # km
yy = np.linspace(-700, 700, 281)
X, Y = np.meshgrid(xx, yy)
# Two centres (mimicking Fennoscandia + Hudson Bay)
peak1 = 9.0 * np.exp(-((X + 350)**2 + (Y - 80)**2) / (2 * 290**2))
peak2 = 6.0 * np.exp(-((X - 400)**2 + (Y + 60)**2) / (2 * 320**2))
uplift = peak1 + peak2

cs = ax_c.contourf(X, Y, uplift, levels=20, cmap="RdYlBu_r")
ax_c.contour(X, Y, uplift, levels=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
              colors=C_BLACK, linewidths=0.5, alpha=0.5)
cb = fig.colorbar(cs, ax=ax_c, shrink=0.8, pad=0.02)
cb.set_label("Vertical uplift rate  (mm yr$^{-1}$)")

ax_c.set_xlabel("Distance E–W  (km)")
ax_c.set_ylabel("Distance N–S  (km)")
ax_c.set_title("(c)  Modelled present-day uplift over a formerly-glaciated region "
                "(synthetic, illustrative)", loc="left", pad=10)
ax_c.set_aspect("equal")
ax_c.grid(ls=":", lw=0.6, alpha=0.4)

# Annotate the two peaks
ax_c.plot(-350, 80, "*", color=C_BLACK, ms=14)
ax_c.plot(400, -60, "*", color=C_BLACK, ms=14)
ax_c.text(-350, 180, "peak 1", ha="center", fontsize=11)
ax_c.text(400, -180, "peak 2", ha="center", fontsize=11)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_postglacial_rebound.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
