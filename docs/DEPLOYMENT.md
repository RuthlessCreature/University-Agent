# Worker 与 MiniMax Token Plan 部署

当前版本已完成 Wrangler 构建检查和本地 Worker 运行时验证。按用户本轮要求，先交付可部署版本；没有部署到云端，也没有填入 MiniMax 订阅 Key。

## 版本与接口

- Worker 入口：`src/index.js`；持久任务：`ResearchProject` Durable Object。
- 模型固定为 `MiniMax-M3`；计费模式为 `token-plan`。
- 国内兼容地址：`https://api.minimax.cn/v1`。国际账号需按账号对应官方文档显式修改地址，不自动切换。
- 模型密钥：`MINIMAX_TOKEN_PLAN_KEY`。普通按量 Key 不会被自动当作订阅 Key 使用。
- 访问口令：`WORKSHOP_ACCESS_TOKEN`。浏览器不接触 MiniMax Key，不把工作台口令存入 localStorage。

官方配置依据（2026-10-17读取）：[订阅 Key 说明](https://platform.minimax.cn/docs/m-plan/quickstart)、[OpenAI兼容文档](https://platform.minimax.cn/docs/api-reference/text-openai-api)。订阅 Key 与按量 Key 不通用；本项目保留用户指定的 M3，不随文档推荐自动换成其他模型。

## 构建与部署命令

```powershell
npm ci
npm test
npm run deploy:check
npx wrangler login
npx wrangler deploy
npx wrangler secret put MINIMAX_TOKEN_PLAN_KEY
npx wrangler secret put WORKSHOP_ACCESS_TOKEN
```

Secret 命令会在终端提示输入，密钥不要写入仓库、截图或聊天。首次部署后，在服务配置齐全前，模型接口会返回配置错误；没有访问口令时，任务接口拒绝运行。确认Secret配置完成，再使用真实授权材料测试。

本机预览使用 `npx wrangler dev --local --port 8789`。当前 `.dev.vars` 仅放一个本地教学测试口令，没有模型 Key，不应直接用作生产口令。旧的本地 Python 文件服务在8788，二者执行范围不同。

## 与本地 Codex 使用同一套 Skill

`tools/sync-shared-skills.mjs` 从锁定的 Skills Git 提交读取24份完整 SKILL.md，写入本地 `.agents/skills/` 和 Worker 的 `src/generated/skill-pack.js`。它拒绝未提交的技能改动；已有安装内容若不一致，也会报错。`skills-lock.json` 记录每份文件哈希、提交和包指纹。

```powershell
npm run skills:sync
npm test
```

测试逐字比较本地文件和Worker实际提示内容。Skill相同只说明指令同源。Python、搜索、PDF/OCR、图像生成等工具的可用性仍须分别实现与验收；当前Worker只接入模型文本处理与受约束DOCX填充，不能自行执行Python或上游科研脚本。

## 用户可见的工作流

Grant：材料清点→要求映射→研究内容→技术路线→综合审查→DOCX工具写入。

Paper：材料审查→IMRAD大纲→主张核验→专业表达→模拟审查→DOCX工具写入。

Patent：技术事实→发明人追问→交底框架→附图结构→专业审核→DOCX工具写入。

每一模型阶段单独执行。返回结构、来源编号和章节限制通过后，保存输出哈希并等待研究者确认；确认绑定输入与输出版本，才允许进入下一阶段。模型意见不自动成为科学核验结果。最后写出的是带来源和未决问题的Word草稿，没有正式提交接口。

Figure与Closeout目前展示工作流定义。Figure的真实数据图在本地课件构建中执行，云端没有连接Nano Banana；Closeout云端文档适配尚未完成，页面不会提供假成功记录。

## 输入支持与恢复

当前接受明确的JSON材料、Grant独立JSON指南及120KB以内的DOCX模板；不接收任意PDF或OCR输入。正文标记为独立文字片段中的 `{{章节标题}}`，章节名称与输入一致。真实复杂模板需额外适配和渲染检查。

任务记录保存在Durable Object，阶段输出与模板分别存储。刷新后输入任务ID和口令可以恢复。请求携带当前版本，重复或过期操作被拒绝；中断超过3分钟的running阶段可以恢复后重试，旧响应不能覆盖新版本。当前使用课堂共享口令，未实现多人身份认证和细粒度项目权限，部署给正式团队使用前需要补上。

## 配置完成后的真实联调

先使用教学例验证一次M3响应，保存模型名、使用量与实际阶段输出；再逐项确认来源和模板章节。审核每个阶段后导出Word，核对下载哈希、正文与原模板，并独立渲染。故意改动指南、删除来源、提交过期版本、模拟接口超时，检查是否停在正确阶段。

本地夹具测试验证了这些契约和文档字节处理，不代表MiniMax或Cloudflare云实例已经联调。真实联调记录应另存，并标明环境和运行版本。
