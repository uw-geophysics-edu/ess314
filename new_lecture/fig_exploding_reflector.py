"""
fig_exploding_reflector.py

Scientific content:
  Two-panel comparison of (left) real zero-offset acquisition, where
  each of many collocated source-receiver pairs sends a wave down,
  has it reflect, and records the return; and (right) the thought
  experiment where the reflector itself "explodes" at t=0 and waves
  propagate only upward to a surface array. The wavefronts at the
  surface are kinematically identical in both cases IF we halve the
  velocity in the exploding-reflector case (because there is no
  down-and-back trip, only an up trip). This is Claerbout's "powerful
  analogy" (§5.1.4) and the conceptual basis for every modern
  migration algorithm.

Reproduces the scientific content of:
  Claerbout, J. F. (2010). Basic Earth Imaging. Stanford Exploration
  Project. http://sepwww.stanford.edu/sep/prof/bei11.2010.pdf
  (Chapter 5, Figure 5.3).

Output: assets/figures/fig_exploding_reflector.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

C_BLUE = "#0072B2"; C_ORANGE = "#E69F00"; C_SKY = "#56B4E9"
C_GREEN = "#009E73"; C_VERM = "#D55E00"; C_PINK = "#CC79A7"; C_BLACK = "#000000"

# -- Geometry --------------------------------------------------------
# A dipping reflector; several source-receiver pairs at the surface
theta_deg = 20.0
theta = np.deg2rad(theta_deg)
# Reflector passes through (x0,z0) with dip theta
x0, z0 = 1.5, 1.0
# Reflector line
s = np.linspace(-1.4, 1.4, 200)
refl_x = x0 + s * np.cos(theta)
refl_z = z0 + s * np.sin(theta)

# Source-receiver positions
sx = np.array([0.6, 1.2, 1.8, 2.4])
# For each, normal ray hits reflector orthogonally
# Normal direction to reflector (pointing up-and-back-toward-surface):
# reflector unit tangent: (cos theta, sin theta); normal = (-sin theta, cos theta)
# The normal ray from surface goes in direction (sin theta, -cos theta) (down and to the right? no — down and away from dip up direction)
# Actually, downgoing normal is (sin theta, cos theta). Wait — reflector dips to the right (z increases with x),
# normal to reflector pointing upward (out of earth, toward surface) is (-sin theta, -cos theta) in (x,z) with z downward.
# So from a surface point (sx, 0), the normal ray going DOWN to the reflector moves in +z and +x (into the dip):
# direction (sin theta, cos theta). Find intersection with reflector line.
# Reflector line: (x - x0) sin theta - (z - z0) cos theta = 0  (any point on line satisfies this)
# Wait, let's parameterize properly. Line through (x0,z0) with tangent (cos theta, sin theta):
# points: (x0 + s cos theta, z0 + s sin theta)
# Surface point plus t*(normal direction): (sx + t sin theta, 0 + t cos theta)
# Set equal: sx + t sin theta = x0 + s cos theta; t cos theta = z0 + s sin theta
# Solve for t (= normal ray length d):
# From second: s = (t cos theta - z0)/sin theta  (if sin theta != 0; else trivial)
# Substitute: sx + t sin theta = x0 + (t cos theta - z0) cos theta / sin theta
# sx + t sin theta - x0 = t cos^2 theta / sin theta - z0 cos theta/sin theta
# Multiply by sin theta: (sx - x0) sin theta + t sin^2 theta = t cos^2 theta - z0 cos theta
# t (sin^2 theta - cos^2 theta) = -z0 cos theta - (sx - x0) sin theta
# t = [z0 cos theta + (sx - x0) sin theta] / (cos^2 theta - sin^2 theta)
# = [z0 cos theta + (sx - x0) sin theta] / cos(2 theta)
# Sanity: theta small, t approx z0.
ds = np.array([
    (z0 * np.cos(theta) + (s_ - x0) * np.sin(theta)) / np.cos(2*theta)
    for s_ in sx
])
# Reflection points R_i
Rx = sx + ds * np.sin(theta)
Rz = ds * np.cos(theta)

fig, (axL, axR) = plt.subplots(
    1, 2, figsize=(13, 5.6),
    gridspec_kw={"width_ratios": [1.0, 1.0], "wspace": 0.22}
)

# === LEFT: real zero-offset acquisition ============================
axL.plot([0, 3.0], [0, 0], color=C_BLACK, lw=1.2)
axL.plot(refl_x, refl_z, color=C_BLUE, lw=2.8, label="Reflector")

# Down-going and up-going rays for each S/R pair
for i, (xs, r_x, r_z, d_i) in enumerate(zip(sx, Rx, Rz, ds)):
    lbl_d = "Normal ray (down + up)" if i == 0 else None
    axL.plot([xs, r_x], [0, r_z], color=C_VERM, lw=1.8, label=lbl_d)
    axL.plot([r_x, xs], [r_z, 0], color=C_VERM, lw=1.8, alpha=0.5)
    # Small arrow heads to indicate direction (down)
    axL.annotate("", xy=(xs + 0.4*(r_x - xs), 0.4*r_z),
                 xytext=(xs + 0.15*(r_x - xs), 0.15*r_z),
                 arrowprops=dict(arrowstyle="->", color=C_VERM, lw=1.5))

# Wavefronts (partial circles around each S centered at (xs,0)) at time t_i = 2*d_i/v
# To show them we pick a common travel time snapshot
v_real = 2.0  # km/s
t_snap = 0.8  # s snapshot
# For each source, wavefront at time t is a circle of radius v*t/2 for zero-offset (down half the time)
# Actually at time t after shot, the outgoing spherical wavefront has radius v*t.
# We illustrate the shape of the outgoing (downgoing) wave at one instant.
t_fronts = [0.45, 0.7]
for t_s in t_fronts:
    r_front = v_real * t_s
    th = np.linspace(np.pi*1.02, np.pi*1.98, 80)  # downgoing semicircle
    for xs in sx:
        axL.plot(xs + r_front*np.cos(th)*0.0 + r_front*np.sin(th - np.pi*1.5),
                 r_front*(-np.cos(th - np.pi*1.5)), color=C_SKY, lw=0.9, alpha=0.45)
# (Simplified; the overlapping arcs convey "many wavefronts")

# Source/receiver markers
axL.plot(sx, np.zeros_like(sx), marker="v", markersize=14, color=C_ORANGE,
         markeredgecolor=C_BLACK, ls="none", zorder=5,
         label="S = R (each is collocated)")
axL.plot(Rx, Rz, marker="*", markersize=14, color=C_VERM,
         markeredgecolor=C_BLACK, ls="none", zorder=5,
         label="Reflection points")

axL.text(1.5, -0.18, "wave travels DOWN then UP  (velocity v)",
         fontsize=11, ha="center", style="italic")

axL.set_xlim(0, 3.0)
axL.set_ylim(1.8, -0.35)
axL.set_xlabel("x (km)")
axL.set_ylabel("z, depth (km)")
axL.set_title("Reality: zero-offset acquisition\n(thousands of source–receiver pairs)")
axL.set_aspect("equal")
axL.grid(alpha=0.25)
axL.legend(loc="lower left", fontsize=9.5, framealpha=0.95)

# === RIGHT: exploding reflector thought experiment =================
axR.plot([0, 3.0], [0, 0], color=C_BLACK, lw=1.2)
axR.plot(refl_x, refl_z, color=C_BLUE, lw=2.8, label="Reflector at t=0 (explodes)")

# Upgoing wavefronts from points along the reflector at one snapshot time.
# In the exploding-reflector model we use v/2, so at time t_s the radius is (v/2)*t_s.
v_explo = v_real / 2.0
# Seed points along reflector
seed_s = np.linspace(-1.3, 1.3, 12)
seed_x = x0 + seed_s * np.cos(theta)
seed_z = z0 + seed_s * np.sin(theta)

# Upgoing rays (straight up in the isotropic constant-velocity case)
for i, (xs_, zs_) in enumerate(zip(seed_x, seed_z)):
    if zs_ > 0 and zs_ < 1.8:
        axR.plot([xs_, xs_], [zs_, 0], color=C_GREEN, lw=1.2, alpha=0.6)

# A single wavefront snapshot
for t_s in t_fronts:
    r_front = v_explo * t_s
    th = np.linspace(np.pi, 2*np.pi, 80)  # upgoing (z negative → upward)
    for xs_, zs_ in zip(seed_x, seed_z):
        xc = xs_ + r_front*np.cos(th)
        zc = zs_ + r_front*np.sin(th)
        axR.plot(xc, zc, color=C_PINK, lw=0.7, alpha=0.35)

# Receiver array at surface
rec_x = np.linspace(0.2, 2.8, 14)
axR.plot(rec_x, np.zeros_like(rec_x), marker="v", markersize=10, color=C_ORANGE,
         markeredgecolor=C_BLACK, ls="none", zorder=5,
         label="Receiver array (surface)")

axR.text(1.5, -0.18, "waves travel ONLY UP  (velocity v/2)",
         fontsize=11, ha="center", style="italic")

axR.set_xlim(0, 3.0)
axR.set_ylim(1.8, -0.35)
axR.set_xlabel("x (km)")
axR.set_ylabel("z, depth (km)")
axR.set_title("Thought experiment: exploding reflector\n(one hypothetical upgoing wavefield)")
axR.set_aspect("equal")
axR.grid(alpha=0.25)
axR.legend(loc="lower left", fontsize=9.5, framealpha=0.95)

fig.tight_layout()
fig.savefig("/tmp/lec16/assets/figures/fig_exploding_reflector.png",
            bbox_inches="tight", dpi=300)
plt.close(fig)
print("Saved fig_exploding_reflector.png")
