# 高校科研教学样课

本目录是收到“像说明书、不像专业高校课件”的反馈后重新编写的连续12页样课。旧200页版本保留为资料底稿，本样课不继承其页面布局，也不以页数证明教学质量。

主题为主动学习辅助文献筛选的研究设计。12页依次讨论申请规定、2026面上与青C正文结构、含糊目标的修改、ASReview原始论文方法图、比较设计、观测指标、分母算例、停止规则、技术路线、证据表述和工作底稿。含讨论约58分钟，尚未授课彩排，讲师未验收。

公开材料与课堂案例分别标记。ASReview图为原论文Fig.1，CC BY4.0，保持比例、未重绘；投影放大主动学习循环局部，裁剪已标注，完整原图随来源保留。国家自然科学基金2026申请规定来自官网PDF，截图仅裁出相应条款。两项裁剪坐标和哈希见asset-transformations.json。1,000条记录的图为算术教学设定，不是真实实验结果。课堂研究问题未经完整查新，不宣称创新性或已证明效果。

2026申请规定明确要求核实AI信息、声明使用情况，禁止AI直接生成申请书。本课交付的是教学研究设计工作底稿，含AI辅助编写与未验证条件，不是可申报材料，也不是Agent真实调用模型的执行结果。

## 文件

- `lesson.py`：课程内容和讲解说明，执行后写出`lesson.json`与`讲师稿.md`。
- `prepare_sources.py`：下载官方原件与公开论文原图，记录网址和SHA-256。
- `prepare_assets.py`：高分辨率渲染官方条款，裁出原论文方法循环，记录裁剪范围。
- `worksheet.py`：生成本课研究设计工作底稿。
- `build.mjs`：专门编排这12页的原生PPTX，使用artifact-tool。
- `render.py`：从最终PPTX经LibreOffice和Poppler输出实际PDF与逐页PNG。
- `output/`：可编辑课件和Word工作底稿。
- `renders/`：最终文件的实际渲染及逐页浏览入口。

依赖使用Codex提供的Node/Python运行时和artifact-tool，不用旧幻灯片生成器。构建需将本目录node_modules链接到运行时模块，设置RUNTIME_NODE_MODULES。先运行lesson.py、prepare_sources.py和worksheet.py，再运行prepare_assets.py刷新高分辨率截图，以documents技能的render_docx.py渲染Word到word-render，最后运行build.mjs和render.py。新增修订以LESSON_REVISION指定新文件名，保留既有终稿。
