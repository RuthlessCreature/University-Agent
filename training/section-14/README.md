# Section 14 本地与云端Agent实际演示

16页，s14-r3。output为可编辑PPT；renders/s14-r3包含PDF及逐页PNG。页面以教学申报材料说明文件输入、运行事件、Word、同源Skill、Harness、Cloudflare与当前模型配置、后台自动执行、表达修订及失败处理。无课堂练习。

国外参考为CMU Generative AI 2025 Lecture 23，已查看物理页29、30、31、32、34、37。第2页使用第30页（印刷页35）完整原图，说明任务、动作与环境关系，不声称实现Mind2Web。产品功能分别查OpenAI与Cloudflare官方说明，具体项目范围据当前代码及实测记录。

demo/input与demo/output保留本轮通过本地8788服务实际运行的Grant、Paper、Patent材料与Word。申报及专利为教学模拟，论文为公开数据教学文字。脚本组织给定文字、检查约束并填入模板，不调用模型。来源台账核对的是给定身份和定位，未验证全部科学事实。

evidence/negative-cases.json为3种错误输入在真实文件执行器中的拒绝记录。targeted-tests.tap是12项定向测试，模型和存储使用夹具；不可称为全系统或云端模型联调。same-skills.json核对24份完整指令和当前云端包指纹，不能据此声称运行工具相同。源代码快照来自有未提交修改的当前工作区，独立保存在evidence/source-snapshot；未改动或代提交应用工作。

云端本轮公开health返回200，报告deepseek-flash已配置、持久化已绑定、minimax停用。使用现有项目专用访问配置发起一次登录返回401，未取得会话、创建任务或调用模型。未更改密码、模型、密钥及部署。历史模型记录不能代替本轮任务，课件第11页写明当前范围。

build.mjs用Artifact Tool构建并最终检查；render.py用LibreOffice导出，check_delivery.py核对包、文件、哈希、来源图、原生表格、预览和记录。演示文件支持编辑，仍是草稿，没有研究者签核。未作Microsoft PowerPoint/Word原生应用测试。

collect_evidence.py会重新请求运行中的本地8788服务并更新本节证据，随后需重新渲染Word、构建PPT和核对哈希。复查既有交付只运行check_delivery.py，避免混入新的运行时间和文件版本。

2026-10-20复核：实际在浏览器点击生成申报草稿并截取含下载入口的页面，随后下载核对同次Word；论文和专利通过本地HTTP重新生成和下载。三份Word已渲染检查，分别2、1、1页。论文数字另从344条公开CSV独立复算，体重非缺失342条，三物种记录数与均值和Word相符；D1原教学定位保留，随包副本及对应说明见evidence/paper-facts-check.json。

24份完整指令随包保存在evidence/skill-instructions，独立检查与源快照中的Worker Skill包逐份一致。12项定向测试本轮实际重跑，模型和存储均为夹具，实际命令、退出码及TAP哈希见targeted-test-execution.json。3项文件异常本轮实际执行，原始失败run.json与未产生Word均检查。Harness第9页的5条原生连接起止节点已核对。

course-artifacts保存前节五类已有本地产物的18项文件快照和manifest，便于讲师现场打开。它们本轮只复制并核对哈希，没有重新执行第8至12节的全部任务。8788本地固定材料服务仍只支持申报、论文、专利三类，不把快照说成新增服务能力。Worker输出范围由代码说明，本轮未登录运行模型。

复查交付只需运行check_delivery.py（需要已准备的python-docx、pypdf等依赖），不需服务、凭据或私有.build目录。validation.json是本轮导出记录，读取记录不等于重跑页面分析。collect_evidence.py用于课程工作区重新采集真实本地输出；使用它前须先实际点击本地申报按钮，并同步更新截图和provenance，之后重新渲染、构建及核对。不要把新旧运行记录混在同一版交付中。
