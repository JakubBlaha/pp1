# Findings

Open problems found while working on the formalism. Each one needs to be resolved in `tex-new/formalism.tex`.

## A test case does not produce one trace

**Status:** partly resolved on 6 Oct 2026: item 1 of "To decide later" is done; items 2 and 3 are open.

**What the formalism says.** `formalism.tex`, Section "Requirements & Test cases":

> A test case exercises a subset of the same entities to produce a concrete trace, which the coverage checker then analyses against the requirement's constraint.

**Why it is wrong.** A test case is a setup, a set of stimuli and a set of assertions. Setup and stimuli fix only some values: the setup fixes values at time 0, and each stimulus fixes the values its operation's effect predicate talks about. Everything else is left open, in particular every value the *system* changes rather than the test. So a test case is satisfied by many traces, not one.

**Example — Req 10, TC2.**

> The software shall enter the emergency mode if any of the following failures individually occurs twice in less than 10 seconds: (a) sensor failure, (b) energy failure, (c) communication failure.
>
> TC2: Sensor failure twice in an interval of 9 seconds → expected: entering emergency mode.

The stimuli are `fire(sensor_failure)` at 0 s and at 9 s. Nothing in the test case says what `emergency_mode` does: it is changed by the system, not by the test. So the test case allows traces where `emergency_mode` becomes true at 9 s, traces where it becomes true at 20 s, traces where it never does, and so on. There is no single "concrete trace".

**What a correct definition would say.** A test case denotes a **set of traces**: all traces that agree with the setup at time 0 and satisfy the effect predicate of every stimulus. The assertions then say which of these traces the test expects.

**Why it matters.**
- The coverage checker (project goal 3) has to be defined over this set of traces, not over a single trace. What "the checker analyses the trace against the requirement" means is therefore undefined at the moment.
- It is the root of the translation problem to the Event Calculus (`calculi.md`, §3.1). EC tools assume that the events listed in the test are *all* the events that happen. That turns the set of traces into a single trace, in which nothing the system does ever happens. For example, `emergency_mode` stays `false` in TC2. The fix discussed there is to keep that assumption only for the events the test fires and to leave the system's own events open. To state this fix, the formalism first has to distinguish **stimulus events** (fired by the test) from **system events** (performed by the software). It currently does not.

**To decide later.**
1. Replace "produce a concrete trace" with the set-of-traces definition.
2. Distinguish stimulus events from system events, for example by marking which operations a test may fire.
3. Define what the coverage checker computes over the set of traces.

> [!TIP]
> **How item 1 was resolved.** `formalism.tex` now says that a test case stands for the set of traces it allows, and defines two sets (Definition "Traces of a test case"):
> - $\mathit{Traces}(\mathit{TC})$: the traces that agree with the setup at time 0 and in which the effect predicate of every stimulus holds;
> - $\mathit{Expected}(\mathit{TC})$: the traces in $\mathit{Traces}(\mathit{TC})$ in which every assertion holds at its time point.
>
> In TC2 above, $\mathit{Traces}$ contains the traces where `emergency_mode` becomes true at 9 s, at 20 s or never; $\mathit{Expected}$ keeps only the first. A condition fixed by the stimuli is still not the same in every trace, because an effect says that an event happens when the test fires it, not *only* then (item 2).

## A reset has no effect on storage — not a problem for coverage

**Status:** closed, no change to the formalism. A rule for what a reset does was added to `formalism.tex` on 4 Oct 2026 and reverted the same day. `formalism.tex` has no `reset` operation; a reset is an ordinary `EventTrigger` fired with `fire`.

**The observation.** Nothing in the formalism says what a reset does to storage. Req 02 (`examples.tex`):

> The software shall store the maximum execution time measurement data in non-volatile memory at address MEASUREMT_BLOCK.

```
Entities: max_exec_time_data (Abstract), MEASUREMT_BLOCK (Storage, non_volatile),
          reset (EventTrigger), ev_reset (Event, type ↦ generic)
Eventually( Val(MEASUREMT_BLOCK, Now) = Val(max_exec_time_data, Now) )
∧ Always( Happening(ev_reset, Now) ⇒ ValAfter(MEASUREMT_BLOCK, Now) = Val(MEASUREMT_BLOCK, Now) )
```

The second line says "the value survives a reset". Take a test that writes 42 to `MEASUREMT_BLOCK` at 1 s and fires `reset` at 5 s. The write's effect holds until the next operation on `MEASUREMT_BLOCK`, and a reset is not such an operation, so the value stays 42 across the reset. That would happen even if the memory were volatile. In the model the second line is therefore always true. We first concluded that it "tests nothing" and added a rule saying that a reset clears every volatile storage.

**Why that was the wrong question.** "Can this requirement be false in the model?" is a question about *satisfaction*. Our goal is *coverage*: does some test exercise each part of the requirement? For the reset part, a covering test must:

1. fire a reset, which is visible in the test's stimuli, and
2. check that the stored value is still there afterwards, which is visible in the test's assertions.

| Test | Stimuli | Assertion | Covers the reset part? |
|---|---|---|---|
| A | store | value = stored data | no, no reset |
| B | store, reset | value after reset = value before | yes |

The checker reads both directly off the test. Whether the memory really keeps its value is the test's *expected outcome*. Checking it is the job of running the test on the real system, not of the formalism. So the formalism does not need to know what a reset does.

> [!TIP]
> **General rule for coverage.** What the test controls (stimuli, setup) decides which conditions of a requirement are made true. What the software or hardware does comes from the test's assertions. The formalism does not need to model the behaviour of the software or the hardware. This rule is also recorded in `CLAUDE.md` ("The goal is coverage, not satisfaction").

**The reset part of Req 02 must stay.** It is what tells the coverage checker that a covering test has to fire a reset and then check the value. Without it, test A alone would count as full coverage.

## `receive` does not fix what is received

**Status:** open. Resolved once one of the channel designs in `channels.md` is adopted (see "Is the concern still valid?" below).

**What the formalism says.** `formalism.tex` has two separate operations for channels:
- `transmit(t, c, expr)` puts the value `expr` on the channel `c`.
- `receive(t, c, dst)` copies the channel's *current* value into a Signal `dst`. It has no argument for the value itself.

A test describes an incoming message with **one** stimulus: the message arrives at the software. In our vocabulary that stimulus is `receive`. It is not "a `transmit` by the other node, followed by a `receive` by the software", which would be two stimuli for one message. But `receive` only says *when* the message arrives, not *what* it contains, so a test that uses it alone leaves the content open.

**Example — Req 08.**

> The software shall operate as Backup when it receives a new data instance of *MastershipInfo* with parameter *Mastership_b* equal to BACKUP.

```
Entities: MastershipInfo (Channel), ev_received_mastership (Event: received),
          Backup (State), ev_entered_backup (Event: entered)
Causes( Happening(ev_received_mastership, Now) ∧ Val(MastershipInfo, Now) = BACKUP,
        Happening(ev_entered_backup, Now) )
```

A test case as a tester might write it:

> TC1: The software receives a MastershipInfo message at 1 s. Expected: the software operates as Backup at 2 s.

With today's operations it can only be formalised like this (using a Signal `mastership_in` as the destination of `receive`):

```
setup:      σ0 = {}
stimuli:    { (1, receive, MastershipInfo, mastership_in) }
assertions: { 2 ↦ { HasHappened(ev_entered_backup, 2) } }
```

Nothing puts a value on `MastershipInfo`, so its value at 1 s is unconstrained. TC1 allows, among others, these two traces:

| Trace | `Val(MastershipInfo, 1)` | Condition of Req 08 at 1 s | Does TC1 exercise Req 08? |
|---|---|---|---|
| A | `BACKUP` | true | yes |
| B | `PRIMARY` | false | no |

The coverage checker cannot decide whether TC1 exercises Req 08. The only way to fix the content with today's operations is to add a second stimulus, `transmit(MastershipInfo, BACKUP)`, before the `receive`. That makes the test describe one message with two stimuli, which is the problem above.

**Fix.** The single stimulus that describes a message must carry its content. `channels.md` proposes two ways to model messages, and both do this:

- **Design A: one message, direction declared on the channel.**
  - Each channel is declared as an input or an output of the software.
  - `transmit(t, c, v)` and `receive(t, c, v)` are two names for the same message with value `v`, so a test writer may use either word.
  - A message on an input channel is a stimulus. A message on an output channel may only appear in an assertion.
  - A channel used in both directions has to be split into two channels.
- **Design B: one message, always named from the software's side.**
  - `receive(c, v)` always means "the message goes *into* the software", and `transmit(c, v)` always means "it goes *out* of the software".
  - In a test case, a message the tester sends is the software's `receive`, and a message the tester expects is the software's `transmit`, whichever word the test writer used.
  - A channel used in both directions needs no splitting.

In both designs, `receive` gets a value argument and loses `dst`. In the Event Calculus this is `Happens(receive(mastership_info, BACKUP), t)`.

**Is the concern still valid?** With either design, **no**, as far as the formalism is concerned. TC1 can no longer be formalised without stating what was received. Written with the content, it becomes:

```
stimuli:    { (1, receive, MastershipInfo, BACKUP) }
```

Every trace of this test has the condition of Req 08 true at 1 s, so the checker can decide that it exercises Req 08.

**Why the stimulus makes `ev_received_mastership` happen.** Every operation's effect contains an `EvtPred(e, label, t)` term. It says: every Event entity whose `target` is `e` and whose `type` is `label` is true at `t`. Req 08 declares exactly such an entity, `ev_received_mastership` with `target ↦ id_MastershipInfo` and `type ↦ received`. So for the stimulus `(1, receive, MastershipInfo, BACKUP)`:

1. In every trace of the test, the effect of `receive` holds: `EvtPred(MastershipInfo, received, 1)`, and the channel holds `BACKUP` after 1.
2. `EvtPred` makes the matching entity true: `Val(ev_received_mastership, 1) = true`, i.e. `Happening(ev_received_mastership, 1)`.
3. The value part holds: `ValAfter(MastershipInfo, 1) = BACKUP`.
4. So the condition of Req 08 is true at `Now = 1` in every trace.

This link only works because the requirement and the test share the same entities and the event's `target` and `type` match the operation. With an event on another target, or no event entity at all, `EvtPred` would make nothing happen.

**Limitation: only "if", not "only if".** `EvtPred` makes the event happen *when* the test sends the message, but nothing says it happens *only* then. A trace where `ev_received_mastership` is also true at 5 s, without any stimulus, satisfies the test as well. For Req 08 this does not matter. For a requirement such as "if MastershipInfo is received twice within 10 s …", the checker could not rule out a second reception the test never sent. Events on input channels should happen *exactly* when the test sends, which is the stimulus-vs-system-event question from the first finding.

This needs one adjustment in Req 08. Because the message now *sets* the channel's value, the timing convention applies: the new value is visible only after 1 s, and `Val(MastershipInfo, 1)` still shows the previous one. The condition must read `ValAfter(MastershipInfo, Now) = BACKUP`.

What remains is a **translation** concern, not a formalism concern. If the English test omits the content, as TC1 does, the translation into the formalism must report the gap rather than invent a value.

**To decide later.** Which channel design to adopt: design A (direction on the channel) or design B (named from the software's side). `channels.md` compares them and recommends design B.
