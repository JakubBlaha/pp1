---
id: ec-tools-reals
title: Most Event Calculus tools handle only integers
parent: cat-ec
status: open
severity: minor
found: 2026-10-03
ec: tooling
ec-why: Needed to run the translated theories for Req 01 (real numbers) and the continuous requirements, not to write them.
related: ec-undecidable
---
## Summary
The DEC reasoner and clingo work with integers and discrete time. Real numbers and continuous time need s(CASP).

## Affects
- Req 01: the factor 1.2
- Req 06: continuous time
- Req 09: continuous time
- Req 10: continuous time

## Sources
- `research/calculi.md`, §5
