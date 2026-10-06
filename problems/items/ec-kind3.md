---
id: ec-kind3
title: Kind 3: the requirement becomes automatically true
parent: ec-software-events
status: proposed
severity: major
found: 2026-10-05
ec: blocker
ec-why: Req 05, Req 07 and Req 13 translate to theories that hold whatever the software does.
related: software-only-conditions
---
## Summary
A software event in the *condition* never happens, so the condition is never true and the requirement holds whatever the software does.

## Explanation
**Example (Req 13).**

$$\mathit{Always}\bigl(\mathit{ForAll}(\mathit{writes}, \lambda \mathit{ev}.\ \mathit{Happening}(\mathit{ev}, \mathit{Now})) \Rightarrow \mathit{Size}(\mathit{Filter}(\mathit{regs}, \lambda e.\ \mathit{ValAfter}_\rho(e, \mathit{Now}) > 10)) \le 2\bigr)$$

The writes are the software's, so they never happen. Software that writes 11 into all four registers would pass.

## Proposed fix
The general fix: once the software's events may happen, the condition can become true.

## Affects
- Req 05: the `Causes` part (the handler returns)
- Req 07: the end of initialisation
- Req 13: the four simultaneous writes

## Sources
- `research/calculi.md`, §3.1, Kind 3
