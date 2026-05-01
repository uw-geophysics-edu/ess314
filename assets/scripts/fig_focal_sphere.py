"""
fig_focal_sphere.py

Scientific content: how a 3-D focal sphere — an imaginary small sphere
centered on the earthquake source — is reduced to the familiar 2-D
"beach ball" by lower-hemisphere stereographic projection.  The figure
shows three stages: full sphere with the two nodal planes, the lower
hemisphere only, and the projected map (the beach ball).

Reproduces (and replaces) the conceptual content of:
  Plummer, McGeary & Carlson (2003). Physical Geology, 9th ed. W.W.
  Norton.  Figs 7.13-7.15.  (Copyrighted; not reproduced.)

Output: assets/figures/fig_focal_sphere.png
License: CC-BY 4.0 (this script).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from matplotlib.patches import Wedge, Circle

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "legend.fontsize": 11, "figure.dpi": 150, "savefig.dpi": 300,
})

C_PUSH = "#D55E00"
C_PULL = "#FFFFFF"
C_FAULT = "#000000"


def main(out_path: str = "assets/figures/fig_focal_sphere.png") -> None:
    fig = plt.figure(figsize=(13, 4.5))

    # ----------- Panel A: 3-D focal sphere with both nodal planes ----
    ax1 = fig.add_subplot(1, 3, 1, projection="3d")

    # Sphere wireframe
    u, v = np.mgrid[0:2*np.pi:60j, 0:np.pi:30j]
    xs = np.cos(u) * np.sin(v)
    ys = np.sin(u) * np.sin(v)
    zs = np.cos(v)
    ax1.plot_wireframe(xs, ys, zs, color="#cccccc", lw=0.4, alpha=0.7)

    # Two nodal planes — vertical N-S fault plane + horizontal auxiliary
    # (purely conceptual, for vertical strike-slip)
    th = np.linspace(0, 2*np.pi, 80)
    # Fault plane: x = 0  (N-S striking, vertical)
    ax1.plot(np.zeros_like(th), np.cos(th), np.sin(th),
             color=C_FAULT, lw=2.4, label="Fault plane")
    # Auxiliary plane: z = 0 (horizontal)
    ax1.plot(np.cos(th), np.sin(th), np.zeros_like(th),
             color="#666666", lw=2.0, ls="--", label="Auxiliary plane")

    # Hypocenter
    ax1.scatter([0], [0], [0], color="#FFD700", s=120, edgecolors="black",
                zorder=10)

    # Light shading of compressional quadrants on the sphere surface
    # Compression for vertical right-lateral N-S fault, vertical aux plane?
    # Wait — for a strike-slip on vertical N-S fault with horizontal slip,
    # the auxiliary plane is also vertical (E-W).  For a horizontal aux
    # plane the slip is vertical, i.e. dip-slip on a vertical fault.
    # Pick instead a 45-deg dipping reverse fault for richer 3-D structure.
    # But simpler:  vertical strike-slip fault, vertical aux plane.
    # Re-draw aux plane vertical E-W
    ax1.lines[-1].remove()  # remove the horizontal aux just plotted
    ax1.plot(np.cos(th), np.zeros_like(th), np.sin(th),
             color="#666666", lw=2.0, ls="--", label="Auxiliary plane")

    ax1.set_xlim(-1.05, 1.05); ax1.set_ylim(-1.05, 1.05)
    ax1.set_zlim(-1.05, 1.05)
    ax1.set_box_aspect((1, 1, 1))
    ax1.set_xlabel("E"); ax1.set_ylabel("N"); ax1.set_zlabel("Up")
    ax1.set_title("(a) Focal sphere\n(both nodal planes)")
    ax1.view_init(elev=18, azim=35)
    ax1.legend(loc="upper left", fontsize=9, bbox_to_anchor=(0.0, 0.92))

    # ----------- Panel B: lower hemisphere only ----------------------
    ax2 = fig.add_subplot(1, 3, 2, projection="3d")
    # Filled lower hemisphere (z < 0) shading by quadrant
    nu, nv = 60, 25
    u_full = np.linspace(0, 2*np.pi, nu)
    v_low = np.linspace(np.pi/2, np.pi, nv)  # lower half only
    U, V = np.meshgrid(u_full, v_low)
    Xs = np.cos(U) * np.sin(V)
    Ys = np.sin(U) * np.sin(V)
    Zs = np.cos(V)

    # Compression quadrants (NE, SW): u in (0, pi/2) U (pi, 3pi/2)
    # azimuth = u (measured from east in spherical convention)
    # but our 'compression' is for x*y > 0  in this strike-slip example
    in_comp = (Xs * Ys) > 0
    color_arr = np.where(in_comp, 0.0, 1.0)  # 0 -> push (orange), 1 -> pull (white)

    from matplotlib.colors import ListedColormap
    cmap = ListedColormap([C_PUSH, "#ffffff"])
    ax2.plot_surface(Xs, Ys, Zs, facecolors=cmap(color_arr),
                     rstride=1, cstride=1, edgecolor="#bbbbbb",
                     linewidth=0.15, alpha=0.95, shade=False)

    # Equator (rim of bowl)
    th = np.linspace(0, 2*np.pi, 80)
    ax2.plot(np.cos(th), np.sin(th), np.zeros_like(th), "k-", lw=1.5)
    # nodal planes within lower hemisphere
    th_low = np.linspace(np.pi, 2*np.pi, 80)
    ax2.plot(np.zeros_like(th_low), np.cos(th_low), np.sin(th_low),
             color=C_FAULT, lw=2.4)
    ax2.plot(np.cos(th_low), np.zeros_like(th_low), np.sin(th_low),
             color="#666666", lw=2.0, ls="--")

    ax2.set_xlim(-1.05, 1.05); ax2.set_ylim(-1.05, 1.05)
    ax2.set_zlim(-1.05, 0.2)
    ax2.set_box_aspect((1, 1, 0.7))
    ax2.set_xlabel("E"); ax2.set_ylabel("N"); ax2.set_zlabel("Down")
    ax2.invert_zaxis()  # depth positive downward, but show Up at top
    ax2.set_title("(b) Lower hemisphere\n(rays leaving downward)")
    ax2.view_init(elev=14, azim=35)

    # ----------- Panel C: projected beach ball -----------------------
    ax3 = fig.add_subplot(1, 3, 3)
    R = 1.0
    # Compression NE & SW quadrants (right-lateral N-S vertical fault):
    ax3.add_patch(Wedge((0, 0), R, 0, 90, facecolor=C_PUSH,
                        edgecolor="black", lw=1.6))
    ax3.add_patch(Wedge((0, 0), R, 180, 270, facecolor=C_PUSH,
                        edgecolor="black", lw=1.6))
    ax3.add_patch(Circle((0, 0), R, fill=False, edgecolor="black", lw=1.6))
    # nodal planes
    ax3.plot([0, 0], [-R, R], color=C_FAULT, lw=2.4)
    ax3.plot([-R, R], [0, 0], color=C_FAULT, lw=2.4)

    # N tick
    ax3.annotate("", xy=(0, R + 0.18), xytext=(0, R + 0.05),
                 arrowprops=dict(arrowstyle="->", lw=1.5))
    ax3.text(0, R + 0.32, "N", ha="center", fontsize=12, fontweight="bold")
    # quadrant labels
    ax3.text(0.5, 0.5, "C", color="white", ha="center", va="center",
             fontsize=14, fontweight="bold")
    ax3.text(-0.5, -0.5, "C", color="white", ha="center", va="center",
             fontsize=14, fontweight="bold")
    ax3.text(-0.5, 0.5, "D", color=C_FAULT, ha="center", va="center",
             fontsize=14, fontweight="bold")
    ax3.text(0.5, -0.5, "D", color=C_FAULT, ha="center", va="center",
             fontsize=14, fontweight="bold")

    ax3.set_xlim(-1.4, 1.4); ax3.set_ylim(-1.4, 1.4)
    ax3.set_aspect("equal")
    ax3.set_xticks([]); ax3.set_yticks([])
    for s in ["top", "right", "bottom", "left"]:
        ax3.spines[s].set_visible(False)
    ax3.set_title("(c) Beach ball\n(map projection)")

    # Caption: C = compression, D = dilatation
    ax3.text(0, -1.65, "C = compression (filled)   "
                       "D = dilatation (white)",
             ha="center", fontsize=10, style="italic")

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    main()
