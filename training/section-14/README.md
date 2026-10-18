# Section 14 本地与云端Agent实际演示

16页，s14-r2。output为可编辑PPT；renders/s14-r2包含PDF及逐页PNG。页面以教学申报材料说明文件输入、运行事件、Word、同源Skill、Harness、Cloudflare与当前模型配置、后台自动执行、表达修订及失败处理。无课堂练习。

国外参考为CMU Generative AI 2025 Lecture 23，已查看物理页29、30、31、32、34、37。第2页使用第30页（印刷页35）完整原图，说明任务、动作与环境关系，不声称实现Mind2Web。产品功能分别查OpenAI与Cloudflare官方说明，具体项目范围据当前代码及实测记录。

demo/input与demo/output保留本轮通过本地8788服务实际运行的Grant、Paper、Patent材料与Word。申报及专利为教学模拟，论文为公开数据教学文字。脚本组织给定文字、检查约束并填入模板，不调用模型。来源台账核对的是给定身份和定位，未验证全部科学事实。

evidence/negative-cases.json为3种错误输入在真实文件执行器中的拒绝记录。targeted-tests.tap是12项定向测试，模型和存储使用夹具；不可称为全系统或云端模型联调。same-skills.json核对24份完整指令和当前云端包指纹，不能据此声称运行工具相同。源代码快照来自有未提交修改的当前工作区，独立保存在evidence/source-snapshot；未改动或代提交应用工作。

云端本轮只访问登录入口和公开health，确认deepseek-flash已配置、持久化已绑定、minimax停用。没有登录、调用模型、上传研究资料或部署变更。登录页面存在窄列显示，未称界面通过验收。本节课件未使用该截图。

build.mjs用Artifact Tool构建并最终检查；render.py用LibreOffice导出，check_delivery.py核对包、文件、哈希、来源图、原生表格、预览和记录。演示文件支持编辑，仍是草稿，没有研究者签核。未作Microsoft PowerPoint/Word原生应用测试。

collect_evidence.py会重新请求运行中的本地8788服务并更新本节证据，随后需重新渲染Word、构建PPT和核对哈希。复查既有交付只运行check_delivery.py，避免混入新的运行时间和文件版本。
