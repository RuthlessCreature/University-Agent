"""Build the 200-page edition from authored cases and actual public/local evidence."""
import collections,csv,hashlib,json,pathlib,runpy,statistics,zipfile
from xml.etree import ElementTree as ET
from advanced_lessons import LESSONS
R=pathlib.Path(__file__).resolve().parents[1]
runpy.run_path(str(R/'src/author_course.py'))
base=json.loads((R/'slides_manifest.json').read_text('utf-8'))
by={s['id']:s for s in base};extra=collections.defaultdict(list)
def page(id,anchor,title,kind,body,notes,source=None,**kw):
    parent=by[anchor]
    d=dict(id=id,module='延伸备课' if kw.get('optional') else parent['module'],title=title,visual_type=kind,body=body,speaker_notes=notes,
           source=source or parent['source'],estimated_time_sec=150,learning_point=title,human_review=False,editorial_review='instructor_acceptance_pending',verification='source-linked; review-required',example_or_data='public data' if source=='penguins' else 'teaching case; not a new research result',workflow_step=id,**kw)
    extra[anchor].append(d)
assert len(LESSONS)==100,len(LESSONS)
for i,row in enumerate(LESSONS,1):
    source=by[row['anchor']]['source']
    if 'PRISMA' in row['analysis']:source='prisma'
    if 'Token Plan' in row['title']:source='minimax-cn;minimax-plan'
    page(f'X{i:03d}',row['anchor'],row['title'],'worked',[row['case'],row['analysis'],row['check']],
         row['case']+' '+row['analysis']+' '+row['check'],source=source,optional=row['optional'],material_label='教学案例与专业方法')

rows=list(csv.DictReader((R/'sources/penguins.csv').open(encoding='utf-8')))
def values(field,subset=rows):return [float(x[field]) for x in subset if x[field]!='NA']
def count(field):
    data=collections.Counter(x[field] if x[field]!='NA' else '未报告' for x in rows)
    return list(data),list(data.values())
def metric(field,method):
    names=['Adelie','Chinstrap','Gentoo'];groups=[values(field,[r for r in rows if r['species']==n]) for n in names]
    return names,[method(v) for v in groups],[len(v) for v in groups]
def histogram(field,start,stop,step):
    vals=values(field);limits=list(range(start,stop+1,step));labels=[f'{a}–<{b}' for a,b in zip(limits,limits[1:])];counts=[sum(a<=x<b for x in vals) for a,b in zip(limits,limits[1:])]
    assert sum(counts)==len(vals)
    return labels,counts
charts=[]
def chart(anchor,title,cats,vals,unit,interpretation,check,**kw):
    id=f'D{len(charts)+1:02d}';spec=dict(categories=cats,values=[round(v,6) if isinstance(v,float) else v for v in vals],unrounded_values=vals,unit=unit,**kw);charts.append(dict(id=id,**spec))
    detail='；'.join(f'{c}：{v:.1f}' if isinstance(v,float) else f'{c}：{v}' for c,v in zip(cats,vals))
    page(id,anchor,title,'datachart',[interpretation,check],detail+'。'+interpretation+' '+check+' 数值由原始CSV复算；嵌入工作簿保留6位小数，图示取1位，未取整值另存JSON。图形只作描述，不给出未执行的统计检验。',source='penguins',chart=spec,material_label='公开真实数据 · 本地复算')
for field,title,interpretation in [
 ('species','物种样本数决定分组比较的起点','三个物种的记录数不相同。比较均值之前，先确认各组样本量及其测量完整性；记录数不能解释为自然种群比例。'),
 ('island','岛屿记录数反映本数据的采样构成','岛屿是采样背景。不同岛屿的样本量与物种分布可能交织，不能把岛屿均值直接解释为岛屿环境的独立影响。'),
 ('year','年份计数不是个体追踪记录','相邻年份都有记录，不代表同一只个体被反复测量。要研究个体变化，需要能识别个体与重复测量的原始设计信息。'),
 ('sex','性别字段的缺失单独计数','性别未报告仍属于原始记录。按性别分析时，需要说明这些记录如何处理，不能把它们随意分到某个类别。')]:
    cats,vals=count(field);chart('M209',title,cats,vals,'记录数',interpretation,'检查每组计数之和是否为344，并说明当前图的分母；其他变量缺失可能使分析n变小。')
fields=['bill_length_mm','bill_depth_mm','flipper_length_mm','body_mass_g','sex'];missing=[sum(r[k]=='NA' for r in rows) for k in fields]
chart('M209','不同字段的缺失数量不能混用',['喙长','喙深','鳍肢长','体重','性别'],missing,'缺失记录数','按字段统计缺失，能解释为什么不同分析使用不同的n。体重缺失2行，不代表只需处理这两行就能完成所有多变量分析。','当前图记录缺失数量；缺失机制仍需采集过程与领域判断，不能由缺失柱高直接推断。')
for field,start,stop,step,title,unit,interpretation in [
 ('body_mass_g',2500,6500,500,'体重直方图保留分布与分箱依据','g','等宽500g分箱展示全部342条有效体重。混合物种分布可能产生多个集中区，不能直接当作同一总体的单一正态分布。'),
 ('flipper_length_mm',170,240,5,'鳍肢长度的分布需要结合物种读','mm','等宽5mm分箱汇总342条有效观测。直方图不保留物种身份；解释分布形状时应再检查分组图。'),
 ('bill_length_mm',30,60,5,'喙长分布与体重回答不同问题','mm','等宽5mm分箱显示有效喙长观测。变量单位相同或都属于形态测量，不表示可以直接互相替代。'),
 ('bill_depth_mm',12,24,2,'喙深的分箱结果可以从原值重算','mm','等宽2mm分箱，左闭右开。改变箱宽会改变外观，原始数值与有效记录数应保持不变。')]:
    cats,vals=histogram(field,start,stop,step);chart('M210',title,cats,vals,'记录数',interpretation,'图注说明箱宽与区间规则；若改变分箱，保留原数据并检查全部观测是否恰好计入一次。',x_unit=unit,gap=0)
for field,method,title,unit,interpretation in [
 ('body_mass_g',statistics.mean,'物种体重均值先报数值与有效 n','g','均值由各组已观察体重计算。组间描述差异需要结合采样、性别、岛屿与年份判断，当前柱图未提供因果识别。'),
 ('body_mass_g',statistics.median,'中位数提供另一种位置概括','g','中位数描述有序观测的中间位置，对极端值的响应不同于均值。两者选择应对应研究问题，不能挑更有利的一个隐去另一个。'),
 ('body_mass_g',statistics.stdev,'标准差描述组内个体离散','g','当前数值为样本标准差，分母使用n−1。SD不是均值的置信区间，也不是组间差异的显著性结果。'),
 ('flipper_length_mm',statistics.mean,'鳍肢长度均值需保留毫米单位','mm','描述不同物种的鳍肢长度均值，有效n与体重相同也需独立计数。图形单位是毫米，不能与体重克数放在同一轴上直接比较。'),
 ('bill_length_mm',statistics.mean,'喙长均值反映另一项形态测量','mm','喙长均值的物种排序与其他形态指标未必完全相同。解释时回到测量定义，不把多项指标压成含义不清的综合优势。'),
 ('bill_depth_mm',statistics.mean,'喙深均值不应被误读成总体定律','mm','当前均值来自特定公开样本。图形显示的是该数据的分组摘要，是否推广到其他年份或地区还需要适当证据。')]:
    cats,vals,ns=metric(field,method);chart('M211',title,[f'{n} n={k}' for n,k in zip(cats,ns)],vals,unit,interpretation,'保存未取整的计算值；展示小数精度统一。没有误差线时不从柱高推断统计显著性。')
assert len(charts)==15
(R/'sources/expanded-descriptive-charts.json').write_text(json.dumps(charts,ensure_ascii=False,indent=2),'utf-8')

def snippet(path,limit=1800):
    p=R.parents[1]/path;return p.read_text('utf-8-sig')[:limit]
evidence=[
 ('M311','教学指南的真实章节约束','training/demos/grant/guide.json','指南是独立输入，章节与要求需要和材料逐项一致。该文件明确标为teaching-simulation，不是官方基金指南。','比较required_sections和实际模板标题；任意一项变化都可能影响后续映射。'),
 ('M312','本地映射表如何连接 R 与 G','training/demos/grant/output/mapping.json','运行产物把目标与要求连接起来，并保留产物及核验方式。它证明映射文件已生成，不能证明科研任务已经完成。','沿R2定位G2、逐条筛选记录与统计报告；缺失其中一环，返回材料补充。'),
 ('M315','运行记录明确写了没有调用模型','training/demos/grant/output/run.json','这是实际CLI运行记录。external_model_called=false，human_approved=false；状态为待审核草稿。','检查输入、模板和指南哈希，再核对artifact_sha256与磁盘Word。不能把文件执行器称作模型自动设计研究。'),
 ('M316','未决问题没有因 Word 写出而消失','training/demos/grant/output/issues.json','研究基础、查新与签核问题保留在输出中。Word可编辑的意义在于继续修改，不能绕开缺失证据。','检查FOUNDATION、NOVELTY与HUMAN-SIGNOFF；关闭问题必须附新材料，不能只改状态。'),
 ('M316','最终导出失败是实际执行结果','evidence/final-export-negative-check.json','这是一次真实负向执行：exit_code=2，错误为final_export_blocked，未产生final文件。','区分已测的失败分支和未完成的科学审查。该记录不能推论所有异常与真实项目条件都已验证。'),
 ('M305','Paper 来源账本保留原论文与数据','training/demos/paper/output/evidence-ledger.json','账本将P1公开论文与D1公开CSV分别登记。两者范围不同，简化数据不能替原论文全部变量。','抽一条Results数值，回到CSV和统计JSON；再抽一条背景解释，回到论文正文。'),
 ('M325','发明人追问是实际产物之一','training/demos/patent/output/questions.json','问题清单由教学输入中的缺口输出。它告诉发明人应补什么，并未虚构参数或效果。','核对每条问题是否有明确对象和用途；研究者补充回答后应更新输入版本并重新检查。'),
 ('M315','HTTP 下载核对的是文件字节','training/demos/http-smoke.json','三条真实HTTP请求生成并下载DOCX，记录状态码、字节数和SHA-256。ZIP结构与下载哈希已核对。','此记录来自本地文件服务，不是Cloudflare执行截图，也没有证明MiniMax真实调用。'),
 ('M334','技术路线保留可编辑源码','training/demos/grant/output/route.mmd','该Mermaid文件由本地输入路线写出，节点与箭头可以修改。文字对应教学流程，不代表每个科学任务已经执行。','修改步骤后同时核对输入、输出、评价与异常出口。导出图片只是展示版本，源文件继续保留。'),
 ('M105','本地与 Worker 共用 Skill 指纹','skills-lock.json','版本锁定包含canonical commit、包指纹与24项Skill文件哈希。本地目录和Worker提示词使用同一字节来源。','同源说明指令一致；可调用工具仍需分开验收。云端没有Python工具时，不能因为Skill相同就声称运行了Python。')]
for i,(anchor,title,path,explanation,check) in enumerate(evidence,1):
    text=snippet(path,1500)
    if path.endswith('.json') and not path.endswith('skills-lock.json'):
        obj=json.loads(snippet(path,20000))
        if path.endswith('guide.json'):obj={k:obj[k] for k in ['id','type','required_sections','requirements']}
        if path.endswith('run.json'):obj={k:v for k,v in obj.items() if k!='events'}
        text=json.dumps(obj,ensure_ascii=False,separators=(', ',': '))[:1500]
    if path.endswith('skills-lock.json'):
        obj=json.loads(snippet(path,20000));text=json.dumps({k:obj[k] for k in ['commit','fingerprint']},ensure_ascii=False,indent=2)+'\n'+str(len(obj['skills']))+' 项 Skill 哈希已登记；完整文件见源码。'
    original=json.loads(snippet(path,20000)) if path.endswith('.json') else None
    headers=[['指南条目','独立指南要求','核对方法'],['要求 → 目标','研究任务与要求','产物及验证'],['记录字段','实际记录（哈希节选）','解释与限制'],['问题编号','仍缺的材料','提交限制'],['检查对象','实际返回','结果说明'],['来源 / 章节','材料或来源编号','阅读与核查'],['问题序号','需要发明人回答的问题','补充依据'],['教学任务','HTTP 与文件记录','证据范围'],['路线步骤','具体动作','执行条件'],['版本项目','锁定内容','同源检查']]
    header=headers[i-1]
    if i==1:
        guide=original;tab=[header,['材料标识',guide['id']+'；'+guide['type'],'教学模拟，不是正式基金指南'],['章节约束','、'.join(guide['required_sections']),'与模板及输入顺序逐项一致']]+[[x['id'],x['text'],x['artifact']+'；'+x['verification']] for x in guide['requirements']]
    elif i==2:tab=[header]+[[x['id']+' → '+','.join(x['goal_ids']),x['text'],x['artifact']+'；'+x['verification']] for x in original['requirements']]
    elif i==3:
        tab=[header,['状态',original['status'],'草稿待审核，不是正式提交']]+[[k,original[k][:20]+'…','显示前20位；完整SHA-256见原JSON'] for k in ['input_sha256','template_sha256','guide_sha256','artifact_sha256']]+[['模型 / 人工 / 科学核验','false / false / not_performed','本地文件流程，未调用模型与科学审查']]
    elif i==4:tab=[header]+[[x['id'],x['issue'],'blocking：最终提交仍被阻止'] for x in original]
    elif i==5:tab=[header,['实际退出码',str(original['exit_code']),'失败分支真实执行'],['错误返回',original['stdout']['error'],'缺少批准与研究条件，拒绝最终导出'],['final文件存在',str(original['final_docx_exists']),'没有生成可误用的最终文件']]
    elif i==6:
        tab=[header]+[[s['id'],s['locator'],'公开来源；具体主张仍需读原文'] for s in original['sources']]+[[s['title'],','.join(s['source_ids']),'章节与来源连接；不自动保证科学正确'] for s in original['sections']]
    elif i==7:tab=[header]+[[str(n+1),question,'由发明人提供事实与对应原始记录'] for n,question in enumerate(original)]
    elif i==8:tab=[header]+[[x['kind'],'HTTP '+str(x['post_status'])+' / 下载 '+str(x['download_status'])+'；'+str(x['bytes'])+'字节','DOCX ZIP有效；SHA-256与运行输出一致'] for x in original]+[['模型调用','全部 external_model_called=false','本地文件链路，不是云端模型联调']]
    elif i==9:
        stages=__import__('re').findall(r'\["([^"]+)"\]',text);tab=[header]+[[f'{n+1:02d}',stage,('输入与授权' if n==0 else '检查前一步输出，再执行本步')] for n,stage in enumerate(stages)]
    else:tab=[header,['来源提交',original['commit'][:20]+'…','同一canonical提交，完整值见锁文件'],['Skill数量',str(len(original['skills'])),'本地目录与Worker包逐项一致'],['包指纹',original['fingerprint'][:20]+'…','锁定版本包；不能只比Skill名称'],['执行范围','指令同源；工具分别验收','相同Skill不等于两端都有Python或检索工具']]
    page(f'RUN{i:02d}',anchor,title,'evidence',[text,explanation,check],explanation+' '+check+' 原始文件：'+path+'\n原始字段摘录：\n'+text,source='teaching',evidence_path=path,evidence_rows=tab,material_label='本地实际文件与运行记录')
assert len(evidence)==10
slides=[]
for s in base:slides.append(s);slides.extend(extra[s['id']])
assert len(slides)==200,len(slides)
budgets={'开场':15,'模块一':65,'模块二':90,'模块三 A':40,'模块三 B':50,'模块三 C':35,'模块三 D':35,'模块四':25,'收尾':15,'延伸备课':110}
for mod,minutes in budgets.items():
    members=[s for s in slides if s['module']==mod];total=sum(s['estimated_time_sec'] for s in members);used=0
    for s in members[:-1]:s['estimated_time_sec']=round(s['estimated_time_sec']/total*minutes*60);used+=s['estimated_time_sec']
    members[-1]['estimated_time_sec']=minutes*60-used
sample_ids={'O02','M103','M107','M204','M206','M210','M211','M304','M312','M321','D06'}
sample_ids.add(next(s['id'] for s in slides if s['title']=='空泛评价换成可观察事实'))
for n,s in enumerate(slides,1):
    s['page']=n;s['sample']=s['id'] in sample_ids;s['human_review']=False
    if s['id']=='O01':s['speaker_notes']+=' 200页版本按讲师语速安排，时间是含演示、讨论与操作的备课预算，未经过完整彩排。可按学员基础选择延伸材料，不能把页数自动等同授课时长。'
(R/'slides_manifest.json').write_text(json.dumps(slides,ensure_ascii=False,indent=2),'utf-8')
handbook='# 高校科研 AI 讲师手册（200页备课版）\n\n主课370分钟，延伸110分钟。页数和时间是编排预算，包含操作、演示与讨论；未做全程授课实测。\n\n'
for s in slides:handbook+=f'## {s["page"]:03d} {s["id"]} {s["title"]}\n\n{s["module"]}，{s["estimated_time_sec"]/60:.1f}分钟。来源：{s["source"]}。\n\n{s["speaker_notes"]}\n\n'
(R/'讲师手册.md').write_text(handbook.rstrip()+'\n','utf-8')
print('200 slides;',sum(s['sample'] for s in slides),'sample;',sum(not s.get('optional') for s in slides),'main;',sum(bool(s.get('optional')) for s in slides),'extension; 15 new native charts; 10 actual artifact pages')
