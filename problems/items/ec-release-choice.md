---
id: ec-release-choice
title: Which values to release does not follow from the entity type
parent: ec-software-events
status: open
severity: minor
found: 2026-10-04
ec: none
ec-why: Only matters for the alternative fix (releasing values); the general fix (opening events) does not need it.
related: stimulus-vs-system, ec-kind1
caused-by: stimulus-vs-system
---
## Summary
Releasing a value from the frame rule (the alternative fix for Kind 1) is right for `counter_1` but wrong for `Switch_b`, although both are Signals.

## Explanation
`Switch_b` (Req 01) is set by the test and must keep its value between two of the test's stimuli. `counter_1` is computed by the software. The translation therefore needs to know which side controls a value, which the formalism does not record.

## Proposed fix
Use the test/software classification from "Who performs an event is not recorded", or prefer the general fix (open events), which needs no decision per value.

## Affects
- Req 01: `Switch_b` versus `EngagementNoSat_u`
- Req 11: `counter_1`

## Sources
- `research/calculi.md`, §3.1, "Fix for this value only"
