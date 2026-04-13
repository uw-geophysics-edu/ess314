"""
fig_dl_denoising_concept.py

Scientific content:
    Deep learning denoising of seismic reflection data is typically
    performed by encoder-decoder convolutional neural networks (CNNs),
    most commonly the U-Net architecture (Ronneberger et al. 2015,
    adapted for seismics by Zhao et al. 2019 and Liu et al. 2020).

    The U-Net learns a non-linear mapping from noisy seismic input to
    a clean (signal) output. Key architectural elements:
      — Encoder (downsampling path): stacked conv + MaxPool layers extract
        multi-scale features from the input gather.
      — Bottleneck: deepest feature representation.
      — Decoder (upsampling path): transposed convolutions expand
        features back to the original resolution.
      — Skip connections: direct links from encoder to decoder preserve
        fine spatial detail lost during downsampling.

    Panel A: schematic U-Net architecture diagram.
    Panel B: Noisy synthetic CMP gather (input).
    Panel C: Denoised gather (simulated output using band-pass filtering
             as a proxy for ML denoising — for illustration only).

Reproduces scientific content of:
    Ronneberger, O. et al. (2015). U-Net: Convolutional networks for
    biomedical image segmentation. MICCAI Proc. doi:10.1007/978-3-319-24574-4_28
    Liu, D. et al. (2020). Self-supervised deep learning for seismic
    data denoising. Geophysics, 85(6), V317–V334. doi:10.1190/geo2019-0501.1

Output: assets/figures/fig_dl_denoising_concept.png
License: CC-BY 4.0 (this script)
"""

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from scipy.signal import fftconvolve, butter, filtfilt

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 11,
    "ytick.labelsize": 11,
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
SKY    = "#56B4E9"

rng = np.random.default_rng(55)

# ── Synthetic noisy gather ────────────────────────────────────────────────────
dt      = 0.002
nt      = 401
t_full  = np.arange(nt) * dt
offsets = np.arange(0, 2001, 200)   # 0–2000 m, 11 traces
n_tr    = len(offsets)

V_rms   = 2000.0
t0_list = [0.35, 0.65, 0.85]
amps    = [1.0, 0.8, 0.6]

def ricker(f0, dt, t_half=0.10):
    tw = np.arange(-t_half, t_half, dt)
    u  = (np.pi * f0 * tw)**2
    return (1 - 2*u) * np.exp(-u)

wav = ricker(30.0, dt)

# Build clean gather
clean = np.zeros((nt, n_tr))
for ix, x in enumerate(offsets):
    spike = np.zeros(nt)
    for t0, amp in zip(t0_list, amps):
        tx  = np.sqrt(t0**2 + x**2/V_rms**2)
        idx = int(round(tx / dt))
        if idx < nt:
            spike[idx] += amp
    clean[:, ix] = fftconvolve(spike, wav, mode="same")

# Add noise to create noisy gather
noise_level = 0.65
noisy = clean + rng.standard_normal((nt, n_tr)) * noise_level

# Simulate denoising with a bandpass filter (proxy for U-Net output)
def bandpass(trace, dt, flo, fhi):
    b, a = butter(4, [flo, fhi], btype="band", fs=1/dt)
    return filtfilt(b, a, trace)

denoised = np.zeros_like(noisy)
for ix in range(n_tr):
    denoised[:, ix] = bandpass(noisy[:, ix], dt, 10, 60)

# ── Figure layout ─────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(17, 8))
gs  = fig.add_gridspec(1, 3, wspace=0.38,
                        width_ratios=[2.0, 1.2, 1.2])
ax_arch  = fig.add_subplot(gs[0, 0])
ax_noisy = fig.add_subplot(gs[0, 1])
ax_clean = fig.add_subplot(gs[0, 2])

# ── Panel A: U-Net architecture schematic ────────────────────────────────────
ax = ax_arch
ax.set_xlim(0, 12)
ax.set_ylim(-1.0, 9.0)
ax.set_aspect("equal", adjustable="box")
ax.axis("off")
ax.set_title("(A) U-Net architecture\n(convolutional encoder–decoder)", fontsize=13)

def draw_box(ax, x, y, w, h, fc, ec=BLACK, label=None, lw=1.5, fontsize=11):
    rect = mpatches.FancyBboxPatch((x - w/2, y - h/2), w, h,
                                    boxstyle="round,pad=0.05",
                                    facecolor=fc, edgecolor=ec, lw=lw, zorder=3)
    ax.add_patch(rect)
    if label:
        ax.text(x, y, label, ha="center", va="center",
                fontsize=fontsize, color=BLACK, zorder=4, wrap=True)

def arrow(ax, x1, y1, x2, y2, color=GRAY, lw=1.2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", color=color, lw=lw),
                zorder=5)

# Input
draw_box(ax, 1.0, 4.0, 1.4, 0.9, fc=SKY,    label="Input\n(noisy\ngather)", fontsize=11)

# Encoder layers (left column, going down)
encoder_y = [4.0, 2.8, 1.6, 0.4]
enc_colors = [GREEN, GREEN, GREEN, ORANGE]
enc_labels = ["Conv\n64ch", "Conv\n128ch", "Conv\n256ch", "Bottleneck\n512ch"]
enc_x = [3.0, 4.2, 5.4, 6.6]

for i, (ex, ey, ec_col, el) in enumerate(zip(enc_x, encoder_y, enc_colors, enc_labels)):
    # Encoder box
    draw_box(ax, ex, ey, 1.4, 0.75, fc=ec_col, label=el, fontsize=7)
    if i == 0:
        arrow(ax, 1.7, 4.0, 2.3, 4.0)
    else:
        # Downsampling arrow (diagonal)
        arrow(ax, enc_x[i-1]+0.7, encoder_y[i-1]-0.38, ex-0.7, ey+0.38,
              color=GREEN)
        ax.text((enc_x[i-1]+ex)/2 - 0.2, (encoder_y[i-1]+ey)/2,
                "Pool", fontsize=7, color=GREEN, ha="center")

# Decoder layers (going back up on right side)
dec_x     = [8.0, 9.2, 10.4]
dec_y     = [1.6, 2.8, 4.0]
dec_colors = [BLUE, BLUE, BLUE]
dec_labels = ["Conv\n256ch", "Conv\n128ch", "Conv\n64ch"]
skip_from = [enc_x[2], enc_x[1], enc_x[0]]
skip_y_enc = [encoder_y[2], encoder_y[1], encoder_y[0]]

# Connection from bottleneck to first decoder
arrow(ax, enc_x[3]+0.7, encoder_y[3]+0.38, dec_x[0]-0.7, dec_y[0]-0.38, color=ORANGE)
ax.text((enc_x[3]+dec_x[0])/2, (encoder_y[3]+dec_y[0])/2 - 0.1,
        "Upsample", fontsize=7, color=ORANGE, ha="center")

for i, (dx, dy, dc_col, dl) in enumerate(zip(dec_x, dec_y, dec_colors, dec_labels)):
    draw_box(ax, dx, dy, 1.4, 0.75, fc=dc_col, label=dl, fontsize=7)
    if i > 0:
        arrow(ax, dec_x[i-1]+0.7, dec_y[i-1]+0.38, dx-0.7, dy-0.38,
              color=BLUE)
        ax.text((dec_x[i-1]+dx)/2 - 0.2, (dec_y[i-1]+dy)/2,
                "Up", fontsize=7, color=BLUE, ha="center")
    # Skip connection (horizontal arrow from encoder to decoder)
    sfx, sfy = skip_from[i], skip_y_enc[i]
    ax.annotate("", xy=(dx - 0.7, dy), xytext=(sfx + 0.7, sfy),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2,
                                connectionstyle="arc3,rad=0.35"),
                zorder=2)

ax.text(7.0, 7.8, "Skip connections\n(preserve fine detail)",
        ha="center", fontsize=11, color=RED,
        bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=RED, alpha=0.8))
# Arrow to label
ax.annotate("", xy=(7.5, 4.4), xytext=(7.5, 7.2),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))

# Output
draw_box(ax, 11.7, 4.0, 1.4, 0.9, fc=SKY, label="Output\n(denoised\ngather)", fontsize=11)
arrow(ax, 11.1, 4.0, 11.0, 4.0)

# Legend boxes
legend_items = [
    mpatches.Patch(facecolor=GREEN, edgecolor=BLACK, label="Encoder (downsample)"),
    mpatches.Patch(facecolor=BLUE, edgecolor=BLACK, label="Decoder (upsample)"),
    mpatches.Patch(facecolor=ORANGE, edgecolor=BLACK, label="Bottleneck"),
    mlines.Line2D([],[], color=RED, lw=1.5, label="Skip connections"),
]
ax.legend(handles=legend_items, loc="upper left", fontsize=11,
          bbox_to_anchor=(0.0, 0.18))

# ── Panels B and C: noisy and denoised gathers ───────────────────────────────
t_ms  = t_full * 1000
scale = 60.0

def plot_gath(ax, data, title):
    for ix, x in enumerate(offsets):
        tr = data[:, ix]
        ax.fill_betweenx(t_ms, x, x + tr * scale,
                          where=tr > 0, facecolor=BLACK, alpha=0.65)
        ax.plot(x + tr * scale, t_ms, color=BLACK, lw=0.35, alpha=0.5)
    ax.set_xlim(-60, 2100)
    ax.set_ylim(800, 0)
    ax.set_xlabel("Offset (m)")
    ax.set_title(title, fontsize=13)

plot_gath(ax_noisy, noisy,    "(B) Input: noisy gather\n(field data + random noise)")
ax_noisy.set_ylabel("Two-way time (ms)")

plot_gath(ax_clean, denoised, "(C) Output: denoised\n(band-pass proxy for U-Net)")
ax_clean.set_ylabel("")
ax_clean.set_yticklabels([])

# SNR labels
ax_noisy.text(0.98, 0.97, "Low SNR", transform=ax_noisy.transAxes,
              ha="right", va="top", fontsize=11, color=RED,
              bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=RED, alpha=0.85))
ax_clean.text(0.98, 0.97, "Improved SNR", transform=ax_clean.transAxes,
              ha="right", va="top", fontsize=11, color=GREEN,
              bbox=dict(boxstyle="round,pad=0.2", fc="white", ec=GREEN, alpha=0.85))

fig.tight_layout()
fig.savefig("assets/figures/fig_dl_denoising_concept.png",
            dpi=300, bbox_inches="tight")
print("Saved: assets/figures/fig_dl_denoising_concept.png")

if __name__ == "__main__":
    plt.show()
