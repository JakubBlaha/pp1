---
name: add-problem
description: Record a newly found problem (in the formalism, the examples, the test cases, the Event Calculus translation or the parser) in the problem-tree web app under problems/, with its affected requirements and tests, its causes, its effect on the Event Calculus translation and at least one solution. Use it whenever a problem is found during work on pp1, or when the user asks to add, record or track a problem.
---

# Add a problem to the problem tree

The problem tree lives in `problems/`: one Markdown file per item in `problems/items/`, compiled by `python3 problems/build.py` into `problems/data.js`, which `problems/index.html` displays. The full file format is in `problems/README.md`.

Do every step in the same turn in which the problem was found.

## 1. Check that it is a new problem, and one that matters

1. Search for an existing item that already covers it:
   ```bash
   grep -il "<keyword>" problems/items/*.md
   grep -h "^title:" problems/items/*.md
   ```
   If one covers it, extend that file instead (add Affects lines, an example, or a sub-problem with `parent:` set to it). Do not create a duplicate.
2. Ask the coverage question from `CLAUDE.md`: does the coverage checker, or the translation to the Event Calculus, need this fixed? A question about whether the software *satisfies* a requirement is not a problem for the formalism. If unsure, say so to the user before adding it.

## 2. Collect the facts

- **Categories** (the possible top-level parents): `grep -H "^title:" problems/items/cat-*.md`
- **Requirements:** `Req 01` … `Req 13`; texts in `req/*.md`, formalisations in `tex-new/examples.tex`.
- **Test case ids:** `grep -Ho "^TC[0-9]*)" req/*.md` (plus `TC_MISSING` where a requirement has one).
- **Possible causes and related problems:** problems this one follows from become `caused-by`.
- **Solutions:** `grep -H "^title:\|^status:\|^solves:" problems/items/s-*.md`

Check every affected requirement and test case yourself, by reading its formalisation and its tests. List each one, not only the first you find.

## 3. Write the problem file

Create `problems/items/<id>.md`. The id is short kebab-case and equals the file name.

```markdown
---
id: <id>
title: <the problem as a short statement, e.g. "receive does not fix what is received">
parent: <category id, or the id of the problem this one is part of>
status: open
severity: major | medium | minor
found: <today, YYYY-MM-DD>
caused-by: <problem ids this follows from, comma-separated; omit if none>
related: <other problem ids worth reading; omit if none>
ec: blocker | work | tooling | none
ec-why: <one sentence: why it does, or does not, stand in the way of the Event Calculus translation>
---
## Summary
<One or two sentences: the problem.>

## Explanation
<The idea in one sentence, then one concrete example from a real requirement or test.>

## Proposed fix
<What to change, in a few lines. Point to the solution item.>

## Affects
- Req 09: <how Req 09 is affected>
- Req 10 / TC3: <how test case TC3 of Req 10 is affected>
- all: <for a problem that concerns every requirement>

## Sources
- `research/<file>.md`, "<section>"
```

Field rules (the build rejects anything else):

| Field | Values |
|---|---|
| `status` | `open` (no agreed fix yet), `decision` (the options are known; the team has to choose), `proposed` (a fix is proposed and ready to apply). A new problem is almost always `open` or `decision`. |
| `severity` | `major`: requirements or tests mean the wrong thing, or a project goal is blocked for many requirements. `medium`: a few requirements, or a workaround exists. `minor`: one place, naming, housekeeping. |
| `ec` | `blocker`: some requirement or test case cannot be written in the Event Calculus until this is decided. `work`: something the translator has to do or be built for. `tooling`: needed to run the translated theories, not to write them. `none`: the translation can be written without solving it. |
| `ec-why` | Required. One sentence. For `none`, say why the translation does not need it. |
| Affects | One line per requirement or test: `- Req NN: note`, `- Req NN / TCn: note`, `- all: note`, or `- none` if no current requirement is affected. |

Other section names are free ("Decision needed", "Trade-offs", …). Summary, Affects and Sources are read specially.

**Writing style** (from `CLAUDE.md`): state the idea in one sentence, show one concrete example, then the fix. Plain language. The reader knows first-order logic and the Event Calculus but not other specialist terms; define such a term in one line if you need it.

**Formulas:** `$...$` inline and `$$...$$` on their own line, rendered by KaTeX. Use only standard commands (`\mathit{Val}_\rho`, `\forall`, `\land`, `\text{...}`, …), never macros defined in the `.tex` files. Write identifiers as `\mathit{Name}`, and code or entity names in backticks.

## 4. Give it at least one solution

Every unresolved problem needs a solution that is not rejected; the build warns otherwise.

- **An existing solution fixes it:** add the id to that solution's `solves:` (or `partly-solves:`) list, and add an Affects line there if the solution changes another requirement.
- **Otherwise:** create `problems/items/s-<name>.md`:

```markdown
---
id: s-<name>
kind: solution
title: <the change, as an imperative, e.g. "Record who controls each entity">
status: proposed
solves: <id>
partly-solves: <ids it fixes only in part; omit if none>
needs: <solution ids that must be applied first; omit if none>
alternative-to: <competing solution ids; omit if none>
---
## Summary
<One or two sentences: what changes.>

## Change
<What exactly changes, and where: formalism.tex section, examples.tex requirement, parser file.>

## Example
<The example from the problem, after the change.>

## Affects
- Req NN: <what changes for it>
```

Use `status: decision` for a solution that is one of several alternatives the team must choose between, and link the alternatives both ways with `alternative-to`.

If the new problem is the cause of problems that already exist, add its id to their `caused-by` too.

## 5. Build and check

```bash
python3 problems/build.py
```

It must finish without errors and without "no proposed solution yet" warnings. Fix and rerun until it does. It checks the field values, the references (`parent`, `caused-by`, `solves`, `needs`, …), cycles, and the requirement and test ids in Affects.

Then check that the formulas parse, if Node.js is available:

```bash
npm install --prefix /tmp/pp1-katex katex@0.16.11      # once
NODE_PATH=/tmp/pp1-katex/node_modules node .claude/skills/add-problem/check_formulas.js problems/data.js
```

It must report `0 failed`. Without Node.js, open the problem in the app instead: a formula KaTeX cannot parse is shown in red.

## 6. Report

Tell the user, in a few lines:
- the title and file (`problems/items/<id>.md`) and the link `problems/index.html#/p/<id>`;
- the affected requirements and tests;
- whether it blocks the Event Calculus translation (`ec`) and why;
- the solution you linked or created.

Do not commit unless the user asks.
