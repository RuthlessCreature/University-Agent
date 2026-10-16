"""Exercise real Wrangler local HTTP/DO storage; deliberately makes no model call."""
from pathlib import Path
import json,urllib.request,urllib.error,sys
ROOT=Path(__file__).resolve().parents[1]
base='http://127.0.0.1:8789'
def request(path,data=None):
    req=urllib.request.Request(base+path,data=None if data is None else json.dumps(data).encode(),headers={'Content-Type':'application/json','X-Workshop-Key':'local-teaching-check'})
    try:
        with urllib.request.urlopen(req,timeout=20) as response:return response.status,json.load(response)
    except urllib.error.HTTPError as error:return error.code,json.load(error)
path=ROOT/'evidence/wrangler-local-smoke.json'
if '--resume' in sys.argv:
    report=json.loads(path.read_text('utf-8'))
    for record in report['projects']:
        status,current=request('/api/projects/'+record['id']);assert status==200 and current['input_sha256']==record['input_sha256'] and current['version']==1
        record['persisted_after_process_restart']=True
else:
    _,health=request('/health');assert not health['model_configured'] and health['persistence_bound']
    report={'environment':'Wrangler local runtime / actual Durable Object storage','external_model_called':False,'cloud_deployed':False,'health':health,'projects':[]}
    for kind in ['grant','paper','patent']:
        _,example=request('/api/examples/'+kind);status,current=request('/api/projects',example);assert status==201
        id=current['id'];status,error=request('/api/projects/'+id,{'action':'execute','version':1});assert status==422 and '订阅 Key' in error['error']
        status,_=request('/api/projects/'+id,{'action':'export','version':1});assert status==409
        _,restored=request('/api/projects/'+id);assert restored['status']=='ready' and restored['version']==1 and restored['input']['kind']==kind
        report['projects'].append({'kind':kind,'id':id,'input_sha256':current['input_sha256'],'template_sha256':current['template_sha256'],'created_http_status':201,'unconfigured_model_blocked':True,'premature_export_blocked':True,'restored_input_matches':True})
path.write_text(json.dumps(report,ensure_ascii=False,indent=2),'utf-8');print('PASS: actual local Worker storage',len(report['projects']),'projects;', 'restart persistence verified' if '--resume' in sys.argv else 'no live model requested')
