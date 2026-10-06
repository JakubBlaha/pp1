---
id: state-inconsistent
title: States are modelled in two incompatible ways
parent: cat-events
status: open
severity: medium
found: 2026-10-03
ec: blocker
ec-why: An `entered` event does not say which state was entered, so "entering Backup" (Req 08) and "entering emergency mode" (Req 10, Req 11) have no unambiguous translation.
related: req10-negative-instant
---
## Summary
`set_state(e, s)` treats a State entity as a variable that holds a state, but the examples treat each state as its own entity, and "emergency mode" appears in two different forms.

## Explanation
- **Req 08:** `Backup` is a State entity, entered through the event `ev_entered_backup`.
- **Req 10:** `emergency_mode` is a State entity compared with $\mathit{Val}_\rho(\mathit{emergency\_mode}, \mathit{Now}) = \mathit{true}$, with no `entered` event.
- **Req 11:** entering emergency mode is an `EventTrigger` called `enter_emergency`.

So the same concept, emergency mode, is a boolean State in Req 10 and an `EventTrigger` in Req 11.

## Proposed fix
Choose one model, for example one State entity per state machine, `set_state(machine, Backup)`, and an `entered` event per state, and align the examples.

## Affects
- Req 08: `Backup` as its own State entity
- Req 10: `emergency_mode` as a boolean State without an `entered` event
- Req 11: entering emergency mode as an `EventTrigger`

## Sources
- `research/calculi.md`, §6
