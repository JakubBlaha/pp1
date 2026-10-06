---
id: s-channel-design-b
kind: solution
title: Channel design B: name messages from the software's side
status: decision
solves: channel-design, receive-content, receive-dst, req08-valafter
partly-solves: future-extensions-missing
alternative-to: s-channel-design-a
---
## Summary
Recommended. `receive(t, c, v)` means a message with value $v$ goes **into** the software, `transmit(t, c, v)` means it goes **out**. In a test, what the tester sends is a `receive`, and what it expects is a `transmit`.

## Change
1. Operations table: `receive(t, c, expr)` sets the channel's value on $(t, t_{\mathit{next}}]$ and makes the `received` event happen, like `transmit`; the destination argument is dropped.
2. A stimulus may never be a `transmit`.
3. Req 08 reads the received value with $\mathit{ValAfter}_\rho$.

## Example
A Req 08 test with the stimulus `receive(1, MastershipInfo, BACKUP)`: the condition of Req 08 holds at 1 s in every trace.

## Trade-offs
Test writers may say "send" or "receive"; the translation decides by where the message appears in the test (stimuli or assertions).

## Affects
- Req 07: the transmission stays a software action
- Req 08: the reception carries its value; read with $\mathit{ValAfter}_\rho$
