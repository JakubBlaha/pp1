---
id: s-enum-values
kind: solution
title: Add enumerated values to the value set
status: proposed
solves: enum-values
---
## Summary
Let requirements use named constants such as `BACKUP` as values of a declared enumeration.

## Change
Add enumerated types to $V_{\text{base}}$, for example $\mathit{Mastership} = \{\mathit{PRIMARY}, \mathit{BACKUP}\}$, and let entities declare which enumeration their values come from. In the Event Calculus an enumeration becomes a sort with constants.

## Example
Req 08's condition $\mathit{Val}_\rho(\mathit{MastershipInfo}, \mathit{Now}) = \mathit{BACKUP}$ then compares with a declared constant.

## Affects
- Req 08: `BACKUP` becomes a value of an enumeration
