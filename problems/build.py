#!/usr/bin/env python3
"""Build ``problems/data.js`` for the problem-tree viewer (``problems/index.html``).

Sources:
  problems/items/*.md    one file per category, problem or solution (format: problems/README.md)
  tex-new/examples.tex   requirement formalisations: text, entities, constraint, notes
  req/*.md               the stakeholders' original requirement texts and test cases

Usage:  python3 problems/build.py
Only the standard library is used. The build stops with a list of errors if a
problem file is malformed or refers to an unknown problem, requirement or test.
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
ITEMS_DIR = HERE / "items"
EXAMPLES_TEX = ROOT / "tex-new" / "examples.tex"
REQ_DIR = ROOT / "req"
PARSER_EXAMPLES = ROOT / "pp1-parser" / "examples"
OUT = HERE / "data.js"

STATUSES = ("open", "decision", "proposed", "resolved", "closed")
SOLUTION_STATUSES = ("proposed", "decision", "applied", "rejected")
UNRESOLVED = ("open", "decision", "proposed")
EC_IMPACT = ("blocker", "work", "tooling", "none")
SEVERITIES = ("major", "medium", "minor")
REQ_IDS = [f"Req {n:02d}" for n in range(1, 14)]
REQ_FILES = {f"Req {n:02d}": f"{n:02d}.md" for n in range(1, 11)}
REQ_FILES.update({"Req 11": "11.custom.md", "Req 12": "12.custom.md", "Req 13": "13.custom.md"})
PARSER_FILES = {f"Req {n:02d}": f"{n:02d}.py" for n in range(1, 14)}
PARSER_FILES["Req 11"] = "00.py"  # the Custom Counter
TITLES_WITHOUT_FORMALISATION = {"Req 12": "Register sum triggers emergency mode"}

errors: list[str] = []
warnings: list[str] = []


def id_list(value: str) -> list[str]:
    return [x.strip() for x in value.split(",") if x.strip()]


# ---------------------------------------------------------------------------
# Problem files
# ---------------------------------------------------------------------------

AFFECTS_RE = re.compile(r"^-\s+(all|Req \d{2})(?:\s*/\s*([A-Za-z0-9_]+))?\s*:\s*(.*)$")


def parse_item(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        errors.append(f"{path.name}: missing '---' front matter")
        return None
    meta: dict[str, str] = {}
    for line in m.group(1).splitlines():
        if line.strip():
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip()

    sections: list[tuple[str, list[str]]] = []
    for line in m.group(2).splitlines():
        heading = re.match(r"^## (.+?)\s*$", line)
        if heading:
            sections.append((heading.group(1).strip(), []))
        elif sections:
            sections[-1][1].append(line)
    named = {title.lower(): "\n".join(lines).strip() for title, lines in sections}

    item = {
        "id": meta.get("id", ""),
        "kind": meta.get("kind", "problem"),
        "title": meta.get("title", ""),
        "short": meta.get("short", ""),
        "order": int(meta.get("order", "0") or 0),
        "parent": meta.get("parent", ""),
        "status": meta.get("status", ""),
        "severity": meta.get("severity", ""),
        "found": meta.get("found", ""),
        "related": id_list(meta.get("related", "")),
        "causedBy": id_list(meta.get("caused-by", "")),
        "solves": id_list(meta.get("solves", "")),
        "partlySolves": id_list(meta.get("partly-solves", "")),
        "needs": id_list(meta.get("needs", "")),
        "alternativeTo": id_list(meta.get("alternative-to", "")),
        "ec": meta.get("ec", ""),
        "ecWhy": meta.get("ec-why", ""),
        "summary": named.get("summary", ""),
        "sections": [
            {"title": title, "body": "\n".join(lines).strip()}
            for title, lines in sections
            if title.lower() not in ("summary", "affects", "sources")
        ],
        "affects": [],
        "sources": named.get("sources", ""),
        "file": f"problems/items/{path.name}",
    }

    where = path.name
    if item["id"] != path.stem:
        errors.append(f"{where}: id '{item['id']}' does not match the file name")
    if not item["title"]:
        errors.append(f"{where}: missing title")
    if item["kind"] not in ("problem", "category", "solution", "goal"):
        errors.append(f"{where}: kind must be 'problem', 'category', 'solution' or 'goal'")
    if item["kind"] == "goal" and not item["summary"]:
        errors.append(f"{where}: missing '## Summary'")
    if item["kind"] == "solution":
        if item["status"] not in SOLUTION_STATUSES:
            errors.append(f"{where}: solution status must be one of {', '.join(SOLUTION_STATUSES)}")
        if item["parent"]:
            errors.append(f"{where}: a solution has no parent")
        if not item["summary"]:
            errors.append(f"{where}: missing '## Summary'")
        if not (item["solves"] or item["partlySolves"]):
            errors.append(f"{where}: a solution must solve or partly solve at least one problem")
    if item["kind"] == "problem":
        if item["status"] not in STATUSES:
            errors.append(f"{where}: status must be one of {', '.join(STATUSES)}")
        if item["severity"] not in SEVERITIES:
            errors.append(f"{where}: severity must be one of {', '.join(SEVERITIES)}")
        if not item["parent"]:
            errors.append(f"{where}: a problem needs a parent")
        if not item["summary"]:
            errors.append(f"{where}: missing '## Summary'")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", item["found"]):
            errors.append(f"{where}: 'found' must be a date YYYY-MM-DD")
        if item["ec"] not in EC_IMPACT:
            errors.append(f"{where}: 'ec' (effect on the Event Calculus translation) must be one of {', '.join(EC_IMPACT)}")
        if not item["ecWhy"]:
            errors.append(f"{where}: missing 'ec-why' (one sentence: why it does or does not affect the translation)")

    for line in named.get("affects", "").splitlines():
        line = line.strip()
        if not line or line.lower() in ("- none", "none"):
            continue
        a = AFFECTS_RE.match(line)
        if not a:
            errors.append(f"{where}: cannot read affects line: {line!r}")
            continue
        item["affects"].append({"req": a.group(1), "test": a.group(2) or "", "note": a.group(3).strip()})
    return item


def load_items() -> list[dict]:
    items = [i for i in (parse_item(p) for p in sorted(ITEMS_DIR.glob("*.md"))) if i]
    ids = {i["id"] for i in items}
    if len(ids) != len(items):
        errors.append("duplicate item ids")
    by_id = {i["id"]: i for i in items}
    kind = {i["id"]: i["kind"] for i in items}

    def check_refs(i, field, wanted):
        for r in i[field]:
            if r not in ids:
                errors.append(f"{i['id']}: unknown item '{r}' in {field}")
            elif kind[r] != wanted:
                errors.append(f"{i['id']}: '{r}' in {field} must be a {wanted}")

    for i in items:
        if i["parent"] and i["parent"] not in ids:
            errors.append(f"{i['id']}: unknown parent '{i['parent']}'")
        for r in i["related"]:
            if r not in ids:
                errors.append(f"{i['id']}: unknown related item '{r}'")
        check_refs(i, "causedBy", "problem")
        check_refs(i, "solves", "problem")
        check_refs(i, "partlySolves", "problem")
        check_refs(i, "needs", "solution")
        check_refs(i, "alternativeTo", "solution")
        # walk up the parents to catch cycles
        seen, p = {i["id"]}, i["parent"]
        while p:
            if p in seen:
                errors.append(f"{i['id']}: parent cycle")
                break
            seen.add(p)
            p = by_id.get(p, {}).get("parent", "")

    # "caused by" (plus problem parents) and "needs" must not contain cycles
    def cycle_check(edges_of, label):
        state: dict[str, int] = {}

        def visit(n, path):
            state[n] = 1
            for m in edges_of(n):
                if state.get(m) == 1:
                    errors.append(f"{label} cycle: {' -> '.join(path + [m])}")
                elif m in by_id and not state.get(m):
                    visit(m, path + [m])
            state[n] = 2

        for n in by_id:
            if not state.get(n):
                visit(n, [n])

    def causes_of(n):
        it = by_id[n]
        parents = [it["parent"]] if it["parent"] and kind.get(it["parent"]) == "problem" else []
        return it["causedBy"] + parents

    cycle_check(causes_of, "caused-by")
    cycle_check(lambda n: by_id[n]["needs"], "needs")

    for i in items:
        if i["kind"] == "problem" and i["status"] in UNRESOLVED:
            if not any(
                i["id"] in s["solves"] + s["partlySolves"]
                for s in items if s["kind"] == "solution" and s["status"] != "rejected"
            ):
                warnings.append(f"{i['id']}: no proposed solution yet")
    return items


# ---------------------------------------------------------------------------
# LaTeX (text mode) to Markdown, keeping math for KaTeX
# ---------------------------------------------------------------------------

MATH_RE = re.compile(
    r"(\$\$.*?\$\$|\$.*?\$|\\\[.*?\\\]|\\begin\{(align\*?|gather\*?|equation\*?)\}.*?\\end\{\2\})",
    re.S,
)


def braced(s: str, i: int) -> tuple[str, int]:
    """Content of the brace group starting at s[i] == '{', and the index after it."""
    depth, j = 0, i
    while j < len(s):
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0:
                return s[i + 1 : j], j + 1
        j += 1
    return s[i + 1 :], len(s)


def replace_macro(s: str, name: str, fn) -> str:
    out, i, pat = [], 0, "\\" + name + "{"
    while True:
        k = s.find(pat, i)
        if k < 0:
            out.append(s[i:])
            return "".join(out)
        arg, end = braced(s, k + len(pat) - 1)
        out.append(s[i:k])
        out.append(fn(arg))
        i = end


def math_to_md(seg: str) -> str:
    if seg.startswith("\\["):
        return "$$" + seg[2:-2].strip() + "$$"
    if seg.startswith("\\begin"):
        return "$$" + seg.strip() + "$$"
    return seg


def inline(s: str) -> str:
    """Convert text-mode LaTeX to Markdown; math segments are kept for KaTeX."""
    parts, pos = [], 0
    for m in MATH_RE.finditer(s):
        parts.append(inline_text(s[pos : m.start()]))
        parts.append(math_to_md(m.group(0)))
        pos = m.end()
    parts.append(inline_text(s[pos:]))
    return "".join(parts)


def inline_text(s: str) -> str:
    s = replace_macro(s, "textit", lambda a: "*" + inline(a) + "*")
    s = replace_macro(s, "emph", lambda a: "*" + inline(a) + "*")
    s = replace_macro(s, "textbf", lambda a: "**" + inline(a) + "**")
    s = replace_macro(s, "textsc", lambda a: inline(a).upper())
    s = replace_macro(s, "texttt", lambda a: "`" + a.replace("\\_", "_") + "`")
    s = replace_macro(s, "todo", lambda a: "**TODO:** " + inline(a))
    s = replace_macro(s, "label", lambda a: "")
    for a, b in (
        ("``", "\u201c"), ("''", "\u201d"), ("---", "\u2014"), ("--", "\u2013"),
        ("\\,", " "), ("~", " "), ("\\_", "_"), ("\\%", "%"), ("\\&", "&"),
        ("\\medskip", ""), ("\\smallskip", ""), ("\\bigskip", ""), ("\\newpage", ""),
        ("\\\\", " "), ("\\ ", " "),
    ):
        s = s.replace(a, b)
    return s


def table_to_md(body: str) -> tuple[list[str], list[list[str]]]:
    body = re.sub(r"\\(toprule|midrule|bottomrule|hline)", "", body)
    rows = []
    for raw in re.split(r"\\\\", body):
        raw = " ".join(raw.split())
        if raw:
            rows.append([inline(c.strip()) for c in raw.split("&")])
    return (rows[0], rows[1:]) if rows else ([], [])


def tex_to_md(tex: str) -> str:
    """Prose with itemize lists and tabular tables to Markdown."""
    tex = re.sub(r"(?<!\\)%.*", "", tex)
    blocks: list[str] = []

    def keep(md: str) -> str:
        blocks.append(md)
        return f"\n\n@@BLOCK{len(blocks) - 1}@@\n\n"

    def itemize(m: re.Match) -> str:
        items = [x for x in re.split(r"\\item", m.group(1)) if x.strip()]
        lines = []
        for it in items:
            it = it.strip()
            label = ""
            if it.startswith("["):
                close = it.find("]")
                label, it = it[1:close] + " ", it[close + 1 :]
            lines.append("- " + label + inline(" ".join(it.split())))
        return keep("\n".join(lines))

    def tabular(m: re.Match) -> str:
        header, rows = table_to_md(m.group(1))
        md = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
        md += ["| " + " | ".join(r) + " |" for r in rows]
        return keep("\n".join(md))

    tex = re.sub(r"\\begin\{itemize\}(.*?)\\end\{itemize\}", itemize, tex, flags=re.S)
    tex = re.sub(r"\\begin\{tabular\}\{[^}]*\}(.*?)\\end\{tabular\}", tabular, tex, flags=re.S)
    tex = re.sub(r"\\(begin|end)\{center\}", "", tex)

    paragraphs = [" ".join(p.split()) for p in re.split(r"\n\s*\n", tex)]
    md = "\n\n".join(inline(p) for p in paragraphs if p)
    md = re.sub(r"@@BLOCK(\d+)@@", lambda m: blocks[int(m.group(1))], md)
    return md.strip()


# ---------------------------------------------------------------------------
# Requirements: examples.tex + req/*.md
# ---------------------------------------------------------------------------


def parse_examples() -> dict[str, dict]:
    tex = EXAMPLES_TEX.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    for chunk in re.split(r"\\subsection\{", tex)[1:]:
        title_tex, end = braced("{" + chunk, 0)
        body = chunk[end - 1 :]
        title = inline_text(title_tex)
        m = re.match(r"Req (\d{2}) – (.*)", title)
        if m:
            req_id, short = f"Req {m.group(1)}", m.group(2).strip()
        elif "Custom Counter" in title:
            req_id, short = "Req 11", "Custom Counter"
        else:
            errors.append(f"examples.tex: cannot map subsection '{title}' to a requirement")
            continue

        r_start = body.find("\\textbf{Requirement:}")
        r_end = body.find("\\medskip", r_start)
        text = tex_to_md(body[r_start + len("\\textbf{Requirement:}") : r_end]) if r_start >= 0 else ""

        entities = {"header": [], "rows": []}
        t_start = body.find("\\begin{tabular}", r_end)
        after_table = r_end
        if t_start >= 0:
            t_end = body.find("\\end{tabular}", t_start)
            inner = re.sub(r"^\\begin\{tabular\}\{[^}]*\}", "", body[t_start:t_end])
            header, rows = table_to_md(inner)
            entities = {"header": ["Entity", "Type", "Modifiers"][: len(header)], "rows": rows}
            after_table = t_end + len("\\end{tabular}")

        f = re.search(r"\\textbf\{Flavour:\}\s*([^\n]*)", body)
        flavour = inline(f.group(1)).strip().rstrip(".") if f else ""

        c_start = body.find("\\textbf{Constraint:}")
        constraint, definitions, notes = "", "", ""
        if c_start >= 0:
            pre = body[after_table:c_start]
            pre = re.sub(r"\\textbf\{(Flavour|Entities):\}[^\n]*", "", pre)
            rest = body[c_start + len("\\textbf{Constraint:}") :]
            env = re.search(r"\\begin\{align\*\}.*?\\end\{align\*\}|\\\[.*?\\\]", rest, re.S)
            if env:
                seg = env.group(0)
                constraint = seg[2:-2].strip() if seg.startswith("\\[") else seg.strip()
                definitions = tex_to_md(pre + "\n\n" + rest[: env.start()])
                notes = tex_to_md(rest[env.end() :])
        out[req_id] = {
            "title": short,
            "text": text,
            "flavour": flavour,
            "entities": entities,
            "definitions": definitions,
            "constraint": constraint,
            "notes": notes,
        }
    return out


def parse_original(req_id: str) -> tuple[str, list[dict]]:
    path = REQ_DIR / REQ_FILES[req_id]
    raw = path.read_text(encoding="utf-8")
    original, _, tests_part = raw.partition("# Test Cases")
    original = "\n".join(l for l in original.splitlines() if not l.strip().startswith("```")).strip()
    tests = []
    for m in re.finditer(r"^(TC\d+)\)\s*(.+?)\s*$", tests_part, re.M):
        tests.append({"id": m.group(1), "text": m.group(2)})
    missing = re.search(r"TEST (TC_MISSING) FOR REQ \d+\s+\[(.+?)\]", tests_part)
    if missing:
        tests.append({"id": missing.group(1), "text": missing.group(2) + " (marked as missing in req/10.md)"})
    return original, tests


def load_requirements() -> list[dict]:
    examples = parse_examples()
    reqs = []
    for rid in REQ_IDS:
        original, tests = parse_original(rid)
        ex = examples.get(rid)
        parser_file = PARSER_EXAMPLES / PARSER_FILES[rid]
        reqs.append({
            "id": rid,
            "slug": rid.lower().replace(" ", "-"),
            "title": ex["title"] if ex else TITLES_WITHOUT_FORMALISATION.get(rid, ""),
            "original": original,
            "formalised": ex is not None,
            **(ex or {}),
            "tests": tests,
            "files": {
                "requirement": f"req/{REQ_FILES[rid]}",
                "parser": f"pp1-parser/examples/{PARSER_FILES[rid]}" if parser_file.exists() else "",
            },
        })
    return reqs


# ---------------------------------------------------------------------------


def main() -> int:
    items = load_items()
    requirements = load_requirements()
    tests = {(r["id"], t["id"]) for r in requirements for t in r["tests"]}
    for i in items:
        for a in i["affects"]:
            if a["req"] != "all" and a["req"] not in REQ_IDS:
                errors.append(f"{i['id']}: unknown requirement '{a['req']}'")
            if a["test"] and (a["req"], a["test"]) not in tests and not a["note"]:
                errors.append(f"{i['id']}: unknown test '{a['req']} / {a['test']}' needs a note")
    if errors:
        print("Build failed:", *errors, sep="\n  - ", file=sys.stderr)
        return 1
    data = {
        "generated": dt.datetime.now().isoformat(timespec="seconds"),
        "statuses": list(STATUSES),
        "severities": list(SEVERITIES),
        "items": items,
        "requirements": requirements,
    }
    OUT.write_text(
        "// Generated by problems/build.py. Do not edit by hand.\n"
        "window.PROBLEM_DATA = " + json.dumps(data, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    n = {k: sum(1 for i in items if i["kind"] == k) for k in ("problem", "solution", "category")}
    print(f"Wrote {OUT.relative_to(ROOT)}: {n['problem']} problems, {n['solution']} solutions, "
          f"{n['category']} categories, {len(requirements)} requirements.")
    for w in warnings:
        print(f"  warning: {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
