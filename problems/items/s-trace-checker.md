---
id: s-trace-checker
kind: solution
title: Build the trace evaluator and coverage checker in the parser
status: proposed
solves: parser-no-semantics
partly-solves: ec-undecidable
needs: s-coverage-rule
---
## Summary
Evaluate conditions on the concrete trace parts that tests determine, instead of only checking types.

## Change
Add to `pp1-parser`:
1. compute the test-controlled part of a test's trace from its setup and stimuli;
2. evaluate each condition of each requirement on it;
3. report, per requirement, which conditions no test exercises.

Evaluating concrete traces also avoids symbolic reasoning, which is undecidable over continuous time.

## Example
A Req 09 test that sets `d` with `calculate` would be reported as exercising nothing, because `ev_written_d` never happens in it.

## Affects
- all: every requirement gets a coverage report
