# 代码改动与实际计算怎样衔接

用公开企鹅数据演示一处可核对的改动：把鳍长均值差从雄减雌改为雌减雄。baseline.py与modified.py都是完整源文件，代码由AI编写或修改，数值由本地Python实际计算。Cursor任务文本仅供讲师演示准备，本轮没有在Cursor操作、调用其模型或生成界面截图，尚未取得教师审定。

打开code-change.diff可见修改范围。两个脚本使用同一CSV、同一筛选和同一统计定义，分别保存至baseline-output与modified-output；目录变更用于防止覆盖。差值的公式、字段名及打印字段一起修改，避免数字变了而标签未变。

用Python运行run_demo.py，可重新执行两份脚本，再调用check_results.py。执行器使用调用run_demo.py的同一个Python，不自动安装软件、不更改全局环境。run-evidence.json记录实际路径、版本、命令、时间、退出码与输入和脚本哈希，两个目录各保留summary.csv、comparison.csv、included_rows.csv及run.json。终端文本是实际进程输出；没有Cursor截图。

check_results.py从原始CSV重新选择记录并复算，检查146条纳入行、每组73条、两组均值和样本SD不变，以及差值方向反转。运行成功只能证明这份代码按本例条件得到相应描述统计，不能证明观测独立、研究设计或科学结论正确。Python与本地WebR的原有跨软件核对继续保留在../cross-tool；SPSS代码已提供但未执行。

Cursor编辑入口与Python解释器的职责可配合Section7第21页讲解：Cursor可读写代码、发起终端命令；解释器实际执行脚本。解释器指运行Python代码的软件。终端是输入命令、查看输出的位置。换编辑器不会自动改变数据含义，但工作目录、解释器、依赖或脚本版本不同，都可能影响执行。
