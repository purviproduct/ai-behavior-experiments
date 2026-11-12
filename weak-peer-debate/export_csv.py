"""Build the CSVs in raw/ from the JSON outputs. Numbers only; the full transcripts stay in the JSON.

    python weak-peer-debate/export_csv.py

raw/weak_peer_pilot.csv        one row per debate: item, arm, trial, A's answer each round, B's number, WOA
raw/weak_peer_calibration.csv  one row per solo calibration answer: round, model, item, rep, answer

WOA (weight of advice) uses the script's own woa() and clip(), so the CSV matches what analyze reports.
No model calls; does not need AIBO.
"""
import csv
import json
from pathlib import Path

from weak_peer import clip, rel_err, woa

RAW = Path(__file__).resolve().parent / "raw"
PILOT = "weak_peer_pilot_20261109T231832Z.json"
CALIBRATIONS = {1: "weak_peer_calibration_20261109T230430Z.json",  # round 1: 18 well-known facts
                2: "weak_peer_calibration_20261109T231018Z.json"}  # round 2: 21 harder items (the pilot's B posts)


def num(x):
    return "" if x is None else x


def r4(x):
    """A derived measure rounded to 4 decimals ("" if missing; -0.0 shown as 0.0)."""
    return "" if x is None else round(x, 4) + 0.0


def pilot_rows() -> list[dict]:
    data = json.loads((RAW / PILOT).read_text(encoding="utf-8"))
    groups = data["meta"]["groups"]
    rows = []
    for t in data["trials"]:
        r1, final = t["values"][0], t["values"][3]
        w = [woa(r1, t["values"][k], t["p"]) for k in (1, 2, 3)]
        rows.append({
            "item": t["item"],
            "group": groups[t["item"]],  # "unsure" or "knows", from A's calibration answers
            "arm": t["arm"],
            "trial": t["trial"],
            "truth": t["truth"],
            "b_number": t["p"],  # B's number; control trials have one too but never see it
            "a_r1": num(r1), "a_r2": num(t["values"][1]), "a_r3": num(t["values"][2]), "a_r4_final": num(final),
            # clipped to [-0.5, 1.5] as in the analysis; blank when B's number is within 5% of A's R1
            "woa_r2": r4(w[0] if w[0] is None else clip(w[0])),
            "woa_r3": r4(w[1] if w[1] is None else clip(w[1])),
            "woa_r4_final": r4(w[2] if w[2] is None else clip(w[2])),
            "woa_r4_final_unclipped": r4(w[2]),
            "rel_err_r1": r4(rel_err(r1, t["truth"])),
            "rel_err_r4_final": r4(rel_err(final, t["truth"])),
            "final_less_accurate_than_r1": int(rel_err(final, t["truth"]) > rel_err(r1, t["truth"]) + 0.01),
            "cost_usd": t["cost"],
        })
    return rows


def calibration_rows() -> list[dict]:
    rows = []
    for rnd, name in CALIBRATIONS.items():
        for r in json.loads((RAW / name).read_text(encoding="utf-8"))["rows"]:
            rows.append({"calibration_round": rnd, "model": r["model"], "item": r["item"], "rep": r["rep"],
                         "truth": r["truth"], "answer": num(r["value"]),
                         "rel_err": "" if r["value"] is None else r4(rel_err(r["value"], r["truth"])), "cost_usd": r["cost"]})
    return rows


def write(path: Path, rows: list[dict]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print(f"wrote {path.name}: {len(rows)} rows")


if __name__ == "__main__":
    write(RAW / "weak_peer_pilot.csv", pilot_rows())
    write(RAW / "weak_peer_calibration.csv", calibration_rows())
