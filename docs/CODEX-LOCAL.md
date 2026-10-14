# Codex 本地科研 Skill 加载

两个仓库需要放在同一级目录：

- University-Skills/：技能定义和来源、测试
- University-Agent/：本地安装器及 Cloudflare 演示端

在 University-Agent 下执行：

node tools/install-skills.mjs --source ../University-Skills --target .agents/skills --dry-run

检查输出后，再正式安装：

node tools/install-skills.mjs --source ../University-Skills --target .agents/skills

只安装课堂必要的一组：

node tools/install-skills.mjs --source ../University-Skills --target .agents/skills --only research-intake,document-parsing,grant-template,grant-research-content,grant-technical-route,claim-audit,academic-humanizer

覆盖旧版本时必须明确加 --force。默认不覆盖；复制文件不自动运行脚本或调用 API。

安装只是让 Codex 识别 Skill 指令，不代表第三方 PDF、论文、图像 API 已配置，也不能证明科研结果正确。讲课时先使用隔离演示目录和脱敏材料。
