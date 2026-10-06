---
id: s-ec-release
kind: solution
title: Release software-computed values from the frame rule
status: proposed
partly-solves: ec-kind1
needs: s-controlled-by
alternative-to: s-ec-open-events
---
## Summary
An alternative for values the software recomputes at every step: exempt them from the frame rule instead of opening events.

## Change
Add $\mathit{ReleasedAt}(\mathit{value}(e) = v, t)$ for all $v$ and $t$, for every software-computed Signal $e$.

## Trade-offs
A released value has no `calculate` events, so a requirement that refers to such an event can never be satisfied. Only useful for Kind 1.

## Affects
- Req 01: `EngagementNoSat_u`
- Req 11: `counter_1`
