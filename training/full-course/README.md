# 高校科研 AI 课程：240 页合并审阅版

Section 0–14 的当前版本已合并为一份可编辑 PPT。分节原稿、240 页讲者备注、图表和图表工作簿均保留。当前合并版本为 course-r3，修正了前版列出的11页流程说明断词。具体来源文件及哈希见 assembly-manifest.json；course-r2 文件留作历史对照。

打开 output/ 中的 PPT 可继续编辑；带章节书签的 PDF 便于浏览。preview.html 显示全部 240 张最终预览，NAVIGATION.md 和 navigation.csv 对照全课页码与分节页码。PPT 页脚沿用各节页码。

## 本轮检查

- 240 页均由实际合并 PPT 经 LibreOffice 转成 PDF，再渲染为 PNG。本轮实际打开11张修改页；其余229张与前版已审阅预览RGB像素相同。前版全部240页曾逐张查看，记录保存在history/course-r2/visual-review.json。
- check_course.py 核对 15 份分节原稿的哈希、240 份幻灯片 XML、240 份讲者备注及原生对象。24 个图表、26 个表格、12 个图片对象、474 条连接线和24份嵌入工作簿均有对应检查。
- validation.json 记录 ArtifactTool 的结构与几何检查；checks.json 记录独立核对结果。自动检查只证明其列明的范围。
- revision-comparison.json 保存新旧合并版240页逐像素比较。wrap-review.json 保存11页修改前后文字、预览哈希和查看范围；涉及的4节共66页，讲者备注和页面数字序列核对一致，其他55张分节预览像素相同。visual-review.json 保留当前逐页审阅依据，前版11处换行问题已修正。

## 仍待完成的事

这份课件目前供教学审阅，尚未取得用户验收。370分钟主讲加110分钟备用材料属于备课分配，尚未做真人计时彩排。

52项原课程主题中，46项登记为已有内容，5项采用替代工具或调整讲法，1项保留来源缺口：Science 编辑政策原始网页本轮仍未成功读取。未拿 Science Partner Journals 的规则代替 Science 本刊政策。逐项范围见 ../curriculum/COURSE_COVERAGE_MATRIX.md。

Section 14 明确区分本地固定材料演示与云端模型任务。此前本轮云端健康请求返回200，登录返回401，未创建模型任务。当前配置为 DeepSeek deepseek-flash，MiniMax 停用。课件中的结构图不能作为云端执行截图；夹具测试不能证明真实模型全流程已经跑通。

公开原图、公开数据的课程二次计算、自编教学材料和实际运行记录，按页保留各自的来源与限定。本轮合并未重新执行所有分节科研产物，也未替代科学审查或正式签核。

## 复查

安装 pypdf 后运行 `python training/full-course/check_course.py`。该检查需要仓库中15份对应分节PPT、课程登记表、当前合并PPT以及渲染PDF和PNG。交付ZIP保留这些依赖与逐文件SHA256清单。

assemble_course.mjs 位于 ../curriculum/，用于按登记版本合并原生PPT部件。render_course.py 用 LibreOffice 和 Poppler 渲染，add_pdf_navigation.py 添加章节书签。compare_revision.py 对照前版实际预览；prepare_wrap_revision.py 登记本次四节修订。输出记录均注明检查范围。
