"""Small helpers shared by the analysis scripts: read an exported CSV and run the tests AIBO reports."""
import csv
from collections import defaultdict
from pathlib import Path

from scipy.stats import fisher_exact, ttest_ind


def load(path):
    """{condition number: [row dict, ...]} from a CSV written by tools/aibo_export.py."""
    out = defaultdict(list)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["rating"] = float(row["rating"]) if row["rating"] not in ("", "None") else None
            out[int(row["condition"])].append(row)
    return dict(sorted(out.items()))


def ratings(rows):
    return [r["rating"] for r in rows if r["rating"] is not None]


def mean(xs):
    return sum(xs) / len(xs)


def sd(xs):
    m = mean(xs)
    return (sum((x - m) ** 2 for x in xs) / (len(xs) - 1)) ** 0.5


def welch_p(a, b):
    """Two-sided Welch t-test p-value, the test AIBO runs on scale ratings."""
    return float(ttest_ind(a, b, equal_var=False).pvalue)


def fisher_p(k1, n1, k2, n2):
    """Two-sided Fisher exact p-value for k1/n1 vs k2/n2."""
    return float(fisher_exact([[k1, n1 - k1], [k2, n2 - k2]]).pvalue)


def fmt_p(p):
    return "<0.0001" if p < 0.0001 else f"{p:.4f}"


def here(file):
    return Path(file).resolve().parent
