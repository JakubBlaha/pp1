---
id: counter-no-flavour
title: The Custom Counter declares no flavour
parent: cat-examples
status: open
severity: minor
found: 2026-10-03
ec: blocker
ec-why: The translation picks discrete or continuous EC from the flavour, and Req 11 declares none.
related: scopes
---
## Summary
Req 11 (the Custom Counter) has no "Flavour" line in `examples.tex`. The parser uses Discrete, matching "at each discrete time step".

## Proposed fix
Add "Flavour: Discrete." to the example.

## Affects
- Req 11: no flavour declared

## Sources
- `research/calculi.md`, §6
