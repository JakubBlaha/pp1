---
id: s-valafter-lint
kind: solution
title: Guard against Val where ValAfter is meant
status: proposed
solves: valafter-pitfall
---
## Summary
Tell the LLM the rule, and let the parser catch the mistake.

## Change
- Prompting guidance: "at the time of an event, read the new value with $\mathit{ValAfter}_\rho$".
- Parser lint: warn when $\mathit{Val}_\rho(e, \mathit{Now})$ appears in a conjunction with $\mathit{Happening}(ev, \mathit{Now})$ where $ev$ targets $e$.

## Affects
- none
