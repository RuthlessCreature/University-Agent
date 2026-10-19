# Section 4 选题与研究问题

14页中文讲授稿，当前修订s4-r7。围绕AI辅助学习案例，讲解前沿扫描、问题收窄、问题类型、可能混杂、空白核对、假说、四维判断、竞争扫描、资源取舍和AI选题流程。没有课堂练习。

## 文件

- output/高校科研AI课程_Section4_选题与研究问题_s4-r7.pptx：可编辑课件。
- renders/s4-r7/：真实PPTX导出的PDF和14张逐页预览。
- lesson.json、build.mjs：内容和制作源码。
- 讲师稿.md：逐页解释、案例边界与出处。
- 国外课件参考.md、sources.json、retrieval.json：原始课件、查看页与采用范围。
- source-data.json：真实研究图表数值及单位。
- 教学模拟与选题示例.md：拟议研究及待核查条件。
- check_delivery.py、checks.json、validation.json、审查记录.md：检查范围与记录。

## 重新构建

使用工作区bundled Node和Python。RUNTIME_NODE_MODULES指向bundled node_modules，当前目录node_modules连接到同一路径。PPTX通过Artifact Tool制作，未使用被否定的165/92页生成器。按presentation技能运行一次操作标记后，执行build.mjs；新修订设置SECTION_REVISION，避免覆盖已交付文件，再执行render.py和check_delivery.py并传同一修订号。

渲染需要LibreOffice与bundled Poppler。本次检查不证明Microsoft PowerPoint或Google Slides的实际显示情况。

## 来源与状态

已查看Utah 2026原始PDF第35、41、52页；NBER来源为作者逐页文字版，不能声称其视觉PDF已查看。真实数据为PNAS 2025公开论文报告值；本科研究方案为教学模拟。没有模型调用或Agent检索执行记录。文件交付供教学审阅，不代表研究题目、科学方案或全课程已获验收。

## 实际检索与材料比较

第2页使用真实Google Scholar检索截图，检索式为“generative AI”“tutoring”，年份2024—2025，保存相关性排序下的前10条记录。对第1、2、4条回到原始来源核对，并逐条说明阅读范围。引用次数记录查询日期，不赋予Web of Science高被引标签。用户已允许使用Google Scholar等可访问入口替代原稿中的数据库。

第10页保留三类定向公开材料的比较、真实论文Figure1及证据解释。trend-packet提供CSV、JSON、原始截图、页面文本、版本归并依据和未决事项。10条搜索结果与三类材料各有选取范围，不能据此估算全领域数量、增长率或未来热点。中文解释由AI编写，尚待教师审定；作者原图按CC BY4.0注明出处。

当前s4-r7的14页已从实际PPTX重新导出。相对s4-r5只有第2页文字变化；第2—14页PNG均有渲染差异，已逐页打开查看，第1页PNG与此前已审页面逐字节一致。s4-r6右侧“报告”出现拆行，已调整为“首条报告被引204次”后重新导出。检查未见遮挡或裁切，未在Microsoft PowerPoint原生实测。文件检查与视觉查看不代表科研结论或教学验收。
