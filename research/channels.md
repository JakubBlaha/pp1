# Sending and receiving on channels: how existing formalisms do it

## The question

A message on a channel has two sides: someone sends it and someone receives it. Our requirements talk about the software's side ("when the software **receives** MastershipInfo …"), while test cases talk about the tester's side ("**send** MastershipInfo with BACKUP"). We want to know:

1. Can "send" and "receive" be one and the same thing with two names?
2. How does the formalism know whether a message is something the **test does** (a stimulus) or something the **software does** (to be checked by an assertion)?
3. What happens when a channel is used in **both directions**, e.g. a command and its acknowledgement on the same DDS topic?

Running example for question 3 (hypothetical, not one of our requirements):

> When the software receives a command on topic CMD, it shall acknowledge it on CMD within 10 ms.

If "send" and "receive" are just two names for one event, the incoming command is also a "send" on CMD at the same instant, so the acknowledgement looks fulfilled before the software has done anything.

## Short answer

Existing formalisms use three approaches. All three agree on one thing: **somewhere it must be known which direction a message goes relative to the system under test**.

| Approach | Where the direction is | Examples | Two-way channel |
|---|---|---|---|
| 1. One shared event | nowhere in the event; in the role of each party | CSP, LOTOS, ioco | split into two channels / two sets of labels |
| 2. Direction on the channel | channel or port declaration (in / out) | TorXakis, UPPAAL TRON, ARINC 653, AADL, SysML, Lustre, Spectra, I/O automata | split into two channels, or declare `in out` |
| 3. Direction in the event | which operation is used (send / receive), from one fixed point of view | TTCN-3, UML sequence diagrams, session types, Event Calculus protocols | works directly |

And all testing formalisms agree on a second thing: **the tester may only produce the system's inputs and may only observe the system's outputs.** No tester produces the system's outputs itself.

---

## Approach 1: one shared event

**The idea.** A message is a single event that both parties take part in. "Send" and "receive" are not different events; they are the two parties' views of the same event.

**CSP (Hoare).** A communication is the event `c.v`: value `v` on channel `c`. The sender writes `c!v → P`, the receiver writes `c?x → Q(x)`. In the trace there is only `c.v`, once. The `!` and `?` are only syntax inside each process.

**LOTOS** works the same way: processes synchronise on a shared *gate*, and the gate itself has no direction. One LOTOS model of a communication protocol makes the consequence explicit: a one-way channel is the synchronisation of the sender's transmission gate with the receiver's reception gate, and "a second synchronisation handles the other way of the communication channel".

**ioco** (Tretmans), the standard theory of model-based testing, uses the same idea. An action `a` is one label shared by the tester and the implementation. As Tretmans puts it, the distinction between inputs and outputs "occurs in the transition systems themselves, and not in their communication". The tester is the mirror image of the implementation: its actions "synchronize with the output actions of the implementation, and vice versa".

**This is exactly your "same thing with two names".** It is a well-established view.

**How they handle direction.** Since the event itself has no direction, it has to come from elsewhere:
- In ioco, the set of labels is split once and for all into implementation **inputs** `L_I` and **outputs** `L_U`. A label is always one or the other.
- In CSP practice, channels are used in one direction only.

**How they handle a two-way channel.** By splitting it: CMD becomes two sets of labels (or two channels, or two synchronisations as in the LOTOS model above), one per direction. Otherwise the command and its acknowledgement are indistinguishable, which is the problem from the running example.

---

## Approach 2: direction declared on the channel

**The idea.** Each channel (or port) is declared as an input or an output **of the system under test**. A message's direction follows from its channel.

**TorXakis** (model-based testing tool, based on ioco). Every model declares its input and its output channels, and channels are unidirectional:

```
MODELDEF Model ::=
  CHAN IN    A, B
  CHAN OUT   C, D
  BEHAVIOUR  …
ENDDEF
```

**UPPAAL TRON** (online testing with timed automata). The user declares which channels are observable **inputs** and **outputs**. This declaration splits the model into the environment and the implementation: the environment sends on inputs and listens to outputs, the implementation sends on outputs and listens to inputs.

**ARINC 653** (avionics partitioning). Every sampling or queuing port is either a `SOURCE` or a `DESTINATION`.

**AADL** (avionics architecture language). Ports are `in`, `out` or `in out`. AADL also has the two styles of communication found in avionics:
- a **data port** holds one value; a new value overwrites the old one;
- an **event data port** queues messages, each with its own payload.

**SysML** flow properties are `in`, `out` or `inout`. Connecting two ports of the same type requires one to be *conjugated*, which flips all directions. This is the mirror again.

The same split appears outside communication too:
- In **Lustre / Kind 2**, a node has inputs and outputs. Its contract has *assumptions*, which may not depend on the current outputs, and *guarantees*, which typically do.
- In **Spectra** (GR(1) synthesis), every variable is either `env` (controlled by the environment) or `sys` (controlled by the system).
- In **I/O automata** (Lynch & Tuttle) and **interface automata** (de Alfaro & Henzinger), every action of a component is an input (`?`) or an output (`!`) *of that component*.

**How they handle a two-way channel.** Either split it into two one-way channels, as TorXakis and ARINC 653 require, or declare it `in out` / `inout`, as AADL and SysML allow. The `inout` case needs approach 3 for the individual messages.

---

## Approach 3: direction in the event

**The idea.** The event itself says which way the message goes, because it is named from one fixed point of view.

**TTCN-3** (ETSI test language, widely used in telecom and automotive). Test cases are written from the **tester's** point of view:
- a port lists the message types allowed `in`, `out` or `inout`;
- the tester uses `send` for a stimulus to the system under test and `receive` to check a response from it.

So `send` and `receive` are different operations, and an `inout` port can carry both directions. When two ports are connected, the `in` of one is linked to the `out` of the other: the mirror once more.

**UML sequence diagrams** (and MSCs). Every message has two occurrences: a *send event* on the sender's lifeline and a *receive event* on the receiver's lifeline. Who sends is always visible from the diagram.

**Multiparty session types.** This approach answers your question most directly. A *global type* describes the whole conversation, and a message is written once, `p → q : m` ("`p` sends `m` to `q`"). Each participant's *local type* is obtained by **projection**: for `p` the message becomes "send `m` to `q`", for `q` it becomes "receive `m` from `p`". So one message has one global description and two local names, and the direction is never lost.

**Event Calculus protocols** (Yolum & Singh, agent interaction protocols). Each message is a single event named after the sender's action, e.g. `Happens(sendGoods(…), t)`, `Happens(sendReceipt(…), t)`. The authors note that they leave out who performs it only because "each action can be performed by only one party". In other words, they rely on a fixed direction per message type (approach 2). Where that does not hold, the sender has to appear in the event term.

---

## What this means for us

### Our running examples in each approach

| | Req 08 (MastershipInfo, input) | Req 07 (MODESET_TOPIC, output) | CMD + acknowledgement (two-way) |
|---|---|---|---|
| Approach 1/2: one event, direction per channel | works | works | must split CMD into `CMD_in`, `CMD_out` |
| Approach 3: event named from one side | works | works | works |

### Option R1: one message, direction per channel (approaches 1 + 2)

This is closest to your original idea.

- Each channel declares `direction ↦ in` or `direction ↦ out`, relative to the software.
- `transmit` and `receive` are two names for one message. In a test case the writer may use either word.
- **Stimulus or assertion follows from the direction:** a message on an `in` channel is a stimulus, and a message on an `out` channel may only appear in an assertion.
- **A two-way topic is modelled as two channels.** Avionics ports (ARINC 653, AADL, AFDX) are mostly one-way anyway.
- **Event Calculus:** one event term per message, `Happens(message(c, v), t)`. It is a stimulus event (the event list says exactly when it happens) if `c` is `in`, and a system event (may happen at any time) if `c` is `out`.
- This is how TorXakis, UPPAAL TRON and ioco work.

### Option R2: one message, two points of view (approach 3, with the mirror from approach 1)

This is closest to your formulation "*received* in the requirement, *send* in the test case".

- **Requirements are written from the software's point of view:** `receive(c, v)` means into the software, and `transmit(c, v)` means out of the software. That is how requirements are already phrased ("the software shall transmit", "when it receives").
- **Test cases are written from the tester's point of view:** the tester *sends* (a stimulus) and *expects* (an assertion).
- **The formalism defines the mirror once:**

  | Tester's view (test case) | Software's view (requirement) |
  |---|---|
  | send `v` on `c` (stimulus) | `receive(c, v)` |
  | expect `v` on `c` (assertion) | `transmit(c, v)` |

- **Two-way channels work without splitting.** In the CMD example, the incoming command is a `receive` and the acknowledgement is a `transmit`, so they cannot be confused.
- **A test writer can still say "receive".** In the stimuli it means the software receives, so `receive(c, v)`. In the expected results it means the tester receives, so an expected `transmit(c, v)`. Where the message appears in the test case decides its meaning, as in TTCN-3.
- **Event Calculus:** two event terms. `receive(c, v)` is always a stimulus event and `transmit(c, v)` is always a system event, so the event name alone settles which group a message belongs to.
- This is how TTCN-3, interface automata and session types work.

### Both options

- **The tester never produces the software's output.** In R1 this is a rule on `out` channels; in R2 a stimulus can never be a `transmit`. This is what every testing formalism above does, and it is what the coverage rule in `CLAUDE.md` requires.
- **The channel keeps holding a value.** Our model, where a message sets the channel's value until the next message, is AADL's data port / ARINC 653's sampling port. Requirements about individual messages, AADL's event data ports, are still covered, because they refer to the `received` / `transmitted` event and read the value at that instant (with `ValAfter`, because of the timing convention).

### Recommendation

Prefer **R2**, for three reasons:
1. It matches your split exactly: "received" in the requirement, "send" in the test case.
2. It handles two-way channels without asking whoever formalises the requirement to split a topic into two entities.
3. It follows the most widely used test language (TTCN-3) and the most precise theory of "one message, two names" (session types).

R1 is the simpler alternative, with no points of view to keep apart, if we accept that a two-way topic must be split into two channels.

---

## Sources

- CSP communication events and `!` / `?`: [CSP lecture notes (Northeastern)](https://khoury.northeastern.edu/~riccardo/courses/csg399-sp06/csp-lec.pdf), [Parallel Programming Concepts (HPI)](https://osm.hpi.de/parProg/2011/03_Theory.pdf)
- LOTOS, a two-way channel as two synchronisations: [LOTOS model of a security protocol (DIMACS workshop)](https://archive.dimacs.rutgers.edu/archive/Workshops/Security/program2/gl97-2/node3.html)
- ioco, input/output labels, tester as mirror: [Tretmans 1996, "Test generation with inputs, outputs and repetitive quiescence"](https://ris.utwente.nl/ws/files/6713476/277_Tre96a.pdf), [Tretmans, Model-based testing with labelled transition systems](https://www.microsoft.com/en-us/research/?p=183376)
- TorXakis `CHAN IN` / `CHAN OUT`: [TorXakis wiki, ModelDefs](https://github.com/TorXakis/TorXakis/wiki/ModelDefs), [Model-Based Testing of Networked Applications (arXiv)](https://arxiv.org/pdf/2102.00378)
- UPPAAL TRON input/output channels: [UPPAAL TRON documentation](https://docs.uppaal.org/extensions/tron), [TRON adaptation](https://homes.cs.aau.dk/~marius/tron/adaptation.html)
- ARINC 653 `SOURCE` / `DESTINATION`: [PTC Modeler, ARINC sampling port](https://support.ptc.com/help/modeler/r9.2/en/Integrity_Modeler/arinc/ARINC_Sampling_port.html), [ARINC queuing port](https://support.ptc.com/help/modeler/r9.2/en/Integrity_Modeler/arinc/ARINC_Queuing_port.html)
- AADL data ports vs event data ports: [Real-Time Model Checking Support for AADL (arXiv)](https://arxiv.org/pdf/1503.00493), [Formalization of the AADL Run-Time Services (arXiv)](https://arxiv.org/pdf/2507.06881)
- SysML flow directions and conjugated ports: [No Magic SysML plugin documentation](https://docs.nomagic.com/x/U1MyB), [SysML plugin user guide](https://www.3ds.com/fileadmin/PRODUCTS-SERVICES/CATIA/NoMagic/pdf/sysml-plugin-user-guide.pdf)
- Kind 2 assumptions and guarantees: [Kind 2 Lustre input documentation](https://kind.cs.uiowa.edu/kind2_user_doc/2_input/1_lustre.html)
- Spectra `env` / `sys`: [Spectra: A Specification Language for Reactive Systems (arXiv)](https://arxiv.org/pdf/1904.06668)
- I/O automata: [Input/output automaton (Wikipedia)](https://en.wikipedia.org/wiki/Input/output_automaton), [Lynch & Tuttle (MIT)](https://groups.csail.mit.edu/tds/papers/Lynch/tuttle.html)
- Interface automata: [de Alfaro & Henzinger, Interface automata](https://research-explorer.ista.ac.at/record/4622)
- TTCN-3 ports and `send` / `receive`: [Grabowski et al., An Introduction to TTCN-3](https://www.swe.informatik.uni-goettingen.de/sites/default/files/publications/GrabowskiEtAll.pdf), [Pietschker, Introduction to TTCN-3 (ETSI)](https://ttcn-3.etsi.org/TTCN3UC2007/Presentations/Tutorials/AndrejPietschker_IntroductionToTTCN3.pdf)
- UML send and receive events: [Sparx Systems, Message](https://www.sparxsystems.com/enterprise_architect_user_guide/14.0/model_domains/message.html)
- Multiparty session types and projection: [Generalising Projection in Asynchronous Multiparty Session Types (arXiv)](https://arxiv.org/pdf/2107.03984), [Bocchi, MPST lecture (BETTY summer school)](https://www.dcs.gla.ac.uk/research/betty/summerschool2016.behavioural-types.eu/programme/BocchiBETTY06_MPST_12.pdf/at_download/file.pdf)
- Event Calculus protocols: [Yolum & Singh, Flexible protocol specification and execution (AAMAS 2002)](https://www.csc2.ncsu.edu/faculty/mpsingh/papers/mas/aamas-02-protocols.pdf)
- DDS readers and writers on the same topic: [RTI community, ignoring local writers](https://community.rti.com/node/1869), [Fast DDS, ignore local endpoints](https://eprosima-Fast-RTPS.readthedocs.io/en/latest/fastdds/property_policies/ignore_local_endpoints.html)
