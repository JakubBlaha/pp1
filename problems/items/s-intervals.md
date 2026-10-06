---
id: s-intervals
kind: solution
title: Make interval functions respect open and closed ends
status: proposed
solves: openness-ignored, sincezero-pair
---
## Summary
Define all interval functions through $\mathit{InInterval}$, and make $\mathit{SinceZero}$ return a proper interval.

## Change
- $\mathit{MaxVal}$, $\mathit{MinVal}$, $\mathit{IntervalIncludes}$, $\mathit{IntervalExcludes}$, $\mathit{StartOfFirstIntervalIn}$ and $\mathit{EndOfFirstIntervalIn}$: use $\mathit{InInterval}$ instead of comparing end points.
- $\mathit{SinceZero}(t) = \mathit{MkIntervalCC}(0, t)$.

## Affects
- none
