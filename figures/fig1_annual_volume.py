"""
fig1_annual_volume.py
Figure 1: Annual job volume trend across three analysis periods.
Shows total jobs, CPU jobs, and GPU jobs side-by-side; secondary axis shows GPU %.
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/table1_annual_volume.txt")
OUT_FILE  = os.path.join(os.path.dirname(__file__), "../figures/fig1_annual_volume.png")

set_style()

# ── load data ────────────────────────────────────────────────────────────────
periods, months, cpu, gpu, total, gpu_pct = [], [], [], [], [], []
with open(DATA_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("period"):
            continue
        parts = line.split("\t")
        periods.append(parts[0])
        months.append(int(parts[1]))
        cpu.append(int(parts[2]))
        gpu.append(int(parts[3]))
        total.append(int(parts[4]))
        gpu_pct.append(float(parts[5]))

x = np.arange(len(periods))
width = 0.28

# ── plot ─────────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(8, 5))

bars_cpu   = ax1.bar(x - width, cpu,   width, label="CPU Jobs",   color=COLORS["blue"],   zorder=3)
bars_gpu   = ax1.bar(x,         gpu,   width, label="GPU Jobs",   color=COLORS["red"],    zorder=3)
bars_total = ax1.bar(x + width, total, width, label="Total Jobs", color=COLORS["orange"], zorder=3, alpha=0.85)

ax1.set_ylabel("Number of Jobs", fontsize=10)
ax1.set_xticks(x)
ax1.set_xticklabels(periods, fontsize=9)
ax1.set_ylim(0, max(total) * 1.25)
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}K"))

# Annotate total bars
for bar, val in zip(bars_total, total):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30000,
             f"{val/1e6:.2f}M", ha="center", va="bottom", fontsize=8,
             color=COLORS["orange"], fontweight="bold")

# Secondary axis: GPU percentage
ax2 = ax1.twinx()
ax2.plot(x, gpu_pct, "o--", color=COLORS["purple"], linewidth=2,
         markersize=7, label="GPU % of Total", zorder=4)
ax2.set_ylabel("GPU Jobs (% of Total)", color=COLORS["purple"], fontsize=10)
ax2.tick_params(axis="y", labelcolor=COLORS["purple"])
ax2.set_ylim(0, 12)
ax2.spines["right"].set_visible(True)
ax2.spines["right"].set_color(COLORS["purple"])

# Annotate GPU% points
for xi, pct in zip(x, gpu_pct):
    ax2.text(xi + 0.12, pct + 0.3, f"{pct:.1f}%",
             fontsize=8, color=COLORS["purple"])

# Note about AY23-24 estimate
ax1.text(0, max(total)*0.08, "* AY 2023-24 totals\nestimated (range\nmidpoint used)",
         fontsize=7.5, color="#666666", ha="center")

# Combined legend
h1, l1 = ax1.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax1.legend(h1 + h2, l1 + l2, loc="upper left", fontsize=9)

# Note about 9-month window
note = "† Fall 2025–Spring 2026 spans 9 months; annualized rate exceeds Full Year 2025."
fig.text(0.5, -0.04, note, ha="center", fontsize=8, color="#555555", style="italic")

ax1.set_title("Figure 1. Aggregate Job Volume Across Analysis Periods\n"
              "Hopper HPC Cluster, George Mason University", fontsize=11, pad=10)

save_fig(fig, OUT_FILE)
