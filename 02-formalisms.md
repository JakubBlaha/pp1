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

Entities are the nouns: things that hold or carry values.

```
ENTITY <name> : <type>
  [ADDRESS <hex_addr>]          // exact memory address
  [REGION <region_name>]        // named memory region
  [VOLATILE | NON_VOLATILE]     // memory kind
  [INITIAL <value>]             // initial / default value
  [PARAMS { <param>: <type> }]  // for structured datatypes
```

### Entity types

| Type            | Meaning                                        |
| --------------- | ---------------------------------------------- |
| `SIGNAL`        | A software signal or variable                  |
| `REGISTER`      | A hardware CPU register                        |
| `MEMORY_REGION` | A named region of memory                       |
| `DDS_TOPIC`     | A DDS communication topic                      |
| `DATATYPE`      | A structured data type with named parameters   |
| `HARDWARE`      | A hardware component (e.g. processor)          |
| `ABSTRACT`      | A higher-level entity not directly addressable |

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

| Syntax                                | Meaning                                            |
| ------------------------------------- | -------------------------------------------------- |
| `<entity>`                            | Current value of entity                            |
| `<entity>[k-1]`                       | Value at the previous discrete time step           |
| `PREV(<entity>)`                      | Alias for `<entity>[k-1]`                          |
| `ADDR(<entity>)`                      | Memory address of entity                           |
| `DIFF(<a>, <b>)`                      | Arithmetic difference `a − b`                      |
| `SIGNED(<expr>)`                      | Interpret bit pattern as signed integer            |
| `MAX_PEAK(<entity>)`                  | Historical maximum peak value of entity            |
| `MIN_PEAK(<entity>)`                  | Historical minimum peak value of entity            |
| `COUNT(ON <event>, SINCE ON <event>)` | Number of times event occurred since another event |

---

## Action Vocabulary (EFFECT)

| Action                                           | Meaning                                    |
| ------------------------------------------------ | ------------------------------------------ |
| `CALCULATE <entity> = <expr>`                    | Compute and assign a value                 |
| `READ <entity> FROM <addr>`                      | Read value from a memory address           |
| `STORE <entity> TO <dst>`                        | Write value to a destination               |
| `INVOKE <entity>`                                | Call a routine or handler                  |
| `HOLD <entity>`                                  | Suspend / freeze execution                 |
| `TOGGLE <entity>`                                | Invert the boolean value of entity         |
| `TRANSMIT <entity>(<param>=<val>) VIA <channel>` | Send a signal over a channel               |
| `SET_STATE <state_name>`                         | Transition to a named system state         |
| `START_EXECUTE <entity>`                         | Begin execution of a task or sequence      |
| `IF <cond> THEN <action>`                        | Conditional action (inline, within a step) |

When `ORDERED` is present, the listed steps must execute in the given sequence. Each step is a state in the implied automaton (TA tier) or is expressed with `U` operators (LTL/MTL/STL tier).

---

## Effect Predicates

Actions describe what the software *does*. Temporal logic formulas reason over *state* — what *holds* as a result. Each action has a corresponding **effect predicate** that captures the observable state produced by that action. These predicates are what appear in LTL/MTL/STL formulas.

| Action                      | Effect predicate          | Meaning of predicate                                |
| --------------------------- | ------------------------- | --------------------------------------------------- |
| `CALCULATE e = expr`        | `e = expr`                | Entity `e` currently holds the computed value       |
| `READ e FROM addr`          | `e = value_at(addr)`      | Entity `e` holds the value currently at `addr`      |
| `STORE e TO dst`            | `value_at(dst) = e`       | Destination `dst` holds the value of `e`            |
| `INVOKE f`                  | `invoked(f)`              | Routine `f` has been called                         |
| `HOLD e`                    | `halted(e)`               | Execution of `e` is suspended                       |
| `TOGGLE e`                  | `e = ¬prev(e)`            | `e` holds the boolean inverse of its previous value |
| `TRANSMIT e(p=v) VIA ch`    | `transmitted(e, p=v, ch)` | Signal `e` with parameter `p=v` was sent over `ch`  |
| `SET_STATE s`               | `mode = s`                | System is currently in state `s`                    |
| `START_EXECUTE seq`         | `executing(seq)`          | Sequence `seq` is currently running                 |
| `ON return(f)` (as trigger) | `returned(f)`             | Routine `f` has returned                            |

The distinction matters: the *action* is an event that occurs at a point in time; the *predicate* is a proposition that holds in the state that follows. In a temporal formula, `F( effect )` means "there exists a future state where the effect predicate holds" — not "the action fires again".

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