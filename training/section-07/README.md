# Section 7 数据处理与统计分析

交付版本s7-r3，22页。用公开Palmer企鹅观测数据讲缺失、分析分母、异常复核、分布、标准差与标准误、独立与配对、均值差和条件区间，再讲P值、重抽样、相关及年份组成。无课堂练习。

12页框架或关系示意，其中10页有多个原生连接符，另有配对示意和重复区间图；6页原生数据图、3页原生表格、1页结果段落。图表自带6个嵌入工作簿，文字、表、图和关系均可编辑。备注提供详细讲解与来源。

国外参考为UC Berkeley 2026年秋季Stat131a的EDA、置信区间与假设检验课件，实际查看页码见“国外课件参考.md”。企鹅数据与数学教学模拟分开标识，区别见“分析说明与材料状态.md”。

analyze.py在本地用NumPy与pandas实际执行，生成results.json与analysis-packet中的分析材料。原始CSV不改。check_delivery.py另用标准库csv和statistics从原始表复算纳入数、均值及标准差，并核对重抽样分位点、二项概率、模拟覆盖数和原生图缓存。validation.json记录嵌入工作簿、包结构与几何检查。

构建用Artifact Tool与build.mjs；render.py将最终PPTX通过LibreOffice转成PDF，再由Poppler生成逐页PNG。运行所用环境与依赖路径见脚本，Python包版本见results.json。最终文件未在Microsoft PowerPoint实机复核。

统计量可复算，不表示研究假设或目标总体已核实。当前简化表不能核验巢与个体依赖关系，bootstrap仅作行独立假设下的教学分析。脚本实算不等于科研Agent全系统已运行。
