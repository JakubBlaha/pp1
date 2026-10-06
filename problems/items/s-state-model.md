---
id: s-state-model
kind: solution
title: Use one model for states: state machines with entered events
status: proposed
solves: state-inconsistent
needs: s-enum-values
---
## Summary
Model each state machine as one State entity whose value is the current state, and give every state its own `entered` event.

## Change
1. A State entity is a state machine; `set_state(t, machine, s)` sets its value to the state $s$.
2. An `entered` event names the state it tracks: $\{\mathit{target} \mapsto id_{\mathit{mode}},\ \mathit{type} \mapsto \mathit{entered},\ \mathit{state} \mapsto \mathit{EMERGENCY}\}$.
3. Req 08, Req 10 and Req 11 use this model.

## Example
Req 10's response becomes $\mathit{Val}_\rho(\mathit{mode}, \mathit{Now}) = \mathit{EMERGENCY}$, and Req 11's antecedent $\mathit{HasHappened}_\rho(\mathit{ev\_entered\_emergency}, \mathit{Now})$.

## Affects
- Req 08: `Backup` becomes a state of a mastership state machine
- Req 10: emergency mode becomes a state with an `entered` event
- Req 11: entering emergency mode becomes the same `entered` event
