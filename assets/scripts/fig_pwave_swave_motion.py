"""
fig_pwave_swave_motion.py

Scientific content: P-wave (longitudinal) and S-wave (transverse) particle
motions, showing compression/rarefaction for P and transverse displacement
for S. Replaces legacy slide 7–8 from 314_2023_4_seismic_waves.pdf which
used images of unknown provenance (grid animations, Bell Labs photo).

Output: assets/figures/fig_pwave_motion.png
        assets/figures/fig_swave_motion.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# ── Global rcParams (MANDATORY at top of every script) ──────────────
mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# Colorblind-safe palette — WCAG AA compliant
BLUE    = "#0072B2"
ORANGE  = "#E69F00"
SKY     = "#56B4E9"
GREEN   = "#009E73"
VERM    = "#D55E00"
PINK    = "#CC79A7"
BLACK   = "#000000"

def make_pwave_fig():
    """P-wave (compressional / longitudinal) particle motion."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 3.5))
    ax.set_title("P-wave (Compressional / Longitudinal)", fontsize=14, fontweight="bold")

    n_particles = 60
    x_eq = np.linspace(0, 10, n_particles)

    # Sinusoidal displacement in x (longitudinal)
    wavelength = 3.0
    amp = 0.12
    k = 2 * np.pi / wavelength
    displacement = amp * np.sin(k * x_eq)
    x_displaced = x_eq + displacement

    # Color by compression vs rarefaction
    grad = np.gradient(displacement, x_eq)
    colors = [BLUE if g < -0.02 else (SKY if g > 0.02 else "#888888") for g in grad]

    ax.scatter(x_displaced, np.zeros_like(x_displaced), c=colors, s=50, zorder=3, edgecolors="none")

    # Arrows showing particle displacement direction
    arrow_idx = np.arange(5, n_particles, 8)
    for i in arrow_idx:
        dx = displacement[i]
        ax.annotate("", xy=(x_eq[i] + dx * 3, 0.15),
                     xytext=(x_eq[i], 0.15),
                     arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8))

    # Labels for compression and rarefaction zones
    comp_x = x_eq[np.argmin(grad)]
    rare_x = x_eq[np.argmax(grad)]
    ax.text(comp_x, -0.25, "C", ha="center", fontsize=12, fontweight="bold", color=BLUE)
    ax.text(rare_x, -0.25, "R", ha="center", fontsize=12, fontweight="bold", color=SKY)

    # Propagation arrow
    ax.annotate("Propagation direction",
                xy=(9.5, 0.45), xytext=(6.0, 0.45),
                fontsize=11,
                arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.5),
                va="center")

    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.5, 0.7)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("assets/figures/fig_pwave_motion.png")
    plt.close()
    print("Saved: assets/figures/fig_pwave_motion.png")


def make_swave_fig():
    """S-wave (shear / transverse) particle motion."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 3.5))
    ax.set_title("S-wave (Shear / Transverse)", fontsize=14, fontweight="bold")

    n_particles = 60
    x_eq_s = np.linspace(0, 10, n_particles)
    amp_s = 0.35
    wavelength_s = 3.0
    k_s = 2 * np.pi / wavelength_s
    y_displaced = amp_s * np.sin(k_s * x_eq_s)

    # Equilibrium line
    ax.axhline(0, color="#CCCCCC", lw=1, ls="--", zorder=1)

    # Particles
    ax.scatter(x_eq_s, y_displaced, c=VERM, s=50, zorder=3, edgecolors="none")

    # Transverse displacement arrows
    arrow_idx_s = np.arange(3, n_particles, 6)
    for i in arrow_idx_s:
        dy = y_displaced[i]
        if abs(dy) > 0.05:
            ax.annotate("", xy=(x_eq_s[i], dy),
                         xytext=(x_eq_s[i], 0),
                         arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))

    # Propagation arrow
    ax.annotate("Propagation direction",
                xy=(9.5, 0.65), xytext=(6.0, 0.65),
                fontsize=11,
                arrowprops=dict(arrowstyle="-|>", color=BLACK, lw=1.5),
                va="center")

    # Callout box
    bbox_props = dict(boxstyle="round,pad=0.4", fc="#FFF3E0", ec=VERM, lw=1.5)
    ax.text(0.5, -0.55, "S-waves cannot propagate in fluids ($\\mu = 0$)",
            fontsize=11, ha="left", va="center", bbox=bbox_props)

    ax.set_xlim(-0.5, 11)
    ax.set_ylim(-0.85, 0.85)
    ax.set_aspect("equal")
    ax.axis("off")

    plt.tight_layout()
    plt.savefig("assets/figures/fig_swave_motion.png")
    plt.close()
    print("Saved: assets/figures/fig_swave_motion.png")


def main():
    make_pwave_fig()
    make_swave_fig()


if __name__ == "__main__":
    main()
