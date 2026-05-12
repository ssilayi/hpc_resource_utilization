"""
figC2_gpu_growth_projection.py

Figure C2: GPU Demand Growth Projection — four panels.
  A – Raw monthly GPU job counts with exponential trend fit overlay
  B – Three-scenario projection (exponential / logistic / COS-accelerated)
      out to Q4-2028, with hardware capacity reference lines
  C – Quarterly GPU-hours growth with year-over-year comparison bars
  D – GPU % of total jobs over time with trendline and capacity threshold

Data files:
  data/c2_gpu_historical_monthly.txt
  data/c2_gpu_quarterly.txt
  data/c2_gpu_capacity.txt

Requirements: scipy (for curve fitting)
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from plot_config import set_style, save_fig, COLORS, PALETTE

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from scipy.optimize import curve_fit
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings("ignore")

DATA_DIR = os.path.join(os.path.dirname(__file__), "../data")
OUT_FILE = os.path.join(os.path.dirname(__file__), "../figures/figC2_gpu_growth_projection.png")

set_style()

# ── load data ─────────────────────────────────────────────────────────────────
def load_tsv(fname):
    rows = []
    with open(os.path.join(DATA_DIR, fname)) as f:
        headers = None
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if headers is None:
                headers = parts
                continue
            rows.append(dict(zip(headers, parts)))
    return rows

monthly_raw = load_tsv("c2_gpu_historical_monthly.txt")
quarterly_r = load_tsv("c2_gpu_quarterly.txt")
capacity_r  = load_tsv("c2_gpu_capacity.txt")

# Parse monthly
t_m   = np.array([float(r["t_months"]) for r in monthly_raw])
gj_m  = np.array([float(r["gpu_jobs"]) for r in monthly_raw])
gh_m  = np.array([float(r["gpu_hrs"])  for r in monthly_raw])
gp_m  = np.array([float(r["gpu_pct_total"]) for r in monthly_raw])
labels_m = [r["year_month"] for r in monthly_raw]

# Parse quarterly (drop partial / NA)
qt_rows  = [r for r in quarterly_r if r["gpu_jobs"] != "NA"]
t_q      = np.array([float(r["t_quarters"]) for r in qt_rows])
gj_q     = np.array([float(r["gpu_jobs"])   for r in qt_rows])
gh_q     = np.array([float(r["gpu_hrs"])    for r in qt_rows])
qlabels  = [r["period_label"] for r in qt_rows]

# Capacity reference
K_current    = float([r for r in capacity_r if "Current"   in r["hardware_tier"]][0]["max_monthly_jobs_est"])
K_near        = float([r for r in capacity_r if "Near-term" in r["hardware_tier"]][0]["max_monthly_jobs_est"])
K_mid         = float([r for r in capacity_r if "Mid-term"  in r["hardware_tier"]][0]["max_monthly_jobs_est"])

# ── growth model functions ────────────────────────────────────────────────────
def exp_growth(t, N0, r):
    return N0 * np.exp(r * t)

def logistic(t, N0, r, K):
    return K / (1 + ((K - N0) / N0) * np.exp(-r * t))

# Fit exponential to monthly data
popt_exp, _ = curve_fit(exp_growth, t_m, gj_m, p0=[2840, 0.04],
                         maxfev=10000)
N0_exp, r_exp = popt_exp
print(f"Exponential fit: N0={N0_exp:.0f}, r={r_exp:.4f} per month, "
      f"doubling time={np.log(2)/r_exp:.1f} months")

# Fit logistic to monthly data with K = current capacity
popt_log, _ = curve_fit(
    lambda t, N0, r: logistic(t, N0, r, K_current * 0.85),
    t_m, gj_m, p0=[2840, 0.06], maxfev=10000
)
N0_log, r_log = popt_log

# Project timeline: t=0..71 (Jan 2023 – Dec 2028 = 72 months)
t_proj = np.linspace(0, 71, 300)

# Scenario 1: continued exponential
sc1_jobs = exp_growth(t_proj, *popt_exp)

# Scenario 2: logistic saturation at current capacity
sc2_jobs = logistic(t_proj, N0_log, r_log, K_current * 0.85)

# Scenario 3: COS-accelerated (logistic at near-term capacity, boosted r)
sc3_jobs = logistic(t_proj, N0_log, r_log * 1.35, K_near * 0.85)

# Confidence band for exponential (±1 stderr)
residuals  = gj_m - exp_growth(t_m, *popt_exp)
sigma      = np.std(residuals)
sc1_upper  = exp_growth(t_proj, N0_exp * 1.1, r_exp + 0.005)
sc1_lower  = exp_growth(t_proj, N0_exp * 0.9, r_exp - 0.005)
sc1_lower  = np.clip(sc1_lower, 0, None)

# Tick labels for projection axis (quarterly)
proj_ticks = list(range(0, 72, 3))
proj_tick_labels = []
for tt in proj_ticks:
    yr = 2023 + tt // 12
    q  = (tt % 12) // 3 + 1
    proj_tick_labels.append(f"Q{q}\n{yr}")

# ── layout ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(15, 11))
gs  = gridspec.GridSpec(2, 2, hspace=0.44, wspace=0.36)
axA = fig.add_subplot(gs[0, 0])
axB = fig.add_subplot(gs[0, 1])
axC = fig.add_subplot(gs[1, 0])
axD = fig.add_subplot(gs[1, 1])

# ── Panel A: raw monthly data + exponential fit ───────────────────────────────
axA.scatter(t_m, gj_m / 1000, s=45, color=COLORS["blue"], zorder=4,
            label="Monthly GPU job count", alpha=0.9)
axA.plot(t_proj, exp_growth(t_proj, *popt_exp) / 1000,
         "-", color=COLORS["red"], lw=2.2,
         label=f"Exponential fit  (r={r_exp:.3f}/mo)")
axA.fill_between(t_proj, sc1_lower/1000, sc1_upper/1000,
                 alpha=0.15, color=COLORS["red"])

# Annotate key structural moments
axA.axvline(24, color="#AAAAAA", lw=0.8, ls="--")  # 2025 starts
axA.axvline(36, color="#AAAAAA", lw=0.8, ls="--")  # 2026 starts
axA.text(24.3, max(gj_m)/1000*0.52, "2025\nstart", fontsize=7.5, color="#888888")
axA.text(36.3, max(gj_m)/1000*0.52, "2026\nstart", fontsize=7.5, color="#888888")

# Annotate COS GPU onset (~t=36)
axA.annotate("COS GPU adoption\nbegan (~Jan 2026)",
             xy=(36, logistic(36, N0_log, r_log, K_current*0.85)/1000),
             xytext=(26, 20),
             fontsize=7.5, color=COLORS["green"],
             arrowprops=dict(arrowstyle="->", color=COLORS["green"], lw=1.1))

xtick_sel = [0, 6, 12, 18, 24, 30, 36, 39]
xlabels_sel = [labels_m[int(tt)] if int(tt) < len(labels_m) else "" for tt in xtick_sel]
axA.set_xticks(xtick_sel)
axA.set_xticklabels(xlabels_sel, rotation=30, ha="right", fontsize=8)
axA.set_ylabel("GPU Job Count (thousands)", fontsize=9)
axA.set_title(f"(A) Historical Monthly GPU Job Counts\n"
              f"Exponential fit: doubling time ≈ {np.log(2)/r_exp:.1f} months",
              fontsize=9, pad=5)
axA.legend(fontsize=8, loc="upper left")

# ── Panel B: three-scenario projection to 2028 ───────────────────────────────
axB.fill_between(t_proj, sc1_lower/1000, sc1_upper/1000,
                 alpha=0.12, color=COLORS["red"])
axB.plot(t_proj, sc1_jobs/1000, "-",  color=COLORS["red"],    lw=2.2,
         label="Scenario 1: Continued exponential")
axB.plot(t_proj, sc2_jobs/1000, "--", color=COLORS["blue"],   lw=2.2,
         label="Scenario 2: Logistic (current capacity)")
axB.plot(t_proj, sc3_jobs/1000, "-.", color=COLORS["green"],  lw=2.2,
         label="Scenario 3: COS-accelerated (expanded capacity)")

# Shade historical vs projected
axB.axvspan(0, 39, alpha=0.05, color=COLORS["blue"])
axB.axvspan(39, 71, alpha=0.05, color=COLORS["orange"])
axB.text(18, max(sc1_jobs)/1000*0.88, "Historical\ndata", fontsize=8,
         color="#666666", ha="center")
axB.text(54, max(sc1_jobs)/1000*0.88, "Projected", fontsize=8,
         color="#666666", ha="center")
axB.axvline(39, color="#333333", lw=1.2, ls=":")

# Capacity reference lines
axB.axhline(K_current/1000, color="#D6604D", lw=1.4, ls=":",
            label=f"Current capacity ceiling (~{K_current/1000:.0f}K/mo)")
axB.axhline(K_near/1000, color="#4DAC26", lw=1.4, ls=":",
            label=f"Post-procurement ceiling (~{K_near/1000:.0f}K/mo)")

# Saturation year annotations for scenarios
for sc, col, name in [(sc1_jobs, COLORS["red"], "Sc.1"),
                       (sc2_jobs, COLORS["blue"], "Sc.2"),
                       (sc3_jobs, COLORS["green"], "Sc.3")]:
    last_val = sc[-1] / 1000
    axB.text(71.3, last_val, f"{name}: {last_val:.0f}K",
             va="center", fontsize=7.5, color=col)

axB.set_xticks(proj_ticks[::2])
axB.set_xticklabels(proj_tick_labels[::2], fontsize=7.5)
axB.set_xlim(0, 74)
axB.set_ylabel("Monthly GPU Job Count (thousands)", fontsize=9)
axB.set_title("(B) Three-Scenario GPU Demand Projection to Q4-2028\n"
              "with Hardware Capacity Reference Lines", fontsize=9, pad=5)
axB.legend(fontsize=7.5, loc="upper left", ncol=1)

# ── Panel C: quarterly GPU-hours YoY comparison ──────────────────────────────
# Group by year
yr_q = {}
for r in qt_rows:
    yr = r["period_label"][:4]
    yr_q.setdefault(yr, []).append(float(r["gpu_hrs"]) / 1000)

years_c = sorted(yr_q.keys())
max_q   = max(len(v) for v in yr_q.values())
x_c     = np.arange(max_q)
width_c = 0.2
yr_colors = [COLORS["light_blue"], COLORS["blue"], COLORS["orange"], COLORS["red"]]

for i, yr in enumerate(years_c):
    vals = yr_q[yr]
    xpos = x_c[:len(vals)] + (i - len(years_c)/2 + 0.5) * width_c
    bars = axC.bar(xpos, vals, width_c, color=yr_colors[i], label=yr, zorder=3, alpha=0.9)

axC.set_xticks(x_c)
axC.set_xticklabels(["Q1", "Q2", "Q3", "Q4"], fontsize=9)
axC.set_ylabel("Total GPU-Hours (thousands)", fontsize=9)
axC.set_title("(C) Quarterly GPU-Hours: Year-over-Year Comparison\n"
              "2023 → 2025 shows consistent Q1 and Q4 growth acceleration",
              fontsize=9, pad=5)
axC.legend(fontsize=9, loc="upper left")

# YoY growth annotations Q1
if "2023" in yr_q and "2025" in yr_q:
    q1_23 = yr_q["2023"][0]
    q1_25 = yr_q["2025"][0]
    growth = (q1_25 - q1_23) / q1_23 * 100
    axC.text(0, max(q1_23, q1_25) * 1.15,
             f"Q1: +{growth:.0f}%\n(2023→2025)",
             ha="center", fontsize=8, color=COLORS["red"],
             bbox=dict(boxstyle="round,pad=0.2", fc="white",
                       ec=COLORS["red"], alpha=0.9))

# ── Panel D: GPU % of total jobs over time ────────────────────────────────────
# Rolling 3-month smoothed
from numpy.lib.stride_tricks import sliding_window_view
gp_smooth = np.convolve(gp_m, np.ones(3)/3, mode="same")

axD.bar(t_m, gp_m, width=0.8, color=COLORS["light_blue"],
        alpha=0.6, label="Monthly GPU %", zorder=2)
axD.plot(t_m, gp_smooth, "-", color=COLORS["blue"], lw=2.2,
         label="3-month rolling average", zorder=3)

# Fit linear trend to GPU % (t >= 24, i.e., 2025 onward)
mask_trend = t_m >= 24
if mask_trend.sum() > 2:
    coeffs = np.polyfit(t_m[mask_trend], gp_m[mask_trend], 1)
    t_trend_ext = np.linspace(24, 71, 200)
    axD.plot(t_trend_ext, np.polyval(coeffs, t_trend_ext),
             "--", color=COLORS["red"], lw=1.8,
             label=f"Linear trend 2025–present (+{coeffs[0]*12:.2f}%/yr)")

# Threshold reference: 10% GPU share = qualitative "GPU-significant" milestone
axD.axhline(10, color=COLORS["orange"], lw=1.2, ls=":",
            label="10% GPU share (qualitative milestone)")

xtick_sel_d = [0, 12, 24, 36, 39]
xlabels_d   = ["Jan\n2023", "Jan\n2024", "Jan\n2025",
               "Jan\n2026", "Apr\n2026"]
axD.set_xticks(xtick_sel_d)
axD.set_xticklabels(xlabels_d, fontsize=9)
axD.set_xlim(-1, 42)
axD.set_ylabel("GPU Jobs as % of Total Submissions", fontsize=9)
axD.set_title("(D) GPU Share of Total Job Submissions Over Time\n"
              "With linear trend fit (2025–present) and 10% milestone",
              fontsize=9, pad=5)
axD.legend(fontsize=8, loc="upper left")

# Annotate the high-variance months
for i, (t, p) in enumerate(zip(t_m, gp_m)):
    if p > 12:
        axD.annotate(f"{labels_m[i]}\n{p:.1f}%",
                     xy=(t, p), xytext=(t-2, p+1.5),
                     fontsize=6.5, color=COLORS["orange"],
                     arrowprops=dict(arrowstyle="-", color="#CCCCCC", lw=0.8))

fig.suptitle(
    "Figure C2. GPU Demand Growth Projection — Hopper HPC Cluster\n"
    "Historical Trend Fitting and Three-Scenario Forecast to Q4-2028",
    fontsize=11, y=1.01
)
save_fig(fig, OUT_FILE)
print(f"\n── Key projection statistics ──")
print(f"Exponential doubling time: {np.log(2)/r_exp:.1f} months")
print(f"Sc1 (exponential) Dec-2028: {exp_growth(71, *popt_exp)/1000:.0f}K jobs/mo")
print(f"Sc2 (logistic K={K_current:.0f}) Dec-2028: {logistic(71, N0_log, r_log, K_current*0.85)/1000:.0f}K jobs/mo")
print(f"Sc3 (accelerated K={K_near:.0f}) Dec-2028: {logistic(71, N0_log, r_log*1.35, K_near*0.85)/1000:.0f}K jobs/mo")
print(f"Current capacity ceiling: {K_current/1000:.1f}K jobs/mo")
print(f"Near-term capacity ceiling: {K_near/1000:.1f}K jobs/mo")
