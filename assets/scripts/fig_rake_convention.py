"""
fig_rake_convention.py

Scientific content: convention for the rake angle lambda, the direction
of slip within the fault plane measured counter-clockwise from the
strike direction (when looking from the hanging-wall side).  Annotated
with the four end-member fault styles.

Original conceptual diagram (Aki & Richards 2002 §4.4 convention).
No copyrighted figure reproduced.

Output: assets/figures/fig_rake_convention.png
License: CC-BY 4.0 (this script).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})


def main(out_path: str = "assets/figures/fig_rake_convention.png") -> None:
    fig, ax = plt.subplots(figsize=(6.6, 6.6))
    R = 1.0

    # circle
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(R * np.cos(th), R * np.sin(th),
            color="#D55E00", lw=2.6)

    # cross axes (strike direction along x; rake measured CCW from strike)
    ax.plot([-R, R], [0, 0], color="#bbbbbb", lw=1.0)
    ax.plot([0, 0], [-R, R], color="#bbbbbb", lw=1.0)
    # 45-deg diagonals
    for ang in (45, 135, 225, 315):
        ax.plot([0, R * np.cos(np.deg2rad(ang))],
                [0, R * np.sin(np.deg2rad(ang))],
                color="#dddddd", lw=0.8, ls=":")

    # arrows at the four end-members (slip direction in fault plane,
    # rake measured from +x = strike, CCW)
    end_members = [
        (0,    "0°",    "left-lateral",   "#0072B2"),
        (90,   "90°",   "reverse",        "#D55E00"),
        (180,  "±180°", "right-lateral",  "#0072B2"),
        (-90,  "−90°",  "normal",         "#009E73"),
    ]
    for ang, lbl, kind, col in end_members:
        a = np.deg2rad(ang)
        ax.annotate("", xy=(0.78 * np.cos(a), 0.78 * np.sin(a)),
                    xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", lw=2.2,
                                     color=col, mutation_scale=18))
        ax.text(1.18 * np.cos(a), 1.18 * np.sin(a),
                f"{lbl}\n{kind}", color=col, ha="center", va="center",
                fontsize=12, fontweight="bold")

    # labelled diagonal angles
    diag_pts = [(45, "45°"), (135, "135°"), (-135, "−135°"), (-45, "−45°")]
    for ang, lbl in diag_pts:
        a = np.deg2rad(ang)
        ax.text(1.04 * np.cos(a), 1.04 * np.sin(a), lbl,
                ha="center", va="center", fontsize=10, color="#666666")

    # central indicator: strike points to the right
    ax.text(0, -0.25, "(rake λ measured CCW\nfrom strike direction)",
            ha="center", va="center", fontsize=10, style="italic",
            color="#444444")
    ax.annotate("strike", xy=(0.94, 0), xytext=(1.32, 0.12),
                arrowprops=dict(arrowstyle="->", color="#444444", lw=1.0),
                fontsize=10, color="#444444")

    ax.set_xlim(-1.55, 1.55); ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("Convention for the rake angle  λ", pad=14)

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    main()
