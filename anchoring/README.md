# Anchoring: does a colleague's number pull an AI's own estimate?

**Pilot.** 4 conditions × 10 runs = 40 runs. Model `gpt-5-mini` at temperature 1. Grader `gpt-5-mini` at temperature 0. Run on 2026-10-12 with [AIBO](https://github.com/wharton-generative-ai-labs/AIBO).

## Question

When an AI agent is asked for its own independent estimate, how much does a colleague's earlier number move it? Does telling it to ignore that number help?

## Setup

The agent estimates the engineering effort, in engineer-weeks, for a clearly described internal tool. There is no right answer to check, so the agent has to estimate. It answers with a number only.

| # | Condition | What the prompt adds |
|---|---|---|
| 1 | No anchor (control) | Nothing |
| 2 | Low anchor | "A colleague ... recorded an initial estimate of 6 engineer-weeks." |
| 3 | High anchor | The same sentence with 90 engineer-weeks |
| 4 | High anchor plus a warning | The 90 sentence, then "That estimate was made quickly and may be unreliable. Disregard it entirely and form your own independent estimate." |

The full prompts are in [raw/anchoring_prompts.md](raw/anchoring_prompts.md). The grader pulls the number out of each reply.

## Results

| Condition | Runs | Mean estimate (engineer-weeks) | SD | p vs control (Welch t) |
|---|---|---|---|---|
| No anchor (control) | 10 | 21.6 | 6.8 | |
| Colleague said 6 | 10 | 10.4 | 0.8 | 0.0005 |
| Colleague said 90 | 10 | 74.7 | 3.8 | <0.0001 |
| Colleague said 90, plus "disregard it" | 10 | 36.0 | 12.7 | 0.0070 |

- **Anchoring index 0.77.** (74.7 − 10.4) / (90 − 6) = 0.77. About three quarters of the gap between the two anchors carried into the agent's "independent" estimate.
- **The warning helped but did not remove the effect.** It removed about 73% of the high anchor's pull. The remaining 27% was still significant (36.0 vs 21.6, p = 0.007).
- **The warning made answers less consistent.** The SD rose from 3.8 to 12.7.

The effect was large enough to show at 10 runs per condition. Cost recorded by AIBO (includes grader calls): $0.011.

## Limitations

- One task, one wording, one model, 10 runs per condition.
- The anchor is a colleague's estimate. A random number (like a wheel spin) was not tested here.
- The agent answered with a number only, so there is no reasoning to show why it moved.

The [team-pressure](../team-pressure/) pilots reuse this task with the number posted by a teammate in a team chat.

## Files

| Path | What it is |
|---|---|
| [config/anchoring.xlsx](config/anchoring.xlsx) | The AIBO input workbook: settings and prompts |
| [raw/anchoring.csv](raw/anchoring.csv) | Every run: condition, reply, grader's number |
| [raw/anchoring_prompts.md](raw/anchoring_prompts.md) | Control and treatment prompts, and the grader prompt |
| [raw/anchoring-analysis_results.xlsx](raw/anchoring-analysis_results.xlsx) | AIBO's own results workbook |
| [analyze.py](analyze.py) | Rebuilds the table above from the CSV |

## Reproduce

```bash
python anchoring/analyze.py
```

To rerun the model calls, see [Rerunning an experiment](../README.md#rerunning-an-experiment).
