---
id: ec-kind2
title: Kind 2: a test's expected outcome becomes impossible
parent: ec-software-events
status: proposed
severity: major
found: 2026-10-04
ec: blocker
ec-why: The expected outcomes of the tests become impossible in the translation.
related: ec-kind1, ec-kind3
---
## Summary
A software event or value change that a test expects never happens.

## Explanation
**Example (Req 06).** The test powers up the processor, but starting the task sequence is the software's event. It never happens, so a test expecting the tasks to start within 2 s cannot pass. Req 06 has no values at all, so the problem is not only about values.

## Proposed fix
The general fix: the software's events may happen at any time.

## Affects
- Req 02: storing into `MEASUREMT_BLOCK`
- Req 03: the read and the write
- Req 04: configuring the IVOR registers
- Req 05: the `Sequence` part
- Req 06: starting the task sequence
- Req 08: entering Backup
- Req 09: toggling `valid_range`
- Req 10: entering emergency mode
- Req 10 / TC2: the expected outcome is impossible
- Req 10 / TC4: the expected outcome is impossible
- Req 10 / TC_MISSING: the expected outcome is impossible
- Req 12: once formalised

## Sources
- `research/calculi.md`, §3.1, Kind 2
