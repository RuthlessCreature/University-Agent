from pathlib import Path
import csv,json,hashlib,re,statistics,math,zipfile,difflib
from xml.etree import ElementTree as E
import numpy as np
from pypdf import PdfReader
r=Path(__file__).resolve().parent;rev='s9-r3';p=next((r/'output').glob('*'+rev+'.pptx'));a=json.loads((r/'figure-data.json').read_text('utf-8'));d=json.loads((r/'lesson.json').read_text('utf-8'))
raw=r/'writing-packet/penguins.csv';assert hashlib.sha256(raw.read_bytes()).hexdigest()==a['raw_sha256']
rr=list(csv.DictReader(raw.open(encoding='utf-8')));assert len(rr)==344
ad=[q for q in rr if q['species']=='Adelie'];assert len(ad)==152
ad=[q for q in ad if q['sex'] in ['female','male'] and q['flipper_length_mm']!='NA'];assert len(ad)==146
for i,sex in enumerate(['female','male']):
 v=[float(q['flipper_length_mm']) for q in ad if q['sex']==sex];assert len(v)==73;assert math.isclose(statistics.mean(v),a[sex]['mean'],abs_tol=1e-10);assert math.isclose(statistics.stdev(v),a[sex]['sd'],abs_tol=1e-10);h=np.histogram(v,bins=a['histogram']['edges'])[0].tolist();assert h==a['histogram']['series'][i]['values']
f=np.array([float(q['flipper_length_mm']) for q in ad if q['sex']=='female']);m=np.array([float(q['flipper_length_mm']) for q in ad if q['sex']=='male']);rng=np.random.default_rng(a['bootstrap']['seed']);B=a['bootstrap']['replicates'];boot=rng.choice(m,(B,len(m)),replace=True).mean(axis=1)-rng.choice(f,(B,len(f)),replace=True).mean(axis=1);assert np.allclose(np.quantile(boot,[.025,.975],method='linear'),a['bootstrap']['percentile_95'],atol=1e-10,rtol=0)
b=r/'writing-packet';r0=(b/'manuscript-r0.md').read_text('utf-8');r1=(b/'manuscript-r1.md').read_text('utf-8');diff=(b/'revision.diff').read_text('utf-8');expected=''.join(difflib.unified_diff(r0.splitlines(True),r1.splitlines(True),fromfile='manuscript-r0.md',tofile='manuscript-r1.md'));assert diff==expected
matrix=list(csv.DictReader((b/'response-matrix.csv').open(encoding='utf-8-sig')));assert len(matrix)==3
for q in matrix:
 for anchor in re.findall(r'\[[A-Z][0-9]+\]',q['anchor']):assert anchor in r1
assert '未完成' in matrix[2]['status'] and '未新增' in r1
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'};diagrams=[]
with zipfile.ZipFile(p) as z:
 slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)];notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)];assert len(slides)==len(notes)==len(d)==22
 for i in range(1,23):
  x=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'));t=' '.join(q.text or '' for q in x.findall('.//a:t',ns));assert d[i-1]['title'] in t;assert all(w not in t for w in ['TODO','课堂练习','占位'])
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
 charts=[n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)];assert len(charts)==1
 x=E.fromstring(z.read(charts[0]));got=[[float(v.text) for v in q.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',ns)] for q in x.findall('.//c:ser',ns)];assert got==[q['values'] for q in a['histogram']['series']]
 assert len([n for n in z.namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')])==1
pdf=r/'renders'/rev/(p.stem+'.pdf');assert len(PdfReader(pdf).pages)==22;assert len(list(pdf.parent.glob('slide-*.png')))==22
v=json.loads((r/'.build'/rev/'validation.json').read_text('utf-8'));sha=hashlib.sha256(p.read_bytes()).hexdigest();assert v['finalSha256']==sha;assert v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8');q=dict(revision=rev,pages=22,notes=22,pdf_pages=22,preview_images=22,editable_connector_diagram_pages=diagrams,native_charts=1,embedded_workbooks=1,public_source_rows=344,analysis_rows=146,review_comments=3,actual_revision_diff_verified=True,pptx_sha256=sha,scope='核对源数据、图表缓存、实际文本差异、回复锚点和导出文件；不代表投稿完成或Agent全系统运行。');(r/'checks.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(q,ensure_ascii=False,indent=2))
