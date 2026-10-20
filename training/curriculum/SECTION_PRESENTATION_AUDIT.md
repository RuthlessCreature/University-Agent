# 逐节课件与图文核对表

按 `section-progress.json` 当前登记版本检查。每节都有前沿高校、研究机构或专业组织的原始讲义记录，且写明实际查看的页段；对应人工视觉审查记录也在表中。Section 4 的NBER资料是作者公开的逐页文字稿，没有把它称作看过视觉PPT；该节另有Utah原始课件可供视觉参照。

表中的对象数量来自每份PPTX中的原生PowerPoint图表、表格、图片和连接线。它能说明页面中含有可编辑图形元素，不能单独证明内容易懂或教学质量。

| Section / 内容 | 当前版本 / 页数 | 前沿讲义及实际查看页 | 原生图表 / 表格 / 图片 / 连接线 | 视觉审查记录 |
|---|---|---|---:|---|
| 0 封面与课程导入 | s0-r4 / 4 | UC Berkeley CS294/194-196 Agentic AI Introduction，物理页6、10、19 | 0 / 0 / 0 / 9 | [审查记录](../section-00/审查记录.md) |
| 1 科研AI的能力、原理与学术边界 | a7 / 12 | GWU MAE-6291 Class 2第5、20、28页；IJS Foundation Models for Science第8、22、29页 | 1 / 2 / 0 / 13 | [审查记录](../section-01-academic/审查记录.md) |
| 2 Agentic AI、AI Agent与科研工作流 | s2-r7 / 18 | Stanford CS224N Lecture 10：第29、30、68页已查看；第61、70页另读文字 | 0 / 2 / 0 / 61 | [审查记录](../section-02/审查记录.md) |
| 3 Humanizer与各类科研产物的表达 | s3-r4 / 18 | UCL Beyond Polishing: AI in Academic Writing，第4、8、10、13、14页 | 2 / 1 / 0 / 32 | [审查记录](../section-03/审查记录.md) |
| 4 选题与研究问题 | s4-r7 / 14 | University of Utah Research 101: Ideas，第35、41、52页；NBER作者文字稿仅作文字参考 | 1 / 1 / 2 / 37 | [审查记录](../section-04/审查记录.md) |
| 5 文献检索、阅读与综述 | s5-r4 / 24 | UCL Social Research Institute证据综合讲义，第14、17、43、56页 | 1 / 4 / 2 / 49 | [审查记录](../section-05/审查记录.md) |
| 6 研究与实验方案 | s6-r5 / 16 | UC Davis BIM283 Lecture 07第2、10、11页；Lecture 09第2、8、9页 | 2 / 3 / 0 / 45 | [审查记录](../section-06/审查记录.md) |
| 7 数据处理与统计分析 | s7-r9 / 22 | UC Berkeley Stat 131a Lectures 2、11、14；CMU Generative AI Lecture 23物理第26页 | 6 / 5 / 0 / 24 | [审查记录](../section-07/审查记录.md) |
| 8 科研图表与技术路线 | s8-r6 / 16 | UBC CPSC447 Marks & Channels第4、6、17页；Network Data第2页 | 7 / 0 / 0 / 32 | [审查记录](../section-08/审查记录.md) |
| 9 论文写作、投稿与返修 | s9-r7 / 22 | University of Göttingen Scientific Writing and Structure Your Work，物理页4、8、9、16、19、21 | 2 / 0 / 0 / 37 | [QA记录](../section-09/QA.md) |
| 10 基金申报与Grant Agent | s10-r5 / 26 | NIH StrokeNet Grant Writing，物理页21、27、29、36、40、51 | 0 / 1 / 1 / 46 | [审查记录](../section-10/审查记录.md) |
| 11 专利挖掘与技术交底 | s11-r7 / 12 | WIPO PCT Seminar Presentation，物理页16、24、94、96 | 0 / 1 / 1 / 21 | [审查记录](../section-11/审查记录.md) |
| 12 项目执行与结题 | s12-r8 / 10 | HaDEA REPA Reporting and Payment Webinar，物理页75、97、98、102、104 | 1 / 2 / 1 / 20 | [审查记录](../section-12/审查记录.md) |
| 13 科研汇报与成果传播 | s13-r10 / 10 | University of Florida Giving Scientific Presentations，物理页3、14、20、23、27、29、31 | 1 / 1 / 2 / 18 | [QA记录](../section-13/QA.md) |
| 14 本地与云端Agent实际演示 | s14-r3 / 16 | CMU Generative AI Lecture 23，物理页29、30、31、32、34、37 | 0 / 3 / 3 / 30 | [QA记录](../section-14/QA.md) |

## 全课核对

15节合计240页。分节PPTX哈希已与登记值逐一比对；每页都有讲者备注。原生对象共24个图表、26个表格、12张图片和474条连接线。合并后的页面、备注、对象、内部链接和实际渲染结果见[course-r4检查记录](../full-course/checks.json)。新旧合并预览逐页比较见[逐像素比较记录](../full-course/revision-comparison.json)，人工查看范围见[视觉审查记录](../full-course/visual-review.json)。

各节审查记录会区分本轮重新打开的页面与沿用相同预览的页面。LibreOffice/Poppler渲染不等于Microsoft PowerPoint桌面实测；文件检查也不等于8小时真人彩排或用户教学验收。公开讲义、公开研究材料、教学模拟和真实工具运行的边界仍以各节来源文件为准。
