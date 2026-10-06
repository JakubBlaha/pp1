---
id: openness-ignored
title: Some interval functions ignore open and closed ends
parent: cat-definitions
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: These functions translate as they are defined; if the definitions are corrected, the translation rules change with them.
related: sincezero-pair
---
## Summary
$\mathit{MaxVal}$, $\mathit{MinVal}$, $\mathit{IntervalIncludes}$, $\mathit{IntervalExcludes}$, $\mathit{StartOfFirstIntervalIn}$ and $\mathit{EndOfFirstIntervalIn}$ compare start and end points directly, ignoring whether an interval is open or closed.

## Explanation
For example,

$$\mathit{MaxVal}_\rho(e, i) = \sup\{\, \mathit{Val}_\rho(e, s) \mid \mathit{Start}(i) \le s \le \mathit{End}(i) \,\}$$

also includes the end points of an open interval. $\mathit{EvtOccCount}$, in contrast, uses $\mathit{InInterval}$ and respects them.

## Proposed fix
Define these functions with $\mathit{InInterval}$.

## Affects
- none

## Sources
- `research/calculi.md`, §6
