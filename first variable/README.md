# Cyber and Operations Risk Composite Index

A data pipeline and analysis project examining whether the growth of cyberattacks
and infrastructure disruptions across industries has outpaced institutional
defensive and regulatory capacity (study window: 2015–2025).

The project builds a composite index from multiple independent, tech-coupled
operational-risk indicators, each drawn from a free, publicly documented data
source, with an emphasis on reproducibility and transparent methodology.

> **Status:** work in progress. Indicator #1 (cyberattacks, EuRepoC) is complete.
> Indicators #2 (outages, IODA) and #3 (supply-chain, Sonatype) are in progress.

## Composite indicators

| # | Indicator | Source | Status |
|---|-----------|--------|--------|
| 1 | Cyberattacks | [EuRepoC Global Dataset of Cyber Incidents](https://eurepoc.eu/) | ✅ Complete |
| 2 | Non-malicious IT / cloud outages | [IODA (CAIDA / Georgia Tech)](https://ioda.inetintel.cc.gatech.edu/) | 🔧 In progress |
| 3 | Third-party / supply-chain dependency | [Sonatype State of the Software Supply Chain](https://www.sonatype.com/state-of-the-software-supply-chain/introduction) | ⏳ Planned |
| — | Cloud market concentration (HHI) | Synergy Research / Canalys market share | ⏳ Covariate (planned) |

FBI IC3 and Verizon DBIR were evaluated and deliberately excluded from the
composite; they measure financial loss and breach detail rather than incident
frequency, and are cited (if at all) only as supporting context.

## Repository structure

```
cyber-ops-risk-index/
├── data/
│   ├── raw/          # Original source datasets (unmodified)
│   └── processed/    # Cleaned + aggregated outputs from the scripts
├── scripts/
│   ├── clean_eurepoc.py    # Raw EuRepoC CSV -> cleaned, flagged, aggregated
│   └── build_visuals.py    # Processed CSVs -> static + interactive figures
├── figures/
│   ├── static/       # 300dpi PNG + PDF (for the academic paper)
│   └── interactive/  # Standalone HTML (Chart.js, for the website)
├── output/           # Human-readable Excel summary workbook
├── requirements.txt
└── README.md
```

## Reproducing the analysis

```bash
# 1. install dependencies
pip install -r requirements.txt

# 2. clean and aggregate the raw EuRepoC data
cd scripts
python clean_eurepoc.py

# 3. generate all figures (static PNG/PDF + interactive HTML)
python build_visuals.py
```

`clean_eurepoc.py` reads `data/raw/eurepoc_global_dataset_1_3.csv` and writes the
processed CSVs to `data/processed/`; `build_visuals.py` reads those and writes
static figures to `figures/static/` and interactive HTML to
`figures/interactive/`. Both scripts resolve paths relative to their own
location, so they run out of the box from the repo root (`python
scripts/clean_eurepoc.py`) or from inside `scripts/` — no path editing needed.

## Key methodological decisions

The cleaning pipeline encodes several deliberate choices, each documented in the
`Cleaning_Log` sheet of the Excel summary and in code comments:

1. **Study window 2015–2024.** 2025 requires a separate provisional pull from
   EuRepoC's TableView (not yet expert-reviewed).
2. **85 incidents dropped** for having no usable date in either `start_date` or
   `end_date`.
3. **February 2023 rule-change flag.** EuRepoC expanded its inclusion criteria in
   Feb 2023 to capture critical-infrastructure incidents regardless of initiator.
   Incidents qualifying *only* under this rule are flagged (`ci_only_post2023_rule`);
   ~24% of the windowed dataset carries the flag, concentrated in 2023–2024
   (≈39% and 43% of those years). The trend is reported both raw and
   rule-adjusted as a sensitivity check — the raw series materially overstates
   2023–2024 growth.
4. **Receiver-category deduplication.** EuRepoC's receiver data repeats one row
   per affected country, so a single multi-country incident can dominate a
   year's sector totals (one 2022 espionage campaign alone accounted for 54% of
   that year's raw "critical infrastructure" tag count). Each incident is counted
   once per distinct category.

## Data sources & licensing

- **EuRepoC Global Dataset of Cyber Incidents** v1.3.2 — Zenodo,
  DOI [10.5281/zenodo.14965395](https://doi.org/10.5281/zenodo.14965395),
  licensed **CC BY-NC 4.0**. The raw dataset in `data/raw/` is redistributed
  here under those terms (attribution, non-commercial). If you fork this repo
  for any commercial purpose, you must remove the raw dataset and obtain it
  directly from EuRepoC under appropriate terms.

See [`LICENSE`](LICENSE) for this project's own code license and important
notes on the data license.
