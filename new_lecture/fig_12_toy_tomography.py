"""
fig_12_toy_tomography.py

Scientific content: The simplest possible tomography problem - a 2x2
grid of cells, four ray paths (two horizontal, two vertical), and a
matrix equation d = G m that maps slownesses (model) to travel times
(data). Shows (a) the geometry, (b) the inversion of the true model
from noise-free data, and (c) how 1% gaussian noise on the data
propagates into the recovered model.

Reproduces the scientific content of:
  Stein, S. and Wysession, M., 2003. An Introduction to Seismology,
  Earthquakes and Earth Structure. Blackwell Publishing, Ch. 7.3
  (paywalled). Aster, R.C., Borchers, B., Thurber, C.H., 2018.
  Parameter Estimation and Inverse Problems, 3rd ed., Elsevier,
  Ch. 1 and Ch. 4. ISBN 9780128134238.

Output: assets/figures/fig_12_toy_tomography.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

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


def draw_grid(ax, slownesses, h=1.0, title="", cmap=None, norm=None):
    """Draw a 2x2 slowness grid with labels."""
    s = np.array(slownesses).reshape(2, 2)
    if cmap is None:
        cmap = mpl.cm.get_cmap("RdBu_r")
    if norm is None:
        vmin, vmax = 0.05, 0.25
        norm = mcolors.Normalize(vmin=vmin, vmax=vmax)

    for i in range(2):        # row: 0=top, 1=bottom
        for j in range(2):    # col: 0=left, 1=right
            x = j * h
            y = (1 - i) * h
            ax.add_patch(plt.Rectangle((x, y), h, h,
                                       facecolor=cmap(norm(s[i, j])),
                                       edgecolor=COLORS[6], lw=1.2))
            ax.text(x + h / 2, y + h / 2,
                    f"$s_{{{2 * i + j + 1}}}$\n{s[i, j]:.3f}",
                    ha="center", va="center", fontsize=11, color=COLORS[6])

    ax.set_xlim(-0.25, 2 * h + 0.25)
    ax.set_ylim(-0.25, 2 * h + 0.25)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(title, color=COLORS[6], fontsize=13)


def draw_geometry(ax, h=1.0):
    """Draw the 2x2 grid with labeled ray paths t1..t4."""
    # Cells
    for i in range(2):
        for j in range(2):
            x = j * h
            y = (1 - i) * h
            ax.add_patch(plt.Rectangle((x, y), h, h,
                                       facecolor="white",
                                       edgecolor=COLORS[6], lw=1.2))
            ax.text(x + h / 2, y + h / 2,
                    f"$s_{{{2 * i + j + 1}}}$",
                    ha="center", va="center", fontsize=15, color=COLORS[6])

    # Horizontal ray t1 through top row
    ax.annotate("", xy=(2 * h + 0.25, 1.5 * h), xytext=(-0.25, 1.5 * h),
                arrowprops=dict(arrowstyle="->", color=COLORS[0], lw=2.0))
    ax.text(2 * h + 0.32, 1.5 * h, "$t_1$",
            fontsize=14, color=COLORS[0], va="center")
    # Horizontal ray t2 through bottom row
    ax.annotate("", xy=(2 * h + 0.25, 0.5 * h), xytext=(-0.25, 0.5 * h),
                arrowprops=dict(arrowstyle="->", color=COLORS[0], lw=2.0))
    ax.text(2 * h + 0.32, 0.5 * h, "$t_2$",
            fontsize=14, color=COLORS[0], va="center")
    # Vertical ray t3 through left column
    ax.annotate("", xy=(0.5 * h, -0.25), xytext=(0.5 * h, 2 * h + 0.25),
                arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=2.0))
    ax.text(0.5 * h, -0.40, "$t_3$",
            fontsize=14, color=COLORS[1], ha="center")
    # Vertical ray t4 through right column
    ax.annotate("", xy=(1.5 * h, -0.25), xytext=(1.5 * h, 2 * h + 0.25),
                arrowprops=dict(arrowstyle="->", color=COLORS[1], lw=2.0))
    ax.text(1.5 * h, -0.40, "$t_4$",
            fontsize=14, color=COLORS[1], ha="center")

    ax.set_xlim(-0.7, 2 * h + 0.7)
    ax.set_ylim(-0.7, 2 * h + 0.5)
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title("(a) Four rays, four cells\n$t_k = \\sum_i G_{ki}\\, s_i$",
                 color=COLORS[6], fontsize=13)


def main(outpath):
    # --- True slowness model: four cells, one slow anomaly (s2 = 0.20)
    # "True" slownesses in s/km (arbitrary units). Higher = slower.
    s_true = np.array([0.10, 0.20, 0.10, 0.10])  # s1, s2, s3, s4
    h = 1.0  # cell size

    # Forward operator G for 4 rays (t1..t4) and 4 cells (s1..s4)
    # t1 = s1*h + s2*h   (horizontal top)
    # t2 = s3*h + s4*h   (horizontal bottom)
    # t3 = s1*h + s3*h   (vertical left)
    # t4 = s2*h + s4*h   (vertical right)
    G = h * np.array([
        [1, 1, 0, 0],
        [0, 0, 1, 1],
        [1, 0, 1, 0],
        [0, 1, 0, 1],
    ], dtype=float)

    d_true = G @ s_true
    # Check determinant - G is singular (rank 3)
    # Damped least squares for uniqueness
    eps = 0.02
    I = np.eye(4)
    m_hat = np.linalg.solve(G.T @ G + eps**2 * I, G.T @ d_true)

    # Noisy data: 1% gaussian noise
    rng = np.random.default_rng(42)
    noise_level = 0.01 * np.mean(d_true)
    d_noisy = d_true + rng.normal(0.0, noise_level, size=4)
    m_noisy = np.linalg.solve(G.T @ G + eps**2 * I, G.T @ d_noisy)

    # Shared colour scale
    vmin, vmax = 0.05, 0.25
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap = mpl.cm.get_cmap("RdBu_r")

    fig = plt.figure(figsize=(15.0, 6.8))
    gs = fig.add_gridspec(1, 4, width_ratios=[1.0, 1.0, 1.0, 0.06],
                          wspace=0.35)

    ax_g = fig.add_subplot(gs[0, 0])
    draw_geometry(ax_g, h=h)

    ax_t = fig.add_subplot(gs[0, 1])
    draw_grid(ax_t, s_true, h=h, cmap=cmap, norm=norm,
              title=f"(b) True model\nt = G m (noise-free)")

    ax_r = fig.add_subplot(gs[0, 2])
    draw_grid(ax_r, m_noisy, h=h, cmap=cmap, norm=norm,
              title=f"(c) Damped inversion with 1% noise\n$\\varepsilon = {eps}$")

    # Shared colour bar
    ax_cb = fig.add_subplot(gs[0, 3])
    sm = mpl.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    cb = fig.colorbar(sm, cax=ax_cb)
    cb.set_label("slowness $s$ (s/km)", fontsize=11)

    # Side-annotation with the matrix form
    fig.text(0.27, 0.05,
             r"$\mathbf{d} = \mathbf{G}\,\mathbf{m}$    "
             r"$\mathbf{m} = (\mathbf{G}^T\mathbf{G} + "
             r"\varepsilon^2 \mathbf{I})^{-1}\mathbf{G}^T\,\mathbf{d}$",
             fontsize=14, color=COLORS[6], ha="center")

    fig.suptitle(
        "Toy tomography: a 2 x 2 cell grid illustrates the forward/inverse workflow",
        y=1.00, color=COLORS[6], fontsize=14,
    )
    fig.tight_layout()
    fig.savefig(outpath, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved: {outpath}")
    print("d_true =", d_true)
    print("d_noisy =", d_noisy)
    print("m_hat (noise-free) =", m_hat)
    print("m_noisy (1% noise) =", m_noisy)


if __name__ == "__main__":
    main("/home/claude/work/ess314/assets/figures/fig_12_toy_tomography.png")
