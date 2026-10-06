---
id: s-reset-rule
kind: solution
title: Give a reset an effect on volatile storage
status: rejected
solves: reset-semantics
---
## Summary
Added and reverted on 4 Oct 2026: the coverage checker does not need to know what a reset does to memory. A covering test fires a reset and asserts the value afterwards.

## Change
A `reset` operation that cleared every Storage without `non_volatile ↦ true`.

## Affects
- Req 02: would have made the reset part depend on the memory type
