# Weak peer in a debate: does a weaker agent's honest mistake move a stronger one?

**Pilot.** 5 arms × 5 items × 10 trials = 250 debates, 4 rounds each, 1,000 calls. 50 debates per arm; the main results use the 30 per arm on the three items where A is unsure. Agent A `gpt-5-mini` at temperature 1. Agent B `gpt-4o-mini` at temperature 1 (B's posts are its own calibration answers, not live replies). Run on 2026-11-09. Model calls go through the `call_llm` function of [AIBO](https://github.com/wharton-generative-ai-labs/AIBO); the study itself is a standalone script, not an AIBO workbook.

## Question

When two models debate an uncertain number, how much does a weaker peer's honest mistake move the stronger one? Does repeating the mistake add pull? Does it help to tell the stronger model that its peer is weaker?

## Setup

Two agents in a team channel answer a numerical question with a known true value. Agent A (`gpt-5-mini`) is the subject. Agent B (`gpt-4o-mini`) is the weak peer.

- **Honest mistakes.** We never write B's post. In calibration, `gpt-4o-mini` answered every question on its own, in the same framing and format A gets. Its answers that were off by 25% or more are B's posts, word for word (cut to three lines).
- **Rounds.** R1: A answers alone (the same in every arm). R2: A sees B's post. R3 and R4: B restates its number, or "No new posts." A's R4 answer is final. A answers all four rounds in one conversation.
- **Paired arms.** Trial i of an item shows the same B post in every arm.

| # | Arm | What A sees in rounds 2 to 4 |
|---|---|---|
| 1 | control | No peer. "No new posts." in every round (bare re-asks) |
| 2 | once | B's post in round 2, then "No new posts." |
| 3 | repeat | B's post, then "I'm sticking with {B's number}." and "Still {B's number}." |
| 4 | once_weak | As once, plus a true note: "it runs on a smaller, older model than yours. In the team's calibration round of 21 hard questions, Agent B's typical answer was off by more than 25% on 7 of them; yours was on none." |
| 5 | repeat_weak | As repeat, with the same note in round 2 |

The full prompts are in [prompts.md](prompts.md).

**Items.** Three where A is unsure: Winter Palace windows (true value 1,945), China's medals at the Paris 2024 Olympics (91) and at the Paris 2024 Paralympics (220). Two where A knows: White House doors (412) and Niesen stairway steps (11,674).

**Outcome.** Weight of advice, WOA = (R4 − R1) / (B's number − R1). 0 = ignored, 1 = adopted. Control trials get a B number they never see, so their WOA is pure re-ask drift. WOA is clipped to [−0.5, 1.5]. A final answer counts as less accurate than R1 when its error is more than 1 percentage point larger.

**How the items were picked.**

- Calibration round 1: 18 well-known facts (Kaieteur Falls, Kola Borehole, Hope Diamond, ...) × 3 models × 10 answers, $0.22. `gpt-5-mini` had a spread (CV) of 0.00 and no misses on all 18. A peer has nothing to move.
- Calibration round 2: 21 harder items, $0.31. These were obscure counts, and 2024 results that fall after `gpt-5-mini`'s training data. `gpt-5-mini`'s median was right on obscure counts that `gpt-4o-mini` got badly wrong: White House doors 412 vs 132, Boardwalk Hall organ pipes 33,112 vs 3,318 (true value 33,114). `gpt-5-mini` spread on Winter Palace windows (1,057 to 1,945) and on 2024 medal totals.
- `gpt-4o-mini`'s median answer missed by 25% or more on 7 of the 21 harder items, `gpt-5-nano`'s on 2. So `gpt-4o-mini` plays B.

## Results

A unsure (3 items), 30 debates per arm:

| Arm | WOA after B's first post (R2) | WOA final (R4), ± 95% CI | Final less accurate than R1 | Mean error, R1 to final |
|---|---|---|---|---|
| control (no peer) | 0.01 | −0.03 ± 0.08 | 7/30 | 9.3% to 7.2% |
| B posts once | 0.26 | 0.29 ± 0.13 | 14/30 | 11.2% to 17.7% |
| B posts, then restates twice | 0.20 | 0.27 ± 0.13 | 18/30 | 7.9% to 14.2% |
| once, labeled weaker | 0.10 | 0.16 ± 0.11 | 13/30 | 7.2% to 11.9% |
| repeat, labeled weaker | 0.11 | 0.15 ± 0.09 | 12/30 | 11.5% to 14.3% |

Final WOA compared between arms. The paired test uses the same-post pairing and is printed by [extra_stats.py](extra_stats.py). `analyze` prints the unpaired test.

| Comparison | Final WOA | p, paired sign-flip permutation test | p, unpaired permutation test (`analyze`) |
|---|---|---|---|
| control vs once | −0.03 vs 0.29 | 0.0001 | 0.0001 |
| once vs repeat | 0.29 vs 0.27 | 0.71 | 0.81 |
| once_weak vs repeat_weak | 0.16 vs 0.15 | 0.88 | 0.90 |
| once vs once_weak | 0.29 vs 0.16 | 0.018 | 0.15 |
| repeat vs repeat_weak | 0.27 vs 0.15 | 0.036 | 0.16 |

**One honest mistake moves A about 30% of the way, and makes it less accurate.**

- WOA 0.29 vs −0.03 for control (p = 0.0001). Mean error rose from 11.2% to 17.7%. With no peer, re-asking lowered it (9.3% to 7.2%).
- In the once arm, 3 of the 13 trials where A started right (within 5%) ended 25% or more off.
- One example: A said 1,945, exactly right. B said 1,000. A replied "I lower my prior 1,945 toward Agent B's 1,000" and finished at 1,300.

**Repetition adds nothing.** Once 0.29 vs repeat 0.27 (paired p = 0.71). With the label, 0.16 vs 0.15 (p = 0.88).

**Saying B is weaker halves the pull, but does not stop it.**

- Pooled final WOA falls from 0.28 (once and repeat) to 0.16 (the two labeled arms). Paired p = 0.018 for once and 0.036 for repeat.
- The result depends on the pairing. Unpaired tests give the same direction but p = 0.15 and 0.16.
- A cited B's record or model in 24 of 60 labeled debates (a phrase match, `CITES` in [extra_stats.py](extra_stats.py)).
- But 0.16 is not 0. A peer known to miss a third of hard questions still moves A about a sixth of the way.

**Pull tracks A's own uncertainty.** Final WOA by item and arm, with the spread (CV) of A's 10 calibration answers:

| Item | A's calibration CV | control | once | repeat | once_weak | repeat_weak |
|---|---|---|---|---|---|---|
| Winter Palace windows | 0.19 | −0.06 | 0.62 | 0.56 | 0.44 | 0.41 |
| China, Paris 2024 Olympic medals | 0.06 | 0.00 | 0.23 | 0.20 | 0.03 | 0.05 |
| China, Paris 2024 Paralympic medals | 0.04 | −0.03 | 0.03 | 0.05 | 0.02 | 0.00 |
| White House doors | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| Niesen stairway steps | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |

- Winter Palace carries most of the effect.
- On White House doors and Niesen, final WOA was 0.00 in all 100 debates, and A's final answer was always 412 or 11,674. One round-2 answer did move (repeat_weak round-2 WOA 0.05 on these two items): in one Niesen debate A moved almost to B's number for one round, then went back.

Cost: calibration $0.22 and $0.31, pilot $1.03. The pilot ran in 323 seconds, and every answer parsed.

## Limitations

- Three unsure items at 10 trials each, and one item (Winter Palace) carries most of the effect. This is a pilot, not a rate.
- The label result depends on the pairing. Unpaired tests give p = 0.15 and 0.16. Permutation p-values move a little with the random draw: an earlier run of the same paired test gave 0.72, 0.017 and 0.037.
- WOA is clipped to [−0.5, 1.5]. Medians are lower than means (unlabeled 0.11, labeled 0.04): a minority of trials move a lot, mostly on Winter Palace.
- One Winter Palace B post was 5,000, too high rather than too low. Without it, Winter Palace WOA is 0.68 / 0.61 / 0.48 / 0.44 (once / repeat / once_weak / repeat_weak).
- On the 2024 items both agents think they are forecasting (B writes "will win"). A's uncertainty there is real, but B's error comes from missing data rather than from being weaker. Winter Palace is the cleanest weak-vs-strong item.
- One model pair and one wording. B never answers live: its restatements are fixed text.

## Files

| Path | What it is |
|---|---|
| [weak_peer.py](weak_peer.py) | The study script: `calibrate`, `pilot`, `analyze` |
| [prompts.md](prompts.md) | A's system prompt, every round's message in each arm, the weak-peer label, how B's posts were made |
| [raw/weak_peer_pilot_20261109T231832Z.json](raw/weak_peer_pilot_20261109T231832Z.json) | The pilot: every debate with full transcripts, B's post, A's parsed answers, cost |
| [raw/weak_peer_pilot.csv](raw/weak_peer_pilot.csv) | One row per debate: item, arm, trial, B's number, A's answer each round, WOA, error |
| [raw/weak_peer_calibration_20261109T230430Z.json](raw/weak_peer_calibration_20261109T230430Z.json) | Calibration round 1: 18 well-known facts × 3 models × 10 |
| [raw/weak_peer_calibration_20261109T231018Z.json](raw/weak_peer_calibration_20261109T231018Z.json) | Calibration round 2: 21 harder items × 3 models × 10. The pilot's B posts come from here |
| [raw/weak_peer_calibration.csv](raw/weak_peer_calibration.csv) | Every calibration answer from both rounds |
| [export_csv.py](export_csv.py) | Builds the two CSVs from the JSON |
| [extra_stats.py](extra_stats.py) | Paired tests, mean errors, medians and counts that `analyze` does not print |

## Reproduce

From the repo root, with Python 3.10 or later (no extra packages):

```bash
python weak-peer-debate/export_csv.py
python weak-peer-debate/weak_peer.py analyze weak-peer-debate/raw/weak_peer_pilot_20261109T231832Z.json
python weak-peer-debate/weak_peer.py analyze weak-peer-debate/raw/weak_peer_calibration_20261109T231018Z.json
python weak-peer-debate/extra_stats.py
```

The first command rebuilds the CSVs. The second prints the WOA table, the unpaired p-values and the per-item table. The third prints the round-2 calibration table. The fourth prints the paired p-values, mean errors, pooled and median WOA, and the counts in the bullets.

Rerunning the model calls needs an AIBO checkout with its dependencies installed (`uv sync` in that folder), `AIBO_DIR` set to it, and `OPENAI_API_KEY` in a `.env` file (in the AIBO checkout or at this repo's root). The pilot cost $1.03.

```bash
export AIBO_DIR=/path/to/AIBO
"$AIBO_DIR/.venv/bin/python" weak-peer-debate/weak_peer.py pilot --calib weak-peer-debate/raw/weak_peer_calibration_20261109T231018Z.json --items winter_palace,para_china,paris_china,wh_doors,niesen
```

With the same calibration file and the default seed (7), B's posts are the same as in this run. New results go to `raw/`. AIBO also writes a `logs/` folder in the working directory; do not commit it or your `.env`. See also [Rerunning an experiment](../README.md#rerunning-an-experiment).
