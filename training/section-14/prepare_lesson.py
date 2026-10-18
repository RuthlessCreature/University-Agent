from pathlib import Path
import json
R=Path(__file__).resolve().parent
refs={
'cmu':{'short':'CMU Generative AI 2025，Lecture 23','title':'Aran Nayebi & Matt Gormley, Code Generation + LLMs / VLMs as Autonomous Agents, Nov. 19, 2025','url':'https://www.cs.cmu.edu/~mgormley/courses/10423-f25/slides/lecture23-code.pdf','location':'物理页29、30、31、32、34、37已查看；采用30页（印刷页35）的输入、动作及历史信息组织；不采用旧论文计数和模型排名'},
'cf':{'short':'Cloudflare Durable Objects官方文档','title':'What are Durable Objects? / Alarms','url':'https://developers.cloudflare.com/durable-objects/api/alarms/','location':'Background及alarm：持久状态与后台唤醒；应用层重试次数另据本项目代码'},
'skills':{'short':'OpenAI官方Skill说明；本地24份指令核对','title':'Skills / Build skills','url':'https://developers.openai.com/plugins/concepts/skills','location':'Skill由SKILL.md和可选脚本、资源组成；实际安装和完整内容比较见evidence/same-skills.json'},
'local':{'short':'本轮本地HTTP、文件与拒绝记录','title':'Section 14实际本地教学运行','url':'demo/output/grant/run.json','location':'evidence/local-http.json；demo/input；demo/output；evidence/negative-cases.json；固定材料，无模型调用'},
'cloud':{'short':'本轮云端健康接口与实际登录页','title':'科研工作台健康检查','url':'https://ikun.homes/health','location':'evidence/cloud-health.json；assets/cloud-health-actual.png；2026-10-18 UTC；仅健康与配置状态，不含本轮模型任务'},
'code':{'short':'当前工作区代码快照；12项定向夹具测试','title':'项目工作流、模型、编辑与导出实现','url':'evidence/source-snapshot/','location':'automatic.js、model.js、workflows.js、writing.js、projects.js；targeted-tests.tap。工作区有未提交应用修改，快照哈希见provenance.json；测试模型与存储使用夹具，不能当作云端联调'}
}
rows=[
('本地与云端Agent实际演示','以教学申报材料为例，沿着输入、执行记录和结果文件，查看每一步究竟完成了什么。','overview','本地固定材料流程已执行；云端本轮只核对入口和健康状态。',['local','cloud'],
'本节将前面讲过的Skill、工作流和Harness放回实际材料中。演示对象是“公开文献筛选与核验流程”的教学申报材料，非真实基金申请。先看本地文件服务如何把给定材料放进模板，再看云端的承载方式、状态记录和工具范围。提醒听众区分写作建议、实际工具动作与生成的文件。页面里的本地与云端不是两套科学结论；它们只是运行位置和可用工具不同。'),
('Agent的动作与环境反馈','模型给出下一步动作后，系统还要执行动作、读取结果，并据此决定后续步骤。','reference','原课件用于解释输入与动作关系；本项目没有实现图中的Mind2Web系统。',['cmu'],
'CMU 2025年Lecture 23物理第30页展示Mind2Web的候选元素、排序模型、预测模型、目标元素和操作。这里只借它说明：任务和前序动作会影响下一步选择，动作必须落到具体环境。课堂用“读模板—填章节—检查文件”替换网页操作细节。不能因课件介绍浏览器Agent，就说本项目已经有自主浏览器；当前Worker的检索、模型和文件生成能力必须分别核对。'),
('申报演示的三份输入','这次输入是教学指南、已有研究设想和Word模板，三者各有不同用途。','inputs','指南编号TEACH-GRANT-01为课程自编，不能当作当年官方基金指南。',['local'],
'打开demo/input/grant可见guide.json、grant.json和template.docx。教学指南要求12个月内形成可复算流程、评价召回与耗时并保留人工判断。材料提供研究目标、六节已有内容及来源编号；模板决定这些内容落到哪里。本地程序不从任意PDF理解指南，也不凭空撰写研究设想。讲师逐项展示输入，让听众知道输出中的句子原先来自哪里。真实申请须换用对应项目当期官方指南及申请人材料。'),
('本地页面到Word的实际操作','点击“生成申报草稿”后，页面实际调用本地文件程序，并提供可下载的Word。','screenshot','这是本轮实际页面截图；固定材料流程没有调用外部模型。',['local'],
'本轮启动8788服务，点击生成申报草稿，页面由读取材料与模板转为“草稿已生成”，出现可编辑Word链接。配图是浏览器实际截图，没有绘制假的执行界面。后续另通过HTTP下载检查了文件哈希。本地演示主要帮助老师理解文件到文件的执行链，不能说它已经自主提出科学问题或查完文献。课程包保留了本轮输入、输出、运行事件和问题清单，课前可重新执行。'),
('本次运行经过的四个环节','运行记录说明程序做了哪些检查；研究方案中的技术路线另有自己的内容。','trace','运行事件与研究技术路线分开读，避免把流程完成误解为科研完成。',['local'],
'grant的run.json记录intake、constraints、outline和docx四个事件。其含义依次是读取输入，检查指南和章节，记录仍需研究者审阅，写入Word。outline的状态为human_review_required，不能改讲成研究者已签核。另一个route.mmd描述教学研究方案中的“材料准入—独立参考答案—固定任务比较—错误分析—人工复核—报告”，它是拟开展研究的路线，不能当成本次程序已完成这些研究步骤的日志。'),
('指南要求与产物的对应','把每条指南要求连到研究目标、交付材料和检验办法，便于检查遗漏。','mapping','映射检查能发现缺项；是否科学可行仍需读具体内容。',['local'],
'本地程序比较指南和材料中的requirements是否一致，并检查每项要求是否关联已有目标，是否写明产物及检验方式。本例R1关联G1，交付代码、依赖、输入和日志；R2关联G2，保存逐条筛选记录及统计报告；R3关联G3，交付Word草稿、来源账本和审核记录。指南中“12个月”是模拟项目安排，不是已经完成12个月研究。程序核对的是对应关系存在与内容一致，没有验证研究设计一定有效。'),
('Word草稿与尚缺的证据','文件已经生成；团队基础、真实查新和研究者签核仍列在问题清单中。','word','教学文字来自给定材料；没有补写团队成果、实验结果或真实签核。',['local'],
'展示实际生成的Word第一页和issues.json。六节内容按模板填入，每节带材料来源，文末保留来源与未决问题。本例缺口有：未提供真实团队基础，未完成真实文献查新与科学可行性审查，未获得研究者签核。技术路线和考核指标可以先组织成草稿，但缺口不能靠润色消失。这里的来源账本只保存给定身份和定位；它没有自动读取所有原始论文来证明每一句科学主张。'),
('本地与Worker中的同源Skill','24份基础Skill的指令内容已逐份比较，云端健康接口报告的包指纹也与本地一致。','same','相同指令便于统一要求；工具、模型与运行结果仍需分别检查。',['skills','cloud'],
'本轮读取University-Skills、工作区安装目录、Agent仓库安装目录及生成的Worker Skill包，统一换行后逐份比较完整内容和SHA256，24份全部一致。云端健康接口返回的包指纹也与skills-lock一致。Skill是办事规则，可带脚本和资源；本课程这24份主要是指令规范。指令里写“查文献”不会自动增加浏览器或数据库账号，写“绘图”也不等于云端已执行绘图代码。同源是可核对的文件事实，不是能力等同保证。'),
('Harness怎样管理一次任务','Harness是任务周围的执行管理：提供工具，保存过程，并处理失败和继续运行。','harness','记录包含输入、输出与版本；程序完成状态仍需与科研结论分开。',['cmu','code'],
'用“执行管理”解释Harness：研究者给目标和材料，模型决定或按工作流处理当前步骤，工具实际读取或写入文件，管理程序保存结果并选择继续、重试或结束。模型本身不会因为写出“已保存”就真的在硬盘产生文件。本地Codex可以使用当前授权的文件和代码工具；本项目Worker只使用已接入的接口与导出工具。讲师指着回路解释每次反馈来自哪里，避免把Harness讲成另一个神秘大模型。'),
('Cloudflare承载的工作流结构','浏览器提交任务，Worker接收请求；持久任务对象保存节点，按步骤调用模型或导出文件。','architecture','这里是依据代码绘制的结构图；不是云端任务执行截图。',['cf','code'],
'Cloudflare Worker承载入口和接口；Durable Object在这里可以理解为每个任务的持久档案与执行状态。浏览器读取进度，后台alarm唤醒后继续下一节点。模型服务返回文字，项目代码另做检查与文件生成；Worker本身不是模型。图中云端模型按本轮健康接口显示为DeepSeek deepseek-flash，MiniMax只保留旧配置且停用，不参与执行或回退。图的箭头说明当前实现关系，不代表本轮已经完整重跑了云端任务。'),
('云端入口与模型配置的核验','本轮可打开登录页；健康接口返回DeepSeek已配置、持久化已绑定、MiniMax停用。','cloudstatus','健康检查不能证明某次模型回答正确，也不能替代完整任务演示。',['cloud'],
'依据本轮实际健康响应，在页面用中文解释检查结果：ok是服务响应，model_configured表示配置检查通过，persistence_bound表示绑定存在，inactive_providers中有minimax。没有显示密码或密钥，没有登录用户账户，也没有发起本轮付费模型调用。当前界面与配置事实可以复核；2026年10月17日已有云端测试记录属于历史记录，讲师若演示当天新任务，应使用当天的运行记录，而非把旧记录当作实时响应。'),
('一次提交后的后台执行','网页负责展示状态，后台按节点保存结果，再继续下一步；刷新页面无需逐节点确认。','automatic','此页讲当前代码的自动流程；12项定向测试使用模型和存储夹具。',['cf','code'],
'当前自动流程先处理需要的检索，再依次执行节点，最后导出文件。每一步结束后保存输出，并安排下一次alarm；页面轮询读取状态。应用代码对失败节点自动重试一次，再失败则停止并显示错误；这与Cloudflare平台alarm抛异常的重试机制不同，不混讲次数。由于已完成结果在任务存储中，关闭页面不应等同取消任务。这个行为本轮通过夹具测试检查，没有通过本轮真实云端模型任务再次验证。'),
('节点文字修订与事实保留','表达修订后，程序比较数字、来源编号和章节结构；研究者还需检查语义有没有变化。','editing','机器比对能够发现部分改动，不能证明文字已达到学术要求。',['code'],
'当前代码先生成节点内容，再自动修订表达，并检查数字、来源和章节。定向测试用342条记录与均值3700.7 g验证数字改变会被拒绝，用D1变成D2验证来源改变会被拒绝。它们是自编测试夹具，不是科研结果。数字完全一样时，也可能把相关性改成因果，或把拟开展写成已完成，因此还要逐句读。Humanizer的目标是让具体读者读懂对象、动作和结论，不是给文字一个“绝无AI味”的程序保证。'),
('错误输入的实际拒绝结果','故意改变教学输入后，文件程序拒绝未知来源、指南不一致和未签核正式导出。','failures','这三项实际跑过文件执行器；不等于已经测试了网络、模型或全部故障。',['local'],
'本轮复制教学输入并作三种小改动，分别运行真实文件执行器。来源改成NOT-A-SOURCE，返回unknown_source；修改指南对应要求，返回guide_requirement_mismatch；直接要求final而未签核，返回final_export_blocked。错误记录在每个案例的run.json中保存。这里检查的是本地固定材料执行器；网页自动草稿无需逐节点人工确认，二者不是同一个提交关口。不能为了看起来流程完整而编造人名、批准事件或把失败节点涂成绿色。'),
('五类任务的当前输出范围','任务入口决定组织材料的顺序，真正交付什么还取决于该运行端接入了哪些工具。','capabilities','本轮实际下载了本地申报、论文、专利三份Word；配图与结题按代码范围说明。',['local','code'],
'本地8788服务实际支持Grant、Paper、Patent固定材料到Word，本轮分别下载并核对文件。当前Worker代码中的申报、论文、专利导出Word；figures整理绘图方案Markdown，没有执行绘图代码；closeout导出结题草稿Markdown。前面课程中真实CSV图是本地数据计算与图表制作，不能转述成云端已自动画完。Nano Banana没有对应服务，本节不能放假的调用截图。讲师可据这个表回答“能不能做”的问题，先说明运行位置再说明输出。'),
('可复查的演示材料包','保留这次用的材料、指令版本、运行结果和问题清单，下一次才能检查变化来自哪里。','archive','实际授课前复查服务、模型和文件；保留未核验项，不把旧记录说成现场运行。',['local','cloud','code'],
'最后沿本例档案回看：输入有指南、材料和模板；规则有Skill版本和程序快照；过程有本地事件、HTTP与失败记录；结果有Word、来源账本和问题清单。下次改模板或输入，应生成新记录并重新检查。示范本地时无需登录云账户；示范云端时应明确公开教学材料的传输范围，并查看当天节点和结果。对真实科研资料另按授权处理。课程帮助教师判断AI做了什么、证据在哪里，科学问题、事实核对与正式提交仍由研究者负责。')]
lesson=[dict(n=i,title=t,thesis=th,kind=k,bottom=b,refs=rs,notes=no) for i,(t,th,k,b,rs,no) in enumerate(rows,1)]
(R/'lesson.json').write_text(json.dumps(lesson,ensure_ascii=False,indent=2)+'\n','utf-8')
(R/'sources.json').write_text(json.dumps(refs,ensure_ascii=False,indent=2)+'\n','utf-8')
(R/'讲师稿.md').write_text('# Section 14 本地与云端Agent实际演示\n\n'+''.join(f"## {d['n']:02d} {d['title']}\n\n{d['notes']}\n\n" for d in lesson),'utf-8')
print('Prepared 16 slides and notes')
