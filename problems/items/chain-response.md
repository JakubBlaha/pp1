---
id: chain-response
title: No construct for "every trigger is followed by a sequence"
parent: cat-constructs
status: open
severity: medium
found: 2026-10-03
ec: none
ec-why: What is written translates; the missing construct is a gap in the formalisation.
related: scopes
---
## Summary
$\mathit{Sequence}$ only requires the steps to happen once, somewhere in the trace. Req 05 needs *every* exception to trigger them.

## Explanation
$$\mathit{Sequence}(\psi_1, \ldots, \psi_n) \Leftrightarrow \exists t_1 \le \cdots \le t_n:\ \psi_i(\rho, t_i) \text{ for all } i$$

Dwyer's *Chain Response* pattern is the missing construct:

$$\mathbf{G}\bigl(\mathit{exception} \rightarrow \mathbf{F}(\mathit{write\_R5} \land \mathbf{F}\,\mathit{invoke\_ieh})\bigr)$$

## Proposed fix
Add a triggered-sequence construct, for example $\mathit{TriggeredSequence}(\psi_{\mathit{trigger}}, \psi_1, \ldots, \psi_n)$.

## Affects
- Req 05: every exception must trigger the steps

## Sources
- `tex-new/examples.tex`, Req 05 notes
- `research/related-formalisms.md`, §6
