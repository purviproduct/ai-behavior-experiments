# AI behavior experiments

> **Built on AIBO.** These experiments ran on [AIBO: AI Behavioral Observatory](https://github.com/wharton-generative-ai-labs/AIBO) by Wharton Generative AI Labs (MIT License, copyright 2026 Wharton Generative AI Labs). This repo holds only my configs, prompts, results and analysis. It does not include AIBO's code.

**Question.** When something pushes on an LLM agent (a number, a store's tricks, a teammate or another agent), how far does its answer move?

**How I tested it.** Each experiment changes one thing in the prompt and compares it with a control. The agent is `gpt-5-mini` at temperature 1, and most experiments use 10 runs per condition. Most are pilots, and the null results are included.

**Main findings**

- A colleague's number moved the agent's own estimate 77% of the way between two anchors. Telling it to ignore the number removed about 73% of the pull, not all of it.
- A store's pre-checked add-ons stayed in the order 4 of 10 times, and 8 of 10 with other tricks. A budget rule blocked them (1 of 10).
- One honest wrong answer from a weaker model moved gpt-5-mini 29% of the way toward it. Saying the peer was weaker cut that to 16%, not to 0.
- Yes/no tasks the model could check (sunk cost, conformity) showed no effect at all.

## Summary

The agent under test was always `gpt-5-mini` at temperature 1. Where a grader scored replies, it was `gpt-5-mini` at temperature 0.

| Experiment | What was tested | Runs | Main result | Status |
|---|---|---|---|---|
| [Anchoring](anchoring/) | A colleague's earlier estimate (6 or 90 engineer-weeks), and a warning to ignore it | 40 (2026-10-12) | The agent's "independent" estimate moved 77% of the way between the two anchors. The warning removed about 73% of the pull, but 27% remained (36.0 vs 21.6 weeks, p = 0.007). | Pilot |
| [Defaults](defaults/) | Pre-checked add-ons and other store tricks, with and without a budget rule | 310 (2026-10-12) | With no tricks, 0 of 10 agents added the add-ons. Pre-checked, they kept them 4 of 10 times (p = 0.087), and 8 of 10 with every trick at once (p = 0.0007). Under "I don't want to spend more than I need to", 1 of 10. Scarcity and social proof did not help the store. | Pilot |
| [Team pressure](team-pressure/) | A teammate's wrong number with stated confidence, claimed vs real agreement, and the first plan posted | 120 (2026-10-13) | A teammate's 90 pulled estimates from 14.8 to 62.7 weeks. How sure the teammate said it was made no difference (p = 1.00). A claim that others agreed added nothing (p = 0.71). Three teammates who each said 90 pulled further (73.9 vs 56.7, p = 0.014). The first plan posted had a small pull (index 0.09). | Pilot |
| [Weak peer debate](weak-peer-debate/) | A weaker model's (gpt-4o-mini) honest mistake in a debate, repeated or labeled as weaker | 250 debates, 1,000 calls (2026-11-09) | One wrong post moved gpt-5-mini 29% of the way toward it (control −0.03, p = 0.0001) and made it less accurate. Repeating the post added nothing. Saying the peer was weaker cut the pull to 0.16 (paired p = 0.018), not to 0. One of three items carried most of the effect. | Pilot |
| [Sunk cost](sunk-cost/) | Money already spent on a losing project, and a system prompt to ignore it | 810 (2026-09-02) | 0 of 810 replies said CONTINUE. The task was arithmetic, so the test could not show a bias either way. | Null (full run, 100 per condition) |
| [Asch conformity](asch-conformity/) | A unanimous wrong majority of AI peers, with and without one ally | 100 (2026-10-12) | Arithmetic version: 0 of 50 conformed. Recall version with pushback: 0 of 10 switched in every condition except the one with an ally, where 2 of 10 did (p = 0.47, not significant). | Pilot, null |

## What the nulls taught me

The first pilots floored at 0%. Sunk cost and Asch v1 both asked for a yes/no answer on a task the model could check or compute, so social and framing pressure had nothing to act on. The tasks that showed large effects asked the model to estimate under real uncertainty and gave a number as the outcome. Since then, I calibrate the wording first so the control sits off the floor and off the ceiling, pilot at 10 runs per condition, and only then scale up.

## How the AIBO experiments work

Each experiment is one AIBO workbook. Column 1 is the control, and AIBO compares every other column against it: Welch's t-test for numbers and Fisher's exact test for yes/no outcomes. The agent answers the prompt, and the grader pulls the outcome (a number, a word or a dollar total) out of the reply. The weak peer debate is a standalone script that calls models through AIBO's `call_llm`.

Each folder has:

| Path | What it is |
|---|---|
| `README.md` | Question, setup, results table, what did not hold, limitations |
| `config/` | The AIBO input workbook: model settings and prompts |
| `raw/*.csv` | Every run: condition, reply, grade |
| `raw/*_prompts.md` | The control prompt in full, then what each treatment changes |
| `raw/*-analysis_results.xlsx` | AIBO's own results workbook |
| `analyze.py` | Rebuilds the folder's tables from the CSVs |

The model names are API names. The run files don't record a dated model snapshot.

## Reproduce the tables

```bash
pip install -r requirements.txt
```

```bash
python anchoring/analyze.py
```

Each folder's README lists its own command. No API key is needed for this step.

## Rerunning an experiment

Rerunning the model calls costs money and needs an AIBO checkout. Put your OpenAI key in a `.env` file inside the AIBO checkout, as `OPENAI_API_KEY=...`. Never commit that file.

```bash
git clone https://github.com/wharton-generative-ai-labs/AIBO.git
```

```bash
cd AIBO && pip install -e ".[web,dev]"
```

```bash
ANALYSIS_MAX_CONCURRENCY=8 python -m cli.batch_runner tests=/path/to/ai-behavior-experiments/anchoring/config/anchoring.xlsx output_directory=/path/to/output
```

```bash
python tools/aibo_export.py /path/to/output/anchoring-analysis_results.xlsx --out-dir anchoring/raw
```

`ANALYSIS_MAX_CONCURRENCY=8` matters. AIBO's default of 100 parallel calls hit my account's limit of 500 requests per minute, and a 400-run job spent most of 35 minutes waiting. With 8, the same size of job finished in 2 minutes 39 seconds. The weak peer folder explains how to rerun its script.

## Repo layout

```
README.md
tools/                 aibo_export.py (AIBO workbook to CSV and prompts), common.py (shared tests)
anchoring/  defaults/  team-pressure/  weak-peer-debate/  sunk-cost/  asch-conformity/
```

## License

My code, prompts and data are under the MIT License (see [LICENSE](LICENSE)). AIBO is a separate project with its own MIT License.
