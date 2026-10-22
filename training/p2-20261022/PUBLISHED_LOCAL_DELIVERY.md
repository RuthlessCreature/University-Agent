# Yusuf本地工作流交付

用户已明确将模型接口配置留待后续，本阶段交付本地文件、运行器、模板、示例与SOP。

总入口位于配套University-Skills仓库的skills/yusuf/SKILL.md。提示词出现【Yusuf】、【Yusuf，…】、【Yusuf...】或【Yusuf帮我…】等标记时，读取该Skill并选择对应科研任务。先安装或显式读取Skill；标记本身不会给其他Agent新增工具或权限。

两个仓库放在同一父目录，保持University-Skills和University-Agent名称。运行University-Skills/tools/install_local_skills.py，可将24个基础Skill及Yusuf总入口安装到该父目录.agents/skills。不会修改全局模型与Key；已有不同版本时停止，不强制覆盖。

## 可检查材料

- examples：Grant、Paper、Patent、Figure各三组任务，包含PROMPT.md、input和task.json。
- templates：公开模板原件、取得方式、来源及指纹。PLOS原件为LaTeX，课程Word另有标识。
- output：总SOP、分节点SOP、12组示例提示词与模型验收边界。
- word-work：模板填写所用的保留副本。
- evidence：已有本地工具输出和检查记录，不代表Provider执行成功。

## 本地使用

先运行University-Skills/tools/task_preflight.py检查所选task.json；报告须写入新的文件。复演准备好的教学草稿及CSV，可运行University-Skills/tools/local_file_demo.py并指定新的--output目录，需要Word页面图时加--render。

具体参数、依赖和模型边界见University-Skills/docs/LOCAL_RUNNER.md。Word导出需要python-docx和lxml；渲染需要准备好的文档渲染脚本、LibreOffice、Poppler和pypdf；图件需要ReportLab与Node/sharp。仓库不包含第三方软件安装程序。

本地交付已在独立目录实际执行，生成申报5页、论文2页、交底4页和真实数据图。12组文件检查与67项源码测试通过；文档页面和图件已有审查记录。历史R4审计中的模型访问缺口仍保留，不能据此宣布完整P2模型验收已通过。

公开原件、教学模拟、研究假说、AI草稿与实际执行分别标注。未提供真实团队、发明人、权属或完整科学证据的地方保持待确认，不投稿、不提交申请、不签名、不部署云端。
