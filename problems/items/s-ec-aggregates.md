---
id: s-ec-aggregates
kind: solution
title: Rewrite fixed-bound counts; use tool aggregates otherwise
status: proposed
solves: ec-aggregates
---
## Summary
Counting and set functions become first-order formulas when the bound is a constant, which holds for all current examples.

## Change
- $\mathit{Size}(\mathit{Filter}(S, P)) \le k$ becomes "there are no $k + 1$ distinct $x \in S$ with $P(x)$".
- $\mathit{EvtOccCount}(ev, i) \ge k$ becomes "$k$ distinct occurrences of $ev$ in $i$".
- Counts that are not constants use the tool's aggregates (`#count` in clingo, `findall` in Prolog).

## Affects
- Req 09: $\mathit{EvtOccCount} = 2$
- Req 10: $\mathit{EvtOccCount} \ge 1$
- Req 13: $\mathit{Size}$ and $\mathit{Filter}$
