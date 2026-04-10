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
```

## 02

```
The software shall store the maximum execution time measurement data in Non-Volatile
Memory in the address region MEASUREMT_BLOCK.
```

## 03

```
The software must perform the following actions in the specified order:
1) Read the calibration constant value at the address 0xAA000018;
2) Store the calibration constant value in the DTSCON register.

```
## 04

```
The software must configure IVORx registers with the addresses of Exception Vectors that
compose the Exception Vector Table, according to the following table:

IVORx Exception
0 Critical input
1 Machine check
```

## 05

```
The software, when handling an exception, must execute the following steps in the following
order:
1) Copy the value of register SRR0 to register R5.
2) Invoke the image exception handler.
3) If the exception handler returns, hold the software execution.
```

## 06

```
The software must start to execute the sequence of tasks allocated to the execution schedule
in less than 2 seconds after processor power-up.
```

## 07

```
The software, after its initialization, shall transmit the signal 'Mode Enable' with value TRUE
through DDS Topic 'MODESET_TOPIC'.
```

## 08

```
The software shall operate as Backup when receive a new data instance of the datatype
MastershipInfo, with parameter [Mastership_b] as BACKUP.

```
## 09

```
The software must toggle valid_range, within 500 ns of a write to d, if ALL the following
conditions are satisfied:
- The difference between last Maximum Peak and Minimum Peak of d is higher than 655;
- It is the second write to d after the Minimum Peak detection;
- Signed value of d is higher than the signed value of last d.
```
