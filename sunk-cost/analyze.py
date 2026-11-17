"""Sunk cost: rebuild the results table from the three CSVs in raw/.

    python sunk-cost/analyze.py

The grader scores 1 for CONTINUE and 0 for CANCEL, so a condition's count of CONTINUE is the sum of its ratings.
"""
import sys
from pathlib import Path

import openpyxl
from scipy.stats import beta

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from common import fisher_p, fmt_p, here, load  # noqa: E402

RUNS = {"Pilot": "sunk_cost", "Full run": "sunk_cost_full", "Debias run": "sunk_cost_debias"}
LABELS = {1: "$5M return, no sunk cost (control)", 2: "$5M return, $40M already spent",
          3: "$7.5M return, no sunk cost", 4: "$7.5M return, $40M already spent"}
PAIRS = [(1, 2), (3, 4)]  # the sunk-cost sentence at each expected return


def clopper_pearson(k, n, alpha=0.05):
    lo = 0.0 if k == 0 else beta.ppf(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta.ppf(1 - alpha / 2, k + 1, n - k)
    return lo, hi


def continue_count(rows):
    return sum(1 for r in rows if r["rating"] == 1)


def aibo_cost(path):
    """Sum of the per-condition 'Cost' row in the results workbook's Analysis Data sheet."""
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    row = next(r for r in wb["Analysis Data"].iter_rows(values_only=True) if r and r[0] == "Cost")
    return sum(float(x) for x in row[1:] if x not in (None, ""))


runs = {name: load(here(__file__) / "raw" / f"{stem}.csv") for name, stem in RUNS.items()}

print("CONTINUE recommendations (grader), out of runs")
print()
print("| condition | " + " | ".join(runs) + " |")
print("|---|" + "---|" * len(runs))
for c, label in LABELS.items():
    cells = []
    for data in runs.values():
        cells.append(f"{continue_count(data[c])}/{len(data[c])}" if c in data else "not run")
    print(f"| {label} | " + " | ".join(cells) + " |")

print()
print("| run | condition | runs | CONTINUE | 95% CI (Clopper-Pearson) | replies exactly 'CANCEL' | missing ratings |")
print("|---|---|---|---|---|---|---|")
for name, data in runs.items():
    for c, rows in data.items():
        k, n = continue_count(rows), len(rows)
        lo, hi = clopper_pearson(k, n)
        exact = sum(1 for r in rows if r["response_1"].strip() == "CANCEL")
        missing = sum(1 for r in rows if r["rating"] is None)
        print(f"| {name} | {LABELS[c]} | {n} | {k} | [{lo:.3f}, {hi:.3f}] | {exact} | {missing} |")

print()
print("Fisher exact p, sunk-cost sentence vs none at the same return")
for name, data in runs.items():
    for a, b in PAIRS:
        if a in data and b in data:
            p = fisher_p(continue_count(data[b]), len(data[b]), continue_count(data[a]), len(data[a]))
            print(f"  {name}: condition {a} vs {b}: p = {fmt_p(p)}")

print()
total_k = sum(continue_count(rows) for data in runs.values() for rows in data.values())
total_n = sum(len(rows) for data in runs.values() for rows in data.values())
main_k = sum(continue_count(rows) for name in ("Full run", "Debias run") for rows in runs[name].values())
main_n = sum(len(rows) for name in ("Full run", "Debias run") for rows in runs[name].values())
print(f"Full and debias runs together: {main_k}/{main_n} CONTINUE")
print(f"All three runs together: {total_k}/{total_n} CONTINUE")
print()
for name, data in runs.items():
    cost = aibo_cost(here(__file__) / "raw" / f"{RUNS[name]}-analysis_results.xlsx")
    print(f"{name}: {len(data)} conditions x {', '.join(str(len(r)) for r in data.values())} runs, "
          f"run date {next(iter(data.values()))[0]['date']}, cost recorded by AIBO ${cost:.4f}")
