---
id: d-signal-write
title: The intended Req 09 test cannot write d
parent: cat-events
status: open
severity: major
found: 2026-10-06
ec: blocker
ec-why: The intended Req 09 test writes to a Signal, which has no translation; written with `calculate` it translates but never triggers the requirement.
related: only-if-gap, system-boundary, parser-no-semantics, signed-values
---
## Summary
In Req 09, `d` is declared a Signal, but `write` only accepts Storage. No stimulus can make the event `ev_written_d` happen, so the test the author intended cannot be written.

## Explanation
The operations table:

| Operation | Target | Event it produces |
|---|---|---|
| `calculate(t, e, expr)` | Signal | `calculated` |
| `write(t, e, expr)` | Storage | `written` |

Req 09 waits for `ev_written_d` (type `written`, target `d`). `write` on `d` is not allowed, and `calculate` on `d` produces a `calculated` event instead.

The parser shows both sides: a test with `write(…, d, …)` is rejected ("write target expects a Storage entity, but 'd' is Signal"), and a test with `calculate(…, d, …)` is accepted but never triggers `ev_written_d`.

**The intended test**, once `d` is Storage (times in ns):

```
setup:      valid_range = false
stimuli:    write(0, d, 50), fire(1, min_peak_det), write(2, d, 900),
            fire(3, max_peak_det), write(4, d, 1000)
assertions: 504 ↦ { ValAfter(valid_range, 504) = true }
```

At 4 ns all three conditions hold: $900 - 50 = 850 > 655$; the writes at 2 and 4 ns are the first and second after the minimum peak; and $1000 > 900$.

## Proposed fix
1. Declare `d` (and, for consistency, `valid_range`) as Storage in `examples.tex` and the parser.
2. Fix "Events happen when the test fires them, but not only then", so that "the second write after the minimum peak" is decidable.

## Affects
- Req 09: no test can trigger the write to `d`

## Sources
- Operations table in `tex-new/formalism.tex`
