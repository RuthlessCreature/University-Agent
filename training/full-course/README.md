# 高校科研 AI 课程：240 页合并审阅版

Section 0–14 已合并为可编辑的 course-r4。Section 1 使用 a7：第11页新增 Nature Portfolio、Science journals 与 PLOS 官方 AI 政策对照，并在讲师稿及配套说明中标明具体用途和限制。Science 依据官方细则 PDF 第1—2页；访问日期不等于政策生效日期。

PPT 保留分节原生页面、240份讲者备注、图表、表格、关系图和工作簿。`output/` 放可编辑PPTX及带15个章节书签的PDF；`preview.html` 可查看240张PNG，`NAVIGATION.md` 和 `navigation.csv` 对应全课与分节页码。

## 已完成的检查

- 新版PPTX实际渲染成240页PDF和240张PNG。与course-r3逐页比较后，第15页为新增内容；第52、70、158、172、190、234页有少量局部渲染像素变化，已查看新版预览。其他233页像素相同。分节源文件除Section 1外均与course-r3使用同一哈希。
- `check_course.py` 核对15个分节PPTX哈希、240份幻灯片XML、240份讲者备注和内部资源链接。总稿保留24个图表、26个表格、12张图片、474条连接线、24个嵌入工作簿，765个组成文件和1506条内部关系均通过检查。
- `validation.json` 记录PPT包结构与页面几何检查；`checks.json` 记录分节源文件与实际渲染检查；`revision-comparison.json` 和 `visual-review.json` 记录逐页比较及本轮查看范围。
- Section 1 的a7通过12页PPT、PDF、PNG、讲者备注、原始研究数据和可编辑对象结构检查；人工查看该节缩略图及新版总课件第15页全尺寸图。

这些检查证明文件结构、来源定位和渲染结果符合记录范围，不代表期刊政策的法律解释、完整科学审查、PowerPoint实测、真人计时彩排或用户教学验收。全课仍供教学审阅；370分钟正式讲授加110分钟延伸内容为讲师分配，尚未真人彩排。52项原始主题的逐项定位见 `../curriculum/COURSE_COVERAGE_MATRIX.md`。

当前云端模型执行状态与课件完成情况分开登记。Section 14 中的结构图不能当作云端执行截图；课件合并也不等于所有科研技能已在真实材料上端到端运行。
