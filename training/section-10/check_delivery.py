from pathlib import Path
from xml.etree import ElementTree as E
import json,hashlib,re,zipfile,subprocess,sys
from docx import Document
from pypdf import PdfReader
r=Path(__file__).resolve().parent;rev='s10-r4';packet=r/'grant-packet';p=next((r/'output').glob('*'+rev+'.pptx'));d=json.loads((r/'lesson.json').read_text('utf-8'));m=json.loads((packet/'grant.json').read_text('utf-8'));guide=json.loads((packet/'guide.json').read_text('utf-8'));e=json.loads((r/'execution-evidence.json').read_text('utf-8'));run=json.loads((packet/'output/run.json').read_text('utf-8'));assert e['positive']==run
for file,key in [(packet/'grant.json','input_sha256'),(packet/'guide.json','guide_sha256'),(packet/'教学材料模板.docx','template_sha256'),(packet/'output/grant-draft.docx','artifact_sha256')]:assert hashlib.sha256(file.read_bytes()).hexdigest()==run[key]
assert run['status']=='draft_review_required' and run['human_approved']==False and run['external_model_called']==False and run['scientific_validation']=='not_performed'
assert hashlib.sha256((r/'runtime-snapshot/local_workflow.py').read_bytes()).hexdigest()==e['executor_sha256']
assert len(e['negative_cases'])==4
for q in e['negative_cases']:
 actual=json.loads((packet/'negative-runs'/(q['case']+'.json')).read_text('utf-8'));assert actual['status']=='failed' and actual['error']==q['actual'] and q['expected'] in q['actual'] and q['blocked'];assert not list((r/'.build/negative-cases'/q['case']).glob('*.docx'))
assert m['requirements']==guide['requirements'];mapping=json.loads((packet/'output/mapping.json').read_text('utf-8'));assert mapping['requirements']==m['requirements'] and mapping['goals']==m['goals']
ledger=json.loads((packet/'output/evidence-ledger.json').read_text('utf-8'));assert ledger['sources']==m['sources']
body='\n'.join(q.text for q in Document(packet/'output/grant-draft.docx').paragraphs)
for sec in m['sections']:assert sec['title'] in body and sec['content'] in body
assert '{{' not in body and 'teaching-simulation' in body and '未开展采样' in body
issues=json.loads((packet/'output/issues.json').read_text('utf-8'));assert len(issues)==5 and all(q['severity']=='blocking' for q in issues)
assert len(PdfReader(packet/'word-preview/grant-draft.pdf').pages)==3 and len(list((packet/'word-preview').glob('page-*.png')))==3
route=(packet/'研究技术路线.mmd').read_text('utf-8');assert 'K --> I' in route and '未齐' in route and '一周后' in route
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'};diagrams=[];tables=[];images=[]
with zipfile.ZipFile(p) as z:
 slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)];notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)];assert len(slides)==len(notes)==len(d)==26
 for i in range(1,27):
  x=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'));t=' '.join(q.text or '' for q in x.findall('.//a:t',ns));assert d[i-1]['title'] in t;assert all(w not in t for w in ['TODO','课堂练习','占位'])
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
  if x.findall('.//a:tbl',ns):tables.append(i)
  if x.findall('.//p:pic',ns):images.append(i)
  assert 'http' in z.read(f'ppt/notesSlides/notesSlide{i}.xml').decode() or 'local:' in z.read(f'ppt/notesSlides/notesSlide{i}.xml').decode()
 assert tables==[22] and images==[25]
 assert len(E.fromstring(z.read('ppt/slides/slide13.xml')).findall('.//p:cxnSp',ns))==8
 x=E.fromstring(z.read('ppt/slides/slide11.xml'));assert len([q for q in x.findall('.//a:prstDash',ns) if q.attrib.get('val')=='dash'])==2
 assert any(z.read(n)==(packet/'word-preview/page-1.png').read_bytes() for n in z.namelist() if n.startswith('ppt/media/') and n.endswith('.png'))
pdf=r/'renders'/rev/(p.stem+'.pdf');assert len(PdfReader(pdf).pages)==26 and len(list(pdf.parent.glob('slide-*.png')))==26
subprocess.run([sys.executable,str(r/'check_route.py'),rev],check=True,capture_output=True)
receipt=r/'.build'/rev/'validation.json'
if not receipt.exists():receipt=r/'validation.json'
v=json.loads(receipt.read_text('utf-8'));sha=hashlib.sha256(p.read_bytes()).hexdigest();assert v['finalSha256']==sha and v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8');q=dict(revision=rev,pages=26,notes=26,pdf_pages=26,preview_images=26,editable_connector_diagram_pages=diagrams,native_table_pages=tables,actual_word_preview_pages=images,word_pages=3,word_embedded_route_figures=2,native_route_endpoint_checks=True,negative_cases_blocked=4,actual_file_execution=True,external_model_called=False,scientific_validation='not_performed',pptx_sha256=sha,scope='指南、输入、模板及Word哈希，内容填充、映射和来源，4项真实异常与导出文件核对；不代表科研有效性或云端模型全系统运行。');(r/'checks.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(q,ensure_ascii=False,indent=2))
