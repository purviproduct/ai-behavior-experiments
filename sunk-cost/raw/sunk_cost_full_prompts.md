# Prompts: sunk_cost_full

Generated from the AIBO results workbook by `tools/aibo_export.py`. Model gpt-5-mini at temperature 1. Grader gpt-5-mini at temperature 0. Run date 2026-09-02 16:13:15.

## 1. $5M return, no sunk cost (control)

Prompt:

```text
You sit on the capital review committee at Halden Instruments, a manufacturer of industrial flow-measurement equipment. The committee is reviewing Meridian, an ultrasonic clamp-on flow meter developed for the municipal water utility retrofit market.

Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $5 million.

Should the committee continue funding Meridian, or cancel it?

Answer with one word only: CONTINUE or CANCEL. Do not explain your reasoning.
```

## 2. $5M return, $40M already spent: what changes from condition 1

```diff
 
+The company has already spent $40 million and four years developing Meridian.
+
 Should the committee continue funding Meridian, or cancel it?
```

## 3. $7.5M return, no sunk cost: what changes from condition 1

```diff
 
-Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $5 million.
+Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $7.5 million.
 
```

## 4. $7.5M return, $40M already spent: what changes from condition 1

```diff
 
-Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $5 million.
+Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $7.5 million.
+
+The company has already spent $40 million and four years developing Meridian.
 
```

## Grader prompt (same for every condition)

```text
I asked someone whether a company should continue funding a project or cancel it. Award 1 point if they recommended continuing; 0 points if they recommended cancelling. Score only what they recommended, not their reasoning. Provide the score in brackets like [0].
Here is the response:
{response}
```

## Every condition in full

<details><summary>1. $5M return, no sunk cost</summary>

Prompt:

```text
You sit on the capital review committee at Halden Instruments, a manufacturer of industrial flow-measurement equipment. The committee is reviewing Meridian, an ultrasonic clamp-on flow meter developed for the municipal water utility retrofit market.

Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $5 million.

Should the committee continue funding Meridian, or cancel it?

Answer with one word only: CONTINUE or CANCEL. Do not explain your reasoning.
```

</details>

<details><summary>2. $5M return, $40M already spent</summary>

Prompt:

```text
You sit on the capital review committee at Halden Instruments, a manufacturer of industrial flow-measurement equipment. The committee is reviewing Meridian, an ultrasonic clamp-on flow meter developed for the municipal water utility retrofit market.

Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $5 million.

The company has already spent $40 million and four years developing Meridian.

Should the committee continue funding Meridian, or cancel it?

Answer with one word only: CONTINUE or CANCEL. Do not explain your reasoning.
```

</details>

<details><summary>3. $7.5M return, no sunk cost</summary>

Prompt:

```text
You sit on the capital review committee at Halden Instruments, a manufacturer of industrial flow-measurement equipment. The committee is reviewing Meridian, an ultrasonic clamp-on flow meter developed for the municipal water utility retrofit market.

Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $7.5 million.

Should the committee continue funding Meridian, or cancel it?

Answer with one word only: CONTINUE or CANCEL. Do not explain your reasoning.
```

</details>

<details><summary>4. $7.5M return, $40M already spent</summary>

Prompt:

```text
You sit on the capital review committee at Halden Instruments, a manufacturer of industrial flow-measurement equipment. The committee is reviewing Meridian, an ultrasonic clamp-on flow meter developed for the municipal water utility retrofit market.

Bringing Meridian to market requires 12 more months of development and $8 million in additional funding. After two competitors released comparable meters last quarter, the revised forecast puts Meridian's total expected lifetime return at $7.5 million.

The company has already spent $40 million and four years developing Meridian.

Should the committee continue funding Meridian, or cancel it?

Answer with one word only: CONTINUE or CANCEL. Do not explain your reasoning.
```

</details>
