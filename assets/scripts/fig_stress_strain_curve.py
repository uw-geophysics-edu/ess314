"""
fig_stress_strain_curve.py
==========================
Stress–strain behavior of an elastic solid, showing the linear (Hookean)
regime, linearity limit, elastic limit, plastic deformation zone, and failure.

Reproduces the scientific content of the stress-strain schematic in:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.
  Cambridge University Press. DOI: 10.1017/9781108685917

This script is an original, Python-generated figure. No element reproduces
the original illustration; it is derived from first-principles schematic geometry.

Output : assets/figures/fig_stress_strain_curve.png
License: CC-BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

# ── Colorblind-safe WCAG AA palette ──────────────────────────────────────────
C_ELASTIC  = '#0072B2'   # blue  – Hookean / linear elastic region
C_NONLIN   = '#E69F00'   # amber – nonlinear elastic
C_PLASTIC  = '#D55E00'   # vermilion – plastic deformation
C_UNLOAD   = '#009E73'   # green – unloading path
C_ANNOT    = '#333333'   # near-black – labels / arrows

def make_curve():
    """Return (strain, stress) arrays for a schematic stress-strain curve."""
    # Linear elastic region  0 → εL
    eps_L = 0.02          # linearity limit strain
    eps_E = 0.035         # elastic limit strain
    eps_F = 0.12          # failure strain

    E_mod = 40.0          # slope in linear region  (arbitrary units)
    sig_L = E_mod * eps_L
    sig_E = sig_L * 1.30  # slight overshoot to elastic limit
    sig_F = sig_E * 1.15  # peak before failure

    # Piece-wise curve
    e1 = np.linspace(0,      eps_L, 50)
    s1 = E_mod * e1                                       # linear

    e2 = np.linspace(eps_L, eps_E, 30)
    s2 = sig_L + (sig_E - sig_L) * np.sin(
             np.pi/2 * (e2 - eps_L)/(eps_E - eps_L))      # nonlinear to elastic limit

    e3 = np.linspace(eps_E, eps_F, 60)
    # gentle curve up to peak then softens
    t  = (e3 - eps_E) / (eps_F - eps_E)
    s3 = sig_E + (sig_F - sig_E) * np.sin(np.pi * t * 0.5) \
         - (sig_F - sig_E * 0.55) * t**2                   # work-hardening then softening

    eps = np.concatenate([e1, e2, e3])
    sig = np.concatenate([s1, s2, s3])
    return eps, sig, eps_L, eps_E, eps_F, sig_L, sig_E

def make_unload(eps, sig, eps_L, eps_E, sig_E):
    """Unloading path from the elastic limit back to permanent strain."""
    # Unloads with the original elastic slope from the elastic limit
    E_mod = sig_L_val = sig_E / 1.30 / 0.02 * 40  # recover slope
    # Straight line from (eps_E, sig_E) down to x-axis with original slope
    eps_perm = eps_E - sig_E / 40.0
    e_unload = np.linspace(eps_E, eps_perm, 40)
    s_unload = sig_E - 40.0 * (e_unload - eps_E) * (-1)
    # slope = -E so sig decreases
    s_unload = sig_E + 40.0 * (eps_E - e_unload)
    return e_unload, s_unload, eps_perm


eps, sig, eps_L, eps_E, eps_F, sig_L, sig_E = make_curve()
e_un, s_un, eps_perm = make_unload(eps, sig, eps_L, eps_E, sig_E)

fig, ax = plt.subplots(figsize=(8, 5.5))

# ── Main curve ──
ax.plot(eps[:50], sig[:50], color=C_ELASTIC, lw=2.5, label='Linear elastic (Hooke\'s law)')
ax.plot(eps[50:80], sig[50:80], color=C_NONLIN, lw=2.5, label='Nonlinear elastic')
ax.plot(eps[80:], sig[80:], color=C_PLASTIC, lw=2.5, label='Plastic deformation')

# ── Unloading path ──
ax.plot(e_un, s_un, color=C_UNLOAD, lw=2.0, ls='--', label='Unloading path')

# ── Permanent strain indicator ──
ax.annotate('', xy=(eps_perm, 0.01), xytext=(0, 0.01),
            arrowprops=dict(arrowstyle='<->', color=C_UNLOAD, lw=1.5))
ax.text(eps_perm/2, 0.25, 'permanent\nstrain', ha='center', va='bottom',
        fontsize=9, color=C_UNLOAD)

# ── Vertical dashed markers ──
for xv, col, lbl in [(eps_L, C_NONLIN, ''), (eps_E, C_PLASTIC, '')]:
    ax.axvline(xv, ls=':', color=col, lw=1.2, alpha=0.7)

# ── Region bracket annotations ──
y_bracket = sig_E * 1.22
# elastic range bracket
ax.annotate('', xy=(eps_E, y_bracket), xytext=(0, y_bracket),
            arrowprops=dict(arrowstyle='<->', color=C_ANNOT, lw=1.2))
ax.text(eps_E/2, y_bracket + 0.2, 'elastic range', ha='center',
        fontsize=9, color=C_ANNOT)
# plastic deformation bracket
ax.annotate('', xy=(eps_F, y_bracket), xytext=(eps_E, y_bracket),
            arrowprops=dict(arrowstyle='<->', color=C_ANNOT, lw=1.2))
ax.text((eps_E + eps_F)/2, y_bracket + 0.2, 'plastic\ndeformation',
        ha='center', fontsize=9, color=C_ANNOT)

# ── Point labels ──
ax.annotate('linearity\nlimit', xy=(eps_L, sig_L),
            xytext=(eps_L - 0.007, 1.20),
            fontsize=8.5, color=C_NONLIN, ha='center',
            arrowprops=dict(arrowstyle='->', color=C_NONLIN, lw=1.0))
ax.annotate('elastic\nlimit', xy=(eps_E, sig_E),
            xytext=(eps_E + 0.015, 1.25),
            fontsize=8.5, color=C_PLASTIC, ha='left',
            arrowprops=dict(arrowstyle='->', color=C_PLASTIC, lw=1.0))

# Failure annotation
sig_peak_idx = np.argmax(sig[80:]) + 80
ax.annotate('failure', xy=(eps[sig_peak_idx], sig[sig_peak_idx]),
            xytext=(eps[sig_peak_idx] - 0.015, 1.28),
            fontsize=8.5, color=C_PLASTIC, ha='left',
            arrowprops=dict(arrowstyle='->', color=C_PLASTIC, lw=1.0))

# ── Hooke's law slope indicator ──
x0, x1 = 0.002, 0.015
ax.plot([x0, x1], [40*x0, 40*x1], color='white', lw=4, zorder=3)
ax.annotate('Hooke\'s law\n(linear)', xy=(0.010, 40*0.010),
            xytext=(0.001, 1.30),
            fontsize=8.5, color=C_ELASTIC,
            arrowprops=dict(arrowstyle='->', color=C_ELASTIC, lw=1.0))

ax.set_xlabel(r'Strain $\varepsilon$ (dimensionless)', fontsize=12)
ax.set_ylabel(r'Stress $\sigma$ (MPa)', fontsize=12)
ax.set_title('Stress–Strain Behavior of an Elastic Solid', fontsize=13, fontweight='bold')
ax.set_xlim(-0.002, eps_F + 0.01)
ax.set_ylim(-1, sig_E * 1.42)
ax.legend(loc='lower right', fontsize=9, framealpha=0.9)
ax.spines[['top', 'right']].set_visible(False)

# Colorblind note
fig.text(0.5, -0.03,
    'Colors: blue = linear elastic, amber = nonlinear elastic, vermilion = plastic. '
    'Line style also encodes the unloading path (dashed).',
    ha='center', fontsize=7.5, style='italic', color='#555')

plt.tight_layout()
plt.savefig('assets/figures/fig_stress_strain_curve.png', dpi=150, bbox_inches='tight')
print('Saved: assets/figures/fig_stress_strain_curve.png')

if __name__ == '__main__':
    pass
