"""
figA2_failure_analysis.py

Figure A2: Job Failure Rate Analysis — four panels.
  A – Stacked bar: exit-state distribution by department (F25-Sp26)
  B – Monthly failure rate vs. avg wait time (dual axis, congestion overlay)
  C – Wasted CPU-hours by failure type and college
  D – Memory over-provisioning ratio by department (scatter: ratio vs OOM risk)

Data files:
  data/a2_exit_states_by_dept.txt
  data/a2_monthly_failure_rates.txt
  data/a2_overprovisioning.txt
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from collections import defaultdict

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
OUT_FILE = os.path.join(os.path.dirname(__file__), "../figures/figA2_failure_analysis.png")

set_style()

# ── helpers ───────────────────────────────────────────────────────────────────
def load_tsv(fname, skip=("#",)):
    rows = []
    with open(os.path.join(DATA_DIR, fname)) as f:
        headers = None
        for line in f:
            line = line.strip()
            if not line or any(line.startswith(s) for s in skip):
                continue
            parts = line.split("\t")
            if headers is None:
                headers = parts
                continue
            rows.append(dict(zip(headers, parts)))
    return rows

# ── load data ────────────────────────────────────────────────────────────────
exit_rows  = load_tsv("a2_exit_states_by_dept.txt")
monthly    = load_tsv("a2_monthly_failure_rates.txt")
overprov   = load_tsv("a2_overprovisioning.txt")

# ── panel A: exit-state stacked bars, F25-Sp26, top depts ────────────────────
STATE_COLORS = {
    "COMPLETED":     "#2166AC",
    "CANCELLED":     "#74ADD1",
    "FAILED":        "#D6604D",
    "TIMEOUT":       "#F4A582",
    "OUT_OF_MEMORY": "#762A83",
    "NODE_FAIL":     "#878787",
}
STATES = ["COMPLETED", "CANCELLED", "FAILED", "TIMEOUT", "OUT_OF_MEMORY"]

# Aggregate by dept for F25S26 period
dept_states = defaultdict(lambda: defaultdict(int))
for r in exit_rows:
    if r["period"] == "F25S26":
        dept_states[r["dept"]][r["state"]] += int(r["job_count"])

# Focus on depts with >1000 jobs
target_depts = ["ceie", "cs", "stat", "ist", "phys", "aoes", "ece", "me", "chem"]
dept_labels  = ["CEIE", "CS", "STAT", "IST", "PHYS", "AOES", "ECE", "ME", "CHEM"]

# Compute failure rates
fail_rates = {}
for d in target_depts:
    total = sum(dept_states[d].values())
    if total == 0:
        fail_rates[d] = 0
        continue
    bad = (dept_states[d]["FAILED"] + dept_states[d]["TIMEOUT"]
           + dept_states[d]["OUT_OF_MEMORY"])
    fail_rates[d] = bad / total * 100

# ── layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(15, 11))
gs  = gridspec.GridSpec(2, 2, hspace=0.42, wspace=0.36)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[1, 0])
axD = fig.add_subplot(gs[1, 1])

# ── Panel A ───────────────────────────────────────────────────────────────────
x     = np.arange(len(target_depts))
width = 0.62
bottoms = np.zeros(len(target_depts))

for state in STATES:
    vals = np.array([dept_states[d][state] for d in target_depts], dtype=float)
    # normalise to pct
    totals = np.array([sum(dept_states[d].values()) for d in target_depts], dtype=float)
    totals[totals == 0] = 1
    pcts = vals / totals * 100
    axA.bar(x, pcts, width, bottom=bottoms, color=STATE_COLORS[state],
            label=state, zorder=3)
    bottoms += pcts

axA.set_xticks(x)
axA.set_xticklabels(dept_labels, fontsize=9)
axA.set_ylabel("Percentage of Jobs (%)", fontsize=9)
axA.set_ylim(0, 110)
axA.set_title("(A) Exit-State Distribution by Department\nFall 2025–Spring 2026",
              fontsize=9, pad=5)
axA.legend(fontsize=7.5, loc="upper right", ncol=2)
axA.axhline(100, color="#CCCCCC", lw=0.5, ls="--")

# Annotate failure rates
for i, d in enumerate(target_depts):
    fr = fail_rates[d]
    color = COLORS["red"] if fr > 10 else COLORS["orange"] if fr > 7 else COLORS["green"]
    axA.text(i, 102, f"{fr:.1f}%", ha="center", fontsize=7,
             color=color, fontweight="bold")
axA.text(0.99, 1.04, "↑ failure rate", transform=axA.transAxes,
         fontsize=7, ha="right", color=COLORS["red"])

# ── Panel B: monthly failure rate vs wait time ────────────────────────────────
months_b  = [r["year_month"] for r in monthly]
fail_b    = [float(r["failure_rate_pct"]) for r in monthly]
wait_b    = [float(r["avg_wait_hrs"]) for r in monthly]
wasted_b  = [float(r["wasted_cpu_hrs"]) / 1e6 for r in monthly]

x_b = np.arange(len(months_b))
axB.bar(x_b, fail_b, 0.5, color=COLORS["red"], alpha=0.75,
        label="Failure Rate (%)", zorder=3)

axB2 = axB.twinx()
axB2.plot(x_b, wait_b, "o-", color=COLORS["purple"], lw=2.2,
          ms=6, label="Avg Wait Time (hrs)", zorder=4)
axB2.set_ylabel("Avg Wait Time (hrs)", fontsize=9, color=COLORS["purple"])
axB2.tick_params(axis="y", labelcolor=COLORS["purple"])
axB2.spines["right"].set_visible(True)
axB2.spines["right"].set_color(COLORS["purple"])
axB2.set_ylim(0, 6)

# Shade congested months
for i, m in enumerate(months_b):
    if m in ("2025-10", "2026-03"):
        axB.axvspan(i-0.45, i+0.45, alpha=0.12, color=COLORS["red"], zorder=1)

axB.set_xticks(x_b)
axB.set_xticklabels(months_b, rotation=30, ha="right", fontsize=8)
axB.set_ylabel("Job Failure Rate (%)", fontsize=9, color=COLORS["red"])
axB.tick_params(axis="y", labelcolor=COLORS["red"])
axB.set_title("(B) Monthly Failure Rate vs. Queue Wait Time\n"
              "Congested months shaded (Oct 2025, Mar 2026)", fontsize=9, pad=5)

h1, l1 = axB.get_legend_handles_labels()
h2, l2 = axB2.get_legend_handles_labels()
axB.legend(h1+h2, l1+l2, fontsize=8, loc="upper left")

# Pearson r annotation
fr_arr = np.array(fail_b); wt_arr = np.array(wait_b)
r = np.corrcoef(fr_arr, wt_arr)[0, 1]
axB.text(0.97, 0.96, f"Pearson r = {r:.2f}",
         transform=axB.transAxes, ha="right", va="top", fontsize=8.5,
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS["purple"], alpha=0.9))

# ── Panel C: wasted CPU-hours by exit state and college ──────────────────────
# Aggregate wasted CPU-hrs by (college, state) for F25S26
waste_agg = defaultdict(lambda: defaultdict(float))
for r in exit_rows:
    if r["period"] == "F25S26" and r["state"] != "COMPLETED":
        waste_agg[r["college"]][r["state"]] += float(r["wasted_cpu_hrs"])

colleges_c  = ["CEC", "COS"]
fail_states = ["FAILED", "TIMEOUT", "OUT_OF_MEMORY", "CANCELLED"]
fc_colors   = [COLORS["red"], COLORS["orange"], COLORS["purple"], COLORS["light_blue"]]

x_c     = np.arange(len(colleges_c))
w_c     = 0.18
offsets = [-1.5, -0.5, 0.5, 1.5]
for j, (state, col) in enumerate(zip(fail_states, fc_colors)):
    vals = [waste_agg[c][state] / 1e6 for c in colleges_c]
    bars = axC.bar(x_c + offsets[j]*w_c, vals, w_c, color=col,
                   label=state, zorder=3)
    for bar, v in zip(bars, vals):
        if v > 0.1:
            axC.text(bar.get_x() + bar.get_width()/2,
                     bar.get_height() + 0.02,
                     f"{v:.1f}M", ha="center", fontsize=7)

axC.set_xticks(x_c)
axC.set_xticklabels(["CEC (Eng. & Computing)", "COS (Science)"], fontsize=9)
axC.set_ylabel("Wasted CPU-Hours (millions)", fontsize=9)
axC.set_title("(C) Wasted CPU-Hours by Exit State and College\n"
              "Fall 2025–Spring 2026", fontsize=9, pad=5)
axC.legend(fontsize=8, loc="upper right")

# Total wasted annotation
for i, c in enumerate(colleges_c):
    total_w = sum(waste_agg[c].values()) / 1e6
    axC.text(i, max([waste_agg[c][s] for s in fail_states])/1e6 * 1.18,
             f"Total: {total_w:.1f}M hrs",
             ha="center", fontsize=8, fontweight="bold",
             color="#333333",
             bbox=dict(boxstyle="round,pad=0.2", fc="#FFF8E1", ec="#E0C000"))

# ── Panel D: memory over-provisioning vs OOM risk ────────────────────────────
cec_depts = [r for r in overprov if r["college"] == "CEC"]
cos_depts  = [r for r in overprov if r["college"] == "COS"]

def plot_group(ax, group, color, marker, label):
    for r in group:
        jobs   = int(r["jobs_sampled"])
        ratio  = float(r["avg_mem_ratio"])
        oom    = float(r["pct_jobs_oom_risk"])
        size   = max(40, jobs / 8000)
        ax.scatter(ratio, oom, s=size, color=color, alpha=0.80,
                   marker=marker, zorder=3, edgecolors="white", lw=0.8)
        axD.annotate(r["dept"].upper(),
                     (ratio, oom),
                     xytext=(4, 3), textcoords="offset points",
                     fontsize=7, color=color, fontweight="bold")

plot_group(axD, cec_depts, COLORS["blue"], "o", "CEC")
plot_group(axD, cos_depts, COLORS["green"], "s", "COS")

# Reference lines
axD.axhline(3.0, color="#CCCCCC", lw=0.8, ls="--")
axD.axvline(2.5, color="#CCCCCC", lw=0.8, ls="--")
axD.text(2.52, 5.6, "High over-provisioning\n& high OOM risk\n→ priority consultation",
         fontsize=7, color=COLORS["red"],
         bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=COLORS["red"], alpha=0.9))

axD.set_xlabel("Avg Memory Over-Provisioning Ratio\n(Requested / Actual Used; 1 = exact)", fontsize=9)
axD.set_ylabel("% Jobs at OOM Risk\n(actual usage within 10% of request)", fontsize=9)
axD.set_title("(D) Memory Over-Provisioning vs. OOM Risk by Department\n"
              "(bubble size ∝ job count; dashed = action thresholds)",
              fontsize=9, pad=5)
h_ = [mpatches.Patch(color=COLORS["blue"],  label="CEC department"),
      mpatches.Patch(color=COLORS["green"], label="COS department")]
axD.legend(handles=h_, fontsize=8, loc="lower right")

fig.suptitle(
    "Figure A2. Job Failure Rate Analysis — Hopper HPC Cluster\n"
    "Exit-State Distribution, Temporal Correlation with Congestion, "
    "Wasted Resources, and Over-Provisioning",
    fontsize=11, y=1.01
)
save_fig(fig, OUT_FILE)
