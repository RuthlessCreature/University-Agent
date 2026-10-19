# Section 4 选题与研究问题

14页中文讲授稿，当前修订s4-r5。围绕AI辅助学习案例，讲解前沿扫描、问题收窄、问题类型、可能混杂、空白核对、假说、四维判断、竞争扫描、资源取舍和AI选题流程。没有课堂练习。

## 文件

- output/高校科研AI课程_Section4_选题与研究问题_s4-r5.pptx：可编辑课件。
- renders/s4-r5/：真实PPTX导出的PDF和14张逐页预览。
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

## 三类材料的具体比较

第2页按2024—2025年窗口比较三条公开记录，第10页用真实论文Figure1说明不同材料能支持的判断。trend-packet包含可编辑CSV与JSON、实际检索文本、来源定位、获取哈希和检查脚本。材料为定向选择，未作全库趋势计数；专利公开日、申请日与更早临时申请日分别登记，arXiv版本保留会议关联。中文解读和拟议问题由AI编写，尚待教师审定；原图依CC BY4.0标注出处，未冒充本项目运行界面。

整节14页已重新渲染并复核。第2、10页补充来源比较，第8页修正孤字换行，其余页面文字与s4-r3一致。s4-r4已逐页查看；最终s4-r5仅第8页PNG变化，其余13页与已查看页面逐字节相同，第8页已另行查看。统计图和内嵌数据表保留，不把三条材料画成全领域热度曲线。未在Microsoft PowerPoint原生实测，文件与程序检查不代表科研或教学验收。
