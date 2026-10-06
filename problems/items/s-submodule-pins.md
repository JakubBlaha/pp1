---
id: s-submodule-pins
kind: solution
title: Keep the submodule pins in sync
status: proposed
solves: circular-submodules
---
## Summary
Update both pins after every formalism change, in a fixed order.

## Change
After a formalism change: bump `pp1-parser/resources/formalism`, commit the parser, bump `pp1-parser` in `pp1`, commit, and push both repositories. Alternatively, drop the parser's own copy of the formalism.

## Affects
- none
