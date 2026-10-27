// 用 Node 版 MathJax 校验示例中每个公式能否编译（无浏览器时的自检）
const fs = require("fs");
const text = fs.readFileSync(process.argv[2] || "examples/demo.md", "utf-8").replace(/`[^`\n]+`/g, "");
const re = /\\begin\{(align|equation|gather)\*?\}[\s\S]*?\\end\{\1\*?\}|\$\$[\s\S]+?\$\$|\\\[[\s\S]+?\\\]|\\\([\s\S]+?\\\)|\$[^$\n]+?\$/g;
require("mathjax").init({
  loader: { load: ["input/tex-full", "output/svg"] },
  tex: { formatError: (jax, err) => { throw err; } }
}).then((MathJax) => {
  let bad = 0, n = 0;
  for (const m of text.match(re) || []) {
    n++;
    let tex = m, display = true;
    if (m.startsWith("$$")) tex = m.slice(2, -2);
    else if (m.startsWith("\\[") || m.startsWith("\\(")) { tex = m.slice(2, -2); display = m[1] === "["; }
    else if (m.startsWith("$")) { tex = m.slice(1, -1); display = false; }
    try { MathJax.tex2svg(tex, { display }); }
    catch (e) { bad++; console.log("FAIL:", m.slice(0, 60), "->", e.message); }
  }
  console.log(`${n} 个公式，失败 ${bad} 个`);
  process.exit(bad ? 1 : 0);
});
