# Variable 2 — Cloud Market Concentration (HHI / CR3)

> **Status: Complete.** Measures the *structural blast radius* of a single cloud-provider
> failure, using the Herfindahl-Hirschman Index (HHI) of cloud infrastructure market share as
> a proxy for systemic concentration.

## Research context

**Research question:** To what extent has the growth of cyberattacks and infrastructure
disruptions across industries outpaced the growth of institutional defensive and regulatory
capacity? (Study window ~2015–2025.)

This is one of four variables. Variables 1–3 measure the **pressure** side of the question
(how attack frequency, structural concentration, and cross-sector cascades have grown);
Variable 4 measures the **capacity** side qualitatively. This module operationalises the
*efficiency–fragility tradeoff*: as fewer providers absorb more of the world's digital
workload, the blast radius of any single failure — malicious or not — grows proportionally.

## What it shows

Rather than counting non-malicious outages directly (Uptime Institute's incident-level data is
paywalled), this module measures the structural precondition for large outages: market
concentration. HHI is computed from AWS/Azure/GCP infrastructure share (2017–2024), with CR3
(top-three combined share) as a corroborating measure. The concentration trend is certified
with a non-parametric Mann-Kendall test rather than resting on OLS assumptions a short annual
series may violate.

## Key findings

| Metric | 2017 | 2023 | Change |
|--------|------|------|--------|
| HHI (Big Three) | 1,269 | 1,658 | **+30.7%** |
| CR3 combined share | 51% | 66% | **+15 pp** |
| AWS | 33% | 31% | −2 pp |
| Microsoft Azure | 12% | 24% | +12 pp |
| Google Cloud | 6% | 11% | +5 pp |

| Trend test (2017–2023, n=7) | Result |
|------|--------|
| Mann-Kendall | p = 0.0027 (significant at 0.01) |
| Kendall's τ | 1.00 (perfectly monotonic) |
| Sen's slope | +70.0 HHI/year |
| OLS slope | +68.9 HHI/year (R² = 0.99) |

## Methodology notes

- **HHI formula.** Σ(sᵢ²) over the Big Three (AWS, Azure, GCP), shares as whole-number points.
  A full-market HHI including all smaller providers would be lower in absolute value but
  directionally identical, since their combined share fell from ~49% (2017) to ~37% (2024).
- **Interpolation (stated limitation).** 2018–2021 provider shares are interpolated from
  Synergy's stated rate-of-change; 2017 and 2022–2024 are confirmed from primary press
  releases. Interpolated values are conservative estimates.
- **2024 reclassification flag.** Synergy moved a portion of Azure revenue (IaaS/PaaS → SaaS)
  in 2024, producing an artifactual HHI drop (1,658 → 1,485). The primary trend is treated as
  2017–2023; the 2024 row is flagged, not silently dropped.
- **Small-n limitation.** With 8 annual points, this is a structural/descriptive argument, not
  a regression claim. Mann-Kendall is the defensible significance test at this *n*;
  cross-variable comparison is done narratively, not as a mathematical merge.

## Data sources

| Year(s) | Source | Type |
|---------|--------|------|
| 2024 | Synergy Research Group Q4 2024 release | Primary |
| 2022–2023 | Synergy; cross-checked (holori, businesstats) | Primary |
| 2018–2021 | Interpolated from Synergy rate-of-change | Interpolated |
| 2017 | Synergy (AWS/Azure); Canalys Q4 2017 (GCP) | Primary |

All Synergy headline share figures are freely accessible at
[srgresearch.com/articles](https://www.srgresearch.com/articles) — no paywall.

## File structure

```
variable-2-cloud-concentration/
├── data/
│   ├── cloud_hhi.csv               # Compiled shares, per-row source notes
│   └── cloud_hhi.xlsx              # 3-sheet workbook: Data / OLS Regression / Key Findings
├── outputs/
│   ├── fig_hhi_dual_axis.png/.pdf      # Fig 1: HHI + CR3 dual-axis (300dpi)
│   ├── fig_provider_shares.png/.pdf    # Fig 2: individual provider shares
│   └── fig_hhi_regression.png/.pdf     # Fig 3: OLS trend + trend-test annotation
├── build_hhi_visuals.py            # Fig 1 & Fig 2
├── build_regression_visual.py      # Fig 3
├── build_hhi_xlsx.py               # 3-sheet workbook
├── trend_tests.py                  # Mann-Kendall + Sen's slope
├── hhi_interactive.html            # Interactive Chart.js dashboard (open in browser)
├── requirements.txt
└── README.md
```

## How to run

```bash
pip install -r requirements.txt
python build_hhi_visuals.py        # static Fig 1 + Fig 2 (PNG/PDF, 300dpi)
python build_regression_visual.py  # static Fig 3
python build_hhi_xlsx.py           # 3-sheet analysis workbook
python trend_tests.py              # Mann-Kendall + Sen's slope values
# hhi_interactive.html — open directly in any browser, no server needed
```

The xlsx workbook contains live formulas (HHI, OLS regression, cross-sheet references); opening
it in Excel or LibreOffice recalculates all values automatically.

## Relation to other variables

| Variable | Phenomenon | Method | Side |
|----------|-----------|--------|------|
| 1 — Cyberattacks | Attack frequency & sector spread | OLS time series | Pressure |
| **2 — Cloud concentration** | **Structural blast radius** | **HHI trend analysis** | **Pressure** |
| 3 — Cross-sector cascade | Cascade breadth over time | Sector-spread heatmap | Pressure |
| 4 — Regulatory capacity | Institutional response speed/scope | Qualitative event study | Capacity |

---
*CompTIA Security+ · Python (pandas, matplotlib, statsmodels) · Chart.js*
