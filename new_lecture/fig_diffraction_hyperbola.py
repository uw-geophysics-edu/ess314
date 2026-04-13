"""
fig_diffraction_hyperbola.py

Scientific content:
    Any discontinuity in the subsurface (fault tip, unconformity edge,
    buried channel edge) acts as a Huygens secondary source. The resulting
    diffraction hyperbola has the equation:

        t_diff(x) = (2/V1) * sqrt((x - x_s)^2 + z_s^2)

    This is identical in form to a primary reflection hyperbola from a
    flat reflector at depth z_s. However, a diffraction:
      (1) has nearly constant amplitude across all offsets (isotropic emission);
      (2) represents energy from a SINGLE POINT, not a flat interface;
      (3) migrates to collapse to a point, not a line.

    An unmigrated seismic section over a SYNCLINE produces a "bowtie"
    pattern: the two dipping limbs each generate a distinct hyperbola;
    their cross-over creates the characteristic X shape. Migration
    collapses the bowtie to the true syncline geometry.

    Panel A: point scatterer geometry with fan of rays to surface receivers.
    Panel B: diffraction hyperbola in t(x) space compared with a primary.
    Panel C: synthetic seismic section showing flat primary + diffraction
             from a fault-tip scatterer (unmigrated).

Reproduces scientific content of:
    Sheriff, R.E. & Geldart, L.P. (1995). Exploration Seismology, 2nd ed.
    Cambridge University Press. Chapter 4, §4.4 (Diffractions).
    Hagedoorn, J.G. (1954). A process of seismic reflection interpretation.
    Geophys. Prosp., 2(2), 85–127. https://doi.org/10.1111/j.1365-2478.1954.tb01281.x

Output: assets/figures/fig_diffraction_hyperbola.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

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

BLUE   = "#0072B2"
ORANGE = "#E69F00"
GREEN  = "#009E73"
RED    = "#D55E00"
GRAY   = "#888888"
BLACK  = "#000000"

rng = np.random.default_rng(3)

# ── Model parameters ─────────────────────────────────────────────────────────
V1   = 2000.0    # m/s
x_s  = 0.0       # m  (scatterer horizontal position)
z_s  = 1000.0    # m  (scatterer depth)
z_r  = 600.0     # m  (flat reflector depth)

# ── Travel-time equations ─────────────────────────────────────────────────────
x_arr = np.linspace(-3000, 3000, 500)    # m

t_diff = (2/V1) * np.sqrt((x_arr - x_s)**2 + z_s**2)   # diffraction
t_prim = np.sqrt((2*z_r/V1)**2 + x_arr**2/V1**2)        # flat reflector

# ── Ricker wavelet ────────────────────────────────────────────────────────────
dt = 0.002
nt = 1001
t_full = np.arange(nt) * dt

def ricker(f0, dt, t_half=0.10):
    tw = np.arange(-t_half, t_half, dt)
    u  = (np.pi * f0 * tw)**2
    return (1 - 2*u) * np.exp(-u)

wav = ricker(30.0, dt)

# ── Synthetic section: flat primary + diffraction at fault-tip scatterer ──────
offsets_sect = np.linspace(-3000, 3000, 120)   # pseudo offset = CMP location
# Here we treat each "trace" as a zero-offset trace at horizontal position x
gather_s = np.zeros((nt, len(offsets_sect)))

for ix, xr in enumerate(offsets_sect):
    spike = np.zeros(nt)
    # Flat reflector primary (zero-offset model)
    t_prim_z = 2*z_r / V1
    idx_p = int(round(t_prim_z / dt))
    if idx_p < nt:
        spike[idx_p] += 1.0

    # Diffraction from point scatterer at (x_s=0, z_s)
    t_diff_z = (2/V1) * np.sqrt((xr - x_s)**2 + z_s**2)
    idx_d = int(round(t_diff_z / dt))
    if idx_d < nt:
        spike[idx_d] += 0.65   # slightly lower amplitude

    gather_s[:, ix] = fftconvolve(spike, wav, mode="same")
    gather_s[:, ix] += rng.standard_normal(nt) * 0.025

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(17, 7))
gs  = fig.add_gridspec(1, 3, wspace=0.40)
ax_geo  = fig.add_subplot(gs[0, 0])
ax_tx   = fig.add_subplot(gs[0, 1])
ax_sect = fig.add_subplot(gs[0, 2])

# ── Panel A: geometry cartoon ─────────────────────────────────────────────────
ax = ax_geo
ax.set_xlim(-1500, 1500)
ax.set_ylim(1300, -200)
ax.set_xlabel("Horizontal position (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("(A) Point scatterer geometry", fontsize=13)

# Surface
ax.axhline(0, color=BLACK, lw=2)

# Fan of rays from scatterer to surface
n_rays = 9
x_rays = np.linspace(-1200, 1200, n_rays)
for xr in x_rays:
    ax.plot([x_s, xr], [z_s, 0], color=ORANGE, lw=0.9, alpha=0.55)
    ax.plot(xr, 0, "v", color=BLACK, ms=6, zorder=5)

# Flat reflector
ax.axhline(z_r, color=BLUE, lw=2.0, ls="--", label=f"Flat reflector ($z={z_r:.0f}$ m)")

# Fault line (vertical) down to scatterer
ax.plot([x_s, x_s], [z_r, z_s], color=RED, lw=2.0, ls="-")

# Scatterer point
ax.plot(x_s, z_s, "*", color=RED, ms=18, zorder=6, label=f"Fault-tip scatterer ($z={z_s:.0f}$ m)")

# Depth annotations
ax.annotate("", xy=(1300, z_r), xytext=(1300, 0),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.2))
ax.text(1380, z_r/2, f"$z_r={z_r:.0f}$ m", ha="left", va="center",
        fontsize=11, color=BLUE)
ax.annotate("", xy=(1300, z_s), xytext=(1300, z_r),
            arrowprops=dict(arrowstyle="<->", color=RED, lw=1.2))
ax.text(1380, (z_r+z_s)/2, f"$\\Delta z={z_s-z_r:.0f}$ m",
        ha="left", va="center", fontsize=11, color=RED)

ax.legend(loc="lower left", fontsize=10)
ax.set_xticks([-1000, 0, 1000])

# ── Panel B: t(x) — diffraction vs primary ────────────────────────────────────
ax = ax_tx
t_ms_d = t_diff * 1000
t_ms_p = t_prim * 1000

ax.plot(x_arr / 1000, t_ms_p, color=BLUE,   lw=2.2, ls="--",
        label=f"Flat-reflector primary ($z_r={z_r:.0f}$ m)")
ax.plot(x_arr / 1000, t_ms_d, color=RED,    lw=2.5,
        label=f"Point diffraction ($z_s={z_s:.0f}$ m)")

# Vertex of diffraction (apex)
t_apex = 2*z_s/V1 * 1000
ax.plot(x_s/1000, t_apex, "*", color=RED, ms=14, zorder=6)
ax.text(x_s/1000 + 0.1, t_apex + 30,
        rf"Apex: $t_{{apex}}={t_apex:.0f}$ ms", fontsize=11, color=RED)

# Parameter box
ax.text(0.98, 0.97,
        f"$V_1={V1:.0f}$ m/s",
        transform=ax.transAxes, ha="right", va="top", fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRAY, alpha=0.9))

ax.set_xlim(-3, 3)
ax.set_ylim(2000, 0)
ax.set_xlabel("Position $x$ (km)")
ax.set_ylabel("Two-way time (ms)")
ax.set_title("(B) Diffraction hyperbola\nvs flat-reflector primary", fontsize=13)
ax.legend(loc="lower left", fontsize=11)

# ── Panel C: synthetic zero-offset section ────────────────────────────────────
ax = ax_sect
t_ms = t_full * 1000
scale = 18.0
dx = offsets_sect[1] - offsets_sect[0]

for ix, xr in enumerate(offsets_sect):
    tr = gather_s[:, ix]
    ax.fill_betweenx(t_ms, xr/1000, xr/1000 + tr * scale / 1000,
                      where=tr > 0, facecolor=BLACK, alpha=0.65)
    ax.plot(xr/1000 + tr * scale / 1000, t_ms,
            color=BLACK, lw=0.25, alpha=0.4)

# Annotate the flat primary and diffraction hyperbola
ax.axhline(2*z_r/V1 * 1000, color=BLUE, lw=1.5, ls="--", alpha=0.6,
           label=f"Primary ({z_r:.0f} m)")
# Diffraction hyperbola overlay
t_diff_sect = (2/V1) * np.sqrt((offsets_sect - x_s)**2 + z_s**2) * 1000
ax.plot(offsets_sect/1000, t_diff_sect, color=RED, lw=2.0, ls="--",
        alpha=0.8, label=f"Diffraction apex ({z_s:.0f} m)")
ax.plot(x_s/1000, 2*z_s/V1*1000, "*", color=RED, ms=12, zorder=6)

ax.set_xlim(offsets_sect[0]/1000, offsets_sect[-1]/1000)
ax.set_ylim(2000, 0)
ax.set_xlabel("CMP position (km)")
ax.set_ylabel("Two-way time (ms)")
ax.set_title("(C) Unmigrated zero-offset section:\nflat primary + fault-tip diffraction", fontsize=13)
ax.legend(loc="lower right", fontsize=11)
ax.text(0.02, 0.04, "Migration required to\ncollapse diffraction to point",
        transform=ax.transAxes, fontsize=10, color=RED,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=RED, alpha=0.8))

fig.tight_layout()
fig.savefig("assets/figures/fig_diffraction_hyperbola.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_diffraction_hyperbola.png")

if __name__ == "__main__":
    plt.show()
