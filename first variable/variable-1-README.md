# Variable 1 — Cyberattack Frequency & Intensity (EuRepoC)

> **Status: Complete.** Measures whether cyberattack frequency has grown over 2015–2024, using
> the EuRepoC Global Dataset of Cyber Incidents, reported both raw and rule-adjusted.

## Research context

**Research question:** To what extent has the growth of cyberattacks and infrastructure
disruptions across industries outpaced the growth of institutional defensive and regulatory
capacity? (Study window ~2015–2025.)

This is one of four variables. Variables 1–3 measure the **pressure** side of the question
(how attack frequency, structural concentration, and cross-sector cascades have grown);
Variable 4 measures the **capacity** side qualitatively. This module answers the most direct
form of the pressure question: is the underlying rate of incidents rising, and does that hold
once a mid-study change in the dataset's own inclusion criteria is accounted for?

## What it shows

A cleaned time series of cyber incidents from the EuRepoC dataset over a 2015–2024 window.
The headline is an OLS trend on the rule-adjusted series, corroborated by a log-linear
specification for an annual growth rate. The analysis is reported both raw and rule-adjusted
because a February 2023 expansion of EuRepoC's inclusion criteria materially inflates 2023–2024
counts; the adjusted series is the defensible growth claim.

## Key findings

| Metric | Result | Note |
|--------|--------|------|
| OLS slope (rule-adjusted) | ≈ +32 incidents/year | Descriptive effect size |
| OLS significance | p ≈ 0.016 | Significant at 0.05 |
| R² | ≈ 0.53 | Moderate linear fit |
| Log-linear growth | ≈ 14% per year | Annual compounding rate |

## Methodology notes

- **Study window 2015–2024.** 2025 requires a separate provisional pull from EuRepoC's
  TableView that is not yet expert-reviewed, so it is excluded from the primary series.
- **February 2023 rule-change flag (stated limitation).** EuRepoC expanded its inclusion
  criteria in Feb 2023 to capture critical-infrastructure incidents regardless of initiator.
  Incidents qualifying *only* under this rule are flagged (`ci_only_post2023_rule`); ~24% of the
  windowed dataset carries the flag, concentrated in 2023–2024 (≈39% and 43% of those years).
  The raw series materially overstates 2023–2024 growth, so results are reported both raw and
  rule-adjusted as a sensitivity check.
- **Receiver-category deduplication.** EuRepoC repeats one row per affected country, so a single
  multi-country incident can dominate a year's sector totals — one 2022 espionage campaign
  (incident 2353) alone accounted for 54% of that year's raw critical-infrastructure tag count.
  Each incident is counted once per distinct category.
- **Dropped records.** 85 incidents with no usable date in either `start_date` or `end_date`
  are dropped rather than imputed.

## Data sources

| Source | Coverage | Type | License |
|--------|----------|------|---------|
| EuRepoC Global Dataset of Cyber Incidents v1.3.2 | 2015–2024 windowed | Primary | CC BY-NC 4.0 |

DOI [10.5281/zenodo.14965395](https://doi.org/10.5281/zenodo.14965395). The raw dataset is
redistributed here under CC BY-NC 4.0 (attribution, non-commercial). Any commercial fork must
remove the raw data and obtain it directly from EuRepoC.

## File structure

```
variable-1-cyberattacks/
├── data/
│   ├── raw/                        # Original EuRepoC CSV (unmodified)
│   └── processed/                  # Cleaned, flagged, aggregated outputs
├── scripts/
│   ├── clean_eurepoc.py            # Raw CSV -> cleaned / flagged / aggregated
│   └── build_visuals.py            # Processed CSVs -> static + interactive figures
├── figures/
│   ├── static/                     # 300dpi PNG + PDF (for the paper)
│   └── interactive/                # Standalone Chart.js HTML (for the website)
├── output/                         # Human-readable Excel summary workbook
├── requirements.txt
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
python scripts/clean_eurepoc.py    # clean + aggregate raw EuRepoC data -> data/processed/
python scripts/build_visuals.py    # static PNG/PDF -> figures/static/, HTML -> figures/interactive/
# interactive HTML — open directly in any browser, no server needed
```

Both scripts resolve paths relative to their own location, so they run from the repo root or
from inside `scripts/` with no path editing.

## Relation to other variables

| Variable | Phenomenon | Method | Side |
|----------|-----------|--------|------|
| **1 — Cyberattacks** | **Attack frequency & sector spread** | **OLS time series** | **Pressure** |
| 2 — Cloud concentration | Structural blast radius | HHI trend analysis | Pressure |
| 3 — Cross-sector cascade | Cascade breadth over time | Sector-spread heatmap | Pressure |
| 4 — Regulatory capacity | Institutional response speed/scope | Qualitative event study | Capacity |

---
*CompTIA Security+ · Python (pandas, matplotlib, statsmodels) · Chart.js*
