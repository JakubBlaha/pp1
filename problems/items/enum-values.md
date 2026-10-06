---
id: enum-values
title: Enumerated values are not part of the value set
parent: cat-time
status: open
severity: medium
found: 2026-10-03
ec: blocker
ec-why: The translation has to declare `BACKUP` as a constant of some sort, and the formalism has no such sort yet.
related: structured-payloads
---
## Summary
Req 08 compares a channel's value with `BACKUP`, but the formalism has no enumeration values.

## Explanation
$V_{\text{base}}$ contains booleans, reals, time points and intervals only. `examples.tex` marks this with a TODO ("Need to add enum values"). The parser works around it by declaring `BACKUP` as an entity of type `Value`.

## Proposed fix
Add enumerated types to $V_{\text{base}}$, or adopt the parser's approach (a `Value` entity per constant) in `examples.tex`.

## Affects
- Req 08: the constant `BACKUP`

## Sources
- `tex-new/examples.tex`, Req 08
- `pp1-parser/examples/08.py`
