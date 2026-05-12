"""
fig6_cpu_distribution.py
Figure 6: CPU cores requested per job — bimodal distribution.
Two panels:
  A – Full histogram (log-scale y) showing the two dominant peaks
  B – Zoomed: 2–50 CPUs (linear) highlighting the gap in intermediate requests
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/cpu_request_distribution.txt")
OUT_FILE  = os.path.join(os.path.dirname(__file__), "../figures/fig6_cpu_distribution.png")

set_style()

# ── load ─────────────────────────────────────────────────────────────────────
ncpus, counts = [], []
with open(DATA_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("ncpus"):
            continue
        p = line.split("\t")
        ncpus.append(int(p[0]))
        counts.append(int(p[1]))

ncpus  = np.array(ncpus)
counts = np.array(counts)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
plt.subplots_adjust(wspace=0.38)

# ── Panel A: full range, log scale ───────────────────────────────────────────
colors_bar = [COLORS["blue"] if n == 1
              else COLORS["red"] if n >= 47
              else COLORS["gray"]
              for n in ncpus]

ax1.bar(ncpus, counts, width=0.8, color=colors_bar, zorder=3)
ax1.set_yscale("log")
ax1.set_xlabel("Number of CPUs Requested per Job", fontsize=10)
ax1.set_ylabel("Number of Jobs (log scale)", fontsize=10)
ax1.set_title("(A) Full Distribution: CPU Cores Requested per Job\n"
              "Hopper HPC, Fall 2025–Spring 2026", fontsize=9, pad=6)
ax1.set_xlim(-1, 52)
ax1.set_ylim(1, max(counts) * 4)

# Annotations
ax1.annotate(f"1 CPU peak:\n{counts[0]:,} jobs\n({counts[0]/sum(counts)*100:.0f}% of total)",
             xy=(1, counts[0]), xytext=(8, counts[0]*0.7),
             fontsize=8, color=COLORS["blue"], fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=COLORS["blue"], lw=1.2))

idx48 = list(ncpus).index(48)
ax1.annotate(f"48-CPU peak:\n{counts[idx48]:,} jobs",
             xy=(48, counts[idx48]), xytext=(35, counts[idx48]*2.5),
             fontsize=8, color=COLORS["red"], fontweight="bold",
             arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.2))

# Shade the "missing" intermediate range
ax1.axvspan(1.5, 46.5, alpha=0.06, color=COLORS["orange"],
            label="Near-absent intermediate range (2–47 CPUs)")
ax1.text(24, 80, "Very few jobs in this range\n(2–47 CPUs)\n→ latent efficiency gap",
         ha="center", fontsize=7.5, color=COLORS["orange"],
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS["orange"], alpha=0.9))

legend_patches = [
    plt.Rectangle((0,0),1,1, color=COLORS["blue"],  label="Single-CPU jobs"),
    plt.Rectangle((0,0),1,1, color=COLORS["red"],   label="Near-full-node jobs (≥47 CPUs)"),
    plt.Rectangle((0,0),1,1, color=COLORS["gray"],  label="Intermediate requests"),
    plt.Rectangle((0,0),1,1, color=COLORS["orange"], alpha=0.3, label="Near-absent range (2–47)"),
]
ax1.legend(handles=legend_patches, fontsize=7.5, loc="lower right")

# ── Panel B: zoomed 2–47, linear scale ───────────────────────────────────────
mask  = (ncpus >= 2) & (ncpus <= 47)
zx    = ncpus[mask]
zy    = counts[mask]
zcolors = [COLORS["orange"] if c < 1000 else COLORS["gray"] for c in zy]

ax2.bar(zx, zy, width=0.8, color=zcolors, zorder=3)
ax2.set_xlabel("Number of CPUs Requested per Job", fontsize=10)
ax2.set_ylabel("Number of Jobs", fontsize=10)
ax2.set_title("(B) Intermediate Range (2–47 CPUs), Linear Scale\n"
              "Highlighting the absence of shared-memory parallel jobs", fontsize=9, pad=6)
ax2.set_xlim(1, 48)

# Power-of-2 markers (common OpenMP thread counts)
for nc in [2, 4, 8, 16, 32]:
    idx = list(ncpus).index(nc) if nc in ncpus else None
    if idx is not None:
        ax2.axvline(nc, color=COLORS["blue"], alpha=0.35, linewidth=1, linestyle="--")
        ax2.text(nc, max(zy)*0.92, str(nc), ha="center", fontsize=7,
                 color=COLORS["blue"], alpha=0.7)

ax2.text(0.5, 0.7,
         "Common multi-threading\ncounts (2,4,8,16,32 CPUs)\nhave low adoption →\nmost users run serially",
         transform=ax2.transAxes, ha="center", fontsize=8,
         color=COLORS["blue"],
         bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=COLORS["blue"], alpha=0.9))

fig.suptitle(
    "Figure 6. Bimodal CPU Request Distribution — Hopper HPC Cluster\n"
    "Fall 2025–Spring 2026 (N = 2,777,817 CPU jobs)",
    fontsize=11, y=1.02
)
save_fig(fig, OUT_FILE)
