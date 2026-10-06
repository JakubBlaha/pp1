---
id: negative-window-start
title: A time window can start before time 0
parent: cat-examples
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: In EC the window becomes a range for a time variable, so an early start causes no problem (`research/calculi.md`, §4).
related: strict-bounds
---
## Summary
In Req 10, $\mathit{MkIntervalOO}(\mathit{Now} - 10, \mathit{Now})$ starts outside the time set when $\mathit{Now} < 10$.

## Explanation
$T = \mathbb{R}_{\ge 0}$, so $\mathit{Now} - 10$ is not a time point for $\mathit{Now} < 10$. The count is still right, because nothing happens before time 0, but the interval is not well-formed.

A plain guard $\mathit{Now} \ge 10$ would be wrong: it would ignore TC2's failures at 0 s and 9 s. Clamping the open start to 0 would be wrong too, because it would exclude the failure at 0 s.

## Proposed fix
Use $[0, \mathit{Now})$ when $\mathit{Now} < 10$, and $(\mathit{Now} - 10, \mathit{Now})$ otherwise.

## Affects
- Req 10: the 10 s window

## Sources
- `tex-new/examples.tex`, Req 10 notes
