---
id: undefined-values
title: No rule for predicates over undefined values
parent: cat-time
status: open
severity: medium
found: 2026-10-03
ec: blocker
ec-why: A comparison with an undefined value becomes false under an existential translation and true under a universal one; the formalism must say which is meant.
related: req10-empty-setup, addr-undefined
---
## Summary
Values can be undefined (valuations are partial), but nothing says what a comparison means when one of its operands is undefined.

## Explanation
**Example (Req 01).** $\mathit{Always}$ also applies at $\mathit{Now} = 0$, where $\mathit{Prev}(0)$ is undefined:

$$\mathit{Val}_\rho(\mathit{EngagementNoSat\_u}, 0) = 1.2 \cdot \mathit{Val}_\rho(\mathit{EngagementNoSat\_u}, \mathit{Prev}(0))$$

Is this true, false, or neither? Lustre avoids the question by making the first step explicit with `->`.

## Proposed fix
Choose one rule, for example "a comparison with an undefined operand is false", and guard recurrences with $\mathit{Now} > 0$. Require tests to give a setup value to every entity they compare.

## Affects
- Req 01: $\mathit{Prev}(\mathit{Now})$ at $\mathit{Now} = 0$
- Req 04: $\mathit{Addr}$ of entities without an address
- Req 11: $\mathit{Prev}(\mathit{Now})$ at $\mathit{Now} = 0$
- Req 10 / TC1: `emergency_mode` has no setup value

## Sources
- `research/related-formalisms.md`, §3 (Lustre)
