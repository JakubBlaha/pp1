**Confidential**

*Table 1 examples of requirements of interest*

| Requirement type                        | Example of requirement text                                                                                                                                                                                                                                                                                                                                |
| :-------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Arithmetic/boolean operations           | The software function shall calculate the signal `[EngagementNoSat_u] according to the following equation:<br>[EngagementNoSat_u] = 1.2*[EngagementNoSat_u](k-1) if [Switch_b] is TRUE;<br>[Lon_u] otherwise.`<br><br>Notes: The initial condition of [EngagementNoSat_u] is equal to 0 and (k) denotes a given time instant.                              |
| Interface with hardware (NVM)           | The software shall store the maximum execution time measurement data in Non-Volatile Memory in the address region MEASUREMT_BLOCK.                                                                                                                                                                                                                         |
| Interface with hardware (CPU registers) | The software must perform the following actions in the specified order:<br>1) Read the calibration constant value at the address 0xAA000018;<br>2) Store the calibration constant value in the DTSCON register.                                                                                                                                            |
| Interrupt/exception handling            | The software must configure IVORx registers with the addresses of Exception Vectors that compose the Exception Vector Table, according to the following table:<br><br>IVORx &nbsp; &nbsp; &nbsp; &nbsp; Exception<br>0 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Critical input<br>1 &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; Machine check |
| Sequenced actions                       | The software, when handling an exception, must execute the following steps in the following order:<br>1) Copy the value of register SRR0 to register R5.<br>2) Invoke the image exception handler.<br>3) If the exception handler returns, hold the software execution.                                                                                    |
| Scheduling                              | The software must start to execute the sequence of tasks allocated to the execution schedule in less than 2 seconds after processor power-up.                                                                                                                                                                                                              |
| I/O processing                          | The software, after its initialization, shall transmit the signal 'Mode Enable' with value TRUE through DDS Topic 'MODESET_TOPIC'.                                                                                                                                                                                                                         |
| State-machine logics                    | The software shall operate as Backup when receive a new data instance of the datatype MastershipInfo, with parameter [Mastership_b] as BACKUP.                                                                                                                                                                                                             |
| Timed operations                        | The software must toggle valid_range, within 500 ns of a write to d, if ALL the following conditions are satisfied:<br>- The difference between last Maximum Peak and Minimum Peak of d is higher than 655;<br>- It is the second write to d after the Minimum Peak detection;<br>- Signed value of d is higher than the signed value of last d.           |

## Arithmetic/boolean operations

> The software function shall calculate the signal [EngagementNoSat_u] according to the following equation:
[EngagementNoSat_u] = 1.2*[EngagementNoSat_u](k-1) if [Switch_b] is TRUE;
[Lon_u] otherwise.

- identify an entities in the equation, in this case `[EngagementNoSat_u]`
- identify constant
- identify relationships between entities, in this case the new value is computed from the old value if the same variable?
- identify a condition
- identify a literal
- identify exclusive expressions (e.g. some expression is computed only based on value of other expressions -- this expression is computed only if this expression value is ???)
- initial variable values
- time -- system needs to be aware of time
  - time sources?

> The software shall store the maximum execution time measurement data in Non-Volatile Memory in the address region MEASUREMT_BLOCK.

- identify entity (e.g. maximum execution time), analyze code? How can we know which entity to link to?
  - it's not a variable, it's some higher level entity
  - identify where/at what address the entity data is being stored
  - is the entity a variable? a call to a function?
  - is the location a volatile memory or not? How to check?
  - needs to be stored in exact memory region. Another entity type.
  - is MEASUREMENT_BLOCK a pointer to some other value?

> The software must perform the following actions in the specified order:
> 1) Read the calibration constant value at the address 0xAA000018;
> 2) Store the calibration constant value in the DTSCON register.

- specific order of actions
- identify entity calibration constant value
- identify from which address the constant value was read
- check that a value is stored in a DTSCON register, we also need to identify what is the dtscon register
- check that actually the value of the calibration constant was stored in the register and not some other value.
- we may need to also include the feature to check what the duration was, how quickly this has happened. If this is in the allowed time constraints.

> The software must configure IVORx registers with the addresses of Exception Vectors that compose the Exception Vector Table, according to the following table:

> IVORx         Exception
> 0               Critical input
> 1               Machine check

- this just says it needs to be configured at some point, but we need the formalism to clearly specify when this will be configured, or maybe we dont. We might need to allow this to be configured anytime, but verify that it was configured correctly.
- identify if the mentioned exception vectors are located at constant addresses, or if their location can change, analyze test cases according to that
- there can be a set of registers, other registers may not need to be checked

> The software must start to execute the sequence of tasks allocated to the execution schedule in less than 2 seconds after processor power-up.

- the language needs to support events, binding to those events, consequences
- again, something needs to be done in some timeframe
- maybe there needs to be some pause between certain actions, that's another feature
- how do we test processor power up? Usually through some pins, the language must be able to reference hardware components, like pins, etc.

> The software, after its initialization, shall transmit the signal 'Mode Enable' with value TRUE through DDS Topic 'MODESET_TOPIC'.

- again, we are seeing "after it's initialization", which means that we need to be able to define an event, but maybe in some abstract way, so that way the test cases can cover the event, but not the specific subevents (like pin states), which can be defined somewhere else or omitted entirely.
- here we will need to support the description of some signal sequences, or at least an abstraction of them (like an entity again). So we might not need to describe the signal perfectly, but we need to support different entity types at least.

> The software shall operate as Backup when receive a new data instance of the datatype MastershipInfo, with parameter [Mastership_b] as BACKUP.

- description of different behaviors, set's of reactions to different events. A behavior might be a set of reactions to specific events or just a set of prescriptions how the system should operate from a high level perspective.
- Events need to have parameters, such as the instance of datatype MastershipInfo.

> The software must toggle valid_range, within 500 ns of a write to d, if ALL the following conditions are satisfied:
> - The difference between last Maximum Peak and Minimum Peak of d is higher than 655;
> - It is the second write to d after the Minimum Peak detection;
> - Signed value of d is higher than the signed value of last d.

- logic, formalism needs to be able to define variables and logical formulas.