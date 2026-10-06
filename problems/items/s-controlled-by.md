---
id: s-controlled-by
kind: solution
title: Record who controls each entity; operations come only from the test
status: proposed
solves: stimulus-vs-system, only-if-gap, trigger-sentence, t-next-from-stimuli, ec-release-choice
needs: s-test-semantics
---
## Summary
Every entity declares whether the test or the software controls it. Operations are the test's stimuli, may only target test-controlled entities, and their events happen exactly when the test fires them.

## Change
1. New entity modifier $\mathit{controlled\_by} \in \{\mathit{test}, \mathit{software}\}$ in the entity-type modifier table.
2. Definition "Operation": an operation is an action the **test** performs. Remove "The trigger condition that invokes an operation is specified at the requirement level".
3. Stimuli may only target entities with $\mathit{controlled\_by} = \mathit{test}$.
4. For a test-controlled entity $e$: its events happen **exactly** at the firing times of the test's operations on $e$ ("only if", in addition to $\mathit{EvtPred}$'s "if"), and its value changes only through them, so $t_{\mathit{next}}$ is well defined.

## Example
Req 09: `d`, `min_peak_det` and `max_peak_det` are test-controlled, `valid_range` is software-controlled. The test's writes to `d` are then the only writes, and "the second write after the minimum peak" can be decided from the stimuli.

## Trade-offs
An entity changed by both sides, such as a variable that a test "forces" and the software also writes, cannot be expressed. None of our requirements has one.

## Affects
- all: every entity gets a `controlled_by` value
- Req 09: `d` and the peak detections become test-controlled
