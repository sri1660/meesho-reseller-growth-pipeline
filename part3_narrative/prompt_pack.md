# Meesho Reseller Growth Monitoring — Prompt Pack

## Trigger

Generate a stakeholder narrative when a category's Month-on-Month (MoM) revenue change is classified as `"flagged"` by the Part 2 growth engine.

The trigger condition is:

`is_flagged(mom_pct) == "flagged"`

---

## Input List

The narrative template receives only verified values from the Part 1 SQL output and Part 2 growth engine.

* `{category}` — category name
* `{previous_revenue}` — verified revenue for the previous month
* `{current_revenue}` — verified revenue for the current month
* `{mom_pct}` — verified Month-on-Month growth percentage
* `{month}` — current month
* `{prev_month}` — previous month

---

## Prompt

You are preparing a stakeholder update for a Meesho category or regional manager.

Use only the verified input values supplied to you. Do not invent, estimate, round, or modify any number.

### Context

Explain what category is being measured and which two months are being compared.

### Insight — Fact

State the verified revenue movement and the exact supplied MoM percentage.

The percentage must be reproduced exactly from `{mom_pct}`.

Do not introduce any numerical value that is not present in the supplied inputs.

### Implication — Hypothesis

Provide a specific and actionable recommendation.

If you suggest a possible reason for the change, label it explicitly as a **Hypothesis**, because the supplied revenue data alone does not prove the cause.

The final narrative should be concise and suitable for a stakeholder or regional manager.

---

## Checklist

Before the narrative is used:

1. **Number validation:** Every number in the narrative must match a supplied input value exactly.
2. **Fact validation:** Every statement labeled as a fact must be supported by the verified Part 1 or Part 2 output.
3. **Hypothesis validation:** Any proposed cause must be labeled as a hypothesis rather than presented as a proven fact.
4. **Actionability validation:** The recommendation must identify a specific next action rather than using a vague instruction such as "look into it."
5. **Privacy validation:** No raw reseller name may appear in an externally facing narrative; reseller references must use the required alias format.
6. **Completeness validation:** The narrative must contain Context, Insight, and Implication.
