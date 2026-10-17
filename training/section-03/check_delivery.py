from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib,json,re,sys,zipfile
from pypdf import PdfReader
root=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 's3-r3'
data=json.loads((root/'lesson.json').read_text('utf-8'));refs=json.loads((root/'sources.json').read_text('utf-8'));facts=json.loads((root/'source-data.json').read_text('utf-8'))
assert len(data)==18 and [d['n'] for d in data]==list(range(1,19))
assert all(k in refs for d in data for k in d['refs'])
ppt=root/'output'/f'高校科研AI课程_Section3_Humanizer_{rev}.pptx'
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
with zipfile.ZipFile(ppt) as z:
 slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)];notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)]
 assert len(slides)==len(notes)==18
 tables=[];diagrams=[];alltext=[];chartowners={}
 for i in range(1,19):
  x=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'));text=' '.join(t.text or '' for t in x.findall('.//a:t',ns));alltext.append(text);assert data[i-1]['title'] in text
  if x.findall('.//a:tbl',ns):tables.append(i)
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
  if x.findall('.//c:chart',ns):chartowners[i]=True
 assert tables==[16] and sorted(chartowners)==[6,12]
 expected_diagrams=[1,3,5,7,8,9,10,11,13,14,15,17,18]
 assert diagrams==expected_diagrams,(diagrams,expected_diagrams)
 charts=[n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)]
 assert len(charts)==2
 values=[]
 for n in charts:
  x=ET.fromstring(z.read(n));v=[float(e.text) for e in x.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',ns)] or [float(e.text) for e in x.findall('.//c:val/c:numLit/c:pt/c:v',ns)];values.append(v)
 assert sorted(values)==sorted([facts['detector']['values'],facts['citation']['values']])
 books=[n for n in z.namelist() if n.endswith('.xlsx')];assert len(books)==2
 assert '无需披露' in alltext[16] and 'FAQ' in alltext[16]
 assert '可能' in alltext[3] and '尚未开始' in alltext[9]
 assert all(('http' in z.read(n).decode() or '本机技能' in z.read(n).decode()) for n in notes)
 assert not any(w in ' '.join(alltext) for w in ['课堂练习','小组讨论','请提交','TODO'])
pdf=root/'renders'/rev/(ppt.stem+'.pdf');assert len(PdfReader(pdf).pages)==18
images=list((root/'renders'/rev).glob('slide-*.png'));assert len(images)==18
validation=json.loads((root/'.build'/rev/'validation.json').read_text('utf-8'));sha=hashlib.sha256(ppt.read_bytes()).hexdigest();assert sha==validation['finalSha256']
assert validation['packageIntegrity']['findingCount']==0 and validation['presentationLayout']['findingCount']==0
(root/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n','utf-8')
report={'revision':rev,'pages':18,'pdf_pages':18,'notes':18,'preview_images':18,'editable_diagram_pages':diagrams,'native_table_pages':tables,'native_chart_pages':[6,12],'chart_values_verified':values,'embedded_workbooks':2,'pptx_sha256':sha,'scope':'课件结构、原生对象、报告数值与明确限定词的检查；不证明全部语义不变，不是外部模型或科研Agent运行测试。'}
(root/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8')
lines=['# Section 3 讲师稿','', '所有中文修订案例均为课程编写的教学模拟，公开课件转述与真实研究图另有来源。无课堂练习。','']
for d in data:
 lines += [f"## 第 {d['n']} 页：{d['title']}",'',d['thesis'],'',d['notes'],'']
 for key in ['before','after','reason','fact','caption','prompt']:
  if d.get(key):lines += [{'before':'原句','after':'修订稿','reason':'修改前提','fact':'需要保留的信息','caption':'图注','prompt':'任务说明'}[key]+'：'+d[key],'']
 lines += ['来源：']+[f"- {refs[k]['title']}；{refs[k]['url']}；定位：{refs[k]['location']}" for k in d['refs']]+['']
(root/'讲师稿.md').write_text('\n'.join(lines),'utf-8')
cases=['# 中文修订案例与差异说明','', '以下为课程编写的模拟情境，不是外部模型实际执行记录或真实科研成果。','']
for n,context,reason in [(8,'预设材料：两种预处理方法、同一数据集、处理步骤和结果比较。','把抽象评价改为预设材料中的对象、操作和讨论范围。'),(9,'预设材料：项目仍在申报阶段，计划比较两条路线；没有提供前期成果。','纠正将计划写成成果的错误；属于内容纠正，不能解释为纯语言润色。'),(10,'预设材料：已完成资料整理和分析方案初稿；缺项在核对；分析尚未开始。','用实际状态替代正面套话；状态来自模拟情境，不能用于真实进展报告。'),(13,'预设稿件：第二段以相关性结果直接作因果解释，尚缺研究设计依据。','定位问题，说明依据并提出修改建议；不能在未读稿件时套用此评语。')]:
 d=data[n-1];cases += [f"## 第{n}页 {d['title']}",'',context,'','原句：'+d['before'],'','修订稿：'+d['after'],'','修改理由：'+reason,'']
(root/'修订案例与差异说明.md').write_text('\n'.join(cases),'utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
