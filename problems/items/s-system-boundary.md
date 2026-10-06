---
id: s-system-boundary
kind: solution
title: Decide the system boundary for each requirement
status: decision
solves: system-boundary
needs: s-controlled-by
---
## Summary
For each requirement or test suite, state what the system under test is, so that every entity can be classified as test- or software-controlled.

## Change
Add a "System under test" line to each formalisation, for example "the component that toggles `valid_range`" for Req 09.

## Decision needed
Req 09: is `d` written by hardware or another component (then the test writes it), or computed by the software under test (then the test can only observe the writes)? The requirement's author intended the test to write `d`.

## Affects
- Req 09: decides who controls `d` and the peak detections
