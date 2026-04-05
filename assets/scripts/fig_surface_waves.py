"""
fig_surface_waves.py
====================
Three-panel figure for surface waves:
  (a) Rayleigh wave: retrograde elliptical particle motion, exponential depth decay
  (b) Rayleigh wave amplitude vs depth (exponential decay to ~0.4λ)
  (c) Love wave: SH trapping in a slow surface layer over a fast half-space

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Figs. 2.9a, 2.9b. Cambridge University Press. DOI: 10.1017/9781108685917
  Also consistent with: MIT OCW 12.201 §4.18–4.21 (CC BY NC SA)

Output : assets/figures/fig_surface_waves.png
License: CC-BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Ellipse

# ── Palette ───────────────────────────────────────────────────────────────────
C_RAYLEIGH = '#0072B2'   # blue    – Rayleigh wave elements
C_LOVE     = '#D55E00'   # vermilion – Love wave elements
C_LAYER    = '#56B4E9'   # sky     – slow surface layer
C_HALFSP   = '#009E73'   # green   – fast half-space
C_SURFACE  = '#333333'   # surface line
C_DECAY    = '#E69F00'   # amber   – depth decay curve

fig, axes = plt.subplots(1, 3, figsize=(14, 5.5))
fig.subplots_adjust(wspace=0.42)

# ═══════════════════════════════════════════════════════════════════════════
# Panel (a) — Rayleigh wave retrograde elliptical motion
# ═══════════════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(-0.2, 12.2)
ax.set_ylim(-5, 0.8)
ax.axhline(0, color=C_SURFACE, lw=2.0)
ax.set_title('(a) Rayleigh wave:\nRetrograde elliptical motion', fontsize=10, fontweight='bold')
ax.set_xlabel('Horizontal distance (arbitrary units)', fontsize=9)
ax.set_ylabel('Depth (arbitrary units)', fontsize=9)
ax.invert_yaxis()

# Propagation direction
ax.annotate('', xy=(11.8, -0.55), xytext=(0.2, -0.55),
            arrowprops=dict(arrowstyle='->', color=C_RAYLEIGH, lw=2.0))
ax.text(6, -0.75, 'Propagation →', ha='center', fontsize=9, color=C_RAYLEIGH)

# Draw ellipses at several depths — amplitude decays exponentially
depths   = [0.3, 1.0, 1.8, 2.7, 3.7]
x_centers = np.linspace(1.5, 10.5, len(depths))
wavelength_ref = 5.0
kR = 2*np.pi / wavelength_ref

for i, (d, xc) in enumerate(zip(depths, x_centers)):
    amp_x = 0.7 * np.exp(-kR * d * 0.4)
    amp_z = 1.0 * np.exp(-kR * d * 0.4)
    if amp_x < 0.05:
        break
    # Retrograde: phase angle offset so the motion is counter-clockwise when viewed normally
    theta = np.linspace(0, 2*np.pi, 80)
    ex = xc + amp_x * np.sin(theta)      # horizontal: forward on the way up
    ez = -d - amp_z * np.cos(theta)      # vertical: retrograde
    ax.plot(ex, ez, color=C_RAYLEIGH, lw=1.5, alpha=0.75)
    # Direction arrow on ellipse
    idx = 15
    ax.annotate('', xy=(ex[idx+1], ez[idx+1]), xytext=(ex[idx], ez[idx]),
                arrowprops=dict(arrowstyle='->', color=C_RAYLEIGH, lw=1.0,
                                mutation_scale=10))
    # Depth tick
    ax.text(-0.15, -d, f'z={d:.1f}', va='center', ha='right', fontsize=7, color='#555')

ax.text(0.5, -4.5, 'Amplitude → 0\nat depth ~0.4λ', fontsize=8.5,
        style='italic', color=C_DECAY)

# ═══════════════════════════════════════════════════════════════════════════
# Panel (b) — Amplitude vs depth (exponential decay)
# ═══════════════════════════════════════════════════════════════════════════
ax = axes[1]
z = np.linspace(0, 5, 200)
lam = wavelength_ref
amp = np.exp(-2*np.pi*z / lam * 0.4)
ax.plot(amp, z, color=C_DECAY, lw=2.5)
ax.axhline(0.4 * lam, color=C_RAYLEIGH, lw=1.5, ls='--', alpha=0.7)
ax.text(0.1, 0.4*lam - 0.2, r'$z \approx 0.4\lambda$', fontsize=9,
        color=C_RAYLEIGH, style='italic')
ax.set_xlabel('Normalized amplitude', fontsize=9)
ax.set_ylabel('Depth (wavelengths)', fontsize=9)
ax.set_title('(b) Rayleigh wave\namplitude vs depth', fontsize=10, fontweight='bold')
ax.invert_yaxis()
ax.set_xlim(-0.05, 1.15)
ax.set_ylim(5.2, -0.2)
ax.spines[['top', 'right']].set_visible(False)

# Vr label
ax.text(0.55, 0.4, r'$V_R \approx 0.92\, V_S$', fontsize=9.5,
        bbox=dict(fc='#EAF4FB', ec=C_RAYLEIGH, alpha=0.95, boxstyle='round,pad=0.3'))

# ═══════════════════════════════════════════════════════════════════════════
# Panel (c) — Love wave: SH trapping in slow layer
# ═══════════════════════════════════════════════════════════════════════════
ax = axes[2]
ax.set_xlim(-0.2, 10.2)
ax.set_ylim(-5, 1.0)
ax.set_title('(c) Love wave: SH-wave trapped\nin slow surface layer', fontsize=10, fontweight='bold')
ax.set_xlabel('Horizontal distance (arbitrary units)', fontsize=9)
ax.set_ylabel('Depth (arbitrary units)', fontsize=9)
ax.invert_yaxis()

# Layer boundary
layer_depth = 2.5
ax.axhline(0, color=C_SURFACE, lw=2.0)
ax.axhline(-layer_depth, color=C_LOVE, lw=2.0, ls='-')

# Layer fills
ax.axhspan(-0.001, -layer_depth, alpha=0.12, color=C_LAYER, label=f'Slow layer (β₁)')
ax.axhspan(-layer_depth, -5.2, alpha=0.12, color=C_HALFSP, label='Fast half-space (β₂ > β₁)')

ax.text(8.0, -0.8, 'β₁ (slow)', fontsize=9, color=C_LAYER, fontweight='bold')
ax.text(8.0, -3.5, 'β₂ > β₁\n(fast)', fontsize=9, color=C_HALFSP, fontweight='bold')

# SH rays bouncing inside layer by total internal reflection
x_seg = [0.5, 2.5, 4.5, 6.5, 8.5]
z_seg = [0.0, -layer_depth, 0.0, -layer_depth, 0.0]
ax.plot(x_seg, z_seg, color=C_LOVE, lw=1.8, ls='--', zorder=5)
# Arrows along rays
for i in range(len(x_seg)-1):
    xm = (x_seg[i]+x_seg[i+1])/2
    zm = (z_seg[i]+z_seg[i+1])/2
    dx = x_seg[i+1]-x_seg[i]
    dz = z_seg[i+1]-z_seg[i]
    ax.annotate('', xy=(xm+dx*0.05, zm+dz*0.05),
                xytext=(xm-dx*0.05, zm-dz*0.05),
                arrowprops=dict(arrowstyle='->', color=C_LOVE, lw=1.2,
                                mutation_scale=12))

# SH particle motion markers (into page = dot, out of page = cross)
for xm, zm in zip([1.5, 3.5, 5.5, 7.5], [-0.8, -1.8, -0.8, -1.8]):
    ax.plot(xm, zm, 'o', ms=8, color=C_LOVE, zorder=6)   # into page
    ax.text(xm+0.15, zm, '⊙', fontsize=10, color=C_LOVE, va='center')

ax.text(0.3, -2.0, 'Total internal\nreflection at\nboundary',
        fontsize=8, color=C_LOVE, style='italic')

# Propagation direction
ax.annotate('', xy=(9.8, -0.55), xytext=(0.2, -0.55),
            arrowprops=dict(arrowstyle='->', color=C_LOVE, lw=2.0))
ax.text(5.0, -0.75, 'Propagation →', ha='center', fontsize=9, color=C_LOVE)

ax.legend(loc='lower right', fontsize=8.5, framealpha=0.9)

# ── Shared title ──────────────────────────────────────────────────────────
fig.suptitle('Surface Waves: Rayleigh and Love', fontsize=13,
             fontweight='bold', y=1.01)
fig.text(0.5, -0.04,
    'Panel (a)/(b): Rayleigh wave particle motion is retrograde elliptical, '
    'decaying exponentially below ~0.4λ depth. '
    'Panel (c): Love wave requires a slow layer overlying a faster half-space '
    '(total internal reflection of SH waves).',
    ha='center', fontsize=7.5, style='italic', color='#555', wrap=True)

plt.savefig('assets/figures/fig_surface_waves.png', dpi=300, bbox_inches='tight')
print('Saved: assets/figures/fig_surface_waves.png')
