from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib,json,re,sys,zipfile,csv,subprocess
from pypdf import PdfReader
r=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 's5-r4'
p=r/'output'/f'高校科研AI课程_Section5_文献检索阅读与综述_{rev}.pptx'
d=json.loads((r/'lesson.json').read_text('utf-8'));refs=json.loads((r/'sources.json').read_text('utf-8'));assert len(d)==24
assert [x['n'] for x in d]==list(range(1,25));assert all(k in refs for x in d for k in x['refs'])
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
diagrams=[];tables=[];pictures=[];texts=[]
with zipfile.ZipFile(p) as z:
 slides=[x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',x)];notes=[x for x in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',x)];assert len(slides)==len(notes)==24
 for i in range(1,25):
  x=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'));txt=' '.join(t.text or '' for t in x.findall('.//a:t',ns));texts.append(txt);assert d[i-1]['title'] in txt
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
  if x.findall('.//a:tbl',ns):tables.append(i)
  if x.findall('.//p:pic',ns):pictures.append(i)
 assert diagrams==[1,3,4,6,8,10,11,12,13,14,15,16,21,22,23,24]
 assert tables==[2,7,17,19] and pictures==[5,9]
 media=[hashlib.sha256(z.read(n)).hexdigest() for n in z.namelist() if n.startswith('ppt/media/')]
 for name in ['pubmed-detail.png','elicit-detail.png']:assert hashlib.sha256((r/'assets'/name).read_bytes()).hexdigest() in media
 assert '2026-09-30' in texts[8] and 'Research Agent' in texts[8]
 assert '中位数' in texts[17] and '194' in texts[17] and '316' in texts[17]
 assert len([n for n in z.namelist() if n.endswith('.xlsx')])==1
 charts=[n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)];assert len(charts)==1
 cn={'c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
 chart=ET.fromstring(z.read(charts[0]));vals=[float(n.text) for n in chart.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',cn)] or [float(n.text) for n in chart.findall('.//c:val/c:numLit/c:pt/c:v',cn)];assert vals==[3.5,4.5]
 assert 'Kestin' in texts[21] and '反证' in texts[21]
 assert '不构成系统综述' in texts[16]
 assert not any(w in ' '.join(texts) for w in ['课堂练习','请提交','TODO','占位'])
 assert all(('http' in z.read(x).decode() or 'local:' in z.read(x).decode()) for x in notes)
 assert len(ET.fromstring(z.read('ppt/slides/slide8.xml')).findall('.//a:tailEnd',ns))==0
pdf=r/'renders'/rev/(p.stem+'.pdf');assert len(PdfReader(pdf).pages)==24;assert len(list((r/'renders'/rev).glob('slide-*.png')))==24
v=json.loads((r/'.build'/rev/'validation.json').read_text('utf-8'));sha=hashlib.sha256(p.read_bytes()).hexdigest();assert v['finalSha256']==sha and v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
rows=list(csv.DictReader((r/'literature-packet/evidence-matrix.csv').open(encoding='utf-8-sig')));assert len(rows)==2;assert {x['doi'] for x in rows}=={'10.1073/pnas.2422633122','10.1038/s41598-025-97652-6'};assert all('PENDING' in x['update_status'] for x in rows)
log=json.loads((r/'literature-packet/search-log.json').read_text('utf-8'));assert log['actual_search']['query']=='"generative AI" learning' and 'PENDING' in log['teaching_query']['status']
subprocess.run([sys.executable,str(r/'literature-packet/reproduce_kestin.py')],check=True,capture_output=True)
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8')
report={'revision':rev,'pages':24,'pdf_pages':24,'notes':24,'preview_images':24,'editable_diagram_pages':diagrams,'native_table_pages':tables,'real_web_screenshot_pages':pictures,'embedded_screenshot_bytes_match':True,'evidence_matrix_records':2,'native_chart_pages':[18],'chart_medians':[3.5,4.5],'descriptive_reproduction_records':316,'unique_student_ids':194,'all_regressions_reproduced':False,'pptx_sha256':sha,'scope':'文件结构、原生连接图与表格、截图字节一致性、指定范围表述及材料表检查。不代表系统检索已完成、论文全面核验或科研Agent全系统已运行。'}
(r/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
