# Section 0：封面与课程导入

当前版本 `s0-r3`，4 页，供逐节审阅。第 4 页改为“今天会跟着做哪些事”，材料背景与打开文件的操作移到对应章节。后续章节尚未据此完成，约 240 页是课程页数预算。

文件位置：

- `output/`：可编辑 PPTX。
- `renders/s0-r3/`：从最终 PPTX 经 LibreOffice 导出的 PDF 与 4 张逐页预览。
- `materials/`：供后续章节选用的公开论文、公开数据、教学任务与 Word 模板，以及来源清单；不是本节课前必备材料。
- `讲师稿.md`：每页讲法、材料说明及需要保留的限定。
- `审查记录.md`、`checks.json`：人工检查记录和自动文件检查结果。
- `../curriculum/course_structure_240.json`：Section 0 加 14 个内容章节的页数安排，共 240 页；Harness 安排在第 2、14 节，Humanizer 在第 3 节单独讲，同时贯穿全课文字修订。

运行环境需要 Artifact Tool、Python、LibreOffice 与 Poppler。`build.mjs` 从本节源文件生成原生可编辑文字和线条；`render.py` 渲染实际最终 PPTX；`check_delivery.py` 检查文件与来源哈希。检查通过不能替代教学审阅。

本节没有数据图、科研示意图或 Agent 执行截图，不添加与课程导入无关的装饰性科研图片。
