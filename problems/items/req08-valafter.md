---
id: req08-valafter
title: Req 08 must read the received value with ValAfter
parent: channel-design
status: open
severity: minor
found: 2026-10-05
ec: blocker
ec-why: Once a message carries its value, Req 08 translated with $\mathit{Val}_\rho$ would read the previous message.
related: valafter-pitfall, timing-convention
caused-by: timing-convention
---
## Summary
Once a message sets the channel's value, Req 08 must read it with $\mathit{ValAfter}_\rho$.

## Explanation
With $\mathit{receive}(t, c, v)$ the message sets the channel's value, and by the timing convention the new value is visible only after $t$. Req 08 reads $\mathit{Val}_\rho(\mathit{MastershipInfo}, \mathit{Now})$, which would show the previous message.

## Proposed fix
Change the condition to $\mathit{ValAfter}_\rho(\mathit{MastershipInfo}, \mathit{Now}) = \mathit{BACKUP}$ when a channel design is adopted.

## Affects
- Req 08: the condition on the received value

## Sources
- `research/findings.md`, "`receive` does not fix what is received"
