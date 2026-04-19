# Abstract Formalism

This document defines the requirement formalism in a layered, abstract way. Each tier introduces new mathematical objects and properties on top of the previous tier. The formalism is independent of any particular temporal logic or automaton model — mapping to a concrete verification backend (LTL, MTL, STL, Timed Automata, etc.) is a separate step, not part of this definition.

---

## Tier 0 — Primitive Domains

These are the base sets from which everything else is constructed.

| Domain    | Symbol | Definition                                                                             |
| --------- | ------ | -------------------------------------------------------------------------------------- |
| Time      | **T**  | A totally ordered set. Discrete (T = N) or dense (T = R>=0), chosen per requirement.   |
| Values    | **V**  | The universe of all data values: booleans, integers, reals, enumerations, bit-vectors. |
| Names     | **N**  | A countable set of identifiers (entity names, event names, state labels).              |
| Addresses | **A**  | A set of storage locations (memory addresses, register identifiers).                   |

---

## Tier 1 — Entities and Traces

This tier defines the fundamental building blocks of the model. Everything in the system — signals, events, states, data — is an entity.

### 1.1 Entity

An **entity** is a named, typed element of the system.

> **Definition.** An entity is a tuple *e = (name, sort, attrs)* where:
> - *name in N*
> - *sort in {SIGNAL, STORAGE, EVENT, CHANNEL, STATE, VALUE, ABSTRACT}*
> - *attrs* is a (possibly empty) set of key-value pairs drawn from a sort-specific attribute schema

Sort-specific attributes:

| Sort     | Allowed attributes                                                                                    |
| -------- | ----------------------------------------------------------------------------------------------------- |
| SIGNAL   | initial value *v0 in V*, datatype *tau*                                                               |
| STORAGE  | address *a in A*, persistence class in {VOLATILE, NON_VOLATILE}, location class in {REGISTER, MEMORY} |
| EVENT    | *(none)* — an event either occurs or does not at a given time point                                   |
| CHANNEL  | carried datatype *tau*                                                                                |
| STATE    | *(none)* — a named behavioral mode                                                                    |
| VALUE    | datatype *tau*                                                                                        |
| ABSTRACT | *(none)* — an opaque concept with no known structure                                                  |

We write **E** for the finite set of all declared entities.

### Entity sorts

| Sort        | Meaning                                                                                                     |
| ----------- | ----------------------------------------------------------------------------------------------------------- |
| `SIGNAL`    | A software-internal variable that holds a value over time. Supports read, write, arithmetic.                |
| `STORAGE`   | An addressable location that holds a value (CPU register, memory address, NVM region).                      |
| `EVENT`     | A discrete occurrence at a point in time. At each time point, an event either occurs or does not.           |
| `CHANNEL`   | A communication medium that carries typed data (e.g. a DDS topic, a bus, a message queue).                  |
| `STATE`     | A named behavioral mode the system can occupy. Used for state-machine modeling.                              |
| `VALUE`     | A named data value or typed data object (e.g. a datatype with parameters, a constant, a transmitted datum). |
| `ABSTRACT`  | An opaque named concept with no known address or structure. Supports identity comparison only.               |

**Datatype as an attribute.** The type of data carried by a SIGNAL, CHANNEL, or VALUE entity is expressed as a *datatype* attribute, which may include a parameter schema *P = { p1: tau1, ..., pn: taun }*. This replaces having a separate DATATYPE sort — datatype is a property of an entity, not an entity kind.

### 1.2 Valuation

A **valuation** is a snapshot of the system at a single point in time.

> **Definition.** A valuation is a function *sigma: E -> V* assigning a value to every entity.

For entities of sort EVENT, the value is boolean: *sigma(e) = true* means the event occurs at that time point, *sigma(e) = false* means it does not.

We write **Sigma** for the set of all valuations.

### 1.3 Trace

A **trace** is the complete observable behavior of the system over time.

> **Definition.** A trace is a function *rho: T -> Sigma* assigning a valuation to each time point.

We write *rho(t)(e)* for the value of entity *e* at time *t*. For EVENT entities, *rho(t)(e) = true* means event *e* occurs at time *t*.

---

## Tier 2 — Expressions, Conditions, and Actions

This tier defines the language of observations and operations over the objects from Tier 1.

### 2.1 Expression

An **expression** is a function from a trace and a time point to a value.

> **Definition.** The set of expressions **Expr** is the smallest set such that:
> - *val(e)* in Expr — current value of entity *e* (semantics: *rho(t)(e)*)
> - *val(e, t')* in Expr — value of entity *e* at absolute time *t'* (semantics: *rho(t')(e)*)
> - *val(e, @ev)* in Expr — value of entity *e* at the most recent time when EVENT entity *ev* occurred (semantics: *rho(t_last)(e)* where *t_last = max{s <= t | rho(s)(ev) = true}*)
> - *prev(e)* in Expr — value at the previous time step (semantics: *rho(t-1)(e)*)
> - *addr(e)* in Expr — address of entity *e* (semantics: static lookup in *attrs(e)*)
> - *diff(a, b)* in Expr for *a, b in Expr* — arithmetic difference
> - *signed(a)* in Expr for *a in Expr* — signed reinterpretation
> - *max_peak(e)*, *min_peak(e)* in Expr — historical extrema: *max{rho(s)(e) | s <= t}*
> - *count(e)* in Expr for EVENT entity *e* — total occurrences: *|{s <= t | rho(s)(e) = true}|*
> - *count(e, since e')* in Expr for EVENT entities *e, e'* — occurrences of *e* since the last *e'*
> - *interval(e, n)* in Expr for EVENT entity *e* — time between the 1st and *n*-th most recent occurrences of *e*
> - any constant *c in V* is in Expr
> - standard arithmetic operators (+, -, *, /) close Expr

Every expression *phi in Expr* has a denotation *[[phi]](rho, t) in V*.

### 2.2 Condition

A **condition** is a boolean-valued predicate over the current state.

> **Definition.** The set of conditions **Cond** is the smallest set such that:
> - *cmp(a, op, b)* in Cond for *a, b in Expr* and *op in {=, !=, <, <=, >, >=}*
> - *is(a, lit)* in Cond for *a in Expr*, *lit in V* — value equals a named constant
> - *occurred(e)* in Cond for EVENT entity *e* — the event occurs at the current time
> - *in_state(s)* in Cond for STATE entity *s* — the system is in state *s*
> - *all_of(C)* in Cond for *C* a finite subset of Cond — conjunction
> - *any_of(C)* in Cond for *C* a finite subset of Cond — disjunction
> - *not(c)* in Cond for *c in Cond* — negation

Every condition *psi in Cond* has a denotation *[[psi]](rho, t) in {true, false}*.

### 2.3 Action

An **action** is an imperative operation whose observable outcome is captured by an **effect predicate**.

> **Definition.** An action is a pair *alpha = (op, pred)* where:
> - *op* is the operation kind (see table below)
> - *pred in Cond* is the effect predicate — the observable proposition that must hold after the action executes

| Operation kind             | Parameters                                 | Effect predicate              |
| -------------------------- | ------------------------------------------ | ----------------------------- |
| *calculate(e, expr)*       | entity *e*, expression *expr*              | *val(e) = [[expr]]*           |
| *read(e, a)*               | entity *e*, address *a*                    | *val(e) = value_at(a)*        |
| *store(e, dst)*            | entity *e*, destination *dst*              | *value_at(dst) = val(e)*      |
| *invoke(e)*                | entity *e*                                 | *invoked(e)*                  |
| *hold(e)*                  | entity *e*                                 | *halted(e)*                   |
| *toggle(e)*                | entity *e*                                 | *val(e) = not(prev(e))*       |
| *transmit(e, binding, ch)* | value *e*, param binding, channel *ch*     | *transmitted(e, binding, ch)* |
| *set_state(s)*             | state *s*                                  | *in_state(s)*                 |

A **conditional action** *if(c, alpha)* has the effect predicate *c => pred(alpha)*.

---

## Tier 3 — Requirements

A requirement is a constraint on the set of admissible traces of the system. This tier defines requirements abstractly — the choice of a concrete verification formalism (temporal logic, automata, etc.) is deferred.

### 3.1 Requirement

> **Definition.** A requirement is a tuple *R = (id, label, entities, constraint)* where:
> - *id in N* is a unique identifier
> - *label* is a human-readable description
> - *entities* is a subset of *E* — the entities participating in this requirement
> - *constraint* is a **trace predicate** (see below)

### 3.2 Trace Predicate

A trace predicate defines which traces satisfy the requirement.

> **Definition.** A trace predicate is a function *P: Trace -> {true, false}*. A trace *rho* **satisfies** a requirement *R* (written *rho |= R*) iff *P(rho) = true*.

Trace predicates are built compositionally from conditions (Tier 2) and **temporal quantifiers**:

> - *always(psi)* — condition *psi* holds at every time point: *for all t in T: [[psi]](rho, t)*
> - *eventually(psi)* — condition *psi* holds at some time point: *there exists t in T: [[psi]](rho, t)*
> - *after(psi1, psi2)* — whenever *psi1* holds, *psi2* holds at some later time: *for all t: [[psi1]](rho, t) implies there exists t' >= t: [[psi2]](rho, t')*
> - *after_within(psi1, psi2, d)* — whenever *psi1* holds, *psi2* holds within duration *d*: *for all t: [[psi1]](rho, t) implies there exists t' in [t, t+d]: [[psi2]](rho, t')*
> - *guarded(psi_trigger, psi_guard, psi_effect)* — whenever *psi_trigger* and *psi_guard* both hold, the effect follows: *for all t: [[psi_trigger]](rho, t) and [[psi_guard]](rho, t) implies there exists t' >= t: [[psi_effect]](rho, t')*
> - *initial(psi)* — condition *psi* holds at time 0: *[[psi]](rho, 0)*
> - *conjunction(P1, P2)* and *disjunction(P1, P2)* — standard boolean composition of trace predicates

These are abstract temporal quantifiers, not operators of any particular logic. They describe *what* the requirement demands without prescribing *how* to verify it.

### 3.3 Effect Structure

When a requirement involves multiple actions, their temporal relationships are expressed as an **effect structure** — a set of steps with explicit constraints on their relative ordering and timing.

> **Definition.** An effect structure is a tuple *S = (steps, constraints)* where:
> - *steps = {s_1, ..., s_n}* is a finite set of actions (from Tier 2.3)
> - *constraints* is a set of **temporal relations** between steps:

| Relation                  | Meaning                                                                        |
| ------------------------- | ------------------------------------------------------------------------------ |
| *precedes(s_i, s_j)*     | *s_i* must complete before *s_j* begins                                        |
| *within(s_i, s_j, d)*    | *s_j* must occur within duration *d* after *s_i*                               |
| *concurrent(s_i, s_j)*   | *s_i* and *s_j* may execute at the same time (no ordering imposed)             |
| *excludes(s_i, s_j)*     | *s_i* and *s_j* must not occur at the same time                                |
| *immediately(s_i, s_j)*  | *s_j* must occur at the next time point after *s_i* (no intervening steps)     |
| *conditional(c, s_i)*    | step *s_i* is only required when condition *c* holds                           |

**Satisfaction of an effect structure.** A trace *rho* satisfies *S* iff there exists a mapping *mu: steps -> T* assigning a time point to each step such that:
- for each step *s_i*: *[[pred(s_i)]](rho, mu(s_i))* holds
- all relations in *constraints* are respected by *mu*

Common patterns expressed as effect structures:

- **Unordered** (all steps must happen, order doesn't matter): steps with no *precedes* constraints between them — they are implicitly *concurrent*.
- **Totally ordered sequence**: *precedes(s_1, s_2), precedes(s_2, s_3), ...* — a linear chain.
- **Parallel with synchronization**: some steps are *concurrent*, others have *precedes* constraints — a partial order (DAG).

---

## Tier 4 — Test Cases and Coverage

A test case is a controlled experiment that checks whether a specific instance of a requirement's constraint holds.

### 4.1 Test Case

> **Definition.** A test case is a tuple *TC = (id, req, setup, stimulus, verdict)* where:
> - *id in N* — unique test identifier
> - *req* — reference to requirement *R*
> - *setup* — a partial valuation *sigma_0: E' -> V* (*E' subset of E*) establishing preconditions
> - *stimulus* — an ordered sequence of test actions:
>   - *fire(e, delay)* — trigger EVENT entity *e* after *delay in T*
>   - *tick(bindings)* — advance one discrete time step, optionally updating entity values
> - *verdict* — a set of **check** assertions:
>   - *check(pred, polarity, deadline)* where *pred in Cond*, *polarity in {POS, NEG}*, and *deadline in T union {infinity}*

A test case **passes** iff the trace *rho* produced by executing the stimulus satisfies:
- for each *check(pred, POS, d)*: *[[pred]](rho, t)* holds within *d* of the final stimulus
- for each *check(pred, NEG, d)*: *[[pred]](rho, t)* does NOT hold within *d*

When the requirement's constraint includes a bounded temporal quantifier (e.g. *after_within* with a finite *d*), at least one check must include a corresponding finite deadline.

### 4.2 Coverage

Coverage analysis determines whether the set of test cases exercises all structurally interesting scenarios of a requirement.

> **Definition.** The **predicate space** of a requirement *R* is the set *PS(R)* of all atomic conditions appearing in *R*'s trace predicate.

> **Definition.** A **coverage obligation** is a pair *(assignment, expected)* where:
> - *assignment: PS(R) -> {true, false}* — a truth assignment to the predicate space
> - *expected in {POS, NEG}* — whether the effect should or should not hold under this assignment

Coverage obligations are derived from the structure of the requirement:

| Structure                           | Obligations                                                                                                         |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| *all_of({c_1, ..., c_n})* in guard  | MC/DC: each *c_i* independently determines the outcome (n+1 assignments)                                           |
| *any_of({c_1, ..., c_n})* in guard  | Each *c_i* alone true (n positive); all false (1 negative)                                                         |
| Finite time bound *d*               | At least one check at the boundary of *d*                                                                          |
| Negative case                       | At least one assignment where the activating condition holds but the guard is false, with expected = NEG            |

> **Definition.** A test suite *{TC_1, ..., TC_m}* **covers** a requirement *R* iff every coverage obligation of *R* is matched by at least one test case whose setup and stimulus realize the obligation's truth assignment.
