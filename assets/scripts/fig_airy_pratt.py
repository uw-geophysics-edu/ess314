"""
fig_airy_pratt.py

Scientific content: Side-by-side schematic cross-sections of the two classical
isostatic-compensation models. Airy isostasy: uniform crustal density with
variable thickness; topography is supported by a deep "root". Pratt isostasy:
uniform compensation depth with laterally varying density; high topography
sits on lower-density columns. Both diagrams obey the equal-pressure
condition at the depth of compensation.

Reproduces conceptually:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Cambridge University Press, §3.5 (UW Libraries e-book; not reproduced).

  Airy, G.B. (1855). On the computation of the effect of the attraction of
  mountain-masses, as disturbing the apparent astronomical latitude of
  stations of geodetic surveys. Phil. Trans. R. Soc. 145, 101–104.
  Public domain.

  Pratt, J.H. (1855). On the attraction of the Himalaya Mountains, and of
  the elevated regions beyond them, upon the plumb-line in India. Phil.
  Trans. R. Soc. 145, 53–100. Public domain.

Output:  assets/figures/fig_airy_pratt.png
License: CC-BY 4.0
"""
import os
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

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

# Reference values (kg/m³, km)
rho_c = 2700.0    # standard crustal density
rho_m = 3300.0    # mantle density
H_ref = 35.0      # reference crustal thickness (km)
heights = [0.0, 1.0, 3.0, 5.0]    # topographic elevations h (km)

# ── Airy: same density, variable thickness ─────────────────────────────────
# Equal-pressure condition gives root  r = ρ_c h / (ρ_m - ρ_c)
# The base of the crust sits at H_ref + r below the reference surface
def airy_root(h):
    return rho_c * h / (rho_m - rho_c)

# ── Pratt: same compensation depth, variable density ──────────────────────
# Equal-pressure condition: ρ_c × H_ref = ρ_block × (H_ref + h)
# So ρ_block(h) = ρ_c × H_ref / (H_ref + h)
def pratt_density(h):
    return rho_c * H_ref / (H_ref + h)

# Spacing between blocks
dx = 1.6
xs = np.arange(len(heights)) * dx

# ── Figure ─────────────────────────────────────────────────────────────────
fig, (axA, axP) = plt.subplots(1, 2, figsize=(13.5, 6.5),
                                gridspec_kw={"wspace": 0.20})

# Airy panel ──────────────────────────────────────────────────────────────
axA.set_title("(a)  Airy — variable thickness,\n      uniform density",
               loc="left", pad=10, fontsize=14)
axA.set_xlim(-0.6, len(heights) * dx)
axA.set_ylim(-58, 7)
axA.axhline(0, color=C_BLACK, lw=1.2)        # surface (sea level reference)
axA.axhline(-H_ref, color=C_BLACK, lw=0.5, ls=":", alpha=0.7)

for x_block, h in zip(xs, heights):
    r = airy_root(h)
    # Topographic block
    axA.add_patch(Rectangle((x_block - 0.6, 0), 1.2, h,
                             facecolor=C_ORANGE, edgecolor=C_BLACK, lw=1.2))
    # Crust above reference base
    axA.add_patch(Rectangle((x_block - 0.6, -H_ref), 1.2, H_ref,
                             facecolor=C_SKY, edgecolor=C_BLACK, lw=1.2))
    # Root
    axA.add_patch(Rectangle((x_block - 0.6, -H_ref - r), 1.2, r,
                             facecolor=C_BLUE, edgecolor=C_BLACK, lw=1.2,
                             alpha=0.65))
    axA.text(x_block, h + 0.6, f"$h={h:.0f}$ km", ha="center", fontsize=11)
    if r > 0:
        axA.text(x_block, -H_ref - r - 1.5, f"$r={r:.1f}$ km",
                  ha="center", color=C_BLUE, fontsize=10)

# Compensation depth annotation — move further down to avoid r-label
axA.axhline(-H_ref - airy_root(max(heights)) - 0.5, color=C_BLACK, lw=0.4,
             ls="--", alpha=0.5)
axA.text(0.02, -H_ref - airy_root(max(heights)) - 1.7,
          "depth of compensation", ha="left", fontsize=10,
          color=C_BLACK)

# Density label
axA.text(0.98, 0.45, r"$\rho_c = 2700$ kg m$^{-3}$",
          transform=axA.transAxes, ha="right", fontsize=12,
          color=C_BLACK,
          bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_BLACK, lw=0.5))
axA.text(0.98, 0.05, r"$\rho_m = 3300$ kg m$^{-3}$",
          transform=axA.transAxes, ha="right", fontsize=12,
          color=C_BLACK,
          bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=C_BLACK, lw=0.5))

axA.set_ylabel("Depth / elevation  (km)")
axA.set_xticks([])
axA.grid(axis="y", ls=":", lw=0.6, alpha=0.5)

# Pratt panel ──────────────────────────────────────────────────────────────
axP.set_title("(b)  Pratt — uniform compensation depth,\n      varying density",
               loc="left", pad=10, fontsize=14)
axP.set_xlim(-0.6, len(heights) * dx)
axP.set_ylim(-58, 7)
axP.axhline(0, color=C_BLACK, lw=1.2)
axP.axhline(-H_ref, color=C_BLACK, lw=1.2, ls="--",
             alpha=0.85)

# Coloring by density: lighter (orange) for lower density, darker (blue) for higher
def colour_for_rho(rho):
    """Map density 2400–2900 to a colour between orange (low) and blue (high)."""
    norm = (rho - 2400.0) / (2900.0 - 2400.0)
    norm = np.clip(norm, 0, 1)
    # interpolate between orange #E69F00 and blue #0072B2
    r1, g1, b1 = 0xE6/255, 0x9F/255, 0x00/255
    r2, g2, b2 = 0x00/255, 0x72/255, 0xB2/255
    return (r1 + (r2-r1)*norm, g1 + (g2-g1)*norm, b1 + (b2-b1)*norm)

for x_block, h in zip(xs, heights):
    rho = pratt_density(h)
    col = colour_for_rho(rho)
    # Topographic block (uses same density)
    axP.add_patch(Rectangle((x_block - 0.6, 0), 1.2, h,
                             facecolor=col, edgecolor=C_BLACK, lw=1.2))
    # Column from surface to compensation depth
    axP.add_patch(Rectangle((x_block - 0.6, -H_ref), 1.2, H_ref,
                             facecolor=col, edgecolor=C_BLACK, lw=1.2,
                             alpha=0.85))
    axP.text(x_block, h + 0.6, f"$h={h:.0f}$ km", ha="center", fontsize=11)
    axP.text(x_block, -H_ref/2,
              r"$\rho=$" + f"\n{rho:.0f}",
              ha="center", va="center", fontsize=10,
              color=C_BLACK)

axP.text(0.5, -42, "Compensation depth (uniform pressure)",
          ha="center", fontsize=11)

axP.set_ylabel("Depth / elevation  (km)")
axP.set_xticks([])
axP.grid(axis="y", ls=":", lw=0.6, alpha=0.5)

fig.suptitle("Two end-member models for compensating high topography",
              fontsize=15, y=1.02)
fig.subplots_adjust(top=0.86, bottom=0.06, left=0.07, right=0.97, wspace=0.20)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_airy_pratt.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
