"""
fig_three_faults.py

Scientific content: the three end-member fault types — strike-slip,
normal, and reverse (thrust) — and the corresponding beach-ball focal
mechanism.  Each row shows: a 3-D block diagram with slip arrows, the
beach ball (lower-hemisphere stereographic projection), and the
characteristic plate-tectonic setting.

Reproduces (and replaces) the conceptual content of:
  Plummer, McGeary & Carlson (2003). Physical Geology, 9th ed.
  Figs 7.17 and 7.21.  W.W. Norton.  (Copyrighted; not reproduced.)

Output: assets/figures/fig_three_faults.png
License: CC-BY 4.0 (this script).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from obspy.imaging.beachball import beach

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})

# Colorblind-safe
HW_COLOR = "#FFB97A"   # hanging wall
FW_COLOR = "#cccccc"   # foot wall
ARROW_COLOR = "#000000"

# Fault parameters (strike, dip, rake) for ObsPy beachball
FAULTS = [
    ("Strike-slip (right-lateral)", (0.0, 90.0, 180.0),
     "Transform plate boundaries\n(San Andreas, North Anatolian)"),
    ("Normal",                      (90.0, 60.0, -90.0),
     "Divergent plate boundaries\n(rifts, mid-ocean ridges)"),
    ("Reverse (thrust)",            (90.0, 30.0, 90.0),
     "Convergent plate boundaries\n(subduction zones, fold-and-thrust belts)"),
]


def draw_block(ax, fault_kind):
    """Draw a half-block with a fault and slip arrows."""
    L = 1.0; H = 0.55
    # Two simple rectangular prisms split by a fault plane.
    # 'strike-slip', 'normal', 'reverse' are the three kinds.
    if fault_kind == "ss":
        # Vertical fault, blocks slide horizontally
        # Left block (back)
        L1 = np.array([[-L, 0, 0], [0, 0, 0], [0, 0, H], [-L, 0, H]])
        L2 = np.array([[-L, 0, 0], [0, 0, 0], [0, -L, 0], [-L, -L, 0]])
        L3 = np.array([[-L, 0, 0], [-L, -L, 0], [-L, -L, H], [-L, 0, H]])
        L4 = np.array([[-L, -L, 0], [0, -L, 0], [0, -L, H], [-L, -L, H]])
        L5 = np.array([[-L, 0, H], [0, 0, H], [0, -L, H], [-L, -L, H]])

        # Right block (front), shifted in y by 0.0 (visualize same height)
        R1 = np.array([[0, 0, 0], [L, 0, 0], [L, 0, H], [0, 0, H]])
        R2 = np.array([[0, 0, 0], [L, 0, 0], [L, -L, 0], [0, -L, 0]])
        R3 = np.array([[L, 0, 0], [L, -L, 0], [L, -L, H], [L, 0, H]])
        R4 = np.array([[0, -L, 0], [L, -L, 0], [L, -L, H], [0, -L, H]])
        R5 = np.array([[0, 0, H], [L, 0, H], [L, -L, H], [0, -L, H]])

        for poly, c in zip([L1, L2, L3, L4, L5], [HW_COLOR]*5):
            ax.add_collection3d(Poly3DCollection([poly],
                                facecolors=c, edgecolors="k", lw=0.6, alpha=0.9))
        for poly, c in zip([R1, R2, R3, R4, R5], [FW_COLOR]*5):
            ax.add_collection3d(Poly3DCollection([poly],
                                facecolors=c, edgecolors="k", lw=0.6, alpha=0.9))
        # Slip arrows on top, parallel to fault (right block toward viewer = -y)
        ax.quiver(0.55, 0, H + 0.04, 0, -0.7, 0,
                  color=ARROW_COLOR, lw=2.0, arrow_length_ratio=0.18)
        ax.quiver(-0.55, -L, H + 0.04, 0, 0.7, 0,
                  color=ARROW_COLOR, lw=2.0, arrow_length_ratio=0.18)
        # right-lateral indicator on top
        ax.text(0.0, -0.5, H + 0.18, "right-lateral",
                color="black", fontsize=10, ha="center", fontweight="bold")

    elif fault_kind == "normal":
        # Dipping plane (60-deg dip toward +y), hanging wall slides DOWN
        # Define fault as plane y = (z) / tan(60deg)  -> z = tan(60deg)*y
        # Use two blocks separated by this plane
        # Hanging wall (in front of plane, i.e. y > z/tan(d)) drops down
        d = np.deg2rad(60)
        # Foot wall (back): trapezoid, full height
        FW = np.array([
            [-L, -L, 0], [L, -L, 0], [L, -L, H], [-L, -L, H],
            [-L, -L, 0], [-L, 0, 0], [-L, H/np.tan(d), H], [-L, -L, H]
        ])
        # Use simpler approach: just two right-angle prisms
        # Foot wall: behind plane; Hanging wall: in front, dropped by 0.15
        drop = 0.18
        # Foot wall block (y from -L to fault, full height)
        # For simplicity, draw a big rectangular foot wall and a dropped
        # smaller hanging wall in front, separated by the dipping plane.
        # Foot wall (back half)
        FW_polys = [
            [[-L, -L, 0], [L, -L, 0], [L, -L, H], [-L, -L, H]],     # back face
            [[-L, -L, 0], [-L, 0, 0], [-L, H/np.tan(d), H], [-L, -L, H]],  # left
            [[L, -L, 0], [L, 0, 0], [L, H/np.tan(d), H], [L, -L, H]],     # right
            [[-L, -L, 0], [L, -L, 0], [L, 0, 0], [-L, 0, 0]],            # bottom (truncated)
            [[-L, -L, H], [L, -L, H], [L, H/np.tan(d), H], [-L, H/np.tan(d), H]],  # top
            # fault face (down-dip, dipping into +y)
            [[-L, 0, 0], [L, 0, 0], [L, H/np.tan(d), H], [-L, H/np.tan(d), H]],
        ]
        for poly in FW_polys:
            ax.add_collection3d(Poly3DCollection([poly],
                                facecolors=FW_COLOR, edgecolors="k", lw=0.6,
                                alpha=0.9))

        # Hanging wall (dropped by 'drop' along z); fault plane is the same
        # Hanging wall is the prism in front (y from 0 to L), top dropped
        HW_polys = [
            [[-L, 0, 0 - drop], [L, 0, 0 - drop], [L, H/np.tan(d), H - drop], [-L, H/np.tan(d), H - drop]],  # fault face
            [[-L, L, 0 - drop], [L, L, 0 - drop], [L, L, H - drop], [-L, L, H - drop]],  # front
            [[-L, 0, 0 - drop], [-L, L, 0 - drop], [-L, L, H - drop], [-L, H/np.tan(d), H - drop]],  # left
            [[L, 0, 0 - drop], [L, L, 0 - drop], [L, L, H - drop], [L, H/np.tan(d), H - drop]],  # right
            [[-L, 0, 0 - drop], [L, 0, 0 - drop], [L, L, 0 - drop], [-L, L, 0 - drop]],  # bottom
            [[-L, H/np.tan(d), H - drop], [L, H/np.tan(d), H - drop],
             [L, L, H - drop], [-L, L, H - drop]],  # top
        ]
        for poly in HW_polys:
            ax.add_collection3d(Poly3DCollection([poly],
                                facecolors=HW_COLOR, edgecolors="k", lw=0.6,
                                alpha=0.9))

        # Slip arrow on hanging wall: down-dip
        ax.quiver(0, 0.05, 0.0, 0, 0.35, -0.55,
                  color=ARROW_COLOR, lw=2.0, arrow_length_ratio=0.20)
        ax.text(0.0, 0.2, -0.30, "extension",
                color="black", fontsize=10, ha="center", fontweight="bold")

    elif fault_kind == "reverse":
        # Same geometry but hanging wall is THRUST UP.  We can mirror the
        # 'normal' construction with hanging wall lifted instead of dropped.
        d = np.deg2rad(30)
        lift = 0.18
        FW_polys = [
            [[-L, -L, 0], [L, -L, 0], [L, -L, H], [-L, -L, H]],     # back face
            [[-L, -L, 0], [-L, 0, 0], [-L, H/np.tan(d), H], [-L, -L, H]],  # left
            [[L, -L, 0], [L, 0, 0], [L, H/np.tan(d), H], [L, -L, H]],     # right
            [[-L, -L, 0], [L, -L, 0], [L, 0, 0], [-L, 0, 0]],            # bottom
            [[-L, -L, H], [L, -L, H], [L, H/np.tan(d), H], [-L, H/np.tan(d), H]],  # top
            [[-L, 0, 0], [L, 0, 0], [L, H/np.tan(d), H], [-L, H/np.tan(d), H]],  # fault face
        ]
        for poly in FW_polys:
            ax.add_collection3d(Poly3DCollection([poly],
                                facecolors=FW_COLOR, edgecolors="k", lw=0.6,
                                alpha=0.9))
        # truncate the hanging-wall foot to fit in the dipping shallow geom
        HW_polys = [
            [[-L, 0, 0 + lift], [L, 0, 0 + lift], [L, H/np.tan(d), H + lift],
             [-L, H/np.tan(d), H + lift]],  # fault face
            [[-L, L, 0 + lift], [L, L, 0 + lift], [L, L, H + lift],
             [-L, L, H + lift]],  # front
            [[-L, 0, 0 + lift], [-L, L, 0 + lift], [-L, L, H + lift],
             [-L, H/np.tan(d), H + lift]],  # left
            [[L, 0, 0 + lift], [L, L, 0 + lift], [L, L, H + lift],
             [L, H/np.tan(d), H + lift]],  # right
            [[-L, 0, 0 + lift], [L, 0, 0 + lift], [L, L, 0 + lift],
             [-L, L, 0 + lift]],  # bottom
            [[-L, H/np.tan(d), H + lift], [L, H/np.tan(d), H + lift],
             [L, L, H + lift], [-L, L, H + lift]],  # top
        ]
        for poly in HW_polys:
            ax.add_collection3d(Poly3DCollection([poly],
                                facecolors=HW_COLOR, edgecolors="k", lw=0.6,
                                alpha=0.9))

        ax.quiver(0, 0.05, 0.05, 0, 0.35, +0.55,
                  color=ARROW_COLOR, lw=2.0, arrow_length_ratio=0.20)
        ax.text(0.0, 0.2, 0.65 + lift, "shortening",
                color="black", fontsize=10, ha="center", fontweight="bold")


def main(out_path: str = "assets/figures/fig_three_faults.png") -> None:
    fig = plt.figure(figsize=(13, 10))
    gs = fig.add_gridspec(3, 3, width_ratios=[1.4, 1.0, 1.4],
                          hspace=0.32, wspace=0.20)

    fkinds = ["ss", "normal", "reverse"]
    for i, ((name, sdr, ctx), fk) in enumerate(zip(FAULTS, fkinds)):
        # --- 3-D block diagram ---
        axB = fig.add_subplot(gs[i, 0], projection="3d")
        draw_block(axB, fk)
        axB.set_xlim(-1.05, 1.05); axB.set_ylim(-1.05, 1.05)
        axB.set_zlim(-0.25, 0.85)
        axB.set_box_aspect((1, 1, 0.7))
        axB.set_axis_off()
        axB.view_init(elev=22, azim=-55)
        axB.set_title(f"({chr(97 + i)}) {name}", y=0.98)

        # --- Beach ball ---
        axM = fig.add_subplot(gs[i, 1])
        bc = beach(list(sdr), xy=(0, 0), width=1.6,
                   facecolor="#D55E00", edgecolor="black", linewidth=1.6)
        axM.add_collection(bc)
        axM.set_xlim(-1.0, 1.0); axM.set_ylim(-1.0, 1.0)
        axM.set_aspect("equal")
        axM.set_xticks([]); axM.set_yticks([])
        for s in ["top", "right", "bottom", "left"]:
            axM.spines[s].set_visible(False)
        axM.set_title("Beach ball", fontsize=12)
        # Strike/dip/rake annotation
        axM.text(0, -1.10, fr"$\phi_s$={sdr[0]:.0f}°, "
                            fr"$\delta$={sdr[1]:.0f}°, "
                            fr"$\lambda$={sdr[2]:.0f}°",
                 ha="center", fontsize=11, style="italic")

        # --- Tectonic setting context box ---
        axT = fig.add_subplot(gs[i, 2])
        axT.set_xlim(0, 1); axT.set_ylim(0, 1)
        axT.axis("off")
        axT.text(0.0, 0.92, "Tectonic setting:", fontsize=12,
                 fontweight="bold", color="#333333")
        axT.text(0.0, 0.65, ctx, fontsize=12, va="top", color="#333333")
        # bullet points: stress regime + slip vector orientation
        if i == 0:
            extra = ("• Maximum compressive stress horizontal,\n"
                     "  at ~45° to the fault\n"
                     "• Slip vector horizontal\n"
                     "• Both nodal planes vertical")
        elif i == 1:
            extra = ("• Minimum compressive stress horizontal\n"
                     "• Slip vector down-dip\n"
                     "• Hanging wall moves down\n"
                     "• Beach ball: white centre, dark margins")
        else:
            extra = ("• Maximum compressive stress horizontal\n"
                     "• Slip vector up-dip\n"
                     "• Hanging wall moves up\n"
                     "• Beach ball: dark centre, white margins")
        axT.text(0.0, 0.30, extra, fontsize=10.5, va="top", color="#333333")

    fig.suptitle("Three end-member fault types and their focal mechanisms",
                 fontsize=15, y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.985))
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    main()
