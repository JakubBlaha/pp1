# Framework

## Overview

Every requirement encodes a causal pattern:

```
TRIGGER → (GUARD?) → EFFECT  (within DEADLINE?)
```

This maps directly to a temporal logic formula:

```
G( trigger ∧ guard  →  F[0, deadline]( effect ) )
```

The formalism defined here is a structured front-end for three temporal logics and Timed Automata. The appropriate backend is chosen per requirement based on what the requirement contains:

| Tier | Use when requirement contains                            |
| ---- | -------------------------------------------------------- |
| LTL  | Only ordering / causality, no time bounds, no arithmetic |
| MTL  | Ordering + concrete time bounds, no arithmetic           |
| STL  | Time bounds + arithmetic on real-valued signals          |
| TA   | Multi-step procedure where each step is a discrete state |

STL subsumes MTL which subsumes LTL, so a higher tier can always be used instead of a lower one — but a lower tier is preferred when it is sufficient, as it is easier to check.

---

## Entity Declarations

Entities are the nouns: things that hold or carry values. Each type has its own set of valid modifiers.

```
ENTITY <name> : SIGNAL
  [INITIAL <value>]                 // default value at time 0

ENTITY <name> : STORAGE
  [ADDRESS <hex_addr>]              // exact memory address (required if known)
  [ATTRIBUTES { <attr>, … }]        // observable attributes, e.g. NON_VOLATILE, REGISTER

ENTITY <name> : DDS_TOPIC

ENTITY <name> : DATATYPE
  [PARAMS { <param>: <type>, … }]   // named parameters of the datatype

ENTITY <name> : STATE               // no modifiers — a named behavioral mode

ENTITY <name> : ABSTRACT            // no modifiers — by definition not directly addressable
```

### Entity types

| Type        | Meaning                                                                                |
| ----------- | -------------------------------------------------------------------------------------- |
| `SIGNAL`    | A software-internal variable; used with `CALCULATE`, `STORE`, `READ`, `TOGGLE`         |
| `STORAGE`   | Any addressable location that holds a value (CPU register, memory address, NVM region) |
| `DDS_TOPIC` | A DDS communication topic; used as the channel in `TRANSMIT … VIA`                     |
| `DATATYPE`  | Data transmitted or received over a channel; used with `TRANSMIT` and `ON receive`     |
| `STATE`     | A named behavioral mode the system can be in; used with `SET_STATE`                    |
| `ABSTRACT`  | A named concept the requirement refers to but that has no known address or structure (e.g. a hardware component, a logical process) |

### Storage attributes (examples)

| Attribute      | Meaning                            |
| -------------- | ---------------------------------- |
| `NON_VOLATILE` | Value persists across power cycles |
| `VOLATILE`     | Value is lost on power loss        |
| `REGISTER`     | A CPU register                     |
| `MEMORY`       | A memory location (not a register) |

Attributes appear in formulas as `has_attribute(<entity>, <attr>)` and can be checked by a test independently of the stored value.

---

## Requirement Structure

```
REQ <id> [<descriptive label>]
  TIER:    LTL | MTL | STL | TA

  // Option A — triggered requirement (event causes the effect)
  TRIGGER: <event_expr>
  [GUARD:  <condition_expr>]
  [DEADLINE: WITHIN <n> <unit> | LESS_THAN <n> <unit>]

  // Option B — untriggered requirement (no causing event)
  MODALITY: INVARIANT | EVENTUAL

  EFFECT: [ORDERED]
    [<n>.] <action_expr>
    ...
```

`TRIGGER` and `MODALITY` are mutually exclusive. Use `TRIGGER` when an event causes the effect. Use `MODALITY` when the requirement is a bare obligation with no causing event: `INVARIANT` means the effect must hold at every instant (`G`); `EVENTUAL` means the effect must hold at some point (`F`).

---

## Event Expressions (TRIGGER)

| Expression                                   | Meaning                        |
| -------------------------------------------- | ------------------------------ |
| `ON <event_name>`                            | A named point event fires      |
| `ON write(<entity>)`                         | A write operation to an entity |
| `ON receive(<datatype> [, <param>=<value>])` | Receive a data instance        |
| `ON return(<entity>)`                        | An invoked routine returns     |

Events that have duration are modelled as two point events: `ON <name>_start` and `ON <name>_end`. For example, `ON exception_start` / `ON exception_end`, `ON initialization_start` / `ON initialization_end`.

---

## Conditions (GUARD)

| Syntax                 | Meaning                                         |
| ---------------------- | ----------------------------------------------- |
| `<expr> > <expr>`      | Greater-than comparison                         |
| `<expr> >= <expr>`     | Greater-or-equal comparison                     |
| `<expr> == <expr>`     | Equality                                        |
| `<expr> IS <literal>`  | Value equals a named constant (TRUE, BACKUP, …) |
| `ALL_OF { <cond>, … }` | All conditions must hold                        |
| `ANY_OF { <cond>, … }` | At least one condition must hold                |
| `NOT <cond>`           | Negation                                        |

---

## Expressions

| Syntax                                | Meaning                                                           |
| ------------------------------------- | ----------------------------------------------------------------- |
| `<entity>`                            | Current value of entity                                           |
| `<entity>[k-1]`                       | Value at the previous discrete time step                          |
| `PREV(<entity>)`                      | Alias for `<entity>[k-1]`                                         |
| `ADDR(<entity>)`                      | Memory address of entity                                          |
| `DIFF(<a>, <b>)`                      | Arithmetic difference `a − b`                                     |
| `SIGNED(<expr>)`                      | Interpret bit pattern as signed integer                           |
| `MAX_PEAK(<entity>)`                  | Historical maximum peak value of entity                           |
| `MIN_PEAK(<entity>)`                  | Historical minimum peak value of entity                           |
| `COUNT(ON <event>)`                   | Total number of times event has occurred                          |
| `COUNT(ON <event>, SINCE ON <event>)` | Number of times event occurred since another event                |
| `INTERVAL(ON <event>, <n>)`           | Time span between the 1st and nth most recent occurrence of event |

---

## Action Vocabulary (EFFECT)

The action is an imperative operation that occurs at a point in time. The effect predicate is the observable proposition that holds in the resulting state — this is what appears in LTL/MTL/STL formulas and in `CHECK` assertions in test cases.

| Action                                           | Meaning                                    | Effect predicate          |
| ------------------------------------------------ | ------------------------------------------ | ------------------------- |
| `CALCULATE <entity> = <expr>`                    | Compute and assign a value                 | `e = expr`                |
| `READ <entity> FROM <addr>`                      | Read value from a memory address           | `e = value_at(addr)`      |
| `STORE <entity> TO <dst>`                        | Write value to a destination               | `value_at(dst) = e`       |
| `INVOKE <entity>`                                | Call a routine or handler                  | `invoked(f)`              |
| `HOLD <entity>`                                  | Suspend / freeze execution                 | `halted(e)`               |
| `TOGGLE <entity>`                                | Invert the boolean value of entity         | `e = ¬prev(e)`            |
| `TRANSMIT <entity>(<param>=<val>) VIA <channel>` | Send a signal over a channel               | `transmitted(e, p=v, ch)` |
| `SET_STATE <state_name>`                         | Transition to a named system state         | `in_state(s)`             |
| `IF <cond> THEN <action>`                        | Conditional action (inline, within a step) | *(predicate of inner action)* |
| `ON return(f)` *(as trigger)*                    | A routine has returned                     | `returned(f)`             |
| *(entity attribute)*                             | Structural property of an entity           | `has_attribute(e, attr)`  |

When `ORDERED` is present, the listed steps must execute in the given sequence. Each step is a state in the implied automaton (TA tier) or is expressed with `U` operators (LTL/MTL/STL tier).

---

## Temporal Logic Translation Reference

```c
// Triggered (LTL)
G( trigger ∧ guard  →  F( effect ) )

// Triggered with deadline (MTL/STL)
G( trigger ∧ guard  →  F[0,d]( effect ) )

// Triggered, ordered steps (LTL)
G( trigger  →  step1 U (step2 U step3) )

// Untriggered, INVARIANT
G( effect )

// Untriggered, EVENTUAL
F( effect )

// Initial condition (STL)
<entity>[0] = <value>
```

---

## Test Case Structure

A test case injects stimuli and observes effects. It reuses entity names, event names, effect predicates, and deadlines from the requirement formalism.

```
TEST <id> FOR REQ <id>
  [SETUP:
    WRITE <entity> = <value>        // set preconditions
    ...]
  STIMULUS: [ORDERED]
    [<n>.] FIRE <event_expr>        // inject a point event
             [DELAY <n> <unit>]     // time after previous stimulus step
    ...
  OBSERVE:
    CHECK [NOT] <effect_predicate>  // verify the effect (or its absence)
    [WITHIN <n> <unit>]             // REQUIRED when requirement has DEADLINE
```

`FIRE` is the tester's action — it injects a named event into the system. `CHECK` evaluates an effect predicate from the requirement's effect predicate table. `NOT` tests that the effect does NOT hold (negative / robustness test cases).

`WITHIN` in `OBSERVE` is **mandatory** when the requirement has a `DEADLINE` field — it is not optional in that case. Omitting it means the test verifies the effect happened but not that it happened in time, which is a separate and required obligation.

**Coverage analysis procedure:**

1. List all predicates referenced in the trigger and effect (the *predicate space*).
2. Enumerate the combinations of trigger predicates that matter, guided by the requirement structure (MC/DC for `ALL_OF`, independence for `ANY_OF`). Full 2^n enumeration is not needed.
3. For each combination, evaluate the formula — does the trigger fire? This determines whether the effect must be true or false.
4. Each combination is a test obligation. Map existing test cases to obligations.
5. Any obligation with no matching test case is a coverage gap.

**Coverage obligations** are derived mechanically from the requirement structure:

| Requirement feature         | Coverage obligations generated                                                                |
| --------------------------- | --------------------------------------------------------------------------------------------- |
| `GUARD: ALL_OF { A, B, … }` | Each condition independently true while others false (MC/DC)                                  |
| `GUARD: ANY_OF { A, B, … }` | Each condition independently true (one per test); all false (negative)                        |
| `DEADLINE: WITHIN d`        | At least one test with `CHECK effect WITHIN d`; at least one boundary test near `d`           |
| Negative case               | At least one test where the trigger fires but the guard is not satisfied → `CHECK NOT effect` |

All obligations must be matched by at least one test for full coverage.
---
