---
id: s-examples-cleanup
kind: solution
title: Tidy the example notes and the Req 10 window
status: proposed
solves: future-extensions-missing, negative-window-start
---
## Summary
Small fixes to `examples.tex` that the translation does not need.

## Change
- Req 07, Req 08: replace the references to the missing "Future Extensions" section.
- Req 10: use the window $[0, \mathit{Now})$ for $\mathit{Now} < 10$ and $(\mathit{Now} - 10, \mathit{Now})$ otherwise.

## Affects
- Req 07: reference replaced
- Req 08: reference replaced
- Req 10: window start
