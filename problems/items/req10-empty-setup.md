---
id: req10-empty-setup
title: Req 10 tests leave emergency_mode undefined
parent: cat-testcases
status: open
severity: minor
found: 2026-10-05
ec: blocker
ec-why: Without setup values the initial state is unknown, so the Req 10 assertions translate to comparisons with undefined values.
related: undefined-values
caused-by: undefined-values
---
## Summary
The tests have no setup, so `emergency_mode` starts undefined, and the negative tests compare an undefined value.

## Proposed fix
Set `emergency_mode = false` in every test's setup.

## Affects
- Req 10 / TC1: no setup value
- Req 10 / TC2: no setup value
- Req 10 / TC3: no setup value
- Req 10 / TC4: no setup value
- Req 10 / TC5: no setup value
- Req 10 / TC6: no setup value
- Req 10 / TC7: no setup value
- Req 10 / TC_MISSING: no setup value
