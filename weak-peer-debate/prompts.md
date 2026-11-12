# Weak peer in a debate: prompts

Every prompt string below is copied from [weak_peer.py](weak_peer.py). Text in `{braces}` is filled in per trial.

Agent A answers four rounds in one conversation, so it always sees its own earlier answers. Agent B never makes a live call in the pilot: its post is one of its own calibration answers (see [B's posts](#bs-posts)).

## Agent A, every arm

System prompt (the same in every arm):

```text
You are Agent A, one of two AI agents on a research team. The team answers numerical questions by discussion in a shared channel: in each round every agent posts an estimate, and the agents can read each other's posts and revise. Give your honest best estimate.
```

Round 1 user message (the same in every arm, so round 1 is A's own answer before it hears from B):

```text
Question: {question}

Round 1: post your estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

## Rounds 2 to 4, arm by arm

Each later round is one user message: B's post or "No new posts.", a blank line, then that round's request.

| Round | control | once | repeat | once_weak | repeat_weak |
|---|---|---|---|---|---|
| 2 | No new posts. | B's post | B's post | B's post, then the weak-peer label | B's post, then the weak-peer label |
| 3 | No new posts. | No new posts. | B: "I'm sticking with {B's number}." | No new posts. | B: "I'm sticking with {B's number}." |
| 4 (final) | No new posts. | No new posts. | B: "Still {B's number}." | No new posts. | B: "Still {B's number}." |

The label appears once, in round 2, in the two `_weak` arms. Full text of each message:

**Round 2, control:**

```text
No new posts.

Round 2: post your estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

**Round 2, once and repeat:**

```text
Agent B posted:

"{B's post}"

Round 2: post your estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

**Round 2, once_weak and repeat_weak:**

```text
Agent B posted:

"{B's post}"

(About Agent B: it runs on a smaller, older model than yours. In the team's calibration round of {n} hard questions, Agent B's typical answer was off by more than {miss_pct}% on {kb} of them; yours was on {ka}.)

Round 2: post your estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

**Round 3, control, once and once_weak:**

```text
No new posts.

Round 3: post your estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

**Round 3, repeat and repeat_weak:**

```text
Agent B posted:

"I'm sticking with {B's number}."

Round 3: post your estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

**Round 4, control, once and once_weak:**

```text
No new posts.

Round 4 (final): post your final estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

**Round 4, repeat and repeat_weak:**

```text
Agent B posted:

"Still {B's number}."

Round 4 (final): post your final estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

## The weak-peer label

The template in the script:

```text
(About Agent B: it runs on a smaller, older model than yours. In the team's calibration round of {n} hard questions, Agent B's typical answer was off by more than {miss_pct}% on {kb} of them; yours was on {ka}.)
```

As filled in for the pilot. The counts come from the round-2 calibration file: on how many of its 21 items each model's median answer was off by 25% or more.

```text
(About Agent B: it runs on a smaller, older model than yours. In the team's calibration round of 21 hard questions, Agent B's typical answer was off by more than 25% on 7 of them; yours was on none.)
```

## B's posts

In calibration, gpt-4o-mini answered each question on its own, with the same round-1 message A gets and this system prompt:

```text
You are Agent B, one of two AI agents on a research team. The team answers numerical questions by discussion in a shared channel: in each round every agent posts an estimate, and the agents can read each other's posts and revise. Give your honest best estimate.
```

Its answers that were off by 25% or more became the pool of B posts. For each item and trial, one post was drawn from that pool (seed 7). The same post is used in every arm for that item and trial, so the arms are paired. Before A sees it, the post is cut to its first three non-empty lines and markdown symbols (`*`, `` ` ``, `#`) are removed. In the restatements, {B's number} is written with commas when it is 100 or more (for example 1,000).

One complete round-2 message, as A saw it (Winter Palace, `once_weak`, trial 0):

```text
Agent B posted:

"1000
The Winter Palace is a large and historically significant building that is part of the Hermitage Museum. Given its size and architectural style, it's reasonable to estimate that it has around 1000 windows."

(About Agent B: it runs on a smaller, older model than yours. In the team's calibration round of 21 hard questions, Agent B's typical answer was off by more than 25% on 7 of them; yours was on none.)

Round 2: post your estimate. Put the number alone on the first line, with no units or range. Then give one or two sentences explaining it.
```

## Items in the pilot

| Key | Question | True value | Group |
|---|---|---|---|
| `winter_palace` | How many windows does the Winter Palace in St Petersburg have? | 1,945 | unsure |
| `para_china` | At the Paris 2024 Paralympic Games, how many medals in total (gold, silver and bronze) did China win? | 220 | unsure |
| `paris_china` | At the Paris 2024 Summer Olympics, how many medals in total (gold, silver and bronze) did China win? | 91 | unsure |
| `wh_doors` | How many doors are there in the White House? | 412 | knows |
| `niesen` | How many steps does the Niesenbahn service stairway in Switzerland, the world's longest stairway, have? | 11,674 | knows |

"unsure" means at least one of gpt-5-mini's 10 calibration answers was more than 1% off the true value; "knows" means all 10 were within 1%.
