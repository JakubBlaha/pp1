---
id: s-test-semantics
kind: solution
title: Define a test case as the set of traces it allows
status: proposed
solves: test-set-of-traces
---
## Summary
Replace "a test case produces a concrete trace" by a definition of all the traces a test case allows.

## Change
In `formalism.tex`, Section "Requirements & Test cases", define

$$\mathit{Traces}(\mathit{TC}) = \{\, \rho \in \Sigma^T \mid \rho(0) \text{ agrees with } \sigma_0, \text{ and the effect of every stimulus holds in } \rho \,\}$$

and state that the assertions select the traces the test expects.

## Example
Req 10, TC2: traces in which `emergency_mode` becomes true at 9 s, at 20 s or never are all allowed; the assertion says the test expects it at 9 s.

## Affects
- all: the meaning of every test case
