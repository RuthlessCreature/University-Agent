from pathlib import Path
import json,hashlib,shutil,urllib.request,subprocess,copy,sys,datetime
R=Path(__file__).resolve().parent; A=R.parents[1]; W=A.parent
def dump(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n','utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
E=R/'evidence'; I=R/'demo/input'; O=R/'demo/output';I.mkdir(parents=True,exist_ok=True)
for kind in ['grant','paper','patent']:
 src=A/'training/demos'/kind; dest=I/kind;dest.mkdir(exist_ok=True)
 for name in [kind+'.json','template.docx']+(['guide.json'] if kind=='grant' else []):shutil.copy2(src/name,dest/name)
 req=urllib.request.Request('http://127.0.0.1:8788/api/local-run/'+kind,data=b'{}',headers={'Content-Type':'application/json'})
 with urllib.request.urlopen(req,timeout=30) as q:run=json.load(q)
 dest=O/kind;shutil.copytree(src/'http-output',dest,dirs_exist_ok=True)
 with urllib.request.urlopen('http://127.0.0.1:8788/artifacts/'+kind,timeout=15) as q:b=q.read()
 assert hashlib.sha256(b).hexdigest()==run['artifact_sha256']==sha(dest/(kind+'-draft.docx'))
 assert not run['external_model_called'] and not run['human_approved']
with urllib.request.urlopen('http://127.0.0.1:8788/health',timeout=15) as q:health=json.load(q)
dump(E/'local-http.json',{'checked_at':now,'health':health,'kinds':['grant','paper','patent'],'artifact_download_hash_verified':True,'scope':'Real local HTTP + Python + DOCX, fixed teaching materials, no model.'})
sys.path.insert(0,str(W/'University-Skills/tools'));from local_workflow import run,WorkflowError
base=json.loads((I/'grant/grant.json').read_text('utf-8-sig')); negatives=[]
for case,expected in [('unknown-source','unknown_source:NOT-A-SOURCE'),('guide-mismatch','guide_requirement_mismatch'),('final-without-signoff','final_export_blocked')]:
 d=copy.deepcopy(base)
 if case=='unknown-source':d['sections'][0]['source_ids']=['NOT-A-SOURCE']
 if case=='guide-mismatch':d['requirements'][0]['text']='与指南不同的教学变更'
 p=R/'demo/negative'/case;p.mkdir(parents=True,exist_ok=True);dump(p/'input.json',d)
 try:run(p/'input.json',I/'grant/template.docx',p/'output',final=case=='final-without-signoff',guide_path=I/'grant/guide.json');raise AssertionError('invalid case was accepted')
 except WorkflowError as e:assert str(e)==expected;negatives.append({'case':case,'actual_error':str(e),'rejected':True,'external_model_called':False})
dump(E/'negative-cases.json',{'checked_at':now,'cases':negatives,'scope':'Real file executor validation errors; deliberate teaching input mutations, not network/model failure tests.'})
manifest=json.loads((W/'University-Skills/skills-manifest.json').read_text('utf-8-sig'));lock=json.loads((A/'skills-lock.json').read_text('utf-8-sig'))
packtext=(A/'src/generated/skill-pack.js').read_text('utf-8');pack=json.loads(packtext[packtext.index('{'):].strip().rstrip(';'))
rows=[]
for q in manifest['skills']:
 def normalized(p):return p.read_bytes().replace(b'\r\n',b'\n')
 source=normalized(W/'University-Skills'/q['path']);lh=hashlib.sha256(source).hexdigest()
 assert source==normalized(W/'.agents/skills'/q['id']/'SKILL.md')==normalized(A/'.agents/skills'/q['id']/'SKILL.md')==pack['skills'][q['id']]['content'].encode()
 assert lh==lock['skills'][q['id']]==pack['skills'][q['id']]['sha256']
 rows.append({'id':q['id'],'sha256_lf':lh,'local_and_worker_equal':True,'integration_scope':q.get('integration_scope','Not declared in manifest')})
cloud=json.loads((E/'cloud-health.json').read_text('utf-8'))
assert cloud['health']['skill_fingerprint']==lock['fingerprint']
dump(E/'same-skills.json',{'checked_at':now,'count':len(rows),'canonical_commit':lock['commit'],'fingerprint':lock['fingerprint'],'cloud_health_fingerprint_matches':True,'normalization':'CRLF converted to LF','skills':rows,'scope':'Instruction bytes on disk and bundle verified; live health reports same fingerprint. Does not prove equal tools or correct model execution.'})
snap=E/'source-snapshot';snap.mkdir(exist_ok=True)
for f in ['src/automatic.js','src/model.js','src/workflows.js','src/writing.js','src/grant.js','src/projects.js','src/word-export.js','skills-lock.json']:
 p=snap/f;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(A/f,p)
shutil.copy2(W/'University-Skills/tools/local_workflow.py',snap/'local_workflow.py')
shutil.copy2(R/'.reference-cache/page-30.png',R/'assets/cmu-2025-page-30.png')
dump(E/'provenance.json',{'checked_at':now,'agent_head':subprocess.check_output(['git','-C',str(A),'rev-parse','HEAD']).decode().strip(),'working_tree_snapshot':True,'reference_pdf':{'url':'https://www.cs.cmu.edu/~mgormley/courses/10423-f25/slides/lecture23-code.pdf','sha256':sha(R/'.reference-cache/cmu-2025-lecture23.pdf'),'physical_pages_viewed':[29,30,31,32,34,37],'adopted_page':30,'printed_number':35},'source_files':[{'path':str(p.relative_to(R)).replace('\\','/'),'sha256':sha(p)} for p in snap.rglob('*') if p.is_file()]})
print('Real HTTP documents: 3; real negative inputs rejected: 3; matching canonical skills:',len(rows))
