# Section 2：Agentic AI、AI Agent 与科研工作流

18 页中文学术讲授课件，无课堂练习。按具体任务解释模型、Agent、工作流、产品、Skill、工具、MCP 与 Harness；第 13—16 页为 Harness 专题。

可编辑 PPT 位于 `output/`，由最终 PPT 经 LibreOffice 导出的 PDF 和 18 张 PNG 位于 `renders/`。原理图、表格和文字均为原生可编辑对象。本节以概念关系为主题，没有为了配图加入研究数据或假造的执行截图。

`lesson.json` 保存逐页内容和讲法；`讲师稿.md` 供备课；`sources.json` 与《国外课件参考》保留来源、具体页面和参考范围。概念示意与教学情境已注明，不表示本节运行了外部科研 Agent。

构建使用 Artifact Tool，需使用 Codex 自带 Node、Python 与模块路径，设置 `RUNTIME_NODE_MODULES`，然后运行 `build.mjs`。渲染使用 `render.py`，文件核验使用 `check_delivery.py`。查看全部最终页面后再交付；程序检查不能判断课堂效果。文件尚未在 Microsoft PowerPoint 中实测。
