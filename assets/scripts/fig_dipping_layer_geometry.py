"""
fig_dipping_layer_geometry.py

Scientific content:
    A dipping reflector at angle delta from horizontal produces an
    asymmetric travel-time curve. Down-dip shooting (receiver in the
    down-dip direction) records MORE moveout than flat-layer NMO;
    up-dip shooting records LESS moveout.

    Exact travel-time equations (source at origin, perpendicular depth h):
        Down-dip:  t_d(x) = sqrt(x^2 + 4hx sin(delta) + 4h^2) / V1
        Up-dip:    t_u(x) = sqrt(x^2 - 4hx sin(delta) + 4h^2) / V1
        Flat:      t_f(x) = sqrt(x^2 + 4h^2) / V1

    Taylor expansion at small x:
        t(x) ≈ t0 ± (sin(delta)/V1)·x + (cos^2(delta)/(2V1^2 t0))·x^2
    The ±(sin(delta)/V1) LINEAR term is absent for flat layers.
    NMO velocity for dipping layer: V_NMO = V1 / cos(delta)

    Panel A: ray-path geometry cartoon showing source, two receivers,
             dipping reflector, and the shifted reflection points.
    Panel B: t(x) for flat, up-dip, and down-dip shooting annotated
             with the linear moveout shift at x = 2400 m.
    Panel C: t^2–x^2 showing the non-linearity caused by the linear
             term in x; curvatures identify V_NMO = V1 / cos(delta).

Reproduces scientific content of:
    Sheriff, R.E. & Geldart, L.P. (1995). Exploration Seismology, 2nd ed.
    Cambridge University Press. Chapter 4, §4.2 (Dipping reflectors).
    Levin, F.K. (1971). Apparent velocity from dipping interface reflections.
    Geophysics, 36(3), 510–516. https://doi.org/10.1190/1.1440188

Output: assets/figures/fig_dipping_layer_geometry.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines

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
GRAY   = "#888888"
BLACK  = "#000000"

# ── Model parameters ─────────────────────────────────────────────────────────
V1    = 2000.0          # m/s
h     = 1000.0          # m  (perpendicular distance from source to reflector)
delta = np.radians(15)  # dip angle (radians)
t0    = 2 * h / V1      # s  zero-offset TWTT (= 1.0 s)

x_arr = np.linspace(0, 3000, 500)  # m

# ── Travel-time curves ────────────────────────────────────────────────────────
t_flat  = np.sqrt(x_arr**2 + 4*h**2) / V1
t_down  = np.sqrt(x_arr**2 + 4*h*x_arr*np.sin(delta) + 4*h**2) / V1
t_up    = np.sqrt(x_arr**2 - 4*h*x_arr*np.sin(delta) + 4*h**2) / V1

# NMO velocity for dipping layer = V1/cos(delta)
V_nmo_dip = V1 / np.cos(delta)

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(17, 6))
gs  = fig.add_gridspec(1, 3, wspace=0.38)
ax_geo  = fig.add_subplot(gs[0, 0])
ax_tx   = fig.add_subplot(gs[0, 1])
ax_t2x2 = fig.add_subplot(gs[0, 2])

# ── Panel A: geometry cartoon ─────────────────────────────────────────────────
ax = ax_geo

# Surface
ax.axhline(0, color=BLACK, lw=2, zorder=3)

# Dipping reflector: passes through (0, h_v) with slope tan(delta)
# h_v = vertical depth below source footprint = h / cos(delta)
h_v = h / np.cos(delta)
x_ref = np.array([-500, 3000])
y_ref = h_v - x_ref * np.tan(delta)   # depth increases down (positive)
ax.plot(x_ref, y_ref, color=GREEN, lw=2.5, label="Dipping reflector")

# Source at x=0
ax.plot(0, 0, marker="*", ms=16, color=RED, zorder=5, label="Source $E$")

# Up-dip receiver (negative x) and down-dip (positive x)
x_up   = -1200
x_down =  1200
ax.plot(x_up,   0, marker="v", ms=12, color=BLUE,   zorder=5, label="Receiver (up-dip)")
ax.plot(x_down, 0, marker="v", ms=12, color=ORANGE, zorder=5, label="Receiver (down-dip)")

# Reflection points on dipping reflector
def refl_point_dip(x_src, x_rcv, h_perp, delta):
    """Image-point method: image of source across reflector."""
    # Image of source at (x_src, 0) across reflector
    # Reflector normal: (sin(delta), cos(delta)) pointing up
    # Perpendicular distance from source to reflector = h_perp
    # Image location:
    xi = x_src - 2*h_perp*np.sin(delta)
    zi = 2*h_perp*np.cos(delta)
    # Reflection point: midpoint on line from image to receiver
    # t = (z_i) / (z_i + 0)... parametric intersection
    # Line from (x_rcv, 0) to (xi, zi): parameterised as P = (x_rcv, 0) + t*((xi - x_rcv), zi)
    # Reflector: y = h_v - x * tan(delta) → cos(delta)*y + sin(delta)*x = h (in perpendicular coords)
    # Simplified: just trace the ray path numerically
    # Reflection point = midpoint between image and receiver at the reflector
    t_param = h_v / (zi - (xi - x_rcv)*np.tan(delta) + h_v)  # approximate
    xp = x_rcv + t_param * (xi - x_rcv)
    yp = h_v - xp * np.tan(delta)
    return xp, yp

# Draw ray paths using perpendicular image-point construction
# Down-dip ray
xp_d = (x_down - 2*h_v*np.sin(delta)**2 + 0) / 2  # approx midpoint
yp_d = h_v - xp_d * np.tan(delta)
# Up-dip ray
xp_u = (x_up + 2*h_v*np.sin(delta)**2) / 2
yp_u = h_v - xp_u * np.tan(delta)

# Simple ray paths: source → reflector ← receiver (drawn heuristically)
xp_d = (x_down * 0.62)
yp_d = h_v - xp_d * np.tan(delta)
xp_u = (x_up * 0.62)
yp_u = h_v - xp_u * np.tan(delta)

ax.plot([0, xp_d, x_down], [0, yp_d, 0], color=ORANGE, lw=1.5, ls="--", alpha=0.9)
ax.plot([0, xp_u, x_up],   [0, yp_u, 0], color=BLUE,   lw=1.5, ls="--", alpha=0.9)

# Flat reflector for reference (dotted)
ax.axhline(h_v, color=GRAY, lw=1.2, ls=":", alpha=0.5, label="Flat reference")
ax.text(2500, h_v + 30, "flat", color=GRAY, fontsize=10, ha="right")

# Reflection point markers
ax.plot(xp_d, yp_d, "o", color=ORANGE, ms=8, zorder=6)
ax.plot(xp_u, yp_u, "o", color=BLUE,   ms=8, zorder=6)

# Dip angle arc
arc_r = 350
theta1 = 270 - np.degrees(delta)
theta2 = 270
wedge = mpatches.Wedge((200, h_v), arc_r, theta1, theta2,
                        color=GREEN, alpha=0.25, zorder=2)
ax.add_patch(wedge)
ax.text(450, h_v + 160, r"$\delta$", fontsize=13, color=GREEN)

# Annotations
ax.annotate("", xy=(x_up,   -80), xytext=(0, -80),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.2))
ax.text(x_up/2, -160, "up-dip $x$", ha="center", fontsize=11, color=BLUE)
ax.annotate("", xy=(x_down,  -80), xytext=(0, -80),
            arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.2))
ax.text(x_down/2, -160, "down-dip $x$", ha="center", fontsize=11, color=ORANGE)

ax.set_xlim(-1600, 3000)
ax.set_ylim(1600, -300)
ax.set_xlabel("Horizontal distance (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("(A) Reflection geometry\ndipping reflector", fontsize=13)
ax.legend(loc="lower left", fontsize=10)
ax.set_xticks([])

# ── Panel B: t(x) travel-time curves ─────────────────────────────────────────
ax = ax_tx
t_ms_flat = t_flat * 1000
t_ms_down = t_down * 1000
t_ms_up   = t_up   * 1000

ax.plot(x_arr, t_ms_flat, color=GRAY,   lw=2.2, ls="--",
        label=f"Flat ($\\delta=0$)")
ax.plot(x_arr, t_ms_down, color=ORANGE, lw=2.5,
        label=f"Down-dip ($\\delta={round(np.degrees(delta))}°$)")
ax.plot(x_arr, t_ms_up,   color=BLUE,   lw=2.5,
        label=f"Up-dip ($\\delta={round(np.degrees(delta))}°$)")

# Annotate linear shift at x=2400 m
xann = 2400
t_d_ann = np.interp(xann, x_arr, t_ms_down)
t_f_ann = np.interp(xann, x_arr, t_ms_flat)
t_u_ann = np.interp(xann, x_arr, t_ms_up)

ax.annotate("", xy=(xann, t_d_ann), xytext=(xann, t_f_ann),
            arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.4))
ax.text(xann + 60, (t_d_ann + t_f_ann)/2,
        r"$+\frac{x\sin\delta}{V_1}$", fontsize=11, color=ORANGE, va="center")

ax.annotate("", xy=(xann, t_u_ann), xytext=(xann, t_f_ann),
            arrowprops=dict(arrowstyle="<->", color=BLUE, lw=1.4))
ax.text(xann + 60, (t_u_ann + t_f_ann)/2,
        r"$-\frac{x\sin\delta}{V_1}$", fontsize=11, color=BLUE, va="center")

# Parameter box
ax.text(0.98, 0.97,
        f"$V_1={V1:.0f}$ m/s\n$h={h:.0f}$ m\n"
        f"$t_0={t0:.2f}$ s\n$\\delta={round(np.degrees(delta))}°$",
        transform=ax.transAxes, ha="right", va="top", fontsize=11,
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=GRAY, alpha=0.9))

ax.set_xlim(0, 3000)
ax.set_ylim(2500, 0)
ax.set_xlabel("Offset $x$ (m)")
ax.set_ylabel("Travel time $t$ (ms)")
ax.set_title(r"(B) Asymmetric $t(x)$ curves", fontsize=13)
ax.legend(loc="lower left", fontsize=11)

# ── Panel C: t^2–x^2 showing curvature difference ────────────────────────────
ax = ax_t2x2
x2 = (x_arr / 1000)**2    # km^2

ax.plot(x2, (t_flat**2) * 1e6, color=GRAY,   lw=2.2, ls="--",
        label="Flat")
ax.plot(x2, (t_down**2) * 1e6, color=ORANGE, lw=2.5,
        label="Down-dip")
ax.plot(x2, (t_up**2  ) * 1e6, color=BLUE,   lw=2.5,
        label="Up-dip")

# NMO velocity tangent line at x=0 (slope = 1/V_NMO²)
x2_tan = np.linspace(0, 4, 50)
slope_nmo = 1 / V_nmo_dip**2 * 1e6  # ms² per km²
y_tan = t0**2 * 1e6 + slope_nmo * x2_tan * 1e6  # careful with units
# Recompute: slope in (km^2, ms^2) units:
# y [ms²] = t0^2 * 1e6 [ms²] + (1/V_NMO^2) [s^2/m^2] * x^2 [m^2] * 1e6 [ms^2/s^2]
# = t0^2 * 1e6 + 1e12/V_NMO^2 * x_km^2
slope_km = 1e12 / V_nmo_dip**2   # ms^2 / km^2
y_tan = t0**2 * 1e6 + slope_km * x2_tan
ax.plot(x2_tan, y_tan, color=GREEN, lw=1.8, ls=":",
        label=f"$V_{{NMO}}=V_1/\\cos\\delta={V_nmo_dip:.0f}$ m/s")

ax.set_xlabel("$x^2$ (km$^2$)")
ax.set_ylabel("$t^2$ (ms$^2$)")
ax.set_title(r"(C) $t^2$–$x^2$: non-linearity from dip", fontsize=13)
ax.legend(loc="upper left", fontsize=11)
ax.set_xlim(0, 9)
ax.set_ylim(0, None)

fig.tight_layout()
fig.savefig("assets/figures/fig_dipping_layer_geometry.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_dipping_layer_geometry.png")

if __name__ == "__main__":
    plt.show()
