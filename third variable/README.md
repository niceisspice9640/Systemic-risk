# Variable 3 — Cross-Sector Cascade Heatmap

Part of a study on whether cyberattacks and infrastructure disruptions have outpaced
institutional defensive and regulatory capacity (~2015–2025). This component maps the
**cross-sector footprint** of major supply-chain and platform incidents over time.

## What it shows

Twelve high-impact incidents (2020–2026), each coded across eight sectors using a strict
**binary rule**: a cell is filled only where public reporting confirms *meaningful
sector-level impact*. Cells stay empty where a sector was exposed but no realized
sector-level cascade was documented. The coding under-counts rather than over-counts.

A demarcation line marks **mid-2023** (public availability of adversarial AI tooling,
WormGPT/FraudGPT). Incidents below the line show broader footprints on average.

## Key finding (and its limits)

Mean sectors hit rises from **3.17 (pre-AI)** to **4.5 (AI-era)**. The IT/Cloud column is
filled for **every** incident — every event in the set cascaded through an IT or cloud
service provider, which is the structural throughline of the study.

**Important caveat, stated up front:** this is *illustrative, not causal*. The two widest
AI-era rows (MOVEit 8/8, CrowdStrike 7/8) stem from a zero-day and a faulty update — neither
caused by AI. The heatmap documents that AI-era incidents in this sample have broader
footprints; it does **not** establish that AI caused the broadening. That remains a
hypothesis for the conclusion, not a proven claim. With 12 events in a convenience sample,
two outliers move the average substantially.

## Methodology notes

- **Sector selection** follows the SPOF/cascade inclusion criterion used across the project:
  events grouped by shared *tech-coupled failure mechanism*, not by outcome.
- **Conservative coding** deliberately leaves "potential-but-unrealized" cascades empty
  (e.g. Okta, LastPass, Log4j have sparse rows despite high theoretical blast radius).
  These are flagged for a narrative footnote so sparse rows aren't misread as low severity.
- **No Retail column (known limitation).** Coop (Kaseya), Starbucks/grocers (Blue Yonder),
  and pharmacies (Change Healthcare) are retail-adjacent and currently absorbed into
  Logistics or Healthcare. Adding a Retail column would sharpen several rows.
- **SK Telecom** is handled qualitatively elsewhere as a *verification-dependency* cascade,
  a distinct typology from the platform-dependency cascades this heatmap captures.

## Files

| File | Purpose |
|---|---|
| `data/cascade_matrix.csv` | Binary sector-impact coding, one row per event |
| `build_cascade_heatmap.py` | Generates the 300dpi PNG/PDF figure for the paper |
| `outputs/fig_cascade_heatmap.png` / `.pdf` | Static academic figure |
| `outputs/cascade_heatmap_interactive.html` | Hover-annotated version for the live site |
| `CODING_RATIONALE.md` | Per-cell sourcing basis and coding-tension notes |

## Sources

Per-incident: CISA advisories, government reports (GAO, Congress, US Dept of Education/FSA,
NY DFS), incident analyses (Mandiant, CrowdStrike, Emsisoft, Volexity), and major-press
reporting. Full per-cell attribution in `CODING_RATIONALE.md`.

## Tech stack

Python (pandas, matplotlib) · vanilla HTML/CSS/JS for the interactive view.
