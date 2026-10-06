---
id: example-assertion-weak
title: The Req 08 example test checks Backup too loosely
parent: cat-testcases
status: open
severity: minor
found: 2026-10-05
ec: none
ec-why: Translates as written; the assertion is only too weak.
related: receive-content
---
## Summary
The example TC1 in `research/findings.md` asserts $\mathit{HasHappened}(\mathit{ev\_entered\_backup}, 2)$, which also holds if Backup was entered *before* the message arrived at 1 s.

## Proposed fix
Assert $\mathit{EvtOccCount}_\rho(\mathit{ev\_entered\_backup}, \mathit{MkIntervalCC}(1, 2)) \ge 1$ instead.

## Affects
- Req 08 / TC1: the example test in `research/findings.md`
