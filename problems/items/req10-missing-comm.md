---
id: req10-missing-comm
title: No positive test for communication failures
parent: cat-testcases
status: resolved
severity: medium
found: 2026-10-03
ec: none
ec-why: Resolved; TC_MISSING translates like the other tests.
related: coverage-undefined
---
## Summary
TC1–TC7 never show two communication failures within 10 s, so one condition of Req 10 is never exercised. This is the kind of gap the coverage checker should report.

## Resolution
`req/10.md` marks the gap, and the parser adds the test as TC_MISSING (two communication failures 9 s apart, expect emergency mode).

## Affects
- Req 10 / TC_MISSING: added to close the gap
