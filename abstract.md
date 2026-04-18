# Abstract Formalism

This document defines the requirement formalism in a layered, abstract way. Each tier introduces new mathematical objects and properties on top of the previous tier.

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

## Tier 1 — Entities, Events, and Traces

This tier defines the fundamental building blocks of the model.

### 1.1 Entity

An **entity** is a named, typed element of the system that can hold a value.

> **Definition.** An entity is a tuple *e = (name, sort, attrs)* where:
> - *name in N*
> - *sort in {SIGNAL, STORAGE, DDS_TOPIC, DATATYPE, STATE, ABSTRACT}*
> - *attrs* is a (possibly empty) set of key-value pairs drawn from a sort-specific attribute schema

Sort-specific attributes:

| Sort      | Allowed attributes                                                                                    |
| --------- | ----------------------------------------------------------------------------------------------------- |
| SIGNAL    | initial value *v0 in V*                                                                               |
| STORAGE   | address *a in A*, persistence class in {VOLATILE, NON_VOLATILE}, location class in {REGISTER, MEMORY} |
| DDS_TOPIC | *(none)*                                                                                              |
| DATATYPE  | a parameter schema *P = { p1: tau1, ..., pn: taun }* where each *tau_i* is a value type               |
| STATE     | *(none)*                                                                                              |
| ABSTRACT  | *(none)*                                                                                              |

We write **E** for the finite set of all declared entities.

### 1.2 State and Valuation

A **valuation** is a snapshot of the system at a single point in time.

> **Definition.** A valuation is a function *sigma: E -> V* assigning a value to every entity.

We write **Sigma** for the set of all valuations.

### 1.3 Event

An **event** is an instantaneous occurrence at a point in time.

> **Definition.** An event kind is a function symbol from the set:
> - *named(n)* — a named point event with label *n in N*
> - *write(e)* — a write to entity *e in E*
> - *receive(e, binding)* — reception of a data instance of datatype *e*, with an optional parameter binding *binding: P -> V*
> - *return(e)* — completion of an invoked routine *e*

Events with duration are modelled as a pair of point events: *(named(n_start), named(n_end))*.

We write **Omega** for the set of all event kinds.

### 1.4 Trace

A **trace** is the complete observable behavior of the system over time.

> **Definition.** A trace is a pair *rho = (sigma, omega)* where:
> - *sigma: T -> Sigma* assigns a valuation to each time point
> - *omega: T -> P(Omega)* assigns a (possibly empty) set of events to each time point

We write *sigma(t)(e)* for the value of entity *e* at time *t*, and *ev in omega(t)* when event *ev* occurs at time *t*.

---

## Tier 2 — Expressions, Conditions, and Actions

This tier defines the language of observations and operations over the objects from Tier 1.

### 2.1 Expression

An **expression** is a function from a trace and a time point to a value.

> **Definition.** The set of expressions **Expr** is the smallest set such that:
> - *val(e)* in Expr — current value of entity *e* (semantics: *sigma(t)(e)*)
> - *prev(e)* in Expr — value at the previous time step (semantics: *sigma(t-1)(e)*)
> - *addr(e)* in Expr — address of entity *e* (semantics: static lookup in *attrs(e)*)
> - *diff(a, b)* in Expr for *a, b in Expr* — arithmetic difference
> - *signed(a)* in Expr for *a in Expr* — signed reinterpretation
> - *max_peak(e)*, *min_peak(e)* in Expr — historical extrema: *max{sigma(s)(e) | s <= t}*
> - *count(ev)* in Expr for *ev in Omega* — total occurrences: *|{s <= t | ev in omega(s)}|*
> - *count(ev, since ev')* in Expr — occurrences of *ev* since the last *ev'*
> - *interval(ev, n)* in Expr — time between the 1st and *n*-th most recent occurrences of *ev*
> - any constant *c in V* is in Expr
> - standard arithmetic operators (+, -, *, /) close Expr

Every expression *phi in Expr* has a denotation *[[phi]](rho, t) in V*.

### 2.2 Condition

A **condition** is a boolean-valued predicate over the current state.

> **Definition.** The set of conditions **Cond** is the smallest set such that:
> - *cmp(a, op, b)* in Cond for *a, b in Expr* and *op in {=, !=, <, <=, >, >=}*
> - *is(a, lit)* in Cond for *a in Expr*, *lit in V* — value equals a named constant
> - *all_of(C)* in Cond for *C* a finite subset of Cond — conjunction
> - *any_of(C)* in Cond for *C* a finite subset of Cond — disjunction
> - *not(c)* in Cond for *c in Cond* — negation

Every condition *psi in Cond* has a denotation *[[psi]](rho, t) in {true, false}*.

### 2.3 Action

An **action** is an imperative operation whose observable outcome is captured by an **effect predicate**.

> **Definition.** An action is a pair *alpha = (op, pred)* where:
> - *op* is the operation kind (see table below)
> - *pred in Cond* is the effect predicate — the observable proposition that must hold after the action executes

| Operation kind             | Parameters                                | Effect predicate              |
| -------------------------- | ----------------------------------------- | ----------------------------- |
| *calculate(e, expr)*       | entity *e*, expression *expr*             | *val(e) = [[expr]]*           |
| *read(e, a)*               | entity *e*, address *a*                   | *val(e) = value_at(a)*        |
| *store(e, dst)*            | entity *e*, destination *dst*             | *value_at(dst) = val(e)*      |
| *invoke(e)*                | entity *e*                                | *invoked(e)*                  |
| *hold(e)*                  | entity *e*                                | *halted(e)*                   |
| *toggle(e)*                | entity *e*                                | *val(e) = not(prev(e))*       |
| *transmit(e, binding, ch)* | datatype *e*, param binding, channel *ch* | *transmitted(e, binding, ch)* |
| *set_state(s)*             | state *s*                                 | *in_state(s)*                 |

A **conditional action** *if(c, alpha)* has the effect predicate *c => pred(alpha)*.

---

## Tier 3 — Requirements

A requirement is a temporal obligation over traces, built from the components defined in Tiers 1-2.

### 3.1 Requirement

> **Definition.** A requirement is a tuple *R = (id, label, form, effects)* where:
> - *id in N* is a unique identifier
> - *label* is a human-readable description
> - *form* is the **requirement form** (see below)
> - *effects = (alpha_1, ..., alpha_n)* is an ordered sequence of actions, optionally marked as **ordered** (sequential execution required)

### 3.2 Requirement Form

A requirement takes exactly one of two forms:

**Triggered form:**

> *triggered(trigger, guard, deadline)* where:
> - *trigger in Omega* — the causing event
> - *guard in Cond union {T}* — an optional condition (*T* = always true)
> - *deadline in T union {infinity}* — an optional time bound

**Untriggered form:**

> *untriggered(modality)* where:
> - *modality in {INVARIANT, EVENTUAL}*

### 3.3 Satisfaction

A trace *rho* **satisfies** a requirement *R* (written *rho |= R*) according to the following rules. Let *eff* denote the conjunction of effect predicates of all actions in *R.effects*.

**Triggered, unordered:**

> *rho |= R* iff for all *t in T*:
> *[[trigger]](rho, t) and [[guard]](rho, t)* implies there exists *t' in [t, t + deadline]* such that *[[eff]](rho, t')*.

In temporal logic notation: *G(trigger ^ guard -> F[0, deadline](eff))*.

**Triggered, ordered** (effects *alpha_1, ..., alpha_n*):

> *rho |= R* iff for all *t in T*:
> *[[trigger]](rho, t)* implies there exist *t <= t_1 <= ... <= t_n <= t + deadline* such that *[[pred(alpha_i)]](rho, t_i)* for all *i*.

In temporal logic notation: *G(trigger -> pred_1 U (pred_2 U ... pred_n))* with time bounds if applicable.

**Untriggered, INVARIANT:**

> *rho |= R* iff for all *t in T*: *[[eff]](rho, t)*.

In temporal logic notation: *G(eff)*.

**Untriggered, EVENTUAL:**

> *rho |= R* iff there exists *t in T*: *[[eff]](rho, t)*.

In temporal logic notation: *F(eff)*.

### 3.4 Verification Tier Selection

The **verification tier** determines which formal backend is used to check satisfaction. It is selected based on the features present in the requirement:

> **Definition.** The verification tier of a requirement *R* is the least element of the chain *LTL < MTL < STL* (with *TA* as an alternative) such that:
> - **LTL** — sufficient when *R* uses only ordering and event causality: *deadline = infinity* and all expressions are boolean-valued.
> - **MTL** — required when *R* has a finite *deadline* but all expressions are boolean-valued.
> - **STL** — required when *R* involves arithmetic over real-valued expressions.
> - **TA** — preferred when *R* has ordered effects with multiple discrete steps forming a procedure.

---

## Tier 4 — Test Cases and Coverage

A test case is a controlled experiment that checks whether a specific instance of a requirement's satisfaction relation holds.

### 4.1 Test Case

> **Definition.** A test case is a tuple *TC = (id, req, setup, stimulus, verdict)* where:
> - *id in N* — unique test identifier
> - *req* — reference to requirement *R*
> - *setup* — a partial valuation *sigma_0: E' -> V* (*E' subset of E*) establishing preconditions
> - *stimulus* — an ordered sequence of test actions:
>   - *fire(ev, delay)* — inject event *ev in Omega* after *delay in T*
>   - *tick(bindings)* — advance one discrete time step, optionally updating entity values
> - *verdict* — a set of **check** assertions:
>   - *check(pred, polarity, deadline)* where *pred in Cond*, *polarity in {POS, NEG}*, and *deadline in T union {infinity}*

A test case **passes** iff the trace *rho* produced by executing the stimulus satisfies:
- for each *check(pred, POS, d)*: *[[pred]](rho, t)* holds within *d* of the final stimulus
- for each *check(pred, NEG, d)*: *[[pred]](rho, t)* does NOT hold within *d*

When the requirement has a finite deadline, at least one check must include a corresponding finite deadline (*deadline != infinity*).

### 4.2 Coverage

Coverage analysis determines whether the set of test cases exercises all structurally interesting scenarios of a requirement.

> **Definition.** The **predicate space** of a requirement *R* is the set *PS(R)* of all atomic conditions appearing in the trigger, guard, and effect predicates of *R*.

> **Definition.** A **coverage obligation** is a pair *(assignment, expected)* where:
> - *assignment: PS(R) -> {true, false}* — a truth assignment to the predicate space
> - *expected in {POS, NEG}* — whether the effect should or should not hold under this assignment

Coverage obligations are derived from the structure of the requirement:

| Structure                          | Obligations                                                                                 |
| ---------------------------------- | ------------------------------------------------------------------------------------------- |
| *all_of({c_1, ..., c_n})* in guard | MC/DC: each *c_i* independently determines the outcome (n+1 assignments)                    |
| *any_of({c_1, ..., c_n})* in guard | Each *c_i* alone true (n positive); all false (1 negative)                                  |
| Finite deadline                    | At least one check at the deadline boundary                                                 |
| Negative case                      | At least one assignment where the trigger fires but the guard is false, with expected = NEG |

> **Definition.** A test suite *{TC_1, ..., TC_m}* **covers** a requirement *R* iff every coverage obligation of *R* is matched by at least one test case whose setup and stimulus realize the obligation's truth assignment.
