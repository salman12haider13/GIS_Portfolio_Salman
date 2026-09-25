"""Recreate the report charts and workflow overview for Geo Copilot.

Source: Salman Haider, Geo Copilot Final Report, sections 2.8, 3.1, 3.2,
3.4 and the query score table in Appendix B (PDF pages 45 to 48).
36 queries were scored against manual reference workflows. Both reported
scores include seven projection warnings that returned no workflow. The
counts must not be presented as successful executions.

Requires matplotlib. Run from any directory; output stays in the project.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon, FancyArrowPatch, Ellipse


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "images" / "projects" / "charts"
OUT.mkdir(parents=True, exist_ok=True)
EVIDENCE = ROOT / "assets" / "images" / "projects" / "evidence"
EVIDENCE.mkdir(parents=True, exist_ok=True)

# Query ID, complexity, function/order score, parameter score.
# These are all 36 GPT 5 rows in Appendix B, not execution pass/fail records.
SCORES = [
    (1, 1, 1, 1), (2, 1, 1, 1), (4, 1, 1, 1), (6, 1, 1, 1),
    (7, 1, 1, 0), (8, 1, 1, 1), (9, 1, 1, 1), (11, 1, 1, 1),
    (12, 1, 1, 1), (13, 1, 1, 1), (14, 1, 1, 1), (16, 1, 1, 1),
    (21, 2, 1, 1), (22, 2, 1, 1), (23, 2, 1, 1), (24, 2, 0, 0),
    (25, 2, 1, 1), (26, 2, 1, 1), (27, 2, 1, 1), (28, 2, 1, 1),
    (29, 2, 1, 1), (30, 2, 1, 1), (31, 2, 1, 1), (32, 2, 0, 0),
    (41, 3, 1, 1), (42, 3, 1, 1), (43, 3, 1, 1), (44, 3, 1, 1),
    (45, 3, 1, 1), (46, 3, 1, 1), (47, 3, 1, 0), (48, 3, 1, 1),
    (49, 3, 1, 1), (50, 3, 0, 0), (51, 3, 1, 1), (52, 3, 1, 0),
]
WARNINGS = {4, 21, 29, 30, 43, 46, 49}
FUNCTION_TOTAL = sum(row[2] for row in SCORES)
PARAMETER_TOTAL = sum(row[3] for row in SCORES)
MATCHING_WORKFLOWS = sum(row[2] == row[3] == 1 and row[0] not in WARNINGS for row in SCORES)
MISMATCHED_WORKFLOWS = sum(row[2] == 0 or row[3] == 0 for row in SCORES)
assert len(SCORES) == 36
assert (FUNCTION_TOTAL, PARAMETER_TOTAL) == (33, 30)
assert (MATCHING_WORKFLOWS, MISMATCHED_WORKFLOWS, len(WARNINGS)) == (23, 6, 7)
assert all(row[2:] == (1, 1) for row in SCORES if row[0] in WARNINGS)


def save_figure(fig, directory, stem):
    fig.savefig(directory / (stem + ".png"), dpi=180, facecolor="white")
    fig.savefig(directory / (stem + ".svg"), facecolor="white")
    svg = directory / (stem + ".svg")
    svg.write_text("\n".join(line.rstrip() for line in svg.read_text(encoding="utf-8").splitlines()) + "\n", encoding="utf-8")
    plt.close(fig)


def clean_axes(ax, limit, ticks):
    ax.set_yticks([])
    ax.set_xlim(0, limit)
    ax.set_xticks(ticks)
    ax.grid(axis="x", color="#D9D9D9", linewidth=0.7)
    ax.set_axisbelow(True)
    ax.spines[["top", "right", "left"]].set_visible(False)


WARNING_NOTE = "Scores include 7 projection warnings\nthat produced no workflow.\nThese are evaluation scores,\nnot execution success rates."

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 14,
    "axes.edgecolor": "#555555",
    "axes.labelcolor": "#222222",
    "text.color": "#222222",
    "xtick.color": "#333333",
    "ytick.color": "#222222",
    "svg.fonttype": "path",
})

fig, ax = plt.subplots(figsize=(4.8, 4.4), facecolor="white")
fig.subplots_adjust(left=0.085, right=0.955, top=0.765, bottom=0.40)
ax.barh([1.35, 0], [FUNCTION_TOTAL, PARAMETER_TOTAL], height=0.55, color="#4472C4", edgecolor="#2F5597", linewidth=0.8)
ax.set_yticks([])
ax.set_xlim(0, 36)
ax.set_ylim(-0.43, 2.16)
ax.set_xticks([0, 12, 24, 36])
ax.set_xlabel("Queries scored correct", labelpad=8, fontsize=12)
ax.grid(axis="x", color="#D9D9D9", linewidth=0.7)
ax.set_axisbelow(True)
ax.spines[["top", "right", "left"]].set_visible(False)
for y, value, label in [(1.35, 33, "Function selection and order"), (0, 30, "Parameter selection")]:
    ax.text(0, y + 0.43, label, ha="left", va="bottom", fontsize=14, backgroundcolor="white")
    ax.text(value - 0.9, y, f"{value} / 36", ha="right", va="center", color="white", weight="bold", fontsize=14)

fig.text(0.06, 0.935, "Geo Copilot evaluation", fontsize=16, ha="left")
fig.text(0.06, 0.865, "GPT 5: 36 test queries", fontsize=14, ha="left")
fig.text(0.06, 0.22, WARNING_NOTE, fontsize=11.5, ha="left", va="top", linespacing=1.3)

save_figure(fig, OUT, "geo-copilot-evaluation")

# Grouped horizontal bars keep the labels and exact denominators readable on a phone.
fig, ax = plt.subplots(figsize=(4.8, 6.3), facecolor="white")
fig.subplots_adjust(left=0.085, right=0.955, top=0.77, bottom=0.30)
clean_axes(ax, 12, [0, 4, 8, 12])
ax.set_ylim(0.10, 6.75)
labels = ["One operation", "Two operations", "More than two operations"]
for level, top_y, label in zip([1, 2, 3], [5.45, 3.35, 1.25], labels):
    rows = [row for row in SCORES if row[1] == level]
    assert len(rows) == 12
    functions, parameters = sum(row[2] for row in rows), sum(row[3] for row in rows)
    ax.text(0, top_y + 0.49, label, ha="left", va="bottom", fontsize=13.5, backgroundcolor="white")
    for y, value, color, text_color in [(top_y, functions, "#4472C4", "white"), (top_y - 0.63, parameters, "#B5B5B5", "#222222")]:
        ax.barh(y, value, height=0.52, color=color, edgecolor="#666666", linewidth=0.5)
        ax.text(value - 0.24, y, f"{value} / 12", ha="right", va="center", color=text_color, fontsize=12, weight="bold")
ax.set_xlabel("Queries scored correct (out of 12)", labelpad=8, fontsize=12)
fig.text(0.06, 0.952, "Scores by task complexity", fontsize=16, ha="left")
fig.text(0.06, 0.90, "GPT 5: 12 queries in each group", fontsize=12.5, ha="left")
fig.legend([Rectangle((0, 0), 1, 1, facecolor="#4472C4"), Rectangle((0, 0), 1, 1, facecolor="#B5B5B5")],
           ["Function / order", "Parameters"], loc="upper left", bbox_to_anchor=(0.043, 0.868),
           ncol=2, frameon=False, fontsize=12, handlelength=1.25, columnspacing=1.1)
fig.text(0.06, 0.175, WARNING_NOTE, fontsize=11.5, ha="left", va="top", linespacing=1.3)
save_figure(fig, OUT, "geo-copilot-complexity")

# Derived categories: remove the seven scored-correct warning responses from
# the 30 parameter-correct responses. This yields 23 matching command workflows.
# The six remaining command workflows contain at least one scored mismatch.
fig, ax = plt.subplots(figsize=(4.8, 5.3), facecolor="white")
fig.subplots_adjust(left=0.085, right=0.955, top=0.80, bottom=0.34)
clean_axes(ax, 36, [0, 12, 24, 36])
ax.set_ylim(-0.43, 3.86)
outcomes = [
    (3.0, MATCHING_WORKFLOWS, "Workflow matched the reference", "#4472C4", "white"),
    (1.5, MISMATCHED_WORKFLOWS, "Workflow had a mismatch", "#C58A4B", "#222222"),
    (0.0, len(WARNINGS), "Projection warning; no workflow", "#B5B5B5", "#222222"),
]
for y, value, label, color, text_color in outcomes:
    ax.text(0, y + 0.43, label, ha="left", va="bottom", fontsize=13, backgroundcolor="white")
    ax.barh(y, value, height=0.58, color=color, edgecolor="#666666", linewidth=0.5)
    ax.text(value - 0.7, y, str(value), ha="right", va="center", color=text_color, fontsize=14, weight="bold")
ax.set_xlabel("Responses (out of 36)", labelpad=8, fontsize=12)
fig.text(0.06, 0.944, "What the responses contained", fontsize=16, ha="left")
fig.text(0.06, 0.88, "GPT 5: 36 test queries", fontsize=14, ha="left")
fig.text(0.06, 0.19, "Derived from the query scores and\nseven warning cases in the report.\nThese categories describe responses,\nnot verified execution success.", fontsize=11.5, ha="left", va="top", linespacing=1.3)
save_figure(fig, OUT, "geo-copilot-response-outcomes")

# A code-native overview, deliberately distinct from an application screenshot.
# It shows the main interaction path. The case study explains the format check
# and error handling omitted from this high-level diagram.
fig = plt.figure(figsize=(6.4, 6.2), facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 640)
ax.set_ylim(620, 0)
ax.axis("off")
ink, line = "#28372F", "#365B49"

def label(x, y, text, size=16, weight="normal", align="center"):
    ax.text(x, y, text, ha=align, va="center", fontsize=size, color=ink, weight=weight, linespacing=1.28)

def box(x, y, width, height, fill="#F1F4ED"):
    ax.add_patch(Rectangle((x, y), width, height, facecolor=fill, edgecolor=line, linewidth=1.35))

def arrow(points):
    for a, b in zip(points[:-2], points[1:-1]):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=line, linewidth=1.4)
    ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>", mutation_scale=15, color=line, linewidth=1.4))

label(28, 36, "Geo Copilot", 24, align="left")
label(28, 72, "ArcGIS Pro + Large Language Models", 15, align="left")
ax.add_patch(Polygon([(46, 110), (290, 110), (272, 214), (28, 214)], closed=True, facecolor="#F1F4ED", edgecolor=line, linewidth=1.35))
label(158, 139, "GIS request", 18)
label(158, 181, "Buffer schools\nby 500 metres", 14)
box(352, 110, 260, 104)
label(482, 139, "Map context", 18)
label(482, 181, "Layers, fields and\ncoordinate systems", 14)
arrow([(158, 214), (158, 238), (275, 238), (275, 266)])
arrow([(482, 214), (482, 238), (365, 238), (365, 266)])
box(170, 267, 300, 90, "#EAF0FA")
label(320, 295, "LLM", 20)
label(320, 331, "Proposed commands", 16)
arrow([(320, 357), (320, 380), (215, 380), (215, 402)])
ax.add_patch(Polygon([(215, 399), (351, 462), (215, 525), (79, 462)], closed=True, facecolor="#F1F4ED", edgecolor=line, linewidth=1.35))
label(215, 445, "Review commands", 14)
label(215, 477, "Execute?", 18)
arrow([(351, 462), (388, 462)])
label(371, 442, "Yes", 11.5)
box(389, 420, 223, 84, "#EAF0FA")
label(500, 447, "ArcGIS Pro", 18)
label(500, 480, "GIS output", 15)
arrow([(215, 525), (215, 563)])
label(239, 541, "No", 12)
ax.add_patch(Ellipse((215, 585), 140, 43, facecolor="white", edgecolor=line, linewidth=1.35))
label(215, 585, "Quit", 15)
save_figure(fig, EVIDENCE, "geo-copilot-overview")
