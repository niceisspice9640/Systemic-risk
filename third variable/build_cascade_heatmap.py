"""
build_cascade_heatmap.py
Variable 3 — Cross-sector cascade heatmap.

Reads data/cascade_matrix.csv (binary sector-impact coding, one row per event)
and produces a 300dpi PNG + PDF heatmap for the academic paper.

Coding rule: a cell is filled only where public reporting confirms meaningful
sector-level impact. Conservative by design (under-counts rather than over-counts).
See CODING_RATIONALE.md for per-cell sourcing.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import os

DATA = "data/cascade_matrix.csv"
OUT = "outputs"
os.makedirs(OUT, exist_ok=True)

SECTORS = ["Financial", "Healthcare", "Telecom", "Government",
           "Education", "Logistics", "Energy_Utilities", "IT_Cloud"]
SECTOR_LABELS = ["Financial\nServices", "Healthcare", "Telecom", "Government",
                 "Education", "Logistics /\nSupply Chain", "Energy /\nUtilities",
                 "IT / Cloud\nServices"]

# --- palette (kept consistent with a restrained, data-forward academic look) ---
INK      = "#1a1a2e"   # near-black ink for text
FILL     = "#2a4d69"   # deep slate-blue for a confirmed impact
EMPTY    = "#eef1f4"   # very light grey for no documented impact
GRIDLINE = "#ffffff"   # white cell separators
DEMARC   = "#c1440e"   # burnt-orange demarcation line (era boundary)
PRE_TINT = "#f7f9fb"
AI_TINT  = "#fdf6f0"

df = pd.read_csv(DATA)
df["dt"] = pd.to_datetime(df["date"], format="%Y-%m")
df = df.sort_values("dt").reset_index(drop=True)

matrix = df[SECTORS].values
n_events, n_sectors = matrix.shape

# index of the first AI-era row (for the demarcation line)
first_ai = df.index[df["era"] == "ai_era"][0]

# breadth = number of sectors hit (row annotation)
breadth = matrix.sum(axis=1)

fig, ax = plt.subplots(figsize=(11.5, 8.5))

cmap = ListedColormap([EMPTY, FILL])
ax.imshow(matrix, cmap=cmap, aspect="auto", vmin=0, vmax=1)

# era background tints (behind cells via axvspan-like shading using pcolor edges)
ax.set_xlim(-0.5, n_sectors - 0.5)
ax.set_ylim(n_events - 0.5, -0.5)

# white gridlines between cells
for x in range(n_sectors + 1):
    ax.axvline(x - 0.5, color=GRIDLINE, lw=2)
for y in range(n_events + 1):
    ax.axhline(y - 0.5, color=GRIDLINE, lw=2)

# demarcation line between eras
ax.axhline(first_ai - 0.5, color=DEMARC, lw=3.2, zorder=5)
ax.annotate("AI-enabled adversarial tooling proliferates\n(WormGPT / FraudGPT, mid-2023)",
            xy=(n_sectors - 0.5, first_ai - 0.5),
            xytext=(n_sectors - 0.45, first_ai - 0.5),
            va="center", ha="left", fontsize=8.5, color=DEMARC,
            fontweight="bold", annotation_clip=False)

# axis labels
ax.set_xticks(range(n_sectors))
ax.set_xticklabels(SECTOR_LABELS, fontsize=9, color=INK)
ax.xaxis.set_ticks_position("top")
ax.xaxis.set_label_position("top")

ylabels = [f"{r.event}" for r in df.itertuples()]
ydates  = [r.dt.strftime("%b %Y") for r in df.itertuples()]
ax.set_yticks(range(n_events))
ax.set_yticklabels([f"{e}\n{d}" for e, d in zip(ylabels, ydates)],
                   fontsize=8.5, color=INK)

# breadth annotation on the right
for i, b in enumerate(breadth):
    ax.annotate(f"{b}/8", xy=(n_sectors - 0.5 + 0.02, i),
                xytext=(n_sectors - 0.5 + 1.35, i),
                va="center", ha="center", fontsize=8, color=INK,
                annotation_clip=False,
                bbox=dict(boxstyle="round,pad=0.25", fc="#f0f0f0", ec="none"))
ax.annotate("sectors\nhit", xy=(n_sectors - 0.5 + 1.35, -1.15),
            va="center", ha="center", fontsize=7.5, color="#666",
            annotation_clip=False)

for spine in ax.spines.values():
    spine.set_visible(False)
ax.tick_params(length=0)

# legend
legend_elems = [
    Patch(facecolor=FILL, edgecolor="none", label="Documented sector-level impact"),
    Patch(facecolor=EMPTY, edgecolor="none", label="No documented sector-level cascade"),
]
ax.legend(handles=legend_elems, loc="upper left",
          bbox_to_anchor=(0.0, -0.04), ncol=2, frameon=False, fontsize=9)

fig.suptitle("Cross-sector cascade footprint of major supply-chain / platform incidents, 2020–2026",
             fontsize=13, fontweight="bold", color=INK, y=0.99, x=0.5)
ax.set_title("Binary coding: a cell is filled only where public reporting confirms meaningful sector impact (conservative).",
             fontsize=8.7, color="#555", pad=34, loc="left")

fig.text(0.01, 0.005,
         "Sources: CISA, government advisories, Mandiant/CrowdStrike/Emsisoft analyses, and major-press reporting per incident (see CODING_RATIONALE.md). "
         "Rows with sparse fills (e.g. Log4j, Okta) reflect high cascade potential but limited documented realized impact.",
         fontsize=6.4, color="#888", ha="left")

plt.tight_layout(rect=[0, 0.02, 1, 0.97])
fig.savefig(f"{OUT}/fig_cascade_heatmap.png", dpi=300, bbox_inches="tight")
fig.savefig(f"{OUT}/fig_cascade_heatmap.pdf", bbox_inches="tight")
print("Saved fig_cascade_heatmap.png / .pdf")
print(f"Events: {n_events} | Pre-AI: {(df.era=='pre_ai').sum()} | AI-era: {(df.era=='ai_era').sum()}")
print("Mean sectors hit — pre-AI:", round(breadth[df.era=='pre_ai'].mean(),2),
      "| AI-era:", round(breadth[df.era=='ai_era'].mean(),2))
