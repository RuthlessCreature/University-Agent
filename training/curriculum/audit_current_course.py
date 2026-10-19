"""Inventory actual decks and publish a manually assessed original-topic mapping.
Page/file checks are automatic; coverage judgments below are editorial assessments.
"""
from pathlib import Path
import json,hashlib,zipfile,re,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parent;A=R.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,s):p.write_text(s.rstrip()+'\n','utf-8')
def dump(p,d):write(p,json.dumps(d,ensure_ascii=False,indent=2))
d=json.loads((R/'section-progress.json').read_text('utf-8'));s=d['sections'][0];f=A/'training/section-00/output/高校科研AI课程_Section0_s0-r4.pptx'
s.update(revision='s0-r4',pptx=str(f.relative_to(A)).replace('\\','/'),sha256=sha(f));s.pop('pending_consistency_review',None);s['consistency_review']='2026-10-19：已去除旧课堂练习安排，补查Berkeley 2025具体页面，修订课程导图。'
d['checked_date']='2026-10-19';d['scope']='240页实际文件已登记；Section 0一致性修订已完成。52条原稿主题覆盖仍有部分缺口，时长为备课分配，未作真人彩排；不代表用户教学验收。';dump(R/'section-progress.json',d)
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'};pages={};inventory=[];offset=0
for s in d['sections']:
 p=A/s['pptx'];assert sha(p)==s['sha256']
 with zipfile.ZipFile(p) as z:
  for n in range(1,s['page_budget']+1):
   x=ET.fromstring(z.read(f'ppt/slides/slide{n}.xml'));bodies=x.findall('.//p:sp/p:txBody',ns);shapes=[''.join(x.itertext()) for x in bodies];title=shapes[1] if len(shapes)>1 else shapes[0];text='\n'.join(x.itertext());key=f'{s["id"]}/{n}';pages[key]={'section':s['id'],'page':n,'global_page':offset+n,'title':title,'text':text,'pptx':s['pptx'],'pptx_sha256':s['sha256']}
   inventory.append({'section':s['id'],'page':n,'global_page':offset+n,'title':title,'images':len(x.findall('.//p:pic',ns)),'charts':len(x.findall('.//{http://schemas.openxmlformats.org/drawingml/2006/chart}chart')),'connectors':len(x.findall('.//p:cxnSp',ns)),'native_tables':len(x.findall('.//a:tbl',ns))})
 offset+=s['page_budget']
assert offset==240
# Rows were located using current titles, slide text and prior section materials; no keyword score is used.
rows=[
('1/11','部分覆盖','Nature与PLOS政策已有对照；Science当前政策尚未核验，需补原始来源。'),
('1/6 2/17','调整讲法','改讲任务能力、证据与作者责任，未把“必然取代”当作事实。'),
('1/7 1/8 2/10','已有对应内容','任务、材料、约束、产物与迭代均有位置；不承诺提示词保证正确。'),
('1/9 5/8 5/9 5/10','已有对应内容','工具用途、检索及引文回查；不是账户操作教学。'),
('1/9 2/6','部分覆盖','通用助手与产品侧重已讲；Claude、ChatGPT、DeepSeek的具体选择示例需再补齐。'),
('7/21 14/15','部分覆盖','Python实际计算与文件交付已有；Cursor及R的衔接示例仍不足。'),
('1/9 2/6 2/18','调整讲法','按任务、材料、工具与权限选择；不把原稿品牌偏好当作永久能力结论。'),
('4/2 4/10','已有对应内容','区分证据层次、覆盖与热度，不把预测当作确定结论。'),
('4/2 5/3 5/6 11/4','部分覆盖','论文、检索记录与专利检索分别讲授，尚缺将三类材料放在一起的趋势比较示例。'),
('4/9 4/12','已有对应内容','四维比较保留；判断依据需明确，未伪造客观分数。'),
('4/4 4/8 6/3','已有对应内容','问题收窄、假说和反证条件均有具体说明。'),
('5/7 5/8 5/9 5/10 5/11','已有对应内容','按关键词、语义、引文追踪和原文回查解释工具组合。'),
('5/15 5/16 5/17 5/24','已有对应内容','两篇全文比较与证据表；不声称任意PDF自动解析已接入。'),
('5/17 5/18 5/19','已有对应内容','区分对象、设计与测量差别，检查是否真的存在结论矛盾。'),
('4/7 5/22','已有对应内容','研究空白需要反证检索与范围限制，不能由少量检索自动定论。'),
('4/11 6/13 6/14','已有对应内容','资源约束、比较方案与备用路径明确。'),
('6/4 6/5 6/9 6/10 6/11','已有对应内容','变量、对照、组合与样本量依据均说明；无“自动最优”保证。'),
('8/11 8/12 8/13 8/15','已有对应内容','节点、条件、并行汇合及draw.io编辑源；自动化文字仍需核对。'),
('6/14 10/16','已有对应内容','风险与失败触发条件、替代方案有对应位置。'),
('7/21 7/22','部分覆盖','自然语言任务与实际Python脚本已对应，R代码版本未完成。'),
('7/3 7/5 7/6 7/7','已有对应内容','原始表、缺失、分母、过滤与异常复核有实际数据例子。'),
('7/10 7/11 7/12 7/15','已有对应内容','按研究问题、独立性、测量及统计假设选择方法，不承诺唯一最优检验。'),
('7/21 7/22','部分覆盖','缺少同一分析的SPSS/R/Python三份代码交付及各自运行状态。'),
('8/2 8/3 8/6 8/7 8/15','已有对应内容','真实数据图、图注与编辑源齐备；是否适合投稿仍按期刊核对。'),
('7/12 7/15 7/18 7/20','已有对应内容','结果解释、混合组成与科研限制分别说明；不自动确认创新发现。'),
('9/2 9/3 9/4 9/8','已有对应内容','主张、证据、结果与图的对应构成叙述。'),
('9/9 5/20','已有对应内容','讨论与替代解释、文献比较有教学示例。'),
('9/11 9/15 9/22','已有对应内容','预审关注证据和论证，未冒充正式期刊评审。'),
('9/3 9/5 9/6 9/7 9/12','已有对应内容','按论文各段的任务与已有证据分工。'),
('3/15 9/13','部分覆盖','期刊要求与写作边界已讲，缺少对应官方作者要求的完整风格适配提示示例。'),
('9/2 9/11 9/22','已有对应内容','逐句主张、引文支持和完整返修包用于检查逻辑。'),
('8/10 8/14 8/16','部分覆盖','数据图和机制草案边界已讲；未提供Midjourney/DALL-E专用提示示例，也未调用Nano Banana。'),
('1/11 3/4 3/16 9/14 10/4','已有对应内容','表达、事实、披露与投稿要求分别说明；目标期刊逐次核对。'),
('9/16','已有对应内容','方法、补研究与文字意见按修改动作分类。'),
('9/17 9/18 9/19 9/20','已有对应内容','回复、修改位置与未完成研究分别给出示例。'),
('9/11 9/15 9/22','已有对应内容','投稿前核对来源、逻辑和文件，AI意见为模拟。'),
('9/21','已有对应内容','拒稿理由、修改与目标期刊要求有对应。'),
('10/8 10/11','已有对应内容','文献脉络、科学问题与可检验关系形成依据。'),
('10/9 10/10 10/12 10/13','已有对应内容','目标、内容、设计与路线相互对应。'),
('10/14','已有对应内容','按对象、条件、方法与已有工作比较创新。'),
('10/6 10/15','已有对应内容','前期成果、本人贡献和条件需真实资料；不补造CV或团队基础。'),
('6/13 10/18 12/8','已有对应内容','任务与费用依据、财务和资产资料分别核对。'),
('10/21 10/24 10/26','调整讲法','预审和未决问题可演示；不编基金委评分或伪造专家签核。'),
('12/3 12/5 12/7','已有对应内容','任务、进展、证据、缺口与后续安排有对应。'),
('12/5 12/6 12/7','已有对应内容','进度、结果段落及未完成部分据证据表整理。'),
('12/5 12/8 12/9 12/10','已有对应内容','材料对应、归档、Word实际产物与正式报送边界分别说明。'),
('12/5 12/8 13/5','部分覆盖','论文、报告和专利类材料有对应；软件著作权成果登记示例尚不足。'),
('11/2 11/6 11/7 11/8 11/10 11/11','已有对应内容','交底、参数、附图和权利要求对应；不据此作法律授权判断。'),
('13/5 13/7 13/8','已有对应内容','普通读者版本、平台用途与分享版本已讲；不安排账户发布。'),
('3/11 13/2 13/3 13/4','已有对应内容','实际科研数据在课件中组织为可编辑图和讲述；不声称云端一键PPT接口已接入。'),
('13/7 13/8 13/10','部分覆盖','身份、入口和传播反馈已有，缺少长期内容安排的具体示例。'),
('2/18 14/15 14/16','已有对应内容','按任务选择协作方式，复核五类输出及材料归档。')]
topics=json.loads((R/'original_topics.json').read_text('utf-8'));assert len(topics)==len(rows)==52
records=[]
for i,(topic,(loc,status,note)) in enumerate(zip(topics,rows),1):
 keys=loc.split();assert all(k in pages for k in keys)
 evidence=[{k:v for k,v in pages[x].items() if k!='text'}|{'excerpt':pages[x]['text'][:220]} for x in keys]
 records.append({'id':i,'original_topic':topic,'status':status,'locations':keys,'assessment':note,'evidence':evidence})
counts={k:sum(x['status']==k for x in records) for k in ['已有对应内容','调整讲法','部分覆盖']}
dump(R/'current-course-audit.json',{'checked_date':'2026-10-19','total_pages':240,'sections':15,'coverage_scope':'Editorial location review of current slide text and selected sections; preliminary topic mapping, not execution completeness or scientific acceptance. Excerpts identify location, not proof of semantic coverage by themselves.','counts':counts,'rows':records,'visual_inventory':inventory,'remaining':'Resolve partially covered original topics; review source freshness and combined delivery; timing allocation is not a rehearsal.'})
head='# 原课程要求与当前240页课件的对应\n\n2026年10月19日复核。依据handoff-inputs中的客户原截图及正文52项，位置均从section-progress登记的当前PPT读取，使用“Section/节内页码”；总页码按0—14顺序计算。旧M编号与旧PPT页码不再作为新课件定位。\n\n“已有对应内容”表示已定位到相关讲授内容，仍需逐条全页复核，不代表相关软件已全部运行；“调整讲法”保留主题并修正原稿中无证据的承诺；“部分覆盖”保留为待补，不能算全部完成。代码、模型和正式科研审核另看各节记录。\n\n'
body='|序号|原稿项目|当前Section/页码|状态|说明|\n|---|---|---|---|---|\n'+''.join(f"|{x['id']}|{x['original_topic'].replace('|','／')}|{'、'.join(x['locations'])}|{x['status']}|{x['assessment']}|\n" for x in records)
write(R/'COURSE_COVERAGE_MATRIX.md',head+body+'\n本轮统计：'+str(counts)+'。范围不足的条目继续修订；不以匹配到关键词代替内容审阅。每个定位对应的文件哈希、页题和摘录见current-course-audit.json。')
write(R/'CLIENT_ORIGINAL_52_ITEMS.md','# 客户原稿52项\n\n原始正文完整保留在original_topics.json，来源为handoff-inputs中的客户截图及.doc文本。当前逐项定位、边界和缺口统一见COURSE_COVERAGE_MATRIX.md，避免同时维护新旧两套页码。历史M编号和旧页码可在Git历史中查阅，不能视为新课件已通过教学验收。')
# Explicit time arithmetic. This is a lecturer selection plan, never a rehearsal claim.
base=[5,20,30,30,25,40,20,35,20,35,45,20,10,10,25];extra=[0,5,10,10,5,15,10,10,10,10,10,5,0,0,10];assert sum(base)==370 and sum(extra)==110
time_rows=[]
for i,s in enumerate(d['sections']):time_rows.append({'section':i,'title':s['title'],'formal_minutes':base[i],'extension_minutes':extra[i],'prepared_minutes':base[i]+extra[i],'rehearsed':False})
dump(R/'teaching-time-plan.json',{'status':'lecturer allocation, not timed rehearsal','formal_minutes':370,'extension_minutes':110,'prepared_minutes':480,'morning_formal_minutes':sum(base[:7]),'afternoon_formal_minutes':sum(base[7:]),'breaks':['10:20–10:30','15:00–15:10'],'lunch':'12:00–13:30','rows':time_rows})
write(R/'讲授时段与延伸素材.md','# 讲授时段与延伸素材\n\n正式时段09:00—12:00、13:30—17:00共390分钟，扣除两次10分钟短休后为370分钟。延伸讲授另备110分钟，合计480分钟。以下是讲师选讲分配，尚未作真人计时彩排；页数和文件检查不能证明实际讲够八小时。\n\n|Section|内容|现场讲授分钟|延伸讲授分钟|备课合计|\n|---|---|---:|---:|---:|\n'+''.join(f"|{x['section']}|{x['title']}|{x['formal_minutes']}|{x['extension_minutes']}|{x['prepared_minutes']}|\n" for x in time_rows)+'\n上午0—6节合计170分钟，另含10:20—10:30短休；第3节可在短休前后分段讲。下午7—14节合计200分钟，另含15:00—15:10短休。午间90分钟不计入授课。延伸部分用于补充案例解释、原图读解、方法比较与讲师演示，不安排学员练习、分组或提交。\n\n正式讲授可先解释页面主问题，延伸时打开相应原文、编辑源或运行材料。具体选择随讲师节奏调整，不把同一段重复计算为两份内容。')
print(json.dumps({'current_pages':offset,'coverage_counts':counts,'partial_topic_ids':[x['id'] for x in records if x['status']=='部分覆盖'],'formal':sum(base),'extension':sum(extra)},ensure_ascii=False))
