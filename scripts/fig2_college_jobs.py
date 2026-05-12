"""
fig2_college_jobs.py
Figure 2: Job submissions by institutional college, Fall 2025-Spring 2026.
Panel A: absolute job counts (horizontal bar).
Panel B: pie / donut share for CEC vs COS vs Other.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/table2_college_jobs.txt")
OUT_FILE  = os.path.join(os.path.dirname(__file__), "../figures/fig2_college_jobs.png")

set_style()

# ── load ─────────────────────────────────────────────────────────────────────
colleges, longs, jobs, shares = [], [], [], []
with open(DATA_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("college"):
            continue
        parts = line.split("\t")
        colleges.append(parts[0])
        longs.append(parts[1])
        jobs.append(int(parts[2]))
        shares.append(float(parts[3]))

# ── layout ───────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(11, 5))
gs  = gridspec.GridSpec(1, 2, width_ratios=[1.6, 1], wspace=0.35)
axA = fig.add_subplot(gs[0])
axB = fig.add_subplot(gs[1])

# ── Panel A: horizontal bar chart ────────────────────────────────────────────
colors_bar = [COLORS["blue"], COLORS["green"], COLORS["orange"],
              COLORS["light_blue"], COLORS["gray"], COLORS["light_red"],
              COLORS["purple"], COLORS["red"]]

y_pos = np.arange(len(colleges))
bars  = axA.barh(y_pos, jobs, color=colors_bar[:len(colleges)],
                 height=0.65, zorder=3)

# Value labels
for bar, val in zip(bars, jobs):
    label = f"{val:,}" if val > 10000 else f"{val:,}"
    xpos  = bar.get_width() + bar.get_width() * 0.02
    if bar.get_width() < 10000:
        xpos = bar.get_width() + 20000
    axA.text(xpos, bar.get_y() + bar.get_height()/2,
             label, va="center", fontsize=8.5, color="#333333")

axA.set_yticks(y_pos)
axA.set_yticklabels([f"{c}  ({l})" for c, l in zip(colleges, longs)], fontsize=9)
axA.set_xlabel("Number of Job Submissions", fontsize=10)
axA.set_xlim(0, max(jobs) * 1.22)
axA.xaxis.set_major_formatter(plt.FuncFormatter(
    lambda v, _: f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1000:.0f}K"))
axA.invert_yaxis()
axA.set_title("(A) Jobs by College", fontsize=10, pad=6)
axA.grid(axis="x", zorder=0)
axA.grid(axis="y", visible=False)

# ── Panel B: donut chart ─────────────────────────────────────────────────────
# Collapse small colleges into "Other"
cec_j  = jobs[colleges.index("CEC")]
cos_j  = jobs[colleges.index("COS")]
chss_j = jobs[colleges.index("CHSS")]
other_j = sum(j for c, j in zip(colleges, jobs)
               if c not in ("CEC", "COS", "CHSS"))

donut_vals   = [cec_j, cos_j, chss_j, other_j]
donut_labels = ["CEC\n(63.7%)", "COS\n(33.3%)", "CHSS\n(2.2%)", "Other\n(<0.2%)"]
donut_colors = [COLORS["blue"], COLORS["green"], COLORS["orange"], COLORS["gray"]]
explode      = (0.04, 0.04, 0.06, 0.06)

wedges, texts = axB.pie(
    donut_vals, labels=donut_labels, colors=donut_colors,
    explode=explode, startangle=140,
    textprops={"fontsize": 9},
    wedgeprops={"linewidth": 1.2, "edgecolor": "white"},
    labeldistance=1.12,
)
# Draw a white circle to make it a donut
centre_circle = plt.Circle((0, 0), 0.55, fc="white")
axB.add_artist(centre_circle)
axB.text(0, 0, f"{sum(donut_vals):,.0f}\nTotal\nJobs",
         ha="center", va="center", fontsize=8.5, fontweight="bold",
         color="#333333")
axB.set_title("(B) Share of Total Submissions", fontsize=10, pad=6)

fig.suptitle(
    "Figure 2. Job Submissions by Institutional College\n"
    "Hopper HPC Cluster, Fall 2025–Spring 2026 (N = 2,905,604 jobs)",
    fontsize=11, y=1.01
)
save_fig(fig, OUT_FILE)
