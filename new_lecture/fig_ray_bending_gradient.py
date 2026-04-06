"""
fig_ray_bending_gradient.py

Ray paths in a medium with velocity increasing linearly with depth.
V(z) = V0 + g*z produces circular arc ray paths.
Depth positive downward (geophysics convention).

Output: assets/figures/fig_ray_bending_gradient.png
License: CC-BY 4.0
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 15, "axes.labelsize": 13,
    "xtick.labelsize": 12, "ytick.labelsize": 12, "legend.fontsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

COLORS = ["#0072B2", "#56B4E9", "#009E73", "#E69F00", "#D55E00"]

def main():
    fig, ax = plt.subplots(figsize=(12, 6))
    V0 = 6.0     # km/s at surface (upper mantle scale)
    g  = 0.005   # (km/s)/km gradient

    takeoff_angles = [20, 30, 40, 50, 60]  # from vertical

    for idx, a_deg in enumerate(takeoff_angles):
        theta0 = np.radians(a_deg)
        p = np.sin(theta0) / V0
        R = 1.0 / (p * g)
        z_turn = (1.0/p - V0) / g

        # Simple numerical integration using Snell's law: dz/dx = cot(theta)
        # with p = sin(theta)/V(z) => sin(theta) = p*V(z) = p*(V0 + g*z)
        # dz = cos(theta)*ds, dx = sin(theta)*ds
        # dx/dz = sin(theta)/cos(theta) = tan(theta)
        # sin(theta) = p*(V0+g*z), cos(theta) = sqrt(1 - sin^2(theta))

        z_arr = np.linspace(0, z_turn, 500)
        sin_th = p * (V0 + g * z_arr)
        sin_th = np.clip(sin_th, 0, 1.0)
        cos_th = np.sqrt(1.0 - sin_th**2)
        # dx/dz = tan(theta) = sin/cos
        dxdz = sin_th / np.where(cos_th > 1e-10, cos_th, 1e-10)
        # Integrate
        x_down = np.zeros_like(z_arr)
        dz = np.diff(z_arr)
        for i in range(1, len(z_arr)):
            x_down[i] = x_down[i-1] + dxdz[i-1] * dz[i-1]

        # Up leg (mirror)
        x_up = 2*x_down[-1] - x_down[::-1]
        z_up = z_arr[::-1]

        x_full = np.concatenate([x_down, x_up[1:]])
        z_full = np.concatenate([z_arr, z_up[1:]])

        c = COLORS[idx]
        ax.plot(x_full, z_full, color=c, lw=2.2, label=f"$\\theta_0={a_deg}°$")
        ax.plot(x_down[-1], z_turn, "o", color=c, markersize=5, zorder=4)

    # Source
    ax.plot(0, 0, "*", color="#D55E00", markersize=16, zorder=5)
    ax.text(15, -15, "Source", fontsize=12, color="#D55E00", fontweight="bold")

    # V(z) profile on right
    xmax = ax.get_xlim()[1]
    z_p = np.linspace(0, ax.get_ylim()[0] if ax.get_ylim()[0] > 0 else 300, 50)
    # recalculate after plot
    z_p = np.linspace(0, z_turn, 50)  # use deepest turning depth
    V_p = V0 + g * z_p

    ax.set_xlabel("Horizontal distance (km)", fontsize=13)
    ax.set_ylabel("Depth (km)", fontsize=13)
    ax.set_title("Ray Paths in a Linear Velocity Gradient: $V(z) = V_0 + gz$",
                 fontsize=14, fontweight="bold")
    ax.invert_yaxis()
    ax.legend(loc="lower right", fontsize=11, framealpha=0.9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    plt.tight_layout()
    plt.savefig("assets/figures/fig_ray_bending_gradient.png", bbox_inches="tight")
    plt.close()
    print("Saved: assets/figures/fig_ray_bending_gradient.png")

if __name__ == "__main__":
    main()
