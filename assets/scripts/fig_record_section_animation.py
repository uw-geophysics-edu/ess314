"""
fig_record_section_animation.py

Scientific content: Animated illustration of how seismic waves radiate from
a hypocenter and arrive at successive seismic stations placed at increasing
hypocentral distance. Three phases — P, S, and Rayleigh-type surface waves —
arrive in time order, and the time gap between P and S grows linearly with
distance, which is the foundation of single-station hypocentral-distance
estimation.

Reproduces the scientific content of:
  Stein, S. & Wysession, M. (2003). An Introduction to Seismology, Earthquakes,
  and Earth Structure. Blackwell. Figs. 1.1-3 and 1.1-4 (P/S/surface arrival
  windows on a single seismogram).

  Lowrie, W. & Fichtner, A. (2020). Fundamentals of Geophysics, 3rd ed.
  Cambridge University Press. Ch. 4 (seismograms and phase identification).

This figure is generated entirely from synthetic waveforms and analytic
arrival-time relations — no data are reproduced from those sources.

Output:
  assets/figures/fig_record_section_animation.gif
  assets/figures/fig_record_section_animation_final.png

License: CC-BY 4.0 (this script and its outputs).
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import animation, patches

# ── Global rcParams (mandatory at top of every figure script) ────────────
mpl.rcParams.update({
    "font.size": 13,
    "axes.titlesize": 15,
    "axes.labelsize": 13,
    "xtick.labelsize": 12,
    "ytick.labelsize": 12,
    "legend.fontsize": 11,
    "figure.dpi": 130,
    "savefig.dpi": 200,
})

# Colorblind-safe WCAG AA palette
COLOR_P = "#0072B2"          # blue — P-wave
COLOR_S = "#E69F00"          # orange — S-wave
COLOR_SURF = "#CC79A7"       # pink — surface wave
COLOR_FAULT = "#000000"      # black — fault line
COLOR_FOCUS = "#D55E00"      # vermilion — focus star
COLOR_STATION = "#009E73"    # green — station triangle
COLOR_GROUND = "#9D9D9D"     # neutral ground tint

# ── Physical setup ───────────────────────────────────────────────────────
# Velocities consistent with continental crust (km/s).
V_P = 6.0
V_S = V_P / np.sqrt(3.0)        # Poisson solid → ~3.46 km/s
V_R = 0.92 * V_S                # Rayleigh wave ≈ 0.92 V_S

# Source location and station distances along the surface
focus_x = 0.0          # km
focus_z = 8.0          # km, depth (positive downward)
station_dx = np.array([20.0, 50.0, 90.0, 140.0])    # km, epicentral distance

# Hypocentral distance (slant range from focus to each station)
hypo_dist = np.sqrt(station_dx**2 + focus_z**2)
n_sta = len(station_dx)

# Arrival times at each station (s)
t_P = hypo_dist / V_P
t_S = hypo_dist / V_S
# Rayleigh waves travel along the surface at V_R; treat surface path ≈ epicentral distance
t_surf = station_dx / V_R

# Record duration to display (s) — long enough for surface wave at the farthest station
t_max = float(np.ceil(t_surf.max() + 8.0))
t_axis = np.linspace(0.0, t_max, 4000)

# ── Synthetic waveform generation ────────────────────────────────────────
def ricker(t, t0, fdom):
    """Zero-phase Ricker wavelet centred at t0, dominant frequency fdom (Hz)."""
    arg = (np.pi * fdom * (t - t0)) ** 2
    return (1.0 - 2.0 * arg) * np.exp(-arg)


def build_seismogram(t, tP, tS, tR, dist):
    """Synthesise a 1-component seismogram for one station.

    Amplitudes follow a simple geometric-spreading scaling: body waves ~ 1/r,
    surface waves ~ 1/sqrt(r). These are stylised, not rigorous.
    """
    body_amp = 80.0 / dist
    p = 1.0 * body_amp * ricker(t, tP, 1.5)            # P pulse
    s = 1.6 * body_amp * ricker(t, tS, 0.9)            # S pulse, lower freq
    surf_amp = 90.0 / np.sqrt(max(dist, 1.0))
    # Surface wave: longer-period dispersive train, simplified as a windowed cosine
    env = np.exp(-((t - tR - 4.0) / 4.0) ** 2)
    surf = surf_amp * env * np.cos(2 * np.pi * 0.18 * (t - tR))
    # Background noise floor
    rng = np.random.default_rng(int(dist * 1000))
    noise = 0.03 * body_amp * rng.standard_normal(t.size)
    return p + s + surf + noise


seismograms = [build_seismogram(t_axis, t_P[i], t_S[i], t_surf[i], hypo_dist[i])
               for i in range(n_sta)]

# Vertical offset between traces in the record section
trace_spacing = max(np.max(np.abs(s)) for s in seismograms) * 2.6

# ── Figure layout: top panel = cross-section (animated wavefronts);
#                  bottom panel = record section (built up frame by frame)
# Stacked vertical layout: cross-section is short and wide (equal aspect, so
# wavefronts remain circular), record section is taller for the four traces.
fig = plt.figure(figsize=(13.5, 9.2))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 2.4], hspace=0.30)
ax_xs = fig.add_subplot(gs[0, 0])
ax_rs = fig.add_subplot(gs[1, 0])

# ── Cross-section panel ──────────────────────────────────────────────────
xs_xmin, xs_xmax = -25.0, 165.0
xs_zmin, xs_zmax = -7.0, 30.0     # negative "depth" above z=0 leaves room for labels
ax_xs.set_xlim(xs_xmin, xs_xmax)
ax_xs.set_ylim(xs_zmax, xs_zmin)         # z=30 at bottom, z=-7 at top
ax_xs.set_xlabel("Horizontal distance from epicenter (km)")
ax_xs.set_ylabel("Depth (km)\n[positive down]", fontsize=11)
ax_xs.set_title("Cross-section: wavefronts radiate outward from the focus",
                fontsize=14, pad=10)
# Equal aspect keeps wavefronts circular (physically correct). The wide
# horizontal range × short vertical range produces a thin strip layout.
ax_xs.set_aspect("equal")
ax_xs.set_yticks([0, 10, 20, 30])     # only label positive depths; air band is unlabeled

# Ground (sky / earth shading for accessibility — not relied on as sole encoding)
ax_xs.axhspan(0.0, xs_zmax, color="#F4EFE6", zorder=0)
ax_xs.axhspan(xs_zmin, 0.0, color="#FBFBFB", zorder=0)
ax_xs.axhline(0.0, color=COLOR_FAULT, lw=1.4, zorder=2)

# Fault line (dashed) through the focus
fault_xs = np.array([focus_x - 8, focus_x + 8])
fault_zs = np.array([focus_z + 12, focus_z - 12])
ax_xs.plot(fault_xs, fault_zs, color=COLOR_FAULT, ls="--", lw=1.6,
           zorder=3, label="Fault")

# Focus marker
ax_xs.plot(focus_x, focus_z, marker="*", color=COLOR_FOCUS, ms=18,
           mec=COLOR_FAULT, mew=0.8, zorder=5, label="Focus (hypocenter)")
# Epicenter (vertical projection to surface)
ax_xs.plot(focus_x, 0.0, marker="o", mec=COLOR_FAULT, mfc="white", ms=9,
           mew=1.4, zorder=5, label="Epicenter")
ax_xs.annotate("", xy=(focus_x, 0.0), xytext=(focus_x, focus_z - 0.5),
               arrowprops=dict(arrowstyle="-|>", color=COLOR_FAULT, lw=1.0),
               zorder=4)

# Stations as triangles on the surface, with labels in the air space above
for i, dx in enumerate(station_dx):
    ax_xs.plot(dx, 0.0, marker="^", color=COLOR_STATION, ms=14,
               mec=COLOR_FAULT, mew=0.8, zorder=6,
               label="Station" if i == 0 else None)
    ax_xs.annotate(f"S{i+1}  Δ={int(dx)} km",
                   xy=(dx, 0.0), xytext=(dx, -3.0),
                   ha="center", va="center", fontsize=10.5,
                   bbox=dict(facecolor="white", edgecolor="none",
                             alpha=0.85, boxstyle="round,pad=0.18"))

ax_xs.legend(loc="lower right", framealpha=0.95)

# Wavefronts: circles centred on focus that expand with frame number.
# Surface wave is generated only along the surface — we'll render it as a
# horizontal "streak" emanating from the epicenter outward in both directions.
wf_P = patches.Circle((focus_x, focus_z), radius=0.0, fill=False,
                      edgecolor=COLOR_P, lw=2.4, zorder=4, label="P wavefront")
wf_S = patches.Circle((focus_x, focus_z), radius=0.0, fill=False,
                      edgecolor=COLOR_S, lw=2.4, ls=(0, (5, 2)), zorder=4,
                      label="S wavefront")
ax_xs.add_patch(wf_P)
ax_xs.add_patch(wf_S)

# Surface-wave "lobes": two short line segments expanding along the surface
surf_left, = ax_xs.plot([], [], color=COLOR_SURF, lw=3.5, solid_capstyle="round",
                         zorder=4, label="Surface wave")
surf_right, = ax_xs.plot([], [], color=COLOR_SURF, lw=3.5, solid_capstyle="round",
                         zorder=4)

# Time annotation in cross-section
time_label = ax_xs.text(0.02, 0.05, "", transform=ax_xs.transAxes,
                        ha="left", va="bottom",
                        fontsize=14, fontweight="bold",
                        bbox=dict(facecolor="white", edgecolor=COLOR_FAULT,
                                  alpha=0.92, boxstyle="round,pad=0.35"))

# Add wavefront items to legend manually (otherwise patches.Circle is awkward)
from matplotlib.lines import Line2D
extra_handles = [
    Line2D([0], [0], color=COLOR_P, lw=2.4, label="P wavefront"),
    Line2D([0], [0], color=COLOR_S, lw=2.4, ls=(0, (5, 2)), label="S wavefront"),
    Line2D([0], [0], color=COLOR_SURF, lw=3.5, label="Surface wave"),
]
existing_handles, existing_labels = ax_xs.get_legend_handles_labels()
# De-duplicate while preserving order
seen = set()
combined = []
for h, lab in list(zip(existing_handles, existing_labels)) + \
             [(h, h.get_label()) for h in extra_handles]:
    if lab not in seen:
        combined.append((h, lab))
        seen.add(lab)
ax_xs.legend([c[0] for c in combined], [c[1] for c in combined],
             loc="center left", bbox_to_anchor=(1.02, 0.5),
             framealpha=0.95, fontsize=10, borderaxespad=0.0)

# ── Record-section panel ─────────────────────────────────────────────────
ax_rs.set_xlim(0.0, t_max)
ax_rs.set_ylim(-trace_spacing, n_sta * trace_spacing + trace_spacing * 0.4)
ax_rs.set_xlabel("Time since origin (s)")
ax_rs.set_yticks([i * trace_spacing for i in range(n_sta)])
ax_rs.set_yticklabels([f"S{i+1}\nΔ={int(station_dx[i])} km" for i in range(n_sta)],
                      fontsize=11)
ax_rs.set_title("Record section: arrivals at each station")
ax_rs.grid(True, color="#DDDDDD", lw=0.6, zorder=0)

# Pre-create line objects for each seismogram (initially empty)
trace_lines = []
for i in range(n_sta):
    line, = ax_rs.plot([], [], color="#222222", lw=1.0, zorder=3)
    trace_lines.append(line)

# Pre-create vertical pick markers for P, S, surface — drawn when revealed
pick_markers = {ph: [] for ph in ("P", "S", "surf")}
for i in range(n_sta):
    yc = i * trace_spacing
    yh = trace_spacing * 0.45
    p_ln, = ax_rs.plot([], [], color=COLOR_P, lw=2.0, zorder=4)
    s_ln, = ax_rs.plot([], [], color=COLOR_S, lw=2.0, ls=(0, (5, 2)), zorder=4)
    r_ln, = ax_rs.plot([], [], color=COLOR_SURF, lw=2.0, ls=(0, (1, 1.5)), zorder=4)
    pick_markers["P"].append(p_ln)
    pick_markers["S"].append(s_ln)
    pick_markers["surf"].append(r_ln)

# Travel-time guide curves on the record section
guide_x = np.linspace(0, station_dx.max() * 1.05, 100)
guide_dist_arr = np.linspace(0, hypo_dist.max() * 1.05, 100)
# In record-section coordinates, y = trace_spacing * station_index
# but station_index isn't continuous. Instead, map travel time to y by linear
# interpolation between the integer-indexed station rows.
# Simpler: just plot a thin guide line connecting the P, S picks across stations.
guide_P_x = t_P
guide_S_x = t_S
guide_R_x = t_surf
guide_y = np.arange(n_sta) * trace_spacing
guide_P_line, = ax_rs.plot([], [], color=COLOR_P, lw=1.0, alpha=0.4, zorder=2)
guide_S_line, = ax_rs.plot([], [], color=COLOR_S, lw=1.0, alpha=0.4, zorder=2)
guide_R_line, = ax_rs.plot([], [], color=COLOR_SURF, lw=1.0, alpha=0.4, zorder=2)

# Phase legend on record-section panel
rs_legend_handles = [
    Line2D([0], [0], color=COLOR_P, lw=2.0, label="P arrival"),
    Line2D([0], [0], color=COLOR_S, lw=2.0, ls=(0, (5, 2)), label="S arrival"),
    Line2D([0], [0], color=COLOR_SURF, lw=2.0, ls=(0, (1, 1.5)),
           label="Surface-wave start"),
]
ax_rs.legend(handles=rs_legend_handles, loc="upper right", fontsize=10,
             framealpha=0.95)

# ── Animation logic ──────────────────────────────────────────────────────
# Frame schedule. Total simulated time = t_max. We use ~80 frames so the GIF
# is compact. Each frame advances the simulation clock by t_max / (N - 1).
N_FRAMES = 80
frame_times = np.linspace(0.0, t_max, N_FRAMES)


def init():
    wf_P.set_radius(0.0)
    wf_S.set_radius(0.0)
    surf_left.set_data([], [])
    surf_right.set_data([], [])
    time_label.set_text("")
    for ln in trace_lines:
        ln.set_data([], [])
    for key in ("P", "S", "surf"):
        for ln in pick_markers[key]:
            ln.set_data([], [])
    guide_P_line.set_data([], [])
    guide_S_line.set_data([], [])
    guide_R_line.set_data([], [])
    return [wf_P, wf_S, surf_left, surf_right, time_label,
            *trace_lines, *pick_markers["P"], *pick_markers["S"],
            *pick_markers["surf"], guide_P_line, guide_S_line, guide_R_line]


def update(frame_idx):
    t_now = frame_times[frame_idx]

    # Expand wavefronts in the cross-section
    wf_P.set_radius(V_P * t_now)
    # S wavefront only grows after a slight delay so the lag is visible
    wf_S.set_radius(max(V_S * t_now, 0.0))

    # Surface-wave streaks along the surface (z = 0). Surface waves are
    # generated when the rupture reaches the surface; we approximate as
    # spreading from the epicenter at t = 0.
    surf_extent = V_R * t_now
    if surf_extent > 0:
        surf_left.set_data([focus_x - surf_extent, focus_x], [0, 0])
        surf_right.set_data([focus_x, focus_x + surf_extent], [0, 0])
    else:
        surf_left.set_data([], [])
        surf_right.set_data([], [])

    time_label.set_text(f"t = {t_now:5.1f} s")

    # Build up each station's seismogram up to t_now, vertically offset
    for i, ln in enumerate(trace_lines):
        mask = t_axis <= t_now
        y = i * trace_spacing + seismograms[i] * mask
        ln.set_data(t_axis[mask], y[mask])

        # Reveal P, S, surface-wave pick markers as their times pass
        yc = i * trace_spacing
        yh = trace_spacing * 0.5
        if t_now >= t_P[i]:
            pick_markers["P"][i].set_data([t_P[i], t_P[i]], [yc - yh, yc + yh])
        if t_now >= t_S[i]:
            pick_markers["S"][i].set_data([t_S[i], t_S[i]], [yc - yh, yc + yh])
        if t_now >= t_surf[i]:
            pick_markers["surf"][i].set_data([t_surf[i], t_surf[i]],
                                              [yc - yh, yc + yh])

    # Travel-time guide lines update incrementally — show only the segments
    # whose endpoints are already revealed
    revealed_P = [i for i in range(n_sta) if t_now >= t_P[i]]
    revealed_S = [i for i in range(n_sta) if t_now >= t_S[i]]
    revealed_R = [i for i in range(n_sta) if t_now >= t_surf[i]]
    if len(revealed_P) >= 2:
        guide_P_line.set_data(t_P[revealed_P], guide_y[revealed_P])
    if len(revealed_S) >= 2:
        guide_S_line.set_data(t_S[revealed_S], guide_y[revealed_S])
    if len(revealed_R) >= 2:
        guide_R_line.set_data(t_surf[revealed_R], guide_y[revealed_R])

    return [wf_P, wf_S, surf_left, surf_right, time_label,
            *trace_lines, *pick_markers["P"], *pick_markers["S"],
            *pick_markers["surf"], guide_P_line, guide_S_line, guide_R_line]


anim = animation.FuncAnimation(
    fig, update, frames=N_FRAMES, init_func=init,
    interval=180, blit=False, repeat=True, repeat_delay=1500,
)

# ── Output ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import os
    os.makedirs("assets/figures", exist_ok=True)
    out_gif = "assets/figures/fig_record_section_animation.gif"
    out_png = "assets/figures/fig_record_section_animation_final.png"

    # Render the static "informative frame" — pick a moment where all three
    # wavefronts are simultaneously visible inside the panel. A good choice
    # is when the P-wavefront has passed S2 but not yet reached S4: at this
    # instant, S1 and S2 already show full P+S+surface arrivals on the
    # record section while S3, S4 still show only the noise floor or the
    # earliest P pulse. This makes the propagation pedagogically obvious.
    informative_t = (t_P[1] + t_P[2]) / 2.0   # midway between P-arrivals at S2 and S3
    informative_frame = int(np.argmin(np.abs(frame_times - informative_t)))
    update(informative_frame)
    fig.savefig(out_png, dpi=200, bbox_inches="tight")
    print(f"Saved static informative frame (t = {frame_times[informative_frame]:.1f} s):"
          f" {out_png}")

    # Now render the animation
    anim.save(out_gif, writer="pillow", fps=8, dpi=110)
    print(f"Saved animation: {out_gif}")
