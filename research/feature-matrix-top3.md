# Feature matrix: the three best candidates

This is `feature-matrix.md` filtered to the three columns that cover the most features: the **Event Calculus** (38 of 41), **SVA / PSL** (34) and **Lola / TeSSLa** (33). The next ones would be Lustre and UPPAAL (32 each) and Event-B / Z / TLA+ (31).

Rows, cell notes and the counting are the same as in `feature-matrix.md`. An empty cell means the formalism does not cover the feature; many cells describe an encoding rather than a built-in operator.

| Feature | Needed for | Event Calculus | SVA / PSL | Lola / TeSSLa |
|---|---|---|---|---|
| **Time and data** |  |  |  |  |
| Discrete time | Req 01, 03, 05, 13 | discrete EC (DEC) | clock cycles | Lola: synchronous steps |
| Continuous time | Req 06, 09, 10 | continuous EC (Shanahan) |  | TeSSLa: real time stamps |
| Real-valued data, arithmetic | Req 01, 09, 13 | FO terms (ASP: integers, s(CASP): reals) | bit vectors, integers | native |
| Enumerated values | Req 08 (`BACKUP`) | constants of a sort | `typedef enum` |  |
| Undefined values | Req 02 (register before first write) | no `value(e)=_` fluent holds | 4-state values (`X`), `$isunknown` | default `x[-1, d]`; TeSSLa: no event |
| Static entity attributes | Req 03, 04 (`address`, `register`) | static facts `address(e, a)` | parameters | constants |
| Set values and set operations | Req 13 (`Size`, `Filter`) | fluents `member(s, x)`; ASP `#count` | arrays, `inside` | TeSSLa: `Set` type |
| **Events** |  |  |  |  |
| Instantaneous events | all | `Happens(e, t)` | `$rose(x)` (SVA), `rose(x)` (PSL) | event streams |
| Event with payload | Req 07, 08 | event term argument `transmit(c, v)` | signal values at the edge | event stream with values |
| **Looking back and forward** |  |  |  |  |
| Previous value (`Prev`) | Req 01, Req 11 | `HoldsAt(f, t−1)` | `$past(x)` (SVA), `prev(x)` (PSL) | `x[-1, d]`, `last` |
| Value just after (`ValAfter`) | Req 03, 05, 07, 09 | DEC: `HoldsAt(f, t+1)` | `\|=>`, `##1` (SVA), `next` (PSL) | Lola future offset `x[1, d]` |
| Value at another named time point | Req 09 (`Val(d, t_Mpd)`) | `HoldsAt(value(x)=v, t')` | sequence-local variables (SVA) | `last(x, trigger)` |
| Time of n-th last / first occurrence | Req 03, 09 (`LastOcc`) | `Happens(e, t1)` with none in between | goto repetition `[->n]` | `time(e)` with `last` |
| Has happened so far | Req 11 | fluent `happened(e)` | auxiliary flag | latch stream |
| Count occurrences in a window | Req 09, 10 (`EvtOccCount`) | fixed n: n existentials; any n: `#count` | `[=n]`, `[->n]` in a cycle window | counter stream |
| Max / min over a window | Req 09 (peaks) | FO, or `#max` in ASP | sequence-local variable | running max stream |
| Time arithmetic, open / closed bounds | Req 09, 10 | arithmetic on time terms | cycle ranges `##[m:n]` | TeSSLa: `time(x) − time(y)` |
| Interval relations | `IntervalIncludes`, `IntervalExcludes` | arithmetic on endpoints |  |  |
| **Temporal constructs** |  |  |  |  |
| `Always` | Req 01, 11, 13 | `∀t` | `assert property (p)` | output `ok` true at every step |
| `Eventually` | Req 02, 04 | `∃t` | `s_eventually` (SVA) | verdict at the end of the trace |
| `Initial` | Req 01 | `Initially`, `HoldsAt(f, 0)` | reset / initial block | default value |
| `Causes` (response) | Req 05, 07, 08, 10 | FO over `t` | `a \|-> s_eventually b` | verdict at the end of the trace |
| `CausesWithin`, incl. strict bound | Req 06, 09 | `∃t' (t ≤ t' ≤ t+d)` | `a \|-> ##[0:d] b` | timeout stream (TeSSLa `delay`) |
| `Immediately` (next step) | construct `Immediately` | `HoldsAt(…, t+1)` | `a \|=> b` | offset `[1]` |
| `Precedes` | construct `Precedes` | FO over `t` | auxiliary flag | latch stream |
| `Excludes` | construct `Excludes` | `∀t ¬(…)` | `assert property (!(a && b))` | stream `not (a and b)` |
| `Sequence` (existential) | Req 03, 05 | `∃t1 ≤ … ≤ tn` | `cover property (a ##[1:$] b)` | state stream |
| Triggered sequence (chain response) | Req 05 (missing construct) | FO over `t` | `t \|-> ##[1:$] s1 ##[1:$] s2` | state stream |
| Scopes (after init, between …) | Req 07 | FO over `t` | PSL `until`, `before`; SVA `disable iff` | latch stream |
| **Operations and state** |  |  |  |  |
| Operations with effects on values | `write`, `calculate`, `set_state`, … | `Initiates` / `Terminates` |  |  |
| Persistence until next change | `(t, t_next]` clause | law of inertia |  | `last` holds the value |
| Values the software changes without an operation | Req 01, 11 (`calculi.md` §3.1) | `ReleasedAt`, or open system events | free design signals | input streams |
| Channels: send / receive a value | Req 07, 08 | event terms `transmit(c, v)`, `receive(c, v)` |  | event stream per channel |
| Stimulus vs software-controlled | `findings.md`, `channels.md` | stimulus events closed, system events open (choice rules) | `assume` vs `assert` property |  |
| **Requirements, tests, coverage** |  |  |  |  |
| Near-natural-language vocabulary | goal 1 (LLM output) |  |  |  |
| Requirement = predicate over a trace | `ρ ⊨ R` | closed FO formula | `assert property` | specification over a trace |
| Test case: setup, stimuli, assertions | goal 2 | `Initially` + event list + `HoldsAt` queries | (testbench, outside SVA) |  |
| Expected absence of a response | Req 10 TC1, TC3, TC5–TC7 | `¬∃t. Happens(e, t)` | `!e throughout` a window | stream `not e` |
| Requirement ↔ test traceability | goal 3 |  |  |  |
| Coverage of requirement conditions | goal 3 |  | `cover property`, PSL `cover` |  |
| Checker on concrete finite traces | goal 3 | DEC reasoner, clingo, s(CASP), RTEC | simulators, formal tools | Lola, TeSSLa evaluators |
| **Features covered** | of 41 | 38 | 34 | 33 |

**Not covered by any of the three:** near-natural-language vocabulary and requirement ↔ test traceability. In the full matrix these come from the requirement and test languages (FRET, EARS, Gherkin, Simulink Requirements Table, SysML v2, ETSI TDL).

## This matrix shows coverage, not translatability

**The difference.** A filled cell means "this feature can be expressed in that formalism *on its own*". Translating our formalism needs more than that: all features must work **together** in one target language, and the translation must keep the meaning. The matrix does not check that.

**Example: Req 09 and SVA / PSL.** Req 09 needs:
- continuous time (500 ns);
- the value of `d` at an earlier time point;
- counting writes in a window;
- open and closed bounds;
- `ValAfter`.

In the SVA / PSL column every one of these cells is filled except continuous time. SVA and PSL only know clock cycles. So the column looks almost complete, yet Req 09 cannot be translated to SVA / PSL at all.

**Three reasons why the counts overstate translatability:**

1. **Some columns are two languages.** "SVA / PSL" and "Lola / TeSSLa" each merge two languages. In the Lola / TeSSLa column, the `ValAfter` cell comes from Lola (future offsets) and the continuous-time cell from TeSSLa (real time stamps). A requirement that needs both is not covered by either language alone. A translation has to pick one.
2. **Many cells are hand-made encodings.** "Auxiliary flag", "latch stream" and "counter stream" mean that someone writes an extra flag or stream for that particular formula. A translation needs a *general* recipe that produces these for any formula. For past-time features such recipes are well known (they are how runtime monitors are built), but for each target it still has to be worked out and checked.
3. **Some cells change the meaning slightly.** The changes are:
   - **End-of-trace verdicts:** "verdict at the end of the trace" (Lola for `Eventually` and `Causes`) turns "eventually" into "before the test ends".
   - **Fixed counts only:** "fixed n" (Event Calculus counting) only works when the count is a constant.
   - **Our deeper rules aren't modelled:** our timing convention `(t, t_next]`, undefined values, and test cases as *sets of traces* (`findings.md`). The matrix doesn't show these mismatches, because no single feature cell captures them.

**What has been checked so far.** Only the Event Calculus was analysed for translatability, construct by construct, in `calculi.md`. That analysis found two real mismatches (values that change without an operation, and counting/sets), both with known fixes. The Event Calculus is also the only candidate that, like our formalism, quantifies freely over time points in first-order logic. That makes a direct translation plausible.

For SVA / PSL and Lola / TeSSLa nothing comparable has been done. Based on the points above:
- **SVA / PSL:** not a translation target for the continuous-time requirements (Req 06, 09, 10). Even for discrete time, our first-order quantification over time points would need restricting to what SVA's sequences and local variables can express (see the example below).
- **Lola / TeSSLa:** a plausible target for *checking concrete finite test traces*, the job of the coverage checker, once one language is chosen. Not for representing a test case as a set of traces.

### Example: "first-order quantification over time points"

**The idea.** In our formalism a predicate can name *any* time point in the trace, for example "the time of the last maximum peak", and compare values at those points. Underneath, such a time point is defined by quantifying over all time points ("the largest `s ≤ Now` at which the event happened"). In SVA an assertion cannot name time points. It only moves forward cycle by cycle from where it starts, or looks back a *fixed* number of cycles with `$past(x, n)`.

**Req 09, first condition:**

> The difference between the last Maximum Peak and the last Minimum Peak of `d` is higher than 655.

Ours (from `examples.tex`, evaluated at a write to `d`):

```
t_Mpd = Start(LastOcc(ev_max_peak_det, Now, 1))     -- time of the last maximum peak
t_mpd = Start(LastOcc(ev_min_peak_det, Now, 1))     -- time of the last minimum peak
Val(d, t_Mpd) − Val(d, t_mpd) > 655
```

`t_Mpd` and `t_mpd` can be any number of steps back, and either can come first.

In SVA this cannot be written inside the assertion:
- `$past(d, n)` needs a constant `n`, but the number of cycles since the last peak varies.
- A sequence-local variable can store `d` when a peak happens, but only if the sequence *starts* at that peak and walks forward to the write. Here the assertion is triggered by the write, and the two peaks lie behind it in an unknown order.

The usual workaround is helper code outside the assertion: two registers that remember `d` at each peak, written by hand for this requirement.

```systemverilog
always @(posedge clk) begin
  if (max_peak_det) last_max <= d;
  if (min_peak_det) last_min <= d;
end
assert property ((write_d && last_max - last_min > 655) |-> ##[0:N] toggle_valid_range);
```

**What "restricting" means.** A translation to SVA would only work for requirements whose time points are either:
- a fixed number of cycles from now, or
- reached by walking forward from the trigger in a known order.

Everything else, like Req 09, needs hand-written helper code. In the Event Calculus the same condition stays a direct formula, because time points are ordinary variables:

```
Happens(max_peak_det, t1) ∧ Happens(min_peak_det, t2) ∧ t1 ≤ t ∧ t2 ≤ t
∧ (no later peak of either kind before t)
∧ HoldsAt(value(d)=v1, t1) ∧ HoldsAt(value(d)=v2, t2) ∧ v1 − v2 > 655
```

**Conclusion.** Read the three columns as *candidates worth investigating*, not as *targets we can translate to*. To decide translatability for SVA / PSL or Lola / TeSSLa, we would need the same construct-by-construct mapping as `calculi.md` does for the Event Calculus.
