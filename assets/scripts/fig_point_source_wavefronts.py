"""
fig_point_source_wavefronts.py
==============================
Propagation of seismic energy from a point source near the Earth's surface,
illustrating body-wave spherical wavefronts and surface-wave circular wavefronts,
with rays perpendicular to wavefronts.

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Fig. 3.9. Cambridge University Press. DOI: 10.1017/9781108685917

Output : assets/figures/fig_point_source_wavefronts.png
License: CC-BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D

# ── Palette ───────────────────────────────────────────────────────────────────
C_SURFACE  = '#0072B2'   # blue  – free surface / surface wave
C_BODY     = '#D55E00'   # vermilion – body wave
C_RAY      = '#009E73'   # green  – rays
C_SOURCE   = '#000000'   # black  – source point
C_FILL     = '#EAF4FB'   # light blue fill – surface plane

fig = plt.figure(figsize=(9, 7))
ax  = fig.add_subplot(111, projection='3d')

# ── Ground surface (horizontal plane z=0) ─────────────────────────────────
xx = np.linspace(-3, 3, 3)
yy = np.linspace(-3, 3, 3)
XX, YY = np.meshgrid(xx, yy)
ZZ = np.zeros_like(XX)
ax.plot_surface(XX, YY, ZZ, alpha=0.18, color=C_FILL, zorder=0)
# border
for xi in [-3, 3]:
    ax.plot([xi, xi], [-3, 3], [0, 0], color=C_SURFACE, lw=0.8, alpha=0.5)
for yi in [-3, 3]:
    ax.plot([-3, 3], [yi, yi], [0, 0], color=C_SURFACE, lw=0.8, alpha=0.5)

# ── Source point P ─────────────────────────────────────────────────────────
src = (0, 0, 0)
ax.scatter(*src, color=C_SOURCE, s=60, zorder=10)
ax.text(0.15, 0.15, 0.15, 'P (source)', fontsize=9, color=C_SOURCE, fontweight='bold')

# ── Spherical body-wave wavefronts (lower hemisphere) ──────────────────────
theta = np.linspace(0, np.pi, 40)          # polar  (0=top, π=bottom)
phi   = np.linspace(0, 2*np.pi, 60)        # azimuth
T, P  = np.meshgrid(theta, phi)

for r, alpha in [(1.0, 0.30), (1.8, 0.20), (2.5, 0.12)]:
    # Only lower hemisphere (z ≤ 0)
    X = r * np.sin(T) * np.cos(P)
    Y = r * np.sin(T) * np.sin(P)
    Z = -r * np.cos(T)            # negative = downward
    mask = Z <= 0.05
    X[~mask] = np.nan
    Y[~mask] = np.nan
    Z[~mask] = np.nan
    ax.plot_surface(X, Y, Z, alpha=alpha, color=C_BODY, linewidth=0)

ax.text(1.9, 0, -1.9, 'body wave\nwavefront', fontsize=8.5,
        color=C_BODY, ha='center')

# ── Surface-wave circular wavefronts (z=0 plane) ───────────────────────────
phi_c = np.linspace(0, 2*np.pi, 120)
for r in [1.0, 1.8, 2.5]:
    ax.plot(r*np.cos(phi_c), r*np.sin(phi_c), np.zeros_like(phi_c),
            color=C_SURFACE, lw=2.0, zorder=5)

ax.text(2.6, 0, 0.2, 'surface wave', fontsize=8.5, color=C_SURFACE)

# ── Rays (perpendicular to wavefronts) ─────────────────────────────────────
ray_dirs = [
    ( 0.7,  0.0, -0.714),
    (-0.7,  0.0, -0.714),
    ( 0.0,  0.7, -0.714),
    ( 0.0, -0.7, -0.714),
    ( 0.0,  0.0, -1.0),    # vertical
    ( 1.0,  0.0,  0.0),    # surface ray
    (-1.0,  0.0,  0.0),
    ( 0.0,  1.0,  0.0),
    ( 0.0, -1.0,  0.0),
]
for dx, dy, dz in ray_dirs:
    length = 2.6
    ax.quiver(0, 0, 0, dx*length, dy*length, dz*length,
              color=C_RAY, arrow_length_ratio=0.12, lw=1.2, alpha=0.75)

ax.text(-2.7, -2.7, -0.3, 'rays ⊥ wavefronts', fontsize=8,
        color=C_RAY, style='italic')

# ── Axes / labels ──────────────────────────────────────────────────────────
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_zlim(-3, 0.5)
ax.set_xlabel('x', fontsize=10)
ax.set_ylabel('y', fontsize=10)
ax.set_zlabel('depth', fontsize=10)
ax.set_title('Point-source seismic wavefronts:\nbody waves (sphere) and surface waves (circle)',
             fontsize=11, fontweight='bold')
ax.view_init(elev=22, azim=-55)

# Legend patches
body_patch    = mpatches.Patch(color=C_BODY,    label='Body-wave wavefront (spherical)')
surface_patch = mpatches.Patch(color=C_SURFACE, label='Surface-wave wavefront (circular)')
ray_patch     = mpatches.Patch(color=C_RAY,     label='Seismic rays (⊥ wavefront)')
ax.legend(handles=[body_patch, surface_patch, ray_patch],
          loc='upper left', fontsize=8.5, framealpha=0.9)

plt.tight_layout()
plt.savefig('assets/figures/fig_point_source_wavefronts.png', dpi=150, bbox_inches='tight')
print('Saved: assets/figures/fig_point_source_wavefronts.png')
