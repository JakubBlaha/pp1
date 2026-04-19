# Abstract Formalism — Final

This document defines the requirement formalism in an abstract, logic-agnostic way. It specifies the base mathematical objects — domains, entities, traces, expressions, predicates, actions, requirements, tests, and coverage — without committing to any particular temporal logic or automaton model. Concrete verification back-ends (LTL / MITL / STL / Timed Automata / direct monitor) are noted at the end as *informative* mappings, not as structural layers of the formalism.

Two project non-negotiables shape the design:

1. **Extensibility.** The ten Embraer requirements are a sample. The formalism must admit new entity kinds and new operations by *extending a dictionary*, not by rewriting the core.
2. **Matchability.** A formalised requirement and a formalised test case must share enough vocabulary to be compared pair-wise; coverage gaps must be mechanically detectable.

---

## 1. Primitive Domains

These are the base sets from which everything else is constructed.

| Domain | Symbol | Definition                                                                                             |
| ------ | ------ | ------------------------------------------------------------------------------------------------------ |
| Time   | **T**  | A totally ordered set. One of three interpretations is chosen per requirement (see below).             |
| Values | **V**  | The universe of data values: booleans, integers, reals, enumerations, bit-vectors, structured records. |

Identifiers (entity names, event names, state labels, type names) and storage addresses are not primitive domains: names are the labels attached to entities at declaration, and addresses are just values bound by the *address* modifier (§2.3). Neither is quantified over independently of the entity set **E**.

**Time flavours.** For each requirement exactly one interpretation of **T** is fixed:

| Flavour | Carrier                          | Used when the requirement…            |
| ------- | -------------------------------- | ------------------------------------- |
| Logical | Countable ordered set, no metric | …only constrains ordering             |
| Metric  | Integer clock ticks (**T = N**)  | …refers to discrete steps             |
| Real    | **T = R>=0** with physical units | …imposes deadlines in physical units  |

The flavour determines which expressions and temporal constructs are well-typed (a duration bound needs metric or real time; a step-offset reference needs metric time).

## 2. The Dictionary

The **dictionary** **D** is the open set of entity types the formalism understands natively. Each entry is a triple *(semantics, operations, modifier schema)* declaring what kind of thing the type denotes, what verbs may act on it (each with an associated effect predicate, §5), and what modifier kinds it admits.

> **Definition.** The formalism is parameterised by a dictionary *D*. The dictionary is *open*: extending the formalism to a new requirement category is done by adding a new entry to *D*, not by altering the core.

### 2.1 Built-in dictionary entries

| Type        | Semantics                                                                                      | Operations (→ effect predicate)                                                                                   | Modifier kinds                                        |
| ----------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `SIGNAL`    | Software-internal value that evolves over time.                                                | *calculate* → value equals a given expression                                                                     | initial value, datatype                               |
| `STORAGE`   | Addressable cell persisting a value (RAM, NVM, CPU register).                                  | *read* → value equals contents at address; *store* → contents at destination equal value; *hold* → value halted   | address, non-volatility, register flag, initial value |
| `EVENT`     | Discrete occurrence at a point in time. Either fires at *t* or does not; carries no value.     | *occurrence* as predicate; *count*, *interval* as expressions                                                     | —                                                     |
| `CHANNEL`   | Communication medium carrying typed data (bus, DDS topic, message queue).                      | *transmit(value, binding)* → transmission predicate holds on the channel; *receive* as event predicate            | carried datatypes                                     |
| `STATE`     | Named behavioural mode (one active at a time within a state group).                            | *set_state* → system is in state; *in_state* as predicate                                                         | —                                                     |
| `VALUE`     | Named datum or sample of a datatype.                                                           | identity comparison; argument to *transmit* / *store*                                                             | datatype                                              |
| `MAPPING`   | Finite table keys → values declared as part of the requirement.                                | lookup at key; key-set; cardinality                                                                               | key datatype, value datatype                          |
| `ABSTRACT`  | Opaque named concept whose internal structure is unknown.                                      | existence and identity comparison only                                                                            | —                                                     |

Three design choices are worth stating explicitly:

- **Event is an entity.** Events are first-class entries of *D*, not a separate mathematical object on the side.
- **Datatype is a modifier, not a type.** A `SIGNAL` / `CHANNEL` / `VALUE` carries a datatype attribute; a datatype declaration itself may define a parameter schema *P = { p1: tau1, ..., pn: taun }*.
- **VALUE is first-class**, distinct from `SIGNAL` (varies over time) and `ABSTRACT` (opaque).

### 2.2 Entity

> **Definition.** An entity is a tuple *e = (name, type, modifiers, description)* where:
> - *name* is a unique identifier
> - *type in D*
> - *modifiers* is a (possibly empty) set of key-value pairs drawn from the modifier schema of *type*
> - *description* is an optional free-text note

We write **E** for the finite set of all declared entities.

### 2.3 Modifiers

| Modifier kind      | Applies to             | Meaning                                              |
| ------------------ | ---------------------- | ---------------------------------------------------- |
| initial value      | SIGNAL, STORAGE        | Value at *t = 0*                                     |
| address            | STORAGE                | Fixed memory address (target-architecture value)     |
| non-volatility     | STORAGE                | Persists across power cycles                         |
| register flag      | STORAGE                | CPU register (vs. memory)                            |
| datatype *tau*     | SIGNAL, VALUE          | Datatype this entity holds or is an instance of      |
| carried datatypes  | CHANNEL                | Set of datatypes the channel may carry               |
| parameter schema   | datatype declaration   | Parameter schema of a named datatype                 |
| key datatype       | MAPPING                | Datatype of the keys                                 |
| value datatype     | MAPPING                | Datatype of the values                               |

Modifiers surface in predicates (§4) as the atom *has(e, m, v)*, so a test can verify them independently of values stored at runtime.

### 2.4 Description

The *description* slot is an escape hatch for context the typed modifiers cannot capture. The formalism does *not* reason over description strings; they are opaque to coverage derivation. Their purpose is (a) human traceability between a requirement and its test cases and (b) downstream semantic matching (reviewer or LLM confirming that two entities named the same in a requirement and a test refer to the same thing). Descriptions never appear in a predicate.

### 2.5 Extending the dictionary

A new entity type is added by declaring (i) what it *is*, (ii) what operations apply and their effect predicates, (iii) what modifiers are admitted. The rest of the formalism operates uniformly over whatever entries *D* contains.

## 3. Valuations and Traces

### 3.1 Valuation

> **Definition.** A valuation is a function *sigma: E -> V* assigning a value to every entity. For entities of type `EVENT`, the value is boolean: *sigma(e) = true* iff the event occurs at that time point.

We write **Sigma** for the set of all valuations.

### 3.2 Trace

> **Definition.** A trace is a function *rho: T -> Sigma*. We write *rho(t)(e)* for the value of entity *e* at time *t*.

Traces are the semantic object. Authors never write them by hand; testing samples them and verifiers reason over them.

## 4. Expressions and Predicates

### 4.1 Expression

An **expression** is a function from a trace and a time point to a value.

> **Definition.** The set of expressions **Expr** is the smallest set such that:
> - *val(e)* — current value: *rho(t)(e)*
> - *val(e, t')* — value at absolute time *t' in T*: *rho(t')(e)*
> - *val(e, @ev)* — value at the last occurrence of EVENT *ev*: *rho(t_last)(e)* with *t_last = max{s <= t | rho(s)(ev) = true}*
> - *prev(e)* — *rho(t-1)(e)* (metric time only)
> - *at(e, n)* — value *n* discrete steps ago: *rho(t-n)(e)* (metric time only, *n >= 1*)
> - *addr(e)* — static lookup of the address modifier on *e*
> - *diff(a, b)*, *signed(a)* for *a, b in Expr*
> - *max_peak(e)*, *min_peak(e)* — historical extrema *sup/inf{rho(s)(e) | s <= t}*
> - *count(e)* for EVENT *e* — total occurrences up to *t*
> - *count(e, since e')*, *count(e, [a, b])* — windowed counts
> - *interval(e, n)* for EVENT *e* — span between the 1st and *n*-th most recent occurrence
> - *lookup(m, k)*, *keys(m)*, *card(m)* for MAPPING *m*
> - any constant *c in V*
> - standard arithmetic combinators (+, -, *, /) closed under *V* where defined

Every *phi in Expr* has a denotation *[[phi]](rho, t) in V*. Value-at-time and value-at-event references are first-class: they let a predicate at the current time speak about values observed elsewhere in the trace without lifting into a temporal operator.

### 4.2 Predicate

A **predicate** is a boolean-valued condition on a trace point.

> **Definition.** The set of predicates **Pred** is the smallest set such that:
> - *cmp(a, op, b)* for *a, b in Expr*, *op in {=, !=, <, <=, >, >=}*
> - *is(a, lit)* for *a in Expr*, *lit in V* — value equals a named constant
> - *occurred(e)* for EVENT *e* — the event fires at the current time
> - *in_state(s)* for STATE *s*
> - *has(e, m, v)* — entity *e* carries modifier *m* with binding *v*
> - *exists(e)*, *same(e1, e2)* for ABSTRACT entities
> - *all_of(C)*, *any_of(C)* for finite *C subset of Pred* — conjunction / disjunction
> - *not(psi)* for *psi in Pred*
> - *forall(x in S, psi(x))*, *exists(x in S, psi(x))* for a finite set *S* (for example *keys(m)*)
> - boolean constants *top*, *bot*

Every *psi in Pred* has a denotation *[[psi]](rho, t) in {true, false}*. Finite conjunction, disjunction, and quantification take a set; tabular requirements are expressed by declaring a MAPPING and quantifying over its domain.

## 5. Actions

An **action** is an imperative operation whose observable outcome is captured by an **effect predicate**.

> **Definition.** An action is a tuple *alpha = (op, args, pred)* where *op* is an operation kind drawn from the dictionary entry of the target entity, *args* are its parameters, and *pred in Pred* is the effect predicate.

Initial operation table (extends with the dictionary):

| Operation                           | Parameters                                    | Effect predicate              |
| ----------------------------------- | --------------------------------------------- | ----------------------------- |
| *calculate(e, expr)*                | entity *e*, expression *expr*                 | *val(e) = [[expr]]*           |
| *read(e, a)*                        | entity *e*, address *a*                       | *val(e) = value_at(a)*        |
| *store(e, dst)*                     | entity *e*, destination *dst*                 | *value_at(dst) = val(e)*      |
| *invoke(e)*                         | entity *e*                                    | *invoked(e)*                  |
| *hold(e)*                           | entity *e*                                    | *halted(e)*                   |
| *toggle(e)*                         | entity *e*                                    | *val(e) = not(prev(e))*       |
| *transmit(v, binding, ch)*          | VALUE *v*, param binding, CHANNEL *ch*        | *transmitted(v, binding, ch)* |
| *set_state(s)*                      | STATE *s*                                     | *in_state(s)*                 |

A **conditional action** *if(c, alpha)* has the effect predicate *c => pred(alpha)*.

## 6. Temporal Constructs

Temporal constructs compose predicates and actions into **trace predicates** — functions *P: Trace -> {true, false}*. A trace *rho* **satisfies** a requirement *R* (written *rho |= R*) iff *R*'s constraint *P* is such that *P(rho) = true*. Each construct is defined by its satisfaction condition, without reference to any specific temporal logic.

### 6.1 Base temporal quantifiers

| Construct                                                   | *rho* satisfies it iff                                                                               |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| *always(psi)*                                               | for all *t in T*: *[[psi]](rho, t)*                                                                  |
| *eventually(psi)*                                           | there exists *t in T*: *[[psi]](rho, t)*                                                             |
| *initial(psi)*                                              | *[[psi]](rho, 0)*                                                                                    |
| *triggered(psi_cond, psi_effect)*                           | for all *t*: *[[psi_cond]](rho, t)* implies there exists *t' >= t*: *[[psi_effect]](rho, t')*        |
| *triggered_within(psi_cond, psi_effect, d)*                 | for all *t*: *[[psi_cond]](rho, t)* implies there exists *t' in [t, t+d]*: *[[psi_effect]](rho, t')* |
| *conjunction(P1, P2)*, *disjunction(P1, P2)*, *negation(P)* | standard boolean composition of trace predicates                                                     |

A *guard* is merely an additional conjunct inside *psi_cond*; the formalism does not privilege a `TRIGGER/GUARD/EFFECT` shape.

### 6.2 Effect structures

When a requirement prescribes several actions, their relative timing is expressed as an **effect structure**.

> **Definition.** An effect structure is a pair *S = (steps, constraints)* where *steps = {s_1, ..., s_n}* is a finite set of actions and *constraints* is a set of temporal relations:

| Relation                  | Meaning                                                                         |
| ------------------------- | ------------------------------------------------------------------------------- |
| *precedes(s_i, s_j)*      | *s_i* completes before *s_j* begins                                             |
| *within(s_i, s_j, d)*     | *s_j* occurs within duration *d* after *s_i*                                    |
| *concurrent(s_i, s_j)*    | no ordering imposed                                                             |
| *excludes(s_i, s_j)*      | *s_i* and *s_j* must not co-occur                                               |
| *immediately(s_i, s_j)*   | *s_j* at the next tick after *s_i*, with no intervening steps                   |
| *conditional(c, s_i)*     | step *s_i* is required only when *c* holds                                      |

> **Satisfaction.** *rho |= S* iff there exists a mapping *mu: steps -> T* such that *[[pred(s_i)]](rho, mu(s_i))* holds for each *s_i* and every relation in *constraints* is respected by *mu*.

Common patterns:

- **Unordered** (all steps must happen, order free): implicit *concurrent* between every pair.
- **Ordered sequence**: *precedes(s_1, s_2), precedes(s_2, s_3), ...* — earlier steps may overlap or repeat.
- **Strict ordered sequence**: *precedes* + pairwise *excludes* — ordered AND blocked until turn. (The distinction matters for coverage: strict ordering generates an extra negative obligation that firing *s_{i+1}* before *s_i* must falsify the effect.)
- **Parallel with join**: a DAG of *precedes* relations.

Events with duration are modelled as a pair of point events (*start* and *end*).

## 7. Requirements

> **Definition.** A requirement is a tuple *R = (id, label, entities, constraint)* where:
> - *id* is a unique requirement identifier
> - *label* is a human-readable description
> - *entities subset of E* — the entities participating in this requirement (type, modifiers, description)
> - *constraint* is a trace predicate built from §§4–6

Entities declared in one requirement may be referenced by others; declaration conflicts are a static error. The constraint may be any composition of the base temporal quantifiers and effect structures — a pure *always*, a pure *eventually*, a *triggered_within*, an effect structure, or a conjunction thereof.

## 8. Test Cases and Coverage

### 8.1 Test case

> **Definition.** A test case is a tuple *TC = (id, req, setup, stimulus, verdict)* where:
> - *id* is a unique test identifier
> - *req* — reference to a requirement *R*
> - *setup* — a partial valuation *sigma_0: E' -> V* (*E' subset of E*) establishing preconditions
> - *stimulus* — an ordered sequence of test actions:
>   - *fire(e, delay)* — trigger EVENT *e* after *delay in T*
>   - *tick(bindings)* — advance one discrete time step, optionally updating entity values
> - *verdict* — a set of **check** assertions *check(pred, polarity, deadline)* with *pred in Pred*, *polarity in {POS, NEG}*, *deadline in T union {infinity}*

> **Pass condition.** *TC* passes on the trace *rho* produced by executing *stimulus* iff:
> - for each *check(pred, POS, d)*: *[[pred]](rho, t)* holds within *d* of the final stimulus
> - for each *check(pred, NEG, d)*: *[[pred]](rho, t)* does NOT hold within *d*

When the requirement's constraint uses a bounded temporal quantifier (*triggered_within* or an effect-structure *within*), at least one check must carry a corresponding finite deadline.

### 8.2 Coverage

> **Definition.** The **predicate space** *PS(R)* is the set of atomic predicates appearing in *R*'s constraint.

> **Definition.** A **coverage obligation** is a pair *(assignment, expected)* where *assignment: PS(R) -> {true, false}* and *expected in {POS, NEG}*.

Obligations are derived from the structure of *R*:

| Structure                             | Obligations                                                                                     |
| ------------------------------------- | ----------------------------------------------------------------------------------------------- |
| *all_of({c_1, ..., c_n})* in cond     | MC/DC: each *c_i* independently determines the outcome (*n+1* assignments)                     |
| *any_of({c_1, ..., c_n})* in cond     | Each *c_i* alone true (*n* positive); all false (*1* negative)                                  |
| Finite time bound *d*                 | At least one check at the boundary of *d* (interior and just beyond)                            |
| Negative case                         | Activating condition holds but guard fails, with *expected = NEG*                               |
| Strict ordered sequence               | Firing *s_{i+1}* before *s_i* must falsify the effect (*expected = NEG*)                        |
| *forall(x in S, psi(x))* (robustness) | Per-element failure tests: for each *x in S*, an assignment where *psi(x)* alone fails          |

> **Definition.** A test suite *{TC_1, ..., TC_m}* **covers** *R* iff every coverage obligation of *R* is matched by at least one test case whose setup and stimulus realise the obligation's truth assignment.

---

## Appendix A. Verification Back-ends (informative)

A concrete verifier re-expresses a constraint in a chosen formalism. The choice is per-requirement and does not change the meaning of the requirement: §§1–8 *define* satisfaction; a back-end *checks* it.

| Constraint flavour                                      | Natural back-end     |
| ------------------------------------------------------- | -------------------- |
| Only ordering, boolean entities                         | LTL                  |
| Ordering + non-punctual time bounds, boolean entities   | MITL / MTL           |
| Time bounds + arithmetic on real-valued signals         | STL                  |
| Multi-step procedure where each step is a discrete mode | Timed Automata       |
| None of the above fit cleanly                           | Direct trace monitor |

Typical encodings (sketch):

- *always(psi)* → `G psi`; *eventually(psi)* → `F psi`; *initial(psi)* → *psi* evaluated at time 0.
- *triggered(c, e)* → `G(c -> F e)`; *triggered_within(c, e, d)* → `G(c -> F[0,d] e)`.
- Effect structure with *precedes* only → nested `F`-chain; *precedes* + *excludes* → nested `U` with negation guards; full DAG → Timed Automaton.
- MC/DC obligations, boundary tests, and quantifier robustness tests are handed to the test harness, not to the logic.

The vocabulary of §§1–8 is the *lingua franca* against which requirement and test case are matched; the back-end is one of several possible implementations behind that interface.
