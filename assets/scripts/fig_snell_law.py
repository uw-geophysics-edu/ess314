"""
fig_snell_law.py
================
Three-panel figure for seismic ray propagation at an interface:
  (a) Huygens' principle: secondary wavelets constructing a new wavefront
  (b) Geometric derivation of Snell's law from wavefront geometry
  (c) General Snell's law: reflected, refracted, and converted waves

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Figs. 3.15, 3.17, 3.18. Cambridge University Press. DOI: 10.1017/9781108685917
  Also consistent with: MIT OCW 12.510 Lecture 4 (CC BY NC SA)

Output : assets/figures/fig_snell_law.png
License: CC-BY 4.0 (this script)
"""
# Colorblind-safe WCAG AA palette:
# #0072B2 (blue), #E69F00 (orange), #56B4E9 (sky), #009E73 (green),
# #D55E00 (vermilion), #CC79A7 (pink), #000000 (black)

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Arc, FancyArrowPatch

mpl.rcParams.update({
    'font.size': 13,
    'axes.titlesize': 12,
    'axes.labelsize': 12,
    'xtick.labelsize': 11,
    'ytick.labelsize': 11,
})

C_INC    = '#0072B2'   # blue      – incident ray / medium 1
C_REFR   = '#009E73'   # green     – refracted ray / medium 2
C_REFL   = '#D55E00'   # vermilion – reflected ray
C_CONV   = '#CC79A7'   # pink      – converted (PS/SP) ray
C_INTER  = '#1a1a1a'   # black     – interface
C_WAVE   = '#56B4E9'   # sky       – wavefronts / Huygens wavelets
C_FILL1  = '#EAF4FB'   # light blue – medium 1 fill
C_FILL2  = '#E8F5E9'   # light green – medium 2 fill

fig, axes = plt.subplots(1, 3, figsize=(15, 5.8))
fig.subplots_adjust(wspace=0.38, left=0.03, right=0.98, top=0.90, bottom=0.08)

# ═══════════════════════════════════════════════════════════════════
# Panel (a) — Huygens' principle
# ═══════════════════════════════════════════════════════════════════
ax = axes[0]
ax.set_xlim(-0.5, 8.5); ax.set_ylim(-0.5, 7.5)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title("(a) Huygens' Principle", fontsize=12, pad=6)

# Initial wavefront (straight line)
wf_y = 1.2
ax.plot([0.0, 8.0], [wf_y, wf_y], color=C_INC, lw=2.0, label='Initial wavefront')
ax.text(8.1, wf_y, 'wavefront\n$t_0$', fontsize=9, va='center', color=C_INC)

# Point sources on the wavefront
pts_x = np.array([0.8, 2.0, 3.2, 4.4, 5.6, 6.8])
r_wavelet = 2.0   # radius grown by time Δt

for i, px in enumerate(pts_x):
    # Wavelet circle
    circle = plt.Circle((px, wf_y), r_wavelet, color=C_WAVE,
                         fill=False, lw=0.9, alpha=0.55)
    ax.add_patch(circle)
    # Source dot
    ax.plot(px, wf_y, 'o', ms=5, color=C_INC, zorder=4)

# New wavefront: tangent line to all wavelets (plane wave → same tangent)
new_y = wf_y + r_wavelet
ax.plot([0.0, 8.0], [new_y, new_y], color=C_WAVE, lw=2.5, ls='-', zorder=5)
ax.text(8.1, new_y, 'new wavefront\n$t_0+\\Delta t$', fontsize=9, va='center', color=C_WAVE)

# Propagation direction arrows
for px in [1.8, 4.2, 6.6]:
    ax.annotate('', xy=(px, new_y - 0.2), xytext=(px, wf_y + 0.2),
                arrowprops=dict(arrowstyle='->', color=C_INC, lw=1.3,
                                mutation_scale=12))

ax.text(4.0, 0.4,
        "Each point on wavefront\n= new point source",
        ha='center', fontsize=9.5, style='italic',
        bbox=dict(fc='white', ec=C_WAVE, alpha=0.85, boxstyle='round,pad=0.3'))

ax.text(4.0, 5.0,
        r"Envelope of wavelets $\Rightarrow$ new wavefront",
        ha='center', fontsize=9.5,
        bbox=dict(fc=C_FILL1, ec=C_INC, alpha=0.90, boxstyle='round,pad=0.3'))

# ═══════════════════════════════════════════════════════════════════
# Panel (b) — Geometric derivation of Snell's law
# ═══════════════════════════════════════════════════════════════════
ax = axes[1]
ax.set_xlim(-0.5, 8.0); ax.set_ylim(-4.5, 5.0)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title("(b) Snell's Law: Geometric Derivation", fontsize=12, pad=6)

# Interface
ax.axhline(0, color=C_INTER, lw=2.0, zorder=2)
ax.fill_between([-0.5, 8.0], [0, 0], [5, 5], color=C_FILL1, alpha=0.35)
ax.fill_between([-0.5, 8.0], [-4.5, -4.5], [0, 0], color=C_FILL2, alpha=0.35)
ax.text(0.1, 4.2, r'$V_1$ (medium 1)', fontsize=10, color=C_INC, style='italic')
ax.text(0.1, -4.0, r'$V_2 > V_1$ (medium 2)', fontsize=10, color=C_REFR, style='italic')

# Points for geometry
A = np.array([1.0, 4.0])   # ray 1 hits interface at B
B = np.array([3.0, 0.0])   # interface hit point 1
E = np.array([6.5, 0.0])   # interface hit point 2

# Incident ray A→B
ax.annotate('', xy=B, xytext=A,
            arrowprops=dict(arrowstyle='->', color=C_INC, lw=2.0, mutation_scale=14))

# Second ray wavefront (parallel to AB, arrives at E same time B is refracted)
# Direction of incident ray
dir_inc = (B - A) / np.linalg.norm(B - A)
C_pt = E + dir_inc * np.linalg.norm(B - A) * 0.95
ax.annotate('', xy=E, xytext=C_pt,
            arrowprops=dict(arrowstyle='->', color=C_INC, lw=2.0, mutation_scale=14,
                            linestyle='dashed'))

# Refracted ray from B
theta1 = np.arctan2(A[0]-B[0], A[1]-B[1])
v_ratio = 1.6   # V2/V1
theta2 = np.arcsin(np.sin(theta1) * v_ratio)
refr_dir = np.array([np.sin(theta2), -np.cos(theta2)])
B_refr = B + refr_dir * 3.5
ax.annotate('', xy=B_refr, xytext=B,
            arrowprops=dict(arrowstyle='->', color=C_REFR, lw=2.0, mutation_scale=14))

# Interface normal at B
ax.plot([B[0], B[0]], [B[1]-0.8, B[1]+0.8], color='gray', lw=1.0, ls='--', alpha=0.7)

# Angle theta1
arc1 = Arc(B, 1.0, 1.0, angle=0,
           theta1=90-np.degrees(theta1), theta2=90, color=C_INC, lw=1.5)
ax.add_patch(arc1)
ax.text(B[0]-0.70, B[1]+0.45, r'$\theta_1$', fontsize=12, color=C_INC)

# Angle theta2
arc2 = Arc(B, 1.0, 1.0, angle=0,
           theta1=270, theta2=270+np.degrees(theta2), color=C_REFR, lw=1.5)
ax.add_patch(arc2)
ax.text(B[0]+0.15, B[1]-0.70, r'$\theta_2$', fontsize=12, color=C_REFR)

# Geometry labels
ax.text((A[0]+B[0])/2 - 0.55, (A[1]+B[1])/2 + 0.3, '$a_1 t$', fontsize=11,
        color=C_INC)
ax.text(B[0] + 0.2, -2.2, '$a_2 t$', fontsize=11, color=C_REFR)
ax.text(B[0]+1.3, 0.28, 'AB', fontsize=9.5, color=C_INTER)

# Snell's law box
ax.text(4.0, 3.8,
        r'$\dfrac{\sin\theta_1}{V_1} = \dfrac{\sin\theta_2}{V_2}$'
        '\n= ray parameter $p$',
        ha='center', fontsize=11, fontweight='bold',
        bbox=dict(fc='#D4EDDA', ec='#28A745', alpha=0.97, boxstyle='round,pad=0.4'))

# ═══════════════════════════════════════════════════════════════════
# Panel (c) — Full Snell's law: P→P, P→S at a boundary
# ═══════════════════════════════════════════════════════════════════
ax = axes[2]
ax.set_xlim(-1.0, 9.0); ax.set_ylim(-5.0, 5.5)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title("(c) General Snell's Law: Incident, Reflected, Refracted",
             fontsize=12, pad=6)

ax.axhline(0, color=C_INTER, lw=2.0, zorder=2)
ax.fill_between([-1, 9], [0, 0], [5.5, 5.5], color=C_FILL1, alpha=0.30)
ax.fill_between([-1, 9], [-5.0, -5.0], [0, 0], color=C_FILL2, alpha=0.30)
ax.text(0.2, 5.0, r'$V_{P1},\ V_{S1}$', fontsize=10, color=C_INC)
ax.text(0.2, -4.5, r'$V_{P2} > V_{P1},\ V_{S2}$', fontsize=10, color=C_REFR)

origin = np.array([4.0, 0.0])
theta_i = 35.0    # incident angle (degrees)
ti_r = np.radians(theta_i)

# Incident P
A_inc = origin + np.array([-np.sin(ti_r), np.cos(ti_r)]) * 4.0
ax.annotate('', xy=origin, xytext=A_inc,
            arrowprops=dict(arrowstyle='->', color=C_INC, lw=2.2, mutation_scale=14))
ax.text((A_inc[0]+origin[0])/2 - 0.6, (A_inc[1]+origin[1])/2 + 0.1,
        'P$_\\mathrm{inc}$', fontsize=11, color=C_INC, fontweight='bold')

# Normal (dashed)
ax.plot([origin[0], origin[0]], [-1.2, 1.2], color='gray', lw=1.0, ls='--', alpha=0.7)

# Angle of incidence
arc_i = Arc(origin, 1.2, 1.2, angle=0,
            theta1=90-theta_i, theta2=90, color=C_INC, lw=1.5)
ax.add_patch(arc_i)
ax.text(origin[0]-0.9, origin[1]+0.42, r'$\theta_i$', fontsize=12, color=C_INC)

# Reflected P (same angle, opposite side)
A_refl = origin + np.array([np.sin(ti_r), np.cos(ti_r)]) * 3.5
ax.annotate('', xy=A_refl, xytext=origin,
            arrowprops=dict(arrowstyle='->', color=C_REFL, lw=2.2, mutation_scale=14))
ax.text((A_refl[0]+origin[0])/2 + 0.1, (A_refl[1]+origin[1])/2 + 0.1,
        'P$_\\mathrm{refl}$', fontsize=11, color=C_REFL, fontweight='bold')
arc_r = Arc(origin, 1.2, 1.2, angle=0,
            theta1=90, theta2=90+theta_i, color=C_REFL, lw=1.5)
ax.add_patch(arc_r)
ax.text(origin[0]+0.12, origin[1]+0.42, r'$\theta_i$', fontsize=12, color=C_REFL)

# Refracted P (Snell's law, V2 > V1 → larger angle)
VP2_VP1 = 1.65
theta_rp = np.degrees(np.arcsin(np.sin(ti_r) * VP2_VP1))
tpr = np.radians(theta_rp)
A_refr_p = origin + np.array([np.sin(tpr), -np.cos(tpr)]) * 3.8
ax.annotate('', xy=A_refr_p, xytext=origin,
            arrowprops=dict(arrowstyle='->', color=C_REFR, lw=2.2, mutation_scale=14))
ax.text((A_refr_p[0]+origin[0])/2 + 0.1, (A_refr_p[1]+origin[1])/2,
        'P$_\\mathrm{refr}$', fontsize=11, color=C_REFR, fontweight='bold')
arc_rp = Arc(origin, 1.4, 1.4, angle=0,
             theta1=270, theta2=270+theta_rp, color=C_REFR, lw=1.5)
ax.add_patch(arc_rp)
ax.text(origin[0]+0.30, origin[1]-0.85, r'$\theta_{P2}$', fontsize=11, color=C_REFR)

# Converted S (refracted, smaller velocity → smaller angle)
VS2_VP1 = 0.95
if np.sin(ti_r) * VS2_VP1 <= 1:
    theta_rs = np.degrees(np.arcsin(np.sin(ti_r) * VS2_VP1))
    tsr = np.radians(theta_rs)
    A_refr_s = origin + np.array([-np.sin(tsr), -np.cos(tsr)]) * 4.0
    ax.annotate('', xy=A_refr_s, xytext=origin,
                arrowprops=dict(arrowstyle='->', color=C_CONV, lw=2.2,
                                mutation_scale=14, linestyle='dashed'))
    ax.text((A_refr_s[0]+origin[0])/2 - 0.7, (A_refr_s[1]+origin[1])/2,
            'S$_\\mathrm{refr}$', fontsize=11, color=C_CONV, fontweight='bold')
    arc_rs = Arc(origin, 1.6, 1.6, angle=0,
                 theta1=270-theta_rs, theta2=270, color=C_CONV, lw=1.5)
    ax.add_patch(arc_rs)
    ax.text(origin[0]-1.2, origin[1]-0.85, r'$\theta_{S2}$', fontsize=11, color=C_CONV)

# Snell's law box
ax.text(4.0, -3.8,
        r'$\dfrac{\sin\theta_i}{V_{P1}} = \dfrac{\sin\theta_{P2}}{V_{P2}} = \dfrac{\sin\theta_{S2}}{V_{S2}} = p$',
        ha='center', fontsize=10, fontweight='bold',
        bbox=dict(fc='#D4EDDA', ec='#28A745', alpha=0.97, boxstyle='round,pad=0.4'))

ax.text(4.0, -2.8, 'ray parameter $p$ = constant', ha='center', fontsize=9.5,
        color='#444', style='italic')

# Legend
handles = [
    mpatches.Patch(color=C_INC,  label='Incident P'),
    mpatches.Patch(color=C_REFL, label='Reflected P'),
    mpatches.Patch(color=C_REFR, label='Refracted P'),
    mpatches.Patch(color=C_CONV, label='Converted S'),
]
ax.legend(handles=handles, loc='upper right', fontsize=8.5, framealpha=0.9)

# ── Title ─────────────────────────────────────────────────────────────────
fig.suptitle("Huygens' Principle and Snell's Law for Seismic Rays",
             fontsize=14, fontweight='bold', y=0.99)
fig.text(0.5, -0.01,
    'Colors: blue = incident/medium 1, green = refracted/medium 2, '
    'vermilion = reflected, pink = converted. '
    'Line style also distinguishes ray types (solid vs dashed).',
    ha='center', fontsize=9.0, style='italic', color='#555')

plt.savefig('assets/figures/fig_snell_law.png', dpi=150, bbox_inches='tight')
print('Saved: assets/figures/fig_snell_law.png')

if __name__ == '__main__':
    pass
