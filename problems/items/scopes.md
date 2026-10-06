---
id: scopes
title: No scopes such as "after Q" or "between Q and R"
parent: cat-constructs
status: open
severity: minor
found: 2026-10-03
ec: none
ec-why: Scopes are encoded with existing constructs, which translate.
related: chain-response, software-only-conditions
---
## Summary
Specification patterns come with scopes. We encode them by hand with $\mathit{Causes}$ or $\mathit{HasHappened}$.

## Explanation
Dwyer's patterns have five scopes: *Globally*, *Before R*, *After Q*, *Between Q and R* and *After Q until R*. "After its initialisation" (Req 07) is the scope *After Q*. The Custom Counter (Req 11) uses $\mathit{HasHappened}$ as its antecedent for the same purpose.

## Proposed fix
Add a scope argument to the temporal constructs.

## Affects
- Req 07: "after its initialisation"
- Req 11: "after the system enters emergency mode"

## Sources
- `research/related-formalisms.md`, §6
