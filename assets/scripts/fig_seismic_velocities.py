"""
fig_seismic_velocities.py
=========================
Horizontal bar chart of representative P-wave velocities (Vp) for
Earth materials and common engineering materials.

Data compiled from:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.,
  Table 3.1. Cambridge University Press. DOI: 10.1017/9781108685917
  Also: Telford et al. (1990). Applied Geophysics, 2nd ed., Cambridge.

Output : assets/figures/fig_seismic_velocities.png
License: CC-BY 4.0
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Data ──────────────────────────────────────────────────────────────────────
materials = {
    # Earth materials — rocks
    'Granite':           (4800, 6400),
    'Basalt':            (5500, 6500),
    'Limestone':         (3500, 6000),
    'Sandstone':         (2000, 4500),
    'Salt rock':         (4200, 5500),
    'Shale':             (2100, 4500),
    # Earth materials — unconsolidated
    'Dry sand':          (200,  1000),
    'Wet sand':          (1500, 2000),
    'Clay (Vs)':         (60,   150),
    # Fluids
    'Seawater':          (1470, 1540),
    'Freshwater':        (1450, 1510),
    'Oil':               (1200, 1350),
    # Engineering materials
    'Steel':             (5800, 6100),
    'Aluminum':          (6100, 6400),
    'Concrete':          (3000, 4500),
    'Ice':               (3000, 4200),
}

# ── Category colors (colorblind-safe) ────────────────────────────────────────
cat_colors = {
    'Granite':    '#0072B2',
    'Basalt':     '#0072B2',
    'Limestone':  '#0072B2',
    'Sandstone':  '#0072B2',
    'Salt rock':  '#0072B2',
    'Shale':      '#0072B2',
    'Dry sand':   '#56B4E9',
    'Wet sand':   '#56B4E9',
    'Clay (Vs)':  '#56B4E9',
    'Seawater':   '#009E73',
    'Freshwater': '#009E73',
    'Oil':        '#009E73',
    'Steel':      '#E69F00',
    'Aluminum':   '#E69F00',
    'Concrete':   '#E69F00',
    'Ice':        '#E69F00',
}

labels = list(materials.keys())[::-1]
lows   = [materials[m][0] for m in labels]
highs  = [materials[m][1] for m in labels]
colors = [cat_colors[m] for m in labels]

fig, ax = plt.subplots(figsize=(9, 7))

y = np.arange(len(labels))
bar_h = 0.65

for i, (lo, hi, lbl, col) in enumerate(zip(lows, highs, labels, colors)):
    # Range bar
    ax.barh(y[i], hi - lo, left=lo, height=bar_h, color=col, alpha=0.75,
            edgecolor='black', lw=0.6, zorder=3)
    # Midpoint marker
    mid = (lo + hi) / 2
    ax.plot(mid, y[i], 'o', color='white', ms=5, zorder=5, mec=col, mew=1.2)
    # Value label at right end
    ax.text(hi + 60, y[i], f'{lo}–{hi}', va='center', fontsize=7.5, color='#333')

ax.set_yticks(y)
ax.set_yticklabels(labels, fontsize=9.5)
ax.set_xlabel(r'$V_P$ (m/s)', fontsize=12)
ax.set_title('Representative P-wave Velocities\nfor Earth and Engineering Materials',
             fontsize=12, fontweight='bold')
ax.set_xlim(0, 8000)
ax.spines[['top', 'right']].set_visible(False)
ax.axvline(1500, color='#aaa', lw=1.0, ls=':', zorder=1)
ax.text(1520, -0.7, 'Vwater\n~1480 m/s', fontsize=7.5, color='#777', style='italic')

# Dividing lines between categories
ax.axhline(5.5, color='#ddd', lw=1.2, zorder=0)    # rocks / unconsolidated
ax.axhline(8.5, color='#ddd', lw=1.2, zorder=0)    # unconsolidated / fluids
ax.axhline(11.5, color='#ddd', lw=1.2, zorder=0)   # fluids / engineering

# Legend
rock_p   = mpatches.Patch(color='#0072B2', alpha=0.75, label='Crystalline / sedimentary rock')
uncon_p  = mpatches.Patch(color='#56B4E9', alpha=0.75, label='Unconsolidated sediment / soil')
fluid_p  = mpatches.Patch(color='#009E73', alpha=0.75, label='Fluid')
eng_p    = mpatches.Patch(color='#E69F00', alpha=0.75, label='Engineering material')
ax.legend(handles=[rock_p, uncon_p, fluid_p, eng_p],
          loc='lower right', fontsize=8.5, framealpha=0.95)

fig.text(0.5, -0.02,
    'Bars show typical ranges; filled circle marks approximate midpoint. '
    'Color and y-position both encode material category.',
    ha='center', fontsize=7.5, style='italic', color='#555')

plt.tight_layout()
plt.savefig('assets/figures/fig_seismic_velocities.png', dpi=70, bbox_inches='tight')
print('Saved: assets/figures/fig_seismic_velocities.png')
