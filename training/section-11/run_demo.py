from pathlib import Path
import sys,json,hashlib
r=Path(__file__).resolve().parent;sys.path.insert(0,str(r/'runtime-snapshot'))
from local_workflow import make_template,run
p=r/'patent-packet';m=json.loads((p/'patent.json').read_text('utf-8'));t=p/'教学交底模板.docx';make_template(t,[s['title'] for s in m['sections']]);v=run(p/'patent.json',t,p/'output');assert v['status']=='draft_review_required' and not v['external_model_called'];(r/'execution-evidence.json').write_text(json.dumps(dict(scope='实际结构核对与材料填充，不调用模型，不作专利性判断',run=v,executor_sha256=hashlib.sha256((r/'runtime-snapshot/local_workflow.py').read_bytes()).hexdigest()),ensure_ascii=False,indent=2),'utf-8');print(v['status'])
