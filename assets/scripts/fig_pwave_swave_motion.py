"""
fig_pwave_swave_motion.py
=========================
Two-panel figure showing particle motion for P-waves and S-waves,
illustrating compression/rarefaction zones and transverse oscillation.

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.
  Cambridge University Press. DOI: 10.1017/9781108685917
  Also consistent with: MIT OCW 12.201 §4.5 (CC BY NC SA)

Output : assets/figures/fig_pwave_swave_motion.png
License: CC-BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ── Palette ───────────────────────────────────────────────────────────────────
C_COMPRESS = '#0072B2'   # blue    – compression zone
C_RAREFY   = '#56B4E9'   # sky     – rarefaction zone
C_NEUTRAL  = '#BBBBBB'   # gray    – neutral / unperturbed
C_ARROW    = '#D55E00'   # vermilion – particle displacement arrows
C_PROP     = '#009E73'   # green   – propagation direction

fig, axes = plt.subplots(2, 1, figsize=(11, 7))
fig.subplots_adjust(hspace=0.55)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 1 — P-wave (compressional, longitudinal)
# ─────────────────────────────────────────────────────────────────────────────
ax = axes[0]
ax.set_xlim(0, 12)
ax.set_ylim(-1.0, 1.8)
ax.axis('off')
ax.set_title('P-wave (Primary / Compressional): particle motion ∥ propagation direction',
             fontsize=10.5, fontweight='bold', pad=4)

# Draw a sinusoidal pressure wave as alternating colored bands
n_particles = 28
x_base = np.linspace(0.3, 11.7, n_particles)
wavelength = 4.0
k = 2 * np.pi / wavelength
A_p = 0.38   # amplitude of particle displacement

# Color each particle zone by local compression state
for i, xb in enumerate(x_base):
    disp = A_p * np.sin(k * xb)
    # Color by local strain ∂u/∂x ≈ displacement gradient
    grad = A_p * k * np.cos(k * xb)
    if grad < -0.2:
        col = C_COMPRESS
    elif grad > 0.2:
        col = C_RAREFY
    else:
        col = C_NEUTRAL

    # Draw particle as circle
    circle = plt.Circle((xb + disp, 0), 0.18, color=col, zorder=3,
                         ec='black', lw=0.5)
    ax.add_patch(circle)
    # Displacement arrow
    if abs(disp) > 0.04:
        ax.annotate('', xy=(xb + disp, 0), xytext=(xb, 0),
                    arrowprops=dict(arrowstyle='->', color=C_ARROW,
                                    lw=1.2, mutation_scale=10))

# Zone labels
for xlabel, lbl, col in [(1.4, 'Compression\n(C)', C_COMPRESS),
                           (3.4, 'Rarefaction\n(R)', C_RAREFY),
                           (5.4, 'C', C_COMPRESS),
                           (7.4, 'R', C_RAREFY),
                           (9.4, 'C', C_COMPRESS)]:
    ax.text(xlabel, -0.65, lbl, ha='center', fontsize=8.5,
            color=col, fontweight='bold')

# Propagation direction arrow
ax.annotate('', xy=(11.5, 1.4), xytext=(0.5, 1.4),
            arrowprops=dict(arrowstyle='->', color=C_PROP, lw=2.0))
ax.text(6.0, 1.6, 'Propagation direction →', ha='center', fontsize=9.5,
        color=C_PROP, fontweight='bold')

# Legend
comp_p = mpatches.Patch(color=C_COMPRESS, label='Compression')
rare_p = mpatches.Patch(color=C_RAREFY,   label='Rarefaction')
neut_p = mpatches.Patch(color=C_NEUTRAL,  label='Neutral')
ax.legend(handles=[comp_p, rare_p, neut_p], loc='lower right', fontsize=8.5,
          framealpha=0.9)
ax.text(0.2, 0.35, 'Particle\ndisplacement\n∥ propagation', fontsize=8, color=C_ARROW)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 2 — S-wave (shear, transverse)
# ─────────────────────────────────────────────────────────────────────────────
ax = axes[1]
ax.set_xlim(0, 12)
ax.set_ylim(-1.5, 2.0)
ax.axis('off')
ax.set_title('S-wave (Secondary / Shear): particle motion ⊥ propagation direction\n'
             '(SV = vertical shear shown here; SH = horizontal shear, into page)',
             fontsize=10.5, fontweight='bold', pad=4)

x_base = np.linspace(0.3, 11.7, 26)
A_s = 0.70   # transverse amplitude

for xb in x_base:
    disp_y = A_s * np.sin(k * xb)
    circle = plt.Circle((xb, disp_y), 0.18, color=C_NEUTRAL, zorder=3,
                         ec='black', lw=0.5)
    ax.add_patch(circle)
    # Vertical displacement arrow
    if abs(disp_y) > 0.07:
        ax.annotate('', xy=(xb, disp_y), xytext=(xb, 0),
                    arrowprops=dict(arrowstyle='->', color=C_ARROW,
                                    lw=1.2, mutation_scale=10))

# Equilibrium line
ax.axhline(0, color='black', lw=0.8, ls='--', alpha=0.5)

# Sinusoidal envelope
x_env = np.linspace(0.3, 11.7, 200)
ax.plot(x_env, A_s * np.sin(k * x_env), color=C_NEUTRAL, lw=1.0, ls=':', alpha=0.6)

# Propagation direction
ax.annotate('', xy=(11.5, 1.65), xytext=(0.5, 1.65),
            arrowprops=dict(arrowstyle='->', color=C_PROP, lw=2.0))
ax.text(6.0, 1.85, 'Propagation direction →', ha='center', fontsize=9.5,
        color=C_PROP, fontweight='bold')

# Amplitude label
ax.annotate('', xy=(0.3, A_s), xytext=(0.3, 0),
            arrowprops=dict(arrowstyle='<->', color=C_ARROW, lw=1.5))
ax.text(0.0, A_s/2, '$A$', ha='right', va='center', fontsize=11, color=C_ARROW)

ax.text(0.2, -0.35, 'Particle\ndisplacement\n⊥ propagation', fontsize=8, color=C_ARROW)

# Key difference callout
ax.text(5.5, -1.25,
    'Key: S-waves require shear rigidity (μ ≠ 0)\n'
    '→ S-waves CANNOT propagate in fluids (μ = 0)',
    ha='center', fontsize=9, style='italic',
    bbox=dict(fc='#FFF3CD', ec='#E69F00', alpha=0.95, boxstyle='round,pad=0.4'))

fig.suptitle('Seismic Body Wave Particle Motion', fontsize=13, fontweight='bold', y=1.01)
fig.text(0.5, -0.02,
    'Colors encode compression state in P-wave (blue=compression, sky=rarefaction, gray=neutral). '
    'Arrow orientation encodes displacement direction independently of color.',
    ha='center', fontsize=7.5, style='italic', color='#555')

plt.savefig('assets/figures/fig_pwave_swave_motion.png', dpi=150, bbox_inches='tight')
print('Saved: assets/figures/fig_pwave_swave_motion.png')
