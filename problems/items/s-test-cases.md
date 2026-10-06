---
id: s-test-cases
kind: solution
title: Check absence over a window and pin assertions to the right time
status: proposed
solves: req10-negative-instant, example-assertion-weak
needs: s-state-model
---
## Summary
Make the negative tests and the Req 08 example test check what they mean to check. Not needed for the translation.

## Change
- Negative Req 10 tests: assert that no `entered` event of emergency mode happens in $(t, t + d]$, for a chosen $d$.
- The Req 08 example test: assert $\mathit{EvtOccCount}_\rho(\mathit{ev\_entered\_backup}, \mathit{MkIntervalCC}(1, 2)) \ge 1$.

## Affects
- Req 08 / TC1: the example test in `research/findings.md`
- Req 10 / TC1: absence window
- Req 10 / TC3: absence window
- Req 10 / TC5: absence window
- Req 10 / TC6: absence window
- Req 10 / TC7: absence window
