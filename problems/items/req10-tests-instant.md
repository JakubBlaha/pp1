---
id: req10-tests-instant
title: Req 10 tests checked the mode at the instant of the second failure
parent: cat-testcases
status: resolved
severity: medium
found: 2026-10-05
ec: none
ec-why: Resolved; the assertions now read the value just after the failure.
related: timing-convention
caused-by: timing-convention
---
## Summary
Under the new timing convention, a mode the software sets at 9 s is visible only after 9 s, so an assertion on $\mathit{Val}_\rho(\mathit{emergency\_mode}, 9)$ could never hold. The parser's tests now use $\mathit{ValAfter}_\rho$.

## Resolution
pp1-parser commit bffb021: the helpers `entered(t)` and `not_entered(t)` read $\mathit{ValAfter}_\rho(\mathit{emergency\_mode}, t)$.

## Affects
- Req 10 / TC1: fixed
- Req 10 / TC2: fixed
- Req 10 / TC3: fixed
- Req 10 / TC4: fixed
- Req 10 / TC5: fixed
- Req 10 / TC6: fixed
- Req 10 / TC7: fixed
- Req 10 / TC_MISSING: fixed
