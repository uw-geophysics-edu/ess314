"""
fig_sp_time_distance.py

Scientific content: The S-minus-P time at a single station is a linear
function of hypocentral distance for a given pair of P- and S-wave
velocities. This is the foundation of single-station distance estimation:
read the S-P time from a seismogram, and a known crustal velocity model
turns it into a hypocentral distance. The slope of the line is the
S-minus-P slowness, (1/V_S - 1/V_P), in s/km.

Reproduces the scientific content of:
  Lowrie & Fichtner (2020), Fundamentals of Geophysics, 3rd ed., Ch. 5
  (earthquake location). Standard textbook derivation, no figures
  reproduced.

Output: assets/figures/fig_sp_time_distance.png
License: CC-BY 4.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 130, "savefig.dpi": 200,
})

# Three crustal velocity scenarios (V_P, V_S in km/s)
scenarios = [
    ("Sedimentary basin\n($V_P=3.0,\\ V_S=1.7$)", 3.0, 1.7, "#0072B2", "-"),
    ("Average crust\n($V_P=6.0,\\ V_S=3.46$)",   6.0, 3.46, "#E69F00", "--"),
    ("Lower crust\n($V_P=7.0,\\ V_S=4.0$)",       7.0, 4.0, "#009E73", "-."),
]

r = np.linspace(0, 200, 400)

fig, ax = plt.subplots(figsize=(10, 6))

for label, vp, vs, color, ls in scenarios:
    sp_time = r * (1 / vs - 1 / vp)
    slope = (1 / vs - 1 / vp)
    ax.plot(r, sp_time, color=color, lw=2.2, ls=ls,
            label=f"{label}\nslope = {slope:.3f} s/km")

# Reference: Omori-style "rule of 8" for average crust — distance in km is
# approximately 8 × (S-P time in seconds)
ax.text(168, 30, "Rule of thumb\n(avg. crust):\n$r \\approx 8\\, (T_S{-}T_P)$",
        ha="center", va="center", fontsize=11.5,
        bbox=dict(facecolor="white", edgecolor="#444444", lw=0.6,
                  boxstyle="round,pad=0.4"))

# Worked-example annotation: a measurement of T_S - T_P = 6 s in average crust
# should imply r ≈ 48 km
ex_t = 6.0
ex_r = ex_t / (1 / 3.46 - 1 / 6.0)
ax.plot([ex_r, ex_r], [0, ex_t], color="#444444", ls=":", lw=1.0)
ax.plot([0, ex_r], [ex_t, ex_t], color="#444444", ls=":", lw=1.0)
ax.plot(ex_r, ex_t, marker="o", color="#D55E00", ms=10, mec="#000",
        mew=0.8, zorder=5)
ax.annotate(f"Worked example:\n"
            f"measure $T_S - T_P = {ex_t:.0f}$ s\n"
            f"→ $r \\approx {ex_r:.0f}$ km",
            xy=(ex_r, ex_t), xytext=(ex_r + 18, ex_t - 8),
            fontsize=11.5,
            arrowprops=dict(arrowstyle="->", color="#D55E00", lw=1.0),
            bbox=dict(facecolor="white", edgecolor="#D55E00", lw=0.8,
                      boxstyle="round,pad=0.35"))

# Cosmetics
ax.set_xlabel("Hypocentral distance $r$ (km)")
ax.set_ylabel("Observed $T_S - T_P$ (s)")
ax.set_title("S-minus-P time depends linearly on hypocentral distance",
             fontsize=14, pad=8)
ax.set_xlim(0, 200)
ax.set_ylim(0, 50)
ax.grid(True, color="#DDDDDD", lw=0.6)
ax.legend(loc="upper left", framealpha=0.95)

# Equation banner along the top of the plot
eqn = (r"$T_S - T_P \;=\; r \left(\dfrac{1}{V_S} - \dfrac{1}{V_P}\right)"
       r" \;\Longrightarrow\; r \;=\; \dfrac{V_P V_S}{V_P - V_S}\,(T_S - T_P)$")
fig.text(0.5, 0.965, eqn, ha="center", va="top", fontsize=13.5,
         bbox=dict(facecolor="#F4F4F4", edgecolor="#888888", lw=0.6,
                   boxstyle="round,pad=0.4"))

fig.tight_layout(rect=[0, 0, 1, 0.92])

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_sp_time_distance.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
