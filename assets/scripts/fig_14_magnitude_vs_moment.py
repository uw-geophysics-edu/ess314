"""
fig_14_magnitude_vs_moment.py

Scientific content: The relation between Mw, mb, Ms and seismic
moment M0, showing how mb and Ms saturate while Mw remains linear
in log10(M0). Saturation occurs because mb and Ms are measured at
fixed periods (1 s and 20 s respectively); for large earthquakes
whose corner frequency falls below those reciprocal periods, the
amplitude at fixed frequency grows much more slowly than M0.

Implementation: A Brune omega-squared source spectrum,
  Omega(f) = M0 / (1 + (f/fc)**2),
with self-similar scaling fc = 0.42 * beta / r and r derived from
constant stress drop Delta_sigma = 3 MPa via the Madariaga (1976)
circular crack relation
  M0 = (16/7) * Delta_sigma * r**3.
For each scale, M(f) is calibrated to equal Mw at low Mw, where the
spectrum is on its plateau and Omega(f) ~ M0.

Reproduces the scientific content of:
  Stein, S., & Wysession, M. (2003). An Introduction to Seismology,
  Earthquakes, and Earth Structure. Blackwell. Figure 9.25.

Reference: Madariaga, R. (1976). Dynamics of an expanding circular
fault. BSSA 66: 639-666.

Output: assets/figures/fig_14_magnitude_vs_moment.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 150,
    "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#E69F00", "#56B4E9", "#009E73",
          "#D55E00", "#CC79A7", "#000000"]


def Mw_from_M0(M0):
    return (2.0 / 3.0) * np.log10(M0) - 6.03


def M0_from_Mw(Mw):
    return 10.0 ** (1.5 * Mw + 9.0)


def corner_frequency(M0, beta=3500.0, stress_drop=3.0e6):
    """Brune corner frequency for omega-square source with self-similar scaling.
    M0 in N*m, beta in m/s, stress_drop in Pa. Returns fc in Hz.
    """
    r = (7.0 * M0 / (16.0 * stress_drop)) ** (1.0 / 3.0)  # source radius (m)
    return 0.42 * beta / r


def magnitude_at_period(M0, T_seconds, calibration_const):
    """Magnitude derived from spectral amplitude at period T."""
    f = 1.0 / T_seconds
    fc = corner_frequency(M0)
    # omega-square spectral level at frequency f:
    Omega_f = M0 / (1.0 + (f / fc) ** 2)
    # Convert to magnitude via M = (2/3) * log10(Omega) + const
    return (2.0 / 3.0) * np.log10(Omega_f) + calibration_const


def main():
    # Mw range and corresponding M0
    Mw_axis = np.linspace(3.0, 9.5, 400)
    M0_axis = M0_from_Mw(Mw_axis)

    # Calibration: at small Mw, the spectrum is flat and Omega(f) -> M0,
    # so M = (2/3)*log10(M0) + const. Choose const so M = Mw at small Mw.
    # That gives const = -6.03 (the same as the Mw definition).
    const = -6.03

    # mb at T = 1 s (f = 1 Hz)
    mb_curve = magnitude_at_period(M0_axis, 1.0, const)
    # Ms at T = 20 s (f = 0.05 Hz)
    Ms_curve = magnitude_at_period(M0_axis, 20.0, const)
    # 1-s and 20-s "log-amplitude" theoretical lines (Madariaga predictions)
    # — these are the dashed reference lines in Stein & Wysession 9.25.
    # They show the unsaturated continuation of mb / Ms given the source spectrum.

    fig, ax = plt.subplots(figsize=(8.4, 6.0))

    # Mw line (solid) — the full range
    ax.plot(np.log10(M0_axis), Mw_axis, color=COLORS[6], lw=2.6,
            label="$M_W$  (moment magnitude)", zorder=4)

    # mb corridor — shown as a band centred on mb_curve, +/- 0.3 unit
    ax.fill_between(np.log10(M0_axis), mb_curve - 0.30, mb_curve + 0.30,
                    color=COLORS[3], alpha=0.32, zorder=2)
    ax.plot(np.log10(M0_axis), mb_curve, color=COLORS[3], lw=2.0,
            label="$m_b$  (body wave, $T = 1$ s)", zorder=3)

    # Ms corridor
    ax.fill_between(np.log10(M0_axis), Ms_curve - 0.25, Ms_curve + 0.25,
                    color=COLORS[1], alpha=0.32, zorder=2)
    ax.plot(np.log10(M0_axis), Ms_curve, color=COLORS[1], lw=2.0,
            label="$M_S$  (surface wave, $T = 20$ s)", zorder=3)

    # Theoretical Madariaga omega-square dashed reference lines
    # 1 s: extrapolation of the mb spectral amplitude assuming pure
    # spectral plateau (slope 1 in Mw-M0 plane)
    Mw_low = np.linspace(3.0, 7.5, 200)
    M0_low = M0_from_Mw(Mw_low)
    ref_1s = magnitude_at_period(M0_low, 1.0, const)
    ax.plot(np.log10(M0_low), ref_1s, color=COLORS[3], lw=1.0, ls="--",
            alpha=0.7, zorder=1)
    ax.text(np.log10(M0_low[120]) + 0.2, ref_1s[120] - 0.5, "1 s",
            color=COLORS[3], fontsize=10, fontstyle="italic")

    # 20 s: similar
    Mw_low2 = np.linspace(3.0, 8.5, 200)
    M0_low2 = M0_from_Mw(Mw_low2)
    ref_20s = magnitude_at_period(M0_low2, 20.0, const)
    ax.plot(np.log10(M0_low2), ref_20s, color=COLORS[1], lw=1.0, ls="--",
            alpha=0.7, zorder=1)
    ax.text(np.log10(M0_low2[150]) + 0.2, ref_20s[150] - 0.5, "20 s",
            color=COLORS[1], fontsize=10, fontstyle="italic")

    # Annotation: saturation regions
    ax.annotate("$m_b$ saturates\n(corner $f_c < 1$ Hz)",
                xy=(20.5, 6.6), xytext=(17.5, 4.5), fontsize=10,
                arrowprops=dict(arrowstyle="->", color=COLORS[3], lw=1.0),
                ha="center", color=COLORS[3])
    ax.annotate("$M_S$ saturates\n(corner $f_c < 0.05$ Hz)",
                xy=(21.7, 8.05), xytext=(19.0, 8.7), fontsize=10,
                arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=1.0),
                ha="center", color=COLORS[1])

    ax.set_xlabel("$\\log_{10}(M_0)$  [N$\\cdot$m]")
    ax.set_ylabel("Magnitude")
    ax.set_title("Magnitude saturation: why $M_W$ is the modern standard")
    ax.set_xlim(12, 22.5)
    ax.set_ylim(2.5, 9.5)
    ax.grid(True, alpha=0.3, ls=":")
    ax.tick_params(direction="in", top=True, right=True)
    ax.legend(loc="upper left", framealpha=0.95)

    fig.tight_layout()
    fig.savefig("assets/figures/fig_14_magnitude_vs_moment.png",
                bbox_inches="tight")
    print("Saved fig_14_magnitude_vs_moment.png")


if __name__ == "__main__":
    main()
