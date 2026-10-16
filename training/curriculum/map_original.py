import pathlib,json
R=pathlib.Path(__file__).resolve().parent;topics=json.loads((R/'original_topics.json').read_text('utf-8'));ss=json.loads((R.parent/'deck-zh/slides_manifest.json').read_text('utf-8'));by={s['id']:s for s in ss}
links=['O02','O01,O02','M101','M102','M102','M102,M213B','M102','M202','M203,M322','M201','M201,M207','M102,M203','M204,M205','M205,E02','M202,E01','M207,M208','M207,M208','M314,M334','M208,E05','M213,M213B','M209,E03','M212','M213B','M210,M331,M332','M301','M301,M302','M302,E02','M305,M306','M302,E06','M307','M301,M306','M331,M333,M334','O02,M304','M324','M324,E11','M305,M307','M307','M311,M313','M313,M314','E08','M317','M318','M316,M307','M402','M402,M404','M401,M404','M401,M405','M321,M323,M325','M403,M405','M405','M403,M405','Z01,Z02']
assert len(topics)==len(links)==52
out='# 客户原稿逐条对照\n\n来源：客户截图及 .doc 中的52条正文项目。已删除联系人和机构推广。原稿中的自动化承诺按科学与工程边界讲授，不能照搬为已实现功能。\n\n|序号|客户原稿项目|课件位置|处理说明|\n|---|---|---|---|\n'
notes={1:'Nature当前网页已核验；Science页面403，列为未核验。',2:'作为讨论观点，删除“必然取代”的无证据断言。',7:'保留工具候选，不把旧产品偏好当作永久能力结论。',9:'论文、预印本和专利分别核对，未执行跨库实时趋势预测。',10:'四维原名保留；评分依据需说明，不虚构客观量化分数。',17:'样本量与参数需设计依据，不能自动称最优。',18:'原生结构图和Mermaid已生成；Draw.io外部集成未实测。',20:'Python已执行；R仅提供源码。',23:'Python已复算；R及SPSS未执行。',24:'生成图后仍需目标期刊与科学审查，不承诺可直接投稿。',28:'本地证据与问题检查；没有真实专业评审。',30:'按作者指南与证据适配，不模仿期刊腔。',32:'保留机制示意教学主题，新增Nano Banana；图像API未配置。',43:'不冒充基金委评分，展示结构预审与未决问题。',48:'真实本地交底草稿；未完成法律查新。'}
for i,(t,ids) in enumerate(zip(topics,links),1):out+=f'|{i}|{t}|'+', '.join(f'{k} p{by[k]["page"]}' for k in ids.split(','))+'|'+notes.get(i,'已列入具体教学页；实现状态见QA报告。')+'|\n'
(R/'CLIENT_ORIGINAL_52_ITEMS.md').write_text(out,'utf-8')
print('52/52 original items mapped')
