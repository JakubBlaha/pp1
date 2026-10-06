---
id: software-only-conditions
title: Some conditions consist only of software behaviour
parent: stimulus-vs-system
status: open
severity: medium
found: 2026-10-05
ec: none
ec-why: Such conditions translate like any other; the open question is how coverage treats them.
related: coverage-undefined, ec-kind3, system-boundary
---
## Summary
When a requirement's condition is made only of things the software does, no stimulus can make it true. A test can only observe it.

## Explanation
**Example (Req 13).** "When the four registers are written at the same timestep": the writes are done by the software. A test can provide inputs that lead to the writes and assert that they happened, but it cannot write the registers itself without doing the software's job.

The same holds for:
- Req 07: the end of initialisation;
- Req 11: entering emergency mode;
- Req 05: the handler returning (the `Causes` part);
- Req 09, if `d` and the peak detections turn out to be the software's.

The rule from `CLAUDE.md` says that stimuli decide which conditions are made true. For these conditions, nothing the test controls does.

## Proposed fix
Let the coverage definition use assertions to establish that such a condition occurred (an "observed condition"), so that a test which sees the four simultaneous writes counts as exercising Req 13.

## Affects
- Req 05: the `Causes` part (the handler returns)
- Req 07: the end of initialisation
- Req 09: only if `d` and the peak detections belong to the software
- Req 11: entering emergency mode
- Req 13: the four simultaneous writes

## Sources
- `research/calculi.md`, §3.1, Kind 3
