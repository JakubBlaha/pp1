---
id: ec-undecidable
title: Symbolic reasoning over continuous time is undecidable
parent: cat-ec
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: Concerns reasoning over the translated theories, not the translation itself.
related: ec-tools-reals, only-if-gap
---
## Summary
Our logic is at least as expressive as TPTL, whose satisfiability over continuous time is undecidable. Checking concrete, finite test traces is not affected.

## Explanation
This matters only if coverage has to be *proven* over all traces of a test, rather than evaluated. If the conditions are decided from the test's own stimuli (see "Events happen when the test fires them, but not only then"), the relevant part of the trace is fully known and can simply be evaluated.

## Affects
- Req 06: continuous time
- Req 09: continuous time
- Req 10: continuous time

## Sources
- `research/related-formalisms.md`, §2 (TPTL)
