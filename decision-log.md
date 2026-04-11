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

---

## Keep both `PREV(x)` and `x[k-1]` — prefer `PREV` for readability

**Decision:** Both notations remain in the formalism. `PREV(x)` is preferred in practice; `x[k-1]` is kept as the mathematical equivalent for reference.

**Reason:** `PREV(x)` is easier to read and less likely to be confused with array indexing. The alias does not add expressive power but improves readability for people writing or reviewing requirements.

---

## Replace `ALWAYS` trigger with `MODALITY: INVARIANT | EVENTUAL`

**Decision:** Remove `ALWAYS` from the event expressions. Untriggered requirements use a `MODALITY` field instead of `TRIGGER`. `MODALITY: INVARIANT` translates to `G(effect)`; `MODALITY: EVENTUAL` translates to `F(effect)`. `TRIGGER` and `MODALITY` are mutually exclusive.

**Reason:** `ALWAYS` was overloaded — it was used for both continuous invariants (`G`) and one-time setup obligations (`F`), which translate to different formulas. Putting it in the `TRIGGER` field was also misleading, since there is no causing event. `MODALITY` makes the distinction explicit and keeps the `TRIGGER` field semantically clean.

**Affected:** REQ 01 changed to `MODALITY: INVARIANT`. REQ 02, 03, 04 changed to `MODALITY: EVENTUAL`.

---

## Collapse `REGISTER` and `MEMORY_REGION` into `STORAGE` with `ATTRIBUTES`

**Decision:** Remove `REGISTER` and `MEMORY_REGION` as distinct entity types. Replace both with `STORAGE`. What kind of storage an entity is (CPU register, NVM region, RAM address, etc.) is expressed via an `ATTRIBUTES { … }` field. Storage attributes are verifiable predicates: `has_attribute(e, attr)` appears in formulas and can be independently checked by a test.

**Reason:** Baking memory volatility and register-vs-memory into the type system encoded hardware domain knowledge in the formalism rather than in verifiable predicates. A register and a memory region are both just addressable locations that hold values — the distinction is an attribute, not a fundamentally different kind of thing. This also means the formalism does not need to be extended for every new hardware-specific category; attributes are open-ended.

**Affected:** Entity declarations in REQ 02, 03, 04, 05 updated to use `STORAGE ATTRIBUTES { … }`. REQ 02 formula gains `∧ has_attribute(MEASUREMT_BLOCK, NON_VOLATILE)` to make the non-volatility constraint explicitly testable.

---

## Clarify entity modifiers per type; fix `ABSTRACT` + `ADDRESS` contradiction

**Decision:** The entity declaration syntax now specifies which modifiers are valid for each type. `ABSTRACT` accepts no modifiers by definition — it is a named concept with no known address or structure. `ADDRESS` and `ATTRIBUTES` are only valid on `STORAGE`. `INITIAL` is only valid on `SIGNAL`. `PARAMS` is only valid on `DATATYPE`.

**Reason:** The previous generic syntax `ENTITY <name> : <type> [ADDRESS …] [ATTRIBUTES …] …` allowed any modifier on any type, which led to contradictions like `ABSTRACT ADDRESS 0xAA000018`. An entity with a known concrete address is by definition addressable and should be `STORAGE`, not `ABSTRACT`.

**Affected:** REQ 03 `calibration_const` changed from `ABSTRACT ADDRESS 0xAA000018` to `STORAGE ADDRESS 0xAA000018`.

---

## Merge `START_EXECUTE` into `INVOKE`; use `invoked(x)` as a point-in-time predicate

**Decision:** Remove `START_EXECUTE` from the action vocabulary. Use `INVOKE` for all cases where the software triggers execution of something — whether a handler routine or a task sequence. The effect predicate is `invoked(x)` in both cases, representing the point in time when execution was triggered, not an ongoing state.

**Reason:** `executing(seq)` was a continuous state predicate, inconsistent with the principle that all effects are point-in-time observations. Starting execution of a task sequence always involves invoking some scheduler or entry point — the action is a point event. `invoked(x)` captures this correctly. Having two verbs (`INVOKE` vs `START_EXECUTE`) for the same concept added vocabulary without adding meaning.

**Affected:** REQ 06 action changed from `START_EXECUTE task_sequence` to `INVOKE task_sequence`, formula updated to use `invoked(task_sequence)`.

---

## `TRANSMIT`/`ON receive` operate on `DATATYPE` only; `SIGNAL` is software-internal

**Decision:** `TRANSMIT` and `ON receive(...)` only ever operate on `DATATYPE` entities. `SIGNAL` entities are software-internal and only appear in actions like `CALCULATE`, `STORE`, `READ`, `TOGGLE`. REQ 07's `ModeEnable` changed from `SIGNAL` to `DATATYPE PARAMS { value: BOOL }`.

**Reason:** A `SIGNAL` lives inside the software; a `DATATYPE` instance is what gets put on a communication channel. The distinction was missing in REQ 07 — `SIGNAL` was used for something transmitted over a DDS topic, which is inconsistent with REQ 08 which correctly used `DATATYPE` for received data. A single-value datatype is just a `DATATYPE` with one parameter, not a fundamentally different thing.

**Affected:** REQ 07 `ModeEnable` changed from `SIGNAL` to `DATATYPE PARAMS { value: BOOL }`.
