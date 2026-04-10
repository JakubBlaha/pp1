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

| Tier | Use when requirement contains |
|------|-------------------------------|
| LTL  | Only ordering / causality, no time bounds, no arithmetic |
| MTL  | Ordering + concrete time bounds, no arithmetic |
| STL  | Time bounds + arithmetic on real-valued signals |
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

| Type             | Meaning |
|------------------|---------|
| `SIGNAL`         | A software signal or variable |
| `REGISTER`       | A hardware CPU register |
| `MEMORY_REGION`  | A named region of memory |
| `DDS_TOPIC`      | A DDS communication topic |
| `DATATYPE`       | A structured data type with named parameters |
| `HARDWARE`       | A hardware component (e.g. processor) |
| `ABSTRACT`       | A higher-level entity not directly addressable |

---

## Requirement Structure

```
REQ <id> [<descriptive label>]
  TIER:    LTL | MTL | STL | TA
  LEVEL:   shall | must

  TRIGGER: <event_expr>
  [GUARD:  <condition_expr>]
  [DEADLINE: WITHIN <n> <unit> | LESS_THAN <n> <unit>]
  EFFECT: [ORDERED]
    [<n>.] <action_expr>
    ...
```

---

## Event Expressions (TRIGGER)

| Expression | Meaning |
|------------|---------|
| `ALWAYS` | No trigger; the property must hold at every instant |
| `ON power_up(<entity>)` | Hardware power-up event |
| `ON initialization` | End of software initialization phase |
| `ON write(<entity>)` | A write operation to an entity |
| `ON receive(<datatype> [, <param>=<value>])` | Receive a data instance |
| `ON return(<entity>)` | An invoked routine returns |
| `AFTER <event_expr>` | After (not during) the named event |
| `WHILE STATE(<name>)` | While the system is in a named state |

---

## Conditions (GUARD)

| Syntax | Meaning |
|--------|---------|
| `<expr> > <expr>` | Greater-than comparison |
| `<expr> >= <expr>` | Greater-or-equal comparison |
| `<expr> == <expr>` | Equality |
| `<expr> IS <literal>` | Value equals a named constant (TRUE, BACKUP, …) |
| `ALL_OF { <cond>, … }` | All conditions must hold |
| `ANY_OF { <cond>, … }` | At least one condition must hold |
| `NOT <cond>` | Negation |

---

## Expressions

| Syntax | Meaning |
|--------|---------|
| `<entity>` | Current value of entity |
| `<entity>[k-1]` | Value at the previous discrete time step |
| `PREV(<entity>)` | Alias for `<entity>[k-1]` |
| `ADDR(<entity>)` | Memory address of entity |
| `DIFF(<a>, <b>)` | Arithmetic difference `a − b` |
| `SIGNED(<expr>)` | Interpret bit pattern as signed integer |
| `MAX_PEAK(<entity>)` | Historical maximum peak value of entity |
| `MIN_PEAK(<entity>)` | Historical minimum peak value of entity |
| `COUNT(ON <event>, SINCE ON <event>)` | Number of times event occurred since another event |

---

## Action Vocabulary (EFFECT)

| Action | Meaning |
|--------|---------|
| `CALCULATE <entity> = <expr>` | Compute and assign a value |
| `READ <entity> FROM <addr>` | Read value from a memory address |
| `STORE <entity> TO <dst>` | Write value to a destination |
| `COPY <src> TO <dst>` | Copy value between two locations |
| `INVOKE <entity>` | Call a routine or handler |
| `HOLD <entity>` | Suspend / freeze execution |
| `TOGGLE <entity>` | Invert the boolean value of entity |
| `TRANSMIT <entity>(<param>=<val>) VIA <channel>` | Send a signal over a channel |
| `CONFIGURE { <entity> <- <expr>, … }` | Set registers or fields according to a mapping |
| `SET_STATE <state_name>` | Transition to a named system state |
| `START_EXECUTE <entity>` | Begin execution of a task or sequence |
| `IF <cond> THEN <action>` | Conditional action (inline, within a step) |

When `ORDERED` is present, the listed steps must execute in the given sequence. Each step is a state in the implied automaton (TA tier) or is expressed with `U` operators (LTL/MTL/STL tier).

---

## Temporal Logic Translation Reference

```
// LTL
G( trigger ∧ guard  →  F( effect ) )

// MTL  (d = deadline value with unit)
G( trigger ∧ guard  →  F[0,d]( effect ) )

// STL  (same shape; predicates may be arithmetic over real-valued signals)
G( trigger ∧ guard  →  F[0,d]( effect ) )

// Ordered steps (LTL)
G( trigger  →  step1 U (step2 U step3) )

// Initial condition (STL)
<entity>[0] = <value>
```

---

# Requirements

## 01

The software function shall calculate the signal [EngagementNoSat_u] according to the following equation:

```
[EngagementNoSat_u] = 1.2*[EngagementNoSat_u](k-1) if [Switch_b] is TRUE;
[Lon_u] otherwise.
Notes: The initial condition of [EngagementNoSat_u] is equal to 0 and (k) denotes a given
time instant.
```

---

```
ENTITY EngagementNoSat_u : SIGNAL  INITIAL 0
ENTITY Switch_b          : SIGNAL
ENTITY Lon_u             : SIGNAL

REQ 01 [Arithmetic / boolean operations]
  TIER:    STL
  LEVEL:   shall
  TRIGGER: ALWAYS
  EFFECT:
    CALCULATE EngagementNoSat_u[k] =
      IF Switch_b IS TRUE:
        1.2 * EngagementNoSat_u[k-1]
      ELSE:
        Lon_u

// Initial condition
EngagementNoSat_u[0] = 0

// STL
G( EngagementNoSat_u =
     (Switch_b = TRUE  →  1.2 * prev(EngagementNoSat_u))
   ∧ (Switch_b ≠ TRUE  →  Lon_u) )
∧ EngagementNoSat_u[0] = 0
```

## 02

```
The software shall store the maximum execution time measurement data in Non-Volatile
Memory in the address region MEASUREMT_BLOCK.
```

```
ENTITY max_exec_time_data : ABSTRACT
ENTITY MEASUREMT_BLOCK    : MEMORY_REGION  NON_VOLATILE

REQ 02 [Interface with hardware – NVM]
  TIER:    LTL
  LEVEL:   shall
  TRIGGER: ALWAYS
  EFFECT:
    STORE max_exec_time_data TO MEASUREMT_BLOCK

// LTL
G( F( stored(max_exec_time_data, MEASUREMT_BLOCK) ) )
```

## 03

```
The software must perform the following actions in the specified order:
1) Read the calibration constant value at the address 0xAA000018;
2) Store the calibration constant value in the DTSCON register.

```

```
ENTITY calibration_const : ABSTRACT  ADDRESS 0xAA000018
ENTITY DTSCON            : REGISTER

REQ 03 [Interface with hardware – CPU registers]
  TIER:    LTL
  LEVEL:   must
  TRIGGER: ALWAYS
  EFFECT:  ORDERED
    1. READ  calibration_const FROM 0xAA000018
    2. STORE calibration_const TO DTSCON

// LTL (ordering via U)
G( F( read(calibration_const, 0xAA000018)
      U stored(calibration_const, DTSCON) ) )
```

## 04

```
The software must configure IVORx registers with the addresses of Exception Vectors that
compose the Exception Vector Table, according to the following table:

IVORx Exception
0 Critical input
1 Machine check
```

```
ENTITY IVOR0         : REGISTER
ENTITY IVOR1         : REGISTER
ENTITY CriticalInput : ABSTRACT   // Exception Vector for critical input
ENTITY MachineCheck  : ABSTRACT   // Exception Vector for machine check

REQ 04 [Interrupt / exception handling – vector table config]
  TIER:    LTL
  LEVEL:   must
  TRIGGER: ALWAYS
  EFFECT:
    CONFIGURE {
      IVOR0 <- ADDR(CriticalInput),
      IVOR1 <- ADDR(MachineCheck)
    }

// LTL
F( IVOR0 = ADDR(CriticalInput) ∧ IVOR1 = ADDR(MachineCheck) )
```

## 05

```
The software, when handling an exception, must execute the following steps in the following
order:
1) Copy the value of register SRR0 to register R5.
2) Invoke the image exception handler.
3) If the exception handler returns, hold the software execution.
```

```
ENTITY SRR0                    : REGISTER
ENTITY R5                      : REGISTER
ENTITY image_exception_handler : ABSTRACT
ENTITY software_execution      : ABSTRACT

REQ 05 [Sequenced actions – exception handling procedure]
  TIER:    TA
  LEVEL:   must
  TRIGGER: WHILE STATE(handling_exception)
  EFFECT:  ORDERED
    1. COPY SRR0 TO R5
    2. INVOKE image_exception_handler
    3. IF image_exception_handler RETURNS:
         HOLD software_execution

// LTL (ordering via U; step 3 is conditional)
G( handling_exception →
     copy(SRR0, R5)
     U (invoke(image_exception_handler)
        U (returns(image_exception_handler) → hold(software_execution))) )
```

## 06

```
The software must start to execute the sequence of tasks allocated to the execution schedule
in less than 2 seconds after processor power-up.
```

```
ENTITY task_sequence : ABSTRACT
ENTITY processor     : HARDWARE

REQ 06 [Scheduling]
  TIER:     MTL
  LEVEL:    must
  TRIGGER:  ON power_up(processor)
  DEADLINE: LESS_THAN 2 seconds
  EFFECT:
    START_EXECUTE task_sequence

// MTL
G( power_up(processor) → F[0, 2s)( executing(task_sequence) ) )
```

## 07

```
The software, after its initialization, shall transmit the signal 'Mode Enable' with value TRUE
through DDS Topic 'MODESET_TOPIC'.
```

```
ENTITY ModeEnable     : SIGNAL
ENTITY MODESET_TOPIC  : DDS_TOPIC

REQ 07 [I/O processing]
  TIER:    LTL
  LEVEL:   shall
  TRIGGER: AFTER ON initialization
  EFFECT:
    TRANSMIT ModeEnable(value=TRUE) VIA MODESET_TOPIC

// LTL
G( initialized → F( transmit(ModeEnable, TRUE, MODESET_TOPIC) ) )
```

## 08

```
The software shall operate as Backup when receive a new data instance of the datatype
MastershipInfo, with parameter [Mastership_b] as BACKUP.

```

```
ENTITY MastershipInfo : DATATYPE  PARAMS { Mastership_b: ENUM }

REQ 08 [State-machine logic]
  TIER:    LTL
  LEVEL:   shall
  TRIGGER: ON receive(MastershipInfo, Mastership_b=BACKUP)
  EFFECT:
    SET_STATE Backup

// LTL
G( receive(MastershipInfo, Mastership_b=BACKUP) → X( mode = BACKUP ) )
```

## 09

```
The software must toggle valid_range, within 500 ns of a write to d, if ALL the following
conditions are satisfied:
- The difference between last Maximum Peak and Minimum Peak of d is higher than 655;
- It is the second write to d after the Minimum Peak detection;
- Signed value of d is higher than the signed value of last d.
```

```
ENTITY valid_range : SIGNAL
ENTITY d           : SIGNAL

REQ 09 [Timed operations]
  TIER:     STL
  LEVEL:    must
  TRIGGER:  ON write(d)
  DEADLINE: WITHIN 500 ns
  GUARD:    ALL_OF {
    DIFF(MAX_PEAK(d), MIN_PEAK(d)) > 655,
    COUNT(ON write(d), SINCE ON MIN_PEAK_DETECTED(d)) == 2,
    SIGNED(d) > SIGNED(PREV(d))
  }
  EFFECT:
    TOGGLE valid_range

// STL
G( write(d)
   ∧ (MAX_PEAK(d) − MIN_PEAK(d) > 655)
   ∧ (COUNT(write(d), SINCE(MIN_PEAK_DETECTED(d))) = 2)
   ∧ (SIGNED(d) > SIGNED(prev(d)))
   →  F[0, 500ns]( toggled(valid_range) ) )
```
