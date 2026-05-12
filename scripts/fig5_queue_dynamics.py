"""
fig5_queue_dynamics.py
Figure 5: Temporal patterns — two panels.
  A – Monthly job submissions across Full Year 2025 (CPU vs GPU, stacked area)
  B – Monthly average run time vs wait time, Fall 2025–Spring 2026,
      with congestion events highlighted
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

MONTHLY_FILE = os.path.join(os.path.dirname(__file__), "../data/monthly_volume_2025.txt")
QUEUE_FILE   = os.path.join(os.path.dirname(__file__), "../data/table9_queue_times.txt")
OUT_FILE     = os.path.join(os.path.dirname(__file__), "../figures/fig5_queue_dynamics.png")

set_style()

# ── load monthly volume ───────────────────────────────────────────────────────
months_v, cpu_v, gpu_v = [], [], []
with open(MONTHLY_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("year"):
            continue
        p = line.split("\t")
        months_v.append(p[0])
        cpu_v.append(int(p[1]))
        gpu_v.append(int(p[2]))

# ── load queue times ──────────────────────────────────────────────────────────
months_q, run_t, wait_t, flags = [], [], [], []
with open(QUEUE_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("year"):
            continue
        p = line.split("\t")
        months_q.append(p[0])
        run_t.append(float(p[1]))
        wait_t.append(float(p[2]))
        flags.append(p[3])

# ── layout ───────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8))
plt.subplots_adjust(hspace=0.42)

# ── Panel A: stacked area + GPU line ─────────────────────────────────────────
x1 = np.arange(len(months_v))
cpu_arr = np.array(cpu_v, dtype=float)
gpu_arr = np.array(gpu_v, dtype=float)

ax1.fill_between(x1, 0, cpu_arr/1000, alpha=0.75, color=COLORS["blue"],
                 label="CPU Jobs", step="mid", zorder=2)
ax1.fill_between(x1, cpu_arr/1000, (cpu_arr+gpu_arr)/1000, alpha=0.75,
                 color=COLORS["orange"], label="GPU Jobs", step="mid", zorder=2)

ax1_r = ax1.twinx()
ax1_r.plot(x1, gpu_arr, "o-", color=COLORS["red"], linewidth=2,
           markersize=5, label="GPU Job Count (right axis)", zorder=3)
ax1_r.set_ylabel("GPU Job Count", fontsize=9, color=COLORS["red"])
ax1_r.tick_params(axis="y", labelcolor=COLORS["red"])
ax1_r.spines["right"].set_visible(True)
ax1_r.spines["right"].set_color(COLORS["red"])
ax1_r.set_ylim(0, max(gpu_arr) * 1.4)

ax1.set_xticks(x1)
ax1.set_xticklabels(months_v, rotation=30, ha="right", fontsize=8.5)
ax1.set_ylabel("Total Job Count (thousands)", fontsize=9)
ax1.set_ylim(0, max((cpu_arr+gpu_arr)/1000) * 1.28)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v:.0f}K"))

# Highlight summer trough and fall/spring peaks
ax1.axvspan(5.5, 6.5, alpha=0.08, color=COLORS["gray"], label="Summer trough")
ax1.axvspan(-0.5, 0.5, alpha=0.08, color=COLORS["green"])
ax1.axvspan(7.5, 9.5, alpha=0.08, color=COLORS["green"])
ax1.text(6, max(cpu_arr+gpu_arr)/1000*0.75, "Summer\ntrough",
         ha="center", fontsize=7.5, color=COLORS["gray"])
ax1.text(8.5, max(cpu_arr+gpu_arr)/1000*1.05, "Fall\npeak",
         ha="center", fontsize=7.5, color=COLORS["green"])

h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax1_r.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, fontsize=8, loc="upper left", ncol=2)
ax1.set_title("(A) Monthly Job Submissions — Full Year 2025\n"
              "Pronounced seasonality aligned with academic calendar", fontsize=9, pad=6)

# ── Panel B: wait time & run time by month ────────────────────────────────────
x2 = np.arange(len(months_q))
bar_width = 0.38

run_bars  = ax2.bar(x2 - bar_width/2, run_t,  bar_width, label="Avg Run Time",
                    color=COLORS["blue"], zorder=3)
wait_bars = ax2.bar(x2 + bar_width/2, wait_t, bar_width, label="Avg Wait Time",
                    color=COLORS["red"], zorder=3)

# Highlight congested months
for i, flag in enumerate(flags):
    if flag == "congested":
        ax2.axvspan(i - 0.55, i + 0.55, alpha=0.12, color=COLORS["red"], zorder=1)
        ax2.text(i, max(wait_t)*1.04,
                 f"CONGESTED\n{wait_t[i]:.1f} hrs wait",
                 ha="center", fontsize=7, color=COLORS["red"], fontweight="bold")
    elif flag == "elevated":
        ax2.axvspan(i - 0.55, i + 0.55, alpha=0.07, color=COLORS["orange"], zorder=1)

# Value annotations on congested wait bars
for bar, val, flag in zip(wait_bars, wait_t, flags):
    if flag in ("congested",):
        ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.08,
                 f"{val:.1f}h", ha="center", fontsize=7.5, color=COLORS["red"],
                 fontweight="bold")

ax2.set_xticks(x2)
ax2.set_xticklabels(months_q, rotation=30, ha="right", fontsize=8.5)
ax2.set_ylabel("Average Time (hours)", fontsize=9)
ax2.set_ylim(0, max(wait_t) * 1.22)
ax2.legend(fontsize=9, loc="upper right")
ax2.set_title("(B) Average Job Run Time vs. Wait Time by Month\n"
              "Fall 2025–Spring 2026 (shaded = congestion events)", fontsize=9, pad=6)

# Semester annotations
ax2.axvline(2, color="#AAAAAA", linewidth=0.8, linestyle=":")
ax2.axvline(5.5, color="#AAAAAA", linewidth=0.8, linestyle=":")
ax2.text(1.0, max(wait_t)*0.88, "Fall 2025", fontsize=7.5, color="#888888", ha="center")
ax2.text(7.0, max(wait_t)*0.88, "Spring 2026", fontsize=7.5, color="#888888", ha="center")

fig.suptitle(
    "Figure 5. Temporal Utilization Patterns and Queue Health\n"
    "Hopper HPC Cluster, George Mason University",
    fontsize=11, y=1.01
)
save_fig(fig, OUT_FILE)
