# Section 4 选题与研究问题

14页中文讲授稿，当前修订s4-r3。围绕AI辅助学习案例，讲解前沿扫描、问题收窄、问题类型、可能混杂、空白核对、假说、四维判断、竞争扫描、资源取舍和AI选题流程。没有课堂练习。

## 文件

- output/高校科研AI课程_Section4_选题与研究问题_s4-r3.pptx：可编辑课件。
- renders/s4-r3/：真实PPTX导出的PDF和14张逐页预览。
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
