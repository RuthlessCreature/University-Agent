# 部署 Cloudflare Worker

1. 准备 Node.js 20+ 和已获批准的 Cloudflare/MiniMax 账号。
2. 安装依赖：`npm install`；运行：`npm test`。
3. 登录：`npx wrangler login`。
4. 注入密钥：`npx wrangler secret put MINIMAX_API_KEY` 和 `npx wrangler secret put WORKSHOP_ACCESS_TOKEN`。
5. 部署：`npm run deploy`；访问 `/health` 检查配置，再使用前端。

说明：Worker 不是本地 Codex 的 Bash 环境；未来文档解析和图像生成须连接隔离执行服务。
