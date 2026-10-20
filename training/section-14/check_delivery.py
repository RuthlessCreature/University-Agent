from pathlib import Path
import json,hashlib,zipfile,sys,re,csv,statistics,xml.etree.ElementTree as ET
from pypdf import PdfReader
from docx import Document
R=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 's14-r3'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ppt=R/'output'/f'高校科研AI课程_Section14_本地与云端Agent实际演示_{rev}.pptx';pdf=R/'renders'/rev/(ppt.stem+'.pdf')
vpath=R/'.build'/rev/'validation.json';validation=load(vpath if vpath.exists() else R/'validation.json');assert validation['finalSha256']==sha(ppt)
assert validation['packageIntegrity']['findingCount']==0 and validation['presentationLayout'].get('finding_count',validation['presentationLayout'].get('findingCount'))==0
lesson=load(R/'lesson.json');assert len(lesson)==16 and len(PdfReader(pdf).pages)==16
assert len(list((R/'renders'/rev).glob('slide-*.png')))==16
with zipfile.ZipFile(ppt) as z:
 slides=[n for n in z.namelist() if re.match(r'ppt/slides/slide\d+\.xml$',n)];assert len(slides)==16
 notes=[n for n in z.namelist() if re.match(r'ppt/notesSlides/notesSlide\d+\.xml$',n)];assert len(notes)==16
 diagrams=[]
 for n in range(1,17):
  x=ET.fromstring(z.read(f'ppt/slides/slide{n}.xml'));texts=''.join(x.itertext());assert lesson[n-1]['title'] in texts
  if len(x.findall('.//{http://schemas.openxmlformats.org/presentationml/2006/main}cxnSp'))>=2:diagrams.append(n)
 for n in [6,11,15]:assert b'<a:tbl>' in z.read(f'ppt/slides/slide{n}.xml')
 media=[z.read(n) for n in z.namelist() if n.startswith('ppt/media/')]
 for f in ['assets/cmu-2025-page-30.png','assets/local-grant-actual.png','demo/word-preview/page-1.png']:assert (R/f).read_bytes() in media
 ns={'a':'http://schemas.openxmlformats.org/drawingml/2006/main','p':'http://schemas.openxmlformats.org/presentationml/2006/main'}
 flow=ET.fromstring(z.read('ppt/slides/slide9.xml'));nodes={}
 for sp in flow.findall('.//p:sp',ns):
  label=''.join(t.text or '' for t in sp.findall('.//a:t',ns));nv=sp.find('./p:nvSpPr/p:cNvPr',ns)
  if nv is not None:nodes[label]=nv.attrib['id']
 edges=[('任务与已有材料','当前步骤：模型或规则'),('当前步骤：模型或规则','工具实际读写'),('工具实际读写','保存结果和版本'),('保存结果和版本','检查并继续或重试'),('检查并继续或重试','当前步骤：模型或规则')]
 assert {(c.find('.//a:stCxn',ns).attrib['id'],c.find('.//a:endCxn',ns).attrib['id']) for c in flow.findall('.//p:cxnSp',ns)}=={(nodes[a],nodes[b]) for a,b in edges}
for k in ['grant','paper','patent']:
 p=R/'demo/output'/k;run=load(p/'run.json');assert run['status']=='draft_review_required' and not run['human_approved'] and not run['external_model_called'];assert sha(p/(k+'-draft.docx'))==run['artifact_sha256']
 assert run['input_sha256']==sha(R/'demo/input'/k/(k+'.json')) and run['template_sha256']==sha(R/'demo/input'/k/'template.docx')
 text='\n'.join(p.text for p in Document(p/(k+'-draft.docx')).paragraphs);assert '来源与未决问题' in text and '{{' not in text
assert load(R/'demo/output/grant/run.json')['guide_sha256']==sha(R/'demo/input/grant/guide.json')
neg=load(R/'evidence/negative-cases.json');assert len(neg['cases'])==3 and all(q['rejected'] for q in neg['cases'])
skills=load(R/'evidence/same-skills.json');assert skills['count']==24 and all(x['local_and_worker_equal'] for x in skills['skills'])
cloud=load(R/'evidence/cloud-health.json')['health'];assert cloud['skill_fingerprint']==skills['fingerprint'] and cloud['model']=='deepseek-flash' and cloud['inactive_providers']==['minimax']
tests=(R/'evidence/targeted-tests.tap').read_text('utf-8-sig');assert re.search(r'(?:ℹ|#) pass 12',tests) and re.search(r'(?:ℹ|#) fail 0',tests)
for f in load(R/'evidence/provenance.json')['source_files']:assert sha(R/f['path'])==f['sha256']
for case in neg['cases']:
 out=R/'demo/negative'/case['case']/'output';actual=load(out/'run.json');assert actual['status']=='failed'
 assert actual['error']==case['actual_error'] and not list(out.glob('*.docx'))
packtext=(R/'evidence/source-snapshot/src/generated/skill-pack.js').read_text('utf-8');pack=json.loads(packtext[packtext.index('{'):].strip().rstrip(';'))
for skill in skills['skills']:
 b=(R/'evidence/skill-instructions'/(skill['id']+'.md')).read_bytes()
 assert hashlib.sha256(b).hexdigest()==skill['sha256_lf']==pack['skills'][skill['id']]['sha256']
 assert b.decode()==pack['skills'][skill['id']]['content']
test_execution=load(R/'evidence/targeted-test-execution.json');assert test_execution['passed']==12 and test_execution['failed']==0 and test_execution['exit_code']==0
assert sha(R/'evidence/targeted-tests.tap')==test_execution['tap_sha256']
auth=load(R/'evidence/cloud-auth-attempt.json');assert auth['status']==401 and not auth['authenticated'] and not auth['cloud_task_created'] and not auth['model_called']
facts=load(R/'evidence/paper-facts-check.json');assert sha(R/facts['source_file'])==facts['source_sha256']
with (R/facts['source_file']).open(encoding='utf-8-sig',newline='') as f:raw=list(csv.DictReader(f))
valid=[q for q in raw if q['body_mass_g'] not in ['','NA']];assert len(raw)==344 and len(valid)==342
for species,group in facts['groups'].items():
 vals=[float(q['body_mass_g']) for q in valid if q['species']==species]
 assert len(vals)==group['records'] and abs(statistics.mean(vals)-group['mean_g'])<1e-10 and abs(statistics.stdev(vals)-group['sample_sd_g'])<1e-10
copied=load(R/'course-artifacts/manifest.json');assert len(copied['files'])==18 and set(f['kind'] for f in copied['files'])=={'grant','paper','patent','figure','closeout'}
assert not copied['researcher_approved'] and not copied['this_turn_reexecuted']
for f in copied['files']:assert sha(R/f['file'])==f['sha256'] and (R/f['file']).stat().st_size==f['bytes']
cap=load(R/'evidence/provenance.json')['browser_capture'];assert sha(R/cap['file'])==cap['sha256'] and sha(R/'demo/output/grant/run.json')==cap['grant_run_sha256']
for name,folder,count in [('grant','word-preview',2),('paper','paper-word-preview',1),('patent','patent-word-preview',1)]:
 assert len(PdfReader(R/'demo'/folder/(name+'-draft.pdf')).pages)==count
 assert len(list((R/'demo'/folder).glob('page-*.png')))==count
result={'revision':rev,'pages':16,'notes':16,'pdf_pages':16,'preview_images':16,'editable_connector_diagram_pages':diagrams,'native_table_pages':[6,11,15],'actual_local_http_documents':3,'actual_invalid_file_inputs_rejected':3,'matching_instruction_files':24,'targeted_fixture_tests_passed':12,'actual_grant_word_preview_pages':len(PdfReader(R/'demo/word-preview/grant-draft.pdf').pages),'this_turn_cloud_health_checked':True,'this_turn_live_cloud_model_task':False,'actual_cloud_login_status':401,'local_course_artifact_snapshots':18,'bundled_skill_instructions_checked':24,'researcher_approved':False,'pptx_sha256':sha(ppt),'scope':'Package, actual local files, copied input/output hashes, 18 existing course artifact snapshots, 24 full instruction files against Worker bundle, current health and failed login, actual fixture test run and declared scope. Geometry/import checks do not prove teaching acceptance; fixture tests do not prove live cloud model operation.'}
(R/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');(R/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
