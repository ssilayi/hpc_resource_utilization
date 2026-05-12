"""
run_all.py
Execute all figure-generation scripts in sequence.
Run from the hpc_plots/ directory:
    python scripts/run_all.py

All figures are saved to hpc_plots/figures/
"""

import subprocess
import sys
import os
import time

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.dirname(SCRIPT_DIR)

FIGURES_DIR = os.path.join(ROOT_DIR, "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

scripts = [
    "fig1_annual_volume.py",          # Fig 1:  Annual job volume trend (3 periods)
    "fig2_college_jobs.py",           # Fig 2:  Jobs by institutional college
    "fig3_department_comparison.py",  # Fig 3:  CEC and COS department profiles
    "fig4_gpu_analysis.py",           # Fig 4:  GPU analysis — dept, Lorenz, top users
    "fig5_queue_dynamics.py",         # Fig 5:  Monthly volume + wait/run times
    "fig6_cpu_distribution.py",       # Fig 6:  Bimodal CPU request distribution
    "fig7_instructional_gpu.py",      # Fig 7:  Instructional GPU utilization
    "fig8_active_users.py",           # Fig 8:  Active users + IST outlier profile
    "figA2_failure_analysis.py",      # Fig A2: Job failure rate analysis
    "figC2_gpu_growth_projection.py", # Fig C2: GPU demand growth projection
]

print("=" * 60)
print("Hopper HPC Utilization Paper — Figure Generator")
print("=" * 60)
print(f"Output directory: {FIGURES_DIR}\n")

successes = []
failures  = []

for script in scripts:
    path = os.path.join(SCRIPT_DIR, script)
    print(f"▶ Running {script} ...", end=" ", flush=True)
    t0 = time.time()
    result = subprocess.run(
        [sys.executable, path],
        capture_output=True, text=True,
        cwd=ROOT_DIR
    )
    elapsed = time.time() - t0
    if result.returncode == 0:
        print(f"✓  ({elapsed:.1f}s)")
        successes.append(script)
    else:
        print(f"✗  FAILED ({elapsed:.1f}s)")
        print(f"   stderr: {result.stderr.strip()[:300]}")
        failures.append(script)

print("\n" + "=" * 60)
print(f"Done: {len(successes)}/{len(scripts)} figures generated successfully.")
if failures:
    print(f"Failed: {failures}")
print("=" * 60)

# List generated files
print("\nGenerated files:")
for f in sorted(os.listdir(FIGURES_DIR)):
    fp = os.path.join(FIGURES_DIR, f)
    size_kb = os.path.getsize(fp) / 1024
    print(f"  {f:<50} {size_kb:6.1f} KB")
