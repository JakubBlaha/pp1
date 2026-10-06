---
id: s-req09-storage
kind: solution
title: Declare d and valid_range as Storage in Req 09
status: proposed
solves: d-signal-write
needs: s-controlled-by, s-system-boundary
---
## Summary
Make `d` a register, so that the test's `write(t, d, v)` is valid and makes `ev_written_d` happen.

## Change
In `examples.tex` and `pp1-parser/examples/09.py`, `d` and `valid_range` become Storage entities. The "only if" rule from "Record who controls each entity" makes the count of writes decidable.

## Example
The intended test from "The intended Req 09 test cannot write d" then validates and exercises the condition.

## Affects
- Req 09: `d` and `valid_range` become Storage
