"""
fig_correction_chain.py

Scientific content: A 200-km topographic transect demonstrating the gravity
reduction chain — observed gravity → free-air anomaly → simple Bouguer
anomaly → terrain-corrected (complete) Bouguer anomaly. Topography includes
a mountain range (Bouguer slab effect) and a valley (terrain effect).

This figure replaces the textbook reduction-chain diagram (e.g. Lowrie &
Fichtner 2020 Fig. 3.13, paywalled) with a Python-generated equivalent.

Reference values:
  • Free-air gradient   ∂g/∂h = -0.3086 mGal/m
  • Bouguer correction  2π G ρ h = 0.0419·10⁻³ × ρ × h  with ρ = 2.67 g/cm³
  • Combined slab + free-air for "normal crust" ≈ 0.197 mGal/m
  • Latitude-normal gravity at ~45°N from GRS80 (Moritz 1980, IUGG, public domain)

Output:  assets/figures/fig_correction_chain.png
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

# ── Topographic profile and "true" subsurface ──────────────────────────────
x = np.linspace(-100, 100, 801)            # km
# Mountain range (Gaussian) + valley
h = (1500.0 * np.exp(-((x + 30.0) / 25.0)**2)         # +1.5 km mountain
     - 200.0 * np.exp(-((x - 50.0) / 12.0)**2)        # -200 m valley
     + 200.0 * np.exp(-((x - 70.0) / 8.0)**2))        # ridge to its east

# A buried high-density body (causes a "true" anomaly we want to recover)
x0_body, z0_body, R_body = 5.0e3, 4_000.0, 2_000.0    # m
drho_body = 400.0                                       # kg m^-3 contrast
G = 6.67430e-11

# Pre-compute observed gravity along profile -------------------------------
# Reference normal gravity at φ = 45°N (GRS80)
g_n_45 = 980_629.4                          # mGal
# Sphere anomaly from the buried body
xm = x * 1e3                                # to metres
M_body = (4.0/3.0) * np.pi * R_body**3 * drho_body
delta_g_body_mGal = (G * M_body * z0_body /
                     ((xm - x0_body)**2 + z0_body**2)**1.5) * 1e5
# Free-air "gobs - gn" component due to elevation
free_air_effect = -0.3086 * h               # mGal (lower than gn at altitude)
# Bouguer slab effect (extra mass under the station)
rho_crust = 2670.0                          # kg m^-3
bouguer_effect = 2.0 * np.pi * G * rho_crust * h * 1e5   # mGal
# Terrain effect: nearby topography always reduces measured g
#   Approximate as a smooth function tied to local topographic roughness
roughness = np.abs(np.gradient(h, np.gradient(x))) * 1e3   # m / km gradient
terrain_effect = 0.5 * roughness            # illustrative magnitude (mGal)
terrain_effect = np.where(terrain_effect > 12.0, 12.0, terrain_effect)

# Observed gravity (g_obs):  g_n + free-air + slab − terrain + body anomaly
g_obs = g_n_45 + free_air_effect + bouguer_effect - terrain_effect + delta_g_body_mGal

# Reductions ---------------------------------------------------------------
FA_corr  = -free_air_effect                 # +0.3086·h applied
delta_g_FA      = g_obs - g_n_45 + FA_corr
B_corr   = -bouguer_effect                  # subtract the slab
delta_g_B       = delta_g_FA + B_corr
T_corr   = +terrain_effect                  # add back terrain
delta_g_CB      = delta_g_B + T_corr        # complete Bouguer anomaly

# ── Figure: 4 stacked panels ──────────────────────────────────────────────
fig, axes = plt.subplots(4, 1, figsize=(11, 10),
                          gridspec_kw={"hspace": 0.55,
                                       "height_ratios": [1.0, 1.0, 1.0, 1.0]})

# (a) Topographic profile
ax = axes[0]
ax.fill_between(x, h, np.full_like(h, h.min() - 200),
                 color=C_ORANGE, alpha=0.45, edgecolor=C_BLACK, lw=1.2)
ax.set_ylabel("Elevation (m)")
ax.set_title("(a)  Topographic profile and buried high-density body",
             loc="left")
# show buried body
theta_b = np.linspace(0, 2*np.pi, 200)
ax.plot((x0_body + R_body*np.cos(theta_b))/1e3,
        -(z0_body + R_body*np.sin(theta_b)),
        color=C_VERM, lw=2)
ax.text(x0_body/1e3 + 0.4, -z0_body, r"$\Delta\rho > 0$", color=C_VERM,
        fontsize=12)
ax.axhline(0, color=C_BLACK, lw=0.8)
ax.set_xlim(x.min(), x.max())
ax.set_ylim(-7000, 2200)
ax.grid(ls=":", lw=0.6, alpha=0.5)

# (b) Observed gravity minus normal
ax = axes[1]
ax.plot(x, g_obs - g_n_45, color=C_BLUE, lw=2.0)
ax.axhline(0, color=C_BLACK, lw=0.6, ls="--")
ax.set_ylabel(r"$g_{obs}-g_n$  (mGal)")
ax.set_title(r"(b)  Raw deviation from normal gravity:  $g_{obs}-g_n$",
             loc="left")
ax.set_xlim(x.min(), x.max())
ax.grid(ls=":", lw=0.6, alpha=0.5)

# (c) Free-air and simple Bouguer anomalies
ax = axes[2]
ax.plot(x, delta_g_FA, color=C_ORANGE, lw=2.0,
        label=r"Free-air anomaly $\Delta g_{FA}$")
ax.plot(x, delta_g_B, color=C_GREEN, lw=2.0,
        label=r"Simple Bouguer anomaly $\Delta g_B$")
ax.axhline(0, color=C_BLACK, lw=0.6, ls="--")
ax.set_ylabel("Anomaly  (mGal)")
ax.set_title("(c)  After free-air and slab corrections", loc="left")
ax.legend(loc="upper right")
ax.set_xlim(x.min(), x.max())
ax.grid(ls=":", lw=0.6, alpha=0.5)

# (d) Complete (terrain-corrected) Bouguer anomaly
ax = axes[3]
ax.plot(x, delta_g_CB, color=C_VERM, lw=2.4,
        label=r"Complete Bouguer anomaly $\Delta g_{CB}$")
ax.axhline(0, color=C_BLACK, lw=0.6, ls="--")
ax.set_xlabel("Profile distance  (km)")
ax.set_ylabel("Anomaly  (mGal)")
ax.set_title("(d)  After terrain correction — the residual reveals the body",
             loc="left")
ax.legend(loc="upper right")
ax.set_xlim(x.min(), x.max())
ax.grid(ls=":", lw=0.6, alpha=0.5)

# Annotation arrow pointing to body's signature in panel d
i_max = np.argmax(delta_g_CB)
ax.annotate("Buried body\nshows up here",
            xy=(x[i_max], delta_g_CB[i_max]),
            xytext=(35, 1.2 * delta_g_CB[i_max]),
            arrowprops=dict(arrowstyle="->", color=C_BLACK, lw=0.9),
            fontsize=11)

fig.suptitle("The gravity reduction chain across a synthetic transect",
             fontsize=15, y=0.995)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_correction_chain.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
