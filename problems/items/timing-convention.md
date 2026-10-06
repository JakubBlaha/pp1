---
id: timing-convention
title: When an operation's effect becomes visible
parent: cat-time
status: resolved
severity: major
found: 2026-10-03
ec: blocker
ec-why: Resolved: effects now start after the firing time, as in EC, so $\mathit{Val}_\rho$ and $\mathit{ValAfter}_\rho$ map to `HoldsAt` at $t$ and just after $t$.
related: valafter-pitfall, req10-tests-instant, parser-outdated
---
## Summary
Resolved on 3 Oct 2026 by adopting the Event Calculus convention: an operation's effect holds strictly after the firing time.

## Explanation
Take `write(5, x, 7)`, where `x` was 3:

| Time | 4 | 5 | 6 |
|---|---|---|---|
| Old convention, effect on $[t, t_{\mathit{next}})$ | 3 | 7 | 7 |
| New convention, effect on $(t, t_{\mathit{next}}]$ | 3 | 3 | 7 |

At a firing time, $\mathit{Val}_\rho$ now gives the value **before** the operation. The value after it is $\mathit{ValAfter}_\rho$:

$$\mathit{ValAfter}_\rho(e, t) = \begin{cases} \mathit{Val}_\rho(e, \mathit{Next}(t)) & \text{if } T = T_D \\ \lim_{t' \to t^+} \mathit{Val}_\rho(e, t') & \text{if } T = T_C \end{cases}$$

The left limit $\mathit{ValBefore}_\rho$ was removed, because $\mathit{Val}_\rho$ at a firing time already gives the old value.

## Resolution
- `formalism.tex` and `CHANGELOG.md`: commit 50d4b25.
- `examples.tex`: Req 02, 03, 05, 07 and 09 read written values with $\mathit{ValAfter}_\rho$.
- Parser: synced in pp1-parser commit bffb021.

## Affects
- Req 02: updated to $\mathit{ValAfter}_\rho$
- Req 03: updated to $\mathit{ValAfter}_\rho$
- Req 05: updated to $\mathit{ValAfter}_\rho$
- Req 07: updated to $\mathit{ValAfter}_\rho$
- Req 09: updated to $\mathit{ValAfter}_\rho$

## Sources
- `CHANGELOG.md`, 3 Oct 2026
