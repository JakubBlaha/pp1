---
id: s-ec-spec
kind: solution
title: Write the complete translation rules
status: proposed
solves: ec-rules-incomplete
needs: s-test-semantics, s-controlled-by, s-ec-open-events, s-undefined-rule, s-state-model, s-intervals, s-ec-aggregates, s-channel-design-b
---
## Summary
Turn the construct-by-construct mapping in `research/calculi.md` §2 into a complete specification, once the decisions it depends on are made.

## Change
1. One rule per construct of the formalism, including intervals, counting (rewritten for fixed bounds) and set functions.
2. The rules for test cases: stimuli become `Happens` facts, the setup `Initially` facts, the assertions `HoldsAt` queries; the software's events become choice rules.
3. The encoding of discrete time (DEC) and continuous time (s(CASP)).
4. One worked translation for each of Req 01–13.

## Trade-offs
Assumes channel design B; with design A only the rules for messages change.

## Affects
- all: defines the translation of every requirement
