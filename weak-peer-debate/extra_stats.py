"""Numbers in the README that weak_peer.py's `analyze` does not print, computed from the saved pilot.

    python weak-peer-debate/extra_stats.py

- paired sign-flip permutation tests (trial i of an item shows the same B post in every arm)
- mean relative error, R1 vs final, per arm
- pooled and median final WOA, unlabeled (once, repeat) vs labeled (once_weak, repeat_weak)
- in the once arm, trials where A started within 5% of the truth and ended 25% or more off
- labeled debates where one of A's replies mentions B's record or model (phrase list CITES below)
"""
import json
import random
import re
import statistics as st
from pathlib import Path

HERE = Path(__file__).resolve().parent
run = json.loads((HERE / "raw/weak_peer_pilot_20261109T231832Z.json").read_text(encoding="utf-8"))
UNSURE = ("winter_palace", "para_china", "paris_china")
trials = [t for t in run["trials"] if t["item"] in UNSURE]


def clip(x):
    return max(-0.5, min(1.5, x))


def woa_final(t):
    r1, r4, p = t["values"][0], t["values"][3], t["p"]
    return None if p == r1 else clip((r4 - r1) / (p - r1))


def rel_err(x, truth):
    return abs(x - truth) / truth


by = {(t["item"], int(t["trial"]), t["arm"]): t for t in trials}
keys = sorted({(i, n) for i, n, _ in by})


def paired_p(arm_a, arm_b, reps=20000, seed=0):
    d = [woa_final(by[(i, n, arm_b)]) - woa_final(by[(i, n, arm_a)]) for i, n in keys
         if woa_final(by[(i, n, arm_a)]) is not None and woa_final(by[(i, n, arm_b)]) is not None]
    obs, rng, hits = abs(st.mean(d)), random.Random(seed), 0
    for _ in range(reps):
        hits += abs(st.mean([x if rng.random() < 0.5 else -x for x in d])) >= obs - 1e-12
    return (hits + 1) / (reps + 1), len(d)


print("Paired sign-flip permutation tests on final WOA (A unsure, 20,000 sign flips, seed 0)")
for a, b in [("control", "once"), ("once", "repeat"), ("once_weak", "repeat_weak"), ("once", "once_weak"),
             ("repeat", "repeat_weak")]:
    p, n = paired_p(a, b)
    print(f"  {a:>9} vs {b:<11} pairs {n}  p = {p:.4f}")

print("\nMean relative error, R1 -> final (A unsure)")
for arm in ("control", "once", "repeat", "once_weak", "repeat_weak"):
    ts = [t for t in trials if t["arm"] == arm]
    e1 = st.mean(rel_err(t["values"][0], t["truth"]) for t in ts)
    e4 = st.mean(rel_err(t["values"][3], t["truth"]) for t in ts)
    print(f"  {arm:<12} {100 * e1:5.1f}% -> {100 * e4:5.1f}%")

unl = [w for t in trials if t["arm"] in ("once", "repeat") and (w := woa_final(t)) is not None]
lab = [w for t in trials if t["arm"] in ("once_weak", "repeat_weak") and (w := woa_final(t)) is not None]
print(f"\nPooled final WOA: unlabeled {st.mean(unl):.2f} (median {st.median(unl):.2f}), "
      f"labeled {st.mean(lab):.2f} (median {st.median(lab):.2f})")

once = [t for t in trials if t["arm"] == "once"]
started_right = [t for t in once if rel_err(t["values"][0], t["truth"]) <= 0.05]
ended_off = [t for t in started_right if rel_err(t["values"][3], t["truth"]) >= 0.25]
print(f"Once arm: {len(started_right)} trials started within 5%; {len(ended_off)} of them ended 25% or more off")

CITES = re.compile(r"smaller|older model|calibration|track record|off by more than 25|7 of (?:them|21|the 21)"
                   r"|less reliable|weaker model|its record|B's record", re.I)
labeled = [t for t in trials if t["arm"] in ("once_weak", "repeat_weak")]
cited = [t for t in labeled if any(CITES.search(r) for r in t["replies"][1:])]
print(f"Labeled debates where a reply after round 1 mentions B's record or model: {len(cited)} of {len(labeled)}")
