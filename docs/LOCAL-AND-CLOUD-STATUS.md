# 本地、Worker与模型分别验收

2026-10-17更新。Python教学服务在127.0.0.1:8788实际接收HTTP请求，处理教学材料和Word模板，生成并下载Grant、Paper、Patent三份DOCX。记录在training/demos/http-smoke.json；模型调用为0。

Worker预览在127.0.0.1:8789，通过Wrangler真实本地运行时使用ResearchProject Durable Object。已实际创建三个任务，检查缺少订阅Key与提前导出被拒绝，并验证进程重启后输入与版本保持。记录在evidence/wrangler-local-smoke.json。这是本地运行证据，尚不是Cloudflare云实例。

Worker模型阶段读取与本地Codex相同的24份完整Skill。技能提交、文件哈希和包指纹在skills-lock.json；测试逐字核对本地安装文件与实际云端提示内容。Python、搜索、PDF/OCR与图像工具仍需分别接入，不能因Skill相同而假称能力相同。

模型配置固定MiniMax-M3、token-plan和国内官方兼容地址api.minimax.cn/v1。使用独立的MINIMAX_TOKEN_PLAN_KEY Secret，普通按量Key不自动代入。Key尚未配置，未作真实模型调用。按用户要求，本轮只交付可部署版本，执行dry-run而不发布。

Worker的受约束DOCX填充工具已在Node中真实处理三份模板，产物位于各案例worker-tool目录。阶段模型响应与完整状态链测试使用明确的夹具，不能当作MiniMax联调。Figure的16张真实数据图已在本地PPT构建中生成；Nano Banana未接入，Closeout云端文件适配也尚未完成。

部署命令、Secret、输入格式、恢复与真实联调步骤见DEPLOYMENT.md。讲师完整授课彩排、科学结论审查与正式科研提交继续独立验收。
