---
id: ec-aggregates
title: Counting and sets are outside first-order logic
parent: cat-ec
status: open
severity: medium
found: 2026-10-03
ec: work
ec-why: The translator has to rewrite counts with fixed bounds into first-order formulas; all current counts have fixed bounds.
related: only-if-gap
---
## Summary
$\mathit{Size}$, $\mathit{Filter}$, $\mathit{EvtOccCount}$, $\mathit{MaxVal}$ and $\mathit{MinVal}$ have no direct counterpart in the Event Calculus.

## Explanation
With a fixed bound they can be rewritten. Req 13's "at most 2 registers are greater than 10" becomes "there are no 3 different registers that are all greater than 10". A general count needs the tool's extras, such as `#count` in clingo.

## Proposed fix
Rewrite fixed bounds (all current examples have them); use the tool's aggregates otherwise.

## Affects
- Req 09: $\mathit{EvtOccCount} = 2$
- Req 10: $\mathit{EvtOccCount} \ge 1$
- Req 13: $\mathit{Size}$ and $\mathit{Filter}$

## Sources
- `research/calculi.md`, §3.2
