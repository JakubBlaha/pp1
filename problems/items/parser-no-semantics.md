---
id: parser-no-semantics
title: The parser checks types, not meaning
parent: cat-parser
status: open
severity: medium
found: 2026-10-06
ec: none
ec-why: The translator can be built next to the parser's type checker; it does not depend on this.
related: d-signal-write, coverage-undefined, valafter-pitfall
---
## Summary
The parser validates types but does not evaluate traces or coverage, so a well-typed test that misses its requirement goes unnoticed.

## Explanation
**Example (Req 09).** A test that sets `d` with `calculate` is accepted, but it never makes `ev_written_d` happen, so it never exercises Req 09.

## Proposed fix
Build the trace evaluator and the coverage checker (goal 3) on top of the parser.

## Affects
- Req 09: a test using `calculate` on `d` is accepted
