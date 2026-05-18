"""
fig_induced_vs_remanent.py

Scientific content: Magnetisation M as a function of applied field H, for
three categories of magnetic ordering, displayed on common axes:

  • Diamagnetic     — linear, small *negative* slope; passes through origin
  • Paramagnetic    — linear, small *positive* slope; passes through origin
  • Ferri/ferro     — non-linear hysteresis loop with non-zero remanent
                       magnetisation M_r at H = 0 and non-zero coercive
                       field H_c at M = 0

The figure makes two pedagogical points explicit:

  1. Diamagnetic and paramagnetic materials are *induced-only*: when the
     applied field H is removed, M returns to zero. They contribute to
     anomalies *while* the surveying field is on, but they carry no
     memory of past fields.

  2. Ferrimagnetic (and ferromagnetic) materials *retain* a non-zero
     magnetisation M_r at H = 0 — this is the *remanent* magnetisation
     that records geomagnetic history. They also have a coercive field
     H_c, the reverse field needed to demagnetise them.

The Königsberger ratio Q = |M_r| / |M_ind| (computed for the same applied
field) measures which response dominates in a given rock.

Reference: Tauxe et al. (2018), *Essentials of Paleomagnetism*, 5th Web
Edition, Ch. 4. Open access: https://earthref.org/MagIC/books/Tauxe/2010/

Output: assets/figures/fig_induced_vs_remanent.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Global rcParams ─────────────────────────────────────────────────
mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# Colorblind-safe palette
C_DIA   = "#A8A8A8"
C_PARA  = "#0072B2"
C_FERRI = "#D55E00"

fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.6),
                         gridspec_kw={"width_ratios": [1.0, 1.0]})

# ── Common H grid (units: arbitrary applied field, e.g. A/m) ──────
H = np.linspace(-1.0, 1.0, 401)

# ── Left panel: induced-only linear responses ─────────────────────
ax = axes[0]

k_dia  = -0.10    # negative, small
k_para = +0.12    # positive, small

M_dia  = k_dia  * H
M_para = k_para * H

ax.axhline(0, color="black", linewidth=0.8, alpha=0.6)
ax.axvline(0, color="black", linewidth=0.8, alpha=0.6)

ax.plot(H, M_dia,  color=C_DIA,  linewidth=3.0,
        label="Diamagnetic (quartz, halite): $k < 0$")
ax.plot(H, M_para, color=C_PARA, linewidth=3.0,
        label="Paramagnetic (olivine, biotite): $k > 0$, small")

# Annotation: "removes the field, M returns to zero"
ax.scatter([0], [0], color="black", s=80, zorder=5)
ax.annotate("Turn $H$ off:\n$M = 0$ for both",
            xy=(0, 0), xytext=(0.35, 0.36),
            fontsize=11.5, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor="black", linewidth=1.0),
            arrowprops=dict(arrowstyle="->", color="black", lw=1.2,
                            connectionstyle="arc3,rad=-0.15"))

ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-0.5, 0.5)
ax.set_xlabel("Applied field $H$  (arbitrary units)")
ax.set_ylabel("Magnetisation $M$  (arbitrary units)")
ax.set_title("Induced-only regime\n"
             "$M = kH$ — vanishes when $H = 0$",
             fontsize=13)
ax.legend(loc="lower right", framealpha=0.95)
ax.grid(True, alpha=0.30)

# ── Right panel: ferri/ferromagnetic hysteresis ───────────────────
ax = axes[1]

# Build a hysteresis loop using a simple tanh-shifted parameterisation
# (qualitatively correct, with explicit M_r and H_c)
M_s = 1.0    # saturation magnetisation
H_c = 0.25   # coercivity
M_r = 0.72   # remanent magnetisation at H = 0

# Approximate upper and lower branches:
#   upper branch: M_up(H)  = M_s * tanh((H + H_c) / w),  w controls steepness
#   lower branch: M_lo(H)  = M_s * tanh((H - H_c) / w)
# At H = 0, M_up = M_s*tanh(H_c/w) — choose w so that this equals M_r.
w = H_c / np.arctanh(M_r / M_s)

# Sweep H from -1 to +1 (upper branch reached by ascending from negative
# saturation) and back (lower branch by descending from positive saturation)
H_sweep_up   = np.linspace(-1.0, 1.0, 300)
H_sweep_down = np.linspace( 1.0, -1.0, 300)
M_up   = M_s * np.tanh((H_sweep_up   + H_c) / w)
M_down = M_s * np.tanh((H_sweep_down - H_c) / w)

ax.axhline(0, color="black", linewidth=0.8, alpha=0.6)
ax.axvline(0, color="black", linewidth=0.8, alpha=0.6)

# Plot the loop
ax.plot(H_sweep_up,   M_up,   color=C_FERRI, linewidth=3.0, label="Sweep up")
ax.plot(H_sweep_down, M_down, color=C_FERRI, linewidth=3.0, linestyle="--",
        label="Sweep down")

# Mark M_r at H = 0 (upper branch)
ax.scatter([0], [M_r], color="black", zorder=5, s=80)
ax.annotate(f"$M_r$ (remanence)\n= {M_r:.2f} $M_s$",
            xy=(0, M_r), xytext=(0.25, M_r + 0.18),
            fontsize=11.5, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=C_FERRI, linewidth=1.4),
            arrowprops=dict(arrowstyle="->", color=C_FERRI, lw=1.4,
                            connectionstyle="arc3,rad=-0.15"))

# Mark -M_r at H = 0 (lower branch)
ax.scatter([0], [-M_r], color="black", zorder=5, s=80)

# Mark H_c on the lower branch
ax.scatter([H_c], [0], color="black", zorder=5, s=80)
ax.annotate(f"$H_c$ (coercivity)\n= {H_c:.2f}",
            xy=(H_c, 0), xytext=(H_c + 0.18, -0.45),
            fontsize=11.5, ha="left", va="center",
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=C_FERRI, linewidth=1.4),
            arrowprops=dict(arrowstyle="->", color=C_FERRI, lw=1.4,
                            connectionstyle="arc3,rad=-0.15"))

# Saturation labels
ax.axhline( M_s, color=C_FERRI, linewidth=0.7, linestyle=":", alpha=0.6)
ax.axhline(-M_s, color=C_FERRI, linewidth=0.7, linestyle=":", alpha=0.6)
ax.text(-1.0, M_s + 0.05, "$+M_s$ (saturation)", fontsize=11,
        ha="left", va="bottom", color=C_FERRI)
ax.text(-1.0, -M_s - 0.05, "$-M_s$", fontsize=11,
        ha="left", va="top", color=C_FERRI)

ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-1.25, 1.25)
ax.set_xlabel("Applied field $H$  (arbitrary units)")
ax.set_ylabel("Magnetisation $M$  (arbitrary units)")
ax.set_title("Remanent regime — ferri / ferromagnetic\n"
             "Hysteresis: $M \\neq 0$ at $H = 0$",
             fontsize=13)
ax.legend(loc="upper left", framealpha=0.95)
ax.grid(True, alpha=0.30)

# ── Master annotation strip below both panels ─────────────────────
fig.suptitle(
    "Two regimes of rock magnetism: induced (lost when the field is removed) vs. remanent (locked in)",
    fontsize=14, fontweight="bold", y=1.02,
)

fig.text(
    0.5, -0.07,
    "Königsberger ratio  $Q = |M_r| / |M_{\\mathrm{ind}}|$  measures which regime dominates the rock's bulk response.  "
    "$Q \\ll 1$: induced dominates (granite, sandstone). "
    "$Q \\gg 1$: remanence dominates (basalt, hematite-rich red beds).",
    fontsize=11.5, ha="center", va="top", style="italic", color="#333333",
    bbox=dict(boxstyle="round,pad=0.4", facecolor="#F4F4F4", edgecolor="#888888"),
)

fig.tight_layout()
fig.savefig("../figures/fig_induced_vs_remanent.png",
            dpi=300, bbox_inches="tight")
plt.close(fig)
print("Wrote assets/figures/fig_induced_vs_remanent.png")
