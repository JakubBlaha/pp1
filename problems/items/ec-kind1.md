---
id: ec-kind1
title: Kind 1: the requirement can no longer be satisfied
parent: ec-software-events
status: proposed
severity: major
found: 2026-10-04
ec: blocker
ec-why: Req 01 and Req 11 translate to unsatisfiable theories.
related: ec-release-choice
---
## Summary
A value that only the software computes is frozen by the frame rule, which contradicts the requirement.

## Explanation
**Example (Req 11).** No event ever changes `counter_1`, so the frame rule keeps it at 0, while the requirement demands 3, 6, 9, …:

$$\mathit{Always}\bigl(\mathit{HasHappened}_\rho(\mathit{ev\_enter\_emergency}, \mathit{Now}) \Rightarrow \mathit{Val}_\rho(\mathit{counter\_1}, \mathit{Now}) = \mathit{Val}_\rho(\mathit{counter\_1}, \mathit{Prev}(\mathit{Now})) + 3\bigr)$$

## Proposed fix
The general fix: let `calculate(counter_1, V)` happen at any time. Alternatively, *release* the value from the frame rule ($\mathit{ReleasedAt}$ in EC).

## Affects
- Req 01: `EngagementNoSat_u`
- Req 11: `counter_1`

## Sources
- `research/calculi.md`, §3.1, Kind 1
