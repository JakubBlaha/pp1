---
id: s-ec-translator
kind: solution
title: Build the translator from the parser's JSON to Event Calculus theories
status: proposed
solves: ec-no-translator
needs: s-ec-spec, s-ec-tools
---
## Summary
A program that reads a module (requirements, entities, test cases) from `pp1-parser` and writes the Event Calculus theory for each requirement and test.

## Change
Add a translation backend to `pp1-parser` that follows the specification: clingo programs (DEC encoding) for discrete requirements, s(CASP) programs for continuous ones. Check it on all examples.

## Affects
- all: every requirement and test case gets a translation
