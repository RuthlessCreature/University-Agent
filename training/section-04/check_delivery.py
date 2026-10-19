from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib,json,re,sys,zipfile,subprocess
from pypdf import PdfReader
r=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 's4-r5'
p=r/'output'/f'高校科研AI课程_Section4_选题与研究问题_{rev}.pptx'
d=json.loads((r/'lesson.json').read_text('utf-8'));refs=json.loads((r/'sources.json').read_text('utf-8'))
assert len(d)==14 and [x['n'] for x in d]==list(range(1,15))
assert all(k in refs for x in d for k in x['refs'])
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
diagrams=[];tables=[];charts=[];alltext=[]
with zipfile.ZipFile(p) as z:
 slides=[x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',x)]
 notes=[x for x in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',x)]
 assert len(slides)==len(notes)==14
 for i in range(1,15):
  x=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'));txt=' '.join(t.text or '' for t in x.findall('.//a:t',ns));alltext.append(txt);assert d[i-1]['title'] in txt
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
  if x.findall('.//a:tbl',ns):tables.append(i)
  if x.findall('.//c:chart',ns):charts.append(i)
 assert diagrams==[1,2,4,5,6,7,8,9,11,13,14]
 assert tables==[12] and charts==[3]
 files=[x for x in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',x)];assert len(files)==1
 x=ET.fromstring(z.read(files[0]));values=[float(v.text) for v in x.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',ns)] or [float(v.text) for v in x.findall('.//c:val/c:numLit/c:pt/c:v',ns)];assert values==[.48,1.27]
 assert len([x for x in z.namelist() if x.endswith('.xlsx')])==1
 assert '127%' in alltext[2] and '相对增幅' in alltext[2]
 assert '对照' in alltext[2] and '教师预设提示' in alltext[2]
 assert '教学模拟' in alltext[3] and '尚不能宣称首次' in alltext[6]
 assert not any(w in ' '.join(alltext) for w in ['课堂练习','请提交','TODO','占位'])
 assert all('来源' in z.read(x).decode() or 'http' in z.read(x).decode() or 'local:' in z.read(x).decode() for x in notes)
 case=json.loads((r/'trend-packet/case.json').read_text('utf-8'))
 assert any(hashlib.sha256(z.read(n)).hexdigest()==case['asset']['sha256'] for n in z.namelist() if n.startswith('ppt/media/'))
 assert all(s in alltext[1] for s in ['2024-05-23','2024-08-15','2025-06-25','US20240274025A1'])
 assert ET.fromstring(z.read('ppt/slides/slide10.xml')).findall('.//p:pic',ns)
pdf=r/'renders'/rev/(p.stem+'.pdf');assert len(PdfReader(pdf).pages)==14
assert len(list((r/'renders'/rev).glob('slide-*.png')))==14
v=json.loads((r/'.build'/rev/'validation.json').read_text('utf-8'));sha=hashlib.sha256(p.read_bytes()).hexdigest();assert sha==v['finalSha256'];assert v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8')
report={'revision':rev,'pages':14,'pdf_pages':14,'notes':14,'preview_images':14,'editable_diagram_pages':diagrams,'native_table_pages':tables,'native_chart_pages':charts,'chart_values_verified':values,'embedded_workbooks':1,'pptx_sha256':sha,'scope':'文件结构、页数、原生对象、指定数据与限定词检查。逐页视觉审阅另记，不代表选题已通过科学审核或Agent全系统已运行。'}
subprocess.run([sys.executable,str(r/'trend-packet/check_case.py')],check=True,capture_output=True)
report['source_comparison']=json.loads((r/'trend-packet/checks.json').read_text('utf-8'))
(r/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
