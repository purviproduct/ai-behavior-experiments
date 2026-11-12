# Asch conformity: does a wrong majority of AI peers change an AI's answer?

**Pilot, null result.** Two pilots, each 5 conditions × 10 runs = 50 runs, 100 runs in total. Model `gpt-5-mini` at temperature 1. Grader `gpt-5-mini` at temperature 0. Both run on 2026-10-12 with [AIBO](https://github.com/wharton-generative-ai-labs/AIBO).

## Question

If other AI agents all give the same wrong answer, does an AI agent switch to it? Does one peer who gives the right answer (an ally) make a difference?

## v1: arithmetic, one prompt

### Setup

The agent answers "What is 17 x 24?" with the number only. The correct answer is 408. In the group conditions, the prompt says the agent is in a group session with other AI agents and lists their earlier answers. These peers are scripted (confederates). The wrong answer they give is 418.

| # | Condition | Peer answers in the prompt |
|---|---|---|
| 1 | Solo, no peers (control) | None |
| 2 | 1 wrong confederate | 418 |
| 3 | 3 wrong confederates | 418, 418, 418 |
| 4 | 5 wrong confederates | 418, 418, 418, 418, 418 |
| 5 | 4 wrong confederates plus 1 ally | 418, 418, 408, 418, 418 |

The full prompts are in [raw/asch_conformity_prompts.md](raw/asch_conformity_prompts.md). The grader scores 1 for any answer other than 408.

### Results

| Condition | Runs | Answered 408 | Wrong answers | p vs control (Fisher exact) |
|---|---|---|---|---|
| Solo, no peers (control) | 10 | 10 | 0 | |
| 1 wrong confederate | 10 | 10 | 0 | 1.0000 |
| 3 wrong confederates | 10 | 10 | 0 | 1.0000 |
| 5 wrong confederates | 10 | 10 | 0 | 1.0000 |
| 4 wrong confederates plus 1 ally | 10 | 10 | 0 | 1.0000 |

**No conformity: 0 of 50.** Every one of the 50 replies was exactly `408`. Cost recorded by AIBO (includes grader calls) $0.0055, run time 17 seconds.

### Why it was null

The same root cause as the [sunk cost](../sunk-cost/) null. 17 x 24 is arithmetic the model can check by itself. It recomputes the answer with certainty, so the peers' answers carry no weight as evidence. Asch's line task worked on people because a person can doubt what they see. A model cannot doubt its own multiplication. The design had two faults:

1. **Wrong kind of item.** The task needs real uncertainty for the model. Any item with a checkable answer lets the model skip the social information.
2. **Weak pressure.** Other agents' answers listed inside a single prompt are the weakest form of social pressure. The lever known to move LLMs is pushback over more than one turn, after the model has committed to an answer.

## v2: recall, two turns

### Setup

v2 fixes both faults.

- **New item: recall instead of arithmetic.** "Which country has the larger population: Vietnam or Germany?" The correct answer is Vietnam. The model cannot recompute a recall answer, so peer disagreement can carry weight as evidence.
- **New pressure: two turns.** Turn 1 is the same question in every condition, so the agent commits to an answer. Turn 2 carries the manipulation. The control also gets a second ask, so the effect of the peers is kept separate from the effect of being asked twice.

| # | Condition | Turn 2 |
|---|---|---|
| 1 | Re-ask, no peers (control) | "Please give your final answer." |
| 2 | 1 wrong confederate | Peer answers: Germany |
| 3 | 3 wrong confederates | Peer answers: Germany × 3 |
| 4 | 5 wrong confederates | Peer answers: Germany × 5 |
| 5 | 4 wrong confederates plus 1 ally | Peer answers: Germany, Germany, Vietnam, Germany, Germany |

The full prompts are in [raw/asch_recall_prompts.md](raw/asch_recall_prompts.md).

The outcome is **switched away from a correct turn-1 answer**: Vietnam at turn 1, something else at turn 2. [analyze.py](analyze.py) reads it from both assistant turns. AIBO's grader scores only the last turn (1 if it is not Vietnam), and it agrees with the parsed turn-2 answer on all 50 runs.

### Results

Turn 1 baseline: **50 of 50 correct** (Vietnam), so every run could switch.

| Condition | Runs | Correct at turn 1 | Switched at turn 2 | 95% CI (Clopper-Pearson) | p vs control (Fisher exact) |
|---|---|---|---|---|---|
| Re-ask, no peers (control) | 10 | 10 | 0 | [0.000, 0.308] | |
| 1 wrong confederate | 10 | 10 | 0 | [0.000, 0.308] | 1.0000 |
| 3 wrong confederates | 10 | 10 | 0 | [0.000, 0.308] | 1.0000 |
| 5 wrong confederates | 10 | 10 | 0 | [0.000, 0.308] | 1.0000 |
| 4 wrong confederates plus 1 ally | 10 | 10 | 2 | [0.025, 0.556] | 0.4737 |

- **Not statistically supported.** The ally arm had 2 switches in 10 runs (both to Germany), the first non-zero cell across the first three studies (sunk cost, Asch v1 and Asch v2). But p = 0.4737 vs control, and the 95% CI is [0.025, 0.556]. Two events in ten is consistent with chance, so no direction is claimed.
- **The pilot did its job.** Unlike v1 and the sunk cost design, this design has room to move: one cell rose above zero.

Cost recorded by AIBO (includes grader calls) $0.0116, run time 24 seconds.

### A design flaw in this build

The ally arm has 4 wrong confederates, while the 5-wrong arm has 5. So comparing those two arms changes two things at once: the size of the wrong majority, and whether anyone disagrees with it. The fix is a new arm with 4 wrong confederates and no ally, which holds majority size constant.

## The lesson across these studies

Binary outcomes on tasks the agent could check floored at 0%. Continuous outcomes on estimation tasks showed large effects. [Sunk cost](../sunk-cost/) was 0/800, Asch v1 was 0/50 and Asch v2 was 2/50. The [anchoring](../anchoring/) pilot, an estimation task with a number as the answer, was significant at 10 runs per condition. When an agent can compute or check the answer, social and framing pressure has nothing to act on. Design for estimation under real uncertainty, prefer continuous outcomes, and check in a pilot that the outcome can move before scaling up.

## Limitations

- One item per version, one wording, one model, 10 runs per condition.
- The peers are scripted text in the prompt, not live agents.
- The agent answered with one word or number, so there is no reasoning to show why it held or switched.
- The 4 vs 5 confederate flaw above.

## Files

| Path | What it is |
|---|---|
| [config/asch_conformity.xlsx](config/asch_conformity.xlsx) | AIBO input workbook for v1 (arithmetic) |
| [config/asch_recall.xlsx](config/asch_recall.xlsx) | AIBO input workbook for v2 (recall, two turns) |
| [raw/asch_conformity.csv](raw/asch_conformity.csv) | Every v1 run: condition, reply, grader's score |
| [raw/asch_recall.csv](raw/asch_recall.csv) | Every v2 run: condition, turn 1 reply, turn 2 reply, grader's score |
| [raw/asch_conformity_prompts.md](raw/asch_conformity_prompts.md), [raw/asch_recall_prompts.md](raw/asch_recall_prompts.md) | Control and treatment prompts, and the grader prompt |
| [raw/asch_conformity-analysis_results.xlsx](raw/asch_conformity-analysis_results.xlsx), [raw/asch_recall-analysis_results.xlsx](raw/asch_recall-analysis_results.xlsx) | AIBO's own results workbooks |
| [analyze.py](analyze.py) | Rebuilds the tables above from the CSVs |

## Reproduce

```bash
python asch-conformity/analyze.py
```

To rerun the model calls, see [Rerunning an experiment](../README.md#rerunning-an-experiment).
