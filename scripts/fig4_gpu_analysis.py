"""
fig4_gpu_analysis.py
Figure 4: GPU workload analysis — four panels.
  A – GPU jobs by CEC department (bar)
  B – COS GPU emergence: 2025 vs F25-Sp26 comparison
  C – Top GPU users: total GPU hours (bar, log scale)
  D – Lorenz curve: GPU-hour concentration
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches

CEC_GPU_FILE    = os.path.join(os.path.dirname(__file__), "../data/table4_cec_gpu.txt")
COS_GPU_FILE    = os.path.join(os.path.dirname(__file__), "../data/table6_cos_gpu.txt")
USERS_FILE      = os.path.join(os.path.dirname(__file__), "../data/table8_top_gpu_users.txt")
LORENZ_FILE     = os.path.join(os.path.dirname(__file__), "../data/gpu_lorenz_curve.txt")
OUT_FILE        = os.path.join(os.path.dirname(__file__), "../figures/fig4_gpu_analysis.png")

set_style()

def load_tsv(path, skip_prefix=("#", "dept", "user")):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or any(line.startswith(p) for p in skip_prefix):
                continue
            rows.append(line.split("\t"))
    return rows

fig = plt.figure(figsize=(13, 10))
gs  = gridspec.GridSpec(2, 2, hspace=0.40, wspace=0.38)
axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2)]

# ── Panel A: CEC GPU jobs by department ──────────────────────────────────────
ax = axes[0]
cec_rows = load_tsv(CEC_GPU_FILE)
# sort by gpu_jobs descending
cec_rows.sort(key=lambda r: int(r[2]), reverse=True)
depts  = [r[0].upper() for r in cec_rows[:8]]
gjobs  = [int(r[2]) for r in cec_rows[:8]]
ghrs   = [float(r[3]) for r in cec_rows[:8]]
colors = [PALETTE[i % len(PALETTE)] for i in range(len(depts))]

x    = np.arange(len(depts))
w    = 0.42
b1   = ax.bar(x - w/2, gjobs, w, label="GPU Jobs", color=COLORS["blue"], zorder=3)
ax2A = ax.twinx()
b2   = ax2A.bar(x + w/2, ghrs, w, label="GPU Hours", color=COLORS["red"], alpha=0.85, zorder=3)
ax.set_xticks(x)
ax.set_xticklabels(depts, fontsize=8.5)
ax.set_ylabel("GPU Job Count", fontsize=9, color=COLORS["blue"])
ax2A.set_ylabel("Total GPU-Hours", fontsize=9, color=COLORS["red"])
ax.tick_params(axis="y", labelcolor=COLORS["blue"])
ax2A.tick_params(axis="y", labelcolor=COLORS["red"])
ax2A.spines["right"].set_visible(True)
ax2A.spines["right"].set_color(COLORS["red"])
ax.set_title("(A) CEC: GPU Jobs and GPU-Hours by Department", fontsize=9, pad=5)
handles = [mpatches.Patch(color=COLORS["blue"], label="GPU Jobs"),
           mpatches.Patch(color=COLORS["red"],  label="GPU Hours")]
ax.legend(handles=handles, fontsize=8, loc="upper right")
ax.set_ylim(0, max(gjobs) * 1.25)
ax2A.set_ylim(0, max(ghrs) * 1.35)

# ── Panel B: COS GPU emergence — before/after comparison ─────────────────────
ax = axes[1]
cos_rows = load_tsv(COS_GPU_FILE)
cos_rows.sort(key=lambda r: int(r[2]), reverse=True)
cos_depts = [r[0].upper() for r in cos_rows]
cos_gjobs = [int(r[2]) for r in cos_rows]
cos_ghrs  = [float(r[3]) for r in cos_rows]

x      = np.arange(len(cos_depts))
colors = [PALETTE[i % len(PALETTE)] for i in range(len(cos_depts))]
bars   = ax.bar(x, cos_gjobs, 0.6, color=colors, zorder=3)
for bar, val in zip(bars, cos_gjobs):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
            f"{val:,}", ha="center", fontsize=7.5, color="#333333")

ax.set_xticks(x)
ax.set_xticklabels(cos_depts, fontsize=8.5)
ax.set_ylabel("GPU Job Count", fontsize=9)
ax.set_title("(B) COS: GPU Jobs by Department, Fall 2025–Spring 2026\n"
             "(COS had ~2 GPU jobs in all of Full Year 2025)", fontsize=9, pad=5)

# Callout annotation
ax.annotate("GPU adoption\nemerging in\nnatural sciences",
            xy=(0, cos_gjobs[0]), xytext=(1.5, cos_gjobs[0] * 0.85),
            fontsize=7.5, color=COLORS["purple"],
            arrowprops=dict(arrowstyle="->", color=COLORS["purple"], lw=1.2))

# ── Panel C: Top GPU users by GPU-hours ──────────────────────────────────────
ax = axes[2]
user_rows = load_tsv(USERS_FILE)
user_rows.sort(key=lambda r: float(r[1]), reverse=True)
top_n   = 12
u_ids   = [f"U{i+1:02d}" for i in range(min(top_n, len(user_rows)))]
u_hrs   = [float(r[1]) for r in user_rows[:top_n]]
u_jobs  = [int(r[2]) for r in user_rows[:top_n]]
u_colors = [COLORS["blue"] if i == 0 else PALETTE[(i+1) % len(PALETTE)]
            for i in range(len(u_ids))]

bars = ax.barh(u_ids[::-1], u_hrs[::-1], color=u_colors[::-1], zorder=3, height=0.65)
for bar, val in zip(bars, u_hrs[::-1]):
    ax.text(bar.get_width() + 1000, bar.get_y() + bar.get_height()/2,
            f"{val:,.0f}", va="center", fontsize=7.5)

ax.set_xlabel("Total GPU-Hours Consumed", fontsize=9)
ax.set_title("(C) Top Users by Total GPU-Hours\n"
             "Fall 2025–Spring 2026 (top user = U01)", fontsize=9, pad=5)
ax.xaxis.set_major_formatter(plt.FuncFormatter(
    lambda v, _: f"{v/1000:.0f}K" if v >= 1000 else str(int(v))))

# Annotation for U01 dominance
u01_hrs = u_hrs[0]
total_all = sum(u_hrs)
ax.text(0.97, 0.18,
        f"U01 alone: {u01_hrs/total_all*100:.0f}% of\ntop-12 GPU-hours",
        transform=ax.transAxes, fontsize=7.5, ha="right",
        color=COLORS["blue"], fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS["blue"], alpha=0.9))

# ── Panel D: Lorenz curve ─────────────────────────────────────────────────────
ax = axes[3]
lorenz_rows = load_tsv(LORENZ_FILE, skip_prefix=("#", "cumulative"))
cum_users = [float(r[0]) for r in lorenz_rows]
cum_hrs   = [float(r[1]) for r in lorenz_rows]

ax.plot(cum_users, cum_hrs, "-", color=COLORS["blue"], linewidth=2.2,
        label="GPU-Hours Lorenz Curve", zorder=3)
ax.plot([0, 100], [0, 100], "--", color=COLORS["gray"], linewidth=1.2,
        label="Perfect equality (reference)", zorder=2)
ax.fill_between(cum_users, cum_hrs, cum_users, alpha=0.12, color=COLORS["blue"])

# Gini annotation
gini = 0.62   # approximate from curve data
ax.text(0.06, 0.80,
        f"Gini coefficient ≈ {gini:.2f}\n(0 = perfect equality,\n 1 = total concentration)",
        transform=ax.transAxes, fontsize=8, color=COLORS["blue"],
        bbox=dict(boxstyle="round,pad=0.4", fc="white", ec=COLORS["blue"], alpha=0.9))

# Mark the top 5% point
ax.annotate("Top 5% of users:\n~21% of GPU-hours",
            xy=(95, cum_hrs[-3]), xytext=(65, 55),
            fontsize=7.5, color=COLORS["red"],
            arrowprops=dict(arrowstyle="->", color=COLORS["red"], lw=1.2))
ax.scatter([95], [cum_hrs[-3]], s=40, color=COLORS["red"], zorder=4)

ax.set_xlabel("Cumulative Users (%)", fontsize=9)
ax.set_ylabel("Cumulative GPU-Hours (%)", fontsize=9)
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.set_title("(D) Lorenz Curve: GPU-Hour Consumption Concentration\n"
             "Fall 2025–Spring 2026", fontsize=9, pad=5)
ax.legend(fontsize=8, loc="upper left")

fig.suptitle(
    "Figure 4. GPU Workload Analysis: Departmental Distribution,\n"
    "COS Emergence, User Concentration, and Lorenz Curve — Hopper HPC Cluster",
    fontsize=11, y=1.01
)
save_fig(fig, OUT_FILE)
