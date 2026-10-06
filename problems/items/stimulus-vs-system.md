---
id: stimulus-vs-system
title: Who performs an event is not recorded
parent: cat-actors
status: proposed
severity: major
found: 2026-10-04
ec: blocker
ec-why: The translation must know which events happen exactly as the test lists them and which the software may produce at any time; the formalism does not record this.
related: only-if-gap, system-boundary, software-only-conditions, ec-software-events, channel-design, t-next-from-stimuli, d-signal-write
---
## Summary
The formalism does not say whether an event or a value change comes from the test (a stimulus) or from the software. Several other problems trace back to this.

## Explanation
The same mechanism, an `EventTrigger` fired with `fire`, is used for things the test does and for things the software does:

| Done by the test | Done by the software |
|---|---|
| sensor, energy and communication failures (Req 10) | invoking the exception handler (Req 05) |
| processor power-up (Req 06) | starting the task sequence (Req 06) |
| the exception (Req 05) | the end of initialisation (Req 07) |

The difference matters in two places:
- **Coverage:** stimuli decide which conditions a test makes true; the software's behaviour can only be checked by assertions.
- **Event Calculus translation:** the test's events must happen exactly as listed, the software's events must be free to happen.

**Example (Req 09).** It is not recorded whether the test or the software writes `d`, yet it decides whether a test can make the condition true at all.

## Proposed fix
1. Operations are performed only by the test: they are exactly the stimuli.
2. Each entity declares whether the **test** or the **software** controls it. Operations may only target test-controlled entities.
3. Events on test-controlled entities happen **exactly** when the test's operations produce them.

This is safe for our requirements: no requirement constraint uses an operation, and every entity is controlled by one side only. Only `d` and the peak detections in Req 09 need a decision (see "Test- or software-controlled depends on the system boundary").

## Affects
- all: every requirement mixes things the test does with things the software does
- Req 05: invoking the handler, its return and holding execution are software events modelled as `EventTrigger`s
- Req 06: starting the task sequence is a software event modelled as an `EventTrigger`
- Req 07: the end of initialisation is a software event modelled as an `EventTrigger`
- Req 09: it is open who writes `d` and who detects the peaks

## Sources
- `research/findings.md`, first finding, item 2 of "To decide later"
- `research/calculi.md`, §3.1
