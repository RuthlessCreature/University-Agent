# Section 8 科研图表与技术路线

交付版本s8-r2，16页，配套PDF、逐页PNG、讲师稿、国外参考定位、材料说明、可编辑路线与独立数据图。

课程用同一公开数据比较均值与分布、坐标范围和误差定义，再讲图注、多面板、配色、AI绘图输入和研究路线。没有课堂练习。7幅原生图分布在第3、4、6、8页；9页含多个原生连接符，另有误差范围与颜色示意。文字、图形和图表可编辑。图注有完整示例。

国外参考为UBC 2026年可视化课程所列原始课件，实际查看7页。课件版本、页码和采用范围见“国外课件参考.md”。公开观测、二次计算、拟议方案和假说示意分别标明。

prepare_figures.py生成计算结果，build.mjs用Artifact Tool生成原生PPT，render.py经LibreOffice与Poppler生成实际渲染，export_route.py输出draw.io与SVG，export_figure.py输出独立数据图。脚本所需运行时路径见文件；NumPy/pandas版本见figure-data.json。

check_delivery.py从源CSV另用标准库复算均值、SD和分母，核对图表缓存、虚线、路线节点连接与导出文件。validation.json保留最终器结果，审查记录说明视觉检查。PPT未在Microsoft PowerPoint中实机复核，draw.io未在应用中交互编辑复核。程序与视觉检查不表示科研结论、机制或Agent全系统通过验收。
