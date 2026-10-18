from pathlib import Path
import sys,json,copy,hashlib,platform
r=Path(__file__).resolve().parent;sys.path.insert(0,str(r/'runtime-snapshot'))
from local_workflow import run,make_template,WorkflowError
p=r/'grant-packet';template=p/'教学材料模板.docx'
make_template(template,['立项依据','研究内容','研究基础'])
result=run(p/'grant.json',template,p/'output',guide_path=p/'guide.json')
assert result['status']=='draft_review_required' and not result['external_model_called']
bad=r/'.build/negative-cases';bad.mkdir(parents=True,exist_ok=True);m=json.loads((p/'grant.json').read_text('utf-8'));cases=[]
for name,expected in [('guide-mismatch','guide_section_mismatch'),('unknown-source','unknown_source'),('missing-template','template_missing_section'),('final-unapproved','final_export_blocked')]:
 inp=copy.deepcopy(m);t=template;guide=p/'guide.json'
 if name=='guide-mismatch':inp['sections'][0]['title']='立项理由'
 if name=='unknown-source':inp['sections'][0]['source_ids']=['NOT-EXISTS']
 if name=='missing-template':t=bad/'incomplete.docx';make_template(t,['立项依据'])
 f=bad/(name+'.json');f.write_text(json.dumps(inp,ensure_ascii=False),'utf-8')
 try:run(f,t,bad/name,final=name=='final-unapproved',guide_path=guide);raise AssertionError('Failure expected')
 except WorkflowError as e:
  assert expected in str(e);cases.append(dict(case=name,expected=expected,actual=str(e),blocked=True))
report=dict(scope='实际本地JSON与DOCX模板核对、原文填充、映射与来源登记；未调用模型，未核验科研真实性，未完成正式提交',python=platform.python_version(),executor_sha256=hashlib.sha256((r/'runtime-snapshot/local_workflow.py').read_bytes()).hexdigest(),positive=result,negative_cases=cases)
(r/'execution-evidence.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print(result['status']);print('4 real negative executions blocked')
