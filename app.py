"""LaTeX + Markdown 渲染工具（支持中文）。

服务端：Markdown -> HTML（先把公式段落保护起来，避免被 Markdown 破坏），再用 bleach 白名单清洗。
前端：本地 MathJax 3（node_modules，无需外网 CDN）渲染公式，中文走系统中文字体。
"""
import argparse
import html
import os
import re

import bleach
import markdown
from flask import Flask, jsonify, render_template, request, send_from_directory

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MATHJAX_DIR = os.path.join(BASE_DIR, "node_modules", "mathjax", "es5")

app = Flask(__name__)

# 公式定界符：环境、$$..$$、\[..\]、\(..\)、$..$（顺序即优先级）
MATH_PATTERN = re.compile(
    r"(\\begin\{(equation|align|gather|multline|eqnarray|cases|matrix|pmatrix|bmatrix)\*?\}.*?\\end\{\2\*?\}"
    r"|\$\$.+?\$\$"
    r"|\\\[.+?\\\]"
    r"|\\\(.+?\\\)"
    r"|(?<![\\$])\$(?!\s)[^$\n]+?(?<![\s\\])\$(?!\d))",
    re.DOTALL,
)
CODE_PATTERN = re.compile(r"(```.*?```|`[^`\n]+`)", re.DOTALL)

ALLOWED_TAGS = list(bleach.sanitizer.ALLOWED_TAGS) + [
    "p", "br", "hr", "pre", "span", "div", "img",
    "h1", "h2", "h3", "h4", "h5", "h6",
    "table", "thead", "tbody", "tr", "th", "td", "del", "sup", "sub",
]
ALLOWED_ATTRS = {"*": ["class"], "a": ["href", "title"], "img": ["src", "alt", "title"]}


def render_text(text: str) -> str:
    """把含 LaTeX 的 Markdown 文本转为安全 HTML，公式原样保留给 MathJax。"""
    stash = []

    def protect(m):
        stash.append(m.group(0))
        return f"MJXPH{len(stash) - 1}PHEND"

    # 代码块里的 $ 不当公式：先切出代码段，只在非代码段里保护公式
    parts = CODE_PATTERN.split(text)
    for i in range(0, len(parts), 2):
        parts[i] = MATH_PATTERN.sub(protect, parts[i])
    body = markdown.markdown("".join(parts), extensions=["tables", "fenced_code", "nl2br", "sane_lists"])
    body = bleach.clean(body, tags=ALLOWED_TAGS, attributes=ALLOWED_ATTRS, strip=True)
    # 还原公式（HTML 转义，MathJax 读取的是文本内容）
    return re.sub(r"MJXPH(\d+)PHEND", lambda m: html.escape(stash[int(m.group(1))], quote=False), body)


@app.route("/")
def index():
    with open(os.path.join(BASE_DIR, "examples", "demo.md"), encoding="utf-8") as f:
        demo = f.read()
    return render_template("index.html", demo=demo)


@app.route("/api/render", methods=["POST"])
def api_render():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    if not isinstance(text, str):
        return jsonify(error="text 必须是字符串"), 400
    if len(text) > 500_000:
        return jsonify(error="文本过长"), 413
    return jsonify(html=render_text(text))


@app.route("/mathjax/<path:filename>")
def mathjax(filename):
    return send_from_directory(MATHJAX_DIR, filename)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8790)
    args = parser.parse_args()
    app.run(host=args.host, port=args.port)
