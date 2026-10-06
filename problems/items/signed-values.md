---
id: signed-values
title: Signed integers have no counterpart
parent: cat-time
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: The formalisation compares plain numbers, which translate directly; the signedness is lost before the translation.
related: d-signal-write
---
## Summary
Req 09 compares "signed values", but $d$ is modelled as a real-valued signal.

## Explanation
Condition 3 of Req 09 says "the signed value of $d$ is higher than the signed value of the last $d$". The formalism only knows mathematical numbers, so the difference between a signed and an unsigned reading of the same register cannot be expressed. `examples.tex` notes this.

## Proposed fix
Add integer types with a width and signedness to $V_{\text{base}}$, or state that values are always read as signed numbers.

## Affects
- Req 09: condition 3

## Sources
- `tex-new/examples.tex`, Req 09 notes
