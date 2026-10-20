"""Check a real software snapshot and keep contribution/registration gaps explicit."""
from pathlib import Path
import csv,json,hashlib,statistics,math
P=Path(__file__).resolve().parent
def load(p):return json.loads(p.read_text('utf-8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
snapshot=load(P/'snapshot.json');ledger=load(P/'成果台账.json');requirements=load(P/'登记材料核对.json')
assert len(snapshot['files'])==7
for item in snapshot['files']:
 p=P/item['path'];assert sha(p)==item['sha256'] and p.stat().st_size==item['bytes']
assert sha(P/'source/analysis.py')==snapshot['source_origin_sha256']==snapshot['program_sha256']
assert sha(P/'source/penguins.csv')==snapshot['data_sha256']==load(P/'source/data-source.json')['sha256']
rows=list(csv.DictReader((P/'source/penguins.csv').open(encoding='utf-8')));assert len(rows)==344
included=[(i+2,q) for i,q in enumerate(rows) if q['species']=='Adelie' and q['sex'] in ['female','male'] and q['flipper_length_mm'] not in ['NA','']];assert len(included)==146
out=P/'source/python-output';run=load(out/'run.json');assert run['actual_execution'] and run['script_sha256']==snapshot['program_sha256'] and run['input_sha256']==snapshot['data_sha256']
saved=list(csv.DictReader((out/'included_rows.csv').open(encoding='utf-8')))
assert [int(q['csv_line']) for q in saved]==[i for i,q in included]
assert [int(q['sex_code']) for q in saved]==[0 if q['sex']=='female' else 1 for i,q in included]
assert [float(q['flipper_mm']) for q in saved]==[float(q['flipper_length_mm']) for i,q in included]
summary=list(csv.DictReader((out/'summary.csv').open(encoding='utf-8')));means=[]
for code,sex in enumerate(['female','male']):
 values=[float(q['flipper_length_mm']) for i,q in included if q['sex']==sex];assert len(values)==73
 means.append(statistics.mean(values));got=summary[code];assert int(got['sex_code'])==code and int(got['n'])==73
 assert math.isclose(float(got['mean_mm']),means[-1],abs_tol=1e-10,rel_tol=0)
 assert math.isclose(float(got['sd_mm']),statistics.stdev(values),abs_tol=1e-10,rel_tol=0)
comp=list(csv.DictReader((out/'comparison.csv').open(encoding='utf-8')))[0];assert math.isclose(float(comp['male_minus_female_mm']),means[1]-means[0],abs_tol=1e-10,rel_tol=0)
console=load(P/'actual-console.json');assert console['actual_execution'] and console['analysis_rows']==146
assert all(not snapshot[k] for k in ['ownership_confirmed','registration_submitted','identified_human_contributors','count_as_registered_software_achievement','external_model_called'])
assert snapshot['registration_number'] is None and snapshot['certificate_file'] is None
with (P/'成果台账.csv').open(encoding='utf-8-sig',newline='') as f:assert list(csv.DictReader(f))==ledger
assert len(ledger)==3 and all(q['count_as_own_achievement']=='否' and q['contribution'] for q in ledger)
assert ledger[1]['category']=='外部论文参考' and '不是本课程论文成果' in ledger[1]['state']
assert ledger[2]['category']=='技术交底教学草稿' and '未作为专利申请或授权' in ledger[2]['state']
assert {q['category'] for q in requirements}>={'申请表','程序与文档鉴别材料','相关证明文件','本人贡献与成果关联','登记结果'}
assert not list(P.rglob('*证书*')),'No apparent registration certificate belongs in this unregistered teaching case'
report={'snapshot':snapshot['snapshot'],'actual_program_execution':True,'input_records':344,'included_records':146,'groups':2,'records_per_group':73,'included_row_ids_checked':146,'descriptive_statistics_independently_recomputed':True,'snapshot_file_hashes_verified':7,'ledger_rows':3,'counted_as_own_achievements':0,'ownership_confirmed':False,'human_contributors_confirmed':False,'registration_submitted':False,'registration_certificate_exists':False,'scope':'Local program execution, exact files, numerical outputs, editable ledger and explicit gaps. Does not establish ownership, personal contribution, eligibility, project acceptance or official registration.'}
(P/'checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n','utf-8');print(json.dumps(report,ensure_ascii=False,indent=2))
