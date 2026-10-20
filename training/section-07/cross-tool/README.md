# 同一公开数据的Python R SPSS代码

问题是：在性别和鳍长均完整的Adelie记录中，雌雄各有多少条，均值和样本标准差是多少，雄性均值减雌性均值为多少？仅作描述统计，不运行显著性检验或因果分析。

penguins.csv为原始344条公开记录的完整复制，来源和哈希见source.json。分析保留146条，雌雄各73条。sex_code中0为female，1为male，单位mm，标准差使用n−1分母。included_rows.csv保存包含表头的CSV物理行号，它不是原始个体ID。

三份完整代码分别为analysis.py、analysis.R、analysis.sps。Python已在本地执行；R源文件已在本地WebR 0.6.0 / R 4.6.0中实际执行，逐行、分组和描述统计与Python比较通过。SPSS没有执行，不附SPSS结果表、输出CSV或假截图。IBM文档完整页面和31版PDF本轮返回403，官方索引提供的语法用于编写；SPSS语法仍需在有许可的软件中运行检查。

讲师可先展示统一任务和筛选条件，再打开三份代码，比较其中的读取、筛选、分组和输出位置。课堂不要求学员安装、注册或执行。

## 生成代码的任务示例

请只使用随附penguins.csv。保留原始文件，选择species为Adelie、sex为female或male且flipper_length_mm完整的记录。分别给出Python标准库、基础R和SPSS语法文件，输出每组n、均值、样本SD，以及male减female的均值差。0编码female，1编码male。三份代码应保存纳入行号，说明缺失值处理、单位和标准差分母。不要生成实验结果或P值，不把未经执行的代码说成已运行。执行后将输出与原始行核对，说明使用的版本和未验证的条件。

## 复跑方式

在本目录运行Python的analysis.py。它默认读取本目录CSV，输出到python-output，也可给第一个参数指定CSV。

桌面R可在本目录执行Rscript analysis.R；本轮没有桌面R或RStudio验证。复现本轮隔离执行，可先用Python执行prepare-r-runtime.py，再用Node执行run-r.mjs。准备脚本下载固定官方npm版本，核对SRI，文件仅存本节.build，不改变全局配置。Windows上对WebR的JS加载器作两处路径到file URL的兼容处理，R.wasm和analysis.R未改；哈希与范围见r-runtime-provenance.json。下载需要联网，分析在本机R解释器执行，不调用模型。

SPSS运行前需把工作目录设为本目录，确认输出文件可覆盖，再打开analysis.sps；本轮未执行这一步。源文件包含输入类型、文本缺失筛选、数字转换、分组统计和输出。运行后须先核对146条纳入行及编码，再核对数字，不能只看输出表外观。

check_results.py核对Python与R的纳入行、编码、值、两组统计和差值，并检查输出、源文件及输入哈希。不执行SPSS，不证明独立抽样、目标总体、模型假设或科学结论。
