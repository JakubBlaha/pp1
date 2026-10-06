---
id: addr-undefined
title: Req 04 compares with addresses that are not declared
parent: cat-examples
status: open
severity: medium
found: 2026-10-06
ec: blocker
ec-why: $\mathit{Addr}(\mathit{CriticalInput})$ has no value to translate to.
related: undefined-values
---
## Summary
$\mathit{Addr}(\mathit{CriticalInput})$ reads the `address` modifier, but `CriticalInput` and `MachineCheck` declare no modifiers, so both addresses are undefined.

## Explanation
$\mathit{Addr}(e) = \mu_e(\mathit{address})$ is undefined when $e$ carries no address. Req 04 compares the IVOR registers with exactly these undefined values:

$$\mathit{Eventually}\bigl(\mathit{Val}_\rho(\mathit{IVOR0}, \mathit{Now}) = \mathit{Addr}(\mathit{CriticalInput}) \land \mathit{Val}_\rho(\mathit{IVOR1}, \mathit{Now}) = \mathit{Addr}(\mathit{MachineCheck})\bigr)$$

Found while building this problem tree.

## Proposed fix
Declare the addresses of the exception vectors with `address ↦ …`, or model them as constants.

## Affects
- Req 04: both addresses are undefined

## Sources
- `tex-new/examples.tex`, Req 04
