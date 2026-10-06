---
id: s-constructs
kind: solution
title: Extend the catalogue of temporal constructs
status: proposed
solves: chain-response, scopes, strict-bounds, immediately-naming
partly-solves: duration-accumulation
---
## Summary
Add the constructs the requirements need, and fix a misleading name.

## Change
1. $\mathit{TriggeredSequence}(\psi_{\mathit{trigger}}, \psi_1, \ldots, \psi_n)$: every trigger is followed by the steps in order.
2. A scope argument for every construct: *Globally*, *After Q*, *Before R*, *Between Q and R*, *After Q until R*.
3. $\mathit{CausesWithin}$ takes an interval, so "less than 2 s" is $[0, 2)$.
4. Rename $\mathit{Immediately}$ to $\mathit{AtNextStep}$.
5. Add an accumulated-duration function once a requirement needs it.

## Example
Req 05: $\mathit{TriggeredSequence}(\mathit{Happening}(\mathit{ev\_exception}, \mathit{Now}), \ldots)$. Req 06: $\mathit{CausesWithin}(\ldots, [0, 2))$.

## Affects
- Req 05: triggered sequence
- Req 06: strict bound
- Req 07: scope *After Q*
- Req 11: scope *After Q*
