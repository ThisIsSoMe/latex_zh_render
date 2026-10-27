# latex_zh_render

中文 LaTeX + Markdown 在线渲染工具。左侧输入，右侧实时预览。

- 公式：`$...$`、`\(...\)`、`$$...$$`、`\[...\]`、`\begin{align}` 等环境；含 amsmath、physics、mhchem、boldsymbol、color
- 中文：正文和 `\text{中文}` 均用系统中文字体（思源宋体/黑体）
- MathJax 3 从本地 `node_modules` 提供，不依赖外网 CDN
- 服务端先保护公式再转 Markdown，避免 `_`、`*` 被误解析；输出经 bleach 白名单清洗

## 运行

```bash
pip install -r requirements.txt
npm install            # 安装 mathjax@3.2.2
python3 app.py --host 0.0.0.0 --port 8790
```

打开 http://<机器IP>:8790/

## 接口

```
POST /api/render  {"text": "..."}  ->  {"html": "..."}
```

返回的 HTML 中公式保持原文，需页面加载 MathJax 后渲染。

## 自检

```bash
node check_tex.js examples/demo.md   # 用 Node 版 MathJax 编译文件中所有公式
```
