"""
buggy_refraction_picker.py

Lab 6, Part 3 — The Debugger Pattern.

This script analyzes a synthetic two-layer seismic refraction dataset.
It is meant to estimate the velocities V1 and V2 of the upper and lower
layers, and the depth h to the refractor, from a table of first-arrival
travel times.

It runs without error. It even produces a plot that looks reasonable.

But the answer it gives for V2 (and therefore h) is wrong.

Your task: figure out where the bug is using your AI assistant — without
just pasting "find the bug" and accepting whatever it says. You should
already know enough geophysics from Lab 3 to verify or reject the AI's
suggestions yourself.

The data below are synthetic and the TRUE values are intentionally not
written in this file — see your worksheet for the expected ranges.
"""

import numpy as np
import matplotlib.pyplot as plt


# ── First-arrival picks from a 2-layer refraction survey ────────────────
# Receiver offset (m) and picked first-arrival travel time (s).
# Shot at x = 0. Geophone spacing = 5 m. 21 picks total.
offsets_m = np.array([
    5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0, 45.0, 50.0,
    55.0, 60.0, 65.0, 70.0, 75.0, 80.0, 85.0, 90.0, 95.0, 100.0,
    105.0
])

times_s = np.array([
    0.0102, 0.0198, 0.0301, 0.0402, 0.0498, 0.0601, 0.0698, 0.0801,
    0.0899, 0.1001, 0.1049, 0.1075, 0.1099, 0.1125, 0.1148, 0.1173,
    0.1201, 0.1224, 0.1252, 0.1273, 0.1301
])


# ── Fit velocities and intercept ─────────────────────────────────────────

def fit_velocities(x, t, n_near=7):
    """
    Estimate V1 from near-offset (direct-wave) picks and V2 from
    far-offset (refracted-wave) picks, plus the intercept time t_i
    of the refracted branch.

    Parameters
    ----------
    x : array of receiver offsets [m]
    t : array of first-arrival travel times [s]
    n_near : number of near-offset picks to use for V1

    Returns
    -------
    V1 : direct-wave velocity [m/s]
    V2 : refracted-wave velocity [m/s]
    t_i : intercept time of the refracted branch [s]
    """
    # Direct wave: fit the first n_near picks.
    slope1, intercept1 = np.polyfit(x[:n_near], t[:n_near], 1)
    V1 = 1.0 / slope1

    # Refracted wave: fit the next set of picks beyond the direct branch.
    slope2, intercept2 = np.polyfit(x[:n_near + 5], t[:n_near + 5], 1)
    V2 = 1.0 / slope2
    t_i = intercept2

    return V1, V2, t_i


def layer_depth(V1, V2, t_i):
    """
    Compute the depth h to the refractor from V1, V2, and the
    refracted-branch intercept time t_i.

    Formula (two-layer flat refractor):
        t_i = 2 * h * cos(theta_c) / V1,
        with cos(theta_c) = sqrt(1 - (V1/V2)**2).
    """
    cos_theta_c = np.sqrt(1.0 - (V1 / V2) ** 2)
    h = t_i * V1 / (2.0 * cos_theta_c)
    return h


# ── Run the analysis ─────────────────────────────────────────────────────

V1, V2, t_i = fit_velocities(offsets_m, times_s, n_near=7)
h = layer_depth(V1, V2, t_i)

print(f"Estimated V1   = {V1:7.1f} m/s")
print(f"Estimated V2   = {V2:7.1f} m/s")
print(f"Intercept t_i  = {t_i*1000:7.2f} ms")
print(f"Layer depth h  = {h:7.2f} m")


# ── Plot ─────────────────────────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(7, 4.5))
ax.plot(offsets_m, times_s * 1000, "o", color="#0072B2",
        label="First arrival picks")

# Direct-wave fit line
x_fit = np.linspace(0, offsets_m.max(), 200)
ax.plot(x_fit, (x_fit / V1) * 1000, "-", color="#E69F00",
        label=f"Direct fit (V1 = {V1:.0f} m/s)")

# Refracted-wave fit line
ax.plot(x_fit, (x_fit / V2 + t_i) * 1000, "--", color="#009E73",
        label=f"Refracted fit (V2 = {V2:.0f} m/s)")

ax.set_xlabel("Receiver offset x (m)")
ax.set_ylabel("First-arrival time t (ms)")
ax.set_title("Lab 6 Part 3 — Buggy refraction picker")
ax.legend(loc="upper left")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("lab6_buggy_output.png", dpi=120, bbox_inches="tight")
plt.show()
