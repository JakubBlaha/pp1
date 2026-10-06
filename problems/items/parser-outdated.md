---
id: parser-outdated
title: The parser implemented the old timing convention
parent: cat-parser
status: resolved
severity: major
found: 2026-10-05
ec: none
ec-why: Resolved; the parser now matches the formalism the translation starts from.
related: timing-convention, req13-outdated
caused-by: timing-convention
---
## Summary
The parser pinned the formalism from before the timing convention and still used $\mathit{ValBefore}$. Synced on 5 Oct 2026.

## Resolution
pp1-parser commits bffb021 (timing convention: Req 02, 03, 05, 07, 09 and the Req 10 tests) and be59f32 (Req 13).

## Affects
- Req 02: fixed
- Req 03: fixed
- Req 05: fixed
- Req 07: fixed
- Req 09: fixed
- Req 10: test assertions fixed
- Req 13: fixed
