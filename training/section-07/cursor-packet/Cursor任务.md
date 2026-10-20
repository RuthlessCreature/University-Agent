# Cursor中的讲师演示任务

AI编写的教学任务，本轮未在Cursor提交或执行。先用编辑器打开cursor-packet文件夹，查看baseline.py和penguins.csv，再将以下任务提供给Agent。文件修改与终端执行是否可用，以当前Cursor入口、运行模式及权限为准。

请先说明baseline.py读取哪个数据文件、保留哪些记录、结果保存在哪里。保持原始CSV和基线脚本不变，在modified.py中把鳍长均值差改成female减male，同时将结果字段名改为female_minus_male_mm，打印输出也使用该字段。输出单独保存至modified-output，避免混用基线结果。

保留species为Adelie、性别为female或male、鳍长完整的筛选条件；分组、样本标准差及单位不变，不新增P值或因果结论。先展示代码差异，逐项说明修改涉及输出目录、差值公式与字段名。

执行前报告实际工作目录及Python解释器路径和版本。用同一个Python解释器分别运行两个文件，保存命令、退出码和输出。比较CSV纳入行、两组n、均值和样本SD；这些应保持一致。检查差值从male减female改为female减male，并回到原CSV独立复算。没有运行权限、解释器不可用或文件生成失败时，如实报告，不写运行成功。

讲师同时查看差异文件、两次run.json和新生成的结果CSV，不把聊天中的成功文字当作运行证据。这个过程由讲师展示，不布置学员练习、安装或文件提交。
