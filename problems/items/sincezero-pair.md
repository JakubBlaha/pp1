---
id: sincezero-pair
title: SinceZero returns a pair, not an interval
parent: cat-definitions
status: open
severity: minor
found: 2026-10-03
ec: blocker
ec-why: `SinceZero` returns a pair where an interval is expected, so it has no well-typed translation. No current requirement uses it.
related: openness-ignored
---
## Summary
$\mathit{SinceZero}(t) = (0, t)$, but intervals are 4-tuples $(t, d, \ell, r)$: start, duration and two openness flags.

## Proposed fix
Define $\mathit{SinceZero}(t) = \mathit{MkIntervalCC}(0, t)$.

## Affects
- none

## Sources
- `research/calculi.md`, §6
