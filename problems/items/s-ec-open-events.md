---
id: s-ec-open-events
kind: solution
title: Translate to the Event Calculus with open system events
status: proposed
solves: ec-software-events, ec-kind1, ec-kind2, ec-kind3
needs: s-controlled-by
---
## Summary
Keep the complete-event-list assumption for the test's events only; the software's events may happen at any time.

## Change
In the translation, the stimuli become `happens` facts, and every software-controlled entity gets a choice rule for the operations that can change it:

```
{ happens(set_state(emergency_mode, V), T) }.
{ happens(calculate(counter_1, V), T) }.
```

EC planners use the same technique for the actions they may choose.

## Affects
- all: the translation of every requirement
