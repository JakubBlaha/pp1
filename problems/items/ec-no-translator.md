---
id: ec-no-translator
title: No translator exists yet
parent: cat-ec
status: open
severity: major
found: 2026-10-06
ec: work
ec-why: The last step: a program that turns the parser's JSON into EC theories.
related: parser-no-semantics
caused-by: ec-rules-incomplete
---
## Summary
Nothing turns a formalised requirement or test case into an Event Calculus theory yet.

## Explanation
The parser already produces typed JSON for every example (`pp1-parser`). A translator would read it and write:
- for each requirement, a closed first-order formula over `Happens` and `HoldsAt`;
- for each test case, the event list (`Happens` facts for the stimuli), the initial values (`Initially` facts) and the assertions (`HoldsAt` queries);
- the effect axioms of the operations, and choice rules for the software's events.

Discrete requirements go to clingo (DEC encoding), continuous ones to s(CASP).

## Proposed fix
Write the translator in `pp1-parser`, following the completed rules.

## Affects
- all: no requirement is translated yet

## Sources
- `research/calculi.md`, §2 and §5
