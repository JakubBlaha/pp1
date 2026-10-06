---
id: circular-submodules
title: pp1 and pp1-parser include each other as submodules
parent: cat-parser
status: open
severity: minor
found: 2026-10-05
ec: none
ec-why: Repository housekeeping only.
related: parser-outdated
---
## Summary
`pp1` contains `pp1-parser`, which contains `pp1` again. A recursive clone nests the repositories, and both have to be pushed before anyone else updates.

## Proposed fix
Keep the parser's formalism pin up to date, or drop one of the two directions.

## Affects
- none
