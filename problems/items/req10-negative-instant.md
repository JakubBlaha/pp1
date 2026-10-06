---
id: req10-negative-instant
title: Negative tests check only a single instant
parent: cat-testcases
status: open
severity: medium
found: 2026-10-05
ec: none
ec-why: The tests translate as written; the weakness is in what they check.
related: state-inconsistent, only-if-gap
---
## Summary
The tests that expect "not entering emergency mode" check one instant only, so they pass even if the software enters emergency mode a moment later.

## Explanation
**Example (TC3).** Its only assertion, at 11 s, is

$$\mathit{ValAfter}_\rho(\mathit{emergency\_mode}, 11) \neq \mathit{true}$$

It passes even if the software enters emergency mode at 11.5 s.

## Proposed fix
Assert absence over a window, for example "no `entered` event of emergency mode in $(11, 11 + d]$". This needs an `entered` event for emergency mode (see "States are modelled in two incompatible ways") and a chosen window length $d$.

## Affects
- Req 10 / TC1: checked at 10 s only
- Req 10 / TC3: checked at 11 s only
- Req 10 / TC5: checked at 11 s only
- Req 10 / TC6: checked at 11 s only
- Req 10 / TC7: checked at 9 s only
