---
id: immediately-naming
title: Immediately means "next step", unlike in FRET
parent: cat-constructs
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: A naming question only.
related: scopes
---
## Summary
Our $\mathit{Immediately}$ means "at the next step". In FRET, *immediately* means "at the same time point".

## Explanation
$$\mathit{Immediately}(\psi_1, \psi_2) \Leftrightarrow \forall t_1:\ \psi_1(\rho, t_1) \Rightarrow \psi_2(\rho, \mathit{Next}(t_1))$$

Readers who know FRET may misread it.

## Proposed fix
Rename it, for example to $\mathit{AtNextStep}$, or document the difference.

## Affects
- none

## Sources
- `research/related-formalisms.md`, §9
