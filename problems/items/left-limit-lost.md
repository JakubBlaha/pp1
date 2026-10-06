---
id: left-limit-lost
title: The value just before a change cannot be named for free signals
parent: timing-convention
status: open
severity: minor
found: 2026-10-04
ec: none
ec-why: No current requirement needs the value just before a change.
related: timing-convention
---
## Summary
Since $\mathit{ValBefore}_\rho$ was removed, a continuous-time signal that changes exactly at $t$ has no way to name its value just before $t$.

## Explanation
Operations never cause this: their effects start after $t$, so $\mathit{Val}_\rho(e, t)$ is the old value. But a value no operation touches is unconstrained and may jump *at* $t$:

| Time | 4.9 | 4.99 | 5.0 | 5.01 |
|---|---|---|---|---|
| Value | 3 | 3 | 7 | 7 |

Here $\mathit{Val}_\rho(s, 5) = 7$, and the 3 can no longer be named.

## Proposed fix
Require well-formed traces: every value is piecewise constant, changes only finitely often in any bounded interval, and every constant piece has the form $(t_i, t_{i+1}]$. Then $\mathit{Val}_\rho(e, t)$ always equals the left limit.

## Affects
- none
