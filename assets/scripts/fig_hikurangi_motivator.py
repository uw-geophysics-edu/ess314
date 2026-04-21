"""
Schematic 2-D cross-section of the Hikurangi subduction margin showing
combined refraction (OBS, long offsets → velocity model) and
reflection (streamer, short offsets → structural picks) imaging.

Geometry is schematic, inspired by published cross-sections from the
Hikurangi margin (Wallace et al. 2009 EPSL; Barker et al. 2018 Science;
Henrys et al. 2006 GRL). All numerical values are approximate.
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe

# Colorblind-safe palette (Wong 2011)
C_BLUE   = "#0072B2"
C_ORANGE = "#E69F00"
C_VERM   = "#D55E00"
C_PINK   = "#CC79A7"
C_GREEN  = "#009E73"

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# Geometry  (x=0: North Island / continent; x=200: open Pacific Ocean)
# ---------------------------------------------------------------------------
XMAX, ZMAX = 200.0, 26.0
x_arr = np.linspace(0, XMAX, 800)

def _sf(x):
    """Seafloor depth (km).  Positive = below sea surface."""
    # Land on left (x<35), gently sloping shelf (35-90), slope+trench (90-120),
    # flat abyssal plain on right (120+).
    shelf   = np.where(x < 35, -0.3,
              np.where(x < 90,  0.8 * (x - 35) / 55,
              np.where(x < 105, 0.8 + 2.8 * (x - 90) / 15,
              np.where(x < 118, 3.6 + 0.3 * np.sin(np.pi * (x - 105) / 13),
                                4.0))))
    return shelf

def _pi(x):
    """Plate interface depth (km) — shallows toward open ocean."""
    # At x=0 (inland North Island): ~20 km; at x=110 (trench): ~3.8 km
    z  = 20.0 - (x / XMAX) * 16.5
    # Gentle listric concavity
    z += 1.0 * np.exp(-((x - 60)**2) / (2 * 30**2))
    return np.clip(z, _sf(x) + 0.4, 25.0)

def _bs(x):
    """Base of sediment / top of basement (km)."""
    thk = 2.5 * np.exp(-((x - 105)**2) / (2 * 35**2)) + 0.5
    return np.minimum(_sf(x) + thk, _pi(x) - 0.4)

def _ms(x):
    """Mid-sediment horizon (km) — representative stratigraphic layer."""
    return 0.5 * (_sf(x) + _bs(x))

def _moho(x):
    """Continental Moho (km)."""
    return 22.0 - 4.0 * np.tanh((x - 80) / 30)

# ---------------------------------------------------------------------------
# Smooth velocity model
# ---------------------------------------------------------------------------
xx = np.linspace(0, XMAX, 350)
zz = np.linspace(0, ZMAX, 250)
XX, ZZ = np.meshgrid(xx, zz)

SF  = _sf(XX);  PI = _pi(XX);  BS = _bs(XX);  MO = _moho(XX)

V = np.full_like(XX, 4.5)  # default

# water
V = np.where(ZZ < SF, 1.5, V)
# sediments
m = (ZZ >= np.maximum(SF, 0)) & (ZZ < BS) & (ZZ < PI)
f = np.clip((ZZ - np.maximum(SF, 0)) / np.maximum(BS - np.maximum(SF, 0), 0.1), 0, 1)
V = np.where(m, 1.8 + 1.7 * f, V)
# accretionary / oceanic basement
m2 = (ZZ >= BS) & (ZZ < PI) & (ZZ >= 0)
V = np.where(m2, 3.5 + 1.0 * np.clip((ZZ - BS) / np.maximum(PI - BS, 0.1), 0, 1), V)
# continental crust
m3 = (ZZ >= np.maximum(SF, 0)) & (ZZ < MO) & (ZZ < PI) & (XX < 110)
V = np.where(m3 & ~m, 5.5 + 1.0 * np.clip((ZZ - BS) / np.maximum(MO - BS, 0.1), 0, 1), V)
# upper mantle
V = np.where((ZZ >= MO) & (XX < 110), 7.8, V)
# slab
V = np.where((ZZ >= PI) & (ZZ < PI + 10), 6.5, V)
# sub-slab mantle
V = np.where(ZZ >= PI + 10, 7.9, V)
# mask land
V = np.where(SF < 0, np.nan, V)

# ---------------------------------------------------------------------------
# Figure
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(13, 5.5))

im = ax.pcolormesh(XX, ZZ, V, cmap="RdYlBu_r", vmin=1.5, vmax=7.9,
                   shading="auto", zorder=1, alpha=0.88)
cb = fig.colorbar(im, ax=ax, pad=0.01, shrink=0.82, label="P-wave velocity (km/s)")
cb.set_ticks([1.5, 2, 3, 4, 5, 6, 7, 7.9])

# --- Land fill (grey-brown) ---
sf_a = _sf(x_arr)
ax.fill_between(x_arr, np.minimum(sf_a, 0), 0,
                where=sf_a < 0, color="#B9A47A", alpha=1.0, zorder=2)
ax.fill_between(x_arr, sf_a, 0,
                where=sf_a < 0, color="#B9A47A", alpha=1.0, zorder=2)
# surface above sea level
ax.axhline(0, color="#3A7CC3", lw=1.0, ls="-", zorder=3, alpha=0.5)

# --- Water fill ---
ax.fill_between(x_arr, 0, np.maximum(sf_a, 0),
                where=sf_a > 0, color="#A8D5F2", alpha=0.65, zorder=2)

# --- Seafloor ---
ax.plot(x_arr, sf_a, color="#003B6F", lw=1.8, zorder=5)

# --- Structural picks ---
bs_a  = _bs(x_arr);  ms_a = _ms(x_arr);  pi_a = _pi(x_arr)

# Mid-sediment horizon
ok1 = (ms_a > sf_a) & (ms_a < pi_a) & (ms_a < ZMAX)
ax.plot(x_arr[ok1], ms_a[ok1], color=C_ORANGE, lw=1.8, ls="--", zorder=6,
        label="Sediment horizon (reflection pick)")

# Base of sediments
ok2 = (bs_a > sf_a) & (bs_a < pi_a) & (bs_a < ZMAX)
ax.plot(x_arr[ok2], bs_a[ok2], color=C_VERM, lw=2.2, ls="--", zorder=6,
        label="Base of sediments (reflection pick)")

# Plate interface (the prize)
ok3 = (pi_a > sf_a) & (pi_a < ZMAX)
ax.plot(x_arr[ok3], pi_a[ok3], color=C_ORANGE, lw=3.5, zorder=7,
        label="Plate interface (Hikurangi décollement)")

# Continental Moho
mo_a = _moho(x_arr)
ok4 = (mo_a < pi_a) & (mo_a < ZMAX) & (x_arr < 115)
ax.plot(x_arr[ok4], mo_a[ok4], color=C_PINK, lw=2.0, ls="-.", zorder=6,
        label="Continental Moho")

# ---------------------------------------------------------------------------
# Instruments
# ---------------------------------------------------------------------------
# Airgun (star) at sea surface, x=75
src_x = 75.0
ax.plot(src_x, 0.0, marker=(8, 2, 0), color=C_VERM, ms=16, zorder=10,
        mec=C_VERM, label="Airgun source")

# Towed streamer (x=82 to 140)
sx = np.linspace(80, 148, 200)
ax.fill_between(sx, -0.15, 0.15, color=C_VERM, alpha=0.55, zorder=8)
ax.text(115, -0.8, "Towed streamer → reflections", ha="center", fontsize=8,
        color=C_VERM, style="italic", zorder=11)

# OBS on seafloor
obs_xs = [40, 58, 75, 95, 115, 140, 160]
for ox in obs_xs:
    oz = max(_sf(np.array([ox]))[0], 0)
    ax.plot(ox, oz, "v", color=C_GREEN, ms=9, zorder=10, mec="k", mew=0.5)
ax.text(95, _sf(np.array([95]))[0] + 0.8, "Ocean-bottom seismometers → refractions",
        ha="center", fontsize=8, color=C_GREEN, style="italic", zorder=11)

# ---------------------------------------------------------------------------
# Ray paths
# ---------------------------------------------------------------------------
# Reflection: source → plate interface → streamer
refl_recv = 135.0
refl_midpt = (src_x + refl_recv) / 2       # 105
refl_z = _pi(np.array([refl_midpt]))[0]
ax.plot([src_x, refl_midpt, refl_recv], [0.0, refl_z, 0.0],
        color=C_BLUE, lw=2.2, zorder=9, label="Reflection ray (→ streamer)")

# Refraction: source → head wave along base-of-sed → distant OBS
obs_refr = 160.0
obs_z    = max(_sf(np.array([obs_refr]))[0], 0)
# Rough head-wave geometry: down to crit interface, horizontal, back up
down_x = (src_x + 95) / 2;  up_x = (95 + obs_refr) / 2
dz = _bs(np.array([down_x]))[0];   uz = _bs(np.array([up_x]))[0]
ax.plot([src_x, down_x, up_x, obs_refr],
        [0.0, dz, uz, obs_z],
        color=C_GREEN, lw=2.0, ls=":", zorder=9, alpha=0.9,
        label="Refraction head wave (→ distant OBS)")

# ---------------------------------------------------------------------------
# Region labels
# ---------------------------------------------------------------------------
def ann(x, z, txt, c="white", fs=8, fw="bold", ha="center"):
    ax.text(x, z, txt, ha=ha, va="center", fontsize=fs, color=c,
            fontweight=fw, style="italic",
            path_effects=[pe.withStroke(linewidth=2, foreground="black")])

ann(35, 5.0,  "Forearc / North Island", c="white")
ann(100, 2.0, "Accretionary\nprism", c="#001F3F", fw="normal")
ann(150, 14,  "Subducting\nPacific plate", c="white")
ann(50, 21,   "Upper mantle", c="#FFE082")
ax.text(0.01, 0.97,
        "Hikurangi subduction margin, New Zealand (schematic, after Wallace et al. 2009; Barker et al. 2018)",
        transform=ax.transAxes, ha="left", va="top", fontsize=7.5, style="italic",
        bbox=dict(fc="white", ec="gray", alpha=0.85, boxstyle="round,pad=0.3"))

# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------
ax.set_ylim(ZMAX, -1.5)
ax.set_xlim(0, XMAX)
ax.set_xlabel("Distance from North Island coast (km)", fontsize=11)
ax.set_ylabel("Depth (km)", fontsize=11)
ax.set_title(
    "Combining refraction and reflection imaging at Hikurangi\n"
    "Refraction (OBS, long offsets) → absolute velocity model  |  "
    "Reflection (streamer, short offsets) → structural image",
    fontsize=11, fontweight="bold")
ax.legend(loc="lower right", fontsize=7.5, ncol=2, framealpha=0.9, edgecolor="gray")
ax.grid(True, alpha=0.15, lw=0.5)

plt.tight_layout()
fig.savefig("assets/figures/fig_hikurangi_motivator.png", dpi=180, bbox_inches="tight")
print("Saved fig_hikurangi_motivator.png")
