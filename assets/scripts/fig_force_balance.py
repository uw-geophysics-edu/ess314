"""
fig_force_balance.py
====================
Two-panel figure illustrating the force balance on an infinitesimal elastic
element used to derive the 1D equation of motion (Newton's 2nd law applied
to a continuum):
  (a) Geometry: element between x and x+dx with face area A_x, displaced by u
  (b) Forces: F_x on left face, F_x + dF_x on right face, net force drives
      acceleration

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Fig. 3.11. Cambridge University Press. DOI: 10.1017/9781108685917
  Also consistent with: MIT OCW 12.510 Lecture 2 (CC BY NC SA)

Output : assets/figures/fig_force_balance.png
License: CC-BY 4.0 (this script)
"""
# Colorblind-safe WCAG AA palette:
# #0072B2 (blue), #E69F00 (orange), #56B4E9 (sky), #009E73 (green),
# #D55E00 (vermilion), #CC79A7 (pink), #000000 (black)

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

mpl.rcParams.update({
    'font.size': 14,
    'axes.titlesize': 14,
    'axes.labelsize': 14,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
})

C_ELEMENT = '#56B4E9'   # sky    – element face
C_FORCE   = '#D55E00'   # vermilion – forces
C_DISP    = '#009E73'   # green  – displacements
C_AXIS    = '#1a1a1a'   # near-black – axes/labels
C_STRESS  = '#0072B2'   # blue   – stress annotation
C_BANNER  = '#0072B2'   # blue   – F=σA banner background

fig, axes = plt.subplots(1, 2, figsize=(14, 7))
fig.subplots_adjust(wspace=0.38, left=0.03, right=0.97, top=0.88, bottom=0.14)

# ═══════════════════════════════════════════════════════════
# Panel (a) — Geometry of the continuum element
# ═══════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(-1.0, 9.2)
ax.set_ylim(-3.2, 6.0)
ax.axis('off')
ax.set_title('(a) Geometry: infinitesimal element $[x,\\ x+dx]$',
             fontsize=14, pad=6)

# x-axis
ax.annotate('', xy=(8.8, 0), xytext=(-0.8, 0),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.5))
ax.text(8.9, 0, '$x$', fontsize=14, va='center', color=C_AXIS)

# Element: left face at x=1.5, right face at x=6.2
left_x, right_x = 1.5, 6.2
face_h = 3.2
face_y0 = 0.4

# Left face (square, representing cross-section A_x)
face_left = mpatches.FancyBboxPatch(
    (left_x, face_y0), 0.14, face_h,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.65, lw=1.5, zorder=3)
ax.add_patch(face_left)
ax.text(left_x - 0.40, face_y0 + face_h/2, '$A_x$',
        fontsize=13, va='center', ha='center', color=C_ELEMENT)

# Right face
face_right = mpatches.FancyBboxPatch(
    (right_x, face_y0), 0.14, face_h,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.65, lw=1.5, zorder=3)
ax.add_patch(face_right)

# Top and bottom connector lines (element boundary)
ax.plot([left_x, right_x], [face_y0, face_y0], 'k--', lw=1.0, alpha=0.5)
ax.plot([left_x, right_x], [face_y0+face_h, face_y0+face_h], 'k--', lw=1.0, alpha=0.5)

# x position markers below axis
for xp, lbl in [(left_x, '$x$'), (right_x, '$x+dx$')]:
    ax.plot([xp+0.07, xp+0.07], [-0.10, 0.10], 'k-', lw=1.2)
    ax.text(xp+0.07, -0.32, lbl, ha='center', fontsize=13, color=C_AXIS)

# dx brace
ax.annotate('', xy=(right_x+0.07, -0.75), xytext=(left_x+0.07, -0.75),
            arrowprops=dict(arrowstyle='<->', color=C_AXIS, lw=1.2))
ax.text((left_x+right_x)/2 + 0.07, -1.02, '$dx$', ha='center', fontsize=13, color=C_AXIS)

# Density label inside element
ax.text((left_x+right_x)/2 + 0.07, face_y0+face_h/2,
        r'$\rho$', ha='center', va='center', fontsize=15, color=C_AXIS, alpha=0.7)

# Mass equation
ax.text((left_x+right_x)/2 + 0.07, 4.30,
        r'$m = \rho\,dx\,A_x$',
        ha='center', fontsize=13,
        bbox=dict(fc='#FFF3CD', ec='#E69F00', alpha=0.95, boxstyle='round,pad=0.35'))

# Displacement arrows: u at left face, u+du at right face
ax.annotate('', xy=(left_x + 0.65, face_y0 + face_h*0.35),
            xytext=(left_x + 0.07, face_y0 + face_h*0.35),
            arrowprops=dict(arrowstyle='->', color=C_DISP, lw=2.2))
ax.text(left_x + 0.68, face_y0 + face_h*0.35 - 0.35,
        r'$u$  (displacement at $x$)', fontsize=12, color=C_DISP)

ax.annotate('', xy=(right_x + 0.90, face_y0 + face_h*0.35),
            xytext=(right_x + 0.07, face_y0 + face_h*0.35),
            arrowprops=dict(arrowstyle='->', color=C_DISP, lw=2.2))
ax.text(right_x + 0.93, face_y0 + face_h*0.35 - 0.35,
        r'$u + \dfrac{\partial u}{\partial x}dx$', fontsize=12, color=C_DISP)

# Strain annotation
ax.text((left_x+right_x)/2 + 0.07, 5.50,
        r'$\varepsilon_{xx} = \partial u/\partial x$  (strain = dimensionless)',
        ha='center', fontsize=12, color=C_DISP, style='italic')

# Variable legend box at the bottom of panel (a)
legend_text = (
    r'$\bf{Variable\ definitions:}$' + '\n'
    r'$x$ = particle position (m) — fixed coordinate in space' + '\n'
    r'$u$ = particle displacement (m) — how far material moved' + '\n'
    r'$a = \partial^2u/\partial t^2$ = particle acceleration (m/s²)' + '\n'
    r'$\varepsilon_{xx} = \partial u/\partial x$ = strain (dimensionless)'
)
ax.text((left_x+right_x)/2 + 0.07, -1.70,
        legend_text,
        ha='center', va='top', fontsize=11, color='#222',
        bbox=dict(fc='#F0F0F0', ec='#888', alpha=0.95, boxstyle='round,pad=0.45'),
        linespacing=1.5)

# ═══════════════════════════════════════════════════════════
# Panel (b) — Force balance → equation of motion
# ═══════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(-2.0, 11.5)
ax.set_ylim(-0.8, 9.2)
ax.axis('off')
ax.set_title('(b) Force balance → equation of motion',
             fontsize=14, pad=6)

# Blue banner: Force = Stress × Area
banner = mpatches.FancyBboxPatch((-1.8, 8.1), 13.1, 0.90,
    boxstyle='round,pad=0.1', fc=C_BANNER, ec='none', alpha=0.92, zorder=4)
ax.add_patch(banner)
ax.text(4.7, 8.55,
        r'Key step:  Force = Stress $\times$ Area  $\;\Rightarrow\;$  $F_x = \sigma_{xx}\,A_x$',
        ha='center', va='center', fontsize=13, fontweight='bold', color='white', zorder=5)

# x-axis
ax.annotate('', xy=(10.8, 0.8), xytext=(-1.5, 0.8),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.5))
ax.text(10.9, 0.8, '$x$', fontsize=14, va='center', color=C_AXIS)

# Element faces
lx2, rx2 = 2.0, 6.5
fh2 = 2.4; fy0 = 1.1
face_l2 = mpatches.FancyBboxPatch((lx2, fy0), 0.14, fh2,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.55, lw=1.5)
face_r2 = mpatches.FancyBboxPatch((rx2, fy0), 0.14, fh2,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.55, lw=1.5)
for f in [face_l2, face_r2]:
    ax.add_patch(f)
ax.plot([lx2, rx2], [fy0, fy0], 'k--', lw=1.0, alpha=0.45)
ax.plot([lx2, rx2], [fy0+fh2, fy0+fh2], 'k--', lw=1.0, alpha=0.45)

# Force F_x on left face (points right = into element)
ax.annotate('', xy=(lx2+0.07, fy0+fh2/2),
            xytext=(lx2 - 1.3, fy0+fh2/2),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=3.0))
ax.text(lx2 - 1.35, fy0+fh2/2 + 0.28,
        r'$F_x = A_x\,\sigma_{xx}$', ha='right', fontsize=12, color=C_FORCE)

# Force F_x + dF_x on right face (points right = out of element)
ax.annotate('', xy=(rx2 + 1.5, fy0+fh2/2),
            xytext=(rx2+0.14, fy0+fh2/2),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=3.0))
ax.text(rx2 + 1.55, fy0+fh2/2 + 0.28,
        r'$F_x+dF_x$', ha='left', fontsize=12, color=C_FORCE)

# Step (1) — Net force
ax.text(4.57, fy0 - 0.55,
        r'(1) Net force: $dF_x = A_x\,\dfrac{\partial\sigma_{xx}}{\partial x}\,dx$',
        ha='center', fontsize=12, fontweight='bold',
        bbox=dict(fc='#EAF4FB', ec=C_STRESS, alpha=0.95, boxstyle='round,pad=0.35'))

# Step (2) — Newton's 2nd law with explicit a = ∂²u/∂t²
ax.text(4.57, 4.30,
        '(2) $F=ma$,  with $a = \\partial^2u/\\partial t^2$ (acceleration):\n'
        r'$\rho\,A_x\,dx\,\dfrac{\partial^2 u}{\partial t^2}'
        r'= A_x\,dx\,\dfrac{\partial\sigma_{xx}}{\partial x}$',
        ha='center', fontsize=12, fontweight='bold',
        bbox=dict(fc='#FFF3CD', ec='#E69F00', alpha=0.95, boxstyle='round,pad=0.35'),
        linespacing=1.6)

# Step (3) — Cancel A_x dx → equation of motion
ax.text(4.57, 6.40,
        r'(3) Cancel $A_x\,dx$:   '
        r'$\rho\,\dfrac{\partial^2 u}{\partial t^2} = \dfrac{\partial\sigma_{xx}}{\partial x}$',
        ha='center', fontsize=14, fontweight='bold',
        bbox=dict(fc='#D4EDDA', ec='#28A745', alpha=0.97, boxstyle='round,pad=0.40'))

# Annotation arrows for physical interpretation
ax.annotate('', xy=(0.0, 6.40), xytext=(1.4, 6.40),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.2))
ax.text(-0.08, 6.40, 'inertia\n(mass\u00d7accel.)', ha='right', fontsize=10.5,
        va='center', color=C_AXIS)
ax.annotate('', xy=(9.5, 6.40), xytext=(8.0, 6.40),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.2))
ax.text(9.58, 6.40, 'elastic restoring\nforce', ha='left', fontsize=10.5,
        va='center', color=C_AXIS)

# ── Title ─────────────────────────────────────────────────────────
fig.suptitle('Deriving the Equation of Motion: Force Balance on a Continuum Element',
             fontsize=15, fontweight='bold', y=1.01)
fig.text(0.5, -0.03,
    'Colors: sky blue = element faces, vermilion = forces, green = displacements. '
    'Symbols and arrows both encode information (WCAG AA dual-coding).',
    ha='center', fontsize=10, style='italic', color='#555')

plt.savefig('assets/figures/fig_force_balance.png', dpi=150, bbox_inches='tight')
print('Saved: assets/figures/fig_force_balance.png')

if __name__ == '__main__':
    pass
