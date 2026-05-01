"""
fig_fault_geometry.py

Scientific content: definitions of strike, dip, and rake — the three
angles that fix the orientation of a fault plane and the direction of
slip within it.  Shows a dipping fault block in 3-D with the strike
line, dip angle, and rake angle (slip vector) annotated.

Reproduces the conceptual content of standard textbook fault-geometry
diagrams (cf. Stein & Wysession 2003 Fig 4.2-3; Aki & Richards 2002
Fig 4.20).  No copyrighted figure reproduced.

Output: assets/figures/fig_fault_geometry.png
License: CC-BY 4.0 (this script).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d.proj3d import proj_transform

mpl.rcParams.update({
    "font.size": 13, "axes.titlesize": 14, "axes.labelsize": 12,
    "xtick.labelsize": 11, "ytick.labelsize": 11,
    "figure.dpi": 150, "savefig.dpi": 300,
})


class Arrow3D(FancyArrowPatch):
    """Small helper to draw 3-D arrows."""
    def __init__(self, x0, y0, z0, dx, dy, dz, *args, **kw):
        super().__init__((0, 0), (0, 0), *args, **kw)
        self._verts3d = (x0, x0 + dx), (y0, y0 + dy), (z0, z0 + dz)

    def do_3d_projection(self, renderer=None):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, _ = proj_transform(xs3d, ys3d, zs3d, self.axes.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        return min(zs3d)


def main(out_path: str = "assets/figures/fig_fault_geometry.png") -> None:
    fig = plt.figure(figsize=(7.5, 6.5))
    ax = fig.add_subplot(111, projection="3d")

    # Coordinates: x = East, y = North, z = Up
    # Fault: strikes N30E (phi_s = 30 deg from North, clockwise),
    #        dips 50 deg to the east (delta = 50 deg).
    # Slip rake: lambda = 60 deg (oblique reverse-right-lateral).
    phi_s = np.deg2rad(30.0)   # strike
    delta = np.deg2rad(50.0)   # dip
    lam   = np.deg2rad(60.0)   # rake

    # Strike unit vector (along fault trace, on horizontal surface)
    s_hat = np.array([np.sin(phi_s), np.cos(phi_s), 0.0])
    # Down-dip unit vector (in fault plane, perpendicular to strike, pointing
    # into the hanging-wall side and downward)
    d_hat = np.array([np.cos(phi_s) * np.cos(delta),
                      -np.sin(phi_s) * np.cos(delta),
                      -np.sin(delta)])
    # Slip unit vector (rake measured in fault plane from strike toward
    # down-dip; sign flipped so positive lambda is reverse / hanging-wall up)
    u_hat = np.cos(lam) * s_hat - np.sin(lam) * d_hat

    # ------- Draw a horizontal "ground surface" reference plane -------
    L = 1.6
    surf_pts = np.array([[-L, -L, 0], [L, -L, 0], [L, L, 0], [-L, L, 0]])
    surf = Poly3DCollection([surf_pts], facecolors="#e8e8e8",
                            edgecolors="#888888", lw=0.7, alpha=0.55)
    ax.add_collection3d(surf)

    # ------- Draw the fault rectangle ---------------------------------
    # Two corners on the surface (along strike, +/- L*s_hat); two below
    # (down-dip, +/- L*s_hat + 1.4*d_hat)
    Lstrike = 1.0
    Ldip = 1.1
    corners = np.array([
         Lstrike * s_hat,
        -Lstrike * s_hat,
        -Lstrike * s_hat + Ldip * d_hat,
         Lstrike * s_hat + Ldip * d_hat,
    ])
    fault = Poly3DCollection([corners], facecolors="#FFB97A",
                             edgecolors="black", lw=1.6, alpha=0.85)
    ax.add_collection3d(fault)

    # ------- Strike line (intersection with surface) ------------------
    p_s0 = -Lstrike * s_hat
    p_s1 =  Lstrike * s_hat
    ax.plot([p_s0[0], p_s1[0]], [p_s0[1], p_s1[1]],
            [p_s0[2], p_s1[2]], color="#009E73", lw=3.5)
    ax.text(p_s1[0] + 0.06, p_s1[1] + 0.06, p_s1[2] + 0.04,
            "strike", color="#009E73", fontweight="bold", fontsize=12)

    # North reference arrow at origin
    arr_N = Arrow3D(0, 0, 0, 0, 0.65, 0,
                    arrowstyle="-|>", mutation_scale=14, lw=1.5,
                    color="#0072B2")
    ax.add_artist(arr_N)
    ax.text(0, 0.72, 0.05, "N", color="#0072B2", fontsize=12,
            fontweight="bold")

    # ------- Strike angle arc (phi from N to strike line, in plane z=0)
    arc_th = np.linspace(np.pi/2 - phi_s, np.pi/2, 40)  # from +x to N is
    # not what we want; we want from N (90 deg in math sense) sweeping
    # clockwise (decreasing math angle) to the strike azimuth.
    arc_th = np.linspace(np.pi/2, np.pi/2 - phi_s, 40)
    r_arc = 0.45
    arc_x = r_arc * np.cos(arc_th)
    arc_y = r_arc * np.sin(arc_th)
    ax.plot(arc_x, arc_y, np.zeros_like(arc_x),
            color="#0072B2", lw=1.6)
    ax.text(0.16, 0.45, 0.02, r"$\phi_s$", color="#0072B2",
            fontsize=14, fontweight="bold")

    # ------- Dip angle arc (delta) ----------------------------------
    # In the vertical plane perpendicular to strike, sweep from horizontal
    # (perpendicular-to-strike on surface) down to the down-dip direction.
    n_horiz = np.array([np.cos(phi_s), -np.sin(phi_s), 0.0])  # horiz, perp to strike
    arc_del = np.linspace(0, delta, 30)
    r_d = 0.35
    arc_pts = (r_d * np.cos(arc_del[:, None]) * n_horiz
               + r_d * np.sin(arc_del[:, None]) * np.array([0, 0, -1]))
    ax.plot(arc_pts[:, 0], arc_pts[:, 1], arc_pts[:, 2],
            color="#D55E00", lw=1.6)
    mid = arc_pts[len(arc_pts) // 2]
    ax.text(mid[0] + 0.08, mid[1] - 0.04, mid[2] - 0.05,
            r"$\delta$", color="#D55E00", fontsize=14, fontweight="bold")

    # ------- Slip vector ---------------------------------------------
    p_origin = 0.05 * d_hat  # tiny offset onto the fault face
    arr_u = Arrow3D(p_origin[0], p_origin[1], p_origin[2],
                    0.85 * u_hat[0], 0.85 * u_hat[1], 0.85 * u_hat[2],
                    arrowstyle="-|>", mutation_scale=18, lw=2.4,
                    color="#CC79A7")
    ax.add_artist(arr_u)
    end = p_origin + 0.95 * u_hat
    ax.text(end[0] + 0.04, end[1] + 0.04, end[2] + 0.06,
            r"$\vec{u}$ (slip)", color="#CC79A7",
            fontsize=12, fontweight="bold")

    # ------- Rake arc (from strike direction within the fault plane) --
    arc_rake = np.linspace(0, lam, 30)
    r_r = 0.35
    arc_pts2 = (r_r * np.cos(arc_rake[:, None]) * s_hat
                - r_r * np.sin(arc_rake[:, None]) * d_hat)
    ax.plot(arc_pts2[:, 0], arc_pts2[:, 1], arc_pts2[:, 2],
            color="#CC79A7", lw=1.6)
    mid2 = arc_pts2[len(arc_pts2) // 2]
    ax.text(mid2[0] + 0.08, mid2[1] + 0.02, mid2[2] - 0.04,
            r"$\lambda$", color="#CC79A7", fontsize=14, fontweight="bold")

    # ------- Cosmetics -------------------------------------------------
    ax.set_xlim(-L, L); ax.set_ylim(-L, L); ax.set_zlim(-L * 0.8, 0.5)
    ax.set_box_aspect((1, 1, 0.55))
    ax.set_xlabel("East"); ax.set_ylabel("North"); ax.set_zlabel("Up")
    ax.set_title(r"Fault geometry: strike $\phi_s$, dip $\delta$, "
                 r"rake $\lambda$")
    ax.view_init(elev=22, azim=-55)

    # Legend: colored swatches in a text block
    legend_txt = (
        r"$\phi_s$ — strike (azimuth, 0–360° from N, CW)" "\n"
        r"$\delta$ — dip (0–90°, fault plane below horizontal)" "\n"
        r"$\lambda$ — rake (slip direction in fault plane,"
        r"  0=left-lateral, 90=reverse, ±180=right-lateral, −90=normal)"
    )
    ax.text2D(0.02, 0.97, legend_txt, transform=ax.transAxes,
              fontsize=10, va="top",
              bbox=dict(boxstyle="round,pad=0.5", fc="white",
                        ec="#bbbbbb"))

    fig.tight_layout()
    fig.savefig(out_path, dpi=300, bbox_inches="tight")
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    main()
