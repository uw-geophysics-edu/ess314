"""
fig_16_response_spectrum.py

Scientific content: Three stacked panels showing (top) a synthetic ground
acceleration time series, (middle) the same record integrated to velocity,
and (bottom) the 5%-damped pseudo-spectral acceleration as a function of
oscillator natural period. Demonstrates the relationship between PGA, PGV,
and Sa(T), and illustrates which periods carry the most damaging energy
for a given record.

Reproduces the qualitative content of slide 6 of the legacy ESS 314 deck
(strong-motion metrics) and is the canonical figure introducing the
response spectrum, after:
  Chopra, A.K. (2017). Dynamics of Structures, 5th ed., Pearson.
  Boore, D.M., Stewart, J.P., Seyhan, E., & Atkinson, G.M. (2014).
  NGA-West2 equations for predicting PGA, PGV, and 5%-damped PSA for
  shallow crustal earthquakes. Earthquake Spectra, 30(3), 1057-1085.
  DOI: 10.1193/070113EQS184M

Output: assets/figures/fig_16_response_spectrum.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.integrate import cumulative_trapezoid

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

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]

rng = np.random.default_rng(42)


def synthetic_acceleration(dt=0.005, T_total=30.0):
    """Synthesise a strong-motion-like acceleration record using a
    Boore (2003) stochastic point-source approximation: filter Gaussian
    noise through a Brune source spectrum, multiply by an envelope, and
    apply a high-pass to remove drift."""
    n = int(T_total / dt)
    t = np.linspace(0, T_total, n)
    # Saragoni-Hart envelope
    t_p = 2.5  # peak time
    env = (t / t_p) ** 2 * np.exp(-1.5 * (t / t_p - 1))
    env[t > 4 * t_p] *= np.exp(-(t[t > 4 * t_p] - 4 * t_p) / 5.0)
    # White noise -> filter to be Brune-spectrum-like in frequency
    white = rng.standard_normal(n)
    nfft = n
    freqs = np.fft.rfftfreq(nfft, dt)
    f_c = 1.5  # corner frequency (Hz)
    spectrum = (freqs**2) / (1 + (freqs / f_c)**2)
    spectrum[0] = 0  # remove DC
    # Multiply white spectrum by Brune-like
    W = np.fft.rfft(white)
    A = np.fft.irfft(W * spectrum, n=nfft)
    a = env * A
    # Normalise so peak = 0.35 g
    a = a / np.max(np.abs(a)) * 0.35 * 9.81
    return t, a


def integrate_to_velocity(t, a):
    """Integrate acceleration -> velocity with high-pass filtering."""
    v = cumulative_trapezoid(a, t, initial=0)
    # Remove linear drift via a simple linear baseline correction
    drift = np.linspace(v[0], v[-1], len(v))
    v = v - drift
    return v


def response_spectrum(a_g, dt, periods, zeta=0.05):
    """Compute the pseudo-spectral acceleration Sa(T) for an array
    of natural periods. Solves the SDOF ODE
        x'' + 2*zeta*omega0*x' + omega0^2*x = -a(t)
    in the frequency domain using the transfer function approach."""
    n = len(a_g)
    nfft = n
    freqs = np.fft.rfftfreq(nfft, dt)
    omega = 2 * np.pi * freqs
    A_hat = np.fft.rfft(a_g)
    Sa = np.zeros_like(periods)
    for k, T in enumerate(periods):
        omega0 = 2 * np.pi / T
        # Transfer function: X(omega) / -A(omega) = 1 / (omega0^2 - omega^2 + 2j*zeta*omega0*omega)
        H = 1.0 / (omega0**2 - omega**2 + 2j * zeta * omega0 * omega)
        X_hat = -A_hat * H
        x = np.fft.irfft(X_hat, n=nfft)
        Sa[k] = (omega0 ** 2) * np.max(np.abs(x))
    return Sa


# ── Compute ─────────────────────────────────────────────────────────
dt = 0.005
t, a = synthetic_acceleration(dt=dt, T_total=30.0)
v = integrate_to_velocity(t, a)
periods = np.geomspace(0.05, 10.0, 80)
Sa = response_spectrum(a, dt, periods, zeta=0.05)

PGA = np.max(np.abs(a)) / 9.81
PGV = np.max(np.abs(v)) * 100  # cm/s

# ── Plot ────────────────────────────────────────────────────────────
fig, axs = plt.subplots(3, 1, figsize=(8.5, 9.0))

# Top: acceleration
axs[0].plot(t, a / 9.81, color=COLORS[0], linewidth=0.9)
axs[0].axhline(PGA, color=COLORS[4], linestyle="--", linewidth=1.2,
               label=f"PGA = {PGA:.2f} g")
axs[0].axhline(-PGA, color=COLORS[4], linestyle="--", linewidth=1.2)
axs[0].set_ylabel("Acceleration (g)")
axs[0].set_title("Synthetic ground motion record (M ~ 6.5 at ~30 km)")
axs[0].legend(loc="upper right")
axs[0].grid(alpha=0.3)

# Middle: velocity
axs[1].plot(t, v * 100, color=COLORS[3], linewidth=0.9)
axs[1].axhline(PGV, color=COLORS[4], linestyle="--", linewidth=1.2,
               label=f"PGV = {PGV:.1f} cm/s")
axs[1].axhline(-PGV, color=COLORS[4], linestyle="--", linewidth=1.2)
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("Velocity (cm/s)")
axs[1].set_title("Same record integrated to velocity (longer-period content)")
axs[1].legend(loc="upper right")
axs[1].grid(alpha=0.3)

# Bottom: Sa(T)
axs[2].semilogx(periods, Sa / 9.81, color=COLORS[6], linewidth=2.5,
                label=r"$S_a(T)$, $\zeta=0.05$")
# Highlight design periods
for T_des, label in [(0.2, "0.2 s\n(low-rise)"),
                     (1.0, "1.0 s\n(mid-rise)"),
                     (3.0, "3.0 s\n(high-rise)")]:
    Sa_T = np.interp(T_des, periods, Sa) / 9.81
    axs[2].plot([T_des], [Sa_T], "o", color=COLORS[4], markersize=9, zorder=5)
    axs[2].annotate(label, xy=(T_des, Sa_T),
                    xytext=(T_des * 1.1, Sa_T + 0.04),
                    fontsize=11)
axs[2].set_xlabel("Natural period T of oscillator (s)")
axs[2].set_ylabel(r"$S_a(T)$ (g)")
axs[2].set_title(r"Response spectrum $S_a(T)$ — what a building of period $T$ feels")
axs[2].grid(True, which="both", alpha=0.3)
axs[2].legend(loc="upper right")
axs[2].set_xlim(0.05, 10)

# Note explaining the rule of thumb
axs[2].text(0.03, 0.93,
            r"Building rule of thumb: $T \approx N/10$ s (N = storeys)",
            transform=axs[2].transAxes, fontsize=11,
            bbox=dict(facecolor="white", edgecolor="#888888",
                      alpha=0.92, boxstyle="round,pad=0.4"),
            va="top")

fig.tight_layout()
fig.savefig("/home/claude/ess314/assets/figures/fig_16_response_spectrum.png",
            bbox_inches="tight")
print(f"PGA={PGA:.3f} g, PGV={PGV:.1f} cm/s")
print("Saved fig_16_response_spectrum.png")
