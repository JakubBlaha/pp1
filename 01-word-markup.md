## Kategorie

| Kategorie                                        | Priklad                                            | Poznamka |
| ------------------------------------------------ | -------------------------------------------------- | -------- |
| konstanty                                        |                                                    |          |
| jednotky                                         |                                                    |          |
| poradi: pred/po                                  | after, before, when                                | automat  |
| pocet vyskytu                                    |                                                    | automat  |
| variace                                          |                                                    |          |
| cas: konstanta + jednotka                        | within 500 ns                                      |          |
| immediate hodnoty registru/pameti/signalu        |                                                    |          |
| hodnota registru/pameti/signalu menici se v case |                                                    |          |
| udalosti                                         | write                                              |          |
| abstraktni entity                                |                                                    |          |
| stav                                             | handling an exception                              |          |
| RFC 2119 - Requirement levels                    | must, shall                                        |          |
| musi-to-rozumnet                                 | toggle                                             |          |
| entita                                           | registr, pamet, signal value                       |          |
| logicke spojky: ALL/ANY/NONE podminek            | ALL the following conditions, one of the following |          |
| transformace                                     | difference between, sum, signed, value, last       |          |
| predikaty                                        |                                                    |          |
| history of entity                                | last                                               |          |
| general behavior                                 | software shall operate as backup                   |          |
| flow control                                     | if then, else, when                                |          |

---
The software shall operate as Backup when receive a new data instance of the datatype
MastershipInfo, with parameter [Mastership_b] as BACKUP.

---
The software must toggle valid_range, within 500 ns of a write to d, if ALL the following
conditions are satisfied:
- The difference between last Maximum Peak and Minimum Peak of d is higher than 655;
- It is the second write to d after the Minimum Peak detection;
- Signed value of d is higher than the signed value of last d.

Dont know:
- second write to ...


čas
logický čas, před a po; metrika - v jednotkách (např. tiky hodin), reálný (sekundy)
pořadí
variace
hodnoty úložišť nebo signálů
úložiště si pamatuje (read, write, hold)
signál se přenáší nebo nastane
události
k nějakému časovému okamžiku nebo k podmínce
souvislost s časem nebo uspořádáním, může nastat souběžně (paralelismus)
příbuznost k signálu (signál/událost nastane)
počet výskytů
abstraktní/neznámé entity
jen výčet/množina subjektů (neznáme je, pouze "že jsou")
v requirementu i v testu ověření, jestli jsou entity stejné ("stejné žluté krabičky", jejichž význam neznáme)
příklad: "maximum execution time measurement" nebo "Mode Enable"
reprezentace různých stavů nebo hodnot v různých časech (lineárně/logicky)
built-in kategorie (kategorie a vlastnosti, jejichž význam bude nástroj znát)
např. hodnoty, úložiště, pořadí, variace, podmínky/implikace

---

## Analyza obrazku - barevne kodovani

Barvy v obrazku:
- **zluta** = entity (registry, pameti, signaly, adresy, abstraktni entity)
- **modra** = RFC 2119 requirement levels (shall, must)
- **cervena** = transformace / operace nad entitami (calculate, difference, signed value, ...)
- **fialova** = akce/slovesa ktera formalismus musi rozumet (toggle, store, read, copy, invoke, hold, execute, transmit, configure, operate, perform)
- **zelena** = udalosti / podminky / casove vazby (write, when, after, if, returns, power-up, initialization, receive)

## Rozbor podle typu requirementu

### 1. Arithmetic/boolean operations
> The software function **shall** *calculate* the signal [EngagementNoSat_u] according to the following equation:
> [EngagementNoSat_u] = 1.2*[EngagementNoSat_u](k-1) if [Switch_b] is TRUE; [Lon_u] otherwise.
> Notes: The initial condition of [EngagementNoSat_u] is equal to 0 and (k) denotes a given time instant.

- entita: signal [EngagementNoSat_u], [Switch_b], [Lon_u]
- akce (fialova): calculate
- transformace: rovnice (equation), nasobeni (1.2*), indexovani v case (k-1)
- flow control: if ... otherwise (podmineny vyraz)
- predikat: is TRUE, is equal to
- konstanty: 0, 1.2
- pocatecni podminka (initial condition): initial condition ... is equal to 0
- casovy odkaz: (k) = time instant, (k-1) = predchozi casovy krok

**Nove kategorie:**
- **rovnice / matematicke vyrazy** — cela rovnice jako formalismus, vcetne operatoru (*, +, -)
- **pocatecni podminky / default hodnoty** — "initial condition is equal to 0"
- **casovy index (diskretni cas)** — (k), (k-1) — odkaz na hodnotu entity v konkretnim casovem kroku

### 2. Interface with hardware (NVM)
> The software **shall** *store* the maximum execution time measurement data in Non-Volatile Memory in the address region MEASUREMT_BLOCK.

- akce: store
- entita: maximum execution time measurement data, Non-Volatile Memory, address region MEASUREMT_BLOCK
- **adresovani** — "in the address region", "at the address" — zpusob odkazu na konkretni misto v pameti

### 3. Interface with hardware (CPU registers)
> The software **must** *perform* the following actions in the specified order:
> 1) Read the calibration constant value at the address 0xAA000018;
> 2) Store the calibration constant value in the DTSCON register.

- akce: perform, Read, Store
- entita: calibration constant value, address 0xAA000018, DTSCON register
- **usporadana sekvence kroku** — "the following actions in the specified order: 1) 2)" — explicitni cislovane poradi
- konstanty: 0xAA000018 (hex adresa)

### 4. Interrupt/exception handling
> The software **must** *configure* IVORx registers with the addresses of Exception Vectors that compose the Exception Vector Table, according to the following table:

- akce: configure
- entita: IVORx registers, Exception Vectors, Exception Vector Table
- **mapovani / tabulkova data** — "according to the following table: IVORx -> Exception" — definice vazeb klice-hodnota

### 5. Sequenced actions
> The software, when handling an exception, **must** *execute* the following steps in the following order:
> 1) Copy the value of register SRR0 to register R5.
> 2) Invoke the image exception handler.
> 3) If the exception handler returns, hold the software execution.

- akce: execute, Copy, Invoke, hold
- entita: register SRR0, register R5, image exception handler, software execution
- udalost/podminka: when handling an exception, returns
- flow control: if
- usporadana sekvence kroku: 1) 2) 3)
- **zdroj-cil (source-destination)** — "Copy value of X to Y" — smerovany presun dat

### 6. Scheduling
> The software **must** start to *execute* the sequence of tasks allocated to the execution schedule in less than 2 seconds after processor power-up.

- akce: start to execute
- entita: sequence of tasks, execution schedule, processor
- cas: less than 2 seconds (casovy limit)
- udalost: power-up
- poradi: after
- **casovy deadline / constraint** — "in less than 2 seconds" — omezeni typu "do X casu"

### 7. I/O processing
> The software, after its initialization, **shall** *transmit* the signal 'Mode Enable' with value TRUE through DDS Topic 'MODESET_TOPIC'.

- akce: transmit
- entita: signal 'Mode Enable', DDS Topic 'MODESET_TOPIC'
- udalost: initialization
- poradi: after
- konstanty/hodnoty: TRUE
- **komunikacni kanal** — "through DDS Topic" — medium/kanal pres ktery se data posilaji

### 8. State-machine logics
> The software **shall** *operate* as Backup when receive a new data instance of the datatype MastershipInfo, with parameter [Mastership_b] as BACKUP.

- akce: operate
- general behavior: operate as Backup
- udalost: receive a new data instance
- entita: datatype MastershipInfo, parameter [Mastership_b]
- konstanty: BACKUP
- **datove typy a parametry** — "datatype MastershipInfo, with parameter [Mastership_b]" — typovana data s pojmenovanymi parametry

### 9. Timed operations
> (jiz analyzovano vyse)

---

## Kompletni tabulka kategorii s priklady z obrazku

| Kategorie                                        | Priklad                                                                                                                                          | Poznamka |
| ------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------ | -------- |
| konstanty                                        | 0, 1.2, 655, 0xAA000018, TRUE, BACKUP                                                                                                            |          |
| jednotky                                         | ns, seconds                                                                                                                                      |          |
| poradi: pred/po                                  | after, before, when, in the specified order, in the following order                                                                              | automat  |
| pocet vyskytu                                    | second write to d                                                                                                                                | automat  |
| variace                                          |                                                                                                                                                  |          |
| cas: konstanta + jednotka                        | within 500 ns, in less than 2 seconds                                                                                                            |          |
| immediate hodnoty registru/pameti/signalu        | with value TRUE, calibration constant value, is equal to 0                                                                                       |          |
| hodnota registru/pameti/signalu menici se v case | [EngagementNoSat_u](k), signed value of d, value of last d                                                                                       |          |
| udalosti                                         | write, power-up, initialization, receive a new data instance, returns                                                                            |          |
| abstraktni entity                                | maximum execution time measurement data, Mode Enable, Exception Vector Table                                                                     |          |
| stav                                             | handling an exception, operate as Backup                                                                                                         |          |
| RFC 2119 - Requirement levels                    | must, shall                                                                                                                                      |          |
| musi-to-rozumnet (akce/slovesa)                  | toggle, calculate, store, read, copy, invoke, hold, execute, transmit, configure, operate, perform                                               |          |
| entita                                           | register SRR0, R5, DTSCON, IVORx, Non-Volatile Memory, address 0xAA000018, signal [EngagementNoSat_u], DDS Topic 'MODESET_TOPIC', valid_range, d |          |
| logicke spojky: ALL/ANY/NONE podminek            | ALL the following conditions, if ... otherwise                                                                                                   |          |
| transformace                                     | difference between, signed value, 1.2*, equation, (k-1)                                                                                          |          |
| predikaty                                        | is higher than, is equal to, is TRUE                                                                                                             |          |
| history of entity                                | last Maximum Peak, last d, (k-1)                                                                                                                 |          |
| general behavior                                 | software shall operate as Backup                                                                                                                 |          |
| flow control                                     | if ... otherwise, if the exception handler returns, when handling an exception                                                                   |          |
****