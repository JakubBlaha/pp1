# Goals of project

1) Take a requirement written in english and transform it into a formal representation.
2) Take test cases supposed to test this requirement written in english and transform them into a formal representation.
3) Validate if the requirement is fully covered by the test cases. (Skip for now, this will be easy to do later).

# Context and stuff we could use:

## Timed Automata

A formalism for modeling systems with a finite set of discrete **states**, **transitions** between them, and one or more real-valued **clocks** that advance continuously. Transitions can have *guards* (conditions on clock values, e.g. `c < 2`) and *resets* (setting a clock back to zero). States can have *invariants* that must hold as long as the system stays in them.

**How it could be used here:**
- **Timing constraints** — req 06 ("start task sequence in less than 2 s after power-up") maps directly: a clock is reset on the power-up event; a transition to the "running" state is guarded by `c ≤ 2`.
- **Timed operations** — req 09 ("toggle `valid_range` within 500 ns of a write to `d`"): a clock is reset on the write event; the automaton must reach the "toggled" state before the clock exceeds 500 ns.
- **Sequenced actions** — reqs 03 and 05 (ordered steps): each step is a state; transitions enforce the required ordering and can additionally carry time guards if needed.
- **State-machine logic** — req 08 (operate as Backup upon receiving a specific event): natural to model as a state machine where the event triggers a transition to the Backup state.

## LTL, MTL, STL logic

### LTL — Linear Temporal Logic

Expresses properties over infinite sequences of discrete states using operators like **G** (globally / always), **F** (eventually), **X** (next step), and **U** (until). It captures *ordering* of events but has no notion of real time.

**How it could be used here:**
- **I/O processing** — req 07 ("after initialization, transmit 'Mode Enable' = TRUE"): `G(initialized → F(transmit_ModeEnable = TRUE))`.
- **State-machine logic** — req 08: `G(receive(MastershipInfo, BACKUP) → X(mode = BACKUP))`.
- **Sequenced actions** — reqs 03 / 05: `G(start → (step1 U (step2 U step3)))`.

LTL is the right choice whenever the requirement talks about *ordering* and *causality* but places no numeric time bound.

---

### MTL — Metric Temporal Logic

LTL extended with **time-bounded** temporal operators, e.g. **F[0,2s]** ("eventually within 2 seconds") or **G[a,b]**. Suitable when a requirement names a concrete time deadline but the underlying signals are still Boolean.

**How it could be used here:**
- **Scheduling** — req 06: `G(power_up → F[0,2s](tasks_running))`.
- **Timed operations** — req 09: `G(write(d) ∧ conditions → F[0,500ns](toggle(valid_range)))`.

MTL is the right choice when an LTL property needs a concrete deadline attached to it.

---

### STL — Signal Temporal Logic

MTL extended to work over **continuous/real-valued signals** rather than just Boolean propositions. Predicates can express arithmetic comparisons (e.g. `x > 655`, `y = 1.2 * y_prev`), making it suitable for requirements involving numeric thresholds or equations over measured values.

**How it could be used here:**
- **Arithmetic / boolean operations** — req 01 (recurrence equation for `EngagementNoSat_u`): the update rule and initial condition can be expressed as an STL formula over the signal's value at consecutive time steps.
- **Timed operations with numeric guards** — req 09 combines a 500 ns deadline *and* three numeric conditions on `d`; STL captures both in a single formula: `G(write(d) ∧ (max_peak − min_peak > 655) ∧ second_write ∧ (d > d_prev) → F[0,500ns](toggle(valid_range)))`.

STL is the right choice when a requirement mixes real-time deadlines with arithmetic conditions over signal values.

# Resouces

## DDS

**Data Distribution Service** — a publish/subscribe middleware standard (OMG DDS) for real-time, scalable data communication. Publishers send data on named **Topics**; subscribers receive it without any direct coupling between the two sides.

**How it could be used here:**
- **I/O processing** — req 07 ("transmit signal 'Mode Enable' with value TRUE through DDS Topic 'MODESET_TOPIC'"): the Topic acts as the communication channel; the formal model must capture the act of publishing a typed value on that Topic after a triggering event (initialization).
- **State-machine logic** — req 08 ("receive a new data instance of the datatype MastershipInfo"): an incoming DDS sample is the event that triggers the state transition; the formal model needs to represent reception of a typed DDS data instance with specific field values.