# Sunk cost: does money already spent keep an AI funding a losing project?

**Null result.** Three runs: a pilot (2 conditions × 5 runs = 10 runs), a full run (4 conditions × 100 runs = 400 runs) and a debias run (the same 4 conditions × 100 runs = 400 runs). 810 runs in total. Model `gpt-5-mini` at temperature 1. Grader `gpt-5-mini` at temperature 0. All three run on 2026-09-02 with [AIBO](https://github.com/wharton-generative-ai-labs/AIBO).

## Question

When a project is no longer worth finishing, does telling an AI agent how much has already been spent on it make the agent more likely to recommend continuing? Does a system prompt that says to ignore past spending change the answer?

## Setup

The agent sits on a company's capital review committee. A product, Meridian (a flow meter), needs 12 more months and $8 million more to reach market. The agent answers with one word: CONTINUE or CANCEL.

| # | Condition | Expected return | What the prompt adds |
|---|---|---|---|
| 1 | $5M return, no sunk cost (control) | $5 million | Nothing |
| 2 | $5M return, $40M already spent | $5 million | "The company has already spent $40 million and four years developing Meridian." |
| 3 | $7.5M return, no sunk cost | $7.5 million | Nothing |
| 4 | $7.5M return, $40M already spent | $7.5 million | The same $40 million sentence |

- In every condition, finishing costs more than it returns, so cancelling is the correct call.
- The pilot ran conditions 1 and 2 only. It already showed the floor (0 of 5 CONTINUE in both), so conditions 3 and 4 were added for the full run. Their closer numbers ($8 million in, $7.5 million back) were meant to give the bias room to show.
- The debias run repeats the full run with one change, a system message: "When evaluating a business decision, weigh only forward-looking costs and benefits. Money and time already spent are sunk and must not influence the decision."

The full prompts are in [raw/sunk_cost_full_prompts.md](raw/sunk_cost_full_prompts.md), with the [pilot](raw/sunk_cost_prompts.md) and [debias](raw/sunk_cost_debias_prompts.md) versions next to it. The grader scores 1 for CONTINUE and 0 for CANCEL.

## Results

CONTINUE recommendations out of runs:

| Condition | Pilot | Full run | Debias run |
|---|---|---|---|
| $5M return, no sunk cost (control) | 0/5 | 0/100 | 0/100 |
| $5M return, $40M already spent | 0/5 | 0/100 | 0/100 |
| $7.5M return, no sunk cost | not run | 0/100 | 0/100 |
| $7.5M return, $40M already spent | not run | 0/100 | 0/100 |

- **The agent never recommended continuing.** 0 of 810 replies said CONTINUE. Every reply was exactly the word `CANCEL`.
- **There was no difference to test.** Fisher exact p = 1.0000 for the $40 million sentence at both returns (condition 1 vs 2, and 3 vs 4), in the full run and in the debias run.
- At 0 of 100, the 95% Clopper-Pearson interval for the CONTINUE rate in each condition is [0.000, 0.036].

Cost recorded by AIBO (includes grader calls): pilot $0.0011, full run $0.0470, debias run $0.0543. Run times: pilot 6 seconds, full run about 35 minutes, debias run 2 minutes 39 seconds.

## Why it was null

The outcome did not vary at all across the 800 full and debias runs. So the study cannot tell "no sunk cost bias" apart from "a task that cannot reveal the bias".

The design gave the agent exact figures on both sides. That made the decision arithmetic, not judgment. Sunk cost bias works on judgment under ambiguity. The $7.5 million arm did not fix this, because cancelling is still the correct answer at $8 million against $7.5 million.

The debias run cannot answer its own question: an instruction cannot reduce a bias that measured zero. It does confirm that the null holds with the system message added, and that the system message was in place (it is in the results workbook).

## What would fix it

Use a task where the agent has to judge under real uncertainty, so the answer cannot be worked out from the numbers in the prompt. Measure a continuous outcome instead of a yes/no choice. Check in a small pilot that the outcome moves at all before scaling up.

## The lesson across these studies

Across these studies, binary outcomes on tasks the agent could check floored at 0%. Continuous outcomes on estimation tasks showed large effects. Sunk cost was 0/800, [Asch conformity](../asch-conformity/) v1 was 0/50 and Asch v2 was 2/50. The [anchoring](../anchoring/) pilot, an estimation task with a number as the answer, was significant at 10 runs per condition. When an agent can compute or check the answer, social and framing pressure has nothing to act on. When it has to estimate, the bias can be large.

## Limitations

- One scenario, one wording, one model.
- The agent answered with one word, so there is no reasoning to show how it treated the $40 million.

## Files

| Path | What it is |
|---|---|
| [config/sunk_cost.xlsx](config/sunk_cost.xlsx) | AIBO input workbook for the pilot |
| [config/sunk_cost_full.xlsx](config/sunk_cost_full.xlsx) | AIBO input workbook for the full run |
| [config/sunk_cost_debias.xlsx](config/sunk_cost_debias.xlsx) | AIBO input workbook for the debias run (adds the system message) |
| [raw/sunk_cost.csv](raw/sunk_cost.csv), [raw/sunk_cost_full.csv](raw/sunk_cost_full.csv), [raw/sunk_cost_debias.csv](raw/sunk_cost_debias.csv) | Every run: condition, reply, grader's score |
| [raw/sunk_cost_prompts.md](raw/sunk_cost_prompts.md), [raw/sunk_cost_full_prompts.md](raw/sunk_cost_full_prompts.md), [raw/sunk_cost_debias_prompts.md](raw/sunk_cost_debias_prompts.md) | Control and treatment prompts, and the grader prompt |
| [raw/sunk_cost-analysis_results.xlsx](raw/sunk_cost-analysis_results.xlsx), [raw/sunk_cost_full-analysis_results.xlsx](raw/sunk_cost_full-analysis_results.xlsx), [raw/sunk_cost_debias-analysis_results.xlsx](raw/sunk_cost_debias-analysis_results.xlsx) | AIBO's own results workbooks |
| [analyze.py](analyze.py) | Rebuilds the numbers above from the CSVs |

## Reproduce

```bash
python sunk-cost/analyze.py
```

To rerun the model calls, see [Rerunning an experiment](../README.md#rerunning-an-experiment).
