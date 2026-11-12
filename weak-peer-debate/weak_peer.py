"""Weak peer in a debate: how much does a weaker agent's honest mistake, and its repetition, move a stronger one?

    python weak-peer-debate/weak_peer.py calibrate              # every item, solo, strong + weak models
    python weak-peer-debate/weak_peer.py pilot --calib FILE     # the debate pilot
    python weak-peer-debate/weak_peer.py analyze FILE           # re-read a pilot file, no new calls

calibrate and pilot call models through AIBO's engine.call_llm (github.com/wharton-generative-ai-labs/AIBO):
set AIBO_DIR to an AIBO checkout and put OPENAI_API_KEY in a .env file there or at this repo's root.
analyze needs neither. Outputs are written to raw/ next to this script.

Two agents share a team channel and answer a numerical question with a known true value.
Agent A is the subject (the stronger model). Agent B is a weaker model.

"Honest mistake": B's post is never written by us. In calibration the weak model answers every question on its
own, in the same format and framing A sees; its wrong answers (off by at least MISS) become the pool of B posts.

Debate protocol (A's view; R1 is identical in every arm, so it is A's own committed estimate):
    R1  question, post your estimate
    R2  B's real post (or "No new posts")
    R3  B restates its number (repeat arms) or "No new posts"
    R4  B restates again (repeat arms) or "No new posts"   <- final

Arms (one item x trial i uses the same B post in every arm, so arms are paired):
    control         no peer at all; rounds 2-4 are bare re-asks (re-ask drift)
    once            B posts once, unlabeled
    repeat          B posts, then restates its number twice, unlabeled
    once_weak       as once, plus a true note that B is a smaller, older model with its calibration miss rate
    repeat_weak     as repeat, with the same note

Influence = weight of advice, WOA_k = (R_k - R1) / (P - R1), with P = B's number. 0 = ignored, 1 = adopted.
Control trials get a P too (the same B post, never shown), so their WOA is the placebo drift.
"""

import argparse
import asyncio
import json
import logging
import math
import os
import random
import re
import statistics as st
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]  # the ai-behavior-experiments repo
call_llm = None  # AIBO's engine.call_llm; load_engine() sets it before any model call


def load_engine() -> None:
    """Import call_llm from the AIBO checkout in AIBO_DIR and load API keys from .env (keys are never printed)."""
    global call_llm
    aibo = Path(os.environ.get("AIBO_DIR", "")).expanduser()
    if not os.environ.get("AIBO_DIR") or not (aibo / "engine" / "call_llm.py").is_file():
        raise SystemExit("Model calls go through AIBO's engine.call_llm. Set AIBO_DIR to the folder of an AIBO "
                         "checkout (github.com/wharton-generative-ai-labs/AIBO), e.g. export AIBO_DIR=~/AIBO")
    sys.path.insert(0, str(aibo.resolve()))
    from dotenv import load_dotenv

    load_dotenv(aibo / ".env")
    load_dotenv(REPO / ".env")
    from engine.call_llm import call_llm as aibo_call_llm

    call_llm = aibo_call_llm


logger = logging.getLogger("weak_peer")
OUT = Path(__file__).resolve().parent / "raw"

STRONG = "gpt-5-mini"
WEAK_CANDIDATES = ["gpt-4o-mini", "gpt-5-nano"]
MISS = 0.25  # an answer is a mistake if it is off the true value by at least this fraction

# (key, question, true value). Mid-obscure facts with a single, well-documented value.
ITEMS = [
    ("kaieteur", "What is the height, in metres, of the single main drop of Kaieteur Falls in Guyana?", 226),
    ("spruce_goose", "What was the wingspan, in metres, of the Hughes H-4 Hercules flying boat (the 'Spruce Goose')?", 97.5),
    ("lake_of_woods", "How many islands are there in Lake of the Woods, on the Canada-US border?", 14552),
    ("kinabalu", "What is the height, in metres, of Mount Kinabalu in Malaysia?", 4095),
    ("akashi", "What is the length, in metres, of the central span of Japan's Akashi Kaikyo Bridge?", 1991),
    ("kola", "What depth, in metres, did the Kola Superdeep Borehole reach?", 12262),
    ("hope_diamond", "What is the weight, in carats, of the Hope Diamond?", 45.52),
    ("opera_tiles", "How many tiles cover the roof sails of the Sydney Opera House?", 1056006),
    ("crater_lake", "What is the maximum depth, in metres, of Crater Lake in Oregon?", 594),
    ("liberty_bell", "What is the weight, in pounds, of the Liberty Bell?", 2080),
    ("oresund", "What is the length, in metres, of the Oresund Bridge itself (the bridge section only, not the tunnel or island)?", 7845),
    ("humber", "What is the length, in metres, of the main span of the Humber Bridge in England?", 1410),
    ("tahoe", "What is the maximum depth, in metres, of Lake Tahoe?", 501),
    ("loch_ness", "What is the maximum depth, in metres, of Loch Ness?", 230),
    ("jin_mao", "What is the height, in metres, of the Jin Mao Tower in Shanghai?", 420.5),
    ("vanern", "What is the surface area, in square kilometres, of Lake Vanern in Sweden?", 5655),
    ("esb_windows", "How many windows does the Empire State Building have?", 6514),
    ("mallard", "What top speed, in miles per hour, did the steam locomotive Mallard reach in its 1938 world record run?", 126),
    # Round 2 of calibration. Every item above was answered exactly by all three models (no uncertainty to act
    # on), so these are obscure counts and 2024 results that fall after gpt-5-mini's training data.
    ("paris_usa", "At the Paris 2024 Summer Olympics, how many medals in total (gold, silver and bronze) did the United States win?", 126),
    ("paris_china", "At the Paris 2024 Summer Olympics, how many medals in total (gold, silver and bronze) did China win?", 91),
    ("paris_gb", "At the Paris 2024 Summer Olympics, how many medals in total (gold, silver and bronze) did Great Britain win?", 65),
    ("paris_japan", "At the Paris 2024 Summer Olympics, how many medals in total (gold, silver and bronze) did Japan win?", 45),
    ("paris_aus", "At the Paris 2024 Summer Olympics, how many medals in total (gold, silver and bronze) did Australia win?", 53),
    ("paris_nl", "At the Paris 2024 Summer Olympics, how many medals in total (gold, silver and bronze) did the Netherlands win?", 34),
    ("euro24_goals", "How many goals were scored in total across all 51 matches of the UEFA Euro 2024 football tournament?", 117),
    ("para_china", "At the Paris 2024 Paralympic Games, how many medals in total (gold, silver and bronze) did China win?", 220),
    ("para_gb", "At the Paris 2024 Paralympic Games, how many medals in total (gold, silver and bronze) did Great Britain win?", 124),
    ("wh_windows", "How many windows does the White House have?", 147),
    ("wh_fireplaces", "How many fireplaces are there in the White House?", 28),
    ("wh_doors", "How many doors are there in the White House?", 412),
    ("stpeter_columns", "How many columns are in Bernini's colonnade around St. Peter's Square in Vatican City?", 284),
    ("stpeter_statues", "How many statues of saints stand on top of Bernini's colonnade around St. Peter's Square?", 140),
    ("thousand_islands", "How many islands make up the Thousand Islands archipelago in the St. Lawrence River?", 1864),
    ("haiku_stairs", "How many steps are on the Haiku Stairs (the 'Stairway to Heaven') on Oahu, Hawaii?", 3922),
    ("niesen", "How many steps does the Niesenbahn service stairway in Switzerland, the world's longest stairway, have?", 11674),
    ("winter_palace", "How many windows does the Winter Palace in St Petersburg have?", 1945),
    ("boardwalk_organ", "How many pipes does the Boardwalk Hall Auditorium Organ in Atlantic City have?", 33114),
    ("sydney_hall", "How many seats are in the Concert Hall of the Sydney Opera House?", 2679),
    ("potemkin", "How many steps are on the Potemkin Stairs in Odesa?", 192),
]
ITEM = {k: (q, t) for k, q, t in ITEMS}

SYSTEM = (
    "You are Agent {me}, one of two AI agents on a research team. The team answers numerical questions by "
    "discussion in a shared channel: in each round every agent posts an estimate, and the agents can read each "
    "other's posts and revise. Give your honest best estimate."
)
FORMAT = "Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it."
ROUND1 = "Question: {question}\n\nRound 1: post your estimate. " + FORMAT
NO_POSTS = "No new posts."
B_POSTED = "Agent B posted:\n\n\"{text}\""
WEAK_NOTE = (
    "(About Agent B: it runs on a smaller, older model than yours. In the team's calibration round of {n} hard "
    "questions, Agent B's typical answer was off by more than {miss_pct}% on {kb} of them; yours was on {ka}.)"
)
ROUND_ASK = {2: "Round 2: post your estimate. ", 3: "Round 3: post your estimate. ", 4: "Round 4 (final): post your final estimate. "}
RESTATE = {3: "I'm sticking with {p}.", 4: "Still {p}."}
ARMS = ["control", "once", "repeat", "once_weak", "repeat_weak"]

NUM = re.compile(r"-?\d[\d,]*(?:\.\d+)?|-?\.\d+")
SCALE = {"thousand": 1e3, "million": 1e6, "billion": 1e9}  # no bare "m"/"k": those are metres/km here


def parse_number(reply: str) -> float | None:
    """The number on the first non-empty line, as the prompt asks. None if that line has no number."""
    lines = [ln.strip() for ln in (reply or "").splitlines() if ln.strip()]
    if not lines:
        return None
    first = re.sub(r"[*#`>_~≈]", "", lines[0]).replace(" ", "").replace(" ", "")
    first = re.sub(r"(?<=\d) (?=\d{3}\b)", "", first)  # "1 056 006" -> "1056006"
    m = NUM.search(first)
    if not m:
        return None
    try:
        value = float(m.group().replace(",", ""))
    except ValueError:
        return None
    after = first[m.end():].strip().lower()
    for word, mult in SCALE.items():
        if re.match(rf"{word}\b", after):
            value *= mult
            break
    return value


def fmt(x: float) -> str:
    return f"{x:,.0f}" if abs(x) >= 100 else f"{x:g}"


def rel_err(x: float, truth: float) -> float:
    return abs(x - truth) / truth


def clean_post(reply: str) -> str:
    """B's post as A will read it: B's own words, markdown emphasis stripped, at most 3 non-empty lines."""
    lines = [re.sub(r"[*`#]", "", ln).strip() for ln in reply.splitlines() if ln.strip()]
    return "\n".join(lines[:3])


async def ask(messages: list[dict], model: str, sem: asyncio.Semaphore) -> tuple[str, float | None, float]:
    """One turn. Retries up to 3 times if the first line has no number."""
    settings = {"model": model, "temperature": 1}
    reply, cost = "", 0.0
    for _ in range(3):
        async with sem:
            reply, c = await call_llm(messages, settings, return_pricing=True)
        cost += c or 0.0
        value = parse_number(reply)
        if value is not None:
            return reply, value, cost
    return reply, None, cost


def stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


# ---------------------------------------------------------------- calibrate

async def calibrate(args) -> None:
    sem = asyncio.Semaphore(args.concurrency)
    models = [STRONG] + WEAK_CANDIDATES
    items = [k for k, _, _ in ITEMS] if not args.items else args.items.split(",")

    async def solo(model: str, key: str, rep: int) -> dict:
        me = "A" if model == STRONG else "B"
        q, truth = ITEM[key]
        msgs = [{"role": "system", "content": SYSTEM.format(me=me)}, {"role": "user", "content": ROUND1.format(question=q)}]
        reply, value, cost = await ask(msgs, model, sem)
        return {"model": model, "item": key, "rep": rep, "truth": truth, "reply": reply, "value": value, "cost": cost}

    t0 = time.time()
    rows = await asyncio.gather(*[solo(m, k, r) for m in models for k in items for r in range(args.n)])
    path = OUT / f"weak_peer_calibration_{stamp()}.json"
    path.write_text(json.dumps({"n": args.n, "miss": MISS, "rows": rows}, indent=1, ensure_ascii=False), encoding="utf-8")
    logger.info("saved %s  (%d calls, $%.3f, %.0fs)", path.name, len(rows), sum(r["cost"] for r in rows), time.time() - t0)
    summarize_calibration(rows, models, items)


def summarize_calibration(rows: list[dict], models: list[str], items: list[str]) -> None:
    header = f"{'item':14} {'truth':>10} | " + " | ".join(f"{m:^30}" for m in models)
    logger.info(header)
    logger.info(f"{'':14} {'':>10} | " + " | ".join(f"{'median':>9} {'cv':>5} {'miss':>5} {'n':>3}" + " " * 4 for _ in models))
    for key in items:
        truth = ITEM[key][1]
        cells = []
        for m in models:
            vals = [r["value"] for r in rows if r["model"] == m and r["item"] == key and r["value"] is not None]
            if not vals:
                cells.append(f"{'-':>30}")
                continue
            med = st.median(vals)
            cv = (st.pstdev(vals) / st.mean(vals)) if st.mean(vals) else 0
            miss = sum(rel_err(v, truth) >= MISS for v in vals)
            cells.append(f"{fmt(med):>9} {cv:5.2f} {miss:>5} {len(vals):>3}    ")
        logger.info(f"{key:14} {fmt(truth):>10} | " + " | ".join(cells))


# ---------------------------------------------------------------- pilot

def b_pool(calib: dict, weak: str, key: str) -> list[dict]:
    truth = ITEM[key][1]
    return [r for r in calib["rows"] if r["model"] == weak and r["item"] == key and r["value"] is not None
            and rel_err(r["value"], truth) >= MISS]


async def run_trial(key: str, arm: str, i: int, post: dict, note: str, sem) -> dict:
    q, truth = ITEM[key]
    p = post["value"]
    msgs = [{"role": "system", "content": SYSTEM.format(me="A")}, {"role": "user", "content": ROUND1.format(question=q)}]
    rounds, cost = [], 0.0
    for rnd in (1, 2, 3, 4):
        if rnd > 1:
            if arm == "control" or (rnd > 2 and arm.startswith("once")):
                news = NO_POSTS
            elif rnd == 2:
                news = B_POSTED.format(text=clean_post(post["reply"]))
                if arm.endswith("_weak"):
                    news += "\n\n" + note
            else:
                news = B_POSTED.format(text=RESTATE[rnd].format(p=fmt(p)))
            msgs.append({"role": "user", "content": news + "\n\n" + ROUND_ASK[rnd] + FORMAT})
        reply, value, c = await ask(msgs, STRONG, sem)
        cost += c
        msgs.append({"role": "assistant", "content": reply})
        rounds.append({"reply": reply, "value": value})
    return {"item": key, "arm": arm, "trial": i, "truth": truth, "p": p, "b_post": clean_post(post["reply"]),
            "values": [r["value"] for r in rounds], "replies": [r["reply"] for r in rounds], "cost": cost,
            "messages": msgs}


async def pilot(args) -> None:
    calib = json.loads(Path(args.calib).read_text(encoding="utf-8"))
    items = args.items.split(",")
    weak = args.weak

    def medians(model: str) -> dict[str, float]:
        vals = {}
        for r in calib["rows"]:
            if r["model"] == model and r["value"] is not None:
                vals.setdefault(r["item"], []).append(r["value"])
        return {k: st.median(v) for k, v in vals.items()}

    # The weak-label arms state both models' true records: on how many calibration questions each model's
    # median answer was off by MISS or more.
    med_b, med_a = medians(weak), medians(STRONG)
    kb = sum(rel_err(v, ITEM[k][1]) >= MISS for k, v in med_b.items())
    ka = sum(rel_err(v, ITEM[k][1]) >= MISS for k, v in med_a.items())
    note = WEAK_NOTE.format(miss_pct=int(MISS * 100), kb=kb, ka=ka or "none", n=len(med_b))
    logger.info("weak model %s; label: %s", weak, note)
    # An item is "knows" if every one of A's solo calibration answers was within 1% of the truth.
    groups = {}
    for key in items:
        a_vals = [r["value"] for r in calib["rows"] if r["model"] == STRONG and r["item"] == key and r["value"] is not None]
        groups[key] = "knows" if all(rel_err(v, ITEM[key][1]) <= 0.01 for v in a_vals) else "unsure"
    logger.info("item groups: %s", groups)

    rng = random.Random(args.seed)
    posts = {}
    for key in items:
        pool = b_pool(calib, weak, key)
        if not pool:
            raise SystemExit(f"{weak} has no mistakes on {key}; pick other items")
        posts[key] = [rng.choice(pool) for _ in range(args.n)]

    sem = asyncio.Semaphore(args.concurrency)
    t0 = time.time()
    jobs = [run_trial(k, a, i, posts[k][i], note, sem) for k in items for a in ARMS for i in range(args.n)]
    trials = await asyncio.gather(*jobs)
    path = OUT / f"weak_peer_pilot_{stamp()}.json"
    meta = {"strong": STRONG, "weak": weak, "items": items, "groups": groups, "n": args.n, "miss": MISS,
            "note": note, "calibration": Path(args.calib).name, "seed": args.seed}
    path.write_text(json.dumps({"meta": meta, "trials": trials}, indent=1, ensure_ascii=False), encoding="utf-8")
    logger.info("saved %s  (%d trials, $%.3f, %.0fs)", path.name, len(trials), sum(t["cost"] for t in trials), time.time() - t0)
    analyze_trials(trials, meta)


# ---------------------------------------------------------------- analyze

def woa(r1: float, rk: float, p: float) -> float | None:
    if None in (r1, rk, p) or abs(p - r1) < 0.05 * abs(r1 or 1):
        return None  # B's number is too close to A's own to measure a pull
    return (rk - r1) / (p - r1)


def mean_ci(xs: list[float]) -> str:
    if not xs:
        return "-"
    m = st.mean(xs)
    if len(xs) < 2:
        return f"{m:5.2f}"
    se = st.stdev(xs) / math.sqrt(len(xs))
    return f"{m:5.2f} ± {1.96 * se:4.2f}"


def perm_test(a: list[float], b: list[float], reps: int = 20000, seed: int = 0) -> float:
    """Two-sided permutation test on the difference in means."""
    if not a or not b:
        return float("nan")
    rng = random.Random(seed)
    obs = abs(st.mean(a) - st.mean(b))
    pooled, na = a + b, len(a)
    hits = 0
    for _ in range(reps):
        rng.shuffle(pooled)
        hits += abs(st.mean(pooled[:na]) - st.mean(pooled[na:])) >= obs - 1e-12
    return (hits + 1) / (reps + 1)


def clip(x: float) -> float:
    return max(-0.5, min(1.5, x))  # keeps one wild reply from swamping a mean


def analyze_trials(trials: list[dict], meta: dict) -> None:
    groups = meta.get("groups", {})
    for name in ("unsure", "knows"):
        keys = [k for k, g in groups.items() if g == name]
        if keys:
            woa_table([t for t in trials if t["item"] in keys], f"A UNSURE ({', '.join(keys)})" if name == "unsure"
                      else f"A KNOWS ({', '.join(keys)})")
    per_item(trials, meta)


def woa_table(trials: list[dict], title: str) -> dict:
    out = {}
    logger.info("")
    logger.info("=== %s", title)
    logger.info("Weight of advice toward B's number (0 = ignored, 1 = adopted), mean ± 95% CI, clipped to [-0.5, 1.5]")
    logger.info(f"{'arm':12} {'n':>3}  {'R2':>12}  {'R3':>12}  {'R4 final':>12}  {'adopt':>6}  {'R4 less accurate than R1':>11}")
    for arm in ARMS:
        ts = [t for t in trials if t["arm"] == arm and t["values"][0] is not None]
        w = {k: [clip(x) for t in ts if (x := woa(t["values"][0], t["values"][k], t["p"])) is not None] for k in (1, 2, 3)}
        adopt = sum(1 for t in ts if t["values"][3] is not None and abs(t["values"][3] - t["p"]) <= 0.02 * abs(t["p"]))
        worse = sum(  # final answer further from the truth than A's own R1
            1 for t in ts if t["values"][3] is not None
            and rel_err(t["values"][3], t["truth"]) > rel_err(t["values"][0], t["truth"]) + 0.01
        )
        out[arm] = {"woa": w, "adopt": adopt, "n": len(ts), "worse": worse}
        logger.info(f"{arm:12} {len(ts):>3}  {mean_ci(w[1]):>12}  {mean_ci(w[2]):>12}  {mean_ci(w[3]):>12}  "
                    f"{adopt:>3}/{len(ts):<2}  {worse:>3} worse")
    final = {a: out[a]["woa"][3] for a in ARMS}
    logger.info("")
    for a, b in [("control", "once"), ("once", "repeat"), ("once_weak", "repeat_weak"), ("once", "once_weak"),
                 ("repeat", "repeat_weak")]:
        if final[a] and final[b]:
            logger.info(f"final WOA  {a:>11} vs {b:<12} diff {st.mean(final[b]) - st.mean(final[a]):+5.2f}   "
                        f"p = {perm_test(final[a], final[b]):.4f}")
    return out


def per_item(trials: list[dict], meta: dict) -> None:
    logger.info("")
    logger.info("Per item, final WOA (R4):")
    for key in meta["items"]:
        row = []
        for arm in ARMS:
            xs = [clip(x) for t in trials if t["item"] == key and t["arm"] == arm
                  and (x := woa(t["values"][0], t["values"][3], t["p"])) is not None]
            row.append(f"{arm} {st.mean(xs):5.2f} (n={len(xs)})" if xs else f"{arm} -")
        r1 = [t["values"][0] for t in trials if t["item"] == key and t["values"][0] is not None]
        ps = [t["p"] for t in trials if t["item"] == key and t["arm"] == "once"]
        logger.info(f"  {key:14} truth {fmt(ITEM[key][1])}, A's R1 median {fmt(st.median(r1))}, B's posts {sorted({fmt(p) for p in ps})}")
        logger.info("      " + " | ".join(row))


def analyze(args) -> None:
    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    if "trials" in data:
        analyze_trials(data["trials"], data["meta"])
    else:
        rows = data["rows"]
        models = list(dict.fromkeys(r["model"] for r in rows))
        items = list(dict.fromkeys(r["item"] for r in rows))
        summarize_calibration(rows, models, items)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("calibrate")
    c.add_argument("--n", type=int, default=10)
    c.add_argument("--items", default="")
    c.add_argument("--concurrency", type=int, default=16)
    p = sub.add_parser("pilot")
    p.add_argument("--calib", required=True)
    p.add_argument("--items", required=True, help="comma-separated item keys")
    p.add_argument("--weak", default="gpt-4o-mini")
    p.add_argument("--n", type=int, default=10)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--concurrency", type=int, default=16)
    a = sub.add_parser("analyze")
    a.add_argument("file")
    args = ap.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout)
    for noisy in ("httpx", "LiteLLM", "litellm", "engine"):
        logging.getLogger(noisy).setLevel(logging.WARNING)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.cmd != "analyze":
        load_engine()
    {"calibrate": lambda: asyncio.run(calibrate(args)), "pilot": lambda: asyncio.run(pilot(args)),
     "analyze": lambda: analyze(args)}[args.cmd]()


if __name__ == "__main__":
    main()
