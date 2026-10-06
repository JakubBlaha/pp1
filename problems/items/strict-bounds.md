---
id: strict-bounds
title: Strict time bounds cannot be written with CausesWithin
parent: cat-constructs
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: The closed interval translates directly; the over-approximation is in the formalisation, not in the translation.
related: negative-window-start
---
## Summary
$\mathit{CausesWithin}$ always uses the closed interval $[t, t+d]$, so "in less than 2 s" is over-approximated by "within 2 s".

## Explanation
$$\mathit{CausesWithin}(c, e, d) \Leftrightarrow \forall t:\ c(\rho, t) \Rightarrow \exists t' \in [t, t + d]:\ e(\rho, t')$$

Req 06 says "in less than 2 seconds", so a start at exactly 2 s should fail, but it passes. MTL can write the strict bound as $\mathbf{F}_{[0,2)}$.

## Proposed fix
Add an open-bound variant, or let $\mathit{CausesWithin}$ take an interval instead of a duration.

## Affects
- Req 06: "in less than 2 seconds"

## Sources
- `tex-new/examples.tex`, Req 06 notes
- `research/related-formalisms.md`, §1
