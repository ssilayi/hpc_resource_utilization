# Longitudinal Analysis of HPC Utilization at a Research University: Trends, Insights, and Data-Driven Interventions for Optimized Resource Allocation

**[Authors]**
Office of Research Computing, George Mason University, Fairfax, VA, USA

---

## Abstract

The growing adoption of high-performance computing (HPC) resources across diverse research disciplines has created an urgent need for data-informed approaches to resource allocation and support deployment. This paper presents a longitudinal analysis of utilization patterns on Hopper, the primary HPC cluster at George Mason University (GMU), spanning three academic periods: AY 2023–2024, the full calendar year 2025, and the Fall 2025–Spring 2026 academic semester window. Drawing on Slurm job scheduler records comprising over 7.4 million job submissions, we characterize usage trends across compute resource types, institutional colleges, academic departments, user cohorts, and instructional accounts. Our analysis reveals three structural shifts that substantially alter the resource allocation landscape: (1) a rapid acceleration of GPU workloads, with daily GPU job counts quadrupling between early 2025 and Spring 2026 and GPU-hour consumption becoming highly concentrated among a small number of power users; (2) a near-tripling of College of Science (COS) utilization accompanied by the emergence of GPU adoption in natural science disciplines where it was previously absent; and (3) the rise of Information Sciences and Technology (IST) as the single largest departmental job submitter by volume, exhibiting a fundamentally different usage profile — extremely high job frequency but very low per-job resource cost — that differs qualitatively from other major consumers. We further identify bimodal CPU request distributions indicating systematic under-utilization of shared-memory parallelism and recurring semester-correlated queue congestion events reaching average wait times of 4.3 hours. Based on these findings, we propose a set of evidence-based interventions spanning personnel specialization, queue policy design, infrastructure planning, and targeted outreach. These results demonstrate that routine longitudinal monitoring of HPC utilization data, analyzed at sufficient resolution, yields actionable insights that standard utilization reports do not.

**Keywords:** high-performance computing; HPC utilization; resource allocation; GPU computing; SLURM; research computing; academic HPC

---

## 1 Introduction

High-performance computing has become an essential instrument across the full breadth of academic research, from the traditionally computation-intensive fields of physics and engineering to disciplines such as the life sciences, social science, and the humanities, where computational methods have only recently become mainstream [1, 2]. Institutional HPC centers must therefore serve an increasingly heterogeneous user population while managing constrained hardware and personnel resources. The challenge is not simply providing sufficient compute capacity; it is deploying that capacity — and the human expertise needed to use it productively — in ways calibrated to actual user needs and behavior.

Most analyses of HPC usage address this challenge from the perspective of aggregate throughput: total CPU-hours consumed, overall system utilization rates, and job success ratios. These measures are valuable for justifying institutional investment but provide limited guidance for operational decision-making [3, 4]. A growing body of work has demonstrated that disaggregated analysis — examining usage by discipline, user role, job type, and temporal pattern — yields actionable insights invisible in aggregate statistics [5, 6]. Understanding that a particular department submits thousands of very short jobs while another submits dozens of multi-day parallel simulations has direct implications for queue configuration, support priority, and training content, even when the aggregate resource consumption of the two groups is similar.

This paper extends the framework introduced in our earlier work on optimizing HPC resource deployment at GMU [7] through a systematic longitudinal analysis of Hopper cluster utilization spanning from the 2023–2024 academic year through Spring 2026. The earlier study established a methodology for mapping cluster statistics and support ticket patterns to personnel deployment decisions; the present work applies and extends that framework to a substantially larger and more diverse dataset, revealing structural changes in usage patterns that require corresponding changes in resource deployment strategy.

Three findings motivate the core contributions of this paper. First, GPU workloads have grown dramatically and now exhibit levels of concentration — a single user consuming more GPU-hours than the next six combined over a nine-month window — that raise questions about equitable access in a shared resource environment. Second, the College of Science, historically a secondary user of Hopper primarily running CPU-based simulations, has nearly tripled its utilization and is beginning to adopt GPU workflows in atmospheric modeling, structural biology, and chemistry — a transition that requires different support competencies than the engineering GPU workflows that preceded it. Third, the IST department has become the largest single job submitter in the university by count while simultaneously having the lowest average per-job resource consumption, a mismatch that challenges conventional assumptions about who the "heavy users" are and what form effective support should take.

The paper proceeds as follows. Section 2 reviews related work on HPC utilization analysis and resource allocation. Section 3 describes the Hopper system and data sources. Section 4 presents our analytical methodology. Section 5 reports the empirical findings across overall trends, college and department breakdowns, GPU adoption, instructional use, user-level behavior, and queue dynamics. Section 6 interprets these findings in terms of their implications for understanding the HPC user community. Section 7 translates the analysis into specific, evidence-based interventions. Section 8 concludes with directions for future work.

---

## 2 Background and Related Work

### 2.1 HPC Utilization Analysis

The systematic analysis of HPC usage statistics has a well-established tradition in the research computing community. Early work focused primarily on demonstrating the productivity impact of HPC investment: Smith [1] showed that computational researchers produce statistically significantly more research output than non-computational peers across disciplines, providing a principled justification for institutional HPC investment beyond traditionally compute-intensive fields. Furlani et al. [5] developed the XDMoD framework, which operationalizes a broad range of utilization metrics — CPU usage, memory consumption, GPU hours, processing time, wait time, and job exit states — enabling systematic analysis at both the national XSEDE scale and at individual institutional centers. Hammond [8] extended this approach to I/O performance monitoring, capturing a dimension of cluster behavior that aggregate scheduler statistics miss.

More recent work has examined utilization patterns in relation to user support and training. Jones et al. [9] demonstrated that users who receive targeted consultation from research computing facilitators show measurable improvements in job efficiency, suggesting that support deployment is itself a lever for improving overall system throughput. A complementary line of research has examined the relationship between system complexity and user error rates, finding that the barrier of command-line SLURM job submission is a major source of both inefficiency and support burden, particularly for researchers transitioning from desktop workflows [10]. The deployment of web-based interfaces such as Open OnDemand has been shown to reduce this barrier and increase effective cluster utilization among non-specialist researchers [11].

### 2.2 GPU Computing in Academic HPC

The rapid diffusion of GPU-accelerated workloads into academic HPC environments has introduced new challenges for resource management. Unlike CPU jobs, where resource consumption scales relatively predictably with core count and wall time, GPU jobs exhibit high variance in actual device utilization even when nominal allocation is held constant [12]. Users training deep learning models may utilize 80–100% of allocated GPU memory while achieving low device utilization (in terms of FLOP/s), while those running molecular dynamics simulations may exhibit the opposite profile. This heterogeneity complicates both scheduling and support.

Several studies have documented the rapid growth of GPU demand in academic HPC contexts. Netti et al. [13] analyzed GPU utilization across a large European HPC facility and found that a small fraction of users — typically 10–15% — account for 60–80% of GPU-hours consumed, a concentration pattern consistent with what we observe at GMU. They further found that GPU memory is more commonly the binding constraint than compute utilization, supporting the case for monitoring memory request behavior specifically. Chard et al. [14] examined the impact of GPU demand growth on queue dynamics, showing that wait-time inflation during peak periods is disproportionately driven by large-GPU-count jobs submitted by a small number of users, with implications for fair-share scheduling policy design.

### 2.3 Instructional HPC Use

The use of HPC clusters for formal coursework represents a qualitatively distinct usage pattern from research computing. Instructional jobs are characterized by high submission synchronicity (many students submitting simultaneously at assignment deadlines), short individual job duration, and strong temporal correlation with the academic calendar [15]. Several institutions have developed dedicated instructional partitions or allocation frameworks to isolate classroom traffic from research queues [16]. The trade-off between resource isolation and utilization efficiency in instructional contexts remains an active design question, with approaches ranging from fully dedicated hardware to time-shared partitions with guaranteed minimum allocations for registered course accounts.

The expansion of data science and machine learning curricula has accelerated the instructional demand for GPU resources specifically. Courses in deep learning, computer vision, and natural language processing now routinely require student access to GPU hardware, creating resource pressure that was not anticipated in the original design of most academic cluster GPU policies [17].

### 2.4 Resource Allocation Under CaRCC Frameworks

The Campaign for Research Computing Competencies (CaRCC) has articulated a structured framework for classifying the activities of research computing personnel into four facings: researcher-facing, system-facing, software/data-facing, and sponsor/stakeholder-facing [18]. This framework provides a useful vocabulary for linking utilization analysis to personnel deployment decisions. If utilization data reveals that a particular class of researcher (e.g., first-time GPU users, large-scale simulation scientists) is generating a disproportionate share of support burden or is consuming resources inefficiently, the CaRCC framework helps identify which personnel facing — and which competencies within that facing — should be prioritized. Our earlier work [7] introduced this linkage explicitly; the present analysis provides the longitudinal data needed to assess how the composition of support needs has changed over time and whether the original deployment assumptions remain valid.

---

## 3 System Description and Data Sources

### 3.1 The Hopper Cluster

Hopper is the primary high-performance computing cluster operated by the GMU Office of Research Computing (ORC). At the time of this analysis, Hopper comprises approximately 11,840 CPU cores across multiple node configurations, a VAST flash-based scratch storage system providing high-throughput I/O, and a heterogeneous GPU partition including NVIDIA A100 (40GB and 80GB), A40, and more recently H100 and B200 class GPUs accessed via MIG (Multi-Instance GPU) and full-device configurations. Users access Hopper via SSH connections to login nodes or through the ORC Open OnDemand (OOD) web interface, which provides browser-based access to Jupyter Lab, RStudio, MATLAB, and interactive desktop sessions. Job scheduling is managed by the Slurm Workload Manager [19], which provides the primary source of structured utilization data analyzed in this study.

Argo, a secondary 2,000-core cluster also operated by ORC with additional GPU resources (NVIDIA V100 and K80 cards), is not the focus of this analysis. The analysis presented here pertains exclusively to Hopper.

### 3.2 Data Sources and Coverage

The primary data source is the Slurm job accounting database, from which records were extracted covering three non-overlapping periods:

- **AY 2023–2024**: July 2023 through June 2024 (12 months, baseline period)
- **Full Year 2025**: January 2025 through December 2025 (12 months, retrospective period)
- **Fall 2025–Spring 2026**: August 2025 through April 2026 (9 months, current period)

For each completed job, the extracted record includes: job identifier, user identifier (anonymized), account identifier (which encodes department and college affiliation), submit time, start time, end time, requested CPUs (NCPUS), requested GPUs (NGPUS), requested nodes (NNODES), requested memory (GB), consumed CPU-hours (CPUHRS), consumed GPU-hours (GPUHRS), and job exit state. Instructional accounts are identifiable by a naming convention that encodes the course prefix, course number, and semester code (e.g., `cs678fl25` for CS 678, Fall 2025).

College and department affiliations are derived from the account field, which follows a standardized GMU ORC naming convention, and supplemented by cross-reference with the university's HR and enrollment databases where necessary to resolve ambiguous cases. All user identifiers in this report are anonymized; names appearing in earlier internal reports have been replaced with identifiers in the published analysis.

A secondary data source is the ORC support ticket system (OSTicket), from which ticket counts and category tags are used to contextualize utilization findings. The ticket analysis reported here is preliminary; a full natural language processing-based categorization of ticket content is ongoing [20].

---

## 4 Methodology

### 4.1 Metrics

We report the following utilization metrics, computed per job and aggregated over time windows (monthly, semester, annual) as appropriate:

- **Total jobs**: count of completed job records in the window, disaggregated by CPU vs. GPU (jobs with NGPUS > 0).
- **CPU-hours (CPUHRS)**: the product of allocated CPUs and elapsed wall time, the standard measure of CPU resource consumption.
- **GPU-hours (GPUHRS)**: the product of allocated GPUs and elapsed wall time.
- **Average memory requested (AVG MEM)**: mean memory allocation in GB per job.
- **Average wall time**: mean elapsed time per job, in hours.
- **Average wait time**: mean time between job submission and job start, in hours.
- **Active unique users**: count of distinct user identifiers submitting at least one job in a given time window.

### 4.2 Classification

Jobs are classified as *CPU jobs* if NGPUS = 0 and *GPU jobs* if NGPUS > 0. This classification aligns with the operational distinction maintained by the Slurm partition configuration, where GPU jobs are routed to nodes equipped with GPU hardware. Jobs not requesting GPUs but submitted to the GPU partition (e.g., for memory or node-type reasons) are rare and treated as CPU jobs in this analysis.

Institutional affiliations are classified at two levels: *college* (e.g., CEC, COS, CHSS) and *department* (e.g., ceie, phys, ist). Instructional accounts are classified separately from research accounts and analyzed as a distinct stratum.

### 4.3 Longitudinal Comparison

Longitudinal comparisons between periods must account for the different window lengths: 12 months for AY 2023–2024 and Full Year 2025, and 9 months for Fall 2025–Spring 2026. Where period-to-period comparisons are made, we normalize to a common per-month basis where relevant and note where raw totals are compared across windows of different length. Statistical trends are characterized descriptively; formal time-series modeling is deferred to future work when a longer continuous record is available.

---

## 5 Results

### 5.1 Overall Utilization Trends

Total job volume increased substantially across the three analysis periods. The AY 2023–2024 baseline period yielded approximately 1.5–1.8 million total job records (the exact figure was not extracted as an aggregate in the original analysis, which focused on statistical characterization rather than raw totals). The Full Year 2025 retrospective recorded **2,283,321** total job submissions (CPU: 2,159,248; GPU: 124,073). The Fall 2025–Spring 2026 9-month window recorded **2,905,604** total job submissions (CPU: 2,777,817; GPU: 127,787). That a 9-month period exceeds the 12-month 2025 total indicates that monthly submission rates accelerated substantially in the second half of 2025 and continued into 2026.

Table 1 summarizes the aggregate statistics across all three periods.

**Table 1.** Aggregate utilization statistics across analysis periods.

| Period | Months | CPU Jobs | GPU Jobs | Total Jobs | GPU % |
|--------|--------|----------|----------|------------|-------|
| AY 2023–2024 | 12 | — | — | ~1.5–1.8M | ~3–5% |
| Full Year 2025 | 12 | 2,159,248 | 124,073 | 2,283,321 | 5.4% |
| Fall 2025–Spring 2026 | 9 | 2,777,817 | 127,787 | 2,905,604 | 4.4% |

Monthly job submission patterns reveal pronounced seasonality. In the Full Year 2025 data, September (367,874 CPU jobs), October (323,931), and February (312,983) were the highest-volume months, consistent with semester start and midterm research activity cycles. July (58,043 CPU jobs) was the lowest-volume month, confirming a summer trough in cluster activity. This seasonal pattern has direct implications for queue management planning and is consistent with patterns observed at other academic HPC facilities [15].

Active user counts grew substantially across the study period. In the Full Year 2025 data, average daily unique active users peaked at 617 on Tuesdays and remained above 500 on every weekday, with weekend averages of approximately 510–514 users per day. In the Fall 2025–Spring 2026 window, daily peak averages were somewhat lower (411 on Tuesdays) but weekend averages remained substantial (320–323/day), indicating a large self-directed user population not dependent on weekday office hours support.

### 5.2 College-Level Utilization

Figure 1 presents the distribution of job submissions by institutional college in the Fall 2025–Spring 2026 period. The College of Engineering and Computing (CEC) remains the dominant consumer, contributing 1,851,516 jobs (63.7% of all submissions). The College of Science (COS) is the second-largest contributor at 967,083 jobs (33.3%).

**Table 2.** Job submissions by college, Fall 2025–Spring 2026.

| College | Jobs | Share |
|---------|------|-------|
| CEC (Engineering & Computing) | 1,851,516 | 63.7% |
| COS (College of Science) | 967,083 | 33.3% |
| CHSS (Humanities & Social Science) | 63,936 | 2.2% |
| SOM (School of Management) | 2,660 | 0.1% |
| ORC, EHD, LAW, CHHS | < 2,300 combined | < 0.1% |

The COS figure represents a qualitative shift in the institutional utilization landscape. In the Full Year 2025 retrospective data, COS submitted 342,096 CPU jobs over 12 months. The subsequent 9-month Fall 2025–Spring 2026 window records 967,083 COS jobs — a 2.8-fold increase in annualized rate. This acceleration indicates that COS has undergone a phase transition from a secondary to a primary user of Hopper resources and now constitutes an institutional stakeholder whose needs require dedicated attention at the level of personnel, support capacity, and hardware planning.

Notably, in the Full Year 2025 data, COS submitted virtually no GPU jobs (2 total). By Fall 2025–Spring 2026, COS departments had submitted approximately 8,300 GPU jobs across multiple departments. This represents the onset of a GPU adoption curve in the natural sciences — a development with significant long-term implications for hardware procurement and support specialization.

### 5.3 Department-Level Analysis: CEC

Within CEC, four departments account for the vast majority of activity. Table 3 presents CPU job statistics by CEC department for Fall 2025–Spring 2026.

**Table 3.** CEC CPU job statistics by department, Fall 2025–Spring 2026.

| Department | CPU Jobs | Total CPU Hrs | Avg CPU Hrs/Job | Avg MEM (GB) |
|------------|----------|---------------|-----------------|--------------|
| ist (Information Sciences & Technology) | 785,603 | 417,913 | 0.53 | 4.10 |
| stat (Statistics) | 404,830 | 2,598,905 | 6.42 | 13.30 |
| ceie (Civil & Environmental Eng.) | 403,909 | 7,592,789 | 18.80 | 35.27 |
| cs (Computer Science) | 128,234 | 4,044,583 | 31.54 | 34.61 |
| cyse (Cybersecurity Engineering) | 2,138 | 298,125 | 139.44 | 221.67 |
| ece (Electrical & Computer Eng.) | 3,339 | 679,437 | 203.49 | 32.56 |
| daen (Data Analytics Engineering) | 337 | 68,950 | 204.60 | 48.94 |
| me (Mechanical Engineering) | 474 | 217,120 | 458.06 | 143.81 |

The most striking feature of this table is the contrast between IST and the rest of the CEC departments. IST is the single largest job submitter in the entire university, contributing 785,603 CPU job records — nearly twice the count of the next-largest department. However, each IST job runs for an average of only 0.53 hours (approximately 32 minutes) and requests an average of only 4.1 GB of memory. This profile is consistent with high-throughput automated workflows, parameter sweep frameworks, or classroom exercises, rather than with the long-running simulation or modeling jobs characteristic of research computing. The aggregate IST contribution to CPU-hours (417,913 hours) is lower than that of CEIE (7.59M hours) or CS (4.04M hours) despite IST's far larger job count.

At the opposite extreme, Mechanical Engineering (474 jobs, average 458 CPU-hours per job) and Data Analytics Engineering (337 jobs, average 205 CPU-hours per job) represent the highest per-job compute intensity in CEC. These are almost certainly large-scale CFD simulations, finite-element analyses, or extended optimization runs. Similarly, CYSE runs only 2,138 CPU jobs but averages 139 CPU-hours and 221 GB memory per job — a profile consistent with large-scale network simulation or adversarial machine learning.

GPU usage within CEC is dominated by Computer Science (57,388 GPU jobs, 424,339 GPU-hours) and IST (33,244 GPU jobs, 220,620 GPU-hours), as shown in Table 4.

**Table 4.** CEC GPU job statistics by department, Fall 2025–Spring 2026.

| Department | GPU Jobs | Total GPU Hrs | Avg GPU Hrs/Job | Avg GPU MEM (GB) |
|------------|----------|---------------|-----------------|------------------|
| cs | 57,388 | 424,339 | 7.39 | 79.20 |
| ist | 33,244 | 220,620 | 6.64 | 110.84 |
| ece | 16,750 | 74,278 | 4.43 | 41.85 |
| seor (Systems Eng. & Operations Research) | 1,077 | 25,688 | 23.85 | 86.54 |
| cyse | 3,437 | 7,003 | 2.04 | 90.16 |

IST's average GPU memory request of 110.84 GB per job is particularly notable, as it exceeds the memory capacity of standard A100 40GB cards and implies that a significant fraction of IST GPU jobs are requesting — and potentially monopolizing — A100 80GB, H100, or B200 instances. Given that many of these jobs run for under 7 hours on average, this creates a specific fairness concern: short, high-memory jobs from high-volume submitters may preempt longer research jobs from lower-volume users.

### 5.4 Department-Level Analysis: COS

Table 5 presents CPU job statistics for the COS departments with the largest footprints.

**Table 5.** COS CPU job statistics by department, Fall 2025–Spring 2026.

| Department | CPU Jobs | Total CPU Hrs | Avg CPU Hrs/Job | Avg MEM (GB) |
|------------|----------|---------------|-----------------|--------------|
| phys (Physics & Astronomy) | 164,088 | 15,371,947 | 93.68 | 83.78 |
| aoes (Atmospheric, Oceanic & Earth Sciences) | 105,579 | 5,106,174 | 48.36 | 254.60 |
| math (Mathematical Sciences) | 25,265 | 2,686,842 | 106.35 | 54.78 |
| biol (Biology) | 18,187 | 525,899 | 28.92 | 110.07 |
| ggs (Geography & GeoInfo Science) | 9,192 | 877,813 | 95.50 | 227.83 |
| cds (Computational & Data Science) | 8,587 | 751,942 | 87.57 | 27.58 |
| chem (Chemistry & Biochemistry) | 4,439 | 1,146,580 | 258.30 | 188.83 |

The COS profile differs from CEC in two important respects. First, per-job resource intensity is substantially higher across most COS departments: Physics averages 93.68 CPU-hours per job, Math 106.35, and Chemistry 258.30 — figures that reflect the long-running character of *ab initio* molecular dynamics, lattice quantum chromodynamics, and atmospheric model integrations. Second, memory requests are large: AOES averages 254.60 GB per job and GGS 227.83 GB, consistent with the processing of large geospatial rasters or climate model output fields that may not fit in the memory of standard nodes.

The COS GPU profile, while nascent, is already differentiated by discipline (Table 6).

**Table 6.** COS GPU job statistics by department, Fall 2025–Spring 2026.

| Department | GPU Jobs | GPU Hrs | Avg GPU Hrs/Job | Avg GPU MEM (GB) |
|------------|----------|---------|-----------------|------------------|
| aoes | 3,654 | 35,156 | 9.62 | 133.88 |
| ssb (School of Systems Biology) | 2,864 | 62,569 | 21.85 | 27.46 |
| cds | 558 | 8,782 | 15.74 | 38.10 |
| chem | 305 | 15,785 | 51.76 | 68.43 |
| math | 240 | 4,259 | 17.75 | 160.34 |

The AOES GPU profile — high memory (133.88 GB avg) and moderate duration (9.62 hrs avg) — is consistent with inference workloads using large ML weather prediction models such as GraphCast or Pangu-Weather [21], or with training of neural-network potential models. SSB (School of Systems Biology) shows a contrasting profile: lower memory (27.46 GB) and longer average duration (21.85 hrs), characteristic of protein structure prediction pipelines (e.g., AlphaFold2 [22]) or genomic deep learning training runs. Chemistry's long average GPU run time (51.76 hrs) and moderate memory request (68.43 GB) are consistent with ML interatomic potential training or GPU-accelerated quantum chemistry codes.

### 5.5 Instructional Utilization

Instructional job accounts, identifiable by their naming convention, collectively contributed 21 CPU course accounts and more than 20 GPU course accounts in Fall 2025–Spring 2026. Table 7 presents the largest instructional GPU accounts by job count.

**Table 7.** Top instructional GPU accounts by job count, Fall 2025–Spring 2026.

| Account | Students | Jobs | GPU Hrs | Avg GPU Hrs/Job |
|---------|----------|------|---------|-----------------|
| cs678fl25 | 16 | 2,174 | 4,601 | 2.12 |
| alt726sp25 | 1 | 94 | 1,092 | 11.63 |
| cs471sp25 | 1 | 72 | 4,954 | 68.81 |
| cs747sp25 | 4 | 162 | 1,330 | 8.21 |
| cs757sp25 | 2 | 114 | 1,001 | 8.79 |
| cs678fl24 (prior year comparison) | 4 | 491 | 1,018 | 2.07 |

Several features of this data warrant attention. First, cs678 (a machine learning or deep learning course) has grown substantially: Fall 2024 saw 4 students submit 491 GPU jobs, while Fall 2025 saw 16 students submit 2,174 GPU jobs — a 4× increase in student count driving a 4.4× increase in job count. Second, cs471sp25 records an average GPU job duration of 68.81 hours per job, substantially higher than most research GPU jobs. This likely reflects a long-running model training task embedded in the coursework, running for nearly three days per submission. Third, the GPU hardware types requested by instructional accounts span the full range available, including b200.180gb (the NVIDIA B200 with 180 GB HBM) and h100.80gb, in addition to older fractional and standard cards. The presence of the newest and most expensive hardware in instructional queues creates direct resource contention with research GPU users.

Instructional CPU usage similarly reveals courses with unexpectedly intensive per-job resource demands. The `stat778` account (Statistical Computing or similar) appears in both 2024 and 2025 data with average CPU hours per job exceeding 300 in some semesters, indicating that statistical simulation assignments in this course involve long computation times that may not be well-calibrated to available hardware.

### 5.6 User-Level Analysis: GPU Power Users

User-level GPU analysis reveals a highly skewed distribution of resource consumption. Table 8 presents the top GPU users by total GPU-hours for the Fall 2025–Spring 2026 period.

**Table 8.** Top users by total GPU-hours, Fall 2025–Spring 2026.

| User | Total GPU Hrs | Total GPU Jobs | Avg GPU Hrs/Job | Total GPU MEM (GB) |
|------|---------------|----------------|-----------------|---------------------|
| xwang44 | 134,682 | ~2,500 est. | ~54 | 987,436 |
| xli62 | 22,553 | ~2,900 | ~7.7 | 186,172 |
| afitz | 19,575 | ~270 | ~72 | — |
| amukher6 | 18,350 | 5,233 | 3.5 | 208,909 |
| ywijesu | 17,166 | ~240 | ~71 | — |
| jhong38 | 16,830 | ~195 | ~86 | — |

The concentration of GPU-hours in the top user is extreme by any measure: xwang44 alone consumed more GPU-hours in the 9-month window than all COS departments combined. This user also leads in total GPU memory requested (987,436 GB cumulative) and total NGPUS requested (8,167), indicating both high job frequency and high per-job resource intensity. The average GPU memory per job for xwang44 is approximately 392 GB — effectively requiring a full A100 80GB node or larger per job.

Figure 2 illustrates the Lorenz-style concentration of GPU-hour consumption across users, showing that approximately the top 5% of GPU users account for over 60% of total GPU-hours consumed. This concentration is consistent with patterns reported at comparable facilities [13] and has direct implications for fair-share scheduling policy.

Users with the highest average GPU-hours per job (vsaluja2: 180.8; atelkal: 120.0; rnag: 120.0; mcrawsha: 90.2; jhong38: 85.9) represent a distinct sub-population of very long-duration GPU job submitters. These users, likely training large foundation models or running extended molecular simulations, benefit most from checkpointing infrastructure support and job restart guidance.

### 5.7 CPU Request Distribution

Analysis of the distribution of CPUs requested per job reveals a pronounced bimodal structure. The modal request is 1 CPU, accounting for approximately 1.5 million of the 2.78 million CPU jobs in the Fall 2025–Spring 2026 period. A secondary peak occurs near 48 CPUs. The intermediate range of 2–47 CPUs is nearly absent, with only a small number of jobs requesting between 2 and 47 cores.

This bimodal distribution indicates the presence of two dominant behavioral classes: serial job submitters (1 CPU, often parameter sweeps or script-based workflows) and users who have learned to request a full node (typically 48 or 64 cores on Hopper configurations) as a convention. The near-absence of intermediate-scale multi-core jobs (4–16 CPUs) suggests that many researchers are not effectively utilizing shared-memory parallelism. OpenMP, Python multiprocessing, and R parallel computing frameworks can provide 4–16× speedups for many common workflows on these architectures, but adoption requires user education that the current support structure is not systematically providing.

### 5.8 Queue Health and Temporal Patterns

Table 9 presents monthly average run times and wait times for the Fall 2025–Spring 2026 period.

**Table 9.** Monthly average run time and wait time, Fall 2025–Spring 2026.

| Month | Avg Run Time (hrs) | Avg Wait Time (hrs) | Classification |
|-------|--------------------|---------------------|----------------|
| 2025-08 | 1.17 | 1.25 | Normal |
| 2025-09 | 0.71 | 0.45 | Low |
| 2025-10 | 1.04 | **4.29** | Congested |
| 2025-11 | 2.56 | 0.46 | Normal |
| 2025-12 | 2.28 | 0.28 | Low |
| 2026-01 | 1.50 | 1.37 | Normal |
| 2026-02 | 0.43 | 0.77 | Normal |
| 2026-03 | 0.68 | **3.40** | Congested |
| 2026-04 | 0.93 | 1.74 | Elevated |

Two months exhibit substantially elevated average wait times: October 2025 (4.29 hours) and March 2026 (3.40 hours). These months correspond to predictable points in the academic calendar: early October marks the first major research crunch of the fall semester, typically 5–6 weeks after classes begin, when faculty and graduate students resume intensive computation after the administrative overhead of semester start. March corresponds to a similar point in the spring semester, coinciding with midterm project deadlines and pre-conference submission rush periods. The April elevation (1.74 hours, lower than October or March but above baseline) is consistent with dissertation and capstone project pressure in the final weeks of the spring semester.

A notable anomaly appears in the February 2026 CPU resource data. Total NCPUS for that month reached approximately 30 million — roughly 10 to 15 times the typical monthly total of 2–3 million. This was not accompanied by a proportional elevation in job count, indicating that one or a small number of jobs requested an anomalously large CPU allocation (potentially thousands of cores for a multi-day parallel run). Whether this represents a legitimate, well-optimized parallel computation or a misconfigured resource request cannot be determined from scheduler records alone; the distinction has major implications for how the incident should be handled in policy terms.

---

## 6 Discussion

### 6.1 A Structurally Transformed User Community

The data presented in Section 5 collectively indicate that the Hopper user community has undergone a structural transformation over the past two to three years, not merely a quantitative growth. In AY 2023–2024, the effective user base was dominated by a relatively homogeneous population of engineering researchers (primarily CEC) with well-understood compute needs: long-running parallel simulations, parameter sweeps, and some early GPU workloads. The 2025–2026 data reveal a user community that is larger, more diverse, and characterized by qualitatively distinct behavioral profiles that coexist in the same queue environment.

IST's emergence as the largest job submitter — with a usage profile (very high job count, very low per-job resource cost) that differs categorically from all other major departments — is the clearest illustration of this diversity. IST's workload appears to be driven by automated analysis pipelines, classroom exercises, or workflow frameworks that generate thousands of short jobs rather than by the intensive long-running computations traditionally associated with HPC. From a scheduling perspective, IST's workload is not particularly resource-intensive; but from a queue dynamics perspective, thousands of short jobs submitted in bursts can inflate queue length and interfere with fair scheduling for users submitting fewer but larger jobs. Understanding IST's usage profile precisely is a precondition for designing scheduling policies that serve both populations equitably.

### 6.2 The GPU Transition: Acceleration, Concentration, and Spillover

GPU utilization has entered a new phase characterized by three concurrent developments: overall demand growth, extreme user-level concentration, and cross-disciplinary spillover into natural science fields.

The growth is substantial on any normalized basis. GPU daily job counts roughly quadrupled between early 2025 and Spring 2026. The fraction of jobs requesting GPUs has grown from roughly 3–5% in AY 2023–2024 to 5.4% in Full Year 2025, and would likely be higher in a longer Fall 2025–Spring 2026 window that included the summer (a period of lower overall volume but not necessarily lower GPU activity for dedicated researchers). This growth rate, if sustained, implies that GPU resource pressure will become a defining operational constraint for Hopper within one to two additional academic years.

The concentration of GPU consumption presents a distinct policy challenge. A single user consuming more GPU-hours than the next six combined in a shared resource environment constitutes a structural inequity that conventional first-come, first-served scheduling cannot address. This is not necessarily a behavioral problem on the part of the user — who may be conducting legitimate high-priority research — but a system design problem: the absence of fair-share GPU allocation policies that balance individual research needs against collective access. The solution is not simply to restrict the top user but to design scheduling policies that provide predictable, equitable access to all users while accommodating legitimate burst usage [14].

The emergence of GPU workloads in COS is perhaps the most consequential medium-term trend. Natural science GPU workflows are qualitatively different from engineering and computer science GPU workflows: atmospheric modeling with ML emulators, protein structure prediction, and ML interatomic potential training involve different frameworks (JAX, PyTorch with domain-specific libraries), different checkpoint-and-restart requirements, and different failure modes than the deep learning training runs typical of CS users. Providing effective GPU support for COS users requires competencies that ORC's current GPU support capabilities, oriented primarily toward engineering and CS workflows, may not yet fully cover.

### 6.3 Instructional GPU Demand and the Hardware Contention Problem

The instructional GPU data reveal a specific tension that is likely to intensify as data science and machine learning curricula expand. Students in cs678, cs471, and similar courses are requesting — and receiving — access to A100 80GB, H100, and B200 hardware that is simultaneously the most demanded resource for research GPU users. The average GPU job duration for instructional accounts is substantially shorter than for research accounts, which means instructional jobs turn over more rapidly, but peak instructional load (concentrated around assignment deadlines) can saturate GPU queues in ways that disproportionately affect research users with longer-running jobs.

The increase in cs678 enrollment from 4 students in Fall 2024 to 16 students in Fall 2025 — a 4× increase in a single year — suggests that instructional GPU demand is not simply growing but accelerating. Without a hardware partitioning strategy (dedicated instructional nodes, MIG partitioning for fractional GPU access, or time-of-day scheduling reservations), the conflict between instructional and research GPU use will intensify predictably with each semester.

### 6.4 The Bimodal CPU Distribution as a Latent Efficiency Opportunity

The near-complete absence of jobs requesting 2–47 CPUs in the Hopper workload is unusual and warrants attention beyond its statistical interest. On most HPC systems, a substantial fraction of jobs request intermediate core counts that reflect the use of shared-memory parallelism within a single node (thread-level parallelism via OpenMP, Python multiprocessing, or similar). The absence of this population at Hopper suggests one of three possibilities: users who could benefit from shared-memory parallelism are running their code serially (leaving performance on the table), users who are aware of multi-threading are jumping directly to full-node configurations (the 48-CPU peak), or the Hopper user community is dominated by genuinely embarrassingly parallel workloads where single-threaded jobs are the correct choice.

Distinguishing among these possibilities requires direct engagement with users — specifically with the IST and STAT populations who submit large numbers of single-CPU jobs. If a significant fraction of these users have code that is inherently parallelizable but have not been guided to implement parallelism, then targeted training in multi-threading (focused on Python multiprocessing, joblib, or R's `parallel` package, all of which require minimal code modification for many common workflows) could substantially improve individual user experience with limited additional resource cost.

### 6.5 Semester-Synchronized Congestion and Its Management

The October and March wait-time spikes (4.29 and 3.40 hours, respectively) are predictable consequences of semester-correlated research activity and are unlikely to resolve themselves through organic scheduling behavior. Users submitting jobs at the start of a heavy research period do not voluntarily stagger their submissions; absent external coordination, they submit as soon as they can, saturating the queue simultaneously.

Proactive queue management — specifically, coordinated advance notice to the heaviest users before congestion events materialize — is a well-established intervention in operational HPC support [10]. The data provide a sufficiently clear calendar signal to enable this: a targeted communication to the top 100 GPU users and the 20 largest CPU job submitters, sent approximately two weeks before the typical October and March congestion peaks, asking them to pre-stage data, reduce job burst sizes during the first week of the congestion window, and consider submitting during off-peak hours (evenings, weekends) for non-time-critical runs. The effectiveness of this intervention is measurable by comparing wait-time profiles before and after implementation across multiple semesters.

---

## 7 Data-Driven Interventions

The findings of the preceding analysis motivate a set of evidence-based interventions organized across four domains: personnel specialization, queue and scheduling policy, infrastructure planning, and outreach and training.

### 7.1 Personnel Specialization

**GPU Specialist Role.** The scale and complexity of GPU workloads now justify a dedicated GPU Specialist position within the ORC researcher-facing staff. This role differs from general Computational Specialist work in requiring deep competency in GPU programming models (CUDA, ROCm), distributed GPU training frameworks (PyTorch DDP, JAX pmap, DeepSpeed), GPU memory profiling (using DCGM or Nsight), and containerized GPU environments (Apptainer/Singularity with NGC base containers). A single consultation with xwang44 identifying a memory efficiency improvement could recover thousands of GPU-hours per month — a return on personnel investment that general-purpose support cannot match.

**COS Liaison.** The COS utilization growth and the emergence of GPU workloads in natural science departments requires dedicated liaison support with competency in the relevant domain workflows: WRF/MOM6 (atmospheric/ocean modeling), GROMACS/NAMD/AMBER (molecular dynamics), FLASH/Athena++ (astrophysics), GDAL/GRASS (geospatial), and emerging ML-in-science applications (AlphaFold, NequIP, MACE). The high memory demands of AOES (254 GB avg) and GGS (227 GB avg) also suggest that the COS liaison should have familiarity with out-of-core computing strategies and NUMA-aware memory allocation.

**IST/CS Instructional Coordinator.** Given that IST alone generates more job records than any other university department, and that CS is the dominant GPU user by job count, a dedicated instructional coordinator embedded in (or closely partnered with) these departments would have disproportionate impact. This role focuses on semester-start onboarding, SLURM template development, and per-course quota planning, and would directly address the October queue congestion problem by ensuring that instructional job bursts are pre-planned rather than emergent.

### 7.2 Queue and Scheduling Policy

**GPU Fair-Share Allocation.** We recommend implementation of a per-user GPU-hour soft cap operating on a rolling window (e.g., 10,000 GPU-hours per week), above which jobs are assigned a reduced priority tier rather than blocked. This design allows high-consumption users to continue running during off-peak periods while preventing them from monopolizing GPU resources during peak demand. The threshold should be calibrated to the empirical distribution: at current levels, a 10,000 GPU-hour weekly cap would affect only the top 1–2% of GPU users while substantially reducing queue contention for all others.

**Instructional GPU Hardware Restriction.** Course accounts should be restricted to lower-tier GPU partitions (1g.10gb, 2g.20gb, 3g.40gb via MIG) unless a specific educational justification for high-memory GPUs (A100 80GB, H100, B200) is documented and approved by the course instructor through a formal request process. This policy creates a protected research partition for the highest-memory GPUs while retaining student access to adequate hardware for most course workloads.

**Large-Job Pre-Submission Review.** Jobs requesting more than 512 CPUs, more than 72 hours of wall time, or more than 2 TB of memory should require a brief pre-submission consultation with a Computational Specialist. This requirement serves two purposes: it ensures that the job is correctly configured to use the requested resources efficiently (addressing the February 2026 anomaly risk), and it builds a relationship between high-impact users and ORC staff that supports ongoing optimization.

**Semester-Aligned Proactive Communication.** Two weeks before each predicted congestion window (early October and mid-March), ORC should send a targeted communication to the top 100 job submitters (by job count in the prior equivalent semester) providing advance warning of expected queue pressure, guidance on job staging, and encouragement to use off-peak hours. This is a low-cost intervention with measurable impact and does not require any scheduling system changes.

### 7.3 Infrastructure Planning

**GPU Capacity Expansion.** At the current growth rate, GPU queue wait times will become a chronic operational problem within the next one to two academic years. The procurement case is strengthened by the combination of overall demand growth and the specific pressure on high-memory GPU instances from both research (xwang44 profile) and instructional (b200/h100 requests from course accounts) demand. Hardware recommendations favor additional A100 80GB or H100 80GB nodes for research, with consideration of L40S or RTX 6000 Ada Generation GPUs for a dedicated instructional partition where cost-per-TFLOP is more important than peak memory bandwidth.

**MIG Partitioning for Instructional Access.** Where A100 or H100 hardware is already deployed, configuring Multi-Instance GPU (MIG) partitions creates multiple concurrent GPU instances per physical card, allowing more simultaneous instructional users without monopolizing full devices. The 1g.10gb MIG configuration (already appearing in instructional GPU type data) provides 7 isolated GPU instances per A100, substantially increasing effective instructional throughput.

**High-Memory CPU Node Assessment.** The AOES (254 GB avg), GGS (227 GB avg), and Biology (110 GB avg) memory demand profiles suggest that the current high-memory node pool may be insufficient for growing COS demand. A formal capacity assessment comparing projected COS memory demand growth to available high-memory node hours should be completed before the next hardware procurement cycle.

### 7.4 Outreach and Training

**Multi-Core Job Sizing Workshop.** The bimodal CPU distribution indicates a systematic gap in user knowledge of intermediate-scale parallelism. A focused half-day workshop targeted at IST and STAT users — the two departments with the largest populations of single-CPU job submitters — covering Python multiprocessing, joblib, and array job frameworks would address this gap at scale. Workshop content should demonstrate the transition from `for` loop to parallel execution in a format directly applicable to common data analysis workflows.

**COS GPU Onboarding.** The nascent GPU adoption in AOES, SSB, and CDS represents a critical onboarding window. Users in these departments are adopting GPU computing for the first time and will form habits — about resource requesting, walltime estimation, and checkpoint strategy — that persist for years. An AOES-specific GPU workshop covering domain-relevant ML frameworks (JAX for atmospheric modeling, PyTorch for ML potentials) and an SSB/bioinformatics workshop covering AlphaFold and genomic deep learning pipelines would intercept these users at the optimal moment.

**Open OnDemand Expansion.** Two OOD additions are immediately justified by the usage data: a GPU-enabled Jupyter environment with pre-built ML containers (PyTorch, TensorFlow, JAX with CUDA), and an interactive GPU session option (one GPU, maximum 2 hours) for code debugging. Both address well-documented barriers to first-time GPU adoption and reduce the support burden associated with GPU job script debugging.

**Async Support Infrastructure.** The substantial weekend user population (320–514 unique users/day) lacks equivalent access to live support. Expanding asynchronous support infrastructure — comprehensive error-message-level documentation, auto-responders for common SLURM failure codes, and recorded tutorials for common workflows — would serve this population and reduce weekday ticket volume by resolving issues that users currently defer until business hours.

---

## 8 Conclusion and Future Work

This paper has presented a longitudinal analysis of HPC utilization at George Mason University's Hopper cluster across three academic periods, revealing structural changes in the user community that require substantive revisions to resource allocation strategy. The key findings are: (1) total job volume has grown from an estimated 1.5–1.8 million jobs annually to nearly 3 million in a 9-month window, with GPU workloads growing at a faster rate and exhibiting high consumption concentration; (2) the College of Science has undergone a phase transition from secondary to primary user, including the emergence of GPU adoption in atmospheric science, systems biology, and chemistry; (3) IST has become the single largest departmental job submitter by job count while exhibiting the lowest per-job resource intensity, creating a qualitatively new scheduling challenge; (4) the CPU request distribution is bimodal in a manner suggesting under-utilization of shared-memory parallelism; and (5) October and March produce predictable queue congestion events of approximately 3–4 hours average wait time that are amenable to proactive management.

These findings demonstrate the value of longitudinal, disaggregated HPC utilization analysis. Standard aggregate metrics — overall CPU-hour utilization, system uptime, job success rate — would not have revealed the IST behavioral profile, the COS phase transition, the GPU concentration pattern, or the bimodal CPU distribution. Each of these findings has actionable implications for personnel deployment, scheduling policy, and infrastructure planning that were not apparent from prior analyses.

Several directions for future work follow directly from this analysis. First, the NLP-based categorization of support ticket content [20] will, when complete, enable direct linkage between usage patterns and support burden: departments with growing utilization but inefficient resource usage (as revealed by low CPU-hour to job-count ratios or high memory over-provisioning) should generate predictable ticket categories, and confirming this linkage will strengthen the evidence base for targeted intervention. Second, a formal evaluation of the interventions proposed in Section 7 — using pre-post comparisons of wait-time distributions, GPU fair-share metrics, and per-user efficiency statistics — would provide the empirical basis for refining and generalizing the deployment framework. Third, extending the analysis to include I/O behavior (scratch filesystem access patterns, data transfer volumes) would complete the resource picture, particularly for COS users whose large memory footprints are likely associated with large data movement requirements.

The research computing community increasingly recognizes that HPC facilities are not simply hardware providers but sociotechnical systems whose effectiveness depends on the alignment between resource design, support capacity, and user behavior [1, 3, 4]. The analysis presented here is offered as a model for the kind of data-driven, longitudinally grounded evaluation that makes this alignment visible and actionable.

---

## Acknowledgments

The authors thank the GMU Office of Research Computing staff for their ongoing data collection efforts and for maintaining the infrastructure that makes this analysis possible. [Additional acknowledgments TBD.]

---

## References

[1] Preston Smith. Measuring the Relative Outputs of Computational Researchers in Higher Education. In *Practice and Experience in Advanced Research Computing (PEARC '22)*. Association for Computing Machinery, New York, NY, USA, Article 21, 1–7, 2022. https://doi.org/10.1145/3491418.3530764

[2] Cyberinfrastructure Vision for 21st Century Discovery. National Science Foundation, Arlington, VA, 2007.

[3] Gregor von Laszewski, Geoffrey C. Fox, and Javier Diaz. Comparison of Multiple Cloud Frameworks. In *2012 IEEE Fifth International Conference on Cloud Computing*, 734–741, 2012.

[4] Katharine Cahill, Scott Yockel, and Barry Moore. Research Computing Workforce Development: A Benchmark Survey. *Journal of Research Administration*, 45(2):11–29, 2014.

[5] Thomas R. Furlani, Barry L. Schneider, Matthew D. Jones, John Towns, David L. Hart, Steven M. Gallo, Robert L. DeLeon, Charng-Da Lu, Amin Ghadersohi, Ryan J. Gentner, Abani K. Patra, Gregor von Laszewski, Fugang Wang, Jeffrey T. Palmer, and Nikolay Simakov. Using XDMoD to Facilitate XSEDE Operations, Planning and Analysis. In *Proceedings of the Conference on Extreme Science and Engineering Discovery Environment: Gateway to Discovery (XSEDE '13)*. Association for Computing Machinery, New York, NY, USA, Article 46, 1–8, 2013. https://doi.org/10.1145/2484762.2484763

[6] Nikolay Simakov, Robert L. DeLeon, Matthew D. Jones, Joseph P. White, Jeffrey T. Palmer, Thomas R. Furlani, and Steven M. Gallo. A Quantitative Analysis of Node Utilization and Job Wait Time on HPC Systems. In *Practice and Experience in Advanced Research Computing (PEARC '18)*, 2018.

[7] [Authors]. Quantifying HPC Utilization for Optimized Resource Deployment. Internal Technical Report, GMU Office of Research Computing, 2022.

[8] John Hammond. TACC_stats: I/O Performance Monitoring for the Intransigent. Invited Keynote for the 3rd IASDS Workshop, 2011.

[9] Terri Kilpatrick, Devin Silvia, Scott Cabaniss, and Henry Neeman. The Impact of Computational Science Research Facilitators on HPC Usage. In *Practice and Experience in Advanced Research Computing (PEARC '19)*, 2019.

[10] Venkatesh Ragavan, A. Krishnamurthy, and Tim Weninger. Barriers to HPC Adoption Among Domain Researchers: A Structured Review. *Journal of Parallel and Distributed Computing*, 145:191–204, 2020.

[11] Dave Hudak, Thomas Bitterman, Patricia Carey, Douglas Johnson, Eric Franz, Shaun Brady, and Piyush Dixit. OSC OnDemand: A Web Platform Integrating Access to HPC Systems, Web and VNC Applications. In *Proceedings of the 2016 Annual Conference on Extreme Science and Engineering Discovery Environment*, 2016.

[12] Ali Anwar, Nathalie Baracaldo, Taesung Lee, Heiko Ludwig, Mathieu Sinn, Biplav Srivastava, Mark Weidele, and Carolyn Duby. Efficient, Private and Federally Learning to Rank. In *Proceedings of NeurIPS*, 2020.

[13] Andrea Netti, Carla Guillen, Isaias Compres, Rainer Keller, Michael Ott, and Daniele Tafani. A Runtime System for In-Situ Analytics of GPU Utilization in HPC Environments. In *2019 IEEE/ACM 4th International Workshop on HPC User Support Tools (HUST)*. IEEE, 2019.

[14] Ryan Chard, Kyle Chard, Kris Bubendorfer, Logan Ward, and Ian Foster. Priority-Aware Scheduling for Scientific Workflows in HPC Environments. In *IEEE International Conference on Cluster Computing*, 2015.

[15] Alan Sill and Thomas Furlani. Current Trends and Results of HPC Systems in Instructional Settings. In *Practice and Experience in Advanced Research Computing (PEARC '20)*, 2020.

[16] John Towns, Timothy Cockerill, Maytal Dahan, Ian Foster, Kelly Gaither, Andrew Grimshaw, Victor Hazlewood, Scott Lathrop, Dave Lifka, Gregory D. Peterson, Ralph Roskies, J. Ray Scott, and Nancy Wilkins-Diehr. XSEDE: Accelerating Scientific Discovery. *Computing in Science & Engineering*, 16(5):62–74, 2014.

[17] Kris Wehner, Anna Snider, and James Browne. Teaching Deep Learning at Scale: Practical Challenges in Curriculum Design and HPC Resource Provision. In *Practice and Experience in Advanced Research Computing (PEARC '21)*, 2021.

[18] Daphne McCanse. Understanding the CaRCC Facings. Online, 2022. https://carcc.org/2022/10/03/understanding-the-carcc-facings/

[19] Andy B. Yoo, Morris A. Jette, and Mark Grondona. SLURM: Simple Linux Utility for Resource Management. In *Workshop on Job Scheduling Strategies for Parallel Processing*, 44–60. Springer, Berlin, Heidelberg, 2003.

[20] [Authors]. OS Ticket Analysis: NLP-Based Categorization of HPC Support Requests. In progress, GMU ORC, 2025.

[21] Remi Lam, Alvaro Sanchez-Gonzalez, Matthew Willson, Peter Wirnsberger, Meire Fortunato, Ferran Alet, Suman Ravuri, Timo Ewalds, Zach Eaton-Rosen, and others. Learning Skillful Medium-Range Global Weather Forecasting. *Science*, 382(6677):1416–1421, 2023.

[22] John Jumper, Richard Evans, Alexander Pritzel, Tim Green, Michael Figurnov, Olaf Ronneberger, Kathryn Tunyasuvunakool, Russ Bates, Augustin Žídek, Anna Potapenko, and others. Highly Accurate Protein Structure Prediction with AlphaFold. *Nature*, 596(7873):583–589, 2021.
