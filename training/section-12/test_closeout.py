from pathlib import Path
import tempfile,shutil,json
from run_closeout import run
r=Path(__file__).resolve().parent;records=[]
cases=[('missing_csv','FileNotFoundError'),('tampered_source','source_hash_mismatch'),('duplicate_requirement','duplicate_requirement'),('overstated_completion','unresolved_completion_claim')]
for name,expected in cases:
 with tempfile.TemporaryDirectory(prefix='s12-negative-') as tmp:
  p=Path(tmp)/'packet';shutil.copytree(r/'closeout-packet/input',p/'input');out=p/'output'
  task=p/'input/taskbook.json'
  if name=='missing_csv':(p/'input/penguins.csv').unlink()
  elif name=='tampered_source':
   f=p/'input/source.json';v=json.loads(f.read_text('utf-8'));v['sha256']='0'*64;f.write_text(json.dumps(v),'utf-8')
  else:
   v=json.loads(task.read_text('utf-8'))
   if name=='duplicate_requirement':v['requirements'].append(v['requirements'][0])
   else:v['overall_completed_claim']=True
   task.write_text(json.dumps(v),'utf-8')
  try:run(p,out)
  except Exception as e:
   assert (isinstance(e,FileNotFoundError) if expected=='FileNotFoundError' else str(e)==expected)
   result=json.loads((out/'run.json').read_text('utf-8'));assert result['status']=='failed' and not list(out.glob('*.docx'))
   records.append(dict(case=name,expected=expected,actual_error_type=type(e).__name__,actual_error=expected if expected=='FileNotFoundError' else str(e),status=result['status'],word_written=False))
  else:raise AssertionError('Expected failure: '+name)
(r/'negative-cases.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),'utf-8');print('Actual failing executions verified:',len(records))
