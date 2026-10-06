---
id: receive-dst
title: receive should lose its destination argument
parent: channel-design
status: proposed
severity: minor
found: 2026-10-05
ec: none
ec-why: Both forms translate; dropping the destination only simplifies the rules.
related: channel-design
---
## Summary
No requirement uses `receive`'s destination Signal, and in a test it would make the test perform the software's copy.

## Explanation
**Hypothetical requirement:** "When the software receives MastershipInfo, it shall store Mastership_b in `current_mastership`." With a destination argument, the test's own stimulus `receive(1, MastershipInfo, current_mastership)` performs the copy, so the requirement looks covered without the test checking anything. Without it, the copy is the software's behaviour, stated in the requirement:

$$\mathit{Always}\bigl(\mathit{Happening}(\mathit{ev\_received\_mastership}, \mathit{Now}) \Rightarrow \mathit{ValAfter}_\rho(\mathit{current\_mastership}, \mathit{Now}) = \mathit{ValAfter}_\rho(\mathit{MastershipInfo}, \mathit{Now})\bigr)$$

`read(t, src, dst)` may keep its destination, because reading is the software's action.

## Proposed fix
Drop the destination argument from `receive` when a channel design is adopted.

## Affects
- none

## Sources
- `research/receive-without-dst.md`
