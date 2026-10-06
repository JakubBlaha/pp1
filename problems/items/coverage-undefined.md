---
id: coverage-undefined
title: What the coverage checker computes is not defined
parent: test-set-of-traces
status: open
severity: major
found: 2026-10-04
ec: none
ec-why: Coverage is computed on top of the translation; translating needs no coverage rule.
related: software-only-conditions, coverage-vs-satisfaction, parser-no-semantics
caused-by: stimulus-vs-system
---
## Summary
Goal 3 needs a rule for when a test *exercises* a condition of a requirement. The formalism has none yet.

## Explanation
Once a test case is a set of traces, a condition can be true in **all** of the test's traces, in **some**, or in **none**. The checker needs a rule saying which of these counts as "exercised".

**Example (Req 10).**
- TC2 (two sensor failures 9 s apart): the sensor condition is true at 9 s in every trace of the test, so TC2 exercises it.
- TC3 (11 s apart): the condition is false in every trace (once "Events happen when the test fires them, but not only then" is fixed), so TC3 exercises the "too far apart" case.

Unique First Cause coverage (Whalen et al., ISSTA 2006) is a ready-made reference: it defines one coverage obligation per condition of an LTL formula.

## Proposed fix
A condition counts as exercised if it holds in **every** trace of the test, which can be decided from the setup and the stimuli. Whether the expected response follows is checked by the test's assertions. Conditions that only the software can make true need a different rule (see "Some conditions consist only of software behaviour").

## Affects
- all: no requirement can be checked for coverage yet

## Sources
- `research/findings.md`, "A test case does not produce one trace", item 3 of "To decide later"
- `research/related-formalisms.md`, §10 (UFC coverage)
