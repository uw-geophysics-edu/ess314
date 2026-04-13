"""
fig_avo_classes.py

Scientific content:
    The amplitude-versus-offset (AVO) response of a reflection is described
    at oblique incidence by the Shuey (1985) two-term approximation:

        R(theta) = R(0) + G * sin^2(theta)

    where:
      R(0) = (Delta Z) / (2 Z_avg)  is the normal-incidence intercept
      G = AVO gradient — sensitive to Delta(Vp/Vs) and fluid content

    AVO classes are defined by the signs of R(0) and G:
      Class I  : R(0) > 0,  G < 0   (hard sand, amplitude dims with offset)
      Class II : R(0) ~ 0,  G < 0   (transition; polarity reversal possible)
      Class IIp: R(0) > 0,  G > 0   (rare; both positive)
      Class III: R(0) < 0,  G < 0   (gas sand; bright, amplitude grows with offset)
      Class IV : R(0) < 0,  G > 0   (soft sand; bright spot, dims with offset)

    Gas sands generally show more negative G relative to wet sands (the
    "fluid substitution effect" on Vp/Vs ratio; Gassmann equations).

    Panel A: R(theta) vs theta (0–40°) for the five AVO classes.
    Panel B: R(0)–G crossplot with background trend and labelled regions.

Reproduces scientific content of:
    Shuey, R.T. (1985). A simplification of the Zoeppritz equations.
    Geophysics, 50(4), 609–614. https://doi.org/10.1190/1.1441936
    Rutherford, S.R. & Williams, R.H. (1989). Amplitude-versus-offset
    variations in gas sands. Geophysics, 54(6), 680–688.
    https://doi.org/10.1190/1.1442696
    Castagna, J.P. & Swan, H.W. (1997). Principles of AVO crossplotting.
    The Leading Edge, 16(4), 337–344. https://doi.org/10.1190/1.1437626

Output: assets/figures/fig_avo_classes.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

BLUE   = "#0072B2"
ORANGE = "#E69F00"
GREEN  = "#009E73"
RED    = "#D55E00"
PINK   = "#CC79A7"
GRAY   = "#888888"
BLACK  = "#000000"

# ── AVO classes: (R0, G, label, color, linestyle) ─────────────────────────────
avo_classes = [
    {"R0":  0.12,  "G": -0.14, "label": "Class I  ($R_0>0$, $G<0$)\ntight/cemented sand",
     "color": BLUE,   "ls": "-"},
    {"R0":  0.03,  "G": -0.11, "label": "Class II ($R_0\\approx 0$, $G<0$)\nnear-critical gas sand",
     "color": ORANGE, "ls": "-"},
    {"R0": -0.09,  "G": -0.12, "label": "Class III ($R_0<0$, $G<0$)\nsoft gas sand (\"bright spot\")",
     "color": RED,    "ls": "-"},
    {"R0": -0.06,  "G":  0.07, "label": "Class IV ($R_0<0$, $G>0$)\nunusual soft sand",
     "color": GREEN,  "ls": "-"},
    {"R0":  0.06,  "G":  0.04, "label": "Class IIp ($R_0>0$, $G>0$)\nbrine sand (rare)",
     "color": PINK,   "ls": "--"},
]

theta_deg = np.linspace(0, 40, 200)
theta_rad = np.radians(theta_deg)

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(15, 7),
                          gridspec_kw={"wspace": 0.40})
ax_r, ax_xp = axes

# ── Panel A: R(theta) vs theta ────────────────────────────────────────────────
for c in avo_classes:
    R_theta = c["R0"] + c["G"] * np.sin(theta_rad)**2
    ax_r.plot(theta_deg, R_theta, color=c["color"], lw=2.5, ls=c["ls"],
              label=c["label"])

ax_r.axhline(0, color=GRAY, lw=1.0, ls=":")
ax_r.axvline(0, color=GRAY, lw=1.0, ls=":", alpha=0.4)

# Shading to show which classes increase vs decrease
ax_r.set_xlabel(r"Incidence angle $\theta$ (°)")
ax_r.set_ylabel(r"Reflection coefficient $R(\theta)$")
ax_r.set_title("(A) AVO response: $R(\\theta) \\approx R(0) + G\\sin^2\\theta$", fontsize=13)
ax_r.legend(loc="lower left", fontsize=10)
ax_r.set_xlim(0, 40)

# ── Panel B: R(0)–G crossplot ─────────────────────────────────────────────────
# Background "wet sand / shale" trend: G ≈ -R0 (the "fluid line")
R0_bg = np.linspace(-0.25, 0.25, 100)
G_bg  = -R0_bg * 0.80     # approximate background trend
ax_xp.plot(R0_bg, G_bg, color=GRAY, lw=1.8, ls="--",
           label="Background trend\n(wet sand / shale)")

# Scatter clusters for each class
rng = np.random.default_rng(17)
for c in avo_classes:
    n_pt = 12
    R0_cl = c["R0"] + rng.standard_normal(n_pt) * 0.012
    G_cl  = c["G"]  + rng.standard_normal(n_pt) * 0.012
    ax_xp.scatter(R0_cl, G_cl, color=c["color"], s=55, alpha=0.75, zorder=4)
    # Centre point labelled
    ax_xp.scatter([c["R0"]], [c["G"]], color=c["color"], s=130, zorder=5,
                  edgecolors="white", linewidths=0.8)
    # Label offset to avoid overlap
    offset = {"Class I": (0.01, -0.015), "Class II": (-0.005, 0.018),
              "Class III": (-0.005, -0.020), "Class IV": (0.01, 0.014),
              "Class IIp": (0.010, 0.010)}
    key = c["label"].split(" ")[1].rstrip("(")   # e.g. "I" or "III"
    full_key = f"Class {key}"
    dx2, dy2 = offset.get(full_key, (0.01, 0.01))
    ax_xp.text(c["R0"] + dx2, c["G"] + dy2,
               f"Class {key}", color=c["color"], fontsize=11,
               fontweight="bold")

# Quadrant labels
ax_xp.axhline(0, color=GRAY, lw=1.0, ls=":")
ax_xp.axvline(0, color=GRAY, lw=1.0, ls=":")

for (x, y, txt) in [
    ( 0.17, -0.18, "$R_0>0$, $G<0$\n(Class I)"),
    (-0.18, -0.18, "$R_0<0$, $G<0$\n(Class III)"),
    (-0.18,  0.10, "$R_0<0$, $G>0$\n(Class IV)"),
    ( 0.12,  0.10, "$R_0>0$, $G>0$\n(Class IIp)"),
]:
    ax_xp.text(x, y, txt, ha="center", va="center",
               fontsize=11, color=GRAY, alpha=0.6)

ax_xp.set_xlabel("Intercept $R(0)$")
ax_xp.set_ylabel("Gradient $G$")
ax_xp.set_title("(B) AVO crossplot $R(0)$ vs $G$\n(gas sands deviate from background trend)",
                fontsize=13)
ax_xp.legend(loc="upper right", fontsize=10)
ax_xp.set_xlim(-0.25, 0.25)
ax_xp.set_ylim(-0.25, 0.20)

fig.tight_layout()
fig.savefig("assets/figures/fig_avo_classes.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_avo_classes.png")

if __name__ == "__main__":
    plt.show()
