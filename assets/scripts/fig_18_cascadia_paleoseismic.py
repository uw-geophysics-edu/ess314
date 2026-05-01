"""
fig_17_cascadia_paleoseismic.py

Scientific content: Timeline plot showing the Cascadia paleo-megathrust
record over the past 10,000 years, with vertical bars marking each of
the ~19 events identified by Goldfinger et al. 2012 from offshore turbidites
and corroborated by coastal-marsh sand layers (Atwater et al. 2015).
Annotations show the mean recurrence interval (~530 years), the time
since the last event (1700 AD = 326 years ago at the time of writing),
and the implied next-50-year probability.

Reproduces the qualitative content of legacy ESS 314 slides 36-38
(coastal sand deposits / Cascadia, turbidite map, paleoseismic timeline).

References:
  Goldfinger, C., et al. (2012). Turbidite event history -- methods and
    implications for Holocene paleoseismicity of the Cascadia subduction
    zone. USGS Professional Paper 1661-F. DOI: 10.3133/pp1661F.
  Atwater, B.F., Musumi-Rokkaku, S., Satake, K., Tsuji, Y., Ueda, K., &
    Yamaguchi, D.K. (2015). The Orphan Tsunami of 1700, 2nd ed. USGS
    Professional Paper 1707.

Output: assets/figures/fig_17_cascadia_paleoseismic.png
License: CC-BY 4.0 (this script)
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

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

COLORS = {
    "primary":   "#0072B2",  # blue
    "next":      "#D55E00",  # vermilion
    "secondary": "#56B4E9",
    "land":      "#A87344",
    "marker":    "#000000",
}

# Goldfinger 2012 turbidite chronology — calibrated calendar years BP
# Approximate values from PP 1661-F Table 4 (events T1 through T18).
# These are deliberately rounded for a teaching figure; the published
# values have ±50-100 yr uncertainties.
events_BP = [
    250,    # T1: AD 1700
    810,    # T2
    1130,   # T3
    1640,   # T4
    1970,   # T5
    2500,   # T6
    3050,   # T7
    3360,   # T8
    3850,   # T9
    4220,   # T10
    4700,   # T11
    5390,   # T12
    5870,   # T13
    6440,   # T14
    7250,   # T15
    7710,   # T16
    8380,   # T17
    9090,   # T18
    9800,   # T19
]
events_BP = np.array(events_BP)
# Convert BP (before 1950 AD) to calendar year AD/CE
# i.e. AD = 1950 - BP for BP > 0
events_AD = 1950 - events_BP
present = 2026
last_event = 1700  # AD: T1
years_since_last = present - last_event

# Compute recurrence intervals (differences between consecutive events)
recurrence = np.abs(np.diff(events_BP))
mean_rec = recurrence.mean()
std_rec = recurrence.std()

# ── Build figure ────────────────────────────────────────────────────
fig, axs = plt.subplots(2, 1, figsize=(13.5, 7.0),
                        gridspec_kw=dict(height_ratios=[3, 1], hspace=0.45))

ax = axs[0]
# Time axis: from 10,000 BP (= 8050 BC) to present
ax.set_xlim(-8100, 2050)
ax.set_ylim(0, 1)

# Draw the present day as a vertical line
ax.axvline(present, color=COLORS["next"], linewidth=2.5, alpha=0.7,
           label="Present (2026)")
ax.fill_betweenx([0, 1], last_event, present,
                 color=COLORS["next"], alpha=0.15)
ax.text(present + 50, 0.55, "TODAY", color=COLORS["next"],
        fontsize=12, fontweight="bold", va="center", ha="left")

# Draw event bars
for ad in events_AD:
    if ad == last_event:
        # Highlight the most recent event (1700) in vermilion
        ax.axvline(ad, color=COLORS["next"], linewidth=2.8,
                   ymin=0.05, ymax=0.85)
    else:
        ax.axvline(ad, color=COLORS["primary"], linewidth=2.0,
                   ymin=0.10, ymax=0.85, alpha=0.85)

# Label the 1700 event - place beneath the event line
ax.annotate("AD 1700\n(orphan tsunami)",
            xy=(last_event, 0.10),
            xytext=(last_event - 2200, 0.30),
            fontsize=11, color=COLORS["next"], fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=COLORS["next"], lw=1.2),
            bbox=dict(facecolor="white", edgecolor=COLORS["next"],
                      boxstyle="round,pad=0.3", alpha=0.95))

# Label the oldest event - place to the right of T19, in the middle
oldest = events_AD.min()
ax.annotate(f"~10 ka BP\n(T19)",
            xy=(oldest, 0.85),
            xytext=(oldest + 600, 0.65),
            fontsize=11, color=COLORS["primary"], fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=COLORS["primary"], lw=1.2),
            bbox=dict(facecolor="white", edgecolor=COLORS["primary"],
                      boxstyle="round,pad=0.3", alpha=0.95))

# Recurrence interval band
ax.text(0.02, 0.05, f"19 events in 10,000 years\n"
                    f"Mean recurrence: ~{mean_rec:.0f} years\n"
                    f"Std deviation:   ~{std_rec:.0f} years\n"
                    f"Range:           {recurrence.min()}-{recurrence.max()} years",
        transform=ax.transAxes, fontsize=11,
        bbox=dict(facecolor="#FFFFE0", edgecolor="#888888",
                  boxstyle="round,pad=0.5", alpha=0.95),
        va="bottom", ha="left", family="monospace")

# Source attribution
ax.text(0.98, 0.03,
        "Events from Goldfinger et al. 2012 (USGS PP 1661-F)\n"
        "and Atwater et al. 2015 (USGS PP 1707)",
        transform=ax.transAxes, fontsize=9,
        ha="right", va="bottom", style="italic", color="#555555")

ax.set_xlabel("Calendar year (AD/BC)")
ax.set_yticks([])
ax.set_title("(a) Cascadia megathrust events of the past 10,000 years")
# Don't add a legend — the AD 1700 and TODAY labels carry the meaning

# Tick formatting: show major calendar dates
ticks = [-8000, -6000, -4000, -2000, 0, 2000]
ax.set_xticks(ticks)
ax.set_xticklabels(["8000 BC", "6000 BC", "4000 BC", "2000 BC", "0",
                     "2000 AD"])

# ── BOTTOM: histogram of recurrence intervals ───────────────────────
ax2 = axs[1]
bins = np.arange(0, 1500, 100)
ax2.hist(recurrence, bins=bins, color=COLORS["primary"], alpha=0.75,
         edgecolor="black", linewidth=0.7)
ax2.axvline(mean_rec, color=COLORS["next"], linestyle="--", linewidth=2.0,
            label=f"Mean = {mean_rec:.0f} yr")
ax2.axvline(years_since_last, color="#000000", linestyle="-", linewidth=2.5,
            label=f"Time since 1700 = {years_since_last} yr")
ax2.set_xlabel("Recurrence interval (years)")
ax2.set_ylabel("Number of events")
ax2.set_title("(b) Distribution of recurrence intervals (n = 18)")
ax2.legend(fontsize=11, loc="upper right")
ax2.grid(alpha=0.3, axis="y")
# Set x-limit so we have room for the data and the legend
ax2.set_xlim(0, 1100)

# Add the implication — placed below the legend, on the right
ax2.text(0.99, 0.45,
         f"326-yr elapsed time sits near\n"
         "the mean of the distribution.\n"
         "Conditional probability of a Cascadia\n"
         "rupture in the next 50 years: ~10-15%\n"
         "(Wirth et al. 2025)",
         transform=ax2.transAxes, fontsize=10, ha="right", va="top",
         bbox=dict(facecolor="#FFFFE0", edgecolor="#888888",
                   boxstyle="round,pad=0.4", alpha=0.95))

fig.savefig("/home/claude/ess314/assets/figures/fig_17_cascadia_paleoseismic.png",
            bbox_inches="tight")
print(f"Mean recurrence: {mean_rec:.0f} yr; std: {std_rec:.0f} yr")
print("Saved fig_17_cascadia_paleoseismic.png")
