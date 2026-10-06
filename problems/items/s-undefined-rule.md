---
id: s-undefined-rule
kind: solution
title: Give undefined values a fixed meaning
status: proposed
solves: undefined-values
partly-solves: req10-empty-setup, addr-undefined
---
## Summary
Decide what a comparison with an undefined operand means, and avoid undefined values where they are not intended.

## Change
1. Rule: a comparison ($\mathit{Cmp}$, $\mathit{Contains}$, …) with an undefined operand is false.
2. Recurrences over $\mathit{Prev}(\mathit{Now})$ are guarded with $\mathit{Now} > 0$, or state their first step separately, like Lustre's `->`.
3. Test cases give a setup value to every entity they compare.

## Example
Req 01 becomes $\mathit{Initial}(\ldots) \land \mathit{Always}(\mathit{Now} > 0 \Rightarrow \ldots)$.

## Affects
- Req 01: guard the recurrence
- Req 04: comparisons with undefined addresses become simply false
- Req 11: guard the recurrence
- Req 10: tests need setup values
