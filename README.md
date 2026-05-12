# Hopper HPC Utilization Paper

**Longitudinal Analysis of HPC Utilization at a Research University:  
Trends, Insights, and Data-Driven Interventions for Optimized Resource Allocation**

*George Mason University — Office of Research Computing*

---

## Repository structure

```
hopper_hpc_paper/
│
├── main.tex              ← Main LaTeX document (compile this)
├── references.bib        ← BibTeX bibliography (22 references)
├── .gitignore
├── README.md             ← This file
│
├── figures/              ← All 8 paper figures (300 DPI PNG)
│   ├── fig1_annual_volume.png
│   ├── fig2_college_jobs.png
│   ├── fig3_department_comparison.png
│   ├── fig4_gpu_analysis.png
│   ├── fig5_queue_dynamics.png
│   ├── fig6_cpu_distribution.png
│   ├── fig7_instructional_gpu.png
│   └── fig8_active_users.png
│
├── scripts/              ← Python scripts that generate the figures
│   ├── plot_config.py    ← Shared style settings (edit colors/fonts here)
│   ├── run_all.py        ← Run this to regenerate all figures at once
│   ├── fig1_annual_volume.py
│   ├── fig2_college_jobs.py
│   ├── fig3_department_comparison.py
│   ├── fig4_gpu_analysis.py
│   ├── fig5_queue_dynamics.py
│   ├── fig6_cpu_distribution.py
│   ├── fig7_instructional_gpu.py
│   └── fig8_active_users.py
│
└── data/                 ← Tab-separated source data for all figures
    ├── table1_annual_volume.txt
    ├── table2_college_jobs.txt
    ├── table3_cec_cpu.txt
    ├── table4_cec_gpu.txt
    ├── table5_cos_cpu.txt
    ├── table6_cos_gpu.txt
    ├── table7_instructional_gpu.txt
    ├── table8_top_gpu_users.txt
    ├── table9_queue_times.txt
    ├── monthly_volume_2025.txt
    ├── monthly_volume_f25_sp26.txt
    ├── cpu_request_distribution.txt
    ├── active_users_weekday.txt
    └── gpu_lorenz_curve.txt
```

---

## Quick start — compile locally

**Requirements:** TeX Live 2022+ or MiKTeX, with `pdflatex` and `bibtex`.

```bash
git clone <your-repo-url>
cd hopper_hpc_paper

pdflatex main.tex
bibtex   main
pdflatex main.tex
pdflatex main.tex    # second pass resolves all cross-references
```

Or with `latexmk` (recommended — handles the full compile cycle automatically):

```bash
latexmk -pdf -bibtex main.tex
```

The compiled PDF will appear as `main.pdf`.

---

## Connecting to Overleaf via Git

Overleaf supports two-way Git synchronisation so you can edit in Overleaf
and push/pull changes to/from this GitHub repository.

### Step 1 — Push this repo to GitHub

```bash
cd hopper_hpc_paper
git init
git add .
git commit -m "Initial commit: paper, figures, scripts, data"

# Create a new GitHub repository (do NOT initialise with a README)
# Then add it as remote and push:
git remote add origin https://github.com/<your-username>/<repo-name>.git
git branch -M main
git push -u origin main
```

### Step 2 — Import into Overleaf from GitHub

1. Log in to [overleaf.com](https://www.overleaf.com).
2. Click **New Project → Import from GitHub**.
3. Authorise Overleaf to access your GitHub account (one-time).
4. Select `<repo-name>` from the list and click **Import to Overleaf**.

Overleaf will create a new project that is linked to your GitHub repository.

### Step 3 — Configure Overleaf compiler

In the Overleaf project:

1. Click the **Menu** button (top-left ☰).
2. Under **Settings**:
   - **Compiler**: `pdfLaTeX`
   - **TeX Live version**: `2023` (or latest available)
   - **Main document**: `main.tex`
   - **Bibliography tool**: `BibTeX`
3. Click the green **Recompile** button.

### Step 4 — Sync changes between Overleaf and GitHub

**Pull changes from GitHub into Overleaf** (after you push from your local machine):

In the Overleaf project: **Menu → GitHub → Pull**.

**Push Overleaf edits back to GitHub**:

In the Overleaf project: **Menu → GitHub → Push**.

> **Tip:** Always pull before you push to avoid merge conflicts.

---

## Regenerating figures

If you update the source data in `data/` and want to regenerate the figures:

```bash
# Install Python dependencies (only needed once)
pip install matplotlib numpy pandas seaborn

# Regenerate all 8 figures
cd hopper_hpc_paper
python scripts/run_all.py
```

This overwrites the PNGs in `figures/`. Then commit and push:

```bash
git add figures/
git commit -m "Update figures from revised data"
git push
```

In Overleaf: **Menu → GitHub → Pull** to pick up the new figures.

---

## Modifying a single figure

Each `scripts/figN_*.py` file is self-contained. For example, to update
the queue-dynamics plot:

```bash
python scripts/fig5_queue_dynamics.py
# → saves figures/fig5_queue_dynamics.png
```

The data it reads is `data/table9_queue_times.txt`. Edit the `.txt` file
then re-run the script.

---

## Style customisation

All figures share the style configuration in `scripts/plot_config.py`:

| Setting | Where | Default |
|---------|-------|---------|
| Primary colour palette | `COLORS` dict | Blue `#2166AC`, Red `#D6604D`, Green `#4DAC26` … |
| Figure DPI (save) | `rcParams["savefig.dpi"]` | 300 |
| Figure DPI (screen) | `rcParams["figure.dpi"]` | 150 |
| Font family | `rcParams["font.family"]` | DejaVu Sans (LaTeX-compatible) |
| Axis spines | `rcParams["axes.spines.*"]` | Top/right removed |

Edit `plot_config.py` and re-run `run_all.py` to apply changes to all figures.

---

## LaTeX document structure (`main.tex`)

| Section | `\label` | Contents |
|---------|----------|----------|
| 1 — Introduction | `sec:intro` | Motivation, three key findings, paper outline |
| 2 — Related Work | `sec:related` | HPC utilisation, GPU computing, instructional use, CaRCC |
| 3 — System & Data | `sec:system` | Hopper description, data periods, fields extracted |
| 4 — Methodology | `sec:method` | Metrics, classification, longitudinal comparison |
| 5 — Results | `sec:results` | Eight subsections, one per analysis dimension |
| 6 — Discussion | `sec:discussion` | Four structural findings interpreted |
| 7 — Interventions | `sec:interventions` | Personnel, policy, infrastructure, training |
| 8 — Conclusion | `sec:conclusion` | Summary and future work |

Figures are referenced as `\ref{fig:annual_volume}`, `\ref{fig:college}`, etc.  
Tables are referenced as `\ref{tab:annual}`, `\ref{tab:cec_cpu}`, etc.

---

## Figure–table correspondence

| Figure | Table(s) | Section |
|--------|----------|---------|
| `fig1_annual_volume.png` | `tab:annual` | 5.1 |
| `fig2_college_jobs.png` | `tab:college` | 5.2 |
| `fig3_department_comparison.png` | `tab:cec_cpu`, `tab:cec_gpu`, `tab:cos_cpu`, `tab:cos_gpu` | 5.3–5.4 |
| `fig4_gpu_analysis.png` | `tab:top_users` | 5.5 |
| `fig5_queue_dynamics.png` | `tab:queue` | 5.8 |
| `fig6_cpu_distribution.png` | *(inline text)* | 5.7 |
| `fig7_instructional_gpu.png` | `tab:instructional` | 5.6 |
| `fig8_active_users.png` | *(inline text)* | 5.1, 5.3 |

---

## Data file format

All files in `data/` are plain-text, tab-separated values (TSV):

- Lines beginning with `#` are comments.
- The first non-comment line is the column header.
- Subsequent lines are data rows.
- Numbers use `.` as the decimal separator.

They can be opened directly in Excel, LibreOffice Calc, or read with
`pandas.read_csv(..., sep='\t', comment='#')`.

---

## Dependencies

| Tool | Version | Purpose |
|------|---------|---------|
| Python | ≥ 3.8 | Figure generation |
| matplotlib | ≥ 3.6 | Plotting |
| numpy | ≥ 1.22 | Numerical arrays |
| pandas | ≥ 1.5 | Data loading (optional) |
| seaborn | ≥ 0.12 | (imported by some scripts) |
| pdflatex | TeX Live 2022+ | PDF compilation |
| bibtex | TeX Live 2022+ | Bibliography |

---

## Citation

If you use the analysis or figures from this work, please cite:

```bibtex
@techreport{orc2026hopper,
  author      = {{GMU Office of Research Computing}},
  title       = {Longitudinal Analysis of {HPC} Utilization at a Research
                 University: Trends, Insights, and Data-Driven Interventions
                 for Optimized Resource Allocation},
  institution = {George Mason University},
  address     = {Fairfax, VA},
  year        = {2026}
}
```

---

*Last updated: May 2026 — GMU Office of Research Computing*
