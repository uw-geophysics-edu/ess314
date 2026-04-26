"""
fig_polarization_baz.py

Scientific content: Single-station back-azimuth estimation from P-wave
polarization. Because P-waves are longitudinally polarized along the
direction of propagation, the ratio of the first-motion amplitudes on
the East and North horizontal components yields the back-azimuth — the
direction *from* the station *to* the source — modulo a 180° ambiguity
that the vertical-component polarity resolves.

Reproduces the scientific content of:
  Stein & Wysession (2003), Ch. 5 §5.3.
  Lowrie & Fichtner (2020), Ch. 5.

Output: assets/figures/fig_polarization_baz.png
License: CC-BY 4.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import patches

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 130, "savefig.dpi": 200,
})

C_N = "#0072B2"
C_E = "#E69F00"
C_Z = "#009E73"
C_TRACE = "#1A1A1A"
C_BAZ = "#D55E00"

fig, axes = plt.subplots(1, 2, figsize=(13.5, 5.6),
                         gridspec_kw=dict(width_ratios=[1.0, 1.0]))

# ── Panel (a): three-component first-motion seismogram ─────────────
ax = axes[0]
t = np.linspace(0, 2.5, 2500)
t_p = 0.5     # P-arrival time
amp_n = 0.85   # peak amplitude on N component (positive)
amp_e = 0.45   # peak amplitude on E component (positive)
amp_z = 0.92   # peak amplitude on Z component (negative — upward = downward in seismogram convention varies)

def first_motion(t, t0, peak, w=0.10):
    arg = ((t - t0) / w) ** 2
    return peak * (1 - 2 * arg) * np.exp(-arg)


n_trace = first_motion(t, t_p, amp_n) + 0.02 * np.random.default_rng(1).standard_normal(t.size)
e_trace = first_motion(t, t_p, amp_e) + 0.02 * np.random.default_rng(2).standard_normal(t.size)
z_trace = first_motion(t, t_p, amp_z) + 0.02 * np.random.default_rng(3).standard_normal(t.size)

# Stack the three traces with vertical offset
spacing = 1.5
ax.plot(t, n_trace + 2 * spacing, color=C_N, lw=1.2)
ax.plot(t, e_trace + 1 * spacing, color=C_E, lw=1.2)
ax.plot(t, z_trace + 0 * spacing, color=C_Z, lw=1.2)

# Phase pick line
ax.axvline(t_p, color="#444", lw=1.0, ls="--", zorder=3)

# Amplitude annotations (peak first-motion)
ax.annotate(f"$A_N = {amp_n:.2f}$", xy=(t_p + 0.05, 2 * spacing + amp_n),
            xytext=(t_p + 0.55, 2 * spacing + amp_n),
            fontsize=11, color=C_N,
            arrowprops=dict(arrowstyle="->", color=C_N, lw=0.8))
ax.annotate(f"$A_E = {amp_e:.2f}$", xy=(t_p + 0.05, 1 * spacing + amp_e),
            xytext=(t_p + 0.55, 1 * spacing + amp_e),
            fontsize=11, color=C_E,
            arrowprops=dict(arrowstyle="->", color=C_E, lw=0.8))
ax.annotate(f"$A_Z = {amp_z:.2f}$ (up)", xy=(t_p + 0.05, 0 + amp_z),
            xytext=(t_p + 0.55, 0 + amp_z),
            fontsize=11, color=C_Z,
            arrowprops=dict(arrowstyle="->", color=C_Z, lw=0.8))

# Component labels
ax.text(0.05, 2 * spacing, "N", fontsize=14, fontweight="bold",
        color=C_N, va="center")
ax.text(0.05, 1 * spacing, "E", fontsize=14, fontweight="bold",
        color=C_E, va="center")
ax.text(0.05, 0, "Z", fontsize=14, fontweight="bold",
        color=C_Z, va="center")

ax.set_xlim(0, 2.5)
ax.set_ylim(-1.6, 4.5)
ax.set_xlabel("Time (s)")
ax.set_yticks([])
ax.set_title("(a) Read first-motion amplitudes on N, E, Z",
             fontsize=13, pad=8)
ax.grid(False)

# ── Panel (b): map view with back-azimuth ──────────────────────────
ax = axes[1]
ax.set_xlim(-1.4, 1.4)
ax.set_ylim(-1.4, 1.4)
ax.set_aspect("equal")
ax.set_xticks([])
ax.set_yticks([])
ax.set_title("(b) Particle-motion vector → back-azimuth (BAZ)",
             fontsize=13, pad=8)

# Compass rose
ax.axhline(0, color="#888", lw=0.6, zorder=1)
ax.axvline(0, color="#888", lw=0.6, zorder=1)
compass = patches.Circle((0, 0), 1.2, fill=False, edgecolor="#888", lw=1.2,
                         zorder=2)
ax.add_patch(compass)
for label, x, y in [("N", 0, 1.30), ("S", 0, -1.30),
                    ("E", 1.30, 0), ("W", -1.30, 0)]:
    ax.text(x, y, label, ha="center", va="center", fontsize=12,
            fontweight="bold", color="#222")

# Station at origin
ax.plot(0, 0, marker="^", color="#009E73", ms=18, mec="#000", mew=1.0,
        zorder=6)
ax.text(0.0, -0.18, "Station", ha="center", va="top", fontsize=11,
        fontweight="bold")

# Draw the particle-motion vector (A_E, A_N) — pointing to source for downward P
A_N_norm = amp_n / np.sqrt(amp_n ** 2 + amp_e ** 2)
A_E_norm = amp_e / np.sqrt(amp_n ** 2 + amp_e ** 2)
# Z is positive upward in seismogram convention here; AZ > 0 means motion is
# upward; for an emergent P arriving from below, upward Z means the source
# is in the direction (A_E, A_N). For downward Z, source is (-A_E, -A_N).
ax.annotate("", xy=(A_E_norm, A_N_norm), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=C_BAZ, lw=2.6,
                            mutation_scale=20))

# Back-azimuth angle arc
azi = np.degrees(np.arctan2(A_E_norm, A_N_norm))   # azimuth from N, clockwise
arc = patches.Arc((0, 0), 0.7, 0.7, angle=0, theta1=90 - azi, theta2=90,
                  color=C_BAZ, lw=2.0)
ax.add_patch(arc)
ax.text(0.18, 0.45, f"BAZ\n= {azi:.0f}°", color=C_BAZ, fontsize=12,
        fontweight="bold", ha="center", va="center")

# Source direction annotation
ax.annotate("To source\n(epicenter)", xy=(A_E_norm * 1.05, A_N_norm * 1.05),
            xytext=(0.95, 1.0),
            fontsize=11, color=C_BAZ, ha="center",
            arrowprops=dict(arrowstyle="->", color=C_BAZ, lw=0.8),
            bbox=dict(facecolor="white", edgecolor=C_BAZ, lw=0.6,
                      boxstyle="round,pad=0.25"))

# Equation box
ax.text(0, -1.05,
        r"$\mathrm{BAZ} = \arctan(A_E / A_N) + 180°\,$ if Z is downward",
        ha="center", va="top", fontsize=11,
        bbox=dict(facecolor="white", edgecolor="#444", lw=0.6,
                  boxstyle="round,pad=0.3"))

fig.suptitle("Single-station back-azimuth from P-wave polarization",
             fontsize=14, y=0.99)
fig.tight_layout(rect=[0, 0, 1, 0.96])

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_polarization_baz.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
