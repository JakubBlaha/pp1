---
id: s-well-formed-traces
kind: solution
title: Require well-formed traces
status: proposed
solves: left-limit-lost
---
## Summary
Restrict traces to piecewise-constant values, so that the value at a change time always equals the value just before it.

## Change
Add to Definition "Trace": every entity's value is piecewise constant, changes only finitely often in any bounded interval, and every constant piece has the form $(t_i, t_{i+1}]$.

## Affects
- none
