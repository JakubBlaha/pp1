---
id: s-ec-timing
kind: solution
title: Adopt the Event Calculus timing convention
status: applied
solves: timing-convention, req10-tests-instant, parser-outdated
---
## Summary
Effects hold on $(t, t_{\mathit{next}}]$, and $\mathit{ValAfter}_\rho$ replaces $\mathit{ValBefore}_\rho$. Applied on 3 Oct 2026 (pp1 commit 50d4b25) and synced to the parser on 5 Oct 2026 (bffb021).

## Affects
- Req 02: uses $\mathit{ValAfter}_\rho$
- Req 03: uses $\mathit{ValAfter}_\rho$
- Req 05: uses $\mathit{ValAfter}_\rho$
- Req 07: uses $\mathit{ValAfter}_\rho$
- Req 09: uses $\mathit{ValAfter}_\rho$
- Req 10: test assertions use $\mathit{ValAfter}_\rho$
