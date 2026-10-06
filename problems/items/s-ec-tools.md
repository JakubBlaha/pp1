---
id: s-ec-tools
kind: solution
title: Use clingo for discrete and s(CASP) for continuous requirements
status: proposed
solves: ec-tools-reals
---
## Summary
Pick the Event Calculus tool per flavour, and scale constants to integers where needed.

## Change
- Discrete requirements: clingo with a DEC encoding; scale real constants to integers (for example the factor 1.2 in Req 01).
- Continuous requirements: s(CASP), which supports rational numbers through CLP(Q).

## Affects
- Req 01: the factor 1.2
- Req 06: continuous time
- Req 09: continuous time
- Req 10: continuous time
