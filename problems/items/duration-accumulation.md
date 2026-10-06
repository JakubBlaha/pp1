---
id: duration-accumulation
title: Accumulated durations cannot be expressed
parent: cat-constructs
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: No requirement uses it.
related: openness-ignored
---
## Summary
"The heater may be on for at most 4 s in any 30 s window" needs a function that adds up durations. The formalism has none, and no current requirement needs it.

## Explanation
Duration Calculus writes this as $\ell \le 30 \Rightarrow \int \mathit{heater} \le 4$.

## Proposed fix
Add a duration-accumulation function when a requirement needs it.

## Affects
- none

## Sources
- `research/related-formalisms.md`, §5
