---
id: reset-semantics
title: A reset has no effect on storage
parent: coverage-vs-satisfaction
status: closed
severity: minor
found: 2026-10-04
ec: none
ec-why: A reset with no effect on memory is an event without effect axioms, which translates directly.
related: coverage-vs-satisfaction
---
## Summary
Nothing in the formalism says what a reset does to memory, so Req 02's "the value survives a reset" holds even for volatile memory. For coverage this is not a problem.

## Explanation
Req 02's reset part:

$$\mathit{Always}\bigl(\mathit{Happening}(\mathit{ev\_reset}, \mathit{Now}) \Rightarrow \mathit{ValAfter}_\rho(\mathit{MEASUREMT\_BLOCK}, \mathit{Now}) = \mathit{Val}_\rho(\mathit{MEASUREMT\_BLOCK}, \mathit{Now})\bigr)$$

A reset is not an operation on `MEASUREMT_BLOCK`, so in the model the value always survives it.

For coverage, the clause is what tells the checker that a covering test must reset and then check the value:

| Test | Stimuli | Assertion | Covers the reset part? |
|---|---|---|---|
| A | store | value = stored data | no, no reset |
| B | store, reset | value after reset = value before | yes |

## Resolution
Closed. A `reset` operation that clears volatile storage was added and reverted on 4 Oct 2026. The reset part of Req 02 must stay.

## Affects
- Req 02: the reset part; it must stay, because it defines what a covering test must do

## Sources
- `research/findings.md`, "A reset has no effect on storage — not a problem for coverage"
