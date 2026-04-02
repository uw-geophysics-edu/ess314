"""
fig_elastic_moduli.py
=====================
Four-panel schematic illustrating the four principal elastic moduli:
Young's modulus (E), shear modulus (mu), bulk modulus (K), and Poisson's
ratio (nu), each with the deformation geometry and defining equation.

Scientific content based on:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.
  Cambridge University Press. §3.1. DOI: 10.1017/9781108685917
  Also consistent with:
  Jaeger, J.C., Cook, N.G.W. & Zimmerman, R. (2007). Fundamentals of Rock
  Mechanics, 4th ed. Blackwell. §1.3.

Output : assets/figures/fig_elastic_moduli.png
License: CC-BY 4.0 (this script)
"""
# Colorblind-safe WCAG AA palette
# #0072B2 (blue), #E69F00 (orange), #56B4E9 (sky), #009E73 (green),
# #D55E00 (vermilion), #CC79A7 (pink), #000000 (black)

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

mpl.rcParams.update({
    'font.size': 13,
    'axes.titlesize': 13,
    'axes.labelsize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
    'legend.fontsize': 11,
    'figure.titlesize': 15,
})

C_INIT  = '#56B4E9'   # sky blue  – initial shape
C_FINAL = '#0072B2'   # blue      – deformed shape
C_FORCE = '#D55E00'   # vermilion – force / stress arrows
C_LABEL = '#1a1a1a'   # near-black
C_EQ    = '#009E73'   # green     – equation box

fig, axes = plt.subplots(1, 4, figsize=(14, 5.5))
fig.subplots_adjust(wspace=0.40, left=0.04, right=0.97, top=0.88, bottom=0.12)


def box3d(ax, origin, size, color, alpha=0.22, ec='black', lw=1.2):
    """Draw a simple 2.5-D box using oblique projection."""
    ox, oy = origin
    sx, sy = size
    sk = 0.30   # skew factor for depth
    depth = sx * 0.35
    # Front face
    front = plt.Polygon([(ox, oy), (ox+sx, oy), (ox+sx, oy+sy), (ox, oy+sy)],
                        closed=True, fc=color, ec=ec, alpha=alpha, lw=lw)
    # Top face
    top = plt.Polygon([(ox, oy+sy), (ox+sx, oy+sy),
                        (ox+sx+depth*sk, oy+sy+depth*sk),
                        (ox+depth*sk, oy+sy+depth*sk)],
                      closed=True, fc=color, ec=ec, alpha=alpha*0.8, lw=lw)
    # Right face
    right = plt.Polygon([(ox+sx, oy), (ox+sx+depth*sk, oy+depth*sk),
                          (ox+sx+depth*sk, oy+sy+depth*sk), (ox+sx, oy+sy)],
                        closed=True, fc=color, ec=ec, alpha=alpha*0.6, lw=lw)
    for p in [front, top, right]:
        ax.add_patch(p)
    return depth * sk


# ═══════════════════════════════════════════════════════════════════
# Panel 1 — Young's modulus E
# ═══════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(-0.3, 2.0); ax.set_ylim(-0.5, 3.0); ax.axis('off')
ax.set_title("Young's modulus $E$", fontsize=13, color=C_LABEL, pad=6)

# Initial (taller) box
box3d(ax, (0.5, 0.0), (0.8, 2.0), C_INIT, alpha=0.25)
ax.text(1.12, 1.0, '$L$', fontsize=12, color=C_INIT, va='center')
ax.annotate('', xy=(1.08, 0.0), xytext=(1.08, 2.0),
            arrowprops=dict(arrowstyle='<->', color=C_INIT, lw=1.3))

# Final (shorter) box overlaid
box3d(ax, (0.5, 0.0), (0.8, 1.55), C_FINAL, alpha=0.45)

# Force arrow down
ax.annotate('', xy=(0.90, -0.35), xytext=(0.90, -0.02),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.2))
ax.text(0.90, -0.42, '$F$', ha='center', fontsize=12, color=C_FORCE, fontweight='bold')

# Delta L annotation
ax.annotate('', xy=(1.55, 1.55), xytext=(1.55, 2.0),
            arrowprops=dict(arrowstyle='<->', color=C_FINAL, lw=1.3))
ax.text(1.62, 1.77, r'$\Delta L$', fontsize=11, color=C_FINAL, va='center')

ax.text(0.90, 2.75,
        r'$E = \dfrac{F/A}{\Delta L/L} = \dfrac{\sigma}{\varepsilon}$',
        ha='center', fontsize=11,
        bbox=dict(fc='#EAF4FB', ec=C_EQ, alpha=0.95, boxstyle='round,pad=0.35'))

# ═══════════════════════════════════════════════════════════════════
# Panel 2 — Shear modulus mu
# ═══════════════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(-0.2, 2.3); ax.set_ylim(-0.4, 2.8); ax.axis('off')
ax.set_title(r'Shear modulus $\mu$', fontsize=13, color=C_LABEL, pad=6)

# Initial rectangle (dashed)
rect_init = plt.Polygon([(0.3, 0.0), (1.5, 0.0), (1.5, 1.8), (0.3, 1.8)],
                        closed=True, fc='none', ec=C_INIT, lw=1.5, ls='--')
ax.add_patch(rect_init)

# Sheared rectangle
dx = 0.45
rect_sh = plt.Polygon([(0.3, 0.0), (1.5, 0.0), (1.5+dx, 1.8), (0.3+dx, 1.8)],
                      closed=True, fc=C_FINAL, ec='black', alpha=0.30, lw=1.3)
ax.add_patch(rect_sh)

# Force arrow at top
ax.annotate('', xy=(1.5+dx+0.20, 1.8), xytext=(0.3+dx, 1.8),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.2))
ax.text(1.5+dx+0.25, 1.8, r'$F$', fontsize=12, color=C_FORCE, va='center', fontweight='bold')

# Reaction at base
ax.annotate('', xy=(0.05, 0.0), xytext=(0.9, 0.0),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.2))

# Angle theta
th = np.arctan2(dx, 1.8)
arc_r = 0.32
thetas = np.linspace(np.pi/2, np.pi/2 - th, 30)
ax.plot(0.3 + arc_r*np.cos(thetas), arc_r*np.sin(thetas), color=C_LABEL, lw=1.2)
ax.text(0.18, 0.22, r'$\theta$', fontsize=12, color=C_LABEL)

# Height
ax.annotate('', xy=(1.75, 0.0), xytext=(1.75, 1.8),
            arrowprops=dict(arrowstyle='<->', color=C_LABEL, lw=1.0))
ax.text(1.83, 0.9, '$W$', fontsize=11, va='center', color=C_LABEL)

ax.text(0.9, 2.52,
        r'$\mu = \dfrac{F/WL}{\tan\theta} = \dfrac{\tau}{\gamma}$',
        ha='center', fontsize=11,
        bbox=dict(fc='#EAF4FB', ec=C_EQ, alpha=0.95, boxstyle='round,pad=0.35'))

# ═══════════════════════════════════════════════════════════════════
# Panel 3 — Bulk modulus K
# ═══════════════════════════════════════════════════════════════════
ax = axes[2]
ax.set_xlim(-0.2, 2.5); ax.set_ylim(-0.4, 2.8); ax.axis('off')
ax.set_title('Bulk modulus $K$', fontsize=13, color=C_LABEL, pad=6)

# Initial cube (larger)
box3d(ax, (0.3, 0.1), (1.2, 1.4), C_INIT, alpha=0.20)
ax.text(-0.10, 0.85, '$V$', fontsize=12, color=C_INIT, va='center')

# Compressed (smaller) cube
box3d(ax, (0.45, 0.22), (0.90, 1.10), C_FINAL, alpha=0.45)
ax.text(0.90, 0.77, r'$V-\Delta V$', fontsize=10, color='white',
        ha='center', va='center', fontweight='bold', zorder=10)

# Confining pressure arrows
P_arrows = [(0.9, 1.55, 0, 0.15), (0.9, -0.12, 0, -0.12),
            (-0.08, 0.77, 0.14, 0), (1.85, 0.77, -0.14, 0)]
for xa, ya, ddx, ddy in P_arrows:
    ax.annotate('', xy=(xa+ddx, ya+ddy), xytext=(xa, ya),
                arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.0))
ax.text(1.78, 1.65, '$P$\n(confining\npressure)', fontsize=9.5,
        color=C_FORCE, va='bottom')

ax.text(0.92, 2.52,
        r'$K = -\dfrac{P}{\Delta V/V}$',
        ha='center', fontsize=11,
        bbox=dict(fc='#EAF4FB', ec=C_EQ, alpha=0.95, boxstyle='round,pad=0.35'))

# ═══════════════════════════════════════════════════════════════════
# Panel 4 — Poisson's ratio nu
# ═══════════════════════════════════════════════════════════════════
ax = axes[3]
ax.set_xlim(-0.3, 2.3); ax.set_ylim(-0.5, 2.8); ax.axis('off')
ax.set_title("Poisson's ratio $\\nu$", fontsize=13, color=C_LABEL, pad=6)

# Initial (tall, narrow)
box3d(ax, (0.55, 0.0), (0.7, 2.2), C_INIT, alpha=0.22)
ax.text(-0.08, 1.1, '$L$', fontsize=12, color=C_INIT, va='center')
ax.annotate('', xy=(-0.04, 0.0), xytext=(-0.04, 2.2),
            arrowprops=dict(arrowstyle='<->', color=C_INIT, lw=1.1))

# Compressed (shorter, wider)
box3d(ax, (0.45, 0.0), (0.90, 1.65), C_FINAL, alpha=0.40)

# Axial compression
ax.annotate('', xy=(0.90, -0.35), xytext=(0.90, 0.0),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.2))
ax.text(0.90, -0.42, '$F$', ha='center', fontsize=12, color=C_FORCE, fontweight='bold')

# Lateral expansion arrows
ax.annotate('', xy=(0.37, 0.85), xytext=(0.48, 0.85),
            arrowprops=dict(arrowstyle='->', color=C_FINAL, lw=1.5))
ax.annotate('', xy=(1.45, 0.85), xytext=(1.35, 0.85),
            arrowprops=dict(arrowstyle='->', color=C_FINAL, lw=1.5))
ax.text(0.90, 0.58, r'$W+\Delta W$', ha='center', fontsize=10, color=C_FINAL)

# W dimension
ax.annotate('', xy=(1.58, 0.0), xytext=(1.58, 1.65),
            arrowprops=dict(arrowstyle='<->', color=C_LABEL, lw=1.0))
ax.text(1.65, 0.82, r'$L-\Delta L$', fontsize=10, va='center', color=C_LABEL)

ax.text(0.90, 2.55,
        r'$\nu = -\dfrac{\Delta W/W}{\Delta L/L}$',
        ha='center', fontsize=11,
        bbox=dict(fc='#EAF4FB', ec=C_EQ, alpha=0.95, boxstyle='round,pad=0.35'))

# ── Shared footer ─────────────────────────────────────────────────
fig.suptitle('Elastic Moduli: Definitions and Deformation Geometries',
             fontsize=15, fontweight='bold', y=0.97)
fig.text(0.5, 0.01,
    'Sky blue = initial body; blue = deformed body; vermilion = applied force direction. '
    'Shape encodes deformation mode independently of color (WCAG AA).',
    ha='center', fontsize=9.5, style='italic', color='#555')

plt.savefig('assets/figures/fig_elastic_moduli.png', dpi=150, bbox_inches='tight')
print('Saved: assets/figures/fig_elastic_moduli.png')

if __name__ == '__main__':
    pass
