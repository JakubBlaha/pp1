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
