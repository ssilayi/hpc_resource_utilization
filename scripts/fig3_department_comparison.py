"""
fig3_department_comparison.py
Figure 3: Department-level resource profiles within CEC and COS.
Four panels:
  A – CEC: job count vs avg CPU hrs/job (bubble = total CPU hrs)
  B – COS: job count vs avg CPU hrs/job (bubble = avg memory)
  C – CEC departments: CPU hrs vs GPU hrs side-by-side bars
  D – COS departments: CPU hrs vs avg memory
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

CEC_FILE = os.path.join(os.path.dirname(__file__), "../data/table3_cec_cpu.txt")
COS_FILE = os.path.join(os.path.dirname(__file__), "../data/table5_cos_cpu.txt")
OUT_FILE = os.path.join(os.path.dirname(__file__), "../figures/fig3_department_comparison.png")

set_style()

def load_dept(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or line.startswith("dept"):
                continue
            p = line.split("\t")
            rows.append({
                "dept": p[0], "long": p[1],
                "jobs": int(p[2]), "total_hrs": float(p[3]),
                "avg_hrs": float(p[4]), "avg_mem": float(p[5])
            })
    return rows

cec = load_dept(CEC_FILE)
cos = load_dept(COS_FILE)

fig, axes = plt.subplots(2, 2, figsize=(13, 10))
plt.subplots_adjust(hspace=0.38, wspace=0.35)

# ── Panel A: CEC bubble (jobs × avg_hrs, bubble = total_hrs) ─────────────────
ax = axes[0, 0]
for i, d in enumerate(cec):
    size = max(30, d["total_hrs"] / 15000)
    color = PALETTE[i % len(PALETTE)]
    ax.scatter(d["jobs"], d["avg_hrs"], s=size, color=color,
               alpha=0.85, zorder=3, edgecolors="white", linewidths=0.8)
    offset_x = d["jobs"] * 0.04
    offset_y = d["avg_hrs"] * 0.08 + 3
    ax.text(d["jobs"] + offset_x, d["avg_hrs"] + offset_y,
            d["dept"].upper(), fontsize=7.5, color=color, fontweight="bold")

ax.set_xlabel("Number of CPU Jobs Submitted", fontsize=9)
ax.set_ylabel("Avg CPU Hours per Job", fontsize=9)
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_title("(A) CEC Departments: Job Volume vs. Per-Job Intensity\n"
             "(bubble size ∝ total CPU hours consumed)", fontsize=9, pad=6)
ax.set_xlim(200, 2_000_000)
ax.set_ylim(0.3, 800)
legend_txt = ("Bubble area proportional\nto total CPU-hours consumed.\n"
              "IST: 785K jobs, 0.53 hrs avg\n"
              "ME: 474 jobs, 458 hrs avg")
ax.text(0.98, 0.97, legend_txt, transform=ax.transAxes,
        fontsize=7, va="top", ha="right", color="#555555",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CCCCCC", alpha=0.9))

# ── Panel B: COS bubble ───────────────────────────────────────────────────────
ax = axes[0, 1]
for i, d in enumerate(cos):
    size = max(40, d["avg_mem"] * 4)
    color = PALETTE[i % len(PALETTE)]
    ax.scatter(d["jobs"], d["avg_hrs"], s=size, color=color,
               alpha=0.85, zorder=3, edgecolors="white", linewidths=0.8)
    offset_x = d["jobs"] * 0.03
    ax.text(d["jobs"] + offset_x, d["avg_hrs"] + 2,
            d["dept"].upper(), fontsize=7.5, color=color, fontweight="bold")

ax.set_xlabel("Number of CPU Jobs Submitted", fontsize=9)
ax.set_ylabel("Avg CPU Hours per Job", fontsize=9)
ax.set_xscale("log")
ax.set_title("(B) COS Departments: Job Volume vs. Per-Job Intensity\n"
             "(bubble size ∝ avg memory requested per job)", fontsize=9, pad=6)
ax.set_xlim(1000, 500_000)
ax.set_ylim(0, 310)
legend_txt = ("Bubble area proportional\nto avg memory per job (GB).\n"
              "AOES: 254 GB avg memory\n"
              "CHEM: 258 hrs avg CPU")
ax.text(0.98, 0.97, legend_txt, transform=ax.transAxes,
        fontsize=7, va="top", ha="right", color="#555555",
        bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#CCCCCC", alpha=0.9))

# ── Panel C: CEC total CPU-hours by department (top 6) ───────────────────────
ax = axes[1, 0]
cec_sorted = sorted(cec, key=lambda d: d["total_hrs"], reverse=True)[:7]
labels = [d["dept"].upper() for d in cec_sorted]
vals   = [d["total_hrs"] / 1e6 for d in cec_sorted]
colors = [PALETTE[i % len(PALETTE)] for i in range(len(labels))]
bars   = ax.bar(labels, vals, color=colors, zorder=3, width=0.65)
for bar, val in zip(bars, vals):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.04,
            f"{val:.1f}M", ha="center", fontsize=8, color="#333333")
ax.set_ylabel("Total CPU-Hours (millions)", fontsize=9)
ax.set_title("(C) CEC: Total CPU-Hours by Department", fontsize=9, pad=6)
ax.set_ylim(0, max(vals) * 1.20)

# ── Panel D: COS avg memory vs avg CPU hrs (scatter with labels) ──────────────
ax = axes[1, 1]
cos_major = [d for d in cos if d["jobs"] > 3000]
for i, d in enumerate(cos_major):
    color = PALETTE[i % len(PALETTE)]
    ax.scatter(d["avg_mem"], d["avg_hrs"],
               s=max(60, d["jobs"]/500), color=color,
               alpha=0.85, zorder=3, edgecolors="white", linewidths=1)
    ax.text(d["avg_mem"] + 3, d["avg_hrs"] + 1,
            d["dept"].upper(), fontsize=8, color=color, fontweight="bold")

ax.set_xlabel("Avg Memory Requested per Job (GB)", fontsize=9)
ax.set_ylabel("Avg CPU Hours per Job", fontsize=9)
ax.set_title("(D) COS: Memory vs. Run-Time Profile\n"
             "(point size ∝ job count; major depts only)", fontsize=9, pad=6)
ax.axhline(100, color="#AAAAAA", linewidth=0.8, linestyle="--")
ax.axvline(100, color="#AAAAAA", linewidth=0.8, linestyle="--")
ax.text(102, 101, "High memory\n& long runtime", fontsize=7, color="#888888")

fig.suptitle(
    "Figure 3. Departmental Resource-Use Profiles — CEC and COS\n"
    "Hopper HPC Cluster, Fall 2025–Spring 2026",
    fontsize=11, y=1.01
)
save_fig(fig, OUT_FILE)
