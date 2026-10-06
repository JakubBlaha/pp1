# Mapping our formalism to the Event Calculus

Source: `tex-new/formalism.tex`, `tex-new/examples.tex`.

## 0. Short answer

**Yes, it maps.** Our formalism is essentially a *functional-fluent Event Calculus*
(EC) with a layer of first-order temporal macros on top:

| Ours | Event Calculus |
|---|---|
| Event entity + `Happening` | `Happens(e, t)` |
| Operation + effect predicate | `Initiates` / `Terminates` axioms |
| the `(t, t_next]` persistence + `t_next` definition | the commonsense law of inertia (`Clipped`) |
| Signal / Storage / Channel / State entity, `Val_ρ` | functional fluent, `HoldsAt(value(e)=v, t)` |
| `setup` of a test case | `Initially` / `HoldsAt(f, 0)` facts |
| `stimuli` of a test case | the *event list* (`Happens` facts) |
| temporal constructs (`Always`, `Causes`, …) | plain FO formulas quantified over the time sort |

Two things do **not** map one-to-one and need a decision:
1. **What the software does** – EC assumes that a value changes only through an event (frame rule) and that only the listed events happen (complete event list). For a test case the listed events are its stimuli, so nothing the software does ever happens. Our formalism assumes neither (§3.1).
2. **Aggregates and first-class sets/intervals** (`Size`, `EvtOccCount`, `MaxVal`, `Filter`, …) are outside pure EC; they are expressible in the tools only via their host language (ASP `#count`, Prolog `findall`) or by rewriting (§2.4).

Everything else maps mechanically. Details per construct follow.

---

## 1. EC recap (only what is used below)

Sorts: events `e`, fluents `f`, time points `t`.
- `Happens(e, t)` – event `e` occurs at `t`. The `Happens` facts we give EC are called the *event list* below (EC literature calls it the *narrative*). For a test case, the event list is its stimuli.
- `Initiates(e, f, t)`, `Terminates(e, f, t)` – effect axioms.
- `HoldsAt(f, t)`, `Initially(f)`.
- `ReleasedAt(f, t)` / `Releases(e, f, t)` – fluent is exempt from inertia (may change arbitrarily, constrained only by other axioms).
- Inertia: a fluent keeps its value until an event terminates it.
- Discrete EC (DEC, Mueller): `Happens(e,t) ∧ Initiates(e,f,t) → HoldsAt(f, t+1)`.
- Continuous EC (Shanahan): `HoldsAt(f,t2) ← Happens(e,t1) ∧ Initiates(e,f,t1) ∧ t1 < t2 ∧ ¬Clipped(t1,f,t2)`.
- Functional (multi-valued) fluents: `HoldsAt(value(e)=v, t)` with a uniqueness axiom; RTEC supports `F=V` fluents natively.

---

## 2. Construct-by-construct mapping

### 2.1 Primitives

| Ours | EC mapping | Notes |
|---|---|---|
| `T_D = ℕ ∪ {∞}` | DEC integer time | `∞` is only used to define `t_next`; it disappears because inertia replaces `t_next`. |
| `T_C = ℝ≥0 ∪ {∞}` | continuous EC | Tool support is the limiting factor: only constraint-based tools (s(CASP)) do dense time. |
| `Δ`, `𝓘` (intervals), `MkInterval*`, `Start`, `End`, `Duration`, `IsLeftOpen`, `InInterval`, `Diff`, `Now`, `Prev`, `Next`, `RelTime` | auxiliary terms/functions over the time sort: `interval(t,d,l,r)`, arithmetic on `t` | Not EC-specific; EC only needs `<` and `+` on time. `Now` becomes the universally quantified time variable of the enclosing formula. |
| `ID_E`, entity `e = (id, t_e, μ_e)` | a constant of a sort named after `t_e` | Entity type ↦ sort. |
| modifiers `μ_e` (`address`, `register`, `non_volatile`) and accessors `Addr`, `IsReg`, `IsNonVol` | static (time-independent) facts: `address(calibration_const, 0xAA000018)` | |
| `EventTypeLabel`, Event modifiers `target`/`type` | **disappear** – the event term itself carries them, see §2.2 | |

### 2.2 Entities and events

**Event entity** `ev` with `target = e`, `type = k`:
`Val_ρ(ev, t) = true` / `Happening(ev, t)` ↦ `∃args. Happens(op_k(e, args), t)`
where `op_k` is the operation producing label `k`:

| label `k` | EC event term |
|---|---|
| `written` | `write(e, v)` |
| `calculated` | `calculate(e, v)` |
| `read` | `read(e, dst)` |
| `entered` | `set_state(e, s)` |
| `transmitted` | `transmit(e, v)` |
| `received` | `receive(e, dst)` |
| `inserted` / `removed` / `cleared` | `insert(e, v)` / `remove(e, v)` / `clear(e)` |
| `generic` (on an EventTrigger) | the EventTrigger constant itself: `Happens(power_up, t)` |

Consequences:
- `EventTrigger` + `fire` + the `generic` Event entity collapse into **one** EC event constant. The two-entity pattern (`processor_power_up` + `ev_power_up`) is not needed.
- `EvtPred` is not needed: it exists only to link an operation to its Event entity; in EC the operation *is* the event.
- **The event-payload limitation (Req 07, Req 08, Future Extensions) disappears**: Req 07 is `Happens(transmit(modeset_topic, true), t)`; Req 08 is `Happens(receive(mastership_info, BACKUP), t)` (or `receive` with a payload argument).
- The note "at most one Event entity per `(target, type)`" disappears – there are no Event entities.

**Value-carrying entities** (Signal, Storage, Channel, State, Abstract):
`Val_ρ(e, t) = v` ↦ `HoldsAt(value(e)=v, t)`.
- Partiality of `σ` (undefined value) ↦ no `value(e)=_` fluent holds; just do not add an existence axiom, only uniqueness.
- `Abstract` entities (Req 02 `max_exec_time_data`) ↦ a fluent that is `ReleasedAt` all times (not driven by our operations).

**Set entities** ↦ a boolean fluent `member(e, x)` per element rather than a set-valued fluent:
`Contains(x, Val_ρ(e,t))` ↦ `HoldsAt(member(e,x), t)`. See §2.4 for `Size` etc.

### 2.3 Operations → effect axioms

The `(t, t_next]` clause in every effect predicate together with the definition of `t_next` is a hand-written frame axiom. In EC it is replaced by inertia, so each row becomes one or two effect axioms:

| Operation | EC axioms |
|---|---|
| `calculate(t,e,expr)`, `write(t,e,expr)`, `transmit(t,e,expr)` | `Initiates(write(e,v), value(e)=v, t)`; `Terminates(write(e,v), value(e)=w, t) ← w ≠ v`. If `expr` depends on state, evaluate it in the body: `Initiates(calculate(e,expr), value(e)=v, t) ← Eval(expr, t) = v` where `Eval` reads `HoldsAt`. |
| `read(t,src,dst)` | `Initiates(read(src,dst), value(dst)=v, t) ← HoldsAt(value(src)=v, t)` (+ terminate the old value). |
| `receive(t,src,dst)` | same as `read`. |
| `set_state(t,e,s)` | `Initiates(set_state(e,s), value(e)=s, t)` |
| `fire(t,e)` | no effect axiom, just `Happens(e, t)` |
| `insert(t,e,v)` | `Initiates(insert(e,v), member(e,v), t)` |
| `remove(t,e,v)` | `Terminates(remove(e,v), member(e,v), t)` |
| `clear(t,e)` | `Terminates(clear(e), member(e,x), t)` for all `x` |

The `Val_ρ(e, t) ∪ {v}` form of our `insert`/`remove` effects is not needed: inertia keeps all other members.

`O_T` (entity type → operations) becomes the sort signature of the event terms.

"The trigger condition that invokes an operation is specified at the requirement level" ↦ EC **trigger axioms**: `Happens(op, t) ← <condition on HoldsAt/Happens at t>`. A requirement may also be kept as a pure constraint (§2.5); EC supports both.

### 2.4 Expressions

| Ours | EC mapping | Pure EC? |
|---|---|---|
| constants, `+ − × /` | FO terms | yes; but clingo/DEC reasoner are integer-only → Req 01's `1.2 ×` needs s(CASP) (CLP(Q)) or scaling |
| `Val_ρ(e,t)` | `HoldsAt(value(e)=v, t)` | yes |
| `ValAfter_ρ(e,t)` | DEC: `HoldsAt(value(e)=v, t+1)`; continuous EC: `HoldsAt(value(e)=v, t')` for `t' > t` up to the next change | yes |
| `HasHappened_ρ(e,t)` | `∃t' ≤ t. Happens(e,t')`; idiomatic EC: fluent `happened(e)` initiated by `e` | yes |
| `LastOcc_ρ(ev,t,1)` | `Happens(ev,t1) ∧ t1 ≤ t ∧ ¬∃t2 (t1 < t2 ≤ t ∧ Happens(ev,t2))`; idiomatic: fluent `last_time(ev)=t1` initiated by `ev` | yes |
| `LastOcc_ρ(ev,t,n)`, `FirstOcc` | `n` distinct existentials + "nothing in between" | yes for fixed `n` (all examples use constant `n`) |
| `EvtOccCount_ρ(ev,i) op k` | for constant `k`: `≥ k` ↦ `k` ordered distinct existentials in `i`; `= k` ↦ `≥k ∧ ¬≥k+1` | yes for constant `k` (Req 09: `= 2`, Req 10: `≥ 1`); general count needs an aggregate (ASP `#count`, Prolog `findall/length`) |
| `MaxVal`, `MinVal` | `∃s∈i. HoldsAt(value(e)=m,s) ∧ ∀s'∈i. value ≤ m`; idiomatic: fluent `max(e)` updated by an effect axiom | yes (fluents are piecewise constant, so sup = max) |
| `Size`, `Filter` | rewrite: `Size(Filter(S,P)) ≤ k` ↦ "no `k+1` distinct `x ∈ S` with `P(x)`"; otherwise aggregate | only for constant bounds |
| `Union`, `Intersection`, `Difference` on Set entities | derived boolean fluents over `member`; on static sets: derived static predicates | yes |
| set-valued *constants* (e.g. `regs = {A,B,C,D}` in Req 13) | static unary predicate `in_regs(x)` | yes |
| `Interval*` predicates | arithmetic on interval terms | yes |

### 2.5 Predicates and temporal constructs

Point-in-time predicates (`Cmp`, `Not`, `AllOf`, `AnyOf`, `Implies`, `ForAll`/`Exists` over finite sets, `Contains`, `Subset`, …) are ordinary FO connectives over `HoldsAt`/`Happens` – no mapping issue.

EC has no modal temporal operators, but **every one of our temporal constructs is already defined by explicit FO quantification over `t`**, so each is a macro:

| Ours | EC formula |
|---|---|
| `Always(ψ)` | `∀t. ψ(t)` |
| `Eventually(ψ)` | `∃t. ψ(t)` |
| `Initial(ψ)` | `ψ(0)` (for fluents: `Initially`) |
| `Causes(ψc, ψe)` | `∀t. ψc(t) → ∃t' ≥ t. ψe(t')` |
| `CausesWithin(ψc, ψe, d)` | `∀t. ψc(t) → ∃t' (t ≤ t' ≤ t+d ∧ ψe(t'))` |
| `Sequence(ψ1..ψn)` | `∃t1 ≤ … ≤ tn. ∧ ψi(ti)` |
| `Precedes`, `Excludes`, `Immediately` | direct FO transcription |
| `∧ ∨ ¬ ⇒ ⇔` on trace predicates | FO connectives on closed formulas |

Caveat for tools: `Eventually`/`Causes` are liveness properties over infinite time. All EC tools reason over a **finite horizon** (DEC reasoner, ASP) or a sliding window (RTEC). For checking test cases this is fine – a test trace has finite stimuli and finitely many assertions – but the semantics becomes "finite-trace" (like LTLf): `Causes` unsatisfied at the horizon = violated.

### 2.6 Requirement and test case

| Ours | EC |
|---|---|
| `flavour` | choice of axiomatisation: DEC vs continuous EC |
| `entities` | sort/constant declarations |
| `constraint` | closed FO formula (§2.5) |
| test `setup` `σ0` | `Initially(value(e)=v)` / `HoldsAt(f, 0)` facts |
| test `stimuli` `(t, op, e, a…)` | event list: `Happens(op(e, a…), t)` |
| test `assertions` | `HoldsAt` queries at given time points |

This is the strongest argument for EC: a test case *is* an EC event list, and EC tools compute the resulting trace for us (deduction = running the event list through the effect axioms + inertia). Today `formalism.tex` does not say how the trace is obtained from stimuli at all; EC gives that for free.

What EC does **not** give us: the coverage check itself (which requirement conditions are exercised). That stays our own algorithm, but it can run on top of the EC model, e.g. in ASP by asking which antecedent atoms of the requirement become true under the event list.

---

## 3. The two real mismatches

### 3.1 Values and events produced by the software

**The difference.** EC is first-order logic plus one built-in rule, the *frame rule*:

> If nothing changes a value, it stays what it was.

Our formalism has no such global rule. Each operation (`write`, `set_state`, …) carries its own "the value stays like this until the next change" clause, and a value that no operation touches is simply unconstrained: it can be anything.

**Why it happens.** When a test case is translated into EC, the EC tools make two assumptions that our formalism does not:

- **Frame rule:** a value changes only when an event changes it.
- **Complete event list:** the only events that happen are the ones in the event list. For a test case, these are its stimuli.

**Where the complete-event-list assumption comes from.** The name is ours; the EC literature does not use it. The assumption itself is standard:

- In Shanahan's EC (*Solving the Frame Problem*, 1997; *The Event Calculus Explained*, 1999), a theory is read with `Happens` *circumscribed*. Circumscription means "make the predicate true for as few arguments as the axioms allow". For `Happens` this means: an event happens only if the event list says so. Mueller's discrete EC (*Commonsense Reasoning*, 2006) does the same.
- In the logic-programming and ASP versions of EC (Kowalski & Sergot 1986; Lee & Palla 2012), it follows from how these languages read facts: anything not stated or derivable is false. A `happens` fact that is not in the program does not hold.

The assumption is not obligatory, though. When EC is used for planning, the actions the planner may choose are deliberately left open: they may or may not happen, and the solver picks them (Shanahan, *An abductive event calculus planner*, 2000; in ASP with choice rules). The general fix below does the same for the software's events.

A value that the *software* changes, not the test, has no event in the event list. By the complete-event-list assumption nothing ever changes it, and by the frame rule it keeps its setup value forever. The same holds for the software's events themselves: a `write`, a `transmit` or entering a state that the software performs is not in the event list, so it never happens. In our formalism the same values and events are unconstrained: a test case allows many traces, one for each way the software could behave (see `findings.md`).

**Where it bites.** Every requirement is affected, because each one has at least one value or event that the software produces, not the test. The naive translation goes wrong in three different ways, depending on where the software's contribution appears in the formula. Each case below gives the requirement, our formalisation (from `examples.tex`) and what goes wrong.

Our formalism does not record who performs an event (`findings.md`, first finding), so below this is read off the requirement's wording. Everything the requirement says the software *shall* do is performed by the software. The failures (Req 10), the power-up (Req 06) and the exception (Req 05) come from the test.

#### Kind 1: the requirement can no longer be satisfied

The requirement demands a change, and the frame rule forbids it.

**Req 01 – arithmetic recurrence**

> The signal *EngagementNoSat_u* shall equal 1.2 × *EngagementNoSat_u*(k−1) when *Switch_b* is true, and *Lon_u* otherwise. The initial value is 0.

```
Entities: EngagementNoSat_u, Switch_b, Lon_u  (all Signal)
Initial( Val(EngagementNoSat_u, 0) = 0 )
∧ Always(
    (Val(Switch_b, Now) = true  ⇒ Val(EngagementNoSat_u, Now) = 1.2 · Val(EngagementNoSat_u, Prev(Now)))
  ∧ (Val(Switch_b, Now) ≠ true  ⇒ Val(EngagementNoSat_u, Now) = Val(Lon_u, Now)) )
```

What goes wrong: no operation ever changes `EngagementNoSat_u`, so the frame rule keeps it at its initial value 0. The second line demands that it equals `Lon_u` whenever `Switch_b` is false, so as soon as `Lon_u` is not 0 no trace satisfies the requirement. If `Switch_b` stays true, `1.2 × 0 = 0` holds and nothing goes wrong. The error therefore appears only on some test traces, which makes it easy to miss.

**Req 11 – Custom Counter**

> After the system enters emergency mode, at each discrete time step the counter *counter_1* is incremented by 3.

```
Entities: enter_emergency (EventTrigger), ev_enter_emergency (Event), counter_1 (Signal)
Always( HasHappened(ev_enter_emergency, Now) ⇒
        Val(counter_1, Now) = Val(counter_1, Prev(Now)) + 3 )
```

What goes wrong: no operation produces the increments. The *system* changes the counter, and the requirement only describes how. Translated naively into EC, the frame rule says "nothing changed it, so it stays at 0", while the requirement says "it becomes 3, then 6". The two contradict each other, so the requirement becomes unsatisfiable purely because of the translation.

> [!TIP]
> **Fix for this value only: release it.** A *released* value is exempt from the frame rule.
>
> **How the translation does it**, using Req 11:
>
> 1. **The requirement does not change.** It is translated as an ordinary constraint:
>
>    ```
>    ∀t. HoldsAt(happened(enter_emergency), t) →
>          (HoldsAt(value(counter_1)=v, t−1) → HoldsAt(value(counter_1)=v+3, t))
>    ```
>
> 2. **The translation adds one rule:** the counter is released at every time point, for every value.
>
>    ```
>    ReleasedAt(value(counter_1)=v, t)     for all v, t
>    ```
>
>    Together with the rule that a value-carrying entity has exactly one value at a time, this means: at every step the counter has some value, chosen freely and independently of the previous step. In ASP this boils down to a choice of exactly one value per step:
>
>    ```
>    1 { holdsAt(value(counter_1, V), T) : val(V) } 1 :- time(T).
>    ```
>
>    On its own, this makes every behaviour of the counter possible, which is again the freedom it has in our formalism.
> 3. **The requirement picks out the allowed behaviours**: only the models where the counter grows by 3 at every step after emergency mode was entered. Unlike the general fix, no events are needed: the values themselves are chosen.
>
> **Which values to release does *not* follow from the entity type.** `counter_1` and `Switch_b` (Req 01) are both Signals. But `Switch_b` is set by the test and must keep its value between two of the test's `calculate` stimuli, so it must not be released. The translation therefore has to know which values the software computes and which the test sets. Our formalism does not record this yet (see `findings.md`).
>
> **Drawback compared to the general fix.** A released counter has no `calculate` events. A requirement that refers to the counter's `calculated` event could therefore never be satisfied.

> [!TIP]
> **General fix: apply the complete-event-list assumption only to the test's own events.** EC normally assumes that the only events that happen are the ones in the event list, i.e. the test's stimuli. Instead, split the events into two groups:
>
> - **Stimulus events** are fired by the test, for example `fire(sensor_failure)`. Exactly the ones in the test happen.
> - **System events** are performed by the software, for example `calculate`, `write` or `set_state`. Any of them may happen at any time.
>
> In ASP this is a choice rule, for example `{ happens(calculate(counter_1, V), T) }`.
>
> **How this fixes Kind 1**, using Req 11:
>
> 1. **The requirement does not change.** It stays the constraint above: once emergency mode was entered, the counter equals its previous value + 3.
> 2. **The translation adds one rule:** the software may calculate `counter_1` at any time, to any value.
>
>    ```
>    { happens(calculate(counter_1, V), T) }.
>    ```
>
>    On its own, this rule makes every behaviour of the counter possible: it can stay at 0, jump to 42, or go 3, 6, 9, …. This is exactly the freedom the counter already has in our formalism, where nothing constrains it.
> 3. **The requirement picks out the allowed behaviours.** Only the models where the counter grows by 3 at every step after emergency mode was entered satisfy the constraint. For example, if emergency mode is entered at step 0 and the counter is 0, the events `calculate(counter_1, 3)` at step 0 and `calculate(counter_1, 6)` at step 1 give the values 3 and 6 at steps 1 and 2 (in discrete EC an effect at `t` is visible at `t+1`).
>
> **Req 01** works the same way with `calculate(EngagementNoSat_u, V)`. Whatever `Lon_u` is, there is a model where `EngagementNoSat_u` follows it.
>
> **Which events to open follows from the entity type.** `counter_1` and `EngagementNoSat_u` are Signals, and the operation that changes a Signal is `calculate`, so the translation can add the rule automatically.
>
> **Why the equation is not turned into a `calculate`.** A rule like "at every step, `calculate(counter_1, v+3)` happens" would describe how the software *works*, not what it *must satisfy*. The requirement would then produce the very behaviour it is checked against, so it could never fail.
>
> **Difference to releasing the value.** The frame rule stays in force: at a step where no `calculate` happens, the counter keeps its value.

#### Kind 2: the expected outcome of a test becomes impossible

The software changes a value or performs an event that the test expects. The event list contains only the test's events, so the software's events never happen, and the values they would change keep their setup values.

**Req 10 – repeated failure triggers emergency mode**

> The software shall enter the emergency mode if any of the following failures individually occurs twice in less than 10 seconds: (a) sensor failure, (b) energy failure, (c) communication failure.

```
Entities: sensor_failure, energy_failure, comm_failure (EventTrigger, each with an Event ev_*_fail),
          emergency_mode (State)
Causes( ( Happening(ev_sensor_fail, Now) ∧ EvtOccCount(ev_sensor_fail, MkIntervalOO(Now−10, Now)) ≥ 1 )
        ∨ ( … energy … ) ∨ ( … comm … ),
        Val(emergency_mode, Now) = true )
```

What goes wrong: in test case TC2 ("sensor failure twice in 9 s, expect emergency mode") the event list consists of the two `fire(sensor_failure)` stimuli. Entering emergency mode is done by the software, so `set_state(emergency_mode, true)` is not in the event list. Under the complete-event-list assumption it never happens, and by the frame rule `emergency_mode` keeps its setup value `false`. TC2's expected outcome, `emergency_mode = true`, is therefore impossible in the translation, although our formalism allows it. TC4 has the same problem. The same would happen to Req 12 ("enter the emergency mode state within 200 ns") once it is formalised; it is not yet in `examples.tex`.

**Req 04 – exception vector table**

> The software must configure the IVORx registers with the addresses of the Exception Vectors: IVOR0 = Critical input, IVOR1 = Machine check.

```
Entities: IVOR0, IVOR1 (Storage, register), CriticalInput, MachineCheck (Storage)
Eventually( Val(IVOR0, Now) = Addr(CriticalInput) ∧ Val(IVOR1, Now) = Addr(MachineCheck) )
```

What goes wrong: the configuring is done by the software, but no `write(IVOR0, …)` event is in the event list. The registers keep their initial values, so the condition can only be true if they happen to start with the right addresses. In every other case `Eventually` never succeeds.

**Req 02 – store to non-volatile memory, first part**

> The software shall store the maximum execution time measurement data in non-volatile memory at address MEASUREMT_BLOCK.

```
Entities: max_exec_time_data (Abstract), MEASUREMT_BLOCK (Storage, non_volatile), reset (EventTrigger)
Eventually( Val(MEASUREMT_BLOCK, Now) = Val(max_exec_time_data, Now) )   ∧   (reset part, see "Not a translation problem" below)
```

What goes wrong: same as Req 04. The software's store into `MEASUREMT_BLOCK` is not a `write` event in the event list, so `MEASUREMT_BLOCK` never changes and can only equal `max_exec_time_data` by coincidence.

**Req 03 – ordered read then store**

> The software must perform the following actions in the specified order: 1) Read the calibration constant value at the address 0xAA000018; 2) Store the calibration constant value in the DTSCON register.

```
Entities: calibration_const (Storage, address 0xAA000018), DTSCON (Storage, register),
          ev_read_cc (Event: read), ev_written_dtscon (Event: written)
Sequence( Happening(ev_read_cc, Now),
          Happening(ev_written_dtscon, Now)
          ∧ ValAfter(DTSCON, Now) = Val(calibration_const, Start(LastOcc(ev_read_cc, Now, 1))) )
```

What goes wrong: both the read and the write are done by the software, so neither is in the event list. They never happen, and `Sequence`, which needs a read followed by a write, is false in every model. A test expecting the software to perform the two steps has an impossible expected outcome.

**Req 05 – exception handling procedure**

> The software, when handling an exception, must execute the following steps in order: (1) copy register SRR0 to R5; (2) invoke the image exception handler; (3) if the handler returns, hold software execution.

```
Entities: SRR0, R5 (Storage, register), ev_written_r5 (Event: written),
          exception, invoke_ieh, return_ieh, hold_exec (EventTrigger, each with an Event ev_*)
Sequence( Happening(ev_exception, Now),
          Happening(ev_written_r5, Now) ∧ ValAfter(R5, Now) = Val(SRR0, Now),
          Happening(ev_invoke_ieh, Now) )
∧ Causes( Happening(ev_return_ieh, Now), Happening(ev_hold_exec, Now) )
```

What goes wrong: the test causes the exception, but copying SRR0 to R5 and invoking the handler are done by the software. They never happen, so the `Sequence` is false in every model, and a test expecting these steps has an impossible expected outcome. The `Causes` part has the opposite problem: the handler's return is a software event in the *condition*, so that part becomes automatically true (Kind 3).

**Req 06 – scheduling deadline**

> The software must start executing the sequence of tasks allocated to the execution schedule in less than 2 seconds after processor power-up.

```
Entities: processor_power_up, invoke_task_seq (EventTrigger, each with an Event ev_*)
CausesWithin( Happening(ev_power_up, Now), Happening(ev_invoke_task_seq, Now), 2 )
```

What goes wrong: the test powers up the processor, but starting the task sequence is done by the software. `ev_invoke_task_seq` never happens, so a test expecting the tasks to start within 2 s has an impossible expected outcome. This requirement has no values at all, which shows that the problem is not only about values.

**Req 08 – state transition on received mastership data, consequence**

> The software shall operate as Backup when it receives a new data instance of *MastershipInfo* with parameter *Mastership_b* equal to BACKUP.

```
Entities: MastershipInfo (Channel), ev_received_mastership (Event: received),
          Backup (State), ev_entered_backup (Event: entered)
Causes( Happening(ev_received_mastership, Now) ∧ Val(MastershipInfo, Now) = BACKUP,
        Happening(ev_entered_backup, Now) )
```

What goes wrong: the message comes from the test, but entering Backup is done by the software. `ev_entered_backup` never happens, so a test expecting the software to operate as Backup has an impossible expected outcome. (The condition has a separate problem in our formalism, see "Not a translation problem" below.)

**Req 09 – timed signal toggle**

> The software must toggle *valid_range*, within 500 ns of a write to *d*, if ALL the following conditions are satisfied: the difference between the last Maximum Peak and Minimum Peak of *d* is higher than 655; it is the second write to *d* after the Minimum Peak detection; the signed value of *d* is higher than the signed value of the last *d*.

```
Entities: d, valid_range (Signal), ev_written_d, ev_written_vr (Event: written),
          min_peak_det, max_peak_det (EventTrigger, each with an Event ev_*)
CausesWithin( Happening(ev_written_d, Now)
              ∧ Val(d, t_Mpd) − Val(d, t_mpd) > 655
              ∧ EvtOccCount(ev_written_d, MkIntervalOC(t_mpd, Now)) = 2
              ∧ ValAfter(d, Now) > ValAfter(d, t_prevd),
              Happening(ev_written_vr, Now) ∧ ValAfter(valid_range, Now) = ¬Val(valid_range, Now),
              500 )
```

What goes wrong: toggling `valid_range` is done by the software, so `ev_written_vr` never happens, and a test expecting the toggle has an impossible expected outcome. This assumes the test provides the writes to `d` and the peak detections. If the software performs them instead, they are in the *condition* and the requirement becomes automatically true (Kind 3).

> [!TIP]
> **General fix:** the same as for Kind 1. Stimulus events happen exactly as listed, and system events may happen at any time.
>
> **How this fixes Kind 2:**
>
> - **Req 10:** in TC2, `set_state(emergency_mode, true)` may now happen. So there is a model where it happens at 9 s, and TC2's expected outcome is possible again. The requirement excludes the models where it never happens.
> - **Req 04:** `write(IVOR0, …)` and `write(IVOR1, …)` may now happen, so there are models where the registers hold the right addresses.
> - **Req 02:** the same holds with `write(MEASUREMT_BLOCK, …)`.
> - **Req 03, 05, 06, 08, 09:** the software's reads, writes, handler invocation, task start, entering Backup and toggle may now happen, so the expected sequences and responses become possible.
>
> Here the frame rule is wanted: a register or a state keeps its value until the software changes it again. That is why opening the events is better than releasing these values.

#### Kind 3: the requirement becomes automatically true, so it tests nothing

A software event appears in the *condition* of the requirement. It never happens, so the condition is never true, and the requirement holds in every model, whatever the test does.

**Req 13 – bounded count of large register values**

> The number of values larger than 10 in the four registers A, B, C, D in different cores, when they are written in parallel at the same timestep, is never greater than 2.

```
Entities: A, B, C, D (Storage, register), ev_written_A … ev_written_D (Event: written)
Always( ForAll({ev_written_A, …, ev_written_D}, λev. Happening(ev, Now))
        ⇒ Size(Filter({A, B, C, D}, λe. ValAfter(e, Now) > 10)) ≤ 2 )
```

What goes wrong: the registers are written by the software. The write events never happen, so "all four are written at the same step" is never true, and the requirement holds in every model. A software that writes 11 into all four registers would pass.

**Req 07 – mode enable transmission after initialisation**

> After its initialisation, the software shall transmit the signal Mode Enable with value TRUE through DDS topic MODESET_TOPIC.

```
Entities: MODESET_TOPIC (Channel), ev_transmitted_modeset (Event: transmitted),
          initialization_end (EventTrigger), ev_init_end (Event)
Causes( Happening(ev_init_end, Now),
        Happening(ev_transmitted_modeset, Now) ∧ ValAfter(MODESET_TOPIC, Now) = true )
```

What goes wrong: the end of initialisation is the software's event, so the condition is never true and the requirement holds in every model. (The transmission in the consequence is also a software event and would never happen either.)

**Req 05, `Causes` part:** the same, with the handler's return as the condition (see Req 05 under Kind 2).

> [!TIP]
> **General fix:** the same as for Kind 1 and Kind 2. The software's events may now happen, so the condition can become true, and the requirement then constrains what follows: the written values in Req 13, the transmission in Req 07, holding execution in Req 05.
>
> For coverage this kind has a further consequence: no stimulus can make such a condition true, because the test does not control it. A test can only observe it through its assertions.

#### Not a translation problem: Req 02 (reset part) and Req 08

These two cases first looked like Kind 3, but their cause is a gap in our formalism, not the translation. Our formalism either has the same problem (Req 02) or is the one that is wrong (Req 08). Both are described in `findings.md`:

- **Req 02, reset part:** our formalism does not say what a reset does to storage, so "the value survives a reset" holds for volatile memory too. This turned out not to matter for coverage: a covering test fires a reset and asserts the value afterwards, and the checker reads both off the test.
- **Req 08, condition:** our `receive` does not fix what is received, so it is undecidable whether a test exercises the requirement. EC handles this case correctly. (Its consequence is a translation problem of Kind 2, see above.)

#### No requirement is unaffected

| Kind | Requirements |
|---|---|
| 1: the requirement can no longer be satisfied | Req 01, Req 11 |
| 2: the expected outcome of a test becomes impossible | Req 02 (first part), 03, 04, 05 (`Sequence`), 06, 08 (consequence), 09, 10, and Req 12 once formalised |
| 3: the requirement becomes automatically true | Req 05 (`Causes`), 07, 13 |

The general fix covers all of them. Req 01 and Req 11 can alternatively be fixed by releasing the value.

**What the test provides itself is not affected.** Inputs such as `Switch_b` and `Lon_u` (Req 01) and `SRR0` (Req 05) stay at their `setup` values unless the test changes them. The events the test fires, such as the failures (Req 10), the power-up (Req 06) and the exception (Req 05), are in the event list. That is fine, because providing them is exactly what a test case does.

**Rule of thumb.** The examples show that "released or not" depends on what kind of value it is, not only on whether an operation touches it:

| Kind of value | EC treatment | Examples |
|---|---|---|
| recomputed at every step by the system | released | `counter_1`, `EngagementNoSat_u`, `max_exec_time_data` (an `Abstract` value) |
| stored, and keeps its value physically (registers, memory, states) | inertial, with the software's `write` / `set_state` as system events that may happen at any time | `IVOR0`/`IVOR1`, `MEASUREMT_BLOCK`, `DTSCON`, `R5`, `A`–`D`, `emergency_mode` |
| value arriving from outside | inertial, with the value carried in the event that delivers it | `MastershipInfo` |
| input set by the test | inertial; the test changes it with operations or `setup` | `Switch_b`, `Lon_u`, `SRR0` |

For events the rule is simpler: the events the test fires are stimulus events, and everything the software does is a system event.

### 3.2 Counting and sets

**The difference.** Plain first-order logic has no sets as values and no counting, so `Size`, `Filter`, `EvtOccCount`, `MaxVal` and `MinVal` have no direct EC counterpart.

**Where it bites.** Req 13 says "at most 2 of the registers A–D are greater than 10".

**The fix for a fixed bound.** Say "there are no 3 different registers that are all greater than 10". Every current example has a fixed bound, so this works for all of them (see §2.4).

**For a general count** ("the number of … equals some computed value") you depend on the tool:
- ASP (clingo): `#count`, `#max` – integers only.
- Prolog-based (RTEC, s(CASP)): `findall`, lists, CLP(Q) reals in s(CASP).

---

## 4. Worked examples

**Req 03** (ordered read then write):
```
∃t1 ≤ t2, v.
  Happens(read(calibration_const, _), t1)
  ∧ HoldsAt(value(calibration_const)=v, t1)
  ∧ Happens(write(dtscon, v), t2)
```
`LastOcc` is not needed – the read value is bound directly. (Note: our version takes the *last* read before the write; this one takes *some* read. To match exactly add `¬∃t'(t1 < t' ≤ t2 ∧ Happens(read(calibration_const,_), t'))`.)

**Req 06**:
```
∀t. Happens(power_up, t) → ∃t'. t ≤ t' ≤ t+2 ∧ Happens(invoke_task_seq, t')
```
(`t' < t+2` for the strict bound – trivially expressible, which also fixes the over-approximation noted in examples.tex.)

**Req 07** (payload now in the event):
```
∀t. Happens(init_end, t) → ∃t' ≥ t. Happens(transmit(modeset_topic, true), t')
```

**Req 10** (count rewritten):
```
∀t, f ∈ {sensor_fail, energy_fail, comm_fail}.
  Happens(f, t) ∧ ∃t0 (t−10 < t0 < t ∧ Happens(f, t0))
  → ∃t' ≥ t. HoldsAt(value(emergency_mode)=true, t')
```
The `Now − 10 < 0` edge case vanishes: `t0` ranges over `T`, no interval term is built.

**Req 13** (the four registers are written at the same step):
```
∀t. (∀x. in_regs(x) → ∃v. Happens(write(x, v), t))
    → ¬∃x1,x2,x3 distinct. ∧_i (in_regs(xi) ∧ Happens(write(xi, vi), t) ∧ vi > 10)
```
The written values come straight from the event terms `write(x, v)`. Reading them from the fluents instead would need `HoldsAt(value(xi)=vi, t+1)` in DEC (our `ValAfter`), because a write at `t` takes effect only after `t`.

**A test case for Req 06**:
```
Happens(power_up, 0).  Happens(invoke_task_seq, 1.5).
```
Checking = evaluating the Req 06 formula on the model of this event list.

---

## 5. Tools

| Tool | Time | Fits | Limits |
|---|---|---|---|
| **DEC reasoner** (Mueller) | discrete | full DEC, arbitrary FO constraints, SAT-based | finite horizon & domains, integers only |
| **ASP encodings** (clingo, e.g. F2LP / Lee & Palla) | discrete | DEC + `#count`/`#max` aggregates; good for coverage queries | integers only, grounding blows up with long horizons |
| **RTEC** (Artikis et al.) | discrete | multi-valued `F=V` fluents natively, interval computation (`holdsFor`), stream/windowed | built for recognition over streams, not arbitrary FO constraints – our temporal macros must be written as Prolog rules |
| **s(CASP)** (Arias, Carro, Gupta et al.) | **continuous** (CLP(Q)) | the only listed option for `T_C`, reals (Req 01 `1.2×`, Req 09 ns) | goal-directed, performance less predictable |

Pragmatic pick: **ASP/clingo with a DEC encoding** for discrete requirements (aggregates + natural "which conditions fired" queries for coverage), **s(CASP)** if continuous flavour must be supported natively.

---

## 6. Issues in `formalism.tex` found along the way

- `State` is used inconsistently: the operation `set_state(e, s)` treats a State entity as a variable holding a state value, but Req 08 (`Backup`) and Req 10 (`emergency_mode`, `Val = true`) treat each state as its own boolean entity.
- `SinceZero(t) = (0, t)` returns a pair, not the 4-tuple of Definition `Interval`.
- `MaxVal`, `MinVal`, `IntervalIncludes`, `IntervalExcludes`, `StartOfFirstIntervalIn` ignore the openness flags.
- Req 10 lists `emergency_mode` as a State but uses no `entered` event; the Custom Counter example declares no flavour.
