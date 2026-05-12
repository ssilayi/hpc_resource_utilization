# Hopper HPC – Updated Resource Deployment Plan (through Spring 2026)
**George Mason University – Office of Research Computing**
*Updated: May 2026 | Covers data from 2023–2024 → 2025 Retrospective → Fall 2025 – Spring 2026*

---

## Executive Summary

Since the original plan was developed using 2023–2024 usage data, Hopper has undergone a structural shift in how it is used. Total job volume grew from roughly 1.5–1.8M annually to 2.28M in 2025 and is on pace for 3.5M+ in 2026. More importantly, the character of that usage has changed: GPU demand has accelerated sharply; COS (College of Science) usage has nearly tripled; IST (Information Sciences & Technology, within CEC) has emerged as the single largest departmental job submitter; instructional use of GPU resources is now widespread across engineering, computer science, and IT curricula; and COS is beginning to adopt GPU workflows for the first time. Each of these shifts requires a targeted response.

The updated plan below provides revised recommendations for personnel deployment, queue management, infrastructure planning, and outreach strategy through AY 2026–2027.

---

## 1. Comprehensive Usage Snapshot

### 1.1 Annual Job Volume

| Period | CPU Jobs | GPU Jobs | Total | GPU % |
|--------|----------|----------|-------|-------|
| AY 2023–2024 (baseline est.) | ~1.4–1.6M | ~55–70K est. | ~1.5–1.8M | ~3–5% |
| Jan–Dec 2025 (full year) | 2,159,248 | 124,073 | **2,283,321** | 5.4% |
| Aug 2025–Apr 2026 (9 months) | 2,777,817 | 127,787 | **2,905,604** | 4.4% |

The 9-month Fall 2025–Spring 2026 window already surpasses the entire 2025 annual total — a clear signal of accelerating growth. On a per-month basis, job volume has roughly doubled since 2023–2024.

### 1.2 GPU Growth Detail

Monthly GPU job counts from the 2025 Retrospective averaged ~10,000–12,000/month through the year. By Spring 2026, daily GPU job peaks were regularly exceeding 1,500–2,000 jobs/day — a level not seen even a year prior. GPU resource requests (NGPUS) are also scaling up: average NGPUS per GPU job in Fall 2025–Spring 2026 ranged from ~0.95 to 1.30 depending on month, with several users regularly requesting 3–5 GPUs per job. GPU hour consumption is heavily concentrated at the top (top user: 134K GPU hrs in 9 months).

### 1.3 Active User Base

| Metric | 2025 (annual) | Fall 2025–Spring 2026 |
|--------|--------------|----------------------|
| Avg active users, Tuesday (peak) | **617/day** | 411/day |
| Avg active users, Saturday | 506/day | 320/day |
| Avg active users, Sunday | 514/day | 323/day |

Weekend usage (320–514 unique users/day) confirms a highly engaged, self-directed community that is not purely weekday-driven. This has implications for support coverage and asynchronous resource availability (documentation, OOD, automated responses).

---

## 2. College-Level Findings and Updated Priorities

### 2.1 CEC – College of Engineering and Computing (63.7% of all jobs)

**CPU Jobs by Department (Fall 2025–Spring 2026):**

| Dept | CPU Jobs | Total CPU Hrs | Avg CPU Hrs/Job | Avg MEM (GB) |
|------|----------|---------------|-----------------|--------------|
| ist (Information Sciences & Technology) | **785,603** | 417,913 | **0.53** | 4.10 |
| ceie (Civil, Env., Infrastructure Eng.) | 403,909 | 7,592,789 | 18.80 | 35.27 |
| stat (Statistics) | 404,830 | 2,598,905 | 6.42 | 13.30 |
| cs (Computer Science) | 128,234 | 4,044,583 | 31.54 | 34.61 |
| cyse (Cyber Security Eng.) | 2,138 | 298,125 | 139.44 | 221.67 |
| ece (Electrical & Computer Eng.) | 3,339 | 679,437 | 203.49 | 32.56 |
| daen (Data Analytics Eng.) | 337 | 68,950 | 204.60 | 48.94 |
| me (Mechanical Engineering) | 474 | 217,120 | 458.06 | 143.81 |
| beng (Bioengineering) | 2,062 | 72,519 | 35.17 | 151.23 |

**Key finding:** IST submits nearly twice as many CPU jobs as any other department within CEC, but each job runs for only ~32 minutes on average. This is consistent with high-throughput parameter sweeps, automated pipelines, or classroom exercises rather than research-grade long-running simulations. IST jobs are high volume but low individual resource cost, meaning they primarily contribute to queue length rather than resource saturation.

By contrast, **me** (Mechanical Engineering) averages 458 CPU hours per job — nearly 900× the IST per-job average. **daen**, **ece**, and **cyse** also show very high per-job CPU hours, suggesting simulation-heavy research (CFD, circuit simulation, ML training).

**GPU Jobs by Department (Fall 2025–Spring 2026):**

| Dept | GPU Jobs | Total GPU Hrs | Avg GPU Hrs | Avg MEM (GB) |
|------|----------|---------------|-------------|--------------|
| cs | **57,388** | 424,339 | 7.39 | 79.20 |
| ist | 33,244 | 220,620 | 6.64 | 110.84 |
| ece | 16,750 | 74,278 | 4.43 | 41.85 |
| seor (Systems Eng. & Operations Res.) | 1,077 | 25,688 | 23.85 | 86.54 |
| cyse | 3,437 | 7,003 | 2.04 | 90.16 |
| daen | 145 | 3,809 | 26.27 | 63.59 |

**Key finding:** CS is the dominant GPU user in CEC by job count (57K jobs), while IST punches above its weight in GPU volume given its even larger CPU job count. Seor and daen, despite their small job counts, run long individual GPU jobs, suggesting research-grade model training. IST's high average GPU memory request (110 GB/job) is notable and may indicate that many IST GPU jobs are requesting full A100 80GB or larger allocations.

### 2.2 COS – College of Science (33.3% of all jobs, up from ~15% in 2025)

**Dramatic growth:** In the full 2025 year, COS submitted only 342,096 CPU jobs. By Fall 2025–Spring 2026 (just 9 months), COS had 967,083 jobs — a 2.8× increase. This is the single biggest structural shift in the usage data and represents COS becoming a genuine co-equal primary user alongside CEC.

**CPU Jobs by Department (Fall 2025–Spring 2026):**

| Dept | CPU Jobs | Total CPU Hrs | Avg CPU Hrs | Avg MEM (GB) |
|------|----------|---------------|-------------|--------------|
| aoes (Atmospheric, Ocean & Earth Sci.) | 105,579 | 5,106,174 | 48.36 | 254.60 |
| phys (Physics & Astronomy) | 164,088 | 15,371,947 | 93.68 | 83.78 |
| math (Mathematical Sciences) | 25,265 | 2,686,842 | 106.35 | 54.78 |
| biol (Biology) | 18,187 | 525,899 | 28.92 | 110.07 |
| ggs (Geography & Geo-Information Sci.) | 9,192 | 877,813 | 95.50 | 227.83 |
| cds (Computational & Data Science) | 8,587 | 751,942 | 87.57 | 27.58 |
| chem (Chemistry & Biochem.) | 4,439 | 1,146,580 | 258.30 | 188.83 |

**Key finding:** Physics (phys) dominates by CPU hours (15.4M hrs) despite being only the largest by job count. Chemistry (chem) runs the longest average jobs (~258 CPU hrs/job) — molecular simulation, quantum chemistry, and materials modeling are characteristic of this pattern. GGS (geographic sciences) and aoes average high memory per job (>225 GB), consistent with large geospatial datasets and climate models.

**GPU Jobs by Department (COS, Fall 2025–Spring 2026):**

| Dept | GPU Jobs | GPU Hrs | Avg GPU Hrs | Avg MEM (GB) |
|------|----------|---------|-------------|--------------|
| aoes | 3,654 | 35,156 | 9.62 | 133.88 |
| ssb (School of Systems Biology) | 2,864 | 62,569 | 21.85 | 27.46 |
| cds | 558 | 8,782 | 15.74 | 38.10 |
| chem | 305 | 15,785 | 51.76 | 68.43 |
| ggs | 459 | 1,597 | 3.48 | 75.97 |
| math | 240 | 4,259 | 17.75 | 160.34 |

**Key finding: COS GPU use is a new phenomenon.** In the 2025 Retrospective, COS had essentially zero GPU jobs (only 2 recorded in the full year). By Fall 2025–Spring 2026, COS departments collectively submitted ~8,300 GPU jobs. This is the earliest phase of a GPU adoption curve in the natural sciences — aoes (atmospheric modeling with neural networks/ML emulators), ssb (systems biology/bioinformatics ML), chem (ML potentials, molecular dynamics), and cds are the leading edge.

### 2.3 Other Colleges

CHSS had 63,936 jobs — substantially up from prior years — but remains CPU-only with short job runtimes. CHHS, LAW, EHD remain marginal users. SOM (School of Management) had 2,660 jobs.

---

## 3. Instructional Use Analysis

### 3.1 Scale and Breadth

The instructional footprint has grown substantially. In Fall 2025–Spring 2026:

- **21+ distinct course accounts** submitted CPU jobs
- **20+ distinct course accounts** submitted GPU jobs
- GPU course accounts spanned CS, AIT, ECE, CDS, BINF, CYSE, and CSI prefixes

The largest instructional GPU accounts by job count:

| Account | Jobs | GPU Hrs | Avg GPU Hrs | Students |
|---------|------|---------|-------------|----------|
| cs678fl25 | 2,174 | 4,601 | 2.12 | 16 |
| alt726fl24 | 126 | 873 | 6.93 | 3 |
| alt726sp25 | 94 | 1,092 | 11.63 | 1 |
| cs471sp25 | 72 | 4,954 | 68.81 | 1 |
| cs747sp25 | 162 | 1,330 | 8.21 | 4 |
| cs757sp25 | 114 | 1,001 | 8.79 | 2 |

### 3.2 GPU Hardware Types Requested by Instructional Users

The instructional GPU type chart reveals requests across: **1g.10gb, 2g.20gb, 3g.40gb, a100.40gb, a100.80gb, b200.180gb, h100.80gb**. The presence of b200.180gb and h100.80gb requests from instructional accounts is significant — students are using (and expecting access to) the newest and most expensive GPU hardware, often for short durations.

**Implication:** This creates potential conflicts with research GPU users who need sustained access to these same cards. A GPU preemption or time-slicing policy for instructional accounts is warranted.

### 3.3 Instructional CPU Hours: The stat778 Anomaly

In the 2025 Retrospective, account **stat778sp25** stands out with an extremely high average CPU hours per job (~300+), suggesting a class in statistical computing running long simulation-based assignments. This class has appeared in both Fall 2024 and Spring 2025, confirming recurrence. The instructor should be engaged proactively before each semester to optimize job sizing.

---

## 4. Power User Analysis

### 4.1 Top GPU Hour Consumers (Fall 2025–Spring 2026)

| User | Total GPUHRS | Avg GPUHRS/Job | Notes |
|------|-------------|----------------|-------|
| xwang44 | 134,682 | very high | Also top by total NGPUS (8,167) and total GPU memory (987K GB) |
| xli62 | 22,553 | moderate | Top NGPUS 2nd, top GPU memory 2nd |
| afitz | 19,575 | high | |
| amukher6 | 18,350 | moderate | Also top by job count (5,233 GPU jobs) |
| ywijesu | 17,166 | high | |
| jhong38 | 16,830 | high | |

xwang44 alone accounts for more GPU hours than the next 6 users combined. This level of concentration — in a shared resource environment — almost certainly impacts queue access for other users during active submission periods.

### 4.2 Users by Average GPU Memory Requested per Job (Top Requesters)

| User | Avg MEM Requested (GB) |
|------|------------------------|
| xwang44 | 392.5 |
| cjaskiew | 350.0 |
| pbhanda2 | 319.9 |
| ddas6 | 257.1 |
| katwal | 256.0 |

These users are routinely requesting nearly full-node GPU memory. This is the profile of users who either genuinely need A100 80GB or H100-class GPUs, or who may be over-provisioning as a defensive measure against OOM errors.

### 4.3 High-AVG-GPU-Hours Users (Job-Level Intensity)

| User | Avg GPUHRS/Job |
|------|----------------|
| vsaluja2 | 180.8 hrs |
| atelkal | 120.0 hrs |
| rnag | 120.0 hrs |
| mcrawsha | 90.2 hrs |
| jhong38 | 85.9 hrs |

These users run very long individual GPU jobs (3–7 days per job). They are likely training large models or running computationally intensive simulations. They benefit most from dedicated time allocations and should be engaged about checkpointing strategies and walltime limits.

---

## 5. Queue Health Analysis

### 5.1 Wait Times and Pressure Events

| Month | Avg Run Time (hrs) | Avg Wait Time (hrs) | Assessment |
|-------|--------------------|---------------------|------------|
| 2025-08 | 1.17 | 1.25 | Normal |
| 2025-09 | 0.71 | 0.45 | Low — summer tail |
| 2025-10 | 1.04 | **4.29** | ⚠ Semester start surge |
| 2025-11 | 2.56 | 0.46 | Normalized |
| 2025-12 | 2.28 | 0.28 | Low — exam/holiday |
| 2026-01 | 1.50 | 1.37 | Normal |
| 2026-02 | 0.43 | 0.77 | Normal |
| 2026-03 | 0.68 | **3.40** | ⚠ Midterm/spring surge |
| 2026-04 | 0.93 | 1.74 | Elevated — dissertation/project season |

Two systematic congestion patterns emerge: **early Fall** (October) and **mid-Spring** (March). These correlate with semester start ramp-ups and midterm research pushes respectively.

### 5.2 February 2026 CPU Anomaly

Total NCPUS in February 2026 reached approximately 30 million — roughly 10–15× any other month. This was not accompanied by a proportionally elevated job count, which means one or a small number of jobs requested an extremely large core count. This warrants direct investigation: was this a legitimate, well-optimized parallel job, or a misconfigured allocation? If the latter, significant compute resources were effectively wasted.

### 5.3 CPU Request Distribution Pattern

The CPU request histogram shows a sharp spike at 1 CPU (>1.5M jobs), a secondary spike at ~48 CPUs, and then essentially zero between 2–47 and between 49–50. This bimodal pattern suggests two dominant user classes: single-threaded job submitters (serial parameter sweeps) and users aware of specific node-count conventions (48 CPUs = one full node on many configurations). There is a notable **gap in multi-core but sub-node jobs** (2–47 CPUs) — suggesting many researchers may not be effectively using shared-memory parallelism or that they lack guidance on intermediate-scale job sizing.

---

## 6. Updated Resource Deployment Plan

### 6.1 Personnel: Revised Priority Tiers

**Tier 1 – GPU Optimization Specialist (New Role)**

The data now unambiguously justifies a dedicated GPU specialist. GPU hours are concentrated in a small population; a single consultation with xwang44, afitz, or vsaluja2 could improve the efficiency of tens of thousands of GPU-hours per semester. This role should cover:

- Deep-dive job profiling (DCGM metrics, GPU utilization vs. allocation ratio)
- Multi-GPU and multi-node GPU workflows (MPI+CUDA, DDP training)
- Containerized GPU environments (Singularity/Apptainer with NGC containers)
- Memory optimization to reduce over-provisioning
- Checkpointing and restart for long-running GPU jobs

**Tier 2 – COS Liaison (Upgraded Priority)**

COS is no longer a secondary user — it is now co-equal to CEC in strategic importance. The liaison role needs a COS-specific focus with awareness of domain workflows: molecular dynamics (GROMACS, NAMD, AMBER), atmospheric modeling (WRF, MOM6), astrophysics (FLASH, Athena++), geospatial computing (GDAL, GRASS), and emerging COS GPU workloads (ML-based climate emulators, AlphaFold, molecular ML potentials). The large memory requests in AOES (254 GB avg) and GGS (227 GB avg) suggest that memory-optimized nodes or out-of-core computing support may also be needed.

**Tier 3 – IST/CS Instructional Coordinator (New Role or Expanded)**

IST alone submits more CPU jobs than any other department in the university. Most are very short (32-minute average), suggesting high-frequency automated submissions or classroom exercises. CS is the dominant GPU user by job count (57K GPU jobs). Together these two departments — largely undergraduate-serving in their instructional footprint — require a dedicated instructional coordinator who:

- Works with IST and CS instructors each semester to plan course compute needs
- Maintains course-specific SLURM templates and OOD environments
- Provides semester-start orientation sessions (timed before the October surge)
- Sets per-course GPU quotas on high-demand hardware (b200, h100)

**Tier 4 – ME/DAEN/ECE Heavy-Compute Liaison (Upgraded)**

Mechanical Engineering (avg 458 CPU hrs/job), Data Analytics Engineering (avg 204 CPU hrs/job), and Electrical/Computer Engineering (avg 203 CPU hrs/job) represent the most computationally intensive research users per job. These are high-value targets for optimization support — helping each group halve their CPU-hours through better parallelism or algorithmic improvements would have more resource impact than onboarding dozens of new light users.

**Tier 5 – Weekend/Async Support (New)**

Active users on weekends (320–514/day) do not have equivalent access to live support. Expanding async resources — comprehensive documentation, chatbot for common SLURM errors, recorded tutorials — would serve this significant portion of the community.

---

### 6.2 Queue Policies: Updated Recommendations

**GPU Fair-Share / Quota Policy (New)**

With a single user consuming more GPU hours than the next 6 combined, the current system has no effective check on individual GPU-resource concentration. Recommended actions:

1. Implement a **per-user GPU-hour weekly soft cap** (e.g., 10,000 GPU-hours/week), above which jobs are assigned lower priority rather than blocked, to prevent total monopolization while still allowing high-throughput work.
2. Introduce a **GPU type restriction policy for instructional accounts**: restrict course accounts to 1g.10gb, 2g.20gb, and 3g.40gb partitions unless a specific educational need for a100/h100/b200 is documented and approved by the instructor.
3. Set **walltime limits by partition**: standard GPU partition: max 72 hrs; high-memory GPU partition: max 120 hrs, requires consultation.

**Large-Job Review Process (New)**

The February 2026 anomaly demonstrates the risk of unchecked large-scale CPU jobs. Implement a **pre-submission consultation requirement** for any job requesting:
- More than 512 CPUs, or
- More than 72 hours walltime, or
- More than 2TB memory

This policy serves both efficiency (ensuring the job is correctly parallelized) and cluster health (preventing runaway jobs from degrading queue performance for weeks).

**Semester-Start Queue Management (Proactive)**

Based on the October and March wait-time spikes:
- Begin proactive outreach to top-100 job submitters two weeks before each semester starts, reminding them to pre-stage data, test with small jobs, and avoid submitting large batches on day 1.
- Consider a **reservation system** for instructional accounts that protects a small allocation of nodes for class use during week 1–3 of each semester.

**Multi-Core Job Encouragement**

The bimodal CPU request distribution (1 CPU or 48 CPUs, almost nothing in between) suggests an opportunity. Publish and promote documentation on using 4–16 core shared-memory parallelism (OpenMP, Python multiprocessing, R parallel packages) for workflows that would benefit. Even shifting 10% of the 1-CPU job mass to 4-CPU jobs would provide significant speedups for those users at minimal queue impact.

---

### 6.3 Infrastructure Recommendations

**GPU Hardware (Near-Term)**

GPU daily job counts roughly quadrupled from early 2025 to April 2026. Instructional users are requesting b200.180gb and h100.80gb GPUs alongside researchers, creating resource pressure on the highest-end nodes. For the next hardware procurement cycle:

- Prioritize **A100 80GB or H100 80GB nodes** (most requested for research)
- Evaluate **MIG (Multi-Instance GPU) partitioning** on existing A100 nodes to allow more concurrent instructional users without monopolizing full GPUs
- Consider **dedicated instructional GPU nodes** (lower-cost cards like RTX 4090 or A40) to offload class workloads from the research partition

**High-Memory CPU Nodes (COS-Driven)**

AOES averages 254 GB memory per CPU job; Chemistry averages 188 GB; GGS averages 227 GB; Bioengineering averages 151 GB. These are consistent with jobs that cannot be efficiently run on standard 192 GB/node configurations. Assess whether the current high-memory node pool is sufficient for growing COS demand.

**Scratch Storage / Parallel Filesystem**

With COS's large-memory jobs processing climate datasets and geospatial rasters, and CS/IST running many short jobs that produce small output files, I/O patterns are increasingly diverse. Review scratch filesystem throughput and evaluate whether a tiered storage arrangement (fast NVMe scratch for GPU/ML workloads, large-capacity Lustre for COS simulation outputs) is warranted.

**Open OnDemand Expansion**

- Add **GPU Jupyter environments** with pre-built ML containers (PyTorch, TensorFlow, JAX with CUDA)
- Add **VS Code Server OOD app** — increasingly expected by CS/IST users
- Add **interactive GPU session** option (1 GPU, 2 hrs max) for code debugging
- Enable **real-time queue monitoring widget** within OOD dashboard

---

### 6.4 Ticket System and Analytics

**Implement GPU ticket category** — immediately. Given that GPU-related issues (CUDA errors, driver mismatches, memory OOM, multi-GPU configuration) are now a significant portion of support requests, they must be trackable as a distinct category to measure trends and allocate support resources.

**Deploy NLP categorization pipeline** from the OS Ticket analysis project. With ~570 active daily users and a growing user base, ticket volume is too high for manual categorization to be sustainable. The ML categorization system should be operational before Fall 2026 semester start.

**Add automated responses for common GPU errors**: Out-of-memory errors, CUDA device mismatch errors, and expired module environments are high-frequency issues that could be partially resolved with an auto-responder pointing to the appropriate documentation.

---

## 7. Domain-Specific Recommendations

### 7.1 COS – Atmospheric, Ocean & Earth Sciences (AOES)

AOES is the largest COS department by job count (105,579 CPU jobs) and is emerging as a GPU user (3,654 GPU jobs, avg 133 GB GPU memory). This profile is consistent with climate modeling groups adopting ML emulators (e.g., FourCastNet, GraphCast, PanguWeather) alongside traditional numerical models (WRF, MOM6).

Recommended: Assign a COS liaison with competency in geoscience workflows; organize a joint workshop with AOES faculty on GPU-accelerated climate modeling.

### 7.2 COS – School of Systems Biology (SSB)

SSB had almost no jobs in 2025, but emerged with 2,864 GPU jobs in just 9 months of Fall 2025–Spring 2026 (62,569 GPU hours). This is likely driven by protein structure prediction (AlphaFold, ESMFold), genomic deep learning, or single-cell analysis. SSB's average GPU memory (27 GB) and moderate per-job GPU hours (21.85 hrs) suggest a workflow that fits well in the current cluster configuration.

Recommended: Proactive outreach to SSB PIs to assess pipeline needs; deploy a pre-configured AlphaFold/ESMFold container in OOD.

### 7.3 CEC – Mechanical Engineering (ME)

Despite only 474 CPU jobs, ME averages 458 CPU hours per job — the highest in the university. These are almost certainly large CFD or finite-element simulations (ANSYS Fluent, OpenFOAM, Abaqus). This department would benefit most from a job efficiency consultation to assess parallelization strategies.

### 7.4 CEC – Cybersecurity Engineering (CYSE)

CYSE averages 139 CPU hours and 221 GB memory per CPU job — very high for a relatively small job count (2,138 jobs). This suggests large-scale network simulation or adversarial ML workloads. The department is a candidate for targeted outreach if job volumes grow.

---

## 8. Semester Action Calendar (2026–2027)

### Summer 2026 (May – July)
- [ ] Investigate and document the February 2026 large-CPU-job event
- [ ] Post job opening or begin retraining for GPU Specialist role
- [ ] Build Fall 2026 class onboarding templates (IST, CS, AIT, ECE)
- [ ] Deploy NLP ticket categorization pipeline (initial version)
- [ ] Add GPU ticket category to OSTicket system
- [ ] Configure MIG partitioning on available A100 nodes for instructional use
- [ ] Publish multi-core job sizing guide (targeting 2–32 CPU jobs)
- [ ] Begin procurement planning for GPU node expansion

### Fall 2026 (August – December)
- [ ] Week -2 before semester: proactive email to top 100 GPU users (pre-staging reminder)
- [ ] Week 1: hold GPU power-user consultation workshop (2 hrs)
- [ ] Week 1: hold COS newcomer orientation (atmospheric/earth sciences focus)
- [ ] Deploy per-user GPU soft cap and instructional GPU quota policies
- [ ] Monitor October queue pressure; trigger proactive queue management if wait time exceeds 2 hrs avg for 3+ consecutive days
- [ ] Launch interactive GPU session OOD app
- [ ] COS liaison: quarterly meeting with AOES, SSB, CDS faculty

### Spring 2027 (January – April)
- [ ] Week -2: proactive outreach before spring surge (February/March)
- [ ] Deploy large-job consultation requirement policy
- [ ] Review GPU fair-share data from Fall 2026; adjust cap threshold if needed
- [ ] Deploy VS Code Server in OOD
- [ ] Retrospective analysis comparing AY 2026–2027 metrics to this baseline
- [ ] GPU hardware procurement decision point: if GPU wait time >2 hrs avg in >2 months → submit for next cycle

---

## 9. Key Performance Indicators (Tracking Dashboard)

| KPI | AY 2023–24 Baseline | AY 2025 Actual | AY 2026 Target |
|-----|---------------------|----------------|----------------|
| Total jobs/year | ~1.5–1.8M | 2.28M | 3.5M+ |
| GPU jobs % of total | ~3–5% | 5.4% | 8–10% |
| Avg daily unique users | ~300–400 | 570 | 700+ |
| Peak monthly avg wait time | — | 4.3 hrs (Oct 2025) | < 2.0 hrs |
| COS CPU jobs/year | ~100–200K est. | 342K | 1.2M |
| COS GPU jobs/year | ~0 | 2 | 15,000+ |
| Instructional GPU accounts/semester | ~5 | 20+ | 25+ |
| GPU tickets (tracked) | 0 | 0 (not categorized) | Categorized & trended |
| Large-job consultations/year | 0 (no policy) | 0 | 10–15 |
| OOD GPU job sessions/week | — | — | 200+ |

---

## 10. Summary of Changes vs. Original Plan

| Original Plan Item | Status | 2026 Update |
|-------------------|--------|-------------|
| Better ticket tagging | Not yet implemented | Now urgent — GPU category critical |
| NLP ticket categorization | In development | Deploy by Summer 2026; automate GPU errors |
| Open OnDemand promotion | Active, effective | Expand: GPU Jupyter, VS Code, interactive GPU |
| Outreach to heavy users | Informal | Formalize as GPU Power User Program with semi-annual consultations |
| Computational Specialist strategic tiering | CPU-focused | Add GPU Specialist, COS Liaison, IST/CS Instructional Coordinator |
| Large-job review | No policy | Implement consultation requirement (>512 CPUs, >72 hrs, >2TB) |
| Instructional onboarding | Ad hoc | Formalize: templates, OOD class environments, semester-start sessions |
| GPU fair-share policy | None | Implement soft cap + instructional GPU type restrictions |
| COS engagement | Low priority | Elevated to Tier 2 — COS GPU adoption now requires specialist support |
| IST/CS volume management | Not anticipated | IST is #1 submitter; IST+CS coordinator role needed |

---

*Data sources: Hopper Utilization Stats 2023–2024 (GMU ORC); Hopper Stats – 2025 Retrospective (Jan–Dec 2025, 41 pages); Hopper Stats – Fall 2025 – Spring 2026 (Aug 2025–Apr 2026, 51 pages); Quantifying HPC Utilization for Optimized Resource Deployment (GMU ORC); OS Ticket Analysis README (GMU ORC).*
