---
id: s-channel-design-a
kind: solution
title: Channel design A: declare a direction per channel
status: decision
solves: channel-design, receive-content, receive-dst, req08-valafter
alternative-to: s-channel-design-b
---
## Summary
Each channel is declared as an input or an output of the software; `transmit` and `receive` are two names for one message.

## Change
1. New channel modifier $\mathit{direction} \in \{\mathit{in}, \mathit{out}\}$.
2. `transmit(t, c, v)` and `receive(t, c, v)` have the same effect and make both events happen.
3. Messages on `in` channels are stimuli; messages on `out` channels may only appear in assertions.

## Trade-offs
A channel used in both directions, such as a command and its acknowledgement on one topic, has to be split into two channels.

## Affects
- Req 07: `MODESET_TOPIC` gets `direction ↦ out`
- Req 08: `MastershipInfo` gets `direction ↦ in`
