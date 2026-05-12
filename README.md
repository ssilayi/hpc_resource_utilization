# Hopper HPC Utilization Paper

**Longitudinal Analysis of HPC Utilization at a Research University:  
Trends, Insights, and Data-Driven Interventions for Optimized Resource Allocation**


---

## Project Overview

This repository contains the LaTeX paper, Python figure-generation scripts, and
source data for a longitudinal study of the Hopper HPC cluster at George Mason
University. The work spans two complementary analysis streams developed in
parallel within the GMU ORC:

### Stream 1 — Cluster utilization statistics (this repo)

Analysis of Slurm job accounting records to characterise how researchers across
GMU colleges and departments use Hopper. We extract CPU/GPU job counts, resource
consumption (CPU-hours, GPU-hours, memory), wait times, and instructional account
usage across three periods:

| Period | Window | Total Jobs |
|--------|--------|------------|
| AY 2023–2024 (baseline) | Jul 2023 – Jun 2024 | ~1.65M est. |
| Full Year 2025 (retrospective) | Jan – Dec 2025 | 2,283,321 |
| Fall 2025 – Spring 2026 (current) | Aug 2025 – Apr 2026 | 2,905,604 |

### Stream 2 — OS ticket analysis (companion repo)

NLP-based analysis of the OSTicket help-desk database to understand researcher
support needs. Tickets are extracted from the OSTicket MySQL database, matched
with Slurm user records via fuzzy name matching, and categorised using
transformer-based clustering (`all-MiniLM-L6-v2`). Key findings: semester-
correlated ticket spikes, software support as the dominant ticket category, and
steadily increasing ticket volume from 2021–2024.

> **Companion repository:**
> ```bash
> git clone https://gitlab.orc.gmu.edu/Abhinav/os_tickets_analysis.git
> ```

Combining both streams allows ORC to move from *describing* cluster usage to
*anticipating* user needs and deploying limited personnel resources more
strategically — the core thesis of the framing document
*Quantifying HPC Utilization for Optimized Resource Deployment* (2022).

---

## Compute Environment

### Clusters (GMU ORC)

**Hopper** — primary cluster (subject of this analysis)
- 11,840 CPU cores
- Slurm workload manager
- Dual high-speed networking: 100 Gbps Ethernet spine / 25 Gbps leaf +
  HDR InfiniBand (100 Gbps per node)
- VAST flash-based scratch storage
- GPU partition: NVIDIA A100 (40 GB & 80 GB), A40, H100, B200 via MIG and
  full-device configurations
- Access via SSH or Open OnDemand web interface
  (JupyterLab, MATLAB, RStudio, interactive desktop)

**Argo** — secondary cluster (not analysed here)
- 2,000 CPU cores, 16–32 cores/node, ≥4 GB/core
- High-memory nodes up to 1.5 TB RAM
- GPUs: 4× NVIDIA V100 32 GB (NVLink) + K80 nodes (20 devices)
- FDR InfiniBand (56 Gbps)

### ORC Personnel — CaRCC Facings

Resources at an HPC centre comprise *compute resources* and *personnel*.
Following the [CaRCC Research Computing and Data Professionals framework](https://carcc.org/wp-content/uploads/2019/01/CI-ProfessionalizationJob-Families-and-CareerGuide.pdf),
GMU ORC personnel are organised into four facings:

| Facing | Role | Headcount |
|--------|------|-----------|
| Researcher-Facing | Computational Scientists + GRAs | 3 + 2 |
| System-Facing | Systems Engineers | 3 |
| Software/Data-Facing | — | — |
| Sponsor/Stakeholder-Facing | Director | 1 |

A central goal of this work is using utilization data to inform *how*
researcher-facing specialists deploy their time — targeting heavy users,
emerging GPU adopters, and instructional accounts for maximum impact.

---

## Repository Structure

```
hopper_hpc_paper/
│
├── main.tex              ← Full LaTeX paper (compile this)
├── references.bib        ← BibTeX bibliography (22 entries)
├── main.pdf              ← Pre-compiled output (19 pages)
├── README.md             ← This file
├── .gitignore            ← Excludes LaTeX build artefacts & Python cache
│
├── figures/              ← 8 paper figures, 300 DPI PNG
│   ├── fig1_annual_volume.png          Table 1  — job volume across 3 periods
│   ├── fig2_college_jobs.png           Table 2  — jobs by institutional college
│   ├── fig3_department_comparison.png  Tables 3-6 — CEC & COS dept profiles
│   ├── fig4_gpu_analysis.png           Table 7  — GPU depts, Lorenz, top users
│   ├── fig5_queue_dynamics.png         Table 9  — monthly volume + wait times
│   ├── fig6_cpu_distribution.png                — bimodal CPU request histogram
│   ├── fig7_instructional_gpu.png      Table 8  — instructional GPU accounts
│   └── fig8_active_users.png                    — daily users + IST outlier
│
├── scripts/              ← Python figure-generation scripts
│   ├── plot_config.py    ← Shared colour palette, rcParams, helpers
│   ├── run_all.py        ← Run all 8 scripts in sequence
│   ├── fig1_annual_volume.py
│   ├── fig2_college_jobs.py
│   ├── fig3_department_comparison.py
│   ├── fig4_gpu_analysis.py
│   ├── fig5_queue_dynamics.py
│   ├── fig6_cpu_distribution.py
│   ├── fig7_instructional_gpu.py
│   └── fig8_active_users.py
│
└── data/                 ← Tab-separated source data (one file per table)
    ├── table1_annual_volume.txt           Aggregate job counts, 3 periods
    ├── table2_college_jobs.txt            Jobs by college, F25–Sp26
    ├── table3_cec_cpu.txt                 CEC CPU job stats by department
    ├── table4_cec_gpu.txt                 CEC GPU job stats by department
    ├── table5_cos_cpu.txt                 COS CPU job stats by department
    ├── table6_cos_gpu.txt                 COS GPU job stats by department
    ├── table7_instructional_gpu.txt       Instructional GPU accounts
    ├── table8_top_gpu_users.txt           Top GPU users (anonymised U01–U15)
    ├── table9_queue_times.txt             Monthly run/wait times, F25–Sp26
    ├── monthly_volume_2025.txt            Monthly jobs, Full Year 2025
    ├── monthly_volume_f25_sp26.txt        Monthly jobs, Fall 25 – Spring 26
    ├── cpu_request_distribution.txt       CPU cores requested histogram
    ├── active_users_weekday.txt           Avg daily users by day of week
    └── gpu_lorenz_curve.txt               GPU-hour concentration Lorenz curve
```

---

## Data Sources

### Slurm job accounting records

Exported from the Hopper Slurm database. Each record includes: user ID
(anonymised), account (encodes department + college), submit/start/end times,
requested and consumed CPUs, GPUs, nodes, memory, CPU-hours, GPU-hours, and
exit state. Instructional accounts follow the convention
`<course><number><semester><year>` (e.g., `cs678fl25` = CS 678, Fall 2025).

### OSTicket database (Stream 2 — companion repo)

Exported from the ORC OSTicket server via `mysqldump`, imported to a local MySQL
instance, and joined with Slurm user data for department-level attribution:

```bash
# On the ORC OSTicket server
mysqldump -u username -p osticket > osticket_dump.sql

# On your local machine
mysql -u username -p osticket < osticket_dump.sql
```

---

## Quick Start — Compile Locally

**Requirements:** TeX Live 2022+ or MiKTeX, Python 3.8+.

```bash
# Clone
git clone https://github.com/<your-username>/hopper_hpc_paper.git
cd hopper_hpc_paper

# Compile the paper (option A: manual)
pdflatex main.tex
bibtex   main
pdflatex main.tex
pdflatex main.tex   # second pass resolves all cross-references

# Compile (option B: latexmk — handles all passes automatically)
latexmk -pdf -bibtex main.tex

# Regenerate all figures
pip install matplotlib numpy pandas seaborn
python scripts/run_all.py
```

---

## Connecting to Overleaf via GitHub

### Step 1 — Push to GitHub

```bash
git init                          # skip if already a repo
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/<you>/<repo>.git
git branch -M main
git push -u origin main
```

### Step 2 — Import into Overleaf

1. Log in to [overleaf.com](https://www.overleaf.com).
2. **New Project → Import from GitHub**.
3. Authorise Overleaf's GitHub access (one-time OAuth).
4. Select the repository and click **Import to Overleaf**.

### Step 3 — Configure Overleaf settings

Menu ☰ → Settings:

| Setting | Value |
|---------|-------|
| Compiler | `pdfLaTeX` |
| TeX Live version | 2023 (or latest) |
| Main document | `main.tex` |
| Bibliography tool | `BibTeX` |

Click the green **Recompile** button. The paper compiles to 19 pages.

### Step 4 — Sync workflow

| Direction | Action |
|-----------|--------|
| GitHub → Overleaf | Menu → GitHub → **Pull** |
| Overleaf → GitHub | Menu → GitHub → **Push** |

> Always **Pull** before **Push** to avoid merge conflicts.

---

## Paper Structure (`main.tex`)

| § | Label | Contents |
|---|-------|----------|
| 1 | `sec:intro` | Motivation, three structural findings, paper outline |
| 2 | `sec:related` | HPC utilisation, GPU in academic HPC, instructional use, CaRCC |
| 3 | `sec:system` | Hopper hardware, Slurm data sources, three coverage periods |
| 4 | `sec:method` | Metrics, job classification, longitudinal comparison |
| 5 | `sec:results` | 8 subsections: volume, college, CEC depts, COS depts, GPU, instructional, CPU distribution, queue |
| 6 | `sec:discussion` | Structural transformation, GPU transition, instructional contention, bimodal CPU gap, congestion |
| 7 | `sec:interventions` | Personnel specialisation, queue/scheduling policy, infrastructure, outreach |
| 8 | `sec:conclusion` | Summary and future work (NLP ticket integration) |

### Figure–Table map

| Figure | Paper tables | `\label` |
|--------|-------------|---------|
| `fig1_annual_volume.png` | Tab. 1 | `fig:annual_volume` |
| `fig2_college_jobs.png` | Tab. 2 | `fig:college` |
| `fig3_department_comparison.png` | Tabs. 3–6 | `fig:dept` |
| `fig4_gpu_analysis.png` | Tab. 7 | `fig:gpu` |
| `fig5_queue_dynamics.png` | Tab. 9 | `fig:queue` |
| `fig6_cpu_distribution.png` | *(inline)* | `fig:cpu_dist` |
| `fig7_instructional_gpu.png` | Tab. 8 | `fig:instructional` |
| `fig8_active_users.png` | *(inline)* | `fig:users` |

---

## Related Work and Repositories

| Work | Description | Location |
|------|-------------|----------|
| **OS Ticket Analysis** | NLP/ML categorisation of ORC help-desk tickets (OSTicket MySQL → transformer clustering); companion to this paper| |
| **GPU Utilization Statistics** | Early GPU-focused Hopper utilisation dashboard  |
| **Quantifying HPC Utilization (2022)** | Original framing paper: CaRCC personnel deployment model + Slurm/ticket methodology | Included in project knowledge base |
| **Hopper Stats 2023–2024** | Baseline utilisation report | Project knowledge base |
| **Hopper Stats 2025 Retrospective** | Full-year 2025 report | Project knowledge base |
| **Hopper Stats Fall 2025–Spring 2026** | Current-period report | Project knowledge base |

---

## Tech Stack

### Figure generation

| Package | Use |
|---------|-----|
| `matplotlib ≥ 3.6` | All plots |
| `numpy ≥ 1.22` | Array operations |
| `pandas ≥ 1.5` | TSV data loading |
| `seaborn ≥ 0.12` | Colour utilities |

### Ticket NLP (companion repo only)

| Package | Use |
|---------|-----|
| `sentence-transformers` | Sentence embeddings (`all-MiniLM-L6-v2`) |
| `scikit-learn` | Agglomerative clustering |
| `transformers` (HuggingFace) | Pre-trained LLM backbone |
| `tensorflow` / `pytorch` | Deep learning backend |
| `fuzzywuzzy` | Fuzzy name matching (Slurm ↔ OSTicket) |
| `wordcloud` | Ticket keyword visualisation |
| `mysql-connector-python` | OSTicket database connection |

### LaTeX packages

| Package | Use |
|---------|-----|
| `natbib` + `abbrvnat` | Numbered citations (`\citep`, `\citet`) |
| `booktabs` + `tabularx` | Publication-quality tables |
| `graphicx` | `\includegraphics` for figures |
| `hyperref` | Coloured cross-references + PDF metadata |
| `geometry` | 1-inch margins, letter paper |

---

## Style Customisation

All figures inherit from `scripts/plot_config.py`. Edit once, regenerate all:

```python
COLORS = {
    "blue":    "#2166AC",   # CPU jobs, primary series
    "red":     "#D6604D",   # Wait times, congestion, GPU hours
    "green":   "#4DAC26",   # COS data, Fall25–Sp26 series
    "orange":  "#E08214",   # Total jobs, GPU stacked bars
    "purple":  "#762A83",   # GPU % trend line
    "gray":    "#878787",   # Background / intermediate ranges
}
```

---

## Data File Format

All `data/*.txt` files are plain-text TSV:

```
# Lines beginning with # are comments
# First non-comment line = column headers
# Decimal separator: .  |  User IDs in table8: anonymised as U01–U15
```

```python
import pandas as pd
df = pd.read_csv("data/table3_cec_cpu.txt", sep="\t", comment="#")
```

---

## Citation

```bibtex
@techreport{orc2026hopper,
  author      = {{Silayi, Swabir}},
  title       = {Longitudinal Analysis of {HPC} Utilization at a Research
                 University: Trends, Insights, and Data-Driven Interventions
                 for Optimized Resource Allocation},
  institution = {Office of Research Computing, George Mason University},
  address     = {Fairfax, VA, USA},
  year        = {2026},
  url         = {https://orc.gmu.edu}
}
```

