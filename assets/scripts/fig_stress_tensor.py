"""
fig_stress_tensor.py
====================
Two-panel figure illustrating the stress tensor concept:
  (a) Normal and shear stress components on a surface element in 3D
  (b) The full stress tensor: 9 components σij on a unit cube face

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Fig. 3.3. Cambridge University Press. DOI: 10.1017/9781108685917
  Stein, S. & Wysession, M. (2003). An Introduction to Seismology,
  Earthquakes, and Earth Structure. Blackwell.

Output : assets/figures/fig_stress_tensor.png
License: CC-BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ── Palette ───────────────────────────────────────────────────────────────────
C_NORMAL = '#0072B2'   # blue    – normal stress
C_SHEAR  = '#D55E00'   # vermilion – shear stress
C_CUBE   = '#56B4E9'   # sky blue – cube face
C_AXIS   = '#333333'   # near-black – axes

fig = plt.figure(figsize=(12, 5.5))

# ═══════════════════════════════════════════════════════════════════════════
# Panel (a) — Force components on a surface element
# ═══════════════════════════════════════════════════════════════════════════
ax1 = fig.add_subplot(121, projection='3d')

# Flat surface element (square in x-z plane, normal in y direction)
sq = 0.6
verts = [[(0,0,0),(sq,0,0),(sq,0,sq),(0,0,sq)]]
face = Poly3DCollection(verts, alpha=0.25, facecolor=C_CUBE, edgecolor='black', lw=1.2)
ax1.add_collection3d(face)

origin = [sq/2, 0, sq/2]

# Normal force (in y-direction = perpendicular to surface)
ax1.quiver(*origin, 0, 0.8, 0, color=C_NORMAL, arrow_length_ratio=0.18, lw=2.5)
ax1.text(origin[0]+0.05, origin[1]+0.9, origin[2], r'$F_y$ (normal)', fontsize=9,
         color=C_NORMAL, fontweight='bold')

# Shear force in x direction
ax1.quiver(*origin, 0.7, 0, 0, color=C_SHEAR, arrow_length_ratio=0.18, lw=2.5)
ax1.text(origin[0]+0.75, origin[1]+0.05, origin[2], r'$F_x$ (shear)', fontsize=9,
         color=C_SHEAR)

# Shear force in z direction
ax1.quiver(*origin, 0, 0, 0.7, color=C_SHEAR, arrow_length_ratio=0.18, lw=2.5,
           linestyle='dashed')
ax1.text(origin[0]+0.05, origin[1]+0.05, origin[2]+0.75, r'$F_z$ (shear)',
         fontsize=9, color=C_SHEAR)

# Area label
ax1.text(sq*0.1, 0.05, sq*0.5, r'$A_y$', fontsize=11, color=C_CUBE)

# Stress components derived
ax1.text(-0.1, -0.3, -0.2,
    r'$\sigma_{yy} = F_y/A_y$  (normal)' + '\n' +
    r'$\sigma_{xy} = F_x/A_y$  (shear)' + '\n' +
    r'$\sigma_{zy} = F_z/A_y$  (shear)',
    fontsize=8.5, color=C_AXIS,
    bbox=dict(fc='white', ec='#ccc', alpha=0.9, boxstyle='round,pad=0.3'))

ax1.set_xlim(-0.2, 1.4)
ax1.set_ylim(-0.3, 1.0)
ax1.set_zlim(-0.1, 1.0)
ax1.set_xlabel('x', fontsize=10)
ax1.set_ylabel('y', fontsize=10)
ax1.set_zlabel('z', fontsize=10)
ax1.set_title('(a) Force components\non a surface element', fontsize=10)
ax1.view_init(elev=18, azim=-65)

# ═══════════════════════════════════════════════════════════════════════════
# Panel (b) — Stress tensor on a unit cube
# ═══════════════════════════════════════════════════════════════════════════
ax2 = fig.add_subplot(122, projection='3d')

# Draw the three visible faces of a unit cube
def cube_face(ax, verts, color, alpha=0.12):
    poly = Poly3DCollection([verts], alpha=alpha, facecolor=color,
                            edgecolor='black', lw=0.8)
    ax.add_collection3d(poly)

cube_face(ax2, [(0,0,0),(1,0,0),(1,1,0),(0,1,0)], C_CUBE)   # bottom z=0
cube_face(ax2, [(1,0,0),(1,1,0),(1,1,1),(1,0,1)], C_CUBE)   # right x=1
cube_face(ax2, [(0,1,0),(1,1,0),(1,1,1),(0,1,1)], C_CUBE)   # back y=1

# Normal stresses (on face centers)
face_origins = {
    'x': (1.0, 0.5, 0.5),   # x-face normal
    'y': (0.5, 1.0, 0.5),   # y-face normal
    'z': (0.5, 0.5, 0.0),   # z-face (pointing inward for visibility)
}
normals = {'x': (0.65,0,0), 'y': (0,0.65,0), 'z': (0,0,-0.65)}

for face, orig in face_origins.items():
    dx, dy, dz = normals[face]
    ax2.quiver(*orig, dx, dy, dz, color=C_NORMAL, arrow_length_ratio=0.20, lw=2.2)
    label = r'$\sigma_{' + face*2 + r'}$'
    ax2.text(orig[0]+dx+0.06, orig[1]+dy+0.04, orig[2]+dz, label,
             fontsize=10, color=C_NORMAL, fontweight='bold')

# Shear stresses (two per visible face — showing x-face and y-face)
shear_def = [
    ((1.0,0.5,0.5), (0,0.55,0),  r'$\sigma_{xy}$'),
    ((1.0,0.5,0.5), (0,0,0.55),  r'$\sigma_{xz}$'),
    ((0.5,1.0,0.5), (0.55,0,0),  r'$\sigma_{yx}$'),
    ((0.5,1.0,0.5), (0,0,0.55),  r'$\sigma_{yz}$'),
]
for orig, vec, lbl in shear_def:
    ax2.quiver(*orig, *vec, color=C_SHEAR, arrow_length_ratio=0.20, lw=1.8,
               linestyle='dashed')
    ax2.text(orig[0]+vec[0]+0.04, orig[1]+vec[1]+0.04, orig[2]+vec[2],
             lbl, fontsize=9, color=C_SHEAR)

ax2.set_xlim(-0.1, 1.8)
ax2.set_ylim(-0.1, 1.8)
ax2.set_zlim(-0.8, 1.2)
ax2.set_xlabel('x', fontsize=10)
ax2.set_ylabel('y', fontsize=10)
ax2.set_zlabel('z', fontsize=10)
ax2.set_title('(b) Stress tensor components\n' +
              r'$\boldsymbol{\sigma}$: 9 components $\sigma_{ij}$, symmetric → 6 independent',
              fontsize=10)
ax2.view_init(elev=20, azim=-55)

# Legend
norm_p  = mpatches.Patch(color=C_NORMAL, label=r'Normal stress $\sigma_{ii}$')
shear_p = mpatches.Patch(color=C_SHEAR,  label=r'Shear stress $\sigma_{ij},\ i\neq j$')
fig.legend(handles=[norm_p, shear_p], loc='lower center', ncol=2, fontsize=9,
           framealpha=0.9, bbox_to_anchor=(0.5, -0.02))

fig.suptitle('The Stress Tensor in 3D', fontsize=13, fontweight='bold')
fig.text(0.5, -0.07,
    'Colors: blue = normal stress components, vermilion = shear stress components. '
    'Arrow type (solid vs dashed) also distinguishes normal from shear.',
    ha='center', fontsize=7.5, style='italic', color='#555')

plt.tight_layout()
plt.savefig('assets/figures/fig_stress_tensor.png', dpi=90, bbox_inches='tight')
print('Saved: assets/figures/fig_stress_tensor.png')
