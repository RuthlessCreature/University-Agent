# 本地与云端分别验收

2026-10-16，本地127.0.0.1:8788已实测接收HTTP请求，调用Python读取教学材料和Word模板，生成并下载Grant、Paper、Patent三份DOCX。记录在training/demos/http-smoke.json。模型调用次数为0，不是自主研究或在线检索演示。

Cloudflare新增ResearchRun Durable Object及配置，保存阶段、输入哈希、版本和审核记录。契约测试使用内存fixture，只检验状态转移、冲突和缺少绑定时的错误响应。未运行真实Cloudflare对象，未部署，不声称有可公开访问网址。前端的旧/api/run仍为文本模型示例；新/api/runs负责状态，不自动调用Office工具服务。

MiniMax官方兼容文档本次查到MiniMax-M3及https://api.minimax.io/v1。模型标识存在不代表账户有权限；本次没有MINIMAX_API_KEY，真实请求未执行。没有Cloudflare Secrets或Nano Banana/Gemini接口配置。不能用其他供应商的Key冒充这些接口联调。

下一项真实联调：由用户在运行环境注入MiniMax及Cloudflare Secrets，执行小额模型请求，部署Worker，检查Durable Object重启后状态和真实文件服务契约。账号机密不写入仓库或聊天。科研文档最终提交、专利查新与讲师全程彩排各需独立验收。

本地命令：node tools/serve-local.mjs。默认只绑定127.0.0.1，仅执行本仓库三个固定教学输入。不要直接暴露到公网；它不是多用户科研服务。
