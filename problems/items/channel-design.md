---
id: channel-design
title: How messages on channels are modelled
parent: cat-events
status: decision
severity: major
found: 2026-10-05
ec: blocker
ec-why: How a message becomes an EC event (one event or two, with or without its value) decides how Req 07, Req 08 and their tests translate.
related: receive-content, receive-dst, req08-valafter, stimulus-vs-system, structured-payloads
---
## Summary
A message has two sides, sending and receiving. We have to decide how the formalism names them and how it knows which side the test is on.

## Explanation
In a test, the tester sends what the software receives, and expects what the software transmits. Two designs fit our needs:

| | Design A: direction on the channel | Design B: named from the software's side |
|---|---|---|
| Idea | each channel is an input or an output; `transmit` and `receive` are two names for one message | `receive` = into the software, `transmit` = out of it |
| In a test | messages on input channels are stimuli; on output channels only assertions | what the tester sends is a `receive`, what it expects is a `transmit` |
| Two-way channel | must be split into two channels | works directly |
| Used by | TorXakis, ioco, ARINC 653, AADL | TTCN-3, interface automata, session types |

**Why plain aliases are not enough.** "When the software receives a command on CMD, it shall acknowledge it on CMD": if sending and receiving are one event, the incoming command also counts as the acknowledgement.

The notes on Req 07 and Req 08 in `examples.tex` call the related issue the "event-payload limitation": the value is checked separately from the event.

## Decision needed
Choose design A or B. `research/channels.md` recommends design B.

## Affects
- Req 07: the transmission on `MODESET_TOPIC`
- Req 08: the reception on `MastershipInfo`

## Sources
- `research/channels.md`
