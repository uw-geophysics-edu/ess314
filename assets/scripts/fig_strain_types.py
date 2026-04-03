"""
fig_strain_types.py
===================
Three-panel figure illustrating the three fundamental strain modes:
  (a) Longitudinal strain — uniaxial compression of a cylinder
  (b) Volumetric strain (dilatation) — isotropic compression of a cube
  (c) Shear strain — angular distortion of a rectangle

Reproduces scientific content from:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Figs 3.4, 3.5, 3.6. Cambridge University Press. DOI: 10.1017/9781108685917

Output : assets/figures/fig_strain_types.png
License: CC-BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Ellipse

# ── Palette ───────────────────────────────────────────────────────────────────
C_ORIG   = '#56B4E9'    # sky blue  – original body
C_DEFORM = '#0072B2'    # blue      – deformed body
C_FORCE  = '#D55E00'    # vermilion – force arrows
C_DIM    = '#333333'    # near-black – dimension labels
ALPHA_O  = 0.25
ALPHA_D  = 0.55

fig, axes = plt.subplots(1, 3, figsize=(13, 5.5))
fig.subplots_adjust(wspace=0.38)

# ═══════════════════════════════════════════════════════════════════════════
# Panel (a) — Longitudinal strain
# ═══════════════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(-0.1, 1.1)
ax.set_ylim(-0.2, 2.0)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(a) Longitudinal strain\n' r'$\varepsilon_{xx} = \Delta h / h$',
             fontsize=10, pad=8)

# Original cylinder (rectangle in 2D, cross-hatched)
h, w = 1.3, 0.55
x0, y0 = 0.225, 0.0
rect_o = mpatches.FancyBboxPatch((x0, y0), w, h, boxstyle='square,pad=0',
    edgecolor='black', facecolor=C_ORIG, alpha=ALPHA_O, lw=1.2)
ax.add_patch(rect_o)

# Deformed (shorter, same width — compression in x)
dh = -0.28
rect_d = mpatches.FancyBboxPatch((x0, y0), w, h+dh, boxstyle='square,pad=0',
    edgecolor='black', facecolor=C_DEFORM, alpha=ALPHA_D, lw=1.5)
ax.add_patch(rect_d)

# Force arrow downward
ax.annotate('', xy=(0.5, y0-0.08), xytext=(0.5, y0-0.01),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.0))
ax.text(0.5, y0-0.15, '$F$', ha='center', fontsize=11, color=C_FORCE, fontweight='bold')

# Dimension: h
ax.annotate('', xy=(x0-0.07, y0), xytext=(x0-0.07, y0+h),
            arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=1.2))
ax.text(x0-0.14, y0+h/2, '$h$', va='center', fontsize=10, color=C_DIM)

# Dimension: Δh
ax.annotate('', xy=(x0-0.07, y0+h+dh), xytext=(x0-0.07, y0+h),
            arrowprops=dict(arrowstyle='<->', color=C_DEFORM, lw=1.2))
ax.text(x0-0.17, y0+h+dh/2, r'$\Delta h$', va='center', fontsize=9, color=C_DEFORM)

# Area label
ax.text(x0+w+0.04, y0+0.1, '$A$', fontsize=10, color=C_DIM)

# Stress label
ax.text(0.5, 0.6, r'$\sigma = F/A$', ha='center', fontsize=10, color=C_DIM,
        bbox=dict(fc='white', ec='none', alpha=0.8))
ax.text(0.5, 0.35, r'$\varepsilon = \Delta h / h$', ha='center', fontsize=10, color=C_DIM,
        bbox=dict(fc='white', ec='none', alpha=0.8))

# ═══════════════════════════════════════════════════════════════════════════
# Panel (b) — Volumetric strain (dilatation)
# ═══════════════════════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(-0.1, 1.2)
ax.set_ylim(-0.15, 1.4)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(b) Volumetric strain\n' r'$\theta = \Delta V / V$', fontsize=10, pad=8)

# Original box
s = 0.8
x0, y0 = 0.2, 0.15
rect_o = mpatches.FancyBboxPatch((x0, y0), s, s, boxstyle='square,pad=0',
    edgecolor='black', facecolor=C_ORIG, alpha=ALPHA_O, lw=1.2)
ax.add_patch(rect_o)

# Deformed (smaller — compressed from all sides)
ds = 0.16
rect_d = mpatches.FancyBboxPatch((x0+ds/2, y0+ds/2), s-ds, s-ds, boxstyle='square,pad=0',
    edgecolor='black', facecolor=C_DEFORM, alpha=ALPHA_D, lw=1.5)
ax.add_patch(rect_d)

# Pressure arrows from all four sides
off = 0.06
cx, cy = x0+s/2, y0+s/2
for (xs, ys, xt, yt) in [
        (cx, y0+s+off, cx, y0+s+0.01),
        (cx, y0-off,   cx, y0-0.01),
        (x0-off, cy,   x0-0.01, cy),
        (x0+s+off, cy, x0+s+0.01, cy)]:
    ax.annotate('', xy=(xt, yt), xytext=(xs, ys),
                arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=1.8))

ax.text(x0+s+0.10, cy+0.12, '$P$\n(confining\npressure)', fontsize=8.5,
        color=C_FORCE, va='center')

ax.text(cx, y0+s+0.17, 'Original volume $V$', ha='center', fontsize=9, color=C_ORIG)
ax.text(cx, cy,  r'$V - \Delta V$', ha='center', va='center', fontsize=9,
        color='white', fontweight='bold', zorder=10)

ax.text(0.55, 0.05,
        r'$K = -P \,/\, (\Delta V/V)$', ha='center', fontsize=10, color=C_DIM)

# ═══════════════════════════════════════════════════════════════════════════
# Panel (c) — Shear strain
# ═══════════════════════════════════════════════════════════════════════════
ax = axes[2]
ax.set_xlim(-0.05, 1.35)
ax.set_ylim(-0.2, 1.3)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(c) Shear strain\n' r'$\gamma = \tan\psi \approx \psi$', fontsize=10, pad=8)

# Original rectangle (dashed outline)
w, h = 0.8, 0.8
x0, y0 = 0.1, 0.1
rect_o = mpatches.FancyBboxPatch((x0, y0), w, h, boxstyle='square,pad=0',
    edgecolor=C_ORIG, facecolor='none', lw=1.5, ls='--')
ax.add_patch(rect_o)
ax.text(x0+0.02, y0+h+0.03, 'Original solid', fontsize=8.5, color=C_ORIG)

# Sheared parallelogram
dx = 0.27   # horizontal offset of top relative to bottom
verts = np.array([[x0, y0], [x0+w, y0], [x0+w+dx, y0+h], [x0+dx, y0+h], [x0, y0]])
poly = plt.Polygon(verts, closed=True, edgecolor='black',
                   facecolor=C_DEFORM, alpha=ALPHA_D, lw=1.5)
ax.add_patch(poly)
ax.text(x0+dx+0.02, y0+h+0.03, 'Sheared solid', fontsize=8.5, color=C_DEFORM)

# Shear force arrow (horizontal, at top)
ax.annotate('', xy=(x0+w+dx+0.12, y0+h), xytext=(x0+dx, y0+h),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.0))
ax.text(x0+w+dx+0.14, y0+h, r'$\tau$ (shear stress)', fontsize=9,
        color=C_FORCE, va='center')

# Reaction at base
ax.annotate('', xy=(x0-0.12, y0), xytext=(x0+w*0.6, y0),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.0))

# Angle ψ arc
psi = np.arctan2(dx, h)
arc_r = 0.20
theta_arr = np.linspace(np.pi/2, np.pi/2 - psi, 30)
ax.plot(x0 + arc_r*np.cos(theta_arr), y0 + arc_r*np.sin(theta_arr),
        color=C_DIM, lw=1.2)
ax.text(x0+0.04, y0+arc_r+0.05, r'$\psi$', fontsize=11, color=C_DIM)
ax.text(x0-0.04, y0+arc_r*0.4,  r'$\gamma = \tan\psi$', fontsize=9.5,
        color=C_DIM, ha='right')

# Height dimension
ax.annotate('', xy=(x0+w+dx+0.14, y0), xytext=(x0+w+dx+0.14, y0+h),
            arrowprops=dict(arrowstyle='<->', color=C_DIM, lw=1.0))
ax.text(x0+w+dx+0.20, y0+h/2, '$h$', va='center', fontsize=10, color=C_DIM)

# ── Shared title ──────────────────────────────────────────────────────────
fig.suptitle('Fundamental Modes of Elastic Strain', fontsize=13, fontweight='bold', y=1.01)

fig.text(0.5, -0.04,
    'Colors: sky blue = original body, blue = deformed body, vermilion = applied forces. '
    'Shape encodes deformation mode independent of color.',
    ha='center', fontsize=7.5, style='italic', color='#555')

plt.savefig('assets/figures/fig_strain_types.png', dpi=90, bbox_inches='tight')
print('Saved: assets/figures/fig_strain_types.png')
