# University Agent

教学版本状态（2026-10-17）：用户否定了下述200页v11课件的教学表达。v11保留为资料底稿，不作为已验收终稿。当前重新编写的连续12页样课位于 [teaching-redesign](training/teaching-redesign/README.md)，先审阅这一段，再决定全课扩展方式。

高校科研 AI 一日培训的中文课件与文件演示。当前 v11 交付包括 12 张样页、200 页备课材料、客户原稿52项逐条对照，以及可重跑的 Grant、Paper、Patent 教学草稿。按讲师语速准备370分钟主课与110分钟延伸，尚未全程彩排。

- 本地演示读取结构化 JSON 和 DOCX 模板，执行指南校验、内容映射、来源检查和 Word 输出。它使用预先编写的教学材料，没有调用模型。
- Worker 使用 MiniMax-M3 Token Plan 配置，完整Skill提示、持久任务、逐阶段审核和受约束DOCX工具已接入。本轮按用户要求先完成可部署版本；没有云部署或真实模型调用。
- 新课件位于 `training/deck-zh/dist/*_v11.pptx`。旧的165页与92页课件及生成器未参与构建。新增100页具体教学案例、15张公开数据原生图和10页实际运行产物解析。

仓库只放实现代码及演示素材；技能规范在 [University-Skills](https://github.com/RuthlessCreature/University-Skills)。

先读 [QA_REPORT.md](QA_REPORT.md)，再看 [客户原稿逐条对照](training/curriculum/CLIENT_ORIGINAL_52_ITEMS.md) 和 [部署说明](docs/DEPLOYMENT.md)。

两个仓库放在同一父目录，在 Python 环境安装 `../University-Skills/requirements-teaching.txt` 后，运行：

```powershell
python training/demos/create_inputs.py
node tools/serve-local.mjs
```

打开 http://127.0.0.1:8788 可重跑三个固定教学案例并下载 Word。Windows 可通过 `TRAINING_PYTHON` 指定 Python 绝对路径。本地服务只监听回环地址，接口只接受三个内置案例。

Worker预览：`npm ci` 后运行 `npx wrangler dev --local --port 8789`；依照部署说明配置口令。该界面与8788的Python教学服务分别验收。`npm run deploy:check`只构建，不发布。

本地 `.agents/skills/` 与 Worker 的版本包包含同一提交的24份完整SKILL.md；`npm test`逐字检查内容和哈希。模型、文件和代码执行工具仍按环境分别登记，Skill同源不等于所有工具均已接通。

PPT 的原始75页文字在 `training/deck-zh/src/author_course.py`，100页案例在 `src/advanced_lessons.py`。运行 `src/expand_course.py` 生成200页清单、公开数据计算及讲师手册，再运行 `src/build.mjs`。构建依赖Codex内置artifact-tool、presentations finalizer与Microsoft YaHei；最终文件渲染依赖LibreOffice和Poppler。脚本中的本机路径需按环境调整，尚未包装为普通npm一键构建。每次成功导出使用新的DECK_REVISION，finalizer拒绝覆盖已完成版本。可直接编辑PPTX；16张数据图均有嵌入的Excel工作簿。
