"""
fig_flexural_bulge.py

Scientific content: Elastic flexure of a thin plate under a vertical line
load. Three panels: (a) cartoon geometry of plate bending under a topographic
load, (b) deflection profile w(x) computed from the analytical solution,
(c) effect of varying flexural rigidity D (equivalently, elastic thickness Te)
on the wavelength and amplitude of the flexural bulge.

Reproduces conceptually:
  Turcotte, D.L. & Schubert, G. (2014). Geodynamics, 3rd ed., Cambridge,
  Ch. 3 (citation only — paywalled).

  Watts, A.B. & Burov, E.B. (2003). Lithospheric strength and its relationship
  to the elastic and seismogenic layer thickness. Earth Planet. Sci. Lett.
  213, 113–131. https://doi.org/10.1016/S0012-821X(03)00289-9 (citation only).

Solution used:
  Plate equation: D w'''' + (ρ_m - ρ_w) g w = q(x)
  For a line load V₀ at x=0 in a fluid of density (ρ_m - ρ_w):
      w(x) = (V₀ α³ / 8 D) exp(-|x|/α) ( cos(|x|/α) + sin(|x|/α) )
  where  α = (4 D / ((ρ_m - ρ_w) g))^(1/4)  is the flexural parameter.

Output:  assets/figures/fig_flexural_bulge.png
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

# Plate flexure constants ──────────────────────────────────────────────────
E   = 70e9          # Young's modulus, Pa
nu  = 0.25          # Poisson's ratio
g   = 9.81          # m/s^2
rho_m = 3300.0
rho_w = 1030.0
delta_rho = rho_m - rho_w     # mantle - water restoring force

def D_from_Te(Te):
    return E * Te**3 / (12.0 * (1.0 - nu**2))

def alpha_from_D(D):
    return (4.0 * D / (delta_rho * g))**0.25

def w_line_load(x, V0, Te):
    D = D_from_Te(Te)
    a = alpha_from_D(D)
    return (V0 * a**3 / (8.0 * D)) * np.exp(-np.abs(x)/a) * \
           (np.cos(np.abs(x)/a) + np.sin(np.abs(x)/a))

# Common load
V0 = 1.5e12          # N/m  (illustrative line load)
x = np.linspace(-800e3, 800e3, 801)

# ── Figure: 3 panels ───────────────────────────────────────────────────────
fig = plt.figure(figsize=(13.5, 9.0))
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.0], hspace=0.45, wspace=0.30)

# Panel (a): cartoon ───────────────────────────────────────────────────────
ax_a = fig.add_subplot(gs[0, 0])
ax_a.set_title("(a)  An elastic plate flexes under a topographic load",
                loc="left", pad=10)
ax_a.set_xlim(-800, 800)
ax_a.set_ylim(-12, 6)
ax_a.axis("off")

# Plate geometry
Te_demo = 25e3        # 25 km elastic thickness
w = w_line_load(x, V0, Te_demo)
plate_top = -w / 1e3                    # km, sign flipped (downward positive in km)

# Plate (lithosphere)
ax_a.fill_between(x / 1e3, plate_top - 0.4, plate_top + 0.4,
                   color=C_ORANGE, alpha=0.65, edgecolor=C_BLACK, lw=1.1,
                   label="Elastic lithosphere")
# Mantle below
ax_a.fill_between(x / 1e3, plate_top + 0.4, np.full_like(x, -12),
                   color=C_SKY, alpha=0.4)
ax_a.text(700, -10, "Mantle", color=C_BLACK, fontsize=11, ha="right")

# Load on top
load_x = np.linspace(-50, 50, 50)
load_top = 1.5 + 1.5 * np.exp(-(load_x / 25)**2)
ax_a.fill_between(load_x, plate_top[len(x)//2 - 25 : len(x)//2 + 25] - 0.4,
                   load_top, color=C_VERM, alpha=0.65, edgecolor=C_BLACK)
ax_a.text(0, 4.5, "topographic load", ha="center", color=C_VERM, fontsize=11)

# Forebulge label
ix_max = np.argmax(plate_top[x > 0])
xb = x[x > 0][ix_max] / 1e3
ax_a.annotate("forebulge", xy=(xb, plate_top[x > 0][ix_max]),
                xytext=(450, -3.0), fontsize=11,
                arrowprops=dict(arrowstyle="->", color=C_BLACK, lw=0.9))

ax_a.legend(loc="lower right", fontsize=10)

# Panel (b): w(x) for one Te ──────────────────────────────────────────────
ax_b = fig.add_subplot(gs[0, 1])
Te_demo = 25e3
w = w_line_load(x, V0, Te_demo)
ax_b.plot(x / 1e3, w * 1e3, color=C_BLUE, lw=2.4)        # mm display
ax_b.axhline(0, color=C_BLACK, lw=0.6, ls="--")
ax_b.set_xlabel("Distance from load  (km)")
ax_b.set_ylabel("Plate deflection  $w(x)$  (m, downward positive)")
ax_b.set_title(f"(b)  Deflection profile, $T_e = {Te_demo/1e3:.0f}$ km",
                loc="left", pad=10)
# Also label the flexural parameter
a = alpha_from_D(D_from_Te(Te_demo))
ax_b.axvline(a / 1e3, ls=":", color=C_VERM, lw=1.3)
ax_b.axvline(-a / 1e3, ls=":", color=C_VERM, lw=1.3)
ax_b.text(a / 1e3 + 18, 0.95 * (w * 1e3).max(),
           rf"$\alpha={a/1e3:.0f}$ km", color=C_VERM, fontsize=11)
ax_b.invert_yaxis()             # downward = positive on plot
ax_b.grid(ls=":", lw=0.6, alpha=0.5)

# Panel (c): vary Te ───────────────────────────────────────────────────────
ax_c = fig.add_subplot(gs[1, :])
for Te, col in zip([10e3, 25e3, 50e3, 80e3],
                    [C_VERM, C_BLUE, C_GREEN, C_PINK]):
    w = w_line_load(x, V0, Te)
    a = alpha_from_D(D_from_Te(Te))
    ax_c.plot(x / 1e3, w * 1e3, color=col, lw=2.0,
              label=fr"$T_e={Te/1e3:.0f}$ km,  $\alpha={a/1e3:.0f}$ km")

ax_c.axhline(0, color=C_BLACK, lw=0.6, ls="--")
ax_c.set_xlabel("Distance from load  (km)")
ax_c.set_ylabel("Plate deflection  $w(x)$  (m, downward positive)")
ax_c.set_title("(c)  Increasing elastic thickness $T_e$ widens "
                "and reduces the deflection",
                loc="left", pad=10)
ax_c.legend(loc="lower right", fontsize=11)
ax_c.invert_yaxis()
ax_c.grid(ls=":", lw=0.6, alpha=0.5)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_flexural_bulge.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
