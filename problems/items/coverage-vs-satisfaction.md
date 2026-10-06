---
id: coverage-vs-satisfaction
title: Lesson: judge changes by coverage, not satisfaction
parent: cat-tests
status: closed
severity: minor
found: 2026-10-04
ec: none
ec-why: A lesson about what the formalism is for; it changes nothing in the translation.
related: reset-semantics, coverage-undefined
---
## Summary
We once added a rule to the formalism so that a requirement could be false in the model. Coverage never needed it. The rule was reverted and the lesson recorded in `CLAUDE.md`.

## Explanation
There are two different questions:
- **Coverage** (our goal): does some test exercise each part of the requirement?
- **Satisfaction**: given the test's inputs, is the requirement true or false?

For coverage, what the test controls (setup, stimuli) decides which conditions are made true, and what the software or hardware does comes from the test's assertions. The formalism does not need to model the behaviour of the software or the hardware.

**Example.** Req 02's "the value survives a reset" can never be false in the model, so we added a rule saying that a reset clears volatile memory. But a coverage checker only needs to see that a test fires a reset and checks the value afterwards.

## Resolution
The reset rule was reverted on 4 Oct 2026. `CLAUDE.md` now asks, before any new semantics is added: does the coverage checker need this to decide which tests exercise which conditions?

## Affects
- Req 02: the reset part of the requirement

## Sources
- `CLAUDE.md`, "The goal is coverage, not satisfaction"
