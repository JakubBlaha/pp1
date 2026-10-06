---
id: only-if-gap
title: Events happen when the test fires them, but not only then
parent: stimulus-vs-system
status: open
severity: major
found: 2026-10-05
ec: blocker
ec-why: EC treats the listed events as the only ones. Unless the formalism says the same, counts such as "the second write" (Req 09) or "twice within 10 s" (Req 10) mean something different after translation.
related: d-signal-write, ec-aggregates, req10-negative-instant
caused-by: test-set-of-traces
---
## Summary
An operation makes its event true at the firing time, but nothing makes the event false at other times. Counts and "the last occurrence" can therefore not be decided.

## Explanation
Every operation's effect contains $\mathit{EvtPred}$:

$$\mathit{EvtPred}(e, ek, t) \equiv \forall ev \in E:\ \bigl(t_{ev} = \text{Event} \land \mu_{ev}(\mathit{target}) = id_e \land \mu_{ev}(\mathit{type}) = ek\bigr) \Rightarrow \mathit{Val}_\rho(ev, t) = \mathit{true}$$

It says that *if* the operation fires, the event happens. It does not say that the event happens *only* then. So a test also allows traces with extra events that it never produced.

**Example (Req 09).** The test writes `d` at 0, 2 and 4 ns, with a minimum peak at 1 ns. A trace with an extra write at 3 ns satisfies the test as well. In that trace the write at 4 ns is the *third* after the peak, so the condition "second write after the minimum peak" is false.

**Example (Req 10, TC3).** Sensor failures at 0 s and 11 s. A trace with an extra sensor failure at 5 s satisfies the test too, and there the condition is true, contradicting TC3's expectation "not entering emergency mode".

## Proposed fix
Part 3 of the fix for "Who performs an event is not recorded": events on test-controlled entities happen exactly when the test's operations produce them.

## Affects
- Req 09: counting writes to `d` ($\mathit{EvtOccCount}$) and finding the previous write ($\mathit{LastOcc}$)
- Req 10: counting failures in the 10 s window
- Req 10 / TC1: "no failure" only holds if no extra failures can appear
- Req 10 / TC3: an extra sensor failure would make the condition true
- Req 10 / TC5: an extra energy failure would make the condition true
- Req 10 / TC6: an extra communication failure would make the condition true
- Req 10 / TC7: an extra failure of the same type would make the condition true

## Sources
- `research/findings.md`, "`receive` does not fix what is received", "Limitation: only 'if', not 'only if'"
