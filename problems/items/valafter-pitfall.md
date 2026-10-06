---
id: valafter-pitfall
title: It is easy to write Val where ValAfter is meant
parent: timing-convention
status: open
severity: minor
found: 2026-10-05
ec: none
ec-why: $\mathit{ValAfter}_\rho$ translates directly; the risk lies in writing the requirement.
related: req08-valafter, parser-no-semantics
---
## Summary
At the time of an event, $\mathit{Val}_\rho$ still shows the old value. Reading the new value needs $\mathit{ValAfter}_\rho$, which people and the LLM will easily get wrong.

## Explanation
**Example (Req 07).** "The software transmits Mode Enable = TRUE" written as

$$\mathit{Happening}(\mathit{ev\_transmitted\_modeset}, \mathit{Now}) \land \mathit{Val}_\rho(\mathit{MODESET\_TOPIC}, \mathit{Now}) = \mathit{true}$$

reads the topic's value *before* the transmission. The correct condition uses $\mathit{ValAfter}_\rho(\mathit{MODESET\_TOPIC}, \mathit{Now})$.

## Proposed fix
- State the rule in the prompting guidance for the LLM: at an event's time, read the new value with $\mathit{ValAfter}_\rho$.
- Let the parser warn when $\mathit{Val}_\rho(e, \mathit{Now})$ appears next to $\mathit{Happening}$ of an event whose target is $e$.

## Affects
- Req 02: reads a value at a reset
- Req 03: reads the value written to DTSCON
- Req 05: reads the value written to R5
- Req 07: reads the transmitted value
- Req 09: reads the written values of `d` and `valid_range`
- Req 13: reads the written register values
- Req 08: will need $\mathit{ValAfter}_\rho$ once messages carry their value
