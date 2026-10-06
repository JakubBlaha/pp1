---
id: receive-content
title: receive does not fix what is received
parent: channel-design
status: open
severity: major
found: 2026-10-04
ec: blocker
ec-why: A test's `receive` carries no value, so it cannot become the event $\mathit{receive}(c, v)$ that Req 08's tests need.
related: channel-design, only-if-gap, example-assertion-weak
---
## Summary
`receive(t, c, dst)` has no argument for the message's content, so a test that delivers a message cannot say what it contains.

## Explanation
`receive` copies the channel's *current* value into a Signal `dst`; only `transmit` puts a value on a channel. A test describes an incoming message with one stimulus, so the content is left open.

**Example (Req 08).** "TC1: the software receives a MastershipInfo message at 1 s":

| Trace | Value on `MastershipInfo` at 1 s | Condition of Req 08 | Exercised? |
|---|---|---|---|
| A | `BACKUP` | true | yes |
| B | `PRIMARY` | false | no |

The checker cannot decide whether TC1 exercises Req 08.

## Proposed fix
Both channel designs give the message stimulus a value, $\mathit{receive}(t, c, v)$. TC1 can then not be written without stating the content.

## Affects
- Req 08: a test cannot state what was received
- Req 08 / TC1: the example test in `research/findings.md`

## Sources
- `research/findings.md`, "`receive` does not fix what is received"
