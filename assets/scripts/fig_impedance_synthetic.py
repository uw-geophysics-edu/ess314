"""
1-D impedance model → reflectivity series → source wavelet → synthetic seismogram.
Four-panel figure for the convolutional model (lecture 08, slide 5).
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
def scipy_ricker(points, a):
    """Ricker (Mexican hat) wavelet — replaces removed scipy.signal.ricker."""
    t = np.arange(-(points // 2), points // 2 + 1) * 1.0
    psi = (1 - 2*(np.pi*a*t)**2 / points**2) * np.exp(-(np.pi*a*t)**2 / points**2)
    return psi[:points]

BLUE   = "#0072B2"
RED    = "#D55E00"
ORANGE = "#E69F00"
DARK   = "#1A1A2E"

# ── Earth model (two-way times at layer tops) ─────────────────────────────────
layer_twt = np.array([0.00, 0.26, 0.50, 0.74, 0.98])   # s
Vp        = np.array([1800, 2400, 2100, 3200, 2800])    # m/s
rho       = np.array([1.80, 2.10, 2.00, 2.45, 2.30])   # g/cm³
Z         = Vp * rho
layer_labels = [
    "Sediments\n1800 m/s",
    "Sandstone\n2400 m/s",
    "Shale\n2100 m/s",
    "Limestone\n3200 m/s",
    "Basement\n2800 m/s",
]
layer_colors = ["#AED6F1", "#F9E79F", "#C8E6C9", "#FFCC80", "#D7BDE2"]

# ── Time axis & reflectivity ──────────────────────────────────────────────────
T_MAX = 1.20
dt    = 0.001
t_ax  = np.arange(0, T_MAX, dt)
r_series = np.zeros(len(t_ax))
R_vals, t_R = [], []
for i in range(len(layer_twt) - 1):
    R = (Z[i + 1] - Z[i]) / (Z[i + 1] + Z[i])
    t_i = layer_twt[i + 1]
    idx = int(round(t_i / dt))
    if 0 <= idx < len(t_ax):
        r_series[idx] = R
    R_vals.append(R)
    t_R.append(t_i)

# ── Ricker wavelet (30 Hz) ────────────────────────────────────────────────────
f_dom = 30
nw    = int(0.12 / dt)
if nw % 2 == 0:
    nw += 1
wav = scipy_ricker(nw, 1.0 / (f_dom * dt))
wav = wav / np.max(np.abs(wav))

# ── Synthetic ─────────────────────────────────────────────────────────────────
synth = np.convolve(r_series, wav, mode="same")

# ── Figure ────────────────────────────────────────────────────────────────────
fig, axes = plt.subplots(1, 4, figsize=(11, 4.8),
                          gridspec_kw={"width_ratios": [1.6, 0.85, 0.85, 1.05]})
fig.subplots_adjust(wspace=0.50)

# Panel A: impedance profile
ax = axes[0]
for i in range(len(layer_twt)):
    t_top = layer_twt[i]
    t_bot = layer_twt[i + 1] if i + 1 < len(layer_twt) else T_MAX
    ax.fill_betweenx([t_top, t_bot], 0, Z[i] / 1000,
                     color=layer_colors[i], alpha=0.8, linewidth=0)
    ax.plot([0, Z[i] / 1000], [t_top, t_top], color="k", lw=0.8)
    ax.text(Z[i] / 1000 * 0.50, (t_top + t_bot) / 2,
            layer_labels[i], fontsize=7, ha="center", va="center")
ax.set_xlim(0, 9)
ax.set_ylim(T_MAX, 0)
ax.set_xlabel("$Z$ (×10³ kg m⁻²s⁻¹)", fontsize=9)
ax.set_ylabel("Two-way time (s)", fontsize=9)
ax.set_title("(A) Impedance\n$Z = \\rho V_P$", fontsize=9)

# Panel B: reflectivity spikes
ax = axes[1]
ax.axvline(0, color="k", lw=0.8)
for R, t in zip(R_vals, t_R):
    col = RED if R > 0 else BLUE
    ax.plot([0, R], [t, t], color=col, lw=3.5)
    ax.plot(R, t, "o", ms=7, color=col, zorder=5)
    ax.text(R + (0.03 if R > 0 else -0.03), t, f"{R:+.2f}",
            fontsize=7, va="center", ha="left" if R > 0 else "right", color=col)
ax.set_xlim(-0.38, 0.38)
ax.set_ylim(T_MAX, 0)
ax.set_xlabel("$R$", fontsize=9)
ax.set_title("(B) Reflectivity\n$r(t)$", fontsize=9)
ax.set_yticklabels([])

# Panel C: wavelet
ax = axes[2]
tw_ms = (np.arange(len(wav)) - len(wav) // 2) * dt * 1000
ax.plot(wav, tw_ms, color=ORANGE, lw=2.2)
ax.fill_betweenx(tw_ms, 0, wav, where=wav > 0, color=ORANGE, alpha=0.45)
ax.fill_betweenx(tw_ms, 0, wav, where=wav < 0, color=RED,    alpha=0.35)
ax.axvline(0, color="k", lw=0.8)
ax.set_ylim(70, -70)
ax.set_xlabel("Amplitude", fontsize=9)
ax.set_title(f"(C) Wavelet\n$w(t)$  ({f_dom} Hz)", fontsize=9)
ax.set_yticklabels([])

# Panel D: synthetic seismogram
ax = axes[3]
ax.plot(synth, t_ax, color=DARK, lw=1.5)
ax.fill_betweenx(t_ax, synth, 0, where=synth > 0, color=BLUE, alpha=0.55)
ax.fill_betweenx(t_ax, synth, 0, where=synth < 0, color=RED,  alpha=0.45)
ax.axvline(0, color="k", lw=0.8)
for t in t_R:
    ax.axhline(t, color="gray", ls=":", lw=0.8, alpha=0.6)
ax.set_xlim(-0.40, 0.40)
ax.set_ylim(T_MAX, 0)
ax.set_xlabel("Amplitude", fontsize=9)
ax.set_title("(D) Synthetic\n$d(t) = w * r$", fontsize=9)
ax.set_yticklabels([])

plt.savefig("assets/figures/fig_impedance_synthetic.png", dpi=150, bbox_inches="tight")
print("Saved: assets/figures/fig_impedance_synthetic.png")
