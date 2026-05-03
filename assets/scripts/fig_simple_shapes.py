"""
fig_simple_shapes.py

Scientific content: Side-by-side gravity anomaly profiles over four canonical
target geometries — a buried sphere, a horizontal cylinder (e.g. tunnel or
pipe), an infinite Bouguer slab (slab edge), and a vertical fault that
offsets a horizontal layer. Each shape produces a characteristic Δg(x)
signature that is the basis for visual interpretation.

Reproduces conceptually:
  Lowrie & Fichtner (2020), Ch. 3.4; Reynolds (2011), Ch. 2.6;
  Kearey, Brooks & Hill (2002), An Introduction to Geophysical Exploration,
  Ch. 6 (citation only — paywalled).

Output:  assets/figures/fig_simple_shapes.png
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

G = 6.67430e-11

# Forward formulas (closed-form, Δg in mGal) ──────────────────────────────
def dg_sphere(x, z, R, drho):
    M = (4.0/3.0) * np.pi * R**3 * drho
    return (G * M * z / (x**2 + z**2)**1.5) * 1e5

def dg_horiz_cyl(x, z, R, drho):
    """Vertical anomaly above a horizontal cylinder (axis perpendicular to
    profile)."""
    lam = np.pi * R**2 * drho                      # mass / unit length
    return (2 * G * lam * z / (x**2 + z**2)) * 1e5

def dg_fault_step(x, z_top, z_bot, drho):
    """Vertical-fault offset in a horizontal layer of density contrast Δρ.
    Closed-form: Δg = 2 G Δρ [ z arctan(x/z) ] from z_top to z_bot.
    Geometry: fault at x=0, hanging-wall block on x>0 side,
    layer between z_top and z_bot offset by Δz."""
    # Difference between two thin layers' contributions
    def slab_step(x, z, drho):
        # gravity jump produced by a slab of thickness dz that exists only
        # for x > 0; analytic answer: Δg(x) = 2 G Δρ dz [π/2 + arctan(x/z)]
        return 2 * G * drho * (np.pi / 2.0 + np.arctan2(x, z))
    # integrate over depth band [z_top, z_bot]
    z = np.linspace(z_top, z_bot, 300)
    dz = z[1] - z[0]
    out = np.zeros_like(x)
    for zi in z:
        out += slab_step(x, zi, drho) * dz
    return out * 1e5  # mGal

x = np.linspace(-2000.0, 2000.0, 801)

# Compute four signatures ────────────────────────────────────────────────
dg_sph = dg_sphere(x, z=600.0, R=150.0, drho=600.0)
dg_cyl = dg_horiz_cyl(x, z=600.0, R=150.0, drho=600.0)
# Fault: horizontal layer 200–400 m thick offset by 200 m
dg_flt = (dg_fault_step(x, 200.0, 400.0, 400.0)
          - dg_fault_step(x, 400.0, 600.0, 400.0))

# Bouguer slab: a horizontal layer of finite extent (causes a smooth step)
def dg_finite_slab(x, z_top, z_bot, drho, x0, x1):
    """Gravity over a finite-width 2D slab (x ∈ [x0, x1], depth ∈ [z_top, z_bot]).

    Uses superposition of two semi-infinite slabs.  The closed-form for a
    semi-infinite slab covering x' ≥ edge at depth z (thickness dz) is
        g_z(x; edge) = 2 G ρ dz · [π/2 + arctan((x − edge)/z)],
    which → 2πGρdz as x → ∞ and → 0 as x → −∞.  The finite slab is then
    g_z[edge=x0] − g_z[edge=x1]: nonzero only when x lies above [x0, x1].
    """
    def semi_inf_slab(x, z, drho, edge):
        return 2 * G * drho * (np.pi / 2.0 + np.arctan2(x - edge, z))
    z = np.linspace(z_top, z_bot, 300)
    dz = z[1] - z[0]
    out = np.zeros_like(x)
    for zi in z:
        out += (semi_inf_slab(x, zi, drho, x0)
                - semi_inf_slab(x, zi, drho, x1)) * dz
    return out * 1e5
dg_slab = dg_finite_slab(x, 100.0, 350.0, 800.0, -300.0, 300.0)

# ── Figure: 2×2 grid (geometry on top of profile in each panel) ──────────
fig, axes = plt.subplots(2, 2, figsize=(13, 8.5),
                          gridspec_kw={"hspace": 0.55, "wspace": 0.30})

# Panel helper
def panel(ax, title, anomaly, sketch_fn, ymax_pad=0.25):
    ax.plot(x, anomaly, color=C_BLUE, lw=2.4)
    ax.axhline(0, color=C_BLACK, lw=0.6, ls="--")
    ax.set_xlabel("Profile distance $x$  (m)")
    ax.set_ylabel(r"$\Delta g$  (mGal)")
    ax.set_title(title, loc="left", pad=10)
    ax.grid(ls=":", lw=0.6, alpha=0.5)
    # inset axes for geometry sketch
    inset = ax.inset_axes([0.62, 0.55, 0.36, 0.42])
    sketch_fn(inset)
    inset.set_xticks([])
    inset.set_yticks([])
    inset.set_xlim(-1500, 1500)
    inset.set_ylim(900, -50)
    inset.axhline(0, color=C_BLACK, lw=1.0)
    inset.set_facecolor("#F7F7F7")

# Sketches -----------------------------------------------------------------
def sk_sphere(ax):
    th = np.linspace(0, 2*np.pi, 100)
    ax.fill(150*np.cos(th), 600 + 150*np.sin(th),
            color=C_VERM, alpha=0.65, edgecolor=C_BLACK)
    ax.text(0.04, 0.05, r"sphere $z=600,\,R=150$ m",
            transform=ax.transAxes, fontsize=9, va="bottom")

def sk_cyl(ax):
    # Plot many small circles to suggest a long cylinder going into the page
    for xc in [0]:
        th = np.linspace(0, 2*np.pi, 100)
        ax.fill(150*np.cos(th) + xc, 600 + 150*np.sin(th),
                color=C_ORANGE, alpha=0.65, edgecolor=C_BLACK)
    ax.text(0.04, 0.05, "horizontal cylinder", transform=ax.transAxes,
            fontsize=9, va="bottom")

def sk_slab(ax):
    ax.fill([-300, 300, 300, -300], [100, 100, 350, 350],
            color=C_GREEN, alpha=0.6, edgecolor=C_BLACK)
    ax.text(0.04, 0.05, "finite Bouguer slab", transform=ax.transAxes,
            fontsize=9, va="bottom")

def sk_fault(ax):
    # Layer offset vertically across a fault at x = 0
    ax.fill([-1500, 0, 0, -1500], [200, 200, 400, 400],
            color=C_SKY, alpha=0.7, edgecolor=C_BLACK)
    ax.fill([0, 1500, 1500, 0], [400, 400, 600, 600],
            color=C_SKY, alpha=0.7, edgecolor=C_BLACK)
    ax.plot([0, 0], [-50, 900], color=C_VERM, lw=2.0)
    ax.text(0.04, 0.05, "vertical fault offset", transform=ax.transAxes,
            fontsize=9, va="bottom")

panel(axes[0, 0], "(a)  Buried sphere", dg_sph, sk_sphere)
panel(axes[0, 1], "(b)  Horizontal cylinder", dg_cyl, sk_cyl)
panel(axes[1, 0], "(c)  Finite slab (Bouguer)", dg_slab, sk_slab)
panel(axes[1, 1], "(d)  Vertical fault offset", dg_flt, sk_fault)

fig.suptitle("Gravity anomaly signatures of canonical subsurface bodies",
             fontsize=15, y=0.998)

OUT = os.path.join(os.path.dirname(__file__), "..", "figures",
                    "fig_simple_shapes.png")
fig.savefig(OUT, bbox_inches="tight")
print(f"Wrote {OUT}")

if __name__ == "__main__":
    pass
