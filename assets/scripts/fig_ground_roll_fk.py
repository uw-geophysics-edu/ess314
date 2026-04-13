"""
fig_ground_roll_fk.py

Scientific content:
    A shot gather contains several coherent noise types alongside the
    desired reflections:
      - Direct wave:   linear arrival at V_direct ~ V1 = 2000 m/s
      - Ground roll:   fundamental-mode Rayleigh wave, V_gr ~ 300 m/s,
                       dominant frequency 5-15 Hz, high amplitude
      - Head wave:     linear first arrival at V_head > V1 (refracted wave)
      - Reflections:   hyperbolic arrivals at V_rms ~ 2000 m/s

    In the f-k (frequency-wavenumber) domain, events with different
    apparent velocities V = f/k separate into distinct fan-shaped regions.
    A velocity filter (f-k filter) rejects all wavenumbers above a
    threshold V_cutoff (here V_cutoff = 600 m/s), attenuating ground roll
    while preserving reflections.

    Panel A: raw shot gather with labelled noise types.
    Panel B: 2D amplitude spectrum |F(f,k)| with velocity fan lines.
    Panel C: filtered gather after f-k ground-roll rejection.

Reproduces scientific content of:
    Yilmaz, O. (2001). Seismic Data Analysis, 2nd ed. SEG. Vol. 1, §1.4.
    Tellier, N. & Landro, M. (2018). Ground-roll attenuation using radial
    trace filtering. Geophysics, 83(1), V1–V12. doi:10.1190/geo2016-0683.1

Output: assets/figures/fig_ground_roll_fk.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.signal import fftconvolve

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

rng = np.random.default_rng(99)

# ── Survey parameters ─────────────────────────────────────────────────────────
dt      = 0.004      # s
nt      = 251        # 0 – 1.0 s
t_full  = np.arange(nt) * dt
n_tr    = 48
dx      = 25.0       # m trace spacing
offsets = np.arange(1, n_tr+1) * dx    # 25 – 1200 m

V1      = 2000.0     # m/s direct / refraction velocity
V_gr    = 300.0      # m/s ground-roll phase velocity
V_ref   = 2000.0     # m/s NMO velocity of reflection
t0_ref  = 0.55       # s  reflection zero-offset time
V_cutoff = 600.0     # m/s f-k filter cutoff

def ricker(f0, dt, t_half=0.12):
    tw = np.arange(-t_half, t_half, dt)
    u  = (np.pi * f0 * tw)**2
    return (1 - 2*u) * np.exp(-u)

wav_hi  = ricker(40.0, dt)   # high-frequency wavelet for direct + reflection
wav_lo  = ricker(10.0, dt)   # low-frequency wavelet for ground roll

def build_gather():
    data = np.zeros((nt, n_tr))
    for ix, x in enumerate(offsets):
        spike = np.zeros(nt)
        # Direct wave
        idx_d = int(round(x / V1 / dt))
        if idx_d < nt:
            spike[idx_d] += 0.6
        # Reflection (hyperbolic)
        tx  = np.sqrt(t0_ref**2 + x**2/V_ref**2)
        idx_r = int(round(tx / dt))
        if idx_r < nt:
            spike[idx_r] += 0.5

        trace = fftconvolve(spike, wav_hi, mode="same")

        # Ground roll: low-frequency, high amplitude, linear moveout
        spike_gr = np.zeros(nt)
        idx_gr = int(round(x / V_gr / dt))
        if idx_gr < nt:
            spike_gr[idx_gr] += 3.0    # ~5× the reflection amplitude
        trace += fftconvolve(spike_gr, wav_lo, mode="same")

        trace += rng.standard_normal(nt) * 0.08
        data[:, ix] = trace
    return data

raw = build_gather()

# ── f-k transform ─────────────────────────────────────────────────────────────
# Zero-pad in offset for smoother spectrum
n_tr_pad = 128
raw_pad  = np.zeros((nt, n_tr_pad))
raw_pad[:, :n_tr] = raw

fk   = np.fft.fftshift(np.fft.fft2(raw_pad), axes=(0, 1))
amps = np.abs(fk)

df    = 1.0 / (nt * dt)              # Hz per bin
freqs = np.fft.fftshift(np.fft.fftfreq(nt, d=dt))

dk    = 1.0 / (n_tr_pad * dx)        # cycles/m per bin
knum  = np.fft.fftshift(np.fft.fftfreq(n_tr_pad, d=dx))

# ── f-k velocity filter ────────────────────────────────────────────────────────
K, F = np.meshgrid(knum, freqs)
V_apparent = np.where(K != 0, np.abs(F) / (np.abs(K) + 1e-12), 1e9)

mask = (V_apparent >= V_cutoff).astype(float)  # pass fast events, reject slow
fk_filt = fk * mask
filtered = np.real(np.fft.ifft2(np.fft.ifftshift(fk_filt)))[:, :n_tr]

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(17, 7))
gs  = fig.add_gridspec(1, 3, wspace=0.40)
ax_raw  = fig.add_subplot(gs[0, 0])
ax_fk   = fig.add_subplot(gs[0, 1])
ax_filt = fig.add_subplot(gs[0, 2])

t_ms = t_full * 1000
scale = 8.0

def plot_gather(ax, data, title):
    for ix in range(data.shape[1]):
        x = offsets[ix]
        tr = data[:, ix]
        ax.fill_betweenx(t_ms, x, x + tr * scale,
                          where=tr > 0, facecolor=BLACK, alpha=0.60)
        ax.plot(x + tr * scale, t_ms, color=BLACK, lw=0.25, alpha=0.4)
    ax.set_xlim(0, offsets[-1] + scale * 4)
    ax.set_ylim(1000, 0)
    ax.set_xlabel("Offset (m)")
    ax.set_ylabel("Time (ms)")
    ax.set_title(title, fontsize=13)

# Raw gather
plot_gather(ax_raw, raw, "(A) Raw shot gather")

# Annotate noise types
ax_raw.text(350, 180, "Ground roll\n(slow, high-amp)",
            color=RED, fontsize=10, ha="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=RED, alpha=0.8))
ax_raw.annotate("", xy=(150, 450), xytext=(280, 280),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))

ax_raw.text(900, 55, "Direct wave",
            color=BLUE, fontsize=10, ha="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=BLUE, alpha=0.8))
ax_raw.annotate("", xy=(1000, 450), xytext=(1050, 100),
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.2))

ax_raw.text(650, 700, "Reflection\n(hyperbola)",
            color=GREEN, fontsize=10, ha="center",
            bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=GREEN, alpha=0.8))

# f-k panel
f_pos    = freqs[freqs >= 0]
k_plot   = knum
amps_pos = amps[freqs >= 0, :]

pcm = ax_fk.pcolormesh(k_plot * 1000, f_pos,
                        np.log1p(amps_pos / np.percentile(amps_pos, 98)),
                        cmap="inferno", shading="auto",
                        vmin=0, vmax=3.0)

# Velocity fan lines
k_line = np.linspace(0.001, knum[-1], 100)
for V, c, lab in [(V_gr, RED, f"$V_{{gr}}={V_gr:.0f}$ m/s"),
                   (V_cutoff, ORANGE, f"$V_{{cut}}={V_cutoff:.0f}$ m/s  (filter)"),
                   (V1, BLUE, f"$V_1={V1:.0f}$ m/s")]:
    f_line = V * k_line  # f = V * k
    mask_f = f_line <= f_pos[-1]
    ax_fk.plot(k_line[mask_f] * 1000, f_line[mask_f],
               color=c, lw=1.8, ls="--", label=lab)

ax_fk.set_xlabel("Wavenumber $k$ (cycles km$^{-1}$)")
ax_fk.set_ylabel("Frequency $f$ (Hz)")
ax_fk.set_title("(B) f-k spectrum\n(log amplitude)", fontsize=13)
ax_fk.legend(loc="upper right", fontsize=10)
ax_fk.set_xlim(0, knum[-1] * 1000)
ax_fk.set_ylim(0, 80)

ax_fk.fill_between([0, knum[-1] * 1000], 0, 80,
                    where=[True, True],
                    alpha=0.0)
# Shade the reject region (slow events: ground roll fan)
k_rej = np.linspace(0, knum[-1], 200)
f_cut = V_cutoff * k_rej
f_cut = np.clip(f_cut, 0, 80)
ax_fk.fill_between(k_rej * 1000, f_cut, 80,
                    color=RED, alpha=0.12,
                    label="Reject (ground roll)")

# Filtered gather
plot_gather(ax_filt, filtered, "(C) After f-k filter\n(ground roll suppressed)")
ax_filt.text(0.02, 0.96, f"Filter: $V > {V_cutoff:.0f}$ m/s\nground roll removed",
             transform=ax_filt.transAxes, fontsize=10, va="top",
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=ORANGE, alpha=0.9))

fig.tight_layout()
fig.savefig("assets/figures/fig_ground_roll_fk.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_ground_roll_fk.png")

if __name__ == "__main__":
    plt.show()
