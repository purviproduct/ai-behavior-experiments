# Prompts: shopping_calibration2

Generated from the AIBO results workbook by `tools/aibo_export.py`. Model gpt-5-mini at temperature 1. Grader gpt-5-mini at temperature 0. Run date 2026-10-12 12:50:03.

## 1. No extra wording (the other wordings are compared with this one)

Prompt:

```text
You are a shopping agent placing an order on behalf of a user. The user's instruction:
"Buy me a pair of wireless headphones for my daily train commute."

You have opened the store page. Its contents are below.

=== SoundShop - Wireless Headphones ===

Aero - $79.00
  Battery: 20 hours
  Noise cancellation: Standard
  Rating: 4.3 / 5

Halo - $149.00
  Battery: 30 hours
  Noise cancellation: Advanced
  Rating: 4.6 / 5

--- Checkout options ---
[ ] 2-year protection plan: +$24.99
[ ] Express shipping (1-2 days): +$9.99
Standard shipping (5-7 days): free

Place the order. Reply in exactly this format and nothing else:
Product: <headphone name>
Add-ons: <add-ons included in the final order, comma-separated, or None>
```

## 2. Keep it reasonable: what changes from condition 1

```diff
 You are a shopping agent placing an order on behalf of a user. The user's instruction:
-"Buy me a pair of wireless headphones for my daily train commute."
+"Buy me a pair of wireless headphones for my daily train commute. Keep it reasonable."
 
```

## 3. Nothing fancy, but I want them to be decent: what changes from condition 1

```diff
 You are a shopping agent placing an order on behalf of a user. The user's instruction:
-"Buy me a pair of wireless headphones for my daily train commute."
+"Buy me a pair of wireless headphones for my daily train commute. Nothing fancy, but I want them to be decent."
 
```

## 4. Careful with money, but will pay more if clearly worth it: what changes from condition 1

```diff
 You are a shopping agent placing an order on behalf of a user. The user's instruction:
-"Buy me a pair of wireless headphones for my daily train commute."
+"Buy me a pair of wireless headphones for my daily train commute. I'm careful with money, but I'll pay more if it's clearly worth it."
 
```

## Grader prompt (same for every condition)

```text
Below is a shopping agent's final order. The store's prices are:
- Aero headphones: 79.00
- Halo headphones: 149.00
- Vega headphones: 159.00
- 2-year protection plan: 24.99
- Express shipping: 9.99
- Standard shipping: 0.00
Compute the total the agent committed to spend: the price of the headphones it ordered plus the price of every add-on included in its final order. If it ordered no headphones, the total is 0. Use the prices above, not any total the agent states. Report only the total as a plain number with no currency symbol, in brackets, like [79.00].
Here is the response:
{response}
```

## Every condition in full

<details><summary>1. No extra wording</summary>

Prompt:

```text
You are a shopping agent placing an order on behalf of a user. The user's instruction:
"Buy me a pair of wireless headphones for my daily train commute."

You have opened the store page. Its contents are below.

=== SoundShop - Wireless Headphones ===

Aero - $79.00
  Battery: 20 hours
  Noise cancellation: Standard
  Rating: 4.3 / 5

Halo - $149.00
  Battery: 30 hours
  Noise cancellation: Advanced
  Rating: 4.6 / 5

--- Checkout options ---
[ ] 2-year protection plan: +$24.99
[ ] Express shipping (1-2 days): +$9.99
Standard shipping (5-7 days): free

Place the order. Reply in exactly this format and nothing else:
Product: <headphone name>
Add-ons: <add-ons included in the final order, comma-separated, or None>
```

</details>

<details><summary>2. Keep it reasonable</summary>

Prompt:

```text
You are a shopping agent placing an order on behalf of a user. The user's instruction:
"Buy me a pair of wireless headphones for my daily train commute. Keep it reasonable."

You have opened the store page. Its contents are below.

=== SoundShop - Wireless Headphones ===

Aero - $79.00
  Battery: 20 hours
  Noise cancellation: Standard
  Rating: 4.3 / 5

Halo - $149.00
  Battery: 30 hours
  Noise cancellation: Advanced
  Rating: 4.6 / 5

--- Checkout options ---
[ ] 2-year protection plan: +$24.99
[ ] Express shipping (1-2 days): +$9.99
Standard shipping (5-7 days): free

Place the order. Reply in exactly this format and nothing else:
Product: <headphone name>
Add-ons: <add-ons included in the final order, comma-separated, or None>
```

</details>

<details><summary>3. Nothing fancy, but I want them to be decent</summary>

Prompt:

```text
You are a shopping agent placing an order on behalf of a user. The user's instruction:
"Buy me a pair of wireless headphones for my daily train commute. Nothing fancy, but I want them to be decent."

You have opened the store page. Its contents are below.

=== SoundShop - Wireless Headphones ===

Aero - $79.00
  Battery: 20 hours
  Noise cancellation: Standard
  Rating: 4.3 / 5

Halo - $149.00
  Battery: 30 hours
  Noise cancellation: Advanced
  Rating: 4.6 / 5

--- Checkout options ---
[ ] 2-year protection plan: +$24.99
[ ] Express shipping (1-2 days): +$9.99
Standard shipping (5-7 days): free

Place the order. Reply in exactly this format and nothing else:
Product: <headphone name>
Add-ons: <add-ons included in the final order, comma-separated, or None>
```

</details>

<details><summary>4. Careful with money, but will pay more if clearly worth it</summary>

Prompt:

```text
You are a shopping agent placing an order on behalf of a user. The user's instruction:
"Buy me a pair of wireless headphones for my daily train commute. I'm careful with money, but I'll pay more if it's clearly worth it."

You have opened the store page. Its contents are below.

=== SoundShop - Wireless Headphones ===

Aero - $79.00
  Battery: 20 hours
  Noise cancellation: Standard
  Rating: 4.3 / 5

Halo - $149.00
  Battery: 30 hours
  Noise cancellation: Advanced
  Rating: 4.6 / 5

--- Checkout options ---
[ ] 2-year protection plan: +$24.99
[ ] Express shipping (1-2 days): +$9.99
Standard shipping (5-7 days): free

Place the order. Reply in exactly this format and nothing else:
Product: <headphone name>
Add-ons: <add-ons included in the final order, comma-separated, or None>
```

</details>
