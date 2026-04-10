# Decision Log

## Drop `X` (next-step) operator from temporal logic translations

**Decision:**

Do not use the LTL `X` (next) operator in any formula. Replace with `F` (eventually).

**Reason:**

The system operates in continuous time. `X` is a discrete-time concept — it refers to the very next state in a discrete sequence, which has no meaningful counterpart in a real-time system and cannot be distinguished from `F` in a test. A test can only observe that an effect happened eventually after a trigger, not that it happened in a specific discrete step.

---

## Model durations as start/end point event pairs; drop `AFTER` and `WHILE STATE`

**Decision:**

Remove `AFTER <event>` and `WHILE STATE(<name>)` from the event expression vocabulary. Any phenomenon that has duration is modelled as two instantaneous point events: `ON <name>_start` and `ON <name>_end`.

**Reason:**

All triggers in the formalism are point events — they fire at a single instant. `WHILE STATE` and `AFTER` introduced implicit duration into the trigger, which cannot be directly tested and added no expressive power that explicit start/end events don't already provide. `AFTER ON x` is simply `ON x_end`; `WHILE STATE(x)` is simply `ON x_start`.

---

## POTENTIAL IMPROVEMENT: Explicit `ON START(x)` / `ON END(x)` syntax for durational events

**Idea:**

Instead of a naming convention (`ON exception_start`, `ON exception_end`), introduce structured syntax `ON START(x)` and `ON END(x)` for events that have duration. The formalism would attach an implicit axiom enforcing that every `START` is eventually followed by an `END` for the same event:

```
G( ON START(e) → F( ON END(e) ) )
```

Additional axioms could enforce that start and end don't fire simultaneously, and optionally that a new `START(e)` cannot fire while `e` is already active.

**Benefit:** The pairing is explicit and machine-checkable rather than a naming convention. The syntax is self-documenting — `ON START(exception)` visually signals it is one half of a paired concept, unlike a flat event name.

**Why not done yet:** Current naming convention is sufficient for the requirements at hand. This would be a natural next step when building a checker that needs to validate trace well-formedness.

---

## Drop `COPY`, use `STORE` for all value transfers

**Decision:** Remove `COPY <src> TO <dst>` from the action vocabulary. Use `STORE <src> TO <dst>` for all value transfer operations, whether register-to-register, value-to-memory, or address-to-register.

**Reason:** `COPY` and `STORE` are semantically identical in the formalism — both move a value from a source to a destination with the same effect predicate (`value_at(dst) = src`). The distinction came from the English wording in the original requirement text, not from any formal difference. Having two verbs for the same operation is a source of inconsistency.

**Affected:** REQ 05 step 1 changed from `COPY SRR0 TO R5` to `STORE SRR0 TO R5`. LTL formula updated accordingly.
