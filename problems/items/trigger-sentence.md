---
id: trigger-sentence
title: Requirements are said to trigger operations, but none does
parent: stimulus-vs-system
status: proposed
severity: minor
found: 2026-10-06
ec: none
ec-why: No requirement triggers an operation, so the translation never needs trigger axioms.
related: stimulus-vs-system
---
## Summary
`formalism.tex` says "The trigger condition that invokes an operation is specified at the requirement level", but no requirement uses an operation.

## Explanation
Every requirement constraint talks about events ($\mathit{Happening}$) and values ($\mathit{Val}_\rho$, $\mathit{ValAfter}_\rho$). None names `write`, `fire` or another operation. The sentence also conflicts with the proposal that operations are performed only by the test.

## Proposed fix
Remove the sentence from the Definition "Operation" when the fix for "Who performs an event is not recorded" is adopted.

## Affects
- none

## Sources
- `tex-new/formalism.tex`, Definition "Operation"
