from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent;A=R.parents[1];rev='s14-r2'
ppt=R/'output'/f'高校科研AI课程_Section14_本地与云端Agent实际演示_{rev}.pptx'
sha=hashlib.sha256(ppt.read_bytes()).hexdigest()
p=A/'training/curriculum/section-progress.json';d=json.loads(p.read_text('utf-8'));d.update(checked_date='2026-10-18',produced_pages=240,next_section=None)
d['scope']='登记Section 0—14实际产物，不表示教学验收或整体交付审查已完成。Section 0一致性复核、全课程覆盖与时长复核仍待处理。'
s=d['sections'][14];s.update(status='produced_for_review',revision=rev,pptx=str(ppt.relative_to(A)).replace('\\','/'),sha256=sha,checks='training/section-14/checks.json')
p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n','utf-8')
p=A/'training/curriculum/各Section讲授清单.md';t=p.read_text('utf-8').replace('Section 0—13已形成224页交付文件供审阅；Section 14待制作。Section 0仍需按新增要求做一致性复核。','Section 0—14已形成240页交付文件供审阅。Section 0一致性、全课程覆盖与时长仍需复核。');p.write_text(t,'utf-8')
refs=json.loads((R/'sources.json').read_text('utf-8'))
(R/'参考资料与采用范围.md').write_text('# Section 14 参考资料与采用范围\n\n'+''.join(f"## {k}\n\n{v['title']}\n\n{v['url']}\n\n{v['location']}\n\n" for k,v in refs.items())+'CMU原课件共41页，采用物理第30页（印刷页35）完整原图。第29页的2021—2023论文计数未采用；第34页标记示例与第37页SeeClick仅用于了解讲授组织，未引入其性能结论。底层论文图不代表本项目实现。\n\n本轮云端浏览器可打开登录页并读取健康JSON；命令行HTTP检查超时，未将超时解释成服务停机。登录页截图出现窄列排版，未用作课件展示，也未宣称云端界面通过视觉验收。健康原始字段与截图保留，不含密钥。本节没有执行新的云端模型任务。\n','utf-8')
(R/'课程覆盖定位.md').write_text('# Section 14 课程覆盖定位\n\n|客户主题或追加要求|本节定位|实际范围|\n|---|---|---|\n|本地执行、文件演示|3—7页|固定教学材料、真实HTTP和Word|\n|同源Skill、Agent与Harness|2、8—9页|原课件关系图、24份内容比较与可编辑回路|\n|Cloudflare与模型接入|10—12页|当前结构、健康状态及后台代码；MiniMax停用|\n|Humanizer与事实保留|13页|修订流程及数字、来源的夹具检查|\n|失败处理与核验|14页|3种错误输入实际拒绝，保留执行边界|\n|论文、申报、专利、图表与结题|15页|按运行端说明当前输出，不冒称工具接入|\n|收尾演示与核验|16页|输入、程序、过程与文件归档|\n\n原客户四模块与原截图定位仍保留于课程覆盖矩阵；本表只登记新课件的实际页面，不把旧页码当作教学验收。无课堂练习。\n','utf-8')
(R/'README.md').write_text('''# Section 14 本地与云端Agent实际演示

16页，s14-r2。output为可编辑PPT；renders/s14-r2包含PDF及逐页PNG。页面以教学申报材料说明文件输入、运行事件、Word、同源Skill、Harness、Cloudflare与当前模型配置、后台自动执行、表达修订及失败处理。无课堂练习。

国外参考为CMU Generative AI 2025 Lecture 23，已查看物理页29、30、31、32、34、37。第2页使用第30页（印刷页35）完整原图，说明任务、动作与环境关系，不声称实现Mind2Web。产品功能分别查OpenAI与Cloudflare官方说明，具体项目范围据当前代码及实测记录。

demo/input与demo/output保留本轮通过本地8788服务实际运行的Grant、Paper、Patent材料与Word。申报及专利为教学模拟，论文为公开数据教学文字。脚本组织给定文字、检查约束并填入模板，不调用模型。来源台账核对的是给定身份和定位，未验证全部科学事实。

evidence/negative-cases.json为3种错误输入在真实文件执行器中的拒绝记录。targeted-tests.tap是12项定向测试，模型和存储使用夹具；不可称为全系统或云端模型联调。same-skills.json核对24份完整指令和当前云端包指纹，不能据此声称运行工具相同。源代码快照来自有未提交修改的当前工作区，独立保存在evidence/source-snapshot；未改动或代提交应用工作。

云端本轮只访问登录入口和公开health，确认deepseek-flash已配置、持久化已绑定、minimax停用。没有登录、调用模型、上传研究资料或部署变更。登录页面存在窄列显示，未称界面通过验收。本节课件未使用该截图。

build.mjs用Artifact Tool构建并最终检查；render.py用LibreOffice导出，check_delivery.py核对包、文件、哈希、来源图、原生表格、预览和记录。演示文件支持编辑，仍是草稿，没有研究者签核。未作Microsoft PowerPoint/Word原生应用测试。

collect_evidence.py会重新请求运行中的本地8788服务并更新本节证据，随后需重新渲染Word、构建PPT和核对哈希。复查既有交付只运行check_delivery.py，避免混入新的运行时间和文件版本。
''','utf-8')
print('Registered 240 produced pages; acceptance and course-wide audit remain open')
