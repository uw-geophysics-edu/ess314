"""
fig_delay_time_method.py

Scientific content:
    The delay-time method for mapping an irregular refractor. Shows
    (a) the cross-section with undulating V1-V2 boundary, forward and
    reverse ray paths, and depth h_G at each geophone; (b) the tangent-arc
    construction in which circular arcs of radius h_G are drawn beneath
    each geophone and their common tangent reconstructs the refractor surface.

Reproduces the scientific content of:
    Telford, W.M., Geldart, L.P. & Sheriff, R.E. (1990). Applied Geophysics,
    2nd ed. Cambridge University Press. §4.4.3 concept.
    (No direct reproduction — original Python generation.)

Output: assets/figures/fig_delay_time_method.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Global rcParams (MANDATORY) ──────────────────────────────────────
mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# Palette
C_LAYER1  = "#56B4E9"
C_LAYER2  = "#D55E00"
C_FWD_RAY = "#0072B2"
C_REV_RAY = "#E69F00"
C_ARC_FWD = "#0072B2"
C_ARC_REV = "#E69F00"
C_REFRACT = "#009E73"
C_SURFACE = "#000000"

# ── Survey geometry ───────────────────────────────────────────────────
L       = 120.0    # profile length (m)
V1, V2  = 600.0, 2400.0   # m/s
tic     = np.arcsin(V1 / V2)

# Geophone positions (8 geophones evenly spaced)
n_geo  = 8
x_geo  = np.linspace(10, L-10, n_geo)

# Undulating refractor: smooth sinusoidal variation in depth
def refractor_depth(x):
    return 10 + 3.5 * np.sin(2 * np.pi * x / (L * 0.7)) + 1.5 * np.cos(2 * np.pi * x / (L * 0.4))

x_fine  = np.linspace(0, L, 500)
z_fine  = refractor_depth(x_fine)
z_geo   = refractor_depth(x_geo)   # true depth at each geophone

# Source positions
x_fwd_src = 0.0
x_rev_src = L

# For delay-time: each geophone's delay time = h_G * cos(tic) / V1
# In this illustration we use the true depths as "recovered" depths from the method
h_G = z_geo.copy()   # these are the depths the method recovers

# ── Figure ────────────────────────────────────────────────────────────
fig, (ax_top, ax_bot) = plt.subplots(
    2, 1, figsize=(11, 9),
    gridspec_kw={"hspace": 0.60}
)

for ax_idx, ax in enumerate([ax_top, ax_bot]):
    ax.set_xlim(-5, L+5)
    depth_max = np.max(z_fine) + 8
    ax.set_ylim(depth_max, -4)   # depth 0 at top, positive downward

    # ── Fill layers ──
    ax.fill_between(x_fine, np.zeros_like(z_fine), z_fine,
                    facecolor=C_LAYER1, alpha=0.35, zorder=1)
    ax.fill_between(x_fine, z_fine, depth_max,
                    facecolor=C_LAYER2, alpha=0.35, zorder=1)

    # ── Refractor surface ──
    ax.plot(x_fine, z_fine, color=C_REFRACT, lw=2.0, zorder=5, label="Refractor (true)")

    # ── Surface ──
    ax.axhline(0, color=C_SURFACE, lw=1.5, zorder=6)

    # ── Velocity labels ──
    ax.text(L*0.05, 4, f"$V_1$ = {int(V1)} m/s", fontsize=11, color="#1a1a1a",
            va="center")
    ax.text(L*0.05, np.mean(z_fine)+5, f"$V_2$ = {int(V2)} m/s", fontsize=11, color="#1a1a1a")

    # ── Source markers ──
    for xs, lab, col in [(x_fwd_src, "$E_F$", C_FWD_RAY), (x_rev_src, "$E_R$", C_REV_RAY)]:
        ax.plot(xs, 0, "v", ms=10, color=col, zorder=7, clip_on=False)
        ax.text(xs + (3 if "F" in lab else -8), -3, lab, fontsize=11,
                color=col, fontweight="bold")

    # ── Geophone markers ──
    ax.plot(x_geo, np.zeros_like(x_geo), "s", ms=7, color="#333", zorder=7)
    for i, xg in enumerate(x_geo):
        ax.text(xg, -2.5, f"$G_{i+1}$", ha="center", fontsize=9, color="#333")

if ax_idx == 0:  # Top panel: cross-section with ray paths
    pass   # label below

# ── Top panel specifics ───────────────────────────────────────────────
ax = ax_top

# Draw forward ray paths from E_F to each geophone via refractor
for i, (xg, zg) in enumerate(zip(x_geo, z_geo)):
    # Approximate down-going ray: straight line at critical angle
    # x_down = tan(tic) * depth  from source
    x_turn_fwd = x_fwd_src + zg * np.tan(tic)
    # Horizontal propagation along refractor from x_turn_fwd to point near geophone
    x_up_start = xg - zg * np.tan(tic)

    if x_up_start > x_turn_fwd:   # valid geometry
        ax.plot([x_fwd_src, x_turn_fwd, x_up_start, xg],
                [0, zg, zg, 0],
                color=C_FWD_RAY, lw=0.8, alpha=0.55, zorder=4)

    # Vertical dashed line from geophone to refractor
    ax.plot([xg, xg], [0, zg], color="#888", lw=0.7, ls="--", zorder=3)
    # h_G label on every other geophone
    if i % 2 == 0:
        ax.text(xg + 1.5, zg/2, f"$h_{{G_{i+1}}}$", fontsize=9, color="#555", va="center")

# Draw one example reverse ray path
xg_ex, zg_ex = x_geo[-2], z_geo[-2]
x_turn_rev = x_rev_src - zg_ex * np.tan(tic)
x_up_start_rev = xg_ex + zg_ex * np.tan(tic)
if x_up_start_rev < x_turn_rev:
    ax.plot([x_rev_src, x_turn_rev, x_up_start_rev, xg_ex],
            [0, zg_ex, zg_ex, 0],
            color=C_REV_RAY, lw=1.2, alpha=0.75, zorder=4)

ax.set_xlabel("Position along profile (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("(a) Cross-section: ray paths and depths $h_G$ at each geophone", fontweight="bold", fontsize=13)

fwd_patch = mpatches.Patch(color=C_FWD_RAY, alpha=0.7, label="Forward ray (from $E_F$)")
rev_patch = mpatches.Patch(color=C_REV_RAY, alpha=0.7, label="Reverse ray (from $E_R$)")
ref_line  = mpatches.Patch(color=C_REFRACT, label="True refractor")
ax.legend(handles=[fwd_patch, rev_patch, ref_line], loc="lower right", fontsize=10)

# ── Bottom panel specifics: tangent-arc construction ──────────────────
ax = ax_bot

theta_arc = np.linspace(np.pi, 2 * np.pi, 120)   # lower half-circle arcs

for i, (xg, hg) in enumerate(zip(x_geo, h_G)):
    # Forward arc (center at geophone position, radius = h_G from forward delay)
    arc_x_fwd = xg + hg * np.cos(theta_arc)
    arc_y_fwd = 0  + hg * np.sin(theta_arc)   # sin is negative in lower half → positive depth
    ax.plot(arc_x_fwd, arc_y_fwd, color=C_ARC_FWD, lw=1.0, ls="--", alpha=0.65, zorder=4)

    # Reverse arc (slightly different radius to represent different shot-side delay)
    # In reality forward and reverse delay times sum; here use a small asymmetry for illustration
    hg_rev = hg * (1 + 0.05 * np.sin(i))   # small asymmetry
    arc_x_rev = xg + hg_rev * np.cos(theta_arc)
    arc_y_rev = 0  + hg_rev * np.sin(theta_arc)
    ax.plot(arc_x_rev, arc_y_rev, color=C_ARC_REV, lw=1.0, ls=":", alpha=0.65, zorder=4)

    # Mark the tangent point (bottom of each arc ≈ minimum of arc_y_fwd)
    idx_min = np.argmax(arc_y_fwd)   # most positive y = deepest point
    ax.plot(arc_x_fwd[idx_min], arc_y_fwd[idx_min],
            "o", ms=5, color=C_REFRACT, zorder=6)

# The recovered refractor surface (tangent envelope) = true refractor in this ideal case
ax.plot(x_fine, z_fine, color=C_REFRACT, lw=2.5, zorder=5,
        label="Recovered refractor (common tangent)")

ax.set_xlabel("Position along profile (m)")
ax.set_ylabel("Depth (m)")
ax.set_title("(b) Tangent-arc construction: recovered refractor is the envelope of depth arcs",
             fontweight="bold", fontsize=13)

fwd_arc = mpatches.Patch(color=C_ARC_FWD, alpha=0.7, label="Forward delay arcs (dashed blue)")
rev_arc = mpatches.Patch(color=C_ARC_REV, alpha=0.7, label="Reverse delay arcs (dotted orange)")
ref_env = mpatches.Patch(color=C_REFRACT, label="Recovered refractor (tangent)")
ax.legend(handles=[fwd_arc, rev_arc, ref_env], loc="lower right", fontsize=10)

fig.tight_layout()
fig.savefig("assets/figures/fig_delay_time_method.png", dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_delay_time_method.png")

if __name__ == "__main__":
    plt.show()
