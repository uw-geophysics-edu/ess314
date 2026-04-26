"""
fig_three_phase_seismogram.py

Scientific content: A synthetic single-component seismogram for a moderate
earthquake recorded at teleseismic distance, with the three principal phases
— P, S, and Rayleigh-type surface waves — highlighted by shaded time
windows. The S-minus-P time and the dominance of long-period surface waves
in the late coda are the diagnostic features that allow first-pass
identification of phases on a real record.

Reproduces the scientific content of:
  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.
  Cambridge University Press, Ch. 4 (seismograms and phase identification).
  Stein & Wysession (2003), An Introduction to Seismology, Earthquakes, and
  Earth Structure, Blackwell, Fig. 1.1-3.

Output: assets/figures/fig_three_phase_seismogram.png
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

C_P = "#0072B2"
C_S = "#E69F00"
C_SURF = "#CC79A7"
C_TRACE = "#1A1A1A"
C_BAND_P = "#E0EEFA"
C_BAND_S = "#FBEFD8"
C_BAND_SURF = "#F4E1EC"

# Parameters chosen to match a teleseismic record (Δ ≈ 60°, depth 30 km)
t_P = 9.0 * 60       # 9 minutes
t_S = 16.5 * 60      # 16.5 minutes
t_surf = 25.0 * 60   # 25 minutes
t_max = 32 * 60

t = np.linspace(0, t_max, 9000)
rng = np.random.default_rng(2026)


def gauss_window(t_arr, t0, width):
    return np.exp(-((t_arr - t0) / width) ** 2)


# Background noise (low amplitude, broadband)
noise = 0.025 * rng.standard_normal(t.size)

# P-wave: short-duration high-frequency pulse
p_envelope = gauss_window(t, t_P + 5, 8)
p_wave = 0.45 * p_envelope * np.cos(2 * np.pi * 0.7 * (t - t_P))
p_wave += 0.18 * gauss_window(t, t_P + 18, 12) * np.cos(2 * np.pi * 0.45 * (t - t_P - 18))

# S-wave: larger amplitude, lower frequency than P
s_envelope = gauss_window(t, t_S + 8, 14)
s_wave = 0.85 * s_envelope * np.cos(2 * np.pi * 0.32 * (t - t_S))
s_wave += 0.30 * gauss_window(t, t_S + 35, 22) * np.cos(2 * np.pi * 0.20 * (t - t_S - 35))

# Surface wave: dispersive train, longest period, largest amplitude
sw_envelope = gauss_window(t, t_surf + 90, 110)
# Frequency that drifts from 0.07 Hz to 0.04 Hz across the wavetrain
phase = 2 * np.pi * (0.07 * (t - t_surf) - 0.5e-4 * (t - t_surf) ** 2)
surface_wave = 1.55 * sw_envelope * np.cos(phase)

# Total
trace = noise + p_wave + s_wave + surface_wave

# ── Plot ────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(13.0, 5.2))

# Time-window shading
ax.axvspan(0, t_P, color="#F1F1F1", alpha=0.55, zorder=0,
           label="_nolegend_")
ax.axvspan(t_P, t_S, color=C_BAND_P, alpha=0.85, zorder=0)
ax.axvspan(t_S, t_surf, color=C_BAND_S, alpha=0.85, zorder=0)
ax.axvspan(t_surf, t_max, color=C_BAND_SURF, alpha=0.85, zorder=0)

# Trace
ax.plot(t, trace, color=C_TRACE, lw=0.85, zorder=4)

# Phase onset markers
for tp, label, color in [(t_P, "P onset", C_P), (t_S, "S onset", C_S),
                         (t_surf, "Surface\nwave start", C_SURF)]:
    ax.axvline(tp, color=color, lw=2.0, zorder=5)

# Window labels along the top
ymax = 2.3
ax.set_ylim(-2.3, ymax)
y_label = ymax - 0.20
ax.text((0 + t_P) / 2, y_label, "Pre-event noise",
        ha="center", va="top", fontsize=11.5, color="#555555")
ax.text((t_P + t_S) / 2, y_label, "P alone",
        ha="center", va="top", fontsize=12, color="#005a8a", fontweight="bold")
ax.text((t_S + t_surf) / 2, y_label, "P + S",
        ha="center", va="top", fontsize=12, color="#a16700", fontweight="bold")
ax.text((t_surf + t_max) / 2, y_label, "P + S + surface waves",
        ha="center", va="top", fontsize=12, color="#7e2360", fontweight="bold")

# S minus P annotation (key diagnostic)
ax.annotate("", xy=(t_S, -1.85), xytext=(t_P, -1.85),
            arrowprops=dict(arrowstyle="<->", color="#444444", lw=1.6))
ax.text((t_P + t_S) / 2, -2.05, r"$T_S - T_P\ \approx\ 7.5$ min",
        ha="center", va="top", fontsize=12, color="#222222",
        bbox=dict(facecolor="white", edgecolor="#444444", lw=0.6,
                  boxstyle="round,pad=0.3"))

# Phase callouts pointing to the trace
ax.annotate("P", xy=(t_P + 4, 0.55), xytext=(t_P - 60, 1.45),
            fontsize=13, fontweight="bold", color=C_P,
            arrowprops=dict(arrowstyle="->", color=C_P, lw=1.0))
ax.annotate("S", xy=(t_S + 8, 0.95), xytext=(t_S - 70, 1.55),
            fontsize=13, fontweight="bold", color=C_S,
            arrowprops=dict(arrowstyle="->", color=C_S, lw=1.0))
ax.annotate("Rayleigh + Love\n(surface waves)",
            xy=(t_surf + 90, 1.55), xytext=(t_surf + 200, 1.95),
            fontsize=12, fontweight="bold", color=C_SURF,
            arrowprops=dict(arrowstyle="->", color=C_SURF, lw=1.0))

# Cosmetic axes
ax.set_xlim(0, t_max)
ax.set_xlabel("Time after origin (minutes)")
ax.set_ylabel("Ground velocity (relative units)")
ax.set_title("Anatomy of a teleseismic seismogram: P, S, and surface waves "
             "in time order", fontsize=14, pad=8)
ax.set_xticks(np.arange(0, t_max + 1, 5 * 60))
ax.set_xticklabels([f"{int(x/60)}" for x in np.arange(0, t_max + 1, 5 * 60)])
ax.grid(False)

fig.tight_layout()

if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out = "assets/figures/fig_three_phase_seismogram.png"
    fig.savefig(out, dpi=200, bbox_inches="tight")
    print(f"Saved: {out}")
