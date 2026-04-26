"""
fig_focal_depth_methods.py

Scientific content: Two complementary methods for resolving earthquake
focal depth.

(a) Local-distance geometry: when a station is close enough that the
    propagation path is essentially straight, the hypocentral distance D
    and the epicentral distance Δ form a right triangle whose vertical leg
    is the focal depth h, giving h = √(D² − Δ²).

(b) Teleseismic depth phases: at large epicentral distances, the direct P
    phase and the depth phase pP (which leaves the source upward, reflects
    once at the free surface above the source, and then travels to the
    station) arrive separated by a time that depends almost entirely on
    the focal depth.

Reproduces the scientific content of:
  Stein & Wysession (2003), Ch. 5 (focal depth determination).
  Lowrie & Fichtner (2020), Ch. 4–5 (depth phases).

Output: assets/figures/fig_focal_depth_methods.png
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

C_DIRECT = "#0072B2"
C_PP = "#E69F00"
C_FOCUS = "#D55E00"
C_STA = "#009E73"
C_FAULT = "#000000"
C_GROUND = "#F0E5D0"

fig = plt.figure(figsize=(14, 7.0))
gs = fig.add_gridspec(2, 2, height_ratios=[3.5, 1.0],
                      width_ratios=[1.0, 1.55],
                      hspace=0.45, wspace=0.18)
ax_a = fig.add_subplot(gs[0, 0])
ax_b = fig.add_subplot(gs[0, 1])
ax_seis = fig.add_subplot(gs[1, 1])

# ── Panel (a): local geometry triangle ─────────────────────────────────
ax = ax_a
xmin, xmax = -3, 18
ymin, ymax = 0, 13
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymax, ymin)
ax.set_aspect("equal")
ax.set_xlabel("Horizontal distance (km)")
ax.set_ylabel("Depth (km)\n[positive down]", fontsize=11)
ax.set_yticks([0, 4, 8, 12])

ax.axhspan(0, ymax, color=C_GROUND, zorder=0)
ax.axhline(0, color=C_FAULT, lw=1.4, zorder=2)

epi = np.array([0.0, 0.0])
sta = np.array([13.0, 0.0])
focus = np.array([0.0, 8.0])

ax.plot([epi[0], sta[0]], [epi[1], sta[1]], color=C_FAULT, lw=2.2, zorder=4)
ax.plot([epi[0], focus[0]], [epi[1], focus[1]], color=C_FAULT, lw=2.2, zorder=4)
ax.plot([focus[0], sta[0]], [focus[1], sta[1]], color=C_DIRECT, lw=2.6,
        zorder=4)

# Right-angle marker
ax.plot([0.55, 0.55, 0.0], [0.55, 0.0, 0.55], color=C_FAULT, lw=1.0,
        zorder=4)

ax.plot(focus[0], focus[1], marker="*", color=C_FOCUS, ms=20, mec="#000",
        mew=0.8, zorder=6, label="Focus")
ax.plot(epi[0], epi[1], marker="o", mec="#000", mfc="white", ms=12, mew=1.2,
        zorder=6, label="Epicenter")
ax.plot(sta[0], sta[1], marker="^", color=C_STA, ms=15, mec="#000", mew=1.0,
        zorder=6, label="Station")

ax.text(sta[0] / 2, 0.65, r"$\Delta$  (epicentral distance)",
        ha="center", va="top", fontsize=12, fontweight="bold")
ax.text(-0.55, focus[1] / 2, r"$h$  (focal depth)", ha="right",
        va="center", fontsize=12, fontweight="bold", rotation=90)
# Place D label as a non-rotated tag adjacent to the hypotenuse midpoint,
# offset to the right where there is room
mid = (focus + sta) / 2
ax.text(mid[0] + 0.6, mid[1] + 0.5, "$D$  (hypocentral\ndistance)",
        ha="left", va="top", fontsize=11.5, fontweight="bold",
        color="#005a8a",
        bbox=dict(facecolor="white", edgecolor="#005a8a", lw=0.6,
                  boxstyle="round,pad=0.25"))

# Pythagorean equation: place at upper-right corner with ample margin
ax.text(15.7, 1.5, r"$h \;=\; \sqrt{D^{2} - \Delta^{2}}$",
        ha="right", va="top", fontsize=14,
        bbox=dict(facecolor="white", edgecolor=C_FAULT, lw=0.8,
                  boxstyle="round,pad=0.4"))

ax.legend(loc="lower left", framealpha=0.95)
ax.set_title("(a) Local geometry: depth from the right triangle",
             fontsize=13, pad=8)

# ── Panel (b): teleseismic depth phase ─────────────────────────────────
ax = ax_b
xmin, xmax = -50, 1200
ymin, ymax = -40, 600
ax.set_xlim(xmin, xmax)
ax.set_ylim(ymax, ymin)
ax.set_aspect("auto")
ax.set_xlabel("Epicentral distance  (km — schematic, not to scale)")
ax.set_ylabel("Depth (km)\n[positive down]", fontsize=11)

xs = np.linspace(xmin, xmax, 200)
surface = -25 * np.cos(np.linspace(0, np.pi / 3, 200)) + 25
ax.fill_between(xs, surface, ymax, color=C_GROUND, zorder=0)
ax.plot(xs, surface, color=C_FAULT, lw=1.5, zorder=2)

src = np.array([0.0, 200.0])
sta = np.array([1100.0, surface[-1] + 5])


def curved_ray(p0, p1, sag=0.5, n=120):
    t = np.linspace(0, 1, n)
    x = p0[0] + (p1[0] - p0[0]) * t
    y = p0[1] + (p1[1] - p0[1]) * t
    span = p1[0] - p0[0]
    y = y + sag * (span / 4) * np.sin(np.pi * t)
    return x, y


xp, yp = curved_ray(src, sta, sag=0.6)
ax.plot(xp, yp, color=C_DIRECT, lw=2.4, zorder=4, label="Direct P")

# pP: nearly vertical up-going leg, then long arc to station
reflect_x = 25.0
reflect_y = -25 * np.cos(np.pi / 3 * (reflect_x - xmin) / (xmax - xmin)) + 25
reflect = np.array([reflect_x, reflect_y])

ax.plot([src[0], reflect[0]], [src[1], reflect[1]], color=C_PP, lw=2.4,
        zorder=4, label="pP (depth phase)")
xpp, ypp = curved_ray(reflect, sta, sag=0.6)
ax.plot(xpp, ypp, color=C_PP, lw=2.4, zorder=4)

ax.plot(reflect[0], reflect[1], marker="o", mfc="white", mec=C_PP, mew=1.6,
        ms=10, zorder=5)

ax.plot(src[0], src[1], marker="*", color=C_FOCUS, ms=20, mec="#000",
        mew=0.8, zorder=6, label="Focus")
ax.plot(0, surface[0], marker="o", mec="#000", mfc="white", ms=12, mew=1.2,
        zorder=6)
ax.plot(sta[0], sta[1], marker="^", color=C_STA, ms=14, mec="#000", mew=1.0,
        zorder=6, label="Station")

ax.annotate("Free-surface\nreflection",
            xy=(reflect[0], reflect[1]),
            xytext=(170, 105),
            fontsize=11, color=C_PP,
            arrowprops=dict(arrowstyle="->", color=C_PP, lw=1.0),
            bbox=dict(facecolor="white", edgecolor=C_PP, lw=0.6,
                      boxstyle="round,pad=0.25"))

ax.legend(loc="lower right", framealpha=0.95, fontsize=10)
ax.set_title(r"(b) Teleseismic depth phase: $t_{pP} - t_P\,\to\,$focal depth",
             fontsize=13, pad=8)

# ── Bottom-right: synthetic seismogram strip ───────────────────────────
ax = ax_seis
t_in = np.linspace(0, 60, 1500)


def pulse(t, t0, w=1.5):
    arg = ((t - t0) / w) ** 2
    return (1 - 2 * arg) * np.exp(-arg)


sig = 1.0 * pulse(t_in, 12) + 0.65 * pulse(t_in, 30)
ax.plot(t_in, sig, color="#1A1A1A", lw=1.0)
ax.axvline(12, color=C_DIRECT, lw=1.6)
ax.axvline(30, color=C_PP, lw=1.6, ls=(0, (5, 2)))
ax.annotate("", xy=(30, -0.95), xytext=(12, -0.95),
            arrowprops=dict(arrowstyle="<->", color="#444", lw=1.4))
ax.text(21, -1.10, r"$t_{pP} - t_P$", ha="center", va="top",
        fontsize=12, color="#222")
ax.text(12, 1.30, "P", ha="center", color=C_DIRECT, fontsize=12,
        fontweight="bold")
ax.text(30, 1.30, "pP", ha="center", color=C_PP, fontsize=12,
        fontweight="bold")
ax.set_xlim(0, 60)
ax.set_ylim(-1.6, 1.7)
ax.set_yticks([])
ax.set_xlabel("Time at station (s)")
ax.set_title("Differential time at station → focal depth",
             fontsize=11, pad=4)
ax.grid(False)

fig.suptitle("Resolving earthquake focal depth: two complementary methods",
             fontsize=15, y=1.00)
fig.tight_layout(rect=[0, 0, 1, 0.96])

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_focal_depth_methods.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
