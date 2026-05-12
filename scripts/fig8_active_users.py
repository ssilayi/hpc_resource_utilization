"""
fig8_active_users.py
Figure 8: Active user patterns.
  A – Avg unique users by weekday: 2025 retrospective vs Fall25-Sp26
  B – IST department profile vs rest-of-CEC: jobs vs CPU-hrs tradeoff
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

USERS_FILE = os.path.join(os.path.dirname(__file__), "../data/active_users_weekday.txt")
CEC_FILE   = os.path.join(os.path.dirname(__file__), "../data/table3_cec_cpu.txt")
OUT_FILE   = os.path.join(os.path.dirname(__file__), "../figures/fig8_active_users.png")

set_style()

# ── load weekly users ─────────────────────────────────────────────────────────
days, retro_u, f25_u = [], [], []
with open(USERS_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("weekday"):
            continue
        p = line.split("\t")
        days.append(p[0])
        retro_u.append(int(p[2]))
        f25_u.append(int(p[3]))

# ── load CEC data ─────────────────────────────────────────────────────────────
cec_depts, cec_jobs, cec_hrs, cec_avg = [], [], [], []
with open(CEC_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("dept"):
            continue
        p = line.split("\t")
        cec_depts.append(p[0].upper())
        cec_jobs.append(int(p[2]))
        cec_hrs.append(float(p[3]))
        cec_avg.append(float(p[4]))

fig = plt.figure(figsize=(12, 5.5))
gs  = gridspec.GridSpec(1, 2, wspace=0.40)
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

# ── Panel A: weekday user counts ─────────────────────────────────────────────
x    = np.arange(len(days))
w    = 0.38
b1   = ax1.bar(x - w/2, retro_u, w, label="Full Year 2025",         color=COLORS["blue"],  zorder=3)
b2   = ax1.bar(x + w/2, f25_u,   w, label="Fall 2025–Spring 2026",  color=COLORS["green"], zorder=3)

ax1.set_xticks(x)
ax1.set_xticklabels(days, fontsize=9)
ax1.set_ylabel("Average Unique Active Users per Day", fontsize=9)
ax1.set_ylim(0, max(retro_u) * 1.25)
ax1.legend(fontsize=9, loc="upper left")
ax1.set_title("(A) Average Daily Active Users by Weekday\n"
              "Two Analysis Periods Compared", fontsize=9, pad=6)

# Annotate the weekend story
for d_idx in [5, 6]:  # Sat, Sun
    ax1.text(d_idx - w/2, retro_u[d_idx] + 5, f"{retro_u[d_idx]}",
             ha="center", fontsize=8, color=COLORS["blue"], fontweight="bold")
    ax1.text(d_idx + w/2, f25_u[d_idx] + 5, f"{f25_u[d_idx]}",
             ha="center", fontsize=8, color=COLORS["green"], fontweight="bold")

ax1.text(5.5, max(retro_u)*0.60,
         f"Weekend users:\n{retro_u[5]}–{retro_u[6]}/day (2025)\n"
         "→ large self-directed\npopulation needs\nasync support",
         ha="center", fontsize=7.5, color="#555555",
         bbox=dict(boxstyle="round,pad=0.3", fc="#FFFDE7", ec="#E0C000", alpha=0.95))

# ── Panel B: IST vs rest of CEC (job count vs avg CPU hrs, log-log) ───────────
ist_mask = [d == "IST" for d in cec_depts]
colors_b = [COLORS["red"] if m else COLORS["blue"] for m in ist_mask]
sizes_b  = [max(40, h/15000) for h in cec_hrs]

ax2.scatter(cec_jobs, cec_avg, s=sizes_b, c=colors_b, alpha=0.85,
            zorder=3, edgecolors="white", linewidths=1.0)
ax2.set_xscale("log")
ax2.set_yscale("log")

for i, (d, j, a, m) in enumerate(zip(cec_depts, cec_jobs, cec_avg, ist_mask)):
    offset = (j*1.15, a*1.1)
    ax2.text(*offset, d, fontsize=8,
             color=COLORS["red"] if m else COLORS["blue"], fontweight="bold")

ax2.set_xlabel("Number of CPU Jobs (log scale)", fontsize=9)
ax2.set_ylabel("Avg CPU Hours per Job (log scale)", fontsize=9)
ax2.set_title("(B) CEC Departments: Volume vs. Per-Job Intensity\n"
              "IST is outlier: highest volume, lowest intensity", fontsize=9, pad=6)

# IST callout
ist_j = cec_jobs[ist_mask.index(True)]
ist_a = cec_avg[ist_mask.index(True)]
ax2.annotate("IST: 785K jobs,\n0.53 hrs avg\n(high frequency,\nlow intensity)",
             xy=(ist_j, ist_a), xytext=(ist_j/8, ist_a*6),
             fontsize=7.5, color=COLORS["red"],
             arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.2),
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS["red"], alpha=0.9))

# ME callout
me_i = cec_depts.index("ME")
ax2.annotate("ME: 474 jobs,\n458 hrs avg\n(low frequency,\nhigh intensity)",
             xy=(cec_jobs[me_i], cec_avg[me_i]), xytext=(cec_jobs[me_i]*4, cec_avg[me_i]*0.4),
             fontsize=7.5, color=COLORS["blue"],
             arrowprops=dict(arrowstyle="->", color=COLORS["blue"], lw=1.2),
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS["blue"], alpha=0.9))

# Quadrant lines
ax2.axhline(10, color="#CCCCCC", linewidth=0.8, linestyle="--")
ax2.axvline(10000, color="#CCCCCC", linewidth=0.8, linestyle="--")

import matplotlib.patches as mpatches
h_ = [mpatches.Patch(color=COLORS["red"],  label="IST (outlier)"),
      mpatches.Patch(color=COLORS["blue"], label="Other CEC departments")]
ax2.legend(handles=h_, fontsize=8, loc="lower left")

fig.suptitle(
    "Figure 8. Active User Patterns and CEC Departmental Usage Profiles\n"
    "Hopper HPC Cluster, George Mason University",
    fontsize=11, y=1.02
)
save_fig(fig, OUT_FILE)
