---
id: goal-ec-translation
kind: goal
title: Translate every requirement and test case into the Event Calculus
---
## Summary
The first goal of the project: every formalised requirement and test case can be translated, mechanically and faithfully, into an Event Calculus theory.

## What the translation produces
- **Requirement:** a closed first-order formula over `Happens(e, t)` and `HoldsAt(f, t)`.
- **Test case:** the event list (`Happens` facts for its stimuli), the initial values (`Initially` facts) and its assertions (`HoldsAt` queries).
- **Operations:** effect axioms (`Initiates`, `Terminates`); the software's events become choice rules.
- **Tools:** clingo for discrete requirements, s(CASP) for continuous ones.

## When it is reached
When no problem marked "blocks the translation" is unresolved, the translation rules are complete, and the translator exists.

## Sources
- `research/calculi.md`
