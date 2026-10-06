---
id: req13-outdated
title: Req 13 used an undefined form of Happening and an outdated text
parent: cat-examples
status: resolved
severity: major
found: 2026-10-03
ec: blocker
ec-why: Resolved: the three-argument $\mathit{Happening}$ had no translation; Req 13 now uses Event entities.
related: valafter-pitfall
---
## Summary
Req 13 called $\mathit{Happening}$ with three arguments over register entities, which is not defined, and formalised an older "read" version of the requirement. Fixed on 5 Oct 2026.

## Explanation
The old antecedent was

$$\mathit{ForAll}\bigl(\mathit{regs},\ \lambda e.\ \mathit{Happening}(e, \mathit{read}, \mathit{Now})\bigr)$$

but $\mathit{Happening}$ takes two arguments, the first an Event entity. In addition, `req/13.custom.md` was changed on 4 Jun 2026 from "read" to "written in parallel".

## Resolution
The antecedent is now $\mathit{ForAll}(\mathit{writes}, \lambda \mathit{ev}.\ \mathit{Happening}(\mathit{ev}, \mathit{Now}))$ over `ev_written_A` … `ev_written_D`, and the written values are read with $\mathit{ValAfter}_\rho$. Commits: `examples.tex` 5c33908, parser be59f32.

## Affects
- Req 13: fixed

## Sources
- `CHANGELOG.md`, 5 Oct 2026
