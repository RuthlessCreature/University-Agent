from pathlib import Path
from xml.etree import ElementTree as E
import json,hashlib,re,zipfile,subprocess,sys
from docx import Document
from pypdf import PdfReader
r=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 's11-r7';packet=r/'patent-packet';p=next((r/'output').glob('*'+rev+'.pptx'))
def load(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d=load(r/'lesson.json');m=load(packet/'patent.json');e=load(r/'execution-evidence.json');run=load(packet/'output/run.json');assert e['run']==run
for file,key in [(packet/'patent.json','input_sha256'),(packet/'教学交底模板.docx','template_sha256'),(packet/'output/patent-draft.docx','artifact_sha256')]:assert sha(file)==run[key],key
assert sha(r/'runtime-snapshot/local_workflow.py')==e['executor_sha256']
assert run['status']=='draft_review_required' and run['human_approved']==False and run['external_model_called']==False and run['scientific_validation']=='not_performed'
ledger=load(packet/'output/evidence-ledger.json');assert ledger['sources']==m['sources']
body='\n'.join(q.text for q in Document(packet/'output/patent-draft.docx').paragraphs)
for sec in m['sections']:assert sec['title'] in body and sec['content'] in body
assert len(m['sections'])==6 and '{{' not in body and 'teaching-simulation' in body and '没有样机' in body
issues=load(packet/'output/issues.json');assert len(issues)==5 and all(q['severity']=='blocking' for q in issues)
assert load(packet/'output/questions.json')==m['questions'] and len(m['questions'])==4
assert len(PdfReader(packet/'word-preview/patent-draft.pdf').pages)==3 and len(list((packet/'word-preview').glob('page-*.png')))==3
route=(packet/'方案流程.mmd').read_text('utf-8');assert route.count('-->')==6
fig=load(r/'source-figure.json');assert fig['physical_pdf_page']==17 and fig['figure']=='FIG. 2' and sha(r/'assets'/fig['asset'])==fig['sha256']
ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'};diagrams=[];tables=[];images=[]
with zipfile.ZipFile(p) as z:
 slides=[n for n in z.namelist() if re.fullmatch(r'ppt/slides/slide\d+\.xml',n)];notes=[n for n in z.namelist() if re.fullmatch(r'ppt/notesSlides/notesSlide\d+\.xml',n)];assert len(slides)==len(notes)==len(d)==12
 for i in range(1,13):
  x=E.fromstring(z.read(f'ppt/slides/slide{i}.xml'));t=' '.join(q.text or '' for q in x.findall('.//a:t',ns));assert d[i-1]['title'] in t;assert all(w not in t for w in ['TODO','课堂练习','占位'])
  if len(x.findall('.//p:cxnSp',ns))>=2:diagrams.append(i)
  if x.findall('.//a:tbl',ns):tables.append(i)
  if x.findall('.//p:pic',ns):images.append(i)
  nt=z.read(f'ppt/notesSlides/notesSlide{i}.xml').decode();assert 'http' in nt or 'local:' in nt
 assert tables==[5] and images==[3]
 assert len(E.fromstring(z.read('ppt/slides/slide7.xml')).findall('.//p:cxnSp',ns))==6
 assert any(z.read(n)==(r/'assets'/fig['asset']).read_bytes() for n in z.namelist() if n.startswith('ppt/media/') and n.endswith('.png'))
pdf=r/'renders'/rev/(p.stem+'.pdf');assert len(PdfReader(pdf).pages)==12 and len(list(pdf.parent.glob('slide-*.png')))==12
subprocess.run([sys.executable,str(r/'check_scheme.py'),rev],check=True,capture_output=True)
receipt=r/'.build'/rev/'validation.json'
if not receipt.exists():receipt=r/'validation.json'
v=load(receipt);digest=sha(p);assert v['finalSha256']==digest and v['packageIntegrity']['findingCount']==v['presentationLayout']['findingCount']==0
(r/'validation.json').write_text(json.dumps(v,ensure_ascii=False,indent=2),'utf-8')
q=dict(revision=rev,pages=12,notes=12,pdf_pages=12,preview_images=12,editable_connector_diagram_pages=diagrams,native_table_pages=tables,original_patent_figure_pages=images,word_pages=3,word_embedded_flow_figures=1,native_flow_and_claim_endpoint_checks=True,word_sections=6,questions=4,blocking_issues=5,actual_file_execution=True,external_model_called=False,scientific_validation='not_performed',pptx_sha256=digest,scope='文件哈希、原文图像、Word段落、来源、待补事项及导出文件核对；不代表专利检索查全、专利性判断、设备验证或用户教学验收。')
(r/'checks.json').write_text(json.dumps(q,ensure_ascii=False,indent=2),'utf-8');print(json.dumps(q,ensure_ascii=False,indent=2))
