# 读懂一篇论文的入门样课

用户要求第一次接触AI的人也能看懂，前一段研究设计样课仍过于抽象。本目录按这个反馈重新写12页，带学员完成一个具体任务：拿到一篇论文，问清它能否支持某个判断，找到原文，再保存阅读笔记。

课堂问题是“AI批作业能让学生成绩提高吗”。材料为Heinrich等2025年PLOS ONE论文，DOI为10.1371/journal.pone.0328041。作者说明没有直接评价学生学习结果，原PDF第2页可搜索learning outcomes定位。这是本次阅读的依据，不把它推成AI有效或无效的通用结论。

页面给出可复制的提问、具体查找动作、原文短语和中文解释、错误与修正后的笔记，以及实际生成的Word。提问与预设回答都是课程示例，没有伪装成外部模型的执行记录。

PPT中的原论文标题图来自PDF首页，原始页以130dpi渲染后裁剪至像素坐标350,168,1045,384，未改写原图文字。原论文和裁图均按CC BY4.0保留署名与来源。主课文字、讲师稿与Word含AI辅助编写。尚未由用户验收，也没有做授课彩排或原生PowerPoint检查。

## 文件与重跑

- `output/`：可编辑课件与阅读笔记。
- `renders/`：交付PPTX实际转换的PDF、逐页PNG和浏览入口。
- `assets/paper.pdf`：公开论文原件。
- `source-locations.json`：从原PDF提取的两处定位依据。
- `讲师稿.md`：逐页讲解与练习说明。

使用Codex运行时的Python、Node和artifact-tool。先运行prepare.py下载并检查原件，运行lesson.py编写课程，再运行worksheet.py生成Word。用documents技能的render_docx.py把Word渲染到word-render后，执行build.mjs，再以render.py转换交付PPTX。node_modules需链接到运行时依赖，RUNTIME_NODE_MODULES指向同一目录。每次修订以LESSON_REVISION指定新名称，保留旧稿。

本段不承担算法或研究设计课程的全部内容。后续内容也须先给具体任务与完整示例，再引入术语，不能把这一要求只用于开场。
