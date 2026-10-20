# Section 7 数据处理与统计分析

交付版本s7-r9，22页。用公开Palmer企鹅观测数据讲缺失、分析分母、异常复核、分布、标准差与标准误、独立与配对、均值差和条件区间，再讲P值、重抽样、相关及年份组成。第21页用一个代码改动说明Cursor编辑、Python执行和结果复核如何衔接；第22页保留Python与R实际结果比较。Python、R、SPSS三份代码继续随包提供。无课堂练习。

6幅原生数据图、5页原生表格，流程与关系使用可编辑图形。6个嵌入工作簿保存图表数据，备注提供讲解与来源。国外参考为UC Berkeley 2026年秋季Stat131a的EDA、置信区间与假设检验课件，实际查看页码见“国外课件参考.md”。企鹅观测、二次计算与数学教学模拟分别标识。

analyze.py实际生成results.json与analysis-packet中的分析材料。cross-tool附完整Python、R和SPSS代码、统一数据与运行说明。Python与本地WebR中的R源文件已实际执行，146条纳入行、编码、数值、两组n、均值、样本SD和差值比较通过。SPSS未执行，包内没有SPSS输出；RStudio与桌面R也未实测。运行环境和哈希见各输出目录的run.json及r-runtime-provenance.json。

check_delivery.py从原始CSV独立复算，核对图缓存、工作簿、PDF页数、代码及输出哈希。cross-tool/check_results.py检查Python与R的数值一致性。validation.json记录文件包与几何检查。此前s7-r7的第21、22页已分别查看；本轮按最终s7-r9重新渲染并对变化页复核，范围见下及revision-comparison.json。

构建使用Artifact Tool与build.mjs；render.py将最终PPTX经LibreOffice转为PDF，再生成逐页PNG。未在Microsoft PowerPoint实机复核。统计量可复算，不表示抽样独立、目标总体或研究结论已核实，也不代表科研Agent全系统已运行。

新增cursor-packet保存同一数据下改动前后的完整Python脚本、代码差异、两次实际输出与命令记录，以及从原CSV独立复算的检查。差值从雄减雌改为雌减雄，146条纳入记录和两组统计不变。Cursor任务与说明由AI编写，未在Cursor操作，尚待教师审定。CMU2025原始课件第26页的采用范围及官方功能来源见cursor-packet/参考资料.md。

当前22页全部重新渲染；仅第21页文字变化；第1—20页PNG与s7-r5逐字节相同，第22页标题局部渲染有差异，文字未变，已另页查看，详见revision-comparison.json。第21页已查看最终预览；程序检查通过不代表软件界面或科学验收。


本轮具体补充：第7页用源CSV实际比较保留全部记录和暂排两条异常标记时的差值；第13页改为连续前20次模拟，显示第18次未覆盖真值；第14页将双侧相加的12根概率柱标红。原始数据、146条正式纳入表及全部1000次模拟均未改变。新增完整代码、两个比较CSV、元数据和说明在analysis-packet。

最终22页从实际PPTX重新导出。相对s7-r7，只有第7、13、14页文字改变，12页PNG有渲染变化，均已逐页打开查看；其余10页与此前已审页面字节一致。s7-r8中IQR和n缩写在s7-r9第7页改为普通话，补齐原始数据出处。新增计算、图表数值、尾部颜色索引及文件检查通过，不代表数据异常原因或模型独立性已获证明。
