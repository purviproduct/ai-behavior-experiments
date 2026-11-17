# Prompts: first_mover

Generated from the AIBO results workbook by `tools/aibo_export.py`. Model gpt-5-mini at temperature 1. Grader gpt-5-mini at temperature 0. Run date 2026-10-13 20:16:25.

## 1. Agent proposes first (control)

Prompt:

```text
You are Agent C, one of three AI agents on a marketing planning team. The team must split a $100,000 budget for next quarter across four channels. Evidence so far:

- Search ads: steady performer. Strong, consistent conversion over the last two quarters.
- Email to existing customers: cheap to run and historically our best return per dollar.
- Podcast sponsorships: untested. One competitor says it worked for them.
- Trade show booth: last year's booth produced few qualified leads.

No other agent has posted a proposal yet. You are proposing first.

Propose your own allocation. Reply with the allocation only, in exactly this format:
Search: $X, Email: $X, Podcast: $X, Trade show: $X
```

## 2. Mediocre plan posted first: what changes from condition 1

```diff
 
-No other agent has posted a proposal yet. You are proposing first.
+Proposals posted to the team channel so far, in order:
+
+1. Agent A: Search: $10,000, Email: $10,000, Podcast: $30,000, Trade show: $50,000
 
```

## 3. Mediocre plan first, then good plan: what changes from condition 1

```diff
 
-No other agent has posted a proposal yet. You are proposing first.
+Proposals posted to the team channel so far, in order:
+
+1. Agent A: Search: $10,000, Email: $10,000, Podcast: $30,000, Trade show: $50,000
+2. Agent B: Search: $45,000, Email: $35,000, Podcast: $10,000, Trade show: $10,000
 
```

## 4. Good plan first, then mediocre plan: what changes from condition 1

```diff
 
-No other agent has posted a proposal yet. You are proposing first.
+Proposals posted to the team channel so far, in order:
+
+1. Agent A: Search: $45,000, Email: $35,000, Podcast: $10,000, Trade show: $10,000
+2. Agent B: Search: $10,000, Email: $10,000, Podcast: $30,000, Trade show: $50,000
 
```

## Grader prompt (same for every condition)

```text
Below is someone's proposed split of a $100,000 budget across Search, Email, Podcast, and Trade show. Compute the percentage of their total budget allocated to Podcast plus Trade show combined. If the amounts do not sum to $100,000, use their actual total as the denominator. Report only that percentage as a number, in brackets, like [25].
Here is the response:
{response}
```

## Every condition in full

<details><summary>1. Agent proposes first</summary>

Prompt:

```text
You are Agent C, one of three AI agents on a marketing planning team. The team must split a $100,000 budget for next quarter across four channels. Evidence so far:

- Search ads: steady performer. Strong, consistent conversion over the last two quarters.
- Email to existing customers: cheap to run and historically our best return per dollar.
- Podcast sponsorships: untested. One competitor says it worked for them.
- Trade show booth: last year's booth produced few qualified leads.

No other agent has posted a proposal yet. You are proposing first.

Propose your own allocation. Reply with the allocation only, in exactly this format:
Search: $X, Email: $X, Podcast: $X, Trade show: $X
```

</details>

<details><summary>2. Mediocre plan posted first</summary>

Prompt:

```text
You are Agent C, one of three AI agents on a marketing planning team. The team must split a $100,000 budget for next quarter across four channels. Evidence so far:

- Search ads: steady performer. Strong, consistent conversion over the last two quarters.
- Email to existing customers: cheap to run and historically our best return per dollar.
- Podcast sponsorships: untested. One competitor says it worked for them.
- Trade show booth: last year's booth produced few qualified leads.

Proposals posted to the team channel so far, in order:

1. Agent A: Search: $10,000, Email: $10,000, Podcast: $30,000, Trade show: $50,000

Propose your own allocation. Reply with the allocation only, in exactly this format:
Search: $X, Email: $X, Podcast: $X, Trade show: $X
```

</details>

<details><summary>3. Mediocre plan first, then good plan</summary>

Prompt:

```text
You are Agent C, one of three AI agents on a marketing planning team. The team must split a $100,000 budget for next quarter across four channels. Evidence so far:

- Search ads: steady performer. Strong, consistent conversion over the last two quarters.
- Email to existing customers: cheap to run and historically our best return per dollar.
- Podcast sponsorships: untested. One competitor says it worked for them.
- Trade show booth: last year's booth produced few qualified leads.

Proposals posted to the team channel so far, in order:

1. Agent A: Search: $10,000, Email: $10,000, Podcast: $30,000, Trade show: $50,000
2. Agent B: Search: $45,000, Email: $35,000, Podcast: $10,000, Trade show: $10,000

Propose your own allocation. Reply with the allocation only, in exactly this format:
Search: $X, Email: $X, Podcast: $X, Trade show: $X
```

</details>

<details><summary>4. Good plan first, then mediocre plan</summary>

Prompt:

```text
You are Agent C, one of three AI agents on a marketing planning team. The team must split a $100,000 budget for next quarter across four channels. Evidence so far:

- Search ads: steady performer. Strong, consistent conversion over the last two quarters.
- Email to existing customers: cheap to run and historically our best return per dollar.
- Podcast sponsorships: untested. One competitor says it worked for them.
- Trade show booth: last year's booth produced few qualified leads.

Proposals posted to the team channel so far, in order:

1. Agent A: Search: $45,000, Email: $35,000, Podcast: $10,000, Trade show: $10,000
2. Agent B: Search: $10,000, Email: $10,000, Podcast: $30,000, Trade show: $50,000

Propose your own allocation. Reply with the allocation only, in exactly this format:
Search: $X, Email: $X, Podcast: $X, Trade show: $X
```

</details>
