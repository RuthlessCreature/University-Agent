# University Agent

高校科研 AI 一日培训的中文课件与本地文件演示。2026-10-17 的交付包括 12 张样页、75 页完整备课材料、客户原稿 52 项逐条对照，以及可重跑的 Grant、Paper、Patent 教学草稿。

- 本地演示读取结构化 JSON 和 DOCX 模板，执行指南校验、内容映射、来源检查和 Word 输出。它使用预先编写的教学材料，没有调用模型。
- Worker 已有 MiniMax-M3 文本适配和新增的 Durable Object 状态代码；本次没有部署 Cloudflare，也没有真实调用 MiniMax。
- 新课件位于 `training/deck-zh/dist/*_v7.pptx`。旧的 165 页和 92 页课件及其生成器未参与构建。

仓库只放实现代码及演示素材；技能规范在 [University-Skills](https://github.com/RuthlessCreature/University-Skills)。

先读 [QA_REPORT.md](QA_REPORT.md)，再看 [客户原稿逐条对照](training/curriculum/CLIENT_ORIGINAL_52_ITEMS.md) 和 [本地与云端状态](docs/LOCAL-AND-CLOUD-STATUS.md)。

两个仓库放在同一父目录，在 Python 环境安装 `../University-Skills/requirements-teaching.txt` 后，运行：

```powershell
python training/demos/create_inputs.py
node tools/serve-local.mjs
```

打开 http://127.0.0.1:8788 可重跑三个固定教学案例并下载 Word。Windows 可通过 `TRAINING_PYTHON` 指定 Python 绝对路径。本地服务只监听回环地址，接口只接受三个内置案例。

PPT 的文字与讲师备注在 `training/deck-zh/src/author_course.py`；运行该文件更新清单和讲师手册，再运行 `src/build.mjs`。构建依赖 Codex 内置 `@oai/artifact-tool`、presentations finalizer、Microsoft YaHei；独立文件渲染依赖 LibreOffice 和 Poppler。脚本中的本机路径需按环境调整，尚未包装为普通 npm 一键构建。可直接在 PowerPoint 编辑交付的 PPTX，图表数据工作簿已嵌入。
