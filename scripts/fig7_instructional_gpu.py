"""
fig7_instructional_gpu.py
Figure 7: Instructional GPU utilization.
  A – Top instructional GPU accounts: jobs and GPU-hours (dual bar)
  B – cs678 enrollment & GPU-jobs growth (Fall 2024 vs Fall 2025)
  C – GPU hardware types requested by instructional accounts (bar)
  D – Per-student GPU-hours for major instructional accounts
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

DATA_FILE = os.path.join(os.path.dirname(__file__), "../data/table7_instructional_gpu.txt")
OUT_FILE  = os.path.join(os.path.dirname(__file__), "../figures/fig7_instructional_gpu.png")

set_style()

# ── load instructional data ───────────────────────────────────────────────────
accounts, descs, students, gjobs, ghrs, avg_hrs = [], [], [], [], [], []
with open(DATA_FILE) as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("account"):
            continue
        p = line.split("\t")
        accounts.append(p[0])
        descs.append(p[1])
        students.append(int(p[2]))
        gjobs.append(int(p[3]))
        ghrs.append(float(p[4]))
        avg_hrs.append(float(p[5]))

fig = plt.figure(figsize=(13, 9))
gs  = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.38)
axes = [fig.add_subplot(gs[i, j]) for i in range(2) for j in range(2)]

# ── Panel A: top 8 accounts — jobs and GPU hours ──────────────────────────────
ax = axes[0]
n   = 8
idxs = sorted(range(len(accounts)), key=lambda i: gjobs[i], reverse=True)[:n]
lbl  = [accounts[i] for i in idxs]
gj   = [gjobs[i] for i in idxs]
gh   = [ghrs[i] for i in idxs]

x    = np.arange(n)
w    = 0.40
b1   = ax.bar(x - w/2, gj, w, label="GPU Jobs",  color=COLORS["blue"], zorder=3)
axr  = ax.twinx()
b2   = axr.bar(x + w/2, gh, w, label="GPU Hours", color=COLORS["red"],  zorder=3, alpha=0.85)

ax.set_xticks(x)
ax.set_xticklabels(lbl, rotation=35, ha="right", fontsize=8)
ax.set_ylabel("GPU Job Count", fontsize=9, color=COLORS["blue"])
axr.set_ylabel("Total GPU-Hours", fontsize=9, color=COLORS["red"])
ax.tick_params(axis="y", labelcolor=COLORS["blue"])
axr.tick_params(axis="y", labelcolor=COLORS["red"])
axr.spines["right"].set_visible(True); axr.spines["right"].set_color(COLORS["red"])
ax.set_title("(A) Instructional GPU Accounts: Jobs and Hours", fontsize=9, pad=5)
import matplotlib.patches as mpatches
h_ = [mpatches.Patch(color=COLORS["blue"], label="GPU Jobs"),
      mpatches.Patch(color=COLORS["red"],  label="GPU Hours")]
ax.legend(handles=h_, fontsize=8, loc="upper right")

# ── Panel B: cs678 growth comparison ─────────────────────────────────────────
ax = axes[1]
semesters  = ["Fall 2024\n(cs678fl24)", "Fall 2025\n(cs678fl25)"]
cs678_stu  = [4, 16]
cs678_jobs = [491, 2174]
cs678_hrs  = [1018, 4601]

x2  = np.arange(2)
w2  = 0.3
ax.bar(x2 - w2, cs678_stu,  w2, label="Students",   color=COLORS["green"],  zorder=3)
ax.bar(x2,      [j/10 for j in cs678_jobs], w2, label="GPU Jobs (÷10)", color=COLORS["blue"], zorder=3)
ax.bar(x2 + w2, [h/10 for h in cs678_hrs], w2, label="GPU Hours (÷10)", color=COLORS["red"], zorder=3)

for xi, stu, job, hr in zip(x2, cs678_stu, cs678_jobs, cs678_hrs):
    ax.text(xi - w2, stu + 0.3,     f"{stu}",    ha="center", fontsize=9, fontweight="bold", color=COLORS["green"])
    ax.text(xi,      job/10 + 0.3,  f"{job:,}",  ha="center", fontsize=8, color=COLORS["blue"])
    ax.text(xi + w2, hr/10 + 0.3,   f"{hr:.0f}", ha="center", fontsize=8, color=COLORS["red"])

ax.set_xticks(x2)
ax.set_xticklabels(semesters, fontsize=9)
ax.set_ylabel("Count (see legend for scaling)", fontsize=9)
ax.legend(fontsize=8, loc="upper left")
ax.set_title("(B) CS678 Growth: Fall 2024 vs Fall 2025\n"
             "4× enrollment → 4.4× GPU jobs, 4.5× GPU-hours", fontsize=9, pad=5)

# growth arrows
for i, (stu_ratio, job_ratio) in enumerate([(cs678_stu[1]/cs678_stu[0],
                                              cs678_jobs[1]/cs678_jobs[0])]):
    ax.text(0.5, max(cs678_stu)/10*9,
            f"Enrollment: ×{stu_ratio:.0f}\nJobs: ×{job_ratio:.1f}\nGPU-hrs: ×{cs678_hrs[1]/cs678_hrs[0]:.1f}",
            transform=ax.get_xaxis_transform(), ha="center",
            fontsize=8.5, color=COLORS["purple"], fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS["purple"], alpha=0.9))

# ── Panel C: GPU hardware types from instructional accounts ───────────────────
ax = axes[2]
hw_types  = ["1g.10gb", "2g.20gb", "3g.40gb", "a100.40gb", "a100.80gb", "b200.180gb", "h100.80gb"]
hw_counts = [440, 820, 620, 140, 1010, 245, 195]  # approx from slide chart
hw_colors = [COLORS["green"], COLORS["light_green"], COLORS["blue"],
             COLORS["light_blue"], COLORS["orange"], COLORS["red"], COLORS["purple"]]
bars = ax.bar(hw_types, hw_counts, color=hw_colors, zorder=3, width=0.65)
for bar, val in zip(bars, hw_counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10,
            str(val), ha="center", fontsize=8)
ax.set_ylabel("Number of GPU Jobs", fontsize=9)
ax.set_xticklabels(hw_types, rotation=30, ha="right", fontsize=8)
ax.set_title("(C) GPU Hardware Types Requested by Instructional Accounts\n"
             "High-end cards (a100.80gb, h100, b200) used by students", fontsize=9, pad=5)
# Annotate research-grade hardware
ax.axvspan(3.5, 6.5, alpha=0.10, color=COLORS["red"])
ax.text(5, max(hw_counts)*0.88, "Research-grade\nGPU tiers",
        ha="center", fontsize=7.5, color=COLORS["red"],
        bbox=dict(boxstyle="round", fc="white", ec=COLORS["red"], alpha=0.9))

# ── Panel D: per-student GPU-hours ───────────────────────────────────────────
ax = axes[3]
per_stu = [(ghrs[i] / max(students[i],1)) for i in range(len(accounts))]
sorted_idx = sorted(range(len(accounts)), key=lambda i: per_stu[i], reverse=True)[:8]
ps_labels = [accounts[i] for i in sorted_idx]
ps_vals   = [per_stu[i] for i in sorted_idx]
ps_students = [students[i] for i in sorted_idx]
ps_colors = [COLORS["red"] if v > 500 else COLORS["blue"] if v > 100 else COLORS["green"]
             for v in ps_vals]
bars = ax.barh(ps_labels[::-1], ps_vals[::-1], color=ps_colors[::-1], zorder=3, height=0.6)
for bar, val, stu in zip(bars, ps_vals[::-1], ps_students[::-1]):
    ax.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2,
            f"{val:.0f} hrs ({stu} student{'s' if stu>1 else ''})",
            va="center", fontsize=7.5)
ax.set_xlabel("GPU-Hours per Student", fontsize=9)
ax.set_title("(D) Per-Student GPU-Hour Consumption\n"
             "Top instructional accounts", fontsize=9, pad=5)
ax.set_xlim(0, max(ps_vals) * 1.35)

fig.suptitle(
    "Figure 7. Instructional GPU Utilization — Hopper HPC Cluster\n"
    "Fall 2025–Spring 2026: Growing Course Demand and Hardware Contention",
    fontsize=11, y=1.01
)
save_fig(fig, OUT_FILE)
