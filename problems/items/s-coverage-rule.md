---
id: s-coverage-rule
kind: solution
title: Define when a test exercises a condition
status: proposed
solves: coverage-undefined, software-only-conditions
needs: s-test-semantics, s-controlled-by
---
## Summary
A condition of a requirement is exercised by a test if it holds in every trace the test allows. A condition made only of software behaviour is exercised when the test's assertions observe it.

## Change
1. Split each requirement into its conditions (the antecedents of $\mathit{Causes}$, $\mathit{CausesWithin}$, $\mathit{Always}(\ldots \Rightarrow \ldots)$ and so on), with one coverage obligation per condition, in the spirit of Unique First Cause coverage.
2. A condition over test-controlled entities is exercised if it is true in every trace of $\mathit{Traces}(\mathit{TC})$; this is decided from the setup and the stimuli.
3. A condition over software-controlled entities is exercised if the test asserts that it occurred (an "observed condition").
4. Whether the response follows is checked by the test's assertions.

## Example
Req 10: TC2 exercises the sensor condition (two failures 9 s apart, in every trace), and TC3 its negation. Req 13: a test exercises the condition only if it asserts that all four registers were written at the same step.

## Affects
- all: defines coverage for every requirement
