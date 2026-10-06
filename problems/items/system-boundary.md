---
id: system-boundary
title: Test- or software-controlled depends on the system boundary
parent: stimulus-vs-system
status: decision
severity: medium
found: 2026-10-06
ec: blocker
ec-why: For Req 09 the translation cannot decide whether the writes to `d` and the peak detections are stimulus events or software events.
related: d-signal-write, software-only-conditions
---
## Summary
Whether the test or the software writes `d` in Req 09 depends on what we call "the system under test". The formalism does not state that boundary.

## Explanation
- **The whole software is under test**, including the code that computes `d`. Then `d` belongs to the software: the test can only provide the inputs that make the software write `d`, and observe the writes.
- **Only the component that toggles `valid_range` is under test**, and `d` is written by something else, such as an ADC peripheral. Then `d` is an input, and the test writes it directly.

The wording "within 500 ns of a write to `d`" suggests that `d` is a data register filled by hardware. The author of the example intended the test to write it.

## Decision needed
State the system boundary, per requirement or per test suite, and classify the entities accordingly. For Req 09 the author's intent suggests: `d` and the peak detections are controlled by the test, `valid_range` by the software.

## Affects
- Req 09: who controls `d` and the peak detections
