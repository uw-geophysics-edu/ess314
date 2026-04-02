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
    'font.size': 13,
    'axes.titlesize': 13,
    'axes.labelsize': 13,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
})

C_ELEMENT = '#56B4E9'   # sky    – element face
C_FORCE   = '#D55E00'   # vermilion – forces
C_DISP    = '#009E73'   # green  – displacements
C_AXIS    = '#1a1a1a'   # near-black – axes/labels
C_STRESS  = '#0072B2'   # blue   – stress annotation

fig, axes = plt.subplots(1, 2, figsize=(12, 5.5))
fig.subplots_adjust(wspace=0.38, left=0.04, right=0.97)

# ═══════════════════════════════════════════════════════════
# Panel (a) — Geometry of the continuum element
# ═══════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(-0.5, 7.5)
ax.set_ylim(-1.0, 4.5)
ax.axis('off')
ax.set_title('(a) Geometry: infinitesimal element $[x,\\ x+dx]$',
             fontsize=12, pad=6)

# x-axis
ax.annotate('', xy=(7.2, 0), xytext=(-0.3, 0),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.5))
ax.text(7.3, 0, '$x$', fontsize=13, va='center', color=C_AXIS)

# Element: left face at x=1.5, right face at x=5.0
left_x, right_x = 1.5, 5.0
face_h = 2.8
face_y0 = 0.4

# Left face (square, representing cross-section A_x)
face_left = mpatches.FancyBboxPatch(
    (left_x, face_y0), 0.12, face_h,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.65, lw=1.5, zorder=3)
ax.add_patch(face_left)
ax.text(left_x - 0.35, face_y0 + face_h/2, '$A_x$',
        fontsize=12, va='center', ha='center', color=C_ELEMENT)

# Right face
face_right = mpatches.FancyBboxPatch(
    (right_x, face_y0), 0.12, face_h,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.65, lw=1.5, zorder=3)
ax.add_patch(face_right)

# Top and bottom connector lines (element boundary)
ax.plot([left_x, right_x], [face_y0, face_y0], 'k--', lw=1.0, alpha=0.5)
ax.plot([left_x, right_x], [face_y0+face_h, face_y0+face_h], 'k--', lw=1.0, alpha=0.5)

# x position markers below axis
for xp, lbl in [(left_x, '$x$'), (right_x, '$x+dx$')]:
    ax.plot([xp+0.06, xp+0.06], [-0.08, 0.08], 'k-', lw=1.2)
    ax.text(xp+0.06, -0.28, lbl, ha='center', fontsize=12, color=C_AXIS)

# dx brace
ax.annotate('', xy=(right_x+0.06, -0.65), xytext=(left_x+0.06, -0.65),
            arrowprops=dict(arrowstyle='<->', color=C_AXIS, lw=1.2))
ax.text((left_x+right_x)/2 + 0.06, -0.88, '$dx$', ha='center', fontsize=12, color=C_AXIS)

# Density label inside element
ax.text((left_x+right_x)/2 + 0.06, face_y0+face_h/2,
        r'$\rho$', ha='center', va='center', fontsize=14, color=C_AXIS, alpha=0.7)

# Mass equation
ax.text(3.3, 3.80,
        r'$m = \rho\,dx\,A_x$',
        ha='center', fontsize=12,
        bbox=dict(fc='#FFF3CD', ec='#E69F00', alpha=0.95, boxstyle='round,pad=0.35'))

# Displacement arrows: u at left face, u+du at right face
ax.annotate('', xy=(left_x + 0.55, face_y0 + face_h*0.35),
            xytext=(left_x + 0.06, face_y0 + face_h*0.35),
            arrowprops=dict(arrowstyle='->', color=C_DISP, lw=1.8))
ax.text(left_x + 0.58, face_y0 + face_h*0.35 - 0.28,
        '$u$', fontsize=12, color=C_DISP)

ax.annotate('', xy=(right_x + 0.75, face_y0 + face_h*0.35),
            xytext=(right_x + 0.06, face_y0 + face_h*0.35),
            arrowprops=dict(arrowstyle='->', color=C_DISP, lw=1.8))
ax.text(right_x + 0.78, face_y0 + face_h*0.35 - 0.28,
        '$u + du$', fontsize=11, color=C_DISP)

# Strain annotation
ax.text(3.3, 4.30,
        r'$\varepsilon_{xx} = \partial u/\partial x$',
        ha='center', fontsize=11, color=C_DISP, style='italic')

# ═══════════════════════════════════════════════════════════
# Panel (b) — Force balance → equation of motion
# ═══════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(-0.5, 8.0)
ax.set_ylim(-0.5, 5.2)
ax.axis('off')
ax.set_title('(b) Force balance → equation of motion',
             fontsize=12, pad=6)

# x-axis
ax.annotate('', xy=(7.5, 0.8), xytext=(-0.2, 0.8),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.5))
ax.text(7.6, 0.8, '$x$', fontsize=13, va='center', color=C_AXIS)

# Element faces
lx2, rx2 = 1.5, 5.0
fh2 = 2.2; fy0 = 1.1
face_l2 = mpatches.FancyBboxPatch((lx2, fy0), 0.12, fh2,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.55, lw=1.5)
face_r2 = mpatches.FancyBboxPatch((rx2, fy0), 0.12, fh2,
    boxstyle='square,pad=0', fc=C_ELEMENT, ec='black', alpha=0.55, lw=1.5)
for f in [face_l2, face_r2]:
    ax.add_patch(f)
ax.plot([lx2, rx2], [fy0, fy0], 'k--', lw=1.0, alpha=0.45)
ax.plot([lx2, rx2], [fy0+fh2, fy0+fh2], 'k--', lw=1.0, alpha=0.45)

# Force F_x on left face (points right = into element)
ax.annotate('', xy=(lx2+0.06, fy0+fh2/2),
            xytext=(lx2 - 1.1, fy0+fh2/2),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.5))
ax.text(lx2 - 1.15, fy0+fh2/2 + 0.22,
        r'$F_x = A_x\,\sigma_{xx}$', ha='right', fontsize=11, color=C_FORCE)

# Force F_x + dF_x on right face (points right = out of element)
ax.annotate('', xy=(rx2 + 1.3, fy0+fh2/2),
            xytext=(rx2+0.12, fy0+fh2/2),
            arrowprops=dict(arrowstyle='->', color=C_FORCE, lw=2.5))
ax.text(rx2 + 1.35, fy0+fh2/2 + 0.22,
        r'$F_x+dF_x$', ha='left', fontsize=11, color=C_FORCE)

# Net force annotation
ax.text(3.3, fy0-0.50,
        r'$dF_x = \dfrac{\partial F}{\partial x}dx = A_x\dfrac{\partial\sigma_{xx}}{\partial x}dx$',
        ha='center', fontsize=11,
        bbox=dict(fc='#EAF4FB', ec=C_STRESS, alpha=0.95, boxstyle='round,pad=0.35'))

# Newton's 2nd law
ax.text(3.3, 3.85,
        r'$\Sigma F = ma \;\Rightarrow\;'
        r' \rho\,A_x\,dx\,\dfrac{\partial^2 u}{\partial t^2}'
        r' = A_x\,dx\,\dfrac{\partial\sigma_{xx}}{\partial x}$',
        ha='center', fontsize=10.5,
        bbox=dict(fc='#FFF3CD', ec='#E69F00', alpha=0.95, boxstyle='round,pad=0.35'))

# Simplify → equation of motion
ax.text(3.3, 4.95,
        r'$\rho\,\dfrac{\partial^2 u}{\partial t^2} = \dfrac{\partial\sigma_{xx}}{\partial x}$',
        ha='center', fontsize=13, fontweight='bold',
        bbox=dict(fc='#D4EDDA', ec='#28A745', alpha=0.97, boxstyle='round,pad=0.40'))

# Annotation arrows for physical interpretation
ax.annotate('', xy=(1.2, 4.95), xytext=(2.0, 4.95),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.0))
ax.text(1.12, 4.95, 'inertia\n(mass × accel.)', ha='right', fontsize=9.5,
        va='center', color=C_AXIS)
ax.annotate('', xy=(5.2, 4.95), xytext=(4.3, 4.95),
            arrowprops=dict(arrowstyle='->', color=C_AXIS, lw=1.0))
ax.text(5.28, 4.95, 'elastic\nrestoring force', ha='left', fontsize=9.5,
        va='center', color=C_AXIS)

# ── Title ─────────────────────────────────────────────────────────
fig.suptitle('Deriving the Equation of Motion: Force Balance on a Continuum Element',
             fontsize=14, fontweight='bold', y=1.01)
fig.text(0.5, -0.03,
    'Colors: sky blue = element faces, vermilion = forces, green = displacements. '
    'Symbols and arrows both encode information (WCAG AA dual-coding).',
    ha='center', fontsize=9.5, style='italic', color='#555')

plt.savefig('assets/figures/fig_force_balance.png', dpi=150, bbox_inches='tight')
print('Saved: assets/figures/fig_force_balance.png')

if __name__ == '__main__':
    pass
