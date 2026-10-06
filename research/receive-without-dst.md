# Dropping the destination argument of `receive`

## The question

Today `formalism.tex` has `receive(t, c, dst)`: it copies the current value of channel `c` into a Signal `dst`. Both channel designs in `channels.md` replace it with `receive(t, c, v)`: a message with value `v` arrives on channel `c`, and the value stays on the channel until the next message. There is no `dst` any more.

Does any of our requirements need `dst`?

## Short answer

**No.** None of our requirements uses `dst`. Only Req 08 uses `receive` at all, and its formalisation reads the received value from the channel itself. Dropping `dst` also removes a hazard for coverage (see "When `dst` would matter" below).

## Scan of all requirements

| Req | What it is about | Uses channels? | Uses `receive`? | Uses `dst`? | Affected? |
|---|---|---|---|---|---|
| 01 | recurrence equation on Signals | no | no | no | no |
| 02 | store data in non-volatile memory | no (Storage) | no | no | no |
| 03 | read calibration constant, store in DTSCON | no (`read` on Storage) | no | no | no |
| 04 | configure IVOR registers | no | no | no | no |
| 05 | copy SRR0 to R5 on exception | no (`write` on Storage) | no | no | no |
| 06 | start tasks within 2 s of power-up | no | no | no | no |
| 07 | transmit Mode Enable on MODESET_TOPIC | yes | no (`transmit`) | no | no |
| 08 | enter Backup on receiving MastershipInfo = BACKUP | yes | yes | **no** | no, apart from `Val` → `ValAfter` (below) |
| 09 | toggle `valid_range` after a write to `d` | no | no | no | no |
| 10 | emergency mode after repeated failures | no | no | no | no |
| 11 | counter after emergency mode | no | no | no | no |
| 12 | read A and B, enter emergency mode | no (`read`) | no | no | no (not formalised yet) |
| 13 | count large register values when read | no (`read`) | no | no | no |

**Req 08 in detail.**

> The software shall operate as Backup when it receives a new data instance of *MastershipInfo* with parameter *Mastership_b* equal to BACKUP.

```
Entities: MastershipInfo (Channel), ev_received_mastership (Event: received),
          Backup (State), ev_entered_backup (Event: entered)
Causes( Happening(ev_received_mastership, Now) ∧ Val(MastershipInfo, Now) = BACKUP,
        Happening(ev_entered_backup, Now) )
```

No destination Signal is declared. The received value is read straight from the channel, `Val(MastershipInfo, Now)`. Without `dst` this still works.

The one change Req 08 needs comes from the timing convention, not from dropping `dst`. With `receive(t, c, v)` the message *sets* the channel's value, and a new value is visible only after `t`. So the condition must read `ValAfter(MastershipInfo, Now) = BACKUP` (also noted in `findings.md`).

## How a requirement refers to a received value without `dst`

- **The value of the message received now:** `ValAfter(c, Now)` at a `received` event on `c`.
- **The value of an earlier message:** `ValAfter(c, Start(LastOcc(ev_received_c, Now, n)))`, i.e. the value just after the n-th last reception.

Both are already in the formalism.

## When `dst` would matter, and why dropping it helps

A requirement could ask the software to *keep* a received value, for example (hypothetical, not one of ours):

> When the software receives MastershipInfo, it shall store Mastership_b in the variable `current_mastership`.

**With `dst`**, a test would write this as the stimulus `receive(1, MastershipInfo, current_mastership)`. The stimulus's own effect then copies the value into `current_mastership`. So the test itself performs the software's job: the requirement looks exercised and satisfied in every trace, without the test checking anything. This breaks the coverage rule in `CLAUDE.md`: what the software does must come from the test's assertions, not from its stimuli.

**Without `dst`**, the copy is software behaviour, stated in the requirement:

```
Always( Happening(ev_received_mastership, Now) ⇒
        ValAfter(current_mastership, Now) = ValAfter(MastershipInfo, Now) )
```

A test now covers this only if it sends the message *and* asserts the value of `current_mastership` afterwards. That is the behaviour we want.

## When `dst` would help

There are three situations. None of them adds expressive power we do not already have, and the deciding question is whether the **test** or the **software** performs the operation.

**1. Shorter formulas when the software does the read.** `dst` is a shorthand for "the source's value at the last read". Req 03 today:

```
ValAfter(DTSCON, Now) = Val(calibration_const, Start(LastOcc(ev_read_cc, Now, 1)))
```

With a `dst` filled by the software's read, `read(t, calibration_const, cc_value)`:

```
ValAfter(DTSCON, Now) = Val(cc_value, Now)
```

The second version is closer to the wording "store the value that was read", but equivalent.

**2. Naming a real variable that tests observe.** If the software keeps the received value in a variable that tests can inspect, `dst` records that the reception fills it. A constraint in the requirement, as in the example above, says the same.

**3. Messages that are consumed when received.** Our channel keeps its value until the next message, like an ARINC 653 *sampling* port. With *queuing* ports, the software takes the message out of the queue, and the channel no longer holds it. A requirement such as "execute the command contained in the received message after the current task" then needs the value kept somewhere: in a `dst`, or through a way to read the payload of the reception event. None of our requirements needs queuing semantics today.

**Rule.**
- **In a stimulus, `dst` is harmful:** it makes the test perform the software's copy.
- **In an operation performed by the software, `dst` is harmless:** it is a shorthand.

So `receive` should have no `dst` in either channel design, because it is always a stimulus (the tester sends). `read` may keep it, because reading is the software's action.

## Related observations (not caused by dropping `dst`)

- **Structured payloads.** Req 08 speaks of a *data instance* with a *parameter* `Mastership_b`, and Req 07 of a *signal* Mode Enable sent on a topic. A channel holds one value, so the formalisations compare the whole channel value with `BACKUP` or `TRUE`. If a message has several fields, we would need record values, which `V_base` does not have. `dst` did not solve this either.
- **`read` has the same shape.** `read(t, src, dst)` copies a Storage into a Signal. Req 03, 12 and 13 use `read` events, but their formalisations never use `dst` either: Req 03 compares `DTSCON` with the value of `calibration_const` at the time of the read. Reading is normally the software's action, not a test stimulus, so the hazard above is less likely here. Still, `read` and `receive` should be decided consistently.
- **Text to update in `formalism.tex` when the change is applied:**
  - The list of value-modifying operations says "the destination side of `read` and `receive`". With the new `receive`, the message modifies the channel itself.
  - The `receive` row of the operations table.
  - Req 08 in `examples.tex`, which needs `ValAfter`.

## Conclusion

Dropping `dst` from `receive` costs nothing for our requirements. Only Req 08 uses `receive`, it does not use `dst`, and its only change, `Val` → `ValAfter`, comes from the timing convention. Dropping `dst` also prevents a test from performing the software's "store the received value" step through its own stimulus.
