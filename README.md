# Efficiency–Fragility in Digital Infrastructure: A Quantitative Study

> **Research question:** To what extent has the growth of cyberattacks and infrastructure
> disruptions across industries outpaced the growth of institutional defensive and regulatory
> capacity? (Study window ~2015–2025.)

The project's conceptual backbone is an **efficiency–fragility tradeoff**: efficiency gains in
digital infrastructure are structurally inseparable from fragility. As more of the digital
economy concentrates onto fewer providers and platforms, the blast radius of any single
failure — malicious or not — grows. Three anchor cases frame the analysis: the 2022 Kakao
data-center fire (infrastructure single point of failure), the 2025 SK Telecom breach
(identity-verification cascade), and the Canvas/Instructure ransomware incident
(centralized-platform risk across sectors).

## The four variables

The study is built from four variables. The first three measure the **pressure** side of the
research question (how attack frequency, structural concentration, and cross-sector cascades
have grown) and are each a self-contained, runnable module. The fourth measures the
**capacity** side and is a qualitative event study written up in the paper — it has no dataset
or code, so it lives in the paper rather than as a repository module.

| Variable | Question it answers | Side | Method | Module |
|---|---|---|---|---|
| **1 — Cyberattacks** | Has attack frequency/intensity grown over 2015–2024? | Pressure | OLS time series | [`variable-1-cyberattacks/`](./variable-1-cyberattacks) |
| **2 — Cloud concentration** | Has the blast radius of a single-provider failure grown? | Pressure | HHI / CR3 trend analysis | [`variable-2-cloud-concentration/`](./variable-2-cloud-concentration) |
| **3 — Cross-sector cascade** | Do incidents cascade across more sectors over time? | Pressure | Sector-spread heatmap | [`variable-3-cascade-heatmap/`](./variable-3-cascade-heatmap) |
| **4 — Regulatory capacity** | How fast and how systemically do institutions respond? | Capacity | Qualitative event study | Paper only (no module) |

Variables 1–3 establish that the pressure side has grown. Variable 4 examines whether
institutional capacity kept pace — its central finding is an asymmetry: firms remediate their
own defects quickly, but neither firms nor regulators systemically address the concentration
and tight coupling that Variables 2 and 3 measure. It is qualitative by design; public sources
cannot support a quantitative capacity index, and forcing one would misrepresent the evidence.

## Repository structure

```
.
├── variable-1-cyberattacks/          # EuRepoC cyberattack dataset analysis
├── variable-2-cloud-concentration/   # Cloud market HHI / concentration analysis
├── variable-3-cascade-heatmap/       # Cross-sector cascade footprint
└── README.md                         # (this file)
```

Each variable module is self-contained, with its own README, data, pipeline scripts, and
figure outputs (300dpi PNG/PDF for print, plus an interactive HTML view for the web build).
Every module README follows the same nine-section structure for consistency.

## Methodological principles

- **Intellectual honesty over quiet omission.** Data limitations are explicit methodology
  notes, not silent absorptions (e.g. HHI interpolation, the Uptime Institute paywall,
  conservative binary cascade coding).
- **Theory-driven, not results-driven.** Variable inclusion criteria are pre-specified;
  sensitivity checks are planned safeguards against cherry-picking.
- **Significance from tests, not trend lines.** At small *n*, non-parametric tests
  (Mann-Kendall) are the defensible significance claim rather than OLS p-values.
- **Causal exogeneity as the inclusion criterion.** What keeps natural disasters and
  geopolitical conflict out of scope is their independence from the *mechanisms* studied
  (SPOF/cascade dynamics, cloud concentration), not their independence from technology.

## Tech stack

Python (pandas, matplotlib, statsmodels, scipy, openpyxl) · Chart.js / D3.js for web
visualizations · LibreOffice-compatible Excel workbooks.

## Data sources

- EuRepoC Global Dataset of Cyber Incidents — Zenodo, DOI
  [10.5281/zenodo.14965395](https://doi.org/10.5281/zenodo.14965395), CC BY-NC 4.0
- Synergy Research Group quarterly press releases; Canalys
- Uptime Institute Annual Outage Analysis (executive summaries)
- Per-incident (Variable 3): CISA, government advisories, and major-press reporting

---
*CompTIA Security+ · Python · pandas · matplotlib · Chart.js*
