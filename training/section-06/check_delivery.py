from pathlib import Path
from xml.etree import ElementTree as ET
import hashlib,json,re,sys,zipfile,csv,io
from pypdf import PdfReader
r=Path(__file__).resolve().parent
rev=sys.argv[1] if len(sys.argv)>1 else 's6-r3'
p=r/'output'/f'高校科研AI课程_Section6_研究与实验方案_{rev}.pptx'
d=json.loads((r/'lesson.json').read_text('utf-8'));refs=json.loads((r/'sources.json').read_text('utf-8'))
assert [x['n'] for x in d]==list(range(1,17));assert all(k in refs for x in d for k in x['refs'])
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main','c':'http://schemas.openxmlformats.org/drawingml/2006/chart'}
diagrams=[];tables=[];texts=[]
with zipfile.ZipFile(p) as z:
 slides=[x for x in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',x)];notes=[x for x in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',x)];assert len(slides)==len(notes)==16
 for i in range(1,17):
  x=ET.fromstring(z.read(f'ppt/slides/slide{i}.xml'));txt=' '.join(t.text or '' for t in x.findall('.//a:t',ns));texts.append(txt);assert d[i-1]['title'] in txt
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
  if x.findall('.//a:tbl',ns):tables.append(i)
 assert diagrams==[1,2,3,4,6,7,8,11,12,14,15,16] and tables==[5,9,13]
 assert all('http' in z.read(x).decode() for x in notes)
 charts=[n for n in z.namelist() if re.fullmatch(r'ppt/(?:slides/)?charts/chart\d+\.xml',n)];assert len(charts)==1
 c=ET.fromstring(z.read(charts[0]));ser=c.findall('.//c:ser',ns);assert len(ser)==2
 values=[[float(t.text) for t in s.findall('.//c:val/c:numRef/c:numCache/c:pt/c:v',ns)] for s in ser]
 if not all(values):values=[[float(t.text) for t in s.findall('.//c:val/c:numLit/c:pt/c:v',ns)] for s in ser]
 assert values==[[60,72],[52,83]],values
 books=[n for n in z.namelist() if n.startswith('ppt/embeddings/') and n.endswith('.xlsx')];assert len(books)==1
 from openpyxl import load_workbook
 wb=load_workbook(io.BytesIO(z.read(books[0])),data_only=True);cells=[v for row in wb.active.values for v in row];assert all(v in cells for v in [60,72,52,83])
 assert not any(w in ' '.join(texts) for w in ['课堂练习','请提交','TODO','占位'])
 assert '独立试样数：3' in texts[6] and '总读数：3 × 3 = 9' in texts[6]
 assert '不据此判断统计显著' in texts[9]
source=json.loads((r/'source-data.json').read_text('utf-8'));rows=list(csv.DictReader((r/'design-packet/public-factorial-data.csv').open(encoding='utf-8-sig')))
assert [{k:int(v) if k!='K' else v for k,v in row.items()} for row in rows]==source['rows']
a=rows[1];b=rows[0];incA=int(a['y'])-int(b['y']);incB=int(rows[5]['y'])-int(rows[4]['y']);assert (incA,incB,incB-incA)==(12,31,19)
assert '未标' in source['response_unit'] and len(source['not_claimed'])==4
pdf=r/'renders'/rev/(p.stem+'.pdf');assert len(PdfReader(pdf).pages)==16;assert len(list((r/'renders'/rev).glob('slide-*.png')))==16
v=json.loads((r/'.build'/rev/'validation.json').read_text('utf-8'));sha=hashlib.sha256(p.read_bytes()).hexdigest();assert v['finalSha256']==sha and v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8')
report={'revision':rev,'pages':16,'pdf_pages':16,'notes':16,'preview_images':16,'editable_diagram_pages':diagrams,'native_table_pages':tables,'native_chart_pages':[10],'chart_series_values':values,'embedded_workbooks':len(books),'source_data_rows':len(rows),'recalculated_increments':[incA,incB,incB-incA],'pptx_sha256':sha,'scope':'文件结构、可编辑对象、图表缓存与工作簿、公开数据一致性及条件增量复算。另有逐页人工视觉检查；不表示已开展研究、统计推断完成或科研Agent全系统运行。'}
(r/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
