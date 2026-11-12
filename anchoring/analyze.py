"""Anchoring: rebuild the results table from raw/anchoring.csv.

    python anchoring/analyze.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from common import fmt_p, here, load, mean, ratings, sd, welch_p  # noqa: E402

LOW, HIGH = 6, 90

data = {c: ratings(rows) for c, rows in load(here(__file__) / "raw" / "anchoring.csv").items()}
labels = {1: "No anchor (control)", 2: "Colleague said 6", 3: "Colleague said 90",
          4: "Colleague said 90, plus 'disregard it'"}

print("| condition | runs | mean (engineer-weeks) | SD | p vs control (Welch t) |")
print("|---|---|---|---|---|")
for c, xs in data.items():
    p = "" if c == 1 else fmt_p(welch_p(xs, data[1]))
    print(f"| {labels[c]} | {len(xs)} | {mean(xs):.1f} | {sd(xs):.1f} | {p} |")

low, high, warned, control = (mean(data[c]) for c in (2, 3, 4, 1))
index = (high - low) / (HIGH - LOW)
removed = (high - warned) / (high - control)
print()
print(f"Anchoring index = (high mean - low mean) / ({HIGH} - {LOW}) = {index:.2f}")
print(f"Share of the high anchor's pull removed by the warning = {removed:.2f}; share left = {1 - removed:.2f}")
print(f"SD with the high anchor {sd(data[3]):.1f}, with the warning {sd(data[4]):.1f}")
