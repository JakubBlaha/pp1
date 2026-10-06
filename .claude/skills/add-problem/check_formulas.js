// Check that every formula in problems/data.js parses with KaTeX.
// Usage: NODE_PATH=<dir with katex installed>/node_modules node check_formulas.js problems/data.js
const fs = require("fs");

let katex;
try {
  katex = require("katex");
} catch (e) {
  console.error("KaTeX not found. Install it once with: npm install --prefix /tmp/pp1-katex katex@0.16.11");
  console.error("then run: NODE_PATH=/tmp/pp1-katex/node_modules node " + process.argv[1] + " problems/data.js");
  process.exit(2);
}

const src = fs.readFileSync(process.argv[2] || "problems/data.js", "utf8");
const data = JSON.parse(src.slice(src.indexOf("=") + 1).trim().replace(/;$/, ""));
let n = 0;
let bad = 0;

function check(tex, display, where) {
  n++;
  try {
    katex.renderToString(tex, { displayMode: display, throwOnError: true, strict: "ignore" });
  } catch (e) {
    bad++;
    console.log(`[${where}] ${e.message.split("\n")[0]}\n   ${tex.slice(0, 160)}`);
  }
}

// Code is skipped, so that a $ inside code is not taken for math.
function scan(md, where) {
  if (!md) return;
  let s = md.replace(/```[\s\S]*?```/g, "").replace(/`[^`\n]+`/g, "");
  s = s.replace(/\$\$([\s\S]+?)\$\$/g, (m, t) => {
    check(t, true, where);
    return "";
  });
  s.replace(/\$([^$\n]+?)\$/g, (m, t) => {
    check(t, false, where);
    return "";
  });
}

for (const it of data.items) {
  scan(it.title, it.id);
  scan(it.summary, it.id);
  scan(it.ecWhy, it.id);
  scan(it.sources, it.id);
  it.sections.forEach((x) => scan(x.body, it.id));
  it.affects.forEach((a) => scan(a.note, it.id));
}
for (const r of data.requirements) {
  ["text", "definitions", "notes", "flavour"].forEach((k) => scan(r[k], r.id + "." + k));
  if (r.constraint) check(r.constraint, true, r.id + ".constraint");
  (r.entities ? r.entities.rows : []).forEach((row) => row.forEach((c) => scan(c, r.id + ".entities")));
}
console.log(`${n} formulas checked, ${bad} failed`);
process.exit(bad ? 1 : 0);
