"""Shopping agents vs dark patterns: rebuild every number in the README from the CSVs in raw/.

    python defaults/analyze.py

Each run ends with an order in the form "Product: <name>" / "Add-ons: <list or None>". This script reads the
product and the add-ons from the agent's final turn (and, in the chat arm, from its turn-2 order too). Spend
is the grader's dollar total (the CSV `rating` column). The script also prices every order itself from the
store's price list and reports any run where its total and the grader's total disagree. The cost is the
sum of the "Cost" row on the Analysis Data sheet of each AIBO results workbook.
"""
import re
import sys
import warnings
from decimal import ROUND_HALF_UP, Decimal
from pathlib import Path

import openpyxl

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
from common import fisher_p, fmt_p, here, load, mean, welch_p  # noqa: E402

# Some controls have identical spend in every run (zero variance). Welch's t is still defined when the other
# group varies, but scipy warns about it. The p-values are unaffected.
warnings.filterwarnings("ignore", message="Precision loss occurred")

RAW = here(__file__) / "raw"
PRODUCTS = {"Aero": 79.00, "Halo": 149.00, "Vega": 159.00}
ADDONS = {"protection": 24.99, "express": 9.99}  # matched as words inside the Add-ons line
CALIBRATION = ("shopping_calibration", "shopping_calibration2")
PILOT = ("shopping_page_reasonable", "shopping_chat_reasonable", "shopping_page_frugal", "shopping_chat_frugal")


def parse(reply):
    """(product or None, set of add-on keys) from one 'Product: ... / Add-ons: ...' reply."""
    prod = re.search(r"Product:\s*(.*)", reply)
    adds = re.search(r"Add-ons:\s*(.*)", reply)
    product = next((p for p in PRODUCTS if prod and p.lower() in prod.group(1).lower()), None)
    addons = {a for a in ADDONS if adds and a in adds.group(1).lower()}
    return product, addons


def runs(name):
    """{condition: [run dict]} with the parsed final order, the parsed turn-2 order (chat only) and spend."""
    out = {}
    for cond, rows in load(RAW / f"{name}.csv").items():
        out[cond] = []
        for r in rows:
            cols = sorted((k for k in r if k.startswith("response_")), key=lambda k: int(k.split("_")[1]))
            turns = [r[k] for k in cols if r[k]]
            product, addons = parse(turns[-1])
            t2_product, t2_addons = parse(turns[1]) if len(turns) >= 3 else (None, set())
            own = (PRODUCTS[product] if product else 0) + sum(ADDONS[a] for a in addons)
            out[cond].append({"label": r["label"], "product": product, "addons": addons, "spend": r["rating"],
                              "own": own, "t2_product": t2_product, "t2_addons": t2_addons})
    return out


def count(rs, test):
    return sum(1 for r in rs if test(r))


def frac(k, rs):
    return f"{k}/{len(rs)}"


def halo(r):
    return r["product"] == "Halo"


def aero(r):
    return r["product"] == "Aero"


def both(r):
    return r["addons"] == set(ADDONS)


def has(addon):
    return lambda r: addon in r["addons"]


def fisher_vs(rs, ctl, test):
    return fmt_p(fisher_p(count(rs, test), len(rs), count(ctl, test), len(ctl)))


def welch_vs(rs, ctl):
    a, b = [r["spend"] for r in rs], [r["spend"] for r in ctl]
    return fmt_p(welch_p(a, b)) if len(set(a + b)) > 1 else "n/a (same spend in every run)"


D = {name: runs(name) for name in CALIBRATION + PILOT}
pr, cr, pf, cf = (D[n] for n in PILOT)

print("## Defaults: runs whose final order had both add-ons (p vs control, Fisher exact)\n")
print("| instruction | channel | control | pre-checked / seller adds both | all tricks |")
print("|---|---|---|---|---|")
for instr, page, chat in (("keep it reasonable", pr, cr), ("don't spend more than I need to", pf, cf)):
    for channel, d in (("page", page), ("chat", chat)):
        cells = [frac(count(d[c], both), d[c]) + ("" if c == 1 else f" (p = {fisher_vs(d[c], d[1], both)})")
                 for c in (1, 5, 6)]
        print(f"| {instr} | {channel} | " + " | ".join(cells) + " |")
print()

print("## Calibration: product choice by instruction wording (no tricks, store page)\n")
print("| workbook | wording | runs | Halo | Aero | added protection plan | added express shipping |")
print("|---|---|---|---|---|---|---|")
for name in CALIBRATION:
    for c, rs in D[name].items():
        print(f"| {name} | {rs[0]['label']} | {len(rs)} | {frac(count(rs, halo), rs)} | "
              f"{frac(count(rs, aero), rs)} | {frac(count(rs, has('protection')), rs)} | "
              f"{frac(count(rs, has('express')), rs)} |")
print()


def page_table(d, title):
    ctl = d[1]
    print(f"## Page, {title}\n")
    print("| condition | Halo | p (Halo, Fisher) | kept both add-ons | p (add-ons, Fisher) | mean spend "
          "| delta vs control | p (spend, Welch t) |")
    print("|---|---|---|---|---|---|---|---|")
    for c, rs in d.items():
        ps = ("", "", "", "") if c == 1 else (
            fisher_vs(rs, ctl, halo), fisher_vs(rs, ctl, both),
            f"{mean([r['spend'] for r in rs]) - mean([r['spend'] for r in ctl]):+.2f}", welch_vs(rs, ctl))
        print(f"| {rs[0]['label']} | {frac(count(rs, halo), rs)} | {ps[0]} | {frac(count(rs, both), rs)} | "
              f"{ps[1]} | ${mean([r['spend'] for r in rs]):.2f} | {ps[2]} | {ps[3]} |")
    allruns = [r for rs in d.values() for r in rs]
    print(f"\nRuns that kept exactly one add-on: {count(allruns, lambda r: len(r['addons']) == 1)}/{len(allruns)}. "
          f"Runs that bought the Vega: {count(allruns, lambda r: r['product'] == 'Vega')}/{len(allruns)}. "
          f"Runs that bought the Aero: {count(allruns, aero)}/{len(allruns)}.")
    for c in (5, 6):
        keepers = [r for r in d[c] if both(r)]
        print(f"{d[c][0]['label']}: runs that kept both add-ons: {len(keepers)}, of which "
              f"Aero {count(keepers, aero)}, Halo {count(keepers, halo)}")
    print()


def chat_table(d, title):
    ctl = d[1]
    print(f"## Chat, {title}\n")
    print("| condition | Halo (final) | switched product after turn 2 | protection plan (final) "
          "| express shipping (final) | p (express, Fisher) | mean spend | p (spend, Welch t) |")
    print("|---|---|---|---|---|---|---|---|")
    for c, rs in d.items():
        switched = count(rs, lambda r: r["product"] != r["t2_product"])
        p_exp, p_sp = ("", "") if c == 1 else (fisher_vs(rs, ctl, has("express")), welch_vs(rs, ctl))
        print(f"| {rs[0]['label']} | {frac(count(rs, halo), rs)} | {frac(switched, rs)} | "
              f"{frac(count(rs, has('protection')), rs)} | {frac(count(rs, has('express')), rs)} | {p_exp} | "
              f"${mean([r['spend'] for r in rs]):.2f} | {p_sp} |")
    allruns = [r for rs in d.values() for r in rs]
    switches = [f"{r['t2_product']} -> {r['product']} ({r['label']})" for r in allruns
                if r["product"] != r["t2_product"]]
    print(f"\nProduct switches after turn 2: {', '.join(switches) or 'none'}")
    t2 = lambda r: "protection" in r["t2_addons"]  # noqa: E731
    print(f"Turn 2 is the same prompt in every condition. Chose the protection plan at turn 2: "
          f"{count(allruns, t2)}/{len(allruns)} overall; by condition "
          + ", ".join(frac(count(rs, t2), rs) for rs in d.values()))
    for c in (5, 6):
        rs = d[c]
        had = [r for r in rs if t2(r)]
        none = [r for r in rs if not r["t2_addons"]]
        print(f"{rs[0]['label']}: final order had both add-ons in {frac(count(rs, both), rs)}: "
              f"{frac(count(had, both), had)} of agents that chose the protection plan at turn 2, "
              f"{frac(count(none, both), none)} of agents that chose no add-ons at turn 2")
    ps = [welch_p([r["spend"] for r in rs], [r["spend"] for r in ctl]) for c, rs in d.items() if c != 1]
    print(f"Smallest spend p vs control (Welch t): {fmt_p(min(ps))}")
    print()


page_table(pr, '"keep it reasonable"')
chat_table(cr, '"keep it reasonable"')
page_table(pf, "\"don't spend more than I need to\"")
chat_table(cf, "\"don't spend more than I need to\"")

print("## Cross-workbook comparison (a hypothesis, not a controlled contrast)\n")
print(f'"Keep it reasonable", no trick: Halo on the page {frac(count(pr[1], halo), pr[1])}, '
      f"in the chat {frac(count(cr[1], halo), cr[1])}, Fisher p = {fisher_vs(cr[1], pr[1], halo)}")
same = D["shopping_calibration2"][2]
print(f'The same "keep it reasonable" page prompt in the calibration: Halo {frac(count(same, halo), same)}, '
      f"added protection plan {frac(count(same, has('protection')), same)}, "
      f"added express shipping {frac(count(same, has('express')), same)}\n")

print("## Grader check\n")
for name, d in D.items():
    allruns = [r for rs in d.values() for r in rs]
    bad = count(allruns, lambda r: abs(r["own"] - r["spend"]) > 0.005)
    unparsed = count(allruns, lambda r: r["product"] is None)
    print(f"{name}: {len(allruns)} runs, date {load(RAW / f'{name}.csv')[1][0]['date']}; grader total differs "
          f"from the price list in {bad}; final turn without a recognised product in {unparsed}")


def aibo_cost(name):
    """Sum of the 'Cost' row on the Analysis Data sheet of raw/<name>-analysis_results.xlsx (model + grader calls)."""
    wb = openpyxl.load_workbook(RAW / f"{name}-analysis_results.xlsx", read_only=True, data_only=True)
    row = next(r for r in wb["Analysis Data"].iter_rows(values_only=True) if r and r[0] == "Cost")
    return sum(Decimal(str(c)) for c in row[1:] if c not in (None, ""))


def dollars(x):
    return f"${x.quantize(Decimal('0.001'), rounding=ROUND_HALF_UP)}"


print("\n## Cost recorded by AIBO (includes grader calls)\n")
costs = {name: aibo_cost(name) for name in CALIBRATION + PILOT}
for name, c in costs.items():
    print(f"{name}: ${c}")
cal, pilot = sum(costs[n] for n in CALIBRATION), sum(costs[n] for n in PILOT)
print(f"Calibration (70 runs): {dollars(cal)}. Pilot (240 runs): {dollars(pilot)}. All 310 runs: {dollars(cal + pilot)}")
