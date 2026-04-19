# Formalism — Unified Draft

This document is the synthesis of three parallel student drafts (`02-formalisms.md`, `pavel-claude.md`, `abstract.md`), the shared decisions logged in `diff.md`, and the professor's constraints recorded in `overleaf.md`. It intentionally replaces tiered organization with concept-based organization, and keeps the definition **logic-agnostic** — LTL, MTL, STL, and Timed Automata are possible back-ends, not parts of the formalism itself.

---

## 0. Goals

Design a representation of embedded software requirements and test cases such that:

1. A requirement written in natural language can be transcribed into a well-defined structure.
2. A test case can be transcribed into a comparable structure.
3. Coverage gaps between the two can be detected mechanically.

Two non-negotiables from the project brief:

- **Extensibility.** The ten Embraer requirements are a sample. New entity kinds, new operations, and new temporal patterns must be expressible without redesigning the core.
- **Matchability.** A formalized requirement and a formalized test case must share enough vocabulary to be compared pair-wise.

The formalism is defined at a higher abstraction level than any specific temporal logic or automaton. It describes *what a trace must satisfy*; the choice of verifier (LTL/MTL/STL/TA/monitor) is downstream.

---

## 1. Universe

### 1.1 Time

Time is a totally ordered set **T**. Per-requirement, one of three interpretations is chosen:

| Flavor  | Domain                            | Used when the requirement…                          |
| ------- | --------------------------------- | --------------------------------------------------- |
| Logical | Countable ordered set, no metric  | …only constrains ordering (req 03, 05)              |
| Metric  | Integer clock ticks (`k`, `k−1`)  | …refers to discrete steps (req 01)                  |
| Real    | ℝ≥0 with physical units           | …imposes physical deadlines (req 06, 09)            |

The choice determines which expressions and constraints are meaningful (e.g. `WITHIN 500 ns` requires real time; `e[k−1]` requires metric time).

### 1.2 Values

**V** is the universe of data values — booleans, integers, reals, enumerations, bit vectors, structured records, and opaque tokens. Every value has a **datatype**: a name plus an optional parameter schema `{ p₁: τ₁, …, pₙ: τₙ }`. Datatype is *not* an entity kind; it is an attribute of an entity that holds or carries values (§2.1).

### 1.3 Entities

An **entity** is a named, typed element that the formalism reasons about.

```
entity = (name, type, modifiers, description?)
```

Every entity has a **type** drawn from the *dictionary* (§2). The type determines which operations and modifiers are legal. Everything a requirement names is an entity — signals, storage cells, states, *events*, channels, values, opaque concepts.

The optional **description** is a free-text note attached to the entity. It exists as an escape hatch for context the typed modifiers cannot capture — "the calibration constant used by the temperature compensation routine", "the MODESET topic as specified in the DDS IDL", and so on. The formalism itself does not reason over description strings; they are opaque to coverage derivation. Their purpose is (a) human traceability between a requirement and its test cases and (b) downstream semantic matching (e.g. an LLM or a reviewer confirming that two entities with the same name in a requirement and a test actually refer to the same thing). Description is for what we *know* about an entity but cannot *type*.

### 1.4 Traces

A **trace** ρ is the complete observable history. At each time point t ∈ T it assigns:
- a value ρ(t)(e) ∈ V to every valued entity (signal, storage, value, …)
- an occurrence flag ρ(t)(e) ∈ {true, false} to every event entity

A requirement R is satisfied by ρ (written `ρ ⊨ R`) iff R's constraint (§7) holds over the trace. Traces are the semantic object — authors never write them by hand; testing samples them and verifiers reason over them.

---

## 2. The Dictionary

The dictionary is the open set of entity types the formalism understands natively. For each entry it declares:
- **Semantics** — what kind of thing this is.
- **Operations** — the verbs that may act on it, each with an associated **effect predicate** (the observable proposition that must hold after the action).
- **Modifiers** — attributes the requirement may attach.

Extending the formalism to a new requirement category is done by **adding a dictionary entry**, not by changing the core.

### 2.1 Built-in entity types

| Type       | Semantics                                                                                                  | Operations (→ effect predicate)                                                                              | Modifiers                       |
| ---------- | ---------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------------- |
| `SIGNAL`   | Software-internal value that evolves over time                                                             | `calculate(e, expr)` → `val(e) = ⟦expr⟧`; arithmetic use                                                     | `@initial`, `@datatype`         |
| `STORAGE`  | Addressable cell that persists a value (RAM, NVM, CPU register)                                            | `read(e, a)` → `val(e) = value_at(a)`; `store(e, dst)` → `value_at(dst) = val(e)`; `hold(e)` → `halted(e)`   | `@addr`, `@non_volatile`, `@register`, `@initial` |
| `STATE`    | Named behavioural mode (one active at a time within a state group)                                         | `set_state(s)` → `in_state(s)`; `in_state(s)` as predicate                                                   | —                               |
| `EVENT`    | Discrete occurrence at a point in time. Either fires at t or does not. An event *happens* — it has no value | `occurred(e)` as predicate; `count(e)`, `interval(e, n)` as expressions                                      | —                               |
| `CHANNEL`  | Communication medium carrying typed data (bus, DDS topic, message queue)                                   | `transmit(v, binding, ch)` → `transmitted(v, binding, ch)`; `receive(v, binding, ch)` as event predicate     | `@carries`                      |
| `VALUE`    | Named datum, constant, or sample of a datatype (`Mode Enable`, a specific `MastershipInfo` instance)       | identity comparison; used as argument to `transmit` / `store`                                                | `@datatype`                     |
| `ABSTRACT` | Opaque named concept whose internal structure is unknown (`calibration constant`, `task sequence`)         | `exists(e)`, `==`, `≠` only                                                                                  | —                               |
| `MAPPING`  | A finite keys-to-values table declared as part of the requirement (e.g. the IVORx → Exception table of req 04) | `m(k)` — lookup; `dom(m)` — key set; `size(m)` — cardinality                                                | `@keys(τ)`, `@values(τ)`        |

Three design choices worth stating explicitly:

- **Event is an entity.** Per `diff.md`, events are first-class entities that happen at points in time, not a separate mathematical object on the side.
- **Datatype is a modifier, not a type.** A `SIGNAL` / `CHANNEL` / `VALUE` carries a `@datatype(τ)` modifier. A datatype declaration itself may define a parameter schema, but a *particular* datum is a `VALUE` entity with that datatype bound.
- **VALUE is a first-class type** (per `diff.md`). It captures things like `'Mode Enable' = TRUE` or `MastershipInfo(Mastership_b = BACKUP)` — a named value, distinct from a signal (which varies over time) and from an abstract (which is opaque).

### 2.2 Modifiers

| Modifier             | Applies to              | Meaning                                            |
| -------------------- | ----------------------- | -------------------------------------------------- |
| `@initial(v)`        | SIGNAL, STORAGE         | Value at t = 0                                     |
| `@addr(0x…)`         | STORAGE                 | Fixed memory address                               |
| `@non_volatile`      | STORAGE                 | Persists across power cycles                       |
| `@register`          | STORAGE                 | CPU register (vs. memory)                          |
| `@datatype(τ)`       | SIGNAL, VALUE           | The (single) datatype this entity holds or is an instance of |
| `@carries({τ₁, …})`  | CHANNEL                 | Set of datatypes this channel may carry (singleton allowed) |
| `@params({p: τ, …})` | datatype declaration    | Parameter schema of a named datatype               |
| `@keys(τ)`           | MAPPING                 | Datatype of the keys                               |
| `@values(τ)`         | MAPPING                 | Datatype of the values                             |

Modifiers surface in constraints as `has(e, @mod)` predicates, so tests can check them independently of values stored at runtime.

The free-text `description` (see §1.3) is *not* a modifier — it carries no machine-checkable semantics and never appears in a `has(…)` predicate. It is the escape hatch for any context an author wants to preserve but cannot reduce to a typed attribute.

### 2.3 Extending the dictionary

A new entity type is added by stating:
1. What it *is* (semantics).
2. What operations apply, and what each operation's effect predicate is.
3. What modifiers are allowed.

Existing types and the rest of the formalism stay unchanged. Predicates, sequencing, and coverage all operate over whatever entries the dictionary contains.

---

## 3. Expressions

An **expression** denotes a value at a trace point. The base forms are:

| Expression                              | Meaning                                                                  |
| --------------------------------------- | ------------------------------------------------------------------------ |
| `e`                                     | Current value of entity `e`                                              |
| `e[k−n]`  /  `PREV(e)`                  | Value of `e` `n` discrete steps ago (n = 1 by default)                   |
| `e @ t`                                 | Value of `e` at absolute time `t`                                        |
| `e @ EV`                                | Value of `e` at the moment event `EV` last fired                         |
| `addr(e)`                               | Address attribute of a STORAGE entity                                    |
| `diff(a, b)`                            | Arithmetic difference `a − b`                                            |
| `signed(a)`                             | Signed reinterpretation of a bit pattern                                 |
| `peak_max(e)`, `peak_min(e)`            | Historical extrema of `e` up to the evaluation time                      |
| `count(EV)`                             | Total occurrences of `EV`                                                |
| `count(EV, since EV')`                  | Occurrences of `EV` since the last occurrence of `EV'`                   |
| `count(EV, [a, b])`                     | Occurrences of `EV` within the time interval `[a, b]`                    |
| `interval(EV, n)`                       | Time span between the 1st and n-th most recent occurrence of `EV`        |
| `m(k)`                                  | Value that MAPPING `m` assigns to key `k`                                |
| `dom(m)`, `size(m)`                     | Key set and cardinality of a MAPPING or set                              |
| constants `c ∈ V`                       | Literals                                                                 |
| `expr + expr`, `−`, `*`, `/`            | Arithmetic closure                                                       |

`e @ t` and `e @ EV` are first-class (per `diff.md`): they let a condition at the current time speak about values observed elsewhere in the trace without lifting into a temporal operator.

---

## 4. Predicates

A **predicate** is a boolean-valued condition on a trace point.

| Predicate          | Meaning                                             |
| ------------------ | --------------------------------------------------- |
| `a op b`           | Comparison, `op ∈ {=, ≠, <, ≤, >, ≥}`               |
| `e IS lit`         | Value equals a named literal (`TRUE`, `BACKUP`, …)  |
| `occurred(EV)`     | Event `EV` fires at the evaluation time             |
| `in_state(s)`      | System is currently in STATE `s`                    |
| `has(e, @mod)`     | Entity modifier holds                               |
| `exists(e)`        | Opaque-entity existence / identity assertion        |
| `ALL_OF { ψ, … }`  | Conjunction over a (finite) set of predicates       |
| `ANY_OF { ψ, … }`  | Disjunction over a (finite) set of predicates       |
| `FOR_EACH x IN S: ψ(x)` | ψ(x) holds for every element x of set / `dom(mapping)` S |
| `FOR_SOME x IN S: ψ(x)` | ψ(x) holds for at least one element of S        |
| `NOT ψ`            | Negation                                            |
| `TRUE`, `FALSE`    | Constant predicates                                 |

Sets and ordered sets are first-class. `ALL_OF` / `ANY_OF` take a set; effect structures (§6.2) are defined over ordered / partially ordered sets of steps. Tabular requirements (e.g. the IVORx → Exception mapping of req 04) are expressed by declaring a `MAPPING` entity and quantifying with `FOR_EACH`:

```
ENTITY ExceptionTable : MAPPING  @keys(INT) @values(ABSTRACT)
  = { 0 → CriticalInput,
      1 → MachineCheck,
      … }

EVENTUAL FOR_EACH x IN dom(ExceptionTable):
  val(IVOR[x]) = addr(ExceptionTable(x))
```

---

## 5. Actions

An **action** is an imperative operation performed at a point in time. Formally:

```
action = (operation, effect_predicate)
```

The operation is the verb (drawn from the operation list of its target entity's type, §2.1). The effect predicate is the observable proposition that must hold afterwards — the thing a verifier or test can check against a trace.

Initial operation table (extends as the dictionary extends):

| Operation                          | Effect predicate                 |
| ---------------------------------- | -------------------------------- |
| `CALCULATE e = expr`               | `val(e) = ⟦expr⟧`                |
| `READ e FROM a`                    | `val(e) = value_at(a)`           |
| `STORE e TO dst`                   | `value_at(dst) = val(e)`         |
| `INVOKE e`                         | `invoked(e)`                     |
| `HOLD e`                           | `halted(e)`                      |
| `TOGGLE e`                         | `val(e) = ¬ PREV(e)`             |
| `TRANSMIT v(binding) VIA ch`       | `transmitted(v, binding, ch)`    |
| `SET_STATE s`                      | `in_state(s)`                    |
| `IF ψ THEN α`                      | `ψ ⇒ pred(α)` (conditional)      |

---

## 6. Temporal Constructs

Temporal constructs compose predicates and actions into **trace predicates** — statements about the whole trace. Each construct is defined by its satisfaction condition, deliberately without referring to any specific temporal logic.

### 6.1 Base temporal quantifiers

| Construct                                    | ρ satisfies it iff                                                     |
| -------------------------------------------- | ---------------------------------------------------------------------- |
| `ALWAYS ψ`                                   | ∀ t ∈ T: ⟦ψ⟧(ρ, t)                                                     |
| `EVENTUAL ψ`                                 | ∃ t ∈ T: ⟦ψ⟧(ρ, t)                                                     |
| `INITIAL ψ`                                  | ⟦ψ⟧(ρ, 0)                                                              |
| `WHEN ψ_cond THEN ψ_effect`                  | ∀ t: ψ_cond(t) ⇒ ∃ t' ≥ t: ψ_effect(t')                                |
| `WHEN ψ_cond THEN ψ_effect WITHIN d`         | ∀ t: ψ_cond(t) ⇒ ∃ t' ∈ [t, t + d]: ψ_effect(t')                       |
| `P AND Q`, `P OR Q`                          | Boolean composition of trace predicates                                |

`WHEN … THEN …` replaces the prescriptive `TRIGGER → GUARD → EFFECT` template. A "guard" is simply an additional conjunct inside the condition side:

```
WHEN ψ_event AND ψ_guard THEN ψ_effect WITHIN d
```

This pattern is *common*, but the formalism does not require requirements to fit it. `ALWAYS`, `EVENTUAL`, `INITIAL`, and effect structures (§6.2) are equally first-class.

### 6.2 Effect structures — ordering and parallelism

When a requirement prescribes several actions, their *relative* timing is expressed as an **effect structure**:

```
structure = (steps, relations)
```

- `steps` is a finite set of actions.
- `relations` is a set of temporal relations between steps:

| Relation                        | Meaning                                                                  |
| ------------------------------- | ------------------------------------------------------------------------ |
| `PRECEDES(sᵢ, sⱼ)`              | `sᵢ` completes before `sⱼ` begins                                        |
| `WITHIN(sᵢ, sⱼ, d)`             | `sⱼ` occurs within duration `d` after `sᵢ`                               |
| `CONCURRENT(sᵢ, sⱼ)`            | No ordering imposed — they may overlap or occur simultaneously           |
| `EXCLUDES(sᵢ, sⱼ)`              | `sᵢ` and `sⱼ` never co-occur                                             |
| `IMMEDIATELY(sᵢ, sⱼ)`           | `sⱼ` at the next tick after `sᵢ`, with no intervening steps              |
| `IF ψ THEN sᵢ`                  | `sᵢ` required only when `ψ` holds at its scheduled time                  |

**Satisfaction.** ρ satisfies the structure iff there exists a mapping μ: steps → T such that every `pred(sᵢ)` holds at μ(sᵢ) and every relation is respected by μ.

Common patterns expressed this way:

| Pattern                | Structure                                                                   |
| ---------------------- | --------------------------------------------------------------------------- |
| `SEQ(s₁, …, sₙ)`       | `PRECEDES(sᵢ, sᵢ₊₁)` — ordered, but earlier steps may overlap / repeat     |
| `SEQ_STRICT(s₁, …, sₙ)`| `PRECEDES` + `EXCLUDES(sᵢ, sⱼ)` for i ≠ j — ordered and blocked until turn |
| `UNORDERED(s₁, …, sₙ)` | `CONCURRENT` between every pair — all must occur, order unconstrained       |
| `PARALLEL_WITH_JOIN`   | A DAG of `PRECEDES` relations — fork/join                                   |

The `SEQ` vs. `SEQ_STRICT` distinction matters because strict ordering implies an additional negative coverage obligation (fire step `i+1` before step `i` → effect must not hold).

### 6.3 `ON EV`

`ON EV` is shorthand for the predicate `occurred(EV)`. A requirement such as "*within 500 ns of a write to d*" is rendered:

```
WHEN ON write(d) AND ψ_guard THEN TOGGLE valid_range  WITHIN 500 ns
```

Events with duration are decomposed into a pair `EV_start` / `EV_end` (per decision log).

---

## 7. Requirements

A requirement is a named, scoped trace predicate:

```
requirement = (id, label, entities, constraint)
```

- `entities` — the entity declarations this requirement uses (type, modifiers). Entities declared in one requirement may be referenced by others; conflicts are a static error.
- `constraint` — a trace predicate built from §§3–6.

The constraint may be any composition of the temporal constructs — a pure `ALWAYS`, a pure `EVENTUAL`, a `WHEN ... THEN ...`, an effect structure, or a conjunction of these. The formalism does not force a `TRIGGER/GUARD/EFFECT` shape; most avionics requirements happen to fit it, but that is a rendering convenience.

### 7.1 Backend mapping (informative)

A concrete verifier can re-express a constraint in a chosen formalism:

| Constraint flavour                                      | Natural back-end      |
| ------------------------------------------------------- | --------------------- |
| Only ordering, boolean signals                          | LTL                   |
| Ordering + non-punctual time bounds, boolean signals    | MITL / MTL            |
| Time bounds + arithmetic on real-valued signals         | STL                   |
| Multi-step procedure where each step is a discrete mode | Timed Automata        |
| None of the above fit cleanly                           | Direct trace monitor  |

The choice is per-requirement and does not change the meaning of the requirement. The formalism *defines* satisfaction; the back-end *checks* satisfaction.

---

## 9. Reserved Keywords

The formalism reserves (at least): `ENTITY`, `REQ`, `WHEN`, `THEN`, `IF`, `ELSE`, `WITHIN`, `ALL_OF`, `ANY_OF`, `FOR_EACH`, `FOR_SOME`, `NOT`, `IS`, `ON`, `PREV`, `SEQ`, `SEQ_STRICT`, `UNORDERED`, `PRECEDES`, `CONCURRENT`, `EXCLUDES`, `IMMEDIATELY`, `ALWAYS`, `EVENTUAL`, `INITIAL`, `TRUE`, `FALSE`, `DECOMPOSE`, plus the operation verbs of the dictionary (`CALCULATE`, `READ`, `STORE`, `INVOKE`, `HOLD`, `TOGGLE`, `TRANSMIT`, `SET_STATE`, …) and the modifier prefix `@`.

Surface syntax is secondary. What matters is that each keyword has one fixed meaning defined in §§3–8.

---

## 10. What This Replaces in the Earlier Drafts

| Earlier idea                                                        | Status in this unified draft                                                        |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| Tier 1 / Tier 2 layering (`abstract.md`)                            | **Removed.** Organization is by concept.                                            |
| `TRIGGER / GUARD / EFFECT / DEADLINE` template (`02-formalisms.md`) | **Demoted to rendering convenience.** `WHEN … THEN … WITHIN d` is the base.         |
| `DDS_TOPIC` + `DATATYPE` as separate sorts (`02-formalisms.md`)     | **Merged.** `CHANNEL` carries `@carries`; datatype is a modifier on signals/values. |
| Formula-first philosophy (`pavel-claude.md`)                        | **Rejected.** Constraints are defined semantically over traces, independent of any one logic. |
| `x @ t` and `x @ EV` expressions (`pavel-claude.md`)                | **Adopted** into §3.                                                                |
| `seq` vs `seq_strict` distinction (`pavel-claude.md`)               | **Adopted** into §6.2.                                                              |
| Quantifier robustness coverage (`pavel-claude.md`)                  | **Adopted** into §8.2.                                                              |
| `MAPPING` for tabular requirements (`pavel-claude.md`)              | **Adopted** into §2.1 and §4.                                                       |
| Event as entity (`diff.md`)                                         | **Adopted** into §2.1.                                                              |
| `VALUE` as entity type (`diff.md`)                                  | **Adopted** into §2.1.                                                              |
| Parallel effect structures with timing constraints (`diff.md`)      | **Adopted** into §6.2.                                                              |
| Logic-agnostic definition (`diff.md`)                               | **Adopted** — §6 defines semantics directly, §7.1 treats logics as back-ends.       |
| Test-case formalism                                                 | **Deferred.** Will be reintroduced once the coverage side is stable.                |

---

## 11. Open Questions

Five hard patterns from the project brief are not fully solved by the current constructs. Each is illustrated with a concrete example that does *not* fit cleanly today.

### 11.1 Interval triggers

The formalism demands point events. A phrase like "*while handling an exception*" (req 05) is only expressible by splitting it into `exception_start` / `exception_end` and tracking "are we currently between the two?" as a piece of state the author has to thread through predicates manually.

Example — what a first-class interval would let us write:

```
WHEN DURING handling_exception AND ON write(R5)
THEN ψ_effect
```

versus the workaround today, which needs an auxiliary STATE `in_exception` plus transitions on the two point events. The question is whether `DURING e` deserves to be a base temporal construct, or a derived shorthand the formalism defines once.

### 11.2 Watchdog / resettable deadlines

A watchdog is "if signal X does not arrive within 100 ms of the last reset, raise a fault." This is a `WITHIN` whose clock is *reset* by a second event. `count` and `interval` don't capture it; neither do any of the effect-structure relations.

Example the formalism cannot currently phrase:

```
WHEN ON watchdog_start
THEN ψ_fault
WITHIN 100 ms  -- but the clock restarts on every ON feed_watchdog
```

### 11.3 Resource budgets

"Low-priority tasks must consume no more than 50 ms of CPU in any 1-second window." This is a bound on a *duration*, not on a count, over a sliding window. `count(EV, [a,b])` gets close but counts events, not accumulated time.

Example:

```
ALWAYS duration_of(executing(low_priority_task), [t−1s, t]) ≤ 50 ms
```

We don't have `duration_of(…)` over an interval, and the sliding window is not a first-class concept.

### 11.4 Mutual exclusion between effect structures

Two separate effect structures — e.g. the initialization sequence (req 06 + 07) and a shutdown sequence — must never be *simultaneously in progress*. Today `EXCLUDES` only relates two steps; it does not relate two whole structures.

Example:

```
EXCLUDES_STRUCTURE(init_sequence, shutdown_sequence)
```

The question is whether to lift `EXCLUDES` to the structure level or to introduce a separate "exclusivity between named behaviours" construct.

### 11.5 Sets of entities with runtime-unknown cardinality

Req 04 has a fixed set of IVORx registers given by a table. But the *real* Exception Vector Table's cardinality is defined by configuration — a future target MCU may have 16 IVORs, another 32. `MAPPING` with a literal table captures one specific configuration; it does not capture "whatever IVORs the target defines."

Example that today requires hard-coding cardinality:

```
ENTITY ExceptionTable : MAPPING @keys(INT) @values(ABSTRACT) @from_config("ivor_table")

EVENTUAL FOR_EACH x IN dom(ExceptionTable):
  val(IVOR[x]) = addr(ExceptionTable(x))
```

The question is how `@from_config(name)` (or some schema-level quantifier) is grounded — does the verifier instantiate the mapping from a configuration artefact, or is the MAPPING parametric in a set that a concrete test binds?

---

These should be addressed either by extending §6 with new temporal constructs or by extending the dictionary with new entity types — whichever keeps the core stable.
