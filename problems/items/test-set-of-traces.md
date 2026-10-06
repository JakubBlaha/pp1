---
id: test-set-of-traces
title: A test case does not produce one trace
parent: cat-tests
status: resolved
severity: major
found: 2026-10-04
ec: blocker
ec-why: Resolved: a test case now stands for the set of traces it allows, which EC can encode as initial values plus the test's events. Which of those events are fixed exactly is still open ("Events happen when the test fires them, but not only then").
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

## Resolution
Applied on 6 Oct 2026 in `tex-new/formalism.tex`, Section "Requirements & Test cases":
- The sentence "to produce a concrete trace" is replaced by a paragraph saying that a test case stands for the set of traces it allows, with the Req 10 example.
- New Definition "Traces of a test case": $\mathit{Traces}(\mathit{TC})$ contains the traces that agree with the setup at time 0 and satisfy the effect of every stimulus; $\mathit{Expected}(\mathit{TC})$ contains those in which every assertion holds.

Still open, as separate problems: an effect says that an event happens when the test fires it, not only then ("Events happen when the test fires them, but not only then"), and what the checker computes over these sets ("What the coverage checker computes is not defined").

## Affects
- all: the coverage checker (goal 3) has no defined meaning until this is fixed

## Sources
- `research/findings.md`, "A test case does not produce one trace"
