# Related formalisms

This note compares our formal base (`tex-new/formalism.tex`) with existing formalisms.
For each one it lists what it **shares** with ours, shows the **same requirement written both ways**, and briefly notes where the two **differ**.
Requirements in the examples are taken from `req/` and `tex-new/examples.tex`.

Our syntax is abbreviated in the examples: `Val(e, t)` stands for $\mathit{Val}_\rho(e, t)$, and so on.

## Overview

| Our layer | Closest existing formalism(s) | What is shared |
|---|---|---|
| Traces $\rho : T \to (E \rightharpoonup V)$ | LTL / MTL / STL semantics | A behaviour is a function from time to states; discrete or continuous time |
| Point predicates with `Now`, `LastOcc`, `FirstOcc` | RTL, TPTL, STL\* | Formulas refer to concrete time points and do arithmetic on them |
| `HasHappened`, `Prev` | Past-time LTL, Lustre | Looking backwards in the trace |
| `EvtOccCount`, `MaxVal`, `MinVal` | Counting MTL, Signal First-Order Logic, stream runtime verification (Lola, TeSSLa) | Aggregates over a time window |
| Intervals and interval predicates | Allen's interval algebra, Duration Calculus | Relations between time spans |
| Temporal constructs (`Always`, `Causes`, …) | Dwyer specification patterns, Konrad–Cheng real-time patterns | A fixed catalogue of named templates instead of free nesting of operators |
| Operations and effect predicates | Event Calculus, Fluent LTL, Event-B / Z / TLA+ | Events change values, and values persist until the next change |
| Requirements written in near-natural vocabulary | FRET (FRETish), EARS | Structured natural language that maps to a formal semantics |
| Test cases and coverage checking | Unique First Cause (UFC) coverage | Measuring how well tests cover a temporal requirement |

---

## 1. LTL, MTL, STL — the trace model and the temporal constructs

**Shared.**
All three logics are interpreted over the same kind of object as ours: a sequence (LTL, discrete MTL) or a function over $\mathbb{R}_{\geq 0}$ (continuous MTL, STL) that assigns a state to each time point.
Our *discrete* and *continuous* flavours correspond directly to discrete-time and continuous-time MTL.
Every one of our temporal constructs can be written as a short LTL or MTL formula:

| Ours | LTL / MTL |
|---|---|
| `Always(ψ)` | $\mathbf{G}\,\psi$ |
| `Eventually(ψ)` | $\mathbf{F}\,\psi$ |
| `Initial(ψ)` | $\psi$ (a formula without a temporal operator is evaluated at time 0) |
| `Causes(c, e)` | $\mathbf{G}(c \rightarrow \mathbf{F}\,e)$ |
| `CausesWithin(c, e, d)` | $\mathbf{G}(c \rightarrow \mathbf{F}_{[0,d]}\,e)$ |
| `Immediately(a, b)` | $\mathbf{G}(a \rightarrow \mathbf{X}\,b)$ |
| `Excludes(a, b)` | $\mathbf{G}\,\lnot(a \land b)$ |
| `Precedes(a, b)` | $\mathbf{G}(b \rightarrow \mathbf{O}\,a)$ (uses the past operator *Once*, see §3) |
| `Sequence(ψ1, ψ2, ψ3)` | $\mathbf{F}(\psi_1 \land \mathbf{F}(\psi_2 \land \mathbf{F}\,\psi_3))$ |

**Example — Req 06** ("start the task sequence in less than 2 s after power-up").

Ours:
```
CausesWithin( Happening(ev_power_up, Now),
              Happening(ev_invoke_task_seq, Now),
              2 )
```
MTL:
$$\mathbf{G}\bigl(\mathit{power\_up} \rightarrow \mathbf{F}_{[0,2]}\,\mathit{invoke\_task\_seq}\bigr)$$

MTL also allows an open bound, $\mathbf{F}_{[0,2)}$, which expresses "less than 2 s" exactly. Our `CausesWithin` is fixed to a closed interval, which is the over-approximation noted in `examples.tex`.

**Example — Req 09, value part.** STL atoms are comparisons over real-valued signals, just like our `Cmp`:
$$\mathbf{G}\bigl(\mathit{write\_d} \land (d > 655) \rightarrow \mathbf{F}_{[0,500]}\,\mathit{toggle}\bigr)$$
Plain STL cannot say "the value of $d$ *at the last maximum peak*", because it has no way to refer back to an earlier time point. **STL\*** (Brim et al., 2014) adds a *freeze* operator that stores the signal value at one moment and compares it later. That is what our `Val(d, t_Mpd)` does.

**Differences.**
- In LTL/MTL/STL the operators nest freely, for example $\mathbf{G}\mathbf{F}\,p$ ("infinitely often"). We cannot nest a temporal construct inside another. `Always(Eventually(ψ))` does not type-check because `Eventually` returns a trace predicate, not a point predicate.
- Most of our expressive power lives in point predicates that name explicit time points (see §2). In LTL the temporal operators carry that power.

---

## 2. RTL and TPTL — logics with explicit time

These are the closest match for our **predicate layer**.

### Real-Time Logic (RTL) — Jahanian & Mok, 1986

**Shared.**
RTL has an *occurrence function* $@(e, i)$, the time of the $i$-th occurrence of event $e$.
Our `LastOcc(ev, t, n)` and `FirstOcc(ev, t, n)` are the same idea.
RTL formulas are first-order formulas over these time terms using $+$, $-$, $<$, $\leq$, which is how we use `Start(LastOcc(…))` together with `Cmp`.

**Example — Req 06.**

RTL:
$$\forall i\; \exists j:\; @(\mathit{power\_up}, i) \leq @(\mathit{invoke}, j) \;\land\; @(\mathit{invoke}, j) - @(\mathit{power\_up}, i) < 2$$

Ours, written explicitly with occurrence times instead of `CausesWithin`:
```
Always( Happening(ev_power_up, Now) ⇒
        Diff( Start(FirstOcc(ev_invoke_task_seq, Now, 1)), Now ) < 2 )
```

**Example — Req 09, condition "second write to d after the minimum peak".**

RTL counts occurrences from the start of the run, so for the current ($j$-th) write it compares occurrence indices. Writes $j-1$ and $j$ come after the $k$-th minimum peak, write $j-2$ does not, and no later minimum peak occurs before write $j$:
$$\exists k:\; @(\mathit{write\_d}, j-2) \leq @(\mathit{min\_peak}, k) < @(\mathit{write\_d}, j-1) \;\land\; @(\mathit{min\_peak}, k+1) > @(\mathit{write\_d}, j)$$
Ours counts relative to `Now` instead:
```
EvtOccCount(ev_written_d, MkIntervalOC(t_mpd, Now)) = 2
```

**Difference.** RTL indexes occurrences absolutely ("the 5th power-up"). We index relative to the evaluation point ("the last 2 writes before now"), which is closer to how requirements are phrased.

### Timed Propositional Temporal Logic (TPTL) — Alur & Henzinger, 1989

**Shared.**
TPTL has a *freeze quantifier* $x.\varphi$. It binds the current time to the variable $x$, so that a later part of the formula can compare against it.
Our `Now`, together with the habit of naming time points (`t_mpd`, `t_prevd`), plays the same role.

**Example — Req 06.**
$$\mathbf{G}\; x.\bigl(\mathit{power\_up} \rightarrow \mathbf{F}\; y.(\mathit{invoke} \land y - x < 2)\bigr)$$
Here $x$ corresponds to the `Now` of the antecedent, and $y$ to the `Now` of the consequent inside `CausesWithin`.

**Consequence of the match.**
Over continuous time, TPTL is undecidable. Our logic has at least the same power (time arithmetic plus quantification over time), so symbolic reasoning, such as proving that a test set covers a requirement, is undecidable in general for the continuous flavour.
Checking one *concrete, finite* test trace is unaffected, because that is evaluation, not satisfiability.

---

## 3. Past-time LTL and Lustre — looking backwards

**Shared.**
Past-time LTL adds the operators Yesterday ($\mathbf{Y}$), Once ($\mathbf{O}$) and Since ($\mathbf{S}$).
Lustre (and SCADE, which is based on it) defines signals by equations using `pre` (the value at the previous step) and `->` (the initial value).

| Ours | Past LTL | Lustre |
|---|---|---|
| `HasHappened(e, Now)` | $\mathbf{O}\,e$ | `e or (false -> pre(...))` (a latch) |
| `Val(x, Prev(Now))` | $\mathbf{Y}$ applied to a value | `pre(x)` |
| `Initial(Val(x, 0) = c)` | — | `c -> …` |

**Example — Req 01** ("EngagementNoSat_u = 1.2 · its previous value if Switch_b, otherwise Lon_u; initial value 0").

Lustre:
```lustre
EngagementNoSat_u = 0 -> if Switch_b then 1.2 * pre(EngagementNoSat_u)
                                     else Lon_u;
```
Ours:
```
Initial( Val(EngagementNoSat_u, 0) = 0 )
∧ Always( (Val(Switch_b, Now) = true  ⇒ Val(EngagementNoSat_u, Now) = 1.2 · Val(EngagementNoSat_u, Prev(Now)))
        ∧ (Val(Switch_b, Now) ≠ true  ⇒ Val(EngagementNoSat_u, Now) = Val(Lon_u, Now)) )
```

**Example — custom counter** ("after entering emergency mode, counter_1 grows by 3 each step").

Past LTL with data:
$$\mathbf{G}\bigl(\mathbf{O}\,\mathit{enter\_emergency} \rightarrow \mathit{counter\_1} = \mathbf{Y}\,\mathit{counter\_1} + 3\bigr)$$

**What this comparison shows.**
Lustre's `->` makes the case $t = 0$ explicit. In our Req 01, `Always` also applies at `Now = 0`, where `Prev(Now)` is undefined. We have no stated rule for what happens to a predicate that uses an undefined value. Lustre's design suggests either guarding with `Now > 0` or giving that rule.

---

## 4. Counting and aggregates — counting MTL, Signal First-Order Logic, stream runtime verification

**Shared.**
Several formalisms add aggregates over a time window, as our `EvtOccCount`, `MaxVal` and `MinVal` do:

- **MTL with counting modalities** (Hirshfeld & Rabinovich) can say "$p$ holds at least $n$ times within the next / last $d$ time units".
- **Signal First-Order Logic** (Bakhirkin, Ferrère, Henzinger & Ničković, 2018) quantifies over time points within bounded windows. This allows "max of $x$ in the last 10 s".
- **Stream runtime verification** languages (Lola, TeSSLa) define derived streams such as counters, last values and running maxima, and evaluate them on a trace. That is exactly the job of our coverage checker.

**Example — Req 10** ("enter emergency mode if a sensor failure occurs twice in less than 10 s").

Ours:
```
Causes( Happening(ev_sensor_fail, Now)
          ∧ EvtOccCount(ev_sensor_fail, MkIntervalOO(Now - 10, Now)) ≥ 1,
        Val(emergency_mode, Now) = true )
```
Counting MTL (past form; notation illustrative):
$$\mathbf{G}\bigl(\mathit{sensor\_fail} \land \overleftarrow{C}_{\geq 1}^{(0,10)}\,\mathit{sensor\_fail} \rightarrow \mathbf{F}\,\mathit{emergency}\bigr)$$

**Example — the custom counter in Lola.**
In Lola, `x[-1, d]` is the previous value of stream `x`, or `d` if there is none:
```
input  bool enter_emergency
output bool active    := enter_emergency || active[-1, false]
output real expected  := if active then counter_1[-1, 0] + 3 else counter_1
output bool ok        := counter_1 == expected
```

**Example — Req 09 in TeSSLa style** (illustrative):
```
def prev_d     := last(d, write_d)          -- value of d at the previous write
def cond3      := d > prev_d                -- "signed value of d higher than last d"
```
This corresponds to our `ValAfter(d, t_prevd)` (the value written at the previous write) with `t_prevd = Start(LastOcc(ev_written_d, Now, 2))`.

**Implication for us.** Lola and TeSSLa have working evaluators. Our formulas could be translated into one of them, and the result would be a trace checker without writing one from scratch.

---

## 5. Allen's interval algebra and Duration Calculus — intervals

**Shared.**
Allen (1983) defines 13 basic relations between two intervals (*before, meets, overlaps, starts, during, finishes, equals* and their inverses).
Our interval predicates are unions of these relations:

| Ours | Allen relation(s) of $i_2$ relative to $i_1$ |
|---|---|
| `IntervalIncludes(i1, i2)` | $i_2$ *starts*, *during*, *finishes* or *equals* $i_1$ |
| `IntervalExcludes(i1, i2)` | $i_2$ *before* or *after* $i_1$ (*meets* is excluded because we use strict $<$) |
| `StartOfFirstIntervalIn(i1, i2)` | union of *equals, starts, started-by, during, finishes, overlapped-by, met-by* |

**Example.** "The read of A happens during the configuration phase":
- Ours: `IntervalIncludes(config_phase, LastOcc(ev_read_A, Now, 1))`
- Allen: $\mathit{read\_A}\ \{\mathit{during}, \mathit{starts}, \mathit{finishes}, \mathit{equals}\}\ \mathit{config\_phase}$

**Duration Calculus** (Zhou, Hoare & Ravn, 1991) also reasons about intervals, but through the length $\ell$ and accumulated durations $\int P$.
The shared idea is that a time span is a first-class object.
"The heater may be on for at most 4 s in any 30 s window" is written $\ell \leq 30 \rightarrow \int \mathit{heater} \leq 4$. We cannot express this yet, because we have no duration-accumulation function. Adding one would be the natural extension in this direction.

**Difference.** Our intervals carry explicit openness flags. Allen's algebra has no endpoint openness, and Duration Calculus ignores measure-zero endpoints. Tracking openness is needed for us because "less than 10 s" and "after the minimum peak" depend on it (Req 09, Req 10).

---

## 6. Dwyer and Konrad–Cheng patterns — the catalogue of temporal constructs

**Shared.**
Dwyer, Avrunin & Corbett (1999) found that most real specifications use a small set of templates.
They catalogued these templates and gave each one a fixed translation to LTL, CTL and other logics.
Konrad & Cheng (2005) added real-time versions with MTL translations.
Our temporal constructs are such a catalogue, with exactly the same aim: the writer (for us, an LLM) picks a template instead of building nested operators.

| Ours | Dwyer / Konrad–Cheng pattern |
|---|---|
| `Always(ψ)` | Universality |
| `Eventually(ψ)` | Existence |
| `Always(¬ψ)` | Absence |
| `Causes(c, e)` | Response |
| `CausesWithin(c, e, d)` | Bounded Response (real-time) |
| `Precedes(a, b)` | Precedence |
| `Sequence(…)` | Chain Precedence / Chain Response (existential variant only) |

**Example — Req 05** ("when handling an exception: copy SRR0 to R5, then invoke the handler").
`examples.tex` notes that `Sequence` is existential and that "every exception triggers the sequence" needs a construct we lack.
Dwyer's **Chain Response** pattern is that construct:
$$\mathbf{G}\bigl(\mathit{exception} \rightarrow \mathbf{F}(\mathit{write\_R5} \land \mathbf{F}\,\mathit{invoke\_ieh})\bigr)$$

**Patterns also have scopes**, which we do not have yet: *Globally, Before R, After Q, Between Q and R, After Q until R*.
Req 07 ("**after its initialisation**, transmit Mode Enable = TRUE") is the Existence pattern with scope *After Q*:
$$\mathbf{G}(\mathit{init\_end} \rightarrow \mathbf{F}\,\mathit{transmit\_modeset})$$
We currently encode it with `Causes`. A scope argument on each construct would be the systematic replacement for antecedents like `HasHappened(…)`, which several examples use.

---

## 7. Event Calculus and Fluent LTL — operations and their effects

These are the closest match for our **operations layer**.
A detailed construct-by-construct mapping to the Event Calculus is in `calculi.md`. This section only summarises it.

### Event Calculus — Kowalski & Sergot, 1986

**Shared.**
The Event Calculus describes how events change *fluents* (properties whose value varies over time):

| Event Calculus | Ours |
|---|---|
| `Happens(e, t)` | `Happening(ev, t)` |
| `Initiates(e, f, t)` — event $e$ at $t$ makes fluent $f$ true | an operation's effect predicate |
| `HoldsAt(f, t)` | `Val(e, t) = v` |
| `Clipped(t1, f, t2)` — $f$ was changed between $t_1$ and $t_2$ | "until $t_{next}$" |
| Law of inertia: a fluent keeps its value until something changes it | $\forall t' \in (t, t_{next}] : \mathit{Val}(e, t') = \ldots$ |

**Example — Req 03** (read the calibration constant, store it to DTSCON).

Event Calculus:
```
Initiates(write(DTSCON, v), value(DTSCON, v), t).
HoldsAt(f, t2) ← Happens(e, t1) ∧ Initiates(e, f, t1) ∧ t1 < t2 ∧ ¬Clipped(t1, f, t2).
```
Ours (operations table):
```
write(t, DTSCON, expr):
    EvtPred(DTSCON, written, t)
    ∀ t' ∈ (t, t_next] : Val(DTSCON, t') = expr(ρ, t)
```

Both use the same timing convention: an effect holds strictly after the event ($t_1 < t_2$ in the EC, $(t, t_{next}]$ for us), so at the firing time the old value is still visible.

**Difference that matters.**
The Event Calculus defines `Clipped` from events in the model and minimises change by circumscription. We define $t_{next}$ from "the next operation that fires", which is a fact about the test's stimuli, not about the trace. Using the EC approach would give operations a semantics in terms of the trace alone.

### Fluent LTL — Giannakopoulou & Magee, 2003

**Shared.**
A fluent is declared as a pair of event sets: those that make it true and those that make it false.
Our `State` entities and `set_state` work the same way.

**Example — Req 08** (enter Backup on receiving MastershipInfo = BACKUP):
```
fluent InBackup = <{enter_backup}, {enter_primary}> initially false
assert R08 = [] (recv_mastership_backup -> <> InBackup)
```
Ours:
```
Causes( Happening(ev_received_mastership, Now) ∧ Val(MastershipInfo, Now) = BACKUP,
        Happening(ev_entered_backup, Now) )
```

---

## 8. Event-B, Z and TLA+ — operations on state

**Shared.**
In these state-based methods an operation is a *before–after predicate* that relates the old state (unprimed variables) to the new state (primed variables).
Our `Val(e, t)` at a firing time plays the role of the unprimed variable and `ValAfter(e, t)` the primed one.
Our `Set` entity and its operations are the set-valued variables of Z and Event-B.

**Example — `insert(t, e, v)`.**

Event-B:
```
insert ≙ ANY v WHERE v ∈ ELEM THEN s := s ∪ {v} END
-- before–after predicate:  s' = s ∪ {v}
```
TLA+:
```
Insert(v) == s' = s \cup {v} /\ UNCHANGED <<other_vars>>
```
Ours:
```
Val(e, t') = Val(e, t) ∪ {v}     for t' ∈ (t, t_next]
```

**Difference.** TLA+ and Event-B state the frame condition explicitly (`UNCHANGED`, or "variables not assigned keep their value"). For us the frame is implicit: an entity no operation fires on is simply unconstrained. Whether "unconstrained" should mean "unchanged" is a design decision these methods force you to make explicitly.

---

## 9. FRET and EARS — structured natural language for requirements

These share our **overall purpose** rather than a single layer.

### FRET / FRETish — NASA (Giannakopoulou et al., 2020)

**Shared.**
FRET is a tool in which engineers write requirements in a restricted English (FRETish).
Each sentence has fixed fields: *scope, condition, component, shall, timing, response*.
FRET translates each sentence into past-time and future-time MTL and can export it to model checkers and runtime monitors.
Our design has the same goals: vocabulary close to natural language, a precise semantics behind every word, and a fixed set of timing templates.

| FRETish timing | Ours |
|---|---|
| `always` | `Always` |
| `eventually` | `Causes` / `Eventually` |
| `within N` | `CausesWithin(…, N)` |
| `at the next timepoint` | `Immediately` |
| `immediately` (same time point) | no direct counterpart |
| `for N`, `after N`, `until`, `before` | no direct counterpart yet |

**Example — Req 06 in FRETish:**
```
Upon processor_power_up the software shall within 2 seconds satisfy task_seq_started.
```
**Example — Req 10 (sensor part) in FRETish:**
```
Upon sensor_failure & sensor_failure_count_10s >= 2 the software shall eventually satisfy emergency_mode.
```
FRET has no counting built in, so the count has to be supplied as a derived signal. Our `EvtOccCount` covers this directly.

**Note on naming.** FRET's `immediately` means "at the same time point" and `at the next timepoint` means $\mathbf{X}$. Our `Immediately` means $\mathbf{X}$, which may surprise readers who know FRET.

### EARS — Mavin et al., 2009

**Shared.**
EARS gives five sentence templates for requirements. Each lines up with one of our constructs:

| EARS template | Ours |
|---|---|
| Ubiquitous: "The *system* shall *response*." | `Always(response)` |
| Event-driven: "**When** *trigger*, the *system* shall *response*." | `Causes(trigger, response)` |
| State-driven: "**While** *state*, the *system* shall *response*." | `Always(Val(state, Now) ⇒ response)` |
| Unwanted behaviour: "**If** *condition*, **then** the *system* shall *response*." | `Causes(condition, response)` |
| Optional feature: "**Where** *feature*, the *system* shall *response*." | entity modifiers / requirement-level configuration |

**Example — Req 08 in EARS:**
"When a MastershipInfo instance with Mastership_b = BACKUP is received, the software shall operate as Backup."

EARS has no formal semantics of its own. It shows that our construct names line up with sentence shapes engineers already use.

---

## 10. Unique First Cause coverage — test coverage of temporal requirements

**Shared.**
Whalen, Rajan, Heimdahl & Miller (ISSTA 2006) define requirements coverage directly over LTL formulas.
*Unique First Cause* (UFC) coverage lifts MC/DC to temporal operators: for every atomic condition, some test must show that this condition alone, at its first relevant occurrence, decides whether the requirement holds.
This is our project goal 3: decide which conditions of a requirement the tests exercise.

**Example — Req 10** (`req/10.md`), sensor-failure part:

| UFC obligation | Test case from `req/10.md` |
|---|---|
| Trigger true, the response must follow | TC2: two sensor failures 9 s apart, expect emergency mode |
| Window condition false (gap ≥ 10 s), no response | TC3: two sensor failures 11 s apart, expect no emergency mode |
| No trigger at all | TC1: no failure |
| "Individually": failures of different types must not combine | TC7: energy failure then comm failure within 9 s |

Corresponding UFC obligations would also be generated for energy and comm failures (TC4–TC6). The obligation "comm failure twice within 10 s" has no test in `req/10.md`. This is exactly the kind of gap the checker should report.

---

## References

- R. Koymans. *Specifying real-time properties with Metric Temporal Logic.* Real-Time Systems, 1990.
- O. Maler, D. Ničković. *Monitoring temporal properties of continuous signals* (STL). FORMATS 2004.
- L. Brim, P. Dluhoš, D. Šafránek, T. Vejpustek. *STL\*: Extending Signal Temporal Logic with signal-value freezing operator.* Information and Computation, 2014.
- F. Jahanian, A. K. Mok. *Safety analysis of timing properties in real-time systems* (RTL). IEEE TSE, 1986.
- R. Alur, T. A. Henzinger. *A really temporal logic* (TPTL). FOCS 1989 / JACM 1994.
- N. Halbwachs, P. Caspi, P. Raymond, D. Pilaud. *The synchronous data flow programming language LUSTRE.* Proc. IEEE, 1991.
- Y. Hirshfeld, A. Rabinovich. *Logics for real time: decidability and complexity* (counting modalities). Fundamenta Informaticae, 2004.
- A. Bakhirkin, T. Ferrère, T. A. Henzinger, D. Ničković. *The first-order logic of signals.* EMSOFT 2018.
- B. D'Angelo et al. *LOLA: Runtime monitoring of synchronous systems.* TIME 2005.
- M. Leucker et al. *TeSSLa: Temporal Stream-based Specification Language.* SBMF 2018.
- J. F. Allen. *Maintaining knowledge about temporal intervals.* CACM, 1983.
- Zhou Chaochen, C. A. R. Hoare, A. P. Ravn. *A calculus of durations.* IPL, 1991.
- M. B. Dwyer, G. S. Avrunin, J. C. Corbett. *Patterns in property specifications for finite-state verification.* ICSE 1999.
- S. Konrad, B. H. C. Cheng. *Real-time specification patterns.* ICSE 2005.
- R. Kowalski, M. Sergot. *A logic-based calculus of events.* New Generation Computing, 1986.
- D. Giannakopoulou, J. Magee. *Fluent model checking for event-based systems.* ESEC/FSE 2003.
- J.-R. Abrial. *Modeling in Event-B.* Cambridge University Press, 2010.
- L. Lamport. *Specifying Systems* (TLA+). Addison-Wesley, 2002.
- D. Giannakopoulou, T. Pressburger, A. Mavridou, J. Schumann. *Generation of formal requirements from structured natural language* (FRET). REFSQ 2020.
- A. Mavin, P. Wilkinson, A. Harwood, M. Novak. *Easy Approach to Requirements Syntax (EARS).* RE 2009.
- M. W. Whalen, A. Rajan, M. P. E. Heimdahl, S. P. Miller. *Coverage metrics for requirements-based testing.* ISSTA 2006.
