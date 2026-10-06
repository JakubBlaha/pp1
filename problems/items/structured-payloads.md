---
id: structured-payloads
title: Messages with several fields cannot be represented
parent: cat-events
status: open
severity: minor
found: 2026-10-05
ec: none
ec-why: The current formalisations compare whole channel values, which translate directly.
related: enum-values, channel-design
---
## Summary
A channel holds one value, but messages often have several fields.

## Explanation
Req 08 speaks of a *data instance* of `MastershipInfo` with a *parameter* `Mastership_b`, and Req 07 of a *signal* Mode Enable sent on a topic. Both formalisations compare the whole channel value with a constant.

## Proposed fix
Add record values with field access to $V_{\text{base}}$, or model one channel per field.

## Affects
- Req 07: the signal Mode Enable on `MODESET_TOPIC`
- Req 08: the parameter `Mastership_b` of `MastershipInfo`

## Sources
- `research/receive-without-dst.md`, "Related observations"
