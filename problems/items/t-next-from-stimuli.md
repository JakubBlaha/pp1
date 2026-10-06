---
id: t-next-from-stimuli
title: An effect lasts until the next operation, not until the next change
parent: cat-events
status: open
severity: medium
found: 2026-10-03
ec: blocker
ec-why: EC ends an effect at the next event that changes the value; the formalism ends it at the next operation. The translation is faithful only if the two coincide.
related: stimulus-vs-system
caused-by: stimulus-vs-system
---
## Summary
An operation's effect lasts until the next *operation* on the same entity. If the software also changes that entity, the effect contradicts the trace.

## Explanation
$$t_{\mathit{next}} = \min\{\, t' > t \mid \text{a value-modifying operation fires on } e \text{ at } t' \,\}$$

This is a fact about the test's stimuli, not about the trace.

**Example.** The test writes `x = 5` at 1 s, and the software writes `x = 7` at 3 s, which is not an operation. The test's effect still says `x = 5` on $(1, \infty)$, because no further operation fires on `x`.

The Event Calculus avoids this: whether a value was changed ($\mathit{Clipped}$) is decided from the events in the model.

## Proposed fix
Define $t_{\mathit{next}}$ from the events in the trace, or rule out entities that both sides change (part 2 of the fix for "Who performs an event is not recorded").

## Affects
- none

## Sources
- `research/related-formalisms.md`, §7
