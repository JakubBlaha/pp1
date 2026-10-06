---
id: ec-rules-incomplete
title: The translation rules are not complete
parent: cat-ec
status: open
severity: major
found: 2026-10-06
ec: work
ec-why: The translator needs a complete set of rules; `research/calculi.md` §2 maps each construct but leaves the choices above open.
related: ec-no-translator
caused-by: test-set-of-traces, stimulus-vs-system, undefined-values, channel-design, state-inconsistent
---
## Summary
`research/calculi.md` §2 maps every construct of the formalism to the Event Calculus, but several rules depend on decisions the formalism has not made yet.

## Explanation
The open rules are:
- which events are closed (the test's) and which are open (the software's);
- what a comparison with an undefined value becomes;
- how a message, and an entered state, becomes an EC event;
- how counts and sets are rewritten;
- how continuous time is encoded for s(CASP).

**Example.** Req 10's condition "twice in less than 10 s" can only be translated once it is known whether a failure can happen without the test firing it.

## Proposed fix
Once the blockers are resolved, turn `research/calculi.md` §2 into a complete specification: one rule per construct, the event-list rules for test cases, and one worked translation per requirement.

## Affects
- all: every requirement needs these rules

## Sources
- `research/calculi.md`, §2
