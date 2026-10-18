from pathlib import Path
import json,hashlib,zipfile,sys,re,xml.etree.ElementTree as ET
from pypdf import PdfReader
from docx import Document
R=Path(__file__).resolve().parent;rev=sys.argv[1] if len(sys.argv)>1 else 's14-r2'
def load(p):return json.loads(p.read_text('utf-8-sig'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
ppt=R/'output'/f'高校科研AI课程_Section14_本地与云端Agent实际演示_{rev}.pptx';pdf=R/'renders'/rev/(ppt.stem+'.pdf')
validation=load(R/'.build'/rev/'validation.json');assert validation['finalSha256']==sha(ppt)
assert validation['packageIntegrity']['findingCount']==0 and validation['presentationLayout']['finding_count']==0
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
result={'revision':rev,'pages':16,'notes':16,'pdf_pages':16,'preview_images':16,'editable_connector_diagram_pages':diagrams,'native_table_pages':[6,11,15],'actual_local_http_documents':3,'actual_invalid_file_inputs_rejected':3,'matching_instruction_files':24,'targeted_fixture_tests_passed':12,'actual_grant_word_preview_pages':len(PdfReader(R/'demo/word-preview/grant-draft.pdf').pages),'this_turn_cloud_health_checked':True,'this_turn_live_cloud_model_task':False,'researcher_approved':False,'pptx_sha256':sha(ppt),'scope':'Package, actual local files, copied input/output hashes, source bytes and declared test scope. Geometry/import checks do not prove teaching acceptance; fixture tests do not prove live cloud model operation.'}
(R/'checks.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n','utf-8');(R/'validation.json').write_text(json.dumps(validation,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
