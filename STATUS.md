# 接手基线与当前状态（2026-10-17）

基线 Agent 9ea539b84b7ce50dbd666d220b43fc7b8b9dc259；Skills 16449ab74f1e55e99943d25c31cc1914f3fcb293。

Git HTTPS 连续失败。通过 GitHub API 下载源文件并逐个校验 blob、tree、commit SHA，恢复同一提交的浅检出，非重新初始化的替代历史。当前分支 feature/teaching-evidence-20261016。

基线自动测试：Agent 5/5，Skills 5/5。Agent 的模型响应测试使用注入 mock；不是 MiniMax 真实调用。24 项 Skill 均为指令定义，不能据此声称第三方脚本已接入。

环境：Codex CLI 0.124.0；Windows Microsoft YaHei 可用；内置 artifact-tool 用于全新 PPTX 构建。未发现 MINIMAX_API_KEY、Cloudflare 或 Gemini/Nano Banana 对应环境变量，未读取或记录其他密钥值。

实施后的逐项状态以 QA_REPORT.md、training/demos/ 和 training/deck-zh/ 的证据为准。云端部署、真实模型调用、完整现场彩排仍需外部条件。

当前增补：200页v11备课材料；Worker Token Plan适配、24项同源Skill、持久任务与模板Word工具；19项Node测试、真实Wrangler本地重启恢复。未配置MiniMax订阅Key，按用户要求暂不云部署，具体证据见QA_REPORT.md与docs/DEPLOYMENT.md。
