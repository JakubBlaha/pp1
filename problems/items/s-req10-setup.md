---
id: s-req10-setup
kind: solution
title: Give the Req 10 tests setup values
status: proposed
solves: req10-empty-setup
---
## Summary
Start every Req 10 test from a known state, so its assertions never compare with an undefined value.

## Change
Set `emergency_mode = false` (or the initial state of the mode machine) in the setup of TC1–TC7 and TC_MISSING, in `req/10.md` and `pp1-parser/examples/10.py`.

## Affects
- Req 10 / TC1: setup value
- Req 10 / TC2: setup value
- Req 10 / TC3: setup value
- Req 10 / TC4: setup value
- Req 10 / TC5: setup value
- Req 10 / TC6: setup value
- Req 10 / TC7: setup value
- Req 10 / TC_MISSING: setup value
