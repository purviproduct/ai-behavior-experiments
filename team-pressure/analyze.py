"""Team pressure: rebuild the three pilot tables and every number in the README from raw/*.csv.

    python team-pressure/analyze.py
"""
import re
import sys
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from common import fmt_p, here, load, mean, ratings, sd, welch_p  # noqa: E402

RAW = here(__file__) / "raw"
PEER = 90      # the wrong estimate (engineer-weeks) every peer posts in the two estimation pilots
MEDIOCRE = 80  # % of the mediocre budget plan in Podcast + Trade show (the good plan has 20%)


def table(rows, labels, unit):
    """Print one results table and return {condition: [grader numbers]}."""
    data = {c: ratings(rs) for c, rs in rows.items()}
    print(f"| Condition | Runs | Mean {unit} | SD | p vs control (Welch t) |")
    print("|---|---|---|---|---|")
    for c, xs in data.items():
        p = "" if c == 1 else fmt_p(welch_p(xs, data[1]))
        print(f"| {labels[c]} | {len(xs)} | {mean(xs):.1f} | {sd(xs):.1f} | {p} |")
    print()
    return data


def index(arm, control, target):
    """Share of the gap between the control mean and the peer's value that the agent moved."""
    return (mean(arm) - mean(control)) / (target - mean(control))


def bare_number_matches(rows):
    """How many replies are a bare number equal to the grader's number."""
    n = 0
    for rs in rows.values():
        for r in rs:
            try:
                n += float(r["response_1"].strip()) == r["rating"]
            except ValueError:
                pass
    return n


def dates(*row_sets):
    return sorted({r["date"] for rows in row_sets for rs in rows.values() for r in rs})


# ---------------------------------------------------------------- 1. Confident error
print("## 1. Confident error\n")
ce_rows = load(RAW / "confident_error.csv")
ce_labels = {1: "No peer message (control)", 2: "Peer says 90", 3: "Peer says 90, hedged",
             4: "Peer says 90, highly confident"}
ce = table(ce_rows, ce_labels, "estimate (engineer-weeks)")
for c in (2, 3, 4):
    print(f"Index, {ce_labels[c]}: (mean - control) / ({PEER} - control) = {index(ce[c], ce[1], PEER):.2f}")
print(f"Hedged vs highly confident: means {mean(ce[3]):.1f} vs {mean(ce[4]):.1f}, p = {welch_p(ce[3], ce[4]):.2f}")
print(f"Replies that are a bare number equal to the grader's number: "
      f"{bare_number_matches(ce_rows)}/{sum(map(len, ce_rows.values()))}")
print()

# ---------------------------------------------------------------- 2. False consensus
print("## 2. False consensus\n")
fc_rows = load(RAW / "false_consensus.csv")
fc_labels = {1: "No peer message (control)", 2: "One peer says 90", 3: "One peer says 90, claims B and C agree",
             4: "Three peers each say 90"}
fc = table(fc_rows, fc_labels, "estimate (engineer-weeks)")
print(f"Claimed consensus vs one peer: p = {fmt_p(welch_p(fc[3], fc[2]))}")
print(f"Three visible peers vs claimed consensus: p = {fmt_p(welch_p(fc[4], fc[3]))}")
print(f"Three visible peers vs one peer: p = {fmt_p(welch_p(fc[4], fc[2]))}")
peer_arm_values = sorted((x, c) for c in (2, 3, 4) for x in fc[c])
print("Three lowest estimates across the three peer arms (value, condition):",
      ", ".join(f"{x:g} (cond {c})" for x, c in peer_arm_values[:3]))
sds = {c: sd(xs) for c, xs in fc.items()}
print("SD by condition:", ", ".join(f"{c}: {s:.1f}" for c, s in sds.items()),
      f"(highest: condition {max(sds, key=sds.get)})")
print(f"Replies that are a bare number equal to the grader's number: "
      f"{bare_number_matches(fc_rows)}/{sum(map(len, fc_rows.values()))}")
print()

# ---------------------------------------------------------------- 3. First mover
print("## 3. First mover\n")
fm_rows = load(RAW / "first_mover.csv")
fm_labels = {1: "Agent proposes first (control)", 2: "Mediocre plan first", 3: "Mediocre first, then good plan",
             4: "Good first, then mediocre plan"}
fm = table(fm_rows, fm_labels, "% in Podcast + Trade show")
print(f"Shift, {fm_labels[2]} vs control: {mean(fm[2]) - mean(fm[1]):.1f} points")
print(f"Index, {fm_labels[2]}: (mean - control) / ({MEDIOCRE} - control) = {index(fm[2], fm[1], MEDIOCRE):.2f}")
print(f"Mediocre first vs good first (both plans posted): means {mean(fm[3]):.1f} vs {mean(fm[4]):.1f}, "
      f"p = {welch_p(fm[3], fm[4]):.2f}")

# The prompt fixes the reply format ("Search: $X, Email: $X, Podcast: $X, Trade show: $X"), so the
# per-channel amounts can be read back from each reply and checked against the grader's number.
SPLIT = re.compile(r"Search:\s*\$?([\d,]+),\s*Email:\s*\$?([\d,]+),\s*Podcast:\s*\$?([\d,]+),"
                   r"\s*Trade show:\s*\$?([\d,]+)")
parsed, agree, strong = 0, 0, []
for c, rs in fm_rows.items():
    for r in rs:
        m = SPLIT.fullmatch(r["response_1"].strip())
        if not m:
            continue
        search, email, podcast, trade = (int(g.replace(",", "")) for g in m.groups())
        total = search + email + podcast + trade
        parsed += 1
        agree += abs(100 * (podcast + trade) / total - r["rating"]) < 1e-9
        strong.append((100 * (search + email) / total, c))
n_fm = sum(map(len, fm_rows.values()))
low = min(s for s, _ in strong)
print(f"Replies in the requested format: {parsed}/{n_fm}")
print(f"Grader's share equals the share computed from the reply: {agree}/{parsed}")
print(f"Lowest Search + Email share in any reply: {low:.0f}% "
      f"({sum(s == low for s, _ in strong)} replies, conditions {sorted({c for s, c in strong if s == low})})")
print()

# ---------------------------------------------------------------- Shared facts for the README
print("## Shared\n")
anchoring = {c: ratings(rs) for c, rs in load(here(__file__).parent / "anchoring" / "raw" / "anchoring.csv").items()}
print(f"Control means: anchoring (no team) {mean(anchoring[1]):.1f}, confident error {mean(ce[1]):.1f}, "
      f"false consensus {mean(fc[1]):.1f}")
print("Run dates (date column):", ", ".join(dates(ce_rows, fc_rows, fm_rows)),
      "| anchoring pilot:", ", ".join(dates(load(here(__file__).parent / "anchoring" / "raw" / "anchoring.csv"))))
print("Models:", sorted({(r["model"], r["temperature"]) for rows in (ce_rows, fc_rows, fm_rows)
                         for rs in rows.values() for r in rs}))
print(f"Runs: {sum(map(len, ce_rows.values())) + sum(map(len, fc_rows.values())) + n_fm}")


def cost(name):
    """Sum of the 'Cost' row in AIBO's Analysis Data sheet (one value per condition)."""
    wb = openpyxl.load_workbook(RAW / f"{name}-analysis_results.xlsx", read_only=True, data_only=True)
    row = next(r for r in wb["Analysis Data"].iter_rows(values_only=True) if r and r[0] == "Cost")
    return sum(float(str(x).lstrip("$")) for x in row[1:] if x not in (None, ""))


def grader(name):
    """(grader model, grader temperature) from the Settings sheet of AIBO's results workbook."""
    wb = openpyxl.load_workbook(RAW / f"{name}-analysis_results.xlsx", read_only=True, data_only=True)
    meta = {r[0]: r[1] for r in wb["Settings"].iter_rows(values_only=True) if r and r[0] is not None}
    return meta["Model for Rating"], meta["Temperature for Rating"]


PILOTS = ("confident_error", "false_consensus", "first_mover")
print("Grader (model, temperature):", sorted({grader(n) for n in PILOTS}))
costs = {n: cost(n) for n in PILOTS}
print("Cost recorded by AIBO:", ", ".join(f"{n} ${v:.4f}" for n, v in costs.items()),
      f"(total ${sum(costs.values()):.4f})")
