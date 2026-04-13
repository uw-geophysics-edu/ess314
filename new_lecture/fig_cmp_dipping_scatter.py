"""
fig_cmp_dipping_scatter.py

Scientific content:
    For a FLAT horizontal reflector, all traces in a CMP gather share the
    same subsurface reflection point (directly below the midpoint).
    For a DIPPING reflector, the reflection point migrates up-dip as
    offset increases — the reflection points are "smeared" laterally.

    This smear means that a dipping-layer CMP gather does NOT sample a
    single subsurface point. Standard NMO stacking therefore images a
    blurred, laterally averaged zone rather than a single dip point.
    The Dip Moveout (DMO) correction is designed to focus the reflection
    points back to a single location before NMO stacking.

    Panel A: flat reflector — all reflection points at the midpoint x=0.
    Panel B: dipping reflector (delta=15 deg) — reflection points smear
             up-dip as offset increases.

Reproduces scientific content of:
    Hale, D. (1984). Dip-moveout by Fourier transform. Geophysics, 49(6),
    741–751. https://doi.org/10.1190/1.1441702
    Sheriff, R.E. & Geldart, L.P. (1995). Exploration Seismology, 2nd ed.
    Cambridge University Press. Chapter 4.

Output: assets/figures/fig_cmp_dipping_scatter.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

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

# ── Model ─────────────────────────────────────────────────────────────────────
V1    = 2000.0
h     = 1000.0          # perpendicular depth at midpoint
delta = np.radians(15)  # dip angle
offsets = np.arange(0, 2201, 400)   # 0, 400, 800, 1200, 1600, 2000 m

def refl_point_flat(x_src, x_rcv, h_flat):
    """Reflection point for flat layer at depth h_flat."""
    x_mid = (x_src + x_rcv) / 2
    return x_mid, h_flat

def refl_point_dip(x_src, x_rcv, h_perp, delta):
    """Reflection point for dipping layer using image-point method.
    Source at x_src = -x/2, receiver at x_rcv = +x/2 (CMP at 0).
    Reflector: z = h_perp/cos(delta) - x*tan(delta).
    Image of source: (xi, zi) = source reflected across the dipping plane.
    """
    # Normal to reflector: n = (-sin(delta), cos(delta)) pointing up
    # Source position: (x_src, 0)
    # Projection of source onto reflector normal:
    # h_s = x_src * (-sin(delta)) + 0 * cos(delta) + h_perp  [signed distance]
    # (using equation of plane: -x sin(delta) + z cos(delta) = h_perp)
    h_s = -x_src * np.sin(delta) + 0 * np.cos(delta)
    # Distance from source to reflector along normal:
    d_s = h_perp - h_s    # perpendicular distance to reflector
    # Image of source:
    xi = x_src + 2 * d_s * (-np.sin(delta))
    zi = 0      + 2 * d_s *   np.cos(delta)
    # Reflection point: on line from image (xi,zi) to receiver (x_rcv, 0)
    # Intersect with reflector: -x sin(delta) + z cos(delta) = h_perp
    # Parameterize: P = (xi,zi) + t*((x_rcv-xi), (0-zi))
    # -[xi + t*(xr-xi)]*sin(delta) + [zi + t*(0-zi)]*cos(delta) = h_perp
    # t*[-(xr-xi)*sin(delta) - zi*cos(delta)] = h_perp - (-xi*sin(delta) + zi*cos(delta))
    num = h_perp - (-xi * np.sin(delta) + zi * np.cos(delta))
    den = -(x_rcv - xi) * np.sin(delta) - zi * np.cos(delta)
    t_param = num / den if abs(den) > 1e-9 else 0.5
    xp = xi + t_param * (x_rcv - xi)
    zp = zi + t_param * (0 - zi)
    return xp, zp

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(14, 7),
                          gridspec_kw={"wspace": 0.38})
ax_flat, ax_dip = axes

for ax, is_dip, title in [
    (ax_flat, False, "(A) Flat reflector\nAll reflection points at midpoint"),
    (ax_dip,  True,  "(B) Dipping reflector ($\\delta=15°$)\nReflection points smear up-dip"),
]:
    ax.set_xlim(-1800, 1800)
    ax.set_ylim(1600, -300)
    ax.set_xlabel("Horizontal position (m)")
    ax.set_ylabel("Depth (m)")
    ax.set_title(title, fontsize=13)

    # Surface
    ax.axhline(0, color=BLACK, lw=2)

    # CMP midpoint at surface (x=0)
    ax.plot(0, 0, "D", color=RED, ms=10, zorder=6, label="CMP midpoint (x=0)")

    if not is_dip:
        # Flat reflector
        ax.axhline(h, color=BLUE, lw=2.5)
        ax.text(1650, h + 40, f"Reflector ($z={h:.0f}$ m)",
                ha="right", fontsize=11, color=BLUE)
        # All reflection points at (0, h)
        xp_all, zp_all = 0, h
        ax.plot(xp_all, zp_all, "*", color=ORANGE, ms=18, zorder=6,
                label="Reflection point (all offsets)")
    else:
        # Dipping reflector
        h_v = h / np.cos(delta)
        x_ref_line = np.array([-1600, 2000])
        z_ref_line = h_v - x_ref_line * np.tan(delta)
        ax.plot(x_ref_line, z_ref_line, color=BLUE, lw=2.5,
                label=f"Reflector ($\\delta={int(np.degrees(delta))}°$)")

    cmap_offsets = plt.cm.plasma(np.linspace(0.1, 0.85, len(offsets)))

    for oi, x in enumerate(offsets):
        if x == 0:
            continue  # skip zero offset for clarity
        x_src = -x / 2
        x_rcv =  x / 2
        color_o = cmap_offsets[oi]

        if not is_dip:
            xp, zp = refl_point_flat(x_src, x_rcv, h)
        else:
            xp, zp = refl_point_dip(x_src, x_rcv, h, delta)

        # Source and receiver
        ax.plot(x_src, 0, "^", color=color_o, ms=8, zorder=4, alpha=0.85)
        ax.plot(x_rcv, 0, "v", color=color_o, ms=8, zorder=4, alpha=0.85)

        # Ray paths
        ax.plot([x_src, xp, x_rcv], [0, zp, 0],
                color=color_o, lw=1.0, alpha=0.65)

        # Reflection point
        ax.plot(xp, zp, "o", color=color_o, ms=9, zorder=5)
        if is_dip:
            ax.text(xp - 30, zp + 50,
                    f"$x={x:.0f}$ m", ha="right", fontsize=11,
                    color=color_o)

    # Smear arrow for dipping case
    if is_dip:
        # Compute first and last reflection points
        x_last = offsets[-1]
        xp1, zp1 = refl_point_dip(-offsets[1]/2,  offsets[1]/2,  h, delta)
        xpN, zpN = refl_point_dip(-x_last/2,        x_last/2,       h, delta)
        ax.annotate("", xy=(xpN, zpN + 80), xytext=(xp1, zp1 + 80),
                    arrowprops=dict(arrowstyle="->", color=RED, lw=2.0))
        ax.text((xp1 + xpN)/2, (zp1 + zpN)/2 - 100,
                "Reflection point\nsmear (up-dip)",
                ha="center", fontsize=11, color=RED,
                bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=RED, alpha=0.8))

    ax.legend(loc="lower left", fontsize=10)

fig.tight_layout()
fig.savefig("assets/figures/fig_cmp_dipping_scatter.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_cmp_dipping_scatter.png")

if __name__ == "__main__":
    plt.show()
