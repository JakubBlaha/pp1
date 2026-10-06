---
id: ec-software-events
title: In the Event Calculus, nothing the software does ever happens
parent: cat-ec
status: proposed
severity: major
found: 2026-10-04
ec: blocker
ec-why: This is the core of the translation scheme: unless the software's events are opened, most requirements translate to theories that contradict their tests.
related: stimulus-vs-system, test-set-of-traces
caused-by: stimulus-vs-system
---
## Summary
EC tools assume a frame rule and a complete event list. For a test case the event list is its stimuli, so the software's events never happen and the values it changes never change.

## Explanation
- **Frame rule:** a value changes only when an event changes it.
- **Complete event list:** only the events in the event list happen. (The EC literature calls the event list the *narrative*, and reads it with `Happens` minimised.)

**Example (Req 10, TC2).** The event list is the two sensor failures. Entering emergency mode is the software's event, so it never happens and `emergency_mode` stays false; TC2's expected outcome is impossible.

Depending on where the software's contribution sits in the formula, this shows up in three ways (the sub-problems).

## Proposed fix
Apply the complete-event-list assumption only to the test's events: stimulus events happen exactly as listed, system events may happen at any time. In ASP this is a choice rule:

```
{ happens(set_state(emergency_mode, V), T) }.
```

EC planners use the same technique for the actions they may choose.

## Affects
- all: every requirement has at least one value or event that the software produces

## Sources
- `research/calculi.md`, §3.1
