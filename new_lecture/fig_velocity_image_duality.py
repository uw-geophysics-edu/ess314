"""
fig_velocity_image_duality.py

Scientific content:
  A minimal implementation of Claerbout's kirchslow subroutine (2010,
  §5.2.1) in Python, applied to a toy earth model containing three
  point scatterers and a short dipping segment. The workflow is:

    1. Forward model (diffract): each earth point spreads along a
       hyperbola in (x, t) data space.  Time-domain sum.
    2. Migrate (sum): for each output pixel (x, z), sum data values
       along the hyperbola t(x') = sqrt( (2z/v)^2 + (2(x-x')/v)^2 ).

  Three migrations are performed with the SAME data but different
  migration velocities: correct v, 0.80 v ("too slow"), 1.25 v ("too
  fast"). Correct v collapses each hyperbola back to a focused point;
  wrong v leaves residual curvature — the classic under- or
  over-migrated signature. This panel is the core pedagogical payoff
  of the lecture: the image *is* the velocity diagnostic.

Reproduces the scientific content of:
  Claerbout, J. F. (2010). Basic Earth Imaging. Stanford Exploration
  Project. http://sepwww.stanford.edu/sep/prof/bei11.2010.pdf
  (Chapter 5, Figure 5.8 and subroutine kirchslow, p. 65).

Output: assets/figures/fig_velocity_image_duality.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 12,
    "axes.titlesize": 13,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
    "legend.fontsize": 10,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

# -- Grids -----------------------------------------------------------
v_true = 2.0                              # km/s (half-velocity for exploding reflector)
nx = 161
nz = 121
nt = 241
x = np.linspace(0.0, 4.0, nx)             # km
z = np.linspace(0.0, 2.0, nz)             # km
t = np.linspace(0.0, 2.4, nt)             # s
dx = x[1] - x[0]
dz = z[1] - z[0]
dt = t[1] - t[0]

# -- Earth model: three point scatterers plus a dipping segment -----
earth = np.zeros((nz, nx))

# Point scatterers
scat = [(0.8, 0.5), (2.0, 1.0), (3.0, 0.7)]
for (xc, zc) in scat:
    ix = int(round((xc - x[0])/dx))
    iz = int(round((zc - z[0])/dz))
    earth[iz, ix] = 1.0

# Short dipping segment (from (1.0, 1.3) to (1.8, 1.7))
p1 = np.array([1.0, 1.3]); p2 = np.array([1.8, 1.7])
for s in np.linspace(0, 1, 40):
    pt = (1 - s) * p1 + s * p2
    ix = int(round((pt[0] - x[0])/dx))
    iz = int(round((pt[1] - z[0])/dz))
    if 0 <= ix < nx and 0 <= iz < nz:
        earth[iz, ix] = 1.0

# -- Ricker wavelet for realistic "point" response -------------------
def ricker(t_axis, f0, t_shift=0.0):
    a = (np.pi * f0 * (t_axis - t_shift))**2
    return (1 - 2*a) * np.exp(-a)

f0 = 25.0  # Hz dominant
wav = ricker(np.linspace(-0.06, 0.06, 31), f0)
wav = wav / np.max(np.abs(wav))

# -- Forward modeling: spread each scatterer into a hyperbola -------
# Zero-offset data: d(x', t) = sum over (xc, zc) with earth[zc,xc]>0 of
# a band-limited impulse at t = sqrt((2 zc / v)^2 + (2 (x' - xc)/v)^2)
data = np.zeros((nt, nx))
zc_idx, xc_idx = np.nonzero(earth)
for iz_c, ix_c in zip(zc_idx, xc_idx):
    zc = z[iz_c]; xc = x[ix_c]
    amp = earth[iz_c, ix_c]
    # Apparent time at each midpoint x':
    t_of_x = np.sqrt((2*zc/v_true)**2 + (2*(x - xc)/v_true)**2)
    it_of_x = np.round((t_of_x - t[0])/dt).astype(int)
    for j, it0 in enumerate(it_of_x):
        # Place wavelet centered at it0
        i1 = it0 - len(wav)//2
        i2 = i1 + len(wav)
        if i1 < 0 or i2 > nt:
            continue
        # 1/sqrt(t) amplitude compensation (simplified Kirchhoff)
        if t_of_x[j] > 1e-6:
            scale = amp / np.sqrt(t_of_x[j])
        else:
            scale = amp
        data[i1:i2, j] += wav * scale

# Normalize data for display
dmax = np.max(np.abs(data))
if dmax > 0:
    data = data / dmax

# -- Kirchhoff migration (Claerbout's kirchslow adjoint) -------------
# For each output pixel (ix, iz), sum data along the hyperbola
# t_mig(x') = sqrt((2 z[iz] / v)^2 + (2 (x[ix] - x')/v)^2)
# over all x' (midpoints).
def kirchhoff_migrate(data, x, z, t, v_mig, aperture_km=1.2):
    nt, nx = data.shape
    nz = len(z)
    dt = t[1] - t[0]
    dx = x[1] - x[0]
    n_ap = int(round(aperture_km / dx))
    mig = np.zeros((nz, nx))
    for iz, zz in enumerate(z):
        two_z_over_v = 2.0 * zz / v_mig
        for ix, xx in enumerate(x):
            # aperture window
            i_lo = max(0, ix - n_ap)
            i_hi = min(nx, ix + n_ap + 1)
            x_ap = x[i_lo:i_hi]
            t_ap = np.sqrt(two_z_over_v**2 + (2*(xx - x_ap)/v_mig)**2)
            it_ap = np.round((t_ap - t[0])/dt).astype(int)
            valid = (it_ap >= 0) & (it_ap < nt)
            if not np.any(valid):
                continue
            # Sum
            mig[iz, ix] = np.sum(data[it_ap[valid], np.arange(i_lo, i_hi)[valid]])
    return mig

# Three migrations
print("Migrating with correct velocity...")
img_correct = kirchhoff_migrate(data, x, z, t, v_true)
print("Migrating with v too slow (0.80 v)...")
img_slow = kirchhoff_migrate(data, x, z, t, 0.80 * v_true)
print("Migrating with v too fast (1.25 v)...")
img_fast = kirchhoff_migrate(data, x, z, t, 1.25 * v_true)

# Normalize each image to own max for consistent display
def norm(a):
    m = np.max(np.abs(a))
    return a / m if m > 0 else a

img_correct_n = norm(img_correct)
img_slow_n = norm(img_slow)
img_fast_n = norm(img_fast)

# -- Figure ----------------------------------------------------------
fig, axs = plt.subplots(2, 2, figsize=(13, 9.5),
                        gridspec_kw={"hspace": 0.42, "wspace": 0.24})

# (a) Zero-offset data
ax = axs[0, 0]
im = ax.imshow(data, extent=[x[0], x[-1], t[-1]*1000, t[0]*1000],
               aspect="auto", cmap="gray_r", vmin=-0.6, vmax=0.6)
ax.set_xlabel("x, midpoint (km)")
ax.set_ylabel("t, two-way time (ms)")
ax.set_title("(a) Zero-offset data: diffraction hyperbolas\n(three point scatterers + dipping segment)")
ax.grid(alpha=0.2, color="#888888")

# (b) Correct migration
ax = axs[0, 1]
im = ax.imshow(img_correct_n, extent=[x[0], x[-1], z[-1], z[0]],
               aspect="auto", cmap="gray_r", vmin=-0.6, vmax=0.6)
# Overlay true scatterer positions as markers
for (xc, zc) in scat:
    ax.plot(xc, zc, marker="+", markersize=12, color="#D55E00",
            markeredgewidth=2.2)
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#009E73", lw=2.0, alpha=0.75)
ax.set_xlabel("x (km)")
ax.set_ylabel("z, depth (km)")
ax.set_title(f"(b) Migration with CORRECT v = {v_true:.1f} km/s\n"
             "hyperbolas collapse to focused points")
ax.grid(alpha=0.2, color="#888888")

# (c) Too-slow migration
ax = axs[1, 0]
im = ax.imshow(img_slow_n, extent=[x[0], x[-1], z[-1], z[0]],
               aspect="auto", cmap="gray_r", vmin=-0.6, vmax=0.6)
for (xc, zc) in scat:
    ax.plot(xc, zc, marker="+", markersize=12, color="#D55E00",
            markeredgewidth=2.2)
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#009E73", lw=2.0, alpha=0.75)
ax.set_xlabel("x (km)")
ax.set_ylabel("z, depth (km)")
ax.set_title(f"(c) Migration with v TOO SLOW (0.80 × v = {0.80*v_true:.2f} km/s)\n"
             "under-migrated: hyperbola residuals frown")
ax.grid(alpha=0.2, color="#888888")

# (d) Too-fast migration
ax = axs[1, 1]
im = ax.imshow(img_fast_n, extent=[x[0], x[-1], z[-1], z[0]],
               aspect="auto", cmap="gray_r", vmin=-0.6, vmax=0.6)
for (xc, zc) in scat:
    ax.plot(xc, zc, marker="+", markersize=12, color="#D55E00",
            markeredgewidth=2.2)
ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color="#009E73", lw=2.0, alpha=0.75)
ax.set_xlabel("x (km)")
ax.set_ylabel("z, depth (km)")
ax.set_title(f"(d) Migration with v TOO FAST (1.25 × v = {1.25*v_true:.2f} km/s)\n"
             "over-migrated: residuals smile")
ax.grid(alpha=0.2, color="#888888")

fig.suptitle("The image IS the velocity diagnostic",
             fontsize=15, y=0.995, fontweight="bold")
fig.savefig("/tmp/lec16/assets/figures/fig_velocity_image_duality.png",
            bbox_inches="tight", dpi=300)
plt.close(fig)
print("Saved fig_velocity_image_duality.png")
