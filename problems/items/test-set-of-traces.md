---
id: test-set-of-traces
title: A test case does not produce one trace
parent: cat-tests
status: open
severity: major
found: 2026-10-04
ec: blocker
ec-why: A test case becomes an event list plus initial values in EC; the formalism must first say whether a test stands for one trace or for all the traces it allows.
related: coverage-undefined, stimulus-vs-system, ec-software-events
---
## Summary
`formalism.tex` says a test case "produces a concrete trace", but its setup and stimuli fix only some values, so a test case allows many traces.

## Explanation
The setup fixes values at time 0, and each stimulus fixes the values its effect predicate talks about. Everything else is left open, in particular everything the software does.

**Example (Req 10, TC2).** The stimuli are two sensor failures, at 0 s and at 9 s. Nothing in the test says what `emergency_mode` does, so the test allows traces where it becomes true at 9 s, at 20 s, or never.

A test case therefore stands for a **set of traces**:

$$\mathit{Traces}(\mathit{TC}) = \{\, \rho \in \Sigma^T \mid \rho(0) \text{ agrees with } \sigma_0, \text{ and the effect of every stimulus holds in } \rho \,\}$$

The assertions then say which of these traces the test expects.

## Fix
Replace "to produce a concrete trace" (Section "Requirements & Test cases" of `formalism.tex`) with the set-of-traces definition, and define the coverage checker over this set.

## Affects
- all: the coverage checker (goal 3) has no defined meaning until this is fixed

## Sources
- `research/findings.md`, "A test case does not produce one trace"
