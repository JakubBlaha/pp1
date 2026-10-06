---
id: s-value-domains
kind: solution
title: Add records and sized integers to the value set
status: proposed
solves: structured-payloads, signed-values
needs: s-enum-values
---
## Summary
Add the remaining kinds of values our requirements mention but the formalism lacks. Not needed for the translation of the current formalisations.

## Change
1. Records with field access, for example $\mathit{Val}_\rho(\mathit{MastershipInfo}, t).\mathit{Mastership\_b}$.
2. Integer types with a width and signedness, for example $\mathit{int16}$.

## Affects
- Req 07: the signal Mode Enable as a field of the message
- Req 08: `Mastership_b` as a field of the message
- Req 09: `d` as a signed integer
