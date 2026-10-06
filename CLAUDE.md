# Working rules for this repo

## Explanation style

Explain things in plain language:

1. State the difference or idea in one sentence.
2. Show one concrete example.
3. Give the fix or conclusion.

Use a small table only to summarise. Keep the pieces short.

The reader knows what theories, first-order logic and propositional logic are, but not specialist terms (frame rule, fluent, left limit, circumscription, …). Introduce such a term only with a one-line plain definition, and lead with the example rather than the formalism.

- The reader is familiar with the concepts of EC
- The generated text needs to read easily.

This applies to chat explanations and to the documents in `research/`.

## The goal is coverage, not satisfaction

The formalism exists to check whether test cases **cover** a requirement: does some test exercise each part of it? It does not exist to decide whether the software **satisfies** the requirement. Judge every proposed change by the coverage question.

- What the test controls (stimuli, setup) decides which conditions of a requirement are made true.
- What the software or hardware does comes from the test's assertions (its expected outcomes). Checking those outcomes is the job of running the test, not of the formalism.
- So the formalism does not need to model the behaviour of the software or the hardware. A requirement that "can never be false in the model" is not a problem as long as a test can exercise it.

Example of the mistake: Req 02 says the stored value survives a reset. We noticed that nothing in the formalism makes a reset clear memory, so the requirement held even for volatile memory, and we added a rule for what a reset does. That answered a satisfaction question. For coverage, the checker only needs to see that a test fires a reset and asserts the value afterwards. The rule was reverted (see `research/findings.md`, "A reset has no effect on storage").

Before adding semantics to the formalism, ask: does the coverage checker need this to decide which tests exercise which conditions? If not, don't add it.

## Problem tree

Every problem found in the formalism, the examples, the test cases, the Event Calculus translation or the parser is tracked in `problems/` and shown by the web app `problems/index.html`. The format is described in `problems/README.md`.

- **A new problem is found:** use the `add-problem` skill (`.claude/skills/add-problem/SKILL.md`). In short: add a file to `problems/items/` in the same turn. List every affected requirement and test case, link its causes (`caused-by`), state whether it is in the way of the Event Calculus translation (`ec`: blocker, work, tooling or none) and why (`ec-why`), and propose at least one solution: a new solution file, or an existing solution extended with `solves`.
- **The first goal is the translation to the Event Calculus.** The app's start page shows what blocks it; keep `ec` and `ec-why` accurate when a problem changes.
- **A problem is fixed, or turns out not to be one:** update its status (and the solution's). Do not delete it.
- **After every change:** run `python3 problems/build.py`. It must finish without errors and without "no proposed solution" warnings.
- Write problems and solutions in the explanation style above.

## Files

Never overwrite an existing file when asked to create a document. Check the path first; if it has content, write a new file.
