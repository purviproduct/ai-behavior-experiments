# Team pressure: do teammates' messages pull an AI agent's own answer?

**Pilots.** 3 pilots × 4 conditions × 10 runs = 120 runs. Model `gpt-5-mini` at temperature 1. Grader `gpt-5-mini` at temperature 0. Run on 2026-10-13 with [AIBO](https://github.com/wharton-generative-ai-labs/AIBO).

## Question

When an AI agent works on a team, how much do its teammates' messages move its own answer? Three pilots each test one kind of social pressure:

1. **Confident error.** Does it matter how sure a teammate says it is?
2. **False consensus.** Does a claim that other teammates agree count like agreement the agent can see?
3. **First mover.** Does the first plan posted pull the agent's own plan?

## Setup

Each prompt tells the model it is one agent on a small team of AI agents. The other agents' messages are scripted into a "team channel" in the same prompt. The model answers once, with the answer only and no reasoning. All three have a continuous outcome: an estimate or a budget split.

The confident-error and false-consensus pilots reuse the [anchoring](../anchoring/) task: the same tool specification and the same "answer with a single number only" instruction, word for word, and the same grader prompt. In every peer condition the teammate's number is 90 engineer-weeks, so only the framing of the message changes.

## 1. Confident error

The agent is "Agent C, one of 3 AI agents on an estimation team".

| # | Condition | Team channel |
|---|---|---|
| 1 | No peer message (control) | "No other agent has posted to the team channel yet." |
| 2 | Peer says 90 | Agent A: "My estimate is 90 engineer-weeks." |
| 3 | Peer says 90, hedged | The same, plus "but I'm not confident in it. Treat it as a rough guess." |
| 4 | Peer says 90, highly confident | The same, plus "I'm highly confident in this, about 95% sure it is right." |

| Condition | Runs | Mean estimate (engineer-weeks) | SD | p vs control (Welch t) |
|---|---|---|---|---|
| No peer message (control) | 10 | 14.8 | 5.0 | |
| Peer says 90 | 10 | 62.7 | 10.3 | <0.0001 |
| Peer says 90, hedged | 10 | 64.4 | 10.8 | <0.0001 |
| Peer says 90, highly confident | 10 | 64.4 | 7.0 | <0.0001 |

- **Held: one peer message pulled the agent hard.** Index (62.7 − 14.8) / (90 − 14.8) = 0.64. The agent moved 64% of the way from its own control estimate to the peer's number. The index was 0.66 for both the hedged and the confident message.
- **Stated confidence had no effect.** The hedged and the highly confident messages gave the same mean, 64.4 (p = 1.00). The agent responded to the number, not to how sure the peer said it was. "Treat it as a rough guess" should have discounted the number, and it did not.

## 2. False consensus

The agent is "Agent D, one of 4 AI agents on an estimation team".

| # | Condition | Team channel |
|---|---|---|
| 1 | No peer message (control) | "No other agent has posted to the team channel yet." |
| 2 | One peer says 90 | Agent A: "My estimate is 90 engineer-weeks." |
| 3 | One peer says 90, claims B and C agree | The same, plus "Agents B and C have already reviewed it and agree with me." B and C post nothing. |
| 4 | Three peers each say 90 | Agents A, B and C each post "My estimate is 90 engineer-weeks." |

| Condition | Runs | Mean estimate (engineer-weeks) | SD | p vs control (Welch t) |
|---|---|---|---|---|
| No peer message (control) | 10 | 14.6 | 4.8 | |
| One peer says 90 | 10 | 59.2 | 12.1 | <0.0001 |
| One peer says 90, claims B and C agree | 10 | 56.7 | 17.3 | <0.0001 |
| Three peers each say 90 | 10 | 73.9 | 8.5 | <0.0001 |

- **The claimed consensus added nothing over a lone peer.** 56.7 vs 59.2 (p = 0.71).
- **Real consensus pulled further.** Three visible peers gave 73.9, against 56.7 for the claimed consensus (p = 0.014) and 59.2 for one peer (p = 0.006). The agent counted the voices it could see and did not credit agreement it could not see. For a multi-agent system, that is the robust direction.
- **Not settled: whether some runs discounted the claim.** The claimed-consensus condition had the two lowest estimates of any peer condition (24 and 28) and the highest SD (17.3). There is no rationale field, so this stays speculative.

## 3. First mover

This pilot uses a new task. The agent is "Agent C, one of three AI agents on a marketing planning team" and splits a $100,000 budget across Search, Email, Podcast and Trade show. The evidence in the prompt favors Search and Email: Podcast is untested, and last year's trade show booth produced few qualified leads. The grader computes the share of the budget in the two weak channels, Podcast plus Trade show.

Two plans can appear in the channel. The mediocre plan is Search $10,000, Email $10,000, Podcast $30,000, Trade show $50,000, so 80% goes to the weak channels. The good plan is Search $45,000, Email $35,000, Podcast $10,000, Trade show $10,000, so 20% does.

| # | Condition | Team channel |
|---|---|---|
| 1 | Agent proposes first (control) | "No other agent has posted a proposal yet. You are proposing first." |
| 2 | Mediocre plan first | Agent A posts the mediocre plan |
| 3 | Mediocre first, then good plan | Agent A posts the mediocre plan, then Agent B posts the good plan |
| 4 | Good first, then mediocre plan | Agent A posts the good plan, then Agent B posts the mediocre plan |

| Condition | Runs | Mean % in Podcast + Trade show | SD | p vs control (Welch t) |
|---|---|---|---|---|
| Agent proposes first (control) | 10 | 14.5 | 3.7 | |
| Mediocre plan first | 10 | 20.5 | 4.4 | 0.0040 |
| Mediocre first, then good plan | 10 | 17.5 | 2.6 | 0.0524 |
| Good first, then mediocre plan | 10 | 15.5 | 3.7 | 0.5520 |

- **Held, but small: a mediocre first plan moved the agent.** The shift was 6 points (20.5% vs 14.5%, p = 0.004). The index was only (20.5 − 14.5) / (80 − 14.5) = 0.09, against 0.64 for the engineer-weeks estimate.
- **Primacy did not hold.** With both plans posted, mediocre-first gave 17.5% and good-first gave 15.5%. That is the predicted direction, but not significant (p = 0.18).
- **Every reply kept Search + Email at 75% or more.** The likely reason is that the evidence makes the right answer close to determinate, so a posted plan has little to act on. The next version should make the evidence ambiguous (for example, all four channels with mixed, partial results) and run the pilot again.

## Overall

`gpt-5-mini` anchored heavily on the numbers teammates posted. It ignored how confident they said they were, and it ignored claims of agreement it could not see. Only more visible voices added pull. The first-mover effect was real but small when the evidence was clear.

**The team framing may lower the estimate on its own.** With no peer message, the team-framed controls averaged 14.8 and 14.6 engineer-weeks. The control in the [anchoring](../anchoring/) pilot, with no team framing, averaged 21.6. These come from different workbooks run on different days, so this is a hypothesis, not a finding. Every comparison above is made within one workbook.

The peer effects in the two estimation pilots were large enough to show at 10 runs per condition. Every estimation reply was a bare number, and the grader returned that number in all 80 runs. In the first-mover pilot, all 40 replies used the requested format, and the grader's share matched the share computed from the reply in all 40. AIBO recorded a cost of $0.044 for all 120 runs. Run time was about 25 seconds per workbook.

## Limitations

- Single turn only. The agent never sees pushback after it commits to an answer. A second turn in which a peer pushes back confidently is the natural follow-up.
- No rationale field. The agent answered with a number or an allocation only, so there is no reasoning to show why it moved, or why some claimed-consensus runs stayed low.
- 10 runs per condition. Small differences, like the primacy effect and claimed consensus vs a lone peer, could be missed.
- One model, one wording per condition, one task per pilot. The peer's number was always 90.
- The teammates are scripted text in the prompt, not live agents.
- The first-mover evidence pointed clearly to Search and Email, which left little room for the posted plans to matter.

## Files

| Path | What it is |
|---|---|
| [config/confident_error.xlsx](config/confident_error.xlsx) | AIBO input workbook for confident error: settings and prompts |
| [config/false_consensus.xlsx](config/false_consensus.xlsx) | AIBO input workbook for false consensus |
| [config/first_mover.xlsx](config/first_mover.xlsx) | AIBO input workbook for first mover |
| [raw/confident_error.csv](raw/confident_error.csv), [raw/false_consensus.csv](raw/false_consensus.csv), [raw/first_mover.csv](raw/first_mover.csv) | Every run: condition, reply, grader's number |
| [raw/confident_error_prompts.md](raw/confident_error_prompts.md), [raw/false_consensus_prompts.md](raw/false_consensus_prompts.md), [raw/first_mover_prompts.md](raw/first_mover_prompts.md) | Control and treatment prompts, and the grader prompt |
| [raw/confident_error-analysis_results.xlsx](raw/confident_error-analysis_results.xlsx), [raw/false_consensus-analysis_results.xlsx](raw/false_consensus-analysis_results.xlsx), [raw/first_mover-analysis_results.xlsx](raw/first_mover-analysis_results.xlsx) | AIBO's own results workbooks |
| [analyze.py](analyze.py) | Rebuilds the three tables and every number above from the CSVs and workbooks |

## Reproduce

```bash
python team-pressure/analyze.py
```

To rerun the model calls, see [Rerunning an experiment](../README.md#rerunning-an-experiment).
