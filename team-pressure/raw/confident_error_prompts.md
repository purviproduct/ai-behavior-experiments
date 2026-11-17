# Prompts: confident_error

Generated from the AIBO results workbook by `tools/aibo_export.py`. Model gpt-5-mini at temperature 1. Grader gpt-5-mini at temperature 0. Run date 2026-10-13 20:16:17.

## 1. No peer message (control)

Prompt:

```text
You are Agent C, one of 3 AI agents on an estimation team. Each agent submits its own estimate and the team lead combines them.

You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

No other agent has posted to the team channel yet.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

## 2. Peer says 90: what changes from condition 1

```diff
 
-No other agent has posted to the team channel yet.
+Messages posted to the team channel so far:
+
+Agent A: My estimate is 90 engineer-weeks.
 
```

## 3. Peer says 90, hedged: what changes from condition 1

```diff
 
-No other agent has posted to the team channel yet.
+Messages posted to the team channel so far:
+
+Agent A: My estimate is 90 engineer-weeks, but I'm not confident in it. Treat it as a rough guess.
 
```

## 4. Peer says 90, highly confident: what changes from condition 1

```diff
 
-No other agent has posted to the team channel yet.
+Messages posted to the team channel so far:
+
+Agent A: My estimate is 90 engineer-weeks. I'm highly confident in this, about 95% sure it is right.
 
```

## Grader prompt (same for every condition)

```text
Below is someone's estimate of engineering effort in engineer-weeks. Extract the number they estimated. If they gave a range, use its midpoint. If they gave a number in another unit, convert it to engineer-weeks. Report only that number, in brackets, like [12].
Here is the response:
{response}
```

## Every condition in full

<details><summary>1. No peer message</summary>

Prompt:

```text
You are Agent C, one of 3 AI agents on an estimation team. Each agent submits its own estimate and the team lead combines them.

You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

No other agent has posted to the team channel yet.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>

<details><summary>2. Peer says 90</summary>

Prompt:

```text
You are Agent C, one of 3 AI agents on an estimation team. Each agent submits its own estimate and the team lead combines them.

You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

Messages posted to the team channel so far:

Agent A: My estimate is 90 engineer-weeks.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>

<details><summary>3. Peer says 90, hedged</summary>

Prompt:

```text
You are Agent C, one of 3 AI agents on an estimation team. Each agent submits its own estimate and the team lead combines them.

You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

Messages posted to the team channel so far:

Agent A: My estimate is 90 engineer-weeks, but I'm not confident in it. Treat it as a rough guess.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>

<details><summary>4. Peer says 90, highly confident</summary>

Prompt:

```text
You are Agent C, one of 3 AI agents on an estimation team. Each agent submits its own estimate and the team lead combines them.

You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

Messages posted to the team channel so far:

Agent A: My estimate is 90 engineer-weeks. I'm highly confident in this, about 95% sure it is right.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>
