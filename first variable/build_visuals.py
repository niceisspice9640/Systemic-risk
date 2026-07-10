"""
EuRepoC Visualization Pipeline
Reads the CSV outputs of clean_eurepoc.py and produces two parallel sets of figures
from the SAME underlying data, so the academic paper and the website always match:

1. STATIC figures (PNG 300dpi + PDF) using matplotlib -> for the academic paper
2. INTERACTIVE figures (standalone .html, Chart.js via CDN) -> for the live website

Run clean_eurepoc.py first to produce the input CSVs this script reads.
"""
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
import json

# Resolve paths relative to this script: read processed CSVs from data/processed,
# write static figures to figures/static and interactive HTML to figures/interactive.
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)
PROC_DIR = os.path.join(REPO_ROOT, "data", "processed")
STATIC_DIR = os.path.join(REPO_ROOT, "figures", "static")
INTERACTIVE_DIR = os.path.join(REPO_ROOT, "figures", "interactive")
os.makedirs(STATIC_DIR, exist_ok=True)
os.makedirs(INTERACTIVE_DIR, exist_ok=True)

def proc(name):
    return os.path.join(PROC_DIR, name)

def static_fig(name):
    return os.path.join(STATIC_DIR, name)

def web_fig(name):
    return os.path.join(INTERACTIVE_DIR, name)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.edgecolor": "#888780",
    "figure.dpi": 100,
})

COLOR_RAW = "#185FA5"
COLOR_ADJ = "#0F6E56"
SECTOR_COLORS = {
    "Critical infrastructure": "#D85A30",
    "State institutions / political system": "#185FA5",
    "Corporate Targets": "#BA7517",
    "Social groups": "#7F77DD",
    "Media": "#D4537E",
    "Education": "#1D9E75",
    "Science": "#639922",
    "Other": "#888780",
}

TYPE_COLORS = {
    "Ransomware": "#E24B4A",
    "Disruption": "#BA7517",
    "Data theft": "#7F77DD",
    "Data theft & Doxing": "#D4537E",
    "Hijacking with Misuse": "#D85A30",
    "Hijacking without Misuse": "#1D9E75",
    "Not available": "#888780",
}

# ---------- Load data ----------
annual = pd.read_csv(proc("eurepoc_annual_summary.csv"))
rcat = pd.read_csv(proc("eurepoc_receiver_category_by_year.csv"), index_col=0)
rcat = rcat.rename(columns={
    "Corporate Targets (corporate targets only coded if the respective company is not part of the critical infrastructure definition)": "Corporate Targets"
})
sector_cols = [c for c in SECTOR_COLORS if c in rcat.columns]
rcat = rcat[sector_cols]

itype = pd.read_csv(proc("eurepoc_incident_type_by_year.csv"), index_col=0)
type_cols = [c for c in TYPE_COLORS if c in itype.columns]
itype = itype[type_cols]

# =========================================================
# 1. STATIC FIGURES (matplotlib) -- for the academic paper
# =========================================================

# --- Figure 1: raw vs adjusted incident trend ---
fig, ax = plt.subplots(figsize=(7, 4.2))
ax.plot(annual["year"], annual["total_incidents"], color=COLOR_RAW, marker="o", linewidth=2, label="Total incidents (raw)")
ax.plot(annual["year"], annual["incidents_excl_ci_only"], color=COLOR_ADJ, marker="o", linewidth=2, linestyle="--", label="Excluding CI-only-rule incidents (adjusted)")
ax.axvline(2023, color="#888780", linestyle=":", linewidth=1)
ax.text(2023.05, ax.get_ylim()[1]*0.95, "Feb 2023 rule change", fontsize=9, color="#666666", va="top")
ax.set_xlabel("Year")
ax.set_ylabel("Number of incidents")
ax.set_xticks(annual["year"])
ax.legend(frameon=False, loc="upper left", fontsize=9)
fig.tight_layout()
fig.savefig(static_fig("fig_trend_raw_vs_adjusted.png"), dpi=300)
fig.savefig(static_fig("fig_trend_raw_vs_adjusted.pdf"))
plt.close(fig)

# --- Figure 2: sector breakdown, stacked bar (deduplicated) ---
fig, ax = plt.subplots(figsize=(7.5, 4.5))
bottom = pd.Series(0, index=rcat.index)
for col in sector_cols:
    ax.bar(rcat.index, rcat[col], bottom=bottom, color=SECTOR_COLORS[col], label=col.replace(" / political system", ""))
    bottom += rcat[col]
ax.set_xlabel("Year")
ax.set_ylabel("Incidents (deduplicated by category)")
ax.set_xticks(rcat.index)
ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper left")
fig.tight_layout()
fig.savefig(static_fig("fig_sector_breakdown.png"), dpi=300)
fig.savefig(static_fig("fig_sector_breakdown.pdf"))
plt.close(fig)

print("Static figures saved: fig_trend_raw_vs_adjusted.[png/pdf], fig_sector_breakdown.[png/pdf]")

# --- Figure 3: incident type breakdown, stacked bar ---
fig, ax = plt.subplots(figsize=(7.5, 4.5))
bottom = pd.Series(0, index=itype.index)
for col in type_cols:
    ax.bar(itype.index, itype[col], bottom=bottom, color=TYPE_COLORS[col], label=col)
    bottom += itype[col]
ax.set_xlabel("Year")
ax.set_ylabel("Incidents (by attack type tag)")
ax.set_xticks(itype.index)
ax.legend(frameon=False, fontsize=8, ncol=2, loc="upper left")
fig.tight_layout()
fig.savefig(static_fig("fig_incident_type_breakdown.png"), dpi=300)
fig.savefig(static_fig("fig_incident_type_breakdown.pdf"))
plt.close(fig)

print("Static figure saved: fig_incident_type_breakdown.[png/pdf]")

# --- Figure 4: OLS trend regression on the rule-adjusted series ---
# Regression is run on the adjusted series (incidents_excl_ci_only), which is the
# series used as the composite input. Linear specification, primary model.
COLOR_TREND = "#B03A2E"
reg_years = annual["year"].values.astype(float)
reg_y = annual["incidents_excl_ci_only"].values.astype(float)
reg_t = reg_years - reg_years.min()  # 0..n for numerical stability
reg_X = sm.add_constant(reg_t)
reg_model = sm.OLS(reg_y, reg_X).fit()
reg_pred = reg_model.get_prediction(reg_X)
reg_fit = reg_pred.predicted_mean
reg_ci = reg_pred.conf_int(alpha=0.05)  # 95% CI
reg_slope = reg_model.params[1]
reg_p = reg_model.pvalues[1]
reg_r2 = reg_model.rsquared

fig, ax = plt.subplots(figsize=(7, 4.2))
ax.scatter(reg_years, reg_y, color=COLOR_ADJ, zorder=3, s=42, label="Adjusted incidents (observed)")
ax.plot(reg_years, reg_y, color=COLOR_ADJ, alpha=0.35, linewidth=1.2, zorder=2)
ax.plot(reg_years, reg_fit, color=COLOR_TREND, linewidth=2, zorder=4,
        label=f"OLS trend (+{reg_slope:.0f}/yr, p={reg_p:.3f}, R\u00b2={reg_r2:.2f})")
ax.fill_between(reg_years, reg_ci[:, 0], reg_ci[:, 1], color=COLOR_TREND, alpha=0.12, zorder=1, label="95% confidence interval")
ax.set_xlabel("Year")
ax.set_ylabel("Number of incidents (rule-adjusted)")
ax.set_xticks(reg_years.astype(int))
ax.legend(frameon=False, fontsize=9, loc="upper left")
fig.tight_layout()
fig.savefig(static_fig("fig_trend_regression.png"), dpi=300)
fig.savefig(static_fig("fig_trend_regression.pdf"))
plt.close(fig)

print(f"Static figure saved: fig_trend_regression.[png/pdf]  (slope={reg_slope:.2f}, p={reg_p:.4f}, R2={reg_r2:.3f})")

# =========================================================
# 2. INTERACTIVE HTML FIGURES (Chart.js via CDN) -- for the website
# =========================================================

HTML_TEMPLATE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title></head>
<body>
<div style="max-width:800px;margin:0 auto;font-family:Arial,sans-serif;">
<div style="position:relative;width:100%;height:380px;">
<canvas id="chart" role="img" aria-label="{aria_label}"></canvas>
</div>
<p style="font-size:12px;color:#666;text-align:center;">{caption}</p>
</div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
{chart_js}
</script>
</body></html>
"""

# --- Web chart 1: trend ---
trend_js = f"""
new Chart(document.getElementById('chart'), {{
  type: 'line',
  data: {{
    labels: {json.dumps(annual['year'].tolist())},
    datasets: [
      {{ label: 'Total incidents (raw)', data: {json.dumps(annual['total_incidents'].tolist())}, borderColor: '{COLOR_RAW}', backgroundColor: '{COLOR_RAW}', borderWidth: 2, pointRadius: 3, tension: 0.15 }},
      {{ label: 'Excluding CI-only-rule incidents (adjusted)', data: {json.dumps(annual['incidents_excl_ci_only'].tolist())}, borderColor: '{COLOR_ADJ}', backgroundColor: '{COLOR_ADJ}', borderWidth: 2, borderDash: [6,4], pointRadius: 3, tension: 0.15 }}
    ]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'Number of incidents' }} }} }}
  }}
}});
"""
with open(web_fig("web_trend_raw_vs_adjusted.html"), "w") as f:
    f.write(HTML_TEMPLATE.format(
        title="Cyber incidents 2015-2024",
        aria_label="Line chart comparing raw and rule-adjusted EuRepoC incident counts by year",
        caption="Source: EuRepoC Global Dataset of Cyber Incidents v1.3.2",
        chart_js=trend_js
    ))

# --- Web chart 2: sector breakdown ---
datasets_js = ",\n".join([
    f"{{ label: '{col}', data: {json.dumps(rcat[col].tolist())}, backgroundColor: '{SECTOR_COLORS[col]}' }}"
    for col in sector_cols
])
sector_js = f"""
new Chart(document.getElementById('chart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(rcat.index.tolist())},
    datasets: [{datasets_js}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ x: {{ stacked: true }}, y: {{ stacked: true, beginAtZero: true, title: {{ display: true, text: 'Incidents (deduplicated)' }} }} }}
  }}
}});
"""
with open(web_fig("web_sector_breakdown.html"), "w") as f:
    f.write(HTML_TEMPLATE.format(
        title="Incidents by sector 2015-2024",
        aria_label="Stacked bar chart of EuRepoC incidents by sector category, deduplicated, by year",
        caption="Source: EuRepoC Global Dataset of Cyber Incidents v1.3.2",
        chart_js=sector_js
    ))

print("Interactive HTML charts saved: web_trend_raw_vs_adjusted.html, web_sector_breakdown.html")

# --- Web chart 3: incident type breakdown ---
datasets_js_type = ",\n".join([
    f"{{ label: '{col}', data: {json.dumps(itype[col].tolist())}, backgroundColor: '{TYPE_COLORS[col]}' }}"
    for col in type_cols
])
type_js = f"""
new Chart(document.getElementById('chart'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(itype.index.tolist())},
    datasets: [{datasets_js_type}]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'top' }} }},
    scales: {{ x: {{ stacked: true }}, y: {{ stacked: true, beginAtZero: true, title: {{ display: true, text: 'Incidents (by attack type tag)' }} }} }}
  }}
}});
"""
with open(web_fig("web_incident_type_breakdown.html"), "w") as f:
    f.write(HTML_TEMPLATE.format(
        title="Incidents by attack type 2015-2024",
        aria_label="Stacked bar chart of EuRepoC incidents by attack type, by year",
        caption="Source: EuRepoC Global Dataset of Cyber Incidents v1.3.2. An incident can carry multiple type tags (e.g. ransomware + disruption), so totals exceed incident counts.",
        chart_js=type_js
    ))

print("Interactive HTML chart saved: web_incident_type_breakdown.html")

# --- Web chart 4: OLS trend regression (with CI band) ---
# Chart.js draws the CI band as two line datasets filling between them. The lower
# bound is hidden from the legend via a filter on its label ("_lo").
reg_lo = [round(v, 1) for v in reg_ci[:, 0]]
reg_hi = [round(v, 1) for v in reg_ci[:, 1]]
reg_fit_r = [round(v, 1) for v in reg_fit]
reg_label = f"OLS trend (+{reg_slope:.0f}/yr, p={reg_p:.3f}, R\u00b2={reg_r2:.2f})"
regression_js = f"""
new Chart(document.getElementById('chart'), {{
  type: 'line',
  data: {{
    labels: {json.dumps(reg_years.astype(int).tolist())},
    datasets: [
      {{ label: '95% confidence interval', data: {json.dumps(reg_hi)}, borderColor: 'transparent', backgroundColor: 'rgba(176,58,46,0.12)', pointRadius: 0, fill: '+1' }},
      {{ label: '_lo', data: {json.dumps(reg_lo)}, borderColor: 'transparent', backgroundColor: 'rgba(176,58,46,0.12)', pointRadius: 0, fill: false }},
      {{ label: '{reg_label}', data: {json.dumps(reg_fit_r)}, borderColor: '{COLOR_TREND}', borderWidth: 2, pointRadius: 0, fill: false }},
      {{ label: 'Adjusted incidents (observed)', data: {json.dumps(reg_y.astype(int).tolist())}, borderColor: '{COLOR_ADJ}', backgroundColor: '{COLOR_ADJ}', showLine: false, pointRadius: 4 }}
    ]
  }},
  options: {{
    responsive: true, maintainAspectRatio: false,
    plugins: {{ legend: {{ position: 'top', labels: {{ filter: i => i.text !== '_lo' }} }} }},
    scales: {{ y: {{ beginAtZero: true, title: {{ display: true, text: 'Incidents (rule-adjusted)' }} }} }}
  }}
}});
"""
with open(web_fig("web_trend_regression.html"), "w") as f:
    f.write(HTML_TEMPLATE.format(
        title="Adjusted incident trend with OLS regression",
        aria_label="Scatter of rule-adjusted EuRepoC cyber incidents per year 2015-2024 with fitted OLS trend line and 95 percent confidence band.",
        caption="Rule-adjusted annual incidents with OLS trend line and 95% confidence interval. Source: EuRepoC v1.3.2. n=10.",
        chart_js=regression_js
    ))

print("Interactive HTML chart saved: web_trend_regression.html")
