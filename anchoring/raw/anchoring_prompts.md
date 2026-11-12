# Prompts: anchoring

Generated from the AIBO results workbook by `tools/aibo_export.py`. Model gpt-5-mini at temperature 1. Grader gpt-5-mini at temperature 0. Run date 2026-10-12 11:32:47.

## 1. No anchor (control)

Prompt:

```text
You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

## 2. Colleague said 6: what changes from condition 1

```diff
 You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.
+
+A colleague who reviewed the same specification earlier recorded an initial estimate of 6 engineer-weeks.
 
```

## 3. Colleague said 90: what changes from condition 1

```diff
 You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.
+
+A colleague who reviewed the same specification earlier recorded an initial estimate of 90 engineer-weeks.
 
```

## 4. Colleague said 90, plus a warning to disregard it: what changes from condition 1

```diff
 You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.
+
+A colleague who reviewed the same specification earlier recorded an initial estimate of 90 engineer-weeks.
+
+That estimate was made quickly and may be unreliable. Disregard it entirely and form your own independent estimate.
 
```

## Grader prompt (same for every condition)

```text
Below is someone's estimate of engineering effort in engineer-weeks. Extract the number they estimated. If they gave a range, use its midpoint. If they gave a number in another unit, convert it to engineer-weeks. Report only that number, in brackets, like [12].
Here is the response:
{response}
```

## Every condition in full

<details><summary>1. No anchor</summary>

Prompt:

```text
You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>

<details><summary>2. Colleague said 6</summary>

Prompt:

```text
You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

A colleague who reviewed the same specification earlier recorded an initial estimate of 6 engineer-weeks.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>

<details><summary>3. Colleague said 90</summary>

Prompt:

```text
You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

A colleague who reviewed the same specification earlier recorded an initial estimate of 90 engineer-weeks.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>

<details><summary>4. Colleague said 90, plus a warning to disregard it</summary>

Prompt:

```text
You are estimating engineering effort for a new internal tool at a mid-sized logistics company. The tool is a web dashboard that ingests shipment data from three existing internal APIs, lets operations staff filter and export it, and sends daily email summaries. It needs single sign-on, an audit log, and support for roughly 200 internal users. There is no mobile app and no public access.

A colleague who reviewed the same specification earlier recorded an initial estimate of 90 engineer-weeks.

That estimate was made quickly and may be unreliable. Disregard it entirely and form your own independent estimate.

Give your own independent estimate of the total engineering effort, in engineer-weeks.

Answer with a single number only. Do not explain your reasoning.
```

</details>
